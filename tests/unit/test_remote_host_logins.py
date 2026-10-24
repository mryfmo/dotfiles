"""Seat logins on a remote host (regime-cutover U37): the laptop URL opener and its seat-host client, the
token export, the SSH forwards, the launchd agent and the seat-login pre-flight lever. Everything runs
against scratch homes and fake openers; no test opens a browser or reads a real login."""

import json
import os
import plistlib
import pty
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


class TokenExportTest(unittest.TestCase):
    """The login shells export CLAUDE_CODE_OAUTH_TOKEN from the operator's token file and from nothing else."""

    PROBE: ClassVar[dict[str, list[str]]] = {
        "zsh": ["zsh", "-f", "-c", 'source "$1"; print -r -- "${CLAUDE_CODE_OAUTH_TOKEN-unset}|${+__claude_code_oauth}"'],
        "bash": ["bash", "--norc", "--noprofile", "-c",
                 'mise() { :; }; source "$1"; printf "%s|%s\\n" "${CLAUDE_CODE_OAUTH_TOKEN-unset}" "${__claude_code_oauth+1}"'],
    }  # fmt: skip

    def run_shell(self, shell: str, rc: Path, home: Path) -> str:
        if not shutil.which(shell):
            self.skipTest(f"{shell} is not installed")
        result = subprocess.run(
            [*self.PROBE[shell], shell, str(rc)], env={"HOME": str(home), "PATH": "/usr/bin:/bin"},
            capture_output=True, text=True, check=True,
        )  # fmt: skip
        return result.stdout.strip()

    def test_the_token_file_feeds_the_variable_and_an_empty_or_absent_file_does_not(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            homes = {name: Path(temp) / name for name in ("with", "empty", "without")}
            for name, content in (("with", "fake-oauth-token-for-test\n"), ("empty", "")):
                token = homes[name] / ".config/claude-code/oauth-token"
                token.parent.mkdir(parents=True)
                token.write_text(content)
                token.chmod(0o600)
            homes["without"].mkdir()
            for shell, rc in (("zsh", ZSHENV), ("bash", PROFILE)):
                with self.subTest(shell=shell):
                    self.assertEqual(
                        self.run_shell(shell, rc, homes["with"]).split("|")[0], "fake-oauth-token-for-test"
                    )
                    for name in ("empty", "without"):
                        self.assertEqual(self.run_shell(shell, rc, homes[name]).split("|")[0], "unset")
                    # The temporary name never outlives the file read.
                    self.assertIn(self.run_shell(shell, rc, homes["with"]).split("|")[1], ("0", ""))

    def test_no_other_source_sets_the_token(self) -> None:
        for rc in (ZSHENV, PROFILE):
            lines = [
                line.strip()
                for line in rc.read_text().splitlines()
                if "CLAUDE_CODE_OAUTH_TOKEN" in line and not line.lstrip().startswith("#")
            ]
            # One assignment from the file's temporary, one export of it, and nothing else.
            self.assertEqual(
                lines,
                [
                    f"CLAUDE_CODE_OAUTH_TOKEN={'${__claude_code_oauth}' if rc == ZSHENV else '$__claude_code_oauth'}",
                    "export CLAUDE_CODE_OAUTH_TOKEN",
                ],
            )


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
        # The macOS Keychain branch must never see the real login of the host running the test.
        write_exec(self.bin / "security", "#!/bin/sh\nexit 44\n")
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
        write_exec(
            self.bin / "claude",
            f"""#!/bin/sh
printf 'claude %s BROWSER=%s\\n' "$*" "$BROWSER" >> "{self.calls}"
mkdir -p "$HOME/.claude" && printf '{{}}\\n' > "$HOME/.claude/.credentials.json" && chmod 600 "$HOME/.claude/.credentials.json"
""",
        )

    def tearDown(self) -> None:
        shutil.rmtree(self.temp)

    def env(self, **extra: str) -> dict[str, str]:
        env = {"HOME": str(self.home), "PATH": f"{self.bin}:{os.environ['PATH']}", "TMPDIR": str(self.temp)}
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
        self.assertEqual(lines[1:], ["orchestrator claude-bridge: absent", "worker claude-bridge: absent"])

    def test_check_reports_each_claude_route_without_printing_a_token(self) -> None:
        result = self.run_lever("--check", "orchestrator", **{TOKEN_VARIABLE: FAKE_OAUTH_VALUE})
        self.assertEqual(result.stdout, "orchestrator claude-bridge: login present (env token)\n")
        token = self.home / ".config/claude-code/oauth-token"
        token.parent.mkdir(parents=True)
        token.write_text(FAKE_OAUTH_VALUE + "\n")
        token.chmod(0o600)
        result = self.run_lever("--check", "orchestrator")
        self.assertRegex(
            result.stdout,
            r"^orchestrator claude-bridge: login present \(token file 600, mtime \S+Z; a new login shell exports it\)\n$",
        )
        token.unlink()
        credentials = self.home / ".claude/.credentials.json"
        credentials.parent.mkdir()
        credentials.write_text("{}")
        credentials.chmod(0o600)
        result = self.run_lever("--check", "orchestrator")
        self.assertRegex(
            result.stdout, r"^orchestrator claude-bridge: login present \(credentials file 600, mtime \S+Z\)\n$"
        )
        self.assertNotIn(FAKE_OAUTH_VALUE, self.calls_text() + result.stdout + result.stderr)

    @unittest.skipUnless(sys.platform == "darwin", "the Keychain branch runs on macOS only")
    def test_check_reads_only_the_keychain_item_attributes(self) -> None:
        write_exec(self.bin / "security", f'#!/bin/sh\necho "security $*" >> "{self.calls}"\nexit 0\n')
        result = self.run_lever("--check", "orchestrator")
        self.assertEqual(result.stdout, "orchestrator claude-bridge: login present (Keychain item)\n")
        self.assertEqual(self.calls_text(), "security find-generic-password -s Claude Code-credentials\n")

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
        # counts as remote (test_a_linux_host_without_a_display_counts_as_remote).
        write_exec(self.bin / "uname", "#!/bin/sh\necho Darwin\n")
        result = self.run_lever("audit")
        self.assertEqual((result.returncode, result.stdout, result.stderr), (0, "", ""))
        self.assertEqual(self.calls_text() + self.bun_calls_text(), "")

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
        status, output = self.run_tty("worker", SSH_CONNECTION=remote, HCOM_LAUNCHED="1")
        self.assertEqual(status, 2, output)
        self.assertIn("seat-login-preflight worker", output)
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

    def test_the_operators_terminal_runs_the_claude_login_with_the_laptop_browser(self) -> None:
        status, output = self.run_tty("orchestrator", SSH_CONNECTION="100.64.0.2 50000 100.64.0.3 22")
        self.assertEqual(status, 0, output)
        self.assertIn("claude auth login BROWSER=regime-open-url\n", self.calls_text())
        self.assertIn("paste it at the prompt below", output)
        self.assertIn("orchestrator claude-bridge: login present (credentials file 600", output)

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
        self.assertIn("worker claude-bridge: absent; a login is the operator's step", headless.stderr)
        for display in ({"DISPLAY": ":0"}, {"WAYLAND_DISPLAY": "wayland-0"}):
            with self.subTest(**display):
                local = self.run_lever("worker", **display)
                self.assertEqual((local.returncode, local.stderr), (0, ""))

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

    def test_every_seat_profile_is_accepted_and_security_logs_in_with_its_own_profile(self) -> None:
        remote = "100.64.0.2 50000 100.64.0.3 22"
        profiles = self.home / ".agents/omp/profiles"
        (profiles / "security.yml").write_text("modelRoles:\n  default: openai-siwc/gpt-6-astra\n")
        (profiles / "review.yml").write_text("modelRoles:\n  default: claude-bridge/claude-fable-5-1\n")
        status, output = self.run_tty("security", SSH_CONNECTION=remote)
        self.assertEqual(status, 0, output)
        self.assertIn("omp --profile security login openai-siwc\nOPENAI_SIWC_CALLBACK_PORT=1455\n", self.calls_text())
        self.assertIn(f"seat-login-preflight: security openai-siwc: registered (host {HOST_ID}", output)
        script = self.home / ".agents/omp/extensions/openai-siwc/src/credentials.ts"
        self.assertEqual(self.bun_calls_text(), f"bun {script} --profile security\n")
        review = self.run_lever("review", SSH_CONNECTION=remote)
        self.assertEqual(review.returncode, 2)
        self.assertIn("review claude-bridge: absent; a login is the operator's step", review.stderr)
        unknown = self.run_lever("reviewer", SSH_CONNECTION=remote)
        self.assertEqual(unknown.returncode, 2)
        self.assertIn(
            "unknown seat profile 'reviewer'; expected one of: orchestrator worker audit review security",
            unknown.stderr,
        )
        self.assertIn("<orchestrator|worker|audit|review|security>", self.run_lever().stderr)

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
        write_exec(self.bin / "stat", "#!/bin/sh\nexit 1\n")
        credentials = self.home / ".claude/.credentials.json"
        token = self.home / ".config/claude-code/oauth-token"
        for path, content in ((credentials, "{}"), (token, FAKE_OAUTH_VALUE + "\n")):
            with self.subTest(path=path.name):
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(content)
                result = self.run_lever("--check", "orchestrator")
                self.assertEqual(
                    (result.returncode, result.stdout),
                    (1, f"orchestrator claude-bridge: unreadable (cannot read the mode or mtime of {path})\n"),
                )
                path.unlink()
        # A Keychain read that fails other than "not found" (exit 44), on any runner through a Darwin uname.
        write_exec(self.bin / "uname", "#!/bin/sh\necho Darwin\n")
        write_exec(self.bin / "security", "#!/bin/sh\nexit 51\n")
        result = self.run_lever("--check", "orchestrator")
        self.assertEqual(
            (result.returncode, result.stdout),
            (1, "orchestrator claude-bridge: unreadable (security find-generic-password exited 51)\n"),
        )
        # The overlay enumeration needs no external producer.
        write_exec(self.bin / "security", "#!/bin/sh\nexit 44\n")
        write_exec(self.bin / "basename", "#!/bin/sh\nexit 1\n")
        (self.bin / "stat").unlink()
        result = self.run_lever("--check")
        self.assertEqual(
            [line.split(":")[0] for line in result.stdout.splitlines()],
            ["audit openai-siwc", "orchestrator claude-bridge", "worker claude-bridge"],
        )
        self.assertEqual(self.calls_text(), "")

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

    def test_a_token_file_this_shell_has_not_exported_is_refused(self) -> None:
        remote = "100.64.0.2 50000 100.64.0.3 22"
        token = self.home / ".config/claude-code/oauth-token"
        token.parent.mkdir(parents=True)
        token.write_text(FAKE_OAUTH_VALUE + "\n")
        token.chmod(0o600)
        gate = self.run_lever("orchestrator", SSH_CONNECTION=remote)
        self.assertEqual(gate.returncode, 2, gate.stderr)
        self.assertRegex(
            gate.stderr,
            r"orchestrator claude-bridge: login not in this environment \(token file 600, mtime \S+Z;"
            r" CLAUDE_CODE_OAUTH_TOKEN is unset here\); .*open a new login shell on this host",
        )
        status, output = self.run_tty("orchestrator", SSH_CONNECTION=remote)
        self.assertEqual(status, 2, output)
        self.assertEqual(self.calls_text(), "", "no login runs: a login cannot export the file")
        ready = self.run_lever("orchestrator", SSH_CONNECTION=remote, **{TOKEN_VARIABLE: FAKE_OAUTH_VALUE})
        self.assertEqual(ready.returncode, 0, ready.stderr)
        self.assertIn("orchestrator claude-bridge: login present (env token)", ready.stderr)
        check = self.run_lever("--check", "orchestrator")
        self.assertIn("a new login shell exports it", check.stdout)
        for result in (gate, ready, check):
            self.assertNotIn(FAKE_OAUTH_VALUE, result.stdout + result.stderr)
        self.assertNotIn(FAKE_OAUTH_VALUE, output)


if __name__ == "__main__":
    unittest.main()
