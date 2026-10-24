#!/usr/bin/env python3
"""Exercise the supplemental check for a dirname or basename substitution that ShellCheck's SC2312 exempts."""

from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CHECK = ROOT / "scripts/ci/masked-dirname-check.sh"

# scripts/orchestrator/hcom-seat:58 at 89427c81, the U31 defect the audit seat found.
U31_SHAPE = 'dir=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P) || exit 2\n'


@unittest.skipUnless(shutil.which("shfmt") or os.environ.get("CI"), "needs shfmt outside CI (CI puts 3.14.1 on PATH)")
class MaskedDirnameCheckTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = Path(tempfile.mkdtemp(prefix="masked-dirname-check-test-"))

    def tearDown(self) -> None:
        shutil.rmtree(self.temp_dir)

    def script(self, name: str, body: str) -> Path:
        path = self.temp_dir / name
        path.write_text("#!/usr/bin/env bash\n" + body)
        return path

    def run_check(self, *paths: Path, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["bash", str(CHECK), *map(str, paths)], text=True, capture_output=True, check=False, env=env
        )

    def test_the_u31_shape_is_reported_at_its_line(self) -> None:
        lever = self.script("lever", "set -euo pipefail\n" + U31_SHAPE)

        result = self.run_check(lever)

        self.assertEqual(1, result.returncode, result.stderr)
        self.assertEqual(
            f"{lever}:3: a $(dirname) or $(basename) inside another command substitution loses its status;"
            " capture it first or split the path in the shell\n",
            result.stdout,
        )

    def test_a_basename_of_a_dirname_substitution_is_reported(self) -> None:
        lever = self.script("lever", 'team="$(basename -- "$(dirname -- "${config}")")"\n')

        result = self.run_check(lever)

        self.assertEqual(1, result.returncode, result.stderr)
        self.assertIn(f"{lever}:2: a $(dirname) or $(basename)", result.stdout)

    def test_a_dirname_of_a_plain_variable_and_text_that_only_mentions_it_pass(self) -> None:
        clean = self.script(
            "clean",
            'dir=$(dirname -- "${path}")\n'
            'name="$(basename "$0")"\n'
            '# dir=$(cd "$(dirname "$0")" && pwd -P) in a comment\n'
            "printf 'run $(cd \"$(dirname x)\")\\n'\n"
            'total=$((count + $(wc -l < "${file}")))\n'
            'echo "$(date) $(dirname "${path}")"\n',
        )

        result = self.run_check(clean)

        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertEqual("", result.stdout)

    def test_every_listed_file_is_read_and_one_finding_fails_the_list(self) -> None:
        clean = self.script("clean", 'dir=$(dirname -- "${path}")\n')
        lever = self.script("lever", U31_SHAPE)

        result = self.run_check(clean, lever)

        self.assertEqual(1, result.returncode, result.stderr)
        self.assertEqual(1, result.stdout.count(":2: a $(dirname)"))
        self.assertIn(str(lever), result.stdout)

    @unittest.skipIf(os.geteuid() == 0, "root reads a mode-000 file")
    def test_an_unreadable_listed_file_refuses_the_list(self) -> None:
        lever = self.script("lever", U31_SHAPE)
        unreadable = self.script("unreadable", "true\n")
        unreadable.chmod(0o000)

        result = self.run_check(lever, unreadable)

        self.assertEqual(2, result.returncode, result.stdout + result.stderr)
        self.assertIn(f"cannot read {unreadable}; the list is refused", result.stderr)
        self.assertEqual("", result.stdout)

    def test_a_missing_file_or_an_empty_list_refuses(self) -> None:
        for paths in ((self.temp_dir / "absent",), ()):
            with self.subTest(paths=paths):
                result = self.run_check(*paths)

                self.assertEqual(2, result.returncode, result.stdout + result.stderr)
                self.assertIn("refused", result.stderr)

    def test_a_substitution_split_across_lines_is_reported_where_the_dirname_opens(self) -> None:
        shapes = {
            "continued": 'dir=$(cd \\\n    "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)\n',
            "multiline": 'dir=$(\n    cd "$(dirname "$0")" && pwd -P\n)\n',
            "quoted": 'dir="$(cd "\n$(basename "$0")")"\n',
        }
        for name, body in shapes.items():
            with self.subTest(shape=name):
                lever = self.script(name, body)

                result = self.run_check(lever)

                self.assertEqual(1, result.returncode, result.stderr)
                self.assertTrue(result.stdout.startswith(f"{lever}:3: a $(dirname) or $(basename)"), result.stdout)
                self.assertEqual(1, result.stdout.count("\n"), result.stdout)

    def test_an_unquoted_heredoc_body_is_read_as_expanded_text(self) -> None:
        # The apostrophe is plain text in the body; a line scan read it as an open single quote.
        lever = self.script("lever", 'cat <<EOF\nit\'s $(cd "$(dirname "$0")" && pwd)\nEOF\n')
        tabbed = self.script("tabbed", '\tcat <<-END\n\tsee $(cd "$(dirname "$0")")\n\tEND\n')

        for path in (lever, tabbed):
            with self.subTest(path=path.name):
                result = self.run_check(path)

                self.assertEqual(1, result.returncode, result.stderr)
                self.assertIn(f"{path}:3: a $(dirname) or $(basename)", result.stdout)

    def test_a_quoted_heredoc_body_and_a_multiline_single_quote_are_literal(self) -> None:
        clean = self.script(
            "clean",
            'cat <<\'EOF\'\ndir=$(cd "$(dirname "$0")")\nEOF\n'
            'cat <<"END"\n$(cd "$(dirname x)")\nEND\n'
            'cat <<\\STOP\n$(cd "$(basename x)")\nSTOP\n'
            "printf '%s\\n' 'line one\n$(cd \"$(dirname x)\")\n'\n"
            'read -r a <<< "$(cat)"\n'
            "x=$((1 << 2))\n",
        )

        result = self.run_check(clean)

        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertEqual("", result.stdout)

    def test_the_scan_resumes_after_a_heredoc_and_a_here_string(self) -> None:
        lever = self.script(
            "lever",
            "cat <<'EOF'\nit's literal\nEOF\nwhile read -r x; do :; done <<< \"${list}\"\n" + U31_SHAPE,
        )

        result = self.run_check(lever)

        self.assertEqual(1, result.returncode, result.stderr)
        self.assertIn(f"{lever}:6: a $(dirname) or $(basename)", result.stdout)

    def test_an_inner_opener_split_from_its_dirname_or_basename_is_reported_where_the_command_starts(self) -> None:
        shapes = {
            "newline": ('dir=$(cd "$(\n    dirname "$0")" && pwd -P)\n', 3),
            "continuation": ('name=$(printf %s "$( \\\n    basename "$0")")\n', 3),
            "blank line": ('dir=$(cd "$(\n\n  dirname -- "$0")")\n', 4),
            "same-line blank": ('dir=$(cd "$( dirname "$0")")\n', 2),
        }
        for name, (body, line) in shapes.items():
            with self.subTest(shape=name):
                lever = self.script(name.replace(" ", "-"), body)

                result = self.run_check(lever)

                self.assertEqual(1, result.returncode, result.stderr)
                self.assertEqual(
                    f"{lever}:{line}: a $(dirname) or $(basename) inside another command substitution loses its"
                    " status; capture it first or split the path in the shell\n",
                    result.stdout,
                )

    def test_every_quoted_delimiter_form_ends_its_heredoc_and_the_scan_resumes(self) -> None:
        # Each body is literal (a nested dirname and an apostrophe that must not count), and the U31 shape after
        # each heredoc must be reported: the delimiter was found, so the walk resumed as code.
        forms = {
            "ANSI-C": ("cat <<$'EOF'", "EOF"),
            "locale": ('cat <<$"EOF"', "EOF"),
            "single then unquoted": ("cat <<'E'OF", "EOF"),
            "unquoted then double": ('cat <<E"O"F', "EOF"),
            "double then single": ("cat <<\"E\"'O'F", "EOF"),
            "backslash": ("cat <<\\EOF", "EOF"),
        }
        lines, expected = ["#!/usr/bin/env bash"], []
        for operator, terminator in forms.values():
            lines += [operator, 'it\'s $(cd "$(dirname "$0")")', terminator, U31_SHAPE.rstrip("\n")]
            expected.append(len(lines))
        lever = self.temp_dir / "forms"
        lever.write_text("\n".join(lines) + "\n")

        result = self.run_check(lever)

        self.assertEqual(1, result.returncode, result.stderr)
        self.assertEqual([f"{lever}:{n}" for n in expected], [x.split(": a ")[0] for x in result.stdout.splitlines()])

    def test_a_comment_or_a_split_command_word_inside_the_inner_substitution_is_reported(self) -> None:
        # Round-2 audit shapes a lexical scan missed: a comment between `$(` and its command word, a command word
        # split by a line continuation; and quoting, a `case` pattern's `)` and backquotes the parser resolves.
        shapes = {
            "comment": ('dir=$(cd "$(\n    # Locate this script.\n    dirname "$0")" && pwd -P)\n', 4),
            "continued word": ('dir=$(cd "$(dir\\\nname "$0")" && pwd -P)\n', 2),
            "escaped word": ('dir=$(cd "$(\\dirname "$0")")\n', 2),
            "quoted word": ('name=$(printf %s "$("basename" "$0")")\n', 2),
            "ansi-c word": ("dir=$(cd \"$($'dirname' \"$0\")\")\n", 2),
            "ansi-c escaped word": ("dir=$(cd \"$($'dir\\x6eame' \"$0\")\")\n", 2),
            "ansi-c wrapped octal word": ("dir=$(cd \"$($'\\544irname' \"$0\")\")\n", 2),
            "locale-quoted word": ('dir=$(cd "$($"dirname" "$0")")\n', 2),
            "command prefix": ('dir=$(cd "$(command -p dirname "$0")")\n', 2),
            "exec prefix": ('dir=$(cd "$(exec basename "$0")")\n', 2),
            "case pattern": ('x=$(case $y in\n  a) echo "$(dirname "$y")" ;;\nesac)\n', 3),
            "backquotes": ('x=$(cd "`dirname "$0"`")\n', 2),
        }
        for name, (body, line) in shapes.items():
            with self.subTest(shape=name):
                lever = self.script(name.replace(" ", "-"), body)

                result = self.run_check(lever)

                self.assertEqual(1, result.returncode, result.stderr)
                self.assertEqual(
                    f"{lever}:{line}: a $(dirname) or $(basename) inside another command substitution loses its"
                    " status; capture it first or split the path in the shell\n",
                    result.stdout,
                )

    def test_a_command_word_with_an_expansion_is_not_a_literal_dirname(self) -> None:
        clean = self.script("clean", 'dir=$(cd "$("${tool}" "$0")")\ndir=$(cd "$(dirname$x "$0")")\n')

        result = self.run_check(clean)

        self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_a_file_shfmt_cannot_parse_refuses_the_list(self) -> None:
        bodies = {
            "substitution": 'x=$(cd "$y"\n',
            "single-quote": "echo 'never closed\n",
            "heredoc": "cat <<EOF\nno terminator\n",
        }
        for name, body in bodies.items():
            with self.subTest(shape=name):
                broken = self.script(name, body)

                result = self.run_check(broken)

                self.assertEqual(2, result.returncode, result.stdout + result.stderr)
                self.assertIn(f"shfmt cannot parse {broken}; the list is refused", result.stderr)
                self.assertEqual("", result.stdout)

    def test_an_ansi_c_delimiter_with_escapes_is_refused_as_shellcheck_refuses_it(self) -> None:
        # bash decodes `$'\x45OF'` to EOF, but neither shfmt 3.14.1 nor ShellCheck 0.11.0 does: both read the
        # heredoc as unterminated. `make shellcheck` fails such a file through ShellCheck (SC1044) whatever this
        # check does, so the check refuses it too rather than read an unparsed file as clean.
        forms = {"hex": "\\x45OF", "octal": "\\105OF", "escaped quote": "E\\'OF"}
        for name, escaped in forms.items():
            with self.subTest(form=name):
                terminator = escaped.encode().decode("unicode_escape")
                path = self.script(name.replace(" ", "-"), f"cat <<$'{escaped}'\nbody\n{terminator}\necho after\n")

                result = self.run_check(path)

                self.assertEqual(2, result.returncode, result.stdout + result.stderr)
                self.assertIn(f"shfmt cannot parse {path}; the list is refused", result.stderr)
                if shutil.which("shellcheck"):
                    lint = subprocess.run(["shellcheck", str(path)], capture_output=True, text=True, check=False)
                    self.assertIn("SC1044", lint.stdout)

    def test_a_missing_shfmt_refuses_the_list(self) -> None:
        clean = self.script("clean", "true\n")

        result = self.run_check(clean, env=os.environ | {"SHFMT": str(self.temp_dir / "no-shfmt")})

        self.assertEqual(2, result.returncode, result.stdout + result.stderr)
        self.assertIn("no-shfmt not found; the list is refused", result.stderr)


if __name__ == "__main__":
    unittest.main()
