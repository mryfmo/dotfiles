"""Exercise scripts/orchestrator/hcom-seat against fake hcom, herdr and omp.

The fakes (tests/fixtures/hcom-seat/fake-tool.py under the three names) record argv; the fake hcom plays the herdr
terminal preset so the test sees what omp receives. HOME is a scratch directory holding the three policy overlays and
the three extension directories (the two routes and the stop gate's); the cwd is a scratch git repository with an `origin/main` ref; `HCOM_DIR` is
`$TMPDIR/u7-hcom`. Nothing touches the real `~/.hcom`, `~/.agents` or a herdr pane.
"""

import json
import os
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))  # dotted runs too; discover -s tests/unit already has it
from scratch_git import git_init, quiet_git_env  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
SEAT = ROOT / "scripts/orchestrator/hcom-seat"
FAKE = ROOT / "tests/fixtures/hcom-seat/fake-tool.py"
GATE_DRIVER = ROOT / "home/dot_agents/omp/hooks/tests/launch-driver.ts"
BUN = shutil.which("bun")
# A real executable binary (Mach-O on macOS, ELF on Linux), for tools hcom-seat requires to be no script.
BINARY_STAND_IN = Path(os.path.realpath("/usr/bin/true"))
SYSTEM_PATH = "/usr/bin:/bin"


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
        self.rules = self.home / ".agents/omp/rules"
        self.rules.mkdir(parents=True)
        for role in ("orchestrator", "worker"):
            (self.rules / f"{role}.md").write_text("## Regime\n")
        self.bridge = self.home / ".local/lib/omp-extensions/pi-claude-bridge"
        self.siwc = self.home / ".agents/omp/extensions/openai-siwc"
        self.gate = self.home / ".agents/omp/hooks"
        self.bridge.mkdir(parents=True)
        self.siwc.mkdir(parents=True)
        self.gate.mkdir(parents=True)
        bindir = root / "bin"
        bindir.mkdir()
        self.bindir = bindir
        # srt plays the sandbox (U85). Copies, not links: hcom-seat runs srt and omp by their physical file, and the
        # fake reads its role from its own name.
        for tool in ("hcom", "herdr", "omp", "srt"):
            shutil.copy(FAKE, bindir / tool)
        # bwrap, socat and rg only satisfy the Linux prerequisite check, which requires binaries (srt runs them by
        # path): copies of the system's `true` binary, so the check runs as written on every host.
        for tool in ("bwrap", "socat", "rg"):
            shutil.copy(BINARY_STAND_IN, bindir / tool)
        self.tools = (root / "home/.local/state/hcom-seat/tools").resolve()
        self.calls = root / "calls"
        self.calls.mkdir()
        self.seats = str(root / "seats")
        self.store = Path(os.environ.get("TMPDIR", self.temp.name)) / "u7-hcom"
        self.store.mkdir(exist_ok=True)
        self.repo = root / "repo"
        self.repo.mkdir()
        # The environment is built, never inherited: the fake bin and the system directories only, under the scratch
        # HOME, so no tool of the host or the runner (a mise shim of claude, a Homebrew jq) reaches hcom-seat's
        # resolution unless a test plants it. No HCOM_* marker, team or login variable of the caller's session leaks.
        self.env = {
            **GIT_IDENTITY,
            "HOME": str(self.home),
            "PATH": f"{bindir}:{SYSTEM_PATH}",
            "TMPDIR": os.environ.get("TMPDIR", tempfile.gettempdir()),
            "HCOM_DIR": str(self.store),
            "FAKE_CALLS": str(self.calls),
        }
        git_init(self.repo, env=self.env)
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
            "--append-system-prompt", str(self.rules / f"{role}.md"),
            *(flag for ext in (*exts, self.gate) for flag in ("-e", str(ext))), "--hcom-team", team,
        ]  # fmt: skip

    def test_a_remote_seat_without_a_login_starts_nothing(self):
        """U37: hcom-seat runs seat-login-preflight beside it before it creates or starts anything. U85 round 28: the
        preflight reads the Keychain only through `security`, a tool hcom-seat resolves, so the test's fake answers
        and no test queries the host's real Keychain."""
        (self.profiles / "worker.yml").write_text("modelRoles:\n  default: claude-bridge/claude-opus-5-5\n")
        fakes = Path(self.temp.name) / "no-keychain"
        fakes.mkdir()
        # security is a resolved tool (U85 round 28), the preflight's one Keychain reader: this fake on the caller's PATH
        # is what it runs, so the host's real Keychain is never queried and its login never counts.
        queries = Path(self.temp.name) / "keychain-queries"
        (fakes / "security").write_text(
            f'#!/bin/sh\necho "$*" >> {shlex.quote(str(queries))}\nexit "${{FAKE_KEYCHAIN_STATUS:-44}}"\n'
        )
        (fakes / "security").chmod(0o755)

        def launch(**extra):
            return self.seat(
                "worker", "--seats-root", self.seats, SSH_CONNECTION="100.64.0.2 50000 100.64.0.3 22",
                PATH=f"{fakes}:{self.env['PATH']}", CLAUDE_CODE_OAUTH_TOKEN=None, CLAUDE_CONFIG_DIR=None, **extra,
            )  # fmt: skip

        run = launch()
        self.assertEqual(run.returncode, 2, run.stderr)
        self.assertIn("worker claude-bridge: absent; a login is the operator's step", run.stderr)
        self.assertEqual(self.calls_of("hcom"), [])
        self.assertFalse(Path(self.seats, "worker").exists())
        self.assertEqual((self.tools / "security").resolve(), (fakes / "security").resolve())
        if sys.platform == "darwin":
            # The Keychain answer is the fake's, whatever the host's Keychain holds: a login there launches the seat.
            self.assertEqual(queries.read_text(), "find-generic-password -s Claude Code-credentials\n")
            run = launch(FAKE_KEYCHAIN_STATUS="0")
            self.assertEqual(run.returncode, 0, run.stderr)
            self.assertIn("worker claude-bridge: login present (Keychain item)", run.stderr)
            self.assertEqual(len(self.calls_of("hcom")), 1)

    def test_a_remote_siwc_seat_reads_its_registration_with_the_resolved_jq(self):
        """U85 round 22: seat-login-preflight reads the openai-siwc registration with jq, and macOS 14 has no
        /usr/bin/jq, so hcom-seat resolves jq like every tool (checked, linked into its private tool directory). With
        the system jq unusable, a jq on the caller's PATH validates the login and the seat launches; with no usable jq
        the preflight refuses the record as unreadable."""
        if sys.platform != "darwin" or not Path("/usr/bin/sandbox-exec").exists():
            self.skipTest("hiding the system jq needs sandbox-exec (macOS); Linux always has /usr/bin/jq")
        # A jq binary to plant, one whose copy runs: the host's own (never a shim: its physical file must be jq), else
        # the system's (macOS launch constraints stop a copy of a platform binary, so each copy is tried first).
        planted_jq = Path(self.temp.name).resolve() / "jq-probe"
        candidates = [Path(p).resolve() for p in (shutil.which("jq"), "/usr/bin/jq") if p and Path(p).exists()]
        real_jq = None
        for candidate in (c for c in candidates if c.name.startswith("jq")):
            shutil.copy(candidate, planted_jq)
            probe = subprocess.run([str(planted_jq), "-n", "1"], capture_output=True, text=True, check=False)
            if probe.returncode == 0:
                real_jq = candidate
                break
        if real_jq is None:
            self.skipTest(f"no jq binary on this host whose copy runs (tried {candidates})")
        real_git = shutil.which("git", path=SYSTEM_PATH)
        if real_git is None:
            self.skipTest("no git in /usr/bin or /bin")
        (self.profiles / "worker.yml").write_text("modelRoles:\n  default: openai-siwc/gpt-6-astra\n")
        agent = self.home / ".omp/profiles/worker/agent"
        (agent / "openai-siwc").mkdir(parents=True)
        host = "urn:uuid:12345678-1234-4123-8123-123456789abc"
        (agent / "openai-siwc/registration.json").write_text(json.dumps({"hostId": host, "clientId": "oaiapp_fake"}))
        (agent / "agent.db").write_text("never read")
        fakes = Path(self.temp.name).resolve() / "siwc-bin"
        fakes.mkdir()
        (fakes / "bun").write_text("#!/bin/sh\nprintf '1\\n'\n")  # src/credentials.ts: one openai-siwc login
        (fakes / "bun").chmod(0o755)
        (fakes / "git").symlink_to(real_git)
        no_system_jq = '(version 1)(allow default)(deny process-exec (literal "/usr/bin/jq"))'
        # The caller's PATH holds exactly what the test planted: the fakes (bun, git, later jq), the fake bin and /bin;
        # /usr/bin, where macOS 15 keeps a jq, is left out, and its jq is denied to every process besides.
        bare = f"{self.bindir}:/bin"

        def launch(path, name):
            env = {**self.env, "PATH": path, "SSH_CONNECTION": "100.64.0.2 50000 100.64.0.3 22"}
            argv = ["/usr/bin/sandbox-exec", "-p", no_system_jq, str(SEAT), "worker", "--name", name]
            return subprocess.run(
                [*argv, "--seats-root", self.seats], cwd=self.repo, env=env, capture_output=True, text=True, check=False
            )

        run = launch(f"{fakes}:{bare}", "worker")
        # The preflight's refusal of an unreadable record (exit 1): `no jq on PATH` where no system jq exists (macOS
        # 14), a jq that cannot run where it exists but is hidden here.
        self.assertEqual((run.returncode, run.stdout), (1, ""), run.stderr)
        self.assertRegex(
            run.stderr, r"worker openai-siwc: unreadable \((no jq on PATH to read )?\S+registration\.json\)"
        )
        self.assertEqual(self.calls_of("hcom"), [])
        shutil.copy(real_jq, fakes / "jq")
        run = launch(f"{fakes}:{bare}", "worker")
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual((self.tools / "jq").resolve(), (fakes / "jq").resolve())
        self.assertEqual(len(self.calls_of("hcom")), 1)

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
        # The seat shim runs omp under srt with --no-extensions first (U85, U66).
        self.assertEqual(omp["argv"], ["--no-extensions", *expected[expected.index("--") + 1 :]])
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
        git_init(foreign, env=self.env)
        refused = self.seat("worker", "--name", "worker-3", "--seats-root", self.seats)
        self.assertEqual((refused.returncode, refused.stdout), (2, ""), refused.stderr)
        self.assertIn(str(foreign), refused.stderr)
        self.assertEqual(len(self.calls_of("hcom")), 2)

    def test_a_seat_directory_holding_omp_project_config_is_refused_before_hcom_starts(self):
        """U66 F005: omp merges the cwd's .omp/config.yml before disabledProviders binds, so the seat never starts."""
        for role, name, directory in (
            ("worker", "worker", Path(self.seats) / "worker"),
            ("orchestrator", "orchestrator", self.repo),
        ):
            with self.subTest(role=role):
                if role == "worker":
                    self.assertEqual(self.seat("worker", "--seats-root", self.seats).returncode, 0)
                (directory / ".omp").mkdir()
                (directory / ".omp/config.yml").write_text("tools:\n  approval:\n    eval: allow\n")
                before = len(self.calls_of("hcom"))
                run = self.seat(role, "--name", name, "--seats-root", self.seats)
                self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
                self.assertIn("seat directory holds .omp, whose project settings omp would apply", run.stderr)
                self.assertEqual(len(self.calls_of("hcom")), before)
                shutil.rmtree(directory / ".omp")
                (directory / ".omp").symlink_to(self.home)
                self.assertEqual(self.seat(role, "--name", name, "--seats-root", self.seats).returncode, 2)
                (directory / ".omp").unlink()

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
        """A missing allow-list refuses the launch instead of reading as an empty list (preferences 21).

        The allow-list is read by the system awk (U85 round 4: no caller PATH entry runs anything), so a failing awk
        planted on the caller's PATH is never consulted; the read keeps its refusal on a failed status.
        """
        bindir = Path(self.temp.name) / "bad-awk"
        bindir.mkdir()
        (bindir / "awk").write_text("#!/bin/sh\nexit 2\n")
        (bindir / "awk").chmod(0o755)
        run = self.seat("worker", "--dry-run", PATH=f"{bindir}:{self.env['PATH']}")
        self.assertEqual(run.returncode, 0, run.stderr)

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
            'printf "7\\t2026-10-24T09:00:00+00:00\\torchestrator\\tworker\\tTASK\\tTASK v1 task_id=c1\\n"\n'
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
        real_git = shutil.which("git", path=SYSTEM_PATH)
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
        (self.profiles / "orchestrator.yml").write_text("modelRoles: {}\n")
        # U75: the seat's standing rules ride --append-system-prompt; omp reads a missing path as literal text, so an
        # absent or empty rules file is refused before anything starts.
        for content in (None, ""):
            with self.subTest(rules=content):
                rules = self.rules / "orchestrator.md"
                rules.unlink()
                if content is not None:
                    rules.write_text(content)
                run = self.seat("orchestrator", "--seats-root", self.seats)
                self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
                self.assertIn(f"standing rules absent or empty: {rules}", run.stderr)
                rules.write_text("## Regime\n")
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

    def settings_of(self, name):
        return json.loads(Path(self.seats, ".sandbox", name, "srt-settings.json").read_text())

    def test_omp_runs_under_srt_behind_a_canary_with_the_seat_roots(self):
        """U85: hcom pins the per-seat shim, which proves the sandbox with a canary and then runs omp under srt."""
        run = self.seat("worker", "--seats-root", self.seats)
        self.assertEqual(run.returncode, 0, run.stderr)
        shim = Path(self.seats, ".sandbox/worker/bin/omp")
        settings = Path(self.seats, ".sandbox/worker/srt-settings.json")
        canary, launch = self.calls_of("srt")
        self.assertEqual(canary["argv"][:5], ["--settings", str(settings), "--", "/bin/sh", "-c"])
        self.assertEqual(
            canary["argv"][-3:], [str(shim.parent.parent / "canary"), str(settings), str(self.home / ".ssh")]
        )
        (omp,) = self.calls_of("omp")
        # Both run by their physical argv: the fake's interpreter, then the file itself (U85 round 2).
        self.assertEqual(launch["argv"][:3], ["--settings", str(settings), "--"])
        # Inside the sandbox /usr/bin/env gives omp the seat's working PATH (U85 round 4).
        self.assertEqual(launch["argv"][3], "/usr/bin/env")
        self.assertTrue(launch["argv"][4].startswith(f"PATH={self.tools}:/usr/bin:/bin:/usr/sbin:/sbin:"))
        self.assertEqual(launch["argv"][5], os.path.realpath(launch["argv"][5]))
        self.assertEqual(launch["argv"][6:], [str(self.bindir / "omp"), *omp["argv"]])
        worker = self.settings_of("worker")
        clone = str(Path(self.seats, "worker"))
        write, deny_read = worker["filesystem"]["allowWrite"], worker["filesystem"]["denyRead"]
        self.assertIn(clone, write)
        self.assertIn(str((self.repo / ".git").resolve()), write)
        self.assertNotIn(str(self.repo), write, "a worker writes its clone and the git store, not the checkout")
        self.assertNotIn(self.seats, write)
        for path in (".ssh", ".aws", ".codex", ".omp/agent", "Workspace", ".local/share/chezmoi"):
            self.assertIn(str(self.home / path), deny_read)
        self.assertIn(self.seats, deny_read, "a worker reads no other seat")
        self.assertIn(str(shim.parent.parent.parent), worker["filesystem"]["denyWrite"], "every seat's sandbox")
        self.assertIn(str((self.repo / ".git/config").resolve()), worker["filesystem"]["denyWrite"])
        self.assertEqual(worker["network"]["allowUnixSockets"], [])
        self.assertNotIn("example.com", worker["network"]["allowedDomains"])
        # srt 0.0.81 grants local binding on every interface, so no seat gets it (U85 round 3).
        self.assertIs(worker["network"]["allowLocalBinding"], False)
        # The protected set and the sandbox come from one list: the write roots include the writable file.
        self.assertIn(str(self.home.resolve() / ".claude.json"), write)
        run = self.seat("orchestrator", "--seats-root", self.seats)
        self.assertEqual(run.returncode, 0, run.stderr)
        orchestrator = self.settings_of("orchestrator")
        # The orchestrator launches no seat (U85 round 2): no herdr socket, no write to the seats root or a sandbox.
        self.assertEqual(orchestrator["network"]["allowUnixSockets"], [])
        self.assertNotIn(self.seats, orchestrator["filesystem"]["allowWrite"])
        self.assertIn(str(self.repo.resolve()), orchestrator["filesystem"]["allowWrite"])
        self.assertIn(str(Path(self.seats, ".sandbox")), orchestrator["filesystem"]["denyWrite"])
        self.assertIn(str(Path(self.seats, ".sandbox")), orchestrator["filesystem"]["denyRead"])

    def test_the_canary_runs_under_a_posix_shell(self):
        """U85 round 2: under dash (Ubuntu's /bin/sh) the canary's denied write must not end the shell."""
        dash = shutil.which("dash")
        if dash is None:
            self.skipTest("dash is not installed")
        run = self.seat("worker", "--seats-root", self.seats, FAKE_SRT_SH=dash)
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual(len(self.calls_of("omp")), 1)

    def test_a_launch_from_inside_a_seat_is_refused(self):
        """U85 round 2: no seat launches a seat, by its environment markers or by its sandbox's read deny."""
        for marker in ("HCOM_LAUNCHED", "HCOM_PROCESS_ID", "HCOM_SEAT_SANDBOX"):
            with self.subTest(marker):
                run = self.seat("worker", "--seats-root", self.seats, "--dry-run", **{marker: "1"})
                self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
                self.assertIn(f"refused inside a seat ({marker} is set)", run.stderr)
        sandboxes = Path(self.seats, ".sandbox")
        sandboxes.mkdir(parents=True)
        sandboxes.chmod(0)
        self.addCleanup(sandboxes.chmod, 0o700)
        run = self.seat("worker", "--seats-root", self.seats)
        self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
        self.assertIn("refused inside a seat sandbox", run.stderr)
        self.assertEqual(self.calls_of("hcom"), [])
        self.assertFalse(Path(self.seats, "worker").exists())

    def test_a_canary_that_finds_the_sandbox_open_starts_no_omp(self):
        """U85, failure injection: an srt that does not contain the canary's probes never reaches omp."""
        for answer in ("write-open read-denied ssh-denied", "write-denied read-open ssh-denied",
                       "write-denied read-denied ssh-open", ""):  # fmt: skip
            with self.subTest(answer):
                run = self.seat("worker", "--seats-root", self.seats, FAKE_SRT_CANARY=answer)
                self.assertEqual(run.returncode, 2, run.stderr)
                self.assertIn("the sandbox does not hold", run.stderr)
                self.assertEqual(self.calls_of("omp"), [])

    def test_a_missing_or_seat_writable_srt_is_refused_before_anything_starts(self):
        (self.bindir / "srt").unlink()
        run = self.seat("worker", "--seats-root", self.seats)
        self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
        self.assertIn("srt not found (mise which, then the caller's PATH)", run.stderr)
        self.assertFalse(Path(self.seats).exists())
        # An srt whose physical file a seat could rewrite would run the next launch uncontained: a copy inside the
        # checkout (the orchestrator's root), and a link outside every root whose target is in the hcom store.
        planted = self.repo / "tools"
        planted.mkdir()
        shutil.copy(FAKE, planted / "srt")
        run = self.seat("orchestrator", "--seats-root", self.seats, PATH=f"{planted}:{self.env['PATH']}")
        self.assertEqual(run.returncode, 2, run.stderr)
        self.assertIn(f"lies under the seat write root {self.repo.resolve()}", run.stderr)
        outside = Path(self.temp.name).resolve() / "outside-bin"
        outside.mkdir()
        target = self.store / "u85-srt"
        shutil.copy(FAKE, target)
        self.addCleanup(target.unlink)
        (outside / "srt").symlink_to(target)
        run = self.seat("worker", "--seats-root", self.seats, PATH=f"{outside}:{self.env['PATH']}")
        self.assertEqual(run.returncode, 2, run.stderr)
        self.assertIn(f"srt {target.resolve()} is or lies under the seat write root {self.store.resolve()}", run.stderr)
        # The interpreter of a `#!` line is held to the same rule: an absolute one in the hcom store is refused, and
        # a `#!/usr/bin/env` name is looked up only in the private tool directory and the system directories.
        interp = self.store / "u85interp"
        shutil.copy("/bin/sh", interp)
        self.addCleanup(interp.unlink)
        (outside / "srt").unlink()
        (outside / "srt").write_text(f"#!{interp}\n" + FAKE.read_text().split("\n", 1)[1])
        (outside / "srt").chmod(0o755)
        run = self.seat("worker", "--seats-root", self.seats, PATH=f"{outside}:{self.env['PATH']}")
        self.assertEqual(run.returncode, 2, run.stderr)
        # The interpreter is named as its `#!` line spells it (the path the kernel follows), the root physically.
        self.assertRegex(run.stderr, rf"srt \S*/u85interp is or lies under the seat write root {self.store.resolve()}")
        (outside / "srt").write_text("#!/usr/bin/env u85interp\n" + FAKE.read_text().split("\n", 1)[1])
        (outside / "u85interp").symlink_to(interp)
        run = self.seat("worker", "--seats-root", self.seats, PATH=f"{outside}:{self.env['PATH']}")
        self.assertEqual(run.returncode, 2, run.stderr)
        self.assertIn("srt: interpreter u85interp not found on PATH", run.stderr)
        # A writable file root, not only a directory: an executable at ~/.claude.json reached through a PATH link.
        claude_json = self.home / ".claude.json"
        shutil.copy(FAKE, claude_json)
        (outside / "srt").unlink()
        (outside / "srt").symlink_to(claude_json)
        run = self.seat("worker", "--seats-root", self.seats, PATH=f"{outside}:{self.env['PATH']}")
        self.assertEqual(run.returncode, 2, run.stderr)
        real = claude_json.resolve()
        self.assertIn(f"srt {real} is or lies under the seat write root {real}", run.stderr)
        self.assertEqual(self.calls_of("hcom"), [])

    def test_hcom_and_herdr_run_by_the_physical_argv_that_was_checked(self):
        """U85 round 3: the launch execs hcom's checked physical file, and hcom's own lookups reach wrappers of it."""
        real = Path(self.temp.name).resolve() / "real-bin"
        real.mkdir()
        links = Path(self.temp.name).resolve() / "link-bin"
        links.mkdir()
        for tool in ("hcom", "herdr"):
            (self.bindir / tool).rename(real / tool)
            (links / tool).symlink_to(real / tool)
        run = self.seat("worker", "--seats-root", self.seats, PATH=f"{links}:{self.env['PATH']}")
        self.assertEqual(run.returncode, 0, run.stderr)
        (hcom,) = self.calls_of("hcom")
        self.assertEqual(hcom["argv0"], str(real / "hcom"), "exec'd by its physical file, not the PATH link")
        herdr = self.calls_of("herdr")
        self.assertTrue(herdr)
        self.assertEqual({call["argv0"] for call in herdr}, {str(real / "herdr")})
        for tool in ("hcom", "herdr"):
            wrapper = Path(self.seats, ".sandbox/worker/bin", tool).read_text()
            self.assertIn(shlex.quote(str(real / tool)), wrapper)

    def plant(self, directory, *names):
        """Executables that record their own run in `<temp>/planted-ran` and fail, as a seat's planted helper would."""
        directory.mkdir(parents=True, exist_ok=True)
        marker = Path(self.temp.name) / "planted-ran"
        for tool in names:
            (directory / tool).write_text(f'#!/bin/sh\necho "{tool} $*" >> {shlex.quote(str(marker))}\nexit 1\n')
            (directory / tool).chmod(0o755)
        return marker

    def test_no_caller_path_entry_runs_a_helper(self):
        """U85 rounds 4 and 6: helpers planted in a seat-writable directory on the caller's PATH never run, bash (the
        interpreter of hcom-seat itself, `#!/bin/bash`) included.

        The system tools hcom-seat and its children call by name (sed, awk, git's helpers, uname, mkdir, mv, ls)
        come from the fixed system directories; a tool resolved from the caller's PATH (git, and jq, which
        seat-login-preflight reads with, U85 round 22) inside a seat write root is refused before it runs.
        """
        planted = self.repo / "bin"  # the checkout, which the orchestrator seat writes
        marker = self.plant(
            planted, "sed", "awk", "uname", "mkdir", "mv", "ls", "cat", "chmod", "env", "readlink", "stat", "bash"
        )
        run = self.seat("worker", "--seats-root", self.seats, PATH=f"{planted}:{self.env['PATH']}")
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertFalse(marker.exists(), marker.read_text() if marker.exists() else "")
        for tool in ("jq", "git"):
            with self.subTest(tool=tool):
                self.plant(planted, tool)
                run = self.seat(
                    "worker", "--seats-root", self.seats, "--name", "worker-2", PATH=f"{planted}:{self.env['PATH']}"
                )
                self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
                self.assertIn(
                    f"{tool} {planted.resolve()}/{tool} is or lies under the seat write root {self.repo.resolve()}",
                    run.stderr,
                )
                self.assertFalse(marker.exists(), marker.read_text() if marker.exists() else "")
                self.assertFalse(Path(self.seats, "worker-2").exists())
                (planted / tool).unlink()

    def test_the_launch_path_never_inherits_a_caller_path_entry(self):
        """U85 round 4: a trailing `:` (the cwd) or any caller entry never reaches hcom, the shim or srt."""
        run = self.seat("worker", "--seats-root", self.seats, PATH=f"{self.env['PATH']}:")
        self.assertEqual(run.returncode, 0, run.stderr)
        sandbox_bin = Path(self.seats, ".sandbox/worker/bin").resolve()
        fixed = f"{self.tools}:/usr/bin:/bin:/usr/sbin:/sbin"
        (hcom,) = self.calls_of("hcom")
        self.assertEqual(hcom["path"], f"{sandbox_bin}:{fixed}")
        for call in self.calls_of("srt"):
            self.assertEqual(call["path"], f"{sandbox_bin}:{fixed}")
        self.assertEqual(Path(self.seats, ".sandbox/worker/bin/omp").read_text().count(f"outer_path={sandbox_bin}:"), 1)

    def test_a_case_alias_or_a_hardlink_of_a_writable_file_is_refused(self):
        """U85 round 5: protection compares (device, inode), never path text, so neither alias passes."""
        outside = Path(self.temp.name).resolve() / "alias-bin"
        outside.mkdir()
        claude_json = self.home / ".claude.json"  # a writable file root of every seat
        shutil.copy(FAKE, claude_json)
        (self.bindir / "srt").unlink()
        os.link(claude_json, outside / "srt")
        run = self.seat("worker", "--seats-root", self.seats, PATH=f"{outside}:{self.env['PATH']}")
        self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
        self.assertIn(f"srt {outside}/srt is or lies under the seat write root {claude_json.resolve()}", run.stderr)
        (outside / "srt").unlink()
        alias = self.home / ".CLAUDE.JSON"
        if not alias.exists():
            self.skipTest("the file system is case-sensitive, so no case alias exists")
        (outside / "srt").symlink_to(alias)
        run = self.seat("worker", "--seats-root", self.seats, PATH=f"{outside}:{self.env['PATH']}")
        self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
        self.assertIn("/.CLAUDE.JSON is or lies under the seat write root", run.stderr)
        self.assertEqual(self.calls_of("hcom"), [])

    def test_mise_in_another_seats_root_never_runs(self):
        """U85 round 5: another program's seat roots (its checkout outside ~/Workspace) are protected before mise runs."""
        other = Path(self.temp.name).resolve() / "elsewhere/checkout"
        settings = self.home / ".local/state/omp-seats/other/.sandbox/orchestrator/srt-settings.json"
        settings.parent.mkdir(parents=True)
        settings.write_text(json.dumps({"filesystem": {"allowWrite": [str(other)]}}))
        marker = self.plant(other / "bin", "mise")
        run = self.seat("worker", "--seats-root", self.seats, PATH=f"{other}/bin:{self.env['PATH']}")
        self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
        self.assertIn(f"mise {other}/bin/mise is or lies under the seat write root {other}", run.stderr)
        self.assertFalse(marker.exists(), marker.read_text() if marker.exists() else "")
        self.assertFalse(Path(self.seats).exists())

    def test_a_seat_commits_unsigned_under_a_signing_host_config(self):
        """U85 round 5: the shim turns signing off, so a host commit.gpgsign=true cannot fail the seat's commits."""
        run = self.seat("worker", "--seats-root", self.seats)
        self.assertEqual(run.returncode, 0, run.stderr)
        (omp,) = self.calls_of("omp")
        signing = Path(self.temp.name) / "signing.gitconfig"
        signing.write_text("[commit]\n\tgpgsign = true\n[tag]\n\tgpgsign = true\n[gpg]\n\tprogram = /usr/bin/false\n")
        clone = Path(self.seats, "worker")
        # The caller's own GIT_CONFIG_COUNT/_KEY_n/_VALUE_n (a test run that turns signing off) outrank the file.
        inherited = ("GIT_CONFIG_COUNT", "GIT_CONFIG_KEY_", "GIT_CONFIG_VALUE_")
        # Stripped, they are added back for background maintenance only (U100): signing is still the file's.
        host = quiet_git_env(
            {k: v for k, v in self.env.items() if not k.startswith(inherited)} | {"GIT_CONFIG_GLOBAL": str(signing)}
        )

        def commit(env, message):
            argv = ["git", "-C", str(clone), "commit", "-q", "--allow-empty", "-m", message]
            return subprocess.run(argv, env=env, capture_output=True, text=True, check=False)

        self.assertNotEqual(commit(host, "host").returncode, 0, "the signing config fails a plain commit")
        seat = commit({**host, **omp["git_config"]}, "seat")
        self.assertEqual(seat.returncode, 0, seat.stderr)
        tag = subprocess.run(["git", "-C", str(clone), "tag", "-a", "t1", "-m", "t"], env={**host, **omp["git_config"]},
                             capture_output=True, text=True, check=False)  # fmt: skip
        self.assertEqual(tag.returncode, 0, tag.stderr)

    def test_host_read_git_state_is_write_denied_and_checked_before_launch(self):
        """U85 round 6: the git state host git reads for a worktree is denied to every seat, and a launch over state a
        seat may have written (a `config.worktree` key host git acts on, a moved `commondir`) is refused."""
        run = self.seat("worker", "--seats-root", self.seats)
        self.assertEqual(run.returncode, 0, run.stderr)
        common = (self.repo / ".git").resolve()
        wt = common / "worktrees/worker"
        deny = self.settings_of("worker")["filesystem"]["denyWrite"]
        for path in (common / "config", common / "config.worktree", common / "info", common / "hooks",
                     wt / "config.worktree", wt / "info", wt / "commondir", wt / "gitdir",
                     Path(self.seats, "worker/.git").resolve()):  # fmt: skip
            self.assertIn(str(path), deny)
            self.assertTrue(path.exists(), path)
        allow_read = self.settings_of("worker")["filesystem"]["allowRead"]
        self.assertIn(str(self.repo.resolve() / ".orchestration/orchestrate"), allow_read)
        self.assertNotIn(str(self.repo.resolve()), allow_read, "a worker reads the records, not the whole checkout")
        for target, text in ((wt / "config.worktree", "[core]\n\tfsmonitor = /tmp/u85-evil\n"),
                             (common / "config.worktree", '[includeIf "gitdir:/"]\n\tpath = /tmp/x\n'),
                             (wt / "config.worktree", "[core]\n\thooksPath = /tmp/h\n"),
                             (wt / "config.worktree", '[filter "x"]\n\tsmudge = /tmp/f\n')):  # fmt: skip
            with self.subTest(target=target.name, text=text.splitlines()[1]):
                target.write_text(text)
                run = self.seat("worker", "--seats-root", self.seats)
                self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
                self.assertIn(f"the git config {target} sets", run.stderr)
                target.write_text("")
        (wt / "config.worktree").write_text("[core]\n\tsparseCheckout = true\n")
        run = self.seat("worker", "--seats-root", self.seats)
        self.assertEqual(run.returncode, 0, run.stderr)
        # Another worktree's commondir, moved by a seat that could write it before this round, refuses every launch.
        run = self.seat("worker", "--seats-root", self.seats, "--name", "worker-2")
        self.assertEqual(run.returncode, 0, run.stderr)
        (common / "worktrees/worker-2/commondir").write_text("/tmp\n")
        run = self.seat("worker", "--seats-root", self.seats)
        self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
        self.assertIn("commondir leads to /tmp", run.stderr)

    def test_a_multiline_commondir_refuses_every_launch(self):
        """U85 round 18: git consumes a pointer file whole (less trailing newlines), so a `commondir` of
        `../..\\n/../../attacker\\n` is no `../..`: it is refused for a worktree next to the launch and for the
        worktree the launch runs in, before git runs."""
        linked = Path(self.temp.name).resolve() / "linked"
        self.git("worktree", "add", "-q", "--detach", str(linked), "HEAD")
        commondir = self.repo / ".git/worktrees/linked/commondir"
        commondir.write_text("../..\n/../../attacker\n")
        for cwd in (self.repo, linked):
            with self.subTest(cwd=cwd.name):
                run = self.seat("worker", "--seats-root", self.seats, cwd=cwd)
                self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
                self.assertIn(f"{commondir.resolve()} as one line free of control characters", run.stderr)
                self.assertFalse(Path(self.seats).exists())
        commondir.write_text("../..\n")
        run = self.seat("worker", "--seats-root", self.seats, cwd=linked)
        self.assertEqual(run.returncode, 0, run.stderr)

    def test_pointer_value_reads_the_whole_file(self):
        """U85 round 18: pointer_value gives a value only for a single line free of control characters; round 19: a
        NUL byte, which bash drops from a command substitution, refuses too."""
        text = SEAT.read_text()
        function = text[text.index("pointer_value() {") : text.index("\n}\n", text.index("pointer_value() {")) + 3]
        scratch = Path(self.temp.name)
        cases = {
            "../..\n": (0, "../..\n"),
            "gitdir: /a/b": (0, "gitdir: /a/b\n"),
            "../..\n/../../attacker\n": (1, ""),
            "/r/.git/objects\0/..\n": (1, ""),
            "../\0..\n": (1, ""),
            "../..\r\n": (1, ""),
            "../..\n\n": (1, ""),
            "": (1, ""),
            "\n": (1, ""),
        }
        for content, expected in cases.items():
            with self.subTest(content=content):
                (scratch / "pointer").write_text(content)
                run = subprocess.run(
                    ["/bin/bash", "-c", f'set -euo pipefail\n{function}\npointer_value "$1"', "_", str(scratch / "pointer")],
                    capture_output=True, text=True, check=False,
                )  # fmt: skip
                self.assertEqual((run.returncode, run.stdout), expected, run.stderr)
        run = subprocess.run(
            ["/bin/bash", "-c", f'{function}\npointer_value "$1"', "_", str(scratch / "absent")],
            capture_output=True, text=True, check=False,
        )  # fmt: skip
        self.assertEqual((run.returncode, run.stdout), (1, ""))

    def test_a_relative_interpreter_is_refused_promptly(self):
        """U85 round 19: an interpreter line naming a relative path (`#!sh`, `#!bin/sh`) is refused (exit 2) before
        any ancestor walk, which never reached `/` from a relative path; every walk goes through ancestors_of."""
        text = SEAT.read_text()
        names = ("refuse", "ancestors_of", "physical_path", "physical_file", "refuse_if_seat_writable", "root_named")
        names += ("refuse_if_link_chain_writable", "find_on_path", "pin_exec")
        functions = "\n".join(
            text[text.index(f"{name}() {{") : text.index("\n}\n", text.index(f"{name}() {{")) + 3] for name in names
        )
        stat_args = "(-L -f '%d:%i')" if sys.platform == "darwin" else "(-L -c '%d:%i')"
        scratch = Path(self.temp.name).resolve()
        for line in ("#!sh", "#!bin/sh", "#!./sh"):
            with self.subTest(line=line):
                tool = scratch / "tool"
                tool.write_text(f"{line}\nexit 0\n")
                tool.chmod(0o755)
                script = (
                    f"set -euo pipefail\nstat_args={stat_args}\nroot_ids=$'\\n' root_id_list=() root_path_list=()\n"
                    f'{functions}\npin_exec tool "$1"\n'
                )
                run = subprocess.run(
                    ["/bin/bash", "-c", script, "_", str(tool)], capture_output=True, text=True, check=False, timeout=20
                )
                self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
                self.assertIn("names no absolute path", run.stderr)
        for path in ("sh", "bin/sh"):
            with self.subTest(walk=path):
                script = f"set -euo pipefail\n{functions}\nancestors_of {path}\n"
                run = subprocess.run(
                    ["/bin/bash", "-c", script], capture_output=True, text=True, check=False, timeout=20
                )
                self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
        # A launch whose git is such a script is refused, not hung.
        outside = scratch / "git-bin"
        outside.mkdir()
        (outside / "git").write_text("#!sh\nexit 0\n")
        (outside / "git").chmod(0o755)
        run = subprocess.run(
            [str(SEAT), "worker", "--seats-root", self.seats], cwd=self.repo, capture_output=True, text=True,
            env={**self.env, "PATH": f"{outside}:{self.env['PATH']}"}, check=False, timeout=120,
        )  # fmt: skip
        self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
        self.assertIn("names no absolute path", run.stderr)

    def test_inherited_git_environment_has_no_effect(self):
        """U85 round 20: hcom-seat removes every inherited `GIT_*` variable before its first git command, so a
        GIT_DIR, GIT_COMMON_DIR or GIT_WORK_TREE naming another repository steers neither host git nor the seat."""
        other = Path(self.temp.name).resolve() / "other"
        git_init(other)
        steer = {"GIT_DIR": str(other / ".git"), "GIT_COMMON_DIR": str(other / ".git"), "GIT_WORK_TREE": str(other)}
        for name, value in steer.items():
            with self.subTest(variable=name):
                run = self.seat("worker", "--seats-root", self.seats, "--name", f"w-{name.lower()}", **{name: value})
                self.assertEqual(run.returncode, 0, run.stderr)
                pointer = Path(self.seats, f"w-{name.lower()}", ".git").read_text()
                self.assertIn(str((self.repo / ".git/worktrees").resolve()), pointer)
                self.assertFalse((other / ".git/worktrees").exists())
        run = self.seat("worker", "--seats-root", self.seats, **steer)
        self.assertEqual(run.returncode, 0, run.stderr)
        for tool in ("hcom", "omp"):
            for call in self.calls_of(tool):
                self.assertEqual([k for k in call["git_env"] if k in steer or k == "GIT_CONFIG_GLOBAL"], [], tool)

    def test_the_main_checkout_is_found_by_identity(self):
        """U85 round 20: the main checkout is the common directory's parent when that parent's `.git` is the common
        directory by identity, never by its spelling: a `commondir` spelled `.GIT` (one directory on a
        case-insensitive volume) still protects the main checkout, not the linked worktree the launch runs in."""
        if not (self.repo / ".GIT").exists():
            self.skipTest("needs a case-insensitive file system")
        linked = Path(self.temp.name).resolve() / "linked"
        self.git("worktree", "add", "-q", "--detach", str(linked), "HEAD")
        (self.repo / ".git/worktrees/linked/commondir").write_text("../../../.GIT\n")
        common = subprocess.run(
            ["git", "-C", str(linked), "rev-parse", "--path-format=absolute", "--git-common-dir"],
            env=self.env, capture_output=True, text=True, check=True,
        ).stdout.strip()  # fmt: skip
        self.assertEqual(Path(common).name, ".GIT", "git keeps the spelling")
        run = self.seat("worker", "--seats-root", self.seats, cwd=linked)
        self.assertEqual(run.returncode, 0, run.stderr)
        deny_read = self.settings_of("worker")["filesystem"]["denyRead"]
        self.assertIn(str(self.repo.resolve()), deny_read)
        self.assertNotIn(str(linked), deny_read)
        # The main checkout stays protected: a seats root inside it is refused from the linked worktree too.
        inside = self.repo / "seats-inside"
        run = self.seat("worker", "--seats-root", str(inside), "--name", "w2", cwd=linked)
        self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
        self.assertIn("the main checkout", run.stderr)

    def test_an_interpreter_in_a_seat_write_root_never_runs(self):
        """U85 round 6: the interpreter of mise or of a resolved tool is held to the identity check before either runs."""
        interp = self.store / "u85interp"
        marker = self.plant(self.store, "u85interp")
        self.addCleanup(interp.unlink)
        outside = Path(self.temp.name).resolve() / "chain-bin"
        for tool in ("mise", "git"):
            with self.subTest(tool=tool):
                outside.mkdir(exist_ok=True)
                for old in outside.iterdir():
                    old.unlink()
                (outside / tool).write_text(f"#!{interp}\n")
                (outside / tool).chmod(0o755)
                run = self.seat("worker", "--seats-root", self.seats, PATH=f"{outside}:{self.env['PATH']}")
                self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
                self.assertRegex(run.stderr, rf"{tool} \S*/u85interp is or lies under the seat write root")
                self.assertFalse(marker.exists(), marker.read_text() if marker.exists() else "")
        self.assertFalse(Path(self.seats).exists())

    def test_no_host_git_command_runs_a_hook_or_a_worktree_config(self):
        """U85 round 7: hcom-seat's own git runs no hook and reads no `config.worktree`, and the git state is checked
        before its first git command, so neither a planted `post-checkout` nor a poisoned main `config.worktree`
        runs anything on the host."""
        marker = Path(self.temp.name) / "hook-ran"
        hooks = self.repo / ".git/hooks"
        hooks.mkdir(exist_ok=True)
        (hooks / "post-checkout").write_text(f"#!/bin/sh\necho post-checkout >> {shlex.quote(str(marker))}\n")
        (hooks / "post-checkout").chmod(0o755)
        run = self.seat("worker", "--seats-root", self.seats)
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertTrue(Path(self.seats, "worker/.git").is_file(), "the worktree was added")
        self.assertFalse(marker.exists(), "the post-checkout hook ran on the host")
        self.git("config", "extensions.worktreeConfig", "true")
        evil = Path(self.temp.name) / "evil-hooks"
        evil.mkdir()
        (evil / "post-checkout").write_text((hooks / "post-checkout").read_text())
        (evil / "post-checkout").chmod(0o755)
        (self.repo / ".git/config.worktree").write_text(f"[core]\n\thooksPath = {evil}\n")
        run = self.seat("worker", "--seats-root", self.seats, "--name", "worker-2")
        self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
        self.assertIn(
            f"the git config {(self.repo / '.git/config.worktree').resolve()} sets core.hookspath", run.stderr
        )
        self.assertFalse(Path(self.seats, "worker-2").exists(), "no git command ran before the check")
        self.assertFalse(marker.exists(), "a hook ran on the host")

    def test_no_seat_reads_another_programs_seats_root(self):
        """U85 round 7: the whole ~/.local/state/omp-seats tree and every configured seats root are read-denied but the
        seat's own paths; the orchestrator keeps its own program's worker clones, never a `.sandbox`."""
        run = self.seat("worker", "--seats-root", self.seats)
        self.assertEqual(run.returncode, 0, run.stderr)
        worker = self.settings_of("worker")["filesystem"]
        omp_seats = str(self.home.resolve() / ".local/state/omp-seats")
        self.assertIn(omp_seats, worker["denyRead"])
        self.assertIn(str(Path(self.seats).resolve()), worker["denyRead"])
        self.assertIn(str(Path(self.seats, "worker").resolve()), worker["allowRead"])
        self.assertIn(str(Path(self.seats, ".state/worker").resolve()), worker["allowRead"])
        self.assertNotIn(str(Path(self.seats).resolve()), worker["allowRead"])
        self.assertFalse(any(Path(omp_seats) in (Path(p), *Path(p).parents) for p in worker["allowRead"]))
        run = self.seat("orchestrator", "--seats-root", self.seats)
        self.assertEqual(run.returncode, 0, run.stderr)
        orchestrator = self.settings_of("orchestrator")["filesystem"]
        self.assertIn(omp_seats, orchestrator["denyRead"])
        self.assertIn(str(Path(self.seats).resolve()), orchestrator["allowRead"])
        self.assertIn(str(Path(self.seats, ".sandbox").resolve()), orchestrator["denyRead"])

    def test_overlapping_seat_roots_are_refused(self):
        """U85 round 8: a seats root inside the checkout (or the hcom store inside one) would nest one seat's write
        roots inside another's, so the launch is refused before anything is created."""
        inside = self.repo / "seats"
        run = self.seat("worker", "--seats-root", str(inside))
        self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
        self.assertIn(
            f"write root {inside.resolve()}/worker lies inside the main checkout {self.repo.resolve()}", run.stderr
        )
        self.assertFalse(inside.exists())
        # Neither exists yet: the absent components decide (U85 round 30), so the nested store is refused as well.
        run = self.seat("worker", "--seats-root", self.seats, HCOM_DIR=str(Path(self.seats, "hcom")))
        self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
        self.assertIn(f"write root {self.seats}/hcom lies inside the seats root {self.seats}", run.stderr)
        self.assertFalse(Path(self.seats).exists())
        Path(self.seats, "hcom").mkdir(parents=True)
        run = self.seat("worker", "--seats-root", self.seats, HCOM_DIR=str(Path(self.seats, "hcom")))
        self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
        self.assertIn("seat write roots must not overlap", run.stderr)
        self.assertEqual(self.calls_of("hcom"), [])

    def test_both_roles_launch_from_a_linked_worktree_and_the_main_checkout_stays_protected(self):
        """U85 round 13: the orchestrator's own directory is the launch checkout, so both roles launch from a linked
        worktree (and from the main checkout), while a worker grant inside the main checkout is still refused."""
        linked = Path(self.temp.name).resolve() / "linked"
        self.git("worktree", "add", "-q", "--detach", str(linked), "HEAD")
        for role in ("orchestrator", "worker"):
            with self.subTest(role=role, cwd="linked worktree"):
                run = self.seat(role, "--seats-root", self.seats, cwd=linked)
                self.assertEqual(run.returncode, 0, run.stderr)
            with self.subTest(role=role, cwd="main checkout"):
                run = self.seat(role, "--seats-root", self.seats, "--name", f"{role}-main")
                self.assertEqual(run.returncode, 0, run.stderr)
        self.assertIn(str(linked), self.settings_of("orchestrator")["filesystem"]["allowWrite"])
        run = self.seat(
            "worker", "--seats-root", self.seats, "--name", "worker-3", cwd=linked, HCOM_DIR=str(self.repo / "hcom")
        )
        self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
        self.assertIn(f"lies inside the main checkout {self.repo.resolve()}", run.stderr)

    def test_overlap_is_decided_by_identity_never_by_path_text(self):
        """U85 round 14: containment is by (device, inode) only. A seats root spelled through a case alias of a write
        root (`~/.CLAUDE/seats` for `~/.claude`) is refused when the alias exists, and, when neither exists yet, by the
        case-folded absent components (U85 round 30); a nonexistent child of an existing alias is caught too."""
        claude = self.home / ".claude"
        alias = self.home / ".CLAUDE"
        run = self.seat("worker", "--seats-root", str(alias / "seats"), "--dry-run")
        self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
        self.assertIn(f"write root {self.home / '.claude'} contains the seats root {alias / 'seats'}", run.stderr)
        claude.mkdir(exist_ok=True)
        if not alias.exists():
            self.skipTest("the file system is case-sensitive, so no case alias exists")
        for seats in (alias / "seats", alias / "new" / "deeper" / "seats"):
            with self.subTest(seats=seats.relative_to(self.home)):
                run = self.seat("worker", "--seats-root", str(seats))
                self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
                self.assertIn(f"contains the seats root {alias}", run.stderr)
                self.assertFalse(seats.exists())
        self.assertEqual(self.calls_of("hcom"), [])

    def test_relative_path_worktrees_launch_for_both_roles(self):
        """U85 round 15: `git worktree add --relative-paths` stores relative `gitdir` and `.git` values; they are
        resolved against their own directories, so both roles launch from such a worktree and next to one."""
        usage = subprocess.run(
            ["git", "worktree", "add", "-h"], cwd=self.repo, env=self.env, capture_output=True, text=True, check=False
        )
        if "relative-paths" not in usage.stdout + usage.stderr:  # listed as `--[no-]relative-paths`
            self.skipTest("this git has no `worktree add --relative-paths` (git 2.48 and later)")
        linked = Path(self.temp.name).resolve() / "relative"
        self.git("worktree", "add", "-q", "--relative-paths", "--detach", str(linked), "HEAD")
        gitdir = (self.repo / ".git/worktrees/relative/gitdir").read_text().strip()
        self.assertFalse(Path(gitdir).is_absolute(), gitdir)
        for role in ("orchestrator", "worker"):
            with self.subTest(role=role, cwd="relative worktree"):
                run = self.seat(role, "--seats-root", self.seats, cwd=linked)
                self.assertEqual(run.returncode, 0, run.stderr)
            with self.subTest(role=role, cwd="main checkout"):
                run = self.seat(role, "--seats-root", self.seats, "--name", f"{role}-main")
                self.assertEqual(run.returncode, 0, run.stderr)

    def test_a_failing_helper_in_the_identity_check_refuses_the_launch(self):
        """U85 round 15: `within` runs inside `||` lists, where `set -e` does not apply, so each helper's status is
        checked explicitly: a helper that prints a path and fails refuses instead of deciding."""
        text = SEAT.read_text()
        functions = "\n".join(
            text[text.index(f"{name}() {{") : text.index("\n}\n", text.index(f"{name}() {{")) + 3]
            for name in ("refuse", "deepest_existing", "within")
        )
        stat_args = "(-L -f '%d:%i')" if sys.platform == "darwin" else "(-L -c '%d:%i')"
        outer = Path(self.temp.name).resolve() / "outer"
        outer.mkdir()
        cases = {
            "exists": f"within {shlex.quote(str(outer))} {shlex.quote(str(outer / 'a/b'))} || status=$?",
            "neither exists": f"within {shlex.quote(str(outer / 'x'))} {shlex.quote(str(outer / 'x/y'))} || status=$?",
        }
        for label, call in cases.items():
            with self.subTest(label):
                script = (
                    f"set -euo pipefail\nstat_args={stat_args}\n{functions}\n"
                    "deepest_existing() { printf '/\\n'; return 7; }\n"
                    f"status=0\n{call}\necho decided=$status\n"
                )
                run = subprocess.run(["/bin/bash", "-c", script], capture_output=True, text=True, check=False)
                self.assertEqual((run.returncode, run.stdout), (2, ""), run.stdout + run.stderr)
                self.assertIn("cannot find an existing directory above", run.stderr)

    def test_own_slots_that_are_links_are_refused(self):
        """U85 round 16: the overlap check exempts a seat's own slots by position, so they are first proved to be
        what they claim. A `.state/<name> -> ..` (the whole seats root) or a `<seats-root>/<name> -> /` is refused
        before anything is created; a real, pre-existing slot still launches."""
        seats = Path(self.seats)
        cases = (
            ("worker", ".state/worker", ".."),
            ("orchestrator", ".state/orchestrator", ".."),
            ("worker", "worker", "/"),
            ("worker", ".state", "/tmp"),
        )
        for role, slot, target in cases:
            with self.subTest(role=role, slot=slot, target=target):
                (seats / slot).parent.mkdir(parents=True, exist_ok=True)
                (seats / slot).symlink_to(target)
                run = self.seat(role, "--seats-root", self.seats)
                self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
                self.assertIn(f"the seat slot {seats / slot} is a symbolic link", run.stderr)
                self.assertFalse((seats / ".sandbox").exists())
                shutil.rmtree(seats)
        (seats / ".state/worker").mkdir(parents=True)
        run = self.seat("worker", "--seats-root", self.seats)
        self.assertEqual(run.returncode, 0, run.stderr)

    def test_srt_write_roots_resolve_cleanly_on_each_os(self):
        """U85 round 27: srt's own TMPDIR roots are chosen per OS (`/private/tmp/claude` on macOS, and on Linux only
        if it exists), and physical_path never prints `//`: a path whose first component does not exist (Linux's
        `/private`) walks up to `/`, whose `cd //` form pwd prints as `//`, and must still come out clean."""
        text = SEAT.read_text()
        functions = "\n".join(
            text[text.index(f"{name}() {{") : text.index("\n}\n", text.index(f"{name}() {{")) + 3]
            for name in ("clean_path", "physical_path", "srt_tmp_roots_for")
        )

        def bash(script, *args):
            return subprocess.run(
                ["/bin/bash", "-c", f"set -euo pipefail\n{functions}\n{script}", "_", *args],
                capture_output=True,
                text=True,
                check=False,
                timeout=20,
            )

        for path in ("/", "/u85-absent", "/u85-absent/tmp/claude", "/u85-absent/a/b/c"):
            with self.subTest(path=path):
                run = bash('physical_path "$1"', path)
                self.assertEqual((run.returncode, run.stdout), (0, f"{path}\n"), run.stderr)
        listing = 'srt_tmp_roots_for "$1"\nfor r in "${srt_tmp_roots[@]}"; do p=$(physical_path "$r"); clean_path "$p"; echo "$r"; done'
        private = ["/private/tmp/claude"] if Path("/private/tmp/claude").exists() else []
        for system, expected in (
            ("Darwin", ["/tmp/claude", "/private/tmp/claude"]),
            ("Linux", ["/tmp/claude", *private]),
        ):
            with self.subTest(os=system):
                run = bash(listing, system)
                self.assertEqual((run.returncode, run.stdout.splitlines()), (0, expected), run.stderr)

    def test_a_fresh_hcom_store_is_created_before_anything_else(self):
        """U85 round 29: an explicit HCOM_DIR that does not exist yet is made (0700, one component at a time) before
        the worktree or any metadata, so a first launch works for both roles; a dry run leaves it absent and says so;
        a store whose deepest existing ancestor is a symbolic link is refused before anything is created."""
        root = Path(self.temp.name).resolve()
        # The seats root is absent too (U85 round 30): both new under one existing directory, decided by their
        # absent components.
        self.assertFalse(Path(self.seats).exists())
        for role in ("worker", "orchestrator"):
            with self.subTest(role=role):
                store = root / f"fresh-{role}" / "hcom"
                run = self.seat(role, "--seats-root", self.seats, "--dry-run", HCOM_DIR=str(store))
                self.assertEqual(run.returncode, 0, run.stderr)
                self.assertIn(f"the hcom store {store} does not exist; a launch creates it", run.stderr)
                self.assertFalse(store.parent.exists())
                run = self.seat(role, "--seats-root", self.seats, HCOM_DIR=str(store))
                self.assertEqual(run.returncode, 0, run.stderr)
                self.assertTrue(store.is_dir() and not store.is_symlink())
                for made in (store, store.parent):
                    self.assertEqual(made.stat().st_mode & 0o777, 0o700, made)
        target = root / "elsewhere"
        target.mkdir()
        (root / "linked").symlink_to(target)
        store = root / "linked" / "new" / "hcom"
        run = self.seat("worker", "--seats-root", self.seats, "--name", "w-link", HCOM_DIR=str(store))
        self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
        self.assertIn(f"would be made under {root / 'linked'}, which is not a real directory", run.stderr)
        self.assertEqual(list(target.iterdir()), [])
        self.assertFalse(Path(self.seats, "w-link").exists())
        self.assertNotIn("w-link", self.git("worktree", "list"))

    def test_absent_paths_under_one_ancestor_are_decided_by_their_components(self):
        """U85 round 30: below the deepest existing ancestor nothing exists, so `within` decides two absent paths by
        that ancestor's identity and their clean components: nested refuses, disjoint passes, `a/b` is no prefix of
        `a/bc`, and an existing outer path is still decided by identity."""
        text = SEAT.read_text()
        functions = "\n".join(
            text[text.index(f"{name}() {{") : text.index("\n}\n", text.index(f"{name}() {{")) + 3]
            for name in ("refuse", "ancestors_of", "deepest_existing", "within")
        )
        stat_args = "(-L -f '%d:%i')" if sys.platform == "darwin" else "(-L -c '%d:%i')"
        root = Path(self.temp.name).resolve() / "anc"
        (root / "exists").mkdir(parents=True)
        (root / "other").mkdir()
        cases = (
            ("new/a", "new/a/b", 0),
            ("new/a", "new/a", 0),
            ("new/a/b", "new/a", 1),
            ("new/a/b", "new/a/bc", 1),
            ("new/a", "new/ab/c", 1),
            ("new/x", "new/y", 1),
            ("new/A", "new/a/b", 0),
            ("exists/new", "other/new", 1),
            ("exists", "exists/new/deeper", 0),
            ("exists", "other/new", 1),
            ("new", "exists", 1),
        )
        for outer, inner, expected in cases:
            with self.subTest(outer=outer, inner=inner):
                script = f'set -euo pipefail\nstat_args={stat_args}\n{functions}\nstatus=0\nwithin "$1" "$2" || status=$?\necho $status\n'
                run = subprocess.run(
                    ["/bin/bash", "-c", script, "_", str(root / outer), str(root / inner)],
                    capture_output=True, text=True, check=False, timeout=20,
                )  # fmt: skip
                self.assertEqual((run.returncode, run.stdout), (0, f"{expected}\n"), run.stderr)

    def test_a_fresh_spark_first_launch_with_the_default_paths(self):
        """U85 round 30: the dotfiles program's first launch on a fresh host (hcom-orchestration SKILL step 0):
        HCOM_DIR=~/.local/state/hcom-regime, HCOM_TEAM=regime, no --seats-root (the derived
        ~/.local/state/omp-seats/<slug>), neither existing, both under ~/.local/state. It launches both roles and makes
        both directories."""
        state = self.home / ".local/state"
        store, seats = state / "hcom-regime", state / "omp-seats/repo"
        self.assertFalse(store.exists() or seats.exists())
        for role in ("worker", "orchestrator"):
            with self.subTest(role=role):
                run = self.seat(role, HCOM_DIR=str(store), HCOM_TEAM="regime", REGIME_SEATS_ROOT=None)
                self.assertEqual(run.returncode, 0, run.stderr)
        self.assertTrue(store.is_dir() and (seats / "worker").is_dir())
        self.assertEqual(len(self.calls_of("hcom")), 2)

    def test_a_self_referencing_link_chain_refuses_promptly(self):
        """U85 round 23: physical_path is iterative with one 40-hop budget per call, so a dangling link naming a
        path under itself (`.state/<name> -> <name>/child`) fails instead of recursing without bound, and a launch
        over such a slot is refused (own_slots_check runs before anything resolves a slot)."""
        text = SEAT.read_text()
        function = text[text.index("physical_path() {") : text.index("\n}\n", text.index("physical_path() {")) + 3]
        scratch = Path(self.temp.name).resolve() / "chain"
        scratch.mkdir()
        (scratch / "w").symlink_to("w/child")
        (scratch / "a").symlink_to("b/x")
        (scratch / "b").symlink_to("a/y")
        for link in ("w", "a", "w/deeper/path"):
            with self.subTest(link=link):
                run = subprocess.run(
                    ["/bin/bash", "-c", f'{function}\nphysical_path "$1"', "_", str(scratch / link)],
                    capture_output=True, text=True, check=False, timeout=20,
                )  # fmt: skip
                self.assertEqual((run.returncode, run.stdout), (1, ""), run.stderr)
        (scratch / "ok").symlink_to("real/sub")
        run = subprocess.run(
            ["/bin/bash", "-c", f'{function}\nphysical_path "$1"', "_", str(scratch / "ok/tail")],
            capture_output=True, text=True, check=False, timeout=20,
        )  # fmt: skip
        self.assertEqual((run.returncode, run.stdout), (0, f"{scratch}/real/sub/tail\n"), run.stderr)
        seats = Path(self.seats)
        for slot in (".state/worker", "worker"):
            with self.subTest(slot=slot):
                (seats / slot).parent.mkdir(parents=True, exist_ok=True)
                (seats / slot).symlink_to("worker/child")
                run = subprocess.run(
                    [str(SEAT), "worker", "--seats-root", self.seats], cwd=self.repo, env=self.env,
                    capture_output=True, text=True, check=False, timeout=120,
                )  # fmt: skip
                self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
                self.assertIn(f"the seat slot {seats / slot} is a symbolic link", run.stderr)
                shutil.rmtree(seats)

    def test_an_optional_tool_interpreter_outside_the_system_directories_is_refused(self):
        """U85 round 24: an optional tool's `#!` interpreter must be spelled in /bin, /usr/bin, /sbin, /usr/sbin or
        ~/.local/share/mise/installs once its directory is followed physically, so a directory alias into a seat
        write root (`alias -> $HCOM_DIR/subdir`, `subdir/interp -> /bin/bash`, which the hop check passes) is
        refused; the same tool with `#!/bin/sh` launches. A best-effort reduction of the accepted G17 residual."""
        subdir = self.store / "u85-alias-target"
        subdir.mkdir()
        self.addCleanup(shutil.rmtree, subdir, True)
        (subdir / "interp").symlink_to("/bin/bash")
        outside = Path(self.temp.name).resolve() / "alias-bin"
        outside.mkdir()
        (outside / "alias").symlink_to(subdir)
        tool = outside / "regime-open-url"
        tool.write_text(f"#!{outside / 'alias/interp'}\nexit 0\n")
        tool.chmod(0o755)
        run = self.seat("worker", "--seats-root", self.seats, PATH=f"{outside}:{self.env['PATH']}")
        self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
        self.assertIn(f"regime-open-url: its interpreter {outside / 'alias/interp'} lies outside /bin", run.stderr)
        self.assertEqual(self.calls_of("hcom"), [])
        tool.write_text("#!/bin/sh\nexit 0\n")
        run = self.seat("worker", "--seats-root", self.seats, PATH=f"{outside}:{self.env['PATH']}")
        self.assertEqual(run.returncode, 0, run.stderr)

    def test_the_linux_reader_checks_jq_status_for_an_empty_list(self):
        """U85 round 16: jq's status for the entry read is checked unconditionally, so a jq that exits 7 or 127
        while the list is empty fails the read instead of reading as an empty list."""
        text = SEAT.read_text()
        functions = "\n".join(
            text[text.index(f"{name}() {{") : text.index("\n}\n", text.index(f"{name}() {{")) + 3]
            for name in ("clean_path", "allow_write_list")
        )
        fake = Path(self.temp.name) / "fake-jq"
        fake.write_text(
            '#!/bin/sh\ncase "$*" in\n*\'allowWrite[]\'*) exit "${JQ_ENTRY_STATUS:-0}" ;;\n*length*) echo 0 ;;\nesac\n'
        )
        fake.chmod(0o755)
        functions = functions.replace("/usr/bin/jq", str(fake))
        fixture = Path(self.temp.name) / "settings.json"
        fixture.write_text(json.dumps({"filesystem": {"allowWrite": []}}))
        for status in (0, 7, 127):
            with self.subTest(status=status):
                run = subprocess.run(
                    ["/bin/bash", "-c", f'{functions}\nallow_write_list Linux "$1"', "_", str(fixture)],
                    env={**os.environ, "JQ_ENTRY_STATUS": str(status)}, capture_output=True, text=True, check=False,
                )  # fmt: skip
                self.assertEqual((run.returncode, run.stdout), (0 if status == 0 else 1, ""), run.stderr)

    def test_a_failing_header_read_refuses_instead_of_skipping_the_interpreter(self):
        """U85 round 17: pin_exec reads a file's first bytes and its interpreter line with checked producers (head,
        under pipefail); a producer that prints a plausible answer and fails refuses, never reads as a file without `#!`. The
        git pointer files are read whole (pointer_value, tested on its own)."""
        text = SEAT.read_text()
        functions = "\n".join(
            text[text.index(f"{name}() {{") : text.index("\n}\n", text.index(f"{name}() {{")) + 3]
            for name in ("refuse", "pin_exec")
        )
        scratch = Path(self.temp.name).resolve()
        counter = scratch / "head-calls"
        fake_head = scratch / "fake-head"
        fake_head.write_text(
            "#!/bin/sh\n"
            f"n=$(cat {shlex.quote(str(counter))}); echo $((n + 1)) > {shlex.quote(str(counter))}\n"
            'if [ "$n" = "${HEAD_FAIL_AT:--1}" ]; then printf \'#!/bin/sh\\n\'; exit 7; fi\n'
            'exec /usr/bin/head "$@"\n'
        )
        fake_head.chmod(0o755)
        functions = functions.replace("/usr/bin/head", str(fake_head))
        stubs = (
            "refuse_if_link_chain_writable() { :; }\nrefuse_if_seat_writable() { :; }\n"
            "physical_file() { printf '%s\\n' \"$1\"; }\nfind_on_path() { return 1; }\n"
        )
        target = scratch / "tool"
        target.write_text("#!/bin/sh\nexit 0\n")
        cases = (
            ("passes", {}, 'pin_exec tool "$1"; printf \'%s \' "${pinned[@]}"', 0, "/bin/sh " + str(target) + " "),
            ("file bytes", {"HEAD_FAIL_AT": "0"}, 'pin_exec tool "$1"', 2, "cannot read tool"),
            ("interpreter line", {"HEAD_FAIL_AT": "1"}, 'pin_exec tool "$1"', 2, "cannot read the interpreter line"),
            (
                "interpreter bytes",
                {"HEAD_FAIL_AT": "2"},
                'pin_exec tool "$1"',
                2,
                "cannot read the interpreter of tool",
            ),
        )
        for label, env, call, status, expected in cases:
            with self.subTest(label):
                counter.write_text("0\n")
                script = f"set -euo pipefail\n{functions}\n{stubs}\n{call}\n"
                run = subprocess.run(
                    ["/bin/bash", "-c", script, "_", str(target)], env={**os.environ, **env},
                    capture_output=True, text=True, check=False,
                )  # fmt: skip
                self.assertEqual(run.returncode, status, run.stdout + run.stderr)
                self.assertIn(expected, run.stdout if status == 0 else run.stderr)
        with self.subTest("a real read error"):
            script = f'set -euo pipefail\n{functions}\n{stubs}\npin_exec tool "$1"\n'
            run = subprocess.run(
                ["/bin/bash", "-c", script, "_", str(scratch)], capture_output=True, text=True, check=False
            )
            self.assertEqual(run.returncode, 2, run.stdout + run.stderr)
            self.assertIn(f"cannot read tool: {scratch}", run.stderr)

    def test_no_file_read_or_command_status_is_masked(self):
        """U85 round 17: hcom-seat passes ShellCheck with check-extra-masked-returns (SC2312) and
        require-variable-braces, and reads no file with `read < file`, whose failure a `||` fallback can mask (file
        reads go through a checked producer such as pointer_value). Both are checked here so the class cannot return."""
        for path in (SEAT, ROOT / "home/dot_local/bin/common/executable_hcom-seat"):
            with self.subTest(path=path.name):
                masked = [
                    f"{number}: {line.strip()}"
                    for number, line in enumerate(path.read_text().splitlines(), 1)
                    if not line.lstrip().startswith("#") and re.search(r"\bread\b[^<#]*<\s*[^<(\s]", line)
                ]
                self.assertEqual(masked, [])
                shellcheck = shutil.which("shellcheck")
                if shellcheck is None:
                    self.skipTest("shellcheck is not installed here")
                run = subprocess.run(
                    [shellcheck, "-x", "-o", "check-extra-masked-returns,require-variable-braces", str(path)],
                    cwd=ROOT, capture_output=True, text=True, check=False,
                )  # fmt: skip
                self.assertEqual(run.returncode, 0, run.stdout + run.stderr)

    def test_a_separate_git_dir_holding_the_seats_root_is_refused(self):
        """U85 round 12: one invariant over the final allowWrite list: a git common directory outside the checkout
        (`--separate-git-dir`) that holds the seats root would grant every worker its siblings, so it is refused."""
        root = Path(self.temp.name).resolve()
        gitdir, checkout = root / "g", root / "sep"
        git_init(checkout, f"--separate-git-dir={gitdir}", env=self.env)
        for args in (
            ["commit", "-q", "--allow-empty", "-m", "init"],
            ["update-ref", "refs/remotes/origin/main", "HEAD"],
        ):
            subprocess.run(["git", *args], cwd=checkout, env=self.env, check=True)
        seats = gitdir / "seats"
        run = self.seat("worker", "--seats-root", str(seats), cwd=checkout)
        self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
        self.assertIn(f"write root {gitdir} contains the seats root {seats}", run.stderr)
        self.assertFalse(seats.exists())
        run = self.seat("worker", "--seats-root", self.seats, cwd=checkout)
        self.assertEqual(run.returncode, 0, run.stderr)

    def test_a_checkout_path_srt_could_misread_creates_nothing(self):
        """U85 round 12: the checkout's physical path is checked clean before any git metadata or worktree is made,
        in a dry run as well."""
        checkout = Path(self.temp.name).resolve() / "has space" / "repo"
        checkout.mkdir(parents=True)
        # No background maintenance after the commit (git_init's repository config): its lock and pack files would
        # race the comparison below.
        git_init(checkout, env=self.env)
        subprocess.run(["git", "commit", "-q", "--allow-empty", "-m", "init"], cwd=checkout, env=self.env, check=True)
        before = sorted(str(path) for path in (checkout / ".git").rglob("*"))
        for extra in ([], ["--dry-run"]):
            with self.subTest(extra=extra):
                run = self.seat("worker", "--seats-root", self.seats, *extra, cwd=checkout)
                self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
                self.assertIn("is not a clean absolute path", run.stderr)
                self.assertEqual(sorted(str(path) for path in (checkout / ".git").rglob("*")), before)
                self.assertFalse(Path(self.seats).exists())

    def test_a_worker_reads_only_the_records_of_a_checkout_outside_workspace(self):
        """U85 round 8: the worker's read deny is the main checkout itself, wherever it lives (here outside
        ~/Workspace), re-opening its git directory and `.orchestration/orchestrate` only."""
        self.assertNotIn(self.home / "Workspace", self.repo.parents)
        run = self.seat("worker", "--seats-root", self.seats)
        self.assertEqual(run.returncode, 0, run.stderr)
        worker = self.settings_of("worker")["filesystem"]
        checkout = self.repo.resolve()
        self.assertIn(str(checkout), worker["denyRead"])
        self.assertIn(str(checkout / ".orchestration/orchestrate"), worker["allowRead"])
        self.assertIn(str(checkout / ".git"), worker["allowRead"])
        self.assertNotIn(str(checkout), worker["allowRead"])
        run = self.seat("orchestrator", "--seats-root", self.seats)
        self.assertEqual(run.returncode, 0, run.stderr)
        orchestrator = self.settings_of("orchestrator")["filesystem"]
        self.assertNotIn(str(checkout), orchestrator["denyRead"])
        self.assertIn(str(checkout), orchestrator["allowRead"])

    def test_the_login_helper_is_on_the_path_the_preflight_runs_with(self):
        """U85 round 8: seat-login-preflight hands an SSH login's URL to `regime-open-url` by name, so the private tool
        directory carries it (with its python3) and the PATH hcom-seat runs the preflight with finds it."""
        shutil.copy(ROOT / "home/dot_local/bin/common/executable_regime-open-url", self.bindir / "regime-open-url")
        (self.bindir / "regime-open-url").chmod(0o755)
        run = self.seat("worker", "--seats-root", self.seats)
        self.assertEqual(run.returncode, 0, run.stderr)
        (hcom,) = self.calls_of("hcom")
        path = hcom["path"].split(":", 1)[1]  # what the preflight ran with: the shim directory comes after it
        self.assertEqual(path, f"{self.tools}:/usr/bin:/bin:/usr/sbin:/sbin")
        found = subprocess.run(
            ["/bin/bash", "-c", "command -v regime-open-url && command -v python3"],
            env={"PATH": path}, capture_output=True, text=True, check=False,
        )  # fmt: skip
        self.assertEqual(found.returncode, 0, found.stderr)
        self.assertEqual(found.stdout.splitlines(), [str(self.tools / "regime-open-url"), str(self.tools / "python3")])
        self.assertEqual(Path(found.stdout.splitlines()[0]).resolve(), (self.bindir / "regime-open-url").resolve())

    def test_a_path_srt_could_read_as_a_pattern_or_an_unclean_path_is_refused(self):
        """U85 round 9: srt reads a settings path as a pattern, so `HCOM_DIR=<store>*` would grant its siblings; every
        input path must be clean (absolute, `[A-Za-z0-9._@+-]` components, no `.`/`..`, no trailing `/`)."""
        sibling = Path(f"{self.store}-srt")
        for label, args, overrides in (
            ("glob in HCOM_DIR", ["--seats-root", self.seats], {"HCOM_DIR": f"{self.store}*"}),
            ("bracket in HCOM_DIR", ["--seats-root", self.seats], {"HCOM_DIR": f"{self.store}[x]"}),
            ("dot-dot in the seats root", ["--seats-root", f"{self.temp.name}/new/../repo/seats"], {}),
            ("dot in the seats root", ["--seats-root", f"{self.seats}/./x"], {}),
            ("trailing slash", ["--seats-root", f"{self.seats}/"], {}),
            ("relative seats root", ["--seats-root", "seats"], {}),
            ("space in CLAUDE_CONFIG_DIR", ["--seats-root", self.seats], {"CLAUDE_CONFIG_DIR": f"{self.home}/a b"}),
        ):
            with self.subTest(label):
                run = self.seat("worker", *args, **overrides)
                self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
                self.assertIn("is not a clean absolute path", run.stderr)
        self.assertFalse(Path(self.seats).exists())
        self.assertFalse((self.repo / "seats").exists())
        self.assertFalse(sibling.exists())
        self.assertEqual(self.calls_of("hcom"), [])

    def test_the_settings_are_written_without_jq_and_read_by_plutil_and_jq_alike(self):
        """U85 round 9: hcom-seat writes the settings itself and reads them back with plutil on macOS (no system jq on
        macOS 14) and /usr/bin/jq on Linux; both readers give the same list from the same file."""
        if sys.platform == "darwin" and Path("/usr/bin/sandbox-exec").exists():
            no_jq = '(version 1)(allow default)(deny process-exec (literal "/usr/bin/jq"))'
            # The caller's PATH leaves out /usr/bin, whose jq is denied (an optional tool hcom-seat would resolve):
            # the fake bin, a planted git and /bin only.
            planted = Path(self.temp.name).resolve() / "no-jq-bin"
            planted.mkdir()
            real_git = shutil.which("git", path=SYSTEM_PATH)
            if real_git is None:
                self.skipTest("no git in /usr/bin or /bin")
            (planted / "git").symlink_to(real_git)
            env = {**self.env, "PATH": f"{planted}:{self.bindir}:/bin"}
            run = subprocess.run(
                ["/usr/bin/sandbox-exec", "-p", no_jq, str(SEAT), "worker", "--seats-root", self.seats],
                cwd=self.repo, env=env, capture_output=True, text=True, check=False,
            )  # fmt: skip
            self.assertEqual(run.returncode, 0, run.stderr)
            # A second launch reads the first one's settings back.
            run = subprocess.run(
                ["/usr/bin/sandbox-exec", "-p", no_jq, str(SEAT), "worker", "--name", "worker-2", "--seats-root",
                 self.seats], cwd=self.repo, env=env, capture_output=True, text=True, check=False,
            )  # fmt: skip
            self.assertEqual(run.returncode, 0, run.stderr)
        else:
            run = self.seat("worker", "--seats-root", self.seats)
            self.assertEqual(run.returncode, 0, run.stderr)
        fixture = Path(self.seats, ".sandbox/worker/srt-settings.json")
        expected = json.loads(fixture.read_text())["filesystem"]["allowWrite"]
        text = SEAT.read_text()
        functions = "\n".join(
            text[text.index(f"{name}() {{") : text.index("\n}\n", text.index(f"{name}() {{")) + 3]
            for name in ("clean_path", "allow_write_list")
        )
        readers = [("Linux", Path("/usr/bin/jq"))]
        if sys.platform == "darwin":
            readers.append(("Darwin", Path("/usr/bin/plutil")))
        for system, tool in readers:
            with self.subTest(reader=tool.name):
                if not tool.exists():
                    self.skipTest(f"{tool} is not installed here")
                run = subprocess.run(
                    ["/bin/bash", "-c", f'{functions}\nallow_write_list "$1" "$2"', "_", system, str(fixture)],
                    capture_output=True, text=True, check=False,
                )  # fmt: skip
                self.assertEqual(run.returncode, 0, run.stderr)
                self.assertEqual(run.stdout.splitlines(), expected)
        for label, entries in (("pattern", ["/tmp/hcom*"]), ("trailing newline", ["/tmp/root\n"])):
            fixture.write_text(json.dumps({"filesystem": {"allowWrite": entries}}))
            for system, tool in readers:
                with self.subTest(reader=tool.name, entry=label):
                    if not tool.exists():
                        self.skipTest(f"{tool} is not installed here")
                    run = subprocess.run(
                        ["/bin/bash", "-c", f'{functions}\nallow_write_list "$1" "$2"', "_", system, str(fixture)],
                        capture_output=True, text=True, check=False,
                    )  # fmt: skip
                    self.assertEqual(run.returncode, 1, run.stdout)

    def test_git_runs_by_its_checked_argv_and_no_link_hop_lies_in_a_write_root(self):
        """U85 round 10: a script-based git whose interpreter is a symlink inside a seat write root (pointing outside,
        so its physical file passes) is refused, since a seat could retarget the link before host git runs."""
        real_git = shutil.which("git", path="/usr/bin:/bin:/opt/homebrew/bin:/usr/local/bin")
        if real_git is None:
            self.skipTest("no git outside a shims directory")
        hop = self.store / "u85-sh"
        hop.symlink_to("/bin/sh")
        self.addCleanup(hop.unlink)
        outside = Path(self.temp.name).resolve() / "git-bin"
        outside.mkdir()
        (outside / "git").write_text(f'#!{hop}\nexec {shlex.quote(real_git)} "$@"\n')
        (outside / "git").chmod(0o755)
        run = self.seat("worker", "--seats-root", self.seats, PATH=f"{outside}:{self.env['PATH']}")
        self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
        self.assertIn("the interpreter of git", run.stderr)
        self.assertIn(f"is or lies under the seat write root {self.store.resolve()}", run.stderr)
        self.assertFalse(Path(self.seats).exists())
        # A git reached through an outside link runs by its physical file: the seat launch still works.
        (outside / "git").unlink()
        (outside / "git").symlink_to(real_git)
        run = self.seat("worker", "--seats-root", self.seats, PATH=f"{outside}:{self.env['PATH']}")
        self.assertEqual(run.returncode, 0, run.stderr)

    def test_the_linux_reader_refuses_non_string_and_multiline_entries(self):
        """U85 round 10: the jq reader refuses an allowWrite entry that is no string or holds a newline, rather than
        dropping or splitting it."""
        if not Path("/usr/bin/jq").exists():
            self.skipTest("/usr/bin/jq is not installed here")
        text = SEAT.read_text()
        functions = "\n".join(
            text[text.index(f"{name}() {{") : text.index("\n}\n", text.index(f"{name}() {{")) + 3]
            for name in ("clean_path", "allow_write_list")
        )
        fixture = Path(self.temp.name) / "settings.json"
        for label, entries, status in (
            ("clean", ["/tmp/a", "/tmp/b"], 0),
            ("empty", [], 0),
            ("number", ["/tmp/a", 7], 1),
            ("object", [{"path": "/tmp/a"}], 1),
            ("newline", ["/tmp/a\n/tmp/b"], 1),
        ):
            with self.subTest(label):
                fixture.write_text(json.dumps({"filesystem": {"allowWrite": entries}}))
                run = subprocess.run(
                    ["/bin/bash", "-c", f'{functions}\nallow_write_list Linux "$1"', "_", str(fixture)],
                    capture_output=True, text=True, check=False,
                )  # fmt: skip
                self.assertEqual(run.returncode, status, run.stdout + run.stderr)
                if status == 0:
                    self.assertEqual(run.stdout.splitlines(), entries)

    def test_a_dry_run_creates_no_git_metadata(self):
        """U85 round 10: a dry run validates the git state and creates nothing in the repository."""
        git_dir = self.repo / ".git"
        shutil.rmtree(git_dir / "hooks", ignore_errors=True)
        (git_dir / "config.worktree").unlink(missing_ok=True)
        before = sorted(str(path) for path in git_dir.rglob("*"))
        run = self.seat("worker", "--seats-root", self.seats, "--dry-run")
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual(sorted(str(path) for path in git_dir.rglob("*")), before)
        self.assertFalse((git_dir / "config.worktree").exists())
        self.assertFalse(Path(self.seats).exists())
        run = self.seat("worker", "--seats-root", self.seats)
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertTrue((git_dir / "config.worktree").exists(), "the real launch creates it for its deny")

    def test_the_linux_tool_stand_ins_are_binaries_as_the_check_requires(self):
        """U85 round 11: the fixture's bwrap, socat and rg are real binaries, so the Linux binary check passes on an
        Ubuntu runner for the right reason; a script in their place is refused there."""
        for tool in ("bwrap", "socat", "rg"):
            with self.subTest(tool=tool):
                self.assertFalse((self.bindir / tool).is_symlink())
                self.assertNotEqual((self.bindir / tool).read_bytes()[:2], b"#!", "hcom-seat refuses a script here")
        if not sys.platform.startswith("linux"):
            self.skipTest("the bwrap/socat/rg check runs on Linux only (the Ubuntu CI job)")
        run = self.seat("worker", "--seats-root", self.seats)
        self.assertEqual(run.returncode, 0, run.stderr)
        (self.bindir / "bwrap").unlink()
        shutil.copy(FAKE, self.bindir / "bwrap")
        run = self.seat("worker", "--seats-root", self.seats, "--name", "worker-2")
        self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
        self.assertIn("is a script; srt runs it by path, so it must be a binary", run.stderr)

    def test_a_dry_run_writes_no_sandbox(self):
        run = self.seat("worker", "--seats-root", self.seats, "--dry-run")
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertIn(f"hcom-seat: sandbox {self.seats}/.sandbox/worker", run.stderr)
        self.assertFalse(Path(self.seats).exists())


if __name__ == "__main__":
    unittest.main()
