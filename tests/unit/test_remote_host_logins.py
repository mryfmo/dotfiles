"""Seat logins on a remote host (regime-cutover U37): the laptop URL opener and its seat-host client, the
token export, the SSH forwards, the launchd agent and the seat-login pre-flight lever. Everything runs
against scratch homes and fake openers; no test opens a browser or reads a real login."""

import http.server
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
import threading
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
# The fake API key the preflight tests place (regime-cutover U512), built at runtime so no file holds a literal the
# secret scan matches; it rides to the fake Models API in the `x-api-key` header and must appear in no line.
FAKE_KEY = "sk-" + "ant-api03-" + "FAKEKEYFORTEST" + "0" * 12


def fake_models_api(case: unittest.TestCase, answer: int | str) -> tuple[str, list[dict[str, str]]]:
    """Start a fake Models API on the loopback for the lifetime of `case`: every GET is recorded (path, `x-api-key`,
    `anthropic-version`) in the returned list, and answered with the HTTP status `answer`, or left hanging past the
    lever's 20 s alarm when `answer` is "hang". Returns the URL the lever is pointed at (REGIME_ANTHROPIC_MODELS_URL)
    and the record list."""
    requests: list[dict[str, str]] = []
    release = threading.Event()

    class Handler(http.server.BaseHTTPRequestHandler):
        def do_GET(self) -> None:
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
            self.send_response(int(answer))
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, *args: object) -> None:
            pass

    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    server.daemon_threads = True
    threading.Thread(target=server.serve_forever, daemon=True).start()
    case.addCleanup(server.server_close)
    case.addCleanup(server.shutdown)
    case.addCleanup(release.set)
    return f"http://127.0.0.1:{server.server_address[1]}/v1/models?limit=1", requests


