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
U31_SHAPE = 'dir=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P) || {\n'


class MaskedDirnameCheckTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = Path(tempfile.mkdtemp(prefix="masked-dirname-check-test-"))

    def tearDown(self) -> None:
        shutil.rmtree(self.temp_dir)

    def script(self, name: str, body: str) -> Path:
        path = self.temp_dir / name
        path.write_text("#!/usr/bin/env bash\n" + body)
        return path

    def run_check(self, *paths: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(["bash", str(CHECK), *map(str, paths)], text=True, capture_output=True, check=False)

    def test_the_u31_shape_is_reported_at_its_line(self) -> None:
        lever = self.script("lever", "set -euo pipefail\n" + U31_SHAPE + "    exit 2\n}\n")

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


if __name__ == "__main__":
    unittest.main()
