"""Exercise scripts/orchestrator/pr-audit.sh, the Codex audit route (regime-cutover U71b, operator decision G18).

The lever runs from the checkout (its self-check reads the checkout's manifest and the generated
`home/dot_agents/codex-audit/config.toml` beside it) in a scratch repository whose `origin` is a local bare repository
holding `main` and `refs/pull/7/head`, with `tests/fixtures/pr-levers/fake-gh.py` as `gh` and
`tests/fixtures/pr-audit/fake-codex.py` as `codex` first on PATH, under a scratch HOME (agent_home_isolation). The
tests assert the exact codex argv (never `-s`), the config each call saw, the probe paths, the refusals (exit 2, no
`codex exec`) and that nothing outside the run directory under TMPDIR is written. The real `codex` and `gh` are never
called.
"""

import contextlib
import hashlib
import io
import json
import os
import shutil
import signal
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))  # dotted runs too; discover -s tests/unit already has it
from agent_home_isolation import isolate_agent_homes, restore_agent_homes, scratch_env
from test_generate_agent_configs import load_generator, sample_manifest
from test_pr_levers import JQ

ROOT = Path(__file__).resolve().parents[2]
LEVER = ROOT / "scripts/orchestrator/pr-audit.sh"
TEMPLATE = ROOT / "home/dot_agents/codex-audit/config.toml"
MANIFEST = ROOT / "home/dot_agents/agent-config.yaml"
FAKE_GH = ROOT / "tests/fixtures/pr-levers/fake-gh.py"
FAKE_CODEX = ROOT / "tests/fixtures/pr-audit/fake-codex.py"
INJECT_PYTHON = ROOT / "tests/fixtures/pr-audit/inject-python.sh"
PAUSE_AFTER_LAUNCH = ROOT / "tests/fixtures/pr-audit/pause-after-launch.bash"
RULES = "## Audit\n\nThe standing audit rules.\n"
BODY = "First paragraph.\n\nProgram-Unit: regime-cutover/U7\n\n## Contract\n\nIt guarantees one thing.\n"


def setUpModule():
    isolate_agent_homes()


def tearDownModule():
    restore_agent_homes()


def tree_state(root, skip):
    """Every file and symlink under ROOT (directories in SKIP left out) mapped to its sha256 or link target."""
    state = {}
    for path in sorted(root.rglob("*")):
        if any(part in (path, *path.parents) for part in skip):
            continue
        if path.is_symlink():
            state[str(path)] = "-> " + os.readlink(path)
        elif path.is_file():
            state[str(path)] = hashlib.sha256(path.read_bytes()).hexdigest()
    return state


def probe_sections(args):
    """The --control, --read and --write lists of the read and write probe's arguments."""
    sections, current = {"--control": [], "--read": [], "--write": []}, None
    for arg in args:
        if arg in sections:
            current = arg
        else:
            sections[current].append(arg)
    return sections["--control"], sections["--read"], sections["--write"]


