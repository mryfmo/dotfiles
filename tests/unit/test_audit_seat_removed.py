"""The long-lived audit seat is gone (regime-cutover U58): every audit is one fresh `omp-run.sh --role audit` run per
head (U57), so the seat's skill, its bus-reply lever and their deployed copies are removed.

The `audit` omp profile, `home/dot_agents/omp/policies/audit.yml` and the openai-siwc extension stay: `omp-run.sh
--role audit` loads them. The dry run applies a scratch source that holds only the real `home/.chezmoiremove` to a
scratch HOME, so it exercises exactly the removal entries and nothing else.
"""

import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
# ~/.agents/skills and ~/.local/bin/common are not exact, so only these entries remove the deployed copies.
REMOVALS = (".agents/skills/hcom-audit", ".claude/skills/hcom-audit", ".local/bin/common/hcom-reply")
GONE = (
    "home/dot_agents/skills/hcom-audit",
    "home/dot_claude/skills/hcom-audit",
    "home/dot_local/bin/common/executable_hcom-reply",
    "tests/unit/test_hcom_reply.py",
)
KEPT = (
    "home/dot_agents/omp/policies/audit.yml",
    "home/dot_agents/omp/extensions/openai-siwc",
    "scripts/orchestrator/omp-run.sh",
)


class AuditSeatRemovedTest(unittest.TestCase):
    def test_the_seat_sources_are_gone_and_the_audit_run_inputs_stay(self):
        for rel in GONE:
            with self.subTest(gone=rel):
                self.assertFalse((ROOT / rel).exists(), rel)
        for rel in KEPT:
            with self.subTest(kept=rel):
                self.assertTrue((ROOT / rel).exists(), rel)

    def test_the_audit_policy_has_no_bus_reply(self):
        self.assertNotIn("hcom-reply", (ROOT / "home/dot_agents/omp/policies/audit.yml").read_text())

    def test_chezmoiremove_removes_the_deployed_skill_and_lever(self):
        entries = [line.strip() for line in (ROOT / "home/.chezmoiremove").read_text().splitlines()]
        for entry in REMOVALS:
            with self.subTest(entry=entry):
                self.assertIn(entry, entries)

    @unittest.skipUnless(shutil.which("chezmoi"), "chezmoi is not installed")
    def test_apply_removes_the_skill_and_the_lever_and_keeps_their_neighbours(self):
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            source, home = base / "source", base / "home"
            source.mkdir()
            shutil.copy(ROOT / "home/.chezmoiremove", source / ".chezmoiremove")
            files = {
                ".agents/skills/hcom-audit/SKILL.md": "retired",
                ".agents/skills/hcom-worker/SKILL.md": "kept",
                ".local/bin/common/hcom-reply": "retired",
                ".local/bin/common/hcom-dispatch": "kept",
                ".agents/omp/policies/audit.yml": "kept",
            }
            for rel, text in files.items():
                (home / rel).parent.mkdir(parents=True, exist_ok=True)
                (home / rel).write_text(text)
            # The Claude side links each shared skill into ~/.agents/skills, as chezmoi deploys it.
            for name in ("hcom-audit", "hcom-worker"):
                link = home / ".claude/skills" / name / "SKILL.md"
                link.parent.mkdir(parents=True)
                link.symlink_to(Path("../../../.agents/skills") / name / "SKILL.md")
            config = base / "chezmoi.toml"
            config.write_text("")
            run = subprocess.run(
                [
                    *("chezmoi", "apply", "--force", "--no-tty"),
                    *("--source", str(source), "--destination", str(home), "--config", str(config)),
                    *("--cache", str(base / "cache"), "--persistent-state", str(base / "state.boltdb")),
                ],
                env=os.environ | {"HOME": str(home)},
                capture_output=True,
                text=True,
                timeout=120,
                check=False,
            )
            self.assertEqual(0, run.returncode, run.stderr)
            left = sorted(str(p.relative_to(home)) for p in home.rglob("*") if p.is_file())
            self.assertEqual(
                [
                    ".agents/omp/policies/audit.yml",
                    ".agents/skills/hcom-worker/SKILL.md",
                    ".claude/skills/hcom-worker/SKILL.md",
                    ".local/bin/common/hcom-dispatch",
                ],
                left,
            )
            for gone in REMOVALS:
                self.assertFalse((home / gone).exists(), f"{gone}: removed")
                self.assertFalse((home / gone).is_symlink(), gone)


if __name__ == "__main__":
    unittest.main()
