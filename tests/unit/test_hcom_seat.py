"""Exercise scripts/orchestrator/hcom-seat against fake hcom, herdr and omp.

The fakes (tests/fixtures/hcom-seat/fake-tool.py under the three names) record argv; the fake hcom plays the herdr
terminal preset so the test sees what omp receives. HOME is a scratch directory holding the three policy overlays and
the three extension directories (the two routes and the stop gate's); the cwd is a scratch git repository with an
`origin/main` ref; `HCOM_DIR` is `hcom` in a directory of each test's own (`tempfile.mkdtemp` under TMPDIR), so
concurrent suites never share it. Nothing touches the real `~/.hcom`, `~/.agents` or a herdr pane.
"""

import collections
import http.server
import json
import os
import re
import shlex
import shutil
import socket
import stat
import subprocess
import sys
import tempfile
import threading
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))  # dotted runs too; discover -s tests/unit already has it
from scratch_git import git_init, quiet_git_env

ROOT = Path(__file__).resolve().parents[2]
SEAT = ROOT / "scripts/orchestrator/hcom-seat"
FAKE = ROOT / "tests/fixtures/hcom-seat/fake-tool.py"
GATE_DRIVER = ROOT / "home/dot_agents/omp/hooks/tests/launch-driver.ts"
BUN = shutil.which("bun")
# A real executable binary (Mach-O on macOS, ELF on Linux), for tools hcom-seat requires to be no script.
BINARY_STAND_IN = Path(os.path.realpath("/usr/bin/true"))
SYSTEM_PATH = "/usr/bin:/bin"
# The rows under the shared Claude Code directory that every seat's settings deny for write (U318).
SHARED_CLAUDE_DENIES = (
    "settings.json",
    "settings.local.json",
    "rules",
    "hooks",
    "plugins",
    "skills",
    "commands",
    "agents",
)
# The fake API key the tests place (regime-cutover U512), built at runtime so no file holds a literal the secret scan
# matches; it rides to the fake Models API in the `x-api-key` header and must appear in no line of any lever.
FAKE_KEY = "sk-" + "ant-api03-" + "FAKEKEYFORTEST" + "0" * 12


def fake_models_api(case, answer):
    """Start a fake Models API on the loopback for the lifetime of `case`: every GET is recorded (path, `x-api-key`,
    `anthropic-version`) in the returned list, and answered with the HTTP status `answer`, or left hanging past the
    lever's 20 s alarm when `answer` is "hang". Returns the URL the lever is pointed at (REGIME_ANTHROPIC_MODELS_URL)
    and the record list."""
    requests = []
    release = threading.Event()

    class Handler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            requests.append(
                {
                    "path": self.path,
                    "x-api-key": self.headers.get("x-api-key", ""),
                    "anthropic-version": self.headers.get("anthropic-version", ""),
                }
            )
            if answer == "hang":
                release.wait(120)
                return
            body = b'{"data": []}' if answer == 200 else b'{"type": "error"}'
            self.send_response(answer)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, *args):
            pass

    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    server.daemon_threads = True
    threading.Thread(target=server.serve_forever, daemon=True).start()
    case.addCleanup(server.server_close)
    case.addCleanup(server.shutdown)
    case.addCleanup(release.set)
    return f"http://127.0.0.1:{server.server_address[1]}/v1/models?limit=1", requests


def closed_loopback_url():
    """A loopback URL nothing listens on, the fixtures' default Models API: a lever that calls it gets a refused
    connection (`unreadable`), never the real API, so no unit test reaches the network."""
    with socket.socket() as probe:
        probe.bind(("127.0.0.1", 0))
        port = probe.getsockname()[1]
    return f"http://127.0.0.1:{port}/v1/models?limit=1"


# The login group table's range (U498, `login_group_of_role`; `LOGIN_GROUPS` beside it in hcom-seat since U498c): the
# login directories `<seats-root>/.state/claude-<group>` a seats root can hold, in the table's order. Every seat's
# settings deny each but its own group's, and the legacy `.state/claude`, for read (U498c).
LOGIN_GROUPS = ("worker", "orchestrator", "audit", "router")


def login_read_denies(seats, group):
    """The denyRead rows a seat of login `group` carries for the login directories under the physical seats root
    `seats` (U498c): every other group's `.state/claude-<group>` in the table's order, then the legacy `.state/claude`."""
    return [f"{seats}/.state/claude-{other}" for other in LOGIN_GROUPS if other != group] + [f"{seats}/.state/claude"]


def file_rows_under_read_denies(fs):
    """The `(allowRead row, denyRead row)` pairs of a rendered settings `filesystem` block whose grant is a regular
    file at or under the deny (U512i, verdict U512h-4c5ec14e: srt 0.0.81's Linux backend binds such a file back into
    the tmpfs it mounts over the denied directory, with the file's parents remade 0755, so the grant loses its
    directory's mode and `claude-keyed`, which holds the key directory to 0700, refuses inside the sandbox what the
    host's preflight passed; hcom-seat's `allow_read_files_check` refuses the shape, and no role renders it)."""
    return [
        (row, deny)
        for row in fs["allowRead"]
        if Path(row).is_file()
        for deny in fs["denyRead"]
        if row == deny or row.startswith(f"{deny}/")
    ]


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


class SeatFixture(unittest.TestCase):
    """The scratch host every hcom-seat test launches in; `tests/unit/test_hcom_seat_dsh.py` builds on it too."""

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
        # A launch whose profile names the claude-bridge route (the fixture's overlays name none, so most launches have
        # nothing to log in) needs the login group's claude.ai login (U318, per group since U498) beside the seats' API
        # key (U512): seat-login-preflight reads the login with `claude auth status` under
        # `<seats-root>/.state/claude-<group>`, and `claude` is a tool hcom-seat resolves, so this fake answers for
        # every launch and no test runs the host's Claude Code. It prints the documented record with the method
        # FAKE_CLAUDE_AUTH_METHOD (`claude.ai` unless set), exits FAKE_CLAUDE_AUTH_STATUS (0 unless set) and records
        # each call with its directory and whether a token name reached it.
        self.claude_calls = root / "claude-auth-calls"
        (bindir / "claude").write_text(
            "#!/bin/sh\n"
            'printf \'%s %s token=%s\\n\' "$*" "${CLAUDE_CONFIG_DIR-unset}" "${CLAUDE_CODE_OAUTH_TOKEN-unset}"'
            f" >> {shlex.quote(str(self.claude_calls))}\n"
            'printf \'{"configDirectory": "%s", "authMethod": "%s"}\\n\' "${CLAUDE_CONFIG_DIR-}"'
            ' "${FAKE_CLAUDE_AUTH_METHOD:-claude.ai}"\n'
            'exit "${FAKE_CLAUDE_AUTH_STATUS:-0}"\n'
        )
        (bindir / "claude").chmod(0o755)
        # `claude-keyed --check` (regime-cutover U512): hcom-seat's gate on the seats' API key file and the preflight's
        # judge of its form, a tool hcom-seat resolves like every other (the installed `~/.local/bin/common/claude-keyed`
        # on a host). This fake records each call with the file the environment named and answers by
        # FAKE_CLAUDE_KEYED_STATUS: 0 (unset) the ok line, 2 a refusal line with FAKE_CLAUDE_KEYED_REASON (the real
        # lever's absent-file reason unless set), anything else that status with a line (unreadable to the callers).
        self.claude_keyed_calls = root / "claude-keyed-calls"
        (bindir / "claude-keyed").write_text(
            "#!/bin/sh\n"
            'printf \'%s REGIME_ANTHROPIC_KEY_FILE=%s\\n\' "$*" "${REGIME_ANTHROPIC_KEY_FILE-unset}"'
            f" >> {shlex.quote(str(self.claude_keyed_calls))}\n"
            '[ "$1" = --check ] && [ $# -eq 1 ] || exit 64\n'
            'case "${FAKE_CLAUDE_KEYED_STATUS:-0}" in\n'
            "0) printf 'key file ok: %s; executable: /fake/sdk/claude\\n' \"${REGIME_ANTHROPIC_KEY_FILE-}\"; exit 0 ;;\n"
            "2) printf 'claude-keyed: refused: %s\\n' \"${FAKE_CLAUDE_KEYED_REASON:-the key file"
            ' ${REGIME_ANTHROPIC_KEY_FILE-} is absent; place the API key there (the U510 handout)}" >&2; exit 2 ;;\n'
            "*) printf 'claude-keyed: refused: cannot read the mode and owner of the key file (stat failed)\\n' >&2;"
            ' exit "${FAKE_CLAUDE_KEYED_STATUS}" ;;\n'
            "esac\n"
        )
        (bindir / "claude-keyed").chmod(0o755)
        # The preflight reads that record with jq; macOS 14 ships no /usr/bin/jq, so a host's jq joins the fixture's
        # PATH where the system has none (hcom-seat resolves it like every tool).
        if not Path("/usr/bin/jq").exists() and shutil.which("jq"):
            (bindir / "jq").symlink_to(Path(shutil.which("jq")).resolve())
        self.tools = (root / "home/.local/state/hcom-seat/tools").resolve()
        self.calls = root / "calls"
        self.calls.mkdir()
        self.seats = str(root / "seats")
        # The hcom store lies outside the scratch tree (a seat write root of its own, beside the seats root) in a
        # directory of this test's own under TMPDIR, so two suites running at once never share it.
        store_parent = Path(tempfile.mkdtemp(prefix="hcom-seat-store-"))
        self.addCleanup(shutil.rmtree, store_parent, True)
        self.store = store_parent / "hcom"
        self.store.mkdir()
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
            # The preflight's Models API call (U512) goes to a loopback port nothing listens on unless a test starts
            # a fake (models_api), so no launch here reaches the real API.
            "REGIME_ANTHROPIC_MODELS_URL": closed_loopback_url(),
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

    def settings_of(self, name):
        return json.loads(Path(self.seats, ".sandbox", name, "srt-settings.json").read_text())

    @property
    def key_file(self):
        """The seats' API key file hcom-seat names to every seat (U512): `<seats-root>/.state/anthropic/api-key`."""
        return Path(self.seats, ".state/anthropic/api-key")

    @property
    def key_dir(self):
        """The key file's directory `<seats-root>/.state/anthropic`, the read grant of every role (U512i)."""
        return self.key_file.parent

    def place_key(self):
        """Place the fake key as the U510 handout does: one line, 0600, in the 0700 `.state/anthropic` directory."""
        self.key_file.parent.mkdir(parents=True, exist_ok=True)
        for directory in (Path(self.seats), Path(self.seats, ".state"), self.key_file.parent):
            directory.chmod(0o700)
        self.key_file.write_text(FAKE_KEY + "\n")
        self.key_file.chmod(0o600)
        return self.key_file

    def models_api(self, answer=200):
        """A fake Models API answering `answer`; its request record is `self.models_requests`."""
        url, self.models_requests = fake_models_api(self, answer)
        return url


