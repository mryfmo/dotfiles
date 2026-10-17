#!/usr/bin/env python3
"""Refuse string-form comparisons of paths, URLs and processes (C-61 rule 6; plan 023 PR F2).
python3 -I scripts/lint-comparisons.py [--list-rules] [--baseline <tsv>] [<file>...] prints each hit as `<file>:<line>:
<rule id> <rule text>` and exits 1 when a hit is outside the baseline or a baseline row matches no hit (a normaliser in
the statement, or `# lint-comparisons: allow <reason>` on the line, accepts; repo-relative paths as git ls-files prints).
"""

import argparse
import ast
import hashlib
import re
import shlex
import subprocess
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
PS = re.compile(
    r"(?:^|[|;&(!]|\$\(|\b(?:if|elif|while|until|then|do|else)\b)\s*ps\s(?!-o\s+\S+=\s+-p\s)[^|]*\|\s*(?:grep|awk|cut|sed)\b"
)
PGREP = re.compile(r"\bpgrep\s+-\w*f\w*(\s+-\S+)*\s+\S*\$")
GREP = re.compile(r"\b(e?grep)((?:\s+-\S+)*)\s+(\"[^\"]*\"|'[^']*'|\S+)")
PY_NORM = re.compile(r"^(realpath|normpath|abspath|resolve|urlsplit|urlparse|unquote|canonical_path|normali[sz]e_\w+)$")


def operand(tok):
    name = re.match(r"\$\{?([A-Za-z_]\w*)", tok)
    if name:
        return bool(TOKEN.search(name.group(1)))
    return bool(LITERAL.search(re.sub(r"\$\{[^}]*\}|\$\w+", "", tok)))


def words(line):
    while (folded := re.sub(r"\$\([^()]*\)", "", line)) != line:
        line = folded
    try:
        return shlex.split(line)
    except ValueError:
        return line.split()


def programs(code):
    for m in re.finditer(r"\bjq\b", code):
        start = m.end() + re.match(r"(?:\\\n|[^'\n])*", code[m.end() :]).end()
        end = code.find("'", start + 1)
        if start < len(code) and code[start] == "'" and end > 0:
            yield start, code[start : end + 1]


def span(prog, p, fn):
    stop, lo, hi, d = (",;" if fn else ",;|"), p, p, 0
    while lo > 0 and not (d == 0 and prog[lo - 1] in stop + "([{"):
        lo -= 1
        d += (prog[lo] in ")]}") - (prog[lo] in "([{")
    d = 0
    while hi < len(prog) and not (d == 0 and prog[hi] in stop + ")]}"):
        d += (prog[hi] in "([{") - (prog[hi] in ")]}")
        hi += 1
    return prog[lo:hi]


def shell_hits(text):
    lines = text.split("\n")
    for n, raw in enumerate(lines, 1):
        line = "" if raw.lstrip().startswith("#") else re.split(r"\s#", raw, maxsplit=1)[0]
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
            if ere and re.search(r"\$\{?[A-Za-z_]", pattern) and "-F" not in flags.split():
                yield n, "R6", "escape_regex" in line
    code = "\n".join("" if line.lstrip().startswith("#") else line for line in lines)
    for begin, region in programs(code):
        prog, first = re.sub(r"\\\([^)]*\)", "", region), code.count("\n", 0, begin) + 1
        for op in JQ_OP.finditer(prog):
            expr = span(prog, op.start(), op.group(0).endswith("("))
            hit = re.search(r"\.(url|path)\b", expr) or any(map(TOKEN.search, re.findall(r"\$(\w+)", expr)))
            if hit or any(map(LITERAL.search, re.findall(r'"([^"]*)"', expr))):
                ok = any(expr.count(d) > 1 for d in JQ_DEF.findall(prog)) or MARKER.search(lines[first - 1])
                yield first + prog.count("\n", 0, op.start()), "R3", ok


def python_hits(text):
    def py_name(node):
        return node.attr if isinstance(node, ast.Attribute) else getattr(node, "id", "")

    def py_operand(node):
        if isinstance(node, ast.Constant):
            return isinstance(node.value, str) and bool(LITERAL.search(node.value))
        return bool(TOKEN.search(py_name(node)))

    def py_calls(nodes, accept):
        return any(accept(py_name(c.func)) for n in nodes for c in ast.walk(n) if isinstance(c, ast.Call))

    try:
        tree = ast.parse(text)
    except SyntaxError:
        return
    for node in ast.walk(tree):
        call = isinstance(node, ast.Call)
        if isinstance(node, ast.Compare) and any(
            isinstance(o, (ast.Eq, ast.NotEq, ast.In, ast.NotIn)) for o in node.ops
        ):
            parts = [node.left, *node.comparators]
        elif call and isinstance(node.func, ast.Attribute) and node.func.attr in ("startswith", "endswith"):
            parts = [node.func.value, *node.args]
        elif (
            call
            and py_name(node.func) in ("compile", "search", "match", "fullmatch")
            and node.args
            and isinstance(node.args[0], ast.JoinedStr)
        ):
            values = [v.value for v in node.args[0].values if isinstance(v, ast.FormattedValue)]
            yield node.lineno, "R6", py_calls(values, lambda name: name == "escape")
            continue
        else:
            continue
        if any(py_operand(p) for p in parts):
            yield node.lineno, "R4", py_calls(parts, PY_NORM.match)


def default_files():
    cmd = ["git", "ls-files", "-z", "--", "home", "scripts", "install"]
    out = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, check=True).stdout
    for rel in filter(None, out.split("\0")):
        first = (ROOT / rel).read_text(errors="replace").split("\n", 1)[0]
        if rel.endswith((".sh", ".bash", ".zsh", ".py", ".tmpl")) or SHEBANG.match(first):
            yield rel, ROOT / rel


def lint(rel, text):
    lines = text.split("\n")
    py = rel.removesuffix(".tmpl").endswith(".py") or re.match(r"#!.*python", lines[0])
    for n, rule, accepted in python_hits(text) if py else shell_hits(text):
        mark = MARKER.search(lines[n - 1])
        if not accepted and not (mark and mark.group(1)):
            yield n, "R0" if mark else rule
    yield from ((n, "R0") for n, raw in enumerate(lines, 1) if (m := MARKER.search(raw)) and not m.group(1))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--list-rules", action="store_true")
    parser.add_argument("--baseline", type=Path, default=ROOT / "scripts/lint-comparisons-baseline.tsv")
    parser.add_argument("files", nargs="*")
    args = parser.parse_args(argv)
    if args.list_rules:
        print("\n".join(f"{rule} {text}" for rule, text in RULES.items()), LIMIT, sep="\n")
        return 0
    rows = args.baseline.read_text().splitlines() if args.baseline.is_file() else []
    rows, used, scanned, failed = (
        {tuple((r.split("\t") + ["", ""])[:3]) for r in rows if r.strip()},
        set(),
        set(),
        False,
    )
    for rel, target in sorted([(f, Path(f)) for f in args.files] or default_files()):
        text, _ = target.read_text(errors="replace"), scanned.add(rel)
        for n, rule in sorted(set(lint(rel, text))):
            key = (rel, rule, hashlib.sha256(text.split("\n")[n - 1].strip().encode()).hexdigest())
            if key in rows:
                used.add(key)
                continue
            print(f"{rel}:{n}: {rule} {RULES[rule]}")
            failed = True
    for rel, rule, _ in sorted(r for r in rows - used if not args.files or r[0] in scanned):
        print(f"stale baseline row {rel} {rule}")
        failed = True
    return int(failed)


if __name__ == "__main__":
    raise SystemExit(main())
