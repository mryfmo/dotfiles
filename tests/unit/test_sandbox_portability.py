"""Guards that keep the repository's own scripts working inside the Claude sandbox (plan 023 PR F, T130).

Measured inside the sandbox: `done < <(...)`, `comm <(...) <(...)` and `cat <(...)` work; only `diff` with a process
substitution argument fails (`diff: /dev/fd/N: Operation not permitted`), so the first guard is exactly that predicate.
The sandbox's writable temporary directory is `$TMPDIR`, never `/tmp`, so the second guard refuses a hard-coded `/tmp`
path unless the line also reads `TMPDIR`. Each guard runs over the tracked files of this checkout and over a temporary
repository holding one offending script.
"""

import re
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ROOTS = ("scripts", "home", "install")
SHELL = re.compile(r"#!.*\b(sh|bash|zsh)\b")
PYTHON = re.compile(r"#!.*python")
DIFF_SUBSTITUTION = re.compile(r"\bdiff\b[^|;&]*[<>]\(")
TMP = re.compile(r"/tmp(/|\b)")


def scan(line):
    """(code, syntax): the line before its comment, and that text with every quoted span and escaped character blanked.

    A comment starts at a `#` at the start or after whitespace, outside quotes. A predicate reads shell syntax (an
    operator, `<(`, a continuation) from `syntax` only, so nothing inside quotes is ever an operator or a comment.
    """
    code, syntax, quote, i = [], [], "", 0
    while i < len(line):
        ch = line[i]
        if ch == "\\" and quote != "'" and i + 1 < len(line):
            code += line[i : i + 2]
            syntax += "  "
            i += 2
            continue
        if quote:
            syntax.append(ch if ch == quote else " ")
            quote = "" if ch == quote else quote
        elif ch in "'\"":
            quote = ch
            syntax.append(ch)
        elif ch == "#" and (i == 0 or line[i - 1].isspace()):
            break
        else:
            syntax.append(ch)
        code.append(ch)
        i += 1
    return "".join(code), "".join(syntax)


def logical_lines(text):
    """(first line number, text) per logical line: a backslash before the newline, outside a comment, joins the next line."""
    start, parts = 1, []
    for n, line in enumerate(text.split("\n"), 1):
        continued = scan(line)[0].endswith("\\")
        parts.append(line[:-1] if continued else line)
        if not continued:
            yield start, "".join(parts)
            start, parts = n + 1, []
    if parts:
        yield start, "".join(parts)


def tracked(repo, kinds):
    """Tracked files under the roots whose name or shebang marks them as the given kinds (shell, python)."""
    out = subprocess.run(["git", "ls-files", "-z", "--", *ROOTS], cwd=repo, capture_output=True, text=True, check=True)
    for rel in filter(None, out.stdout.split("\0")):
        path = repo / rel
        first = path.read_text(errors="replace").split("\n", 1)[0]
        if rel.endswith((".sh", ".bash", ".zsh")) or SHELL.match(first):
            kind = "shell"
        else:
            kind = "python" if rel.endswith(".py") or PYTHON.match(first) else None
        if kind in kinds:
            yield rel, path


def hits(repo, kinds, refused):
    return [
        f"{rel}:{n}: {line.strip()}"
        for rel, path in tracked(repo, kinds)
        for n, line in logical_lines(path.read_text(errors="replace"))
        if refused(*scan(line), line)
    ]


def diff_refused(_code, syntax, _line):
    return bool(DIFF_SUBSTITUTION.search(syntax))


