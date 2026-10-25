#!/usr/bin/env python3
"""Refuse string-form comparisons of paths, URLs and processes (C-61 rule 6; plan 023 PR F2).
python3 -I scripts/lint-comparisons.py [--list-rules] [--baseline <tsv>] [<file>...] [--changed <path>... | --all] prints
each hit as `<file>:<line>: <rule id> <rule text>` and exits 1 when a hit outside the baseline, or a baseline row matching
no hit, is in a changed file (a normaliser in the statement, or `# lint-comparisons: allow <reason>` on the line,
accepts; paths as git ls-files prints). In an unchanged file both are warnings. The changed files are --changed's, else
`git diff --name-only --no-renames origin/main...HEAD`'s (a rename changes both paths); --all prints every hit and
stale row and exits 0. Shell is read only from shfmt's JSON AST (`-ln zsh` for zsh, else bash): a missing shfmt, a parse
failure or output that is no JSON refuses, and nothing stands in for the parser. A command is read at command position,
after its leading assignments and the known WRAPPERS (their options, option values, `--` and operands): an unknown
wrapper hides the command after it, accepted for precision, so a data argument (`printf '%s' jq "…"`) is never read as
a command. A shell's -c string and eval's arguments are shell code: they are parsed again, every rule reads them, and
their hits are reported on the outer lines; an expansion the outer shell performs is an unknown value there, whatever
quoting the nested text puts around it. Options and command names are read from a word's literal text after the
shell joins its fragments (`''-i` is `-i`)."""

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
JQ_NORM = re.compile(r"canonical_path|normali[sz]e_\w+")
JQ_FN = ("startswith", "endswith", "ltrimstr", "rtrimstr", "test")
JQ_LEX = re.compile(
    r"\s+|#[^\n]*|\.[A-Za-z_]\w*|\$[A-Za-z_]\w*|[A-Za-z_]\w*|==|!=|[<>]=|//=?|\|=|\?//|[-+*/%]=|.", re.DOTALL
)
ANSI = {"a": "\a", "b": "\b", "e": "\x1b", "E": "\x1b", "f": "\f", "n": "\n", "r": "\r", "t": "\t", "v": "\v"}
ANSI_ESC = re.compile(
    r"\\(?:([0-7]{1,3})|x([0-9A-Fa-f]{1,2})|u([0-9A-Fa-f]{1,4})|U([0-9A-Fa-f]{1,8})|c(.)|(.))", re.DOTALL
)
JQ_SKIP = {"--arg": 2, "--argjson": 2, "--slurpfile": 2, "--rawfile": 2, "--indent": 1, "-L": 1, "--library-path": 1}
# commands that run the rest of their words as a command, each with its options that take the next word as a value
WRAPPERS = {
    "command": set(),
    "builtin": set(),
    "exec": {"-a"},
    "env": {"-u", "-C", "-P", "-S", "--unset", "--chdir", "--split-string"},
    "nice": {"-n", "--adjustment"},
    "nohup": set(),
    "timeout": {"-s", "-k", "--signal", "--kill-after"},
    "stdbuf": {"-i", "-o", "-e", "--input", "--output", "--error"},
    "time": {"-f", "-o", "--format", "--output"},
    "sudo": {"-u", "-g", "-h", "-p", "-r", "-t", "-C", "-D", "-T", "-U", "--user", "--group", "--host", "--prompt"},
    "xargs": {"-I", "-a", "-d", "-E", "-L", "-n", "-P", "-s", "--arg-file", "--delimiter", "--max-args"},
}
# a wrapper's positional operand before the command: env's and sudo's NAME=value, timeout's duration
WRAPPER_OPERAND = re.compile(r"[A-Za-z_]\w*=.*|\d+(\.\d+)?[smhd]?", re.DOTALL)
JQ_NAME = re.compile(r"jq([-._][A-Za-z0-9._-]*)?(\.exe)?")  # jq, jq-1.7, jq-linux64, jq.exe
GREPS = ("pgrep", "grep", "egrep")
SHELLS = ("bash", "sh", "zsh", "dash", "ksh", "mksh")
NORM = {"R1": SH_NORM, "R2": SH_NORM, "R6": "escape_regex"}  # the normaliser that accepts a rule's hit, if any
LITS = ("Lit", "SglQuoted", "ExtGlob")  # the word parts that are literal text
OUTER = re.compile(r"lintcmpX(\w*?)Xpmctnil")  # spelled()'s token: an outer expansion inside a nested string
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


