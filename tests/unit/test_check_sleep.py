"""Exercise scripts/check-sleep.sh, make doctor's sleep check, with a stub uname and a stub pmset on PATH.

The script runs as a subprocess; the stubs are written into a temporary directory that leads PATH, so no real
pmset or uname is consulted and nothing is changed.
"""

import os
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts/check-sleep.sh"
DISABLED = "#!/bin/bash\nprintf ' SleepDisabled\\t\\t%s\\n hibernatemode\\t\\t3\\n' {value}\n"


class CheckSleepTest(unittest.TestCase):
    def run_check(self, system, pmset_body):
        with tempfile.TemporaryDirectory() as temp:
            bin_dir = Path(temp) / "bin"
            bin_dir.mkdir()
            for name, body in (("uname", f"#!/bin/bash\necho {system}\n"), ("pmset", pmset_body)):
                stub = bin_dir / name
                stub.write_text(body)
                stub.chmod(0o755)
            env = {**os.environ, "PATH": f"{bin_dir}{os.pathsep}{os.environ['PATH']}"}
            return subprocess.run(["bash", str(SCRIPT)], env=env, capture_output=True, text=True, check=False)

    def test_check_sleep_fails_unless_sleepdisabled_is_1_on_macos_and_warns_on_linux(self):
        cases = (
            ("Darwin", DISABLED.format(value=1), 0, "sleep check: SleepDisabled is 1"),
            (
                "Darwin",
                DISABLED.format(value=0),
                1,
                "sleep check: SleepDisabled is 0; run: sudo pmset -a disablesleep 1",
            ),
            (
                "Darwin",
                "#!/bin/bash\nprintf ' hibernatemode\\t\\t3\\n'\n",
                1,
                "no SleepDisabled line; run: sudo pmset -a disablesleep 1",
            ),
            (
                "Darwin",
                "#!/bin/bash\necho 'pmset: no power source' >&2\nexit 2\n",
                1,
                "pmset -g failed: pmset: no power source",
            ),
            ("Linux", "#!/bin/bash\nexit 99\n", 0, "sleep check: skipped (not macOS)"),
        )
        for system, pmset_body, code, text in cases:
            with self.subTest(system=system, expect=text):
                result = self.run_check(system, pmset_body)
                self.assertEqual(code, result.returncode, result.stdout + result.stderr)
                self.assertIn(text, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
