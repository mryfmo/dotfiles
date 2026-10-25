"""Guards that keep the repository's own scripts working inside the Claude sandbox (plan 023 PR F, T130).

Measured inside the sandbox: `done < <(...)`, `comm <(...) <(...)` and `cat <(...)` work; only `diff` with a process
substitution argument fails (`diff: /dev/fd/N: Operation not permitted`), so the first guard is exactly that predicate.
The sandbox's writable temporary directory is `$TMPDIR`, never `/tmp`, so the second guard refuses a hard-coded `/tmp`
path unless the same line's code really reads `TMPDIR`. Each guard runs over the tracked files of this checkout and over
a temporary repository holding one script.
"""

import io
import re
import subprocess
import tempfile
import tokenize
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ROOTS = ("scripts", "home", "install")
SHELL = re.compile(r"#!.*\b(sh|bash|zsh)\b")
PYTHON = re.compile(r"#!.*python")
TMP = re.compile(r"/tmp(/|\b)")
SHELL_TMPDIR = re.compile(r"\$\{?TMPDIR\b")
PYTHON_TMPDIR = re.compile(r"\bTMPDIR\b|\btempfile\b")
ASSIGNMENT = re.compile(r"[A-Za-z_][A-Za-z0-9_]*(\[[^]]*\])?\+?=")
PREFIXES = ("command", "builtin", "exec")


def shell_scan(text):
    """(commands, code) for shell text. commands: (first line, words) per simple command, each word as written minus
    backslash-newlines; code: the text with comments blanked, newlines kept. Quote and escape state carry across lines;
    `$(`, `<(`, `>(` bodies stay inside their word. Shortcut: heredoc bodies are scanned as commands.
    """
    code, commands, words, cur = list(text), [], [], []
    i, n, line, start = 0, len(text), 1, None

    def flush_word():
        if cur:
            words.append("".join(cur))
            cur.clear()

    def flush_command():
        nonlocal start
        flush_word()
        if words:
            commands.append((start, list(words)))
            words.clear()
        start = None

    def nested(j):
        """End of the `(`...`)` body opening at j - 1, quotes and nested parens skipped."""
        depth = 1
        while j < n and depth:
            c = text[j]
            if c == "\\":
                j += 2
                continue
            if c == "'":
                j = text.find("'", j + 1) % (n + 1) + 1
                continue
            if c == '"':
                j = double(j)
                continue
            depth += {"(": 1, ")": -1}.get(c, 0)
            j += 1
        return j

    def double(j):
        """End of the double-quoted string opening at j."""
        j += 1
        while j < n and text[j] != '"':
            if text[j] == "\\":
                j += 1
            elif text[j] == "$" and text[j + 1 : j + 2] == "(":
                j = nested(j + 2) - 1
            j += 1
        return j + 1

    def take(j):
        nonlocal i, line
        seg = text[i:j]
        line += seg.count("\n")
        cur.append(seg.replace("\\\n", ""))
        i = j

    while i < n:
        c = text[i]
        if start is None and c not in " \t\n;&|()":
            start = line
        if c == "\\":
            if text[i + 1 : i + 2] == "\n":
                i, line = i + 2, line + 1
            else:
                take(i + 2)
        elif c == "'":
            take(text.find("'", i + 1) % (n + 1) + 1)
        elif c == '"':
            take(double(i))
        elif c in "<>$" and text[i + 1 : i + 2] == "(":
            take(nested(i + 2))
        elif c == "#" and not cur:
            end = text.find("\n", i) % (n + 1)
            code[i:end] = " " * (end - i)
            i = end
        elif c == "&" and cur and cur[-1][-1:] in "<>":
            take(i + 1)
        elif c in " \t":
            flush_word()
            i += 1
        elif c in ";&|\n()":
            flush_command()
            line += c == "\n"
            i += 1
        else:
            take(i + 1)
    flush_command()
    return commands, "".join(code)


def unquote(word):
    return re.sub(r"\\(.)", r"\1", word.replace("'", "").replace('"', ""))


def diff_hits(commands):
    """Commands whose command word is diff and that pass a `<(` or `>(` word."""
    for line, words in commands:
        k = 0
        while k < len(words) and (ASSIGNMENT.match(words[k]) or words[k] in PREFIXES):
            k += 1
        cmd = words[k:]
        if cmd and unquote(cmd[0]).rsplit("/", 1)[-1] == "diff" and any(w.startswith(("<(", ">(")) for w in cmd[1:]):
            yield line, " ".join(cmd)


def python_code(text):
    """The text with Python comments blanked; the text itself when it does not tokenize."""
    lines = text.split("\n")
    try:
        for tok in tokenize.generate_tokens(io.StringIO(text).readline):
            if tok.type == tokenize.COMMENT:
                (row, col), (_, end) = tok.start, tok.end
                lines[row - 1] = lines[row - 1][:col] + " " * (end - col) + lines[row - 1][end:]
    except (tokenize.TokenError, SyntaxError):
        pass
    return "\n".join(lines)


def tmp_hits(code, reads_tmpdir):
    for n, line in enumerate(code.split("\n"), 1):
        if TMP.search(line) and not reads_tmpdir.search(line):
            yield n, line.strip()


