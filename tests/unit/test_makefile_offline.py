"""The two validator recipes run from the uv cache when it holds PyYAML, through the index only when it does not.

Plan 022 T5. `make -C <root> validate-agent-assets` runs with a stub `uv` first on PATH: it appends its argv as one
line to a log, and exits with $PROBE_RC for the probe (argv ending in `-c import yaml`) and $RUN_RC otherwise.
"""

import os
import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
STUB = """#!/usr/bin/env bash
echo "$*" >> "$UV_LOG"
if [ "${*: -2}" = "-c import yaml" ]; then exit "$PROBE_RC"; fi
exit "$RUN_RC"
"""
PROBE = "run --offline --with pyyaml python -c import yaml"


class MakefileOfflineTest(unittest.TestCase):
    def test_validator_targets_try_the_offline_form_first(self):
        makefile = (ROOT / "Makefile").read_text()
        definition = re.search(r"^UV_PYYAML = (.*)$", makefile, re.MULTILINE)[1]
        self.assertIn("uv run --offline --with pyyaml", definition)
        self.assertIn("uv run --with pyyaml", definition)
        self.assertIn("validate-agent-assets:\n\t$(UV_PYYAML) scripts/validate-agent-assets.py\n", makefile)
        self.assertIn("render-check:\n\t$(UV_PYYAML) scripts/generate-agent-configs.py --check\n", makefile)

    def test_the_recipe_falls_back_only_when_the_cache_is_cold(self):
        offline = "run --offline --with pyyaml scripts/validate-agent-assets.py"
        index = "run --with pyyaml scripts/validate-agent-assets.py"
        for probe_rc, run_rc, expected, succeeds in (
            ("0", "0", [PROBE, offline], True),
            ("1", "0", [PROBE, index], True),
            # A validator finding is not retried: the probe runs no validator.
            ("0", "1", [PROBE, offline], False),
        ):
            with self.subTest(probe_rc=probe_rc, run_rc=run_rc), tempfile.TemporaryDirectory() as directory:
                bin_dir, log = Path(directory) / "bin", Path(directory) / "uv.log"
                bin_dir.mkdir()
                (bin_dir / "uv").write_text(STUB)
                (bin_dir / "uv").chmod(0o755)
                env = {**os.environ, "PATH": f"{bin_dir}{os.pathsep}{os.environ['PATH']}", "UV_LOG": str(log)}
                result = subprocess.run(
                    [shutil.which("make"), "-C", str(ROOT), "validate-agent-assets"],
                    env={**env, "PROBE_RC": probe_rc, "RUN_RC": run_rc},
                    capture_output=True,
                    text=True,
                    timeout=60,
                    check=False,
                )
                self.assertEqual(succeeds, result.returncode == 0, result.stdout + result.stderr)
                self.assertEqual(expected, log.read_text().splitlines())


if __name__ == "__main__":
    unittest.main()
