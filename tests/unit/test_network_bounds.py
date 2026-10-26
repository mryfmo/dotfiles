"""Every CI Bats run names a stalled test, and every scripted download ends (regime-cutover U99).

The download convention, for setup.sh, install/**, scripts/** (make update, the levers, the CI helpers) and the
workflow steps: curl gets `--connect-timeout 30 --speed-limit 1024 --speed-time 60` (30 s to connect, and a transfer
under 1 KB/s for 60 s fails); wget gets `--timeout=60 --tries=3`; `snap install` runs under `timeout`. apt-get needs
nothing: its http and https methods give up a connection or a read that stays silent for Acquire::http::Timeout, 30 s
unless configured (apt methods/basehttp.cc), and https inherits the http value.

The check is a closed-world text rule, not a parser (treadmill-u99-scanner): every line of a scanned file that holds
the word curl or wget, in any context (strings and comments included), carries that tool's canonical options, with
their exact values, once per occurrence of the word, and no other value of a time or retry option. Every other such
line is listed in EXEMPT by its file and exact text, with its reason; an entry whose line is gone fails. A line whose
options sit on a continuation line is either rewritten or exempted with the exact options that line must carry.
"""

from __future__ import annotations

import os
import re
import shutil
import signal
import subprocess
import sys
import tempfile
import textwrap
import time
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))  # dotted runs too; discover -s tests/unit already has it
from agent_home_isolation import isolate_agent_homes, restore_agent_homes


def setUpModule() -> None:
    isolate_agent_homes()


def tearDownModule() -> None:
    restore_agent_homes()


