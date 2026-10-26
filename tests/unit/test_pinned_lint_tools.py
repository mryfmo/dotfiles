"""One version per lint tool, read by every consumer (regime-cutover U97).

ShellCheck, shfmt, ruff and prettier each have one pin in home/dot_mise/config.toml: the `version` of the
`[tools."http:shellcheck"]`, `[tools."http:shfmt"]` and `[tools."http:ruff"]` tables (with each platform's sha256) and
the exact `"npm:prettier"` version. Hosts install them through mise; CI's test jobs install them from a copy of that
file; and scripts/ci/pinned-tool-version.sh, which the lint targets and CI's lint steps run first, refuses a tool on
PATH of any other version, naming both. These tests hold each consumer to the config's value, so a version written
anywhere else, or a lint gate that skips the guard, fails here. A fake tool on PATH stands in for each version.
"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import tempfile
import tomllib
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WORKFLOW = ROOT / ".github/workflows/test.yaml"
MAKEFILE = ROOT / "Makefile"
MISE_CONFIG = ROOT / "home/dot_mise/config.toml"
GUARD = ROOT / "scripts/ci/pinned-tool-version.sh"
# Each lint tool's mise key and the banner its `--version` prints, as the real releases print it.
TOOLS = {
    "shellcheck": ("http:shellcheck", "ShellCheck - shell script analysis tool\nversion: {v}\nlicense: GNU GPLv3\n"),
    "shfmt": ("http:shfmt", "v{v}\n"),
    "ruff": ("http:ruff", "ruff {v}\n"),
    "prettier": ("npm:prettier", "{v}\n"),
}
# The files that run or name a lint tool and must hold no version of their own.
CONSUMERS = (
    MAKEFILE,
    GUARD,
    ROOT / "scripts/lint-comparisons.py",
    ROOT / "scripts/ci/masked-dirname-check.sh",
    ROOT / "tests/unit/test_sandbox_portability.py",
)
COPY = '"${RUNNER_TEMP}/statusline-mise"'
INSTALL_STEP = "Put the pinned `ShellCheck` and `shfmt` on PATH"
INSTALL_RUN = (
    f"mise -C {COPY} install http:shellcheck http:shfmt\n"
    f'dirname "$(mise -C {COPY} which --tool http:shellcheck shellcheck)" >> "${{GITHUB_PATH}}"\n'
    f'dirname "$(mise -C {COPY} which --tool http:shfmt shfmt)" >> "${{GITHUB_PATH}}"\n'
)
SHFMT_RUN = (
    "scripts/ci/pinned-tool-version.sh home/dot_mise/config.toml shfmt\n"
    "git ls-files -- ':(glob)install/**/*.sh' ':(glob)scripts/**/*.sh' | xargs shfmt -i 4 -sr -d\n"
)
FORMAT_RUN = (
    f"mise -C {COPY} x http:ruff -- \\\n"
    '  sh -c \'cd "${GITHUB_WORKSPACE}" && scripts/ci/pinned-tool-version.sh home/dot_mise/config.toml ruff && '
    'git ls-files -z "*.py" | xargs -0 ruff format --config ruff.toml --check\'\n'
    f"mise -C {COPY} x node npm:prettier -- \\\n"
    '  sh -c \'cd "${GITHUB_WORKSPACE}" && scripts/ci/pinned-tool-version.sh home/dot_mise/config.toml prettier && '
    'git ls-files -z "*.md" | xargs -0 prettier --check\'\n'
)


def pins(config: Path = MISE_CONFIG) -> dict[str, str]:
    """Each lint tool's pinned version, read with tomllib."""
    tools = tomllib.loads(config.read_text())["tools"]
    found = {}
    for tool, (key, _) in TOOLS.items():
        entry = tools[key]
        found[tool] = entry if isinstance(entry, str) else entry["version"]
    return found


def pin_line(tool: str, version: str) -> str:
    """The config text that holds a tool's pin."""
    key = TOOLS[tool][0]
    if key.startswith("http:"):
        return f'[tools."{key}"]\nversion = "{version}"'
    return f'"{key}" = "{version}"'


def commands(run: str) -> list[str]:
    """A run block's lines that are not comments."""
    return [line for line in run.splitlines() if not line.lstrip().startswith("#")]


