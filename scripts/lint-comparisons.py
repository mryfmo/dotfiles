#!/usr/bin/env python3
"""Refuse string-form comparisons of paths, URLs and processes (C-61 rule 6; plan 023 PR F2).
python3 -I scripts/lint-comparisons.py [--list-rules] [--baseline <tsv>] [<file>...] [--changed <path>... | --all] prints
each hit as `<file>:<line>: <rule id> <rule text>` and exits 1 when a hit outside the baseline, or a baseline row matching
no hit, is in a changed file (a normaliser in the statement, or `# lint-comparisons: allow <reason>` on the line,
accepts; paths as git ls-files prints). In an unchanged file both are warnings. The changed files are --changed's, else
`git diff --name-only --no-renames origin/main...HEAD`'s (a rename changes both paths); --all prints every hit and
stale row and exits 0."""

import argparse
import ast
import hashlib
import io
import os
import re
import shlex
import shutil
import subprocess
import sys
import tokenize
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RULES = {
    "R0": "the allow marker carries no reason",
    "R1": "shell [[ ]] or [ ] compares a path or URL operand by its string form",
    "R2": "shell case matches a path or URL operand by its string form",
    "R3": "jq compares a URL or path by its string form",
    "R4": "Python compares a path or URL by its string form",
    "R5": "a process is read as text (ps piped to grep, awk, cut or sed; pgrep -f on a variable)",
    "R6": "an identifier is interpolated into a regex (grep -E on $name; re.* on an f-string)",
}
LIMIT = "shortcut: the lint is statement-local, so a variable normalised on an earlier line and compared later is a hit (mark it with the marker and its reason); upgrade to a cross-line data-flow when a second such marker is needed"
TOKEN = re.compile(
    r"(?:^|[_.\-]|(?<=[a-z0-9])(?=[A-Z]))(?i:(?:path|url|cwd|dir|root|file|home|pid|proc)s?)(?:$|[_.\-]|(?<=[a-z])(?=[A-Z]))"
)
LITERAL = re.compile(r"/|~|file://|\.html|%2F")
MARKER = re.compile(r"#\s*lint-comparisons:\s*allow\b[ \t]*(\S*)")
SHEBANG = re.compile(r"^#!.*\b(sh|bash|zsh|python\d*)\b")
SH_NORM = re.compile(
    r"\brealpath\b|\bpwd -P\b|\bcd -P\b|\breadlink -f\b|\bcanonical_path\b|\bnormali[sz]e_\w+|python3 -I -c .*(os\.path\.(realpath|normpath)|urllib\.parse)"
)
JQ_DEF = re.compile(r"\bdef (canonical_path|normali[sz]e_\w+)\b")
JQ_OP = re.compile(r"==|!=|\b(?:startswith|endswith|ltrimstr|rtrimstr|test)\(")
JQ_QUOTE = re.compile(
    r"""(?:\\[\s\S]|"\$(?:[^"\\\n]|\\[\s\S])*"|"(?!(?:[^"\\\n]|\\[\s\S])*")|[^'"\\\n])*+('[^']*'|"(?:[^"\\\n]|\\[\s\S])*")"""
)  # the first quoted word on the jq word's line that is no "$expansion": a '…' or a "…" program
JQ_ARG = re.compile(r"(?<!\S)(?:--(?:arg|argjson|slurpfile|rawfile)(?:[\s\\]+\S+)?|--indent|-L|--library-path)[\s\\]+$")
PS = re.compile(
    r"(?:^|[|;&(!]|\$\(|\b(?:if|elif|while|until|then|do|else)\b)\s*ps\s(?!-o\s+\S+=\s+-p\s)[^|]*\|\s*(?:grep|awk|cut|sed)\b"
)
PGREP = re.compile(r"""\bpgrep\s+-\w*f\w*(\s+-\S+)*\s+("[^"]*\$|[^\s'"]*\$)""")  # the whole pattern, quoted or not
GREP = re.compile(r"\b(e?grep)((?:\s+-\S+)*)\s+(\"[^\"]*\"|'[^']*'|\S+)")
PY_NORM = re.compile(
    r"^(os\.path\.(realpath|normpath|abspath)|(pathlib\.)?Path\(\)\.resolve|(urllib\.parse\.)?(urlsplit|urlparse|unquote)|canonical_path|normali[sz]e_\w+)$"
)
RE_FUNCS = ("re.compile", "re.search", "re.match", "re.fullmatch")
GIT_C = ("core.hooksPath=/dev/null", "core.fsmonitor=false", "protocol.allow=never", "protocol.https.allow=always")
GIT_C += ("core.attributesFile=/dev/null", "core.sshCommand=false")
OPS = (ast.Eq, ast.NotEq, ast.In, ast.NotIn)


