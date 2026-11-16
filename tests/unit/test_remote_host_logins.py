"""Seat logins on a remote host (regime-cutover U37): the laptop URL opener and its seat-host client, the
token export, the SSH forwards, the launchd agent and the seat-login pre-flight lever. Everything runs
against scratch homes and fake openers; no test opens a browser or reads a real login."""

import json
import os
import plistlib
import pty
import re
import select
import shutil
import socket
import stat
import subprocess
import sys
import tempfile
import time
import unittest
import urllib.error
import urllib.request
from pathlib import Path
from typing import ClassVar

ROOT = Path(__file__).resolve().parents[2]
COMMON = ROOT / "home/dot_local/bin/common"
OPENER = COMMON / "executable_regime-url-opener"
OPEN_URL = COMMON / "executable_regime-open-url"
PREFLIGHT = ROOT / "scripts/orchestrator/seat-login-preflight"
# The operator's one writer of the seats' Claude token file (regime-cutover U551).
PLACER = ROOT / "scripts/orchestrator/seat-token-place"
HCOM_SEAT = ROOT / "scripts/orchestrator/hcom-seat"
ZSHENV = ROOT / "home/dot_zshenv"
PROFILE = ROOT / "home/dot_profile"
SSH_CONFIG = ROOT / "home/private_dot_ssh/private_config.tmpl"
PLIST = ROOT / "home/Library/LaunchAgents/com.mryfmo.dotfiles.url-opener.plist.tmpl"
CHEZMOI = shutil.which("chezmoi")
SIWC_URL = "https://auth.openai.com/api/accounts/authorize?response_type=code&state=s&code_challenge=c"
CLAUDE_URL = "https://claude.com/cai/oauth/authorize?code=true&state=s"
HOST_ID = "urn:uuid:11111111-1111-4111-8111-111111111111"
# Built at runtime, so this file never holds a literal the committed-secret scan matches.
TOKEN_VARIABLE = "CLAUDE_CODE_OAUTH_" + "TOKEN"
FAKE_OAUTH_VALUE = "fake-" + "oauth-value"
# The fixture's seats' Claude setup-token (regime-cutover U551): the form the preflight holds the token file to (TOKEN_FORM_RE,
# one text with hcom-seat, seat-token-place and acp-broker), never a real token, built at runtime so no file holds a
# literal the secret scan matches; it must appear in no line of the lever.
FAKE_OAT = "sk-ant-oat01-" + "FAKETOKENFORTEST" + "0" * 44


def write_exec(path: Path, body: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body)
    path.chmod(0o755)
    return path


def render(text: str, os_name: str) -> str:
    with tempfile.TemporaryDirectory() as temp:
        result = subprocess.run(
            [CHEZMOI, "--source", temp, "--cache", f"{temp}/cache", "--persistent-state", f"{temp}/state",
             "execute-template", "--init", "--override-data",
             json.dumps({"chezmoi": {"os": os_name, "homeDir": "/render-home"}})],
            input=text, text=True, capture_output=True, check=True,
        )  # fmt: skip
    return result.stdout


class UrlOpenerTest(unittest.TestCase):
    """`regime-url-opener` opens only allow-listed https sign-in URLs, logs no query, and binds loopback."""

    def setUp(self) -> None:
        self.temp = Path(tempfile.mkdtemp(prefix="url-opener-"))
        self.opened = self.temp / "opened.txt"
        for name in ("open", "xdg-open"):
            write_exec(self.temp / "bin" / name, f'#!/bin/sh\nprintf "%s\\n" "$*" >> "{self.opened}"\n')
        self.log = self.temp / "state/url-opener.log"
        env = {"PATH": f"{self.temp / 'bin'}:/usr/bin:/bin", "HOME": str(self.temp)}
        self.server = subprocess.Popen(
            [sys.executable, "-I", str(OPENER), "--port", "0", "--log", str(self.log)],
            env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
        )  # fmt: skip
        line = self.server.stdout.readline()
        self.assertTrue(line.startswith("regime-url-opener: listening on 127.0.0.1:"), line)
        self.port = int(line.rsplit(":", 1)[1])

    def tearDown(self) -> None:
        self.server.terminate()
        self.server.communicate(timeout=10)
        shutil.rmtree(self.temp)

    def post(self, body: str, headers: dict[str, str] | None = None, path: str = "/open") -> int:
        request = urllib.request.Request(
            f"http://127.0.0.1:{self.port}{path}", data=body.encode(), method="POST",
            headers={"X-Regime-Open": "1"} if headers is None else headers,
        )  # fmt: skip
        try:
            with urllib.request.build_opener(urllib.request.ProxyHandler({})).open(request, timeout=10) as response:
                return response.status
        except urllib.error.HTTPError as error:
            return error.code

    def opened_urls(self) -> list[str]:
        return self.opened.read_text().splitlines() if self.opened.exists() else []

    def test_allow_listed_sign_in_urls_are_opened_with_the_system_opener(self) -> None:
        self.assertEqual(self.post(SIWC_URL), 200)
        self.assertEqual(self.post(CLAUDE_URL), 200)
        self.assertEqual(self.opened_urls(), [SIWC_URL, CLAUDE_URL])

    def test_a_fresh_home_gets_the_log_parent_and_the_start_is_recorded(self) -> None:
        # setUp started the opener with a log under a directory that did not exist, as on a fresh home.
        self.assertEqual(stat.S_IMODE(self.log.parent.stat().st_mode), 0o700)
        self.assertRegex(self.log.read_text(), rf"^\S+Z listening on 127\.0\.0\.1:{self.port}\n$")

    def test_anything_else_is_refused_and_nothing_opens(self) -> None:
        cases = {
            "https://evil.example/authorize": 403,
            "http://auth.openai.com/api/accounts/authorize": 403,
            "https://user:pw@auth.openai.com/x": 403,
            "https://auth.openai.com:8443/x": 403,
            "https://auth.openai.com.evil.example/x": 403,
            "file:///etc/passwd": 403,
            f"{SIWC_URL} {CLAUDE_URL}": 400,
            "": 400,
        }
        for url, status in cases.items():
            with self.subTest(url=url):
                self.assertEqual(self.post(url), status)
        with self.subTest("no X-Regime-Open header (a web page in the browser)"):
            self.assertEqual(self.post(SIWC_URL, headers={}), 403)
        with self.subTest("another path"):
            self.assertEqual(self.post(SIWC_URL, path="/"), 404)
        self.assertEqual(self.opened_urls(), [])

    def test_the_log_names_the_decision_and_never_the_query(self) -> None:
        self.post(SIWC_URL)
        self.post("https://evil.example/authorize?code=secret-looking")
        log = self.log.read_text()
        self.assertRegex(
            log, r"\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ opened https://auth.openai.com/api/accounts/authorize\n"
        )
        self.assertIn("refused host not on the allow-list https://evil.example/authorize\n", log)
        self.assertNotIn("state=", log)
        self.assertNotIn("secret-looking", log)
        self.assertEqual(stat.S_IMODE(self.log.parent.stat().st_mode), 0o700)

    def test_the_client_hands_the_url_to_the_opener(self) -> None:
        env = {"PATH": "/usr/bin:/bin", "REGIME_URL_OPENER_PORT": str(self.port)}
        result = subprocess.run(
            [sys.executable, "-I", str(OPEN_URL), SIWC_URL], check=False, env=env, capture_output=True, text=True
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.opened_urls(), [SIWC_URL])
        refused = subprocess.run(
            [sys.executable, "-I", str(OPEN_URL), "https://evil.example/x"],
            check=False,
            env=env,
            capture_output=True,
            text=True,
        )
        self.assertEqual(refused.returncode, 1)
        self.assertIn("refused the URL (403", refused.stderr)


