#!/usr/bin/env python3
"""The repository takes its CI-only paths on a GitHub Actions runner only, never because an agent shell exports CI=true.

omp's bash tool exports CI=true (with npm_config_yes, GIT_EDITOR and GIT_TERMINAL_PROMPT) into every command it runs on
the operator's hosts. scripts/lib/ci-runner.sh is the one shell definition; setup.sh carries a copy and
home/.chezmoi.yaml.tmpl states the same test in template syntax. These tests run every consumer under the agent shell's
environment and under a runner's, and keep the three statements equal.
"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))  # dotted runs too; discover -s tests/unit already has it
from scratch_git import quiet_git  # noqa: E402

quiet_git()  # U100: no git command in this module's scratch repositories starts background maintenance

ROOT = Path(__file__).resolve().parents[2]
LIB = ROOT / "scripts/lib/ci-runner.sh"
GUARD = ROOT / "home/.chezmoiscripts/common/run_before_00-refuse-dirty-source.sh.tmpl"
DECRYPT = ROOT / "home/.chezmoiscripts/common/run_before_01-decrypt-private-key.sh.tmpl"
CONFIG = ROOT / "home/.chezmoi.yaml.tmpl"
CHEZMOI = shutil.which("chezmoi")
# What omp's bash tool exports into every command (dist/cli.js of @oh-my-pi/pi-coding-agent 18.12.6, as of 18.11.3).
AGENT_SHELL = {"CI": "true", "npm_config_yes": "true", "GIT_EDITOR": "true", "GIT_TERMINAL_PROMPT": "0"}
RUNNER_VARIABLES = ("CI", "GITHUB_ACTIONS", "RUNNER_TEMP", *AGENT_SHELL)


def host_env(**extra: str) -> dict[str, str]:
    """This process's environment without any CI or runner variable, plus `extra`."""
    env = {key: value for key, value in os.environ.items() if key not in RUNNER_VARIABLES}
    return env | extra


class CiRunnerDefinitionTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = Path(tempfile.mkdtemp(prefix="ci-runner-test-"))
        self.cases = {
            "host": host_env(),
            "agent shell": host_env(**AGENT_SHELL),
            "GITHUB_ACTIONS without RUNNER_TEMP": host_env(CI="true", GITHUB_ACTIONS="true"),
            "RUNNER_TEMP without GITHUB_ACTIONS": host_env(CI="true", RUNNER_TEMP=str(self.temp_dir)),
            "GITHUB_ACTIONS=1": host_env(GITHUB_ACTIONS="1", RUNNER_TEMP=str(self.temp_dir)),
            "runner": host_env(CI="true", GITHUB_ACTIONS="true", RUNNER_TEMP=str(self.temp_dir)),
        }

    def tearDown(self) -> None:
        shutil.rmtree(self.temp_dir)

    def shell_decides(self, script: Path, env: dict[str, str]) -> bool:
        probe = 'source "$1"; set +e; is_ci_runner'
        result = subprocess.run(["bash", "-c", probe, "_", str(script)], env=env, cwd=ROOT, check=False)
        return result.returncode == 0

    def test_only_a_github_actions_runner_counts(self) -> None:
        for label, env in self.cases.items():
            with self.subTest(label):
                self.assertEqual(label == "runner", self.shell_decides(LIB, env))

    def test_setup_sh_carries_the_library_function_unchanged(self) -> None:
        helper = LIB.read_text()
        body = helper[helper.index("#\n# @description Succeed on a GitHub Actions runner") :]
        setup = (ROOT / "setup.sh").read_text()
        begin = "# --- ci-runner.sh begin ---\n"
        copy = setup[setup.index(begin) + len(begin) : setup.index("# --- ci-runner.sh end ---\n")]
        self.assertEqual(body, copy)
        for label, env in self.cases.items():
            with self.subTest(label):
                self.assertEqual(label == "runner", self.shell_decides(ROOT / "setup.sh", env))

    def test_setup_sh_never_executes_the_ci_value(self) -> None:
        # The old is_ci ran "${CI}" as a command: CI=1 failed with 127 and CI=yes ran yes forever.
        marker = self.temp_dir / "ran"
        fake = self.temp_dir / "bin"
        fake.mkdir()
        (fake / "yes").write_text(f"#!/bin/sh\ntouch {marker}\n")
        (fake / "yes").chmod(0o755)
        for value in ("1", "yes", "true"):
            with self.subTest(value):
                env = host_env(CI=value, PATH=f"{fake}:{os.environ['PATH']}")
                result = subprocess.run(
                    ["bash", "-c", "source ./setup.sh; set +e; is_ci_or_not_tty; echo rc=$?"],
                    env=env,
                    cwd=ROOT,
                    stdin=subprocess.DEVNULL,
                    capture_output=True,
                    text=True,
                    timeout=30,
                    check=False,
                )
                self.assertEqual("rc=0\n", result.stdout, result.stderr)
                self.assertNotIn("command not found", result.stderr)
                self.assertFalse(marker.exists())

    @unittest.skipUnless(CHEZMOI, "chezmoi is not installed")
    def test_the_config_template_agrees_with_the_library(self) -> None:
        for label, env in self.cases.items():
            with self.subTest(label):
                result = subprocess.run(
                    [
                        *(str(CHEZMOI), "--source", str(ROOT / "home"), "--config", str(self.temp_dir / "none.yaml")),
                        *("--cache", str(self.temp_dir / "cache"), "--persistent-state", str(self.temp_dir / "state")),
                        *("execute-template", "--init", "--no-tty", "--promptString", "Full name=Operator"),
                        *("--override-data", '{"email": "e@example.invalid", "system": "client"}'),
                    ],
                    input=CONFIG.read_text(),
                    env=env | {"HOME": str(self.temp_dir)},
                    capture_output=True,
                    text=True,
                    check=True,
                )
                runner = label == "runner"
                self.assertEqual(runner, '    name: "CI"' in result.stdout.splitlines(), result.stdout)
                # Off the runner the config keeps age encryption; an agent shell's make init must not drop it.
                self.assertEqual(not runner, 'encryption: "age"' in result.stdout.splitlines(), result.stdout)

    def test_no_repository_code_reads_the_generic_ci_variable(self) -> None:
        tracked = subprocess.run(
            ["git", "ls-files", "-z", "--", "home", "install", "scripts", "setup.sh", "Makefile"],
            cwd=ROOT,
            capture_output=True,
            check=True,
        ).stdout.split(b"\0")
        reader = re.compile(r'\$\{?CI\b|env "CI"|environ(?:\.get)?[(\[]"CI"')
        offenders = []
        for name in filter(None, tracked):
            path = ROOT / name.decode()
            if path.is_file() and not path.is_symlink():
                text = path.read_text(errors="replace")
                offenders += [
                    f"{name.decode()}:{n}" for n, line in enumerate(text.splitlines(), 1) if reader.search(line)
                ]
        self.assertEqual([], offenders)


@unittest.skipUnless(CHEZMOI and shutil.which("git"), "needs chezmoi and git")
class DirtySourceGuardTest(unittest.TestCase):
    """The rendered guard, run against a scratch clone whose home/ holds an untracked file."""

    def setUp(self) -> None:
        self.temp_dir = Path(tempfile.mkdtemp(prefix="dirty-guard-test-"))
        self.repo = self.temp_dir / "repo"
        (self.repo / "home").mkdir(parents=True)
        (self.repo / "scripts/lib").mkdir(parents=True)
        shutil.copy(LIB, self.repo / "scripts/lib/ci-runner.sh")
        (self.repo / "home/tracked").write_text("tracked\n")
        git = ["git", "-C", str(self.repo), "-c", "user.name=t", "-c", "user.email=t@t", "-c", "commit.gpgsign=false"]
        subprocess.run([*git, "init", "--quiet", "--initial-branch=main"], check=True)
        subprocess.run([*git, "add", "."], check=True)
        subprocess.run([*git, "commit", "--quiet", "-m", "base"], check=True)
        rendered = subprocess.run(
            [
                *(str(CHEZMOI), "--source", str(self.repo / "home"), "--config", str(self.temp_dir / "none.yaml")),
                *("--cache", str(self.temp_dir / "cache"), "--persistent-state", str(self.temp_dir / "state")),
                "execute-template",
            ],
            input=GUARD.read_text(),
            env=host_env(HOME=str(self.temp_dir)),
            capture_output=True,
            text=True,
            check=True,
        ).stdout
        self.guard = self.temp_dir / "guard.sh"
        self.guard.write_text(rendered)
        (self.repo / "home/untracked").write_text("not merged\n")

    def tearDown(self) -> None:
        shutil.rmtree(self.temp_dir)

    def run_guard(self, env: dict[str, str]) -> subprocess.CompletedProcess[str]:
        return subprocess.run(["bash", str(self.guard)], env=env, capture_output=True, text=True, check=False)

    def test_an_agent_shell_exporting_ci_true_is_refused(self) -> None:
        for label, env in (("host", host_env()), ("agent shell", host_env(**AGENT_SHELL))):
            with self.subTest(label):
                result = self.run_guard(env)
                self.assertEqual(1, result.returncode, result.stderr)

    def test_a_github_actions_runner_is_skipped(self) -> None:
        result = self.run_guard(host_env(CI="true", GITHUB_ACTIONS="true", RUNNER_TEMP=str(self.temp_dir)))
        self.assertEqual(0, result.returncode, result.stderr)