def operand(tok):  # a path-named variable, or a literal path piece beside any expansion
    name = re.match(r"\$\{?([A-Za-z_]\w*)", tok)
    return bool(name and TOKEN.search(name.group(1))) or bool(LITERAL.search(re.sub(r"\$\{[^}]*\}|\$\w+", "", tok)))


def comment(line):  # a shell line's comment: from the first unquoted # that starts a word, else ""
    q, i = "", 0
    while i < len(line):
        if line[i] == "\\" and q != "'":
            i += 2
            continue
        if q:
            q = "" if line[i] == q else q
        elif line[i] in "'\"":
            q = line[i]
        elif line[i] == "#" and (i == 0 or line[i - 1] in " \t;|&("):
            return line[i:]
        i += 1
    return ""


def words(line):
    while (folded := re.sub(r"\$\([^()]*\)", "", line)) != line:
        line = folded
    try:
        return shlex.split(line)
    except ValueError:
        return line.split()


def programs(code):
    for m in re.finditer(r"\bjq\b[\"})]*", code):  # also "$jq", "${jq}" and "$(command -v jq)"
        rest = code[m.end() :]
        while (folded := re.sub(r"\$\([^()]*\)", lambda f: "$" + "_" * (len(f[0]) - 1), rest)) != rest:
            rest = folded  # an argument's command substitution is one "$…" word: its inner quotes fold, same length
        q = JQ_QUOTE.match(rest)  # the program, after the options and their arguments (jq 1.8 --help)
        while q and JQ_ARG.search(rest, 0, q.start(1)):
            q = JQ_QUOTE.match(rest, q.end())
        if q:  # the program's text, a double-quoted one as the shell hands it to jq
            begin, inner = m.end() + q.start(1) + 1, q[1][1:-1]
            yield begin, re.sub(r'\\([\\"$`])', r"\1", inner) if q[1][0] == '"' else inner


def jq_mask(prog):  # (code, literals): prog with its strings and comments blanked, and with all but string characters
    code, lits, ctx, i = list(prog), [" "] * len(prog), [0], 0  # ctx: None in a string, else a parenthesis depth
    while i < len(prog):
        c, two = prog[i], prog[i : i + 2]
        if ctx[-1] is None:  # in a string: "\(" opens an interpolation, which is code until its ")"
            code[i] = " "
            if two == "\\(":
                code[i + 1], i = " ", i + 2
                ctx.append(0)
                continue
            lits[i : i + len(two)] = two if c == "\\" else c
            ctx.pop() if c == '"' else None
            i += len(two) if c == "\\" else 1
            continue
        if c == "#":  # a comment, to the end of its line
            end = prog.find("\n", i) % (len(prog) + 1) or len(prog)
            code[i:end], i = [" "] * (end - i), end
            continue
        if c == '"':
            code[i] = " "
            ctx.append(None)
        elif c in "([{":
            ctx[-1] += 1
        elif c in ")]}" and ctx[-1] == 0 and len(ctx) > 1:  # an interpolation closes: back in its string
            code[i] = " "
            ctx.pop()
        elif c in ")]}" and ctx[-1]:
            ctx[-1] -= 1
        i += 1
    return "".join(code), "".join(lits)


def span(prog, p, fn):
    stop, lo, hi, d = (",;" if fn else ",;|"), p, p, 0
    while lo > 0 and not (d == 0 and prog[lo - 1] in stop + "([{"):
        lo -= 1
        d += (prog[lo] in ")]}") - (prog[lo] in "([{")
    d = 0
    while hi < len(prog) and not (d == 0 and prog[hi] in stop + ")]}"):
        d += (prog[hi] in "([{") - (prog[hi] in ")]}")
        hi += 1
    return lo, hi