def shfmt_tree(rel, text, zsh=None, label=None):  # (AST, text as parsed): shfmt's JSON AST is the only shell reader,
    # and it refuses; zsh set: a nested string (-c, eval) in that dialect, already free of chezmoi actions
    if zsh is None:
        zsh = rel.removesuffix(".tmpl").endswith(".zsh") or re.match(r"#!.*\bzsh\b", text)
        if rel.endswith(".tmpl"):
            text = re.sub(r"\{\{.*?\}\}", blank, text, flags=re.DOTALL)
    cmd = [*shfmt(), "-ln", "zsh" if zsh else "bash", "--tojson"]
    run = subprocess.run(cmd, input=text, capture_output=True, text=True, check=False)
    if run.returncode:
        sys.exit(f"lint-comparisons: {label or rel}: {run.stderr.strip()}")
    try:
        tree = json.loads(run.stdout)
    except (ValueError, RecursionError):
        tree = None
    if not isinstance(tree, dict) or tree.get("Type") != "File":  # JSON that is no shfmt file node is no AST either
        sys.exit(f"lint-comparisons: {label or rel}: shfmt gave no JSON AST")
    return tree, text


def nodes(n):  # every node at or below n, iteratively (a long && chain nests deep), heredoc bodies included: an
    # unquoted body's substitutions run, and shfmt parses them as the body word's parts
    todo = [n]
    while todo:
        n = todo.pop()
        if isinstance(n, dict):
            yield n
            todo.extend(n.values())
        elif isinstance(n, list):
            todo.extend(n)


def stmts(tree):  # each statement with the outermost statement of its &&, || or | chain, also those in heredoc bodies
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
            todo.extend((v, top if k in keep else None) for k, v in n.items())


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
        if dollar and c == "\\" and (m := ANSI_ESC.match(raw, i)):  # bash's $'…' table; an unknown escape stays as is
            o, h, u, big, ctl, one = m.groups()
            num = int(o, 8) if o else int(h, 16) if h else int(u or big, 16) if u or big else None
            got = chr(num) if num is not None and num <= 0x10FFFF else chr(ord(ctl) & 31) if ctl else None
            if got is None:
                got = (ANSI.get(one) or (one if one in "\\'\"?" else m[0])) if one else m[0]
            yield from ((x, line) for x in got)
            line, i = line + m[0].count("\n"), m.end()
            continue
        if c == "\\" and n and kind == "Lit" and (not quoted or n in '\\"$`\n'):
            if n != "\n":  # bash deletes a backslash-newline
                yield n, line
            line, i = line + (n == "\n"), i + 2
            continue
        yield c, line
        line, i = line + (c == "\n"), i + 1


def static(word):  # the literal text of a word, its runtime expansions left out
    return "".join(c for part, quoted in flat(word) for c, _ in chars(part, quoted))


def leading(word):  # (part, quoted) of the first part that adds text: an empty literal ('' or "") adds none
    return next(((p, q) for p, q in flat(word) if p["Type"] not in LITS or next(chars(p, q), None)), None)


def option(word, signs="-"):  # a literal option: the word's text starts with one of signs and that text is literal
    # (empty fragments before it vanish, as the shell joins them), never an expansion's
    first = leading(word)
    return bool(first) and first[0]["Type"] in LITS and static(word)[:1] in signs


