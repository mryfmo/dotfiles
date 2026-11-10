"""Exercise scripts/orchestrator/regime-env, the per-repository derivation the levers source (regime-cutover U33).

Each test sources the helper from the checkout (its own self-check reads the checkout's manifest pin) in a bash
process whose HOME is a scratch directory, with the working directory in a scratch git repository. Nothing reads the
real `~/.local/state`.
"""

import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))  # dotted runs too; discover -s tests/unit already has it
from scratch_git import git_init, quiet_git_env  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
HELPER = ROOT / "scripts/orchestrator/regime-env"
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
PROBE = (
    'printf "%s|%s|%s|%s|%s\\n" "${REGIME_TOPLEVEL:-}" "${REGIME_SLUG:-}" "${HCOM_DIR:-}" "${HCOM_TEAM:-}" '
    '"${REGIME_SEATS_ROOT:-}"'
)
STORE_PROBE = 'printenv REGIME_STORE_ROOT; printf "exported=%s\\n" "$?"'


class RegimeEnvTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.home = self.root / "home"
        self.home.mkdir()
        self.repo = self.root / "Kit Pilot"
        self.repo.mkdir()
        self.env = {"PATH": os.environ["PATH"], "HOME": str(self.home), **GIT_IDENTITY}
        git_init(self.repo, env=self.env)
        self.git("commit", "-q", "--allow-empty", "-m", "init")

    def git(self, *args, cwd=None):
        return subprocess.run(
            ["git", *args], cwd=cwd or self.repo, env=self.env, capture_output=True, text=True, check=True
        ).stdout.strip()

    def bash(self, script, cwd=None, **overrides):
        env = {**self.env, **{key: value for key, value in overrides.items() if value is not None}}
        return subprocess.run(
            ["bash", "-c", f'set -euo pipefail; . "{HELPER}"; {script}'],
            cwd=cwd or self.repo,
            env=env,
            capture_output=True,
            text=True,
            timeout=60,
            check=False,
        )

    def test_the_slug_is_sanitised_to_the_team_grammar(self):
        cases = {
            "/x/dotfiles": "dotfiles",
            "/x/Kit Pilot": "kit-pilot",
            "/x/My.Repo_v2": "my-repo_v2",
            "/x/" + "a" * 50: "a" * 40,
            "/x/dotfiles/": "dotfiles",
        }
        for path, slug in cases.items():
            with self.subTest(path=path):
                run = self.bash(f'regime_slug "{path}"')
                self.assertEqual((run.returncode, run.stdout), (0, slug + "\n"), run.stderr)
        for path in ("/x/.dotfiles", "/x/_x", "/x/-x"):
            with self.subTest(refused=path):
                self.assertEqual(self.bash(f'regime_slug "{path}"').returncode, 1)

    def bind(self):
        store = self.home / ".local/state/hcom/kit-pilot"
        store.mkdir(parents=True, exist_ok=True)
        (store / "origin").write_text(f"{self.repo}\n")
        return store

    def test_a_derived_store_needs_its_origin_except_for_regime_init(self):
        """Only regime-init (--unbound-ok) may use a derived store before its origin binds it (Codex 4366521824)."""
        run = self.bash("regime_env test")
        self.assertEqual(run.returncode, 1)
        self.assertIn("has no origin file binding it", run.stderr)
        self.assertEqual(self.bash("regime_env test --unbound-ok").returncode, 0)

    @staticmethod
    def clear(path):
        """Remove a scratch path that is a symlink or a directory."""
        if path.is_symlink():
            path.unlink()
        elif path.exists():
            shutil.rmtree(path)

    def test_a_symlink_in_the_derived_store_path_is_refused(self):
        """~/.local/state/hcom, the store and origin must be plain (Codex 4366521828), for regime-init too."""
        elsewhere = self.root / "elsewhere"
        elsewhere.mkdir()
        state = self.home / ".local/state"
        state.mkdir(parents=True)
        for label, make in (
            ("parent", lambda: (state / "hcom").symlink_to(elsewhere)),
            ("store", lambda: ((state / "hcom").mkdir(), (state / "hcom/kit-pilot").symlink_to(elsewhere))),
            (
                "origin",
                lambda: (
                    (state / "hcom/kit-pilot").mkdir(parents=True),
                    (state / "hcom/kit-pilot/origin").symlink_to(elsewhere / "o"),
                ),
            ),
        ):
            with self.subTest(symlink=label):
                make()
                run = self.bash("regime_env test --unbound-ok")
                self.assertEqual(run.returncode, 1, run.stderr)
                self.assertIn("is a symlink", run.stderr)
                self.clear(state / "hcom")
        self.assertEqual(list(elsewhere.iterdir()), [], "nothing written through a symlink")

    def test_the_store_root_is_a_fixed_derivation_from_the_physical_home_and_the_slug(self):
        """U215c (the mechanism-change row of 2026-11-07T18:05:48Z, form remove; verdicts U215-11a32ed6 P1 and
        U215-a081d8ba P1 `:127`, P2 `:135` and `:140`): the program stores lie under one root per repository slug,
        `<physical HOME>/.local/state/regime-store/<slug>`, derived from HOME resolved by `pwd -P` and from the slug
        this helper already derives for the hcom store, and from nothing else: no binding file, option or environment
        value chooses it, so nothing a seat writes enters it (hcom-seat grants the hcom store to every seat for the
        bus). It is exported for a derived and for an explicit `HCOM_DIR` alike, for `--unbound-ok` too, and the helper
        makes nothing; a HOME given through a symbolic link resolves to the physical directory; round 2's binding
        `<HCOM_DIR>/store-root`, planted with `<HCOM_DIR>/store` in it and unreadable, is not read (a read would fail
        under a non-root harness; its content never reaches the root). Outside a checkout, with an explicit `HCOM_DIR`,
        there is no slug and the root is exported empty. A refusal (the next test) is the function's return 1; each
        caller maps it to its own status (`regime-init` exit 2, asserted in test_regime_init; `bus-history.sh` and
        `hcom-dispatch` exit 1), so no caller's status is claimed here."""
        hcom_store = self.bind()
        root = self.home / ".local/state/regime-store/kit-pilot"
        for args in ("test", "test --unbound-ok"):
            with self.subTest(args=args):
                run = self.bash(f"regime_env {args}; {STORE_PROBE}")
                self.assertEqual((run.returncode, run.stdout), (0, f"{root}\nexported=0\n"), run.stderr)
        self.assertFalse((self.home / ".local/state/regime-store").exists(), "the helper derives and makes nothing")
        linked_home = self.root / "home-link"
        linked_home.symlink_to(self.home)
        run = self.bash(f"regime_env test; {STORE_PROBE}", HOME=str(linked_home))
        self.assertEqual((run.returncode, run.stdout), (0, f"{root}\nexported=0\n"), "HOME through a link")
        planted = hcom_store / "store-root"
        planted.write_text(f"{hcom_store}/store\n")
        planted.chmod(0)
        run = self.bash(f"regime_env test; {STORE_PROBE}")
        self.assertEqual((run.returncode, run.stdout, run.stderr), (0, f"{root}\nexported=0\n", ""), "not read")
        self.assertEqual(sorted(path.name for path in hcom_store.iterdir()), ["origin", "store-root"])
        explicit = self.root / "explicit"
        explicit.mkdir()
        (explicit / "store-root").write_text(f"{explicit}/store\n")
        run = self.bash(f"regime_env test; {STORE_PROBE}", HCOM_DIR=str(explicit))
        self.assertEqual(
            (run.returncode, run.stdout), (0, f"{root}\nexported=0\n"), "an explicit store chooses nothing"
        )
        outside = self.root / "outside"
        outside.mkdir()
        run = self.bash(f"regime_env test; {STORE_PROBE}", cwd=outside, HCOM_DIR=str(explicit))
        self.assertEqual((run.returncode, run.stdout), (0, "\nexported=0\n"), "no slug outside a checkout")
        self.assertFalse((hcom_store / "store").exists(), "no store under the hcom store")
        self.assertFalse((explicit / "store").exists())

    def test_a_store_root_component_that_is_a_link_a_file_or_unsearchable_is_refused_by_name(self):
        """U215c (verdict U215-a081d8ba P1 `:147`, P2 `:135`): every component of the root from `.local` down is held
        by its own test under a parent this user can search (the shape of seat-login-preflight's
        claude_config_validate): absent, or a real directory of this user that is no symbolic link and that this user
        can search. A link at `regime-store` or at `regime-store/<slug>` is refused by name (return 1; physical
        resolution and the walk leave no textual prefix to pass), a file at either too, and a `.local/state` of mode
        000 is refused naming it, never read as absent and never passed with an empty or a derived root (the
        failed-read rule, standing order 21; skipped as root, who searches everything). Nothing is written."""
        self.bind()
        elsewhere = self.root / "elsewhere"
        elsewhere.mkdir()
        state = self.home / ".local/state"
        parent = state / "regime-store"
        root = parent / "kit-pilot"
        for label, plant, named, reason in (
            ("a link at regime-store", lambda: parent.symlink_to(elsewhere), parent, "is a symlink"),
            ("a link at the root", lambda: (parent.mkdir(), root.symlink_to(elsewhere)), root, "is a symlink"),
            ("a file at regime-store", lambda: parent.write_text(""), parent, "is not a real directory"),
            ("a file at the root", lambda: (parent.mkdir(), root.write_text("")), root, "is not a real directory"),
        ):
            with self.subTest(label):
                plant()
                for args in ("test", "test --unbound-ok"):
                    run = self.bash(f"regime_env {args}; {STORE_PROBE}")
                    self.assertEqual((run.returncode, run.stdout), (1, ""), run.stderr)
                    self.assertIn(f"test: refused: the store root component {named} {reason}", run.stderr)
            # Cleared outside the subTest, so a failing assertion still leaves the next case its clean start.
            for path in (root, parent):
                if path.is_symlink() or path.is_file():
                    path.unlink()
                elif path.is_dir():
                    path.rmdir()
        self.assertEqual(list(elsewhere.iterdir()), [], "nothing written through a link")
        if os.geteuid() == 0:
            self.skipTest("root searches a mode-000 directory")
        state.chmod(0)
        try:
            for args in ("test", "test --unbound-ok"):
                with self.subTest(unsearchable=args):
                    run = self.bash(f"regime_env {args}; {STORE_PROBE}")
                    self.assertEqual((run.returncode, run.stdout), (1, ""), run.stderr)
                    self.assertIn(f"test: refused: cannot search the store root component {state}", run.stderr)
        finally:
            state.chmod(0o700)
        self.assertFalse(parent.exists())

    def test_defaults_derive_from_the_main_checkout_and_explicit_values_win(self):
        self.bind()
        run = self.bash(f"regime_env test; {PROBE}")
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual(
            run.stdout.strip().split("|"),
            [
                str(self.repo),
                "kit-pilot",
                str(self.home / ".local/state/hcom/kit-pilot"),
                "kit-pilot",
                str(self.home / ".local/state/omp-seats/kit-pilot"),
            ],
        )
        worktree = self.root / "seats/worker"
        self.git("worktree", "add", "-q", "--detach", str(worktree), "HEAD")
        run = self.bash(f"regime_env test; {PROBE}", cwd=worktree)
        self.assertEqual(run.stdout.strip().split("|")[:2], [str(self.repo), "kit-pilot"], "a seat worktree")
        run = self.bash(f"regime_env test; {PROBE}", HCOM_DIR="/s", HCOM_TEAM="t", REGIME_SEATS_ROOT="/r")
        self.assertEqual(run.stdout.strip().split("|")[2:], ["/s", "t", "/r"])
        run = self.bash('regime_env test; printf "%s\\n" "$(printenv HCOM_DIR)|$(printenv HCOM_TEAM)"')
        self.assertEqual(run.stdout.strip(), f"{self.home}/.local/state/hcom/kit-pilot|kit-pilot", "exported")

    def test_outside_a_checkout_only_an_explicit_store_passes(self):
        outside = self.root / "outside"
        outside.mkdir()
        run = self.bash("regime_env test", cwd=outside)
        self.assertEqual(run.returncode, 1)
        self.assertIn("test: not inside a git checkout and HCOM_DIR is unset", run.stderr)
        run = self.bash(f"regime_env test; {PROBE}", cwd=outside, HCOM_DIR="/s")
        self.assertEqual((run.returncode, run.stdout.strip().split("|")[:3]), (0, ["", "", "/s"]), run.stderr)

    def test_a_store_whose_origin_names_another_checkout_is_refused(self):
        store = self.home / ".local/state/hcom/kit-pilot"
        store.mkdir(parents=True)
        (store / "origin").write_text(f"{self.repo}\n")
        self.assertEqual(self.bash("regime_env test").returncode, 0, "its own origin")
        (store / "origin").write_text("/elsewhere/Kit Pilot\n")
        run = self.bash("regime_env test")
        self.assertEqual(run.returncode, 1)
        self.assertIn("test: refused: the store", run.stderr)
        self.assertIn("belongs to /elsewhere/Kit Pilot", run.stderr)
        self.assertEqual(self.bash("regime_env test", HCOM_DIR=str(store)).returncode, 0, "an explicit store wins")

    def test_a_failing_producer_refuses(self):
        """An unreadable origin and a failing tr refuse instead of deriving (preferences 21)."""
        store = self.home / ".local/state/hcom/kit-pilot"
        (store / "origin").mkdir(parents=True)
        run = self.bash("regime_env test")
        self.assertEqual(run.returncode, 1)
        self.assertIn("cannot read", run.stderr)
        shutil.rmtree(store)
        fake = self.root / "fake"
        fake.mkdir()
        (fake / "tr").write_text("#!/bin/sh\nexit 3\n")
        (fake / "tr").chmod(0o755)
        run = self.bash("regime_env test", PATH=f"{fake}:{self.env['PATH']}")
        self.assertEqual(run.returncode, 1)
        self.assertIn("cannot derive a repository slug", run.stderr)

    def test_dispatch_and_history_refuse_a_derived_store_that_does_not_exist(self):
        """The derived store is refused like an explicit one until a seat launch creates hcom.db (README "hcom bus")."""
        self.bind()
        for script, args in (
            ("bus-history.sh", ["kit-pilot"]),
            ("hcom-dispatch", ["kit-pilot", "operator", "worker", "PING v1 task_id=x"]),
        ):
            with self.subTest(script=script):
                run = subprocess.run(
                    [str(ROOT / "scripts/orchestrator" / script), *args],
                    cwd=self.repo,
                    env=self.env,
                    capture_output=True,
                    text=True,
                    timeout=60,
                    check=False,
                )
                self.assertEqual(run.returncode, 1, run.stdout)
                self.assertIn(
                    f"store absent: ${{HCOM_DIR}}/hcom.db (HCOM_DIR={self.home}/.local/state/hcom/kit-pilot)",
                    run.stderr,
                )
                self.assertFalse((self.home / ".local/state/hcom/kit-pilot/hcom.db").exists(), "nothing created")


if __name__ == "__main__":
    unittest.main()
