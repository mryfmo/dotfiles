"""Guards that keep the repository's own scripts working inside the Claude sandbox (plan 023 PR F, T130).

Measured inside the sandbox: `done < <(...)`, `comm <(...) <(...)` and `cat <(...)` work; only `diff` with a process
substitution argument fails (`diff: /dev/fd/N: Operation not permitted`). The sandbox's writable temporary directory is
`$TMPDIR`, never `/tmp`.

Contract: the guards catch accidental, ordinary forms and fail closed on the rest; a refused odd form is fixed by
writing it the plain way, never by teaching the guard a new spelling.
- diff: a command is refused when one of its arguments is literally `diff` or ends in `/diff` and a later argument holds
  a process substitution, whatever command word runs it (env, sudo, xargs or a wrapper of one's own cannot hide it;
  `command -v diff <(x)` is refused too). A later argument whose literal text holds `<(` or `>(` counts as one, since
  shfmt keeps a substitution inside `${x:-<(...)}` as text. Redirection targets are no arguments.
- shell /tmp: a literal `/tmp` path, single-quoted text included, is refused unless it is the operand of a
  `${TMPDIR...}` expansion or its word expands TMPDIR outside single quotes.
- The sandbox's own directory is no `/tmp` path in this sense: exactly `/tmp/claude` or `/private/tmp/claude`, or
  either followed by `/` and components of `[A-Za-z0-9._-]` (no `.` or `..` component), standing as a whole path
  (start, whitespace, a quote, `=`, `:` or a bracket before it; end, whitespace, a quote, `:`, `;`, `,` or a bracket
  after it). Anything else after `claude` (`@`, `+`, a glob character, `$`) is refused. These paths are the TMPDIR srt
  hands the sandboxed child and keeps writable whatever the policy says
  (`SANDBOX_OWN_WRITE_PATHS` and `generateProxyEnvVars` in @anthropic-ai/sandbox-runtime 0.0.81
  dist/sandbox/sandbox-utils.js:499-508, 687-691), so a script naming them (hcom-seat lists them as srt's implicit
  write roots) runs inside the sandbox too. Nothing else under `/tmp` is.
- Python /tmp: a string constant holding a `/tmp` path is refused unless its statement reads TMPDIR by a canonical
  spelling (`os.environ.get("TMPDIR"...)`, `os.environ["TMPDIR"]`, `os.getenv("TMPDIR"...)`) or calls `tempfile.*` with
  the constant outside that call's arguments (an explicit `dir="/tmp"` bypasses TMPDIR). Aliased reads (`from os import
  getenv`) are refused: fail closed, fixed by the canonical spelling.

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
# srt's own TMPDIR, writable in the sandbox; a `..` component may follow nowhere in the path.
# srt's own TMPDIR as a whole path: a path boundary before, `/claude` or components under it, a path boundary after.
SANDBOX_TMP = re.compile(
    r"(?:(?<=^)|(?<=[\s\"'=:(\[{]))(?:/private)?/tmp/claude(?:/(?!\.\.?(?:/|$|[\s\"':;,)\]}]))[A-Za-z0-9._-]+)*"
    r"(?=$|[\s\"':;,)\]}])"
)

SHFMT = (["shfmt"], ["mise", "x", "shfmt@3.14.1", "--", "shfmt"])  # PATH's, else .github/workflows/test.yaml's pin
ENV_READS = ("os.environ.get", "os.getenv")


def tmp_hits(value):
    """The /tmp matches of `value` outside the sandbox's own directory, at their offsets in `value`."""
    return TMP.finditer(SANDBOX_TMP.sub(lambda m: "_" * len(m.group()), value))


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


def substitutes(word):
    """The argument holds a process substitution, or literal `<(`/`>(` text where shfmt left one unparsed; nested
    command and process substitution bodies are their own commands."""
    todo = list(word.get("Parts") or [])
    while todo:
        n = todo.pop()
        if isinstance(n, list):
            todo.extend(n)
        elif isinstance(n, dict):
            if n.get("Type") == "ProcSubst" or n.get("Type") == "Lit" and re.search(r"[<>]\(", n.get("Value", "")):
                return True
            if n.get("Type") != "CmdSubst":
                todo.extend(n.values())
    return False


def diff_lines(tree):
    """Lines of each command with a `diff` argument followed by an argument that substitutes a process."""
    for n in nodes(tree):
        args = n.get("Args") or [] if n.get("Type") == "CallExpr" else []
        names = [i for i, w in enumerate(args) if (lit := literal(w)) and (lit == "diff" or lit.endswith("/diff"))]
        if names and any(substitutes(w) for w in args[names[0] + 1 :]):
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
            for m in tmp_hits(value):
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