def tmp_refused(code, _syntax, line):
    return bool(TMP.search(code)) and "TMPDIR" not in line


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
        }
        for args in (
            ["init", "-q", "-b", "main"],
            ["add", "."],
            ["-c", "commit.gpgsign=false", "commit", "-q", "-m", "x"],
        ):
            subprocess.run(["git", *args], cwd=repo, env={**env, "PATH": "/usr/bin:/bin:/opt/homebrew/bin"}, check=True)
        return repo

    def test_no_process_substitution_in_tracked_scripts(self):
        offending = "#!/usr/bin/env bash\n# diff <(a) <(b) in a comment is fine\ndiff <(sort a) <(sort b)\n"
        self.assertEqual(
            ["scripts/bad.sh:3: diff <(sort a) <(sort b)"],
            hits(self.repo_with("bad.sh", offending), {"shell"}, diff_refused),
        )
        accepted = "#!/usr/bin/env bash\nwhile read -r l; do :; done < <(printf 'a\\n')\ncomm -23 <(printf 'a\\n') <(printf 'b\\n')\n"
        self.assertEqual([], hits(self.repo_with("ok.sh", accepted), {"shell"}, diff_refused))
        self.assertEqual([], hits(ROOT, {"shell"}, diff_refused))

    def test_no_hard_coded_tmp_in_tracked_scripts(self):
        offending = '#!/usr/bin/env bash\n# /tmp in a comment is fine\nout=/tmp/out.txt\nt="${TMPDIR:-/tmp}/x"\n'
        self.assertEqual(
            ["scripts/bad.sh:3: out=/tmp/out.txt"],
            hits(self.repo_with("bad.sh", offending), {"shell", "python"}, tmp_refused),
        )
        self.assertEqual(
            [],
            hits(self.repo_with("ok.py", 'd = os.environ.get("TMPDIR", "/tmp")\n'), {"shell", "python"}, tmp_refused),
        )
        self.assertEqual([], hits(ROOT, {"shell", "python"}, tmp_refused))

    def test_a_continued_diff_command_is_refused(self):
        continued = "#!/usr/bin/env bash\ndiff \\\n<(sort a) \\\n<(sort b)\n"
        self.assertEqual(
            ["scripts/bad.sh:2: diff <(sort a) <(sort b)"],
            hits(self.repo_with("bad.sh", continued), {"shell"}, diff_refused),
        )
        trailing = "#!/usr/bin/env bash\nfoo # a comment ending in a backslash \\\ndiff <(a) <(b)\n"
        self.assertEqual(
            ["scripts/bad.sh:3: diff <(a) <(b)"], hits(self.repo_with("bad.sh", trailing), {"shell"}, diff_refused)
        )
        last = "diff <(a) <(b) \\"
        self.assertEqual(
            ["scripts/bad.sh:1: diff <(a) <(b)"], hits(self.repo_with("bad.sh", last), {"shell"}, diff_refused)
        )

    def test_a_quoted_hash_is_not_a_comment(self):
        quoted = (
            "#!/usr/bin/env bash\n"
            'diff --label "baseline # current" <(sort a) <(sort b)\n'
            "printf 'copy # /tmp/out'\n"
            "x=1 # a comment may name /tmp\n"
        )
        repo = self.repo_with("bad.sh", quoted)
        self.assertEqual(
            ['scripts/bad.sh:2: diff --label "baseline # current" <(sort a) <(sort b)'],
            hits(repo, {"shell"}, diff_refused),
        )
        self.assertEqual(["scripts/bad.sh:3: printf 'copy # /tmp/out'"], hits(repo, {"shell"}, tmp_refused))

    def test_a_quoted_span_is_never_shell_syntax(self):
        quoted = (
            "#!/usr/bin/env bash\n"
            "diff --label 'old|new' <(sort a) <(sort b)\n"
            'diff --label "a;b" <(sort a) <(sort b)\n'
            'diff --label "a&b" <(sort a) <(sort b)\n'
            'diff --label "a\\"b # c" <(sort a) <(sort b)\n'
            "echo 'diff <(a) <(b)'\n"
            'diff "<(a)" b\n'
            'echo "a\\" # /tmp"\n'
        )
        repo = self.repo_with("bad.sh", quoted)
        self.assertEqual(
            [f"scripts/bad.sh:{n}: {text}" for n, text in enumerate(quoted.split("\n")[1:5], 2)],
            hits(repo, {"shell"}, diff_refused),
        )
        self.assertEqual(['scripts/bad.sh:8: echo "a\\" # /tmp"'], hits(repo, {"shell"}, tmp_refused))


if __name__ == "__main__":
    unittest.main()
