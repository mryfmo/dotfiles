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
        # The seats root the login groups' Claude Code directories live in (U318, per group since U498), passed as
        # hcom-seat passes its resolved one: the orchestrator profile's group directory, the worker's, and the legacy
        # shared directory the kit neither reads nor removes.
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
        shared = self.shared
        self.assertEqual(
            lines[1:],
            [
                f"orchestrator claude-bridge: absent (no {shared})",
                f"worker claude-bridge: absent (no {self.shared_worker})",
            ],
        )

    def test_check_reports_the_shared_directorys_method_and_never_a_token(self) -> None:
        """U318: `--check` names the shared directory and the method of its login from one `claude auth status` call
        under it; a token variable in the environment is no input (U312) and never reaches the call; an absent
        directory is absent without a call; `oauth_token`, `api_key` and an exit 1 are absent; any other exit, a
        non-JSON body, a record without a method and two records are unreadable (exit 1), never absent."""
        shared = str(self.shared)
        result = self.run_lever("--check", "orchestrator", **{TOKEN_VARIABLE: FAKE_OAUTH_VALUE})
        self.assertEqual((result.returncode, result.stdout), (0, f"orchestrator claude-bridge: absent (no {shared})\n"))
        self.assertEqual(self.calls_text(), "", "no call without the directory")
        self.shared.mkdir(parents=True)
        result = self.run_lever("--check", "orchestrator", **{TOKEN_VARIABLE: FAKE_OAUTH_VALUE})
        self.assertEqual(
            (result.returncode, result.stdout),
            (0, f"orchestrator claude-bridge: login present (claude.ai, {shared})\n"),
        )
        self.assertEqual(
            self.calls_text(), f"claude auth status CLAUDE_CONFIG_DIR={shared} BROWSER=unset token=unset\n"
        )
        unreadable = f"unreadable (claude auth status printed no auth status record under {shared})"
        for extra, expected, status in (
            ({"FAKE_CLAUDE_AUTH_METHOD": "oauth_token"}, f"absent (authMethod oauth_token under {shared}, not claude.ai)", 0),
            ({"FAKE_CLAUDE_AUTH_METHOD": "api_key"}, f"absent (authMethod api_key under {shared}, not claude.ai)", 0),
            ({"FAKE_CLAUDE_AUTH_STATUS": "1"}, f"absent (not logged in under {shared})", 0),
            ({"FAKE_CLAUDE_AUTH_STATUS": "5"}, f"unreadable (claude auth status exited 5 under {shared})", 1),
            ({"FAKE_CLAUDE_AUTH_BODY": "not json"}, unreadable, 1),
            ({"FAKE_CLAUDE_AUTH_BODY": '{"loggedIn": true}'}, unreadable, 1),
            ({"FAKE_CLAUDE_AUTH_BODY": '{"authMethod": "claude.ai"} {"authMethod": "claude.ai"}'}, unreadable, 1),
        ):  # fmt: skip
            with self.subTest(**extra):
                result = self.run_lever("--check", "orchestrator", **extra)
                self.assertEqual(
                    (result.returncode, result.stdout),
                    (status, f"orchestrator claude-bridge: {expected}\n"),
                    result.stderr,
                )
        self.assertNotIn(FAKE_OAUTH_VALUE, self.calls_text() + result.stdout + result.stderr)

    def test_the_seats_root_derives_from_the_checkout_when_none_is_passed(self) -> None:
        """U318, U498: without REGIME_SEATS_ROOT the group directory is `~/.local/state/omp-seats/<slug>/.state/claude-<group>`
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
            rf"^orchestrator claude-bridge: absent \(no {re.escape(str(home))}/\.local/state/omp-seats/[a-z0-9][a-z0-9_-]{{0,39}}/\.state/claude-orchestrator\)\n$",
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

    def test_check_names_each_login_groups_directory(self) -> None:
        """U498: `--check` derives the directory per login group from the one table (`login_group_of_role`): the
        orchestrator and worker profiles name `.state/claude-orchestrator` and `.state/claude-worker`, a deployed dsh
        overlay on the claude-bridge route names the router group's `.state/claude-router` (the gateway child is the
        Router's), and a profile outside the table is unreadable (exit 1), never absent, with no call. Each line reads
        its own group's directory: a worker login present leaves the orchestrator's absent."""
        profiles = self.home / ".agents/omp/profiles"
        for profile in ("dsh", "other"):
            (profiles / f"{profile}.yml").write_text("modelRoles:\n  default: claude-bridge/claude-haiku-5-5\n")
        result = self.run_lever("--check")
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertEqual(
            result.stdout.splitlines(),
            [
                f"audit openai-siwc: absent (no {self.home}/.omp/profiles/audit/agent/openai-siwc/registration.json)",
                f"dsh claude-bridge: absent (no {self.seats}/.state/claude-router)",
                f"orchestrator claude-bridge: absent (no {self.shared})",
                "other claude-bridge: unreadable (no login group for the profile other; the table names orchestrator,"
                " worker, audit, dsh and router)",
                f"worker claude-bridge: absent (no {self.shared_worker})",
            ],
        )
        self.assertEqual(self.calls_text(), "", "no call without a directory")
        self.shared_worker.mkdir(parents=True)
        self.legacy.mkdir()
        result = self.run_lever("--check", "orchestrator", "worker", "dsh")
        self.assertEqual(
            (result.returncode, result.stdout),
            (
                0,
                f"orchestrator claude-bridge: absent (no {self.shared})\n"
                f"worker claude-bridge: login present (claude.ai, {self.shared_worker})\n"
                f"dsh claude-bridge: absent (no {self.seats}/.state/claude-router)\n",
            ),
            result.stderr,
        )
        self.assertEqual(
            self.calls_text(), f"claude auth status CLAUDE_CONFIG_DIR={self.shared_worker} BROWSER=unset token=unset\n"
        )
        self.assertNotIn(f"{self.legacy})", result.stdout, "the legacy shared directory is read by no line")

    def test_the_refusal_names_the_legacy_shared_directory_when_the_groups_is_absent(self) -> None:
        """U498 (standing order 54): the kit neither reads, copies nor deletes U318's shared `.state/claude`. When it
        exists and the group's directory did not before this run, the profile mode's refusal prints the group's
        command and names the legacy directory as the one the operator may remove after logging in per group; the
        directory and its contents are untouched. With the group's directory present, or no legacy one, the refusal
        says nothing of it, and `--check` never mentions it."""
        self.legacy.mkdir(parents=True)
        (self.legacy / "marker").write_text("")
        refused = self.run_lever("worker", DISPLAY=":0", FAKE_CLAUDE_AUTH_STATUS="1")
        self.assertEqual(refused.returncode, 2, refused.stderr)
        self.assertEqual(
            refused.stderr,
            f"seat-login-preflight: worker claude-bridge: absent (not logged in under {self.shared_worker}); log in"
            f" once: CLAUDE_CONFIG_DIR={self.shared_worker} claude auth login; a login is the operator's step: run that"
            " command in your own terminal on this host, then start the seat again; the legacy shared directory"
            f" {self.legacy} (one login per seats root, U318) is read by no seat: remove it once every running group"
            " is logged in\n",
        )
        self.assertEqual(sorted(path.name for path in self.legacy.iterdir()), ["marker"])
        self.assertTrue(self.shared_worker.is_dir() and not self.shared_worker.is_symlink())
        self.assertEqual(stat.S_IMODE(os.lstat(self.shared_worker).st_mode), 0o700)
        # The group's directory exists now (this run made it), so the next refusal names no legacy directory.
        again = self.run_lever("worker", DISPLAY=":0", FAKE_CLAUDE_AUTH_STATUS="1")
        self.assertEqual(again.returncode, 2, again.stderr)
        self.assertNotIn("legacy", again.stderr)
        self.assertTrue(again.stderr.endswith("then start the seat again\n"), again.stderr)
        check = self.run_lever("--check", "worker", FAKE_CLAUDE_AUTH_STATUS="1")
        self.assertEqual(
            (check.returncode, check.stdout),
            (0, f"worker claude-bridge: absent (not logged in under {self.shared_worker})\n"),
        )
        self.assertNotIn("legacy", check.stdout + check.stderr)
        self.assertEqual(
            self.calls_text(),
            f"claude auth status CLAUDE_CONFIG_DIR={self.shared_worker} BROWSER=unset token=unset\n" * 3,
        )

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
        """U190b, U318: the seat's child logs in by the shared directory's login wherever it runs, so a local host (no
        SSH session; a display on Linux) without that login refuses with the printed command (no BROWSER prefix
        there), making the directory 0700 with its parents first; one with a claude.ai login there passes; the
        operator's own `~/.claude` is never an input. Round 1 exited 0 there before any check, and a host-only login
        started a seat whose first bridge turn would end `Not logged in`."""
        credentials = self.home / ".claude/.credentials.json"
        credentials.parent.mkdir()
        credentials.write_text("{}")
        credentials.chmod(0o600)
        shared = str(self.shared)
        not_logged_in = self.run_lever("orchestrator", DISPLAY=":0", FAKE_CLAUDE_AUTH_STATUS="1")
        self.assertEqual(not_logged_in.returncode, 2, not_logged_in.stderr)
        self.assertEqual(
            not_logged_in.stderr,
            f"seat-login-preflight: orchestrator claude-bridge: absent (not logged in under {shared}); log in once:"
            f" CLAUDE_CONFIG_DIR={shared} claude auth login; a login is the operator's step: run that command in your"
            " own terminal on this host, then start the seat again\n",
        )
        for path in (self.seats, self.seats / ".state", self.shared):
            self.assertTrue(path.is_dir() and not path.is_symlink(), path)
            self.assertEqual(stat.S_IMODE(os.lstat(path).st_mode), 0o700, path)
        ready = self.run_lever("orchestrator", DISPLAY=":0")
        self.assertEqual(ready.returncode, 0, ready.stderr)
        self.assertEqual(
            ready.stderr, f"seat-login-preflight: orchestrator claude-bridge: login present (claude.ai, {shared})\n"
        )
        self.assertEqual(
            self.calls_text(), f"claude auth status CLAUDE_CONFIG_DIR={shared} BROWSER=unset token=unset\n" * 2
        )
        self.assertEqual(self.bun_calls_text(), "")
        self.assertEqual(credentials.read_text(), "{}", "the operator's store is untouched")

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
        root: `--check` prints the one spelling (round 2 printed `<root>//.state/claude` for the first, U318), the profile
        mode makes the chain 0700 at the root and prints the command with the one spelling, and the one status call
        runs under it. A relative root is no seats root (unreadable, never a directory relative to the cwd)."""
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
                    (check.returncode, check.stdout), (0, f"orchestrator claude-bridge: absent (no {self.shared})\n")
                )
        self.assertFalse(self.seats.exists(), "--check makes nothing")
        gate = self.run_lever(
            "orchestrator", DISPLAY=":0", FAKE_CLAUDE_AUTH_STATUS="1", REGIME_SEATS_ROOT=f"{self.seats}//"
        )
        self.assertEqual(gate.returncode, 2, gate.stderr)
        self.assertIn(
            f"orchestrator claude-bridge: absent (not logged in under {self.shared}); log in once:"
            f" CLAUDE_CONFIG_DIR={self.shared} claude auth login;",
            gate.stderr,
        )
        for path in (self.seats, self.seats / ".state", self.shared):
            self.assertTrue(path.is_dir() and not path.is_symlink(), path)
            self.assertEqual(stat.S_IMODE(os.lstat(path).st_mode), 0o700, path)
        self.assertEqual(sorted(path.name for path in self.seats.iterdir()), [".state"])
        self.assertEqual(
            self.calls_text(), f"claude auth status CLAUDE_CONFIG_DIR={self.shared} BROWSER=unset token=unset\n"
        )
        relative = self.run_lever("--check", "orchestrator", REGIME_SEATS_ROOT="seats")
        self.assertEqual(
            (relative.returncode, relative.stdout),
            (
                1,
                "orchestrator claude-bridge: unreadable (no seats root: REGIME_SEATS_ROOT seats is not an absolute path)\n",
            ),
        )

    def test_a_seats_root_with_a_space_a_quote_and_a_dollar_prints_a_command_whose_eval_sets_the_exact_directory(
        self,
    ) -> None:
        """U318b (verdict U318-e0dd8cc2, P2 at :293): the printed operator command carried the directory unquoted, so a
        seats root with a space split it into wrong arguments. The assignment is shell-quoted: `eval` of the printed
        line, on the laptop and in the SSH form, runs `claude auth login` with `CLAUDE_CONFIG_DIR` set to the exact
        directory, which the profile mode made 0700 first."""
        seats = self.temp / "a b'$c"
        shared = seats / ".state/claude-orchestrator"
        command_re = re.compile(r"; log in once: (.*); a login is the operator's step")
        for extra, browser in (({"DISPLAY": ":0"}, "unset"), ({"SSH_CONNECTION": "100.64.0.2 50000 100.64.0.3 22"}, "regime-open-url")):  # fmt: skip
            with self.subTest(**extra):
                refused = self.run_lever(
                    "orchestrator", FAKE_CLAUDE_AUTH_STATUS="1", REGIME_SEATS_ROOT=str(seats), **extra
                )
                self.assertEqual(refused.returncode, 2, refused.stderr)
                self.assertIn(
                    f"orchestrator claude-bridge: absent (not logged in under {shared}); log in once: ", refused.stderr
                )
                match = command_re.search(refused.stderr)
                self.assertIsNotNone(match, refused.stderr)
                command = match.group(1)
                self.assertEqual(command.count("\n"), 0, command)
                self.assertNotIn(f"CLAUDE_CONFIG_DIR={shared} ", command, "the directory is quoted, not pasted raw")
                self.calls.unlink()
                pasted = subprocess.run(
                    ["bash", "-c", 'eval "$1"', "_", command], env=self.env(), check=False, capture_output=True, text=True
                )  # fmt: skip
                self.assertEqual(pasted.returncode, 64, "the fake claude saw `auth login`")
                self.assertEqual(
                    self.calls_text(), f"claude auth login CLAUDE_CONFIG_DIR={shared} BROWSER={browser} token=unset\n"
                )
        for path in (seats, seats / ".state", shared):
            self.assertTrue(path.is_dir() and not path.is_symlink(), path)
            self.assertEqual(stat.S_IMODE(os.lstat(path).st_mode), 0o700, path)
        check = self.run_lever("--check", "orchestrator", FAKE_CLAUDE_AUTH_STATUS="1", REGIME_SEATS_ROOT=str(seats))
        self.assertEqual(
            (check.returncode, check.stdout),
            (0, f"orchestrator claude-bridge: absent (not logged in under {shared})\n"),
        )

    def lever_functions(self, *names: str) -> str:
        """Functions of the lever, extracted by name as `test_hcom_seat`'s `identity_functions` does, so a test can
        overlay one producer and run the rest as written."""
        text = PREFLIGHT.read_text()
        return "\n".join(
            text[text.index(f"{name}() {{") : text.index("\n}\n", text.index(f"{name}() {{")) + 3] for name in names
        )

    def test_a_failed_login_command_producer_refuses_naming_it_and_prints_no_empty_command(self) -> None:
        """U318b (verdict U318-e0dd8cc2, P3 at :331): the `claude_login_command` substitution's status was unread, so an
        injected exit 9 read as an ordinary absence with an empty command. `claude_login_refuse`, the function the
        profile mode runs for the Claude route, reads it: a producer that fails, with or without a partial line,
        refuses (exit 2) naming `claude_login_command`, and no `CLAUDE_CONFIG_DIR=` reaches the operator."""
        functions = self.lever_functions("die", "claude_login_command", "claude_login_refuse")
        self.assertIn("step=$(claude_login_command) || die", functions)
        line = "orchestrator claude-bridge: absent (not logged in under /x/.state/claude)"
        prefix = f"set -euo pipefail\n{functions}\nclaude_config=/x/.state/claude\n"

        def run(overlay: str) -> subprocess.CompletedProcess[str]:
            script = f"{prefix}{overlay}\nclaude_login_refuse '{line}'\n"
            return subprocess.run(["bash", "-c", script], env=self.env(), check=False, capture_output=True, text=True)

        as_written = run("")
        self.assertEqual(as_written.returncode, 2, as_written.stderr)
        self.assertEqual(
            as_written.stderr,
            f"seat-login-preflight: {line}; log in once: CLAUDE_CONFIG_DIR=/x/.state/claude claude auth login; a login"
            " is the operator's step: run that command in your own terminal on this host, then start the seat again\n",
        )
        for label, overlay in (
            ("exit 9", "claude_login_command() { return 9; }"),
            ("partial line then exit 9", "claude_login_command() { printf 'CLAUDE_CONFIG_DIR=/x/.state/claude claude auth login\\n'; return 9; }"),
        ):  # fmt: skip
            with self.subTest(label=label):
                failed = run(overlay)
                self.assertEqual(failed.returncode, 2, failed.stderr)
                self.assertEqual(
                    failed.stderr,
                    f"seat-login-preflight: {line}; cannot name the operator's login step: claude_login_command failed\n",
                )
                self.assertEqual(failed.stdout, "")
                self.assertNotIn("CLAUDE_CONFIG_DIR=", failed.stdout + failed.stderr)
                self.assertNotIn("log in once", failed.stdout + failed.stderr)

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
        # The Claude route outside a TTY, and inside a seat: the printed command, no login run (U318).
        status, output = self.run_tty("worker", SSH_CONNECTION=remote, HCOM_LAUNCHED="1", FAKE_CLAUDE_AUTH_STATUS="1")
        self.assertEqual(status, 2, output)
        self.assertIn(f"BROWSER=regime-open-url CLAUDE_CONFIG_DIR={self.shared_worker} claude auth login", output)
        self.assertEqual(
            self.calls_text(), f"claude auth status CLAUDE_CONFIG_DIR={self.shared_worker} BROWSER=unset token=unset\n"
        )

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

    def test_the_operators_terminal_names_the_login_command_for_claude_and_runs_no_login(self) -> None:
        """U318: the Claude login is the operator's own `claude auth login` under the shared directory, with
        `BROWSER=regime-open-url` in an SSH session (the laptop's browser, the code-paste flow); the preflight prints
        it and runs no login, in a TTY too."""
        remote = "100.64.0.2 50000 100.64.0.3 22"
        status, output = self.run_tty("orchestrator", SSH_CONNECTION=remote, FAKE_CLAUDE_AUTH_STATUS="1")
        self.assertEqual(status, 2, output)
        self.assertIn(
            f"log in once: BROWSER=regime-open-url CLAUDE_CONFIG_DIR={self.shared} claude auth login; a login is the"
            " operator's step: run that command in your own terminal on this host",
            output,
        )
        self.assertEqual(
            self.calls_text(), f"claude auth status CLAUDE_CONFIG_DIR={self.shared} BROWSER=unset token=unset\n"
        )
        self.assertFalse((self.home / ".claude").exists())

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
        headless = self.run_lever("worker", FAKE_CLAUDE_AUTH_STATUS="1")
        self.assertEqual(headless.returncode, 2, headless.stderr)
        self.assertIn(
            f"worker claude-bridge: absent (not logged in under {self.shared_worker}); log in once:", headless.stderr
        )
        for display in ({"DISPLAY": ":0"}, {"WAYLAND_DISPLAY": "wayland-0"}):
            with self.subTest(**display):
                # With a display the host is local: the SIWC route does nothing there, while the Claude route's rule
                # holds on every host (U190b): the worker refuses without the shared directory's login, and a token
                # variable in the environment is no input (U312).
                local = self.run_lever("audit", **display)
                self.assertEqual((local.returncode, local.stderr), (0, ""))
                for extra in ({}, {TOKEN_VARIABLE: FAKE_OAUTH_VALUE}):
                    refused = self.run_lever("worker", **display, **extra, FAKE_CLAUDE_AUTH_STATUS="1")
                    self.assertEqual(refused.returncode, 2, refused.stderr)
                    self.assertIn(
                        f"worker claude-bridge: absent (not logged in under {self.shared_worker})", refused.stderr
                    )
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
        # The login reader (U318): a `claude auth status` that fails, or a jq that cannot read its record, is unreadable
        # in `--check` and a refusal (exit 1) in the profile mode, never absent.
        self.shared.mkdir(parents=True)
        remote = "100.64.0.2 50000 100.64.0.3 22"
        result = self.run_lever("--check", "orchestrator", FAKE_CLAUDE_AUTH_STATUS="3")
        self.assertEqual(
            (result.returncode, result.stdout),
            (1, f"orchestrator claude-bridge: unreadable (claude auth status exited 3 under {self.shared})\n"),
        )
        gate = self.run_lever("orchestrator", SSH_CONNECTION=remote, FAKE_CLAUDE_AUTH_STATUS="3")
        self.assertEqual(gate.returncode, 1, gate.stderr)
        self.assertIn(f"exited 3 under {self.shared}); fix or move the record aside", gate.stderr)
        write_exec(self.bin / "jq", "#!/bin/sh\nexit 5\n")
        result = self.run_lever("--check", "orchestrator")
        self.assertEqual(
            (result.returncode, result.stdout),
            (
                1,
                f"orchestrator claude-bridge: unreadable (claude auth status printed no auth status record under {self.shared})\n",
            ),
        )
        (self.bin / "jq").unlink()
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

    def test_readiness_counts_the_shared_directorys_claude_ai_login_alone(self) -> None:
        """U318, U498: a seat starts on its login group's claude.ai login alone. A credentials file of the operator's
        own `~/.claude` and a token variable in the environment are no input (U190, U312); an `oauth_token` or
        `api_key` method under the directory is absent too, naming the command for that group; in the operator's
        terminal the same state names the command and runs no login."""
        remote = "100.64.0.2 50000 100.64.0.3 22"
        shared = str(self.shared)
        command = f"BROWSER=regime-open-url CLAUDE_CONFIG_DIR={shared} claude auth login"
        worker_command = f"BROWSER=regime-open-url CLAUDE_CONFIG_DIR={self.shared_worker} claude auth login"
        credentials = self.home / ".claude/.credentials.json"
        credentials.parent.mkdir()
        credentials.write_text("{}")
        credentials.chmod(0o600)
        variable_only = self.run_lever(
            "orchestrator", SSH_CONNECTION=remote, FAKE_CLAUDE_AUTH_STATUS="1", **{TOKEN_VARIABLE: FAKE_OAUTH_VALUE}
        )
        self.assertEqual(variable_only.returncode, 2, variable_only.stderr)
        self.assertIn(
            f"orchestrator claude-bridge: absent (not logged in under {shared}); log in once: {command}; a login is the"
            " operator's step",
            variable_only.stderr,
        )
        self.assertEqual(
            self.calls_text(), f"claude auth status CLAUDE_CONFIG_DIR={shared} BROWSER=unset token=unset\n"
        )
        for method in ("oauth_token", "api_key"):
            with self.subTest(method=method):
                other = self.run_lever("worker", SSH_CONNECTION=remote, FAKE_CLAUDE_AUTH_METHOD=method)
                self.assertEqual(other.returncode, 2, other.stderr)
                self.assertIn(
                    f"worker claude-bridge: absent (authMethod {method} under {self.shared_worker}, not claude.ai); log in"
                    f" once: {worker_command}",
                    other.stderr,
                )
        present = self.run_lever("orchestrator", SSH_CONNECTION=remote, **{TOKEN_VARIABLE: FAKE_OAUTH_VALUE})
        self.assertEqual(present.returncode, 0, present.stderr)
        self.assertEqual(
            present.stderr, f"seat-login-preflight: orchestrator claude-bridge: login present (claude.ai, {shared})\n"
        )
        # In the operator's terminal the same absent state names the command and runs no login.
        status, output = self.run_tty("worker", SSH_CONNECTION=remote, FAKE_CLAUDE_AUTH_STATUS="1")
        self.assertEqual(status, 2, output)
        self.assertIn(f"log in once: {worker_command}; a login is the operator's step", output)
        self.assertNotIn("auth login", self.calls_text())
        self.assertEqual(self.calls_text().count("claude auth status"), 5)
        for text in (variable_only.stderr, other.stderr, present.stderr, output):
            self.assertNotIn(FAKE_OAUTH_VALUE, text)


if __name__ == "__main__":
    unittest.main()
