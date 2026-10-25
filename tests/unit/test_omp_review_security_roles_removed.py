"""The omp `review` and `security` seat roles are gone (regime-cutover U72, F071): no launcher started them
(`omp-run.sh` and `hcom-seat` accept orchestrator, worker and audit only), so their manifest roles, rendered
overlays and preflight entries are removed, and `home/.chezmoiremove` deletes the deployed overlays, because
`~/.agents/omp/profiles` is not an exact directory.

The Codex and Claude model profiles named `review` and `security` (`model_profiles`, `~/.codex/<name>.config.toml`)
are a different thing and stay. The dry run applies a scratch source that holds only the real
`home/.chezmoiremove` to a scratch HOME, so it exercises exactly the removal entries.
"""

import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RETIRED = ("review", "security")
REMOVALS = tuple(f".agents/omp/profiles/{role}.yml" for role in RETIRED)


class OmpReviewSecurityRolesRemovedTest(unittest.TestCase):
    def test_only_the_seat_overlays_render_and_the_model_profiles_stay(self):
        # The generator renders one overlay per manifest omp role, and `generate-agent-configs.py --check` (CI's render
        # check) fails when the rendered set and the roles differ, so the rendered set is the role list. The Codex
        # profile scripts are rendered per model profile, so theirs is the model-profile list. No PyYAML needed.
        overlays = sorted(p.name for p in (ROOT / "home/dot_agents/omp/profiles").iterdir())
        self.assertEqual(["audit.yml.tmpl", "orchestrator.yml.tmpl", "worker.yml.tmpl"], overlays)
        for role in RETIRED:
            with self.subTest(role=role):
                self.assertTrue((ROOT / f"home/dot_codex/modify_private_{role}.config.toml").is_file())

    def test_chezmoiremove_lists_the_deployed_overlays(self):
        entries = [line.strip() for line in (ROOT / "home/.chezmoiremove").read_text().splitlines()]
        for entry in REMOVALS:
            with self.subTest(entry=entry):
                self.assertIn(entry, entries)

    @unittest.skipUnless(shutil.which("chezmoi"), "chezmoi is not installed")
    def test_apply_removes_the_retired_overlays_and_keeps_the_seat_overlays(self):
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            source, home = base / "source", base / "home"
            source.mkdir()
            shutil.copy(ROOT / "home/.chezmoiremove", source / ".chezmoiremove")
            for role in ("orchestrator", "worker", "audit", *RETIRED):
                overlay = home / f".agents/omp/profiles/{role}.yml"
                overlay.parent.mkdir(parents=True, exist_ok=True)
                overlay.write_text("modelRoles: {}\n")
            config = base / "chezmoi.toml"
            config.write_text("")
            run = subprocess.run(
                [
                    *("chezmoi", "apply", "--force", "--no-tty"),
                    *("--source", str(source), "--destination", str(home), "--config", str(config)),
                    *("--cache", str(base / "cache"), "--persistent-state", str(base / "state.boltdb")),
                ],
                env={k: v for k, v in os.environ.items() if k != "CI"} | {"HOME": str(home)},
                capture_output=True,
                text=True,
                timeout=120,
                check=False,
            )
            self.assertEqual(0, run.returncode, run.stderr)
            left = sorted(p.name for p in (home / ".agents/omp/profiles").iterdir())
            self.assertEqual(["audit.yml", "orchestrator.yml", "worker.yml"], left)


if __name__ == "__main__":
    unittest.main()