def step_blocks(workflow: str) -> list[dict[str, str]]:
    """Each step as {name, if, run}, `run: |` blocks whole and dedented; text only, because the unit-test run in CI
    has no PyYAML."""
    steps: list[dict[str, str]] = []
    lines = workflow.splitlines()
    index = 0
    while index < len(lines):
        start = re.match(r"^(\s*)- name: (.*)$", lines[index])
        index += 1
        if not start:
            continue
        key_indent = len(start.group(1)) + 2
        step = {"name": start.group(2).strip(), "if": "", "run": ""}
        steps.append(step)
        while index < len(lines) and not re.match(r"^\s*- name: ", lines[index]):
            line = lines[index]
            index += 1
            if line.strip() and len(line) - len(line.lstrip()) < key_indent:
                index -= 1
                break
            if match := re.match(rf"^ {{{key_indent}}}if: (.*)$", line):
                step["if"] = match.group(1).strip()
            elif match := re.match(rf"^ {{{key_indent}}}run: (.*)$", line):
                if match.group(1).strip() != "|":
                    step["run"] = match.group(1).strip() + "\n"
                    continue
                body = []
                while index < len(lines) and (
                    not lines[index].strip() or len(lines[index]) - len(lines[index].lstrip()) > key_indent
                ):
                    body.append(lines[index])
                    index += 1
                while body and not body[-1].strip():
                    body.pop()
                indent = min(len(line) - len(line.lstrip()) for line in body if line.strip())
                step["run"] = "".join(f"{line[indent:]}\n" for line in body)
    return steps