ROOT = Path(__file__).resolve().parents[2]
RUNNER = ROOT / "scripts/run_unit_test.sh"
WRAPPER = ROOT / "scripts/ci/run-bats.py"
WORKFLOWS = ROOT / ".github/workflows"
BASH = shutil.which("bash") or "/bin/bash"
# Every file that runs a network command on a host or a runner: the bootstrap, the installers, everything under
# scripts/ (update-agent-assets.sh and upgrade-tools.sh behind make update, the release helper, the orchestrator
# levers, the CI helpers) and the workflows. Compiled Python caches are not sources.
NETWORK_SOURCES = [
    ROOT / "setup.sh",
    *sorted((ROOT / "install").rglob("*.sh")),
    *sorted(p for p in (ROOT / "scripts").rglob("*") if p.is_file() and "__pycache__" not in p.parts),
    *sorted(WORKFLOWS.glob("*.y*ml")),
]
# One spelling per tool, values included.
CANONICAL = {"curl": "--connect-timeout 30 --speed-limit 1024 --speed-time 60", "wget": "--timeout=60 --tries=3"}
SNAP_CANONICAL = 'timeout --kill-after=30 "${limit}" snap install'
TOOL = re.compile(r"\b(curl|wget)\b")
SNAP = re.compile(r"\bsnap\s+(?:install|refresh)\b")
# Any other time or retry option, long or short, with or without a value: a second, zero or larger value next to the
# canonical options would override them.
OTHER_BOUND = re.compile(
    r"(?<!\S)(?:--(?:connect-timeout|max-time|speed-limit|speed-time|timeout|tries|read-timeout|dns-timeout|"
    r"waitretry|retry[\w-]*)\b|-[mYyTt](?!\S))"
)
MENTION = "names the tool without running it"
# (file, exact stripped line) -> (reason, None) or (reason, (offset, exact options that line offset lines below must
# carry)). Every entry must still match a line.
EXEMPT: dict[tuple[str, str], tuple[str, tuple[int, str] | None]] = {
    (
        "setup.sh",
        "# Network bounds: curl gets 30 s to connect and fails a transfer under 1 KB/s for 60 s; wget waits",
    ): (f"comment; {MENTION}", None),
    ("setup.sh", "if command -v curl > /dev/null 2>&1; then"): (f"presence check; {MENTION}", None),
    ("setup.sh", "# The credential goes through curl's config on stdin, never the command line."): (
        f"comment; {MENTION}",
        None,
    ),
    (
        "setup.sh",
        "# wget reads the credential from a private wgetrc (mktemp creates it 0600), never the command line.",
    ): (f"comment; {MENTION}", None),
    ("setup.sh", "#   gh can check the asset against it (`make docker` passes it to the Dockerfile). Needs curl."): (
        f"comment; {MENTION}",
        None,
    ),
    ("setup.sh", "# @description Download one URL to standard output, preferring curl over wget. curl gets 30 s to"): (
        f"shdoc; {MENTION}",
        None,
    ),
    (
        "setup.sh",
        "#   connect and fails a transfer under 1 KB/s for 60 s; wget waits at most 60 s for any one connect",
    ): (f"shdoc; {MENTION}", None),
    ("setup.sh", "elif command -v wget > /dev/null 2>&1; then"): (f"presence check; {MENTION}", None),
    ("setup.sh", 'echo "Neither curl nor wget is available; cannot download ${url}." >&2'): (
        f"message; {MENTION}",
        None,
    ),
    ("setup.sh", "# @description Download one URL to a file, preferring curl over wget, with fetch_url's bounds."): (
        f"shdoc; {MENTION}",
        None,
    ),
    ("setup.sh", "printf 'Neither curl nor wget is available; cannot download %s.\\n' \"${url}\" >&2"): (
        f"message; {MENTION}",
        None,
    ),
    (
        "install/common/aws_cli.sh",
        "# curl gets 30 s to connect and fails a transfer under 1 KB/s for 60 s, so a stalled download ends.",
    ): (f"comment; {MENTION}", None),
    (
        "install/common/mise.sh",
        "# Each curl gets 30 s to connect and fails a transfer under 1 KB/s for 60 s, so a stalled download ends.",
    ): (f"comment; {MENTION}", None),
    (
        "install/ubuntu/server/starship.sh",
        "# Each curl gets 30 s to connect and fails a transfer under 1 KB/s for 60 s, so a stalled download ends.",
    ): (f"comment; {MENTION}", None),
    ("install/ubuntu/client/docker.sh", "curl \\"): ("an apt-get install package name", None),
    ("install/ubuntu/common/dependencies.sh", "curl"): ("a PACKAGES entry", None),
    ("install/ubuntu/common/dependencies.sh", "wget"): ("a PACKAGES entry", None),
    (
        "install/ubuntu/client/ghostty.sh",
        "#   answer within the timeout (curl exit 5, 6, 7, 28, 35, 52 or 56), or answers HTTP 5xx;",
    ): (f"shdoc; {MENTION}", None),
    (
        "install/ubuntu/client/ghostty.sh",
        "#   other curl failure (a local error, not evidence of the network): curl's status, unchanged.",
    ): (f"shdoc; {MENTION}", None),
    (
        "install/ubuntu/client/ghostty.sh",
        "out=\"$(curl -q --silent --show-error --output /dev/null --write-out '%{http_connect} %{http_code}' \\",
    ): (
        "the PPA probe bounds itself tighter than the convention (5 s to connect, 15 s in all); options on line +1",
        (1, "--connect-timeout 5 --max-time 15"),
    ),
    ("install/ubuntu/client/ghostty.sh", 'printf \'%s (curl exit %s)\\n\' "${url}" "${status}"'): (
        f"message; {MENTION}",
        None,
    ),
    (
        "scripts/generate-agent-configs.py",
        '"# shell after a pipe (`curl ... | sh`), which no prefix rule can name without matching Codex\'s own shell.",',
    ): ("a rendered comment about command policy; names the tool without running it", None),
    (
        "scripts/validate-agent-assets.py",
        "# too, an allow row that mentions `gh`, `graphql`, `api.github.com`, `curl` or `wget` must be byte-identical to an",
    ): (f"comment; {MENTION}", None),
    ("scripts/lib/github-release.sh", "#   Only curl or wget and awk are needed, so a fresh machine can run it."): (
        f"comment; {MENTION}",
        None,
    ),
    (
        "scripts/lib/github-release.sh",
        "# Network bounds: curl gets 30 s to connect and fails a transfer under 1 KB/s for 60 s; wget waits",
    ): (f"comment; {MENTION}", None),
    ("scripts/lib/github-release.sh", "if command -v curl > /dev/null 2>&1; then"): (
        f"presence check; {MENTION}",
        None,
    ),
    (
        "scripts/lib/github-release.sh",
        "# The credential goes through curl's config on stdin, never the command line.",
    ): (f"comment; {MENTION}", None),
    (
        "scripts/lib/github-release.sh",
        "# wget reads the credential from a private wgetrc (mktemp creates it 0600), never the command line.",
    ): (f"comment; {MENTION}", None),
    (
        "scripts/lib/github-release.sh",
        "#   gh can check the asset against it (`make docker` passes it to the Dockerfile). Needs curl.",
    ): (f"comment; {MENTION}", None),
    ("scripts/lib/installer-pins.sh", "#   tode and terminal-browser install through a vendor `curl | bash` script"): (
        f"comment; {MENTION}",
        None,
    ),
    (
        ".github/workflows/test.yaml",
        "sudo apt-get update && sudo apt-get install -y bats curl iproute2 parallel ruby shellcheck",
    ): ("an apt-get install package name", None),
    (".github/workflows/test.yaml", "sudo apt-get install -y jq curl"): ("an apt-get install package name", None),
}
# The manifest_record lines of update-agent-assets.sh store each asset's source ("curl -fsSL <url>", then its sha256
# step) as data in ~/.agents/.installed-manifest.json; they run nothing. Matched by exact text like every entry.
MANIFEST_RECORDS = (
    "ensure_crit_cli",
    "update_codex_understand_anything",
    "update_terminal_code",
    "update_terminal_browser",
    "update_pi_claude_bridge",
)
SNAP_EXEMPT = {
    (
        "install/ubuntu/client/misc.sh",
        "# @exitcode The last `snap install` exit status after the final failed attempt.",
    ): "shdoc",
    (
        "install/ubuntu/client/misc.sh",
        "printf 'install_chromium: snap install chromium timed out after %s s (SNAP_INSTALL_TIMEOUT); snapd may still finish it (snap changes)\\n' \\",
    ): "message",
    (
        "install/ubuntu/client/misc.sh",
        "printf 'install_chromium: snap install chromium failed (attempt %d/3, exit %d)\\n' \\",
    ): "message",
}