@unittest.skipUnless(JQ, "no jq or gojq (gh's --jq dialect) on this host")
class PrAuditTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.bin = self.root / "bin"
        self.bin.mkdir()
        (self.bin / "gh").symlink_to(FAKE_GH)
        (self.bin / "codex").symlink_to(FAKE_CODEX)
        self.rec = self.root / "rec"
        self.rec.mkdir()
        self.tmp = self.root / "tmp"
        self.tmp.mkdir()
        self.home = self.root / "home"
        (self.home / ".codex").mkdir(parents=True)
        (self.home / ".ssh").mkdir()
        (self.home / ".ssh/id_ed25519").write_text("not a key\n")
        self.auth = self.home / ".codex/auth.json"
        self.auth.write_text('{"tokens": {}}\n')
        gitconfig = self.root / "gitconfig"
        gitconfig.write_text("[user]\n\tname = t\n\temail = t@example.invalid\n[init]\n\tdefaultBranch = main\n")
        self.env = {
            **scratch_env(self.home),
            "PATH": f"{self.bin}:{os.environ['PATH']}",
            "TMPDIR": str(self.tmp),
            "LC_ALL": "C",
            "GIT_CONFIG_GLOBAL": str(gitconfig),
            "GIT_CONFIG_NOSYSTEM": "1",
            "FAKE_GH_CALLS": str(self.rec / "gh-calls"),
            "FAKE_GH_RESPONSES": str(self.rec / "gh-responses.json"),
            "FAKE_GH_STATE": str(self.rec / "gh-state.json"),
            "FAKE_GH_JQ": JQ,
            "FAKE_CODEX_CALLS": str(self.rec / "codex-calls"),
            "PR_AUDIT_WAIT_TRIES": "1",
            "PR_AUDIT_WAIT_SECONDS": "0",
        }
        self.origin = self.root / "origin.git"
        self.repo = self.root / "repo"
        self.git("init", "-q", "--bare", str(self.origin), cwd=self.root)
        self.git("init", "-q", str(self.repo), cwd=self.root)
        (self.repo / "AGENTS.md").write_text(f"# Rules\n\n{RULES}\n## Other\n\nNot audit rules.\n")
        self.git("add", "AGENTS.md")
        self.git("commit", "-q", "-m", "main")
        self.main = self.git("rev-parse", "HEAD")
        self.git("checkout", "-q", "-b", "feat")
        (self.repo / "AGENTS.md").write_text("# Rules\n\n## Audit\n\nThe head's own rules, which never bind.\n")
        (self.repo / "change.txt").write_text("changed\n")
        self.git("add", "-A")
        self.git("commit", "-q", "-m", "head")
        self.head = self.git("rev-parse", "HEAD")
        self.git("remote", "add", "origin", str(self.origin))
        self.git("push", "-q", "origin", "main", "feat:refs/pull/7/head")
        self.git("checkout", "-q", "main")
        self.answer()

    def git(self, *args, cwd=None):
        return subprocess.run(
            ["git", *args], cwd=cwd or self.repo, env=self.env, check=True, capture_output=True, text=True
        ).stdout.strip()

    def answer(self, head=None, base="main", body=BODY, fail=None):
        responses = [
            {"match": r"^repo view --json nameWithOwner$", "json": {"nameWithOwner": "acme/widgets"}},
            {
                "match": r"^pr view 7 --repo acme/widgets --json state,baseRefName,headRefOid,url$",
                "json": {
                    "state": "OPEN",
                    "baseRefName": base,
                    "headRefOid": head or self.head,
                    "url": "https://github.com/acme/widgets/pull/7",
                },
            },
            {"match": r"^pr view 7 --repo acme/widgets --json body$", "json": {"body": body}},
        ]
        if fail is not None:
            responses.insert(0, {"match": fail, "exit": 1, "stderr": "gh: injected failure\n"})
        (self.rec / "gh-responses.json").write_text(json.dumps(responses))

    def failing_tool(self, name, pattern, action="exit 2"):
        """PATH for a run where NAME runs ACTION when its arguments match the sh case PATTERN, else the real NAME."""
        real = shutil.which(name, path=self.env["PATH"])
        fakes = Path(tempfile.mkdtemp(dir=self.root, prefix="fakes-"))
        tool = fakes / name
        tool.write_text(f'#!/bin/sh\nREAL={real}\ncase "$*" in {pattern}) {action} ;; esac\nexec "$REAL" "$@"\n')
        tool.chmod(0o755)
        return f"{fakes}:{self.env['PATH']}"

    def set_main_agents(self, text):
        """Move main (in the checkout and origin) to a commit whose AGENTS.md is TEXT; the head's merge base stays."""
        (self.repo / "AGENTS.md").write_text(text)
        self.git("commit", "-q", "-am", "main rules")
        self.git("push", "-q", "origin", "main")

    def assert_stopped(self, run, code, message):
        """Exit CODE naming MESSAGE, no `codex exec`, and no run directory left."""
        self.assertEqual(run.returncode, code, run.stdout + run.stderr)
        self.assertIn(message, run.stderr)
        self.assertEqual(run.stdout, "")
        self.assertEqual([c for c in self.codex_calls() if c["argv"][:1] == ["exec"]], [], "no audit ran")
        self.assertEqual(list(self.tmp.iterdir()), [], "no run directory is left")

    def run_lever(self, *args, lever=LEVER, **env):
        return subprocess.run(
            [str(lever), *args],
            cwd=self.repo,
            env={**self.env, **env},
            capture_output=True,
            text=True,
            timeout=120,
            check=False,
        )

    def codex_calls(self):
        path = self.rec / "codex-calls"
        return [json.loads(line) for line in path.read_text().splitlines()] if path.exists() else []

    def assert_refused(self, run, message, exec_ran=False):
        self.assertEqual(run.returncode, 2, run.stdout + run.stderr)
        self.assertIn("refused:", run.stderr)
        self.assertIn(message, run.stderr)
        self.assertEqual([c for c in self.codex_calls() if c["argv"][:1] == ["exec"]], [], "a refusal runs no audit")
        self.assertEqual(list(self.tmp.iterdir()), [], "a refusal leaves no run directory")

    def lever_copy(self, edit):
        """A checkout layout in scratch with the lever, its manifest and the audit config EDIT returns."""
        tree = self.root / "tree"
        (tree / "scripts/orchestrator").mkdir(parents=True)
        (tree / "home/dot_agents/codex-audit").mkdir(parents=True)
        shutil.copy2(LEVER, tree / "scripts/orchestrator/pr-audit.sh")
        shutil.copy2(MANIFEST, tree / "home/dot_agents/agent-config.yaml")
        (tree / "home/dot_agents/codex-audit/config.toml").write_text(edit(TEMPLATE.read_text()))
        return tree / "scripts/orchestrator/pr-audit.sh"

    def test_the_audit_runs_codex_exec_without_a_sandbox_flag_under_the_audit_profile(self):
        before = tree_state(self.root, (self.tmp, self.rec))
        run = self.run_lever("7")
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertIn("sandbox probes passed", run.stderr)
        rundirs = list(self.tmp.iterdir())
        self.assertEqual(len(rundirs), 1)
        rundir = rundirs[0]
        verdict = rundir / "verdict.md"
        self.assertEqual(run.stdout, f"{verdict}\nVerdict: correct\n")
        self.assertEqual(sorted(p.name for p in rundir.iterdir()), ["codex.log", "prompt.md", "verdict.md"])
        self.assertEqual(tree_state(self.root, (self.tmp, self.rec)), before, "nothing outside the run dir is written")

        calls = self.codex_calls()
        self.assertEqual([c["argv"][0] for c in calls], ["sandbox", "sandbox", "exec"])
        work = rundir / "work"
        exec_argv = ["exec", "--strict-config", "--skip-git-repo-check", "--ephemeral", "-C", str(work / "cwd")]
        self.assertEqual(calls[2]["argv"], [*exec_argv, "-o", str(verdict), "-"])
        for call in calls:
            self.assertNotIn("-s", call["argv"])
            self.assertFalse(
                any(a.startswith("--sandbox") or a in ("-P", "--permission-profile") for a in call["argv"])
            )
            if call["argv"][0] == "sandbox":
                self.assertEqual(call["argv"][:4], ["sandbox", "--", "/bin/sh", "-c"])
            self.assertEqual(call["cwd"], str(work / "cwd"))
            self.assertEqual(call["env"]["HOME"], str(work / "home"))
            self.assertEqual(call["env"]["CODEX_HOME"], str(work / "codex-home"))
            self.assertEqual(call["env"]["TMPDIR"], str(work / "scratch-tmpdir"))
            self.assertIsNone(call["env"]["XDG_DATA_HOME"])
            self.assertEqual(call["auth_link"], str(self.auth))
            self.assertEqual(call["config"], calls[0]["config"])

        prompt = calls[2]["prompt"]
        self.assertIn("The standing audit rules.", prompt)
        self.assertNotIn("Not audit rules.", prompt)
        self.assertNotIn("The head's own rules", prompt)
        self.assertIn("It guarantees one thing.", prompt)
        self.assertIn(f"diff {self.main}..{self.head}", prompt)

    def test_codex_refreshing_its_login_writes_the_callers_auth_json_and_nothing_else(self):
        """The one write outside the run directory: Codex's own token refresh through the login link lands on the
        caller's auth.json (learn.chatgpt.com/docs/auth/ci-cd-auth.md: keep the refreshed file; one copy per serialized
        job stream), never on a copy in the run directory, and changes no other file."""
        before = tree_state(self.root, (self.tmp, self.rec))
        run = self.run_lever("7", FAKE_CODEX_REFRESH='{"tokens": {"refreshed": true}}\n')
        self.assertEqual(run.returncode, 0, run.stderr)
        after = tree_state(self.root, (self.tmp, self.rec))
        changed = sorted(path for path in before.keys() | after.keys() if before.get(path) != after.get(path))
        self.assertEqual(changed, [str(self.auth)])
        self.assertEqual(self.auth.read_text(), '{"tokens": {"refreshed": true}}\n')
        self.assertFalse(self.auth.is_symlink())
        (rundir,) = self.tmp.iterdir()
        self.assertFalse((rundir / "work").exists(), "the scratch CODEX_HOME and its link are gone")

    def test_the_config_is_the_generated_source_with_every_path_resolved(self):
        link = self.root / "homelink"
        link.symlink_to(self.home)
        env = scratch_env(link)
        run = self.run_lever("7", **env)
        self.assertEqual(run.returncode, 0, run.stderr)
        sandbox, _, exec_call = self.codex_calls()
        config = exec_call["config"]
        codex_home = exec_call["env"]["CODEX_HOME"]
        work = Path(codex_home).parent
        source = TEMPLATE.read_text()

        def entry(line):
            return line.startswith('"') and line.endswith(('" = "read"', '" = "write"', '" = "deny"'))

        self.assertEqual(
            [line for line in config.splitlines() if not entry(line)],
            [line for line in source.splitlines() if not entry(line)],
        )
        self.assertIn('default_permissions = "audit"', config.splitlines())
        self.assertNotIn("sandbox_mode", config)
        access = {}
        for line in filter(entry, config.splitlines()):
            key, _, value = line[1:-1].partition('" = "')
            self.assertNotIn(key, access, "no path is named twice")
            access[key] = value
        # The allowlist: nothing readable by default; the special names pass through unchanged.
        self.assertEqual(access[":root"], "deny")
        self.assertEqual(access[":minimal"], "read")
        self.assertEqual(access[":tmpdir"], "write")
        self.assertEqual([key for key, value in access.items() if value == "write"], [":tmpdir"])
        self.assertEqual(access[str(work / "repo")], "read")
        self.assertEqual(access[str(work / "cwd")], "read")
        self.assertEqual(access["/var/tmp"], "deny")
        for key in access:
            self.assertTrue(key.startswith(":") or os.path.isabs(key), key)
        for spelling in (link, self.home):  # the HOME as given and its resolved form
            self.assertEqual(access[f"{spelling}/.local/share/mise/installs"], "read")
            for rel in (
                ".ssh",
                ".codex",
                ".config/gh",
                ".local/share/gh",
                ".claude.json",
                ".netrc",
                "Library/Keychains",
            ):
                self.assertEqual(access[f"{spelling}/{rel}"], "deny")
        self.assertEqual(access[codex_home], "deny")
        self.assertEqual(access[str(self.auth)], "deny")
        controls, reads, writes = probe_sections(sandbox["probe_paths"])
        self.assertEqual(controls, [str(work / "repo/.git/HEAD"), str(work / "repo")])
        self.assertEqual(sandbox["probe_output"], "pr-audit-probe: all denied\n")
        self.assertIn(f"{link}/.codex/auth.json", reads)
        self.assertIn(str(self.auth), reads)
        self.assertIn(f"{codex_home}/auth.json", reads)
        self.assertIn(f"{self.home}/.ssh", reads)
        self.assertIn(str(work.parent / "canary"), reads)
        self.assertIn(str(link), reads)
        self.assertNotIn(f"{self.home}/.aws", reads, "only paths that exist are probed")
        self.assertEqual(writes[0], str(work.parent))
        self.assertIn("/var/tmp", writes, "an absolute deny key that is a directory gets a write probe")
        self.assertFalse((work.parent / "canary").exists(), "the canary is removed after the probe")

    def test_every_store_the_callers_environment_names_is_probed(self):
        stores = {name: self.root / "stores" / name.lower() for name in ("CLAUDE_CONFIG_DIR", "GH_CONFIG_DIR")}
        stores |= {name: self.root / "stores" / name.lower() for name in ("XDG_CONFIG_HOME", "XDG_DATA_HOME")}
        for path in stores.values():
            path.mkdir(parents=True)
        run = self.run_lever("7", **{name: str(path) for name, path in stores.items()})
        self.assertEqual(run.returncode, 0, run.stderr)
        _, reads, _ = probe_sections(self.codex_calls()[0]["probe_paths"])
        for path in stores.values():
            self.assertIn(str(path), reads)

    def test_a_relative_store_inside_an_allowed_root_refuses(self):
        """U71b audit round 8: a relative GH_CONFIG_DIR resolving under an allowed read root (here the mise installs
        under the real HOME) would be readable through the allowlist; it was skipped, now the run is refused."""
        store = self.home / ".local/share/mise/installs/gh-store"
        store.mkdir(parents=True)
        (store / "hosts.yml").write_text("token\n")
        for value in ("../home/.local/share/mise/installs/gh-store", "~/.local/share/mise/installs/gh-store"):
            with self.subTest(value=value):
                self.assert_stopped(self.run_lever("7", GH_CONFIG_DIR=value), 2, "inside the allowed root")
                self.assertEqual(self.codex_calls(), [], "no probe and no audit")

    def test_a_relative_store_elsewhere_is_probed_and_denied(self):
        store = self.root / "stores/gh"
        store.mkdir(parents=True)
        (store / "hosts.yml").write_text("token\n")
        run = self.run_lever("7", GH_CONFIG_DIR="../stores/gh", CLAUDE_CONFIG_DIR="../stores/../stores/gh")
        self.assertEqual(run.returncode, 0, run.stderr)
        sandbox = self.codex_calls()[0]
        _, reads, _ = probe_sections(sandbox["probe_paths"])
        self.assertIn(str(store), reads)
        self.assertIn(f"{self.repo}/../stores/gh", reads)
        self.assertEqual(sandbox["probe_output"], "pr-audit-probe: all denied\n")

    def test_a_store_that_cannot_be_resolved_refuses_before_the_probes(self):
        store = self.root / "stores/claude-unresolvable"
        store.mkdir(parents=True)
        path = self.failing_tool("perl", "*realpath*claude-unresolvable", "exit 1")
        run = self.run_lever("7", PATH=path, CLAUDE_CONFIG_DIR=str(store))
        self.assert_stopped(run, 2, "cannot resolve CLAUDE_CONFIG_DIR")
        self.assertEqual(self.codex_calls(), [], "no probe and no audit")

    def test_a_current_directory_that_cannot_be_resolved_refuses(self):
        gone = self.root / "gone"
        gone.mkdir()
        run = subprocess.run(
            ["/bin/sh", "-c", 'cd "$1" && rmdir "$1" && exec "$2" 7', "sh", str(gone), str(LEVER)],
            env=self.env,
            capture_output=True,
            text=True,
            timeout=120,
            check=False,
        )
        self.assert_stopped(run, 2, "cannot resolve the current directory")
        self.assertFalse((self.rec / "gh-calls").exists())

    def test_no_codex_on_path_refuses_before_any_call(self):
        run = self.run_lever("7", PATH="/usr/bin:/bin")
        self.assert_stopped(run, 2, "no codex on PATH")
        self.assertFalse((self.rec / "gh-calls").exists())

    def test_a_signal_between_the_launch_and_the_pid_stops_supervisor_and_codex(self):
        """U71b audit round 11: TERM or HUP after the lever launched the supervisor but before `codex_pid=$!` found no
        pid, so the lever exited and left the supervisor and codex running. The signal is now held until the pid is
        known; the lever now finds the supervisor in its job table. A BASH_ENV fixture pauses the lever between the
        `codex exec` supervisor's launch and its `wait`."""
        for signum in (signal.SIGTERM, signal.SIGHUP):
            with self.subTest(signal=signum.name):
                for path in self.tmp.iterdir():
                    shutil.rmtree(path)
                (self.rec / "codex-calls").unlink(missing_ok=True)
                marker = self.root / f"codex-still-ran-{signum.name}"
                pidfile = self.root / f"lever-{signum.name}.pid"
                lever = subprocess.Popen(
                    [str(LEVER), "7"],
                    cwd=self.repo,
                    env={
                        **self.env,
                        "BASH_ENV": str(PAUSE_AFTER_LAUNCH),
                        "PR_AUDIT_TEST_PAUSE_FILE": str(pidfile),
                        "PR_AUDIT_TIMEOUT": "600",
                        "FAKE_CODEX_HANG": str(marker),
                    },
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                )
                deadline = time.monotonic() + 60
                while not pidfile.exists():
                    self.assertIsNone(lever.poll(), "the lever ended before it launched codex exec")
                    self.assertLess(time.monotonic(), deadline)
                    time.sleep(0.02)
                os.kill(int(pidfile.read_text()), signum)  # inside the 2 s window before `wait "$!"`
                stdout, stderr = lever.communicate(timeout=60)
                self.assertEqual(lever.returncode, 128 + signum, stderr)
                self.assertEqual(stdout, "")
                self.assertIn(f"stopped by SIG{signum.name[3:]}", stderr)
                time.sleep(4)
                self.assertFalse(marker.exists(), "codex outlived a signal sent before its supervisor's pid was known")

    def test_a_signal_before_the_cleanup_trap_still_removes_the_run_directory(self):
        """The run directory's creation and the EXIT trap that removes it are one held window too."""
        pidfile = self.root / "lever-mktemp.pid"
        lever = subprocess.Popen(
            [str(LEVER), "7"],
            cwd=self.repo,
            env={
                **self.env,
                "BASH_ENV": str(PAUSE_AFTER_LAUNCH),
                "PR_AUDIT_TEST_PAUSE_FILE": str(pidfile),
                "PR_AUDIT_TEST_PAUSE_COMMAND": "trap cleanup EXIT",
                "PR_AUDIT_TEST_PAUSE_AT": "1",
            },
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        deadline = time.monotonic() + 60
        while not pidfile.exists():
            self.assertIsNone(lever.poll(), "the lever ended before it made the run directory")
            self.assertLess(time.monotonic(), deadline)
            time.sleep(0.02)
        os.kill(int(pidfile.read_text()), signal.SIGTERM)
        _, stderr = lever.communicate(timeout=60)
        self.assertEqual(lever.returncode, 143, stderr)
        self.assertEqual(list(self.tmp.iterdir()), [], "the run directory made before the trap is removed")
        self.assertEqual(self.codex_calls(), [])

    def test_a_config_that_does_not_select_the_audit_profile_is_refused(self):
        cases = (
            (lambda text: text.replace('default_permissions = "audit"\n', ""), "does not make the permission profile"),
            (lambda text: text.replace('"audit"\n', '":workspace"\n', 1), "does not make the permission profile"),
            (lambda text: 'sandbox_mode = "read-only"\n' + text, "names sandbox_mode"),
            (
                lambda text: text.replace("[permissions.audit]\n", "[permissions.other]\n"),
                "no single [permissions.audit]",
            ),
            (lambda text: text.replace('":root" = "deny"', '":root" = "read"'), "does not deny :root once"),
            (lambda text: text + '"etc/x" = "deny"\n', "which is not ~/<path>"),
            (lambda text: text + '"/opt/x" = "write"\n', "only :tmpdir"),
            (lambda text: text + '"~/.ssh/x" = "read"\n"~/.ssh/x" = "deny"\n', "to both read and deny"),
            (lambda text: text.replace('"~/.ssh" = "deny"', '"~/.ssh"  =  "deny"'), "filesystem lines"),
        )
        for edit, message in cases:
            with self.subTest(message=message):
                shutil.rmtree(self.root / "tree", ignore_errors=True)
                self.assert_refused(self.run_lever("7", lever=self.lever_copy(edit)), message)

    def test_a_login_that_is_missing_or_not_a_regular_file_is_refused(self):
        (self.root / "dir").mkdir()
        for target in (None, self.root / "dir", Path("/dev/null"), self.root / "absent"):
            with self.subTest(target=target):
                self.auth.unlink(missing_ok=True)
                if target is not None:
                    self.auth.symlink_to(target)
                self.assert_refused(self.run_lever("7"), "missing or not a readable regular file")
                self.assertEqual(self.codex_calls(), [])

    def test_a_probe_that_reads_a_denied_path_or_reaches_the_network_is_refused(self):
        for mode, message in (
            ("readable", "pr-audit-probe: readable"),
            ("curl0", "did not show the network denied"),
            ("nocurl", "did not show the network denied"),
            ("curl127", "did not show the network denied"),  # curl could not run: no evidence either way
            ("curl126", "did not show the network denied"),
            ("curl28", "did not show the network denied"),  # a timeout is no proof of a denial
        ):
            with self.subTest(mode=mode):
                self.assert_refused(self.run_lever("7", FAKE_CODEX_PROBE=mode), message)

    def test_a_denial_counts_only_with_its_permission_error_and_working_tools(self):
        """U71b audit round 5: a probe tool that could not run (exit 42, 126, 127, no denial text) is no denial, and the
        positive controls (cat and ls in the tree, mkdir in the scratch TMPDIR) must pass in the same sandbox run."""
        for mode, message in (
            ("toolexit42", "unproven read of"),
            ("toolexit126", "unproven read of"),
            ("toolexit127", "unproven read of"),
            ("controlexit127", "pr-audit-probe: control: mkdir in the scratch TMPDIR failed"),
            ("controlexit42", "pr-audit-probe: control: mkdir in the scratch TMPDIR failed"),
        ):
            with self.subTest(mode=mode):
                (self.rec / "codex-calls").unlink(missing_ok=True)
                self.assert_refused(self.run_lever("7", FAKE_CODEX_PROBE=mode), message)

    def test_the_probe_script_tells_denials_from_failures_on_its_own(self):
        """The lever's probe script itself, run outside any sandbox with tools that fail one way each."""
        self.assertEqual(self.run_lever("7").returncode, 0)
        argv = next(c["argv"] for c in self.codex_calls() if "for p do" in " ".join(c["argv"]))
        script = argv[argv.index("-c") + 1]
        tree = self.root / "tree-probe"
        (tree / "dir").mkdir(parents=True)
        (tree / "file").write_text("x\n")
        scratch = self.root / "scratch-tmpdir"
        scratch.mkdir()
        bindir = self.root / "probe-bin"
        bindir.mkdir()

        def run(tools, *args):
            for name, body in tools.items():
                (bindir / name).write_text(f"#!/bin/sh\n{body}\n")
                (bindir / name).chmod(0o755)
            env = {**self.env, "PATH": f"{bindir}:{self.env['PATH']}", "TMPDIR": str(scratch)}
            done = subprocess.run(
                ["/bin/sh", "-c", script, "sh", *args], env=env, capture_output=True, text=True, check=False
            )
            for name in tools:
                (bindir / name).unlink()
            return done.returncode, done.stdout.strip()

        denied = 'case "$*" in *denied*) echo "$0: x: Operation not permitted" >&2; exit 1 ;; esac; exec /bin/{} "$@"'
        controls = ("--control", str(tree / "file"), str(tree / "dir"))
        target = str(tree / "denied")
        tools = {name: denied.format(name) for name in ("cat", "ls", "mkdir")}
        self.assertEqual(run(tools, *controls, "--read", target, "--write", target), (0, "pr-audit-probe: all denied"))
        for code in ("42", "126", "127"):
            failing = f'case "$*" in *denied*) exit {code} ;; esac; exec /bin/{{}} "$@"'
            for name, label in (("cat", "unproven read of"), ("mkdir", "unproven write to")):
                with self.subTest(tool=name, exit=code):
                    status, out = run(
                        {**tools, name: failing.format(name)}, *controls, "--read", target, "--write", target
                    )
                    self.assertEqual(status, 3, out)
                    self.assertIn(label, out)
                    self.assertIn(f"(exit {code})", out)
            for name in ("cat", "ls", "mkdir"):
                with self.subTest(control=name, exit=code):
                    status, out = run({**tools, name: f"exit {code}"}, *controls, "--read", target)
                    self.assertEqual(status, 3, out)
                    self.assertIn("pr-audit-probe: control:", out)
        status, out = run({}, *controls, "--read", str(tree / "file"))
        self.assertEqual((status, out), (3, f"pr-audit-probe: readable {tree / 'file'}"))
        status, out = run({}, *controls, "--write", str(tree / "dir"))
        self.assertEqual((status, out), (3, f"pr-audit-probe: writable {tree / 'dir'}"))
        self.assertEqual(list((tree / "dir").iterdir()), [], "the write probe removes what it made")

    def test_only_a_resolve_or_connect_failure_counts_as_network_denied(self):
        for mode in ("curl6", "curl7"):
            with self.subTest(mode=mode):
                for path in self.tmp.iterdir():
                    shutil.rmtree(path)
                run = self.run_lever("7", FAKE_CODEX_PROBE=mode)
                self.assertEqual(run.returncode, 0, run.stderr)

    def test_a_template_read_that_fails_midway_runs_nothing(self):
        """A read error is never taken for the end of the file, which would drop the deny keys after it."""
        fake = self.root / "fakecat"
        fake.mkdir()
        cat = fake / "cat"
        cat.write_text(
            '#!/bin/sh\ncase "$*" in *codex-audit/config.toml) /usr/bin/head -n 28 "$2"; exit 1 ;; esac\n'
            'exec /bin/cat "$@"\n'
        )
        cat.chmod(0o755)
        run = self.run_lever("7", PATH=f"{fake}:{self.env['PATH']}")
        self.assertEqual(run.returncode, 1, run.stdout + run.stderr)
        self.assertIn("cannot read", run.stderr)
        self.assertEqual(self.codex_calls(), [], "no probe and no audit run on a partial config")

    def test_the_head_is_checked_out_without_the_callers_git_filters(self):
        """A .gitattributes in the head cannot make the caller's filter drivers run before confinement."""
        marker = self.root / "smudge-ran"
        self.git("checkout", "-q", "feat")
        (self.repo / ".gitattributes").write_text("* filter=mark\n")
        self.git("add", ".gitattributes")
        self.git("commit", "-q", "-m", "attributes")
        head = self.git("rev-parse", "HEAD")
        self.git("push", "-q", "-f", "origin", "feat:refs/pull/7/head")
        self.git("checkout", "-q", "main")
        # The lever removes the caller's GIT_CONFIG_GLOBAL, so the drivers go where its git would look: both files.
        for path in (Path(self.env["GIT_CONFIG_GLOBAL"]), self.home / ".gitconfig"):
            with path.open("a") as config:
                config.write(f'[filter "mark"]\n\tsmudge = "touch {marker}; cat"\n\tprocess = "touch {marker}"\n')
        attributes = self.home / ".config/git/attributes"
        attributes.parent.mkdir(parents=True)
        attributes.write_text("* filter=mark\n")
        self.answer(head=head)
        run = self.run_lever("7")
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertFalse(marker.exists(), "a filter driver ran on the audited tree")

    def test_the_callers_git_variables_never_change_the_audited_range(self):
        """U71b audit round 7: an inherited GIT_GRAFT_FILE made main a child of the head, so merge-base(main, head) was
        the head and the range empty. Every GIT_* the caller exports is removed before any git runs."""
        grafts = self.root / "grafts"
        grafts.write_text(f"{self.main} {self.head}\n")  # main's parent becomes the head
        other = self.root / "other-repo"
        self.git("init", "-q", str(other), cwd=self.root)
        empty_objects = self.root / "empty-objects"
        (empty_objects / "info").mkdir(parents=True)
        index = self.root / "foreign-index"
        before = tree_state(self.root, (self.tmp, self.rec))
        for name, value in (
            ("GIT_GRAFT_FILE", str(grafts)),
            ("GIT_DIR", str(other / ".git")),
            ("GIT_OBJECT_DIRECTORY", str(empty_objects)),
            ("GIT_ALTERNATE_OBJECT_DIRECTORIES", str(empty_objects)),
            ("GIT_INDEX_FILE", str(index)),
            ("GIT_WORK_TREE", str(other)),
            ("GIT_COMMON_DIR", str(other / ".git")),
            ("GIT_CEILING_DIRECTORIES", str(self.root)),
        ):
            with self.subTest(variable=name):
                for path in self.tmp.iterdir():
                    shutil.rmtree(path)
                (self.rec / "codex-calls").unlink(missing_ok=True)
                run = self.run_lever("7", **{name: value})
                self.assertEqual(run.returncode, 0, run.stderr)
                prompt = next(c for c in self.codex_calls() if c["argv"][:1] == ["exec"])["prompt"]
                self.assertIn(f"diff {self.main}..{self.head}", prompt)
                self.assertFalse(index.exists(), "the caller's index file is never written")
                self.assertEqual(tree_state(self.root, (self.tmp, self.rec)), before)

    def test_a_grafts_or_shallow_file_in_the_audited_repository_refuses(self):
        """The fresh repository holds neither; a git that wrote one during the fetch is a refusal, not a range."""
        for name in ("info/grafts", "shallow"):
            with self.subTest(file=name):
                for path in self.tmp.iterdir():
                    shutil.rmtree(path)
                action = f'"$REAL" "$@"; s=$?; d="${{5%/}}/.git"; mkdir -p "$d/info"; : > "$d/{name}"; exit $s'
                path = self.failing_tool("git", "*fetch*", action)
                self.assert_stopped(
                    self.run_lever("7", PATH=path), 2, "rewrites the history the audited range rests on"
                )

    def test_a_moved_head_a_foreign_base_or_no_contract_is_refused(self):
        for answer, message in (
            ({"head": "c" * 40}, "the head moved"),
            ({"base": "release"}, "not main"),
            ({"body": "Program-Unit: regime-cutover/U7\n\nNo contract here.\n"}, "no '## Contract' section"),
        ):
            with self.subTest(message=message):
                self.answer(**answer)
                self.assert_refused(self.run_lever("7"), message)

    def test_usage_is_checked_before_any_call(self):
        for args in ((), ("x7",), ("7", "8")):
            with self.subTest(args=args):
                self.assert_refused(self.run_lever(*args), "")
                self.assertFalse((self.rec / "gh-calls").exists())

    def test_a_failed_run_or_a_message_without_a_verdict_line_exits_1(self):
        awk = self.failing_tool("awk", "*", "exit 2")
        for env in (
            {"FAKE_CODEX_EXEC_EXIT": "1"},
            {"FAKE_CODEX_VERDICT": "Verdict: correct\n\nmore text\n"},
            {"PATH": awk},  # the read of the verdict's last line fails: no verdict is printed
        ):
            with self.subTest(env=env):
                for path in self.tmp.iterdir():
                    shutil.rmtree(path)
                run = self.run_lever("7", **env)
                self.assertEqual(run.returncode, 1, run.stderr)
                self.assertEqual(run.stdout, "")

    def test_the_timeout_stops_every_process_codex_started(self):
        """PR_AUDIT_TIMEOUT ends the audit, not just the launcher: a child codex left behind would keep running on the
        login after the lever reported the run failed."""
        marker = self.root / "child-still-ran"
        started = time.monotonic()
        run = self.run_lever("7", PR_AUDIT_TIMEOUT="1", FAKE_CODEX_HANG=str(marker))
        self.assertEqual(run.returncode, 1, run.stderr)
        self.assertLess(time.monotonic() - started, 30)
        time.sleep(4)
        self.assertFalse(marker.exists(), "a process codex started outlived the deadline")
        self.assertIn("codex exec exited 124", run.stderr)

    def test_a_signal_to_the_lever_stops_every_process_codex_started(self):
        """INT, TERM or HUP while codex runs stops codex's whole process group, not just the lever (U71b audit round 4:
        the supervisor died and the audit outlived it). INT goes to the lever's process group, as a terminal sends it;
        TERM and HUP go to the lever alone, as `kill` sends them."""
        for signum, to_group in ((signal.SIGINT, True), (signal.SIGTERM, False), (signal.SIGHUP, False)):
            with self.subTest(signal=signum.name):
                for path in self.tmp.iterdir():
                    shutil.rmtree(path)
                (self.rec / "codex-calls").unlink(missing_ok=True)
                marker = self.root / f"child-still-ran-{signum.name}"
                lever = subprocess.Popen(
                    [str(LEVER), "7"],
                    cwd=self.repo,
                    env={**self.env, "PR_AUDIT_TIMEOUT": "600", "FAKE_CODEX_HANG": str(marker)},
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    start_new_session=True,
                )
                deadline = time.monotonic() + 60
                while not any(c["argv"][:1] == ["exec"] for c in self.codex_calls()):
                    self.assertIsNone(lever.poll(), "the lever ended before codex exec ran")
                    self.assertLess(time.monotonic(), deadline)
                    time.sleep(0.1)
                if to_group:
                    os.killpg(lever.pid, signum)
                else:
                    lever.send_signal(signum)
                stdout, stderr = lever.communicate(timeout=30)
                self.assertEqual(lever.returncode, 128 + signum, stderr)
                self.assertEqual(stdout, "")
                self.assertIn(f"stopped by SIG{signum.name[3:]}", stderr)
                time.sleep(4)
                self.assertFalse(marker.exists(), "a process codex started outlived the signal")
                (rundir,) = self.tmp.iterdir()
                self.assertFalse((rundir / "work").exists(), "the scratch tree is removed")

    def injected(self, code):
        """PATH and environment for a run whose codex supervisor runs CODE first (tests/fixtures/pr-audit/inject-python.sh)."""
        bindir = Path(tempfile.mkdtemp(dir=self.root, prefix="inject-"))
        (bindir / "python3").symlink_to(INJECT_PYTHON)
        (bindir / "inject.py").write_text(code)
        return {
            "PATH": f"{bindir}:{self.env['PATH']}",
            "PR_AUDIT_TEST_REAL_PYTHON": shutil.which("python3", path=self.env["PATH"]),
            "PR_AUDIT_TEST_INJECT": str(bindir / "inject.py"),
        }

    def test_a_supervisor_that_cannot_launch_codex_refuses(self):
        """A failed setsid or exec in the child raises in the supervisor: mark, exit 125, refusal, no codex call."""
        setsid = (
            "import errno, subprocess\n"
            "class Popen(subprocess.Popen):\n"
            "    def __init__(self, *a, **k):\n"
            "        if k.get('start_new_session'):\n"
            "            raise OSError(errno.EPERM, 'setsid failed')\n"
            "        super().__init__(*a, **k)\n"
            "subprocess.Popen = Popen\n"
        )
        execfail = (
            "import subprocess\n"
            "_Popen = subprocess.Popen\n"
            "def Popen(argv, **k):\n"
            "    return _Popen(['/nonexistent/codex', *argv[1:]], **k)\n"
            "subprocess.Popen = Popen\n"
        )
        crash = "import signal\ndef boom(*a):\n    raise RuntimeError('injected')\nsignal.signal = boom\n"
        for name, code, reason in (
            ("setsid", setsid, "launch: [Errno 1] setsid failed"),
            ("exec", execfail, "launch: [Errno 2] No such file or directory"),
            ("any other exception", crash, "supervisor: RuntimeError: injected"),
        ):
            with self.subTest(failure=name):
                for path in self.tmp.iterdir():
                    shutil.rmtree(path)
                (self.rec / "codex-calls").unlink(missing_ok=True)
                run = self.run_lever("7", **self.injected(code))
                self.assert_stopped(run, 2, f"codex's supervisor failed ({reason}")
                self.assertEqual(self.codex_calls(), [], "codex never ran")

    def test_a_killpg_error_other_than_esrch_refuses_and_esrch_does_not(self):
        code = (
            "import errno, os\n"
            "def killpg(pgid, sig):\n"
            "    raise OSError(errno.{0}, os.strerror(errno.{0}))\n"
            "os.killpg = killpg\n"
        )
        for name, text in (
            ("EPERM", "PermissionError: [Errno 1] Operation not permitted"),
            ("EINVAL", "OSError: [Errno 22] Invalid argument"),
        ):
            with self.subTest(errno=name):
                for path in self.tmp.iterdir():
                    shutil.rmtree(path)
                run = self.run_lever("7", **self.injected(code.format(name)))
                self.assert_stopped(
                    run, 2, f"codex's supervisor failed (killpg SIGTERM: {text}; killpg SIGKILL: {text})"
                )
        for path in self.tmp.iterdir():
            shutil.rmtree(path)
        run = self.run_lever("7", **self.injected(code.format("ESRCH")))  # the group is gone: nothing to stop
        self.assertEqual(run.returncode, 0, run.stderr)

    def test_the_deadline_kills_a_group_that_ignores_term(self):
        marker = self.root / "term-ignorer-still-ran"
        started = time.monotonic()
        run = self.run_lever("7", PR_AUDIT_TIMEOUT="1", FAKE_CODEX_HANG=str(marker), FAKE_CODEX_IGNORE_TERM="1")
        self.assertEqual(run.returncode, 1, run.stderr)
        self.assertIn("codex exec exited 124", run.stderr)
        self.assertLess(time.monotonic() - started, 40)
        time.sleep(9)
        self.assertFalse(marker.exists(), "a TERM-ignoring process outlived the deadline's KILL")

    def test_a_signal_to_the_supervisor_before_or_after_the_launch_stops_codex(self):
        """Before Popen returns the signal is pending and acted on right after; after, it stops the group at once."""
        before = (
            "import os, signal, subprocess, sys\n"
            "_Popen = subprocess.Popen\n"
            "def Popen(argv, **k):\n"
            "    if 'exec' in argv:\n"
            "        os.kill(os.getpid(), signal.SIGTERM)\n"
            "    return _Popen(argv, **k)\n"
            "subprocess.Popen = Popen\n"
        )
        pidfile = self.root / "supervisor.pid"
        after = (
            "import os, subprocess\n"
            "_Popen = subprocess.Popen\n"
            "def Popen(argv, **k):\n"
            "    proc = _Popen(argv, **k)\n"
            "    if 'exec' in argv:\n"
            f"        open({str(pidfile)!r} + '.tmp', 'w').write(str(os.getpid()))\n"
            f"        os.rename({str(pidfile)!r} + '.tmp', {str(pidfile)!r})\n"
            "    return proc\n"
            "subprocess.Popen = Popen\n"
        )
        for name, code in (("before", before), ("after", after)):
            with self.subTest(moment=name):
                for path in self.tmp.iterdir():
                    shutil.rmtree(path)
                (self.rec / "codex-calls").unlink(missing_ok=True)
                marker = self.root / f"codex-still-ran-{name}"
                lever = subprocess.Popen(
                    [str(LEVER), "7"],
                    cwd=self.repo,
                    env={**self.env, **self.injected(code), "PR_AUDIT_TIMEOUT": "600", "FAKE_CODEX_HANG": str(marker)},
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                )
                if name == "after":
                    deadline = time.monotonic() + 60
                    while not (pidfile.exists() and any(c["argv"][:1] == ["exec"] for c in self.codex_calls())):
                        self.assertIsNone(lever.poll(), "the lever ended before codex exec ran")
                        self.assertLess(time.monotonic(), deadline)
                        time.sleep(0.02)
                    os.kill(int(pidfile.read_text()), signal.SIGTERM)
                _, stderr = lever.communicate(timeout=60)
                self.assertEqual(lever.returncode, 1, stderr)
                self.assertIn("codex exec exited 143", stderr)
                time.sleep(4)
                self.assertFalse(marker.exists(), "codex outlived the signal to its supervisor")

    def run_exec_injection(self, code, timeout="600"):
        """Start the lever with CODE injected into its supervisors and a hanging, TERM-ignoring fake `codex exec`;
        return the running lever and the marker its child would touch."""
        marker = self.root / "exec-child-still-ran"
        lever = subprocess.Popen(
            [str(LEVER), "7"],
            cwd=self.repo,
            env={
                **self.env,
                **self.injected(code),
                "PR_AUDIT_TIMEOUT": timeout,
                "FAKE_CODEX_HANG": str(marker),
                "FAKE_CODEX_IGNORE_TERM": "1",
            },
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        return lever, marker

    def assert_gone(self, *pids):
        for pid in pids:
            with self.assertRaises(ProcessLookupError, msg=f"process {pid} is still alive"):
                os.kill(pid, 0)

    def test_a_signal_while_the_supervisor_waits_stops_within_the_grace(self):
        """U71b audit round 13: the handler re-entered Popen.wait while its lock was held and deadlocked. The injection
        holds that lock for 0.5 s in every poll (kqueue and pidfd off, `_try_wait` slowed), so the TERM lands inside
        it; the handler now only records the signal and the main flow stops the group."""
        pidfile = self.root / "supervisor.pid"
        code = (
            "import os, subprocess, time\n"
            "_Popen = subprocess.Popen\n"
            "_try_wait = _Popen._try_wait\n"
            "class Popen(_Popen):\n"
            "    def __init__(self, argv, **k):\n"
            "        super().__init__(argv, **k)\n"
            "        if 'exec' in argv:\n"
            "            self._u71b_slow = True\n"
            f"            open({str(pidfile)!r} + '.tmp', 'w').write(str(os.getpid()))\n"
            f"            os.rename({str(pidfile)!r} + '.tmp', {str(pidfile)!r})\n"
            "    def _wait_kqueue(self, timeout):\n"
            "        return False\n"
            "    def _wait_pidfd(self, timeout):\n"
            "        return False\n"
            "    def _try_wait(self, flags):\n"
            "        if getattr(self, '_u71b_slow', False):\n"
            "            time.sleep(0.5)\n"
            "        return _try_wait(self, flags)\n"
            "subprocess.Popen = Popen\n"
        )
        lever, marker = self.run_exec_injection(code)
        deadline = time.monotonic() + 60
        while not (pidfile.exists() and any(c["argv"][:1] == ["exec"] for c in self.codex_calls())):
            self.assertIsNone(lever.poll(), "the lever ended before codex exec ran")
            self.assertLess(time.monotonic(), deadline)
            time.sleep(0.02)
        record = next(c for c in self.codex_calls() if c["argv"][:1] == ["exec"])
        sent = time.monotonic()
        os.kill(int(pidfile.read_text()), signal.SIGTERM)
        _, stderr = lever.communicate(timeout=30)
        self.assertLess(time.monotonic() - sent, 5 + 3, "the stop took longer than the grace")
        self.assertEqual(lever.returncode, 1, stderr)
        self.assertIn("codex exec exited 143", stderr)
        time.sleep(1)
        self.assert_gone(record["pid"], record["child_pid"])
        self.assertFalse(marker.exists())

    def test_an_exception_after_the_launch_still_stops_the_group(self):
        """U71b audit round 13: a wait() that raised exited through the mark and left the group running."""
        code = (
            "import subprocess, time\n"
            "_Popen = subprocess.Popen\n"
            "class Popen(_Popen):\n"
            "    def wait(self, timeout=None):\n"
            "        if 'exec' in self.args and not getattr(self, '_u71b_raised', False):\n"
            "            self._u71b_raised = True\n"
            "            time.sleep(1.5)\n"
            "            raise RuntimeError('injected wait')\n"
            "        return super().wait(timeout)\n"
            "subprocess.Popen = Popen\n"
        )
        lever, marker = self.run_exec_injection(code)
        _, stderr = lever.communicate(timeout=60)
        self.assertEqual(lever.returncode, 2, stderr)
        self.assertIn("codex's supervisor failed (supervisor: RuntimeError: injected wait)", stderr)
        record = next(c for c in self.codex_calls() if c["argv"][:1] == ["exec"])
        time.sleep(1)
        self.assert_gone(record["pid"], record["child_pid"])
        time.sleep(8)
        self.assertFalse(marker.exists(), "a group member outlived the supervisor's exception")

    def test_an_exception_in_the_stops_term_still_kills_the_group(self):
        code = (
            "import os, signal, subprocess\n"
            "_Popen = subprocess.Popen\n"
            "_killpg = os.killpg\n"
            "_exec = []\n"
            "def Popen(argv, **k):\n"
            "    if 'exec' in argv:\n"
            "        _exec.append(True)\n"
            "    return _Popen(argv, **k)\n"
            "def killpg(pgid, sig):\n"
            "    if _exec and sig == signal.SIGTERM:\n"
            "        raise RuntimeError('injected term')\n"
            "    return _killpg(pgid, sig)\n"
            "subprocess.Popen = Popen\n"
            "os.killpg = killpg\n"
        )
        lever, marker = self.run_exec_injection(code, timeout="2")
        _, stderr = lever.communicate(timeout=60)
        self.assertEqual(lever.returncode, 2, stderr)
        self.assertIn("codex's supervisor failed (killpg SIGTERM: RuntimeError: injected term)", stderr)
        record = next(c for c in self.codex_calls() if c["argv"][:1] == ["exec"])
        time.sleep(1)
        self.assert_gone(record["pid"], record["child_pid"])
        time.sleep(8)
        self.assertFalse(marker.exists(), "the group outlived a failed TERM")

    def run_escape(self, mode):
        pidfile = self.root / f"escaped-{mode}.pid"
        run = self.run_lever("7", PR_AUDIT_TIMEOUT="2", FAKE_CODEX_ESCAPE=f"{mode}:{pidfile}")
        pid = int(pidfile.read_text())
        self.addCleanup(lambda: subprocess.run(["kill", "-9", str(pid)], capture_output=True, check=False))
        return run, pid

    @unittest.skipUnless(sys.platform.startswith("linux"), "the child subreaper exists on Linux only")
    def test_on_linux_every_escaped_descendant_is_stopped(self):
        """U71b audit round 14: a descendant in a session of its own outlived the group stop. The supervisor is the
        child subreaper on Linux, so it inherits every orphan and KILLs them all."""
        for mode in ("single", "double"):
            with self.subTest(mode=mode):
                for path in self.tmp.iterdir():
                    shutil.rmtree(path)
                run, pid = self.run_escape(mode)
                self.assertEqual(run.returncode, 1, run.stderr)
                self.assertIn("codex exec exited 124", run.stderr)
                self.assert_gone(pid)
                self.assertNotIn("still running", run.stderr)

    @unittest.skipUnless(sys.platform == "darwin", "macOS has no subreaper; the lever only reports")
    def test_on_macos_an_escaped_descendant_is_reported(self):
        """macOS residual, detection only: a descendant in a session of its own outlives the run and is named."""
        run, pid = self.run_escape("single")
        self.assertEqual(run.returncode, 1, run.stderr)
        self.assertIn("codex exec exited 124", run.stderr)
        self.assertIn("still running after it stopped", run.stderr)
        self.assertIn(f"{pid} sleep 30", run.stderr)

    def test_a_failed_subreaper_refuses(self):
        """The prctl that makes the supervisor the subreaper must succeed on Linux (shown here as Linux on any host)."""
        code = (
            "import ctypes, sys\n"
            "sys.platform = 'linux'\n"
            "class Libc:\n"
            "    def prctl(self, *args):\n"
            "        ctypes.set_errno(1)\n"
            "        return -1\n"
            "ctypes.CDLL = lambda *a, **k: Libc()\n"
        )
        run = self.run_lever("7", **self.injected(code))
        self.assert_stopped(
            run, 2, "codex's supervisor failed (subreaper: PermissionError: [Errno 1] Operation not permitted)"
        )
        self.assertEqual(self.codex_calls(), [], "codex never ran")

    def test_a_signal_during_a_wait_that_returns_wins_over_codex_status(self):
        """U71b audit round 14 (P3): a TERM recorded while the last wait() returned was ignored and the run exited 0."""
        code = (
            "import os, signal, subprocess\n"
            "_Popen = subprocess.Popen\n"
            "class Popen(_Popen):\n"
            "    def wait(self, timeout=None):\n"
            "        status = super().wait(timeout)\n"
            "        if 'exec' in self.args:\n"
            "            os.kill(os.getpid(), signal.SIGTERM)\n"
            "        return status\n"
            "subprocess.Popen = Popen\n"
        )
        run = self.run_lever("7", **self.injected(code))
        self.assertEqual(run.returncode, 1, run.stdout + run.stderr)
        self.assertIn("codex exec exited 143", run.stderr)
        self.assertEqual(run.stdout, "")

    # Each step of the supervisor's stop made to raise in the `codex exec` run (U71b audit round 15): the step's name in
    # the mark, and the injected Python that makes it raise.
    STOP_STEP_INJECTIONS = (
        (
            "ignore signals",
            (
                "_signal = signal.signal\n"
                "def _ignore(sig, handler):\n"
                "    if handler is signal.SIG_IGN:\n"
                "        raise RuntimeError('injected step')\n"
                "    return _signal(sig, handler)\n"
                "signal.signal = _ignore\n"
            ),
        ),
        (
            "snapshot",
            (
                "_run = subprocess.run\n"
                "_ps = []\n"
                "def _first_ps(argv, **k):\n"
                "    if argv[0] == '/bin/ps':\n"
                "        _ps.append(1)\n"
                "        if len(_ps) == 1:\n"
                "            raise RuntimeError('injected step')\n"
                "    return _run(argv, **k)\n"
                "subprocess.run = _first_ps\n"
            ),
        ),
        (
            "killpg SIGTERM",
            (
                "_killpg = os.killpg\n"
                "def _term(pgid, sig):\n"
                "    if sig == signal.SIGTERM:\n"
                "        raise RuntimeError('injected step')\n"
                "    return _killpg(pgid, sig)\n"
                "os.killpg = _term\n"
            ),
        ),
        (
            "grace",
            (
                "_poll = subprocess.Popen.poll\n"
                "def _grace_poll(self):\n"
                "    if 'exec' in self.args:\n"
                "        raise RuntimeError('injected step')\n"
                "    return _poll(self)\n"
                "subprocess.Popen.poll = _grace_poll\n"
            ),
        ),
        (
            "killpg SIGKILL",
            (
                "_killpg = os.killpg\n"
                "def _kill(pgid, sig):\n"
                "    if sig == signal.SIGKILL:\n"
                "        raise RuntimeError('injected step')\n"
                "    return _killpg(pgid, sig)\n"
                "os.killpg = _kill\n"
            ),
        ),
        (
            "reap",
            (
                "_wait = subprocess.Popen.wait\n"
                "def _reap(self, timeout=None):\n"
                "    if timeout == 5:\n"
                "        raise RuntimeError('injected step')\n"
                "    return _wait(self, timeout)\n"
                "subprocess.Popen.wait = _reap\n"
            ),
        ),
        (
            "sweep",
            (
                "_listdir = os.listdir\n"
                "def _proc(path='.'):\n"
                "    if path == '/proc':\n"
                "        raise RuntimeError('injected step')\n"
                "    return _listdir(path)\n"
                "os.listdir = _proc\n"
            ),
        ),
        (
            "survivors",
            (
                "_run = subprocess.run\n"
                "_ps = []\n"
                "def _second_ps(argv, **k):\n"
                "    if argv[0] == '/bin/ps':\n"
                "        _ps.append(1)\n"
                "        if len(_ps) == 2:\n"
                "            raise RuntimeError('injected step')\n"
                "    return _run(argv, **k)\n"
                "subprocess.run = _second_ps\n"
            ),
        ),
    )

    def test_each_stop_step_that_raises_still_stops_the_group(self):
        """U71b audit round 15: a statement of the stop that raised skipped the steps after it (rounds 13 to 15). Each
        step now runs on its own; whichever raises, the group is gone and the run fails closed (exit 125, refusal)."""
        for name, body in self.STOP_STEP_INJECTIONS:
            with self.subTest(step=name):
                if name == "sweep" and not sys.platform.startswith("linux"):
                    self.skipTest("the subreaper sweep runs on Linux only")
                for path in self.tmp.iterdir():
                    shutil.rmtree(path)
                (self.rec / "codex-calls").unlink(missing_ok=True)
                marker = self.root / f"step-{name.replace(' ', '-')}"
                code = "import os, signal, subprocess, sys\nif 'exec' in sys.argv:\n" + "".join(
                    f"    {line}\n" for line in body.splitlines()
                )
                started = time.monotonic()
                run = self.run_lever(
                    "7",
                    PR_AUDIT_TIMEOUT="2",
                    FAKE_CODEX_HANG=str(marker),
                    FAKE_CODEX_HANG_DELAY="10",  # past the deadline and the 5 s grace a raising TERM leaves
                    **self.injected(code),
                )
                self.assertEqual(run.returncode, 2, run.stdout + run.stderr)
                self.assertEqual(run.stdout, "")
                self.assertIn("refused: codex's supervisor failed (", run.stderr)
                self.assertIn(f"{name}: RuntimeError: injected step", run.stderr)
                record = next(c for c in self.codex_calls() if c["argv"][:1] == ["exec"])
                time.sleep(1)
                self.assert_gone(record["pid"], record["child_pid"])
                time.sleep(max(0.0, 11 - (time.monotonic() - started)))
                self.assertFalse(marker.exists(), f"a group member outlived a raising {name} step")

    def test_a_wait_that_returns_after_the_deadline_is_the_deadline(self):
        """U71b audit round 15 (P3): a wait() returning after the deadline gave codex's status instead of 124."""
        code = (
            "import subprocess, sys, time\n"
            "_wait = subprocess.Popen.wait\n"
            "def wait(self, timeout=None):\n"
            "    if 'exec' in self.args and timeout is not None and timeout < 1:\n"
            "        time.sleep(3)\n"
            "        return 0\n"
            "    return _wait(self, timeout)\n"
            "subprocess.Popen.wait = wait\n"
        )
        marker = self.root / "late-return"
        run = self.run_lever("7", PR_AUDIT_TIMEOUT="1", FAKE_CODEX_HANG=str(marker), **self.injected(code))
        self.assertEqual(run.returncode, 1, run.stdout + run.stderr)
        self.assertIn("codex exec exited 124", run.stderr)

    def test_a_mark_that_cannot_be_read_is_a_failure_not_a_run(self):
        code = "import subprocess\ndef Popen(*a, **k):\n    raise OSError(1, 'no')\nsubprocess.Popen = Popen\n"
        env = self.injected(code)
        cat = self.failing_tool("cat", "*group-mark*", "exit 1")
        env["PATH"] = f"{cat.split(':', 1)[0]}:{env['PATH']}"
        self.assert_stopped(self.run_lever("7", **env), 1, "cannot read")
        self.assertEqual(self.codex_calls(), [], "codex never ran")

    def test_the_callers_perl_variables_are_removed(self):
        """PERL5OPT would load code into the perl that bounds gh and git and resolves paths; the lever removes PERL*."""
        run = self.run_lever("7", PERL5OPT="-MU71bNoSuchModule")
        self.assertEqual(run.returncode, 0, run.stderr)

    def test_no_python3_on_path_refuses(self):
        bindir = Path(tempfile.mkdtemp(dir=self.root, prefix="nopython-"))
        for tool in (
            "codex",
            "gh",
            "git",
            "perl",
            "awk",
            "grep",
            "sed",
            "cat",
            "rm",
            "mkdir",
            "mktemp",
            "od",
            "ln",
            "shasum",
        ):
            found = shutil.which(tool, path=self.env["PATH"])
            if found:
                (bindir / tool).symlink_to(found)
        run = self.run_lever("7", PATH=f"{bindir}:/bin:/usr/sbin:/sbin")
        if shutil.which("python3", path="/bin:/usr/sbin:/sbin"):
            self.skipTest("a python3 in /bin")
        self.assert_stopped(run, 2, "no python3 on PATH")

    def test_main_audit_rules_that_cannot_be_read_whole_refuse_before_codex(self):
        """main:AGENTS.md is read once and whole (U71b audit round 3): a failed or short read never yields rules."""
        for pattern, action, message in (
            ("*cat-file\\ blob*:AGENTS.md*", "exit 128", "cannot read AGENTS.md of main"),
            ("*cat-file\\ -s*:AGENTS.md*", "exit 128", "cannot read the size of AGENTS.md"),
            ("*cat-file\\ blob*:AGENTS.md*", '"$REAL" "$@" | head -c 20; exit 0', "read 20 of the"),
        ):
            with self.subTest(action=action, pattern=pattern):
                path = self.failing_tool("git", pattern, action)
                self.assert_stopped(self.run_lever("7", PATH=path), 2, message)
                self.assertEqual(self.codex_calls(), [], "no probe either")

    def test_main_without_one_nonempty_audit_section_refuses_before_codex(self):
        for text, message in (
            ("# Rules\n\n## Other\n\nNot audit rules.\n", "has 0 '## Audit' headings"),
            ("## Audit\n\nOne.\n\n## Audit\n\nTwo.\n", "has 2 '## Audit' headings"),
            ("# Rules\n\n## Audit\n\n   \n\n## Other\n\nText.\n", "an empty '## Audit' section"),
            ("# Rules\n\n## Audit\n", "an empty '## Audit' section"),  # a section cut before its body
            ("# Rules\n\n## Audit \n\nTrailing space is another heading.\n", "has 0 '## Audit' headings"),
        ):
            with self.subTest(text=text):
                self.set_main_agents(text)
                self.assert_stopped(self.run_lever("7"), 2, message)
                self.assertEqual(self.codex_calls(), [])

    def test_every_other_safety_read_that_fails_stops_before_the_audit(self):
        """Each producer a safety decision reads (preferences 21): its failure is a stop, never an empty answer."""
        grep = lambda pattern: {"PATH": self.failing_tool("grep", pattern)}
        git = lambda pattern: {"PATH": self.failing_tool("git", pattern, "exit 128")}
        perl = lambda pattern: {"PATH": self.failing_tool("perl", pattern, "exit 1")}
        cases = (
            ("profile default", grep("*default_permissions*"), 1, "cannot search"),
            ("sandbox_mode", grep("*sandbox_mode*"), 1, "cannot search"),
            ("profile table", grep("*permissions.audit*"), 1, "cannot search"),
            ("filesystem lines", grep("*'\"(read|write|deny)\"'*"), 1, "cannot search"),
            ("root deny", grep('*\':root" = "deny"\'*'), 1, "cannot search"),
            ("contract", grep("*Contract*"), 1, "cannot read"),
            ("rendered paths", grep("*'^\"/'*"), 1, "cannot search the rendered config"),
            ("resolved paths", grep("-c\\ ."), 1, "cannot count the resolved paths"),
            ("repository root", git("*--show-toplevel*"), 2, "run from the repository checkout"),
            ("common directory", git("*--git-common-dir*"), 1, "cannot read the git common directory"),
            ("origin url", git("*remote\\ get-url*"), 1, "has no origin remote"),
            ("repack", git("*repack*"), 1, "git repack"),
            ("repack that copies nothing", {"PATH": self.failing_tool("git", "*repack*", "exit 0")}, 1, "on its own"),
            ("self-contained objects", git("*rev-list*"), 1, "on its own"),
            ("alternates removal", {"PATH": self.failing_tool("rm", "*alternates*", "exit 1")}, 1, "alternates"),
            ("checkout", git("*checkout*"), 1, "git checkout"),
            ("probe output", {"PATH": self.failing_tool("cat", "*probe.out*", "exit 1")}, 1, "cannot read"),
            ("allowed root realpath", perl("*realpath*/work/repo"), 2, "cannot resolve the allowed path"),
            ("git init", git("*init\\ -q*"), 1, "git init"),
            ("run directory", {"PATH": self.failing_tool("mktemp", "*pr-audit-7*", "exit 1")}, 1, "mktemp failed"),
            ("scratch tree", {"PATH": self.failing_tool("mkdir", "*scratch-tmpdir*", "exit 1")}, 1, "scratch tree"),
            (
                "login link",
                {"PATH": self.failing_tool("ln", "*auth.json*", "exit 1")},
                1,
                "cannot link the Codex login",
            ),
            ("body removal", {"PATH": self.failing_tool("rm", "*body.md*", "exit 1")}, 1, "cannot remove"),
            ("group mark removal", {"PATH": self.failing_tool("rm", "*group-mark*", "exit 1")}, 1, "group-mark"),
            ("canary removal", {"PATH": self.failing_tool("rm", "*canary*", "exit 1")}, 1, "cannot remove the canary"),
            ("login realpath", {"PATH": self.failing_tool("perl", "*realpath*")}, 2, "cannot resolve the Codex login"),
            ("gh repository", {"FAIL": "^repo view"}, 1, "cannot read the repository"),
            ("gh head and base", {"FAIL": "^pr view 7 .*headRefOid"}, 1, "cannot read pull request 7"),
            ("gh body", {"FAIL": "^pr view 7 .*--json body$"}, 1, "cannot read the body"),
            ("fetch", git("*fetch*"), 1, "git fetch of refs/pull/7/head"),
            ("fetched head", git("*'refs/audit/head^{commit}'*"), 2, "the head moved"),
            ("fetched main", git("*'refs/audit/main^{commit}'*"), 1, "cannot resolve the fetched main"),
            ("merge base", git("*merge-base*"), 1, "git merge-base"),
            ("probe runner", {"FAKE_CODEX_PROBE": "failrun"}, 2, "the sandbox read and write probe did not pass"),
            ("nonce", {"PATH": self.failing_tool("od", "*")}, 1, "cannot read /dev/urandom"),
            (
                "prompt body copy",
                {"PATH": self.failing_tool("cat", "*body.md*", "exit 1")},
                1,
                "cannot write the prompt",
            ),
        )
        for name, env, code, message in cases:
            with self.subTest(read=name):
                for path in self.tmp.iterdir():
                    shutil.rmtree(path)
                (self.rec / "codex-calls").unlink(missing_ok=True)
                self.answer(fail=env.pop("FAIL", None))
                self.assert_stopped(self.run_lever("7", **env), code, message)

    def test_a_deny_path_that_cannot_be_resolved_refuses(self):
        locked = self.home / "locked"
        locked.mkdir()
        locked.chmod(0)
        self.addCleanup(locked.chmod, 0o755)
        lever = self.lever_copy(lambda text: text + '"~/locked/inner" = "deny"\n')
        self.assert_stopped(self.run_lever("7", lever=lever), 2, f"cannot resolve {locked}")


class AuditConfigSourceTest(unittest.TestCase):
    """The generator renders codex.audit only as an allowlist whose keys the lever can resolve.

    The committed file equals the render of the real manifest through `generate-agent-configs.py --check`."""

    def test_a_filesystem_entry_the_lever_cannot_resolve_fails_the_render(self):
        module = load_generator()
        manifest = sample_manifest()
        text = module.render_codex_audit_config(manifest)
        self.assertIn('default_permissions = "audit"\n', text)
        self.assertIn('":root" = "deny"\n', text)
        self.assertIn('"~/.ssh" = "deny"\n', text)
        good = dict(manifest["codex"]["audit"]["filesystem"])
        for change in (
            {"etc/x": "deny"},
            {"~/../x": "deny"},
            {"~/a/./b": "read"},
            {'~/a"b': "deny"},
            {"$OTHER": "read"},
            {":workspace_roots": "read"},
            {"/opt/x": "write"},
            {"/opt/x": "allow"},
            {":root": "read"},
            {"$AUDIT_TREE": "deny"},
            {"$CODEX_HOME": None},
            {"$CODEX_LOGIN_HOME": None},
        ):
            with self.subTest(change=change):
                filesystem = {**good, **change}
                filesystem = {key: value for key, value in filesystem.items() if value is not None}
                manifest["codex"]["audit"]["filesystem"] = filesystem
                with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
                    module.render_codex_audit_config(manifest)


if __name__ == "__main__":
    unittest.main()
