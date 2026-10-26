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
from typing import NamedTuple

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
# The long options that bound or retry a transfer, curl's and wget's. wget accepts any unambiguous prefix of a long
# option, so a prefix of one of these (`--time=0`, `--tri=0`) counts too, as does every `--retry…` option.
BOUND_LONG = (
    "connect-timeout", "max-time", "speed-limit", "speed-time", "timeout", "tries", "read-timeout", "dns-timeout",
    "waitretry", "keepalive-time", "expect100-timeout", "happy-eyeballs-timeout-ms", "limit-rate",
)  # fmt: skip
LONG_OPTION = re.compile(r"(?<![\w-])--([A-Za-z][\w-]*)")
# A short-option cluster holding curl's -m (max time), -y (speed time) or -Y (speed limit), or wget's -T (timeout) or
# -t (tries), separate or attached to a value or other options: `-m 0`, `-m0`, `-y0`, `-Y0`, `-T0`, `-t0`, `-sSm0`.
SHORT_BOUND = re.compile(r"(?<![\w-])-[A-Za-z0-9]*[mYyTt]")


def bound_options(text: str) -> list[str]:
    """Every time or retry option in the text, in any spelling: long, `=`-joined, abbreviated (wget), short, attached."""
    found = [m.group(0) for m in SHORT_BOUND.finditer(text)]
    for match in LONG_OPTION.finditer(text):
        name = match.group(1)
        if name.startswith("retry") or any(full.startswith(name) for full in BOUND_LONG):
            found.append(match.group(0))
    return found


class Exempt(NamedTuple):
    """Why a line that holds curl or wget is exempt from carrying the canonical options on its own text.

    `continued` is the number of continuation lines after a line ending in `\\`; they are checked: together they hold
    `options` exactly (when given) and, apart from it, no time or retry option in any spelling, and the last one ends
    the command. A `call` carries the canonical options on its own line unless `options` names its own bound.
    """

    reason: str
    continued: int = 0
    options: str = ""
    call: bool = False