def command(call):  # a CallExpr's words and argument nodes from its command word on, past the WRAPPERS, their
    # options, the values those options take and their positional operands
    args, i = call.get("Args") or [], 0
    while i < len(args) and os.path.basename(static(args[i])) in WRAPPERS:
        takes, i = WRAPPERS[os.path.basename(static(args[i]))], i + 1
        while i < len(args) and option(args[i]):
            flag, i = static(args[i]), i + 1
            if flag == "--":
                break
            i += flag in takes
        while i < len(args) and WRAPPER_OPERAND.fullmatch(static(args[i])):
            i += 1
    return [static(a) for a in args[i:]], args[i:]


def stage(stmt, last):  # the CallExpr one pipeline stage runs: through a subshell or a block, to an inner pipe's end
    cmd = (stmt or {}).get("Cmd") or {}
    if cmd.get("Type") in ("Subshell", "Block") and cmd.get("Stmts"):
        return stage(cmd["Stmts"][-1 if last else 0], last)
    if cmd.get("Type") == "BinaryCmd" and cmd["Op"] == "|":
        return stage(cmd["Y" if last else "X"], last)
    return cmd if cmd.get("Type") == "CallExpr" else {}


def is_jq(word):  # the command word runs jq: written out (j"q", $bin/jq-1.7, jq.exe), a jq parameter, or
    # $(command -v jq)
    if JQ_NAME.fullmatch(os.path.basename(static(word))):
        return True
    for n in nodes(word):
        index = [x.get("Value") for x in nodes(n.get("Index") or {})]
        if n.get("Type") == "ParamExp" and "jq" in [(n.get("Param") or {}).get("Value"), *index]:
            return True
        if "jq" in outer_names(n):
            return True
        last = command(stage((n.get("Stmts") or [None])[-1], True))[0][-1:] if n.get("Type") == "CmdSubst" else []
        if last and JQ_NAME.fullmatch(os.path.basename(last[0])):
            return True
    return False


def outer_names(node):  # the names of the outer expansions a nested string's text carries (see spelled), "" for one
    # that is no plain name; they sit in literal parts, whatever quoting the nested text puts around them
    return [x for n in nodes(node) if n.get("Type") in LITS for x in OUTER.findall(n.get("Value") or "")]


def expands(node):  # a parameter expansion below: a name, or a positional or special parameter ($1, ${10}, $@, $?), or
    # an outer expansion in a nested string
    return any(n.get("Type") == "ParamExp" for n in nodes(node)) or bool(outer_names(node))


def operand(word):  # any top-level part is a path-named variable (not its ${#length}) or carries a path-named outer
    # expansion, or the literal text holds a path piece; a substitution or an empty literal before it hides nothing
    for part, _ in flat(word):
        name = part["Type"] == "ParamExp" and not part.get("Length") and (part.get("Param") or {}).get("Value")
        if any(x and TOKEN.search(x) for x in [name, *outer_names(part)]):
            return True
    return bool(LITERAL.search(static(word)))


def program(word, src):  # the jq program one shell word hands over, its fragments in order: (text, line per character)
    pairs = []  # shortcut: an expansion is runtime text and is left out; scan it if one hides a hit
    for part, quoted in flat(word):
        pairs += chars(part, quoted, src(part) if part["Type"] == "Lit" else None)
    return "".join(c for c, _ in pairs), [n for _, n in pairs]


