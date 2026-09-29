"""Tests for scripts/ua-symbol-coverage.py."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts/ua-symbol-coverage.py"


def graph(*symbols: str) -> dict:
    nodes = [{"id": "file:a.py", "type": "file", "filePath": "a.py"}]
    nodes += [
        {"id": f"function:a.py:{name}", "type": "function", "filePath": "a.py"}
        for name in symbols
    ]
    return {"nodes": nodes, "edges": []}


class UaSymbolCoverageTest(unittest.TestCase):
    def test_flags_unexplained_symbol_loss_only(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            repo = Path(temporary)
            subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
            (repo / "a.py").write_text(
                "def one():\n    pass\n\n\ndef two():\n    pass\n"
            )
            subprocess.run(["git", "add", "a.py"], cwd=repo, check=True)
            subprocess.run(
                [
                    "git",
                    "-c",
                    "user.name=t",
                    "-c",
                    "user.email=t@t",
                    "commit",
                    "-qm",
                    "a",
                ],
                cwd=repo,
                check=True,
            )
            old, dropped, kept = (
                repo / "old.json",
                repo / "dropped.json",
                repo / "kept.json",
            )
            old.write_text(json.dumps(graph("one", "two")))
            dropped.write_text(json.dumps(graph("one")))
            kept.write_text(json.dumps(graph("one", "two", "three")))

            def run(new: Path) -> subprocess.CompletedProcess[str]:
                return subprocess.run(
                    [
                        sys.executable,
                        str(SCRIPT),
                        str(old),
                        str(new),
                        "--repo-ref",
                        "HEAD",
                    ],
                    cwd=repo,
                    capture_output=True,
                    text=True,
                    check=False,
                )

            regression = run(dropped)
            self.assertEqual(1, regression.returncode, regression.stdout)
            self.assertIn("| a.py | 2 | 1 | 2 | REGRESSION |", regression.stdout)
            self.assertIn("regressions: 1", regression.stdout)

            clean = run(kept)
            self.assertEqual(0, clean.returncode, clean.stdout)
            self.assertIn("| a.py | 2 | 3 | 2 | ok |", clean.stdout)
            self.assertIn("regressions: 0", clean.stdout)


if __name__ == "__main__":
    unittest.main()
