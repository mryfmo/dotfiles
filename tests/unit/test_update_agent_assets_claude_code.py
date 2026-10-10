#!/usr/bin/env python3
"""Exercise ensure_claude_code in update-agent-assets.sh against a fake Anthropic release server."""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import tempfile
import textwrap
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
UPDATER = ROOT / "scripts/update-agent-assets.sh"
FINGERPRINT = "31DDDE24DDFAB679F42D7BD2BAA929FF1A7ECACE"
VERSION = "2.1.287"
PLATFORMS = ("darwin-arm64", "darwin-x64", "linux-arm64", "linux-arm64-musl", "linux-x64", "linux-x64-musl")
# The downloaded binary: its own install step creates the native layout, as Anthropic's binary does.
BINARY = textwrap.dedent(
    """\
    #!/bin/bash
    printf 'binary %s\\n' "$*" >> "$TEST_LOG"
    if [ "$1" = install ]; then
        mkdir -p "$HOME/.local/share/claude/versions" "$HOME/.local/bin"
        cp "$0" "$HOME/.local/share/claude/versions/$2"
        [ -z "${TAMPER_ON_INSTALL:-}" ] || printf 'tampered\\n' >> "$HOME/.local/share/claude/versions/$2"
        ln -sfn "$HOME/.local/share/claude/versions/$2" "$HOME/.local/bin/claude"
        [ -z "${FAIL_AFTER_LAUNCHER:-}" ] || exit 1
        if [ -n "${OTHER_VERSION:-}" ]; then
            cp "$0" "$HOME/.local/share/claude/versions/${OTHER_VERSION}"
            ln -sfn "$HOME/.local/share/claude/versions/${OTHER_VERSION}" "$HOME/.local/bin/claude"
        fi
    fi
    """
)


class EnsureClaudeCodeTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = Path(tempfile.mkdtemp(prefix="claude-code-test-"))
        self.home = self.temp / "home"
        self.bin = self.temp / "bin"
        self.served = self.temp / "served"
        self.log = self.temp / "calls.log"
        self.bin.mkdir()
        jq = shutil.which("jq")
        self.assertIsNotNone(jq, "jq is required for ensure_claude_code tests")
        (self.bin / "jq").symlink_to(jq)
        (self.home / ".claude").mkdir(parents=True)
        (self.home / ".claude/settings.json").write_text(json.dumps({"autoUpdatesChannel": "stable"}))
        key = self.home / ".local/share/claude-code-keys/claude-code.asc"
        key.parent.mkdir(parents=True)
        key.write_text("fake release key\n")
        self.serve("claude-code-releases/stable", f"{VERSION}\n")
        self.serve(f"claude-code-releases/{VERSION}/manifest.json.sig", "GOOD\n")
        for platform in PLATFORMS:
            self.serve(f"claude-code-releases/{VERSION}/{platform}/claude", BINARY)
        self.write_manifest(VERSION, hashlib.sha256(BINARY.encode()).hexdigest())
        self.fake(
            "curl",
            """
            out=""
            while [ "$#" -gt 0 ]; do
                case "$1" in
                -o) out="$2"; shift 2 ;;
                -*) shift ;;
                *) url="$1"; shift ;;
                esac
            done
            printf 'curl %s\\n' "${url}" >> "$TEST_LOG"
            [ -z "${OFFLINE:-}" ] || exit 6
            file="$SERVED/${url#https://downloads.claude.ai/}"
            [ -f "${file}" ] || exit 22
            if [ -n "${out}" ]; then cp "${file}" "${out}"; else cat "${file}"; fi
            """,
        )
        self.fake(
            "gpg",
            """
            printf 'gpg %s\\n' "$*" >> "$TEST_LOG"
            case "$*" in
            *show-only*) printf 'pub:-:4096:1:BAA929FF1A7ECACE:1700000000::::::scESC:\\nfpr:::::::::%s:\\n' "${KEY_FPR}" ;;
            *--dearmor*)
                while [ "$1" != --output ]; do shift; done
                cp "${@: -1}" "$2"
                ;;
            esac
            """,
        )
        self.fake(
            "gpgv",
            """
            printf 'gpgv %s\\n' "$*" >> "$TEST_LOG"
            [ "$(cat "${@: -2:1}")" = GOOD ]
            """,
        )
        self.fake(
            "mise",
            """
            printf 'mise %s\\n' "$*" >> "$TEST_LOG"
            case "$1" in
            ls) [ -z "${OLD_MISE:-}" ] || printf 'npm:@anthropic-ai/claude-code  2.1.292\\n' ;;
            esac
            """,
        )

    def tearDown(self) -> None:
        shutil.rmtree(self.temp)

    def fake(self, name: str, body: str) -> None:
        path = self.bin / name
        path.write_text("#!/bin/bash\n" + textwrap.dedent(body))
        path.chmod(0o755)

    def serve(self, relative: str, content: str) -> None:
        path = self.served / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)

    def write_manifest(self, version: str, checksum: str) -> None:
        platforms = {platform: {"binary": "claude", "checksum": checksum, "size": 1} for platform in PLATFORMS}
        self.serve(
            f"claude-code-releases/{VERSION}/manifest.json",
            json.dumps({"version": version, "platforms": platforms}),
        )

    def install_active(self, content: str = BINARY) -> Path:
        binary = self.home / f".local/share/claude/versions/{VERSION}"
        binary.parent.mkdir(parents=True, exist_ok=True)
        binary.write_text(content)
        binary.chmod(0o755)
        (self.home / ".local/bin").mkdir(parents=True, exist_ok=True)
        (self.home / ".local/bin/claude").symlink_to(binary)
        return binary

    def run_ensure(self, path: str | None = None, **extra: str) -> subprocess.CompletedProcess[str]:
        env = {
            "HOME": str(self.home),
            "PATH": path or f"{self.bin}:/usr/bin:/bin",
            "SERVED": str(self.served),
            "TEST_LOG": str(self.log),
            "KEY_FPR": FINGERPRINT,
            **extra,
        }
        if "TMPDIR" in os.environ:
            env["TMPDIR"] = os.environ["TMPDIR"]
        return subprocess.run(
            ["bash", "-c", 'source "$1"; ensure_claude_code', "_", str(UPDATER)],
            env=env,
            text=True,
            capture_output=True,
            check=False,
        )

    def calls(self) -> list[str]:
        return self.log.read_text().splitlines() if self.log.exists() else []

    def manifest_steps(self) -> dict:
        path = self.home / ".agents/.installed-manifest.json"
        return json.loads(path.read_text())["steps"] if path.exists() else {}

    def test_fresh_install_runs_the_binary_only_after_the_signature_and_sha256_verify(self) -> None:
        result = self.run_ensure(OLD_MISE="1")

        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        calls = self.calls()
        verify = next(index for index, call in enumerate(calls) if call.startswith("gpgv "))
        self.assertLess(verify, calls.index(f"binary install {VERSION}"))
        # Only the pinned key can validate: gpgv reads the scratch homedir, never the user's keyrings.
        self.assertRegex(calls[verify], r"^gpgv --homedir \S+/gnupg --keyring \S+/claude-code-keyring\.gpg ")
        self.assertIn(f"curl https://downloads.claude.ai/claude-code-releases/{VERSION}/manifest.json.sig", calls)
        launcher = self.home / ".local/bin/claude"
        self.assertEqual(f"{VERSION}", os.readlink(launcher).rsplit("/", 1)[1])
        retire = calls.index("mise uninstall --all npm:@anthropic-ai/claude-code")
        self.assertEqual("mise reshim", calls[retire + 1])
        step = self.manifest_steps()["ensure_claude_code"]
        self.assertEqual(VERSION, step["source_version"])
        self.assertEqual([str(launcher), str(self.home / ".local/share/claude")], step["paths"])

    def test_a_bad_manifest_signature_installs_and_runs_nothing(self) -> None:
        self.serve(f"claude-code-releases/{VERSION}/manifest.json.sig", "FORGED\n")

        result = self.run_ensure()

        self.assertEqual(1, result.returncode, result.stdout + result.stderr)
        self.assertIn(f"The signature on the Claude Code {VERSION} release manifest did not verify.", result.stderr)
        self.assertFalse([call for call in self.calls() if call.startswith("binary ")])
        self.assertFalse((self.home / ".local/bin/claude").exists())
        self.assertNotIn("ensure_claude_code", self.manifest_steps())

    def test_a_key_with_another_fingerprint_is_refused_before_gpgv(self) -> None:
        result = self.run_ensure(KEY_FPR="0" * 40)

        self.assertEqual(1, result.returncode, result.stdout + result.stderr)
        self.assertIn("Claude Code release key validation failed.", result.stderr)
        self.assertFalse([call for call in self.calls() if call.startswith(("gpgv ", "binary "))])

    def test_a_binary_that_does_not_match_the_signed_sha256_never_runs(self) -> None:
        self.write_manifest(VERSION, "0" * 64)

        result = self.run_ensure()

        self.assertEqual(1, result.returncode, result.stdout + result.stderr)
        self.assertIn(f"Claude Code {VERSION} does not match its signed manifest; nothing ran.", result.stderr)
        self.assertFalse([call for call in self.calls() if call.startswith("binary ")])

    def test_a_signed_manifest_of_another_release_cannot_stand_in(self) -> None:
        self.write_manifest("2.1.200", hashlib.sha256(BINARY.encode()).hexdigest())

        result = self.run_ensure()

        self.assertEqual(1, result.returncode, result.stdout + result.stderr)
        self.assertIn(f"The signed Claude Code {VERSION} manifest lists no sha256", result.stderr)
        self.assertFalse([call for call in self.calls() if call.startswith("binary ")])

    def test_an_installed_binary_that_fails_the_check_is_removed(self) -> None:
        result = self.run_ensure(TAMPER_ON_INSTALL="1")

        self.assertEqual(1, result.returncode, result.stdout + result.stderr)
        self.assertIn(
            f"Claude Code {VERSION} does not match its signed release manifest; its version and launcher were removed",
            result.stderr,
        )
        self.assertFalse((self.home / f".local/share/claude/versions/{VERSION}").exists())
        self.assertFalse((self.home / ".local/bin/claude").is_symlink())
        self.assertNotIn("ensure_claude_code", self.manifest_steps())

    def test_an_active_native_install_is_re_verified_without_downloading_the_binary(self) -> None:
        self.install_active()

        result = self.run_ensure()

        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        calls = self.calls()
        self.assertIn(f"curl https://downloads.claude.ai/claude-code-releases/{VERSION}/manifest.json", calls)
        self.assertFalse([call for call in calls if call.endswith("/claude") or call.startswith("binary ")])
        self.assertNotIn("curl https://downloads.claude.ai/claude-code-releases/stable", calls)
        self.assertIn("ensure_claude_code", self.manifest_steps())

    def test_a_tampered_active_binary_fails_and_cannot_run_again(self) -> None:
        binary = self.install_active(BINARY + "# tampered\n")

        result = self.run_ensure()

        self.assertEqual(1, result.returncode, result.stdout + result.stderr)
        self.assertIn(f"Claude Code {VERSION} does not match its signed release manifest", result.stderr)
        self.assertFalse(binary.exists())
        self.assertFalse(os.path.lexists(self.home / ".local/bin/claude"))

    def test_a_launcher_left_at_another_version_removes_both(self) -> None:
        result = self.run_ensure(OTHER_VERSION="2.1.296")

        self.assertEqual(1, result.returncode, result.stdout + result.stderr)
        self.assertIn(f"claude install {VERSION} left the launcher at 2.1.296", result.stderr)
        versions = self.home / ".local/share/claude/versions"
        self.assertEqual([], sorted(path.name for path in versions.iterdir()))
        self.assertFalse(os.path.lexists(self.home / ".local/bin/claude"))

    def test_a_failed_install_step_leaves_no_launcher_or_version(self) -> None:
        result = self.run_ensure(FAIL_AFTER_LAUNCHER="1")

        self.assertEqual(1, result.returncode, result.stdout + result.stderr)
        self.assertIn(f"binary install {VERSION}", self.calls())
        self.assertFalse((self.home / f".local/share/claude/versions/{VERSION}").exists())
        self.assertFalse(os.path.lexists(self.home / ".local/bin/claude"))
        self.assertNotIn("ensure_claude_code", self.manifest_steps())

    def test_offline_keeps_what_is_there_and_installs_nothing(self) -> None:
        result = self.run_ensure(OFFLINE="1")
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn("nothing was installed", result.stderr)
        self.assertFalse((self.home / ".local/bin/claude").exists())

        binary = self.install_active()
        result = self.run_ensure(OFFLINE="1")
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn(f"could not re-verify Claude Code {VERSION}", result.stderr)
        self.assertTrue(binary.exists())

    def test_without_gpg_nothing_is_installed(self) -> None:
        system = self.temp / "system-bin"
        system.mkdir()
        for directory in ("/usr/bin", "/bin"):
            for entry in os.scandir(directory):
                if entry.name not in {"gpg", "gpgv", "curl", "jq"} and not os.path.lexists(system / entry.name):
                    (system / entry.name).symlink_to(entry.path)
        (self.bin / "gpg").unlink()
        (self.bin / "gpgv").unlink()

        result = self.run_ensure(path=f"{self.bin}:{system}")

        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn("it needs curl, gpg, gpgv, jq and shasum", result.stderr)
        self.assertFalse([call for call in self.calls() if call.startswith("binary ")])

    def test_the_old_mise_install_is_found_by_its_directory_when_mise_does_not_list_it(self) -> None:
        old = self.temp / "mise-data/installs/npm-anthropic-ai-claude-code/2.1.292"
        old.mkdir(parents=True)

        result = self.run_ensure(MISE_DATA_DIR=str(self.temp / "mise-data"))

        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn("mise uninstall --all npm:@anthropic-ai/claude-code", self.calls())

        self.log.unlink()
        shutil.rmtree(self.temp / "mise-data")
        result = self.run_ensure(MISE_DATA_DIR=str(self.temp / "mise-data"))

        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertFalse([call for call in self.calls() if call.startswith("mise uninstall")])

    def test_a_recorded_mise_repair_keeps_the_old_install_and_names_the_remedy(self) -> None:
        manifest = self.home / ".agents/.installed-manifest.json"
        manifest.parent.mkdir(parents=True)
        manifest.write_text(json.dumps({"version": 1, "steps": {"ensure_mise_npm_agent_cli:claude": {"paths": []}}}))

        result = self.run_ensure(OLD_MISE="1")

        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn("remove-agent-asset ensure_mise_npm_agent_cli:claude --yes", result.stdout)
        self.assertFalse([call for call in self.calls() if call.startswith("mise uninstall")])

    def test_without_a_channel_setting_nothing_is_installed(self) -> None:
        (self.home / ".claude/settings.json").write_text("{}")

        result = self.run_ensure()

        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn("no autoUpdatesChannel (stable or latest) could be read", result.stderr)
        self.assertEqual([], self.calls())


if __name__ == "__main__":
    unittest.main()