def shell_hits(text):
    lines, buf, at = text.split("\n"), "", 0
    for n, raw in enumerate(lines, 1):
        code, at = raw[: len(raw) - len(comment(raw))], at if buf else n
        if code.endswith("\\"):  # a continuation: the statement goes on, reported at its first line
            buf += code[:-1] + " "
            continue
        line, buf, n = buf + code, "", at
        toks = words(line)
        for i, tok in enumerate(toks):
            test = tok in ("==", "!=", "=") and 0 < i < len(toks) - 1 and ("[[" in toks[:i] or "[" in toks[:i])
            if test and (operand(toks[i - 1]) or operand(toks[i + 1])):
                yield n, "R1", SH_NORM.search(line)
            if tok == "in" and i > 1 and toks[i - 2] == "case" and operand(toks[i - 1]):
                yield n, "R2", SH_NORM.search(line)
        if PS.search(line) or PGREP.search(line):
            yield n, "R5", False
        for cmd, flags, pattern in GREP.findall(line):
            ere = cmd == "egrep" or re.search(r"\s-\w*E|--extended-regexp", flags)
            # a '…' pattern, or an escaped \$, interpolates nothing
            interpolated = pattern[:1] != "'" and re.search(r"(?<!\\)\$\{?[A-Za-z_]", pattern)
            if ere and interpolated and "-F" not in flags.split():
                yield n, "R6", "escape_regex" in line
    code = "\n".join("" if line.lstrip().startswith("#") else line for line in lines)
    for begin, region in programs(code):
        prog, first = region, code.count("\n", 0, begin) + 1
        bare, lits = jq_mask(prog)  # strings and comments hold no operator and apply no normaliser
        keyword = r"(?<![\w.$])(?:and|or|if|then|elif|else|end)(?!\w)"  # each bounds an operand, as a ; does
        bare = re.sub(keyword, lambda m: ";" * len(m[0]), bare)
        for op in JQ_OP.finditer(bare):
            lo, hi = span(bare, op.start(), op.group(0).endswith("("))
            expr, sides = bare[lo:hi], (bare[lo : op.start()], bare[op.start() : hi])
            hit = re.search(r"\.(url|path)\b", expr) or any(map(TOKEN.search, re.findall(r"\$(\w+)", expr)))
            if hit or LITERAL.search(lits[lo:hi]):
                ok = any(all(d in re.findall(r"(?<![\w.$])\w+", s) for s in sides) for d in JQ_DEF.findall(bare))
                yield first + prog.count("\n", 0, op.start()), "R3", ok or MARKER.search(comment(lines[first - 1]))


def python_hits(text):
    def dotted(node):
        if isinstance(node, ast.Attribute):
            return dotted(node.value) + "." + node.attr
        return dotted(node.func) + "()" if isinstance(node, ast.Call) else getattr(node, "id", "?")

    def py_operand(node):
        if isinstance(node, ast.Constant):
            return isinstance(node.value, str) and bool(LITERAL.search(node.value))
        return bool(TOKEN.search(node.attr if isinstance(node, ast.Attribute) else getattr(node, "id", "")))

    def py_calls(nodes, accept):
        return any(accept(dotted(c.func)) for n in nodes for c in ast.walk(n) if isinstance(c, ast.Call))

    def escaped(node):  # a formatted value whose every fragment is re.escape's: a call, a join of escapes, a constant
        name = dotted(node.func) if isinstance(node, ast.Call) else ""
        if name == "re.escape" or isinstance(node, ast.Constant):
            return True
        arg = node.args[0] if name.endswith(".join") and len(node.args) == 1 else None
        if isinstance(arg, ast.Call) and dotted(arg.func) == "map" and arg.args:
            return dotted(arg.args[0]) == "re.escape"
        return isinstance(arg, (ast.GeneratorExp, ast.ListComp)) and escaped(arg.elt)

    try:
        tree = ast.parse(text)
    except SyntaxError:
        return
    for node in ast.walk(tree):
        call = isinstance(node, ast.Call)
        if isinstance(node, ast.Compare) and any(isinstance(o, OPS) for o in node.ops):
            parts = [node.left, *node.comparators]
        elif call and isinstance(node.func, ast.Attribute) and node.func.attr in ("startswith", "endswith"):
            parts = [node.func.value, *node.args]
        elif call and dotted(node.func) in RE_FUNCS and node.args and isinstance(node.args[0], ast.JoinedStr):
            values = [v.value for v in node.args[0].values if isinstance(v, ast.FormattedValue)]
            yield node.lineno, "R6", bool(values) and all(map(escaped, values))
            continue
        else:
            continue
        if any(py_operand(p) for p in parts):
            yield node.lineno, "R4", py_calls(parts, PY_NORM.match)


