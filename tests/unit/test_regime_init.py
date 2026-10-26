"""Exercise scripts/orchestrator/regime-init in a scratch repository (regime-cutover U33).

The checkout copy runs with HOME in a scratch directory, so the store origin lands under that HOME, and the
templates come from the checkout's home/dot_agents/regime (the directory beside the manifest its self-check reads).
"""

import os
import subprocess
import tempfile
import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))  # dotted runs too; discover -s tests/unit already has it
from scratch_git import git_init, quiet_git_env  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
INIT = ROOT / "scripts/orchestrator/regime-init"
TEMPLATES = ROOT / "home/dot_agents/regime"
STORE_FILES = ("preferences.md", "units.tsv", "ledger.tsv", "decisions.tsv", "gates.md")
# U100: an env built from scratch carries scratch_git's settings too, so no commit starts background maintenance.
GIT_IDENTITY = quiet_git_env(
    {
        "GIT_CONFIG_GLOBAL": "/dev/null",
        "GIT_CONFIG_NOSYSTEM": "1",
        "GIT_AUTHOR_NAME": "t",
        "GIT_AUTHOR_EMAIL": "t@example.invalid",
        "GIT_COMMITTER_NAME": "t",
        "GIT_COMMITTER_EMAIL": "t@example.invalid",
    }
)


class AuditSectionTest(unittest.TestCase):
    def test_this_repository_audit_section_is_the_template_byte_for_byte(self):
        # One source (F013): regime-init appends the template to other repositories, and the audit of this one reads
        # its own AGENTS.md, so the two sections never drift. The section runs from its heading to the next one.
        text = (ROOT / "AGENTS.md").read_text()
        start = text.index("\n## Audit\n") + 1
        end = text.find("\n## ", start)
        section = text[start : end if end != -1 else len(text)]
        self.assertEqual(section, (TEMPLATES / "AGENTS-audit-section.md").read_text())


class RegimeInitTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.home = self.root / "home"
        self.home.mkdir()
        self.repo = self.root / "kit-pilot"
        self.repo.mkdir()
        self.env = {"PATH": os.environ["PATH"], "HOME": str(self.home), **GIT_IDENTITY}
        git_init(self.repo, env=self.env)
        subprocess.run(["git", "commit", "-q", "--allow-empty", "-m", "init"], cwd=self.repo, env=self.env, check=True)
        self.store = self.repo / ".orchestration/orchestrate/pilot"
        self.origin = self.home / ".local/state/hcom/kit-pilot/origin"

    def init(self, *args, cwd=None, env=None):
        return subprocess.run(
            [str(INIT), *args],
            cwd=cwd or self.repo,
            env=env or self.env,
            capture_output=True,
            text=True,
            timeout=60,
            check=False,
        )

    def rows(self, stdout):
        return {line.split("\t")[1]: line.split("\t")[0] for line in stdout.splitlines() if "\t" in line}

    def test_the_first_run_creates_the_store_and_the_origin_and_the_second_changes_nothing(self):
        run = self.init("pilot")
        self.assertEqual(run.returncode, 0, run.stderr)
        for name in STORE_FILES:
            with self.subTest(file=name):
                self.assertEqual((self.store / name).read_bytes(), (TEMPLATES / name).read_bytes())
                self.assertEqual(self.rows(run.stdout)[str(self.store / name)], "created")
        self.assertEqual(self.origin.read_text(), f"{self.repo}\n")
        self.assertIn((TEMPLATES / "AGENTS-audit-section.md").read_text(), run.stdout, "the section is printed")
        self.assertFalse((self.repo / "AGENTS.md").exists(), "without --write-agents nothing is appended")
        self.assertIn("hcom-dispatch kit-pilot operator orchestrator-<word>", run.stdout)

        again = self.init("pilot")
        self.assertEqual(again.returncode, 0, again.stderr)
        self.assertEqual(set(self.rows(again.stdout).values()), {"unchanged"})
        self.assertIn("nothing changed", again.stdout)

    def test_an_inherited_store_and_team_are_named_and_the_hint_is_always_printed(self):
        """From a seat, HCOM_DIR and HCOM_TEAM are inherited and win; regime-init says so (orchestrator pilot, U33b)."""
        plain = self.init("pilot")
        self.assertIn("env -u HCOM_DIR -u HCOM_TEAM <command>", plain.stdout)
        self.assertNotIn("note: this shell set", plain.stderr)
        seat_store = self.root / "seat-store"
        inherited = self.init("pilot", env={**self.env, "HCOM_DIR": str(seat_store), "HCOM_TEAM": "regime"})
        self.assertEqual(inherited.returncode, 0, inherited.stderr)
        self.assertIn(f"note: this shell set HCOM_DIR={seat_store} HCOM_TEAM=regime", inherited.stderr)
        self.assertIn("env -u HCOM_DIR -u HCOM_TEAM regime-init pilot", inherited.stderr)

    def test_the_printed_listing_names_the_store_in_effect(self):
        """The printed `hcom list` line carries HCOM_DIR, quoted, so a fresh shell lists this store (audit U33 F2)."""
        fake = self.root / "fake"
        fake.mkdir()
        (fake / "hcom").write_text('#!/bin/sh\nprintf "%s\\n" "$HCOM_DIR" > "$0.dir"\n')
        (fake / "hcom").chmod(0o755)
        for label, extra, store in (
            ("derived", {}, self.home / ".local/state/hcom/kit-pilot"),
            ("explicit, with a space", {"HCOM_DIR": str(self.root / "seat store")}, self.root / "seat store"),
        ):
            with self.subTest(label):
                run = self.init("pilot", env={**self.env, **extra})
                self.assertEqual(run.returncode, 0, run.stderr)
                (line,) = [row.strip() for row in run.stdout.splitlines() if row.strip().endswith("hcom list -v")]
                self.assertTrue(line.startswith("HCOM_DIR="), line)
                subprocess.run(["bash", "-c", line], env={"PATH": f"{fake}:{self.env['PATH']}"}, check=True)
                self.assertEqual((fake / "hcom.dir").read_text(), f"{store}\n")

    def test_a_changed_store_file_is_kept_unless_forced(self):
        self.init("pilot")
        (self.store / "units.tsv").write_text("local edit\n")
        kept = self.init("pilot")
        self.assertEqual(self.rows(kept.stdout)[str(self.store / "units.tsv")], "kept")
        self.assertEqual((self.store / "units.tsv").read_text(), "local edit\n")
        forced = self.init("pilot", "--force")
        self.assertEqual(self.rows(forced.stdout)[str(self.store / "units.tsv")], "replaced")
        self.assertEqual((self.store / "units.tsv").read_bytes(), (TEMPLATES / "units.tsv").read_bytes())

    def test_write_agents_appends_the_section_once_and_leaves_an_existing_audit_section(self):
        (self.repo / "AGENTS.md").write_text("# AGENTS.md\n\nProject rules.\n")
        run = self.init("pilot", "--write-agents")
        self.assertEqual(run.returncode, 0, run.stderr)
        section = (TEMPLATES / "AGENTS-audit-section.md").read_text()
        self.assertEqual((self.repo / "AGENTS.md").read_text(), "# AGENTS.md\n\nProject rules.\n\n" + section)
        self.assertEqual(self.init("pilot", "--write-agents").returncode, 0)
        self.assertEqual((self.repo / "AGENTS.md").read_text().count("## Audit"), 1, "a second run appends nothing")

    def test_refusals_write_nothing(self):
        outside = self.root / "outside"
        outside.mkdir()
        for label, args, cwd in (
            ("outside a checkout", ["pilot"], outside),
            ("bad program", ["Pilot/1"], None),
            ("no program", [], None),
            ("unknown flag", ["pilot", "--all"], None),
        ):
            with self.subTest(label):
                run = self.init(*args, cwd=cwd)
                self.assertEqual(run.returncode, 2, run.stdout)
                self.assertTrue(run.stderr.startswith("regime-init: "), run.stderr)
        self.assertFalse((self.repo / ".orchestration").exists())
        self.assertFalse((self.home / ".local").exists())

        self.origin.parent.mkdir(parents=True)
        self.origin.write_text("/elsewhere/kit-pilot\n")
        run = self.init("pilot")
        self.assertEqual(run.returncode, 2, run.stdout)
        self.assertIn("belongs to /elsewhere/kit-pilot", run.stderr)
        self.assertFalse((self.repo / ".orchestration").exists(), "a collision writes nothing")
        self.origin.unlink()

        target = self.root / "elsewhere"
        target.mkdir()
        (self.repo / ".orchestration").symlink_to(target)
        run = self.init("pilot")
        self.assertEqual(run.returncode, 2, run.stdout)
        self.assertIn("is a symlink", run.stderr)
        self.assertEqual(list(target.iterdir()), [], "nothing written through the symlink")

    def test_a_symlinked_store_or_origin_refuses_before_anything_is_written(self):
        """A symlinked derived store, or a dangling origin symlink, writes neither the binding nor the store files
        (Codex 4366521828)."""
        elsewhere = self.root / "elsewhere"
        elsewhere.mkdir()
        state = self.home / ".local/state/hcom"
        state.mkdir(parents=True)
        (state / "kit-pilot").symlink_to(elsewhere)
        run = self.init("pilot")
        self.assertEqual(run.returncode, 2, run.stdout)
        self.assertIn("is a symlink", run.stderr)
        (state / "kit-pilot").unlink()
        (state / "kit-pilot").mkdir()
        (state / "kit-pilot/origin").symlink_to(elsewhere / "origin")
        run = self.init("pilot")
        self.assertEqual(run.returncode, 2, run.stdout)
        self.assertIn("is a symlink", run.stderr)
        self.assertEqual(list(elsewhere.iterdir()), [], "nothing written through either symlink")
        self.assertFalse((self.repo / ".orchestration").exists(), "no store file before the binding is safe")
        explicit = self.root / "explicit-store"
        explicit.symlink_to(elsewhere)
        run = self.init("pilot", env={**self.env, "HCOM_DIR": str(explicit)})
        self.assertEqual(run.returncode, 2, run.stdout)
        self.assertIn("is a symlink", run.stderr)
        self.assertFalse((self.repo / ".orchestration").exists())

    def test_a_failing_comparison_or_agents_read_refuses_instead_of_writing(self):
        """cmp and grep exit 2 on a read error; neither is read as "differs" or "no section" (preferences 21)."""
        self.init("pilot")
        (self.store / "units.tsv").write_text("local edit\n")
        (self.repo / "AGENTS.md").write_text("# AGENTS.md\n")
        fake = self.root / "fake"
        fake.mkdir()
        for tool in ("cmp", "grep"):
            (fake / tool).write_text("#!/bin/sh\nexit 2\n")
            (fake / tool).chmod(0o755)
        env = {**self.env, "PATH": f"{fake}:{self.env['PATH']}"}
        run = self.init("pilot", "--force", env=env)
        self.assertEqual(run.returncode, 2, run.stdout)
        self.assertIn("cannot compare", run.stderr)
        self.assertEqual((self.store / "units.tsv").read_text(), "local edit\n", "--force replaced nothing")
        (fake / "cmp").unlink()
        run = self.init("pilot", "--write-agents", env=env)
        self.assertEqual(run.returncode, 2, run.stdout)
        self.assertIn(f"cannot read {self.repo}/AGENTS.md", run.stderr)
        self.assertEqual((self.repo / "AGENTS.md").read_text(), "# AGENTS.md\n", "nothing appended")


if __name__ == "__main__":
    unittest.main()
