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
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))  # dotted runs too; discover -s tests/unit already has it
from scratch_git import git_init  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
WORKFLOW = ROOT / ".github/workflows/test.yaml"
MAKEFILE = ROOT / "Makefile"
MISE_CONFIG = ROOT / "home/dot_mise/config.toml"
GUARD = ROOT / "scripts/ci/pinned-tool-version.sh"
RUNNER = ROOT / "scripts/ci/run-on-lint-files.sh"
# The three checks, each on its file set: the commands make format and CI's steps both run.
SET_CHECKS = (
    "scripts/ci/run-on-lint-files.sh shell shfmt -i 4 -sr -d",
    "scripts/ci/run-on-lint-files.sh python ruff format --config ruff.toml --check",
    "scripts/ci/run-on-lint-files.sh markdown prettier --check",
)
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
    ROOT / "scripts/ci/install-pinned-lint-tools.sh",
    ROOT / "scripts/ci/run-on-lint-files.sh",
    ROOT / "scripts/lint-comparisons.py",
    ROOT / "scripts/ci/masked-dirname-check.sh",
    ROOT / "tests/unit/test_sandbox_portability.py",
)
COPY = '"${RUNNER_TEMP}/statusline-mise"'
COMMAND_SECONDS = 60
INSTALL_STEP = "Put the pinned `ShellCheck` and `shfmt` on PATH"
INSTALL = ROOT / "scripts/ci/install-pinned-lint-tools.sh"
# The step's whole run: every install and lookup is checked inside the script, none in the YAML (round-1 audit).
INSTALL_RUN = f"scripts/ci/install-pinned-lint-tools.sh {COPY} shellcheck shfmt\n"
SHFMT_RUN = (
    "scripts/ci/pinned-tool-version.sh home/dot_mise/config.toml shfmt\n"
    "scripts/ci/run-on-lint-files.sh shell shfmt -i 4 -sr -d\n"
)
FORMAT_RUN = (
    f"mise -C {COPY} x http:ruff -- \\\n"
    '  sh -c \'cd "${GITHUB_WORKSPACE}" && scripts/ci/pinned-tool-version.sh home/dot_mise/config.toml ruff && '
    "scripts/ci/run-on-lint-files.sh python ruff format --config ruff.toml --check'\n"
    f"mise -C {COPY} x node npm:prettier -- \\\n"
    '  sh -c \'cd "${GITHUB_WORKSPACE}" && scripts/ci/pinned-tool-version.sh home/dot_mise/config.toml prettier && '
    "scripts/ci/run-on-lint-files.sh markdown prettier --check'\n"
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

    def fake(self, tool: str, version: str | None, *, fails: bool = False, status: int = 0) -> None:
        """A `tool` on PATH whose --version prints the real banner for `version` (none: no version line) and exits
        `status`; fails: prints nothing and exits 3. Every call is logged to <tool>.log, and any other call succeeds
        without output."""
        banner = TOOLS[tool][1].format(v=version) if version is not None else f"{tool}\n"
        body = "exit 3" if fails else f"printf '%s' '{banner}'; exit {status}"
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

    def test_a_producer_that_prints_a_valid_value_and_fails_is_refused(self):
        # Round-2 audit of 473b63a1: each producer's status decides, not only its output. awk printing the right pin
        # and exiting non-zero, and a tool printing the pinned banner and exiting non-zero, are each refused.
        real_awk = shutil.which("awk")
        awk = self.bin / "awk"
        awk.write_text(f'#!/bin/sh\n"{real_awk}" "$@"\nexit 4\n')
        awk.chmod(0o755)
        for tool, version in pins().items():
            with self.subTest(tool, producer="awk"):
                self.fake(tool, version)
                refused = self.guard(MISE_CONFIG, tool)
                self.assertEqual(1, refused.returncode, refused.stdout)
                self.assertIn(f"cannot read {MISE_CONFIG}", refused.stderr)
                self.assertEqual("", refused.stdout)
        awk.unlink()
        for tool, version in pins().items():
            with self.subTest(tool, producer="--version"):
                self.fake(tool, version, status=5)
                refused = self.guard(MISE_CONFIG, tool)
                self.assertEqual(1, refused.returncode, refused.stdout)
                self.assertIn(f'"{tool} --version" failed; {MISE_CONFIG} pins {tool} {version}', refused.stderr)
                self.assertEqual("", refused.stdout)

    def test_no_script_lets_a_variable_select_a_lint_tool(self):
        # Round-2 audit of 473b63a1: the guard checks the tool on PATH, so a consumer that honoured SHFMT (or the like)
        # could run a binary the guard never saw. No script, Makefile rule or test reads such a variable.
        pattern = re.compile(
            r"\$\{?(SHFMT|SHELLCHECK|RUFF|PRETTIER)\b|environ(?:\.get)?\(?\[?[\"'](SHFMT|SHELLCHECK|RUFF|PRETTIER)[\"']"
        )
        listed = (
            subprocess.run(
                ["git", "ls-files", "-z", "--", "Makefile", "scripts", "install", "home", "tests", ".github"],
                cwd=ROOT,
                capture_output=True,
                check=True,
                timeout=60,
            )
            .stdout.decode()
            .split("\0")
        )
        found = []
        for name in filter(None, listed):
            path = ROOT / name
            if path == Path(__file__).resolve() or path.is_symlink() or not path.is_file():
                continue
            text = path.read_text(errors="replace")
            found += [f"{name}:{number}" for number, line in enumerate(text.splitlines(), 1) if pattern.search(line)]
        self.assertEqual([], found)

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
                    # Round-6 audit of 000e9faa: an indented duplicate was not read, so the first pin passed alone.
                    (
                        "twice, indented",
                        text.replace(pin_line(tool, version), f'{pin_line(tool, version)}\n    version = "{version}"')
                        if TOOLS[tool][0].startswith("http:")
                        else text.replace(
                            pin_line(tool, version), f"{pin_line(tool, version)}\n  {pin_line(tool, version)}"
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
        self.assertIn(
            "timeout --kill-after=10 180 sudo apt-get -o Acquire::http::Timeout=15 -o Acquire::Retries=3"
            " install -y bats curl iproute2 parallel ruby\n",
            install,
        )


BAD_SHELL = "#!/usr/bin/env bash\nif true;then echo  bad;fi\n"


def dotted(paths: list[str]) -> list[str]:
    return [f"./{path}" for path in paths]


def runnable(tool: str, cwd: Path) -> bool:
    """Whether the tool answers --version from cwd: a mise shim with no config there is on PATH but runs nothing."""
    if not shutil.which(tool):
        return False
    probe = subprocess.run([tool, "--version"], cwd=cwd, capture_output=True, timeout=60, check=False)
    return probe.returncode == 0


# The shell set of LintFileSetTest's repository: its .sh files, its scripts by bash or sh shebang, nothing excluded.
SHELL_SET = [
    # Paths git prints in C style (core.quotePath=true): a tab, a double quote and a non-ASCII byte, each decoded.
    "home/caf\u00e9.sh",
    "home/dot_local/bin/executable_tool",
    # Round-4 audit of 3b293cd5: the interpreter is a token, so a comment naming zsh does not exclude the script.
    "home/env-comment",
    "home/env-split",
    "home/locked/inner.sh",
    "home/modify_config.yml",
    "home/outside.sh",
    'home/quote"d.sh',
    "home/tab\tname.sh",
    "install/common/tracked.sh",
    "scripts/ci/pinned-tool-version.sh",
    "scripts/ci/run-on-lint-files.sh",
    "scripts/lib/deep.sh",
]
EXCLUDED = (
    ".orchestration/tasks/copy.sh",
    "home/prompt.zsh",
    "home/zsh-script.sh",
    "home/zsh-abs",
    "home/zsh-env",
    "tests/install/t.bats",
    "home/run_once.sh.tmpl",
    "home/executable_py",
    "home/uv-tool",
    "home/ruby-tool",
    "home/link.sh",
    "home/image.png",
)


class InstallPinnedLintToolsTest(unittest.TestCase):
    """scripts/ci/install-pinned-lint-tools.sh against a fake mise: every install and lookup is checked before PATH."""

    def setUp(self):
        self.scratch = Path(tempfile.mkdtemp(prefix="install-pinned-lint-tools-")).resolve()
        self.addCleanup(shutil.rmtree, self.scratch)
        (self.scratch / "bin").mkdir()
        self.installs = self.scratch / "installs"
        for tool in ("shellcheck", "shfmt"):
            binary = self.installs / tool / tool
            binary.parent.mkdir(parents=True)
            binary.write_text("#!/bin/sh\n")
            binary.chmod(0o755)
        self.github_path = self.scratch / "github_path"
        self.github_path.write_text("")
        mise = self.scratch / "bin/mise"
        # `mise -C <dir> install <keys>` and `mise -C <dir> which --tool <key> <tool>`; WHICH_<tool> overrides the
        # path printed, WHICH_RC_<tool> the status; every call is logged.
        mise.write_text(
            "#!/bin/bash\n"
            'printf "%s\\n" "$*" >> "$MISE_LOG"\n'
            'case "$3" in\n'
            '  install) exit "${INSTALL_RC:-0}" ;;\n'
            '  which) tool=$6; rc_var="WHICH_RC_$tool"; path_var="WHICH_$tool"\n'
            '    [ "${!rc_var:-0}" -eq 0 ] || exit "${!rc_var}"\n'
            '    printf "%s\\n" "${!path_var-$INSTALLS/$tool/$tool}" ;;\n'
            "esac\n"
        )
        mise.chmod(0o755)

    def run_install(self, *tools: str, **extra: str) -> subprocess.CompletedProcess[str]:
        env = os.environ | {
            "PATH": f"{self.scratch / 'bin'}:{os.environ['PATH']}",
            "GITHUB_PATH": str(self.github_path),
            "INSTALLS": str(self.installs),
            "MISE_LOG": str(self.scratch / "mise.log"),
            **extra,
        }
        return subprocess.run(
            [str(INSTALL), str(self.scratch / "copy"), *tools],
            env=env,
            capture_output=True,
            text=True,
            timeout=COMMAND_SECONDS,
            check=False,
        )

    def test_each_checked_binary_directory_goes_on_path(self):
        result = self.run_install("shellcheck", "shfmt")
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual(
            [str(self.installs / "shellcheck"), str(self.installs / "shfmt")], self.github_path.read_text().splitlines()
        )
        copy = self.scratch / "copy"
        self.assertEqual(
            [
                f"-C {copy} install http:shellcheck http:shfmt",
                f"-C {copy} which --tool http:shellcheck shellcheck",
                f"-C {copy} which --tool http:shfmt shfmt",
            ],
            (self.scratch / "mise.log").read_text().splitlines(),
        )

    def test_a_failed_install_or_lookup_puts_nothing_on_path(self):
        not_executable = self.scratch / "plain"
        not_executable.write_text("")
        for name, extra, message in (
            ("install fails", {"INSTALL_RC": "1"}, "mise install http:shellcheck http:shfmt failed"),
            ("lookup fails", {"WHICH_RC_shfmt": "37"}, "mise which --tool http:shfmt shfmt failed"),
            ("lookup prints nothing", {"WHICH_shfmt": ""}, "mise named nothing for shfmt"),
            ("lookup prints a relative path", {"WHICH_shfmt": "shfmt"}, "mise named shfmt for shfmt"),
            ("lookup names no executable", {"WHICH_shfmt": str(not_executable)}, f"mise named {not_executable}"),
            ("lookup names a directory", {"WHICH_shfmt": str(self.installs)}, f"mise named {self.installs}"),
        ):
            with self.subTest(name):
                self.github_path.write_text("")
                result = self.run_install("shellcheck", "shfmt", **extra)
                self.assertEqual(1, result.returncode, result.stdout)
                self.assertIn(message, result.stderr)
                # Not even shellcheck's directory, though its lookup succeeded: nothing is appended before all pass.
                self.assertEqual("", self.github_path.read_text())

    def test_a_call_it_cannot_serve_installs_nothing(self):
        for name, tools, extra, message in (
            ("no tool", (), {}, "usage:"),
            ("unknown tool", ("ruff",), {}, "ruff is not a pinned lint tool this step installs"),
            ("no GITHUB_PATH", ("shfmt",), {"GITHUB_PATH": ""}, "usage:"),
        ):
            with self.subTest(name):
                (self.scratch / "mise.log").unlink(missing_ok=True)
                result = self.run_install(*tools, **extra)
                self.assertEqual(2, result.returncode)
                self.assertIn(message, result.stderr)
                self.assertFalse((self.scratch / "mise.log").exists())


class LintFileSetTest(unittest.TestCase):
    """make format and CI check the same tracked files, from scripts/ci/run-on-lint-files.sh (U97)."""

    def setUp(self):
        self.repo = Path(tempfile.mkdtemp(prefix="lint-file-set-test-")).resolve()
        self.bin = self.repo.parent / f"{self.repo.name}-bin"
        self.bin.mkdir()
        self.addCleanup(shutil.rmtree, self.bin)
        self.addCleanup(shutil.rmtree, self.repo)
        for relative in ("scripts/ci/run-on-lint-files.sh", "scripts/ci/pinned-tool-version.sh"):
            (self.repo / relative).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / relative, self.repo / relative)
        (self.repo / "home/dot_mise").mkdir(parents=True)
        shutil.copy2(MISE_CONFIG, self.repo / "home/dot_mise/config.toml")
        bad = BAD_SHELL
        files = {
            ".gitignore": "ignored/\nscripts/ignored.sh\n",
            "install/common/tracked.sh": "#!/usr/bin/env bash\necho tracked\n",
            "scripts/lib/deep.sh": "#!/usr/bin/env bash\necho deep\n",
            "home/outside.sh": "#!/usr/bin/env bash\necho outside\n",
            # In the set by shebang alone, with no shell extension.
            "home/dot_local/bin/executable_tool": "#!/usr/bin/env bash\necho tool\n",
            "home/modify_config.yml": "#!/bin/sh\nexec cat\n",
            "home/env-split": "#!/usr/bin/env -S bash -e\necho split\n",
            "home/env-comment": "#!/usr/bin/env -S bash # zsh is not supported\necho comment\n",
            "home/caf\u00e9.sh": "#!/bin/sh\necho cafe\n",
            'home/quote"d.sh': "#!/bin/sh\necho quoted\n",
            "home/tab\tname.sh": "#!/bin/sh\necho tab\n",
            # Recognised non-shell forms the repository uses: no word names bash or sh.
            "home/uv-tool": "#!/usr/bin/env -S uv run --no-cache --script\nprint( 'bad' )\n",
            "home/ruby-tool": "#!/usr/bin/env ruby\nputs( 'bad' )\n",
            "home/locked/inner.sh": "#!/usr/bin/env bash\necho inner\n",
            "home/zsh-abs": bad.replace("/usr/bin/env bash", "/bin/zsh"),
            "home/zsh-env": bad.replace("bash", "zsh"),
            # Tracked but excluded, each badly formatted so that reading it would fail the check.
            ".orchestration/tasks/copy.sh": bad,
            "home/prompt.zsh": bad.replace("bash", "zsh"),
            "home/zsh-script.sh": bad.replace("/usr/bin/env bash", "/bin/zsh"),
            "tests/install/t.bats": bad,
            "home/run_once.sh.tmpl": bad,
            "home/executable_py": "#!/usr/bin/env python3\nprint( 'bad' )\n",
            "tool.py": "print(1)\n",
            "notes.md": "# notes\n",
        }
        for name, body in files.items():
            (self.repo / name).parent.mkdir(parents=True, exist_ok=True)
            (self.repo / name).write_text(body)
        (self.repo / "home/link.sh").symlink_to("outside.sh")  # a symlink is no script of its own
        # A binary whose first line holds NUL bytes: read without a warning and left out (no shell shebang).
        (self.repo / "home/image.png").write_bytes(b"\x89PNG\x00\x00\x00\rIHDR\x00\n\x1a\n")
        git_init(self.repo)
        self.git("add", "-A")
        self.git("commit", "-q", "-m", "fixture")
        # Not tracked: a new file, an ignored file, and an ignored directory's copies, each badly formatted.
        for name in ("scripts/untracked.sh", "scripts/ignored.sh", "ignored/scripts/copy.sh", "untracked.py", "x.md"):
            (self.repo / name).parent.mkdir(parents=True, exist_ok=True)
            (self.repo / name).write_text(bad)

    def git(self, *args):
        env = os.environ | {"GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t"}
        env |= {"GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t"}
        subprocess.run(["git", "-C", str(self.repo), "-c", "commit.gpgsign=false", *args], check=True, env=env)

    def run_set(self, *args: str, env: dict | None = None) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [str(self.repo / "scripts/ci/run-on-lint-files.sh"), *args],
            cwd=self.repo,
            env=env,
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )

    def fake_tools(self) -> dict:
        """shfmt, ruff and prettier that report their pins, log each file argument, and fail when one holds `bad`."""
        for tool, version in pins().items():
            if tool == "shellcheck":
                continue
            banner = TOOLS[tool][1].format(v=version)
            path = self.bin / tool
            path.write_text(
                "#!/bin/sh\n"
                f"if [ \"$1\" = --version ]; then printf '%s' '{banner}'; exit 0; fi\n"
                "status=0\n"
                'for arg in "$@"; do\n'
                '  [ -f "$arg" ] || continue\n'
                '  printf \'%s\\n\' "$arg" >> "$0.log"\n'
                '  if grep -q bad "$arg"; then status=1; fi\n'
                "done\n"
                'exit "$status"\n'
            )
            path.chmod(0o755)
        return os.environ | {"PATH": f"{self.bin}:{os.environ['PATH']}"}

    def logged(self, tool: str) -> list[str]:
        log = self.bin / f"{tool}.log"
        return sorted(log.read_text().splitlines()) if log.exists() else []

    def test_each_set_is_the_tracked_files_of_its_patterns_only(self):
        for name, expected in (
            ("shell", SHELL_SET),
            ("python", ["tool.py"]),
            ("markdown", ["notes.md"]),
        ):
            with self.subTest(name):
                result = self.run_set(name, "printf", "%s\\n")
                self.assertEqual(0, result.returncode, result.stderr)
                # Each path reaches the command as ./<path>, so none can read as an option.
                self.assertEqual(dotted(expected), sorted(result.stdout.splitlines()))

    def test_the_shell_set_excludes_records_zsh_bats_templates_other_shells_and_symlinks(self):
        listed = [line.removeprefix("./") for line in self.run_set("shell", "printf", "%s\\n").stdout.splitlines()]
        self.assertEqual(
            "", self.git_output("ls-files", "--others", "--exclude-standard", "home", ".orchestration", "tests")
        )
        for name in EXCLUDED:
            with self.subTest(name):
                self.assertIn(name, self.git_output("ls-files", name))  # tracked, and still not in the set
                self.assertNotIn(name, listed)

    def git_output(self, *args: str) -> str:
        return subprocess.run(["git", "-C", str(self.repo), *args], capture_output=True, text=True, check=True).stdout

    def test_a_first_line_read_that_fails_stops_the_shell_set_whatever_it_printed(self):
        # Round-3 audit of fa319844: bash's `read` returns 1 at end of file and on a read error alike, so a failed read
        # of a shebang-only script read as "not a script" and dropped it. The first line now comes from head, whose
        # status is checked: a head that fails stops the run with 2 naming the file, whether it printed a valid bash
        # shebang first or nothing.
        fake = self.repo.parent / f"{self.repo.name}-head"
        fake.mkdir()
        self.addCleanup(shutil.rmtree, fake)
        for name, body in (
            ("a bash shebang, then exit 1", "printf '#!/usr/bin/env bash\\n'\nexit 1\n"),
            ("no output, exit 1", "exit 1\n"),
        ):
            with self.subTest(name):
                (fake / "head").write_text(
                    "#!/bin/sh\n"
                    # Only the shebang-only script's read fails; every other file is read by the real head.
                    f'case "$*" in *home/dot_local/bin/executable_tool*) {body.replace(chr(10), "; ")} ;; esac\n'
                    f'exec {shutil.which("head")} "$@"\n'
                )
                (fake / "head").chmod(0o755)
                env = os.environ | {"PATH": f"{fake}:{os.environ['PATH']}"}
                result = self.run_set("shell", "true", env=env)
                self.assertEqual(2, result.returncode, result.stdout + result.stderr)
                self.assertIn(
                    "cannot read home/dot_local/bin/executable_tool to tell whether it is a shell script; "
                    "nothing was checked",
                    result.stderr,
                )
        # The same runs without the fault list the script and print nothing on stderr, the binary file included.
        clean = self.run_set("shell", "printf", "%s\\n")
        self.assertEqual(0, clean.returncode, clean.stderr)
        self.assertIn("./home/dot_local/bin/executable_tool", clean.stdout.splitlines())
        self.assertEqual("", clean.stderr)

    def test_the_script_uses_no_construct_backed_by_a_temporary_file(self):
        # Round-5 audit of cdf72bb6: bash 3.2 backs here-strings and here-documents with a temporary file, and an
        # `or-colon` hid a failure to make one, so a script was excluded. Neither, nor `|| true`, is in the script.
        text = RUNNER.read_text()
        for construct in ("<<<", "<<", "|| :", "|| true"):
            self.assertNotIn(construct, text)

    def test_the_set_is_the_same_with_tmpdir_unwritable_under_every_bash(self):
        # macOS's /bin/bash (3.2) and the bash on PATH (5 on CI) both classify the fixture with TMPDIR unwritable.
        locked = self.repo.parent / f"{self.repo.name}-tmp"
        locked.mkdir(mode=0o555)
        self.addCleanup(shutil.rmtree, locked, True)
        self.addCleanup(locked.chmod, 0o755)
        shells = {path for path in ("/bin/bash", shutil.which("bash")) if path and Path(path).exists()}
        for shell in sorted(shells):
            with self.subTest(shell):
                result = subprocess.run(
                    [shell, str(self.repo / "scripts/ci/run-on-lint-files.sh"), "shell", "printf", "%s\\n"],
                    cwd=self.repo,
                    env=os.environ | {"TMPDIR": str(locked)},
                    capture_output=True,
                    text=True,
                    timeout=60,
                    check=False,
                )
                self.assertEqual(0, result.returncode, result.stderr)
                self.assertEqual(dotted(SHELL_SET), sorted(result.stdout.splitlines()))
                self.assertEqual("", result.stderr)

    def assert_stops(self, message: str) -> None:
        result = self.run_set("shell", "true")
        self.assertEqual(2, result.returncode, result.stdout + result.stderr)
        self.assertIn(f"run-on-lint-files: {message}; nothing was checked", result.stderr)

    @unittest.skipIf(os.geteuid() == 0, "root searches any directory")
    def test_a_script_under_an_unsearchable_directory_stops_the_shell_set(self):
        # Round-4 audit of 3b293cd5: `-f` was false under an unsearchable parent, so the script was excluded. The index
        # says it is a regular file, so the failed read is an error that names it.
        locked = self.repo / "home/locked"
        locked.chmod(0)
        self.addCleanup(locked.chmod, 0o755)
        self.assert_stops("cannot read home/locked/inner.sh to tell whether it is a shell script")

    def test_a_file_deleted_from_the_work_tree_but_indexed_stops_the_shell_set(self):
        (self.repo / "scripts/lib/deep.sh").unlink()
        self.assert_stops("cannot read scripts/lib/deep.sh to tell whether it is a shell script")

    def test_a_symlink_and_a_gitlink_are_excluded_by_their_index_mode(self):
        # Neither is read: a gitlink has no file in the work tree here, and a .sh name does not bring it in.
        head = self.git_output("rev-parse", "HEAD").strip()
        self.git("update-index", "--add", "--cacheinfo", f"160000,{head},vendor/sub.sh")
        modes = dict(
            line.split(" ", 1)[0:1] + [line.split("\t", 1)[1]]
            for line in self.git_output("ls-files", "-s", "--", "home/link.sh", "vendor/sub.sh").splitlines()
        )
        self.assertEqual({"120000": "home/link.sh", "160000": "vendor/sub.sh"}, modes)
        result = self.run_set("shell", "printf", "%s\\n")
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual(dotted(SHELL_SET), sorted(result.stdout.splitlines()))

    def test_a_shebang_outside_the_table_stops_the_shell_set(self):
        # Round-7 audit of 1198f86d: `env -S "sh"` passed the "mentions a shell" test. Every `#!` line must match the
        # table exactly; any other stops the run, whatever it names and whatever the file is called.
        for first in (
            '#!/usr/bin/env -S "sh"',
            "#!/usr/bin/env -Sbash",
            "#!/usr/local/bin/bash",
            "#!/usr/bin/perl",
            "#!/usr/bin/env -S -- NAME=value bash",
            "#!/usr/bin/env -i PATH=/x bash",
            "#!/usr/bin/env -u FOO sh",
            "#!/opt/homebrew/bin/bash -e",
            "#!/usr/bin/env --split-string=sh",
            "#!/bin/dash",
            "#!/usr/bin/env -S zsh -f",
            "#!/usr/bin/env node",
            "#!/usr/bin/env",
            "#!",
        ):
            with self.subTest(first):
                for extension in ("", ".sh"):
                    name = f"home/unrecognised{extension}"
                    (self.repo / name).write_text(f"{first}\necho x\n")
                    self.git("add", "--", name)
                    self.assert_stops(
                        f"{name}: unrecognised shebang; add it to the table with its kind "
                        "(SHEBANG_FORMS in scripts/ci/run-on-lint-files.sh)"
                    )
                    self.git("rm", "-q", "--cached", "--", name)
                    (self.repo / name).unlink()

    def test_each_table_entry_classifies_as_its_kind(self):
        # Every SHEBANG_FORMS row, with free words after its interpreter part, and named with and without .sh:
        # shell is in either way, zsh is out either way, other is in only by the .sh name.
        text = RUNNER.read_text()
        table = text[text.index("SHEBANG_FORMS=(\n") : text.index("\n)\n", text.index("SHEBANG_FORMS=(\n"))]
        forms = [re.match(r"\s*'(\w+) ([^']+)'", line) for line in table.splitlines()[1:]]
        self.assertTrue(forms and all(forms), table)
        self.assertEqual({"shell", "zsh", "other"}, {form.group(1) for form in forms}, "the table names every kind")
        added = []
        for number, form in enumerate(forms):
            for extension in ("", ".sh"):
                name = f"home/form-{number}{extension}"
                (self.repo / name).write_text(f"#!{form.group(2)} --free word\necho x\n")
                added.append((name, form.group(1), extension))
        self.git("add", "--", *(name for name, _, _ in added))
        result = self.run_set("shell", "printf", "%s\\n")
        self.assertEqual(0, result.returncode, result.stderr)
        listed = set(result.stdout.splitlines())
        for name, kind, extension in added:
            with self.subTest(name=name, kind=kind):
                expected = kind == "shell" or (kind == "other" and extension == ".sh")
                self.assertEqual(expected, f"./{name}" in listed)

    def test_every_shebang_the_repository_uses_is_a_recognised_form(self):
        # The closed set covers the tree: the real shell set lists without a refusal.
        result = subprocess.run(
            [str(RUNNER), "shell", "true"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=COMMAND_SECONDS,
            check=False,
        )
        self.assertEqual(0, result.returncode, result.stderr)

    def test_an_unmerged_index_stops_every_set(self):
        blob = (
            subprocess.run(
                ["git", "-C", str(self.repo), "hash-object", "-w", "--stdin"],
                input=b"x\n",
                capture_output=True,
                check=True,
                timeout=COMMAND_SECONDS,
            )
            .stdout.decode()
            .strip()
        )
        subprocess.run(
            ["git", "-C", str(self.repo), "update-index", "--index-info"],
            input=f"100644 {blob} 1\tnotes.md\n100644 {blob} 2\tnotes.md\n".encode(),
            check=True,
            timeout=COMMAND_SECONDS,
        )
        for name in ("shell", "python", "markdown"):
            with self.subTest(name):
                result = self.run_set(name, "true")
                if name == "python":
                    self.assertEqual(0, result.returncode, result.stderr)  # notes.md is outside the python set
                    continue
                self.assertEqual(2, result.returncode, result.stdout + result.stderr)
                self.assertIn("notes.md is unmerged in the index; nothing was checked", result.stderr)

    @unittest.skipIf(os.geteuid() == 0, "root reads any file")
    def test_a_tracked_file_that_cannot_be_read_stops_the_shell_set(self):
        # Round-1 audit of 35739993: a failed first-line read was an exclusion, so the file was dropped and the check
        # passed on the rest. It is now a failure that names the file.
        unreadable = self.repo / "scripts/lib/deep.sh"
        unreadable.chmod(0)
        self.addCleanup(unreadable.chmod, 0o644)
        result = self.run_set("shell", "true")
        self.assertEqual(2, result.returncode, result.stdout)
        self.assertIn(
            "cannot read scripts/lib/deep.sh to tell whether it is a shell script; nothing was checked", result.stderr
        )

    def test_a_tracked_file_named_like_an_option_is_checked_as_a_file(self):
        # Round-1 audit of 35739993: `shfmt -d -version …` printed the version and exited 0. Each path is passed as
        # ./<path>, which shfmt, ruff and prettier all read as a path.
        names = {
            "shell": ("-version", "--help", "-l"),
            "python": ("-version.py", "--help.py"),
            "markdown": ("--help.md", "-l.md"),
        }
        bad = {"shell": BAD_SHELL, "python": "x=( 1 )\n", "markdown": "# a\n\n\n\nb\n"}
        for kind, files in names.items():
            for name in files:
                (self.repo / name).write_text(bad[kind])
        self.git("add", "--", *(name for files in names.values() for name in files))
        self.git("commit", "-q", "-m", "option-named files")
        listed = self.run_set("shell", "printf", "%s\\n").stdout.splitlines()
        for name in names["shell"]:
            self.assertIn(f"./{name}", listed)
        for kind, command in (
            ("shell", ("shfmt", "-i", "4", "-sr", "-d")),
            ("python", ("ruff", "format", "--check")),
            ("markdown", ("prettier", "--check")),
        ):
            with self.subTest(kind):
                if not runnable(command[0], self.repo):
                    self.skipTest(f"{command[0]} does not run here")
                result = self.run_set(kind, *command)
                self.assertNotEqual(0, result.returncode, result.stdout + result.stderr)
                for name in names[kind]:
                    self.assertIn(name, result.stdout + result.stderr)

    def test_a_set_that_cannot_be_listed_is_refused_never_empty(self):
        for args, message in (
            (("shell",), "usage:"),
            (("css", "true"), "css is not a lint file set"),
        ):
            with self.subTest(args=args):
                result = self.run_set(*args)
                self.assertEqual(2, result.returncode)
                self.assertIn(message, result.stderr)
        (self.repo / "notes.md").unlink()
        self.git("rm", "-q", "--cached", "notes.md")
        empty = self.run_set("markdown", "true")
        self.assertEqual(2, empty.returncode)
        self.assertIn("the markdown set lists no tracked file; nothing was checked", empty.stderr)
        outside = subprocess.run(
            [str(RUNNER), "shell", "true"], cwd=self.bin, capture_output=True, text=True, timeout=30, check=False
        )
        self.assertEqual(2, outside.returncode)
        self.assertIn("git ls-files failed for the shell set", outside.stderr)

    def test_make_format_reads_tracked_files_only_and_fails_on_a_tracked_one(self):
        env = self.fake_tools()

        def make_format():
            return subprocess.run(
                ["make", "-s", "-f", str(MAKEFILE), "format"],
                cwd=self.repo,
                env=env,
                capture_output=True,
                text=True,
                timeout=120,
                check=False,
            )

        # The untracked and ignored files are badly formatted; none is read, so make format passes.
        clean = make_format()
        self.assertEqual(0, clean.returncode, clean.stdout + clean.stderr)
        self.assertEqual(dotted(SHELL_SET), self.logged("shfmt"))
        self.assertEqual(["./tool.py"], self.logged("ruff"))
        self.assertEqual(["./notes.md"], self.logged("prettier"))
        # The same bad text in a tracked file of the set fails it.
        (self.repo / "home/dot_local/bin/executable_tool").write_text(BAD_SHELL)
        dirty = make_format()
        self.assertNotEqual(0, dirty.returncode)

    @unittest.skipUnless(shutil.which("shfmt"), "needs shfmt (CI puts the pin on PATH)")
    def test_the_real_shfmt_check_ignores_untracked_and_ignored_files_and_fails_a_tracked_one(self):
        check = ("shell", "shfmt", "-i", "4", "-sr", "-d")
        self.assertEqual(0, self.run_set(*check).returncode)
        (self.repo / "home/dot_local/bin/executable_tool").write_text(BAD_SHELL)
        failed = self.run_set(*check)
        self.assertNotEqual(0, failed.returncode)
        self.assertIn("home/dot_local/bin/executable_tool", failed.stdout)
        for name in ("untracked.sh", "ignored", *EXCLUDED):
            self.assertNotIn(name, failed.stdout + failed.stderr)

    def test_make_format_and_ci_run_the_same_check_on_the_same_set(self):
        result = subprocess.run(
            ["make", "-n", "-s", "format"], cwd=ROOT, capture_output=True, text=True, timeout=60, check=True
        )
        self.assertEqual(list(SET_CHECKS), result.stdout.splitlines()[1:])
        steps = {step["name"]: step for step in step_blocks(WORKFLOW.read_text())}
        ci = "\n".join(
            commands(steps["Run `shfmt`"]["run"]) + commands(steps["Check Python and Markdown formatting"]["run"])
        )
        for check in SET_CHECKS:
            self.assertIn(check, ci)
        # Neither side lists files any other way.
        for text in (result.stdout, ci):
            self.assertNotIn("git ls-files", text)
            self.assertNotRegex(text, r"shfmt [^\n]* \.$")


if __name__ == "__main__":
    unittest.main()
