#!/usr/bin/env python3
"""Exercise the supplemental check for a command substitution nested inside another, the shape SC2312 lets through."""

from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CHECK = ROOT / "scripts/ci/masked-dirname-check.sh"


def on_ci_runner() -> bool:
    """scripts/lib/ci-runner.sh decides, never the generic CI variable an agent shell exports."""
    probe = 'source "$1" && is_ci_runner'
    return (
        subprocess.run(["bash", "-c", probe, "_", str(ROOT / "scripts/lib/ci-runner.sh")], check=False).returncode == 0
    )


# scripts/orchestrator/hcom-seat:58 at 89427c81, the U31 defect its audit found.
MESSAGE = "a command substitution inside another one loses its status; capture it first, or split a path in the shell"

U31_SHAPE = 'dir=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P) || exit 2\n'


@unittest.skipUnless(shutil.which("shfmt") or on_ci_runner(), "needs shfmt off the CI runner (CI puts 3.14.1 on PATH)")
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
            f"{lever}:3: {MESSAGE}\n",
            result.stdout,
        )

    def test_a_basename_of_a_dirname_substitution_is_reported(self) -> None:
        lever = self.script("lever", 'team="$(basename -- "$(dirname -- "${config}")")"\n')

        result = self.run_check(lever)

        self.assertEqual(1, result.returncode, result.stderr)
        self.assertIn(f"{lever}:2: {MESSAGE}", result.stdout)

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
        self.assertEqual(1, result.stdout.count(f":2: {MESSAGE}"))
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

    def test_a_substitution_split_across_lines_is_reported_where_the_inner_one_opens(self) -> None:
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
                self.assertTrue(result.stdout.startswith(f"{lever}:3: {MESSAGE}"), result.stdout)
                self.assertEqual(1, result.stdout.count("\n"), result.stdout)

    def test_an_unquoted_heredoc_body_is_read_as_expanded_text(self) -> None:
        # The apostrophe is plain text in the body; a line scan read it as an open single quote.
        lever = self.script("lever", 'cat <<EOF\nit\'s $(cd "$(dirname "$0")" && pwd)\nEOF\n')
        tabbed = self.script("tabbed", '\tcat <<-END\n\tsee $(cd "$(dirname "$0")")\n\tEND\n')

        for path in (lever, tabbed):
            with self.subTest(path=path.name):
                result = self.run_check(path)

                self.assertEqual(1, result.returncode, result.stderr)
                self.assertIn(f"{path}:3: {MESSAGE}", result.stdout)

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
        self.assertIn(f"{lever}:6: {MESSAGE}", result.stdout)

    def test_an_inner_opener_split_from_its_command_is_reported_where_the_inner_one_opens(self) -> None:
        shapes = {
            "newline": ('dir=$(cd "$(\n    dirname "$0")" && pwd -P)\n', 2),
            "continuation": ('name=$(printf %s "$( \\\n    basename "$0")")\n', 2),
            "blank line": ('dir=$(cd "$(\n\n  dirname -- "$0")")\n', 2),
            "same-line blank": ('dir=$(cd "$( dirname "$0")")\n', 2),
        }
        for name, (body, line) in shapes.items():
            with self.subTest(shape=name):
                lever = self.script(name.replace(" ", "-"), body)

                result = self.run_check(lever)

                self.assertEqual(1, result.returncode, result.stderr)
                self.assertEqual(f"{lever}:{line}: {MESSAGE}\n", result.stdout)

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
        self.assertEqual(
            [f"{lever}:{n}" for n in expected], [x.removesuffix(f": {MESSAGE}") for x in result.stdout.splitlines()]
        )

    def test_the_command_name_is_irrelevant(self) -> None:
        # Spellings bash resolves at run time, a command word that is an expansion, and a command that is neither
        # dirname nor basename: each nested substitution is reported at the line where it opens.
        shapes = {
            "ansi-c wrapped octal word": ('dir=$(cd "$($\'\\544irname\' "$0")")\n', 2),
            "command prefix": ('dir=$(cd "$(command -p dirname "$0")")\n', 2),
            "exec prefix": ('dir=$(cd "$(exec -a x dirname "$0")")\n', 2),
            "absolute path": ('dir=$(cd "$(/usr/bin/dirname "$0")")\n', 2),
            "expansion word": ('dir=$(cd "$("${tool}" "$0")")\n', 2),
            "other command": ('x=$(echo "$(printf %s x)")\n', 2),
            "inner on a later line": ('x=$(echo \\\n  "$(printf %s x)")\n', 3),
        }
        for name, (body, line) in shapes.items():
            with self.subTest(shape=name):
                lever = self.script(name.replace(" ", "-"), body)

                result = self.run_check(lever)

                self.assertEqual(1, result.returncode, result.stderr)
                self.assertEqual(f"{lever}:{line}: {MESSAGE}\n", result.stdout)

    def test_a_comment_a_split_word_a_case_pattern_or_backquotes_inside_the_outer_substitution_are_reported(
        self,
    ) -> None:
        # Round-2 audit shapes a lexical scan missed: a comment between `$(` and its command word, a command word
        # split by a line continuation, a `case` pattern's `)` and backquotes the parser resolves.
        shapes = {
            "comment": ('dir=$(cd "$(\n    # Locate this script.\n    dirname "$0")" && pwd -P)\n', 2),
            "continued word": ('dir=$(cd "$(dir\\\nname "$0")" && pwd -P)\n', 2),
            "case pattern": ('x=$(case $y in\n  a) echo "$(dirname "$y")" ;;\nesac)\n', 3),
            "backquotes": ('x=$(cd "`dirname "$0"`")\n', 2),
        }
        for name, (body, line) in shapes.items():
            with self.subTest(shape=name):
                lever = self.script(name.replace(" ", "-"), body)

                result = self.run_check(lever)

                self.assertEqual(1, result.returncode, result.stderr)
                self.assertEqual(f"{lever}:{line}: {MESSAGE}\n", result.stdout)

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
        # PATH holds only what the check needs besides shfmt (U97: the shfmt is PATH's, no variable selects it).
        clean = self.script("clean", "true\n")
        bare = self.temp_dir / "bare-bin"
        bare.mkdir()
        for tool in ("python3", "cat"):
            (bare / tool).symlink_to(shutil.which(tool))

        result = subprocess.run(
            [shutil.which("bash"), str(CHECK), str(clean)],
            text=True,
            capture_output=True,
            check=False,
            env={"PATH": str(bare)},
            timeout=60,
        )

        self.assertEqual(2, result.returncode, result.stdout + result.stderr)
        self.assertIn("shfmt not found; the list is refused", result.stderr)

    def test_a_shfmt_variable_cannot_select_another_binary(self) -> None:
        # Round-2 audit of 473b63a1: the guard checks PATH's shfmt, so SHFMT pointing elsewhere must change nothing.
        clean = self.script("clean", "x=$(true)\n")  # one substitution: a run that sees none is refused (U105)
        other = self.temp_dir / "other-shfmt"
        other.write_text(f'#!/bin/sh\ntouch "{self.temp_dir}/other-ran"\nexit 0\n')
        other.chmod(0o755)

        result = self.run_check(clean, env=os.environ | {"SHFMT": str(other)})

        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertFalse((self.temp_dir / "other-ran").exists())


if __name__ == "__main__":
    unittest.main()