MENTION = "names the tool without running it"
# (file, the whole stripped line, exactly) -> Exempt. Every entry must still match a line (test_no_exemption_is_stale).
EXEMPT: dict[tuple[str, str], Exempt] = {
    (
        "setup.sh",
        "# Network bounds: curl gets 30 s to connect and fails a transfer under 1 KB/s for 60 s; wget waits",
    ): Exempt("comment; names the tool without running it"),
    ("setup.sh", "if command -v curl > /dev/null 2>&1; then"): Exempt(
        "presence check; names the tool without running it"
    ),
    ("setup.sh", "# The credential goes through curl's config on stdin, never the command line."): Exempt(
        "comment; names the tool without running it"
    ),
    (
        "setup.sh",
        "# wget reads the credential from a private wgetrc (mktemp creates it 0600), never the command line.",
    ): Exempt("comment; names the tool without running it"),
    (
        "setup.sh",
        "#   gh can check the asset against it (`make docker` passes it to the Dockerfile). Needs curl.",
    ): Exempt("comment; names the tool without running it"),
    (
        "setup.sh",
        "# @description Download one URL to standard output, preferring curl over wget. curl gets 30 s to",
    ): Exempt("shdoc; names the tool without running it"),
    (
        "setup.sh",
        "#   connect and fails a transfer under 1 KB/s for 60 s; wget waits at most 60 s for any one connect",
    ): Exempt("shdoc; names the tool without running it"),
    ("setup.sh", "elif command -v wget > /dev/null 2>&1; then"): Exempt(
        "presence check; names the tool without running it"
    ),
    ("setup.sh", 'echo "Neither curl nor wget is available; cannot download ${url}." >&2'): Exempt(
        "message; names the tool without running it"
    ),
    (
        "setup.sh",
        "# @description Download one URL to a file, preferring curl over wget, with fetch_url's bounds.",
    ): Exempt("shdoc; names the tool without running it"),
    ("setup.sh", "printf 'Neither curl nor wget is available; cannot download %s.\\n' \"${url}\" >&2"): Exempt(
        "message; names the tool without running it"
    ),
    (
        "install/common/aws_cli.sh",
        "# curl gets 30 s to connect and fails a transfer under 1 KB/s for 60 s, so a stalled download ends.",
    ): Exempt("comment; names the tool without running it"),
    (
        "install/common/mise.sh",
        "# Each curl gets 30 s to connect and fails a transfer under 1 KB/s for 60 s, so a stalled download ends.",
    ): Exempt("comment; names the tool without running it"),
    (
        "install/ubuntu/server/starship.sh",
        "# Each curl gets 30 s to connect and fails a transfer under 1 KB/s for 60 s, so a stalled download ends.",
    ): Exempt("comment; names the tool without running it"),
    ("install/ubuntu/client/docker.sh", "curl \\"): Exempt("an apt-get install package name", continued=1),
    ("install/ubuntu/common/dependencies.sh", "curl"): Exempt("a PACKAGES entry"),
    ("install/ubuntu/common/dependencies.sh", "wget"): Exempt("a PACKAGES entry"),
    (
        "install/ubuntu/client/ghostty.sh",
        "#   answer within the timeout (curl exit 5, 6, 7, 28, 35, 52 or 56), or answers HTTP 5xx;",
    ): Exempt("shdoc; names the tool without running it"),
    (
        "install/ubuntu/client/ghostty.sh",
        "#   other curl failure (a local error, not evidence of the network): curl's status, unchanged.",
    ): Exempt("shdoc; names the tool without running it"),
    (
        "install/ubuntu/client/ghostty.sh",
        "out=\"$(curl -q --silent --show-error --output /dev/null --write-out '%{http_connect} %{http_code}' \\",
    ): Exempt(
        "the PPA probe bounds itself tighter than the convention: 5 s to connect, 15 s in all",
        continued=1,
        options="--connect-timeout 5 --max-time 15",
        call=True,
    ),
    ("install/ubuntu/client/ghostty.sh", 'printf \'%s (curl exit %s)\\n\' "${url}" "${status}"'): Exempt(
        "message; names the tool without running it"
    ),
    (
        "scripts/generate-agent-configs.py",
        '"# shell after a pipe (`curl ... | sh`), which no prefix rule can name without matching Codex\'s own shell.",',
    ): Exempt("a rendered comment about command policy; names the tool without running it"),
    (
        "scripts/validate-agent-assets.py",
        "# too, an allow row that mentions `gh`, `graphql`, `api.github.com`, `curl` or `wget` must be byte-identical to an",
    ): Exempt("comment; names the tool without running it"),
    (
        "scripts/lib/github-release.sh",
        "#   Only curl or wget and awk are needed, so a fresh machine can run it.",
    ): Exempt("comment; names the tool without running it"),
    (
        "scripts/lib/github-release.sh",
        "# Network bounds: curl gets 30 s to connect and fails a transfer under 1 KB/s for 60 s; wget waits",
    ): Exempt("comment; names the tool without running it"),
    ("scripts/lib/github-release.sh", "if command -v curl > /dev/null 2>&1; then"): Exempt(
        "presence check; names the tool without running it"
    ),
    (
        "scripts/lib/github-release.sh",
        "# The credential goes through curl's config on stdin, never the command line.",
    ): Exempt("comment; names the tool without running it"),
    (
        "scripts/lib/github-release.sh",
        "# wget reads the credential from a private wgetrc (mktemp creates it 0600), never the command line.",
    ): Exempt("comment; names the tool without running it"),
    (
        "scripts/lib/github-release.sh",
        "#   gh can check the asset against it (`make docker` passes it to the Dockerfile). Needs curl.",
    ): Exempt("comment; names the tool without running it"),
    (
        "scripts/lib/installer-pins.sh",
        "#   tode and terminal-browser install through a vendor `curl | bash` script",
    ): Exempt("comment; names the tool without running it"),
    (
        ".github/workflows/test.yaml",
        "sudo apt-get update && sudo apt-get install -y bats curl iproute2 parallel ruby",
    ): Exempt("an apt-get install package name"),
    (".github/workflows/test.yaml", "sudo apt-get install -y jq curl"): Exempt("an apt-get install package name"),
    # U96's chezmoi externals prefetch (scripts/lib/chezmoi-externals.sh and its copy in setup.sh): its own allowlisted
    # retry loop, so curl's --retry stays off; --max-time 900 caps one attempt on the checked continuation.
    **{
        (relative, line): entry
        for relative in ("setup.sh", "scripts/lib/chezmoi-externals.sh")
        for line, entry in (
            ("# @stdout The HTTP status curl saw.", Exempt(f"shdoc; {MENTION}")),
            (
                "# @exitcode * curl's exit status (22 for an HTTP error, 18 for a truncated transfer).",
                Exempt(f"shdoc; {MENTION}"),
            ),
            (
                "curl --proto '=http,https' --location --fail --silent --show-error --connect-timeout 30 --speed-limit 1024 --speed-time 60 \\",
                Exempt("the prefetch download; options on line +1", continued=1, options="--max-time 900", call=True),
            ),
            (
                '# Retried only from an allowlist of transient remote or network faults (curl(1), "Exit codes"): 6 could not',
                Exempt(f"comment; {MENTION}"),
            ),
            (
                'case "${status}/${code}" in # lint-comparisons: allow curl\'s exit status and HTTP code, not a path',
                Exempt(f"case on curl's status; {MENTION}"),
            ),
            (
                "printf 'chezmoi external %s: %s: download failed after %s attempt(s) (last: curl exit %s, HTTP %s); nothing cached\\n' \\",
                Exempt(f"message; {MENTION}", continued=1),
            ),
            (
                "printf 'chezmoi external %s: %s: attempt %s failed (curl exit %s, HTTP %s); retrying in %ss\\n' \\",
                Exempt(f"message; {MENTION}", continued=1),
            ),
            (
                "#   before it is cached. Without curl the step only says so, and chezmoi fetches the externals itself as before.",
                Exempt(f"shdoc; {MENTION}"),
            ),
            ("if ! command -v curl > /dev/null 2>&1; then", Exempt(f"presence check; {MENTION}")),
            (
                "printf 'chezmoi externals: curl not found; chezmoi fetches them itself, without retries\\n' >&2",
                Exempt(f"message; {MENTION}"),
            ),
        )
    },
    (
        "scripts/lib/chezmoi-externals.sh",
        "#   tests/unit/test_chezmoi_externals.py keeps the copies equal. It needs curl, awk and sha256sum or shasum.",
    ): Exempt(f"comment; {MENTION}"),
    ("setup.sh", "curl -fsSL --connect-timeout 30 --speed-limit 1024 --speed-time 60 -K - \\"): Exempt(
        "a bounded call whose remaining arguments continue", continued=1, call=True
    ),
    ("setup.sh", "curl -fsSL --connect-timeout 30 --speed-limit 1024 --speed-time 60 \\"): Exempt(
        "a bounded call whose remaining arguments continue", continued=1, call=True
    ),
    ("setup.sh", 'wget --config="${wgetrc}" --timeout=60 --tries=3 -qO - \\'): Exempt(
        "a bounded call whose remaining arguments continue", continued=1, call=True
    ),
    (
        "install/common/aws_cli.sh",
        "curl --fail --location --silent --show-error --connect-timeout 30 --speed-limit 1024 --speed-time 60 \\",
    ): Exempt("a bounded call whose remaining arguments continue", continued=1, call=True),
    (
        "install/common/aws_cli.sh",
        'staged_version="$(curl --fail --location --silent --show-error --connect-timeout 30 --speed-limit 1024 --speed-time 60 \\',
    ): Exempt("a bounded call whose remaining arguments continue", continued=1, call=True),
    (
        "install/common/mise.sh",
        'curl -fsSL --connect-timeout 30 --speed-limit 1024 --speed-time 60 "${base_url}/${artifact}" \\',
    ): Exempt("a bounded call whose remaining arguments continue", continued=1, call=True),
    (
        "install/common/mise.sh",
        'if curl -fsSL --connect-timeout 30 --speed-limit 1024 --speed-time 60 "${base_url}/SHASUMS256.asc" \\',
    ): Exempt("a bounded call whose remaining arguments continue", continued=1, call=True),
    (
        "install/common/mise.sh",
        'curl -fsSL --connect-timeout 30 --speed-limit 1024 --speed-time 60 "${base_url}/SHASUMS256.txt" \\',
    ): Exempt("a bounded call whose remaining arguments continue", continued=1, call=True),
    ("install/macos/common/brew.sh", "curl -fsSL --connect-timeout 30 --speed-limit 1024 --speed-time 60 \\"): Exempt(
        "a bounded call whose remaining arguments continue", continued=1, call=True
    ),
    (
        "install/ubuntu/client/docker.sh",
        "sudo curl -fsSL --connect-timeout 30 --speed-limit 1024 --speed-time 60 https://download.docker.com/linux/ubuntu/gpg \\",
    ): Exempt("a bounded call whose remaining arguments continue", continued=1, call=True),
    (
        "install/ubuntu/client/tailscale.sh",
        "curl -fsSL --connect-timeout 30 --speed-limit 1024 --speed-time 60 \\",
    ): Exempt("a bounded call whose remaining arguments continue", continued=1, call=True),
    ("install/ubuntu/client/zed.sh", "curl -fsSL --connect-timeout 30 --speed-limit 1024 --speed-time 60 \\"): Exempt(
        "a bounded call whose remaining arguments continue", continued=1, call=True
    ),
    (
        "install/ubuntu/server/starship.sh",
        'curl -fsSL --connect-timeout 30 --speed-limit 1024 --speed-time 60 "${base_url}/${artifact}" \\',
    ): Exempt("a bounded call whose remaining arguments continue", continued=1, call=True),
    (
        "install/ubuntu/server/starship.sh",
        'expected="$(curl -fsSL --connect-timeout 30 --speed-limit 1024 --speed-time 60 \\',
    ): Exempt("a bounded call whose remaining arguments continue", continued=1, call=True),
    (
        "scripts/lib/github-release.sh",
        "curl -fsSL --connect-timeout 30 --speed-limit 1024 --speed-time 60 -K - \\",
    ): Exempt("a bounded call whose remaining arguments continue", continued=1, call=True),
    ("scripts/lib/github-release.sh", "curl -fsSL --connect-timeout 30 --speed-limit 1024 --speed-time 60 \\"): Exempt(
        "a bounded call whose remaining arguments continue", continued=1, call=True
    ),
    ("scripts/lib/github-release.sh", 'wget --config="${wgetrc}" --timeout=60 --tries=3 -qO - \\'): Exempt(
        "a bounded call whose remaining arguments continue", continued=1, call=True
    ),
    (
        "scripts/update-agent-assets.sh",
        'curl -fsSL --connect-timeout 30 --speed-limit 1024 --speed-time 60 "${CODEX_UNDERSTAND_ANYTHING_INSTALLER_URL}" \\',
    ): Exempt("a bounded call whose remaining arguments continue", continued=1, call=True),
    (
        "scripts/update-agent-assets.sh",
        'curl -fsSL --connect-timeout 30 --speed-limit 1024 --speed-time 60 "${PI_CLAUDE_BRIDGE_TARBALL_URL}" \\',
    ): Exempt("a bounded call whose remaining arguments continue", continued=1, call=True),
    (
        ".github/workflows/agent-assets.yml",
        'curl -fsSL --connect-timeout 30 --speed-limit 1024 --speed-time 60 "${base_url}/chezmoi_${chezmoi_version}_checksums.txt" \\',
    ): Exempt("a bounded call whose remaining arguments continue", continued=2, call=True),
    (
        ".github/workflows/agent-assets.yml",
        "curl --fail --location --silent --show-error --connect-timeout 30 --speed-limit 1024 --speed-time 60 \\",
    ): Exempt("a bounded call whose remaining arguments continue", continued=1, call=True),
    (
        ".github/workflows/remote.yaml",
        'curl -fsSL --connect-timeout 30 --speed-limit 1024 --speed-time 60 "${base_url}/chezmoi_${chezmoi_version}_checksums.txt" \\',
    ): Exempt("a bounded call whose remaining arguments continue", continued=2, call=True),
    (
        ".github/workflows/test.yaml",
        'curl -fsSL --connect-timeout 30 --speed-limit 1024 --speed-time 60 "${base_url}/chezmoi_${chezmoi_version}_checksums.txt" \\',
    ): Exempt("a bounded call whose remaining arguments continue", continued=2, call=True),
    (
        "scripts/update-agent-assets.sh",
        'manifest_record "ensure_crit_cli" installer "${tag}" "${target}" -- "curl -fsSL https://github.com/${CRIT_RELEASE_REPO}/releases/download/${tag}/${artifact}" "curl -fsSL https://github.com/${CRIT_RELEASE_REPO}/releases/download/${tag}/checksums.txt" "shasum -a 256 <binary>" "install -m 0755 <binary> ${target}" ||',
    ): Exempt(
        "manifest_record stores the asset's source as data in ~/.agents/.installed-manifest.json; it runs nothing"
    ),
    (
        "scripts/update-agent-assets.sh",
        'manifest_record "update_codex_understand_anything" installer "${CODEX_UNDERSTAND_ANYTHING_INSTALLER_COMMIT}" "${HOME}/.understand-anything/repo" "${HOME}/.agents/skills/understand" "${HOME}/.agents/skills/understand-chat" "${HOME}/.agents/skills/understand-dashboard" "${HOME}/.agents/skills/understand-diff" "${HOME}/.agents/skills/understand-domain" "${HOME}/.agents/skills/understand-explain" "${HOME}/.agents/skills/understand-figma" "${HOME}/.agents/skills/understand-knowledge" "${HOME}/.agents/skills/understand-onboard" -- "curl -fsSL ${CODEX_UNDERSTAND_ANYTHING_INSTALLER_URL}" "shasum -a 256 <installer>" "bash <installer> codex" ||',
    ): Exempt(
        "manifest_record stores the asset's source as data in ~/.agents/.installed-manifest.json; it runs nothing"
    ),
    (
        "scripts/update-agent-assets.sh",
        'manifest_record "update_terminal_code" installer "${TERMINAL_CODE_PIN_VERSION}" "${HOME}/.local/lib/tode" "${HOME}/.local/bin/tode" "${HOME}/.local/state/tode/install.json" -- "curl -fsSL ${TERMINAL_CODE_INSTALLER_URL}" "shasum -a 256 <installer>" "bash <installer>" ||',
    ): Exempt(
        "manifest_record stores the asset's source as data in ~/.agents/.installed-manifest.json; it runs nothing"
    ),
    (
        "scripts/update-agent-assets.sh",
        'manifest_record "update_terminal_browser" installer "${TERMINAL_BROWSER_PIN_VERSION}" "${HOME}/.local/share/terminal-browser/app" "${HOME}/.local/bin/terminal-browser" "${HOME}/.local/state/terminal-browser/skills.links" -- "curl -fsSL ${TERMINAL_BROWSER_INSTALLER_URL}" "shasum -a 256 <installer>" "TERMINAL_BROWSER_SKIP_EDITOR_SETUP=1 bash <installer>" ||',
    ): Exempt(
        "manifest_record stores the asset's source as data in ~/.agents/.installed-manifest.json; it runs nothing"
    ),
    (
        "scripts/update-agent-assets.sh",
        'manifest_record "update_pi_claude_bridge" installer "${PI_CLAUDE_BRIDGE_PIN_VERSION}" "${install_dir}" "${install_dir}/RECEIPT" "${install_dir}/node_modules/@anthropic-ai/claude-agent-sdk" -- "curl -fsSL ${PI_CLAUDE_BRIDGE_TARBALL_URL}" "shasum -a 256 <tarball>" "patch -p1 -F0 -d <staging> -i <each home/dot_agents/assets/pi-claude-bridge/patches/*.patch in order>" "bun install --production --omit=peer --frozen-lockfile" "bun run gap-check.ts <staging>/src ${omp_dir}"',
    ): Exempt(
        "manifest_record stores the asset's source as data in ~/.agents/.installed-manifest.json; it runs nothing"
    ),
}
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