class PinnedLintToolsTest(unittest.TestCase):
    def setUp(self):
        self.scratch = Path(tempfile.mkdtemp(prefix="pinned-lint-tools-test-"))
        self.bin = self.scratch / "bin"
        self.bin.mkdir()

    def tearDown(self):
        shutil.rmtree(self.scratch)

    def fake(self, tool: str, version: str | None, *, fails: bool = False) -> None:
        """A `tool` on PATH whose --version prints the real banner for `version` (none: no version line); every
        call is logged to <tool>.log, and any other call succeeds without output."""
        banner = TOOLS[tool][1].format(v=version) if version is not None else f"{tool}\n"
        body = "exit 3" if fails else f"printf '%s' '{banner}'"
        path = self.bin / tool
        path.write_text(f'#!/bin/sh\necho "$*" >> "$0.log"\nif [ "$1" = --version ]; then {body}; fi\nexit 0\n')
        path.chmod(0o755)

    def env(self) -> dict:
        return os.environ | {"PATH": f"{self.bin}:{os.environ['PATH']}"}

    def guard(self, config: Path, *tools: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [str(GUARD), str(config), *tools],
            cwd=ROOT,
            env=self.env(),
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )

    def make(self, target: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["make", "-s", target], cwd=ROOT, env=self.env(), capture_output=True, text=True, timeout=120, check=False
        )

    def test_each_lint_tool_has_one_exact_pin(self):
        tools = tomllib.loads(MISE_CONFIG.read_text())["tools"]
        for tool, (key, _) in TOOLS.items():
            with self.subTest(tool):
                self.assertEqual([key], [name for name in tools if re.search(rf"(^|[:/]){tool}$", name)])
                self.assertRegex(pins()[tool], r"^\d+(\.\d+)+$")

    def test_the_guard_accepts_each_pin_and_refuses_any_other_version_naming_both(self):
        for tool, version in pins().items():
            key = TOOLS[tool][0]
            with self.subTest(tool):
                self.fake(tool, version)
                accepted = self.guard(MISE_CONFIG, tool)
                self.assertEqual(0, accepted.returncode, accepted.stderr)
                self.assertEqual(f"==> {tool} {version}, the version {MISE_CONFIG} pins\n", accepted.stdout)
                for installed, shown in (("0.0.1", "0.0.1"), ("99.0.0", "99.0.0"), (f"{version}.1", f"{version}.1")):
                    self.fake(tool, installed)
                    refused = self.guard(MISE_CONFIG, tool)
                    self.assertEqual(1, refused.returncode, refused.stdout)
                    self.assertIn(
                        f"the {tool} on PATH is version {shown}, but {MISE_CONFIG} pins {tool} {version}; "
                        f'run "mise install {key}"',
                        refused.stderr,
                    )
                    self.assertEqual("", refused.stdout)
                self.fake(tool, None)
                self.assertIn(f"is version unknown, but {MISE_CONFIG}", self.guard(MISE_CONFIG, tool).stderr)
                self.fake(tool, version, fails=True)
                failed = self.guard(MISE_CONFIG, tool)
                self.assertEqual(1, failed.returncode)
                self.assertIn(f'"{tool} --version" failed; {MISE_CONFIG} pins {tool} {version}', failed.stderr)

    def test_every_tool_is_checked_and_one_skew_fails_the_whole_call(self):
        versions = pins()
        for tool, version in versions.items():
            self.fake(tool, version)
        self.fake("ruff", "0.0.1")
        result = self.guard(MISE_CONFIG, *TOOLS)
        self.assertEqual(1, result.returncode)
        accepted = [f"==> {tool} {versions[tool]}, the version {MISE_CONFIG} pins" for tool in TOOLS if tool != "ruff"]
        self.assertEqual(accepted, result.stdout.splitlines())
        self.assertIn("the ruff on PATH is version 0.0.1", result.stderr)

    def test_the_guard_reads_each_pin_from_the_config_it_is_given(self):
        # A copy of the real config with one pin moved: the guard follows the file, so its reader and tomllib's
        # agree, and the guard holds no version of its own.
        text = MISE_CONFIG.read_text()
        for tool, version in pins().items():
            with self.subTest(tool):
                moved = self.scratch / "moved.toml"
                moved.write_text(text.replace(pin_line(tool, version), pin_line(tool, "7.7.7")))
                self.assertEqual("7.7.7", pins(moved)[tool])
                self.fake(tool, "7.7.7")
                self.assertEqual(0, self.guard(moved, tool).returncode)
                self.fake(tool, version)
                self.assertEqual(1, self.guard(moved, tool).returncode)
                for name, body in (
                    ("no pin", text.replace(pin_line(tool, version), pin_line(tool, version).replace(tool, "other"))),
                    ("latest", text.replace(pin_line(tool, version), pin_line(tool, "latest"))),
                    (
                        "twice",
                        text.replace(pin_line(tool, version), f'{pin_line(tool, version)}\nversion = "{version}"')
                        if TOOLS[tool][0].startswith("http:")
                        else text.replace(
                            pin_line(tool, version), f"{pin_line(tool, version)}\n{pin_line(tool, version)}"
                        ),
                    ),
                ):
                    broken = self.scratch / "broken.toml"
                    broken.write_text(body)
                    refused = self.guard(broken, tool)
                    self.assertEqual(1, refused.returncode, f"{name}: {refused.stdout}")
                    self.assertIn(f"{broken} pins no {tool} version", refused.stderr, name)

    def test_the_guard_refuses_a_call_it_cannot_check(self):
        for args, status, message in (
            ((str(MISE_CONFIG),), 2, "usage: pinned-tool-version.sh"),
            ((str(MISE_CONFIG), "black"), 2, "black is not a pinned lint tool"),
            ((str(self.scratch / "absent.toml"), "ruff"), 1, "cannot read the mise config"),
        ):
            with self.subTest(args=args):
                result = subprocess.run(
                    [str(GUARD), *args], cwd=ROOT, capture_output=True, text=True, timeout=30, check=False
                )
                self.assertEqual(status, result.returncode)
                self.assertIn(message, result.stderr)

    def test_no_consumer_holds_a_version_of_its_own(self):
        workflow = "\n".join(line for step in step_blocks(WORKFLOW.read_text()) for line in commands(step["run"]))
        for tool, version in pins().items():
            with self.subTest(tool):
                for path in CONSUMERS:
                    code = "\n".join(
                        line for line in path.read_text().splitlines() if not line.lstrip().startswith("#")
                    )
                    self.assertNotIn(version, code, path)
                self.assertNotIn(version, workflow)
                self.assertNotRegex(workflow, rf"\b{tool}@")

    def test_each_lint_target_runs_the_guard_first(self):
        for target, tools in (("shellcheck", "shellcheck shfmt"), ("format", "shfmt ruff prettier")):
            with self.subTest(target):
                result = subprocess.run(
                    ["make", "-n", "-s", target], cwd=ROOT, capture_output=True, text=True, timeout=60, check=True
                )
                self.assertEqual(
                    f"scripts/ci/pinned-tool-version.sh home/dot_mise/config.toml {tools}",
                    result.stdout.splitlines()[0],
                )

    def test_a_lint_target_stops_at_the_guard_before_it_lints(self):
        versions = pins()
        for target, skewed, others in (
            ("shellcheck", "shellcheck", ("shfmt",)),
            ("shellcheck", "shfmt", ("shellcheck",)),
            ("format", "shfmt", ("ruff", "prettier")),
            ("format", "ruff", ("shfmt", "prettier")),
            ("format", "prettier", ("shfmt", "ruff")),
        ):
            with self.subTest(target=target, skewed=skewed):
                for log in self.bin.glob("*.log"):
                    log.unlink()
                self.fake(skewed, "0.0.1")
                for tool in others:
                    self.fake(tool, versions[tool])
                result = self.make(target)
                self.assertNotEqual(0, result.returncode)
                self.assertIn(
                    f"the {skewed} on PATH is version 0.0.1, but home/dot_mise/config.toml pins", result.stderr
                )
                self.assertNotIn("==> ShellCheck with .shellcheckrc", result.stdout)
                # Each tool was asked its version and nothing else: no file was linted or formatted.
                for tool in (skewed, *others):
                    self.assertEqual("--version\n", (self.bin / f"{tool}.log").read_text(), tool)

    def test_ci_installs_the_pins_from_the_copied_config_and_nothing_else(self):
        blocks = step_blocks(WORKFLOW.read_text())
        steps = {step["name"]: step for step in blocks}
        names = [step["name"] for step in blocks]
        self.assertEqual(len(names), len(steps), "step names are unique")
        self.assertIn(
            'cp home/dot_mise/config.toml "${statusline_mise_dir}/mise.toml"',
            steps["Prepare statusline tool config"]["run"],
        )
        self.assertIn(
            f"mise -C {COPY} install http:ruff npm:prettier", commands(steps["Install statusline tools"]["run"])
        )
        self.assertEqual(INSTALL_RUN, steps[INSTALL_STEP]["run"])
        self.assertEqual(SHFMT_RUN, "".join(f"{line}\n" for line in commands(steps["Run `shfmt`"]["run"])))
        self.assertEqual(
            FORMAT_RUN, "".join(f"{line}\n" for line in commands(steps["Check Python and Markdown formatting"]["run"]))
        )
        self.assertEqual("make shellcheck\n", steps["Run `ShellCheck`"]["run"])
        # Every row of the matrix runs them: the condition is the one every test step has.
        for name in (INSTALL_STEP, "Run `shfmt`", "Check Python and Markdown formatting", "Run `ShellCheck`"):
            self.assertEqual("${{ steps.decide.outputs.should_test == 'true' }}", steps[name]["if"], name)
        order = [
            names.index(name)
            for name in (
                "Prepare statusline tool config",
                "Setup mise for statusline smoke",
                "Install statusline tools",
                INSTALL_STEP,
                "Run `shfmt`",
                "Check Python and Markdown formatting",
                "Run `ShellCheck`",
            )
        ]
        self.assertEqual(sorted(order), order)
        # No other step's commands install or run one of these tools: apt and brew lines included.
        for tools, expected in (
            (("shellcheck", "shfmt"), [INSTALL_STEP, "Run `shfmt`", "Run `ShellCheck`"]),
            (("ruff", "prettier"), ["Install statusline tools", "Check Python and Markdown formatting"]),
        ):
            mentions = [
                step["name"]
                for step in blocks
                if any(re.search(rf"\b{tool}\b(?![.\w])", line) for line in commands(step["run"]) for tool in tools)
            ]
            self.assertEqual(expected, mentions, tools)
        install = steps["Install tools"]["run"]
        self.assertIn("brew install bash bats-core gawk parallel\n", install)
        self.assertIn("sudo apt-get install -y bats curl iproute2 parallel ruby\n", install)


if __name__ == "__main__":
    unittest.main()