def python_tmp_lines(text):
    """Lines of each string constant holding /tmp that its statement neither excuses by a canonical TMPDIR read nor by
    a tempfile call the constant is no argument of."""

    def is_tmpdir(node):
        return isinstance(node, ast.Constant) and node.value == "TMPDIR"

    for stmt in ast.walk(ast.parse(text)):
        if not isinstance(stmt, ast.stmt):
            continue
        found = list(own_nodes(stmt))
        calls = [n for n in found if isinstance(n, ast.Call)]
        if any(dotted(c.func) in ENV_READS and c.args and is_tmpdir(c.args[0]) for c in calls) or any(
            isinstance(n, ast.Subscript)
            and isinstance(n.ctx, ast.Load)  # `os.environ["TMPDIR"] = "/tmp/x"` writes TMPDIR, reads nothing
            and dotted(n.value) == "os.environ"
            and is_tmpdir(n.slice)
            for n in found
        ):
            continue
        tempfile_calls = [c for c in calls if dotted(c.func).startswith("tempfile.")]
        in_tempfile_args = {id(x) for c in tempfile_calls for a in (*c.args, *c.keywords) for x in ast.walk(a)}
        for n in found:
            if isinstance(n, ast.Constant) and isinstance(n.value, str):
                if tempfile_calls and id(n) not in in_tempfile_args:
                    continue
                yield from (n.lineno + n.value[: m.start()].count("\n") for m in tmp_hits(n.value))


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
    "exec -afoo diff <(printf a) <(printf b)\n": [2],
    "env LC_ALL=C diff <(printf a) <(printf b)\n": [2],
    "sudo -u root nice -n 5 timeout 5s diff a <(b)\n": [2],
    "my_wrapper --flag diff a <(b)\n": [2],
    "diff ${left:-<(printf a)} ${right:-<(printf b)}\n": [2],
    "command -v diff <(x)\n": [2],  # fail closed: no command word excuses a diff argument
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
    ("bad.py", 'd = tempfile.mkdtemp(dir="/tmp")\n'): [1],
    ("bad.py", 'd = environ.get("TMPDIR", "/tmp")\n'): [1],
    # fail closed: an aliased read is no canonical spelling, so the constant is refused although it would run fine
    ("bad.py", 'from os import getenv as env\nout = env("TMPDIR", "/tmp")\n'): [2],
    ("bad.py", "from tempfile import gettempdir\nd = gettempdir() or '/tmp'\n"): [2],
    ("bad.py", 'os.environ["TMPDIR"] = "/tmp/work"\n'): [1],
    ("bad.sh", SH + "roots=(/tmp/claudex /tmp/claude.d /tmp/claude-1)\n"): [2],
    ("bad.sh", SH + "out=/tmp/claude/../x\n"): [2],
    ("bad.sh", SH + "out=/tmp/claude/a/.. /tmp/y\n"): [2],
    ("bad.py", 'out = "/private/tmp/claudes"\n'): [1],
    ("bad.sh", SH + "out=/tmp/claude@escape\n"): [2],
    ("bad.sh", SH + "out=/tmp/claude+escape\n"): [2],
    ("bad.sh", SH + "rm -rf /tmp/claude*\n"): [2],
    ("bad.sh", SH + "rm -rf /tmp/claude/*\n"): [2],
    ("bad.sh", SH + "out=/tmp/claude/./x\n"): [2],
    ("bad.sh", SH + "out=/tmp/claude/x/\n"): [2],
    ("bad.sh", SH + "out=/x/tmp/claude\n"): [2],
    ("bad.py", 'out = "/tmp/claude@escape"\n'): [1],
    ("bad.py", 'out = "/tmp/claude+escape"\n'): [1],
    ("bad.py", 'out = "/tmp/claude*"\n'): [1],
}
TMP_ACCEPTED = (
    ("ok.sh", SH + 't="${TMPDIR:-/tmp}/x"\nx=1 # a comment may name /tmp\n'),
    ("ok.sh", SH + 'out="$TMPDIR"/tmp/x\n'),
    ("ok.sh", SH + "out=${TMPDIR:-/private/tmp}\n"),
    ("ok.py", 'd = os.environ.get("TMPDIR", "/tmp")\n'),
    ("ok.py", 'd = os.getenv("TMPDIR") or "/tmp"\n'),
    ("ok.py", 'd = os.environ["TMPDIR"] if "TMPDIR" in os.environ else "/tmp"\n'),
    ("ok.py", "d = tempfile.gettempdir() or '/tmp'\n"),
    ("ok.py", 'd = tempfile.mkdtemp(dir=os.environ.get("TMPDIR", "/tmp"))\n'),
    ("ok.py", 'x = os.environ["TMPDIR"] or "/tmp"\n'),
    ("ok.sh", SH + 'roots=("${HOME}/.npm/_logs" /tmp/claude /private/tmp/claude)\nout=/tmp/claude/x\n'),
    ("ok.py", 'roots = ["/tmp/claude", "/private/tmp/claude/x"]\n'),
    ("ok.sh", SH + 'printf "%s\\n" /tmp/claude:/private/tmp/claude/a.b/c-d_1\n'),
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
