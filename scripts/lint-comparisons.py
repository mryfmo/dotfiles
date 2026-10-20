#!/usr/bin/env python3
"""Refuse string-form comparisons of paths, URLs and processes (C-61 rule 6; plan 023 PR F2).
python3 -I scripts/lint-comparisons.py [--list-rules] [--baseline <tsv>] [<file>...] [--changed <path>... | --all] prints
each hit as `<file>:<line>: <rule id> <rule text>` and exits 1 when a hit outside the baseline, or a baseline row matching
no hit, is in a changed file (a normaliser in the statement, or `# lint-comparisons: allow <reason>` on the line,
accepts; paths as git ls-files prints). In an unchanged file both are warnings. The changed files are --changed's, else
`git diff --name-only --no-renames origin/main...HEAD`'s (a rename changes both paths); --all prints every hit and
stale row and exits 0. Shell is read only from shfmt's JSON AST (`-ln zsh` for zsh, else bash): a missing shfmt, a parse
failure or output that is no JSON refuses, and nothing stands in for the parser."""

import argparse
import ast
import functools
import hashlib
import io
import json
import os
import re
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
JQ_SKIP = {"--arg": 2, "--argjson": 2, "--slurpfile": 2, "--rawfile": 2, "--indent": 1, "-L": 1, "--library-path": 1}
SHFMT = (["shfmt"], ["mise", "x", "shfmt@3.14.1", "--", "shfmt"])  # PATH's, else .github/workflows/test.yaml's pin
PY_NORM = re.compile(
    r"^(os\.path\.(realpath|normpath|abspath)|(pathlib\.)?Path\(\)\.resolve|(urllib\.parse\.)?(urlsplit|urlparse|unquote)|canonical_path|normali[sz]e_\w+)$"
)
RE_FUNCS = ("re.compile", "re.search", "re.match", "re.fullmatch")
GIT_C = ("core.hooksPath=/dev/null", "core.fsmonitor=false", "protocol.allow=never", "protocol.https.allow=always")
GIT_C += ("core.attributesFile=/dev/null", "core.sshCommand=false")
OPS = (ast.Eq, ast.NotEq, ast.In, ast.NotIn)


@functools.cache
def shfmt():  # the first shfmt invocation that runs
    for cmd in SHFMT:
        try:
            run = subprocess.run([*cmd, "--version"], stdin=subprocess.DEVNULL, capture_output=True, check=False)
        except OSError:
            continue
        if run.returncode == 0:
            return cmd
    sys.exit("lint-comparisons: shfmt missing")


def blank(m):  # a chezmoi action is no shell: blanked to spaces, newlines and offsets kept; an include alone on its
    # line is the no-op `:`, since it expands to whole statements (a subshell of includes alone would be empty)
    head, tail = m.string[: m.start()].rpartition("\n")[2], m.string[m.end() :].partition("\n")[0]
    lone = not head.strip() and not tail.strip() and re.match(r"\{\{-?\s*(?:include|includeTemplate|template)\b", m[0])
    return (":" if lone else " ") + re.sub(r"[^\n]", " ", m[0][1:])


def shfmt_tree(rel, text):  # (AST, text as parsed): shfmt's JSON AST is the only shell reader, and it refuses
    zsh = rel.removesuffix(".tmpl").endswith(".zsh") or re.match(r"#!.*\bzsh\b", text)
    if rel.endswith(".tmpl"):
        text = re.sub(r"\{\{.*?\}\}", blank, text, flags=re.DOTALL)
    cmd = [*shfmt(), "-ln", "zsh" if zsh else "bash", "--tojson"]
    run = subprocess.run(cmd, input=text, capture_output=True, text=True, check=False)
    if run.returncode:
        sys.exit(f"lint-comparisons: {rel}: {run.stderr.strip()}")
    try:
        tree = json.loads(run.stdout)
    except (ValueError, RecursionError):
        tree = None
    if not isinstance(tree, dict) or tree.get("Type") != "File":  # JSON that is no shfmt file node is no AST either
        sys.exit(f"lint-comparisons: {rel}: shfmt gave no JSON AST")
    return tree, text


def nodes(n):  # every node at or below n, iteratively (a long && chain nests deep); heredoc bodies are data
    todo = [n]
    while todo:
        n = todo.pop()
        if isinstance(n, dict):
            yield n
            todo.extend(v for k, v in n.items() if k != "Hdoc")
        elif isinstance(n, list):
            todo.extend(n)


def stmts(tree):  # each statement with the outermost statement of its &&, || or | chain; heredoc bodies left out
    todo = [(tree, None)]
    while todo:
        n, top = todo.pop()
        if isinstance(n, list):
            todo.extend((x, top) for x in n)
        elif isinstance(n, dict):
            if "Cmd" in n:
                top = top or n
                yield n, top
            keep = ("X", "Y") if n.get("Type") == "BinaryCmd" else ("Cmd",)  # the chain goes on; elsewhere a new one
            todo.extend((v, top if k in keep else None) for k, v in n.items() if k != "Hdoc")


