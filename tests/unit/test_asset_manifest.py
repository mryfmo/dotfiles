#!/usr/bin/env python3
"""Verify agent asset install manifest recording."""

from __future__ import annotations

import json
import os
import shutil
import stat
import subprocess
import tempfile
import textwrap
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
LIBRARY = ROOT / "scripts/lib/asset-manifest.sh"
UPDATER = ROOT / "scripts/update-agent-assets.sh"


class AssetManifestTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = Path(tempfile.mkdtemp(prefix="asset-manifest-test-"))
        self.home = self.temp_dir / "home"
        self.home.mkdir()

    def tearDown(self) -> None:
        shutil.rmtree(self.temp_dir)

    def run_bash(
        self, script: str, *, env: dict[str, str] | None = None
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["bash", "-c", script],
            cwd=ROOT,
            env={**os.environ, "HOME": str(self.home), **(env or {})},
            text=True,
            capture_output=True,
            check=False,
        )

    def manifest(self) -> dict[str, object]:
        return json.loads(
            (self.home / ".agents/.installed-manifest.json").read_text()
        )

    def test_records_schema_two_steps_and_replaces_one_whole_entry(self) -> None:
        result = self.run_bash(
            f"""
            source {LIBRARY}
            manifest_record first plugin 1.0 "$HOME/old path" -- "tool install first"
            manifest_record second rsync 2.0 "$HOME/second" -- "rsync source destination"
            manifest_record first plugin 1.1 "$HOME/new path" -- "tool update first"
            """
        )

        self.assertEqual(0, result.returncode, result.stderr)
        data = self.manifest()
        self.assertEqual(1, data["version"])
        self.assertEqual({"first", "second"}, set(data["steps"]))
        first = data["steps"]["first"]
        self.assertEqual("plugin", first["kind"])
        self.assertEqual("1.1", first["source_version"])
        self.assertEqual([str(self.home / "new path")], first["paths"])
        self.assertEqual(["tool update first"], first["commands"])
        self.assertRegex(
            first["installed_at"], r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$"
        )
        mode = stat.S_IMODE(
            (self.home / ".agents/.installed-manifest.json").stat().st_mode
        )
        self.assertEqual(0o600, mode)

    def test_failed_atomic_commit_leaves_previous_manifest_intact(self) -> None:
        seed = self.run_bash(
            f"source {LIBRARY}; manifest_record stable plugin 1 \"$HOME/stable\""
        )
        self.assertEqual(0, seed.returncode, seed.stderr)
        before = self.manifest()

        result = self.run_bash(
            f"""
            source {LIBRARY}
            mv() {{ return 1; }}
            manifest_record stable plugin 2 "$HOME/replacement"
            """
        )

        self.assertEqual(0, result.returncode)
        self.assertEqual(
            ["warning: failed to record asset manifest step stable"],
            result.stderr.splitlines(),
        )
        self.assertEqual(before, self.manifest())

    def test_unwritable_destination_warns_once_without_failing(self) -> None:
        (self.home / ".agents").write_text("not a directory")

        result = self.run_bash(
            f"source {LIBRARY}; manifest_record broken plugin unknown \"$HOME/path\""
        )

        self.assertEqual(0, result.returncode)
        self.assertEqual(
            ["warning: failed to record asset manifest step broken"],
            result.stderr.splitlines(),
        )

    def test_two_real_install_steps_record_under_fake_home(self) -> None:
        bin_dir = self.temp_dir / "bin"
        bin_dir.mkdir()
        jq = shutil.which("jq")
        self.assertIsNotNone(jq, "jq is required for asset manifest tests")
        (bin_dir / "jq").symlink_to(jq)
        log = self.temp_dir / "commands.log"
        self._executable(
            bin_dir / "rsync", 'printf "rsync %s\\n" "$*" >> "$TEST_LOG"\n'
        )
        self._executable(
            bin_dir / "herdr",
            """
            if [[ "$1" == "--version" ]]; then
                printf 'herdr 9.9.9\n'
            else
                printf 'herdr %s\n' "$*" >> "$TEST_LOG"
            fi
            """,
        )

        result = self.run_bash(
            f"""
            source {UPDATER}
            update_compactiondb
            ensure_herdr_integrations
            """,
            env={
                "PATH": f"{bin_dir}:/usr/bin:/bin",
                "TEST_LOG": str(log),
            },
        )

        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        data = self.manifest()
        self.assertEqual(
            {"update_compactiondb", "ensure_herdr_integrations"},
            set(data["steps"]),
        )
        self.assertEqual("2.0.0+dotfiles.5", data["steps"]["update_compactiondb"]["source_version"])
        self.assertEqual("9.9.9", data["steps"]["ensure_herdr_integrations"]["source_version"])
        self.assertEqual(
            [
                "herdr integration install claude",
                "herdr integration install codex",
            ],
            data["steps"]["ensure_herdr_integrations"]["commands"],
        )

    def test_same_run_mise_repairs_preserve_both_identity_steps(self) -> None:
        bin_dir = self.temp_dir / "bin"
        bin_dir.mkdir()
        jq = shutil.which("jq")
        self.assertIsNotNone(jq, "jq is required for asset manifest tests")
        (bin_dir / "jq").symlink_to(jq)
        state = self.temp_dir / "state"
        state.mkdir()
        for cli in ("claude", "codex"):
            self._executable(
                bin_dir / cli,
                f"""
                if [[ -f "$TEST_STATE/{cli}" ]]; then
                    printf '{cli} 1.0.0\n'
                    exit 0
                fi
                exit 1
                """,
            )
        self._executable(
            bin_dir / "mise",
            """
            case "$1" in
            install)
                case "$*" in
                *claude-code) touch "$TEST_STATE/claude" ;;
                *openai/codex) touch "$TEST_STATE/codex" ;;
                esac
                ;;
            where)
                printf '%s/install/%s\n' "$HOME" "$2"
                ;;
            esac
            """,
        )

        result = self.run_bash(
            f"""
            source {UPDATER}
            ensure_mise_npm_agent_cli claude npm:@anthropic-ai/claude-code
            ensure_mise_npm_agent_cli codex npm:@openai/codex
            """,
            env={
                "PATH": f"{bin_dir}:/usr/bin:/bin",
                "TEST_STATE": str(state),
            },
        )

        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertEqual(
            {
                "ensure_mise_npm_agent_cli:claude",
                "ensure_mise_npm_agent_cli:codex",
            },
            set(self.manifest()["steps"]),
        )

    def test_updater_has_one_recording_call_for_each_install_step(self) -> None:
        updater = UPDATER.read_text()
        steps = (
            "ensure_herdr_integrations",
            "update_claude_superpowers",
            "update_claude_crit",
            "update_claude_ponytail",
            "update_claude_understand_anything",
            "update_codex_superpowers",
            "update_codex_crit",
            "update_codex_ponytail",
            "update_codex_understand_anything",
            "update_compactiondb",
        )

        self.assertEqual(11, updater.count('manifest_record "'))
        self.assertEqual(
            1,
            updater.count('manifest_record "ensure_mise_npm_agent_cli:${cli}"'),
        )
        for step in steps:
            self.assertEqual(1, updater.count(f'manifest_record "{step}"'), step)

    def test_chezmoi_rendered_updater_uses_inlined_manifest_library(self) -> None:
        rendered = self.temp_dir / "06-install-agent-assets.sh"
        rendered.write_text(LIBRARY.read_text() + UPDATER.read_text())

        syntax = subprocess.run(
            ["bash", "-n", str(rendered)],
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(0, syntax.returncode, syntax.stderr)

        result = self.run_bash(
            f'source {rendered}; manifest_record rendered plugin 1 "$HOME/rendered" -- "render install"'
        )

        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual("1", self.manifest()["steps"]["rendered"]["source_version"])

    @staticmethod
    def _executable(path: Path, body: str) -> None:
        path.write_text("#!/usr/bin/env bash\n" + textwrap.dedent(body))
        path.chmod(0o755)


if __name__ == "__main__":
    unittest.main()