def manifest_record_exempt(relative: str, line: str) -> bool:
    # The key is the repo-relative POSIX name tree() builds, the same form as every EXEMPT key.
    return relative == "scripts/update-agent-assets.sh" and any(  # lint-comparisons: allow table-key
        line.startswith(f'manifest_record "{name}" installer ') for name in MANIFEST_RECORDS
    )


def carries(line: str, tool: str, count: int) -> bool:
    """The line carries the tool's canonical options once per occurrence of the tool word, and no other time or
    retry option."""
    canonical = CANONICAL[tool]
    return line.count(canonical) >= count and not OTHER_BOUND.search(line.replace(canonical, " "))


def violations(relative: str, text: str, exempt=None, snap_exempt=None) -> list[str]:
    """The lines of one file that break the rule, as `file:line: text`."""
    exempt = EXEMPT if exempt is None else exempt
    snap_exempt = SNAP_EXEMPT if snap_exempt is None else snap_exempt
    lines = text.splitlines()
    bad = []
    for number, raw in enumerate(lines, 1):
        line = raw.strip()
        where = f"{relative}:{number}: {line}"
        tools = TOOL.findall(line)
        if tools:
            entry = exempt.get((relative, line))
            if entry is not None:
                options = entry[1]
                if options is not None:
                    offset, exact = options
                    other = lines[number - 1 + offset].strip() if number - 1 + offset < len(lines) else ""
                    if exact not in other or OTHER_BOUND.search(other.replace(exact, " ")):
                        bad.append(f"{where} (line +{offset} must carry exactly {exact})")
            elif not manifest_record_exempt(relative, line):
                for tool in ("curl", "wget"):
                    if tool in tools and not carries(line, tool, tools.count(tool)):
                        bad.append(where)
                        break
        if SNAP.search(line) and SNAP_CANONICAL not in line and (relative, line) not in snap_exempt:
            bad.append(where)
    return bad


