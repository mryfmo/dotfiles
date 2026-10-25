from __future__ import annotations

import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HOOK = ROOT / "home/dot_claude/hooks/executable_format-edited-files.py"


@unittest.skipUnless(shutil.which("prettier"), "prettier is not installed")
class FormatEditedFilesTest(unittest.TestCase):
    def test_project_prettier_config_code_never_runs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            subprocess.run(["git", "init", "-q", str(repo)], check=True)
            marker = repo / "MARKER"
            # A sandboxed command can write this file; the hook runs outside the sandbox.
            (repo / "prettier.config.js").write_text(
                f'require("fs").writeFileSync({json.dumps(str(marker))}, "ran");\nmodule.exports = {{ tabWidth: 8 }};\n'
            )
            document = repo / "a.md"
            document.write_text("# T\n\n*  a\n")
            result = subprocess.run(
                [str(HOOK)],
                input=json.dumps({"tool_input": {"file_path": str(document)}}),
                capture_output=True,
                text=True,
                check=False,
                env=os.environ,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertFalse(marker.exists())
            self.assertEqual(document.read_text(), "# T\n\n- a\n")


if __name__ == "__main__":
    unittest.main()
