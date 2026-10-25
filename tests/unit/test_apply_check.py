#!/usr/bin/env python3
"""Verify the disposable apply check (U82): `make apply-check` picks docker or podman, refuses without either and
starts one network-less container per system; scripts/apply-check.sh refuses outside a CI runner and fails on a tree
that does not apply; CI runs `make apply-check` itself on every pull request."""

from __future__ import annotations

import datetime
import json
import os
import shutil
import subprocess
import tempfile
import textwrap
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts/apply-check.sh"
WORKFLOW = ROOT / ".github/workflows/apply-check.yml"
MAKE = shutil.which("make")
CHEZMOI = shutil.which("chezmoi")
# The CI step's credential: make apply-check must keep it on the host.
STEP_CREDENTIAL = "credential-of-the-ci-step"


import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))  # dotted runs too; discover -s tests/unit already has it
from agent_home_isolation import isolate_agent_homes, restore_agent_homes


def setUpModule() -> None:
    isolate_agent_homes()


def tearDownModule() -> None:
    restore_agent_homes()


def published_hours_ago(hours: float) -> str:
    moment = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=hours)
    return moment.strftime("%Y-%m-%dT%H:%M:%SZ")


class MakeApplyCheckTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = Path(tempfile.mkdtemp(prefix="apply-check-test-"))
        self.bin_dir = self.temp_dir / "bin"
        self.bin_dir.mkdir()
        self.log = self.temp_dir / "calls.log"
        # Only these tools are on PATH, so a host's own docker, podman, curl or gh never answers.
        for tool in ("awk", "bash", "cat", "date", "env", "git"):
            (self.bin_dir / tool).symlink_to(shutil.which(tool))
        page = self.temp_dir / "releases.json"
        release = {"tag_name": "v2.73.0", "draft": False, "prerelease": False, "published_at": published_hours_ago(100)}
        # Indented as the API answers: github-release.sh reads the top-level fields by their indentation.
        page.write_text(json.dumps([release], indent=2) + "\n")
        self.executable("curl", f'printf "curl %s\\n" "$*" >> "{self.log}"\ncat "{page}"\n')
        self.executable("gh", "exit 1\n")

    def tearDown(self) -> None:
        shutil.rmtree(self.temp_dir)

    def executable(self, name: str, body: str) -> None:
        path = self.bin_dir / name
        path.write_text("#!/bin/bash\n" + textwrap.dedent(body))
        path.chmod(0o755)

    def make(self, **env: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [str(MAKE), "--no-print-directory", "apply-check"],
            cwd=ROOT,
            env={"PATH": str(self.bin_dir), "HOME": str(self.temp_dir), **env},
            text=True,
            capture_output=True,
            check=False,
        )

    @unittest.skipUnless(MAKE, "make is not installed")
    def test_refuses_without_docker_or_podman_before_anything_runs(self) -> None:
        result = self.make()

        self.assertNotEqual(0, result.returncode)
        self.assertIn("no container engine: install docker or podman (neither is on PATH)", result.stderr)
        self.assertFalse(self.log.exists())

    @unittest.skipUnless(MAKE, "make is not installed")
    def test_runs_a_fresh_client_and_server_in_podman_without_network_or_credentials(self) -> None:
        dockerfile_id = subprocess.run(
            ["git", "hash-object", "Dockerfile"], cwd=ROOT, text=True, capture_output=True, check=True
        ).stdout.strip()
        # An image make docker-image built from this Dockerfile: reused, so nothing is verified or built.
        self.executable(
            "podman",
            f"""
            printf 'podman %s\\n' "$*" >> "{self.log}"
            case "$1:$*" in
                inspect:*chezmoi.version*) printf '2.73.0\\n' ;;
                inspect:*chezmoi.sha256*) printf '%s\\n' "{"a" * 64}" ;;
                inspect:*dotfiles.dockerfile*) printf '%s\\n' "{dockerfile_id}" ;;
                run:*--system\\ server*) exit "${{SERVER_EXIT:-0}}" ;;
            esac
            exit 0
            """,
        )
        for server_exit, summary in (("0", "client=passed server=passed"), ("1", "client=passed server=failed")):
            with self.subTest(server_exit=server_exit):
                self.log.unlink(missing_ok=True)

                result = self.make(SERVER_EXIT=server_exit, GITHUB_TOKEN=STEP_CREDENTIAL)

                self.assertEqual(server_exit != "0", result.returncode != 0, result.stderr)
                self.assertIn(f"make apply-check: {summary}\n", result.stdout)
                runs = [line for line in self.log.read_text().splitlines() if line.startswith("podman run ")]
                self.assertEqual(
                    [
                        "podman run --rm --network none -e GITHUB_ACTIONS=true -e RUNNER_TEMP=/tmp "
                        f"-v {ROOT}:/src:ro dotfiles bash /src/scripts/apply-check.sh --system {system}"
                        for system in ("client", "server")
                    ],
                    runs,
                )
                self.assertNotIn("podman build", self.log.read_text())
                self.assertNotIn(STEP_CREDENTIAL, self.log.read_text())
                self.assertNotIn("GITHUB_TOKEN", self.log.read_text())


class ApplyCheckScriptTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = Path(tempfile.mkdtemp(prefix="apply-check-script-test-"))
        self.runner_temp = self.temp_dir / "runner"
        self.runner_temp.mkdir()

    def tearDown(self) -> None:
        shutil.rmtree(self.temp_dir)

    def run_script(self, script: Path, env: dict[str, str]) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["/bin/bash", str(script), "--system", "client", "--chezmoi", str(CHEZMOI or "chezmoi")],
            env={"PATH": "/usr/bin:/bin", "HOME": str(self.temp_dir), "RUNNER_TEMP": str(self.runner_temp), **env},
            text=True,
            capture_output=True,
            check=False,
        )

    def test_refuses_in_an_agent_shell_that_only_exports_ci(self) -> None:
        result = self.run_script(SCRIPT, {"CI": "true"})

        self.assertEqual(2, result.returncode)
        self.assertIn("refusing to run outside a CI runner", result.stderr)
        self.assertEqual([], list(self.runner_temp.iterdir()))

    @unittest.skipUnless(CHEZMOI, "chezmoi is not installed")
    def test_a_tree_that_does_not_apply_fails_and_the_same_tree_without_the_defect_passes(self) -> None:
        tree = self.temp_dir / "tree"
        tree.mkdir()
        for name in (".chezmoiroot", "home", "scripts"):
            source = ROOT / name
            if source.is_dir():
                shutil.copytree(source, tree / name, symlinks=True)
            else:
                shutil.copy2(source, tree / name)
        script = tree / "scripts/apply-check.sh"
        # The test's own PATH: the modify scripts and check-agent-runtime.py need the python3 (3.11 or newer) it has.
        runner = {"GITHUB_ACTIONS": "true", "PATH": os.environ["PATH"]}

        passed = self.run_script(script, runner)

        self.assertEqual(0, passed.returncode, passed.stdout[-4000:] + passed.stderr[-4000:])
        self.assertIn(
            "apply-check summary (client): init=passed apply=passed verify=passed unmanaged-file=passed shell-rc=passed "
            "chezmoi-doctor=passed agent-runtime=passed\n",
            passed.stdout,
        )

        (tree / "home/dot_apply-check-defect.tmpl").write_text("{{ .apply_check_missing_key.value }}\n")

        failed = self.run_script(script, runner)

        self.assertEqual(1, failed.returncode)
        self.assertIn("apply-check summary (client): init=passed apply=failed\n", failed.stdout)
        # The scratch HOME and the source copy are gone either way.
        self.assertEqual([], list(self.runner_temp.iterdir()))


class ApplyCheckWorkflowTest(unittest.TestCase):
    def test_every_pull_request_and_main_push_runs_make_apply_check_unconditionally(self) -> None:
        text = WORKFLOW.read_text()
        on = text.split("\non:\n", 1)[1].split("\n\n", 1)[0]
        self.assertIn("  push:\n    branches: [main]\n", on)
        self.assertIn("  pull_request:\n    branches: [main]\n", on)
        self.assertNotIn("paths", on)
        body = text.split("\njobs:\n", 1)[1]
        lines = [line.strip() for line in body.splitlines()]
        # One job, no condition anywhere that could skip the command and still report success.
        self.assertEqual(
            ["apply-container:"],
            [line.strip() for line in body.splitlines() if line.startswith("  ") and not line.startswith("   ")],
        )
        for key in ("if:", "- if:", "needs:", "continue-on-error:"):
            with self.subTest(key=key):
                self.assertFalse([line for line in lines if line.startswith(key)])
        self.assertEqual(["run: make apply-check"], [line for line in lines if line.startswith("run:")])


if __name__ == "__main__":
    unittest.main()