def stale(files: dict[str, str], exempt=None, snap_exempt=None) -> list[str]:
    """The exemptions whose file no longer holds their exact line."""
    exempt = EXEMPT if exempt is None else exempt
    snap_exempt = SNAP_EXEMPT if snap_exempt is None else snap_exempt
    lines = {relative: {line.strip() for line in text.splitlines()} for relative, text in files.items()}
    gone = [f"{r}: {t}" for r, t in [*exempt, *snap_exempt] if t not in lines.get(r, set())]
    for name in MANIFEST_RECORDS:
        if not any(
            l.startswith(f'manifest_record "{name}" installer ')
            for l in lines.get("scripts/update-agent-assets.sh", ())
        ):
            gone.append(f"scripts/update-agent-assets.sh: manifest_record {name}")
    return gone


def tree() -> dict[str, str]:
    texts = {}
    for path in NETWORK_SOURCES:
        try:
            texts[path.relative_to(ROOT).as_posix()] = path.read_text()
        except UnicodeDecodeError:
            continue
    return texts


class NetworkBoundTest(unittest.TestCase):
    def test_every_curl_and_wget_line_carries_the_canonical_bound_or_is_exempted(self) -> None:
        bad = [hit for relative, text in tree().items() for hit in violations(relative, text)]
        self.assertEqual([], bad)

    def test_no_exemption_is_stale(self) -> None:
        self.assertEqual([], stale(tree()))
        # The table is the only way out, so a scan that saw no download line would be a broken scan.
        downloads = sum(
            1
            for relative, text in tree().items()
            for line in text.splitlines()
            if any(CANONICAL[t] in line for t in CANONICAL)
        )
        self.assertGreater(downloads, 40)

    def test_the_audit_bypasses_fail(self) -> None:
        # Audits of c7629e24 and 86e1f99e: bare calls, substitutions, array values, defaults and zero values.
        for snippet in (
            "curl https://x.invalid/a",
            "wget https://x.invalid/a",
            'printf "%s\\n" "$(curl -fsSL https://x.invalid/a)"',
            'artifacts=("$(curl https://x.invalid/a)")',
            'y="${x:-$(curl -fsSL https://x.invalid/a)}"',
            "curl --connect-timeout 0 --speed-limit 1024 --speed-time 60 https://x.invalid/a",
            "curl --connect-timeout 30 --speed-limit 0 --speed-time 60 https://x.invalid/a",
            "curl --connect-timeout 30 --speed-limit 1024 --speed-time 60 --max-time 0 https://x.invalid/a",
            "curl --connect-timeout 30 --speed-limit 1024 --speed-time 60 -m 0 https://x.invalid/a",
            "wget --timeout=0 --tries=0 https://x.invalid/a",
            "wget --timeout=60 --tries=3 --tries=0 https://x.invalid/a",
            "wget --timeout=60 --tries=3 -T 0 https://x.invalid/a",
            "a=$(curl --connect-timeout 30 --speed-limit 1024 --speed-time 60 u) b=$(curl u)",
            "curl -fsSL \\",
            "# curl https://x.invalid/a",
            "sudo snap install chromium",
        ):
            with self.subTest(snippet=snippet):
                self.assertEqual(1, len(violations("install/x.sh", snippet + "\n", {}, {})), snippet)

    def test_canonical_calls_pass(self) -> None:
        for snippet in (
            "curl -fsSL --connect-timeout 30 --speed-limit 1024 --speed-time 60 https://x.invalid/a -o a",
            'v="$(curl --connect-timeout 30 --speed-limit 1024 --speed-time 60 https://x.invalid/a)"',
            "wget --timeout=60 --tries=3 -qO - https://x.invalid/a",
            'sudo timeout --kill-after=30 "${limit}" snap install chromium && return 0',
            "curlrc and wgetrc are other words",
        ):
            with self.subTest(snippet=snippet):
                self.assertEqual([], violations("install/x.sh", snippet + "\n", {}, {}), snippet)

    def test_an_exemption_needs_its_exact_line_and_its_options(self) -> None:
        exempt = {("install/x.sh", "curl \\"): ("options on line +1", (1, "--connect-timeout 5 --max-time 15"))}
        self.assertEqual([], violations("install/x.sh", "curl \\\n  --connect-timeout 5 --max-time 15 u\n", exempt, {}))
        for options in ("--connect-timeout 0 --max-time 15 u", "--connect-timeout 5 --max-time 15 --max-time 0 u", "u"):
            with self.subTest(options=options):
                self.assertEqual(1, len(violations("install/x.sh", f"curl \\\n  {options}\n", exempt, {})))
        # A line that changed, even by one character, is no longer exempt, and its entry is stale.
        self.assertEqual(
            1, len(violations("install/x.sh", "curl  \\\n", {("install/x.sh", "curl \\"): ("x", None)}, {}))
        )
        self.assertEqual(
            ["install/x.sh: curl \\"],
            stale(
                {
                    "install/x.sh": "curl  \\\n",
                    "scripts/update-agent-assets.sh": "\n".join(
                        f'manifest_record "{n}" installer' + " x" for n in MANIFEST_RECORDS
                    ),
                },
                {("install/x.sh", "curl \\"): ("x", None)},
                {},
            ),
        )


