"""The agmsg docs, skill and deployed skill tree are gone (regime-cutover U27; U26 removed the tooling, U32 the rules).

Only the retire path stays (`make agmsg-retire`, `herdr-agents --retire-agmsg`, run before `chezmoi apply`), and the
hcom bus keeps its `AGMSG-` line kinds (D-024-133). The dry run applies a scratch source that holds only the real
`home/.chezmoiremove` to a scratch HOME, so it exercises exactly the removal entries and nothing else.
"""

import os
import re
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
)
RETIRED = re.compile(
    r"agmsg|codex-orchestrate|pr-feedback|crit-review|regime-counters|acceptance record", re.IGNORECASE
)
# The bus line kinds and the kept retire path's own names are not old-regime prose.
ALLOWED = re.compile(r"AGMSG-[A-Z]*|make agmsg-retire|--retire-agmsg")
RETIRE_PARAGRAPH = "Before `chezmoi apply`, `make update` runs `make agmsg-retire`"


def stray(text):
    """Return each paragraph that still names the old regime once the allowed names are taken out."""
    return [p for p in re.split(r"\n\s*\n", text) if RETIRED.search(ALLOWED.sub("", p))]


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

    def test_readme_keeps_only_the_retire_paragraph_and_the_bus_line_kinds(self):
        paragraphs = stray((ROOT / "README.md").read_text())
        self.assertEqual(1, len(paragraphs), paragraphs)
        self.assertTrue(paragraphs[0].startswith(RETIRE_PARAGRAPH), paragraphs[0][:200])

    def test_agents_md_and_the_seat_doc_name_no_old_regime(self):
        for name in ("AGENTS.md", "docs/orchestrator-seat.md"):
            with self.subTest(file=name):
                self.assertEqual([], stray((ROOT / name).read_text()))

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
            }
            for rel, text in files.items():
                (home / rel).parent.mkdir(parents=True, exist_ok=True)
                (home / rel).write_text(text)
            # The Claude side links each shared skill into ~/.agents/skills, as chezmoi deploys it.
            for name in ("agmsg-orchestration", "other"):
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
                [".agents/skills/other/SKILL.md", ".claude/commands/keep.md", ".claude/skills/other/SKILL.md"], left
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