def tracked(repo):
    """(path, kind) per tracked file under the roots whose name or shebang marks it as shell or python."""
    out = subprocess.run(["git", "ls-files", "-z", "--", *ROOTS], cwd=repo, capture_output=True, text=True, check=True)
    for rel in filter(None, out.stdout.split("\0")):
        text = (repo / rel).read_text(errors="replace")
        first = text.split("\n", 1)[0]
        if rel.endswith((".sh", ".bash", ".zsh")) or SHELL.match(first):
            yield rel, "shell", text
        elif rel.endswith(".py") or PYTHON.match(first):
            yield rel, "python", text


def diff_guard(repo):
    return [
        f"{rel}:{n}: {cmd}"
        for rel, kind, text in tracked(repo)
        if kind == "shell"
        for n, cmd in diff_hits(shell_scan(text)[0])
    ]


def tmp_guard(repo):
    found = []
    for rel, kind, text in tracked(repo):
        if kind == "shell":
            found += [f"{rel}:{n}: {line}" for n, line in tmp_hits(shell_scan(text)[1], SHELL_TMPDIR)]
        else:
            found += [f"{rel}:{n}: {line}" for n, line in tmp_hits(python_code(text), PYTHON_TMPDIR)]
    return found


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

    def sh(self, body):
        return "#!/usr/bin/env bash\n" + body

    def test_tracked_scripts_pass_both_guards(self):
        self.assertEqual([], diff_guard(ROOT))
        self.assertEqual([], tmp_guard(ROOT))

    def test_diff_with_process_substitution_is_refused(self):
        cases = {
            "# diff <(a) <(b) in a comment is fine\ndiff <(sort a) <(sort b)\n": ["2: diff <(sort a) <(sort b)"],
            "diff --label 'a;b' <(printf a) <(printf b)\n": ["1: diff --label 'a;b' <(printf a) <(printf b)"],
            'diff --label "base \\\n# current" \\\n<(printf a) <(printf b)\n': [
                '1: diff --label "base # current" <(printf a) <(printf b)'
            ],
            "diff \\\n<(sort a) \\\n<(sort b)\n": ["1: diff <(sort a) <(sort b)"],
            "foo # a comment ending in a backslash \\\ndiff <(a) <(b)\n": ["2: diff <(a) <(b)"],
            'diff --label "baseline # current" <(sort a) <(sort b)\n': [
                '1: diff --label "baseline # current" <(sort a) <(sort b)'
            ],
            "x=1 command diff a <(b)\n": ["1: diff a <(b)"],
            "true && /usr/bin/diff <(a) b\n": ["1: /usr/bin/diff <(a) b"],
        }
        for body, want in cases.items():
            with self.subTest(body=body):
                got = diff_guard(self.repo_with("bad.sh", self.sh(body)))
                self.assertEqual([f"scripts/bad.sh:{int(w.split(':')[0]) + 1}:{w.split(':', 1)[1]}" for w in want], got)

    def test_diff_without_process_substitution_is_accepted(self):
        for body in (
            "while read -r l; do :; done < <(printf 'a\\n')\n",
            "comm -23 <(printf 'a\\n') <(printf 'b\\n')\n",
            "printf '%s\\n' 'diff <(a) <(b)'\n",
            'echo "diff <(a) <(b)"\n',
            "diff a b; cat <(x)\n",
            "diff a b 2>&1 | cat <(x)\n",
        ):
            with self.subTest(body=body):
                self.assertEqual([], diff_guard(self.repo_with("ok.sh", self.sh(body))))

    def test_hard_coded_tmp_is_refused(self):
        cases = {
            ("bad.sh", self.sh("# /tmp in a comment is fine\nout=/tmp/out.txt\n")): ["3: out=/tmp/out.txt"],
            ("bad.sh", self.sh("out=/tmp/out.txt # TMPDIR\n")): ["2: out=/tmp/out.txt"],
            ("bad.sh", self.sh("printf 'copy # /tmp/out'\n")): ["2: printf 'copy # /tmp/out'"],
            ("bad.py", 'out = "/tmp/out.txt"  # TMPDIR\n'): ['1: out = "/tmp/out.txt"'],
        }
        for (name, body), want in cases.items():
            with self.subTest(body=body):
                self.assertEqual([f"scripts/{name}:{w}" for w in want], tmp_guard(self.repo_with(name, body)))

    def test_tmp_beside_a_real_tmpdir_read_is_accepted(self):
        for name, body in (
            ("ok.sh", self.sh('t="${TMPDIR:-/tmp}/x"\nx=1 # a comment may name /tmp\n')),
            ("ok.sh", self.sh('d=$TMPDIR; [ -n "$d" ] || d=/tmp\n')),
            ("ok.py", 'd = os.environ.get("TMPDIR", "/tmp")\n'),
            ("ok.py", "d = tempfile.gettempdir() or '/tmp'\n"),
        ):
            with self.subTest(body=body):
                self.assertEqual([], tmp_guard(self.repo_with(name, body)))


if __name__ == "__main__":
    unittest.main()
