import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[2]
HOOK_PATH = ROOT / "home/dot_claude/hooks/executable_format-edited-files.py"

_spec = importlib.util.spec_from_file_location("format_edited_files", HOOK_PATH)
assert _spec is not None and _spec.loader is not None
format_edited_files = importlib.util.module_from_spec(_spec)
sys.modules[_spec.name] = format_edited_files
_spec.loader.exec_module(format_edited_files)


_real_run = subprocess.run


class RecordingRun:
    """Records every subprocess.run call as (argv, cwd); runs `git` for real
    (needed so repository_root() resolves against an actual temp repo) and
    fakes every other command (no real ruff/prettier/ty execution)."""

    def __init__(self):
        self.calls: list[tuple[list[str], Path | None]] = []

    def __call__(self, argv, *, cwd=None, **kwargs):
        del kwargs
        self.calls.append((list(argv), Path(cwd) if cwd is not None else None))
        if argv and argv[0] == "git":
            return _real_run(argv, cwd=cwd, capture_output=True, text=True, check=False)
        return subprocess.CompletedProcess(argv, 0)

    def formatter_calls(self, tool: str) -> list[tuple[list[str], Path | None]]:
        return [(argv, cwd) for argv, cwd in self.calls if argv and argv[0] == tool]


class TestFormatEditedFiles(unittest.TestCase):
    def setUp(self):
        self._tmp = mock.patch.object(sys, "dont_write_bytecode", True)
        self._tmp.start()
        self.addCleanup(self._tmp.stop)

    def _init_repo(self, root: Path) -> None:
        subprocess.run(["git", "init", "-q", str(root)], check=True)

    def test_groups_by_repository_root_and_forces_ruff_exclusions(self):
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp).resolve()
            repo = tmp_path / "repo"
            repo.mkdir()
            self._init_repo(repo)
            (repo / ".prettierignore").write_text("kit/\n", encoding="utf-8")

            kit_dir = repo / "kit"
            kit_dir.mkdir()
            other_dir = repo / "other"
            other_dir.mkdir()
            md_a = kit_dir / "a.md"
            md_a.write_text("# a\n", encoding="utf-8")
            md_b = other_dir / "b.md"
            md_b.write_text("# b\n", encoding="utf-8")

            outside_dir = tmp_path / "outside"
            outside_dir.mkdir()
            py_outside = outside_dir / "c.py"
            py_outside.write_text("x = 1\n", encoding="utf-8")

            payload = {
                "tool_input": {
                    "file_path": str(md_a),
                    "extra": [
                        {"file_path": str(md_b)},
                        {"path": str(py_outside)},
                    ],
                },
            }

            recorder = RecordingRun()
            with (
                mock.patch.object(format_edited_files.subprocess, "run", recorder),
                mock.patch.object(
                    sys, "stdin", mock.Mock(read=lambda: json.dumps(payload))
                ),
            ):
                status = format_edited_files.main()

            self.assertEqual(status, 0)

            prettier_calls = recorder.formatter_calls("npx")
            self.assertEqual(len(prettier_calls), 1)
            argv, cwd = prettier_calls[0]
            self.assertEqual(cwd, repo)
            self.assertIn("--ignore-path", argv)
            self.assertEqual(
                argv[argv.index("--ignore-path") + 1], str(repo / ".prettierignore")
            )
            relative_files = {
                a
                for a in argv
                if a
                not in {
                    "npx",
                    "prettier@2",
                    "--write",
                    "--ignore-path",
                    str(repo / ".prettierignore"),
                }
            }
            self.assertEqual(relative_files, {"kit/a.md", "other/b.md"})

            ruff_calls = recorder.formatter_calls("uvx")
            self.assertTrue(
                ruff_calls, "expected ruff invocations for the outside .py file"
            )
            for argv, cwd in ruff_calls:
                if "ty" in argv:
                    self.assertNotIn("--force-exclude", argv)
                    continue
                self.assertIn("--force-exclude", argv)
                self.assertEqual(cwd, outside_dir)
                self.assertIn("c.py", argv)


if __name__ == "__main__":
    unittest.main()
