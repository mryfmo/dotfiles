"""Guards that keep the repository's own scripts working inside the Claude sandbox (plan 023 PR F, T130).

Measured inside the sandbox: `done < <(...)`, `comm <(...) <(...)` and `cat <(...)` work; only `diff` with a process
substitution argument fails (`diff: /dev/fd/N: Operation not permitted`), so the first guard is exactly that predicate.
The sandbox's writable temporary directory is `$TMPDIR`, never `/tmp`, so the second guard refuses a hard-coded `/tmp`
path unless the same word expands TMPDIR (shell) or the same statement reads it or calls tempfile (Python).

Shell is read only from shfmt's JSON syntax tree (PATH's shfmt, which CI pins, else the pinned mise form); a missing
shfmt or a parse failure fails the test, and no text scan stands in for the parser. A comment ending in a backslash is
reported, since shfmt joins the next line to the command there and bash does not. Python is read with ast.
"""

import ast
import functools
import json
import re
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ROOTS = ("scripts", "home", "install")
SHELL = re.compile(r"#!.*\b(sh|bash|zsh)\b")
PYTHON = re.compile(r"#!.*python")
TMP = re.compile(r"/tmp(/|\b)")
SHFMT = (["shfmt"], ["mise", "x", "shfmt@3.14.1", "--", "shfmt"])  # PATH's, else .github/workflows/test.yaml's pin
WRAPPERS = ("command", "builtin", "exec")
ENV_READS = ("os.environ.get", "environ.get", "os.getenv", "getenv")
ENVIRON = ("os.environ", "environ")


@functools.cache
def shfmt():
    for cmd in SHFMT:
        try:
            run = subprocess.run([*cmd, "--version"], stdin=subprocess.DEVNULL, capture_output=True, check=False)
        except OSError:
            continue
        if run.returncode == 0:
            return cmd
    raise RuntimeError("shfmt missing: the shell guards have no parser")


def blank(m):
    """A chezmoi action is no shell: blanked with lines kept; an include alone on its line is `:`, since it expands to
    whole statements."""
    head, tail = m.string[: m.start()].rpartition("\n")[2], m.string[m.end() :].partition("\n")[0]
    lone = not head.strip() and not tail.strip() and re.match(r"\{\{-?\s*(?:include|includeTemplate|template)\b", m[0])
    return (":" if lone else " ") + re.sub(r"[^\n]", " ", m[0][1:])


def shell_tree(rel, text):
    zsh = rel.removesuffix(".tmpl").endswith(".zsh") or re.match(r"#!.*\bzsh\b", text)
    if rel.endswith(".tmpl"):
        text = re.sub(r"\{\{.*?\}\}", blank, text, flags=re.DOTALL)
    cmd = [*shfmt(), "-ln", "zsh" if zsh else "bash", "--tojson"]
    run = subprocess.run(cmd, input=text, capture_output=True, text=True, check=False)
    if run.returncode:
        raise RuntimeError(f"{rel}: {run.stderr.strip()}")
    tree = json.loads(run.stdout)
    if not isinstance(tree, dict) or tree.get("Type") != "File":
        raise RuntimeError(f"{rel}: shfmt gave no JSON AST")
    return tree


def nodes(tree):
    """Every node at or below tree, heredoc bodies included (an unquoted one runs its substitutions)."""
    todo = [tree]
    while todo:
        n = todo.pop()
        if isinstance(n, dict):
            yield n
            todo.extend(n.values())
        elif isinstance(n, list):
            todo.extend(n)


def literal(word):
    """The word's text after quote removal when it holds no expansion, else None."""
    out = []
    for part in word.get("Parts") or []:
        kind = part["Type"]
        if kind == "Lit":
            out.append(re.sub(r"\\(.)", r"\1", part.get("Value", "")))
        elif kind == "SglQuoted":
            out.append(part.get("Value", ""))
        elif kind == "DblQuoted" and all(p["Type"] == "Lit" for p in part.get("Parts") or []):
            out += [p.get("Value", "") for p in part.get("Parts") or []]
        else:
            return None
    return "".join(out)