# A bare Bats run in a workflow or the runner: `bats` as a command word, not run_bats, bats-core or a package list.
BARE_BATS = re.compile(r"(?<![\w/.-])bats\s")


class RunBatsBoundTest(unittest.TestCase):
    """run_bats (scripts/run_unit_test.sh, then scripts/ci/run-bats.py) against a fake `bats` that writes Bats'
    extended stream."""

    def setUp(self) -> None:
        self.temp = Path(tempfile.mkdtemp(prefix="run-bats-"))
        self.addCleanup(shutil.rmtree, self.temp, True)
        (self.temp / "bin").mkdir()
        # The python3 the runner calls, so the case does not depend on the host's.
        (self.temp / "bin/python3").symlink_to(sys.executable)
        self.pids = self.temp / "pids"
        # The wrapper signals nothing, so the case itself stops what its fake left running.
        self.addCleanup(self.kill_recorded)

    def kill_recorded(self) -> None:
        for line in self.pids.read_text().split() if self.pids.exists() else []:
            try:
                os.kill(int(line), signal.SIGKILL)
            except OSError:
                pass

    def fake_bats(self, body: str) -> None:
        script = self.temp / "bin/bats"
        script.write_text(f'#!{BASH}\nprintf "%s\\n" "$*" > "{self.temp}/args"\n' + textwrap.dedent(body))
        script.chmod(0o755)

    def run_bats(self, bound: str, *args: str) -> tuple[int, str, str, float]:
        env = {
            "PATH": f"{self.temp / 'bin'}:/usr/bin:/bin",
            "HOME": str(self.temp),
            "TMPDIR": str(self.temp),
            "BATS_PER_TEST_TIMEOUT": bound,
            "PIDS": str(self.pids),
        }
        out, err = self.temp / "out", self.temp / "err"
        started = time.monotonic()
        # Files, not pipes: what a stalled test leaves running keeps its copies of stdout and stderr, and the time
        # measured is the wrapper's own return.
        with out.open("w") as stdout, err.open("w") as stderr:
            process = subprocess.Popen(
                [BASH, "-c", 'source "$1" && shift && run_bats "$@"', "_", str(RUNNER), *args],
                env=env, stdin=subprocess.DEVNULL, stdout=stdout, stderr=stderr,
            )  # fmt: skip
            status = process.wait(timeout=60)
        return status, out.read_text(), err.read_text(), time.monotonic() - started

    def test_a_stalled_test_is_named_and_the_run_fails_within_the_bound(self) -> None:
        # The stalled test's grandchild is what kept the PR #570 jobs alive until the job timeout.
        self.fake_bats(
            """\
            printf '1..2\\nsuite tests/x.bats\\nbegin 1 [x] fast\\nok 1 [x] fast\\nbegin 2 [x] misc\\n'
            echo $$ >> "${PIDS}"
            sleep 300 &
            echo $! >> "${PIDS}"
            wait
            """
        )
        status, out, err, elapsed = self.run_bats("2", "-r", "tests/x/")
        self.assertEqual(124, status, out + err)
        self.assertLess(elapsed, 4)
        self.assertEqual(
            "1..2\nrunning: 1 [x] fast\nok 1 [x] fast\nrunning: 2 [x] misc\n"
            "not ok 2 [x] misc # timeout after 2 s (BATS_PER_TEST_TIMEOUT)\n",
            out,
        )
        self.assertEqual("--formatter cat -r tests/x/\n", (self.temp / "args").read_text())

    def test_output_from_a_running_test_does_not_extend_its_bound(self) -> None:
        self.fake_bats(
            """\
            printf '1..1\\nbegin 1 [x] chatty\\n'
            echo $$ >> "${PIDS}"
            while true; do printf '# still running\\n'; sleep 0.2; done
            """
        )
        status, out, err, elapsed = self.run_bats("2", "tests/x.bats")
        self.assertEqual(124, status, out + err)
        self.assertLess(elapsed, 4)
        self.assertIn("not ok 1 [x] chatty # timeout after 2 s", out)

    def test_loading_the_files_is_bounded_too(self) -> None:
        # Bats sources every file before its plan line; nothing runs Bats outside the bound (no `bats --count`).
        self.fake_bats('echo $$ >> "${PIDS}"\nsleep 300\n')
        status, out, err, elapsed = self.run_bats("2", "tests/x.bats")
        self.assertEqual(124, status, out + err)
        self.assertLess(elapsed, 4)
        self.assertIn("not ok - Bats printed nothing for 2 s outside a test", out)

    def test_pass_and_fail_statuses_are_kept(self) -> None:
        for code in (0, 1):
            with self.subTest(status=code):
                verdict = "ok 2 [x] b" if code == 0 else "not ok 2 [x] b"
                self.fake_bats(
                    f"""\
                    printf '1..2\\nsuite tests/x.bats\\nbegin 1 [x] a\\nok 1 [x] a\\nbegin 2 [x] b\\n# output of b\\n'
                    printf '{verdict}\\n'
                    exit {code}
                    """
                )
                status, out, err, elapsed = self.run_bats("30", "tests/x.bats")
                self.assertEqual(code, status, err)
                self.assertLess(elapsed, 10)
                self.assertEqual(
                    f"1..2\nrunning: 1 [x] a\nok 1 [x] a\nrunning: 2 [x] b\n# output of b\n{verdict}\n", out
                )

    def test_a_run_that_plans_no_test_fails(self) -> None:
        for body, shown in (("printf '1..0\\n'\n", "0"), ("exit 0\n", "nothing")):
            with self.subTest(plan=shown):
                self.fake_bats(body)
                status, out, err, _ = self.run_bats("30", "--filter-tags", "common,ubuntu:client", "x.bats")
                self.assertEqual(1, status, out + err)
                self.assertIn(f"expected at least one test; Bats planned {shown}", err)

    def test_the_wrapper_signals_nothing(self) -> None:
        # Stopping processes is the step's timeout-minutes and the runner's job, not this wrapper's.
        text = WRAPPER.read_text()
        for api in (r"import signal", r"os\.kill", r"killpg", r"setsid", r"start_new_session", r'"ps"'):
            with self.subTest(api=api):
                self.assertNotRegex(text, api)
        self.assertIn('python3 -I -S "${here}/ci/run-bats.py"', RUNNER.read_text())