class OpenUrlWithoutOpenerTest(unittest.TestCase):
    def test_no_opener_is_a_named_failure_and_the_caller_keeps_the_url(self) -> None:
        with socket.socket() as probe:
            probe.bind(("127.0.0.1", 0))
            port = probe.getsockname()[1]
        env = {"PATH": "/usr/bin:/bin", "REGIME_URL_OPENER_PORT": str(port)}
        result = subprocess.run(
            [sys.executable, "-I", str(OPEN_URL), SIWC_URL], check=False, env=env, capture_output=True, text=True
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn(f"no laptop opener on 127.0.0.1:{port}", result.stderr)
        self.assertIn("open the URL shown above yourself", result.stderr)

    @unittest.skipUnless(Path("/usr/bin/python3").exists(), "no system python3")
    def test_both_scripts_compile_under_the_system_python_launchd_uses(self) -> None:
        for script in (OPENER, OPEN_URL):
            with self.subTest(script=script.name):
                result = subprocess.run(
                    ["/usr/bin/python3", "-I", "-c", "import ast, sys; ast.parse(open(sys.argv[1]).read())", str(script)],
                    check=False, capture_output=True, text=True,
                )  # fmt: skip
                self.assertEqual(result.returncode, 0, result.stderr)


class OpenerStartTest(unittest.TestCase):
    def test_a_failed_bind_is_recorded_in_the_log_it_creates(self) -> None:
        """Under launchd stdout and stderr are /dev/null, so the log is the only place a start failure shows."""
        with tempfile.TemporaryDirectory() as temp, socket.socket() as taken:
            taken.bind(("127.0.0.1", 0))
            taken.listen()
            port = taken.getsockname()[1]
            log = Path(temp) / "fresh/state/url-opener.log"
            result = subprocess.run(
                [sys.executable, "-I", str(OPENER), "--port", str(port), "--log", str(log)],
                env={"PATH": "/usr/bin:/bin", "HOME": temp}, capture_output=True, text=True, timeout=30, check=False,
            )  # fmt: skip
            self.assertEqual(result.returncode, 1, result.stderr)
            self.assertIn(f"cannot bind 127.0.0.1:{port}", result.stderr)
            self.assertRegex(log.read_text(), rf"^\S+Z failed to bind 127\.0\.0\.1:{port}: .+\n$")

    def test_the_opener_starts_without_a_reverse_dns_lookup(self) -> None:
        """HTTPServer.server_bind calls socket.getfqdn, which took about 35 s per start on macos-15 runners."""
        probe = (
            "import runpy, socket, sys\n"
            "def refuse(*args):\n"
            "    print('getfqdn called', file=sys.stderr, flush=True)\n"
            "    raise SystemExit(3)\n"
            "socket.getfqdn = refuse\n"
            "sys.argv = sys.argv[1:]\n"
            "runpy.run_path(sys.argv[0], run_name='__main__')\n"
        )
        with tempfile.TemporaryDirectory() as temp:
            server = subprocess.Popen(
                [sys.executable, "-I", "-c", probe, str(OPENER), "--port", "0", "--log", f"{temp}/opener.log"],
                env={"PATH": "/usr/bin:/bin", "HOME": temp}, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
            )  # fmt: skip
            try:
                line = server.stdout.readline()
            finally:
                server.terminate()
                _, stderr = server.communicate(timeout=10)
            self.assertTrue(line.startswith("regime-url-opener: listening on 127.0.0.1:"), line + stderr)
            self.assertNotIn("getfqdn called", stderr)


class TokenExportTest(unittest.TestCase):
    """U312: no shell exports CLAUDE_CODE_OAUTH_TOKEN; U318: no code path reads the retired token file. A zsh or a
    login shell on a host that still holds the file leaves the variable unset, so the operator's interactive Claude
    Code, its hooks and every other child keep the host's own login, and the seats log in by the shared directory."""

    PROBE: ClassVar[dict[str, list[str]]] = {
        "zsh": ["zsh", "-f", "-c", 'source "$1"; print -r -- "${CLAUDE_CODE_OAUTH_TOKEN-unset}"'],
        "bash": ["bash", "--norc", "--noprofile", "-c",
                 'mise() { :; }; source "$1"; printf "%s\\n" "${CLAUDE_CODE_OAUTH_TOKEN-unset}"'],
    }  # fmt: skip

    def run_shell(self, shell: str, rc: Path, home: Path) -> str:
        if not shutil.which(shell):
            self.skipTest(f"{shell} is not installed")
        result = subprocess.run(
            [*self.PROBE[shell], shell, str(rc)], env={"HOME": str(home), "PATH": "/usr/bin:/bin"},
            capture_output=True, text=True, check=True,
        )  # fmt: skip
        return result.stdout.strip()

    def test_no_shell_exports_the_token_file(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            home = Path(temp)
            token = home / ".config/claude-code/oauth-token"
            token.parent.mkdir(parents=True)
            token.write_text("fake-oauth-token-for-test\n")
            token.chmod(0o600)
            for shell, rc in (("zsh", ZSHENV), ("bash", PROFILE)):
                with self.subTest(shell=shell):
                    self.assertEqual(self.run_shell(shell, rc, home), "unset")

    def test_no_rc_line_names_the_variable(self) -> None:
        for rc in (ZSHENV, PROFILE):
            with self.subTest(rc=rc.name):
                lines = [
                    line.strip()
                    for line in rc.read_text().splitlines()
                    if "CLAUDE_CODE_OAUTH_TOKEN" in line and not line.lstrip().startswith("#")
                ]
                self.assertEqual(lines, [])

    def test_the_shim_is_the_one_exporter_and_no_rc_file_names_the_retired_token_file(self) -> None:
        """U312, U318, U551: the rc files export nothing of a token and name neither the retired `~/.config/claude-code/
        oauth-token` file nor `claude setup-token`; of the levers (source and installed copy) hcom-seat holds the one
        `export CLAUDE_CODE_OAUTH_TOKEN`, inside the shim text it writes, which reads the seats' token file, and the
        preflight and the broker export the name nowhere (the broker passes the value to its workers' omp launch as an
        `env -i` assignment, and clears the name from its own connection); none names the retired file."""
        for rc in (ZSHENV, PROFILE):
            with self.subTest(path=str(rc.relative_to(ROOT))):
                text = rc.read_text()
                for needle in ("oauth-token", "setup-token", "CLAUDE_CODE_OAUTH_TOKEN"):
                    self.assertNotIn(needle, "\n".join(l for l in text.splitlines() if not l.lstrip().startswith("#")))
        levers = {HCOM_SEAT: 1, PREFLIGHT: 0, ROOT / "scripts/orchestrator/acp-broker": 0}
        for lever, exports in list(levers.items()):
            for path in (lever, COMMON / f"executable_{lever.name}"):
                with self.subTest(path=str(path.relative_to(ROOT))):
                    text = path.read_text()
                    self.assertEqual(text.count("export CLAUDE_CODE_OAUTH_TOKEN"), exports)
                    self.assertNotIn("oauth-token", text, "the retired token file is named by no lever")


@unittest.skipUnless(CHEZMOI, "chezmoi is not installed")
class SshForwardTest(unittest.TestCase):
    """The laptop's SSH config forwards the two loopback ports to a host tagged `seat-host`, and only on macOS."""

    def ssh_g(self, config: str, host: str) -> list[str]:
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "config"
            path.write_text(config)
            result = subprocess.run(["ssh", "-F", str(path), "-G", host], capture_output=True, text=True, check=True)
        return [
            line
            for line in result.stdout.splitlines()
            if line.split(" ", 1)[0] in ("tag", "localforward", "remoteforward")
        ]

    @unittest.skipUnless(shutil.which("ssh"), "ssh is not installed")
    def test_a_tagged_host_gets_both_forwards_and_another_host_none(self) -> None:
        managed = render(SSH_CONFIG.read_text(), "darwin")
        # conf.d is the operator's own; stand in for it with one tagged and one untagged entry.
        body = "".join(line + "\n" for line in managed.splitlines() if not line.startswith("Include "))
        hosts = "Host seat-box\n  Tag seat-host\nHost other-box\n  HostName 127.0.0.1\n"
        self.assertEqual(
            self.ssh_g(hosts + body, "seat-box"),
            ["tag seat-host", "localforward 1455 [127.0.0.1]:1455", "remoteforward [127.0.0.1]:1456 [127.0.0.1]:1456"],
        )
        self.assertEqual(self.ssh_g(hosts + body, "other-box"), [])

    def test_only_macos_renders_the_block_and_linux_keeps_the_old_file(self) -> None:
        darwin = render(SSH_CONFIG.read_text(), "darwin")
        linux = render(SSH_CONFIG.read_text(), "linux")
        self.assertIn("Match tagged seat-host\n", darwin)
        self.assertNotIn("Match", linux)
        self.assertTrue(linux.endswith("Include ~/.ssh/work.d/config\n"), repr(linux[-40:]))
        self.assertTrue(darwin.startswith(linux), "the macOS render only appends")


@unittest.skipUnless(CHEZMOI, "chezmoi is not installed")
class UrlOpenerAgentTest(unittest.TestCase):
    def test_launchd_starts_the_opener_on_the_loopback_port_and_keeps_it_alive(self) -> None:
        plist = plistlib.loads(render(PLIST.read_text(), "darwin").encode())
        self.assertEqual(plist["Label"], "com.mryfmo.dotfiles.url-opener")
        self.assertEqual(
            plist["ProgramArguments"],
            ["/usr/bin/python3", "-I", "/render-home/.local/bin/common/regime-url-opener", "--port", "1456"],
        )
        self.assertTrue(plist["RunAtLoad"])
        self.assertTrue(plist["KeepAlive"])
        # launchd opens these before Python runs; a fresh home has no log directory, so they must not need one.
        self.assertEqual((plist["StandardOutPath"], plist["StandardErrorPath"]), ("/dev/null", "/dev/null"))
        self.assertNotIn("WorkingDirectory", plist)
        ignore = (ROOT / "home/.chezmoitemplates/chezmoiignore.d/ubuntu/common").read_text().splitlines()
        self.assertIn("Library", ignore)


class PreflightTest(unittest.TestCase):
    """`seat-login-preflight`: presence and mtimes only, fail closed on unreadable records, logins only in the operator's TTY."""

    def setUp(self) -> None:
        self.temp = Path(tempfile.mkdtemp(prefix="seat-login-"))
        self.home = self.temp / "home"
        self.bin = self.temp / "bin"
        self.calls = self.temp / "calls.txt"
        self.bun_calls = self.temp / "bun-calls.txt"
        profiles = self.home / ".agents/omp/profiles"
        profiles.mkdir(parents=True)
        (profiles / "audit.yml").write_text(
            "# Generated\nmodelRoles:\n  default: openai-siwc/gpt-6-astra\nskills:\n  customDirectories: []\n"
        )
        (profiles / "orchestrator.yml").write_text("modelRoles:\n  default: claude-bridge/claude-fable-5-2\n")
        (profiles / "worker.yml").write_text("modelRoles:\n  default: claude-bridge/claude-opus-5-5\n")
        # The seats root the login groups' Claude Code directories live in (U318, per group since U498), passed as
        # hcom-seat passes its resolved one: the orchestrator profile's group directory, the worker's, and the legacy
        # shared directory the kit neither reads nor removes (U551: none holds a credential the lever reads).
        self.seats = self.temp / "seats"
        self.shared = self.seats / ".state/claude-orchestrator"
        self.shared_worker = self.seats / ".state/claude-worker"
        self.legacy = self.seats / ".state/claude"
        # The SIWC readiness count (src/credentials.ts) without a real agent.db: FAKE_SIWC_LOGINS logins.
        write_exec(
            self.bin / "bun",
            f"""#!/bin/sh
printf 'bun %s\\n' "$*" >> "{self.bun_calls}"
[ "${{FAKE_BUN_FAILS:-0}}" = 1 ] && exit 2
printf '%s\\n' "${{FAKE_SIWC_LOGINS:-1}}"
""",
        )
        # The fake logins record what the pre-flight handed them, then create what a real login leaves.
        write_exec(
            self.bin / "omp",
            f"""#!/bin/sh
{{ printf 'omp %s\\n' "$*"
  printf 'OPENAI_SIWC_CALLBACK_PORT=%s\\n' "$OPENAI_SIWC_CALLBACK_PORT"
  printf 'PI_CONFIG_FILES:\\n'; cat "$PI_CONFIG_FILES"
  printf 'xdg-open:\\n'; cat "$(command -v xdg-open)"
  printf 'open:\\n'; cat "$(command -v open)"; }} >> "{self.calls}"
[ "${{FAKE_LOGIN_FAILS:-0}}" = 1 ] && exit 9
[ "${{FAKE_LOGIN_NOOP:-0}}" = 1 ] && exit 0
agent="$HOME/.omp/profiles/$2/agent"
mkdir -p "$agent/openai-siwc"
printf '{{"hostId":"{HOST_ID}","clientId":"oaiapp_fake"}}\\n' > "$agent/openai-siwc/registration.json"
: > "$agent/agent.db"
""",
        )
        # The seats' Claude token file (U551), `<seats-root>/.state/claude-token`, the Claude route's one input: placed
        # by place_token as seat-token-place writes it; no `claude` is on PATH, since the lever runs none.
        self.token_file = self.seats / ".state/claude-token"

    def tearDown(self) -> None:
        shutil.rmtree(self.temp)

    def env(self, **extra: str) -> dict[str, str]:
        env = {
            "HOME": str(self.home), "PATH": f"{self.bin}:{os.environ['PATH']}", "TMPDIR": str(self.temp),
            "REGIME_SEATS_ROOT": str(self.seats),
        }  # fmt: skip
        env.update(extra)
        return env

    def run_lever(self, *args: str, **extra: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [str(PREFLIGHT), *args],
            env=self.env(**extra),
            check=False,
            capture_output=True,
            text=True,
            stdin=subprocess.DEVNULL,
        )

    def run_tty(self, *args: str, **extra: str) -> tuple[int, str]:
        """Run with stdin, stdout and stderr on a pseudo-terminal, as in the operator's own pane."""
        main, replica = pty.openpty()
        process = subprocess.Popen(
            [str(PREFLIGHT), *args], env=self.env(**extra), stdin=replica, stdout=replica, stderr=replica
        )
        os.close(replica)
        chunks: list[bytes] = []
        deadline = time.monotonic() + 30
        while time.monotonic() < deadline:
            ready, _, _ = select.select([main], [], [], 0.2)
            if ready:
                try:
                    data = os.read(main, 4096)
                except OSError:
                    break
                if not data:
                    break
                chunks.append(data)
            elif process.poll() is not None:
                break
        os.close(main)
        return process.wait(timeout=10), b"".join(chunks).decode(errors="replace").replace("\r\n", "\n")

    def calls_text(self) -> str:
        return self.calls.read_text() if self.calls.exists() else ""

    def bun_calls_text(self) -> str:
        return self.bun_calls.read_text() if self.bun_calls.exists() else ""

    def place_token(self, root: Path | None = None, content: str = FAKE_OAT) -> Path:
        """Place the fixture token as seat-token-place does: one line, 0600, in the 0700 `.state` of the 0700 root."""
        root = root or self.seats
        (root / ".state").mkdir(parents=True, exist_ok=True)
        for path in (root, root / ".state"):
            path.chmod(0o700)
        path = root / ".state/claude-token"
        path.write_text(content + "\n")
        path.chmod(0o600)
        return path

    def token_absent(self, root: Path | None = None) -> str:
        """The Claude route's state without a token file under `root` (the fixture's seats root unless given)."""
        return f"token absent (no {(root or self.seats) / '.state/claude-token'})"

    def token_present(self, root: Path | None = None) -> str:
        return f"token present ({(root or self.seats) / '.state/claude-token'})"

    STEPS = (
        "the seats' Claude credential is the operator's step: 1) run `claude setup-token` in your own terminal on this"
        " host (the browser opens; sign in; the token prints once), 2) place it with `seat-token-place`"
        " (handouts/claude-setup-token-u551.md), then start the seat again"
    )

    def refusal(self, line: str) -> str:
        """The profile mode's refusal of an absent token: the state line, then the operator's two steps."""
        return f"seat-login-preflight: {line}; {self.STEPS}\n"

    def register(self, profile: str = "audit", record: str | None = None) -> Path:
        agent = self.home / f".omp/profiles/{profile}/agent"
        (agent / "openai-siwc").mkdir(parents=True)
        reg = agent / "openai-siwc/registration.json"
        reg.write_text(record if record is not None else json.dumps({"hostId": HOST_ID, "clientId": "oaiapp_fake"}))
        (agent / "agent.db").write_text("never read")
        return reg

    def test_check_prints_one_line_per_profile_from_presence_and_mtimes(self) -> None:
        self.register()
        result = self.run_lever("--check")
        self.assertEqual(result.returncode, 0, result.stderr)
        lines = result.stdout.splitlines()
        self.assertRegex(
            lines[0],
            rf"^audit openai-siwc: registered \(host {HOST_ID}, client oaiapp_fake\), agent\.db mtime \d{{4}}-\d\d-\d\dT\d\d:\d\d:\d\dZ$",
        )
        self.assertEqual(
            lines[1:],
            [f"orchestrator claude-bridge: {self.token_absent()}", f"worker claude-bridge: {self.token_absent()}"],
        )

    def test_check_judges_the_token_file_by_its_form_and_never_prints_the_token(self) -> None:
        """U551: `--check` judges the Claude route by the seats' Claude token file `<seats-root>/.state/claude-token`
        alone, by its form: absent, a symbolic link (refused before anything resolves it), a directory, a mode other
        than 0600, a line off the form, two lines, a carriage return, a missing line feed and an empty file are each
        `token absent (<reason>)` naming the file and the fault (exit 0: absent is a state, not a failure), the
        token's bytes in no line; a 0600 file holding one line of the form is `token present (<file>)`. No `claude`
        runs (none is on PATH), no call leaves the host, a token variable in the environment is no input (U312), and
        `--check` makes nothing."""
        token = self.token_file
        result = self.run_lever("--check", "orchestrator", **{TOKEN_VARIABLE: FAKE_OAUTH_VALUE})
        self.assertEqual(
            (result.returncode, result.stdout), (0, f"orchestrator claude-bridge: {self.token_absent()}\n")
        )
        self.assertEqual(self.calls_text(), "", "no producer of a login runs")
        self.place_token()
        result = self.run_lever("--check", "orchestrator", **{TOKEN_VARIABLE: FAKE_OAUTH_VALUE})
        self.assertEqual(
            (result.returncode, result.stdout), (0, f"orchestrator claude-bridge: {self.token_present()}\n")
        )
        elsewhere = self.temp / "elsewhere-token"
        elsewhere.write_text(FAKE_OAT + "\n")
        elsewhere.chmod(0o600)
        form = "holds no token of the form sk-ant-oat01-<20 to 255 of [A-Za-z0-9_-]>; the content is never printed"
        one_line = "holds more than its one line: a second line, a carriage return or other bytes beyond the token"
        no_feed = "holds no line ending in a line feed; the token is one line, as seat-token-place writes it"
        cases = (
            ("a link", lambda: token.symlink_to(elsewhere), f"{token} is a symbolic link; the token file must be a regular file of this user"),
            ("a directory", lambda: token.mkdir(), f"{token} is not a regular file"),
            ("mode 0644", lambda: (self.place_token(), token.chmod(0o644)), f"{token} has mode 644, not 0600"),
            ("a key, not a token", lambda: self.place_token(content="sk-ant-api03-" + "NOTATOKEN" + "0" * 40), f"{token} {form}"),
            ("a short token", lambda: self.place_token(content="sk-ant-oat01-" + "short"), f"{token} {form}"),
            ("two lines", lambda: self.place_token(content=FAKE_OAT + "\nsecond"), f"{token} {one_line}"),
            ("a carriage return", lambda: self.place_token(content=FAKE_OAT + "\r"), f"{token} {form}"),
            ("no line feed", lambda: (self.place_token(), token.write_text(FAKE_OAT)), f"{token} {no_feed}"),
            ("empty", lambda: (self.place_token(), token.write_text("")), f"{token} {no_feed}"),
        )  # fmt: skip
        for label, plant, reason in cases:
            with self.subTest(case=label):
                if token.is_symlink() or token.is_file():
                    token.unlink()
                elif token.is_dir():
                    token.rmdir()
                plant()
                result = self.run_lever("--check", "orchestrator", **{TOKEN_VARIABLE: FAKE_OAUTH_VALUE})
                self.assertEqual(
                    (result.returncode, result.stdout),
                    (0, f"orchestrator claude-bridge: token absent ({reason})\n"),
                    result.stderr,
                )
                self.assertNotIn(FAKE_OAT, result.stdout + result.stderr)
                self.assertNotIn("NOTATOKEN", result.stdout + result.stderr)
        self.assertEqual(elsewhere.read_text(), FAKE_OAT + "\n", "the link's target is untouched")
        self.assertEqual(self.calls_text(), "")
        self.assertNotIn(FAKE_OAUTH_VALUE, self.calls_text() + result.stdout + result.stderr)
        self.assertFalse(self.shared.exists(), "--check makes nothing")

    def test_the_seats_root_derives_from_the_checkout_when_none_is_passed(self) -> None:
        """U318, U498, U551: without REGIME_SEATS_ROOT the token file is `~/.local/state/omp-seats/<slug>/.state/claude-token`
        of the checkout the command runs in (regime-env's slug, HOME in physical form); outside a checkout the Claude
        route is unreadable, never absent, and the SIWC route is untouched."""
        env = {key: value for key, value in self.env().items() if key != "REGIME_SEATS_ROOT"}
        inside = subprocess.run(
            [str(PREFLIGHT), "--check", "orchestrator"], env=env, cwd=ROOT,
            capture_output=True, text=True, check=False, stdin=subprocess.DEVNULL,
        )  # fmt: skip
        home = self.home.resolve()
        self.assertEqual(inside.returncode, 0, inside.stderr)
        self.assertRegex(
            inside.stdout,
            rf"^orchestrator claude-bridge: token absent \(no {re.escape(str(home))}/\.local/state/omp-seats/[a-z0-9][a-z0-9_-]{{0,39}}/\.state/claude-token\)\n$",
        )
        outside = subprocess.run(
            [str(PREFLIGHT), "--check", "orchestrator", "audit"], env=env, cwd=self.temp,
            capture_output=True, text=True, check=False, stdin=subprocess.DEVNULL,
        )  # fmt: skip
        self.assertEqual(outside.returncode, 1, outside.stderr)
        self.assertEqual(
            outside.stdout.splitlines()[0],
            "orchestrator claude-bridge: unreadable (no seats root: set REGIME_SEATS_ROOT or run inside a checkout)",
        )
        self.assertTrue(outside.stdout.splitlines()[1].startswith("audit openai-siwc: absent (no "), outside.stdout)
        self.assertEqual(self.calls_text(), "")

    def test_check_judges_every_claude_profile_by_the_one_token_file_and_refuses_a_profile_outside_the_table(
        self,
    ) -> None:
        """U498, U551: `--check` runs the login group table (`login_group_of_role`) for every profile with a seat login
        route, so a profile outside it refuses the lever (exit 2) naming the profile, its route and the table, never
        `absent` and never `unreadable` (U498b); the lines before it print, no call runs and nothing is made. Every
        claude-bridge profile (the orchestrator and worker seats, a deployed dsh overlay whose gateway child is the
        Router's) is judged by the one token file of the seats root, so one placement turns every Claude line present
        at once, whatever its group directory holds; the legacy shared `.state/claude` is read by no line."""
        profiles = self.home / ".agents/omp/profiles"
        (profiles / "dsh.yml").write_text("modelRoles:\n  default: claude-bridge/claude-haiku-5-5\n")
        before = [
            f"audit openai-siwc: absent (no {self.home}/.omp/profiles/audit/agent/openai-siwc/registration.json)",
            f"dsh claude-bridge: {self.token_absent()}",
            f"orchestrator claude-bridge: {self.token_absent()}",
        ]
        for route in ("openai-siwc/gpt-6-astra", "claude-bridge/claude-haiku-5-5"):
            with self.subTest(route=route):
                (profiles / "other.yml").write_text(f"modelRoles:\n  default: {route}\n")
                result = self.run_lever("--check")
                self.assertEqual(result.returncode, 2, result.stderr)
                self.assertEqual(result.stdout.splitlines(), before, "the lines before the refusal print")
                self.assertEqual(
                    result.stderr,
                    f"seat-login-preflight: refused: the profile other ({route.split('/')[0]}) is outside the login group"
                    " table login_group_of_role, which names orchestrator, worker, audit, dsh and router; it has no login"
                    " group, so no line is printed for it\n",
                )
                self.assertEqual(
                    self.calls_text() + self.bun_calls_text(), "", "no call for a profile outside the table"
                )
                self.assertFalse((self.seats / ".state").exists(), "nothing made")
        (profiles / "other.yml").unlink()
        result = self.run_lever("--check")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.splitlines(), [*before, f"worker claude-bridge: {self.token_absent()}"])
        self.place_token()
        self.shared_worker.mkdir(parents=True, exist_ok=True)
        self.legacy.mkdir()
        (self.legacy / ".credentials.json").write_text("{}")
        result = self.run_lever("--check", "orchestrator", "worker", "dsh")
        self.assertEqual(
            (result.returncode, result.stdout),
            (0, "".join(f"{p} claude-bridge: {self.token_present()}\n" for p in ("orchestrator", "worker", "dsh"))),
            result.stderr,
        )
        self.assertEqual(self.calls_text(), "", "no login producer runs")
        self.assertNotIn(f"{self.legacy})", result.stdout, "the legacy shared directory is read by no line")
        self.assertNotIn(FAKE_OAT, result.stdout + result.stderr)

    def test_the_login_group_table_maps_each_role_and_refuses_any_other(self) -> None:
        """U498: the preflight's `login_group_of_role` is the role table copied from hcom-seat as text
        (`tests/unit/test_hcom_seat.py` holds the two texts equal): worker to worker, orchestrator to orchestrator,
        audit to audit, dsh and router to router; any other name returns 1 and prints nothing."""
        table = self.lever_functions("login_group_of_role")
        script = f'set -euo pipefail\n{table}\nlogin_group_of_role "$1"\n'
        for role, group in (
            ("worker", "worker"), ("orchestrator", "orchestrator"), ("audit", "audit"), ("dsh", "router"), ("router", "router"),
        ):  # fmt: skip
            with self.subTest(role=role):
                run = subprocess.run(["bash", "-c", script, "_", role], capture_output=True, text=True, check=False)
                self.assertEqual((run.returncode, run.stdout, run.stderr), (0, f"{group}\n", ""))
        for role in ("claude", "review", "WORKER", ""):
            with self.subTest(role=role):
                run = subprocess.run(["bash", "-c", script, "_", role], capture_output=True, text=True, check=False)
                self.assertEqual((run.returncode, run.stdout), (1, ""), run.stderr)

    def test_an_unreadable_record_is_never_read_as_absent(self) -> None:
        reg = self.register(record="{ not json")
        result = self.run_lever("--check", "audit")
        self.assertEqual(result.returncode, 1)
        self.assertEqual(result.stdout, f"audit openai-siwc: unreadable ({reg})\n")

    def test_a_failing_jq_with_a_valid_record_is_unreadable_not_absent(self) -> None:
        reg = self.register()
        write_exec(self.bin / "jq", "#!/bin/sh\nexit 5\n")
        result = self.run_lever("--check", "audit")
        self.assertEqual((result.returncode, result.stdout), (1, f"audit openai-siwc: unreadable ({reg})\n"))
        remote = self.run_lever("audit", SSH_CONNECTION="100.64.0.2 50000 100.64.0.3 22")
        self.assertEqual(remote.returncode, 1)
        self.assertIn(f"unreadable ({reg}); fix or move the record aside", remote.stderr)
        self.assertEqual(self.calls_text(), "")

    def test_a_profile_without_a_route_is_named(self) -> None:
        result = self.run_lever("--check", "missing")
        overlay = self.home / ".agents/omp/profiles/missing.yml"
        self.assertEqual(result.stdout, f"missing: no route (overlay {overlay} absent or without modelRoles.default)\n")

    def test_a_local_host_does_nothing(self) -> None:
        # Explicitly local on every runner: macOS, no SSH session. A Linux CI runner has no display, which
        # counts as remote (test_a_linux_host_without_a_display_counts_as_remote). The SIWC route alone keeps this
        # exit; the Claude route is checked on every host (test_the_claude_rule_holds_on_a_local_host).
        write_exec(self.bin / "uname", "#!/bin/sh\necho Darwin\n")
        result = self.run_lever("audit")
        self.assertEqual((result.returncode, result.stdout, result.stderr), (0, "", ""))
        self.assertEqual(self.calls_text() + self.bun_calls_text(), "")

    def test_the_claude_rule_holds_on_a_local_host(self) -> None:
        """U190b, U551: the seat's child runs on the seats' token wherever it runs, so a local host (no SSH session; a
        display on Linux) without the token file refuses with the two printed steps and makes nothing (the group's
        directory is hcom-seat's to make at a launch); one with the token placed passes with the one line; the
        operator's own `~/.claude` is never an input. Round 1 exited 0 there before any check, and a host-only login
        started a seat whose first bridge turn would end `Not logged in`."""
        credentials = self.home / ".claude/.credentials.json"
        credentials.parent.mkdir()
        credentials.write_text("{}")
        credentials.chmod(0o600)
        absent = self.run_lever("orchestrator", DISPLAY=":0")
        self.assertEqual(absent.returncode, 2, absent.stderr)
        self.assertEqual(absent.stderr, self.refusal(f"orchestrator claude-bridge: {self.token_absent()}"))
        self.assertFalse(self.seats.exists(), "nothing made: the chain is hcom-seat's to make")
        self.place_token()
        ready = self.run_lever("orchestrator", DISPLAY=":0")
        self.assertEqual(ready.returncode, 0, ready.stderr)
        self.assertEqual(ready.stderr, f"seat-login-preflight: orchestrator claude-bridge: {self.token_present()}\n")
        self.assertEqual(sorted(path.name for path in (self.seats / ".state").iterdir()), ["claude-token"])
        self.assertEqual(self.calls_text() + self.bun_calls_text(), "", "no producer of a login runs")
        self.assertEqual(credentials.read_text(), "{}", "the operator's store is untouched")
        self.assertNotIn(FAKE_OAT, absent.stderr + ready.stderr)

    def assert_component_refused(self, result: subprocess.CompletedProcess[str], path: Path | str, kind: str) -> None:
        """U318b, U498: a bad component of the group directory chain refuses the lever (exit 2) naming it and its kind."""
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertEqual(
            result.stderr,
            f"seat-login-preflight: refused: the login group's Claude Code directory path component {path} is {kind};"
            " move it aside before a seat starts\n",
        )

    def test_a_shared_directory_that_is_a_link_or_a_file_refuses_naming_it_never_absent(self) -> None:
        """U318, U318b: the shared directory must be a real directory (hcom-seat refuses a link too): a symbolic link
        or a file there refuses `--check` and the profile mode (exit 2, the component named) before any call, never
        absent, and the profile mode replaces nothing."""
        self.shared.parent.mkdir(parents=True)
        elsewhere = self.temp / "elsewhere"
        elsewhere.mkdir()
        self.shared.symlink_to(elsewhere)
        check = self.run_lever("--check", "orchestrator")
        self.assert_component_refused(check, self.shared, "a symbolic link")
        self.assertEqual(check.stdout, "")
        gate = self.run_lever("orchestrator", SSH_CONNECTION="100.64.0.2 50000 100.64.0.3 22")
        self.assert_component_refused(gate, self.shared, "a symbolic link")
        self.assertTrue(self.shared.is_symlink())
        self.shared.unlink()
        self.shared.write_text("")
        check = self.run_lever("--check", "orchestrator")
        self.assert_component_refused(check, self.shared, "not a directory")
        gate = self.run_lever("orchestrator", DISPLAY=":0")
        self.assert_component_refused(gate, self.shared, "not a directory")
        self.assertTrue(self.shared.is_file() and not self.shared.is_symlink())
        self.assertEqual(self.calls_text() + self.bun_calls_text(), "", "no claude call ran")

    def test_check_refuses_a_linked_state_parent_naming_it(self) -> None:
        """U318b (verdict U318-e0dd8cc2, P2 at :333): `--check` judged the leaf alone, so a linked `.state` parent
        reached another directory's leaf and was reported by it. Both modes now hold the seats root, `.state` and the
        group directory to real directories of this user, in this order, and refuse at the first that is not, naming
        it; the SIWC line before it still prints, nothing is made and the link is kept."""
        self.seats.mkdir()
        elsewhere = self.temp / "elsewhere"
        (elsewhere / "claude-orchestrator").mkdir(parents=True)
        state = self.seats / ".state"
        state.symlink_to(elsewhere)
        self.assertTrue(self.shared.is_dir(), "the leaf resolves through the link: the round-1 hole")
        check = self.run_lever("--check", "orchestrator")
        self.assert_component_refused(check, state, "a symbolic link")
        self.assertEqual(check.stdout, "")
        every = self.run_lever("--check")
        self.assert_component_refused(every, state, "a symbolic link")
        self.assertRegex(every.stdout, r"^audit openai-siwc: absent \(no .*\)\n$")
        gate = self.run_lever("orchestrator", SSH_CONNECTION="100.64.0.2 50000 100.64.0.3 22")
        self.assert_component_refused(gate, state, "a symbolic link")
        self.assertTrue(state.is_symlink())
        self.assertEqual(sorted(path.name for path in elsewhere.iterdir()), ["claude-orchestrator"])
        self.assertEqual(sorted(path.name for path in self.seats.iterdir()), [".state"])
        self.assertEqual(self.calls_text() + self.bun_calls_text(), "", "no claude call ran")

    def test_check_refuses_a_file_at_state_or_the_seats_root_and_another_users_directory(self) -> None:
        """U318b: a regular file at `.state` was reported `absent` with exit 0 by `--check` (the leaf's `-e` was false
        under it); it refuses, exit 2, naming `.state`, as does a file at the seats root and a directory of another
        user (the login would land outside what this kit made), in both modes, with nothing made or replaced."""
        self.seats.mkdir()
        state = self.seats / ".state"
        state.write_text("")
        for args in (("--check", "orchestrator"), ("orchestrator",), ("worker",)):
            with self.subTest(args=args):
                self.assert_component_refused(self.run_lever(*args, DISPLAY=":0"), state, "not a directory")
        self.assertTrue(state.is_file())
        self.assertEqual(sorted(path.name for path in self.seats.iterdir()), [".state"])
        state.unlink()
        self.seats.rmdir()
        self.seats.write_text("")
        self.assert_component_refused(self.run_lever("--check", "orchestrator"), self.seats, "not a directory")
        self.assert_component_refused(self.run_lever("orchestrator", DISPLAY=":0"), self.seats, "not a directory")
        self.assertTrue(self.seats.is_file())
        other = Path("/usr")
        if os.geteuid() != 0 and other.stat().st_uid != os.geteuid():
            for args in (("--check", "orchestrator"), ("orchestrator",)):
                with self.subTest(args=args, root=str(other)):
                    result = self.run_lever(*args, DISPLAY=":0", REGIME_SEATS_ROOT=str(other))
                    self.assert_component_refused(result, other, "a directory of another user")
            self.assertFalse((other / ".state").exists())
        self.assertEqual(self.calls_text() + self.bun_calls_text(), "", "no claude call ran")

    def test_a_linked_root_spelled_with_trailing_or_dot_components_refuses_naming_the_link(self) -> None:
        """U318c (verdict U318b-ad9b9456, P2 at :320): `REGIME_SEATS_ROOT=<link>//` kept a trailing slash (`${root%/}`
        strips one), and a trailing slash makes `-L` follow the link, so `--check` exited 0 and the profile mode made
        the group directory through it. The root is normalised to one spelling before any test (no empty, `.` or `..`
        component, no trailing slash) by parameter expansion alone, never `realpath`, so every spelling of the link
        refuses (exit 2) naming the link in both modes, and nothing is made through it."""
        elsewhere = self.temp / "elsewhere"
        elsewhere.mkdir()
        link = self.temp / "link"
        link.symlink_to(elsewhere)
        spellings = (f"{link}//", f"{link}/./", f"{link}/.", f"{link}///./", f"{link}/x/..", f"{link}/./x/../")
        for spelling in spellings:
            for args, extra in ((("--check", "orchestrator"), {}), (("orchestrator",), {"DISPLAY": ":0"})):
                with self.subTest(spelling=spelling, args=args):
                    result = self.run_lever(*args, REGIME_SEATS_ROOT=spelling, **extra)
                    self.assert_component_refused(result, link, "a symbolic link")
                    self.assertEqual(result.stdout, "")
        self.assertTrue(link.is_symlink(), "the link is kept")
        self.assertEqual(sorted(path.name for path in elsewhere.iterdir()), [], "nothing made through the link")
        self.assertEqual(sorted(path.name for path in self.temp.iterdir()), ["bin", "elsewhere", "home", "link"])
        self.assertEqual(self.calls_text() + self.bun_calls_text(), "", "no claude call ran")

    @unittest.skipIf(os.geteuid() == 0, "root searches a mode-000 directory, so nothing is unknown to it")
    def test_a_root_this_user_cannot_search_refuses_naming_the_component_never_absent(self) -> None:
        """U318c (verdict U318b-ad9b9456, P2 at :327): a file predicate that could not run was read as absence, so an
        owned root of mode 000 hid a linked `.state`: `--check` printed `absent` with exit 0 and the profile mode failed
        at `mkdir` with exit 1. Each component is now judged only under a parent this user can search (a test such as
        `-L` or `-e` answers false both for "not so" and for "could not look"): a root this user cannot search refuses
        (exit 2) naming `.state` and the root, a parent of the root it cannot search refuses naming the root, in both
        modes; the link is kept, nothing is made and no call runs."""
        remote = {"SSH_CONNECTION": "100.64.0.2 50000 100.64.0.3 22"}
        elsewhere = self.temp / "elsewhere"
        elsewhere.mkdir()
        self.seats.mkdir()
        state = self.seats / ".state"
        state.symlink_to(elsewhere)
        locked = self.temp / "locked"
        locked.mkdir()
        inner = locked / "seats"

        def refusal(component: Path, parent: Path) -> str:
            return (
                f"seat-login-preflight: refused: cannot read the login group's Claude Code directory path component"
                f" {component} (permission denied: {parent} is not searchable by this user); fix its mode before a"
                " seat starts\n"
            )

        self.seats.chmod(0)
        locked.chmod(0)
        try:
            for args, extra in (
                (("--check", "orchestrator"), {}),
                (("orchestrator",), {"DISPLAY": ":0"}),
                (("worker",), remote),
            ):
                with self.subTest(args=args, root="mode 000"):
                    result = self.run_lever(*args, **extra)
                    self.assertEqual(
                        (result.returncode, result.stdout, result.stderr), (2, "", refusal(state, self.seats))
                    )
                with self.subTest(args=args, root="under a mode-000 parent"):
                    result = self.run_lever(*args, REGIME_SEATS_ROOT=str(inner), **extra)
                    self.assertEqual((result.returncode, result.stdout, result.stderr), (2, "", refusal(inner, locked)))
            # The SIWC line before the Claude route still prints; the refusal is the lever's exit.
            every = self.run_lever("--check")
            self.assertEqual((every.returncode, every.stderr), (2, refusal(state, self.seats)))
            self.assertRegex(every.stdout, r"^audit openai-siwc: absent \(no .*\)\n$")
        finally:
            self.seats.chmod(0o700)
            locked.chmod(0o700)
        self.assertTrue(state.is_symlink(), "the link is kept")
        self.assertEqual(sorted(path.name for path in elsewhere.iterdir()), [], "nothing made through the link")
        self.assertEqual(sorted(path.name for path in locked.iterdir()), [], "nothing made under the locked parent")
        self.assertEqual(self.calls_text() + self.bun_calls_text(), "", "no claude call ran")

    def test_a_plain_root_keeps_one_spelling_whatever_its_trailing_or_dot_components(self) -> None:
        """U318c: the normalisation changes nothing for a plain root. `<root>//`, `<root>/./` and `<root>/x/..` are the
        root: `--check` prints the one spelling (round 2 printed `<root>//.state/claude` for the first, U318), the
        profile mode names the token file with the one spelling and makes nothing (U551). A relative root is no seats
        root (unreadable, never a directory relative to the cwd)."""
        for spelling in (
            f"{self.seats}//",
            f"{self.seats}/./",
            f"{self.seats}/x/..",
            f"{self.seats}///.",
            f"{self.seats}/",
        ):
            with self.subTest(spelling=spelling):
                check = self.run_lever("--check", "orchestrator", REGIME_SEATS_ROOT=spelling)
                self.assertEqual(
                    (check.returncode, check.stdout), (0, f"orchestrator claude-bridge: {self.token_absent()}\n")
                )
        self.assertFalse(self.seats.exists(), "--check makes nothing")
        gate = self.run_lever("orchestrator", DISPLAY=":0", REGIME_SEATS_ROOT=f"{self.seats}//")
        self.assertEqual(gate.returncode, 2, gate.stderr)
        self.assertEqual(gate.stderr, self.refusal(f"orchestrator claude-bridge: {self.token_absent()}"))
        self.assertFalse(self.seats.exists(), "the profile mode makes nothing either")
        self.assertEqual(self.calls_text(), "")
        relative = self.run_lever("--check", "orchestrator", REGIME_SEATS_ROOT="seats")
        self.assertEqual(
            (relative.returncode, relative.stdout),
            (
                1,
                "orchestrator claude-bridge: unreadable (no seats root: REGIME_SEATS_ROOT seats is not an absolute path)\n",
            ),
        )

    def test_a_seats_root_with_a_space_a_quote_and_a_dollar_names_the_token_file_whole(self) -> None:
        """U318b (verdict U318-e0dd8cc2, P2 at :293) named the printed command's quoting; U551 prints no command: the
        lines name the token file under a seats root holding a space, a quote and a `$` as one spelling, in both
        modes and on both host kinds, and a token placed at exactly that file turns the line present."""
        seats = self.temp / "a b'$c"
        token = seats / ".state/claude-token"
        for extra in ({"DISPLAY": ":0"}, {"SSH_CONNECTION": "100.64.0.2 50000 100.64.0.3 22"}):
            with self.subTest(**extra):
                refused = self.run_lever("orchestrator", REGIME_SEATS_ROOT=str(seats), **extra)
                self.assertEqual(refused.returncode, 2, refused.stderr)
                self.assertEqual(refused.stderr, self.refusal(f"orchestrator claude-bridge: token absent (no {token})"))
        self.assertFalse(seats.exists(), "nothing made")
        self.place_token(seats)
        check = self.run_lever("--check", "orchestrator", REGIME_SEATS_ROOT=str(seats))
        self.assertEqual(
            (check.returncode, check.stdout), (0, f"orchestrator claude-bridge: token present ({token})\n")
        )
        ready = self.run_lever("orchestrator", DISPLAY=":0", REGIME_SEATS_ROOT=str(seats))
        self.assertEqual(
            (ready.returncode, ready.stderr),
            (0, f"seat-login-preflight: orchestrator claude-bridge: token present ({token})\n"),
        )
        self.assertEqual(self.calls_text(), "")

    def lever_functions(self, *names: str) -> str:
        """Functions of the lever, extracted by name as `test_hcom_seat`'s `identity_functions` does, so a test can
        overlay one producer and run the rest as written."""
        text = PREFLIGHT.read_text()
        return "\n".join(
            text[text.index(f"{name}() {{") : text.index("\n}\n", text.index(f"{name}() {{")) + 3] for name in names
        )

    def test_a_remote_host_with_a_login_passes_with_one_line(self) -> None:
        self.register()
        result = self.run_lever("audit", SSH_CONNECTION="100.64.0.2 50000 100.64.0.3 22")
        self.assertEqual(result.returncode, 0)
        self.assertTrue(result.stderr.startswith("seat-login-preflight: audit openai-siwc: registered"), result.stderr)

    def test_without_the_operators_terminal_a_missing_login_refuses_and_runs_nothing(self) -> None:
        remote = "100.64.0.2 50000 100.64.0.3 22"
        result = self.run_lever("audit", SSH_CONNECTION=remote)
        self.assertEqual(result.returncode, 2)
        self.assertIn(
            "a login is the operator's step: run `seat-login-preflight audit` in your own terminal", result.stderr
        )
        # The Claude route outside a TTY, and inside a seat: the two printed steps, nothing run (U551).
        status, output = self.run_tty("worker", SSH_CONNECTION=remote, HCOM_LAUNCHED="1")
        self.assertEqual(status, 2, output)
        self.assertIn(f"worker claude-bridge: {self.token_absent()}; {self.STEPS}", output)
        self.assertEqual(self.calls_text(), "")

    def test_the_operators_terminal_runs_the_siwc_login_with_the_pinned_port_and_the_laptop_opener(self) -> None:
        status, output = self.run_tty("audit", SSH_CONNECTION="100.64.0.2 50000 100.64.0.3 22")
        self.assertEqual(status, 0, output)
        calls = self.calls_text()
        self.assertIn("omp --profile audit login openai-siwc\nOPENAI_SIWC_CALLBACK_PORT=1455\n", calls)
        self.assertIn(f"PI_CONFIG_FILES:\nextensions:\n  - {self.home}/.agents/omp/extensions/openai-siwc\n", calls)
        self.assertIn(
            'xdg-open:\n#!/bin/sh\nexec regime-open-url "$@"\nopen:\n#!/bin/sh\nexec regime-open-url "$@"\n', calls
        )
        self.assertIn(
            "audit needs a openai-siwc login on this host; the sign-in opens in the browser of 100.64.0.2", output
        )
        self.assertIn(
            f"seat-login-preflight: audit openai-siwc: registered (host {HOST_ID}, client oaiapp_fake)", output
        )
        self.assertEqual(list(self.temp.glob("seat-login.*")), [], "the scratch opener directory is removed")

    def test_the_operators_terminal_names_the_two_steps_for_claude_and_runs_nothing(self) -> None:
        """U551: the Claude route has nothing to run: with the token file absent the preflight prints the operator's two
        steps (`claude setup-token` in the operator's own terminal, then `seat-token-place`) and runs no login and no
        browser, in a TTY too; the operator's `~/.claude` is not touched."""
        remote = "100.64.0.2 50000 100.64.0.3 22"
        status, output = self.run_tty("orchestrator", SSH_CONNECTION=remote)
        self.assertEqual(status, 2, output)
        self.assertIn(f"orchestrator claude-bridge: {self.token_absent()}; {self.STEPS}", output)
        self.assertEqual(self.calls_text(), "", "no login, no omp, no claude")
        self.assertFalse((self.home / ".claude").exists())
        self.assertFalse(self.seats.exists(), "nothing made")

    def test_a_failed_or_ineffective_login_keeps_the_seat_from_starting(self) -> None:
        remote = "100.64.0.2 50000 100.64.0.3 22"
        status, output = self.run_tty("audit", SSH_CONNECTION=remote, FAKE_LOGIN_FAILS="1")
        self.assertEqual(status, 1, output)
        self.assertIn("the openai-siwc login exited 9", output)
        status, output = self.run_tty("audit", SSH_CONNECTION=remote, FAKE_LOGIN_NOOP="1")
        self.assertEqual(status, 1, output)
        self.assertIn("audit openai-siwc: absent", output)
        self.assertIn("after the login", output)

    def test_a_linux_host_without_a_display_counts_as_remote(self) -> None:
        write_exec(self.bin / "uname", "#!/bin/sh\necho Linux\n")
        headless = self.run_lever("worker")
        self.assertEqual(headless.returncode, 2, headless.stderr)
        self.assertEqual(headless.stderr, self.refusal(f"worker claude-bridge: {self.token_absent()}"))
        for display in ({"DISPLAY": ":0"}, {"WAYLAND_DISPLAY": "wayland-0"}):
            with self.subTest(**display):
                # With a display the host is local: the SIWC route does nothing there, while the Claude route's rule
                # holds on every host (U190b): the worker refuses without the token file, and a token variable in the
                # environment is no input (U312).
                local = self.run_lever("audit", **display)
                self.assertEqual((local.returncode, local.stderr), (0, ""))
                for extra in ({}, {TOKEN_VARIABLE: FAKE_OAUTH_VALUE}):
                    refused = self.run_lever("worker", **display, **extra)
                    self.assertEqual(refused.returncode, 2, refused.stderr)
                    self.assertIn(f"worker claude-bridge: {self.token_absent()}", refused.stderr)
                    self.assertNotIn(FAKE_OAUTH_VALUE, refused.stderr)

    def test_a_profile_without_a_login_route_passes_and_an_unreadable_overlay_does_not(self) -> None:
        remote = "100.64.0.2 50000 100.64.0.3 22"
        (self.home / ".agents/omp/profiles/worker.yml").write_text("modelRoles: {}\n")
        result = self.run_lever("worker", SSH_CONNECTION=remote)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("worker: no route", result.stderr)
        self.assertIn("nothing to log in", result.stderr)
        write_exec(self.bin / "awk", "#!/bin/sh\nexit 2\n")
        overlay = self.home / ".agents/omp/profiles/audit.yml"
        broken = self.run_lever("audit", SSH_CONNECTION=remote)
        self.assertEqual(broken.returncode, 1)
        self.assertIn(f"audit: unreadable ({overlay})", broken.stderr)
        check = self.run_lever("--check", "audit")
        self.assertEqual((check.returncode, check.stdout), (1, f"audit: unreadable ({overlay})\n"))
        self.assertEqual(self.calls_text(), "")

    def test_the_retired_review_and_security_seat_profiles_are_refused_even_with_a_deployed_overlay(self) -> None:
        remote = "100.64.0.2 50000 100.64.0.3 22"
        profiles = self.home / ".agents/omp/profiles"
        (profiles / "security.yml").write_text("modelRoles:\n  default: openai-siwc/gpt-6-astra\n")
        (profiles / "review.yml").write_text("modelRoles:\n  default: claude-bridge/claude-fable-5-2\n")
        for profile in ("review", "security", "reviewer"):
            with self.subTest(profile=profile):
                refused = self.run_lever(profile, SSH_CONNECTION=remote)
                self.assertEqual(refused.returncode, 2)
                self.assertIn(f"unknown seat profile '{profile}'", refused.stderr)
        self.assertEqual(self.calls_text() + self.bun_calls_text(), "")

    def test_a_record_that_breaks_the_store_schema_is_unreadable_not_registered(self) -> None:
        remote = "100.64.0.2 50000 100.64.0.3 22"
        records = (
            {"hostId": "bad", "clientId": "oaiapp_x"},
            {"hostId": HOST_ID + "\nx", "clientId": "oaiapp_x"},
            {"hostId": HOST_ID, "clientId": None},
            {"hostId": HOST_ID, "clientId": ""},
            {"hostId": HOST_ID, "clientId": "oaiapp\tx"},
            {"hostId": HOST_ID, "clientId": "oaiapp_x", "accountId": 7},
            [HOST_ID, "oaiapp_x"],
        )
        one = json.dumps({"hostId": HOST_ID, "clientId": "oaiapp_x"})
        # store.ts reads the file with JSON.parse, so a stream of valid records, or none, is not one record.
        texts = [json.dumps(record) for record in records] + [
            one + one,
            f"{one}\n{one}\n",
            "",
            " \n",
            one + " trailing",
        ]
        for text in texts:
            with self.subTest(text=text):
                shutil.rmtree(self.home / ".omp", ignore_errors=True)
                reg = self.register(record=text)
                check = self.run_lever("--check", "audit")
                self.assertEqual((check.returncode, check.stdout), (1, f"audit openai-siwc: unreadable ({reg})\n"))
                gate = self.run_lever("audit", SSH_CONNECTION=remote)
                self.assertEqual(gate.returncode, 1, gate.stderr)
                self.assertIn(f"unreadable ({reg}); fix or move the record aside", gate.stderr)
        self.assertEqual(self.calls_text() + self.bun_calls_text(), "")

    def test_a_failed_producer_is_unreadable_never_absent_or_local(self) -> None:
        write_exec(self.bin / "uname", "#!/bin/sh\nexit 1\n")
        for args in (("audit",), ("--check",)):
            with self.subTest(args=args):
                result = self.run_lever(*args)
                self.assertEqual(result.returncode, 1, result.stderr)
                self.assertIn("cannot read the system name: uname -s failed", result.stderr)
        (self.bin / "uname").unlink()
        db = self.register().parent.parent / "agent.db"
        write_exec(self.bin / "date", "#!/bin/sh\nexit 1\n")
        result = self.run_lever("--check", "audit")
        self.assertEqual(
            (result.returncode, result.stdout), (1, f"audit openai-siwc: unreadable (cannot read the mtime of {db})\n")
        )
        (self.bin / "date").unlink()
        # The token judge (U551) has two states and no third: a `stat` or `wc` that fails on a placed file is `token
        # absent (cannot read ...)` in `--check` (exit 0) and the two steps in the profile mode (exit 2), never a pass;
        # a jq that fails touches the Claude route not at all.
        token = self.place_token()
        remote = "100.64.0.2 50000 100.64.0.3 22"
        for tool, reason in (("stat", f"cannot read the mode of {token}"), ("wc", f"cannot read the size of {token}")):
            with self.subTest(tool=tool):
                write_exec(self.bin / tool, "#!/bin/sh\nexit 1\n")
                result = self.run_lever("--check", "orchestrator")
                self.assertEqual(
                    (result.returncode, result.stdout), (0, f"orchestrator claude-bridge: token absent ({reason})\n")
                )
                gate = self.run_lever("orchestrator", SSH_CONNECTION=remote)
                self.assertEqual(gate.returncode, 2, gate.stderr)
                self.assertEqual(gate.stderr, self.refusal(f"orchestrator claude-bridge: token absent ({reason})"))
                (self.bin / tool).unlink()
        write_exec(self.bin / "jq", "#!/bin/sh\nexit 5\n")
        result = self.run_lever("--check", "orchestrator")
        self.assertEqual(
            (result.returncode, result.stdout), (0, f"orchestrator claude-bridge: {self.token_present()}\n")
        )
        (self.bin / "jq").unlink()
        token.unlink()
        # The overlay enumeration needs no external producer.
        write_exec(self.bin / "basename", "#!/bin/sh\nexit 1\n")
        result = self.run_lever("--check")
        self.assertEqual(
            [line.split(":")[0] for line in result.stdout.splitlines()],
            ["audit openai-siwc", "orchestrator claude-bridge", "worker claude-bridge"],
        )
        self.assertNotIn("auth login", self.calls_text())

    def test_a_registration_without_a_stored_login_is_not_ready(self) -> None:
        remote = "100.64.0.2 50000 100.64.0.3 22"
        db = self.register().parent.parent / "agent.db"
        check = self.run_lever("--check", "audit", FAKE_SIWC_LOGINS="0")
        self.assertEqual(check.returncode, 0)
        self.assertTrue(check.stdout.startswith(f"audit openai-siwc: registered (host {HOST_ID}"), check.stdout)
        self.assertEqual(self.bun_calls_text(), "", "--check stays metadata only")
        gate = self.run_lever("audit", SSH_CONNECTION=remote, FAKE_SIWC_LOGINS="0")
        self.assertEqual(gate.returncode, 2, gate.stderr)
        self.assertIn(
            f"audit openai-siwc: absent (registered: host {HOST_ID}, client oaiapp_fake; no openai-siwc login in {db});"
            " a login is the operator's step",
            gate.stderr,
        )
        script = self.home / ".agents/omp/extensions/openai-siwc/src/credentials.ts"
        self.assertEqual(self.bun_calls_text(), f"bun {script} --profile audit\n")
        for extra in ({"FAKE_BUN_FAILS": "1"}, {"FAKE_SIWC_LOGINS": "many"}):
            with self.subTest(**extra):
                broken = self.run_lever("audit", SSH_CONNECTION=remote, **extra)
                self.assertEqual(broken.returncode, 1, broken.stderr)
                self.assertIn(f"unreadable (cannot count the openai-siwc logins in {db}); fix or move", broken.stderr)
        # In the operator's terminal the same state is a login to run, and a login that stores nothing fails.
        status, output = self.run_tty("audit", SSH_CONNECTION=remote, FAKE_SIWC_LOGINS="0")
        self.assertEqual(status, 1, output)
        self.assertIn("omp --profile audit login openai-siwc\n", self.calls_text())
        self.assertIn("no openai-siwc login in", output)
        self.assertIn("after the login", output)

    def test_readiness_counts_the_token_file_alone(self) -> None:
        """U551: a seat starts on the seats' Claude token file alone. A credentials file of the operator's own
        `~/.claude`, a login directory of the group under the seats root and a token variable in the environment are
        no input (U190, U312, U318): without the file the profile mode refuses naming the two steps, in the operator's
        terminal too, running nothing; with the file placed it passes whatever the environment holds, and no `claude`
        process runs."""
        remote = "100.64.0.2 50000 100.64.0.3 22"
        credentials = self.home / ".claude/.credentials.json"
        credentials.parent.mkdir()
        credentials.write_text("{}")
        credentials.chmod(0o600)
        self.shared.mkdir(parents=True)
        (self.shared / ".credentials.json").write_text("{}")
        variable_only = self.run_lever("orchestrator", SSH_CONNECTION=remote, **{TOKEN_VARIABLE: FAKE_OAUTH_VALUE})
        self.assertEqual(variable_only.returncode, 2, variable_only.stderr)
        self.assertEqual(variable_only.stderr, self.refusal(f"orchestrator claude-bridge: {self.token_absent()}"))
        for profile in ("worker", "orchestrator"):
            with self.subTest(profile=profile):
                refused = self.run_lever(profile, SSH_CONNECTION=remote)
                self.assertEqual(refused.returncode, 2, refused.stderr)
                self.assertEqual(refused.stderr, self.refusal(f"{profile} claude-bridge: {self.token_absent()}"))
        status, output = self.run_tty("worker", SSH_CONNECTION=remote)
        self.assertEqual(status, 2, output)
        self.assertIn(f"worker claude-bridge: {self.token_absent()}; {self.STEPS}", output)
        self.place_token()
        present = self.run_lever("orchestrator", SSH_CONNECTION=remote, **{TOKEN_VARIABLE: FAKE_OAUTH_VALUE})
        self.assertEqual(present.returncode, 0, present.stderr)
        self.assertEqual(present.stderr, f"seat-login-preflight: orchestrator claude-bridge: {self.token_present()}\n")
        status, tty = self.run_tty("worker", SSH_CONNECTION=remote)
        self.assertEqual(status, 0, tty)
        self.assertIn(f"seat-login-preflight: worker claude-bridge: {self.token_present()}", tty)
        self.assertEqual(self.calls_text(), "", "no login, no omp, no claude")
        self.assertEqual(credentials.read_text(), "{}")
        for text in (variable_only.stderr, refused.stderr, output, present.stderr, tty):
            self.assertNotIn(FAKE_OAUTH_VALUE, text)
            self.assertNotIn(FAKE_OAT, text)


class SeatTokenPlaceTest(unittest.TestCase):
    """`seat-token-place` (U551): the operator's one writer of `<seats-root>/.state/claude-token`, run against a scratch
    HOME and seats root with the token on stdin; nothing of a real token or terminal is touched."""

    def setUp(self) -> None:
        # Physical (macOS's TMPDIR lies under the /var link): the lever refuses a link anywhere in the root's path (U552).
        self.temp = Path(tempfile.mkdtemp(prefix="seat-token-place-")).resolve()
        self.home = self.temp / "home"
        self.home.mkdir()
        self.bin = self.temp / "bin"
        self.bin.mkdir()
        self.seats = self.temp / "seats"
        self.token = self.seats / ".state/claude-token"

    def tearDown(self) -> None:
        for path in self.temp.rglob("*"):
            if path.is_dir() and not path.is_symlink() and not os.access(path, os.R_OK | os.X_OK):
                path.chmod(0o700)
        shutil.rmtree(self.temp)

    def run_placer(
        self, *args: str, stdin: str | None, env: dict[str, str] | None = None, cwd: Path | None = None
    ) -> subprocess.CompletedProcess[str]:
        environment = {"HOME": str(self.home), "PATH": f"{self.bin}:/usr/bin:/bin", "TMPDIR": str(self.temp)}
        environment.update(env or {})
        return subprocess.run(
            [str(PLACER), *args], env=environment, cwd=cwd or self.temp, input=stdin,
            stdin=None if stdin is not None else subprocess.DEVNULL, capture_output=True, text=True, check=False,
        )  # fmt: skip

    def assert_placed(self, result: subprocess.CompletedProcess[str], token: str = FAKE_OAT) -> None:
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, f"seat-token-place: placed {self.token} ({len(token)} characters, mode 0600)\n")
        self.assertEqual(result.stderr, "token: \n", "the prompt and the newline after the hidden input alone")
        self.assertEqual(self.token.read_text(), token + "\n")
        self.assertEqual(stat.S_IMODE(os.lstat(self.token).st_mode), 0o600)
        self.assertTrue(self.token.is_file() and not self.token.is_symlink())
        for path in (self.seats, self.seats / ".state"):
            self.assertTrue(path.is_dir() and not path.is_symlink(), path)
        self.assertEqual(stat.S_IMODE(os.lstat(self.seats / ".state").st_mode), 0o700)
        self.assertEqual(
            sorted(p.name for p in (self.seats / ".state").iterdir()), ["claude-token"], "no temporary left"
        )
        self.assertNotIn(token, result.stdout + result.stderr)

    def test_the_placer_writes_one_0600_line_in_the_0700_chain_and_prints_the_count_alone(self) -> None:
        """The fixture token pasted at the prompt: the chain is made 0700 under umask 077, the file holds the one line
        with one line feed, mode 0600, and the one stdout line names the file and the character count, never the
        token; the prompt and a newline are the whole of stderr. A 0644 previous file refuses before the prompt,
        naming its mode, and stays byte for byte (U552, verdict U552-484346a3 P2: the previous token lay readable and
        is the operator's to settle first); tightened to 0600 it is replaced through the exclusive temporary (0600
        again, no temporary left, `.state` tightened to 0700), and the placed file reads `token present` in the
        pre-flight and `--check`."""
        self.assert_placed(self.run_placer("--seats-root", str(self.seats), stdin=FAKE_OAT + "\n"))
        self.assertEqual(stat.S_IMODE(os.lstat(self.seats).st_mode), 0o700, "a root this lever made is 0700")
        self.token.write_text("old\n")
        self.token.chmod(0o644)
        (self.seats / ".state").chmod(0o755)
        second = "sk-ant-oat01-" + "SECONDFIXTURETOKEN" + "1" * 42
        wide = self.run_placer("--seats-root", str(self.seats), stdin=second + "\n")
        self.assertEqual((wide.returncode, wide.stdout), (1, ""), wide.stderr)
        self.assertEqual(wide.stderr, f"seat-token-place: refused: {self.token} has mode 644, not 0600; remove it or chmod 600 it, then run again (nothing written)\n")  # fmt: skip
        self.assertEqual(self.token.read_text(), "old\n")
        self.assertEqual(stat.S_IMODE(os.lstat(self.token).st_mode), 0o644)
        self.assertEqual(sorted(p.name for p in (self.seats / ".state").iterdir()), ["claude-token"], "no temporary")
        self.assertNotIn(second, wide.stderr)
        self.assertNotIn("token: ", wide.stderr, "refused before the prompt")
        self.token.chmod(0o600)
        self.assert_placed(self.run_placer("--seats-root", str(self.seats), stdin=second + "\n"), second)
        # The pre-flight reads the placed file as present, by the same form.
        profiles = self.home / ".agents/omp/profiles"
        profiles.mkdir(parents=True)
        (profiles / "orchestrator.yml").write_text("modelRoles:\n  default: claude-bridge/claude-fable-5-2\n")
        check = subprocess.run(
            [str(PREFLIGHT), "--check", "orchestrator"],
            env={"HOME": str(self.home), "PATH": f"{self.bin}:/usr/bin:/bin", "REGIME_SEATS_ROOT": str(self.seats)},
            capture_output=True, text=True, check=False, stdin=subprocess.DEVNULL,
        )  # fmt: skip
        self.assertEqual(
            (check.returncode, check.stdout), (0, f"orchestrator claude-bridge: token present ({self.token})\n")
        )

    def test_a_pasted_line_is_stripped_of_csi_sequences_a_carriage_return_and_whitespace(self) -> None:
        """A terminal's bracketed paste wraps the line in `ESC [ 200 ~` and `ESC [ 201 ~`, a Windows clipboard adds a
        carriage return and a pasted line may carry spaces or a tab at either end: each is stripped and the token is
        placed as its own characters; the count is the token's."""
        for label, stdin in (
            ("a bracketed paste", f"\x1b[200~{FAKE_OAT}\x1b[201~\n"),
            ("a carriage return", f"{FAKE_OAT}\r\n"),
            ("surrounding whitespace", f"  \t{FAKE_OAT} \n"),
            ("a paste with other CSI sequences", f"\x1b[?2004l\x1b[200~ {FAKE_OAT}\x1b[201~\x1b[0m\r\n"),
            ("a partial line then EOF", FAKE_OAT),
        ):
            with self.subTest(label=label):
                if self.seats.exists():
                    shutil.rmtree(self.seats)
                self.assert_placed(self.run_placer("--seats-root", str(self.seats), stdin=stdin))

    def test_eof_empty_csi_only_and_off_form_inputs_write_nothing_and_print_the_count_alone(self) -> None:
        """The failure injections of the brief: an end of input before a line, an empty line, a line of CSI sequences
        alone, a line off the token's form (a key, a short token, a token with a space or a carriage return inside)
        and, since U552, a second line behind the first (with or without its line feed; round 3, verdict
        U552-953af858 P2: a blank one, a blank one with more behind it and one of spaces, which round 2 passed by
        judging the bytes read instead of the read's status) each refuse (exit 1) naming the character count after
        stripping or the second line, and never the input; nothing is written, not even the chain's directories'
        content beyond the empty `.state`, and a previous file survives byte for byte."""
        self.assert_placed(self.run_placer("--seats-root", str(self.seats), stdin=FAKE_OAT + "\n"))
        before = self.token.read_bytes()
        cases = (
            ("EOF", None, "no token was read (end of input before a line; nothing written)"),
            ("an empty line", "\n", "the input is empty after stripping (nothing written)"),
            ("CSI sequences alone", "\x1b[200~\x1b[201~\n", "the input is empty after stripping (nothing written)"),
            ("whitespace alone", "   \n", "the input is empty after stripping (nothing written)"),
            ("a key, not a token", "sk-ant-api03-" + "NOTATOKEN" + "0" * 40 + "\n", "the input (62 characters after stripping) is not a token of the form"),
            ("a short token", "sk-ant-oat01-" + "short\n", "the input (18 characters after stripping) is not a token of the form"),
            ("a space inside", FAKE_OAT[:30] + " " + FAKE_OAT[30:] + "\n", f"the input ({len(FAKE_OAT) + 1} characters after stripping) is not a token of the form"),
            ("a carriage return inside", FAKE_OAT[:30] + "\r" + FAKE_OAT[30:] + "\n", f"the input ({len(FAKE_OAT) + 1} characters after stripping) is not a token of the form"),
            ("a second line", FAKE_OAT + "\nsecond\n", "the input holds more than one line (nothing written)"),
            ("a second line without its line feed", FAKE_OAT + "\nx", "the input holds more than one line (nothing written)"),
            ("a blank second line", FAKE_OAT + "\n\n", "the input holds more than one line (nothing written)"),
            ("a blank second line with more behind it", FAKE_OAT + "\n\nsecond\n", "the input holds more than one line (nothing written)"),
            ("a second line of spaces", FAKE_OAT + "\n   \n", "the input holds more than one line (nothing written)"),
        )  # fmt: skip
        for label, stdin, reason in cases:
            with self.subTest(label=label):
                result = self.run_placer("--seats-root", str(self.seats), stdin=stdin)
                self.assertEqual((result.returncode, result.stdout), (1, ""), result.stderr)
                self.assertTrue(result.stderr.startswith("token: \n"), result.stderr)
                self.assertIn(f"seat-token-place: refused: {reason}", result.stderr)
                if stdin and stdin.strip().replace("\x1b", ""):
                    self.assertNotIn(stdin.strip().replace("\x1b", ""), result.stderr, "the input is never printed")
                self.assertNotIn("NOTATOKEN", result.stderr)
                self.assertEqual(self.token.read_bytes(), before, "the previous file is untouched")
                self.assertEqual(
                    sorted(p.name for p in (self.seats / ".state").iterdir()), ["claude-token"], "no temporary left"
                )
        # Without a previous file nothing is written at all: the chain alone, empty.
        self.token.unlink()
        result = self.run_placer("--seats-root", str(self.seats), stdin="not-a-" + "token\n")
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertEqual(sorted(p.name for p in (self.seats / ".state").iterdir()), [])
        self.assertNotIn("not-a-" + "token", result.stderr)

    def test_a_link_in_the_chain_or_at_the_destination_refuses_with_nothing_written_through_it(self) -> None:
        """A symbolic link at the seats root, at `.state` or at the destination refuses (exit 1) before the token is
        read, naming the link; nothing is written at the link's target, and a file at `.state` or a root of another
        user refuses the same way. Since U552 a link above the root (`--seats-root <link>/seats`) refuses the same
        way, by lstat on the link before anything is made (verdict U552-484346a3 P2: round 1 wrote through it)."""
        elsewhere = self.temp / "elsewhere"
        elsewhere.mkdir()
        target = elsewhere / "target"
        target.write_text("target\n")
        self.seats.mkdir(mode=0o700)
        (self.seats / ".state").mkdir(mode=0o700)
        self.token.symlink_to(target)
        result = self.run_placer("--seats-root", str(self.seats), stdin=FAKE_OAT + "\n")
        self.assertEqual((result.returncode, result.stdout), (1, ""), result.stderr)
        self.assertEqual(result.stderr, f"seat-token-place: refused: {self.token} is a symbolic link; the token file must be a regular file of this user (nothing written)\n")  # fmt: skip
        self.assertEqual(target.read_text(), "target\n")
        self.assertTrue(self.token.is_symlink(), "the link is neither removed nor replaced")
        self.token.unlink()
        for linked in (self.seats / ".state", self.seats):
            with self.subTest(linked=linked):
                shutil.rmtree(linked)
                linked.symlink_to(elsewhere)
                result = self.run_placer("--seats-root", str(self.seats), stdin=FAKE_OAT + "\n")
                self.assertEqual((result.returncode, result.stdout), (1, ""), result.stderr)
                self.assertEqual(result.stderr, f"seat-token-place: refused: {linked} is a symbolic link; the seats root and its .state must be real directories of this user (nothing written)\n")  # fmt: skip
                self.assertEqual(
                    sorted(p.name for p in elsewhere.iterdir()), ["target"], "nothing written through the link"
                )
                linked.unlink()
        self.seats.mkdir(mode=0o700)
        (self.seats / ".state").write_text("")
        result = self.run_placer("--seats-root", str(self.seats), stdin=FAKE_OAT + "\n")
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn(f"{self.seats}/.state is not a directory of this user (nothing written)", result.stderr)
        self.assertNotIn(FAKE_OAT, result.stderr)
        self.assertEqual(sorted(p.name for p in elsewhere.iterdir()), ["target"])
        # U552: a link above the root refuses before anything is made or read; nothing is written through it.
        linked_parent = self.temp / "linked-parent"
        linked_parent.symlink_to(elsewhere)
        result = self.run_placer("--seats-root", f"{linked_parent}/seats", stdin=FAKE_OAT + "\n")
        self.assertEqual((result.returncode, result.stdout), (1, ""), result.stderr)
        self.assertEqual(result.stderr, f"seat-token-place: refused: {linked_parent} is a symbolic link above the seats root; every directory of the root's path must be real (nothing written)\n")  # fmt: skip
        self.assertEqual(sorted(p.name for p in elsewhere.iterdir()), ["target"], "nothing made through the link")
        self.assertNotIn("token: ", result.stderr, "refused before the prompt")

    def test_a_callers_exported_token_variable_reaches_no_child_of_the_placer(self) -> None:
        """U552 (verdict U552-484346a3 P1): the variable the pasted line is read into is unset before the read, so a
        caller's exported `token` (whose export attribute a plain read would keep) carries the pasted line into neither
        mktemp's environment nor any other child; the placement itself is unchanged."""
        record = self.temp / "mktemp-env"
        write_exec(
            self.bin / "mktemp",
            f'#!/bin/sh\nprintf \'%s\\n\' "${{token-unset}}" >> {record}\nexec /usr/bin/mktemp "$@"\n',
        )
        result = self.run_placer(
            "--seats-root", str(self.seats), stdin=FAKE_OAT + "\n", env={"token": "caller-" + "exported-value"}
        )
        self.assert_placed(result)
        self.assertEqual(record.read_text(), "unset\n", "the pasted line reached no child's environment")
        (self.bin / "mktemp").unlink()

    def test_a_failed_temporary_leaves_the_previous_file_byte_for_byte(self) -> None:
        """A `mktemp` that fails, or one that names a path outside `.state`, refuses after the token was read and
        before anything is renamed: the previous file is byte for byte what it was, no temporary stays behind and the
        token is printed nowhere."""
        self.assert_placed(self.run_placer("--seats-root", str(self.seats), stdin=FAKE_OAT + "\n"))
        before = self.token.read_bytes()
        second = "sk-ant-oat01-" + "SECONDFIXTURETOKEN" + "1" * 42
        for label, body, reason in (
            ("mktemp fails", "#!/bin/sh\nexit 1\n", f"cannot make a temporary file in {self.seats}/.state (nothing written)"),
            ("mktemp names a path elsewhere", f"#!/bin/sh\nprintf '%s\\n' {self.temp}/nowhere/claude-token.tmp\n", f"mktemp made no regular file under {self.seats}/.state (nothing written)"),
        ):  # fmt: skip
            with self.subTest(label=label):
                write_exec(self.bin / "mktemp", body)
                result = self.run_placer("--seats-root", str(self.seats), stdin=second + "\n")
                self.assertEqual((result.returncode, result.stdout), (1, ""), result.stderr)
                self.assertIn(f"seat-token-place: refused: {reason}", result.stderr)
                self.assertEqual(self.token.read_bytes(), before)
                self.assertEqual(sorted(p.name for p in (self.seats / ".state").iterdir()), ["claude-token"])
                self.assertNotIn(second, result.stdout + result.stderr)
        (self.bin / "mktemp").unlink()

    def test_a_failing_uname_or_stat_refuses_before_the_prompt_and_writes_nothing(self) -> None:
        """Round 3 (verdict U552-953af858 P2; standing order 21): the placer's two producers, `uname -s` for the one
        stat form and `stat` for a present destination's mode, are read with their status and their output's shape: a
        uname that prints a system name and fails refuses (exit 2) before the chain is made; a stat that prints a
        plausible mode and fails, prints nothing or prints no octal mode refuses (exit 1) naming the destination,
        before the prompt; nothing is written, the previous file is byte for byte what it was and no temporary stays."""
        write_exec(self.bin / "uname", "#!/bin/sh\necho Darwin\nexit 1\n")
        result = self.run_placer("--seats-root", str(self.seats), stdin=FAKE_OAT + "\n")
        self.assertEqual((result.returncode, result.stdout), (2, ""), result.stderr)
        self.assertEqual(result.stderr, "seat-token-place: refused: cannot read the system name: uname -s failed\n")
        self.assertFalse(self.seats.exists() or self.seats.is_symlink(), "refused before the chain is made")
        (self.bin / "uname").unlink()
        self.assert_placed(self.run_placer("--seats-root", str(self.seats), stdin=FAKE_OAT + "\n"))
        before = self.token.read_bytes()
        second = "sk-ant-oat01-" + "SECONDFAKETOKEN" + "1" * 44
        for label, body in (
            ("stat prints a mode and fails", "#!/bin/sh\necho 600\nexit 7\n"),
            ("stat prints nothing", "#!/bin/sh\nexit 0\n"),
            ("stat prints no octal mode", "#!/bin/sh\necho rw-------\n"),
        ):
            with self.subTest(label=label):
                write_exec(self.bin / "stat", body)
                result = self.run_placer("--seats-root", str(self.seats), stdin=second + "\n")
                self.assertEqual((result.returncode, result.stdout), (1, ""), result.stderr)
                self.assertEqual(
                    result.stderr,
                    f"seat-token-place: refused: cannot read the mode of {self.token} (nothing written)\n",
                )
                self.assertNotIn("token: ", result.stderr, "refused before the prompt")
                self.assertEqual(self.token.read_bytes(), before, "the previous file is untouched")
                self.assertEqual(
                    sorted(p.name for p in (self.seats / ".state").iterdir()), ["claude-token"], "no temporary left"
                )
                self.assertNotIn(second, result.stdout + result.stderr)
        (self.bin / "stat").unlink()
        self.assert_placed(self.run_placer("--seats-root", str(self.seats), stdin=second + "\n"), token=second)

    def test_the_seats_root_comes_from_the_option_the_environment_or_the_checkout_and_must_be_clean(self) -> None:
        """Without `--seats-root` the root is `REGIME_SEATS_ROOT`, else `~/.local/state/omp-seats/<slug>` of the
        checkout the lever runs in (regime-env's slug, as the pre-flight derives it); outside a checkout with neither
        it refuses (exit 2) before reading anything; a relative root, one with `..` or a trailing slash is refused
        (exit 2) as unclean; a usage error is exit 2 too."""
        env_root = self.run_placer(stdin=FAKE_OAT + "\n", env={"REGIME_SEATS_ROOT": str(self.seats)})
        self.assert_placed(env_root)
        shutil.rmtree(self.seats)
        derived = self.run_placer(stdin=FAKE_OAT + "\n", cwd=ROOT)
        self.assertEqual(derived.returncode, 0, derived.stderr)
        self.assertRegex(
            derived.stdout,
            rf"^seat-token-place: placed {re.escape(str(self.home.resolve()))}/\.local/state/omp-seats/[a-z0-9][a-z0-9_-]{{0,39}}/\.state/claude-token \({len(FAKE_OAT)} characters, mode 0600\)\n$",
        )
        outside = self.run_placer(stdin=FAKE_OAT + "\n")
        self.assertEqual((outside.returncode, outside.stdout), (2, ""), outside.stderr)
        self.assertIn(
            "no seats root: pass --seats-root, set REGIME_SEATS_ROOT or run inside a checkout", outside.stderr
        )
        for bad in ("seats", f"{self.seats}/", f"{self.seats}/../seats", f"{self.temp}/a b"):
            with self.subTest(root=bad):
                result = self.run_placer("--seats-root", bad, stdin=FAKE_OAT + "\n")
                self.assertEqual((result.returncode, result.stdout), (2, ""), result.stderr)
                self.assertIn("is not a clean absolute path", result.stderr)
        usage = self.run_placer("--nope", stdin=FAKE_OAT + "\n")
        self.assertEqual(usage.returncode, 2, usage.stderr)
        self.assertIn("usage: seat-token-place [--seats-root <dir>]", usage.stderr)
        for result in (outside, usage):
            self.assertNotIn(FAKE_OAT, result.stdout + result.stderr)
        self.assertNotIn("token" + ": ", outside.stderr + usage.stderr, "refused before the prompt")

    def test_the_token_form_is_one_text_across_the_three_levers(self) -> None:
        """The token's form (`TOKEN_FORM_RE`) is one text in hcom-seat, seat-login-preflight and seat-token-place, so
        no lever admits a line another refuses (U551b adds acp-broker, which hands the token to its workers)."""
        forms = {}
        for lever in (HCOM_SEAT, PREFLIGHT, PLACER):
            (line,) = [l for l in lever.read_text().splitlines() if l.startswith("TOKEN_FORM_RE=")]
            forms[lever.name] = line
        self.assertEqual(len(set(forms.values())), 1, forms)
        self.assertEqual(forms["hcom-seat"], "TOKEN_FORM_RE='^sk-ant-oat01-[A-Za-z0-9_-]{20,255}$'")
        self.assertRegex(FAKE_OAT, r"^sk-ant-oat01-[A-Za-z0-9_-]{20,255}$")


if __name__ == "__main__":
    unittest.main()
