import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CHEZMOI = shutil.which("chezmoi")


@unittest.skipUnless(CHEZMOI, "chezmoi is not installed")
class ChezmoiRemoveAgmsgTest(unittest.TestCase):
    """`chezmoi apply` with the repo's .chezmoiremove retires the stale agmsg symlink farm only."""

    def test_apply_removes_the_symlink_farm_and_keeps_installer_owned_paths(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            source, home, config = base / "src", base / "home", base / "cfg"
            for directory in (source, home, config):
                directory.mkdir()
            shutil.copy(ROOT / "home/.chezmoiremove", source / ".chezmoiremove")
            vendored = source / "dot_agents/skills/agmsg"
            farm = home / ".claude/skills/agmsg"
            (farm / "scripts/lib").mkdir(parents=True)
            for relative in ("SKILL.md", "scripts/send.sh", "scripts/lib/storage.sh"):
                (farm / relative).symlink_to(vendored / relative)
            other = home / ".claude/skills/other/SKILL.md"
            other.parent.mkdir(parents=True)
            other.write_text("keep\n")
            command = home / ".claude/commands/agmsg.md"
            command.parent.mkdir(parents=True)
            command.write_text("upstream-rendered command\n")
            state = home / ".agents/skills/agmsg/db/messages.db"
            state.parent.mkdir(parents=True)
            state.write_bytes(b"live state")

            result = subprocess.run(
                [
                    CHEZMOI,
                    "--source",
                    str(source),
                    "--destination",
                    str(home),
                    "--config",
                    str(config / "chezmoi.yaml"),
                    "--persistent-state",
                    str(config / "state.boltdb"),
                    "--no-tty",
                    "apply",
                    "--force",
                ],
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertFalse(farm.exists() or farm.is_symlink())
            self.assertEqual(other.read_text(), "keep\n")
            self.assertEqual(command.read_text(), "upstream-rendered command\n")
            self.assertEqual(state.read_bytes(), b"live state")


class ChezmoiRemoveRetiredShellFilesTest(unittest.TestCase):
    """T75: deleted shell files are retired on machines that applied them before."""

    RETIRED = (
        ".config/alias/client.sh",
        ".config/alias/server.sh",
        ".config/tango.yml",
        ".local/bin/common/setup-python-env",
        ".local/bin/server/history.sh",
        ".local/bin/server/cache.sh",
    )

    def test_retired_targets_are_listed_and_have_no_source(self) -> None:
        entries = (ROOT / "home/.chezmoiremove").read_text().splitlines()
        sources = {
            path.relative_to(ROOT / "home").as_posix().replace("dot_", ".").replace("executable_", "")
            for path in (ROOT / "home").rglob("*")
            if path.is_file()
        }
        for target in self.RETIRED:
            with self.subTest(target=target):
                self.assertIn(target, entries)
                self.assertNotIn(target, sources)


if __name__ == "__main__":
    unittest.main()
