"""The agmsg docs, skill, deployed skill tree and retire helper are gone (regime-cutover U27; U26 removed the tooling, U32
the rules, U72 the `herdr-agents` retire step that `make update` ran before `chezmoi apply`).

No live file names the old regime: scripts/lint-retired-terms.py checks every tracked file against the one list,
scripts/retired-terms.tsv (U72), so this module keeps only the removals. The dry run applies a scratch source that holds
only the real `home/.chezmoiremove` to a scratch HOME, so it exercises exactly the removal entries and nothing else.
"""

import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))  # dotted runs too; discover -s tests/unit already has it
from agent_home_isolation import isolate_agent_homes, restore_agent_homes

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


def setUpModule() -> None:
    isolate_agent_homes()


def tearDownModule() -> None:
    restore_agent_homes()


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

    def retire_shim(self, home: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["bash", "-c", f"source {ROOT / 'scripts/update-agent-assets.sh'}; retire_agmsg_shim"],
            cwd=ROOT,
            env={**os.environ, "HOME": str(home)},
            text=True,
            capture_output=True,
            check=False,
            timeout=30,  # a FIFO at the shim path must be refused, never opened and waited on
        )

    @staticmethod
    def write_shim(home: Path, owner_home: Path | None = None) -> Path:
        """Write ~/.agents/bin/agy-tui as agmsg wrote it on both hosts (owner under `owner_home`, default `home`)."""
        owner = (owner_home or home) / ".agents/skills/agmsg/scripts/drivers/types/antigravity/agy-tui.sh"
        shim = home / ".agents/bin/agy-tui"
        shim.parent.mkdir(parents=True, exist_ok=True)
        shim.write_text(
            "#!/usr/bin/env bash\nset -euo pipefail\n# agmsg Antigravity TUI launcher shim\n"
            f'# agmsg-shim-owner: {owner}\nexec bash {owner} "$@"\n'
        )
        shim.chmod(0o711)
        return shim

    def test_make_update_removes_the_dangling_agmsg_shim_and_its_empty_bin(self):
        with tempfile.TemporaryDirectory() as temp:
            home = Path(temp)
            self.write_shim(home)
            first = self.retire_shim(home)
            self.assertEqual(0, first.returncode, first.stderr)
            self.assertFalse((home / ".agents/bin").exists(), "the emptied ~/.agents/bin is removed")
            self.assertTrue((home / ".agents").is_dir())
            again = self.retire_shim(home)
            self.assertEqual(
                (0, "", ""), (again.returncode, again.stdout, again.stderr), "a second run changes nothing"
            )

    def test_an_unrelated_file_keeps_the_bin_directory(self):
        with tempfile.TemporaryDirectory() as temp:
            home = Path(temp)
            self.write_shim(home)
            (home / ".agents/bin/mine").write_text("keep\n")
            self.assertEqual(0, self.retire_shim(home).returncode)
            self.assertEqual(["mine"], os.listdir(home / ".agents/bin"))
            self.assertEqual(0, self.retire_shim(home).returncode)
            self.assertEqual(["mine"], os.listdir(home / ".agents/bin"))

    SWAP_POINT = "# Verified: from here on, nothing is removed by name."
    REMOVED_POINT = "# Removed: only the bin directory opened above may go."

    def retire_shim_with_swap(self, home: Path, swap: str, point: str = SWAP_POINT) -> subprocess.CompletedProcess[str]:
        """Run the step with SWAP (Python) injected at POINT, a comment line of the step's own program: python3 is
        wrapped so that program is run with SWAP inserted there (SWAP_POINT: after verification, before anything is
        moved or removed; REMOVED_POINT: after the shim is gone, before `bin` is removed)."""
        wrapper = (
            'python3() { local program; program="$(cat)"; '
            'case "${program}" in *"${SWAP_POINT}"*) ;; *) echo "no swap point" >&2; return 99 ;; esac; '
            'command python3 "$@" <<< "${program/"${SWAP_POINT}"/${SWAP}}"; }'
        )
        return subprocess.run(
            ["bash", "-c", f"source {ROOT / 'scripts/update-agent-assets.sh'}; {wrapper}; retire_agmsg_shim"],
            cwd=ROOT,
            env={**os.environ, "HOME": str(home), "SWAP_POINT": point, "SWAP": swap},
            text=True,
            capture_output=True,
            check=False,
            timeout=30,
        )

    def test_no_path_is_followed_through_a_symlinked_agents_directory(self):
        # Round-6 audit: `.agents` swapped for a symlink after its check redirected the removal out of HOME. Every
        # operation is relative to the directories opened at the start, so the symlink's target is never touched.
        with tempfile.TemporaryDirectory() as temp:
            home, elsewhere = Path(temp) / "home", Path(temp) / "elsewhere"
            self.write_shim(home)
            self.write_shim(elsewhere, owner_home=home)  # a shim that would pass verification, outside HOME
            (elsewhere / ".agents/bin/keep-empty").mkdir()
            swap = f'os.rename(agents, agents + ".moved")\nos.symlink({str(elsewhere / ".agents")!r}, agents)'
            result = self.retire_shim_with_swap(home, swap)
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertTrue((elsewhere / ".agents/bin/agy-tui").is_file(), "nothing outside HOME is removed")
            self.assertTrue((elsewhere / ".agents/bin/keep-empty").is_dir())
            # The verified shim, in the directory the step opened, is the one removed, with its emptied bin.
            self.assertFalse((home / ".agents.moved/bin").exists())
        # Before any open: a symlinked `.agents` or `bin` refuses and removes nothing.
        for link in (".agents", ".agents/bin"):
            with self.subTest(symlink=link), tempfile.TemporaryDirectory() as temp:
                home, elsewhere = Path(temp) / "home", Path(temp) / "elsewhere"
                self.write_shim(elsewhere, owner_home=home)
                target = elsewhere / (".agents" if link == ".agents" else ".agents/bin")
                (home / link).parent.mkdir(parents=True, exist_ok=True)
                (home / link).symlink_to(target)
                result = self.retire_shim(home)
                self.assertEqual(1, result.returncode, result.stdout + result.stderr)
                self.assertIn("is not a real directory", result.stderr)
                self.assertTrue((elsewhere / ".agents/bin/agy-tui").is_file())

    def test_a_bin_directory_swapped_in_before_its_removal_is_kept(self):
        # Round-6 audit: the final rmdir by path removed an empty replacement `bin` that never held the shim.
        with tempfile.TemporaryDirectory() as temp:
            home = Path(temp)
            self.write_shim(home)
            swap = 'os.rename(bin_dir, bin_dir + ".old")\nos.mkdir(bin_dir)'
            result = self.retire_shim_with_swap(home, swap, self.REMOVED_POINT)
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertIn("it is not the directory the shim was removed from", result.stdout)
            self.assertTrue((home / ".agents/bin").is_dir(), "the replacement bin is kept")
            self.assertEqual([], os.listdir(home / ".agents/bin.old"), "the shim itself was removed")

    def test_a_file_swapped_in_after_verification_is_kept(self):
        # Round-5 audit: removal by name deleted whatever held the name by then. Removal is by the verified inode.
        with tempfile.TemporaryDirectory() as temp:
            home = Path(temp)
            self.write_shim(home)
            swap = (
                'replacement = os.path.join(bin_dir, "replacement")\n'
                'with open(replacement, "w") as out:\n'
                '    out.write("operator file\\n")\n'
                "os.replace(replacement, shim)"
            )
            result = self.retire_shim_with_swap(home, swap)
            self.assertEqual(1, result.returncode, result.stdout + result.stderr)
            self.assertIn("changed before its removal", result.stderr)
            self.assertEqual("operator file\n", (home / ".agents/bin/agy-tui").read_text())
            self.assertEqual(["agy-tui"], os.listdir(home / ".agents/bin"), "the quarantine directory is gone")
            # The same harness with no swap removes the shim, so the injection point is the one the step runs.
            home2 = home / "control"
            self.write_shim(home2)
            result = self.retire_shim_with_swap(home2, "pass")
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertFalse((home2 / ".agents/bin").exists())

    def test_a_newline_named_entry_keeps_the_bin_directory(self):
        with tempfile.TemporaryDirectory() as temp:
            home = Path(temp)
            self.write_shim(home)
            (home / ".agents/bin/\n").write_text("keep\n")
            result = self.retire_shim(home)
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertEqual(["\n"], os.listdir(home / ".agents/bin"))

    def owner_dir(self, home: Path) -> Path:
        return home / ".agents/skills/agmsg/scripts/drivers/types/antigravity"

    def test_anything_short_of_positive_proof_keeps_the_file_and_fails(self):
        def own(home: Path) -> None:
            (home / ".agents/bin/agy-tui").write_text("#!/bin/sh\nexec agy\n")

        def owner_present(home: Path) -> None:
            self.write_shim(home)
            self.owner_dir(home).mkdir(parents=True)
            (self.owner_dir(home) / "agy-tui.sh").write_text("x\n")

        def owner_unstatable(home: Path) -> None:
            # lstat of the owner fails with EACCES, not ENOENT: its absence is not proven.
            self.write_shim(home)
            self.owner_dir(home).mkdir(parents=True)
            (home / ".agents/skills/agmsg").chmod(0)

        def unreadable(home: Path) -> None:
            self.write_shim(home).chmod(0)

        def symlink(home: Path) -> None:
            target = self.write_shim(home, owner_home=home).rename(home / "real")
            (home / ".agents/bin/agy-tui").symlink_to(target)

        def fifo(home: Path) -> None:
            os.mkfifo(home / ".agents/bin/agy-tui")

        cases = {
            "own agy-tui": (own, "is not the retired agmsg shim", True),
            "owner of another home": (
                lambda home: self.write_shim(home, owner_home=home / "elsewhere"),
                "is not the retired agmsg shim",
                True,
            ),
            "owner still present": (owner_present, "still exists", True),
            "owner lstat error": (owner_unstatable, "cannot prove its owner", False),
            "read error": (unreadable, "cannot open it", False),
            "symlink": (symlink, "is not a regular file", True),
            "fifo": (fifo, "is not a regular file", True),
        }
        for label, (make, message, as_root) in cases.items():
            if not as_root and os.geteuid() == 0:
                continue  # root bypasses the permission bits that inject the failure
            with self.subTest(case=label), tempfile.TemporaryDirectory() as temp:
                home = Path(temp)
                (home / ".agents/bin").mkdir(parents=True)
                make(home)
                try:
                    result = self.retire_shim(home)
                    self.assertEqual(1, result.returncode, result.stdout + result.stderr)
                    self.assertIn(message, result.stderr)
                    self.assertTrue(
                        (home / ".agents/bin/agy-tui").is_symlink() or (home / ".agents/bin/agy-tui").exists()
                    )
                finally:
                    for path in (home / ".agents/skills/agmsg", home / ".agents/bin/agy-tui"):
                        if path.exists() and not path.is_symlink():
                            path.chmod(0o700)


if __name__ == "__main__":
    unittest.main()