def effective(args):
    """The arguments from the command word on, past command, builtin and exec with their options; `command -v` and
    `command -V` only look the name up, so they run nothing."""
    i = 0
    while i < len(args) and literal(args[i]) in WRAPPERS:
        wrapper = literal(args[i])
        i += 1
        while i < len(args) and (opt := literal(args[i]) or "").startswith("-"):
            i += 1
            if opt == "--":
                break
            if wrapper == "command" and set(opt[1:]) & {"v", "V"}:
                return []
            if wrapper == "exec" and "a" in opt[1:]:
                i += 1  # exec -a takes the process name as its operand
    return args[i:]


def diff_lines(tree):
    """Lines of each command that runs diff with a process substitution argument; redirection targets are no arguments."""
    for n in nodes(tree):
        if n.get("Type") != "CallExpr":
            continue
        args = effective(n.get("Args") or [])
        name = args and literal(args[0])
        runs_diff = name and (name == "diff" or name.endswith("/diff"))
        if runs_diff and any(p["Type"] == "ProcSubst" for w in args[1:] for p in w.get("Parts") or []):
            yield n["Pos"]["Line"]


def expands_tmpdir(part):
    param = part.get("Param") or {}
    return part.get("Type") == "ParamExp" and param.get("Value") == "TMPDIR" and not part.get("Length")


def word_expands_tmpdir(word):
    """A ParamExp of TMPDIR at the word's top level or inside its double quotes; single-quoted text is literal."""
    for part in word.get("Parts") or []:
        inner = part.get("Parts") or [] if part["Type"] == "DblQuoted" else [part]
        if any(expands_tmpdir(p) for p in inner):
            return True
    return False


def shell_tmp_lines(tree):
    """Lines of each literal /tmp outside a TMPDIR expansion's operand and outside a word that expands TMPDIR."""
    todo = [(tree, False)]
    while todo:
        n, ok = todo.pop()
        if isinstance(n, list):
            todo.extend((x, ok) for x in n)
            continue
        if not isinstance(n, dict):
            continue
        if n.get("Type") in ("CmdSubst", "ProcSubst"):
            ok = False  # a nested command is judged on its own words
        if "Parts" in n and "Type" not in n:  # a Word
            ok = ok or word_expands_tmpdir(n)
        if n.get("Type") in ("Lit", "SglQuoted") and not ok:
            value = n.get("Value", "")
            for m in TMP.finditer(value):
                yield n["Pos"]["Line"] + value[: m.start()].count("\n")
        todo.extend((v, ok or expands_tmpdir(n)) for v in n.values())


def dotted(node):
    if isinstance(node, ast.Attribute):
        return f"{dotted(node.value)}.{node.attr}"
    return node.id if isinstance(node, ast.Name) else ""


def own_nodes(stmt):
    """The statement's own expressions, its nested statements left to themselves."""
    todo = [stmt]
    while todo:
        n = todo.pop()
        yield n
        todo.extend(c for c in ast.iter_child_nodes(n) if not isinstance(c, (ast.stmt, ast.excepthandler)))


def reads_tmpdir(found, from_tempfile):
    def is_tmpdir(node):
        return isinstance(node, ast.Constant) and node.value == "TMPDIR"

    for n in found:
        if isinstance(n, ast.Call):
            name = dotted(n.func)
            if name in ENV_READS and n.args and is_tmpdir(n.args[0]):
                return True
            if name.startswith("tempfile.") or name in from_tempfile:
                return True
        if isinstance(n, ast.Subscript) and dotted(n.value) in ENVIRON and is_tmpdir(n.slice):
            return True
    return False


def python_tmp_lines(text):
    """Lines of each string constant holding /tmp in a statement that neither reads TMPDIR nor calls tempfile."""
    tree = ast.parse(text)
    from_tempfile = {
        a.asname or a.name
        for n in ast.walk(tree)
        if isinstance(n, ast.ImportFrom) and n.module == "tempfile"
        for a in n.names
    }
    for stmt in ast.walk(tree):
        if not isinstance(stmt, ast.stmt):
            continue
        found = list(own_nodes(stmt))
        if reads_tmpdir(found, from_tempfile):
            continue
        for n in found:
            if isinstance(n, ast.Constant) and isinstance(n.value, str):
                yield from (n.lineno + n.value[: m.start()].count("\n") for m in TMP.finditer(n.value))


