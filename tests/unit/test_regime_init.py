"""Exercise scripts/orchestrator/regime-init in a scratch repository (regime-cutover U33; U215, U215b: the store outside
it, under a bound root).

The checkout copy runs with HOME in a scratch directory, so the store origin, the store-root binding
(`~/.local/state/hcom/<slug>/store-root`) and the program store (`~/.local/state/regime-store/<slug>/<program>`, the
default root, U215b) land under that HOME and nothing under the scratch checkout or the hcom store, and the templates
come from the checkout's home/dot_agents/regime (the directory beside the manifest its self-check reads).
"""

import os
import shutil
import stat
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
        # U215b: the program store lies under the root bound in `<HCOM_DIR>/store-root`, by default
        # `~/.local/state/regime-store/<slug>`, never under the checkout and never under the hcom store (hcom-seat
        # grants the hcom store to every seat for the bus, verdict U215-11a32ed6 P1).
        self.hcom_store = self.home / ".local/state/hcom/kit-pilot"
        self.origin = self.hcom_store / "origin"
        self.binding = self.hcom_store / "store-root"
        self.store_parent = self.home / ".local/state/regime-store"
        self.store_root = self.store_parent / "kit-pilot"
        self.store = self.store_root / "pilot"

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

    def assert_private_directory_of_this_user(self, path):
        """`path` is a real directory (no symlink), mode 0700, owned by this user (U215: the shape of hcom-seat's
        state_root_make)."""
        status = os.lstat(path)
        self.assertTrue(stat.S_ISDIR(status.st_mode), f"{path} is not a directory")
        self.assertEqual(stat.S_IMODE(status.st_mode), 0o700, path)
        self.assertEqual(status.st_uid, os.getuid(), path)

    def make_private(self, *paths):
        """Make each scratch directory (parents too) and set it and every store component above it to 0700, the mode
        regime-init holds a component to, so a case's refusal names exactly the component it plants or re-modes."""
        for path in paths:
            path.mkdir(parents=True, exist_ok=True)
        for component in (self.store_parent, self.store_root, self.store):
            if component.is_dir() and not component.is_symlink():
                component.chmod(0o700)

    def test_the_first_run_creates_the_store_and_the_origin_and_the_second_changes_nothing(self):
        run = self.init("pilot")
        self.assertEqual(run.returncode, 0, run.stderr)
        # U215b: `regime-store`, `<slug>` and `<program>` are made under ~/.local/state, each 0700 and this user's; the
        # binding beside origin holds the root, 0600; the hcom store holds the two bindings and nothing else; the
        # checkout gets no `.orchestration` directory.
        self.assert_private_directory_of_this_user(self.store_parent)
        self.assert_private_directory_of_this_user(self.store_root)
        self.assert_private_directory_of_this_user(self.store)
        self.assertEqual(self.binding.read_text(), f"{self.store_root}\n")
        self.assertEqual(stat.S_IMODE(os.lstat(self.binding).st_mode), 0o600)
        self.assertEqual(sorted(path.name for path in self.hcom_store.iterdir()), ["origin", "store-root"])
        self.assertFalse((self.repo / ".orchestration").exists(), "nothing is created under the checkout")
        self.assertEqual(self.rows(run.stdout)[str(self.store_root)], "created")
        self.assertEqual(self.rows(run.stdout)[str(self.binding)], "created")
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
        self.assertEqual(set(self.rows(again.stdout).values()), {"unchanged", "checkout-guard: unchanged"})
        self.assertEqual(self.rows(again.stdout)[str(self.store_root)], "unchanged")
        self.assertEqual(self.rows(again.stdout)[str(self.binding)], "unchanged")
        self.assertIn("nothing changed", again.stdout)
        self.assertEqual(self.binding.read_text(), f"{self.store_root}\n")
        self.assertEqual(sorted(path.name for path in self.hcom_store.iterdir()), ["origin", "store-root"])
        self.assertFalse((self.repo / ".orchestration").exists())

    def test_a_pre_made_component_whose_mode_is_not_0700_refuses_before_anything_is_written(self):
        """U215b (verdict U215-11a32ed6 P2 `:172`): a `regime-store`, `<slug>` or `<program>` directory found in place
        is held to a real directory of this user whose mode is 0700, read by `/usr/bin/stat`; any other mode (0777,
        and 0750) is refused by name with exit 2 before the binding, the templates, the origin or the hook are written,
        and the directory keeps its mode (nothing is chmod-ed into compliance). The parents above the one that fails
        are 0700, so the refusal names exactly the offending component."""
        hook = self.repo / ".git/hooks/reference-transaction"
        for label, path, mode in (
            ("regime-store 0777", self.store_parent, 0o777),
            ("regime-store/kit-pilot 0777", self.store_root, 0o777),
            ("regime-store/kit-pilot/pilot 0777", self.store, 0o777),
            ("regime-store/kit-pilot 0750", self.store_root, 0o750),
        ):
            with self.subTest(label):
                self.make_private(path)
                path.chmod(mode)
                run = self.init("pilot")
                self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
                self.assertTrue(run.stderr.startswith("regime-init: refused: "), run.stderr)
                self.assertIn(f"{path} has mode {mode:o}, not 0700", run.stderr)
                self.assertEqual(stat.S_IMODE(os.lstat(path).st_mode), mode, "the directory keeps its mode")
                self.assertFalse(self.binding.exists(), "the binding is written after the directories are held")
                self.assertFalse((self.store / "units.tsv").exists(), "no template")
                self.assertFalse(self.origin.exists(), "the origin is written after the store")
                self.assertFalse(hook.exists(), "the guard is installed after the store")
                self.assertFalse((self.repo / ".orchestration").exists())
            # Cleared outside the subTest, so a failing assertion still leaves the next case its clean start.
            self.store_parent.chmod(0o700)
            shutil.rmtree(self.store_parent)
        run = self.init("pilot")
        self.assertEqual(run.returncode, 0, run.stderr)
        for path in (self.store_parent, self.store_root, self.store):
            self.assert_private_directory_of_this_user(path)

    def test_a_bound_root_under_home_is_honoured_and_one_outside_home_is_refused(self):
        """U215b: a binding in place before the first run (an operator's choice; U221's move) is honoured when its path
        lies under HOME: the store is made there, 0700 root and program directory, the default root is not made and
        the binding row is `unchanged`; a binding naming a path outside HOME is refused by name (regime-env's grammar,
        exit 2 here) before anything is written there."""
        chosen = self.home / "records/kit-pilot"
        (self.home / "records").mkdir()
        self.hcom_store.mkdir(parents=True)
        self.binding.write_text(f"{chosen}\n")
        run = self.init("pilot")
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assert_private_directory_of_this_user(chosen)
        self.assert_private_directory_of_this_user(chosen / "pilot")
        for name in STORE_FILES:
            self.assertEqual((chosen / "pilot" / name).read_bytes(), (TEMPLATES / name).read_bytes())
        self.assertEqual(self.rows(run.stdout)[str(chosen)], "created")
        self.assertEqual(self.rows(run.stdout)[str(self.binding)], "unchanged")
        self.assertEqual(self.binding.read_text(), f"{chosen}\n", "the binding is kept as written")
        self.assertFalse(self.store_parent.exists(), "the default root is not made")
        outside = self.root / "outside-root"
        self.binding.write_text(f"{outside}\n")
        run = self.init("pilot")
        self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
        self.assertIn(f"refused: the store-root binding {self.binding}", run.stderr)
        self.assertFalse(outside.exists(), "nothing made outside HOME")
        self.assertFalse(self.store_parent.exists())

    def test_the_first_run_installs_the_checkout_guard_and_a_commit_passes_until_u219_moves_its_trigger(self):
        """regime-init runs `checkout-guard.sh install` on the checkout it prepares (U129): the first run writes the
        `reference-transaction` hook (a `checkout-guard: installed` row), and the second run finds the lever's own hook
        (`unchanged`) and reports nothing changed; a round-1 `pre-commit` the lever recognises is removed and counts
        as a change. U215: the hook's trigger is still the checkout's `.orchestration/orchestrate/*/units.tsv`
        (checkout-guard.sh, U219's lever), which this lever no longer creates, so a commit in a freshly prepared
        checkout passes until U219 moves the trigger (handoff/07-store-move-design.md, the checkout-guard row); the
        pass is pinned here so that unit's change turns this line. The containment that holds until U219 (verdict
        U215-11a32ed6 P2 `:127`): the live store of this program stays inside the main checkout, untouched by this
        lever, so its `units.tsv` is still there and the installed guard still fires on this program's checkout; no
        fresh checkout is initialised before U219 lands (the hosts of today carry no `store-root` binding); and a
        fresh checkout prepared despite that holds only templates, nothing the records boundary protects."""
        hook = self.repo / ".git/hooks/reference-transaction"
        run = self.init("pilot")
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual(self.rows(run.stdout)[str(hook)], "checkout-guard: installed")
        self.assertTrue(os.access(hook, os.X_OK))
        (self.repo / "work.txt").write_text("work\n")
        subprocess.run(["git", "add", "work.txt"], cwd=self.repo, env=self.env, check=True)
        commit = subprocess.run(
            ["git", "commit", "-q", "-m", "work"], cwd=self.repo, env=self.env, capture_output=True, text=True
        )
        self.assertEqual(commit.returncode, 0, commit.stderr)
        self.assertNotIn("checkout-guard:", commit.stderr, "inert until U219 moves the trigger to the new store")
        self.assertFalse((self.repo / ".orchestration").exists())
        again = self.init("pilot")
        self.assertEqual(again.returncode, 0, again.stderr)
        self.assertEqual(self.rows(again.stdout)[str(hook)], "checkout-guard: unchanged")
        self.assertIn("nothing changed", again.stdout)
        # Round 1's pre-commit, byte for byte: removed on the next run, which is a change.
        lever = (ROOT / "scripts/orchestrator/checkout-guard.sh").read_text()
        body = lever.split("cat << 'ROUND1_PRE_COMMIT' > ", 1)[1].split("\n", 1)[1].split("\nROUND1_PRE_COMMIT\n", 1)[0]
        (self.repo / ".git/hooks/pre-commit").write_text(body + "\n")
        upgraded = self.init("pilot")
        self.assertEqual(upgraded.returncode, 0, upgraded.stderr)
        self.assertEqual(
            self.rows(upgraded.stdout)[str(self.repo / ".git/hooks/pre-commit")], "checkout-guard: removed"
        )
        self.assertNotIn("nothing changed", upgraded.stdout)
        self.assertFalse((self.repo / ".git/hooks/pre-commit").exists())
        # The guard's refusal is regime-init's: a foreign hook stops the run with exit 2 after the store rows.
        hook.write_text("#!/bin/sh\nexit 0\n")
        refused = self.init("pilot")
        self.assertEqual(refused.returncode, 2, refused.stdout)
        self.assertIn("is not this lever's hook", refused.stderr)
        self.assertIn("checkout-guard.sh install", refused.stderr)

    def test_a_checkout_path_holding_installed_still_reports_nothing_changed(self):
        """The receipt is read by its full shape at line start (`checkout-guard: installed<TAB><path>`), never as the
        word anywhere (U129 round 2): with the checkout under a directory named `installed`, the second run still
        prints the nothing-changed line."""
        repo = self.root / "installed" / "kit-named"
        repo.mkdir(parents=True)
        git_init(repo, env=self.env)
        subprocess.run(["git", "commit", "-q", "--allow-empty", "-m", "init"], cwd=repo, env=self.env, check=True)
        first = self.init("pilot", cwd=repo)
        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertIn("checkout-guard: installed\t", first.stdout)
        self.assertNotIn("nothing changed", first.stdout)
        again = self.init("pilot", cwd=repo)
        self.assertEqual(again.returncode, 0, again.stderr)
        self.assertIn("checkout-guard: unchanged\t" + str(repo / ".git/hooks/reference-transaction"), again.stdout)
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
        self.assertFalse(self.store_root.exists(), "a collision writes nothing")
        self.assertFalse(self.binding.exists())
        self.assertFalse((self.repo / ".orchestration").exists())
        self.origin.unlink()

        # U215: the checkout's `.orchestration` is no longer a path regime-init writes, so a symlink there is no
        # refusal of this lever (the store's own components are, below); the directory stays untouched.
        target = self.root / "elsewhere"
        target.mkdir()
        (self.repo / ".orchestration").symlink_to(target)
        run = self.init("pilot")
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual(list(target.iterdir()), [], "nothing written under the checkout's link")
        self.assertTrue((self.store / "units.tsv").is_file(), "the store is made under HOME")

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
        self.assertFalse(self.store_root.exists(), "no store file before the binding is safe")
        self.assertFalse((self.repo / ".orchestration").exists())
        explicit = self.root / "explicit-store"
        explicit.symlink_to(elsewhere)
        run = self.init("pilot", env={**self.env, "HCOM_DIR": str(explicit)})
        self.assertEqual(run.returncode, 2, run.stdout)
        self.assertIn("is a symlink", run.stderr)
        self.assertEqual(list(elsewhere.iterdir()), [])
        self.assertFalse((self.repo / ".orchestration").exists())

    def test_a_planted_entry_at_a_store_component_or_the_binding_refuses_before_anything_is_written(self):
        """U215, U215b: `regime-store`, the store root `regime-store/<slug>` and the program store under it are each
        made (0700) or found as a real directory of this user with mode 0700; a symbolic link planted at any of them,
        or a file at the root or the program store, is refused by name (exit 2) before the binding, the templates, the
        origin or the hook are written, the shape of hcom-seat's state_root_make; a link planted at the binding itself
        is regime-env's refusal, exit 2 here, with nothing written."""
        elsewhere = self.root / "elsewhere"
        elsewhere.mkdir()
        self.hcom_store.mkdir(parents=True)
        hook = self.repo / ".git/hooks/reference-transaction"
        for label, plant, planted in (
            ("a link at regime-store", lambda: self.store_parent.symlink_to(elsewhere), self.store_parent),
            (
                "a link at the store root",
                lambda: (self.make_private(self.store_parent), self.store_root.symlink_to(elsewhere)),
                self.store_root,
            ),
            (
                "a link at the program store",
                lambda: (self.make_private(self.store_root), self.store.symlink_to(elsewhere)),
                self.store,
            ),
            (
                "a file at the store root",
                lambda: (self.make_private(self.store_parent), self.store_root.write_text("")),
                self.store_root,
            ),
            (
                "a file at the program store",
                lambda: (self.make_private(self.store_root), self.store.write_text("")),
                self.store,
            ),
            ("a link at the binding", lambda: self.binding.symlink_to(elsewhere / "store-root"), self.binding),
        ):
            with self.subTest(label):
                plant()
                run = self.init("pilot")
                self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
                self.assertTrue(run.stderr.startswith("regime-init: "), run.stderr)
                self.assertIn(str(planted), run.stderr, "the refusal names the planted component")
                self.assertEqual(list(elsewhere.iterdir()), [], "nothing written through a link")
                self.assertFalse(self.binding.is_file(), "the binding is written after the store")
                self.assertFalse(self.origin.exists(), "the origin is written after the store")
                self.assertFalse(hook.exists(), "the guard is installed after the store")
                self.assertFalse((self.repo / ".orchestration").exists())
            # The planted entry is cleared outside the subTest, so a failing assertion still leaves the next case
            # its clean start (nothing follows a link: each entry is a link, a file or an empty 0700 directory).
            for path in (self.binding, self.store, self.store_root, self.store_parent):
                if path.is_symlink() or path.is_file():
                    path.unlink()
                elif path.is_dir():
                    path.rmdir()
        run = self.init("pilot")
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assert_private_directory_of_this_user(self.store_parent)
        self.assert_private_directory_of_this_user(self.store_root)
        self.assert_private_directory_of_this_user(self.store)

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
