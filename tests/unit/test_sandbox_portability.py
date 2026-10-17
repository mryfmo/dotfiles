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


def code(line):
    """The line before its comment: a `#` at the start or after whitespace, outside quotes; a quoted `#` is code."""
    quote = ""
    for i, ch in enumerate(line):
        if quote:
            quote = "" if ch == quote else quote
        elif ch in "'\"":
            quote = ch
        elif ch == "#" and (i == 0 or line[i - 1].isspace()):
            return line[:i]
    return line  # shortcut: a backslash-escaped quote reads as a quote; upgrade when a tracked line needs it


def logical_lines(text):
    """(first line number, text) per logical line: a backslash before the newline, outside a comment, joins the next line."""
    start, parts = 1, []
    for n, line in enumerate(text.split("\n"), 1):
        continued = code(line).endswith("\\")
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
        if refused(code(line), line)
    ]


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
        def refused(code_line, _line):
            return bool(DIFF_SUBSTITUTION.search(code_line))

        offending = "#!/usr/bin/env bash\n# diff <(a) <(b) in a comment is fine\ndiff <(sort a) <(sort b)\n"
        self.assertEqual(
            ["scripts/bad.sh:3: diff <(sort a) <(sort b)"],
            hits(self.repo_with("bad.sh", offending), {"shell"}, refused),
        )
        accepted = "#!/usr/bin/env bash\nwhile read -r l; do :; done < <(printf 'a\\n')\ncomm -23 <(printf 'a\\n') <(printf 'b\\n')\n"
        self.assertEqual([], hits(self.repo_with("ok.sh", accepted), {"shell"}, refused))
        self.assertEqual([], hits(ROOT, {"shell"}, refused))

    def test_no_hard_coded_tmp_in_tracked_scripts(self):
        def refused(code_line, line):
            return bool(TMP.search(code_line)) and "TMPDIR" not in line

        offending = '#!/usr/bin/env bash\n# /tmp in a comment is fine\nout=/tmp/out.txt\nt="${TMPDIR:-/tmp}/x"\n'
        self.assertEqual(
            ["scripts/bad.sh:3: out=/tmp/out.txt"],
            hits(self.repo_with("bad.sh", offending), {"shell", "python"}, refused),
        )
        self.assertEqual(
            [], hits(self.repo_with("ok.py", 'd = os.environ.get("TMPDIR", "/tmp")\n'), {"shell", "python"}, refused)
        )
        self.assertEqual([], hits(ROOT, {"shell", "python"}, refused))

    def test_a_continued_diff_command_is_refused(self):
        def refused(code_line, _line):
            return bool(DIFF_SUBSTITUTION.search(code_line))

        continued = "#!/usr/bin/env bash\ndiff \\\n<(sort a) \\\n<(sort b)\n"
        self.assertEqual(
            ["scripts/bad.sh:2: diff <(sort a) <(sort b)"],
            hits(self.repo_with("bad.sh", continued), {"shell"}, refused),
        )
        trailing = "#!/usr/bin/env bash\nfoo # a comment ending in a backslash \\\ndiff <(a) <(b)\n"
        self.assertEqual(
            ["scripts/bad.sh:3: diff <(a) <(b)"], hits(self.repo_with("bad.sh", trailing), {"shell"}, refused)
        )
        last = "diff <(a) <(b) \\"
        self.assertEqual(["scripts/bad.sh:1: diff <(a) <(b)"], hits(self.repo_with("bad.sh", last), {"shell"}, refused))

    def test_a_quoted_hash_is_not_a_comment(self):
        def diff_refused(code_line, _line):
            return bool(DIFF_SUBSTITUTION.search(code_line))

        def tmp_refused(code_line, line):
            return bool(TMP.search(code_line)) and "TMPDIR" not in line

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


if __name__ == "__main__":
    unittest.main()