def flat(word):  # a word's parts with its double quotes opened: (part, quoted)
    for part in word.get("Parts") or []:
        yield from ((x, True) for x in part.get("Parts") or []) if part["Type"] == "DblQuoted" else [(part, False)]


def chars(part, quoted, raw=None):  # (character, source line) of a literal part after the shell's quote removal, an
    # extglob's pattern as written, nothing for an expansion; raw: a Lit's source, which keeps the backslash-newlines its
    # Value drops, so each character keeps its own source line
    kind, line, i = part["Type"], part["Pos"]["Line"], 0
    if kind not in ("Lit", "SglQuoted", "ExtGlob"):
        return
    dollar = kind == "SglQuoted" and part.get("Dollar")  # $'…' decodes its escapes, on the line they are written on
    if raw is None:  # shfmt omits an empty Value ('' or @())
        raw = (part.get("Pattern") or {}).get("Value", "") if kind == "ExtGlob" else part.get("Value", "")
    while i < len(raw):
        c, n = raw[i], raw[i + 1 : i + 2]
        if c == "\\" and not n and kind == "Lit":  # a backslash-newline split between two parts (the next has its line)
            break
        if c == "\\" and n and (dollar or kind == "Lit" and (not quoted or n in '\\"$`\n')):
            if not (kind == "Lit" and n == "\n"):  # bash deletes a backslash-newline
                yield ({"n": "\n", "t": "\t", "r": "\r"}.get(n, n) if dollar else n), line
            line, i = line + (n == "\n"), i + 2
            continue
        yield c, line
        line, i = line + (c == "\n"), i + 1


def static(word):  # the literal text of a word, its runtime expansions left out
    return "".join(c for part, quoted in flat(word) for c, _ in chars(part, quoted))


def expands(node):  # a parameter expansion below: a name, or a positional or special parameter ($1, ${10}, $@, $?)
    return any(n.get("Type") == "ParamExp" for n in nodes(node))


def operand(word):  # a path-named variable first (not its ${#length}), or a literal path piece beside any expansion
    first = next(flat(word), ({}, False))[0]
    name = first.get("Type") == "ParamExp" and not first.get("Length") and (first.get("Param") or {}).get("Value")
    return bool(name and TOKEN.search(name) or LITERAL.search(static(word)))


def program(word, src):  # the jq program one shell word hands over, its fragments in order: (text, line per character)
    pairs = []  # shortcut: an expansion is runtime text and is left out; scan it if one hides a hit
    for part, quoted in flat(word):
        pairs += chars(part, quoted, src(part) if part["Type"] == "Lit" else None)
    return "".join(c for c, _ in pairs), [n for _, n in pairs]


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
            step = len(two) if c == "\\" else 1  # an escape is two characters
            code[i : i + step], lits[i : i + step] = [" "] * step, prog[i : i + step]
            ctx.pop() if c == '"' else None
            i += step
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


