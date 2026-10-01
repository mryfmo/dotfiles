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
        path = path.replace("__", "/").replace("_py", ".py").replace("_rb", ".rb").replace("_sh", ".sh")
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
            (self.repo / name.replace("_py", ".py").replace("_rb", ".rb").replace("_sh", ".sh")).write_text(text)
        subprocess.run(["git", "add", "-A"], cwd=self.repo, check=True)
        subprocess.run(
            ["git", "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-qm", "c"],
            cwd=self.repo,
            check=True,
        )

    def run_coverage(
        self, old: dict, new: dict, ref: str = "HEAD", old_ref: str | None = None
    ) -> subprocess.CompletedProcess[str]:
        (self.repo / "old.json").write_text(json.dumps(old))
        (self.repo / "new.json").write_text(json.dumps(new))
        refs = [f"--repo-ref={ref}"] + ([f"--old-ref={old_ref}"] if old_ref else [])
        return subprocess.run(
            [sys.executable, str(SCRIPT), "old.json", "new.json", *refs],
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

    def test_deleted_path_with_old_ref_is_explained(self) -> None:
        self.commit(a_py=defs("one", "two"), b_py=defs("keep"))
        (self.repo / "a.py").unlink()
        self.commit()

        result = self.run_coverage(
            graph(a_py=("one", "two"), b_py=("keep",)),
            graph(b_py=("keep",)),
            old_ref="HEAD~1",
        )
        self.assertEqual(0, result.returncode, result.stdout)
        self.assertIn("| a.py | 2 | 0 | gone | explained |", result.stdout)

    def test_absent_path_without_old_ref_is_regression(self) -> None:
        self.commit(a_py=defs("one", "two"), b_py=defs("keep"))
        (self.repo / "a.py").unlink()
        self.commit()

        result = self.run_coverage(
            graph(a_py=("one", "two"), b_py=("keep",)), graph(b_py=("keep",))
        )
        self.assertEqual(1, result.returncode, result.stdout)
        self.assertIn("| a.py | 2 | 0 | gone | REGRESSION |", result.stdout)

    def rename_a_to_b(self) -> None:
        (self.repo / "pkg").mkdir()
        (self.repo / "pkg/a.py").write_text(defs("one", "two"))
        self.commit()
        subprocess.run(["git", "mv", "pkg/a.py", "pkg/b.py"], cwd=self.repo, check=True)
        self.commit()

    def test_rename_preserving_symbols_is_ok(self) -> None:
        self.rename_a_to_b()

        result = self.run_coverage(
            graph(pkg__a_py=("one", "two")),
            graph(pkg__b_py=("one", "two")),
            old_ref="HEAD~1",
        )
        self.assertEqual(0, result.returncode, result.stdout)
        self.assertIn("| pkg/a.py | 2 | 2 | renamed → pkg/b.py | ok |", result.stdout)

    def test_rename_dropping_symbols_is_regression(self) -> None:
        self.rename_a_to_b()

        result = self.run_coverage(
            graph(pkg__a_py=("one", "two")), graph(pkg__b_py=()), old_ref="HEAD~1"
        )
        self.assertEqual(1, result.returncode, result.stdout)
        self.assertIn(
            "| pkg/a.py | 2 | 0 | renamed → pkg/b.py | REGRESSION |", result.stdout
        )
        self.assertIn("regressions: 1", result.stdout)

    def test_partial_deletion_in_changed_source_is_regression(self) -> None:
        self.commit(a_py=defs("one"))
        old = graph(a_py=("one", "two"))

        extra_loss = self.run_coverage(old, graph(a_py=()))
        self.assertEqual(1, extra_loss.returncode, extra_loss.stdout)
        self.assertIn("| a.py | 2 | 0 | 1 | REGRESSION |", extra_loss.stdout)

        accounted = self.run_coverage(old, graph(a_py=("one",)))
        self.assertEqual(1, accounted.returncode, accounted.stdout)
        self.assertIn("| a.py | 2 | 1 | 1 | REGRESSION |", accounted.stdout)

    def test_def_column_reads_the_new_graph_revision(self) -> None:
        self.commit(a_py=defs("one", "two"))
        self.commit(a_py=defs("one"))
        old, new = graph(a_py=("one", "two")), graph(a_py=("one",))

        deleted_at_ref = self.run_coverage(old, new, ref="HEAD")
        self.assertEqual(1, deleted_at_ref.returncode, deleted_at_ref.stdout)
        self.assertIn("| a.py | 2 | 1 | 1 | REGRESSION |", deleted_at_ref.stdout)

        unchanged_at_ref = self.run_coverage(old, new, ref="HEAD~1")
        self.assertEqual(1, unchanged_at_ref.returncode, unchanged_at_ref.stdout)
        self.assertIn("| a.py | 2 | 1 | 2 | REGRESSION |", unchanged_at_ref.stdout)

    def test_uv_run_script_shebang_is_python(self) -> None:
        self.commit(tool="#!/usr/bin/env -S uv run --script\n" + defs("one"))

        result = self.run_coverage(graph(tool=("one", "two")), graph(tool=("one",)))
        self.assertEqual(1, result.returncode, result.stdout)
        self.assertIn("| tool | 2 | 1 | 1 | REGRESSION |", result.stdout)

    def test_unchanged_source_loss_is_noted(self) -> None:
        self.commit(a_py=defs("one", "two"))
        self.commit(b_py=defs("other"))
        old, new = graph(a_py=("one", "two", "nested")), graph(a_py=("one", "two"))

        by_defs = self.run_coverage(old, new)
        self.assertEqual(1, by_defs.returncode, by_defs.stdout)
        self.assertIn("| a.py | 3 | 2 | 2 | REGRESSION |  |", by_defs.stdout)

        unchanged = self.run_coverage(old, new, old_ref="HEAD~1")
        self.assertEqual(1, unchanged.returncode, unchanged.stdout)
        self.assertIn(
            "| a.py | 3 | 2 | 2 | REGRESSION | source unchanged |", unchanged.stdout
        )

    def test_ruby_visibility_prefixed_defs_are_counted(self) -> None:
        self.commit(
            lib_rb="class A\n  def one\n  end\n\n  private def two\n  end\nend\n"
        )

        result = self.run_coverage(graph(lib_rb=("A", "one", "two")), graph(lib_rb=("A", "one")))
        self.assertEqual(1, result.returncode, result.stdout)
        self.assertIn("| lib.rb | 3 | 2 | 3 | REGRESSION |", result.stdout)

    def test_low_similarity_move_with_no_symbols_is_regression(self) -> None:
        self.commit(a_py=defs("one", "two"))
        (self.repo / "a.py").unlink()
        self.commit(b_py=defs("one", "two") + "".join(f"x{i} = {i}\n" for i in range(80)))

        result = self.run_coverage(
            graph(a_py=("one", "two")), graph(b_py=()), old_ref="HEAD~1"
        )
        self.assertEqual(1, result.returncode, result.stdout)
        self.assertIn("| a.py | 2 | 0 | gone | explained |", result.stdout)
        self.assertIn(
            "| b.py | 0 | 0 | 2 | REGRESSION | new file, no symbols |", result.stdout
        )

    def test_partially_covered_new_file_is_not_flagged(self) -> None:
        # Documented ceiling: def-like lines overcount graph nodes, so only a
        # new file with zero symbols is flagged.
        self.commit(a_py=defs("keep"))
        self.commit(b_py=defs("one", "two"))

        result = self.run_coverage(
            graph(a_py=("keep",)), graph(a_py=("keep",), b_py=("one",)), old_ref="HEAD~1"
        )
        self.assertEqual(0, result.returncode, result.stdout)
        self.assertIn("| b.py | 0 | 1 | 2 | ok |  |", result.stdout)

    def test_shell_names_with_punctuation_are_counted(self) -> None:
        self.commit(
            s_sh="foo?() {\n  :\n}\nfunction bar@baz {\n  :\n}\narr=()\n"
        )

        result = self.run_coverage(graph(s_sh=("a", "b")), graph(s_sh=("a", "b")))
        self.assertEqual(0, result.returncode, result.stdout)
        self.assertIn("| s.sh | 2 | 2 | 2 | ok |", result.stdout)

    def test_comment_lines_are_not_definitions(self) -> None:
        self.commit(s_sh="real() {\n  :\n}\n#disabled() { :; }\n  # gone() {\n")

        result = self.run_coverage(graph(), graph(s_sh=("real",)))
        self.assertEqual(0, result.returncode, result.stdout)
        self.assertIn("| s.sh | 0 | 1 | 1 | ok |", result.stdout)

    def test_python_defs_inside_strings_do_not_count(self) -> None:
        self.commit(doc_py='DOC = """\ndef not_a_real_function():\n"""\n')

        result = self.run_coverage(graph(), graph(doc_py=()))
        self.assertEqual(0, result.returncode, result.stdout)
        self.assertIn("| doc.py | 0 | 0 | 0 | ok |", result.stdout)

    def test_grammar_file_missing_from_graph_fails_in_covered_directories(self) -> None:
        self.commit(a_py=defs("keep"), b_py=defs("one", "two"))
        (self.repo / "sub").mkdir()
        (self.repo / "sub/c.py").write_text(defs("three"))
        self.commit()
        unchanged = graph(a_py=("keep",))

        result = self.run_coverage(unchanged, unchanged)
        self.assertEqual(1, result.returncode, result.stdout)
        self.assertIn("| b.py | 0 | 0 | 2 | REGRESSION | missing from graph |", result.stdout)
        self.assertNotIn("sub/c.py", result.stdout)
        self.assertIn("regressions: 1", result.stdout)


if __name__ == "__main__":
    unittest.main()