def git(*args):  # plan 024 5.14 item 2: env -i, a system git by its absolute path, -C, no system or global config
    exe = shutil.which("git", path=os.defpath) or sys.exit(f"lint-comparisons: no git in {os.defpath}")
    cmd = [os.path.realpath(exe), "-C", str(ROOT), *(x for c in GIT_C for x in ("-c", c)), *args]  # not PATH's git
    env = {"GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": "/dev/null"}
    return filter(None, subprocess.run(cmd, env=env, capture_output=True, text=True, check=True).stdout.split("\0"))


def default_files():
    for rel in git("ls-files", "-z", "--", "home", "scripts", "install"):
        first = (ROOT / rel).read_text(errors="replace").split("\n", 1)[0]
        if rel.endswith((".sh", ".bash", ".zsh", ".py", ".tmpl")) or SHEBANG.match(first):
            yield rel, ROOT / rel


def notes(text, py):  # each line's comment, where alone the allow marker counts (Python: its comment tokens)
    if not py:
        return {n: comment(raw) for n, raw in enumerate(text.split("\n"), 1)}
    try:
        toks = tokenize.generate_tokens(io.StringIO(text).readline)
        return {t.start[0]: t.string for t in toks if t.type == tokenize.COMMENT}
    except (tokenize.TokenError, SyntaxError):
        return {}


def lint(rel, text):
    lines = text.split("\n")
    py = rel.removesuffix(".tmpl").endswith(".py") or re.match(r"#!.*python", lines[0])
    note = notes(text, py)
    for n, rule, accepted in python_hits(text) if py else shell_hits(text):
        mark = MARKER.search(note.get(n, ""))
        if not accepted and not (mark and mark.group(1)):
            yield n, "R0" if mark else rule
    yield from ((n, "R0") for n, c in note.items() if (m := MARKER.search(c)) and not m.group(1))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--list-rules", action="store_true")
    parser.add_argument("--baseline", type=Path, default=ROOT / "scripts/lint-comparisons-baseline.tsv")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--changed", nargs="*", metavar="PATH")
    mode.add_argument("--all", action="store_true")
    parser.add_argument("files", nargs="*")
    args = parser.parse_args(argv)
    if args.list_rules:
        print("\n".join(f"{rule} {text}" for rule, text in RULES.items()), LIMIT, sep="\n")
        return 0
    rows = args.baseline.read_text().splitlines() if args.baseline.is_file() else []
    rows = Counter(tuple((r.split("\t") + ["", ""])[:3]) for r in rows if r.strip())
    diff = ("diff", "--name-only", "--no-renames", "-z", "--no-ext-diff", "--no-textconv", "origin/main...HEAD")
    changed = None if args.all else set(git(*diff) if args.changed is None else args.changed)
    used, scanned, failed, warned = Counter(), set(), False, Counter()

    def report(rel, line, kind):  # a changed file's finding fails; an unchanged file's warns; --all prints both
        nonlocal failed
        failed |= changed is not None and rel in changed
        warned[kind] += changed is not None and rel not in changed
        print(f"warning: {line}" if changed is not None and rel not in changed else line)

    for rel, target in sorted([(f, Path(f)) for f in args.files] or default_files()):
        text, _ = target.read_text(errors="replace"), scanned.add(rel)
        for n, rule in sorted(set(lint(rel, text))):
            key = (rel, rule, hashlib.sha256(text.split("\n")[n - 1].strip().encode()).hexdigest())
            if used[key] < rows[key]:
                used[key] += 1
                if changed is None:
                    print(f"{rel}:{n}: {rule} {RULES[rule]} (baseline)")
                continue
            report(rel, f"{rel}:{n}: {rule} {RULES[rule]}", "hit")
    for rel, rule, _ in sorted(r for r in (rows - used).elements() if not args.files or r[0] in scanned):
        report(rel, f"stale baseline row {rel} {rule}", "row")
    if sum(warned.values()):
        print(f"warning: {warned['hit']} unbaselined hit(s) and {warned['row']} stale row(s) in unchanged files")
    return int(failed)


if __name__ == "__main__":
    raise SystemExit(main())