def shell_hits(rel, text):  # (hits, comments): the shell rules on shfmt's AST; a marker counts only in a comment node
    tree, text = shfmt_tree(rel, text)
    data, hits = text.encode(), []
    comments = [c for c in nodes(tree) if "Hash" in c and "Text" in c]
    note = {c["Hash"]["Line"]: "#" + c["Text"] for c in comments}
    code = bytearray(data)  # the source with its comments blanked: a normaliser counts in code only
    for c in comments:
        code[c["Pos"]["Offset"] : c["End"]["Offset"]] = b" " * (c["End"]["Offset"] - c["Pos"]["Offset"])
    code = code.decode(errors="replace").split("\n")

    def src(n):
        return data[n["Pos"]["Offset"] : n["End"]["Offset"]].decode(errors="replace")

    def accepted(lo, hi, norm=None):  # a normaliser in the code of lines lo..hi, or a marker with its reason there
        if norm and re.search(norm, "\n".join(code[lo - 1 : hi])):
            return True
        return any((m := MARKER.search(note.get(k, ""))) and m.group(1) for k in range(lo, hi + 1))

    for stmt, top in stmts(tree):  # a statement's lines are its whole chain's, continued lines included
        cmd, lo, hi = stmt["Cmd"], top["Pos"]["Line"], top["End"]["Line"]
        if not isinstance(cmd, dict):
            continue
        t, args = cmd.get("Type"), cmd.get("Args") or []
        words, at = [static(a) for a in args], cmd["Pos"]["Line"]
        tests = [n for n in nodes(cmd) if n.get("Type") == "BinaryTest" and n["Op"] in ("==", "!=", "=")]
        if t == "TestClause" and any(operand(n["X"]) or operand(n["Y"]) for n in tests):
            hits.append((at, "R1", accepted(lo, hi, SH_NORM)))
        if t == "CallExpr" and words[:1] in (["["], ["test"]):
            pairs = [(args[i - 1], args[i + 1]) for i in range(2, len(args) - 1) if words[i] in ("==", "!=", "=")]
            if any(operand(x) or operand(y) for x, y in pairs):
                hits.append((at, "R1", accepted(lo, hi, SH_NORM)))
        if t == "CaseClause" and operand(cmd["Word"]):  # for this, the statement ends at its `in`
            hits.append((at, "R2", accepted(lo, cmd.get("In", cmd["Word"]["End"])["Line"], SH_NORM)))
        if t == "BinaryCmd" and cmd["Op"] == "|":  # ps piped to a text reader, unless ps -o <fields>= -p
            ps, reader = ([static(a) for a in (x.get("Cmd") or {}).get("Args") or []] for x in (cmd["X"], cmd["Y"]))
            fields = ps[1:2] == ["-o"] and ps[2:3] and ps[2].endswith("=") and ps[3:4] == ["-p"]
            if ps[:1] == ["ps"] and not fields and reader[:1] in (["grep"], ["awk"], ["cut"], ["sed"]):
                hits.append((at, "R5", accepted(lo, hi)))
        tool = next((i for i, w in enumerate(words) if os.path.basename(w) in ("pgrep", "grep", "egrep")), None)
        if t == "CallExpr" and tool is not None:  # also git grep, command grep, xargs grep
            name, k = os.path.basename(words[tool]), tool + 1
            while k < len(args) and words[k].startswith("-"):
                k += 1
            flags, pattern = words[tool + 1 : k], args[k] if k < len(args) else {}
            if name == "pgrep" and any(re.fullmatch(r"-\w*f\w*", f) for f in flags) and expands(pattern):
                hits.append((at, "R5", accepted(lo, hi)))
            ere = name == "egrep" or any(re.match(r"-\w*E|--extended-regexp", f) for f in flags)
            if name != "pgrep" and ere and "-F" not in flags and expands(pattern):
                hits.append((at, "R6", accepted(lo, hi, "escape_regex")))
        jq = next((i for i, a in enumerate(args) if re.search(r"\bjq\b", src(a))), None)
        if t == "CallExpr" and jq is not None:  # also "$jq" and "$(command -v jq)"
            i = jq + 1  # the program: past the options and their operands (jq 1.8 --help) and pure expansions
            while i < len(args) and words[i] not in ("-f", "--from-file"):
                if words[i].startswith("-") or not words[i] and expands(args[i]):
                    i += 1 + JQ_SKIP.get(words[i], 0)
                    continue
                prog, lines = program(args[i], src)
                hits.extend((lines[p], "R3", ok or accepted(lo, hi)) for p, ok in jq_hits(prog))
                break
    return hits, note


def jq_hits(prog):  # (offset, accepted) per string-form comparison in one whole jq program
    bare, lits = jq_mask(prog)  # strings and comments hold no operator and apply no normaliser
    view = bare  # the program's code alone, before its keywords become bounds
    bare = re.sub(r"(?<![\w.$])(?:and|or|then|elif|else)(?!\w)", lambda m: ";" * len(m[0]), bare)  # bounds
    bare = re.sub(r"(?<![\w.$])if(?!\w)", "( ", re.sub(r"(?<![\w.$])end(?!\w)", "  )", bare))  # one operand
    for op in JQ_OP.finditer(bare):
        lo, hi = span(bare, op.start(), op.group(0).endswith("("))
        expr, sides = bare[lo:hi], (bare[lo : op.start()], bare[op.start() : hi])
        hit = re.search(r"\.(url|path)\b", expr) or any(map(TOKEN.search, re.findall(r"\$(\w+)", expr)))
        if hit or LITERAL.search(lits[lo:hi]):
            ok = any(all(d in re.findall(r"(?<![\w.$])\w+", s) for s in sides) for d in JQ_DEF.findall(bare))
            row, end = prog.rfind("\n", 0, op.start()) + 1, (prog.find("\n", op.start()) + 1 or len(prog) + 1) - 1
            sharp = [i for i in range(row, end) if prog[i] == "#" and view[i] == lits[i] == " "]  # a jq comment
            mark = MARKER.search(prog[sharp[0] : end]) if sharp else None
            yield op.start(), ok or bool(mark and mark.group(1))


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
        joined = name.endswith(".join") and len(node.args) == 1 and isinstance(node.func.value, ast.Constant)
        arg = node.args[0] if joined else None  # a constant separator: an escaped one would be its own call
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
        if rel.removesuffix(".tmpl").endswith((".sh", ".bash", ".zsh", ".py")) or SHEBANG.match(first):
            yield rel, ROOT / rel


def notes(text):  # each line's Python comment token, where alone the allow marker counts
    try:
        toks = tokenize.generate_tokens(io.StringIO(text).readline)
        return {t.start[0]: t.string for t in toks if t.type == tokenize.COMMENT}
    except (tokenize.TokenError, SyntaxError):
        return {}


def lint(rel, text):
    lines = text.split("\n")
    py = rel.removesuffix(".tmpl").endswith(".py") or re.match(r"#!.*python", lines[0])
    hits, note = (python_hits(text), notes(text)) if py else shell_hits(rel, text)
    for n, rule, accepted in hits:
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