def misread_lines(tree):
    """Lines of each comment ending in a backslash: shfmt 3.14.1 joins the next line to the command, bash does not, so
    the tree cannot vouch for that line."""
    for n in nodes(tree):
        if "Hash" in n and n.get("Text", "").rstrip("\n").endswith("\\"):
            yield n["Pos"]["Line"]


def findings(rel, text):
    """{"diff": [line...], "tmp": [line...], "misread": [line...]} for one file, by its kind."""
    if rel.removesuffix(".tmpl").endswith(".py") or PYTHON.match(text):
        return {"diff": [], "tmp": sorted(set(python_tmp_lines(text))), "misread": []}
    tree = shell_tree(rel, text)
    rules = {"diff": diff_lines, "tmp": shell_tmp_lines, "misread": misread_lines}
    return {rule: sorted(set(lines(tree))) for rule, lines in rules.items()}


def tracked(repo):
    """(path, text) per tracked shell or Python file under the roots, by name (a chezmoi template's too) or shebang; a
    chezmoi symlink_ template holds a link target, no script."""
    out = subprocess.run(["git", "ls-files", "-z", "--", *ROOTS], cwd=repo, capture_output=True, text=True, check=True)
    for rel in filter(None, out.stdout.split("\0")):
        if Path(rel).name.startswith("symlink_"):
            continue
        text = (repo / rel).read_text(errors="replace")
        if (
            rel.removesuffix(".tmpl").endswith((".sh", ".bash", ".zsh", ".py"))
            or SHELL.match(text)
            or PYTHON.match(text)
        ):
            yield rel, text


def guard(repo):
    """`<path>:<line>: <rule>: <source line>` per hit across the repository's tracked scripts."""
    hits = []
    for rel, text in tracked(repo):
        lines = text.split("\n")
        hits += [f"{rel}:{n}: {rule}: {lines[n - 1].strip()}" for rule, ns in findings(rel, text).items() for n in ns]
    return hits


SH = "#!/usr/bin/env bash\n"
DIFF_REFUSED = {
    "diff <(sort a) <(sort b)\n": [2],
    "# diff <(a) <(b) in a comment\ndiff a <(b)\n": [3],
    "diff --label 'a;b' <(printf a) <(printf b)\n": [2],
    'diff --label "base \\\n# current" \\\n<(printf a) <(printf b)\n': [2],
    "diff \\\n<(sort a) \\\n<(sort b)\n": [2],
    'diff --label "baseline # current" <(sort a) <(sort b)\n': [2],
    "x=1 command diff a <(b)\n": [2],
    "true && /usr/bin/diff <(a) b\n": [2],
    "out=$(diff a <(b))\n": [2],
    "cat <(diff a <(b))\n": [2],
    "if diff a <(b); then :; fi\n": [2],
    "f() { diff a <(b); }\n": [2],
    "command -- diff a <(b)\n": [2],
    "exec -- diff a <(b)\n": [2],
    "exec -a name diff a <(b)\n": [2],
    "diff a >(cat)\n": [2],
    "x=$( # it's a comment\n:)\ndiff a <(b)\n": [4],
    "cat <<EOF\n$(diff a <(b))\nEOF\n": [3],
}
DIFF_ACCEPTED = (
    "while read -r l; do :; done < <(printf 'a\\n')\n",
    "comm -23 <(printf 'a\\n') <(printf 'b\\n')\n",
    "printf '%s\\n' 'diff <(a) <(b)'\n",
    'echo "diff <(a) <(b)"\n',
    "diff a b; cat <(x)\n",
    "diff a b 2>&1 | cat <(x)\n",
    "diff a b > >(cat)\n",
    "command -v diff <(x)\n",
    "cat <<'EOF'\ndiff <(a) <(b)\nEOF\n",
    "cat <<EOF\ndiff <(a) <(b)\nEOF\n",
)
TMP_REFUSED = {
    ("bad.sh", SH + "# /tmp in a comment is fine\nout=/tmp/out.txt\n"): [3],
    ("bad.sh", SH + "out=/tmp/out.txt # TMPDIR\n"): [2],
    ("bad.sh", SH + "printf 'copy # /tmp/out'\n"): [2],
    ("bad.sh", SH + "out='/tmp/$TMPDIR/out'\n"): [2],
    ("bad.sh", SH + 'out="${HOME:-/tmp}/x"\n'): [2],
    ("bad.sh", SH + 'd=$TMPDIR; [ -n "$d" ] || d=/tmp\n'): [2],
    ("bad.sh", SH + 'x="$TMPDIR$(mktemp -p /tmp)"\n'): [2],
    ("bad.py", 'out = "/tmp/out.txt"  # TMPDIR\n'): [1],
    ("bad.py", 'out = "/tmp/TMPDIR/out"\n'): [1],
    ("bad.py", 'if os.environ.get("TMPDIR"):\n    out = "/tmp/x"\n'): [2],
}
TMP_ACCEPTED = (
    ("ok.sh", SH + 't="${TMPDIR:-/tmp}/x"\nx=1 # a comment may name /tmp\n'),
    ("ok.sh", SH + 'out="$TMPDIR"/tmp/x\n'),
    ("ok.sh", SH + "out=${TMPDIR:-/private/tmp}\n"),
    ("ok.py", 'd = os.environ.get("TMPDIR", "/tmp")\n'),
    ("ok.py", 'd = os.getenv("TMPDIR") or "/tmp"\n'),
    ("ok.py", 'd = os.environ["TMPDIR"] if "TMPDIR" in os.environ else "/tmp"\n'),
    ("ok.py", "d = tempfile.gettempdir() or '/tmp'\n"),
    ("ok.py", "from tempfile import gettempdir\nd = gettempdir() or '/tmp'\n"),
)


