"""The agmsg docs, skill, deployed skill tree and retire helper are gone (regime-cutover U27; U26 removed the tooling, U32
the rules, U72 the `herdr-agents` retire step that `make update` ran before `chezmoi apply`).

No live file names the old regime: scripts/lint-retired-terms.py checks every tracked file against the one list,
scripts/retired-terms.tsv (U72), so this module keeps only the removals. The dry run applies a scratch source that holds
only the real `home/.chezmoiremove` to a scratch HOME, so it exercises exactly the removal entries and nothing else.
"""

import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REMOVALS = (
    ".agents/skills/agmsg/**",
    ".claude/commands/agmsg.md",
    ".claude/skills/agmsg/**",
    # The deleted skill's deployed copies: ~/.agents/skills is not exact, so only these entries remove them (U27b F1).
    ".agents/skills/agmsg-orchestration",
    ".claude/skills/agmsg-orchestration",
    # The retire helper's deployed copy: nothing on either host is left for it to retire (U72).
    ".local/bin/common/herdr-agents",
)


class AgmsgRemovedTest(unittest.TestCase):
    def test_the_agmsg_orchestration_skill_is_gone_on_both_sides(self):
        for side in ("home/dot_agents/skills", "home/dot_claude/skills"):
            with self.subTest(side=side):
                self.assertEqual([], sorted(p.name for p in (ROOT / side).iterdir() if "agmsg" in p.name))

    def test_chezmoiremove_removes_the_deployed_tree_and_its_command(self):
        entries = [line.strip() for line in (ROOT / "home/.chezmoiremove").read_text().splitlines()]
        for entry in REMOVALS:
            with self.subTest(entry=entry):
                self.assertIn(entry, entries)

    @unittest.skipUnless(shutil.which("chezmoi"), "chezmoi is not installed")
    def test_apply_removes_the_tree_and_the_command_and_keeps_their_neighbours(self):
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            source, home = base / "source", base / "home"
            source.mkdir()
            shutil.copy(ROOT / "home/.chezmoiremove", source / ".chezmoiremove")
            files = {
                ".agents/skills/agmsg/db/messages.db": "db",
                ".agents/skills/agmsg/scripts/send.sh": "s",
                ".agents/skills/agmsg-orchestration/SKILL.md": "retired",
                ".agents/skills/other/SKILL.md": "kept",
                ".claude/commands/agmsg.md": "c",
                ".claude/commands/keep.md": "kept",
                ".local/bin/common/herdr-agents": "retired",
                ".local/bin/common/hcom-seat": "kept",
            }
            for rel, text in files.items():
                (home / rel).parent.mkdir(parents=True, exist_ok=True)
                (home / rel).write_text(text)
            # The Claude side links each shared skill file into the chezmoi source tree, as the generator renders it
            # ({{ .chezmoi.sourceDir }}/dot_agents/skills/<name>/<file>, scripts/generate-agent-configs.py). The link
            # target outlives the apply, so a Claude link that is left behind still reads as a file.
            chezmoi_source = base / "chezmoi-source"
            for name in ("agmsg-orchestration", "other"):
                skill = chezmoi_source / "dot_agents/skills" / name / "SKILL.md"
                skill.parent.mkdir(parents=True)
                skill.write_text(name)
                link = home / ".claude/skills" / name / "SKILL.md"
                link.parent.mkdir(parents=True)
                link.symlink_to(skill)
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
                    ".agents/skills/other/SKILL.md",
                    ".claude/commands/keep.md",
                    ".claude/skills/other/SKILL.md",
                    ".local/bin/common/hcom-seat",
                ],
                left,
            )
            for gone in (
                ".agents/skills/agmsg",
                ".agents/skills/agmsg-orchestration",
                ".claude/skills/agmsg-orchestration",
            ):
                self.assertFalse((home / gone).exists(), f"{gone}: the directory itself is removed")
                self.assertFalse((home / gone).is_symlink(), gone)


if __name__ == "__main__":
    unittest.main()