def jq_tokens(prog, i=0, inner=False):  # ([(kind, text, offset)], end): str (its literal text), comment, field, var,
    # ident, punct, op; a string's \( … ) is code between ( and ) tokens. A tokeniser, not a parser of jq's grammar
    out, depth = [], 0
    while i < len(prog):
        if prog[i] == '"':
            j, start = i + 1, i
            while j < len(prog) and prog[j] != '"':
                if prog.startswith("\\(", j):
                    sub, end = jq_tokens(prog, j + 2, True)
                    out += [("str", prog[start + 1 : j], start), ("punct", "(", j), *sub, ("punct", ")", end - 1)]
                    start, j = end - 1, end
                    continue
                j += 2 if prog[j] == "\\" else 1
            out.append(("str", prog[start + 1 : j], start))
            i = j + 1
            continue
        if inner and prog[i] == ")" and depth == 0:
            return out, i + 1
        tok = JQ_LEX.match(prog, i)[0]
        depth += (tok in "([{") - (tok in ")]}") if len(tok) == 1 else 0
        kind = (
            "comment"
            if tok[0] == "#"
            else "field"
            if tok[0] == "." and len(tok) > 1
            else "var"
            if tok[0] == "$"
            else "op"
        )
        kind = "ident" if tok[0].isalpha() or tok[0] == "_" else "punct" if tok in "()[]{},;:|" else kind
        if not tok.isspace():
            out.append((kind, tok, i))
        i += len(tok)
    return out, i