def workflow_steps(text: str) -> list[str]:
    """Each step of a workflow, as its text: from its `- ` line to the next step or the end of its list."""
    steps, current, indent = [], None, None
    for line in text.splitlines():
        match = re.match(r"^(\s*)- (?:name|uses|run|id|if|env|shell|with):", line)
        stripped = len(line) - len(line.lstrip())
        if match and (indent is None or len(match.group(1)) == indent):
            if current is not None:
                steps.append("\n".join(current))
            current, indent = [line], len(match.group(1))
        elif current is not None and line.strip() and stripped <= indent:
            steps.append("\n".join(current))
            current, indent = None, None
        elif current is not None:
            current.append(line)
    if current is not None:
        steps.append("\n".join(current))
    return steps


class CiBatsRunTest(unittest.TestCase):
    """Every Bats run CI starts goes through run_bats, in a step with its own timeout-minutes."""

    def test_the_runner_calls_bats_only_through_run_bats(self) -> None:
        calls_ = [line.strip() for line in RUNNER.read_text().splitlines() if BARE_BATS.search(line.split("#")[0])]
        self.assertEqual([], calls_)
        self.assertIn('["bats", "--formatter", "cat", *argv]', WRAPPER.read_text())
        text = RUNNER.read_text()
        for function in ("run_common_test", "run_os_specific_test", "run_files_test"):
            start = text.index(f"function {function}() {{\n")
            self.assertIn("run_bats ", text[start : text.index("\n}\n", start)], function)

    def test_no_workflow_runs_bats_directly(self) -> None:
        bare, through_runner = [], set()
        for workflow in sorted(WORKFLOWS.glob("*.y*ml")):
            for number, line in enumerate(workflow.read_text().splitlines(), 1):
                command = line.split("#")[0].strip()
                if "run_bats" in command or "run_unit_test.sh" in command:
                    through_runner.add(workflow.name)
                # Package installs name the bats package; they do not run it.
                if BARE_BATS.search(command) and "install" not in command:
                    bare.append(f"{workflow.name}:{number}: {command}")
        self.assertEqual([], bare)
        self.assertLessEqual({"test.yaml", "macos.yaml", "ubuntu.yaml"}, through_runner)
        unit_test = (WORKFLOWS / "test.yaml").read_text()
        step = unit_test[unit_test.index("- name: Run unit test\n") :]
        step = step[: step.index("\n      - name: ")]
        self.assertEqual(2, step.count("./scripts/run_unit_test.sh"), step)

    def test_every_bats_step_has_its_own_timeout(self) -> None:
        found, missing = 0, []
        for workflow in sorted(WORKFLOWS.glob("*.y*ml")):
            for step in workflow_steps(workflow.read_text()):
                if "run_bats" not in step and "run_unit_test.sh" not in step:
                    continue
                found += 1
                match = re.search(r"^\s+timeout-minutes: ([0-9]+)$", step, re.MULTILINE)
                # Above one per-test bound (1200 s, scripts/ci/run-bats.py), so the stalled test is named first.
                if not match or int(match.group(1)) * 60 <= 1200:
                    missing.append(f"{workflow.name}: {step.splitlines()[0].strip()}")
        self.assertEqual([], missing)
        self.assertEqual(3, found)


if __name__ == "__main__":
    unittest.main()
