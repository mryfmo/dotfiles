#!/usr/bin/env python3
"""Verify truthful runtime artifact, doctor, and upgrade behavior."""

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

    def test_agent_runs_are_private_and_ignored(self) -> None:
        repo = self.temp_dir / "repo"
        home = self.temp_dir / "home"
        bin_dir = self.temp_dir / "bin"
        repo.mkdir()
        home.mkdir()
        shutil.copy(ROOT / ".gitignore", repo / ".gitignore")
        shutil.copy(
            ROOT / "home/dot_local/bin/common/executable_agent-fanout",
            repo / "agent-fanout",
        )
        self.executable(bin_dir / "codex", "printf 'fake agent output\\n'\n")
        self.run_test_command(["git", "init", "-q"], cwd=repo, check=True)

        result = self.run_test_command(
            ["bash", "./agent-fanout", "--no-claude", "secret prompt"],
            cwd=repo,
            env={
                **os.environ,
                "HOME": str(home),
                "PATH": f"{bin_dir}:{os.environ['PATH']}",
            },
        )

        self.assertEqual(0, result.returncode, result.stderr)
        runs = repo / ".agents/runs"
        run_dir = next(runs.iterdir())
        self.assertEqual(0o700, stat.S_IMODE(runs.stat().st_mode))
        self.assertEqual(0o700, stat.S_IMODE(run_dir.stat().st_mode))
        for artifact in run_dir.iterdir():
            if artifact.is_file():
                self.assertEqual(
                    0, stat.S_IMODE(artifact.stat().st_mode) & 0o077, artifact
                )
        status = self.run_test_command(
            ["git", "status", "--short", "--ignored", ".agents/runs"],
            cwd=repo,
            check=True,
        )
        self.assertIn("!! .agents/runs/", status.stdout)

    def test_agent_asset_update_removes_node_global_shadows_before_agent_commands(
        self,
    ) -> None:
        repo = self.temp_dir / "agent-assets-repo"
        home = self.temp_dir / "agent-assets-home"
        bin_dir = repo / "bin"
        (repo / "scripts").mkdir(parents=True)
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
        first_agent_call = min(
            i for i, call in enumerate(calls) if call.startswith(("claude ", "codex "))
        )
        self.assertLess(calls.index("npm uninstall -g @openai/codex"), first_agent_call)
        self.assertLess(
            calls.index("npm uninstall -g @anthropic-ai/claude-code"), first_agent_call
        )

    def test_agent_asset_update_repairs_broken_claude_with_npm_backend(self) -> None:
        repo = self.temp_dir / "agent-assets-repair-repo"
        home = self.temp_dir / "agent-assets-repair-home"
        bin_dir = home / ".local/bin"
        shim_dir = home / ".local/share/mise/shims"
        (repo / "scripts").mkdir(parents=True)
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
            if [ "$*" = "install --force --locked npm:@anthropic-ai/claude-code" ]; then
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
        repair = "mise npm 0 install --force --locked npm:@anthropic-ai/claude-code"
        self.assertIn(repair, calls)
        self.assertFalse(
            any(
                call.endswith("npm:@openai/codex") and call.startswith("mise ")
                for call in calls
            )
        )
        self.assertLess(
            calls.index(repair), calls.index("claude plugin marketplace list")
        )

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
            "Codex Superpowers was not installed: the OpenAI-curated catalog is "
            "unavailable.",
            result.stdout,
        )
        self.assertIn(
            "Run `codex login`, then `codex plugin add "
            "superpowers@openai-curated`.",
            result.stdout,
        )
        self.assertIn(
            "Error: plugin superpowers@openai-curated was not found", result.stderr
        )

    def crit_fixture(
        self, installed_version: str | None = None
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
        payload = repo / "crit-linux-amd64"
        self.executable(payload, "printf 'crit v9.9.9 (fixture)\\n'\n")
        checksum = subprocess.run(
            ["shasum", "-a", "256", str(payload)],
            text=True,
            capture_output=True,
            check=True,
        ).stdout.split()[0]
        self.executable(
            bin_dir / "uname",
            """
            case "$1" in
                -s) printf 'Linux\\n' ;;
                -m) printf 'x86_64\\n' ;;
                *) printf 'Linux\\n' ;;
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
        self.assertIn(
            "/v9.9.9/crit-linux-amd64", (repo / "commands.log").read_text()
        )
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

    def update_fixture(
        self, *, branch: str = "main", upstream: str = "origin/main", dirty: bool = False
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
                "pull --ff-only") printf 'git pull --ff-only\\n' >> "$TEST_LOG" ;;
            esac
            """,
        )
        self.executable(bin_dir / "chezmoi", "printf 'chezmoi %s\\n' \"$*\" >> \"$TEST_LOG\"\n")
        self.executable(bin_dir / "mise", "printf 'mise %s\\n' \"$*\" >> \"$TEST_LOG\"\n")
        self.executable(
            bin_dir / "herdr",
            """
            if [ "$*" = "status server --json" ]; then
                printf '{"status":"not_running"}\\n'
            fi
            """,
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
            "Notice: local source not pulled (tracked files have staged or "
            "unstaged changes); run 'git -C ",
            result.stdout,
        )
        self.assertIn(" pull' to fetch remote updates.", result.stdout)

    def test_agent_launchers_do_not_hardcode_model_ids(self) -> None:
        herdr = (ROOT / "home/dot_local/bin/common/executable_herdr-agents").read_text()
        fanout = (
            ROOT / "home/dot_local/bin/common/executable_agent-fanout"
        ).read_text()

        for text in (herdr, fanout):
            self.assertNotIn("claude-fable-5", text)
            self.assertNotIn("gpt-5.6", text)
            self.assertNotIn("model_reasoning_effort=", text)
        self.assertIn('--profile "${HERDR_AGENTS_CODEX_PROFILE:-standard}"', herdr)
        self.assertIn("model-profiles.env", fanout)

    def test_agent_fanout_applies_profile_args_from_generated_fragment(self) -> None:
        repo = self.temp_dir / "fanout-profile-repo"
        output_dir = repo / "output"
        bin_dir = self.temp_dir / "fanout-profile-bin"
        repo.mkdir()
        shutil.copy(
            ROOT / "home/dot_local/bin/common/executable_agent-fanout",
            repo / "agent-fanout",
        )
        self.executable(bin_dir / "codex", "exit 0\n")
        profile_env = self.temp_dir / "model-profiles.env"
        profile_env.write_text(
            'MODEL_PROFILE_INTERACTIVE="deep"\n'
            'MODEL_PROFILE_EXPRESS_CLAUDE_ARGS="--model haiku --effort low"\n'
            'MODEL_PROFILE_EXPRESS_CODEX_ARGS="--profile express"\n'
        )
        env = {
            **os.environ,
            "PATH": f"{bin_dir}:{os.environ['PATH']}",
            "AGENT_FANOUT_PROFILE_ENV": str(profile_env),
        }

        result = self.run_test_command(
            [
                "bash",
                "./agent-fanout",
                "--dry-run",
                "--no-claude",
                "--profile",
                "express",
                "--output-dir",
                str(output_dir),
                "prompt",
            ],
            cwd=repo,
            env=env,
        )

        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn(
            "DRY RUN: codex --profile express exec --full-auto <prompt>",
            (output_dir / "codex.log").read_text(),
        )

        result = self.run_test_command(
            [
                "bash",
                "./agent-fanout",
                "--dry-run",
                "--no-claude",
                "--profile",
                "nope",
                "--output-dir",
                str(output_dir),
                "prompt",
            ],
            cwd=repo,
            env=env,
        )

        self.assertEqual(2, result.returncode, result.stderr)
        self.assertIn("Unknown model profile: nope", result.stderr)

    def test_agent_fanout_preserves_caller_umask_for_child_agents(self) -> None:
        repo = self.temp_dir / "fanout-umask-repo"
        bin_dir = self.temp_dir / "fanout-umask-bin"
        observed_umask = self.temp_dir / "child-umask.txt"
        repo.mkdir()
        shutil.copy(
            ROOT / "home/dot_local/bin/common/executable_agent-fanout",
            repo / "agent-fanout",
        )
        self.executable(bin_dir / "codex", 'umask > "$OBSERVED_UMASK"\n')

        result = self.run_test_command(
            [
                "bash",
                "-c",
                'umask 0022; exec bash ./agent-fanout --no-claude "secret prompt"',
            ],
            cwd=repo,
            env={
                **os.environ,
                "PATH": f"{bin_dir}:{os.environ['PATH']}",
                "OBSERVED_UMASK": str(observed_umask),
            },
        )

        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual("0022", observed_umask.read_text().strip())

    def test_agent_fanout_restricts_preexisting_output_artifacts(self) -> None:
        repo = self.temp_dir / "fanout-existing-repo"
        output_dir = repo / "output"
        bin_dir = self.temp_dir / "fanout-existing-bin"
        repo.mkdir()
        output_dir.mkdir()
        shutil.copy(
            ROOT / "home/dot_local/bin/common/executable_agent-fanout",
            repo / "agent-fanout",
        )
        self.executable(bin_dir / "codex", "exit 0\n")
        artifacts = [
            output_dir / name for name in ("prompt.txt", "codex.log", "summary.txt")
        ]
        for artifact in artifacts:
            artifact.write_text("old public content\n")
            artifact.chmod(0o644)

        result = self.run_test_command(
            [
                "bash",
                "./agent-fanout",
                "--dry-run",
                "--no-claude",
                "--output-dir",
                str(output_dir),
                "secret",
            ],
            cwd=repo,
            env={**os.environ, "PATH": f"{bin_dir}:{os.environ['PATH']}"},
        )

        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual(0o700, stat.S_IMODE(output_dir.stat().st_mode))
        for artifact in artifacts:
            self.assertEqual(0o600, stat.S_IMODE(artifact.stat().st_mode), artifact)

    def test_agent_fanout_refuses_symlink_artifacts(self) -> None:
        repo = self.temp_dir / "fanout-symlink-repo"
        output_dir = repo / "output"
        bin_dir = self.temp_dir / "fanout-symlink-bin"
        target = self.temp_dir / "must-not-change.txt"
        repo.mkdir()
        output_dir.mkdir()
        target.write_text("preserve me\n")
        (output_dir / "codex.log").symlink_to(target)
        shutil.copy(
            ROOT / "home/dot_local/bin/common/executable_agent-fanout",
            repo / "agent-fanout",
        )
        self.executable(bin_dir / "codex", "exit 0\n")

        result = self.run_test_command(
            [
                "bash",
                "./agent-fanout",
                "--dry-run",
                "--no-claude",
                "--output-dir",
                str(output_dir),
                "secret",
            ],
            cwd=repo,
            env={**os.environ, "PATH": f"{bin_dir}:{os.environ['PATH']}"},
        )

        self.assertNotEqual(0, result.returncode)
        self.assertIn("Refusing unsafe artifact path", result.stderr)
        self.assertEqual("preserve me\n", target.read_text())

    def doctor_environment(
        self, *, fail: str = "", os_name: str = "Linux"
    ) -> dict[str, str]:
        fixture_name = (fail or "healthy").replace(":", "-").replace(" ", "-")
        bin_dir = self.temp_dir / f"doctor-bin-{fixture_name}-{os_name}"
        log = self.temp_dir / "doctor.log"
        bin_dir.mkdir()
        missing = fail.removeprefix("missing:") if fail.startswith("missing:") else ""
        for command in ("git", "chezmoi", "mise", "uv", "gh", "brew"):
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
        return {
            **os.environ,
            "HOME": str(home),
            "PATH": f"{bin_dir}:/usr/bin:/bin",
            "FAIL_COMMAND": fail,
            "TEST_LOG": str(log),
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
                self.assertEqual(
                    expected_status, result.returncode, result.stdout + result.stderr
                )
                self.assertIn(summary, result.stdout)

        result = self.run_test_command(
            ["bash", str(ROOT / "scripts/check-tools.sh")],
            env=self.doctor_environment(fail="missing:brew", os_name="Darwin"),
        )
        self.assertNotEqual(0, result.returncode)
        self.assertIn("required missing: brew", result.stderr)

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

        self.executable(
            repo / "scripts/check-agent-runtime.py", "printf 'runtime healthy\\n'\n"
        )
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

        result = self.run_test_command(
            ["make", "doctor", "REPAIR=1"], cwd=repo, env=env
        )

        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn("repair=1", result.stdout)

    def upgrade_fixture(
        self, fail_phase: str, os_name: str = "Linux"
    ) -> tuple[Path, dict[str, str]]:
        repo = self.temp_dir / f"upgrade-{fail_phase}"
        bin_dir = repo / "bin"
        home = repo / "home"
        (repo / "scripts/lib").mkdir(parents=True)
        home.mkdir()
        shutil.copy(
            ROOT / "scripts/upgrade-tools.sh", repo / "scripts/upgrade-tools.sh"
        )
        shutil.copy(
            ROOT / "scripts/lib/installer-pins.sh",
            repo / "scripts/lib/installer-pins.sh",
        )
        # Hermetic downloads keep the pin-bump phase off the network in tests.
        self.executable(
            bin_dir / "curl",
            """
            printf 'curl %s\n' "$*" >> "$TEST_LOG"
            request="$*"
            out=""
            while [ "$#" -gt 0 ]; do
                if [ "$1" = "-o" ]; then out="$2"; shift; fi
                shift
            done
            [ -n "$out" ] || exit 1
            case "$request" in
                *tode.sh/install*|*terminal-browser.sh/install*)
                    printf 'VERSION="v9.9.9"\nCHANNEL="stable"\n' > "$out"
                    ;;
                *crit-linux-amd64*) printf 'fixture amd64\n' > "$out" ;;
                *crit-linux-arm64*) printf 'fixture arm64\n' > "$out" ;;
            esac
            """,
        )
        self.executable(
            repo / "scripts/update-agent-assets.sh",
            """
            printf 'assets\n' >> "$TEST_LOG"
            [[ "$FAIL_PHASE" != assets ]]
            """,
        )
        self.executable(bin_dir / "uname", f"printf '{os_name}\\n'\n")
        self.executable(
            bin_dir / "brew",
            """
            printf 'brew %s\n' "$*" >> "$TEST_LOG"
            [[ "$FAIL_PHASE:$1" != homebrew:update ]]
            """,
        )
        self.executable(
            bin_dir / "mise",
            """
            printf 'mise %s\n' "$*" >> "$TEST_LOG"
            case "$1" in
                self-update) [[ "$FAIL_PHASE" != mise_self ]] ;;
                ls) [[ "$FAIL_PHASE" != mise_inventory ]] && printf 'python 3.13 fixture\nfd 10.3.0 fixture\nhttp:bats 1.13.0 fixture\nhttp:gcloud 575.0.1 fixture\n' ;;
                install) [[ "$FAIL_PHASE" != mise_install ]] ;;
                use)
                    case "$*" in
                        *npm:@openai/codex*) [[ "$FAIL_PHASE" != codex_cli ]] ;;
                        *npm:@anthropic-ai/claude-code*) [[ "$FAIL_PHASE" != claude_cli ]] ;;
                    esac
                    ;;
                upgrade) [[ "$FAIL_PHASE" != mise_upgrade ]] ;;
                exec)
                    shift
                    [[ "$1" == node ]] || exit 90
                    shift
                    [[ "$1" == -- ]] || exit 91
                    shift
                    [[ "$1" == npm ]] || exit 92
                    shift
                    printf 'npm %s\n' "$*" >> "$TEST_LOG"
                    [[ "$1" == view ]] && printf '1.2.3\n'
                    true
                    ;;
                where)
                    [[ "$FAIL_PHASE" != mise_where ]] || exit 9
                    mkdir -p "$HOME/mise-prefix"; printf '%s\n' "$HOME/mise-prefix"
                    ;;
            esac
            """,
        )
        self.executable(
            bin_dir / "npm",
            """
            printf 'npm %s\n' "$*" >> "$TEST_LOG"
            [[ "$1" == view ]] && printf '1.2.3\n'
            [[ "$1" != list ]]
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
            case "$*" in
                *issues/1115*) printf 'open\n' ;;
                *tomasz-tomczyk/crit/releases/latest*) printf 'v9.9.9\n' ;;
                *musistudio/claude-code-router/releases/latest*) printf 'v3.0.15\n' ;;
            esac
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
            "FAIL_PHASE": fail_phase,
            "HOME": str(home),
            "PATH": f"{bin_dir}:/usr/bin:/bin",
            "TEST_LOG": str(log),
        }
        return repo, env

    def test_upgrade_required_failures_are_nonzero_and_independent(self) -> None:
        cases = (
            ("homebrew", "Darwin", []),
            ("mise_self", "Linux", []),
            ("mise_inventory", "Linux", []),
            ("mise_install", "Linux", []),
            ("mise_upgrade", "Linux", []),
            ("codex_cli", "Linux", []),
            ("claude_cli", "Linux", []),
            ("mise_where", "Linux", []),
            ("assets", "Linux", []),
            ("uv", "Linux", []),
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
        self.assertIn(
            "Skipping mise self-update: managed by package manager.", result.stdout
        )
        self.assertIn(
            "Skipping mise upgrade for pinned HTTP tool: http:bats.", result.stdout
        )
        self.assertIn(
            "Skipping mise upgrade for pinned HTTP tool: http:gcloud.", result.stdout
        )
        log = (repo / "commands.log").read_text()
        self.assertNotIn("mise self-update --yes", log)
        self.assertIn("mise upgrade --bump --yes --before 7d python", log)
        self.assertNotIn("mise upgrade --bump --yes --before 7d fd", log)
        self.assertNotIn("mise upgrade --bump --yes --before 7d http:", log)
        self.assertIn(
            "mise use --global --pin --yes --minimum-release-age 0s npm:@openai/codex@1.2.3",
            log,
        )
        codex_install = next(
            line
            for line in log.splitlines()
            if line.startswith("npm install -g") and "@openai/codex@1.2.3" in line
        )
        claude_install = next(
            line
            for line in log.splitlines()
            if line.startswith("npm install -g")
            and "@anthropic-ai/claude-code@1.2.3" in line
        )
        self.assertIn("--ignore-scripts", codex_install)
        self.assertNotIn("--allow-scripts", codex_install)
        self.assertIn("--ignore-scripts=false", claude_install)
        self.assertIn("--allow-scripts=@anthropic-ai/claude-code", claude_install)

        repo, env = self.upgrade_fixture("mise_upgrade")
        marker = repo / "lib/mise/mise-self-update-instructions.toml"
        marker.parent.mkdir(parents=True)
        marker.write_text('message = "managed by fixture package manager"\n')
        result = self.run_test_command(
            ["bash", "scripts/upgrade-tools.sh"], cwd=repo, env=env
        )
        self.assertEqual(1, result.returncode, result.stdout + result.stderr)
        self.assertIn("required failure: mise inventory/install/upgrade", result.stderr)

    def test_upgrade_uses_current_mise_node_after_runtime_replacement(self) -> None:
        """Reject ambient npm after mise replaces the active Node runtime."""
        repo, env = self.upgrade_fixture("none")
        fallback_bin = repo / "fallback-bin"
        self.executable(
            fallback_bin / "npm",
            """
            printf 'fallback npm %s\n' "$*" >> "$TEST_LOG"
            exit 86
            """,
        )
        removed_node_bin = repo / "removed-node-26.6.0" / "bin"
        env["PATH"] = f"{removed_node_bin}:{fallback_bin}:{env['PATH']}"

        result = self.run_test_command(
            ["bash", "scripts/upgrade-tools.sh"], cwd=repo, env=env
        )

        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        log = (repo / "commands.log").read_text()
        self.assertNotIn("fallback npm", log)
        self.assertIn("mise exec node -- npm view @openai/codex version", log)
        self.assertIn(
            "mise exec node -- npm view @anthropic-ai/claude-code version", log
        )
        self.assertRegex(
            log, r"mise exec node -- npm install -g .* @openai/codex@1\.2\.3"
        )
        self.assertRegex(
            log,
            r"mise exec node -- npm install -g .* @anthropic-ai/claude-code@1\.2\.3",
        )

    def test_upgrade_github_extensions_are_warning_only(self) -> None:
        repo, env = self.upgrade_fixture("gh")
        result = self.run_test_command(
            ["bash", "scripts/upgrade-tools.sh"],
            cwd=repo,
            env=env,
        )

        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn("optional warnings: 1", result.stdout)

    def test_upgrade_bumps_terminal_and_crit_pins_from_fetched_artifacts(self) -> None:
        repo, env = self.upgrade_fixture("none")

        result = self.run_test_command(
            ["bash", "scripts/upgrade-tools.sh"],
            cwd=repo,
            env=env,
        )

        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn(
            "Pinned tode v9.9.9, terminal-browser v9.9.9, and crit v9.9.9",
            result.stdout,
        )
        pins = (repo / "scripts/lib/installer-pins.sh").read_text()
        self.assertIn('TERMINAL_CODE_PIN_VERSION="v9.9.9"', pins)
        self.assertIn('TERMINAL_BROWSER_PIN_VERSION="v9.9.9"', pins)
        self.assertIn('CRIT_PIN_VERSION="v9.9.9"', pins)
        self.assertRegex(pins, r'TERMINAL_CODE_INSTALLER_SHA256="[0-9a-f]{64}"')
        self.assertRegex(pins, r'CRIT_LINUX_AMD64_SHA256="[0-9a-f]{64}"')
        self.assertRegex(pins, r'CRIT_LINUX_ARM64_SHA256="[0-9a-f]{64}"')
        log = (repo / "commands.log").read_text()
        self.assertIn("curl -fsSL https://tode.sh/install", log)
        self.assertIn("curl -fsSL https://terminal-browser.sh/install", log)
        self.assertIn("crit-linux-amd64", log)
        self.assertIn("crit-linux-arm64", log)

    def test_upgrade_skips_ccr_notice_when_gh_is_unavailable(self) -> None:
        repo, env = self.upgrade_fixture("none")
        (repo / "bin/gh").unlink()
        for command in ("awk", "bash", "dirname", "mkdir", "mktemp", "rm"):
            source = shutil.which(command)
            self.assertIsNotNone(source)
            (repo / f"bin/{command}").symlink_to(source)
        env["PATH"] = str(repo / "bin")

        result = self.run_test_command(
            ["bash", "scripts/upgrade-tools.sh"],
            cwd=repo,
            env=env,
        )

        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertNotIn("CCR gate G1", result.stdout)
        self.assertNotIn("CCR latest release", result.stdout)

    def test_upgrade_reports_ccr_adoption_gate_values(self) -> None:
        repo, env = self.upgrade_fixture("none")

        result = self.run_test_command(
            ["bash", "scripts/upgrade-tools.sh"],
            cwd=repo,
            env=env,
        )

        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn("CCR gate G1 (#1115): open", result.stdout)
        self.assertIn("CCR latest release: v3.0.15", result.stdout)
        self.assertIn("G2/G3 require manual primary-source verification", result.stdout)


if __name__ == "__main__":
    unittest.main()