def shell_hits(rel, text, zsh=None, label=None):  # (hits, comments): the shell rules on shfmt's AST; a marker counts
    # only in a comment node; zsh and label: a nested string's dialect and its place in the file, for an error
    tree, text = shfmt_tree(rel, text, zsh, label)
    data, hits = text.encode(), []
    comments = [c for c in nodes(tree) if "Hash" in c and "Text" in c]
    note = {c["Hash"]["Line"]: "#" + c["Text"] for c in comments}
    code = bytearray(data)  # the source with its comments blanked: a normaliser counts in code only
    hdocs = [p for r in nodes(tree) if r.get("Hdoc") for p in r["Hdoc"].get("Parts") or [] if p["Type"] == "Lit"]
    for c in comments + hdocs:  # a heredoc body's literal text is data; its substitutions are code
        code[c["Pos"]["Offset"] : c["End"]["Offset"]] = re.sub(
            rb"[^\n]", b" ", code[c["Pos"]["Offset"] : c["End"]["Offset"]]
        )
    code = code.decode(errors="replace").split("\n")

    def src(n):
        return data[n["Pos"]["Offset"] : n["End"]["Offset"]].decode(errors="replace")

    def accepted(lo, hi, norm=None):  # a normaliser in the code of lines lo..hi, or a marker with its reason there
        if norm and re.search(norm, "\n".join(code[lo - 1 : hi])):
            return True
        return any((m := MARKER.search(note.get(k, ""))) and m.group(1) for k in range(lo, hi + 1))

    def shell_text(words):  # (character, outer line) of the text a nested shell parses: each word as the outer shell
        # hands it over, joined by spaces. The outer shell performs its expansions before the nested parse, so the
        # nested quoting cannot protect them: each becomes the token spelled(name), which the rules read as an
        # unknown value in any quoting; only the outer literal text stays literal
        pairs = []
        for k, word in enumerate(words):
            if k:
                pairs.append((" ", pairs[-1][1] if pairs else word["Pos"]["Line"]))
            for part, quoted in flat(word):
                if part["Type"] in LITS:
                    pairs += chars(part, quoted, src(part) if part["Type"] == "Lit" else None)
                    continue
                name = part["Type"] == "ParamExp" and not part.get("Length") and (part.get("Param") or {}).get("Value")
                pairs += [(c, part["Pos"]["Line"]) for c in spelled(name if re.fullmatch(r"\w+", name or "") else "")]
        return pairs

    for stmt, top in stmts(tree):  # a statement's lines are its whole chain's, continued lines included
        cmd, lo, hi = stmt["Cmd"], top["Pos"]["Line"], top["End"]["Line"]
        if not isinstance(cmd, dict):
            continue
        t, (words, args), at = cmd.get("Type"), command(cmd), cmd["Pos"]["Line"]
        tests = [n for n in nodes(cmd) if n.get("Type") == "BinaryTest" and n["Op"] in ("==", "!=", "=")]
        if t == "TestClause" and any(operand(n["X"]) or operand(n["Y"]) for n in tests):
            hits.append((at, "R1", accepted(lo, hi, SH_NORM)))
        if t == "CallExpr" and words[:1] in (["["], ["test"]):
            ops = range(2, len(args) - 1)
            pairs = [(args[i - 1], args[i + 1]) for i in ops if words[i] in ("==", "!=", "=")]
            if any(operand(x) or operand(y) for x, y in pairs):
                hits.append((at, "R1", accepted(lo, hi, SH_NORM)))
        if t == "CaseClause" and operand(cmd["Word"]):  # for this, the statement ends at its `in`
            hits.append((at, "R2", accepted(lo, cmd.get("In", cmd["Word"]["End"])["Line"], SH_NORM)))
        if t == "BinaryCmd" and cmd["Op"] == "|":  # ps piped to a text reader, unless ps -o <fields>= -p
            ps, reader = command(stage(cmd["X"], True))[0], command(stage(cmd["Y"], False))[0]
            fields = ps[1:2] == ["-o"] and ps[2:3] and ps[2].endswith("=") and ps[3:4] == ["-p"]
            if ps[:1] == ["ps"] and not fields and reader[:1] in (["grep"], ["awk"], ["cut"], ["sed"]):
                hits.append((at, "R5", accepted(lo, hi)))
        git = words[:1] == ["git"] and "grep" in words  # git grep: grep as git's subcommand
        tool = 0 if words and os.path.basename(words[0]) in GREPS else words.index("grep") if git else None
        if t == "CallExpr" and tool is not None:  # also git grep, command grep, xargs grep
            name, k = os.path.basename(words[tool]), tool + 1
            while k < len(args) and option(args[k]):
                k += 1
            flags, pattern = words[tool + 1 : k], args[k] if k < len(args) else {}
            if name == "pgrep" and any(re.fullmatch(r"-\w*f\w*", f) for f in flags) and expands(pattern):
                hits.append((at, "R5", accepted(lo, hi)))
            ere = name == "egrep" or any(re.match(r"-\w*E|--extended-regexp", f) for f in flags)
            if name != "pgrep" and ere and "-F" not in flags and expands(pattern):
                hits.append((at, "R6", accepted(lo, hi, "escape_regex")))
        if t == "CallExpr" and args and is_jq(args[0]):
            i = 1  # the program: past the options and their operands (jq 1.8 --help) and pure expansions
            while i < len(args) and words[i] not in ("-f", "--from-file"):
                if option(args[i]) or not words[i] and expands(args[i]):
                    i += 1 + JQ_SKIP.get(words[i], 0)
                    continue
                prog, lines = program(args[i], src)
                found, marks = jq_hits(prog)
                for (
                    p,
                    text,
                ) in marks:  # a jq comment is a comment: it marks a hit on its line, or is R0 without a reason
                    note.setdefault(lines[p], text)
                hits.extend((lines[p], "R3", ok or accepted(lo, hi)) for p, ok in found)
                break
        nested, nested_zsh = executed(words, args) if t == "CallExpr" else ([], False)
        if nested:  # the nested hits land on the outer lines their text came from
            text_lines = shell_text(nested)
            starts = [0] + [k + 1 for k, (c, _) in enumerate(text_lines) if c == "\n"]
            where = [text_lines[min(s, len(text_lines) - 1)][1] if text_lines else at for s in starts]
            inner, inner_note = shell_hits(rel, "".join(c for c, _ in text_lines), nested_zsh, f"{rel}:{at}")
            hits.extend((where[n - 1], rule, ok or accepted(lo, hi, NORM.get(rule))) for n, rule, ok in inner)
            for n, c in inner_note.items():
                note.setdefault(where[n - 1], c)
    return hits, note


def spelled(name):  # the literal token that stands for an outer expansion in a nested string
    return f"lintcmpX{name}Xpmctnil"


