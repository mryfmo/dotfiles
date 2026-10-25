"""Exercise scripts/orchestrator/hcom-seat against fake hcom, herdr and omp.

The fakes (tests/fixtures/hcom-seat/fake-tool.py under the three names) record argv; the fake hcom plays the herdr
terminal preset so the test sees what omp receives. HOME is a scratch directory holding the three policy overlays and
the three extension directories (the two routes and the stop gate's); the cwd is a scratch git repository with an `origin/main` ref; `HCOM_DIR` is
`$TMPDIR/u7-hcom`. Nothing touches the real `~/.hcom`, `~/.agents` or a herdr pane.
"""

import json
import os
import shlex
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SEAT = ROOT / "scripts/orchestrator/hcom-seat"
FAKE = ROOT / "tests/fixtures/hcom-seat/fake-tool.py"
GATE_DRIVER = ROOT / "home/dot_agents/omp/hooks/tests/launch-driver.ts"
BUN = shutil.which("bun")
GIT_IDENTITY = {
    "GIT_CONFIG_GLOBAL": "/dev/null",
    "GIT_CONFIG_NOSYSTEM": "1",
    "GIT_AUTHOR_NAME": "t",
    "GIT_AUTHOR_EMAIL": "t@example.invalid",
    "GIT_COMMITTER_NAME": "t",
    "GIT_COMMITTER_EMAIL": "t@example.invalid",
}


class HcomSeatTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        root = Path(self.temp.name).resolve()  # physical, so the canonical extension paths hcom-seat passes compare
        self.home = root / "home"
        self.policies = self.home / ".agents/omp/policies"
        self.profiles = self.home / ".agents/omp/profiles"
        self.policies.mkdir(parents=True)
        self.profiles.mkdir(parents=True)
        for role in ("orchestrator", "worker", "audit"):
            (self.policies / f"{role}.yml").write_text("tools: {}\n")
            (self.profiles / f"{role}.yml").write_text("modelRoles: {}\n")
        self.bridge = self.home / ".local/lib/omp-extensions/pi-claude-bridge"
        self.siwc = self.home / ".agents/omp/extensions/openai-siwc"
        self.gate = self.home / ".agents/omp/hooks"
        self.bridge.mkdir(parents=True)
        self.siwc.mkdir(parents=True)
        self.gate.mkdir(parents=True)
        bindir = root / "bin"
        bindir.mkdir()
        for tool in ("hcom", "herdr", "omp"):
            (bindir / tool).symlink_to(FAKE)
        self.calls = root / "calls"
        self.calls.mkdir()
        self.seats = str(root / "seats")
        self.store = Path(os.environ.get("TMPDIR", self.temp.name)) / "u7-hcom"
        self.store.mkdir(exist_ok=True)
        self.repo = root / "repo"
        self.repo.mkdir()
        self.env = {
            **os.environ,
            **GIT_IDENTITY,
            "HOME": str(self.home),
            "PATH": f"{bindir}:{os.environ['PATH']}",
            "HCOM_DIR": str(self.store),
            "FAKE_CALLS": str(self.calls),
        }
        # The checkout's slug (`repo`) is the team unless a test sets one, whatever the caller's session holds.
        self.env.pop("HCOM_TEAM", None)
        self.git("init", "-q")
        self.git("commit", "-q", "--allow-empty", "-m", "init")
        self.git("update-ref", "refs/remotes/origin/main", "HEAD")
        self.head = self.git("rev-parse", "HEAD")

    def git(self, *args, cwd=None):
        return subprocess.run(
            ["git", *args], cwd=cwd or self.repo, env=self.env, capture_output=True, text=True, check=True
        ).stdout.strip()

    def seat(self, *args, cwd=None, **overrides):
        env = {**self.env, **{key: value for key, value in overrides.items() if value is not None}}
        for key in (key for key, value in overrides.items() if value is None):
            env.pop(key, None)
        return subprocess.run(
            [str(SEAT), *args], cwd=cwd or self.repo, env=env, capture_output=True, text=True, check=False
        )

    def calls_of(self, tool):
        path = self.calls / tool
        return [json.loads(line) for line in path.read_text().splitlines()] if path.exists() else []

    def launch_line(self, role, name, directory, *exts, team="repo"):
        """The launch hcom-seat builds: the route's extensions, then the stop gate's directory and the team flag."""
        return [
            "hcom", "omp", "--tag", name, "--dir", directory, "--terminal", "herdr", "--go", "--",
            "--profile", role, "--config", str(self.policies / f"{role}.yml"), "--config", str(self.profiles / f"{role}.yml"),
            *(flag for ext in (*exts, self.gate) for flag in ("-e", str(ext))), "--hcom-team", team,
        ]  # fmt: skip

    def test_a_remote_seat_without_a_login_starts_nothing(self):
        """U37: hcom-seat runs seat-login-preflight beside it before it creates or starts anything."""
        (self.profiles / "worker.yml").write_text("modelRoles:\n  default: claude-bridge/claude-opus-5-5\n")
        fakes = Path(self.temp.name) / "no-keychain"
        fakes.mkdir()
        (fakes / "security").write_text("#!/bin/sh\nexit 44\n")  # the host's real Keychain login never counts
        (fakes / "security").chmod(0o755)
        run = self.seat(
            "worker", "--seats-root", self.seats, SSH_CONNECTION="100.64.0.2 50000 100.64.0.3 22",
            PATH=f"{fakes}:{self.env['PATH']}", CLAUDE_CODE_OAUTH_TOKEN=None, CLAUDE_CONFIG_DIR=None,
        )  # fmt: skip
        self.assertEqual(run.returncode, 2, run.stderr)
        self.assertIn("worker claude-bridge: absent; a login is the operator's step", run.stderr)
        self.assertEqual(self.calls_of("hcom"), [])
        self.assertFalse(Path(self.seats, "worker").exists())

    def test_the_worker_launch_reaches_omp_in_a_worktree_of_origin_main(self):
        clone = f"{self.seats}/worker"
        run = self.seat("worker", "--seats-root", self.seats)
        self.assertEqual(run.returncode, 0, run.stderr)
        expected = self.launch_line("worker", "worker", clone, self.bridge, self.siwc)
        self.assertEqual([call["argv"] for call in self.calls_of("hcom")], [expected[1:]])
        self.assertEqual(self.git("rev-parse", "HEAD", cwd=clone), self.head)
        common = Path(self.git("rev-parse", "--git-common-dir", cwd=clone)).resolve()
        self.assertEqual(common, (self.repo / ".git").resolve())
        (omp,) = self.calls_of("omp")
        self.assertEqual(omp["argv"], expected[expected.index("--") + 1 :])
        self.assertEqual(Path(omp["cwd"]).resolve(), Path(clone).resolve())
        self.assertEqual(
            {key: omp["env"][key] for key in ("HCOM_LAUNCHED", "HCOM_TAG", "HCOM_DIR")},
            {"HCOM_LAUNCHED": "1", "HCOM_TAG": "worker", "HCOM_DIR": str(self.store)},
        )
        self.assertNotIn("HCOM_TEAM", omp["env"], "hcom does not pass HCOM_TEAM into the pane; --hcom-team carries it")
        self.assertEqual(self.calls_of("herdr")[0]["argv"], ["tab", "create", "--label", "worker"])
        again = self.seat("worker", "--seats-root", self.seats)
        self.assertEqual(again.returncode, 0, again.stderr)
        self.assertEqual(self.git("worktree", "list", "--porcelain").count("worktree "), 2)
        foreign = Path(self.seats) / "worker-3"
        foreign.mkdir()
        subprocess.run(["git", "init", "-q"], cwd=foreign, env=self.env, check=True)
        refused = self.seat("worker", "--name", "worker-3", "--seats-root", self.seats)
        self.assertEqual((refused.returncode, refused.stdout), (2, ""), refused.stderr)
        self.assertIn(str(foreign), refused.stderr)
        self.assertEqual(len(self.calls_of("hcom")), 2)

    def test_each_role_gets_its_directory_and_extension_order(self):
        for role, name, directory, exts in (
            ("orchestrator", "orchestrator", str(self.repo.resolve()), (self.bridge, self.siwc)),
            ("worker", "worker-2", f"{self.seats}/worker-2", (self.bridge, self.siwc)),
        ):
            with self.subTest(role=role):
                run = self.seat(role, "--name", name, "--seats-root", self.seats, "--dry-run")
                self.assertEqual(run.returncode, 0, run.stderr)
                self.assertEqual(shlex.split(run.stdout), self.launch_line(role, name, directory, *exts))
        self.assertEqual(self.calls_of("hcom"), [])
        self.assertFalse(Path(self.seats).exists())

    def test_an_absent_optional_extension_is_dropped_and_ext_replaces_the_list(self):
        shutil.rmtree(self.siwc)
        run = self.seat("worker", "--seats-root", self.seats, "--dry-run")
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual(
            shlex.split(run.stdout), self.launch_line("worker", "worker", f"{self.seats}/worker", self.bridge)
        )
        self.siwc.mkdir(parents=True)
        run = self.seat("worker", "--seats-root", self.seats, "--ext", str(self.siwc), "--dry-run")
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual(
            shlex.split(run.stdout), self.launch_line("worker", "worker", f"{self.seats}/worker", self.siwc)
        )

    def test_an_extension_outside_the_allow_list_is_refused_before_launch(self):
        """`--ext` loads only claude.levers.extensions directories (regime-cutover U31)."""
        mine = self.home / "mine"
        mine.mkdir()
        (self.home / "link-to-mine").symlink_to(mine)
        (self.home / "link-to-bridge").symlink_to(self.bridge)
        for ext in (mine, self.home / "link-to-mine", Path(self.temp.name)):
            with self.subTest(ext=ext.name):
                run = self.seat("worker", "--seats-root", self.seats, "--ext", str(ext))
                self.assertEqual(run.returncode, 2, run.stdout)
                self.assertIn("is not in the allow-list (claude.levers.extensions)", run.stderr)
        self.assertEqual(self.calls_of("hcom"), [])
        self.assertFalse(Path(self.seats).exists())
        link = self.home / "link-to-bridge"
        run = self.seat("worker", "--seats-root", self.seats, "--ext", str(link), "--dry-run")
        self.assertEqual(run.returncode, 0, run.stderr)
        # The launch carries the canonical allow-list path, so swapping the symlink after the check changes nothing.
        self.assertEqual(
            shlex.split(run.stdout), self.launch_line("worker", "worker", f"{self.seats}/worker", self.bridge)
        )
        self.assertNotIn(str(link), run.stdout)
        link.unlink()
        link.symlink_to(mine)
        self.assertEqual(self.seat("worker", "--seats-root", self.seats, "--ext", str(link)).returncode, 2)
        self.assertEqual(self.calls_of("hcom"), [])

    @unittest.skipIf(os.geteuid() == 0, "root enters a mode-000 directory, so cd cannot be made to fail")
    def test_an_extension_directory_that_cannot_be_resolved_is_a_refusal(self):
        """`cd` into the extension fails, so its canonical path is unknown: the launch is refused (preferences 21)."""
        self.bridge.chmod(0)
        self.addCleanup(self.bridge.chmod, 0o755)
        run = self.seat("worker", "--seats-root", self.seats, "--dry-run")
        self.assertEqual(run.returncode, 2, run.stdout)
        self.assertIn("cannot resolve extension directory", run.stderr)
        self.assertEqual(self.calls_of("hcom"), [])

    def test_an_unreadable_or_missing_allow_list_is_a_refusal(self):
        """A failed read of the allow-list refuses the launch instead of reading as an empty list (preferences 21)."""
        bindir = Path(self.temp.name) / "bad-awk"
        bindir.mkdir()
        (bindir / "awk").write_text("#!/bin/sh\nexit 2\n")
        (bindir / "awk").chmod(0o755)
        run = self.seat("worker", "--dry-run", PATH=f"{bindir}:{self.env['PATH']}")
        self.assertEqual(run.returncode, 2, run.stdout)
        self.assertIn("cannot read the extension allow-list", run.stderr)

        checkout = Path(self.temp.name) / "checkout"
        (checkout / "scripts/orchestrator").mkdir(parents=True)
        (checkout / "home/dot_agents").mkdir(parents=True)
        shutil.copy2(SEAT, checkout / "scripts/orchestrator/hcom-seat")
        shutil.copy2(SEAT.parent / "regime-env", checkout / "scripts/orchestrator/regime-env")
        manifest = (ROOT / "home/dot_agents/agent-config.yaml").read_text()
        listed = (
            "    extensions:\n      - ~/.local/lib/omp-extensions/pi-claude-bridge\n"
            "      - ~/.agents/omp/extensions/openai-siwc\n      - ~/.agents/omp/hooks\n"
        )
        self.assertIn(listed, manifest)
        (checkout / "home/dot_agents/agent-config.yaml").write_text(manifest.replace(listed, ""))
        run = subprocess.run(
            [str(checkout / "scripts/orchestrator/hcom-seat"), "worker", "--dry-run"],
            cwd=self.repo,
            env=self.env,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(run.returncode, 2, run.stdout)
        self.assertIn("no extension allow-list (claude.levers.extensions)", run.stderr)
        self.assertEqual(self.calls_of("hcom"), [])

    def test_the_store_team_and_seats_root_are_derived_from_the_checkout(self):
        """Without HCOM_DIR, HCOM_TEAM or --seats-root, hcom-seat derives them from the repository (U33)."""
        derived = {"HCOM_DIR": str(self.home / ".local/state/hcom/repo"), "HCOM_TEAM": "repo"}
        run = self.seat("worker", "--dry-run", HCOM_DIR=None, HCOM_TEAM=None)
        self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
        self.assertIn("has no origin file binding it", run.stderr, "only regime-init binds a derived store")
        Path(derived["HCOM_DIR"]).mkdir(parents=True)
        (Path(derived["HCOM_DIR"]) / "origin").write_text(f"{self.repo}\n")
        clone = str(self.home / ".local/state/omp-seats/repo/worker")
        run = self.seat("worker", "--dry-run", HCOM_DIR=None, HCOM_TEAM=None)
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual(shlex.split(run.stdout), self.launch_line("worker", "worker", clone, self.bridge, self.siwc))
        self.assertIn(f"environment HCOM_DIR={derived['HCOM_DIR']} HCOM_TEAM=repo", run.stderr)

        run = self.seat("worker", HCOM_DIR=None, HCOM_TEAM=None)
        self.assertEqual(run.returncode, 0, run.stderr)
        (launch,) = self.calls_of("hcom")
        self.assertEqual(
            {key: launch["env"].get(key) for key in derived}, derived, "the seat inherits the derived pair"
        )
        self.assertEqual(self.git("rev-parse", "HEAD", cwd=clone), self.head)

        run = self.seat("worker", "--dry-run", HCOM_DIR=str(self.store), HCOM_TEAM="explicit")
        self.assertIn(f"environment HCOM_DIR={self.store} HCOM_TEAM=explicit", run.stderr)
        self.assertEqual(shlex.split(run.stdout)[-2:], ["--hcom-team", "explicit"], "an explicit team rides the flag")

    def test_the_team_crosses_the_launch_boundary_as_a_flag_and_the_gate_blocks_on_it(self):
        """An explicit team whose name is not the slug survives hcom dropping HCOM_TEAM, and the gate reads it (U33c).

        The launcher half runs everywhere; the gate half runs the real stop-gate.ts under bun, as omp runs it in
        the pane, with the argv and the environment the fake hcom handed to omp.
        """
        run = self.seat("orchestrator", HCOM_TEAM="custom")  # HCOM_DIR is explicit; the checkout's slug is `repo`
        self.assertEqual(run.returncode, 0, run.stderr)
        (omp,) = self.calls_of("omp")
        self.assertNotIn("HCOM_TEAM", omp["env"])
        self.assertEqual(omp["argv"][-4:], ["-e", str(self.gate), "--hcom-team", "custom"])
        if BUN is None:
            self.skipTest("bun is not installed, so the gate half cannot run here")
        bus = self.home / ".local/bin/common/bus-history.sh"
        bus.parent.mkdir(parents=True)
        # One outstanding TASK the orchestrator sent, on thread `custom` only; the slug's thread is empty.
        bus.write_text(
            '#!/bin/sh\nprintf "%s\\n" "$1" >> "$HOME/bus-calls"\n[ "$1" = custom ] || exit 0\n'
            'printf "7\\t2026-10-24T09:00:00+00:00\\torchestrator\\tworker\\tAGMSG-TASK\\tAGMSG-TASK v1 task_id=c1\\n"\n'
        )
        bus.chmod(0o755)
        # The seat's own name last: omp["env"] carries every HCOM_* the caller's session held.
        env = {**omp["env"], "PATH": os.environ["PATH"], "HOME": str(self.home), "HCOM_NAME": "orchestrator"}

        def gate(argv):
            ran = subprocess.run(
                [BUN, str(GATE_DRIVER), json.dumps(argv)], cwd=omp["cwd"], env=env, capture_output=True, text=True,
                timeout=60, check=False,
            )  # fmt: skip
            self.assertEqual(ran.returncode, 0, ran.stderr)
            return json.loads(ran.stdout)

        blocked = gate(omp["argv"])
        self.assertEqual(blocked["team"], "custom", "the gate exports the team into the seat")
        self.assertEqual(blocked["result"]["decision"], "block")
        self.assertIn("on hcom thread custom: c1 awaiting RESULT (row 7)", blocked["result"]["reason"])
        # Without the flag the same environment has no team, and the gate never guesses the checkout's slug.
        unflagged = gate(omp["argv"][:-2])
        self.assertIsNone(unflagged["result"])
        self.assertEqual(
            unflagged["warnings"],
            [
                "stop-gate: inert, no team (launched without --hcom-team and HCOM_TEAM is unset); the turn ends unchecked."
            ],
        )
        self.assertEqual((self.home / "bus-calls").read_text(), "custom\n")

    def test_a_repository_without_origin_main_seats_at_head(self):
        self.git("update-ref", "-d", "refs/remotes/origin/main")
        run = self.seat("worker", "--seats-root", self.seats)
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertIn("origin/main is absent", run.stderr)
        self.assertEqual(self.git("rev-parse", "HEAD", cwd=f"{self.seats}/worker"), self.head)

    def test_a_broken_or_unreadable_origin_main_is_refused_not_replaced_by_head(self):
        """Only an absent origin/main seats at HEAD; a broken ref, a non-commit or a failed git refuses (audit U33 F1)."""
        ref = Path(self.git("rev-parse", "--git-path", "refs/remotes/origin/main"))
        ref = ref if ref.is_absolute() else self.repo / ref
        tree = self.git("rev-parse", "HEAD^{tree}")
        for label, content, message in (
            ("broken ref", "garbage\n", "does not resolve to a commit"),
            ("tree object", f"{tree}\n", "does not resolve to a commit: tree"),
        ):
            with self.subTest(label):
                ref.write_text(content)
                run = self.seat("worker", "--seats-root", self.seats)
                self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
                self.assertIn(message, run.stderr)
        self.git("update-ref", "refs/remotes/origin/main", self.head)
        wrapper = Path(self.temp.name) / "failing-git"
        wrapper.mkdir()
        real_git = shutil.which("git")
        (wrapper / "git").write_text(
            f'#!/bin/sh\ncase " $* " in *" for-each-ref "*) echo "fatal: injected" >&2; exit 128 ;; esac\nexec "{real_git}" "$@"\n'
        )
        (wrapper / "git").chmod(0o755)
        run = self.seat("worker", "--seats-root", self.seats, PATH=f"{wrapper}:{self.env['PATH']}")
        self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
        self.assertIn("cannot inspect refs/remotes/origin/main", run.stderr)
        self.assertEqual(self.calls_of("hcom"), [])
        self.assertFalse(Path(self.seats).exists())

    def test_a_derived_store_owned_by_another_checkout_is_refused(self):
        store = self.home / ".local/state/hcom/repo"
        store.mkdir(parents=True)
        (store / "origin").write_text("/elsewhere/repo\n")
        run = self.seat("worker", "--dry-run", HCOM_DIR=None, HCOM_TEAM=None)
        self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
        self.assertIn("belongs to /elsewhere/repo", run.stderr)
        self.assertEqual(self.calls_of("hcom"), [])

    def test_refusals_exit_2_before_anything_is_created_or_started(self):
        (self.policies / "orchestrator.yml").unlink()
        outside = Path(self.temp.name) / "outside"
        outside.mkdir()
        for label, args, overrides, cwd in (
            ("unknown role", ["reviewer"], {}, None),
            # U58: the audit is one omp-run.sh per head, never a seat, though its overlays stay installed for omp-run.
            ("the audit is no seat", ["audit"], {}, None),
            ("no role", [], {}, None),
            ("bad name", ["worker", "--name", "Worker/1"], {}, None),
            ("bad team", ["worker"], {"HCOM_TEAM": "Bad Team"}, None),
            ("missing value", ["worker", "--name"], {}, None),
            ("unknown flag", ["worker", "--pane", "w1"], {}, None),
            ("HCOM_DIR unset outside a checkout", ["worker"], {"HCOM_DIR": None}, outside),
            ("hcom absent", ["worker"], {"PATH": "/usr/bin:/bin"}, None),
            ("policy overlay absent", ["orchestrator"], {}, None),
            ("required extension absent", ["worker", "--ext", str(self.home / "nowhere")], {}, None),
            ("outside a checkout", ["worker"], {}, outside),
        ):
            with self.subTest(label):
                run = self.seat(*args, "--seats-root", self.seats, cwd=cwd, **overrides)
                self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
                self.assertTrue(run.stderr.startswith("hcom-seat: "), run.stderr)
        self.assertIn("unknown role 'audit'; expected orchestrator or worker", self.seat("audit", "--dry-run").stderr)
        (self.policies / "orchestrator.yml").write_text("tools: {}\n")
        (self.profiles / "orchestrator.yml").unlink()
        run = self.seat("orchestrator", "--seats-root", self.seats)
        self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
        self.assertIn("profile overlay absent", run.stderr)
        shutil.rmtree(self.bridge)
        run = self.seat("worker", "--seats-root", self.seats)
        self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
        self.assertIn(str(self.bridge), run.stderr)
        self.bridge.mkdir(parents=True)
        shutil.rmtree(self.gate)
        run = self.seat("worker", "--seats-root", self.seats, "--ext", str(self.bridge))
        self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
        self.assertIn(f"extension directory absent: {self.gate}", run.stderr, "--ext never drops the gate")
        self.assertEqual([self.calls_of(tool) for tool in ("hcom", "herdr", "omp")], [[], [], []])
        self.assertFalse(Path(self.seats).exists())


if __name__ == "__main__":
    unittest.main()