def closed_loopback_url() -> str:
    """A loopback URL nothing listens on, the fixture's default Models API: a lever that calls it gets a refused
    connection (`unreadable`), never the real API, so no unit test reaches the network."""
    with socket.socket() as probe:
        probe.bind(("127.0.0.1", 0))
        port = probe.getsockname()[1]
    return f"http://127.0.0.1:{port}/v1/models?limit=1"


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

    def test_no_lever_or_rc_file_names_the_token_file_or_setup_token(self) -> None:
        """U318: the token file and `claude setup-token` retire from code: neither lever (source and installed copy)
        nor an rc file names them."""
        for path in (
            ZSHENV,
            PROFILE,
            PREFLIGHT,
            HCOM_SEAT,
            *(COMMON / f"executable_{lever.name}" for lever in (PREFLIGHT, HCOM_SEAT)),
        ):
            with self.subTest(path=str(path.relative_to(ROOT))):
                text = path.read_text()
                for needle in ("oauth-token", "setup-token"):
                    self.assertNotIn(needle, text)


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
        (profiles / "orchestrator.yml").write_text("modelRoles:\n  default: claude-bridge/claude-fable-5-1\n")
        (profiles / "worker.yml").write_text("modelRoles:\n  default: claude-bridge/claude-opus-5-5\n")
        # The seats root the shared Claude Code directory lives in (U318), passed as hcom-seat passes its resolved one.
        self.seats = self.temp / "seats"
        self.shared = self.seats / ".state/claude"
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
        # `claude auth status` (U318): the documented record with the method FAKE_CLAUDE_AUTH_METHOD (`claude.ai` unless
        # set) or the body FAKE_CLAUDE_AUTH_BODY when set, exit FAKE_CLAUDE_AUTH_STATUS (0 unless set); every call is
        # recorded with its directory, BROWSER and whether a token name reached it. A login is never run (exit 64).
        write_exec(
            self.bin / "claude",
            f"""#!/bin/sh
printf 'claude %s CLAUDE_CONFIG_DIR=%s BROWSER=%s token=%s\\n' "$*" "${{CLAUDE_CONFIG_DIR-unset}}" "${{BROWSER-unset}}" "${{{TOKEN_VARIABLE}-unset}}" >> "{self.calls}"
[ "$1 $2" = "auth status" ] || exit 64
if [ -n "${{FAKE_CLAUDE_AUTH_BODY-}}" ]; then printf '%s\\n' "${{FAKE_CLAUDE_AUTH_BODY}}"
else printf '{{"loggedIn": true, "configDirectory": "%s", "authMethod": "%s"}}\\n' "${{CLAUDE_CONFIG_DIR-}}" "${{FAKE_CLAUDE_AUTH_METHOD:-claude.ai}}"
fi
exit "${{FAKE_CLAUDE_AUTH_STATUS:-0}}"
""",
        )
        # The seats' API key file (U512), `<seats-root>/.state/anthropic/api-key`, the one input of the Claude route.
        self.key_dir = self.seats / ".state/anthropic"
        self.key_file = self.key_dir / "api-key"
        # `claude-keyed --check` (U512, the U510 lever): the form judge of the key file. This fake records each call
        # with the file the environment named; unless FAKE_CLAUDE_KEYED_STATUS forces a status, it answers as the real
        # lever does for the one thing these tests vary, the file's presence: the ok line (exit 0) when the file is
        # there, the lever's absent-file refusal (exit 2) when not; FAKE_CLAUDE_KEYED_REASON replaces the reason, and
        # a forced status that is neither 0 nor 2 prints a line and exits with it (unreadable to the lever).
        write_exec(
            self.bin / "claude-keyed",
            f"""#!/bin/sh
printf 'claude-keyed %s REGIME_ANTHROPIC_KEY_FILE=%s\\n' "$*" "${{REGIME_ANTHROPIC_KEY_FILE-unset}}" >> "{self.calls}"
[ "$1" = --check ] && [ $# -eq 1 ] || exit 64
status=${{FAKE_CLAUDE_KEYED_STATUS-}}
if [ -z "$status" ]; then if [ -f "${{REGIME_ANTHROPIC_KEY_FILE-}}" ]; then status=0; else status=2; fi; fi
case "$status" in
0) printf 'key file ok: %s; executable: /fake/sdk/claude\\n' "${{REGIME_ANTHROPIC_KEY_FILE-}}"; exit 0 ;;
2) printf 'claude-keyed: refused: %s\\n' "${{FAKE_CLAUDE_KEYED_REASON:-the key file ${{REGIME_ANTHROPIC_KEY_FILE-}} is absent; place the API key there (the U510 handout)}}" >&2; exit 2 ;;
*) printf 'claude-keyed: refused: cannot read the mode and owner of the key file (stat failed)\\n' >&2; exit "$status" ;;
esac
""",
        )
        # The Models API the lever calls (U512): a loopback port nothing listens on unless a test starts a fake
        # (models_api), so no test reaches the real API.
        self.models_url = closed_loopback_url()

    def tearDown(self) -> None:
        shutil.rmtree(self.temp)

    def env(self, **extra: str) -> dict[str, str]:
        env = {
            "HOME": str(self.home), "PATH": f"{self.bin}:{os.environ['PATH']}", "TMPDIR": str(self.temp),
            "REGIME_SEATS_ROOT": str(self.seats), "REGIME_ANTHROPIC_MODELS_URL": self.models_url,
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

    def absent_line(self, profile: str, root: Path | None = None) -> str:
        """The state line of a Claude-route profile with no key file under `root` (the fixture's seats root unless
        given): the fake lever's refusal reason, the real lever's text for an absent file."""
        key = (root or self.seats) / ".state/anthropic/api-key"
        return f"{profile} claude-bridge: absent (the key file {key} is absent; place the API key there (the U510 handout))"

    def key_step(self, root: Path | None = None) -> str:
        """The operator's two steps the lever prints for an absent or rejected key (the U510 handout's steps 2 and 3),
        for a root whose paths need no quoting."""
        key_dir = (root or self.seats) / ".state/anthropic"
        key = key_dir / "api-key"
        return (
            f"(umask 077; mkdir -p {key_dir}; printf 'key: '; IFS= read -rs k; printf '%s\\n' \"$k\" > {key}; unset k;"
            f" echo) && REGIME_ANTHROPIC_KEY_FILE={key} claude-keyed --check"
        )

    def refusal(self, line: str, root: Path | None = None) -> str:
        """The profile mode's refusal for an absent or rejected key: the state line, then the two steps."""
        return (
            f"seat-login-preflight: {line}; place the key once: {self.key_step(root)}; the key is the operator's step"
            " (handouts/anthropic-api-key-u510.md, steps 2 and 3): run those commands in your own terminal on this"
            " host, then start the seat again\n"
        )

    def place_key(self, root: Path | None = None) -> Path:
        """Place the fake key as the handout does: one line, 0600, in the 0700 `.state/anthropic` directory."""
        key_dir = (root or self.seats) / ".state/anthropic"
        key_dir.mkdir(parents=True, exist_ok=True)
        key_dir.chmod(0o700)
        key = key_dir / "api-key"
        key.write_text(FAKE_KEY + "\n")
        key.chmod(0o600)
        return key

    def models_api(self, answer: int | str) -> str:
        """A fake Models API answering `answer`; its request record is `self.models_requests`."""
        url, self.models_requests = fake_models_api(self, answer)
        return url

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
        self.assertEqual(lines[1:], [self.absent_line("orchestrator"), self.absent_line("worker")])

    def test_check_judges_the_key_by_claude_keyed_and_the_models_api_and_never_prints_the_key(self) -> None:
        """U512: `--check` judges the Claude route by the seats' API key file `<seats-root>/.state/anthropic/api-key`:
        its form by one `claude-keyed --check` (the lever's refusal reason is the absent line, and no call reaches the
        API then), its validity by one `GET /v1/models?limit=1` with the key in `x-api-key` (python3 reads it from the
        file; no argument or environment holds it): 200 is `key ok`, 401 and 403 `key rejected`, any other code, a
        hang past the 20 s alarm, a refused connection, a claude-keyed status that is neither 0 nor 2 and a Models API
        URL off the loopback are unreadable (exit 1), never absent. The key's bytes reach no line, a token variable in
        the environment is no input, and `claude auth status` is never called."""
        key = str(self.key_file)
        token = {TOKEN_VARIABLE: FAKE_OAUTH_VALUE}
        url = self.models_api(200)
        result = self.run_lever("--check", "orchestrator", REGIME_ANTHROPIC_MODELS_URL=url, **token)
        self.assertEqual(
            (result.returncode, result.stdout), (0, f"{self.absent_line('orchestrator')}\n"), result.stderr
        )
        self.assertEqual(self.calls_text(), f"claude-keyed --check REGIME_ANTHROPIC_KEY_FILE={key}\n")
        self.assertEqual(self.models_requests, [], "no call to the API without a key file")
        self.place_key()
        for answer, expected, status in (
            (200, f"key ok ({key})", 0),
            (401, f"key rejected ({key}; HTTP 401)", 0),
            (403, f"key rejected ({key}; HTTP 403)", 0),
            (500, f"unreadable (the Models API answered HTTP 500 for the API key file {key})", 1),
            (404, f"unreadable (the Models API answered HTTP 404 for the API key file {key})", 1),
        ):
            with self.subTest(answer=answer):
                self.calls.unlink()
                url = self.models_api(answer)
                result = self.run_lever("--check", "orchestrator", REGIME_ANTHROPIC_MODELS_URL=url, **token)
                self.assertEqual(
                    (result.returncode, result.stdout),
                    (status, f"orchestrator claude-bridge: {expected}\n"),
                    result.stderr,
                )
                self.assertEqual(
                    self.models_requests,
                    [{"path": "/v1/models?limit=1", "x-api-key": FAKE_KEY, "anthropic-version": "2023-06-01"}],
                )
                self.assertEqual(self.calls_text(), f"claude-keyed --check REGIME_ANTHROPIC_KEY_FILE={key}\n")
                self.assertNotIn(FAKE_KEY, result.stdout + result.stderr)
        # An endpoint that never answers: the alarm (20 s) ends the call, unreadable, never a pass.
        url = self.models_api("hang")
        started = time.monotonic()
        result = self.run_lever("--check", "orchestrator", REGIME_ANTHROPIC_MODELS_URL=url)
        self.assertGreaterEqual(time.monotonic() - started, 19.0)
        self.assertEqual(
            (result.returncode, result.stdout),
            (1, f"orchestrator claude-bridge: unreadable (the Models API did not answer within 20 s for the API key file {key})\n"),
            result.stderr,
        )  # fmt: skip
        # A connection nothing answers (the network denied where this runs) is unreadable, never absent.
        result = self.run_lever("--check", "orchestrator")
        self.assertEqual(
            (result.returncode, result.stdout),
            (1, f"orchestrator claude-bridge: unreadable (the Models API could not be reached for the API key file {key}; the network may be denied where this runs)\n"),
            result.stderr,
        )  # fmt: skip
        # The lever's own refusal of a present file rides as the reason; a status that is neither 0 nor 2 is unreadable.
        reason = f"the key file {key} has mode 644; the key must be readable by this user alone (0600)"
        result = self.run_lever(
            "--check", "orchestrator", FAKE_CLAUDE_KEYED_STATUS="2", FAKE_CLAUDE_KEYED_REASON=reason
        )
        self.assertEqual((result.returncode, result.stdout), (0, f"orchestrator claude-bridge: absent ({reason})\n"))
        result = self.run_lever("--check", "orchestrator", FAKE_CLAUDE_KEYED_STATUS="5")
        self.assertEqual(
            (result.returncode, result.stdout),
            (1, f"orchestrator claude-bridge: unreadable (claude-keyed --check exited 5 for the API key file {key})\n"),
        )
        # The Models API URL may be overridden to a loopback http URL alone (the tests' fake); anything else is refused
        # before a call, so the key never leaves this host for another name.
        for bad in ("https://evil.example/v1/models?limit=1", "http://127.0.0.2:80/", "http://localhost:80/", "file:///etc/passwd"):  # fmt: skip
            with self.subTest(url=bad):
                result = self.run_lever("--check", "orchestrator", REGIME_ANTHROPIC_MODELS_URL=bad)
                self.assertEqual(
                    (result.returncode, result.stdout),
                    (1, f"orchestrator claude-bridge: unreadable (REGIME_ANTHROPIC_MODELS_URL is not a loopback http://127.0.0.1:<port>/ URL; the Models API call for the API key file {key} is refused)\n"),
                )  # fmt: skip
        self.assertNotIn("claude auth", self.calls_text())
        self.assertNotIn(FAKE_KEY, self.calls_text())
        self.assertFalse(self.shared.exists(), "--check makes nothing")

    def test_the_seats_root_derives_from_the_checkout_when_none_is_passed(self) -> None:
        """U318: without REGIME_SEATS_ROOT the shared directory is `~/.local/state/omp-seats/<slug>/.state/claude` of
        the checkout the command runs in (regime-env's slug, HOME in physical form); outside a checkout the Claude
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
            rf"^orchestrator claude-bridge: absent \(the key file {re.escape(str(home))}/\.local/state/omp-seats/[a-z0-9][a-z0-9_-]{{0,39}}/\.state/anthropic/api-key is absent; place the API key there \(the U510 handout\)\)\n$",
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
        self.assertRegex(
            self.calls_text(),
            rf"^claude-keyed --check REGIME_ANTHROPIC_KEY_FILE={re.escape(str(home))}/\.local/state/omp-seats/[a-z0-9][a-z0-9_-]{{0,39}}/\.state/anthropic/api-key\n$",
        )

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
        """U190b, U318, U512: the seat's child runs on the seats' API key wherever it runs, so a local host (no SSH
        session; a display on Linux) without the key file refuses with the handout's two steps, making the shared
        Claude Code directory 0700 with its parents first; one whose key the Models API accepts passes; the operator's
        own `~/.claude` is never an input. Round 1 exited 0 there before any check, and a host-only login started a
        seat whose first bridge turn would end `Not logged in`."""
        credentials = self.home / ".claude/.credentials.json"
        credentials.parent.mkdir()
        credentials.write_text("{}")
        credentials.chmod(0o600)
        key = str(self.key_file)
        no_key = self.run_lever("orchestrator", DISPLAY=":0")
        self.assertEqual(no_key.returncode, 2, no_key.stderr)
        self.assertEqual(no_key.stderr, self.refusal(self.absent_line("orchestrator")))
        for path in (self.seats, self.seats / ".state", self.shared):
            self.assertTrue(path.is_dir() and not path.is_symlink(), path)
            self.assertEqual(stat.S_IMODE(os.lstat(path).st_mode), 0o700, path)
        self.place_key()
        ready = self.run_lever("orchestrator", DISPLAY=":0", REGIME_ANTHROPIC_MODELS_URL=self.models_api(200))
        self.assertEqual(ready.returncode, 0, ready.stderr)
        self.assertEqual(ready.stderr, f"seat-login-preflight: orchestrator claude-bridge: key ok ({key})\n")
        self.assertEqual(self.calls_text(), f"claude-keyed --check REGIME_ANTHROPIC_KEY_FILE={key}\n" * 2)
        self.assertEqual(self.bun_calls_text(), "")
        self.assertEqual(credentials.read_text(), "{}", "the operator's store is untouched")
        self.assertNotIn(FAKE_KEY, no_key.stderr + ready.stderr)

    def assert_component_refused(self, result: subprocess.CompletedProcess[str], path: Path | str, kind: str) -> None:
        """U318b: a bad component of the shared directory chain refuses the lever (exit 2) naming it and its kind."""
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertEqual(
            result.stderr,
            f"seat-login-preflight: refused: the shared Claude Code directory path component {path} is {kind}; move it"
            " aside before a seat starts\n",
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
        """U318b (verdict U318-e0dd8cc2, P2 at :333): `--check` judged the `claude` leaf alone, so a linked `.state`
        parent reached another directory's `claude` and was reported by it. Both modes now hold the seats root,
        `.state` and `claude` to real directories of this user, in this order, and refuse at the first that is not,
        naming it; the SIWC line before it still prints, nothing is made and the link is kept."""
        self.seats.mkdir()
        elsewhere = self.temp / "elsewhere"
        (elsewhere / "claude").mkdir(parents=True)
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
        self.assertEqual(sorted(path.name for path in elsewhere.iterdir()), ["claude"])
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
        `.state/claude` through it. The root is normalised to one spelling before any test (no empty, `.` or `..`
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
                f"seat-login-preflight: refused: cannot read the shared Claude Code directory path component"
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
        root: `--check` prints the one spelling (round 2 printed `<root>//.state/claude` for the first), the profile
        mode makes the chain 0700 at the root and prints the steps with the one spelling, and every call of the key
        judge names the key file in it. A relative root is no seats root (unreadable, never a directory relative to
        the cwd)."""
        for spelling in (
            f"{self.seats}//",
            f"{self.seats}/./",
            f"{self.seats}/x/..",
            f"{self.seats}///.",
            f"{self.seats}/",
        ):
            with self.subTest(spelling=spelling):
                check = self.run_lever("--check", "orchestrator", REGIME_SEATS_ROOT=spelling)
                self.assertEqual((check.returncode, check.stdout), (0, f"{self.absent_line('orchestrator')}\n"))
        self.assertFalse(self.seats.exists(), "--check makes nothing")
        gate = self.run_lever("orchestrator", DISPLAY=":0", REGIME_SEATS_ROOT=f"{self.seats}//")
        self.assertEqual(gate.returncode, 2, gate.stderr)
        self.assertEqual(gate.stderr, self.refusal(self.absent_line("orchestrator")))
        for path in (self.seats, self.seats / ".state", self.shared):
            self.assertTrue(path.is_dir() and not path.is_symlink(), path)
            self.assertEqual(stat.S_IMODE(os.lstat(path).st_mode), 0o700, path)
        self.assertEqual(sorted(path.name for path in self.seats.iterdir()), [".state"])
        self.assertEqual(self.calls_text(), f"claude-keyed --check REGIME_ANTHROPIC_KEY_FILE={self.key_file}\n" * 6)
        relative = self.run_lever("--check", "orchestrator", REGIME_SEATS_ROOT="seats")
        self.assertEqual(
            (relative.returncode, relative.stdout),
            (
                1,
                "orchestrator claude-bridge: unreadable (no seats root: REGIME_SEATS_ROOT seats is not an absolute path)\n",
            ),
        )

    def test_a_seats_root_with_a_space_a_quote_and_a_dollar_prints_steps_whose_eval_places_the_exact_file(
        self,
    ) -> None:
        """U318b (verdict U318-e0dd8cc2, P2 at :293): the printed operator command carried the directory unquoted, so a
        seats root with a space split it into wrong arguments. U512: the two steps are shell-quoted (`%q`): `eval` of
        the printed text, on the laptop and in the SSH form, with the key on stdin, writes exactly the key file (0600
        in its 0700 directory) and runs `claude-keyed --check` on exactly that path; the profile mode made the shared
        directory 0700 first."""
        seats = self.temp / "a b'$c"
        key = seats / ".state/anthropic/api-key"
        step_re = re.compile(r"; place the key once: (.*); the key is the operator's step")
        for extra in ({"DISPLAY": ":0"}, {"SSH_CONNECTION": "100.64.0.2 50000 100.64.0.3 22"}):
            with self.subTest(**extra):
                refused = self.run_lever("orchestrator", REGIME_SEATS_ROOT=str(seats), **extra)
                self.assertEqual(refused.returncode, 2, refused.stderr)
                self.assertIn(f"{self.absent_line('orchestrator', seats)}; place the key once: ", refused.stderr)
                match = step_re.search(refused.stderr)
                self.assertIsNotNone(match, refused.stderr)
                command = match.group(1)
                self.assertEqual(command.count("\n"), 0, command)
                self.assertNotIn(f"> {key};", command, "the file is quoted, not pasted raw")
                self.assertNotIn(f"REGIME_ANTHROPIC_KEY_FILE={key} ", command, "the file is quoted, not pasted raw")
                self.calls.unlink()
                pasted = subprocess.run(
                    ["bash", "-c", 'eval "$1"', "_", command], env=self.env(), input=FAKE_KEY + "\n",
                    check=False, capture_output=True, text=True,
                )  # fmt: skip
                self.assertEqual(pasted.returncode, 0, pasted.stderr)
                self.assertEqual(pasted.stdout, f"key: \nkey file ok: {key}; executable: /fake/sdk/claude\n")
                self.assertEqual(key.read_text(), FAKE_KEY + "\n")
                self.assertEqual(stat.S_IMODE(os.lstat(key).st_mode), 0o600)
                self.assertEqual(stat.S_IMODE(os.lstat(key.parent).st_mode), 0o700)
                self.assertEqual(self.calls_text(), f"claude-keyed --check REGIME_ANTHROPIC_KEY_FILE={key}\n")
                key.unlink()
        for path in (seats, seats / ".state", seats / ".state/claude"):
            self.assertTrue(path.is_dir() and not path.is_symlink(), path)
            self.assertEqual(stat.S_IMODE(os.lstat(path).st_mode), 0o700, path)
        check = self.run_lever("--check", "orchestrator", REGIME_SEATS_ROOT=str(seats))
        self.assertEqual((check.returncode, check.stdout), (0, f"{self.absent_line('orchestrator', seats)}\n"))

    def lever_functions(self, *names: str) -> str:
        """Functions of the lever, extracted by name as `test_hcom_seat`'s `identity_functions` does, so a test can
        overlay one producer and run the rest as written."""
        text = PREFLIGHT.read_text()
        return "\n".join(
            text[text.index(f"{name}() {{") : text.index("\n}\n", text.index(f"{name}() {{")) + 3] for name in names
        )

    def test_a_failed_key_step_producer_refuses_naming_it_and_prints_no_empty_step(self) -> None:
        """U318b (verdict U318-e0dd8cc2, P3 at :331): the `claude_login_command` substitution's status was unread, so an
        injected exit 9 read as an ordinary absence with an empty command. `claude_login_refuse`, the function the
        profile mode runs for the Claude route, reads it: a producer that fails, with or without a partial line,
        refuses (exit 2) naming `claude_login_command`, and no step reaches the operator (U512: the step is the
        handout's two commands on the key file)."""
        functions = self.lever_functions("die", "claude_login_command", "claude_login_refuse")
        self.assertIn("step=$(claude_login_command) || die", functions)
        line = (
            "orchestrator claude-bridge: absent (the key file /x/.state/anthropic/api-key is absent; place the API key"
            " there (the U510 handout))"
        )
        prefix = (
            f"set -euo pipefail\n{functions}\n"
            "claude_key_dir=/x/.state/anthropic claude_key_file=/x/.state/anthropic/api-key\n"
        )

        def run(overlay: str) -> subprocess.CompletedProcess[str]:
            script = f"{prefix}{overlay}\nclaude_login_refuse '{line}'\n"
            return subprocess.run(["bash", "-c", script], env=self.env(), check=False, capture_output=True, text=True)

        as_written = run("")
        self.assertEqual(as_written.returncode, 2, as_written.stderr)
        self.assertEqual(as_written.stderr, self.refusal(line, Path("/x")))
        for label, overlay in (
            ("exit 9", "claude_login_command() { return 9; }"),
            ("partial line then exit 9", "claude_login_command() { printf 'REGIME_ANTHROPIC_KEY_FILE=/x/.state/anthropic/api-key claude-keyed --check\\n'; return 9; }"),
        ):  # fmt: skip
            with self.subTest(label=label):
                failed = run(overlay)
                self.assertEqual(failed.returncode, 2, failed.stderr)
                self.assertEqual(
                    failed.stderr,
                    f"seat-login-preflight: {line}; cannot name the operator's key step: claude_login_command failed\n",
                )
                self.assertEqual(failed.stdout, "")
                self.assertNotIn("REGIME_ANTHROPIC_KEY_FILE=", failed.stdout + failed.stderr)
                self.assertNotIn("place the key once", failed.stdout + failed.stderr)

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
        # The Claude route outside a TTY, and inside a seat: the printed steps, no login run (U318, U512).
        status, output = self.run_tty("worker", SSH_CONNECTION=remote, HCOM_LAUNCHED="1")
        self.assertEqual(status, 2, output)
        self.assertIn(
            f"REGIME_ANTHROPIC_KEY_FILE={self.key_file} claude-keyed --check; the key is the operator's step", output
        )
        self.assertEqual(self.calls_text(), f"claude-keyed --check REGIME_ANTHROPIC_KEY_FILE={self.key_file}\n")

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

    def test_the_operators_terminal_names_the_key_step_for_claude_and_runs_no_login(self) -> None:
        """U318, U512: the Claude route has no login to run: the operator places the key by the handout's two steps,
        which the preflight prints, in a TTY too, running nothing (no `claude auth login`, no browser)."""
        remote = "100.64.0.2 50000 100.64.0.3 22"
        status, output = self.run_tty("orchestrator", SSH_CONNECTION=remote)
        self.assertEqual(status, 2, output)
        self.assertIn(
            f"place the key once: {self.key_step()}; the key is the operator's step (handouts/anthropic-api-key-u510.md,"
            " steps 2 and 3): run those commands in your own terminal on this host",
            output,
        )
        self.assertEqual(self.calls_text(), f"claude-keyed --check REGIME_ANTHROPIC_KEY_FILE={self.key_file}\n")
        self.assertFalse((self.home / ".claude").exists())
        self.assertNotIn("BROWSER=", output)
        self.assertNotIn("auth login", output)

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
        self.assertIn(f"{self.absent_line('worker')}; place the key once:", headless.stderr)
        for display in ({"DISPLAY": ":0"}, {"WAYLAND_DISPLAY": "wayland-0"}):
            with self.subTest(**display):
                # With a display the host is local: the SIWC route does nothing there, while the Claude route's rule
                # holds on every host (U190b): the worker refuses without the shared directory's login, and a token
                # variable in the environment is no input (U312).
                local = self.run_lever("audit", **display)
                self.assertEqual((local.returncode, local.stderr), (0, ""))
                for extra in ({}, {TOKEN_VARIABLE: FAKE_OAUTH_VALUE}):
                    refused = self.run_lever("worker", **display, **extra)
                    self.assertEqual(refused.returncode, 2, refused.stderr)
                    self.assertIn(self.absent_line("worker"), refused.stderr)
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
        (profiles / "review.yml").write_text("modelRoles:\n  default: claude-bridge/claude-fable-5-1\n")
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
        # The key judge (U512): a `claude-keyed --check` that exits neither 0 nor 2, or no claude-keyed on PATH, is
        # unreadable in `--check` and a refusal (exit 1) in the profile mode, never absent.
        self.shared.mkdir(parents=True)
        remote = "100.64.0.2 50000 100.64.0.3 22"
        key = str(self.key_file)
        result = self.run_lever("--check", "orchestrator", FAKE_CLAUDE_KEYED_STATUS="3")
        self.assertEqual(
            (result.returncode, result.stdout),
            (1, f"orchestrator claude-bridge: unreadable (claude-keyed --check exited 3 for the API key file {key})\n"),
        )
        gate = self.run_lever("orchestrator", SSH_CONNECTION=remote, FAKE_CLAUDE_KEYED_STATUS="3")
        self.assertEqual(gate.returncode, 1, gate.stderr)
        self.assertIn(f"exited 3 for the API key file {key}); fix or move the record aside", gate.stderr)
        (self.bin / "claude-keyed").unlink()
        result = self.run_lever("--check", "orchestrator", PATH=f"{self.bin}:/usr/bin:/bin")
        self.assertEqual(
            (result.returncode, result.stdout),
            (1, f"orchestrator claude-bridge: unreadable (no claude-keyed on PATH to judge the API key file {key})\n"),
        )
        # The overlay enumeration needs no external producer.
        write_exec(self.bin / "basename", "#!/bin/sh\nexit 1\n")
        result = self.run_lever("--check")
        self.assertEqual(
            [line.split(":")[0] for line in result.stdout.splitlines()],
            ["audit openai-siwc", "orchestrator claude-bridge", "worker claude-bridge"],
        )
        self.assertNotIn("auth login", self.calls_text())
        self.assertNotIn("claude auth", self.calls_text())

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

    def test_readiness_counts_the_key_file_alone(self) -> None:
        """U318, U512: a seat starts on the seats' API key file alone, judged by `claude-keyed --check` and the Models
        API. A credentials file of the operator's own `~/.claude` and a token variable in the environment are no input
        (U190, U312); a key the API rejects (401) is absent too, naming the handout's steps; in the operator's terminal
        the same state names the steps and runs no login."""
        remote = "100.64.0.2 50000 100.64.0.3 22"
        key = str(self.key_file)
        credentials = self.home / ".claude/.credentials.json"
        credentials.parent.mkdir()
        credentials.write_text("{}")
        credentials.chmod(0o600)
        variable_only = self.run_lever("orchestrator", SSH_CONNECTION=remote, **{TOKEN_VARIABLE: FAKE_OAUTH_VALUE})
        self.assertEqual(variable_only.returncode, 2, variable_only.stderr)
        self.assertEqual(variable_only.stderr, self.refusal(self.absent_line("orchestrator")))
        self.assertEqual(self.calls_text(), f"claude-keyed --check REGIME_ANTHROPIC_KEY_FILE={key}\n")
        self.place_key()
        rejected = self.run_lever("worker", SSH_CONNECTION=remote, REGIME_ANTHROPIC_MODELS_URL=self.models_api(401))
        self.assertEqual(rejected.returncode, 2, rejected.stderr)
        self.assertEqual(rejected.stderr, self.refusal(f"worker claude-bridge: key rejected ({key}; HTTP 401)"))
        present = self.run_lever(
            "orchestrator", SSH_CONNECTION=remote, REGIME_ANTHROPIC_MODELS_URL=self.models_api(200),
            **{TOKEN_VARIABLE: FAKE_OAUTH_VALUE},
        )  # fmt: skip
        self.assertEqual(present.returncode, 0, present.stderr)
        self.assertEqual(present.stderr, f"seat-login-preflight: orchestrator claude-bridge: key ok ({key})\n")
        # In the operator's terminal the same rejected state names the steps and runs no login.
        status, output = self.run_tty("worker", SSH_CONNECTION=remote, REGIME_ANTHROPIC_MODELS_URL=self.models_api(401))
        self.assertEqual(status, 2, output)
        self.assertIn(
            f"key rejected ({key}; HTTP 401); place the key once: {self.key_step()}; the key is the operator's step",
            output,
        )
        self.assertNotIn("auth login", self.calls_text())
        self.assertNotIn("claude auth", self.calls_text())
        self.assertEqual(self.calls_text().count("claude-keyed --check"), 4)
        for text in (variable_only.stderr, rejected.stderr, present.stderr, output):
            self.assertNotIn(FAKE_OAUTH_VALUE, text)
            self.assertNotIn(FAKE_KEY, text)


if __name__ == "__main__":
    unittest.main()