class SandboxPortabilityTest(unittest.TestCase):
    def repo_with(self, name, text):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        repo = Path(temp.name).resolve()
        (repo / "scripts").mkdir()
        (repo / "scripts" / name).write_text(text)
        env = {
            "GIT_AUTHOR_NAME": "t",
            "GIT_AUTHOR_EMAIL": "t@t",
            "GIT_COMMITTER_NAME": "t",
            "GIT_COMMITTER_EMAIL": "t@t",
            "PATH": "/usr/bin:/bin:/opt/homebrew/bin",
        }
        for args in (
            ["init", "-q", "-b", "main"],
            ["add", "."],
            ["-c", "commit.gpgsign=false", "commit", "-q", "-m", "x"],
        ):
            subprocess.run(["git", *args], cwd=repo, env=env, check=True)
        return repo

    def test_tracked_scripts_pass_both_guards(self):
        self.assertEqual([], guard(ROOT))

    def test_a_tracked_offending_script_is_reported(self):
        repo = self.repo_with("bad", SH + "diff a <(b)\nout=/tmp/x\n")
        self.assertEqual(["scripts/bad:2: diff: diff a <(b)", "scripts/bad:3: tmp: out=/tmp/x"], guard(repo))

    def test_diff_with_a_process_substitution_argument_is_refused(self):
        for body, want in DIFF_REFUSED.items():
            with self.subTest(body=body):
                self.assertEqual(want, findings("bad.sh", SH + body)["diff"])

    def test_diff_without_a_process_substitution_argument_is_accepted(self):
        for body in DIFF_ACCEPTED:
            with self.subTest(body=body):
                self.assertEqual([], findings("ok.sh", SH + body)["diff"])

    def test_hard_coded_tmp_is_refused(self):
        for (name, body), want in TMP_REFUSED.items():
            with self.subTest(body=body):
                self.assertEqual(want, findings(name, body)["tmp"])

    def test_tmp_beside_a_real_tmpdir_read_is_accepted(self):
        for name, body in TMP_ACCEPTED:
            with self.subTest(body=body):
                self.assertEqual([], findings(name, body)["tmp"])

    def test_a_script_shfmt_cannot_parse_fails(self):
        with self.assertRaisesRegex(RuntimeError, "bad.sh: "):
            findings("bad.sh", SH + "f() {\n")

    def test_a_comment_ending_in_a_backslash_is_reported_as_misread(self):
        # bash runs the diff on line 3; shfmt folds it into foo's arguments, so the file is refused, not passed
        body = SH + "foo # a comment ending in a backslash \\\ndiff <(a) <(b)\n"
        self.assertEqual([2], findings("bad.sh", body)["misread"])
        self.assertEqual([], findings("ok.sh", SH + "foo \\\n  bar # a plain comment\n")["misread"])


if __name__ == "__main__":
    unittest.main()