class HcomSeatTest(SeatFixture):
    def test_a_seat_without_a_login_or_an_api_key_file_starts_nothing(self):
        """U37: hcom-seat runs seat-login-preflight beside it before it creates or starts anything. U512: hcom-seat
        names the seats' API key file `<seats-root>/.state/anthropic/api-key` to every seat as
        REGIME_ANTHROPIC_KEY_FILE and runs `claude-keyed --check` on it (a tool it resolves like every other; the
        tests' fixture lever answers) after the preflight and before the seat's settings are written, for every role
        and in a dry run too (where it runs before the dry run prints): a refusal (exit 2) is the launch's refusal,
        naming the lever's line and the handout's step; a status that is neither 0 nor 2 is unreadable, a refusal too
        (standing order 21). U318, U498: on the claude-bridge route the preflight judges the worker group's claude.ai
        login under `.state/claude-worker` through `claude`, a tool hcom-seat resolves (this fake answers and no test
        runs the host's Claude Code), and the same key file with the same lever and the key's validity by one Models
        API call (the fixture's fake endpoint), on one line, naming the operator's step of each state that is not
        present, so the seat starts on a 200 alone (U512e: the key decides; a present login beside an absent key passes
        the preflight as the login route, until U513 retires it, and the launcher's own gate refuses); U190b: the rule
        holds on a local host too."""
        key = self.key_file
        handout = "handouts/anthropic-api-key-u510.md"
        shared = Path(self.seats, ".state/claude-worker")
        command = f"CLAUDE_CONFIG_DIR={shared} claude auth login"
        key_absent = f"absent (the key file {key} is absent; place the API key there (the U510 handout))"

        def launch(*extra_args, **extra):
            overrides = {
                "SSH_CONNECTION": "100.64.0.2 50000 100.64.0.3 22",
                "CLAUDE_CODE_OAUTH_TOKEN": None,
                "CLAUDE_CONFIG_DIR": None,
                **extra,
            }
            return self.seat("worker", "--seats-root", self.seats, *extra_args, **overrides)

        # The fixture's worker has no login route (`modelRoles: {}`), so the preflight has nothing to judge and the
        # launcher's own gate is the refusal, the one every role gets.
        absent = (
            f"hcom-seat: claude-keyed: refused: the key file {key} is absent; place the API key there (the U510"
            f" handout); place the API key at {key} by the U510 handout ({handout}, steps 2 and 3), then start the"
            " seat again\n"
        )
        # A dry run runs the check too and makes nothing, not even the seats root.
        run = launch("--dry-run", FAKE_CLAUDE_KEYED_STATUS="2")
        self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
        self.assertIn(absent, run.stderr)
        self.assertFalse(Path(self.seats).exists(), "the dry run makes no seats root")
        # A launch makes the key directory (0700, inside `.state`) so the operator's file has a place, and no more; the
        # preflight's "no route" line comes first (it runs before the gate), the gate's refusal is the last line.
        run = launch(FAKE_CLAUDE_KEYED_STATUS="2")
        self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
        self.assertTrue(run.stderr.startswith("seat-login-preflight: worker: no route ("), run.stderr)
        self.assertTrue(run.stderr.endswith("\n" + absent), run.stderr)
        self.assertEqual(self.calls_of("hcom"), [])
        self.assertFalse(Path(self.seats, "worker").exists())
        self.assertEqual(sorted(p.name for p in Path(self.seats).iterdir()), [".state"])
        self.assertEqual(sorted(p.name for p in Path(self.seats, ".state").iterdir()), ["anthropic"])
        self.assertTrue(key.parent.is_dir() and not key.parent.is_symlink(), key.parent)
        self.assertEqual(stat.S_IMODE(os.lstat(key.parent).st_mode), 0o700)
        self.assertEqual(sorted(p.name for p in key.parent.iterdir()), [])
        # The lever's own reason rides whole, whatever it is; a local host (no SSH session) refuses the same.
        run = launch(SSH_CONNECTION=None, FAKE_CLAUDE_KEYED_STATUS="2", FAKE_CLAUDE_KEYED_REASON=f"the key file {key} has mode 644; the key must be readable by this user alone (0600)")  # fmt: skip
        self.assertEqual(run.returncode, 2, run.stderr)
        self.assertTrue(
            run.stderr.endswith(
                f"\nhcom-seat: claude-keyed: refused: the key file {key} has mode 644; the key must be readable by this"
                f" user alone (0600); place the API key at {key} by the U510 handout ({handout}, steps 2 and 3), then"
                " start the seat again\n"
            ),
            run.stderr,
        )
        # A check that exits neither 0 nor 2 is unreadable, never a pass.
        run = launch(FAKE_CLAUDE_KEYED_STATUS="5")
        self.assertEqual(run.returncode, 2, run.stderr)
        self.assertTrue(
            run.stderr.endswith(
                f"\nhcom-seat: cannot judge the API key file {key}: claude-keyed --check exited 5 (unreadable:"
                " claude-keyed: refused: cannot read the mode and owner of the key file (stat failed)); the launch is"
                " refused\n"
            ),
            run.stderr,
        )
        self.assertEqual(self.calls_of("hcom"), [])
        self.assertEqual((self.tools / "claude-keyed").resolve(), (self.bindir / "claude-keyed").resolve())
        self.assertEqual((self.tools / "claude").resolve(), (self.bindir / "claude").resolve())
        self.assertEqual(self.claude_keyed_calls.read_text(), f"--check REGIME_ANTHROPIC_KEY_FILE={key}\n" * 4)
        self.assertFalse(self.claude_calls.exists(), "no login route, so the preflight read no login")
        # On the claude-bridge route the preflight judges the group's login and the key file first, the key with the
        # same lever; a present login beside an absent key passes the preflight (U512e: the login route, until U513
        # retires it) with the line as information, followed by the key's placement commands as information (U512f),
        # and the launcher's own gate is the refusal.
        (self.profiles / "worker.yml").write_text("modelRoles:\n  default: claude-bridge/claude-opus-5-5\n")
        run = launch(FAKE_CLAUDE_KEYED_STATUS="2")
        self.assertEqual(run.returncode, 2, run.stderr)
        self.assertTrue(
            run.stderr.startswith(
                f"seat-login-preflight: worker claude-bridge: login present (claude.ai, {shared}); {key_absent}; place"
                " the key once: (umask 077; "
            ),
            run.stderr,
        )
        self.assertIn(
            "; the preflight passes on the group's login, but hcom-seat starts no seat until the key is placed; the key"
            " is the operator's step (handouts/anthropic-api-key-u510.md, steps 2 and 3): run those commands in your own"
            " terminal on this host\nhcom-seat: ",
            run.stderr,
        )
        self.assertTrue(run.stderr.endswith("\n" + absent), run.stderr)
        self.assertEqual(self.calls_of("hcom"), [])
        self.assertFalse(Path(self.seats, "worker").exists())
        # The preflight made the group's directory (0700) for the operator's login; the launch made nothing else but
        # the key directory of the earlier launches.
        self.assertTrue(shared.is_dir() and not shared.is_symlink(), shared)
        self.assertEqual(stat.S_IMODE(os.lstat(shared).st_mode), 0o700)
        self.assertEqual(sorted(p.name for p in Path(self.seats).iterdir()), [".state"])
        self.assertEqual(sorted(p.name for p in Path(self.seats, ".state").iterdir()), ["anthropic", "claude-worker"])
        # An absent login beside the absent key names both steps, the login's first; a local host (no SSH session)
        # refuses the same, and the command has no BROWSER prefix there (U190b: the child logs in by the group
        # directory's login wherever it runs).
        run = launch(FAKE_CLAUDE_AUTH_STATUS="1", FAKE_CLAUDE_KEYED_STATUS="2")
        self.assertEqual(run.returncode, 2, run.stderr)
        self.assertIn(
            f"worker claude-bridge: absent (not logged in under {shared}); {key_absent}; log in once:"
            f" BROWSER=regime-open-url {command}; place the key once: ",
            run.stderr,
        )
        self.assertIn(
            "; the login and the key are the operator's steps (handouts/anthropic-api-key-u510.md, steps 2 and 3, for"
            " the key): run those commands in your own terminal on this host, then start the seat again",
            run.stderr,
        )
        run = launch(SSH_CONNECTION=None, FAKE_CLAUDE_AUTH_STATUS="1", FAKE_CLAUDE_KEYED_STATUS="2")
        self.assertEqual(run.returncode, 2, run.stderr)
        self.assertIn(f"; log in once: {command}; place the key once: ", run.stderr)
        # With the key placed and accepted, the key decides (U512e): a token or key login under the directory is
        # information, and the seat starts on the key alone; the pass names the group's login command as information
        # (U512f) and the launch proceeds.
        self.place_key()
        run = launch(
            "--name",
            "worker-keyed",
            FAKE_CLAUDE_AUTH_METHOD="oauth_token",
            REGIME_ANTHROPIC_MODELS_URL=self.models_api(200),
        )
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertIn(
            f"seat-login-preflight: worker claude-bridge: absent (authMethod oauth_token under {shared}, not claude.ai);"
            f" key ok ({key}); log in once: BROWSER=regime-open-url {command}; the seat starts on the accepted key"
            " (U512e), so the login is information: run that command in your own terminal on this host to add the"
            " group's login\n",
            run.stderr,
        )
        self.assertEqual(len(self.calls_of("hcom")), 1)
        # A placed key the Models API rejects (401) beside an absent login: both steps, the login's first.
        run = launch(FAKE_CLAUDE_AUTH_STATUS="1", REGIME_ANTHROPIC_MODELS_URL=self.models_api(401))
        self.assertEqual(run.returncode, 2, run.stderr)
        self.assertIn(
            f"worker claude-bridge: absent (not logged in under {shared}); key rejected ({key}; HTTP 401); log in once:"
            f" BROWSER=regime-open-url {command}; place the key once: ",
            run.stderr,
        )
        self.assertEqual(len(self.calls_of("hcom")), 1)
        self.assertEqual(self.models_requests, [{"path": "/v1/models?limit=1", "x-api-key": FAKE_KEY, "anthropic-version": "2023-06-01"}])  # fmt: skip
        # Every login call ran under the group's directory and without a token name: one per launch on the route,
        # through the fake alone.
        self.assertEqual(self.claude_calls.read_text(), f"auth status {shared} token=unset\n" * 5)
        # The claude.ai login under the directory and a key the Models API accepts are what the seat can use; the
        # key's bytes reach no line.
        run = launch(REGIME_ANTHROPIC_MODELS_URL=self.models_api(200))
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertIn(
            f"seat-login-preflight: worker claude-bridge: login present (claude.ai, {shared}); key ok ({key})\n",
            run.stderr,
        )
        self.assertEqual(len(self.calls_of("hcom")), 2)
        self.assertNotIn(FAKE_KEY, run.stdout + run.stderr + self.claude_keyed_calls.read_text() + self.claude_calls.read_text())  # fmt: skip
        # The dry run's environment line and the shim carry the file and the group's directory; the launch's omp saw
        # them exported.
        run = launch("--dry-run")
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertIn(
            f" REGIME_STORE_ROOT={self.home.resolve()}/.local/state/regime-store/repo REGIME_ANTHROPIC_KEY_FILE={key}"
            f" CLAUDE_CONFIG_DIR={shared} (login group worker)\n",
            run.stderr,
        )
        shim = Path(self.seats, ".sandbox/worker/bin/omp").read_text()
        self.assertIn(f"key_file={key}", shim)
        self.assertIn("\nexport REGIME_ANTHROPIC_KEY_FILE=${key_file}\n", shim)

    def test_a_link_at_the_key_path_refuses_before_anything_resolves_or_exports_it(self):
        """U512b (verdict U512-2a49d363, P2 at hcom-seat:2416): `physical_path` resolved the key path before the form
        check, so a checker that refuses links never saw the link, and the dry run exported the link's target. The
        lever now judges the contract path's form first (its own link refusal, before `claude-keyed --check` and
        before any resolve): a link at `<seats-root>/.state/anthropic/api-key` refuses (exit 2) the dry run and the
        launch, prints no environment line, calls no checker, follows the link to nothing and leaves it in place."""
        key = self.key_file
        elsewhere = self.home / "elsewhere-key"
        elsewhere.write_text(FAKE_KEY + "\n")
        elsewhere.chmod(0o600)
        key.parent.mkdir(parents=True)
        for directory in (Path(self.seats), Path(self.seats, ".state"), key.parent):
            directory.chmod(0o700)
        key.symlink_to(elsewhere)
        refusal = (
            f"hcom-seat: the API key file {key} is a symbolic link; the seats' key file must be a regular file of this"
            " user, placed by the U510 handout (handouts/anthropic-api-key-u510.md, steps 2 and 3)\n"
        )
        for extra in (["--dry-run"], []):
            with self.subTest(extra=extra):
                run = self.seat("worker", "--seats-root", self.seats, *extra, SSH_CONNECTION="100.64.0.2 50000 100.64.0.3 22")  # fmt: skip
                self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
                self.assertTrue(run.stderr.endswith(refusal), run.stderr)
                self.assertNotIn("REGIME_ANTHROPIC_KEY_FILE=", run.stderr, "the dry run exports nothing")
                self.assertNotIn(str(elsewhere), run.stderr, "the target is never named: the link was not followed")
        self.assertFalse(self.claude_keyed_calls.exists(), "no checker ran on the link or its target")
        self.assertEqual(self.calls_of("omp"), [])
        self.assertTrue(key.is_symlink(), "the launch neither removed nor replaced the link")
        self.assertEqual(elsewhere.read_text(), FAKE_KEY + "\n")
        self.assertNotIn(FAKE_KEY, run.stdout + run.stderr)

    def test_a_preflight_component_refusal_stops_the_launch_with_exit_2(self):
        """U318c: hcom-seat runs seat-login-preflight with `|| exit $?`, so a component refusal of the shared Claude
        Code directory chain (exit 2, the component named) is the launch's refusal, status and text unchanged, before
        anything is made or started. The one component shape the launcher's own checks let through to the preflight
        is a seats root that is a directory of another user: a link or a file at `.state`, and a root this user cannot
        search, are refused by `own_slots_check` or `physical_path` first with the launcher's own line, and a trailing
        `//` never reaches it, since the launcher passes the physical root. A dry run exits before the preflight, so
        the launches here run against the fake hcom, which records every call."""
        if os.geteuid() == 0:
            self.skipTest("root owns every directory, so none is another user's")
        (self.profiles / "worker.yml").write_text("modelRoles:\n  default: claude-bridge/claude-opus-5-5\n")
        candidates = ("/var/empty", "/usr/share/misc", "/usr/share/zoneinfo")
        other = next((Path(c) for c in candidates if Path(c).is_dir() and Path(c).stat().st_uid != os.geteuid()), None)
        if other is None:
            self.skipTest(f"no directory of another user among {candidates}")
        real = Path(os.path.realpath(other))
        run = self.seat("worker", "--seats-root", str(other))
        line = (
            f"seat-login-preflight: refused: the login group's Claude Code directory path component {real} is a"
            " directory of another user; move it aside before a seat starts\n"
        )
        self.assertEqual((run.returncode, run.stdout, run.stderr), (2, "", line))
        self.assertEqual(self.calls_of("hcom"), [], "no seat started")
        self.assertFalse(self.claude_calls.exists(), "the chain refused before the one status call")
        self.assertFalse((real / ".state").exists() or (real / ".sandbox").exists(), "nothing made")
        # The preflight run directly, with the root the launcher hands it, gives the same status and text.
        direct = subprocess.run(
            [str(SEAT.parent / "seat-login-preflight"), "worker"], cwd=self.repo,
            env={**self.env, "REGIME_SEATS_ROOT": str(real)}, capture_output=True, text=True, check=False,
        )  # fmt: skip
        self.assertEqual((direct.returncode, direct.stdout, direct.stderr), (run.returncode, run.stdout, run.stderr))
        # A planted link at `.state` under the fixture's seats root stops the launch with exit 2 as well, by the
        # launcher's own slot check before the preflight runs, in a dry run too; the link is kept and nothing is made.
        seats = Path(self.seats)
        seats.mkdir()
        elsewhere = self.home / "elsewhere"
        elsewhere.mkdir()
        (seats / ".state").symlink_to(elsewhere)
        for extra in ([], ["--dry-run"]):
            with self.subTest(extra=extra):
                run = self.seat("worker", "--seats-root", self.seats, *extra)
                self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
                self.assertIn(f"hcom-seat: the seat slot {seats}/.state is a symbolic link", run.stderr)
        self.assertEqual(self.calls_of("hcom"), [])
        self.assertFalse(self.claude_calls.exists())
        self.assertTrue((seats / ".state").is_symlink())
        self.assertEqual(sorted(p.name for p in elsewhere.iterdir()), [])
        self.assertEqual(sorted(p.name for p in seats.iterdir()), [".state"])

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
        # U512: the launch made the seats' API key directory before the gate ran, and nothing else of the seat.
        self.assertEqual(sorted(p.name for p in Path(self.seats).iterdir()), [".state"])
        self.assertEqual(sorted(p.name for p in Path(self.seats, ".state").iterdir()), ["anthropic"])

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
        self.assertIn(
            "unknown role 'audit'; expected orchestrator, worker, dsh or router", self.seat("audit", "--dry-run").stderr
        )
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

    def plant_claude_env_recorder(self):
        """Replace the omp fake with one that records the Claude variables the shim handed it (the shared fake keeps
        HCOM_* only); the record is a file under the scratch tree, never a stream the launch prints."""
        record = self.calls / "omp-claude-env"
        (self.bindir / "omp").write_text(
            "#!/bin/sh\n"
            "printf 'CLAUDE_CONFIG_DIR=%s\\nCLAUDE_CODE_OAUTH_TOKEN=%s\\nREGIME_ANTHROPIC_KEY_FILE=%s\\n'"
            ' "${CLAUDE_CONFIG_DIR-unset}" "${CLAUDE_CODE_OAUTH_TOKEN-unset}" "${REGIME_ANTHROPIC_KEY_FILE-unset}"'
            f" >> {shlex.quote(str(record))}\n"
        )
        return record

    def claude_env_of(self, record):
        """The last omp run's record as a dict."""
        lines = record.read_text().splitlines()
        return dict(line.split("=", 1) for line in lines[-3:])

    def test_omp_runs_under_srt_behind_a_canary_with_the_seat_roots(self):
        """U85: hcom pins the per-seat shim, which proves the sandbox with a canary and then runs omp under srt."""
        run = self.seat("worker", "--seats-root", self.seats)
        self.assertEqual(run.returncode, 0, run.stderr)
        shim = Path(self.seats, ".sandbox/worker/bin/omp")
        settings = Path(self.seats, ".sandbox/worker/srt-settings.json")
        # The version read (U141) comes first, before the seat's shim directory exists.
        version, canary, launch = self.calls_of("srt")
        self.assertEqual(version["argv"], ["--version"])
        self.assertEqual(canary["argv"][:5], ["--settings", str(settings), "--", "/bin/sh", "-c"])
        self.assertEqual(
            canary["argv"][-4:-1], [str(shim.parent.parent / "canary"), str(settings), str(self.home / ".ssh")]
        )
        # U190b: the fourth probe opens a file under the operator's ~/.claude/debug, srt 0.0.81's implicit grant.
        self.assertRegex(canary["argv"][-1], rf"^{re.escape(str(self.home / '.claude/debug/hcom-seat-canary-'))}\d+$")
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
        # U189: the package the checkout's Claude Code hooks import, beside the hooks, for the clone and the checkout.
        self.assertIn(str(Path(self.seats, "worker") / ".claude/contextdb"), worker["filesystem"]["denyWrite"])
        self.assertIn(str((self.repo / ".claude/contextdb").resolve()), worker["filesystem"]["denyWrite"])
        self.assertEqual(worker["network"]["allowUnixSockets"], [])
        self.assertNotIn("example.com", worker["network"]["allowedDomains"])
        # srt 0.0.81 grants local binding on every interface, so no seat gets it (U85 round 3).
        self.assertIs(worker["network"]["allowLocalBinding"], False)
        # U190: the operator's Claude Code state is no write root of either role, and nothing under ~/.claude is;
        # the bridge child's state lives in the seat's own slot, a real 0700 directory the launch creates.
        home = self.home.resolve()
        for path in (str(home / ".claude.json"), str(home / ".claude")):
            self.assertNotIn(path, write)
        self.assertEqual([entry for entry in write if entry.startswith(str(home / ".claude"))], [])
        # U190b: being no root is not enough (srt grants ~/.claude/debug of the real HOME on its own), so the operator's
        # Claude Code state is denied explicitly, for write and for read.
        self.assert_operator_claude_denied(worker)
        # U318, U498: the bridge child's state lives in its login group's Claude Code directory, a real 0700 directory
        # the launch creates inside `.state`; no per-seat directory exists any more.
        state_claude = Path(self.seats, ".state/claude-worker")
        self.assertTrue(state_claude.is_dir() and not state_claude.is_symlink(), state_claude)
        self.assertEqual(stat.S_IMODE(os.lstat(state_claude).st_mode), 0o700)
        self.assertFalse(Path(self.seats, ".state/worker/claude").exists())
        self.assertIn(str(Path(self.seats, ".state/worker")), write)
        # A caller's CLAUDE_CONFIG_DIR is no root either, and the shim hands omp the group's directory.
        caller_config = self.home / "claude-config"
        caller_config.mkdir()
        record = self.plant_claude_env_recorder()
        run = self.seat("worker", "--seats-root", self.seats, CLAUDE_CONFIG_DIR=str(caller_config))
        self.assertEqual(run.returncode, 0, run.stderr)
        worker = self.settings_of("worker")
        write = worker["filesystem"]["allowWrite"]
        self.assertNotIn(str(caller_config), write)
        self.assert_operator_claude_denied(worker, str(caller_config))
        self.assertEqual(self.claude_env_of(record)["CLAUDE_CONFIG_DIR"], str(state_claude.resolve()))
        # A caller whose CLAUDE_CONFIG_DIR is ~/.claude itself adds no third entry.
        run = self.seat("worker", "--seats-root", self.seats, CLAUDE_CONFIG_DIR=str(home / ".claude"))
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assert_operator_claude_denied(self.settings_of("worker"))
        run = self.seat("orchestrator", "--seats-root", self.seats, CLAUDE_CONFIG_DIR=str(caller_config))
        self.assertEqual(run.returncode, 0, run.stderr)
        orchestrator = self.settings_of("orchestrator")
        for path in (str(home / ".claude.json"), str(home / ".claude"), str(caller_config)):
            self.assertNotIn(path, orchestrator["filesystem"]["allowWrite"])
        self.assertEqual(
            [entry for entry in orchestrator["filesystem"]["allowWrite"] if entry.startswith(str(home / ".claude"))], []
        )
        self.assert_operator_claude_denied(orchestrator, str(caller_config))
        self.assertEqual(
            self.claude_env_of(record)["CLAUDE_CONFIG_DIR"],
            str(Path(self.seats, ".state/claude-orchestrator").resolve()),
        )
        shutil.copy(FAKE, self.bindir / "omp")
        run = self.seat("orchestrator", "--seats-root", self.seats)
        self.assertEqual(run.returncode, 0, run.stderr)
        orchestrator = self.settings_of("orchestrator")
        # The orchestrator launches no seat (U85 round 2): no herdr socket, no write to the seats root or a sandbox.
        self.assertEqual(orchestrator["network"]["allowUnixSockets"], [])
        self.assertNotIn(self.seats, orchestrator["filesystem"]["allowWrite"])
        self.assertIn(str(self.repo.resolve()), orchestrator["filesystem"]["allowWrite"])
        self.assertIn(str(Path(self.seats, ".sandbox")), orchestrator["filesystem"]["denyWrite"])
        self.assertIn(str(Path(self.seats, ".sandbox")), orchestrator["filesystem"]["denyRead"])
        self.assertIn(str((self.repo / ".claude/contextdb").resolve()), orchestrator["filesystem"]["denyWrite"])
        self.assert_operator_claude_denied(orchestrator)

    def assert_operator_claude_denied(self, settings, *extra):
        """Both deny lists carry `~/.claude`, `~/.claude.json` and the given caller directory, once each."""
        home = self.home.resolve()
        expected = [str(home / ".claude"), str(home / ".claude.json"), *extra]
        for key in ("denyWrite", "denyRead"):
            listed = settings["filesystem"][key]
            for path in expected:
                self.assertEqual(listed.count(path), 1, (key, path, listed))
            self.assertEqual([entry for entry in listed if entry.startswith(str(home / ".claude"))], expected[:2])

    def test_the_shim_exports_the_groups_directory_and_the_key_file_and_clears_a_callers_token(self):
        """U318, U498: the bridge child logs in by its login group's claude.ai login, which Claude Code stores and
        refreshes there; the shim exports that directory. U512: its key is the one file
        `<seats-root>/.state/anthropic/api-key`, exported as REGIME_ANTHROPIC_KEY_FILE for `claude-keyed` to read, and
        no token. U312: a CLAUDE_CODE_OAUTH_TOKEN in the caller's environment is no input, at a launch whose preflight
        found the login and the key and when the shim runs directly."""
        (self.profiles / "worker.yml").write_text("modelRoles:\n  default: claude-bridge/claude-opus-5-5\n")
        record = self.plant_claude_env_recorder()
        caller = "fake-" + "caller-value-u190"
        key = str(self.place_key())
        url = self.models_api(200)
        run = self.seat("worker", "--seats-root", self.seats, CLAUDE_CODE_OAUTH_TOKEN=caller, REGIME_ANTHROPIC_MODELS_URL=url)  # fmt: skip
        self.assertEqual(run.returncode, 0, run.stderr)
        shared = str(Path(self.seats, ".state/claude-worker"))
        self.assertIn(f"worker claude-bridge: login present (claude.ai, {shared}); key ok ({key})", run.stderr)
        expected = {"CLAUDE_CONFIG_DIR": shared, "CLAUDE_CODE_OAUTH_TOKEN": "unset", "REGIME_ANTHROPIC_KEY_FILE": key}
        self.assertEqual(self.claude_env_of(record), expected)
        # The preflight's one login call ran under the group's directory and without the caller's token name; its
        # key judge and the launcher's gate each ran the lever on the file.
        self.assertEqual(self.claude_calls.read_text(), f"auth status {shared} token=unset\n")
        self.assertEqual(self.claude_keyed_calls.read_text(), f"--check REGIME_ANTHROPIC_KEY_FILE={key}\n" * 2)
        shim = Path(self.seats, ".sandbox/worker/bin/omp")
        env = {**self.env, "CLAUDE_CODE_OAUTH_TOKEN": caller}
        direct = subprocess.run([str(shim), "--version"], env=env, capture_output=True, text=True, check=False)
        self.assertEqual(direct.returncode, 0, direct.stderr)
        self.assertEqual(self.claude_env_of(record), expected)
        for text in (run.stdout, run.stderr, direct.stdout, direct.stderr, shim.read_text()):
            self.assertNotIn(caller, text)
            self.assertNotIn(FAKE_KEY, text)
        self.assertNotIn("oauth-token", shim.read_text(), "the shim reads no token file")

    def test_a_read_grant_that_is_a_regular_file_under_a_read_deny_refuses_the_launch(self):
        """U512i (verdict U512h-4c5ec14e P1 `hcom-seat:2817`, class sandbox-mount-mode): srt 0.0.81's Linux backend
        mounts a tmpfs over a read-denied directory and binds each allowed path back into it, making a bound file's
        parents inside the tmpfs with bwrap's default mode, so a read grant of a regular file under a read deny loses
        the file's directory mode inside the sandbox (the key file granted alone under the seats-root deny, rounds 1
        to 5, left `.state/anthropic` 0755 there, and `claude-keyed`, which holds it to 0700, refused the key the
        host's preflight had passed). `allow_read_files_check` refuses, after the rows are rendered and before the
        settings file is written, any role whose allowRead holds a regular file at or under a denyRead row, naming
        both paths and the reason. Through the fixture: the worker's records row `<checkout>/.orchestration/orchestrate`
        lies under its checkout deny, so a regular file planted there refuses the worker's launch (exit 2, the line,
        no settings file, no hcom), while the orchestrator, whose checkout is no deny of its own, launches with the
        same file in place and renders no such row; a directory there launches the worker too. The key directory
        grant of every role (U512i) passes the same check at every launch (the per-role assertions beside it)."""
        self.place_key()
        checkout = self.repo.resolve()
        records = checkout / ".orchestration/orchestrate"
        records.parent.mkdir(parents=True, exist_ok=True)
        records.write_text("")
        run = self.seat("worker", "--seats-root", self.seats)
        self.assertEqual(run.returncode, 2, run.stderr)
        self.assertIn(
            f"hcom-seat: the allowRead row {records} is a regular file under the denyRead row {checkout}: a file-only"
            " read grant under a read-denied directory loses its parent's mode inside srt's Linux sandbox (the file is"
            " bound back into a tmpfs whose directories are made 0755, verdict U512h-4c5ec14e), so a judge of that mode"
            " cannot pass there; grant the file's directory instead\n",
            run.stderr,
        )
        self.assertFalse(Path(self.seats, ".sandbox/worker/srt-settings.json").exists(), "no settings file written")
        self.assertEqual(self.calls_of("hcom"), [], "nothing started")
        run = self.seat("orchestrator", "--seats-root", self.seats)
        self.assertEqual(run.returncode, 0, run.stderr)
        fs = self.settings_of("orchestrator")["filesystem"]
        self.assertIn(str(records), fs["allowRead"])
        self.assertNotIn(str(checkout), fs["denyRead"])
        self.assertEqual(file_rows_under_read_denies(fs), [])
        records.unlink()
        records.mkdir()
        run = self.seat("worker", "--seats-root", self.seats)
        self.assertEqual(run.returncode, 0, run.stderr)
        fs = self.settings_of("worker")["filesystem"]
        self.assertIn(str(records), fs["allowRead"])
        self.assertIn(str(checkout), fs["denyRead"])
        self.assertEqual(file_rows_under_read_denies(fs), [])
        self.assertEqual(len(self.calls_of("hcom")), 2)

    def test_a_callers_token_reaches_no_child_of_the_launcher(self):
        """Codex P2 on PR 712 (review comment 4498955210, `hcom-seat:2210`, a residual on U318): the U312 head cleared
        CLAUDE_CODE_OAUTH_TOKEN inside the generated shim alone, so hcom, herdr and the shim's srt canary inherited a
        caller's variable before the shim's unset. The launcher clears the name before its first child process: an
        hcom spawned by a launcher invoked with the variable set sees it unset, and so does the key judge."""
        (self.profiles / "worker.yml").write_text("modelRoles:\n  default: claude-bridge/claude-opus-5-5\n")
        caller = "fake-" + "caller-value-u318"
        record = self.calls / "hcom-claude-env"
        (self.bindir / "hcom").write_text(
            "#!/bin/sh\n"
            f"printf 'CLAUDE_CODE_OAUTH_TOKEN=%s\\n' \"${{CLAUDE_CODE_OAUTH_TOKEN-unset}}\" >> {shlex.quote(str(record))}\n"
        )
        key = str(self.place_key())
        url = self.models_api(200)
        run = self.seat("worker", "--seats-root", self.seats, CLAUDE_CODE_OAUTH_TOKEN=caller, REGIME_ANTHROPIC_MODELS_URL=url)  # fmt: skip
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual(record.read_text(), "CLAUDE_CODE_OAUTH_TOKEN=unset\n")
        shared = str(Path(self.seats, ".state/claude-worker"))
        self.assertEqual(self.claude_calls.read_text(), f"auth status {shared} token=unset\n")
        self.assertEqual(self.claude_keyed_calls.read_text(), f"--check REGIME_ANTHROPIC_KEY_FILE={key}\n" * 2)
        self.assertNotIn(caller, run.stdout + run.stderr)
        self.assertNotIn(FAKE_KEY, run.stdout + run.stderr)

    def test_every_role_gets_its_login_groups_claude_code_directory_whose_configuration_no_seat_can_change(self):
        """U498 (one login per seat group, replacing U318's one directory per seats root): the bridge child of a seat
        runs under its login group's `CLAUDE_CONFIG_DIR`, `<seats-root>/.state/claude-<group>` (worker to `worker`,
        orchestrator to `orchestrator`, from the one table), a real 0700 directory the launch makes; it is write row 2
        and a read root of the role's settings, and its settings, rules, hooks, plugins, skills, commands and agents are
        write-denied, so no seat changes what another seat's child loads from it. The legacy shared directory
        `.state/claude` is made and granted by no launch (the kit does not read or copy a login, order 54) and, since
        U498c, denied for read by every one, like every other group's directory. U512: the key file
        `<seats-root>/.state/anthropic/api-key` is write-denied to every role, so no seat rewrites the key, and its
        directory `.state/anthropic`, a 0700 slot the launch makes, is a read root of every role beside the group's
        directory (U512i, verdict U512h-4c5ec14e: the directory, not the file, since a file-only read grant under the
        read-denied seats root loses its parent's mode inside srt's Linux tmpfs, where `claude-keyed` holds the
        directory to 0700; a directory bind keeps its mode); the file itself stands in no grant list, nothing else under
        the directory is granted, and no allowRead row of either role is a regular file under a denyRead row. A
        linked group directory, or a linked key directory, refuses before anything is made, and no seat may take a
        `claude-*` name, `claude` or `anthropic`."""
        key = self.place_key()
        record = self.plant_claude_env_recorder()
        legacy = Path(self.seats, ".state/claude")
        for role in ("worker", "orchestrator"):
            with self.subTest(role=role):
                group_dir = Path(self.seats, f".state/claude-{role}")
                run = self.seat(role, "--seats-root", self.seats)
                self.assertEqual(run.returncode, 0, run.stderr)
                self.assertTrue(group_dir.is_dir() and not group_dir.is_symlink(), group_dir)
                self.assertEqual(stat.S_IMODE(os.lstat(group_dir).st_mode), 0o700)
                self.assertTrue(key.parent.is_dir() and not key.parent.is_symlink(), key.parent)
                self.assertEqual(stat.S_IMODE(os.lstat(key.parent).st_mode), 0o700)
                fs = self.settings_of(role)["filesystem"]
                self.assertEqual(fs["allowWrite"][2], str(group_dir), "row 2 of every role's write roots")
                for kind in ("allowWrite", "allowRead"):
                    self.assertEqual(fs[kind].count(str(group_dir)), 1, (kind, fs[kind]))
                self.assertEqual(fs["allowRead"][fs["allowRead"].index(str(group_dir)) + 1], str(key.parent), "the key directory beside the group's directory (U512i)")  # fmt: skip
                self.assertEqual((fs["allowRead"].count(str(key.parent)), fs["denyWrite"].count(str(key))), (1, 1), fs)
                self.assertNotIn(str(key), fs["allowRead"] + fs["allowWrite"] + fs["denyRead"], "the file is in no list but denyWrite")  # fmt: skip
                self.assertNotIn(str(key.parent), fs["allowWrite"] + fs["denyRead"] + fs["denyWrite"])
                self.assertEqual([row for row in fs["allowWrite"] + fs["allowRead"] if row.startswith(f"{key.parent}/")], [], "nothing under the key directory is granted")  # fmt: skip
                self.assertTrue(key.is_file() and not key.is_symlink(), key)
                self.assertEqual(file_rows_under_read_denies(fs), [], f"a {role} allowRead row is a regular file under a denyRead row (U512i)")  # fmt: skip
                denied = [f"{group_dir}/{name}" for name in SHARED_CLAUDE_DENIES]
                self.assertEqual([row for row in fs["denyWrite"] if row.startswith(f"{group_dir}/")], denied)
                self.assertEqual([row for row in fs["denyRead"] if row.startswith(str(group_dir))], [])
                for kind in ("allowWrite", "allowRead", "denyWrite"):
                    self.assertEqual(
                        [row for row in fs[kind] if row == str(legacy) or row.startswith(f"{legacy}/")], [], kind
                    )
                # U498c: the legacy directory is denied for read by name, once, and granted by nothing.
                self.assertEqual(
                    [row for row in fs["denyRead"] if row == str(legacy) or row.startswith(f"{legacy}/")], [str(legacy)]
                )
                env = self.claude_env_of(record)
                self.assertEqual(env, {"CLAUDE_CONFIG_DIR": str(group_dir), "CLAUDE_CODE_OAUTH_TOKEN": "unset", "REGIME_ANTHROPIC_KEY_FILE": str(key)})  # fmt: skip
                self.assertFalse(Path(self.seats, ".state", role, "claude").exists(), "no per-seat directory")
        self.assertFalse(legacy.exists() or legacy.is_symlink(), "the legacy shared directory is not made")
        # Two groups, two directories: a worker's child and an orchestrator's child rotate no refresh token together.
        self.assertNotEqual(
            self.settings_of("worker")["filesystem"]["allowWrite"][2],
            self.settings_of("orchestrator")["filesystem"]["allowWrite"][2],
        )
        # A linked group directory refuses (exit 2) before anything starts; so does a login directory's name as a seat's,
        # and the key directory's.
        group_dir = Path(self.seats, ".state/claude-worker")
        shutil.rmtree(group_dir)
        elsewhere = self.home / "elsewhere"
        elsewhere.mkdir()
        group_dir.symlink_to(elsewhere)
        launches = len(record.read_text().splitlines())
        run = self.seat("worker", "--seats-root", self.seats)
        self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
        self.assertIn(f"the login group directory {group_dir} is a symbolic link", run.stderr)
        for name in ("claude-worker", "claude-router", "claude-x", "claude"):
            with self.subTest(name=name):
                run = self.seat("worker", "--name", name, "--seats-root", self.seats, "--dry-run")
                self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
                self.assertIn(f"the seat name '{name}' is taken by the Claude Code login directories", run.stderr)
        run = self.seat("worker", "--name", "anthropic", "--seats-root", self.seats, "--dry-run")
        self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
        self.assertIn("the seat name 'anthropic' is taken by the seats' API key directory", run.stderr)
        self.assertTrue(group_dir.is_symlink(), "the launch neither removed nor replaced the link")
        # A linked key directory (U512) refuses the same, in a dry run too, with the link kept and nothing made.
        group_dir.unlink()
        group_dir.mkdir(0o700)
        shutil.rmtree(key.parent)
        key.parent.symlink_to(elsewhere)
        for extra in ([], ["--dry-run"]):
            with self.subTest(extra=extra):
                run = self.seat("worker", "--seats-root", self.seats, *extra)
                self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
                self.assertIn(f"the seat slot {key.parent} is a symbolic link", run.stderr)
        self.assertEqual(len(record.read_text().splitlines()), launches, "no omp ran")
        self.assertTrue(key.parent.is_symlink(), "the launch neither removed nor replaced the link")
        self.assertEqual(sorted(p.name for p in elsewhere.iterdir()), [])

    def test_the_login_group_table_is_one_text_in_both_levers(self):
        """U498: the login group of a role is one table, `login_group_of_role`, held as the same text by hcom-seat and
        seat-login-preflight (copied, each lever's tests asserting it): worker to worker, orchestrator to orchestrator,
        audit to audit, dsh to router and router to router (the dsh gateway child is the Router's); any other name
        fails (status 1) and prints nothing, so a caller's unread status is the lever's refusal, never a directory."""
        tables = {}
        for lever in (SEAT, SEAT.parent / "seat-login-preflight"):
            text = lever.read_text()
            start = text.index("login_group_of_role() {")
            tables[lever.name] = text[start : text.index("\n}\n", start) + 3]
        self.assertEqual(tables["hcom-seat"], tables["seat-login-preflight"])
        table = tables["hcom-seat"]
        script = f'set -euo pipefail\n{table}\nlogin_group_of_role "$1"\n'
        roles = (
            ("worker", "worker"), ("orchestrator", "orchestrator"), ("audit", "audit"), ("dsh", "router"), ("router", "router"),
        )  # fmt: skip
        for role, group in roles:
            with self.subTest(role=role):
                run = subprocess.run(["bash", "-c", script, "_", role], capture_output=True, text=True, check=False)
                self.assertEqual((run.returncode, run.stdout, run.stderr), (0, f"{group}\n", ""))
        for role in ("claude", "Worker", "worker ", "", "review"):
            with self.subTest(role=role):
                run = subprocess.run(["bash", "-c", script, "_", role], capture_output=True, text=True, check=False)
                self.assertEqual((run.returncode, run.stdout), (1, ""), run.stderr)
        # U498c: the table's range, the array `LOGIN_GROUPS` beside the table in hcom-seat (the login directories every
        # seat denies for read but its own group's), is the set of groups the table gives its roles, each once, in the
        # table's order, so a group the table gains is denied without a second list diverging from it.
        (array,) = [line for line in SEAT.read_text().splitlines() if line.startswith("LOGIN_GROUPS=(")]
        run = subprocess.run(
            ["bash", "-c", f'set -euo pipefail\n{array}\nprintf "%s\\n" "${{LOGIN_GROUPS[@]}}"\n'],
            capture_output=True, text=True, check=False,
        )  # fmt: skip
        self.assertEqual((run.returncode, run.stderr), (0, ""), run.stderr)
        table_range = list(dict.fromkeys(group for _, group in roles))
        self.assertEqual(run.stdout.split("\n")[:-1], table_range)
        self.assertEqual(run.stdout.split("\n")[:-1], list(LOGIN_GROUPS))

    def test_every_seat_is_denied_the_other_login_groups_directories_and_the_legacy_one(self):
        """U498c (verdict U498-4d18d6dd P1 `hcom-seat:2062`; the finding's site is the orchestrator's allowRead of the
        whole seats root): srt reopens a root's subtree under an allow but for a more specific deny, so until this head
        a seat whose settings allowed the seats root for read, the orchestrator, could read another group's login
        directory (`.state/claude-worker`, with its `.credentials.json` on Linux). Every role's settings carry one
        denyRead row per login directory that is not its own group's: the other groups' `.state/claude-<group>` in the
        table's order (LOGIN_GROUPS, the range of `login_group_of_role`) and the legacy `.state/claude`, each once,
        under the physical seats root, with no grant and no other deny at or under any of them; the own group's
        directory stays allowed for read and write and stands in no deny list. The orchestrator keeps its read grant
        of the seats root, and the worker group's login is denied under it."""
        seats = str(Path(self.seats).resolve())
        for role in ("worker", "orchestrator"):
            with self.subTest(role=role):
                run = self.seat(role, "--seats-root", self.seats)
                self.assertEqual(run.returncode, 0, run.stderr)
                fs = self.settings_of(role)["filesystem"]
                own = f"{seats}/.state/claude-{role}"
                denied = login_read_denies(seats, role)
                self.assertEqual([row for row in fs["denyRead"] if row.startswith(f"{seats}/.state/claude")], denied)
                for row in denied:
                    self.assertEqual(fs["denyRead"].count(row), 1, (row, fs["denyRead"]))
                    for key in ("allowRead", "allowWrite", "denyWrite"):
                        self.assertEqual([r for r in fs[key] if r == row or r.startswith(f"{row}/")], [], (key, row))
                self.assertNotIn(own, denied)
                self.assertEqual((fs["allowRead"].count(own), fs["allowWrite"].count(own)), (1, 1))
                self.assertEqual([r for r in fs["denyRead"] if r == own or r.startswith(f"{own}/")], [])
                self.assertNotIn(own, fs["denyWrite"])
        orchestrator = self.settings_of("orchestrator")["filesystem"]
        self.assertIn(seats, orchestrator["allowRead"], "the verdict's grant: the orchestrator reads the seats root")
        self.assertIn(
            f"{seats}/.state/claude-worker", orchestrator["denyRead"], "the worker group's login, denied under it"
        )
        self.assertNotIn(f"{seats}/.state/claude-orchestrator", orchestrator["denyRead"], "its own group's login, kept")

    def test_a_dry_run_names_the_login_groups_directory_in_its_environment_line(self):
        """U498 ACCEPTANCE 1: `hcom-seat <role> --name probe --dry-run` prints on stderr the environment a launch
        exports, naming the role's login group directory as CLAUDE_CONFIG_DIR (`.state/claude-worker` for a worker,
        `.state/claude-orchestrator` for the orchestrator) and the group; the dry run makes no seats root."""
        for role in ("worker", "orchestrator"):
            with self.subTest(role=role):
                run = self.seat(role, "--name", "probe", "--seats-root", self.seats, "--dry-run")
                self.assertEqual(run.returncode, 0, run.stderr)
                (line,) = [row for row in run.stderr.splitlines() if row.startswith("hcom-seat: environment ")]
                self.assertIn(f"HCOM_DIR={self.store} ", line)
                self.assertTrue(
                    line.endswith(
                        f" CLAUDE_CONFIG_DIR={Path(self.seats, f'.state/claude-{role}')} (login group {role})"
                    ),
                    line,
                )
        self.assertFalse(Path(self.seats).exists(), "a dry run makes no seats root")

    def test_every_launch_makes_every_login_groups_directory_before_its_settings_file_so_each_deny_binds(self):
        """U498d (verdict U498-8f2cca8c P1 `hcom-seat:2713`; the mechanism-change row of 2026-11-12T15:05:20Z, form
        allowlist: the table's range made real). srt 0.0.81's Linux backend mounts nothing for a denyRead entry that
        is not there (`dist/sandbox/linux-sandbox-utils.js:1810-1812`), so until this head the orchestrator's U498c
        deny of `.state/claude-worker` bound nothing before the worker group's first launch or the operator's login
        made that directory, and its read grant of the seats root reached the credentials made later. Now every
        launch of every role makes every group's directory of the table's range (LOGIN_GROUPS), 0700, empty, this
        user's, before its settings file is written (login_dirs_make), so every login directory row of every role's
        denyRead names a directory that exists when srt reads the file; the legacy `.state/claude` is in no range and
        is made by nothing (standing order 54). A group directory planted as a symbolic link or a file, the own
        group's or another's, refuses the launch naming it, with nothing made and nothing started; a dry run makes
        nothing, as before."""
        seats = Path(self.seats).resolve()
        groups = [seats / f".state/claude-{group}" for group in LOGIN_GROUPS]
        legacy = seats / ".state/claude"
        run = self.seat("worker", "--name", "probe", "--seats-root", self.seats, "--dry-run")
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertFalse(seats.exists(), "a dry run makes no seats root and no login directory")
        # The omp fake reads the settings srt was started with (the shim's HCOM_SEAT_SANDBOX names the sandbox) and
        # records, for every denyRead row under the seats root, whether it is a real directory at that moment: on
        # Linux the deny binds only then.
        record = self.calls / "deny-rows-present"
        (self.bindir / "omp").write_text(
            "#!/usr/bin/env python3\n"
            "import json, os\n"
            "sandbox = os.environ['HCOM_SEAT_SANDBOX']\n"
            "fs = json.load(open(os.path.join(sandbox, 'srt-settings.json')))['filesystem']\n"
            f"seats = {str(seats)!r}\n"
            "rows = {row: os.path.isdir(row) and not os.path.islink(row) for row in fs['denyRead']"
            " if row.startswith(seats + '/')}\n"
            f"open({str(record)!r}, 'a').write(json.dumps(rows) + chr(10))\n"
        )
        for role in ("worker", "orchestrator"):
            with self.subTest(role=role):
                run = self.seat(role, "--seats-root", self.seats)
                self.assertEqual(run.returncode, 0, run.stderr)
                settings_file = Path(self.seats, ".sandbox", role, "srt-settings.json")
                for path in groups:
                    self.assertTrue(path.is_dir() and not path.is_symlink(), path)
                    self.assertEqual(stat.S_IMODE(os.lstat(path).st_mode), 0o700, path)
                    self.assertEqual(path.stat().st_uid, os.geteuid(), "a directory of this user")
                    self.assertEqual(list(path.iterdir()), [], "made empty: no login is made, read or copied")
                    self.assertLessEqual(
                        path.stat().st_mtime_ns, settings_file.stat().st_mtime_ns, "before the settings file is written"
                    )
                self.assertFalse(
                    legacy.exists() or legacy.is_symlink(), "the legacy shared directory is made by nothing"
                )
                fs = self.settings_of(role)["filesystem"]
                denied = login_read_denies(str(seats), role)
                self.assertEqual([row for row in fs["denyRead"] if row.startswith(f"{seats}/.state/claude")], denied)
                present = json.loads(record.read_text().splitlines()[-1])
                for row in denied:
                    self.assertEqual(present[row], row != str(legacy), (row, present))
                # Every denyRead row under the seats root but the legacy directory is a directory when srt reads the file.
                self.assertEqual([row for row, ok in present.items() if not ok], [str(legacy)], present)
        # A link or a file at any group's directory, the own group's or another's, refuses before anything is made
        # or started; the entry is neither followed, removed nor replaced.
        launches = len(record.read_text().splitlines())
        hcom_calls = len(self.calls_of("hcom"))
        elsewhere = self.home / "elsewhere"
        elsewhere.mkdir()
        for group, plant in (("audit", "link"), ("router", "file"), ("worker", "link")):
            with self.subTest(group=group, plant=plant):
                path = seats / f".state/claude-{group}"
                shutil.rmtree(path)
                if plant == "link":
                    path.symlink_to(elsewhere)
                    message = f"the login group directory {path} is a symbolic link"
                else:
                    path.write_text("")
                    message = f"the login group directory {path} is not a directory"
                run = self.seat("worker", "--seats-root", self.seats)
                self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
                self.assertIn(message, run.stderr)
                self.assertEqual(len(self.calls_of("hcom")), hcom_calls, "nothing started")
                self.assertTrue(
                    path.is_symlink() if plant == "link" else path.is_file(), "neither removed nor replaced"
                )
                self.assertEqual(sorted(p.name for p in elsewhere.iterdir()), [])
                path.unlink()
                path.mkdir(0o700)
        self.assertEqual(len(record.read_text().splitlines()), launches, "no omp ran")

    def test_the_make_step_makes_the_tables_range_on_a_scratch_root_and_refuses_a_planted_entry_by_name(self):
        """U498d: `login_dirs_make`, the make step, run from the lever's own text (with `refuse` and the `LOGIN_GROUPS`
        line) on a scratch seats root whose `.state` exists: one 0700 directory per group of the range, empty, and
        nothing else; a second run keeps them (present or made, each is a real directory of this user); a regular
        file or a symbolic link planted at a group's path refuses (exit 2) naming the group and the path, the other
        directories untouched; the legacy `.state/claude` is never made."""
        text = SEAT.read_text()
        functions = "\n".join(
            text[text.index(f"{name}() {{") : text.index("\n}\n", text.index(f"{name}() {{")) + 3]
            for name in ("refuse", "login_dirs_make")
        )
        (array,) = [line for line in text.splitlines() if line.startswith("LOGIN_GROUPS=(")]
        root = Path(self.temp.name).resolve() / "scratch-seats"
        (root / ".state").mkdir(parents=True)
        script = f"set -euo pipefail\n{array}\n{functions}\nseats_root=$1\nlogin_dirs_make\n"

        def make():
            return subprocess.run(["bash", "-c", script, "_", str(root)], capture_output=True, text=True, check=False)

        for attempt in ("made", "kept"):
            with self.subTest(attempt):
                run = make()
                self.assertEqual((run.returncode, run.stdout, run.stderr), (0, "", ""))
                self.assertEqual(
                    sorted(p.name for p in (root / ".state").iterdir()), sorted(f"claude-{g}" for g in LOGIN_GROUPS)
                )
                for group in LOGIN_GROUPS:
                    path = root / f".state/claude-{group}"
                    self.assertTrue(path.is_dir() and not path.is_symlink(), path)
                    self.assertEqual(stat.S_IMODE(os.lstat(path).st_mode), 0o700, path)
                    self.assertEqual(list(path.iterdir()), [], path)
        for group, plant in (("worker", "file"), ("router", "link")):
            with self.subTest(group=group, plant=plant):
                path = root / f".state/claude-{group}"
                path.rmdir()
                if plant == "file":
                    path.write_text("")
                else:
                    path.symlink_to(root)
                run = make()
                self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
                self.assertIn(
                    f"the {group} login group's Claude Code directory {path} is not a real directory of this user",
                    run.stderr,
                )
                for other in LOGIN_GROUPS:
                    if other != group:
                        self.assertTrue((root / f".state/claude-{other}").is_dir(), other)
                path.unlink()
                path.mkdir(0o700)
        self.assertFalse((root / ".state/claude").exists() or (root / ".state/claude").is_symlink())

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
        """U85, failure injection: an srt that does not contain the canary's probes never reaches omp. U190b: the
        fourth probe, a write open under the operator's `~/.claude/debug` (srt 0.0.81's implicit grant), refuses
        naming it; a three-word answer of an older shim's shape refuses too."""
        for answer in ("write-open read-denied ssh-denied debug-denied", "write-denied read-open ssh-denied debug-denied",
                       "write-denied read-denied ssh-open debug-denied", "write-denied read-denied ssh-denied", ""):  # fmt: skip
            with self.subTest(answer):
                run = self.seat("worker", "--seats-root", self.seats, FAKE_SRT_CANARY=answer)
                self.assertEqual(run.returncode, 2, run.stderr)
                self.assertIn("the sandbox does not hold", run.stderr)
                self.assertEqual(self.calls_of("omp"), [])
        run = self.seat(
            "worker", "--seats-root", self.seats, FAKE_SRT_CANARY="write-denied read-denied ssh-denied debug-open"
        )
        self.assertEqual(run.returncode, 2, run.stderr)
        self.assertIn("the sandbox does not hold (operator Claude debug writable); omp not started", run.stderr)
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

    def test_an_srt_of_another_line_is_refused_before_anything_starts(self):
        """U141: hcom-seat encodes srt 0.0.81's behaviours (SRT_LINE); an installed srt whose major.minor differs, or
        whose `--version` fails or prints nothing, is refused (exit 2) naming the line before any seats root, store
        or process exists. A patch release of the encoded line launches."""
        for version in ("0.1.0", "1.0.81", "fail", ""):
            with self.subTest(version=version or "empty"):
                run = self.seat("worker", "--seats-root", self.seats, FAKE_SRT_VERSION=version)
                self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
                self.assertIn("hcom-seat: ", run.stderr)
                self.assertIn("0.0 line", run.stderr)
                if version in ("0.1.0", "1.0.81"):
                    self.assertIn(f"srt {version} is not of the 0.0 line hcom-seat encodes", run.stderr)
                else:
                    self.assertIn("cannot read the srt version", run.stderr)
                self.assertFalse(Path(self.seats).exists())
                self.assertEqual(self.calls_of("omp"), [])
                self.assertEqual(self.calls_of("hcom"), [])
                self.assertEqual([call["argv"] for call in self.calls_of("srt")], [["--version"]])
                (self.calls / "srt").unlink()
        run = self.seat("worker", "--seats-root", self.seats, FAKE_SRT_VERSION="0.0.99")
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual(len(self.calls_of("omp")), 1)

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
            # The version read (U141) runs before the seat's shim directory exists, on the private tool directory alone.
            self.assertEqual(call["path"], fixed if call["argv"] == ["--version"] else f"{sandbox_bin}:{fixed}")
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

    def test_a_root_in_the_operators_claude_state_is_refused(self):
        """U190b: the operator's Claude Code state is protected like the checkout. A store or seats root that is,
        contains or lies under `~/.claude`, `~/.claude.json` or the caller's CLAUDE_CONFIG_DIR refuses, naming it,
        before anything is created (round 1 accepted `HCOM_DIR=~/.claude` and granted the directory whole)."""
        home = self.home.resolve()
        claude = home / ".claude"
        cases = (
            ("the store is ~/.claude", [], {"HCOM_DIR": str(claude)},
             f"write root {claude} contains the operator's Claude Code directory {claude}"),
            ("the seats root lies under ~/.claude", ["--seats-root", str(claude / "seats")], {},
             f"lies inside the operator's Claude Code directory {claude}"),
            ("the store is ~/.claude.json", [], {"HCOM_DIR": str(home / ".claude.json")},
             f"contains the operator's Claude Code settings file {home / '.claude.json'}"),
            ("the store holds the caller's CLAUDE_CONFIG_DIR", [],
             {"HCOM_DIR": str(home / "cfg"), "CLAUDE_CONFIG_DIR": str(home / "cfg/claude")},
             f"contains the caller's CLAUDE_CONFIG_DIR {home / 'cfg/claude'}"),
        )  # fmt: skip
        for label, args, overrides, expected in cases:
            for dry_run in ((), ("--dry-run",)):
                with self.subTest(label, dry_run=bool(dry_run)):
                    run = self.seat("worker", *(args or ["--seats-root", self.seats]), *dry_run, **overrides)
                    self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
                    self.assertIn(expected, run.stderr)
                    self.assertFalse(Path(self.seats).exists())
                    self.assertFalse(claude.exists() or (home / "cfg").exists())
                    self.assertEqual(self.calls_of("hcom"), [])
        # The same with the directory present, for both roles (every launch checks the orchestrator's roots too).
        claude.mkdir()
        for role in ("worker", "orchestrator"):
            with self.subTest(role=role):
                run = self.seat(role, "--seats-root", self.seats, HCOM_DIR=str(claude))
                self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
                self.assertIn(f"contains the operator's Claude Code directory {claude}", run.stderr)
                self.assertEqual(list(claude.iterdir()), [])
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
        root (`~/.OMP/run/seats` for `~/.omp/run`; U190 made `~/.claude` no root) is refused when the alias exists,
        and, when neither exists yet, by the case-folded absent components (U85 round 30); a nonexistent child of an
        existing alias is caught too."""
        root = self.home / ".omp/run"
        alias = self.home / ".OMP/run"
        run = self.seat("worker", "--seats-root", str(alias / "seats"), "--dry-run")
        self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
        self.assertIn(f"write root {root} contains the seats root {alias / 'seats'}", run.stderr)
        root.mkdir(parents=True, exist_ok=True)
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

    def identity_functions(self):
        """The identity code of hcom-seat, extracted: the table builder and the pairwise decision (U95)."""
        text = SEAT.read_text()
        return "\n".join(
            text[text.index(f"{name}() {{") : text.index("\n}\n", text.index(f"{name}() {{")) + 3]
            for name in (
                "refuse", "clean_path", "require_clean_path", "ancestors_of", "identity_table", "ascii_lower",
                "within_ix",
            )
        )  # fmt: skip

    def test_a_failing_helper_in_the_identity_check_refuses_the_launch(self):
        """U85 round 15, U95: the identity table's one producer (stat) is checked: one that prints a plausible answer
        and fails refuses instead of deciding. The case fold is builtin (ascii_lower), no `tr` runs."""
        self.assertNotIn("/usr/bin/tr", self.identity_functions())
        stat_args = "(-L -f '%d:%i')" if sys.platform == "darwin" else "(-L -c '%d:%i')"
        outer = Path(self.temp.name).resolve() / "outer"
        outer.mkdir()
        fakes = Path(self.temp.name).resolve() / "failing"
        fakes.mkdir()
        (fakes / "stat").write_text("#!/bin/sh\nfor a; do echo 1:2; done\nexit 7\n")
        (fakes / "stat").chmod(0o755)
        for label, inner in (("exists", outer / "a/b"), ("neither exists", outer / "x/y")):
            with self.subTest(case=label):
                functions = self.identity_functions().replace("/usr/bin/stat", str(fakes / "stat"))
                script = (
                    f"set -euo pipefail\nstat_args={stat_args}\n{functions}\n"
                    'status=0\nidentity_table "$1" "$2"\nwithin_ix 0 1 || status=$?\necho decided=$status\n'
                )
                run = subprocess.run(
                    ["/bin/bash", "-c", script, "_", str(outer), str(inner)],
                    capture_output=True, text=True, check=False,
                )  # fmt: skip
                self.assertEqual((run.returncode, run.stdout), (2, ""), run.stdout + run.stderr)
                self.assertIn("cannot read the identity", run.stderr)

    def test_every_batched_producer_fails_closed(self):
        """U95: each batch hcom-seat runs over many paths refuses when its producer fails after printing plausible
        output, prints too few records, or prints a malformed one: physical_paths (cd, physical_path, a record's
        printf; it calls no pwd and prints nothing back), sizes_of (stat), pointer_values (cat, and its sizes), and
        the identity table (stat; its fold is builtin, so a fold that keeps case, changes length or fails refuses).
        Round 3: every result is assigned to its input's index, and the overlap check refuses when a worktree has no
        resolved path, so it cannot miss one. dir_entries (the one enumeration) refuses a failed or short read, and
        admin_dirs_match refuses an orphan, an unlisted or a duplicated record, and its producers (stat, cat, cd)
        failing after plausible output; git_state_check's one mkdir for every missing info/ and hooks/ refuses when
        it fails, fails after a partial creation, or leaves a link."""
        text = SEAT.read_text()
        names = (
            "refuse",
            "clean_path",
            "require_clean_path",
            "physical_path",
            "physical_paths",
            "physical_each",
            "sizes_of",
        )
        names += ("pointer_values", "ancestors_of", "identity_table", "ascii_lower", "within_ix")
        names += ("operator_claude_paths", "seat_overlap_check")
        names += ("dir_entries", "admin_dirs_match", "git_state_check", "git_form_path")
        functions = "\n".join(
            text[text.index(f"{name}() {{") : text.index("\n}\n", text.index(f"{name}() {{")) + 3] for name in names
        )
        darwin = sys.platform == "darwin"
        args = (
            "stat_args=(-L -f '%d:%i') size_args=(-L -f '%z')"
            if darwin
            else "stat_args=(-L -c '%d:%i') size_args=(-L -c '%s')"
        )
        root = Path(self.temp.name).resolve() / "batch"
        for name in ("a", "b", "real", "d"):
            (root / name).mkdir(parents=True)
        (root / "c").symlink_to("real")
        (root / "file").write_text("")
        for name in ("a", "b"):
            (root / name / "commondir").write_text("../..\n")
        # Present directories, a link, and absent paths (one below the link, one below an ancestor of its own), all
        # resolved in the one subshell.
        dirs = [str(root / n) for n in ("a", "b", "c", "absent", "c/gone/deeper", "d/gone")]
        pointers = [str(root / n / "commondir") for n in ("a", "b")]
        fakes = root / "fakes"
        fakes.mkdir()

        def fake(name, body):
            path = fakes / name
            path.write_text(f"#!/bin/sh\n{body}\n")
            path.chmod(0o755)
            return str(path)

        def run(call, script_args, replace=None, prelude=""):
            body = functions
            for real, stand_in in (replace or {}).items():
                body = body.replace(real, stand_in)
            script = f"set -euo pipefail\n{args}\n{body}\n{prelude}\n{call}\n"
            return subprocess.run(
                ["/bin/bash", "-c", script, "_", *script_args], capture_output=True, text=True, check=False, timeout=30
            )

        paths_call = 'physical_paths "$@"\nprintf "%s\\n" "${phys_list[@]}"'
        good = run(paths_call, dirs)
        self.assertEqual(good.returncode, 0, good.stderr)
        self.assertEqual(
            good.stdout.split(),
            [str(root / n) for n in ("a", "b", "real", "absent", "real/gone/deeper", "d/gone")],
        )
        paths_cases = {
            "cd fails after a plausible PWD": 'cd() { if [[ $3 == */b/ ]]; then PWD=/plausible/b; return 7; fi; builtin cd "$@"; }',
            "a record is dropped": 'printf() { [[ $# == 3 && $2 == */b ]] && return 0; builtin printf "$@"; }',
            "a record's printf fails (the audit's case)": 'printf() { [[ $# == 3 && $2 == */b ]] && return 7; builtin printf "$@"; }',
            "physical_path is never called": "physical_path() { echo /plausible/a; return 7; }",
            "cd fails for an absent path's ancestor": 'cd() { if [[ $3 == */d/ ]]; then PWD=/plausible/d; return 7; fi; builtin cd "$@"; }',
            "an absent path's record is dropped": 'printf() { [[ $# == 3 && $3 == /gone ]] && return 0; builtin printf "$@"; }',
            "a malformed record": 'cd() { builtin cd "$@" || return; [[ $PWD != */b ]] || PWD=relative; }',
        }
        self.assertEqual(run(paths_call, dirs, prelude=paths_cases.pop("physical_path is never called")).returncode, 0)
        for label, prelude in paths_cases.items():
            with self.subTest(producer="physical_paths", case=label):
                result = run(paths_call, dirs, prelude=prelude)
                self.assertEqual((result.returncode, result.stdout), (2, ""), result.stdout + result.stderr)
        # A path that is, or lies below, a regular file or a dangling link is no directory-backed worktree: refused,
        # with no fallback process.
        (root / "dangling").symlink_to("nowhere")
        for label, path in (("a regular file", "file"), ("below a file", "file/x/y"), ("a dangling link", "dangling")):
            with self.subTest(producer="physical_paths", case=label):
                result = run(paths_call, [*dirs, str(root / path)])
                self.assertEqual((result.returncode, result.stdout), (2, ""), result.stdout + result.stderr)
                self.assertIn(f"the worktree record {root / path} is not backed by a directory", result.stderr)
                self.assertIn("git worktree prune", result.stderr)
        # physical_each (U272f), the judge's resolver over rendered settings rows, files and absent tails included:
        # a batch whose subshell fails, an empty batch, a short batch, a `fail` record, a malformed record and a
        # record too many each refuse; the real batch resolves every row.
        each_call = 'physical_each "$@"\nprintf "%s\\n" "${phys_list[@]}"'
        rows = [*dirs, str(root / "file"), str(root / "c/file-gone")]
        good = run(each_call, rows)
        self.assertEqual(good.returncode, 0, good.stderr)
        self.assertEqual(
            good.stdout.split(),
            [
                str(root / n)
                for n in ("a", "b", "real", "absent", "real/gone/deeper", "d/gone", "file", "real/file-gone")
            ],
        )
        real_each = (
            "physical_path_real() {" + functions[functions.index("physical_path() {") + len("physical_path() {") :]
        )
        real_each = real_each[: real_each.index("\n}\n") + 3]
        each_cases = {
            "the batch fails after plausible output": 'printf() { [[ $# == 3 && $2 == */b ]] && exit 7; builtin printf "$@"; }',
            "an empty batch": "physical_path() { return 0; }",
            "a short batch": real_each + '\nphysical_path() { [[ $1 == */b ]] || physical_path_real "$1"; }',
            "a fail record": real_each + '\nphysical_path() { [[ $1 != */b ]] && physical_path_real "$1"; }',
            "a malformed record": real_each
            + '\nphysical_path() { if [[ $1 == */b ]]; then echo relative; else physical_path_real "$1"; fi; }',
            "a record too many": real_each
            + '\nphysical_path() { physical_path_real "$1" && [[ $1 != */b ]] || physical_path_real "$1"; }',
        }
        for label, prelude in each_cases.items():
            with self.subTest(producer="physical_each", case=label):
                result = run(each_call, rows, prelude=prelude)
                self.assertEqual((result.returncode, result.stdout), (2, ""), result.stdout + result.stderr)
                self.assertIn("settings path", result.stderr)
        sizes_call = 'sizes_of "$@"\nprintf "%s\\n" "${size_list[@]}"'
        self.assertEqual(run(sizes_call, pointers).stdout.split(), ["6", "6"])
        stat_cases = {
            "fails after plausible output": fake("stat-fail", "for a; do echo 6; done\nexit 7"),
            "too few lines": fake("stat-short", "echo 6"),
            "a malformed line": fake("stat-bad", "for a; do echo six; done"),
        }
        for label, stand_in in stat_cases.items():
            with self.subTest(producer="sizes_of (stat)", case=label):
                result = run(sizes_call, pointers, {"/usr/bin/stat": stand_in})
                self.assertEqual((result.returncode, result.stdout), (2, ""), result.stdout + result.stderr)
                self.assertIn("cannot read the size", result.stderr)
        values_call = 'pointer_values "$@"\nprintf "%s\\n" "${pointer_list[@]}"'
        self.assertEqual(run(values_call, pointers).stdout.split(), ["../..", "../.."])
        cat_cases = {
            "fails after plausible output": fake("cat-fail", "printf '../..\\n../..\\n'\nexit 7"),
            "a short read": fake("cat-short", "printf '../..\\n'"),
            "a long read": fake("cat-long", "printf '../..\\n../..\\nmore\\n'"),
        }
        for label, stand_in in cat_cases.items():
            with self.subTest(producer="pointer_values (cat)", case=label):
                result = run(values_call, pointers, {"/bin/cat": stand_in})
                self.assertEqual((result.returncode, result.stdout), (2, ""), result.stdout + result.stderr)
                self.assertIn("cannot read the git pointer files", result.stderr)
        tr_cases = {
            "fails after plausible output": fake("tr-fail", "cat\nexit 7"),
            "a short output": fake("tr-short", "head -c 3"),
        }
        for label, stand_in in tr_cases.items():
            with self.subTest(producer="pointer_values (tr)", case=label):
                result = run(values_call, pointers, {"/usr/bin/tr": stand_in})
                self.assertEqual((result.returncode, result.stdout), (2, ""), result.stdout + result.stderr)
                self.assertIn("cannot read the git pointer files", result.stderr)
        with self.subTest(producer="pointer_values (its sizes)"):
            result = run(values_call, pointers, {"/usr/bin/stat": stat_cases["fails after plausible output"]})
            self.assertEqual((result.returncode, result.stdout), (2, ""), result.stdout + result.stderr)
        table_call = 'identity_table "$@"\nwithin_ix 0 1 && echo inside || echo outside'
        table_args = [str(root), str(root / "a/NEW")]
        self.assertEqual(run(table_call, table_args).stdout, "inside\n")
        fold = run('ascii_lower "$1" out\nprintf "%s\\n" "$out"', ["/New/ABC.x-Y_z@1+Q/"])
        self.assertEqual(fold.stdout, "/new/abc.x-y_z@1+q/\n", fold.stderr)
        table_cases = {
            ("stat", "too few lines"): ("/usr/bin/stat", fake("id-short", "echo 1:2")),
            ("stat", "a malformed line"): ("/usr/bin/stat", fake("id-bad", "for a; do echo id; done")),
            ("stat", "fails after plausible output"): (
                "/usr/bin/stat",
                fake("id-fail", "for a; do echo 1:2; done\nexit 7"),
            ),
        }
        for (producer, label), (real, stand_in) in table_cases.items():
            with self.subTest(producer=f"identity_table ({producer})", case=label):
                result = run(table_call, table_args, {real: stand_in})
                self.assertEqual((result.returncode, result.stdout), (2, ""), result.stdout + result.stderr)
        fold_cases = {
            "keeps upper case": 'ascii_lower() { printf -v "$2" \'%s\' "$1"; }',
            "changes the length": "ascii_lower() { printf -v \"$2\" '%s' /new/; }",
            "fails": "ascii_lower() { return 1; }",
        }
        for label, prelude in fold_cases.items():
            with self.subTest(producer="identity_table (fold)", case=label):
                result = run(table_call, table_args, prelude=prelude)
                self.assertEqual((result.returncode, result.stdout), (2, ""), result.stdout + result.stderr)
                self.assertIn("cannot fold the absent part", result.stderr)
        # The overlap consumer: two worktrees under the checkout both reach the deny list; one without its resolved
        # path, or a protected path without its result, refuses.
        # dir_entries: an empty directory lists nothing; a listing that fails after plausible output, or counts
        # other entries than the glob saw, refuses; an unreadable or linked directory refuses before any glob.
        listed = root / "listed"
        (listed / ".dot").mkdir(parents=True)
        (listed / "plain").mkdir()
        (root / "empty").mkdir()
        entries_call = 'dir_entries "$1"\nprintf "%s\\n" ${dir_list[@]+"${dir_list[@]}"}'
        good = run(entries_call, [str(listed)])
        self.assertEqual(
            (good.returncode, sorted(good.stdout.split())), (0, [str(listed / ".dot"), str(listed / "plain")])
        )
        empty = run(entries_call, [str(root / "empty")])
        self.assertEqual((empty.returncode, empty.stdout), (0, "\n"), empty.stderr)
        absent = run(entries_call, [str(root / "absent-dir")])
        self.assertEqual((absent.returncode, absent.stdout), (0, "\n"), absent.stderr)
        (root / "linked-dir").symlink_to(listed)
        ls_cases = {
            "fails after plausible output": ({"/bin/ls": fake("ls-fail", "printf '.dot\\nplain\\n'\nexit 7")}, listed),
            "counts fewer entries": ({"/bin/ls": fake("ls-short", "printf 'plain\\n'")}, listed),
            "counts an entry the glob missed": ({"/bin/ls": fake("ls-more", "printf 'x\\n'")}, root / "empty"),
            "a linked directory": (None, root / "linked-dir"),
        }
        for label, (replace, target) in ls_cases.items():
            with self.subTest(producer="dir_entries", case=label):
                result = run(entries_call, [str(target)], replace)
                self.assertEqual((result.returncode, result.stdout), (2, ""), result.stdout + result.stderr)
                self.assertIn("cannot list", result.stderr)
        # admin_dirs_match: the admin directories, one to one with the worktrees git lists. Two admin directories
        # recording one worktree, one recording an unlisted path, and an orphan refuse; so do its producers failing
        # after plausible output (the gitdir sizes, the gitdir read, the resolving cd).
        admin_root = root / "common"
        for t in ("a", "b"):
            (admin_root / "worktrees" / t).mkdir(parents=True)
            (root / "trees" / t).mkdir(parents=True)
            (admin_root / "worktrees" / t / "gitdir").write_text(f"{root}/trees/{t}/.git\n")
        listed = f"{root}/trees/a {root}/trees/b"
        match_call = (
            f"git_fix_hint='' worktree_phys=(${{listed_override:-{listed}}})\n"
            'dir_entries "$1/worktrees"\nadmin_dirs=("${dir_list[@]}")\nadmin_dirs_match "$1"\necho matched'
        )
        good = run(match_call, [str(admin_root)])
        self.assertEqual((good.returncode, good.stdout), (0, "matched\n"), good.stderr)
        gitdir_b = admin_root / "worktrees/b/gitdir"

        def recorded(text):
            return lambda: gitdir_b.write_text(text)

        def orphan():
            (admin_root / "worktrees/c").mkdir()
            (admin_root / "worktrees/c/gitdir").write_text(f"{root}/trees/a/.git\n")

        match_cases = {
            "two admin directories recording one worktree": (recorded(f"{root}/trees/a/.git\n"), None, "", "records too"),
            "a record git does not list": (recorded(f"{root}/elsewhere/.git\n"), None, "", "does not list"),
            "an orphan admin directory": (orphan, None, "", "holds 3 worktree git directories but git lists 2"),
            "stat fails after plausible output": (
                None, {"/usr/bin/stat": fake("stat-pass-fail", '/usr/bin/stat "$@"\nexit 7')}, "", "cannot read the size",
            ),
            "cat fails after plausible output": (
                None, {"/bin/cat": fake("cat-pass-fail", '/bin/cat "$@"\nexit 7')}, "", "cannot read the git pointer files",
            ),
            "cd fails after a plausible PWD": (
                None, None, 'cd() { if [[ $3 == */trees/b/ ]]; then PWD=/plausible/b; return 7; fi; builtin cd "$@"; }',
                "cannot resolve the path",
            ),
        }  # fmt: skip
        # A case alias on a case-insensitive volume: git lists `trees/a` and `TREES/A` (two admin directories), which
        # `cd -P` leaves as two texts for one directory; identity sees one.
        alias = root / "TREES/A"
        if alias.exists() and alias.samefile(root / "trees/a"):
            match_cases["two admin directories recording one worktree by case alias"] = (
                recorded(f"{alias}/.git\n"),
                None,
                f"listed_override='{root}/trees/a {alias}'",
                "records too",
            )
        for label, (mutate, replace, prelude, message) in match_cases.items():
            with self.subTest(producer="admin_dirs_match", case=label):
                if mutate:
                    mutate()
                try:
                    result = run(match_call, [str(admin_root)], replace, prelude)
                    self.assertEqual((result.returncode, result.stdout), (2, ""), result.stdout + result.stderr)
                    self.assertIn(message, result.stderr)
                finally:
                    gitdir_b.write_text(f"{root}/trees/b/.git\n")
                    shutil.rmtree(admin_root / "worktrees/c", ignore_errors=True)
        # git_form_path: git's own pointer form only.
        form_call = 'for v in "$@"; do if git_form_path "$v"; then echo "ok $v"; else echo "no $v"; fi; done'
        forms = {
            "/abs/.git/worktrees/t": "ok", "../..": "ok", "../../.git/worktrees/t": "ok", "t/.git": "ok",
            "/abs/link/": "no", "/abs/link/.": "no", "/abs/./x": "no", "a/../b": "no", "/abs/..": "no", "": "no",
            "/abs//x": "no", "../": "no", ".": "no", "/": "no",
        }  # fmt: skip
        result = run(form_call, list(forms))
        self.assertEqual(result.stdout.splitlines(), [f"{v} {k}" for k, v in forms.items()], result.stderr)
        # git_state_check's mkdir batch (a real launch): every missing info/ and hooks/ in one /bin/mkdir run. A mkdir
        # that fails outright, one that creates some directories and then fails, and one after which a directory
        # is a link each refuse; the real mkdir makes all three.
        state = root / "state"

        def fresh_state():
            shutil.rmtree(state, ignore_errors=True)
            (state / "worktrees/a").mkdir(parents=True)
            (state / "worktrees/a/commondir").write_text("../..\n")
            (state / "worktrees/a/gitdir").write_text(f"{root}/trees/a/.git\n")

        state_call = f"dry_run=0 git_fix_hint=''\ngit_state_check {state} ''\necho checked"
        missing = [state / "info", state / "hooks", state / "worktrees/a/info"]
        fresh_state()
        good = run(state_call, [])
        self.assertEqual((good.returncode, good.stdout), (0, "checked\n"), good.stderr)
        self.assertTrue(all(d.is_dir() and not d.is_symlink() for d in missing))
        mkdir_cases = {
            "fails outright": (fake("mkdir-fail", "exit 1"), "cannot create the git state directories"),
            "creates some, then fails": (
                fake("mkdir-partial", 'shift\n/bin/mkdir -- "$1"\nexit 1'), "cannot create the git state directories"
            ),
            "leaves a link": (
                fake("mkdir-link", 'shift\nfor d; do last=$d; /bin/mkdir -- "$d"; done\n/bin/rmdir -- "$last"\n'
                     f'/bin/ln -s {root} "$last"'),
                "is not a real directory after it was created",
            ),
        }  # fmt: skip
        for label, (stand_in, message) in mkdir_cases.items():
            with self.subTest(producer="git_state_check (mkdir)", case=label):
                fresh_state()
                result = run(state_call, [], {"/bin/mkdir": stand_in})
                self.assertEqual((result.returncode, result.stdout), (2, ""), result.stdout + result.stderr)
                self.assertIn(message, result.stderr)
        # The overlap consumer: worktrees outside every write root pass; one without its resolved path refuses.
        checkout, seats, away = root / "checkout", root / "seats", root / "away"
        checkout.mkdir()
        seats.mkdir()
        for tree in ("w1", "w2"):
            (away / tree).mkdir(parents=True)
        trees = [str(away / t) for t in ("w1", "w2")]
        overlap = (
            f"seats_root={seats} checkout={checkout} common={root}/no-git repo={checkout} root_ids=$'\\n'\n"
            f'worktree_paths=({checkout} "$@")\nworktree_phys=("$@")\n'
        )
        overlap_call = 'seat_overlap_check orchestrator "$checkout" "$checkout"\necho checked'
        whole = run(overlap_call, trees, prelude=overlap)
        self.assertEqual((whole.returncode, whole.stdout), (0, "checked\n"), whole.stderr)
        result = run(overlap_call, trees, prelude=overlap + 'worktree_phys=("$1")')
        self.assertEqual((result.returncode, result.stdout), (2, ""), result.stdout + result.stderr)
        self.assertIn("were not all resolved", result.stderr)

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
        """U85 round 30: below the deepest existing ancestor nothing exists, so within_ix decides two absent paths by
        that ancestor's identity and their clean components: nested refuses, disjoint passes, `a/b` is no prefix of
        `a/bc`, and an existing outer path is still decided by identity."""
        functions = self.identity_functions()
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
                script = (
                    f"set -euo pipefail\nstat_args={stat_args}\n{functions}\n"
                    'status=0\nidentity_table "$1" "$2"\nwithin_ix 0 1 || status=$?\necho $status\n'
                )
                run = subprocess.run(
                    ["/bin/bash", "-c", script, "_", str(root / outer), str(root / inner)],
                    capture_output=True, text=True, check=False, timeout=20,
                )  # fmt: skip
                self.assertEqual((run.returncode, run.stdout), (0, f"{expected}\n"), run.stderr)

    def test_a_worktree_inside_a_seat_write_root_refuses(self):
        """U95 (operator decision U95-nested-refuse-decided): a linked worktree inside any seat's write root refuses the
        launch, as in U85, dry runs included: Claude Code's `<checkout>/.claude/worktrees/x` inside the orchestrator's
        checkout, present or absent, for both roles (every launch checks the orchestrator's roots). The message names
        the worktree and `git worktree move`, `remove` and `prune`. Once it is moved out, both launch."""
        nested = self.repo / ".claude/worktrees/x"
        self.git("worktree", "add", "-q", "--detach", str(nested), "HEAD")
        nested = nested.resolve()
        for state in ("present", "absent"):
            if state == "absent":
                shutil.rmtree(nested)
            for role in ("orchestrator", "worker"):
                for dry in (["--dry-run"], []):
                    with self.subTest(state=state, role=role, dry=bool(dry)):
                        run = self.seat(role, "--seats-root", self.seats, *dry)
                        self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
                        self.assertIn(
                            f"the worktree {nested} lies inside the orchestrator seat's write root", run.stderr
                        )
                        for advice in ("git worktree move", "git worktree remove", "git worktree prune"):
                            self.assertIn(advice, run.stderr)
                        self.assertEqual(self.calls_of("hcom"), [])
        self.git("worktree", "prune")
        away = Path(self.temp.name).resolve() / "away"
        self.git("worktree", "add", "-q", "--detach", str(away), "HEAD")
        for role in ("orchestrator", "worker"):
            with self.subTest(moved=role):
                run = self.seat(role, "--seats-root", self.seats, "--dry-run")
                self.assertEqual(run.returncode, 0, run.stderr)

    def test_worktree_git_directories_are_checked_in_git_s_shape(self):
        """U95: every worktree's admin directory `<common>/worktrees/<id>` is enumerated once, dot names included as
        git's own readdir does, held one to one to the worktrees git lists, and checked in git's shape: a real
        directory with `commondir` (without it git takes the directory for its own common directory and reads a config
        and hooks a seat can write), none of the names git keeps in the common directory, and each git file absent or
        a regular file, its type read before its size or content (a FIFO no longer reads as empty or blocks). One
        fresh worktree outside every write root per deviation; the plain shape launches. A dot-named admin
        directory's git files are write-denied to every seat."""
        common = (self.repo / ".git").resolve()
        away = Path(self.temp.name).resolve() / "away"

        def fifo(name):
            def make(admin):
                (admin / name).unlink(missing_ok=True)
                os.mkfifo(admin / name)

            return make

        def linked_admin(admin):
            admin.rename(admin.with_name(admin.name + "-real"))
            admin.symlink_to(admin.name + "-real")

        cases = {
            "git directory a link": (linked_admin, "is not a real directory (a symbolic link"),
            "config.worktree a FIFO": (fifo("config.worktree"), "config.worktree is not a regular file"),
            "commondir a FIFO": (fifo("commondir"), "commondir is not a regular file"),
            "gitdir a FIFO": (fifo("gitdir"), "gitdir is not a regular file"),
            "commondir missing": (lambda admin: (admin / "commondir").unlink(), "has no commondir"),
            "config in it": (lambda admin: (admin / "config").write_text(""), "holds config"),
            "hooks in it": (lambda admin: (admin / "hooks").mkdir(), "holds hooks"),
            "objects in it": (lambda admin: (admin / "objects").mkdir(), "holds objects"),
            "packed-refs in it": (lambda admin: (admin / "packed-refs").write_text(""), "holds packed-refs"),
            "an orphan beside it": (
                lambda admin: ((common / "worktrees/orphan").mkdir(), (common / "worktrees/orphan/commondir").write_text("../..\n")),
                "worktree git directories but git lists",
            ),
        }  # fmt: skip
        for n, (label, (mutate, message)) in enumerate(cases.items()):
            with self.subTest(deviation=label):
                tree = away / f"d{n}"
                self.git("worktree", "add", "-q", "--detach", str(tree), "HEAD")
                admin = common / "worktrees" / f"d{n}"
                try:
                    mutate(admin)
                    run = subprocess.run(
                        [str(SEAT), "worker", "--seats-root", self.seats, "--dry-run"], cwd=self.repo, env=self.env,
                        capture_output=True, text=True, check=False, timeout=120,
                    )  # fmt: skip
                    self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
                    self.assertIn(message, run.stderr)
                    self.assertIn("git worktree", run.stderr)
                finally:
                    # Always undone, a FIFO above all: a later `git worktree add` would block reading it.
                    shutil.rmtree(tree, ignore_errors=True)
                    if admin.is_symlink():
                        admin.unlink()
                        admin = admin.with_name(admin.name + "-real")
                    shutil.rmtree(admin, ignore_errors=True)
                    shutil.rmtree(common / "worktrees/orphan", ignore_errors=True)
        plain = away / "plain"
        self.git("worktree", "add", "-q", "--detach", str(plain), "HEAD")
        hidden = common / "worktrees/.hidden"
        (common / "worktrees/plain").rename(hidden)
        (plain / ".git").write_text(f"gitdir: {hidden}\n")
        self.assertIn(f"worktree {plain}\n", self.git("worktree", "list", "--porcelain") + "\n")
        for role in ("worker", "orchestrator"):
            with self.subTest(shape="plain, dot-named", role=role):
                run = self.seat(role, "--seats-root", self.seats)
                self.assertEqual(run.returncode, 0, run.stderr)
                deny = self.settings_of(role)["filesystem"]["denyWrite"]
                for name in ("gitdir", "commondir", "config.worktree", "info"):
                    self.assertIn(str(hidden / name), deny)

    def test_a_launch_from_a_worktree_with_a_fifo_commondir_refuses_before_git(self):
        """U95 round 12: the launch checkout's own git files are type-checked before its common directory is derived
        and before any git command: from a linked worktree whose admin directory's `commondir` is a FIFO (or a link,
        or missing) the launch refuses at once instead of leaving the guess at the admin directory, missing the FIFO
        in the scan and blocking in the first git command. No git process starts (a PATH git that logs every call),
        and the run ends well inside the timeout. A `.git` that is a link refuses the same way."""
        common = (self.repo / ".git").resolve()
        tree = Path(self.temp.name).resolve() / "away" / "t"
        self.git("worktree", "add", "-q", "--detach", str(tree), "HEAD")
        admin = common / "worktrees" / "t"
        log = Path(self.temp.name) / "git-calls"
        wrapper = Path(self.temp.name) / "logging-git"
        wrapper.mkdir()
        real_git = shutil.which("git", path=SYSTEM_PATH)
        (wrapper / "git").write_text(f'#!/bin/sh\nprintf "%s\\n" "$*" >> "{log}"\nexec "{real_git}" "$@"\n')
        (wrapper / "git").chmod(0o755)
        env = {**self.env, "PATH": f"{wrapper}:{self.env['PATH']}"}

        def fifo():
            (admin / "commondir").unlink()
            os.mkfifo(admin / "commondir")

        def link():
            (admin / "commondir").unlink()
            (admin / "commondir").symlink_to(common / "worktrees" / "elsewhere")

        def git_link():
            (tree / ".git").rename(tree / "dot-git")
            (tree / ".git").symlink_to("dot-git")

        cases = {
            "commondir a FIFO": (fifo, "commondir is not a regular file"),
            "commondir a link": (link, "commondir is not a regular file"),
            "commondir missing": (lambda: (admin / "commondir").unlink(), "has no commondir"),
            ".git a link": (git_link, "is not a regular file or a real directory"),
        }
        for label, (mutate, message) in cases.items():
            with self.subTest(label):
                mutate()
                try:
                    log.unlink(missing_ok=True)
                    run = subprocess.run(
                        [str(SEAT), "worker", "--seats-root", self.seats, "--dry-run"], cwd=tree, env=env,
                        capture_output=True, text=True, check=False, timeout=60,
                    )  # fmt: skip
                    self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
                    self.assertIn(message, run.stderr)
                    self.assertFalse(log.exists(), "a git command ran before the refusal")
                finally:
                    (admin / "commondir").unlink(missing_ok=True)
                    (admin / "commondir").write_text("../..\n")
                    if (tree / ".git").is_symlink():
                        (tree / ".git").unlink()
                        (tree / "dot-git").rename(tree / ".git")
        log.unlink(missing_ok=True)
        run = subprocess.run(
            [str(SEAT), "worker", "--seats-root", self.seats, "--dry-run"], cwd=tree, env=env,
            capture_output=True, text=True, check=False, timeout=120,
        )  # fmt: skip
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertTrue(log.exists(), "the logging git is the one hcom-seat runs")

    def test_git_pointers_must_be_in_git_s_form(self):
        """U95 round 19: a path read from a git pointer file must be in git's own form before any type test: a trailing
        `/` or `/.` makes `[[ -L … ]]` follow a link, so a `.git` naming `<link>/` passed as a real directory. The
        launch checkout's `.git` (`<link>/`, `<link>/.`, `a/../b`, empty) refuses before any git command; another
        worktree's `commondir` (`../../`, `../../.`, `../x/../..`) and `gitdir` back-pointer (`<tree>/./.git`,
        `<tree>/.git/`) refuse in the checks."""
        common = (self.repo / ".git").resolve()
        tree = Path(self.temp.name).resolve() / "away" / "t"
        self.git("worktree", "add", "-q", "--detach", str(tree), "HEAD")
        admin = common / "worktrees/t"
        alias = Path(self.temp.name).resolve() / "alias"
        alias.symlink_to(admin)
        log = Path(self.temp.name) / "git-calls"
        wrapper = Path(self.temp.name) / "logging-git"
        wrapper.mkdir()
        real_git = shutil.which("git", path=SYSTEM_PATH)
        (wrapper / "git").write_text(f'#!/bin/sh\nprintf "%s\\n" "$*" >> "{log}"\nexec "{real_git}" "$@"\n')
        (wrapper / "git").chmod(0o755)
        env = {**self.env, "PATH": f"{wrapper}:{self.env['PATH']}"}
        dot_git = (tree / ".git").read_text()
        for label, value in (
            ("a link with a trailing slash", f"{alias}/"),
            ("a link with a trailing dot", f"{alias}/."),
            ("a .. after a name", f"{common}/worktrees/x/../t"),
            ("empty", ""),
        ):
            with self.subTest(pointer=".git", form=label):
                (tree / ".git").write_text(f"gitdir: {value}\n")
                log.unlink(missing_ok=True)
                run = subprocess.run(
                    [str(SEAT), "worker", "--seats-root", self.seats, "--dry-run"], cwd=tree, env=env,
                    capture_output=True, text=True, check=False, timeout=60,
                )  # fmt: skip
                self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
                self.assertIn("not a path in git's own form", run.stderr)
                self.assertFalse(log.exists(), "a git command ran before the refusal")
        (tree / ".git").write_text(dot_git)
        for name, values, original in (
            ("commondir", ("../../", "../../.", "../x/../.."), "../..\n"),
            ("gitdir", (f"{tree}/./.git", f"{tree}/.git/"), f"{tree}/.git\n"),
        ):
            for value in values:
                with self.subTest(pointer=name, form=value):
                    (admin / name).write_text(f"{value}\n")
                    run = self.seat("worker", "--seats-root", self.seats, "--dry-run")
                    self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
                    # git lists `<tree>/.git/` itself as the worktree (it strips only a final `/.git`), so that record
                    # refuses one step earlier, as not backed by a directory.
                    self.assertTrue(
                        f"{admin / name} holds '{value}', not a path in git's own form" in run.stderr
                        or f"the worktree record {value} is not backed by a directory" in run.stderr,
                        run.stderr,
                    )
            (admin / name).write_text(original)
        run = self.seat("worker", "--seats-root", self.seats, "--dry-run")
        self.assertEqual(run.returncode, 0, run.stderr)

    def add_worktrees(self, first, count, absent=False):
        """Register worktrees w<first>..w<first+count-1> outside every seat write root the way `git worktree add
        --no-checkout` does, every other one with an empty `config.worktree`; with `absent`, their directories are
        never made (prunable records, as after a deleted worktree)."""
        common = (self.repo / ".git").resolve()
        outside = Path(self.temp.name).resolve() / "many"
        outside.mkdir(exist_ok=True)
        for n in range(first, first + count):
            tree = outside / f"w{n}"
            admin = common / "worktrees" / f"w{n}"
            admin.mkdir(parents=True)
            (admin / "gitdir").write_text(f"{tree}/.git\n")
            (admin / "commondir").write_text("../..\n")
            (admin / "HEAD").write_text(f"{self.head}\n")
            if n % 2:
                (admin / "config.worktree").write_text("")
            if not absent:
                tree.mkdir()
                (tree / ".git").write_text(f"gitdir: {admin}\n")

    def spawn_counts(self):
        """Run a worker dry run and count what hcom-seat starts, recorded by bash itself: BASH_ENV installs a DEBUG
        trap, inherited by every function and subshell (`set -T`), that appends `$BASH_SUBSHELL`, the subshell level
        of the last record in this shell, and `$BASH_COMMAND` before each simple command, in one O_APPEND write. Two
        counts come out: the commands whose command word runs a program (an absolute path such as /usr/bin/stat or
        /bin/mkdir, a program found by name, or a variable command word such as `"${git_cmd[@]}"`; no builtin,
        keyword or function of hcom-seat or regime-env), and the forked subshells (a record whose level exceeds the
        last level its own shell recorded: each command substitution, pipeline element or `( … )` that runs a
        command). Every process hcom-seat itself starts is one of the two; what those processes start in turn
        (xargs's stat runs, git's helpers) is theirs. Deterministic: no clock, no host load, no trace interleaving."""
        names = subprocess.run(
            ["/bin/bash", "-c", "compgen -b; compgen -k"], capture_output=True, text=True, check=True
        )
        internal = set(names.stdout.split())
        for source in (SEAT, SEAT.parent / "regime-env"):
            internal |= set(re.findall(r"^\s*([A-Za-z_][A-Za-z0-9_]*)\(\) \{", source.read_text(), re.MULTILINE))
        hook = Path(self.temp.name) / "count-hook.bash"
        hook.write_text(
            "set -T\n"
            """trap 'builtin printf "%s\\t%s\\t%s\\0" "$BASH_SUBSHELL" "${u95_level:-0}" "$BASH_COMMAND" """
            """>> "$U95_TRACE"; u95_level=$BASH_SUBSHELL' DEBUG\n"""
        )
        trace = Path(self.temp.name) / "count-trace"
        trace.write_text("")
        env = {**self.env, "BASH_ENV": str(hook), "U95_TRACE": str(trace)}
        run = self.seat("worker", "--seats-root", self.seats, "--dry-run", **env)
        self.assertEqual(run.returncode, 0, run.stderr)
        assignment = re.compile(r"""^[A-Za-z_]\w*(\[[^]]*\])?\+?=("[^"]*"|'[^']*'|\$\([^)]*\)|[^\s"'])*(\s+|$)""")
        programs, subshells = collections.Counter(), 0
        for record in trace.read_text().split("\0")[:-1]:
            level, last, command = record.split("\t", 2)
            subshells += int(level) > int(last)
            if re.match(r"[A-Za-z_]\w*(\[[^]]*\])?\+?=\(", command):
                continue  # an array assignment runs nothing
            while (prefix := assignment.match(command)) and prefix.end():
                command = command[prefix.end() :]
            word = command.split()[0] if command.split() else ""
            if word.startswith(("/", '"$', "$")) or (re.fullmatch(r"[A-Za-z][\w.+-]*", word) and word not in internal):
                programs[word] += 1
        return programs, subshells

    def assert_same_counts(self, few, many):
        """The program counts, by name, and the subshell counts of two spawn_counts results are equal."""
        self.assertIn("/usr/bin/stat", few[0], "the counter sees programs run by absolute path")
        grown = many[0].copy()
        grown.subtract(few[0])
        self.assertEqual(+grown, collections.Counter(), "programs run more often with more worktrees")
        self.assertEqual(-grown, collections.Counter(), "programs run less often with more worktrees")
        self.assertEqual(many[1], few[1], "subshells forked with more worktrees and with fewer")

    def test_the_checks_start_no_more_processes_for_more_worktrees(self):
        """U95, a regression test for the measured shape "present worktrees": the overlap and git-state checks
        resolve worktree records in batches (one identity table, one size read, one pointer read, one resolving
        subshell), and a dry run with 300 registered worktrees started the same programs and subshells as one with 10.
        Not a general guarantee; the user-visible requirement is the launch latency (PR body). The configs here are
        absent or empty; non-empty ones have their own test. Counted by bash's own DEBUG trap (spawn_counts), not timed: a
        wall-clock bound inside the parallel suite is flaky. Before U95 the count grew with the worktrees (several
        stat runs and subshells per worktree and write root)."""
        self.seat("worker", "--seats-root", self.seats, "--dry-run")  # the private tool links exist from here on
        self.add_worktrees(0, 10)
        few = self.spawn_counts()
        self.add_worktrees(10, 290)
        self.assertEqual(len(self.git("worktree", "list").splitlines()), 301)
        self.assert_same_counts(few, self.spawn_counts())

    def test_each_non_empty_config_worktree_costs_one_git_config_and_an_empty_one_nothing(self):
        """U95 round 14: the one per-worktree cost the checks keep. git config validates one --file per run (a
        concatenation would let one file's section run into the next), so each non-empty `config.worktree` (a sparse
        checkout's `core.sparseCheckout`) costs exactly one git process in one subshell; an empty one (what a launch
        creates) is skipped by its size, and an absent one is not read. 10 worktrees with 5 empty configs, then 3 made
        sparse (+3), then 300 worktrees with 150 empty configs and the same 3 sparse (no more)."""
        self.seat("worker", "--seats-root", self.seats, "--dry-run")  # the private tool links exist from here on
        self.add_worktrees(0, 10)
        empty = self.spawn_counts()
        common = (self.repo / ".git").resolve()
        for n in (1, 3, 5):
            (common / f"worktrees/w{n}/config.worktree").write_text("[core]\n\tsparseCheckout = true\n")
        sparse = self.spawn_counts()
        grown = sparse[0].copy()
        grown.subtract(empty[0])
        self.assertEqual(+grown, collections.Counter({'"${git_cmd[@]}"': 3}), "one git per non-empty config.worktree")
        self.assertEqual(-grown, collections.Counter(), "nothing runs less often")
        self.assertEqual(sparse[1], empty[1] + 3, "one subshell per non-empty config.worktree")
        self.add_worktrees(10, 290)
        self.assert_same_counts(sparse, self.spawn_counts())

    def test_two_git_directories_recording_one_worktree_by_case_alias_refuse(self):
        """U95 round 15: on a case-insensitive volume (APFS by default; skipped on a case-sensitive one, detected at
        runtime) a second admin directory whose `gitdir` spells an existing worktree in other case makes git list two
        worktrees for one directory. `cd -P` keeps the spelling, so the texts differ; admin_dirs_match compares
        identities and refuses the duplicate."""
        tree = Path(self.temp.name).resolve() / "away" / "t"
        self.git("worktree", "add", "-q", "--detach", str(tree), "HEAD")
        alias = tree.parent.parent / "AWAY" / "T"
        if not (alias.exists() and alias.samefile(tree)):
            self.skipTest("a case-sensitive volume: no case alias")
        common = (self.repo / ".git").resolve()
        twin = common / "worktrees" / "twin"
        twin.mkdir()
        for name in ("commondir", "HEAD"):
            shutil.copy(common / "worktrees/t" / name, twin / name)
        (twin / "gitdir").write_text(f"{alias}/.git\n")
        self.assertIn(f"worktree {alias}\n", self.git("worktree", "list", "--porcelain") + "\n")
        for role in ("worker", "orchestrator"):
            with self.subTest(role=role):
                run = self.seat(role, "--seats-root", self.seats, "--dry-run")
                self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
                self.assertIn("which another worktree git directory records too", run.stderr)
        shutil.rmtree(twin)
        run = self.seat("worker", "--seats-root", self.seats, "--dry-run")
        self.assertEqual(run.returncode, 0, run.stderr)

    def test_a_worktree_record_not_backed_by_a_directory_refuses(self):
        """U95 round 16: a registered worktree whose path is a regular file, or lies below one, is a corrupt record,
        not a worktree: the launch refuses for both roles, dry runs included, naming the record and `git worktree
        prune`/`git worktree repair`, instead of resolving it with a per-record fallback process. Without the record
        the launch succeeds."""
        scratch = Path(self.temp.name).resolve()
        common = (self.repo / ".git").resolve()
        (scratch / "stale-file").write_text("")
        (scratch / "under").write_text("")
        for label, path in (("the path a regular file", scratch / "stale-file"), ("below a file", scratch / "under/x")):
            with self.subTest(label):
                admin = common / "worktrees" / "stale"
                admin.mkdir(parents=True)
                try:
                    (admin / "gitdir").write_text(f"{path}/.git\n")
                    (admin / "commondir").write_text("../..\n")
                    (admin / "HEAD").write_text(f"{self.head}\n")
                    self.assertIn(f"worktree {path}\n", self.git("worktree", "list", "--porcelain") + "\n")
                    for role in ("worker", "orchestrator"):
                        run = self.seat(role, "--seats-root", self.seats, "--dry-run")
                        self.assertEqual((run.returncode, run.stdout), (2, ""), f"{role}: {run.stderr}")
                        self.assertIn(f"the worktree record {path} is not backed by a directory", run.stderr)
                        self.assertIn("git worktree prune", run.stderr)
                        self.assertIn("git worktree repair", run.stderr)
                finally:
                    shutil.rmtree(admin)
        run = self.seat("worker", "--seats-root", self.seats, "--dry-run")
        self.assertEqual(run.returncode, 0, run.stderr)

    def test_more_seat_directories_start_no_more_processes(self):
        """U95 round 13: the seat directories under the seats root are resolved in one batch (physical_paths) in both
        overlap checks; a regression test for the measured shape "seats": a dry run with 10 of them started the same
        processes as one with 1. Before, each cost
        one physical_path subshell per check (1 vs 10 seats: 2 vs 11 substitutions per check)."""
        self.seat("worker", "--seats-root", self.seats, "--dry-run")  # the private tool links exist from here on
        seats = Path(self.seats)
        (seats / "s0").mkdir(parents=True)
        few = self.spawn_counts()
        for n in range(1, 10):
            (seats / f"s{n}").mkdir()
        self.assertEqual(len([p for p in seats.iterdir() if p.name.startswith("s")]), 10)
        self.assert_same_counts(few, self.spawn_counts())

    def test_absent_worktrees_start_no_more_processes_either(self):
        """U95 round 12: registered worktrees whose directories are gone (prunable records, outside every write root)
        are resolved in the same one subshell as present ones (physical_paths: the deepest existing ancestor by
        builtins, then `cd -P`); a regression test for the measured shape "absent": 300 of them started the same
        processes as 10. Before, each absent path cost
        two subshells of physical_path (10 vs 300 absent: 21 vs 601 subshells)."""
        self.seat("worker", "--seats-root", self.seats, "--dry-run")  # the private tool links exist from here on
        self.add_worktrees(0, 10, absent=True)
        self.assertEqual(self.git("worktree", "list").count("prunable"), 10)
        few = self.spawn_counts()
        self.add_worktrees(10, 290, absent=True)
        self.assertEqual(self.git("worktree", "list").count("prunable"), 300)
        self.assert_same_counts(few, self.spawn_counts())

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

    def test_every_omp_launch_makes_the_routers_credential_root_and_denies_it_for_read_and_write(self):
        """U353d (verdict U353-318f268d P1 `:2383` and P2 `:2393`; the mechanism-change row of 2026-11-07T12:55:26Z,
        form remove). srt 0.0.81's Linux backend mounts nothing for a denyRead entry that is not there
        (`dist/sandbox/linux-sandbox-utils.js:1810-1812`), so the U353b row, which named `<DSH_HOME>/router-credentials`
        whether or not it existed, left an omp seat started before the Router's first launch free to read the login
        once the Router had made the root; and the omp rows denied the root for read alone, so a worker launched with
        `DSH_HOME` equal to `HCOM_DIR` held the root under an allowWrite root with no covering denyWrite. Now every
        launch of every role makes the root (the caller's `DSH_HOME`, else `~/.dsh`, held to a clean path and resolved
        physically, a linked home through its target; the home made too when absent) as a 0700 directory of this user
        before the settings file is written, and the orchestrator and worker rows carry its physical path once in
        denyRead and once in denyWrite with no grant at or under it; a present root is kept; a dry run makes nothing and
        says what a launch would make; a planted link or file at the root's path refuses by name with nothing made and
        nothing started; a `DSH_HOME` that is not a clean absolute path refuses."""
        home = self.home.resolve()
        default_root = home / ".dsh/router-credentials"
        run = self.seat("worker", "--seats-root", self.seats, "--dry-run")
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertIn(
            f"hcom-seat: the worker role's credential root {default_root} does not exist; a launch creates it (0700)",
            run.stderr,
        )
        self.assertFalse((home / ".dsh").exists() or (home / ".dsh").is_symlink(), "a dry run makes nothing")
        for role in ("worker", "orchestrator"):
            with self.subTest(role=role):
                run = self.seat(role, "--seats-root", self.seats)
                self.assertEqual(run.returncode, 0, run.stderr)
                self.assertNotIn("does not exist; a launch creates it", run.stderr)
                self.assertTrue(default_root.is_dir() and not default_root.is_symlink(), "the launch makes the root")
                self.assertEqual(stat.S_IMODE(default_root.stat().st_mode), 0o700)
                self.assertEqual(default_root.stat().st_uid, os.geteuid(), "a directory of this user")
                self.assertEqual(stat.S_IMODE((home / ".dsh").stat().st_mode), 0o700, "the absent home is made 0700")
                settings_file = Path(self.seats, ".sandbox", role, "srt-settings.json")
                self.assertLessEqual(
                    default_root.stat().st_mtime_ns,
                    settings_file.stat().st_mtime_ns,
                    "the root exists before the settings file is written",
                )
                fs = self.settings_of(role)["filesystem"]
                self.assertEqual(fs["denyRead"].count(str(default_root)), 1, fs["denyRead"])
                self.assertEqual(fs["denyWrite"].count(str(default_root)), 1, fs["denyWrite"])
                for key in ("allowRead", "allowWrite"):
                    under = [row for row in fs[key] if row == str(default_root) or row.startswith(f"{default_root}/")]
                    self.assertEqual(under, [], key)
                self.assertEqual(list(default_root.iterdir()), [], "the root is made empty and nothing is placed in it")
        self.assertEqual(len(self.calls_of("omp")), 2, "both launches reached omp")
        # A caller's DSH_HOME, spelled directly and through a link: the row and the made root are the physical path.
        other_home = Path(self.temp.name).resolve() / "other-dsh-home"
        other_home.mkdir()
        linked = Path(self.temp.name).resolve() / "linked-dsh-home"
        linked.symlink_to(other_home)
        other_root = other_home / "router-credentials"
        for spelled in (other_home, linked):
            with self.subTest(dsh_home=str(spelled)):
                run = self.seat("worker", "--seats-root", self.seats, DSH_HOME=str(spelled))
                self.assertEqual(run.returncode, 0, run.stderr)
                self.assertTrue(other_root.is_dir() and not other_root.is_symlink())
                self.assertEqual(stat.S_IMODE(other_root.stat().st_mode), 0o700)
                fs = self.settings_of("worker")["filesystem"]
                self.assertEqual(
                    (fs["denyRead"].count(str(other_root)), fs["denyWrite"].count(str(other_root))), (1, 1)
                )
                self.assertNotIn(str(default_root), fs["denyRead"] + fs["denyWrite"])
        # DSH_HOME equal to HCOM_DIR (the auditor's probe): the root lies under the store, a write root of the worker,
        # and the denyWrite row covers it.
        store_root = self.store.resolve() / "router-credentials"
        run = self.seat("worker", "--seats-root", self.seats, DSH_HOME=str(self.store))
        self.assertEqual(run.returncode, 0, run.stderr)
        fs = self.settings_of("worker")["filesystem"]
        self.assertIn(str(self.store.resolve()), fs["allowWrite"])
        self.assertEqual((fs["denyRead"].count(str(store_root)), fs["denyWrite"].count(str(store_root))), (1, 1))
        self.assertTrue(store_root.is_dir() and not store_root.is_symlink())
        self.assertEqual(stat.S_IMODE(store_root.stat().st_mode), 0o700)
        # A DSH_HOME that is no clean absolute path refuses before anything is resolved.
        run = self.seat("worker", "--seats-root", self.seats, DSH_HOME="relative/dsh")
        self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
        self.assertIn("DSH_HOME 'relative/dsh' is not a clean absolute path", run.stderr)
        # A planted link (into the operator's own gh directory) or a regular file at the root's path refuses by name,
        # for both omp roles, in a dry run too, with no seats root, no tool run and nothing at the link's target.
        planted_home = Path(self.temp.name).resolve() / "planted-dsh-home"
        planted_home.mkdir()
        outside = home / ".config/gh"
        outside.mkdir(parents=True)
        planted = planted_home / "router-credentials"
        planted.symlink_to(outside)
        fresh_seats = str(Path(self.temp.name).resolve() / "fresh-seats")
        tools_before = (len(self.calls_of("srt")), len(self.calls_of("hcom")), len(self.calls_of("omp")))
        for role in ("worker", "orchestrator"):
            for args in ([], ["--dry-run"]):
                with self.subTest(case="a link", role=role, args=args):
                    run = self.seat(role, "--seats-root", fresh_seats, *args, DSH_HOME=str(planted_home))
                    self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
                    self.assertIn(
                        f"the {role} role's credential root {planted} is a symbolic link; it must be a real directory"
                        " inside DSH_HOME, or absent",
                        run.stderr,
                    )
                    self.assertFalse(Path(fresh_seats).exists(), "no seats root and no settings file")
                    self.assertEqual(list(outside.iterdir()), [], "nothing written at the link's target")
        planted.unlink()
        planted.write_text("")
        for role in ("worker", "orchestrator"):
            with self.subTest(case="a regular file", role=role):
                run = self.seat(role, "--seats-root", fresh_seats, DSH_HOME=str(planted_home))
                self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
                self.assertIn(f"the {role} role's credential root {planted} exists and is not a directory", run.stderr)
                self.assertFalse(Path(fresh_seats).exists())
        self.assertEqual(
            (len(self.calls_of("srt")), len(self.calls_of("hcom")), len(self.calls_of("omp"))),
            tools_before,
            "no refused launch ran a tool",
        )

    def make_store_root(self):
        """The program store's root as regime-init leaves it (U215c): `regime-store` and `<slug>` under the scratch
        HOME's `.local/state`, each a 0700 directory of this user, the shape hcom-seat holds every component to
        (U219c; a parent made with Python's default mode is refused by the launch, as regime-init refuses it)."""
        root = self.home.resolve() / ".local/state/regime-store/repo"
        root.parent.mkdir(parents=True, mode=0o700)
        root.mkdir(mode=0o700)
        return root

    def store_root_modes(self, root):
        """(mode, is a real directory, owned by this user) of the root and of its `regime-store` parent."""
        return [
            (stat.S_IMODE(os.lstat(p).st_mode), p.is_dir() and not p.is_symlink(), os.lstat(p).st_uid == os.getuid())
            for p in (root.parent, root)
        ]

    def test_the_store_root_is_read_by_both_roles_and_written_by_the_orchestrator_alone(self):
        """U219 (store move 3 of 5, handoff/07-store-move-design.md): regime-env derives the program store's root
        `<physical HOME>/.local/state/regime-store/<slug>` (U215c) and hcom-seat grants it, in its physical form, to
        the worker's and the orchestrator's `allowRead` and to the orchestrator's `allowWrite` (its row 7, the held
        slot after `~/.omp/run`, printed verbatim, U219c) and to no other grant list: the worker reads the records and
        writes none, and its `denyWrite` carries the root (U219c, verdict U219-985b7c04 P1 `:1981`: the deny srt
        applies under any grant a link could fold onto the root), the orchestrator's does not. A launch that finds the
        root absent makes it (U219c, the same verdict's P2 `:1815`: srt 0.0.81's Linux backend skips an absent write
        or deny path), both components 0700 directories of this user, before its settings file is written; a root
        regime-init made passes as it is. No seat grants the hcom store's `~/.local/state/hcom` tree or
        `~/.local/state/regime-store` above the root."""
        home = self.home.resolve()
        root = home / ".local/state/regime-store/repo"
        for present in (False, True):
            if present:
                self.assertEqual(self.store_root_modes(root), [(0o700, True, True)] * 2, "made by the earlier launch")
            else:
                self.assertFalse(root.parent.exists(), "absent before the first launch")
            for role in ("worker", "orchestrator"):
                with self.subTest(role=role, present=present):
                    run = self.seat(role, "--seats-root", self.seats)
                    self.assertEqual(run.returncode, 0, run.stderr)
                    fs = self.settings_of(role)["filesystem"]
                    self.assertEqual(fs["allowRead"].count(str(root)), 1, fs["allowRead"])
                    self.assertEqual(
                        fs["allowWrite"].count(str(root)), 1 if role == "orchestrator" else 0, fs["allowWrite"]
                    )
                    if role == "orchestrator":
                        self.assertEqual(fs["allowWrite"][7], str(root), "row 7, the held slot after ~/.omp/run")
                        self.assertEqual(fs["allowWrite"][6], str(home / ".omp/run"))
                    self.assertEqual(
                        fs["denyWrite"].count(str(root)), 0 if role == "orchestrator" else 1, fs["denyWrite"]
                    )
                    self.assertEqual(
                        [row for row in fs["denyRead"] if row == str(root) or row.startswith(f"{root}/")], []
                    )
                    self.assertEqual([row for row in fs["denyWrite"] if row.startswith(f"{root}/")], [])
                    for key in ("allowRead", "allowWrite"):
                        above = [row for row in fs[key] if Path(row) in root.parents]
                        self.assertEqual(above, [], f"{key} grants a directory above the root")
                    self.assertEqual(
                        fs["allowWrite"][2],
                        str(Path(self.seats, f".state/claude-{role}")),
                        "row 2 is the group directory",
                    )
                    self.assertEqual(
                        self.store_root_modes(root), [(0o700, True, True)] * 2, "the launch makes the root"
                    )
        self.assertEqual(len(self.calls_of("omp")), 4, "every launch reached omp")
        # The dry run names the derived root beside the pair (the seat inherits it from regime-env's export, U215c;
        # the fake hcom records HCOM_* names alone, so the export is read here, on stderr).
        run = self.seat("worker", "--seats-root", self.seats, "--dry-run")
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertIn(f"environment HCOM_DIR={self.store} HCOM_TEAM=repo REGIME_STORE_ROOT={root}", run.stderr)

    def test_an_hcom_store_that_is_inside_or_contains_the_store_root_is_refused_by_name(self):
        """U219 (verdict U215-15c6be1e P1 `:127`, held residual on this unit): the hcom store `HCOM_DIR` is every seat's
        write grant, so a store root equal to it, inside it or containing it would put the records inside a worker's
        write root. The launch is refused naming both paths (exit 2, nothing printed on stdout) right after regime-env
        derives the root, before the seats root, a slot, a settings file or hcom exists, for both roles and in a dry
        run too; the paths are compared physically (a link spelling the store is seen through), so `HCOM_DIR` through a
        link into the root is refused as well; a store beside the root, under `~/.local/state/hcom`, passes."""
        home = self.home.resolve()
        root = self.make_store_root()
        linked = home / "store-link"
        linked.symlink_to(root)
        fresh_seats = str(Path(self.temp.name).resolve() / "fresh-seats")
        for label, store, message in (
            ("equal", root, f"the hcom store HCOM_DIR {root} is the store root REGIME_STORE_ROOT {root}"),
            (
                "inside",
                root / "hcom",
                f"the hcom store HCOM_DIR {root}/hcom lies inside the store root REGIME_STORE_ROOT {root}",
            ),
            (
                "containing",
                root.parent,
                f"the hcom store HCOM_DIR {root.parent} contains the store root REGIME_STORE_ROOT {root}",
            ),
            (
                "through a link",
                linked,
                f"the hcom store HCOM_DIR {linked} ({root}) is the store root REGIME_STORE_ROOT {root}",
            ),
        ):
            for role in ("worker", "orchestrator"):
                for args in ([], ["--dry-run"]):
                    with self.subTest(label, role=role, args=args):
                        run = self.seat(role, "--seats-root", fresh_seats, *args, HCOM_DIR=str(store))
                        self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
                        self.assertIn(message, run.stderr)
                        self.assertIn("every seat's write grant", run.stderr)
                        self.assertFalse(Path(fresh_seats).exists(), "no seats root, no slot, no settings file")
        self.assertEqual(self.calls_of("hcom"), [])
        self.assertEqual(sorted(p.name for p in root.iterdir()), [], "nothing made under the root")
        # The control: the derived store beside the root passes and the settings carry both.
        derived = home / ".local/state/hcom/repo"
        derived.mkdir(parents=True)
        (derived / "origin").write_text(f"{self.repo}\n")
        run = self.seat("worker", "--seats-root", self.seats, HCOM_DIR=None, HCOM_TEAM=None)
        self.assertEqual(run.returncode, 0, run.stderr)
        fs = self.settings_of("worker")["filesystem"]
        self.assertIn(str(derived), fs["allowWrite"])
        self.assertIn(str(root), fs["allowRead"])

    def test_an_executable_planted_under_the_store_root_never_runs(self):
        """U219b (verdict U219-ce7e875e P1 `:2158`): the orchestrator writes `<HOME>/.local/state/regime-store/<slug>`,
        so the parent `~/.local/state/regime-store` is in the protected set whole, from the lever's start, like
        `~/.local/state/hcom` and `~/.local/state/omp-seats`: a `git` planted under the root and first on the caller's
        PATH is refused by name before anything runs it (round 1 granted the root in the settings but not here, and the
        auditor's planted git ran three times on the host before the late write-root refusal), for both roles, in a
        launch and in a dry run; the planted file never runs (the record it would write does not exist), no seats
        root, slot or settings file is made, and hcom is never called."""
        home = self.home.resolve()
        root = self.make_store_root()
        planted = root / "bin"
        marker = self.plant(planted, "git")
        for role in ("worker", "orchestrator"):
            for args in ([], ["--dry-run"]):
                with self.subTest(role=role, args=args):
                    run = self.seat(role, "--seats-root", self.seats, *args, PATH=f"{planted}:{self.env['PATH']}")
                    self.assertFalse(marker.exists(), marker.read_text() if marker.exists() else "")
                    self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
                    self.assertIn(
                        f"git {planted}/git is or lies under the seat write root {home}/.local/state/regime-store",
                        run.stderr,
                    )
                    self.assertFalse(Path(self.seats).exists(), "no seats root, no slot, no settings file")
        self.assertEqual(self.calls_of("hcom"), [])
        # The control: the same root, nothing planted on PATH, launches and grants the root as round 1 did.
        run = self.seat("orchestrator", "--seats-root", self.seats)
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertIn(str(root), self.settings_of("orchestrator")["filesystem"]["allowWrite"])

    def test_a_write_root_that_is_or_lies_inside_the_store_root_is_refused_before_any_settings_file(self):
        """U219c (verdict U219-985b7c04 P1 `:1981`): round 2 judged `HCOM_DIR` alone against the store root, so a
        worker whose `~/.omp/run` was a link to the root launched with the records in its `allowWrite`. Every rendered
        `allowWrite` row of every role is judged against the root by identity (`store_root_judge`, the judge's first
        step; the orchestrator's own held row 7 alone is exempt, by its position and byte equality): a worker's
        `~/.omp/run` linked to the root and an orchestrator whose `~/.omp/profiles/orchestrator` links to the root
        each refuse (exit 2) naming the row and the root, before the settings file is written and before hcom runs
        (the worker's worktree exists by then: its render needs it, and git's `HEAD is now at` is the one line on
        stdout). A seats root inside the root, so a worker whose own slot lies inside it, is refused earlier and by
        construction: the orchestrator's row 7 is the root, which contains the seats root, the overlap invariant's
        protected path (`seat_overlap_check`), before anything is made under the root. The same launches pass once
        the link is a directory again."""
        home = self.home.resolve()
        root = self.make_store_root()
        (home / ".omp/profiles").mkdir(parents=True)
        run_root, profile = home / ".omp/run", home / ".omp/profiles/orchestrator"
        inner_seats = str(root / "seats")
        judged = "is, contains or lies inside the store root REGIME_STORE_ROOT"
        cases = (
            ("the worker's ~/.omp/run linked to the root", "worker", run_root, self.seats,
             f"the worker role's allowWrite row {root} {judged} {root}; the launch is refused before its settings file is written"),
            ("the worker's own slot inside the root", "worker", None, inner_seats,
             f"the orchestrator seat's write root {root} contains the seats root {inner_seats}; seat write roots must not overlap"),
            ("the orchestrator's profile linked to the root", "orchestrator", profile, self.seats,
             f"the orchestrator role's allowWrite row {root} {judged} {root}; the launch is refused before its settings file is written"),
        )  # fmt: skip
        for label, role, link, seats, message in cases:
            with self.subTest(case=label):
                try:
                    if link is not None:
                        link.symlink_to(root)
                    run = self.seat(role, "--seats-root", seats)
                    self.assertEqual(run.returncode, 2, run.stderr)
                    self.assertIn(run.stdout.split(" ")[0], ("", "HEAD"), f"git's worktree echo at most: {run.stdout}")
                    self.assertIn(message, run.stderr)
                    self.assertFalse(Path(seats, ".sandbox").exists(), "no settings file, no shim")
                    if link is not None:
                        self.assertTrue(link.is_symlink(), "the launch neither removed nor replaced the link")
                finally:
                    if link is not None and link.is_symlink():
                        link.unlink()
        self.assertEqual(self.calls_of("hcom"), [])
        self.assertEqual(sorted(p.name for p in root.iterdir()), [], "nothing made under the root")
        # The control: with `~/.omp/run` and the profile real directories, both roles launch and the root is granted
        # as before (the worker's deny row, the orchestrator's held write row).
        for role in ("worker", "orchestrator"):
            run = self.seat(role, "--seats-root", self.seats)
            self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual(self.settings_of("worker")["filesystem"]["denyWrite"].count(str(root)), 1)
        self.assertEqual(self.settings_of("orchestrator")["filesystem"]["allowWrite"][7], str(root))

    def test_the_orchestrators_store_root_row_is_the_held_path_through_a_swap_between_the_hold_and_the_render(self):
        """U219c (verdict U219-985b7c04 P1 `:2161`): round 2 put the held root into `extra`, which `seat_write_roots`
        resolves again, so a directory-to-link swap of the root during `seat_roots_out`, restored right after,
        rendered the link's target (the auditor's `~/.config/autostart`) as the orchestrator's write root. The swap is
        injected through bash's DEBUG trap (BASH_ENV): the root becomes a link to `~/.config/autostart` right before
        the top-level `seat_roots_out=...` command and is restored at the next command. The rendered `allowWrite`
        carries the held path at row 7 and the target nowhere; the trap's record proves the swap happened."""
        home = self.home.resolve()
        root = self.make_store_root()
        outside = home / ".config/autostart"
        outside.mkdir(parents=True)
        mark = Path(self.temp.name) / "swap-mark"
        hook = Path(self.temp.name) / "swap-hook.bash"
        hook.write_text(
            "__u219_swapped=0\n"
            "trap '"
            'if [[ ${__u219_swapped} == 0 && ${BASH_COMMAND} == "seat_roots_out="* ]]; then '
            '/bin/mv "${U219_ROOT-}" "${U219_ROOT-}.held" && /bin/ln -s "${U219_OUTSIDE-}" "${U219_ROOT-}"'
            ' && __u219_swapped=1 && builtin echo swapped >> "${U219_MARK-}"; '
            "elif [[ ${__u219_swapped} == 1 ]]; then "
            '/bin/rm "${U219_ROOT-}" && /bin/mv "${U219_ROOT-}.held" "${U219_ROOT-}"'
            ' && __u219_swapped=2 && builtin echo restored >> "${U219_MARK-}"; '
            "fi' DEBUG\n"
        )
        run = self.seat(
            "orchestrator", "--seats-root", self.seats,
            BASH_ENV=str(hook), U219_ROOT=str(root), U219_OUTSIDE=str(outside), U219_MARK=str(mark),
        )  # fmt: skip
        self.assertEqual(mark.read_text(), "swapped\nrestored\n", "the swap ran around seat_roots_out")
        self.assertEqual(run.returncode, 0, run.stderr)
        settings = self.settings_of("orchestrator")
        self.assertNotIn(str(outside), json.dumps(settings), "the link's target is granted nowhere")
        self.assertEqual(settings["filesystem"]["allowWrite"][7], str(root), settings["filesystem"]["allowWrite"])
        self.assertEqual(settings["filesystem"]["allowWrite"].count(str(root)), 1)
        self.assertTrue(root.is_dir() and not root.is_symlink(), "the root is a directory again")
        self.assertEqual(sorted(outside.iterdir()), [], "nothing written at the target")
        self.assertEqual(len(self.calls_of("omp")), 1)

    def test_a_launch_makes_the_absent_store_root_before_its_settings_file_and_a_planted_entry_refuses_by_name(self):
        """U219c (verdict U219-985b7c04 P2 `:1815`): srt 0.0.81's Linux backend skips an absent write path and an
        absent deny path, so a root granted but never made left the first `regime-init` inside a Linux orchestrator
        seat unable to write it and the worker's deny void. A launch of either role whose root is absent makes both
        components (`regime-store`, `<slug>`) 0700 directories of this user, before `seat_sandbox_write` writes the
        settings file (bash's DEBUG trap records the order); a dry run makes nothing and says what a launch would make;
        a symbolic link or a regular file at either component refuses by name (regime-env's hold of the components,
        U215c) and so does a directory of another mode (the launch's hold, as regime-init refuses it), exit 2 and
        nothing on stdout, launch and dry run alike, before the seats root, a slot or a settings file exists."""
        home = self.home.resolve()
        root = home / ".local/state/regime-store/repo"
        trace = Path(self.temp.name) / "trace"
        hook = Path(self.temp.name) / "trace-hook.bash"
        hook.write_text(
            'set -T\ntrap \'builtin printf "%s\\t%s\\0" "$BASH_COMMAND" "${path-}" >> "$U219_TRACE"\' DEBUG\n'
        )
        with self.subTest(case="a dry run makes nothing"):
            run = self.seat("worker", "--seats-root", self.seats, "--dry-run")
            self.assertEqual(run.returncode, 0, run.stderr)
            self.assertIn(f"the program store's root {root} does not exist; a launch creates it (0700)", run.stderr)
            self.assertFalse(root.parent.exists())
        for role in ("worker", "orchestrator"):
            with self.subTest(case="a launch makes it", role=role):
                try:
                    trace.write_text("")
                    run = self.seat(role, "--seats-root", self.seats, BASH_ENV=str(hook), U219_TRACE=str(trace))
                    self.assertEqual(run.returncode, 0, run.stderr)
                    self.assertEqual(self.store_root_modes(root), [(0o700, True, True)] * 2)
                    commands = trace.read_text().split("\0")[:-1]
                    made = [i for i, c in enumerate(commands) if c == f'/bin/mkdir "${{path}}"\t{root}']
                    written = [i for i, c in enumerate(commands) if c.startswith("seat_sandbox_write\t")]
                    self.assertTrue(made and written, (made, written))
                    self.assertLess(made[0], written[0], "the root is made before the settings file is written")
                    self.assertTrue(Path(self.seats, ".sandbox", role, "srt-settings.json").is_file())
                finally:
                    if root.parent.exists():
                        shutil.rmtree(root.parent)
        self.assertEqual(len(self.calls_of("omp")), 2)
        outside = home / ".config/autostart"
        outside.mkdir(parents=True)
        fresh_seats = str(Path(self.temp.name).resolve() / "fresh-seats")
        wrong = home / ".local/state/regime-store"

        def planted(kind, path):
            if kind == "link":
                path.symlink_to(outside)
                return f"the store root component {path} is a symlink"
            if kind == "file":
                path.write_text("")
                return f"the store root component {path} is not a real directory of this user"
            path.mkdir(mode=0o755)
            os.chmod(path, 0o755)
            return f"the store root component {path} has mode 755, not 0700"

        def cleared():
            if wrong.is_symlink() or wrong.is_file():
                wrong.unlink()
            elif wrong.is_dir():
                shutil.rmtree(wrong)

        for kind in ("link", "file", "mode"):
            for component in (wrong, root):
                for role in ("worker", "orchestrator"):
                    for args in ([], ["--dry-run"]):
                        with self.subTest(kind=kind, component=component.name, role=role, args=args):
                            try:
                                if component is root:
                                    wrong.mkdir(mode=0o700)
                                message = planted(kind, component)
                                run = self.seat(role, "--seats-root", fresh_seats, *args)
                                self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
                                self.assertIn(message, run.stderr)
                                self.assertFalse(Path(fresh_seats).exists(), "no seats root, no slot, no settings file")
                                self.assertEqual(sorted(outside.iterdir()), [], "nothing written at a link's target")
                            finally:
                                cleared()
        self.assertEqual(len(self.calls_of("omp")), 2, "no refused launch reached omp")


if __name__ == "__main__":
    unittest.main()
