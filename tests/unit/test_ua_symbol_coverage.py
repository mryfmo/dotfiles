"""Tests for home/dot_local/bin/common/executable_ua-symbol-coverage."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "home/dot_local/bin/common/executable_ua-symbol-coverage"


def graph(**files: tuple[str, ...]) -> dict:
    nodes = []
    for path, symbols in files.items():
        path = path.replace("__", "/").replace("_py", ".py")
        nodes.append({"id": f"file:{path}", "type": "file", "filePath": path})
        nodes += [
            {"id": f"function:{path}:{name}", "type": "function", "filePath": path}
            for name in symbols
        ]
    return {"nodes": nodes, "edges": []}


def defs(*names: str) -> str:
    return "".join(f"def {name}():\n    pass\n\n\n" for name in names)


class UaSymbolCoverageTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.repo = Path(self.temporary.name)
        subprocess.run(["git", "init", "-q"], cwd=self.repo, check=True)

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def commit(self, **files: str) -> None:
        for name, text in files.items():
            (self.repo / name.replace("_py", ".py")).write_text(text)
        subprocess.run(["git", "add", "-A"], cwd=self.repo, check=True)
        subprocess.run(
            ["git", "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-qm", "c"],
            cwd=self.repo,
            check=True,
        )

    def run_coverage(
        self, old: dict, new: dict, ref: str = "HEAD"
    ) -> subprocess.CompletedProcess[str]:
        (self.repo / "old.json").write_text(json.dumps(old))
        (self.repo / "new.json").write_text(json.dumps(new))
        return subprocess.run(
            [sys.executable, str(SCRIPT), "old.json", "new.json", f"--repo-ref={ref}"],
            cwd=self.repo,
            capture_output=True,
            text=True,
            check=False,
        )

    def test_flags_unexplained_symbol_loss_only(self) -> None:
        self.commit(a_py=defs("one", "two"))
        old = graph(a_py=("one", "two"))

        regression = self.run_coverage(old, graph(a_py=("one",)))
        self.assertEqual(1, regression.returncode, regression.stdout)
        self.assertIn("| a.py | 2 | 1 | 2 | REGRESSION |", regression.stdout)
        self.assertIn("regressions: 1", regression.stdout)

        clean = self.run_coverage(old, graph(a_py=("one", "two", "three")))
        self.assertEqual(0, clean.returncode, clean.stdout)
        self.assertIn("| a.py | 2 | 3 | 2 | ok |", clean.stdout)
        self.assertIn("regressions: 0", clean.stdout)

    def test_unresolvable_ref_fails_closed(self) -> None:
        self.commit(a_py=defs("one", "two"))
        for ref in ("no-such-ref", "--output=leak", ""):
            with self.subTest(ref=ref):
                result = self.run_coverage(
                    graph(a_py=("one", "two")), graph(a_py=()), ref=ref
                )
                self.assertEqual(2, result.returncode, result.stdout + result.stderr)
                self.assertIn("ua-symbol-coverage: --repo-ref", result.stderr)
                self.assertNotIn("regressions:", result.stdout)
        self.assertFalse((self.repo / "leak").exists())

    def test_file_gone_at_ref_is_explained(self) -> None:
        self.commit(a_py=defs("one", "two"), b_py=defs("keep"))
        (self.repo / "a.py").unlink()
        self.commit()

        result = self.run_coverage(
            graph(a_py=("one", "two"), b_py=("keep",)), graph(b_py=("keep",))
        )
        self.assertEqual(0, result.returncode, result.stdout)
        self.assertIn("| a.py | 2 | 0 | gone | explained |", result.stdout)

    def test_partial_deletion_is_explained_only_up_to_the_source_loss(self) -> None:
        self.commit(a_py=defs("one"))
        old = graph(a_py=("one", "two"))

        extra_loss = self.run_coverage(old, graph(a_py=()))
        self.assertEqual(1, extra_loss.returncode, extra_loss.stdout)
        self.assertIn("| a.py | 2 | 0 | 1 | REGRESSION |", extra_loss.stdout)

        accounted = self.run_coverage(old, graph(a_py=("one",)))
        self.assertEqual(0, accounted.returncode, accounted.stdout)
        self.assertIn("| a.py | 2 | 1 | 1 | explained |", accounted.stdout)

    def test_ref_is_the_new_graph_revision_not_the_base(self) -> None:
        self.commit(a_py=defs("one", "two"))
        self.commit(a_py=defs("one"))
        old, new = graph(a_py=("one", "two")), graph(a_py=("one",))

        deleted_at_ref = self.run_coverage(old, new, ref="HEAD")
        self.assertEqual(0, deleted_at_ref.returncode, deleted_at_ref.stdout)
        self.assertIn("| a.py | 2 | 1 | 1 | explained |", deleted_at_ref.stdout)

        unchanged_at_ref = self.run_coverage(old, new, ref="HEAD~1")
        self.assertEqual(1, unchanged_at_ref.returncode, unchanged_at_ref.stdout)
        self.assertIn("| a.py | 2 | 1 | 2 | REGRESSION |", unchanged_at_ref.stdout)

    def test_uv_run_script_shebang_is_python(self) -> None:
        self.commit(tool="#!/usr/bin/env -S uv run --script\n" + defs("one"))

        result = self.run_coverage(graph(tool=("one", "two")), graph(tool=("one",)))
        self.assertEqual(0, result.returncode, result.stdout)
        self.assertIn("| tool | 2 | 1 | 1 | explained |", result.stdout)


if __name__ == "__main__":
    unittest.main()
