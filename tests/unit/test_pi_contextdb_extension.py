#!/usr/bin/env python3
"""Run the Pi CompactionDB extension tests with repository-provided tools."""

from __future__ import annotations

import shutil
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EXTENSION = ROOT / "home/dot_pi/agent/extensions/contextdb.ts"
NODE_TEST = ROOT / "tests/unit/pi_contextdb_extension.test.mjs"
TYPE_DECLARATIONS = ROOT / "tests/unit/pi_contextdb_extension_types.d.ts"


class PiContextdbExtensionTest(unittest.TestCase):
    def test_node_behavior_suite(self) -> None:
        result = subprocess.run(
            ["node", "--test", str(NODE_TEST)],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_typescript_contract(self) -> None:
        tsc = shutil.which("tsc")
        if tsc is None:
            self.skipTest("tsc unavailable; node --check is the syntax fallback")
        result = subprocess.run(
            [
                tsc,
                "--noEmit",
                "--target",
                "ES2022",
                "--module",
                "NodeNext",
                "--moduleResolution",
                "NodeNext",
                "--skipLibCheck",
                str(TYPE_DECLARATIONS),
                str(EXTENSION),
            ],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_node_syntax_fallback(self) -> None:
        result = subprocess.run(
            ["node", "--check", str(EXTENSION)],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout)


if __name__ == "__main__":
    unittest.main()