def carries(line: str, tool: str, count: int) -> bool:
    """The line carries the tool's canonical options once per occurrence of the tool word, and no other time or
    retry option in any spelling."""
    canonical = CANONICAL[tool]
    return line.count(canonical) >= count and not bound_options(line.replace(canonical, " "))


def continuation_errors(lines: list[str], index: int, entry: Exempt) -> list[str]:
    """What is wrong with the continuation lines of the exempted line at index (0-based)."""
    line = lines[index].strip()
    if not entry.continued:
        return ["continues onto the next line without a checked continuation"] if line.endswith("\\") else []
    if not line.endswith("\\"):
        return [f"the entry names {entry.continued} continuation line(s) but the line does not continue"]
    rest = [raw.strip() for raw in lines[index + 1 : index + 1 + entry.continued]]
    if len(rest) < entry.continued or any(not r.endswith("\\") for r in rest[:-1]) or rest[-1].endswith("\\"):
        return [f"the command does not end after exactly {entry.continued} continuation line(s)"]
    joined = " ".join(rest)
    if entry.options:
        if joined.count(entry.options) != 1:
            return [f"the continuation must carry exactly {entry.options}"]
        joined = joined.replace(entry.options, " ")
    hits = bound_options(joined)
    return [f"the continuation carries {hits}"] if hits else []