def executed(words, args):  # (the words a command runs as shell code, zsh): a shell's -c string, eval's arguments
    name = os.path.basename(words[0]) if words else ""
    if name == "eval":  # eval takes -- before its arguments
        return args[2 if len(args) > 1 and option(args[1]) and words[1] == "--" else 1 :], False
    if name not in SHELLS:
        return [], False
    i, string = 1, False
    while i < len(args) and option(args[i], "-+"):
        flag, i = words[i], i + 1
        if flag == "--":
            break
        if flag in ("-o", "+o", "-O", "+O"):  # set and shopt options take the next word
            i += 1
        elif not flag.startswith("--") and "c" in flag[1:]:  # -c, also combined: -ec, -lc
            string = True
    return (args[i : i + 1] if string else []), name == "zsh"


def jq_hits(prog):  # ([(offset, accepted)] per string-form comparison, [(offset, text)] per jq comment)
    toks = jq_tokens(prog)[0]
    marks = [(p, t) for k, t, p in toks if k == "comment"]
    toks = [x for x in toks if x[0] != "comment"]
    g = [t if k in ("ident", "punct") else "" for k, t, _ in toks]  # grammar words; a string's text is never one

    def opens(i):
        return g[i] in ("(", "[", "{", "if")  # if … end is one operand, like parentheses

    def closes(i):
        return g[i] in (")", "]", "}", "end")

    def bound(i, fn):  # a function's subject arrives through |, so | bounds only an operator's operands
        return g[i] in (",", ";", "and", "or", "then", "elif", "else") or g[i] == "|" and not fn

    stack, inner = [], []
    for i in range(len(toks)):
        inner.append(stack[-1] if stack else "")
        if opens(i):
            stack.append(g[i])
        elif closes(i) and stack:
            stack.pop()
    defs = {g[i + 1] for i in range(len(g) - 1) if g[i] == "def" and JQ_NORM.fullmatch(g[i + 1])}

    def invoked(i, name):  # the normaliser is applied here: not its definition, nor an object key
        prev, nxt = g[i - 1] if i else "", g[i + 1] if i + 1 < len(g) else ""
        return g[i] == name and prev != "def" and nxt != ":" and not (inner[i] == "{" and prev in ("{", ","))

    found = []
    for k, (kind, t, p) in enumerate(toks):
        fn = g[k] in JQ_FN and g[k + 1 : k + 2] == ["("]
        if not fn and not (kind == "op" and t in ("==", "!=")):
            continue
        lo, depth = k, 0
        while lo > 0 and not (depth == 0 and (opens(lo - 1) or bound(lo - 1, fn))):
            lo -= 1
            depth += closes(lo) - opens(lo)
        hi, depth = k, 0
        while hi < len(toks) and not (depth == 0 and (closes(hi) or bound(hi, fn))):
            depth += opens(hi) - closes(hi)
            hi += 1
        named = (  # an outer shell expansion spliced into the program (see spelled) counts by its name
            x[0] == "field"
            and x[1] in (".url", ".path")
            or x[0] == "var"
            and TOKEN.search(x[1][1:])
            or any(n and TOKEN.search(n) for n in OUTER.findall(x[1]))
            for x in toks[lo:hi]
        )
        if any(named) or any(x[0] == "str" and LITERAL.search(x[1]) for x in toks[lo:hi]):
            sides = (range(lo, k), range(k, hi))
            found.append((p, any(all(any(invoked(i, d) for i in r) for r in sides) for d in defs)))
    return found, marks


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

    def escaped(node):  # a formatted value whose every fragment is re.escape's: a call, a join of escapes, a constant,
        # or a concatenation (+ or a nested f-string) of those
        name = dotted(node.func) if isinstance(node, ast.Call) else ""
        if name == "re.escape" or isinstance(node, ast.Constant):
            return True
        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
            return escaped(node.left) and escaped(node.right)
        if isinstance(node, ast.JoinedStr):
            return all(escaped(v.value) for v in node.values if isinstance(v, ast.FormattedValue))
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
