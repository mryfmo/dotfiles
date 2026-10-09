#!/usr/bin/env python3
"""Verify truthful runtime artifact, doctor, and upgrade behavior."""

from __future__ import annotations

import json
import os
import re
import shutil
import stat
import subprocess
import tempfile
import textwrap
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


class RuntimeHealthTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = Path(tempfile.mkdtemp(prefix="runtime-health-test-"))

    def tearDown(self) -> None:
        shutil.rmtree(self.temp_dir)

    def executable(self, path: Path, body: str) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("#!/bin/bash\n" + textwrap.dedent(body))
        path.chmod(0o755)

    @staticmethod
    def run_test_command(
        command: list[str],
        *,
        cwd: Path | None = None,
        env: dict[str, str] | None = None,
        check: bool = False,
    ) -> subprocess.CompletedProcess[str]:
        """Run a fixed test command whose dynamic arguments come only from its fixture."""
        return subprocess.run(
            command,
            cwd=cwd,
            env=env,
            text=True,
            capture_output=True,
            check=check,
        )

    def test_client_bashrc_treats_private_sources_as_optional(self) -> None:
        home = self.temp_dir / "bashrc-home"
        server = home / ".local/bin/server"
        common = home / ".local/bin/common"
        server.mkdir(parents=True)
        common.mkdir(parents=True)
        for path in (
            common / "dev",
            common / "git-delete-merged-branches",
        ):
            path.write_text(":\n")

        command = [
            "bash",
            "--noprofile",
            "--rcfile",
            str(ROOT / "home/dot_bash/client/bashrc"),
            "-i",
            "-c",
            "true",
        ]
        env = {**os.environ, "HOME": str(home), "TERM": "dumb"}

        public_only = self.run_test_command(command, env=env)

        self.assertEqual(0, public_only.returncode)
        self.assertNotIn("prompt.sh", public_only.stderr)
        self.assertNotIn("aliases.sh", public_only.stderr)

        (server / "prompt.sh").write_text("printf 'private-prompt\\n'\n")
        (server / "aliases.sh").write_text("printf 'private-aliases\\n'\n")

        with_private = self.run_test_command(command, env=env)

        self.assertEqual(0, with_private.returncode)
        self.assertIn("private-prompt", with_private.stdout)
        self.assertIn("private-aliases", with_private.stdout)

    def test_agent_asset_update_runs_gh_extension_ensure(self) -> None:
        result = self.run_test_command(
            [
                "bash",
                "-c",
                textwrap.dedent(
                    """
                    source "$1"
                    remove_node_global_agent_cli_shadows() { :; }
                    ensure_mise_npm_agent_cli() { :; }
                    update_claude_superpowers() { :; }
                    update_claude_crit() { :; }
                    update_claude_ponytail() { :; }
                    update_claude_understand_anything() { :; }
                    update_codex_superpowers() { :; }
                    update_codex_crit() { :; }
                    update_codex_ponytail() { :; }
                    update_codex_understand_anything() { :; }
                    update_terminal_code() { :; }
                    update_terminal_browser() { :; }
                    update_compactiondb() { :; }
                    update_agmsg() { :; }
                    ensure_herdr_integrations() { :; }
                    ensure_gh_extensions() { printf 'gh-extensions-ensured\\n'; }
                    main
                    """
                ),
                "_",
                str(ROOT / "scripts/update-agent-assets.sh"),
            ],
            env={**os.environ, "HOME": str(self.temp_dir)},
        )

        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertEqual("gh-extensions-ensured\n", result.stdout)

    def test_agent_asset_update_removes_node_global_shadows_before_agent_commands(
        self,
    ) -> None:
        repo = self.temp_dir / "agent-assets-repo"
        home = self.temp_dir / "agent-assets-home"
        bin_dir = repo / "bin"
        (repo / "scripts").mkdir(parents=True)
        (repo / "install/common").mkdir(parents=True)
        home.mkdir()
        shutil.copy(
            ROOT / "scripts/update-agent-assets.sh",
            repo / "scripts/update-agent-assets.sh",
        )
        (repo / "scripts/lib").mkdir()
        shutil.copy(
            ROOT / "scripts/lib/asset-manifest.sh",
            repo / "scripts/lib/asset-manifest.sh",
        )
        shutil.copy(
            ROOT / "scripts/lib/installer-pins.sh",
            repo / "scripts/lib/installer-pins.sh",
        )
        shutil.copy(
            ROOT / "install/common/gh_extensions.sh",
            repo / "install/common/gh_extensions.sh",
        )
        (repo / "vendor/compactiondb").mkdir(parents=True)
        (repo / "vendor/compactiondb/CHANGELOG.md").write_text("## 2.0.0+dotfiles.5\n")
        # Keep the run hermetic: downloads fail fast instead of hitting the network.
        self.executable(bin_dir / "curl", "exit 1\n")
        self.executable(
            bin_dir / "npm",
            """
            printf 'npm %s\n' "$*" >> "$TEST_LOG"
            """,
        )
        for command in ("claude", "codex"):
            self.executable(
                bin_dir / command,
                f"""
                printf '{command} %s\\n' "$*" >> "$TEST_LOG"
                """,
            )
        log = repo / "commands.log"

        result = self.run_test_command(
            ["bash", "scripts/update-agent-assets.sh"],
            cwd=repo,
            env={
                **os.environ,
                "HOME": str(home),
                "PATH": f"{bin_dir}:/usr/bin:/bin",
                "TEST_LOG": str(log),
            },
        )

        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        calls = log.read_text().splitlines()
        first_agent_call = min(i for i, call in enumerate(calls) if call.startswith(("claude ", "codex ")))
        self.assertLess(calls.index("npm uninstall -g @openai/codex"), first_agent_call)
        self.assertLess(calls.index("npm uninstall -g @anthropic-ai/claude-code"), first_agent_call)

    def test_agent_asset_update_repairs_broken_claude_with_npm_backend(self) -> None:
        repo = self.temp_dir / "agent-assets-repair-repo"
        home = self.temp_dir / "agent-assets-repair-home"
        bin_dir = home / ".local/bin"
        shim_dir = home / ".local/share/mise/shims"
        (repo / "scripts").mkdir(parents=True)
        (repo / "install/common").mkdir(parents=True)
        home.mkdir()
        shutil.copy(
            ROOT / "scripts/update-agent-assets.sh",
            repo / "scripts/update-agent-assets.sh",
        )
        (repo / "scripts/lib").mkdir()
        shutil.copy(
            ROOT / "scripts/lib/asset-manifest.sh",
            repo / "scripts/lib/asset-manifest.sh",
        )
        shutil.copy(
            ROOT / "scripts/lib/installer-pins.sh",
            repo / "scripts/lib/installer-pins.sh",
        )
        shutil.copy(
            ROOT / "install/common/gh_extensions.sh",
            repo / "install/common/gh_extensions.sh",
        )
        (repo / "vendor/compactiondb").mkdir(parents=True)
        (repo / "vendor/compactiondb/CHANGELOG.md").write_text("## 2.0.0+dotfiles.5\n")
        # Keep the run hermetic: downloads fail fast instead of hitting the network.
        self.executable(bin_dir / "curl", "exit 1\n")
        self.executable(bin_dir / "npm", "exit 1\n")
        self.executable(
            shim_dir / "claude",
            """
            printf 'broken-claude %s\n' "$*" >> "$TEST_LOG"
            exit 99
            """,
        )
        self.executable(
            shim_dir / "codex",
            """
            printf 'codex %s\n' "$*" >> "$TEST_LOG"
            """,
        )
        self.executable(
            bin_dir / "mise",
            """
            printf 'mise %s %s %s\n' \
                "${MISE_NPM_PACKAGE_MANAGER:-}" \
                "${npm_config_min_release_age:-}" \
                "$*" >> "$TEST_LOG"
            if [ "$*" = "install --force npm:@anthropic-ai/claude-code" ]; then
                cat > "$BROKEN_CLAUDE" <<'EOF'
#!/bin/bash
printf 'claude %s\n' "$*" >> "$TEST_LOG"
EOF
                chmod +x "$BROKEN_CLAUDE"
            fi
            """,
        )
        log = repo / "commands.log"

        result = self.run_test_command(
            ["bash", "scripts/update-agent-assets.sh"],
            cwd=repo,
            env={
                **os.environ,
                "BROKEN_CLAUDE": str(shim_dir / "claude"),
                "HOME": str(home),
                "PATH": f"{bin_dir}:/usr/bin:/bin",
                "TEST_LOG": str(log),
            },
        )

        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        calls = log.read_text().splitlines()
        repair = "mise npm 0 install --force npm:@anthropic-ai/claude-code"
        self.assertIn(repair, calls)
        self.assertFalse(any(call.endswith("npm:@openai/codex") and call.startswith("mise ") for call in calls))
        self.assertLess(calls.index(repair), calls.index("claude plugin marketplace list"))

    def test_codex_superpowers_reports_login_step_when_curated_catalog_is_missing(
        self,
    ) -> None:
        result = self.run_test_command(
            [
                "bash",
                "-c",
                textwrap.dedent(
                    """
                    source "$1"
                    has_command() { return 0; }
                    command_output_contains() { return 1; }
                    codex() {
                        if [ "$*" = "plugin add superpowers@openai-curated" ]; then
                            printf 'Error: plugin superpowers@openai-curated was not found\n' >&2
                            return 1
                        fi
                    }
                    manifest_codex_plugin_version() { printf 'unknown\n'; }
                    manifest_record() { :; }
                    update_codex_superpowers
                    """
                ),
                "_",
                str(ROOT / "scripts/update-agent-assets.sh"),
            ],
            env={**os.environ, "HOME": str(self.temp_dir)},
        )

        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn(
            "Codex Superpowers was not installed: the OpenAI-curated catalog is unavailable.",
            result.stdout,
        )
        self.assertIn(
            "Run `codex login`, then `codex plugin add superpowers@openai-curated`.",
            result.stdout,
        )
        self.assertNotIn("Error:", result.stdout + result.stderr)

    def test_codex_crit_normalizes_managed_marketplace_mode(self) -> None:
        home = self.temp_dir / "codex-crit-home"
        marketplace = home / ".agents/plugins/marketplace.json"
        result = self.run_test_command(
            [
                "bash",
                "-c",
                textwrap.dedent(
                    """
                    source "$1"
                    has_command() { return 0; }
                    ensure_crit_cli() { return 0; }
                    crit() {
                        if [ "$*" = "install codex-plugin --force" ]; then
                            mkdir -p "$HOME/.agents/plugins"
                            umask 002
                            printf '{}\n' > "$HOME/.agents/plugins/marketplace.json"
                        elif [ "$*" = "--version" ]; then
                            printf 'crit v9.9.9\n'
                        fi
                    }
                    manifest_record() { :; }
                    update_codex_crit
                    """
                ),
                "_",
                str(ROOT / "scripts/update-agent-assets.sh"),
            ],
            env={**os.environ, "HOME": str(home)},
        )

        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertEqual(0o644, stat.S_IMODE(marketplace.stat().st_mode))

    def crit_fixture(
        self,
        installed_version: str | None = None,
        *,
        os_name: str = "Linux",
        arch: str = "x86_64",
    ) -> tuple[Path, Path, dict[str, str], str]:
        repo = self.temp_dir / "crit-repo"
        home = self.temp_dir / "crit-home"
        bin_dir = repo / "bin"
        (repo / "scripts/lib").mkdir(parents=True)
        (home / ".local/bin").mkdir(parents=True)
        shutil.copy(
            ROOT / "scripts/update-agent-assets.sh",
            repo / "scripts/update-agent-assets.sh",
        )
        shutil.copy(
            ROOT / "scripts/lib/asset-manifest.sh",
            repo / "scripts/lib/asset-manifest.sh",
        )
        shutil.copy(
            ROOT / "scripts/lib/installer-pins.sh",
            repo / "scripts/lib/installer-pins.sh",
        )
        (repo / "vendor/compactiondb").mkdir(parents=True)
        artifact_arch = "amd64" if arch in ("x86_64", "amd64") else "arm64"
        payload = repo / f"crit-{os_name.lower()}-{artifact_arch}"
        self.executable(payload, "printf 'crit v9.9.9 (fixture)\\n'\n")
        checksum = subprocess.run(
            ["shasum", "-a", "256", str(payload)],
            text=True,
            capture_output=True,
            check=True,
        ).stdout.split()[0]
        self.executable(
            bin_dir / "uname",
            f"""
            case "$1" in
                -s) printf '{os_name}\\n' ;;
                -m) printf '{arch}\\n' ;;
                *) printf '{os_name}\\n' ;;
            esac
            """,
        )
        self.executable(
            bin_dir / "curl",
            """
            printf 'curl %s\\n' "$*" >> "$TEST_LOG"
            out=""
            while [ "$#" -gt 0 ]; do
                if [ "$1" = "-o" ]; then out="$2"; shift; fi
                shift
            done
            cp "$CRIT_PAYLOAD" "$out"
            """,
        )
        jq = shutil.which("jq")
        self.assertIsNotNone(jq)
        (bin_dir / "jq").symlink_to(jq)
        if installed_version is not None:
            self.executable(
                home / ".local/bin/crit",
                f"printf 'crit v{installed_version} (fixture)\\n'\n",
            )
        log = repo / "commands.log"
        env = {
            **os.environ,
            "CRIT_PAYLOAD": str(payload),
            "DOTFILES_SOURCE_DIR": str(repo),
            "HOME": str(home),
            "PATH": f"{bin_dir}:{home / '.local/bin'}:/usr/bin:/bin",
            "TEST_LOG": str(log),
        }
        return repo, home, env, checksum

    def test_linux_crit_install_is_pinned_atomic_and_recorded(self) -> None:
        repo, home, env, checksum = self.crit_fixture()
        result = self.run_test_command(
            [
                "bash",
                "-c",
                "source scripts/update-agent-assets.sh; "
                "CRIT_PIN_VERSION=v9.9.9; "
                f"CRIT_LINUX_AMD64_SHA256={checksum}; "
                "ensure_crit_cli",
            ],
            cwd=repo,
            env=env,
        )

        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        target = home / ".local/bin/crit"
        self.assertTrue(target.stat().st_mode & stat.S_IXUSR)
        self.assertIn("crit v9.9.9", self.run_test_command([str(target)]).stdout)
        self.assertIn("/v9.9.9/crit-linux-amd64", (repo / "commands.log").read_text())
        manifest = json.loads((home / ".agents/.installed-manifest.json").read_text())
        self.assertEqual([str(target)], manifest["steps"]["ensure_crit_cli"]["paths"])

    def test_linux_crit_correct_version_is_download_free(self) -> None:
        repo, home, env, checksum = self.crit_fixture("9.9.9")
        result = self.run_test_command(
            [
                "bash",
                "-c",
                "source scripts/update-agent-assets.sh; "
                "CRIT_PIN_VERSION=v9.9.9; "
                f"CRIT_LINUX_AMD64_SHA256={checksum}; "
                "ensure_crit_cli",
            ],
            cwd=repo,
            env=env,
        )

        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertFalse((repo / "commands.log").exists())
        manifest = json.loads((home / ".agents/.installed-manifest.json").read_text())
        self.assertEqual(
            [str(home / ".local/bin/crit")],
            manifest["steps"]["ensure_crit_cli"]["paths"],
        )

    def test_linux_crit_prefers_pinned_target_over_older_path_binary(self) -> None:
        repo, home, env, checksum = self.crit_fixture("9.9.9")
        self.executable(
            repo / "bin/crit",
            "printf 'crit v1.0.0 (shadow)\\n'\n",
        )
        result = self.run_test_command(
            [
                "bash",
                "-c",
                "source scripts/update-agent-assets.sh; "
                "CRIT_PIN_VERSION=v9.9.9; "
                f"CRIT_LINUX_AMD64_SHA256={checksum}; "
                "ensure_crit_cli; crit --version",
            ],
            cwd=repo,
            env=env,
        )

        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertFalse((repo / "commands.log").exists())
        self.assertIn("crit v9.9.9", result.stdout)
        self.assertNotIn("shadow", result.stdout)

    def test_linux_crit_checksum_failure_preserves_existing_binary(self) -> None:
        repo, home, env, _checksum = self.crit_fixture("1.0.0")
        target = home / ".local/bin/crit"
        previous = target.read_bytes()
        result = self.run_test_command(
            [
                "bash",
                "-c",
                "source scripts/update-agent-assets.sh; "
                "CRIT_PIN_VERSION=v9.9.9; "
                f"CRIT_LINUX_AMD64_SHA256={'0' * 64}; "
                "ensure_crit_cli",
            ],
            cwd=repo,
            env=env,
        )

        self.assertNotEqual(0, result.returncode)
        self.assertEqual(previous, target.read_bytes())

    def test_linux_crit_failure_does_not_leak_cleanup_trap(self) -> None:
        repo, _home, env, _checksum = self.crit_fixture("1.0.0")
        result = self.run_test_command(
            [
                "bash",
                "-c",
                "source scripts/update-agent-assets.sh; "
                "CRIT_PIN_VERSION=v9.9.9; "
                f"CRIT_LINUX_AMD64_SHA256={'0' * 64}; "
                "ensure_crit_cli || :; "
                "later_function() { :; }; later_function",
            ],
            cwd=repo,
            env=env,
        )

        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertNotIn("unbound variable", result.stderr)

    def test_darwin_crit_install_is_pinned_atomic_and_recorded(self) -> None:
        repo, home, env, checksum = self.crit_fixture(os_name="Darwin", arch="arm64")
        result = self.run_test_command(
            [
                "bash",
                "-c",
                "source scripts/update-agent-assets.sh; "
                "CRIT_PIN_VERSION=v9.9.9; "
                f"CRIT_DARWIN_ARM64_SHA256={checksum}; "
                "ensure_crit_cli",
            ],
            cwd=repo,
            env=env,
        )

        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        target = home / ".local/bin/crit"
        self.assertTrue(target.stat().st_mode & stat.S_IXUSR)
        self.assertIn("crit v9.9.9", self.run_test_command([str(target)]).stdout)
        log = (repo / "commands.log").read_text()
        self.assertIn("/v9.9.9/crit-darwin-arm64", log)
        self.assertNotIn("crit-darwin-amd64", log)
        self.assertNotIn("crit-linux", log)
        self.assertNotIn("brew", log)
        manifest = json.loads((home / ".agents/.installed-manifest.json").read_text())
        self.assertEqual([str(target)], manifest["steps"]["ensure_crit_cli"]["paths"])

    def test_darwin_crit_checksum_failure_preserves_existing_binary(self) -> None:
        repo, home, env, _checksum = self.crit_fixture("1.0.0", os_name="Darwin", arch="arm64")
        target = home / ".local/bin/crit"
        previous = target.read_bytes()
        result = self.run_test_command(
            [
                "bash",
                "-c",
                "source scripts/update-agent-assets.sh; "
                "CRIT_PIN_VERSION=v9.9.9; "
                f"CRIT_DARWIN_ARM64_SHA256={'0' * 64}; "
                "ensure_crit_cli",
            ],
            cwd=repo,
            env=env,
        )

        self.assertNotEqual(0, result.returncode)
        self.assertIn("checksum mismatch", result.stdout + result.stderr)
        self.assertEqual(previous, target.read_bytes())

    def agmsg_fixture(
        self,
        *,
        preinstalled_version: str | None = None,
        corrupt_state_on_install: bool = False,
    ) -> tuple[Path, Path, dict[str, str], str]:
        repo = self.temp_dir / "agmsg-repo"
        home = self.temp_dir / "agmsg-home"
        bin_dir = repo / "bin"
        (repo / "scripts/lib").mkdir(parents=True)
        home.mkdir()
        shutil.copy(
            ROOT / "scripts/update-agent-assets.sh",
            repo / "scripts/update-agent-assets.sh",
        )
        shutil.copy(
            ROOT / "scripts/lib/asset-manifest.sh",
            repo / "scripts/lib/asset-manifest.sh",
        )
        shutil.copy(
            ROOT / "scripts/lib/installer-pins.sh",
            repo / "scripts/lib/installer-pins.sh",
        )
        (repo / "vendor/compactiondb").mkdir(parents=True)

        fixture_src = self.temp_dir / "agmsg-fixture-src"
        top = fixture_src / "agmsg-fake"
        (top / "scripts").mkdir(parents=True)
        (top / "SKILL.md").write_text("# fake agmsg skill\n")
        (top / "VERSION").write_text("9.9.9\n")
        self.executable(top / "scripts/send.sh", "printf 'sent\n'\n")
        self.executable(
            top / "install.sh",
            """
            SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
            cmd=agmsg
            update_only=false
            while [ $# -gt 0 ]; do
                case "$1" in
                --update) update_only=true; shift ;;
                --cmd) cmd="$2"; shift 2 ;;
                --agent-type) shift 2 ;;
                *) shift ;;
                esac
            done
            skill_dir="$HOME/.agents/skills/$cmd"
            if [ "$update_only" = true ] && [ ! -f "$skill_dir/.agmsg" ]; then
                echo "not installed" >&2
                exit 1
            fi
            mkdir -p "$skill_dir/scripts" "$skill_dir/agents"
            cp "$SCRIPT_DIR/SKILL.md" "$skill_dir/SKILL.md"
            cp "$SCRIPT_DIR/VERSION" "$skill_dir/VERSION"
            cp "$SCRIPT_DIR/scripts/send.sh" "$skill_dir/scripts/send.sh"
            chmod +x "$skill_dir/scripts/send.sh"
            touch "$skill_dir/.agmsg"
            printf 'openai: fake\n' > "$skill_dir/agents/openai.yaml"
            # Like upstream install.sh: create the store when it is missing.
            if [ ! -f "$skill_dir/db/messages.db" ]; then
                mkdir -p "$skill_dir/db"
                printf 'fresh store\n' > "$skill_dir/db/messages.db"
            fi
            if [ -n "${AGMSG_FIXTURE_TOUCH_RUN:-}" ]; then
                mkdir -p "$skill_dir/run"
                printf 'restarted\n' > "$skill_dir/run/remote-sync.team.pid"
            fi
            if [ -n "${AGMSG_FIXTURE_CORRUPT_STATE:-}" ]; then
                printf 'corrupted\n' >> "$skill_dir/teams/example/data.txt" 2>/dev/null || true
            fi
            printf 'install.sh ran: update=%s cmd=%s\n' "$update_only" "$cmd" >> "${TEST_LOG:-/dev/null}"
            """,
        )
        tarball = self.temp_dir / "agmsg-fixture.tar.gz"
        subprocess.run(
            ["tar", "czf", str(tarball), "-C", str(fixture_src), "agmsg-fake"],
            check=True,
        )
        checksum = subprocess.run(
            ["shasum", "-a", "256", str(tarball)],
            text=True,
            capture_output=True,
            check=True,
        ).stdout.split()[0]

        self.executable(
            bin_dir / "curl",
            f"""
            printf '%s\n' "$*" >> "$TEST_LOG"
            out=""
            args=("$@")
            for ((i = 0; i < ${{#args[@]}}; i++)); do
                if [[ "${{args[$i]}}" == "-o" ]]; then
                    out="${{args[$((i + 1))]}}"
                fi
            done
            cp {tarball} "$out"
            """,
        )
        jq = shutil.which("jq")
        self.assertIsNotNone(jq, "jq is required for asset manifest tests")
        (bin_dir / "jq").symlink_to(jq)

        if preinstalled_version is not None:
            skill_dir = home / ".agents/skills/agmsg"
            (skill_dir / "scripts").mkdir(parents=True)
            (skill_dir / "VERSION").write_text(f"{preinstalled_version}\n")
            self.executable(skill_dir / "scripts/send.sh", "printf 'sent\n'\n")
            (skill_dir / ".agmsg").touch()

        log = repo / "commands.log"
        env = {
            **os.environ,
            "DOTFILES_SOURCE_DIR": str(repo),
            "HOME": str(home),
            "PATH": f"{bin_dir}:/usr/bin:/bin",
            "TEST_LOG": str(log),
        }
        if corrupt_state_on_install:
            env["AGMSG_FIXTURE_CORRUPT_STATE"] = "1"
        return repo, home, env, checksum

    def test_agmsg_fresh_install_populates_skill_and_records_manifest(self) -> None:
        repo, home, env, checksum = self.agmsg_fixture()
        result = self.run_test_command(
            [
                "bash",
                "-c",
                "source scripts/update-agent-assets.sh; "
                f"AGMSG_PIN_SHA256={checksum}; "
                "AGMSG_PIN_VERSION=9.9.9; "
                "update_agmsg",
            ],
            cwd=repo,
            env=env,
        )

        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertNotIn("installer failed", result.stdout + result.stderr)
        self.assertFalse((home / ".agents/backups").exists())
        skill_dir = home / ".agents/skills/agmsg"
        self.assertEqual("9.9.9\n", (skill_dir / "VERSION").read_text())
        self.assertTrue((skill_dir / "scripts/send.sh").is_file())
        log = (repo / "commands.log").read_text()
        self.assertIn("update=false", log)
        manifest = json.loads((home / ".agents/.installed-manifest.json").read_text())
        self.assertIn("update_agmsg", manifest["steps"])

    def test_agmsg_already_pinned_skips_download(self) -> None:
        repo, home, env, checksum = self.agmsg_fixture(preinstalled_version="1.4.2")
        result = self.run_test_command(
            [
                "bash",
                "-c",
                "source scripts/update-agent-assets.sh; "
                f"AGMSG_PIN_SHA256={checksum}; "
                "AGMSG_PIN_VERSION=1.4.2; "
                "update_agmsg",
            ],
            cwd=repo,
            env=env,
        )

        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertFalse((repo / "commands.log").exists())

    def test_agmsg_checksum_mismatch_fails_closed(self) -> None:
        repo, home, env, _checksum = self.agmsg_fixture()
        result = self.run_test_command(
            [
                "bash",
                "-c",
                f"source scripts/update-agent-assets.sh; AGMSG_PIN_SHA256={'0' * 64}; update_agmsg",
            ],
            cwd=repo,
            env=env,
        )

        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn("checksum mismatch", result.stdout + result.stderr)
        self.assertIn("installer failed", result.stdout + result.stderr)
        self.assertFalse((home / ".agents/skills/agmsg").exists())

    def test_agmsg_update_never_touches_teams_db_run(self) -> None:
        repo, home, env, checksum = self.agmsg_fixture(preinstalled_version="1.0.0")
        skill_dir = home / ".agents/skills/agmsg"
        for state_dir in ("teams", "db", "run"):
            (skill_dir / state_dir / "example").mkdir(parents=True)
            (skill_dir / state_dir / "example/data.txt").write_text("live state\n")

        result = self.run_test_command(
            [
                "bash",
                "-c",
                "source scripts/update-agent-assets.sh; "
                f"AGMSG_PIN_SHA256={checksum}; "
                "AGMSG_PIN_VERSION=9.9.9; "
                "update_agmsg",
            ],
            cwd=repo,
            env=env,
        )

        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        for state_dir in ("teams", "db", "run"):
            self.assertEqual("live state\n", (skill_dir / state_dir / "example/data.txt").read_text())

    def test_agmsg_migrates_marker_less_legacy_dir_without_losing_live_state(
        self,
    ) -> None:
        repo, home, env, checksum = self.agmsg_fixture()
        skill_dir = home / ".agents/skills/agmsg"
        (skill_dir / "scripts").mkdir(parents=True)
        for state_dir in ("teams", "db", "run"):
            (skill_dir / state_dir / "example").mkdir(parents=True)
            (skill_dir / state_dir / "example/data.txt").write_text("live state\n")

        result = self.run_test_command(
            [
                "bash",
                "-c",
                "source scripts/update-agent-assets.sh; "
                f"AGMSG_PIN_SHA256={checksum}; "
                "AGMSG_PIN_VERSION=9.9.9; "
                "update_agmsg",
            ],
            cwd=repo,
            env=env,
        )

        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        log = (repo / "commands.log").read_text()
        self.assertIn("update=false", log)
        self.assertNotIn("update=true", log)
        self.assertNotIn("installer failed", result.stdout + result.stderr)
        self.assertEqual("9.9.9\n", (skill_dir / "VERSION").read_text())
        self.assertTrue((skill_dir / ".agmsg").exists())
        for state_dir in ("teams", "db", "run"):
            self.assertEqual("live state\n", (skill_dir / state_dir / "example/data.txt").read_text())
        backups = list((home / ".agents/backups").glob("agmsg-state-*"))
        self.assertEqual(1, len(backups))
        self.assertEqual("live state\n", (backups[0] / "teams/example/data.txt").read_text())
        self.assertIn(f"live state copied to {backups[0]}", result.stdout)

    def test_agmsg_update_aborts_when_install_corrupts_live_state(self) -> None:
        repo, home, env, checksum = self.agmsg_fixture(preinstalled_version="1.0.0", corrupt_state_on_install=True)
        skill_dir = home / ".agents/skills/agmsg"
        (skill_dir / "teams/example").mkdir(parents=True)
        (skill_dir / "teams/example/data.txt").write_text("live state\n")

        result = self.run_test_command(
            [
                "bash",
                "-c",
                "source scripts/update-agent-assets.sh; "
                f"AGMSG_PIN_SHA256={checksum}; "
                "AGMSG_PIN_VERSION=9.9.9; "
                "update_agmsg",
            ],
            cwd=repo,
            env=env,
        )

        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        output = result.stdout + result.stderr
        self.assertIn(
            "install.sh --update --cmd agmsg --agent-type claude-code changed or removed existing live state", output
        )
        self.assertIn(str(skill_dir / "teams/example/data.txt"), output)
        self.assertIn("installer failed", output)

    def test_agmsg_migration_reports_an_installer_that_mutates_live_state(
        self,
    ) -> None:
        repo, home, env, checksum = self.agmsg_fixture(corrupt_state_on_install=True)
        skill_dir = home / ".agents/skills/agmsg"
        (skill_dir / "scripts").mkdir(parents=True)
        (skill_dir / "teams/example").mkdir(parents=True)
        (skill_dir / "teams/example/data.txt").write_text("live state\n")
        (skill_dir / "db").mkdir()
        (skill_dir / "db/messages.db").write_bytes(b"sqlite bytes")

        result = self.run_test_command(
            [
                "bash",
                "-c",
                "source scripts/update-agent-assets.sh; "
                f"AGMSG_PIN_SHA256={checksum}; "
                "AGMSG_PIN_VERSION=9.9.9; "
                "update_agmsg",
            ],
            cwd=repo,
            env=env,
        )

        output = result.stdout + result.stderr
        self.assertEqual(0, result.returncode, output)
        self.assertNotIn("update=true", (repo / "commands.log").read_text())
        backup = next((home / ".agents/backups").glob("agmsg-state-*"))
        self.assertIn(
            "install.sh --cmd agmsg --agent-type claude-code changed or removed "
            f"existing live state (the installer or a concurrent writer); pre-install state copy: {backup}",
            output,
        )
        self.assertIn("agmsg installer failed (installed: none)", output)
        self.assertEqual("live state\n", (backup / "teams/example/data.txt").read_text())
        self.assertEqual(b"sqlite bytes", (backup / "db/messages.db").read_bytes())

    def test_agmsg_accepts_a_store_the_installer_creates_and_notes_run_changes(
        self,
    ) -> None:
        repo, home, env, checksum = self.agmsg_fixture()
        skill_dir = home / ".agents/skills/agmsg"
        for state_dir in ("teams", "db", "run"):
            (skill_dir / state_dir).mkdir(parents=True)
            (skill_dir / state_dir / ".keep").write_text("")
        env["AGMSG_FIXTURE_TOUCH_RUN"] = "1"

        result = self.run_test_command(
            [
                "bash",
                "-c",
                "source scripts/update-agent-assets.sh; "
                f"AGMSG_PIN_SHA256={checksum}; "
                "AGMSG_PIN_VERSION=9.9.9; "
                "update_agmsg",
            ],
            cwd=repo,
            env=env,
        )

        output = result.stdout + result.stderr
        self.assertEqual(0, result.returncode, output)
        self.assertNotIn("installer failed", output)
        self.assertEqual("fresh store\n", (skill_dir / "db/messages.db").read_text())
        self.assertIn("agmsg: note: run/ changed during install.sh", result.stdout)

    def test_agmsg_reports_an_installer_that_leaves_the_wrong_version(self) -> None:
        repo, home, env, checksum = self.agmsg_fixture()

        result = self.run_test_command(
            [
                "bash",
                "-c",
                f"source scripts/update-agent-assets.sh; AGMSG_PIN_SHA256={checksum}; update_agmsg",
            ],
            cwd=repo,
            env=env,
        )

        output = result.stdout + result.stderr
        self.assertEqual(0, result.returncode, output)
        self.assertIn(
            "agmsg: install.sh --cmd agmsg --agent-type claude-code left VERSION 9.9.9 (want 1.5.0)",
            output,
        )
        self.assertIn("agmsg installer failed (installed: none)", output)

    def test_agmsg_refuses_to_install_when_the_state_snapshot_is_empty(self) -> None:
        repo, home, env, checksum = self.agmsg_fixture(preinstalled_version="1.0.0")
        skill_dir = home / ".agents/skills/agmsg"
        (skill_dir / "teams/example").mkdir(parents=True)
        (skill_dir / "teams/example/data.txt").write_text("live state\n")
        bin_dir = repo / "bin"
        for tool in ("sha256sum", "shasum"):
            self.executable(bin_dir / tool, "exit 0\n")

        result = self.run_test_command(
            [
                "bash",
                "-c",
                "source scripts/update-agent-assets.sh; "
                f"AGMSG_PIN_SHA256={checksum}; "
                "AGMSG_PIN_VERSION=9.9.9; "
                "update_agmsg",
            ],
            cwd=repo,
            env=env,
        )

        output = result.stdout + result.stderr
        self.assertEqual(0, result.returncode, output)
        self.assertIn("hashed fewer live-state files than exist", output)
        self.assertIn("could not snapshot the live state", output)
        self.assertFalse((repo / "commands.log").exists())
        self.assertEqual("1.0.0\n", (skill_dir / "VERSION").read_text())

    def test_agmsg_refuses_to_install_without_tar(self) -> None:
        repo, home, env, checksum = self.agmsg_fixture()
        no_tar = self.temp_dir / "no-tar-bin"
        no_tar.mkdir()
        for directory in ("/usr/bin", "/bin"):
            for tool in Path(directory).iterdir():
                link = no_tar / tool.name
                if tool.name != "tar" and not (link.exists() or link.is_symlink()):
                    link.symlink_to(tool)
        env["PATH"] = f"{repo / 'bin'}:{no_tar}"

        result = self.run_test_command(
            [
                "bash",
                "-c",
                f"source scripts/update-agent-assets.sh; AGMSG_PIN_SHA256={checksum}; update_agmsg",
            ],
            cwd=repo,
            env=env,
        )

        output = result.stdout + result.stderr
        self.assertEqual(0, result.returncode, output)
        self.assertIn("agmsg: tar not found; nothing was installed", output)
        self.assertFalse((repo / "commands.log").exists())
        self.assertFalse((home / ".agents/skills/agmsg").exists())

    def update_fixture(
        self,
        *,
        branch: str = "main",
        upstream: str = "origin/main",
        dirty: bool = False,
        unmerged: bool = False,
    ) -> tuple[subprocess.CompletedProcess[str], Path]:
        repo = self.temp_dir / f"update-{'dirty' if dirty else 'clean'}"
        home = repo / "home"
        bin_dir = repo / "bin"
        (repo / "scripts").mkdir(parents=True)
        home.mkdir()
        shutil.copy(ROOT / "Makefile", repo / "Makefile")
        self.executable(
            bin_dir / "git",
            f"""
            case "$*" in
                "branch --show-current") printf '{branch}\\n' ;;
                "rev-parse --abbrev-ref --symbolic-full-name @{{upstream}}") printf '{upstream}\\n' ;;
                "diff --quiet"|"diff --cached --quiet") exit {int(dirty)} ;;
                "ls-files -u") if [ {int(unmerged)} -eq 1 ]; then printf '100644 conflict 1\\tfile\\n'; fi ;;
                "pull --ff-only") printf 'git pull --ff-only\\n' >> "$TEST_LOG" ;;
            esac
            """,
        )
        self.executable(bin_dir / "chezmoi", 'printf \'chezmoi %s\\n\' "$*" >> "$TEST_LOG"\n')
        self.executable(bin_dir / "mise", 'printf \'mise %s\\n\' "$*" >> "$TEST_LOG"\n')
        self.executable(
            bin_dir / "herdr",
            """
            if [ "$*" = "status server --json" ]; then
                printf '{"status":"not_running"}\\n'
            fi
            """,
        )
        self.executable(
            repo / "scripts/upgrade-tools.sh",
            'printf \'upgrade-tools %s\\n\' "$*" >> "$TEST_LOG"\n',
        )
        self.executable(
            repo / "scripts/update-agent-assets.sh",
            "printf 'assets\\n' >> \"$TEST_LOG\"\n",
        )
        jq = shutil.which("jq")
        self.assertIsNotNone(jq)
        (bin_dir / "jq").symlink_to(jq)
        log = repo / "calls"
        result = self.run_test_command(
            ["make", "update"],
            cwd=repo,
            env={
                **os.environ,
                "HOME": str(home),
                "PATH": f"{bin_dir}:/usr/bin:/bin",
                "TEST_LOG": str(log),
            },
        )
        return result, log

    def test_make_update_pulls_clean_main_before_apply(self) -> None:
        result, log = self.update_fixture()

        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertEqual("git pull --ff-only", log.read_text().splitlines()[0])

    def test_make_update_skips_dirty_main_with_manual_pull_notice(self) -> None:
        result, log = self.update_fixture(dirty=True)

        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertNotIn("git pull --ff-only", log.read_text())
        self.assertIn(
            "Notice: local source not pulled (tracked files have staged or unstaged changes); run 'git -C ",
            result.stdout,
        )
        self.assertIn(" pull' to fetch remote updates.", result.stdout)

    def test_make_update_reports_unmerged_index_before_dirty_notice(self) -> None:
        result, log = self.update_fixture(dirty=True, unmerged=True)

        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertNotIn("git pull --ff-only", log.read_text())
        self.assertIn(
            "index has unmerged files; resolve the conflict (git add/commit or git reset) before pulling",
            result.stdout,
        )
        self.assertNotIn("tracked files have staged or unstaged changes", result.stdout)

    def test_make_update_reports_unmerged_feature_branch_before_branch_notice(
        self,
    ) -> None:
        result, log = self.update_fixture(branch="feature/x", unmerged=True)

        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertNotIn("git pull --ff-only", log.read_text())
        self.assertIn("index has unmerged files", result.stdout)
        self.assertNotIn("current branch is", result.stdout)

    def test_agent_launchers_do_not_hardcode_model_ids(self) -> None:
        herdr = (ROOT / "home/dot_local/bin/common/executable_herdr-agents").read_text()

        self.assertNotIn("claude-fable-5", herdr)
        self.assertNotIn("gpt-5.6", herdr)
        self.assertNotIn("model_reasoning_effort=", herdr)
        # --add-worker passes the worker profile (default standard), never a model id.
        self.assertIn('args="--profile ${HERDR_AGENTS_WORKER_PROFILE} --sandbox workspace-write', herdr)
        self.assertIn('"${HERDR_AGENTS_WORKER_PROFILE:-${MODEL_PROFILE_INTERACTIVE:-standard}}"', herdr)

    def doctor_environment(self, *, fail: str = "", os_name: str = "Linux") -> dict[str, str]:
        fixture_name = (fail or "healthy").replace(":", "-").replace(" ", "-")
        bin_dir = self.temp_dir / f"doctor-bin-{fixture_name}-{os_name}"
        log = self.temp_dir / "doctor.log"
        bin_dir.mkdir()
        missing = fail.removeprefix("missing:") if fail.startswith("missing:") else ""
        for command in ("git", "chezmoi", "mise", "uv", "gh", "brew", "bwrap", "socat"):
            if command == missing:
                continue
            self.executable(
                bin_dir / command,
                """
                printf '%s %s\\n' "$(basename "$0")" "$*" >> "$TEST_LOG"
                if [[ "$(basename "$0"):$*" == "$FAIL_COMMAND" ]]; then exit 9; fi
                printf '%s healthy\\n' "$(basename "$0")"
                """,
            )
        self.executable(bin_dir / "uname", f"printf '{os_name}\\n'\n")
        home = self.temp_dir / "doctor-home"
        (home / ".local/share/chezmoi-private").mkdir(parents=True, exist_ok=True)
        private_config = home / ".config/chezmoi-private/chezmoi.yaml"
        private_config.parent.mkdir(parents=True, exist_ok=True)
        private_config.touch()
        (home / ".ssh").mkdir(parents=True, exist_ok=True)
        (home / ".ssh/id_ed25519.pub").touch()
        return {
            **os.environ,
            "HOME": str(home),
            "PATH": f"{bin_dir}:/usr/bin:/bin",
            "FAIL_COMMAND": fail,
            "TEST_LOG": str(log),
            # Keep the host's AppArmor userns restriction out of these fixtures.
            "APPARMOR_USERNS_SYSCTL": str(self.temp_dir / "no-userns-restriction"),
        }

    def test_doctor_required_optional_and_healthy_statuses(self) -> None:
        cases = (
            ("", 0, "required failures: 0"),
            ("missing:chezmoi", 1, "required failures: 1"),
            ("git:--version", 1, "required failures: 1"),
            ("gh:extension list", 0, "optional warnings: 1"),
        )
        for fail, expected_status, summary in cases:
            with self.subTest(fail=fail):
                result = self.run_test_command(
                    ["bash", str(ROOT / "scripts/check-tools.sh")],
                    env=self.doctor_environment(fail=fail),
                )
                self.assertEqual(expected_status, result.returncode, result.stdout + result.stderr)
                self.assertIn(summary, result.stdout)

        result = self.run_test_command(
            ["bash", str(ROOT / "scripts/check-tools.sh")],
            env=self.doctor_environment(fail="missing:brew", os_name="Darwin"),
        )
        self.assertNotEqual(0, result.returncode)
        self.assertIn("required missing: brew", result.stderr)

    def test_doctor_has_no_github_role_check(self) -> None:
        # One GitHub login per machine: the tool check compares no identities; the runtime check reports the login.
        script = (ROOT / "scripts/check-tools.sh").read_text()
        self.assertNotIn("check_github_identities", script)
        self.assertNotIn("GitHub role", script)

    def test_doctor_reports_claude_sandbox_prerequisites(self) -> None:
        bin_dir = self.temp_dir / "sandbox-bin"
        self.executable(bin_dir / "uname", "printf 'Linux\\n'\n")
        self.executable(bin_dir / "bwrap", "exit 0\n")
        script = f"source {ROOT / 'scripts/check-tools.sh'}; check_claude_sandbox; echo warnings=$optional_warnings"

        result = self.run_test_command(["/bin/bash", "-c", script], env={"PATH": str(bin_dir)})
        output = result.stdout + result.stderr
        self.assertEqual(0, result.returncode, output)
        self.assertIn(f"found:   bwrap -> {bin_dir / 'bwrap'}", output)
        self.assertIn("prerequisite is missing: socat", output)
        self.assertIn("warnings=1", output)

        self.executable(bin_dir / "socat", "exit 0\n")
        result = self.run_test_command(["/bin/bash", "-c", script], env={"PATH": str(bin_dir)})
        self.assertIn(f"found:   socat -> {bin_dir / 'socat'}", result.stdout)
        self.assertIn("warnings=0", result.stdout)

        self.executable(bin_dir / "uname", "printf 'Darwin\\n'\n")
        result = self.run_test_command(["/bin/bash", "-c", script], env={"PATH": str(bin_dir)})
        self.assertIn("not applicable: Claude Code sandbox prerequisites", result.stdout)
        self.assertIn("warnings=0", result.stdout)

    def test_make_doctor_propagates_runtime_drift_after_tool_checks(self) -> None:
        repo = self.temp_dir / "doctor-repo"
        home = self.temp_dir / "doctor-runtime-home"
        (repo / "scripts").mkdir(parents=True)
        (repo / "home/dot_agents").mkdir(parents=True)
        (repo / "home/dot_claude").mkdir()
        (repo / "home/dot_codex").mkdir()
        (home / ".agents").mkdir(parents=True)
        (home / ".claude").mkdir()
        (home / ".codex").mkdir()
        shutil.copy(ROOT / "Makefile", repo / "Makefile")
        shutil.copy(ROOT / "scripts/check-tools.sh", repo / "scripts/check-tools.sh")
        self.executable(
            repo / "scripts/check-agent-runtime.py",
            "printf 'runtime drift\\n' >&2\nexit 7\n",
        )
        env = self.doctor_environment()
        env["HOME"] = str(home)

        result = self.run_test_command(["make", "doctor"], cwd=repo, env=env)

        self.assertNotEqual(0, result.returncode)
        self.assertIn("runtime drift", result.stderr)
        self.assertIn("git --version", (self.temp_dir / "doctor.log").read_text())
        self.assertIn("Doctor summary: tools=passed; runtime=failed", result.stdout)

        self.executable(repo / "scripts/check-agent-runtime.py", "printf 'runtime healthy\\n'\n")
        result = self.run_test_command(["make", "doctor"], cwd=repo, env=env)
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_make_doctor_does_not_skip_runtime_check_when_deployed_root_is_missing(
        self,
    ) -> None:
        repo = self.temp_dir / "doctor-missing-runtime-repo"
        home = self.temp_dir / "doctor-missing-runtime-home"
        (repo / "scripts").mkdir(parents=True)
        (repo / "home/dot_agents").mkdir(parents=True)
        (repo / "home/dot_claude").mkdir()
        (repo / "home/dot_codex").mkdir()
        (home / ".agents").mkdir(parents=True)
        (home / ".claude").mkdir()
        shutil.copy(ROOT / "Makefile", repo / "Makefile")
        shutil.copy(ROOT / "scripts/check-tools.sh", repo / "scripts/check-tools.sh")
        self.executable(
            repo / "scripts/check-agent-runtime.py",
            "printf 'missing runtime root\\n' >&2\nexit 7\n",
        )
        env = self.doctor_environment()
        env["HOME"] = str(home)

        result = self.run_test_command(["make", "doctor"], cwd=repo, env=env)

        self.assertNotEqual(0, result.returncode)
        self.assertIn("missing runtime root", result.stderr)
        self.assertIn("Doctor summary: tools=passed; runtime=failed", result.stdout)

    def test_make_doctor_passes_repair_variable_to_runtime_check(self) -> None:
        repo = self.temp_dir / "doctor-repair-repo"
        home = self.temp_dir / "doctor-repair-home"
        (repo / "scripts").mkdir(parents=True)
        (repo / "home/dot_agents").mkdir(parents=True)
        (repo / "home/dot_claude").mkdir()
        (repo / "home/dot_codex").mkdir()
        home.mkdir()
        shutil.copy(ROOT / "Makefile", repo / "Makefile")
        shutil.copy(ROOT / "scripts/check-tools.sh", repo / "scripts/check-tools.sh")
        self.executable(
            repo / "scripts/check-agent-runtime.py",
            "printf 'repair=%s\\n' \"${REPAIR:-unset}\"\n",
        )
        env = self.doctor_environment()
        env["HOME"] = str(home)

        result = self.run_test_command(["make", "doctor", "REPAIR=1"], cwd=repo, env=env)

        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn("repair=1", result.stdout)

    def upgrade_fixture(self, fail_phase: str, os_name: str = "Linux") -> tuple[Path, dict[str, str]]:
        repo = self.temp_dir / f"upgrade-{fail_phase}"
        bin_dir = repo / "bin"
        home = repo / "home"
        (repo / "scripts").mkdir(parents=True)
        home.mkdir()
        shutil.copy(ROOT / "scripts/upgrade-tools.sh", repo / "scripts/upgrade-tools.sh")
        self.executable(bin_dir / "uname", f"printf '{os_name}\\n'\n")
        self.executable(
            bin_dir / "brew",
            """
            printf 'brew %s\n' "$*" >> "$TEST_LOG"
            [[ "$FAIL_PHASE:$1" != homebrew:update ]] || exit 1
            case "$*" in
                "outdated --formula --quiet") printf 'jq\n' ;;
                upgrade\ *) printf 'brew-env HOMEBREW_VERIFY_ATTESTATIONS=%s HOMEBREW_NO_ASK=%s\n' \
                    "${HOMEBREW_VERIFY_ATTESTATIONS:-unset}" "${HOMEBREW_NO_ASK:-unset}" >> "$TEST_LOG" ;;
            esac
            """,
        )
        self.executable(
            bin_dir / "mise",
            """
            printf 'mise %s\n' "$*" >> "$TEST_LOG"
            printf 'MISE_CONFIG_DIR=%s\n' "$MISE_CONFIG_DIR" >> "$TEST_LOG"
            printf 'MISE_CEILING_PATHS=%s\n' "$MISE_CEILING_PATHS" >> "$TEST_LOG"
            case "$1" in
                self-update) [[ "$FAIL_PHASE" != mise_self ]] ;;
                ls) [[ "$FAIL_PHASE" != mise_inventory ]] && printf 'node 26.0.0 fixture\npython 3.13 fixture\nnpm:ccusage 20.0.0 fixture\nfd 10.3.0 fixture\nhttp:bats 1.13.0 fixture\nhttp:gcloud 575.0.1 fixture\n' ;;
                install)
                    [[ "$FAIL_PHASE" != mise_install ]] || exit 1
                    # The bare install moves a "latest" node that is not installed yet.
                    [[ "$FAIL_PHASE:$*" != "node_by_install:install --yes" ]] || touch "$NODE_MOVED"
                    case "$FAIL_PHASE:$*" in
                        npm_reinstall*:"install --yes npm:ccusage@20.0.0")
                            # The download fails after mise created a partial install directory.
                            mkdir -p "$CCUSAGE_DIR/partial"
                            exit 1
                            ;;
                        npm_reinstall_final_fails:"install --yes")
                            # The first bare install succeeds; the final one cannot reach the network.
                            [ ! -e "$NODE_MOVED.bare-install" ] || exit 1
                            touch "$NODE_MOVED.bare-install"
                            ;;
                    esac
                    case "$*" in
                        "install --yes") mkdir -p "$CCUSAGE_DIR" ;;
                        "install --yes npm:ccusage@20.0.0") mkdir -p "$CCUSAGE_DIR" && touch "$CCUSAGE_DIR/rebuilt" ;;
                    esac
                    ;;
                upgrade)
                    [[ "$FAIL_PHASE" != mise_upgrade ]] || exit 1
                    # Upgrading node moves the current node, which the script must notice.
                    [[ "$*" != "upgrade --yes node" || "$FAIL_PHASE" == node_stays* || "$FAIL_PHASE" == node_by_install ]] || touch "$NODE_MOVED"
                    ;;
                current)
                    case "$2" in
                        node) [ -e "$NODE_MOVED" ] && printf '27.0.0\n' || printf '26.0.0\n' ;;
                        npm:ccusage) printf '20.0.0\n' ;;
                    esac
                    ;;
                where) [[ "$2" != npm:ccusage ]] || printf '%s\n' "$CCUSAGE_DIR" ;;
            esac
            """,
        )
        self.executable(
            bin_dir / "uv",
            """
            printf 'uv %s\n' "$*" >> "$TEST_LOG"
            [[ "$FAIL_PHASE" != uv ]]
            """,
        )
        self.executable(
            bin_dir / "gh",
            """
            printf 'gh %s\n' "$*" >> "$TEST_LOG"
            [[ "$FAIL_PHASE:$1" != gh:extension ]] || exit 9
            """,
        )
        self.executable(
            bin_dir / "sudo",
            """
            printf 'sudo %s\n' "$*" >> "$TEST_LOG"
            [[ "$FAIL_PHASE" != apt ]]
            """,
        )
        self.executable(bin_dir / "apt-get", "exit 0\n")
        log = repo / "commands.log"
        env = {
            **os.environ,
            # GitHub Actions sets CI=true, which makes the script skip every phase.
            "CI": "false",
            "FAIL_PHASE": fail_phase,
            "HOME": str(home),
            "PATH": f"{bin_dir}:/usr/bin:/bin",
            "TEST_LOG": str(log),
            # Outside the repository, so the no-file-written assertion still holds.
            "NODE_MOVED": str(self.temp_dir / f"upgrade-{fail_phase}.node-moved"),
            # The installed npm:ccusage, outside the repository; "original" marks the install before any rebuild.
            "CCUSAGE_DIR": str(self.temp_dir / f"upgrade-{fail_phase}.ccusage"),
            # The npm-tools node marker lives outside the repository, like the host state it stands for.
            "XDG_STATE_HOME": str(self.temp_dir / f"upgrade-{fail_phase}.state"),
        }
        (Path(env["CCUSAGE_DIR"]) / "original").parent.mkdir(parents=True)
        (Path(env["CCUSAGE_DIR"]) / "original").touch()
        for name in ("MISE_CONFIG_DIR", "MISE_CEILING_PATHS", "XDG_CONFIG_HOME"):
            env.pop(name, None)
        return repo, env

    def test_upgrade_runs_mise_against_the_applied_host_config_and_edits_no_file(self) -> None:
        # chezmoi applies the config to ~/.config/mise whatever XDG_CONFIG_HOME or an inherited MISE_CONFIG_DIR say.
        for override in (None, "XDG_CONFIG_HOME", "MISE_CONFIG_DIR"):
            with self.subTest(override=override):
                repo, env = self.upgrade_fixture(f"host-config-{override}")
                expected = f"{env['HOME']}/.config/mise"
                if override:
                    env[override] = str(repo / "elsewhere")
                before = {path.relative_to(repo) for path in repo.rglob("*")}

                result = self.run_test_command(["bash", "scripts/upgrade-tools.sh"], cwd=repo, env=env)

                self.assertEqual(0, result.returncode, result.stdout + result.stderr)
                log = (repo / "commands.log").read_text().splitlines()
                self.assertEqual(
                    {f"MISE_CONFIG_DIR={expected}"}, {line for line in log if line.startswith("MISE_CONFIG_DIR=")}
                )
                # A parent directory's mise.toml must not join the inventory: the ceiling is the checkout.
                ceilings = {line.split("=", 1)[1] for line in log if line.startswith("MISE_CEILING_PATHS=")}
                self.assertEqual({repo.resolve()}, {Path(ceiling).resolve() for ceiling in ceilings})
                after = {path.relative_to(repo) for path in repo.rglob("*")}
                self.assertEqual(before | {Path("commands.log")}, after)
                self.assertNotIn("chezmoi", "\n".join(log))

    def test_upgrade_skips_every_phase_when_ci_is_true(self) -> None:
        repo, env = self.upgrade_fixture("none")
        env["CI"] = "true"

        result = self.run_test_command(["bash", "scripts/upgrade-tools.sh", "--system"], cwd=repo, env=env)

        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertEqual("CI=true: skipping installed-tool updates.\n", result.stdout)
        self.assertFalse((repo / "commands.log").exists())

    def test_upgrade_homebrew_verifies_attestations_when_gh_is_present(self) -> None:
        for with_gh in (True, False):
            with self.subTest(with_gh=with_gh):
                repo, env = self.upgrade_fixture(f"homebrew-attest-{with_gh}", "Darwin")
                if not with_gh:
                    (repo / "bin/gh").unlink()
                    # Runner images ship /usr/bin/gh; hide only gh, not the rest of the system tools.
                    system = repo / "system-bin"
                    system.mkdir()
                    for directory in ("/usr/bin", "/bin"):
                        for entry in os.scandir(directory):
                            if entry.name != "gh" and not os.path.lexists(system / entry.name):
                                (system / entry.name).symlink_to(entry.path)
                    env["PATH"] = f"{repo / 'bin'}:{system}"
                result = self.run_test_command(["bash", "scripts/upgrade-tools.sh"], cwd=repo, env=env)

                self.assertEqual(0, result.returncode, result.stdout + result.stderr)
                log = (repo / "commands.log").read_text().splitlines()
                self.assertIn("brew upgrade --formula jq", log)
                attest = "1" if with_gh else "unset"
                self.assertIn(f"brew-env HOMEBREW_VERIFY_ATTESTATIONS={attest} HOMEBREW_NO_ASK=1", log)
                skipped = "gh not found; Homebrew bottle attestation verification is skipped."
                self.assertEqual(not with_gh, skipped in result.stdout)

    def test_upgrade_network_only_phases_warn_and_the_mise_phase_still_runs(self) -> None:
        # An offline host must still converge: only installing the declared mise tools is required.
        for phase, os_name in (("homebrew", "Darwin"), ("mise_self", "Linux"), ("uv", "Linux"), ("gh", "Linux")):
            with self.subTest(phase=phase):
                repo, env = self.upgrade_fixture(phase, os_name)
                result = self.run_test_command(["bash", "scripts/upgrade-tools.sh"], cwd=repo, env=env)

                self.assertEqual(0, result.returncode, result.stdout + result.stderr)
                self.assertIn("required failures: 0; optional warnings: 1", result.stdout)
                log = (repo / "commands.log").read_text().splitlines()
                self.assertIn("mise install --yes", log)
                self.assertIn("mise upgrade --yes python", log)

    def test_upgrade_required_failures_are_nonzero_and_independent(self) -> None:
        cases = (
            ("mise_inventory", "Linux", []),
            ("mise_install", "Linux", []),
            ("apt", "Linux", ["--system"]),
        )
        for phase, os_name, args in cases:
            with self.subTest(phase=phase):
                repo, env = self.upgrade_fixture(phase, os_name)
                result = self.run_test_command(
                    ["bash", "scripts/upgrade-tools.sh", *args],
                    cwd=repo,
                    env=env,
                )
                self.assertEqual(1, result.returncode, result.stdout + result.stderr)
                self.assertIn("required failures:", result.stdout)
                log = (repo / "commands.log").read_text()
                if phase != "apt":
                    self.assertIn("gh extension upgrade --all", log)

    def test_upgrade_skips_unavailable_mise_self_update(self) -> None:
        repo, env = self.upgrade_fixture("none")
        marker = repo / "lib/mise-self-update-instructions.toml"
        marker.parent.mkdir()
        marker.write_text('message = "managed by fixture package manager"\n')
        result = self.run_test_command(
            ["bash", "scripts/upgrade-tools.sh"],
            cwd=repo,
            env=env,
        )

        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn("Skipping mise self-update: managed by package manager.", result.stdout)
        self.assertIn("Skipping mise upgrade for pinned HTTP tool: http:bats.", result.stdout)
        self.assertIn("Skipping mise upgrade for pinned HTTP tool: http:gcloud.", result.stdout)
        log = (repo / "commands.log").read_text().splitlines()
        self.assertFalse([line for line in log if line.startswith("mise self-update")])
        # One bare install (a per-tool install of a "latest" request needs the network), then per-tool upgrades.
        self.assertIn("mise install --yes", log)
        # Only exact versions (the npm rebuild) are installed per tool; a per-tool "latest" install needs the network.
        self.assertFalse([line for line in log if line.startswith("mise install --yes ") and "@" not in line])
        self.assertIn("mise upgrade --yes python", log)
        self.assertNotIn("mise upgrade --yes fd", log)
        self.assertFalse([line for line in log if line.startswith("mise upgrade --yes http:")])
        # The config's minimum_release_age is the cooldown; nothing bumps or rewrites a request.
        for flag in ("--bump", "--before", "--pin", " use "):
            self.assertFalse([line for line in log if flag in line], flag)

        repo, env = self.upgrade_fixture("mise_install")
        marker = repo / "lib/mise/mise-self-update-instructions.toml"
        marker.parent.mkdir(parents=True)
        marker.write_text('message = "managed by fixture package manager"\n')
        result = self.run_test_command(["bash", "scripts/upgrade-tools.sh"], cwd=repo, env=env)
        self.assertEqual(1, result.returncode, result.stdout + result.stderr)
        self.assertIn("required failure: mise inventory/install/upgrade", result.stderr)

    def test_upgrade_rebuilds_npm_tools_when_the_node_marker_differs(self) -> None:
        # The marker records the node the npm: tools were built on, so a node moved by an earlier run or by the
        # installer during chezmoi apply is rebuilt as well as one moved here.
        for name, phase, marker, rebuilt, warning, recorded in (
            ("marker absent", "node_stays-absent", None, True, False, "26.0.0"),
            ("marker equal", "node_stays-equal", "26.0.0", False, False, "26.0.0"),
            ("marker differs, node moved before this run", "node_stays-differs", "25.0.0", True, False, "26.0.0"),
            ("node upgraded in this run", "none", "26.0.0", True, False, "27.0.0"),
            ("node moved by the bare install", "node_by_install", "26.0.0", True, False, "27.0.0"),
            ("rebuild fails: previous install kept, not recorded", "npm_reinstall", "26.0.0", True, True, "26.0.0"),
            # The first update on an existing host has no marker; offline, the working tool must survive.
            ("marker absent and rebuild fails", "npm_reinstall-absent", None, True, True, None),
        ):
            with self.subTest(name):
                repo, env = self.upgrade_fixture(phase)
                marker_file = Path(env["XDG_STATE_HOME"]) / "dotfiles/npm-tools-node"
                tool = Path(env["CCUSAGE_DIR"])
                if marker is not None:
                    marker_file.parent.mkdir(parents=True)
                    marker_file.write_text(f"{marker}\n")

                result = self.run_test_command(["bash", "scripts/upgrade-tools.sh"], cwd=repo, env=env)

                self.assertEqual(0, result.returncode, result.stdout + result.stderr)
                log = (repo / "commands.log").read_text().splitlines()
                exact = [line for line in log if line.startswith("mise install --yes npm:")]
                self.assertEqual(["mise install --yes npm:ccusage@20.0.0"] if rebuilt else [], exact)
                self.assertFalse([line for line in log if "--force" in line])
                self.assertEqual(
                    warning, "optional warning: npm: tools were not all reinstalled on node 27.0.0" in result.stderr
                )
                self.assertIn(f"required failures: 0; optional warnings: {int(warning)}", result.stdout)
                # After a rebuild a final bare install confirms every declared tool is present.
                self.assertEqual(2 if rebuilt else 1, log.count("mise install --yes"))
                # A successful rebuild replaces the install; a failed one restores it untouched.
                self.assertEqual(rebuilt and not warning, (tool / "rebuilt").exists())
                self.assertEqual(not (rebuilt and not warning), (tool / "original").exists())
                self.assertFalse((tool / "partial").exists())
                self.assertFalse(Path(f"{tool}.before-node-rebuild").exists())
                if recorded is None:
                    self.assertFalse(marker_file.exists())
                else:
                    self.assertEqual(f"{recorded}\n", marker_file.read_text())

    def test_upgrade_fails_when_the_final_install_fails_after_a_rebuild(self) -> None:
        # The rebuild restored the previous install, but the final bare install fails: not converged.
        repo, env = self.upgrade_fixture("npm_reinstall_final_fails")
        marker_file = Path(env["XDG_STATE_HOME"]) / "dotfiles/npm-tools-node"
        marker_file.parent.mkdir(parents=True)
        marker_file.write_text("26.0.0\n")

        result = self.run_test_command(["bash", "scripts/upgrade-tools.sh"], cwd=repo, env=env)

        self.assertEqual(1, result.returncode, result.stdout + result.stderr)
        self.assertIn("optional warning: npm: tools were not all reinstalled on node 27.0.0", result.stderr)
        self.assertIn("required failure: mise inventory/install/upgrade", result.stderr)
        self.assertTrue((Path(env["CCUSAGE_DIR"]) / "original").exists())
        self.assertEqual(2, (repo / "commands.log").read_text().splitlines().count("mise install --yes"))
        # The failed final install leaves the marker unwritten, so the next run rebuilds again.
        self.assertEqual("26.0.0\n", marker_file.read_text())

    def test_upgrade_fails_when_the_node_marker_cannot_be_written(self) -> None:
        repo, env = self.upgrade_fixture("node_stays-unwritable")
        # A regular file where the state directory should be makes mkdir -p fail.
        Path(env["XDG_STATE_HOME"]).write_text("not a directory\n")

        result = self.run_test_command(["bash", "scripts/upgrade-tools.sh"], cwd=repo, env=env)

        self.assertEqual(1, result.returncode, result.stdout + result.stderr)
        self.assertIn("required: could not record the npm-tools node in", result.stderr)
        self.assertIn("required failure: mise inventory/install/upgrade", result.stderr)

    def test_upgrade_failure_after_a_successful_install_only_warns(self) -> None:
        # Converged means the declared tools are installed; an upgrade that cannot reach its archive only warns.
        repo, env = self.upgrade_fixture("mise_upgrade")

        result = self.run_test_command(["bash", "scripts/upgrade-tools.sh"], cwd=repo, env=env)

        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn("warning: mise upgrade failed for python; continuing", result.stderr)
        self.assertIn(
            "optional warning: mise upgrade failed for at least one tool; its installed version stays", result.stderr
        )
        self.assertIn("required failures: 0; optional warnings: 1", result.stdout)
        self.assertNotIn("required failure: mise inventory/install/upgrade", result.stderr)
        self.assertIn("mise install --yes", (repo / "commands.log").read_text().splitlines())

    def test_upgrade_self_updates_mise_to_its_latest_release(self) -> None:
        repo, env = self.upgrade_fixture("none")

        result = self.run_test_command(["bash", "scripts/upgrade-tools.sh"], cwd=repo, env=env)

        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        log = (repo / "commands.log").read_text().splitlines()
        self.assertIn("mise self-update --yes --no-plugins", log)


if __name__ == "__main__":
    unittest.main()