def violations(relative: str, text: str, exempt=None, snap_exempt=None) -> list[str]:
    """The lines of one file that break the rule, as `file:line: text`."""
    exempt = EXEMPT if exempt is None else exempt
    snap_exempt = SNAP_EXEMPT if snap_exempt is None else snap_exempt
    lines = text.splitlines()
    bad = []
    for index, raw in enumerate(lines):
        line = raw.strip()
        where = f"{relative}:{index + 1}: {line}"
        tools = TOOL.findall(line)
        if tools:
            entry = exempt.get((relative, line))
            if entry is None:
                if line.endswith("\\"):
                    bad.append(f"{where} (continues onto the next line; put its options on this line or exempt it)")
                elif not all(carries(line, tool, tools.count(tool)) for tool in set(tools)):
                    bad.append(where)
            else:
                bad += [f"{where} ({error})" for error in continuation_errors(lines, index, entry)]
                if entry.call and not entry.options and not all(carries(line, t, tools.count(t)) for t in set(tools)):
                    bad.append(f"{where} (an exempted call must still carry the canonical options)")
        if SNAP.search(line) and SNAP_CANONICAL not in line and (relative, line) not in snap_exempt:
            bad.append(where)
    return bad


def stale(files: dict[str, str], exempt=None, snap_exempt=None) -> list[str]:
    """The exemptions whose file no longer holds their whole line, exactly."""
    exempt = EXEMPT if exempt is None else exempt
    snap_exempt = SNAP_EXEMPT if snap_exempt is None else snap_exempt
    lines = {relative: {line.strip() for line in text.splitlines()} for relative, text in files.items()}
    return [f"{r}: {t}" for r, t in [*exempt, *snap_exempt] if t not in lines.get(r, set())]


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
        # Audits of c7629e24, 86e1f99e and 7b00c8c2: bare calls, substitutions, array values, defaults, zero values in
        # every spelling, and a call that continues onto a line without the tool word.
        canonical = "curl --connect-timeout 30 --speed-limit 1024 --speed-time 60"
        for snippet in (
            "curl https://x.invalid/a",
            "wget https://x.invalid/a",
            'printf "%s\\n" "$(curl -fsSL https://x.invalid/a)"',
            'artifacts=("$(curl https://x.invalid/a)")',
            'y="${x:-$(curl -fsSL https://x.invalid/a)}"',
            "curl --connect-timeout 0 --speed-limit 1024 --speed-time 60 https://x.invalid/a",
            "curl --connect-timeout 30 --speed-limit 0 --speed-time 60 https://x.invalid/a",
            f"{canonical} --max-time 0 https://x.invalid/a",
            f"{canonical} --max-time=0 https://x.invalid/a",
            f"{canonical} -m 0 https://x.invalid/a",
            f"{canonical} -m0 https://x.invalid/a",
            f"{canonical} -y0 -Y0 https://x.invalid/a",
            f"{canonical} -sSy0 https://x.invalid/a",
            f"{canonical} --retry 0 https://x.invalid/a",
            "wget --timeout=0 --tries=0 https://x.invalid/a",
            "wget --timeout=60 --tries=3 --tries=0 https://x.invalid/a",
            "wget --timeout=60 --tries=3 -T 0 https://x.invalid/a",
            "wget --timeout=60 --tries=3 -T0 -t0 https://x.invalid/a",
            "wget --timeout=60 --tries=3 --read-timeout=0 https://x.invalid/a",
            "wget --timeout=60 --tries=3 --time=0 --tri=0 https://x.invalid/a",
            "a=$(curl --connect-timeout 30 --speed-limit 1024 --speed-time 60 u) b=$(curl u)",
            f"{canonical} \\\n  -m0 https://x.invalid/a",
            f"{canonical} \\\n  https://x.invalid/a",
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

    def test_an_exemption_needs_its_exact_line_and_a_checked_continuation(self) -> None:
        probe = {
            ("install/x.sh", "curl \\"): Exempt(
                "x", continued=1, options="--connect-timeout 5 --max-time 15", call=True
            )
        }
        self.assertEqual([], violations("install/x.sh", "curl \\\n  --connect-timeout 5 --max-time 15 u\n", probe, {}))
        for rest in (
            "--connect-timeout 0 --max-time 15 u",
            "--connect-timeout 5 --max-time 15 -m0 u",
            "--connect-timeout 5 --max-time 15 u \\\n  -m0",
            "u",
        ):
            with self.subTest(rest=rest):
                self.assertEqual(1, len(violations("install/x.sh", f"curl \\\n  {rest}\n", probe, {})))
        call = "curl -fsSL --connect-timeout 30 --speed-limit 1024 --speed-time 60 \\"
        continued = {("install/x.sh", call): Exempt("x", continued=1, call=True)}
        self.assertEqual([], violations("install/x.sh", f"{call}\n  -o a u\n", continued, {}))
        self.assertEqual(1, len(violations("install/x.sh", f"{call}\n  -y0 u\n", continued, {})))
        # A mention that continues needs its continuation named, and is checked like a call's.
        mention = {("install/x.sh", "curl \\"): Exempt("a package name")}
        self.assertEqual(1, len(violations("install/x.sh", "curl \\\n  lsb-release\n", mention, {})))
        # The whole line must match: a manifest_record line that gained "$(curl …)" is no longer exempt.
        record = 'manifest_record "x" installer v1 /t -- "curl -fsSL https://x.invalid/a" "shasum -a 256 <a>"'
        table = {("scripts/x.sh", record): Exempt("manifest data")}
        self.assertEqual([], violations("scripts/x.sh", record + "\n", table, {}))
        self.assertEqual(1, len(violations("scripts/x.sh", record + ' "$(curl https://x.invalid/b)"\n', table, {})))
        # A line that changed, even by one character, is no longer exempt, and its entry is stale.
        self.assertEqual(
            1, len(violations("install/x.sh", "curl  lsb\n", {("install/x.sh", "curl lsb"): Exempt("x")}, {}))
        )
        self.assertEqual(
            ["install/x.sh: curl lsb"],
            stale({"install/x.sh": "curl  lsb\n"}, {("install/x.sh", "curl lsb"): Exempt("x")}, {}),
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
        named = (
            "1..2\nrunning: 1 [x] fast\nok 1 [x] fast\nrunning: 2 [x] misc\n"
            "not ok 2 [x] misc # timeout after 2 s (BATS_PER_TEST_TIMEOUT)\n"
        )
        self.assertTrue(out.startswith(named), out)
        # Everything after the named line is the diagnosis, as TAP comments.
        self.assertTrue(all(line.startswith("#") for line in out[len(named) :].splitlines()), out)
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

    def trace_run(self, value: str | None, open_fd: bool = True) -> tuple[subprocess.CompletedProcess[str], bytes]:
        """run_bats with a fake bats that writes to the descriptor BASH_XTRACEFD names, as bashcov's traced shells do;
        the caller holds a pipe on that descriptor and reads what reaches it."""
        self.fake_bats(
            """\
            printf '1..1\\nbegin 1 [x] a\\nok 1 [x] a\\n'
            if [ -n "${BASH_XTRACEFD:-}" ]; then printf 'trace-line\\n' >&"${BASH_XTRACEFD}" || exit 9; fi
            exit 0
            """
        )
        read_end, write_end = os.pipe()
        self.addCleanup(os.close, read_end)
        env = {"PATH": f"{self.temp / 'bin'}:/usr/bin:/bin", "HOME": str(self.temp), "BATS_PER_TEST_TIMEOUT": "30"}
        if value is not None:
            env["BASH_XTRACEFD"] = value.format(fd=write_end)
        result = subprocess.run(
            [BASH, "-c", 'source "$1" && shift && run_bats "$@"', "_", str(RUNNER), "tests/x.bats"],
            env=env, capture_output=True, text=True, timeout=60, check=False,
            pass_fds=(write_end,) if open_fd else (),
        )  # fmt: skip
        os.close(write_end)
        os.set_blocking(read_end, False)
        try:
            received = os.read(read_end, 4096)
        except BlockingIOError:
            received = b""
        return result, received

    def test_the_trace_descriptor_reaches_bats(self) -> None:
        # Audit of 374e62e3: Popen's close_fds dropped bashcov's trace pipe, so coverage was lost and the run passed.
        result, received = self.trace_run("{fd}")
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertEqual(b"trace-line\n", received)

    def test_no_trace_descriptor_works_as_before(self) -> None:
        result, received = self.trace_run(None)
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertEqual(b"", received)

    def test_a_trace_descriptor_that_is_not_open_fails_loudly(self) -> None:
        # 200 is not open in the wrapper (nothing passes it); a non-number is no descriptor at all.
        for value, message in (("200", "is not an open descriptor"), ("x", "is not a descriptor number")):
            with self.subTest(value=value):
                result, _ = self.trace_run(value, open_fd=False)
                self.assertEqual(1, result.returncode, result.stdout + result.stderr)
                self.assertIn(message, result.stderr)
                self.assertFalse((self.temp / "args").exists(), "Bats ran")

    def test_a_timed_out_test_is_diagnosed_with_the_command_it_stalled_in(self) -> None:
        # The PR #570 and #571 stalls ended with only the test's name; the diagnosis names the stalled process.
        probe = self.temp / "bin/stall-probe"
        probe.write_text('#!/bin/sh\necho $$ >> "${PIDS}"\nsleep 300\n')
        probe.chmod(0o755)
        self.fake_bats(
            """\
            printf '1..1\\nbegin 1 [x] misc\\n'
            echo $$ >> "${PIDS}"
            stall-probe --waiting-on dpkg
            """
        )
        status, out, err, elapsed = self.run_bats("2", "tests/x.bats")
        self.assertEqual(124, status, out + err)
        self.assertLess(elapsed, 4 + 10)  # the bound, 2 s of slack, and at most PS_TIMEOUT for the listing
        after = out[out.index("not ok 1 [x] misc # timeout after 2 s") :]
        self.assertIn("# diagnosis: the processes under Bats (pid, elapsed, state, wchan, command)", after)
        probe_line = next(line for line in after.splitlines() if "stall-probe" in line)
        self.assertIn("--waiting-on dpkg", probe_line)
        self.assertTrue(any("sleep 300" in line for line in after.splitlines()), after)

    def test_a_failed_or_hung_ps_leaves_the_timeout_exit(self) -> None:
        for body, reason in (("exit 3", "ps exited 3"), ("exec sleep 60", "timed out after 10 seconds")):
            with self.subTest(ps=body):
                (self.temp / "bin/ps").write_text(f"#!/bin/sh\n{body}\n")
                (self.temp / "bin/ps").chmod(0o755)
                self.fake_bats("printf '1..1\\nbegin 1 [x] misc\\n'\necho $$ >> \"${PIDS}\"\nsleep 300\n")
                status, out, err, _ = self.run_bats("2", "tests/x.bats")
                self.assertEqual(124, status, out + err)
                self.assertIn("not ok 1 [x] misc # timeout after 2 s", out)
                line = next(line for line in out.splitlines() if line.startswith("# diagnosis unavailable: "))
                self.assertIn(reason, line)

    def test_the_wrapper_signals_nothing(self) -> None:
        # Stopping processes is the step's timeout-minutes and the runner's job, not this wrapper's; its one `ps`
        # call only lists them.
        text = WRAPPER.read_text()
        for api in (r"import signal", r"os\.kill", r"killpg", r"setsid", r"start_new_session", r"\bkill\b"):
            with self.subTest(api=api):
                self.assertNotRegex(text, api)
        self.assertEqual(1, text.count('["ps", '))
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

    def test_a_failed_dirname_stops_run_bats_before_python_runs(self) -> None:
        # Audit of 7b00c8c2: the guard on `here="$(dirname …)"`; without it python3 would run "/ci/run-bats.py".
        temp = Path(tempfile.mkdtemp(prefix="run-bats-dirname-"))
        self.addCleanup(shutil.rmtree, temp, True)
        (temp / "bin").mkdir()
        marker = temp / "python-ran"
        (temp / "bin/python3").write_text(f'#!/bin/sh\ntouch "{marker}"\nexit 0\n')
        (temp / "bin/python3").chmod(0o755)
        # The runner sets -e when sourced, so the status is caught with `||`.
        script = 'source "$1" && dirname() { return 23; } && { run_bats x || echo "status=$?"; }'
        result = subprocess.run(
            [BASH, "-c", script, "_", str(RUNNER)],
            env={"PATH": f"{temp / 'bin'}:/usr/bin:/bin", "HOME": str(temp)},
            capture_output=True, text=True, timeout=30, check=False,
        )  # fmt: skip
        self.assertEqual("status=1\n", result.stdout, result.stderr)
        self.assertFalse(marker.exists())

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
                # Above one per-test bound (scripts/ci/run-bats.py's DEFAULT_BOUND), so the stalled test is named first.
                bound = int(re.search(r"^DEFAULT_BOUND = ([0-9]+)$", WRAPPER.read_text(), re.MULTILINE).group(1))
                if not match or int(match.group(1)) * 60 <= bound:
                    missing.append(f"{workflow.name}: {step.splitlines()[0].strip()}")
        self.assertEqual([], missing)
        self.assertEqual(3, found)


if __name__ == "__main__":
    unittest.main()