class MacosInstallerTest(unittest.TestCase):
    """The run_once installers with a fake brew: nothing installed, one untrusted tap with one installed formula."""

    FAKE_BREW = """
        brew() {
            case "$*" in
                "list --formula --full-name") echo other/tap/tool ;;
                "list --cask --full-name") ;;
                list\\ *) return 1 ;;
                "untrust --tap") printf 'Untrusted taps:\\n  other/tap\\n' ;;
                *) echo "brew $*" ;;
            esac
        }
    """

    def brew_calls(self, script: str, function: str, env: dict[str, str]) -> list[str]:
        result = subprocess.run(
            ["bash", "-c", f'{self.FAKE_BREW}\nsource "$1"; {function}', "_", f"install/macos/common/{script}"],
            env=env,
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
        return [line.split()[1] for line in result.stdout.splitlines() if line.startswith("brew ")]

    def test_an_agent_shell_installs_and_trusts_no_tap(self) -> None:
        env = host_env(**AGENT_SHELL)
        self.assertEqual(["install"], self.brew_calls("dependencies.sh", "install_brew_packages", env))
        self.assertEqual(["install"], self.brew_calls("docker.sh", "install_docker", env))
        self.assertEqual(["install"], self.brew_calls("misc.sh", "install_brew_cask_packages", env))
        self.assertEqual([], self.brew_calls("brew.sh", "handle_ci_untrusted_taps", env))

    def test_a_runner_validates_and_trusts_its_image_taps(self) -> None:
        with tempfile.TemporaryDirectory() as runner_temp:
            env = host_env(CI="true", GITHUB_ACTIONS="true", RUNNER_TEMP=runner_temp)
            self.assertEqual(["info"], self.brew_calls("dependencies.sh", "install_brew_packages", env))
            self.assertEqual(["info"], self.brew_calls("docker.sh", "install_docker", env))
            self.assertEqual(["trust"], self.brew_calls("brew.sh", "handle_ci_untrusted_taps", env))


@unittest.skipUnless(CHEZMOI, "chezmoi is not installed")
class DecryptRetryTest(unittest.TestCase):
    """An apply without a terminal cannot ask for the age passphrase; the next apply must ask again."""

    def test_every_apply_retries_a_skipped_restore(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            temp_dir = Path(temp)
            source = temp_dir / "repo/home"
            (source / ".chezmoiscripts").mkdir(parents=True)
            shutil.copy(DECRYPT, source / ".chezmoiscripts" / DECRYPT.name)
            (temp_dir / "repo/scripts/lib").mkdir(parents=True)
            shutil.copy(LIB, temp_dir / "repo/scripts/lib/ci-runner.sh")
            (source / ".key.txt.age").write_text("")
            (temp_dir / "dest").mkdir()
            command = [
                *(str(CHEZMOI), "--source", str(source), "--destination", str(temp_dir / "dest")),
                *("--config", str(temp_dir / "none.yaml"), "--cache", str(temp_dir / "cache")),
                *("--persistent-state", str(temp_dir / "state")),
            ]
            env = host_env(**AGENT_SHELL, HOME=str(temp_dir))
            for attempt in ("first", "second"):
                with self.subTest(attempt):
                    applied = subprocess.run(
                        [*command, "apply", "--no-tty"],
                        env=env,
                        stdin=subprocess.DEVNULL,
                        capture_output=True,
                        text=True,
                        check=False,
                    )
                    self.assertEqual(0, applied.returncode, applied.stderr)
                    status = subprocess.run(
                        [*command, "status"],
                        env=env,
                        stdin=subprocess.DEVNULL,
                        capture_output=True,
                        text=True,
                        check=True,
                    )
                    self.assertIn("decrypt-private-key.sh", status.stdout)


if __name__ == "__main__":
    unittest.main()
