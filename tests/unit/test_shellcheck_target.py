#!/usr/bin/env python3
"""Pin the required ShellCheck CI step to `make shellcheck`, and that target to its two groups and both checks.

The step runs a target the pull request itself can change (U38's threat table, residual (a)), so the wiring is pinned
here: the step runs exactly `make shellcheck`; the target's dry run names exactly the installer group and the masked
group, each linted with the root .shellcheckrc (no --norc) and scripts/ci/masked-dirname-check.sh; and the target, run
in a scratch repository, fails on an SC2312 finding or a masked dirname in either group, and refuses a group that lists
no file, no bash script, or (the installer group) a file that is not a bash script.

The target first refuses a shellcheck or shfmt that is not the version home/dot_mise/config.toml pins (U97);
tests/unit/test_pinned_lint_tools.py checks that guard and every consumer of the pins.
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
from scratch_git import git_init  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
WORKFLOW = ROOT / ".github/workflows/test.yaml"
MAKEFILE = ROOT / "Makefile"
MISE_CONFIG = ROOT / "home/dot_mise/config.toml"
GUARD = ROOT / "scripts/ci/pinned-tool-version.sh"


def on_ci_runner() -> bool:
    """scripts/lib/ci-runner.sh decides, never the generic CI variable an agent shell exports."""
    probe = 'source "$1" && is_ci_runner'
    return (
        subprocess.run(["bash", "-c", probe, "_", str(ROOT / "scripts/lib/ci-runner.sh")], check=False).returncode == 0
    )


INSTALLER_GROUP = ["setup.sh", "install/*.sh", "install/**/*.sh", "scripts/*.sh", "scripts/lib/*"]
MASKED_GROUP = ["scripts/orchestrator/*", "home/dot_local/bin/common/executable_*"]
GIT_ENV = {"GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t", "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t"}
# SC2312 only: printf masks the substitution's status. The default checks (--norc) pass it.
MASKED_RETURN = '#!/usr/bin/env bash\nprintf "%s\\n" "$(false)"\n'
# The U31 shape SC2312 exempts; only masked-dirname-check.sh reports it.
MASKED_DIRNAME = '#!/usr/bin/env bash\ndir=$(cd "$(dirname "$0")" && pwd -P) || exit 1\necho "${dir}"\n'
CLEAN = '#!/usr/bin/env bash\nprintf "%s\\n" "${1:-}"\n'


def run_steps(workflow: str) -> list[tuple[str, str]]:
    """Return (name, run) for each step of the workflow, run as written after `run:`."""
    steps, name = [], None
    for line in workflow.splitlines():
        if match := re.match(r"^\s*- name: (.*)$", line):
            name = match.group(1).strip()
        elif (match := re.match(r"^\s*run: (.*)$", line)) and name is not None:
            steps.append((name, match.group(1).strip()))
    return steps


class ShellCheckStepTest(unittest.TestCase):
    def test_the_required_step_runs_exactly_make_shellcheck(self):
        steps = run_steps(WORKFLOW.read_text())
        shellcheck = [run for name, run in steps if name == "Run `ShellCheck`"]
        self.assertEqual(["make shellcheck"], shellcheck)
        # No other step lints shell, so the target is the only ShellCheck the workflow runs. The one other step that
        # names it installs the pin and runs nothing else (tests/unit/test_pinned_lint_tools.py holds its text, U97).
        install = 'scripts/ci/install-pinned-lint-tools.sh "${RUNNER_TEMP}/statusline-mise" shellcheck shfmt'
        others = [(name, run) for name, run in steps if "shellcheck" in run.lower() and name != "Run `ShellCheck`"]
        self.assertEqual([("Put the pinned `ShellCheck` and `shfmt` on PATH", install)], others)

    def test_the_target_dry_run_names_both_groups_and_both_checks(self):
        result = subprocess.run(
            ["make", "-n", "-s", "shellcheck"], cwd=ROOT, capture_output=True, text=True, timeout=60, check=True
        )
        lines = result.stdout.splitlines()
        # The version guard runs first, on the one pin file, before either group is linted.
        self.assertEqual(
            "scripts/ci/pinned-tool-version.sh home/dot_mise/config.toml shellcheck shfmt", lines[0], result.stdout
        )
        commands = [line for line in lines if line.startswith("bash ")]
        self.assertEqual(2, len(commands), result.stdout)
        for command, mode, group in zip(commands, ("every", "bash"), (INSTALLER_GROUP, MASKED_GROUP)):
            with self.subTest(mode=mode):
                self.assertTrue(command.endswith(" _ " + " ".join([mode] + [f"'{p}'" for p in group])), command)
                self.assertIn("shellcheck -x $files || status=1;", command)
                self.assertIn("scripts/ci/masked-dirname-check.sh $files || status=1;", command)
                self.assertNotIn("--norc", command)
                self.assertNotIn("xargs", command)
                self.assertIn('echo "shellcheck: no file in $*" >&2; exit 1;', command)
                self.assertIn('echo "shellcheck: no bash script in $*" >&2; exit 1;', command)
        self.assertEqual(
            ["enable=check-extra-masked-returns", "source-path=SCRIPTDIR"],
            (ROOT / ".shellcheckrc").read_text().splitlines(),
        )


@unittest.skipUnless(
    (shutil.which("shellcheck") and shutil.which("shfmt")) or on_ci_runner(),
    "needs shellcheck and shfmt off the CI runner",
)
class ShellCheckTargetBehaviourTest(unittest.TestCase):
    """The target runs in a scratch repository holding the Makefile's two inputs and the files under test."""

    def setUp(self):
        self.repo = Path(tempfile.mkdtemp(prefix="shellcheck-target-test-"))
        (self.repo / "scripts/ci").mkdir(parents=True)
        shutil.copy2(ROOT / "scripts/ci/masked-dirname-check.sh", self.repo / "scripts/ci/masked-dirname-check.sh")
        shutil.copy2(GUARD, self.repo / "scripts/ci/pinned-tool-version.sh")
        (self.repo / "home/dot_mise").mkdir(parents=True)
        shutil.copy2(MISE_CONFIG, self.repo / "home/dot_mise/config.toml")
        shutil.copy2(ROOT / ".shellcheckrc", self.repo / ".shellcheckrc")
        for name, body in (
            ("clean.sh", CLEAN),
            ("masked-return.sh", MASKED_RETURN),
            ("masked-dirname.sh", MASKED_DIRNAME),
            ("notes.txt", "not a script\n"),
            ("tool.py", "#!/usr/bin/env python3\nprint('ok')\n"),
        ):
            (self.repo / name).write_text(body)
        git_init(self.repo, env=os.environ | GIT_ENV)
        self.git("add", "-A")
        self.git("commit", "-q", "-m", "fixture")

    def tearDown(self):
        shutil.rmtree(self.repo)

    def git(self, *args):
        subprocess.run(
            ["git", "-C", str(self.repo), "-c", "commit.gpgsign=false", *args], check=True, env=os.environ | GIT_ENV
        )

    def make(self, installer: str, masked: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                "make",
                "-s",
                "-f",
                str(MAKEFILE),
                "shellcheck",
                f"SHELLCHECK_INSTALLER_GROUP={installer}",
                f"SHELLCHECK_MASKED_GROUP={masked}",
            ],
            cwd=self.repo,
            capture_output=True,
            text=True,
            timeout=120,
            check=False,
        )

    def test_the_fixtures_show_what_only_the_rc_and_the_dirname_check_catch(self):
        # The instrument can fail: without the rc, ShellCheck passes both findings the target must refuse.
        for name in ("masked-return.sh", "masked-dirname.sh"):
            with self.subTest(name=name):
                plain = subprocess.run(
                    ["shellcheck", "--norc", "-x", name], cwd=self.repo, capture_output=True, text=True, check=False
                )
                self.assertEqual(0, plain.returncode, plain.stdout)

    def test_clean_groups_pass_and_the_masked_group_skips_a_non_bash_script(self):
        result = self.make("clean.sh", "clean.sh tool.py")

        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        linted = [line for line in result.stdout.splitlines() if not line.startswith("==> ")]
        self.assertEqual(["clean.sh", "clean.sh"], linted)

    def test_either_group_fails_on_an_sc2312_finding_or_a_masked_dirname(self):
        for finding, expected in (
            ("masked-return.sh", "In masked-return.sh line 2:"),
            (
                "masked-dirname.sh",
                "masked-dirname.sh:2: a command substitution inside another one loses its status",
            ),
        ):
            for installer, masked in ((finding, "clean.sh"), ("clean.sh", finding)):
                with self.subTest(installer=installer, masked=masked):
                    result = self.make(installer, masked)

                    self.assertNotEqual(0, result.returncode, result.stdout + result.stderr)
                    self.assertIn(expected, result.stdout + result.stderr)
                    if finding == "masked-return.sh":
                        self.assertIn("SC2312", result.stdout)

    def test_a_group_with_no_file_or_no_bash_script_is_refused(self):
        for installer, masked, message in (
            ("absent/*", "clean.sh", "shellcheck: no file in absent/*"),
            ("clean.sh", "absent/*", "shellcheck: no file in absent/*"),
            ("notes.txt", "clean.sh", "shellcheck: no bash script in notes.txt"),
            ("clean.sh", "tool.py", "shellcheck: no bash script in tool.py"),
        ):
            with self.subTest(installer=installer, masked=masked):
                result = self.make(installer, masked)

                self.assertNotEqual(0, result.returncode, result.stdout + result.stderr)
                self.assertIn(message, result.stderr)

    def test_the_installer_group_refuses_a_listed_file_that_is_not_a_bash_script(self):
        result = self.make("clean.sh tool.py", "clean.sh")

        self.assertNotEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn("shellcheck: not a bash script, in clean.sh tool.py:\ntool.py\n", result.stderr)


if __name__ == "__main__":
    unittest.main()
