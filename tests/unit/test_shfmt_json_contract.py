#!/usr/bin/env python3
"""Exercise scripts/ci/shfmt_json_contract.py and the walkers that run it (regime-cutover U105, plan P-23).

The pinned shfmt must parse the fixtures under tests/fixtures/shfmt-json into the node table; the captured trees
beside them are the parser's own output, regenerated with

    cd tests/fixtures/shfmt-json && for f in contract.sh contract-backquotes; do
        shfmt -ln bash --to-json < "$f" > "${f%.sh}.json"; done

and are what the negative cases here alter. The decision rows need shfmt on PATH: the mise config installs it on the
hosts and CI puts the pinned version there.
"""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import tomllib
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/ci"))
import shfmt_json_contract as contract  # noqa: E402

sys.path.insert(0, str(ROOT / "tests/unit"))
import test_sandbox_portability as sandbox  # noqa: E402

MODULE = ROOT / "scripts/ci/shfmt_json_contract.py"
FIXTURES = ROOT / "tests/fixtures/shfmt-json"
FIXTURE = FIXTURES / "contract.sh"
BACKQUOTES = FIXTURES / "contract-backquotes"
CAPTURES = {FIXTURE: FIXTURES / "contract.json", BACKQUOTES: FIXTURES / "contract-backquotes.json"}
CHECK = ROOT / "scripts/ci/masked-dirname-check.sh"
HOOK = ROOT / "home/dot_claude/hooks/executable_enforce-uv.sh"
LINT = ROOT / "scripts/lint-comparisons.py"
NESTED_LINE = 7  # contract.sh: the one command substitution that opens inside another
BACKQUOTES_LINE = 4  # contract-backquotes: the backquoted substitution, inside another
MESSAGE = "a command substitution inside another one loses its status; capture it first, or split a path in the shell"
# A file node whose statements carry no Cmd: the shape a renamed field leaves, which every walk must refuse to read as
# "no findings".
UNREADABLE_TREE = {"Type": "File", "Stmts": [{"Command": {"Type": "CallExpr"}}]}
# Each walker's source region and the shapes a field name or Type string takes in it: a subscript, a .get(), a key
# test, a Type comparison, a tuple of names, or a jq path. Every name found must be a kind or a field of TABLE.
PYTHON_ACCESSORS = (
    r'\[\s*"([A-Z]\w+)"\s*\]',
    r'\.get\(\s*"([A-Z]\w+)"',
    r'"([A-Z]\w+)"\s+(?:not\s+)?in\s+\w',
    r'Type"\]?\)?\s*(?:==|!=)\s*"([A-Z]\w+)"',
    r'\(\s*"([A-Z]\w+)"(?:\s*,\s*"[A-Z]\w+")*\s*,?\s*\)',
    r'\(\s*"[A-Z]\w+"(?:\s*,\s*"([A-Z]\w+)")+\s*,?\s*\)',
)
WALKERS = {
    CHECK: (re.compile(r"cat << 'PY'\n(.*?)\nPY\n", re.DOTALL), PYTHON_ACCESSORS),
    HOOK: (re.compile(r"function split_segments\(\) \{\n(.*?)\n\}\n", re.DOTALL), (r"\.([A-Z]\w+)",)),
    LINT: (re.compile(r"^def shfmt_tree\(.*?^def python_hits\(", re.DOTALL | re.MULTILINE), PYTHON_ACCESSORS),
    ROOT / "tests/unit/test_sandbox_portability.py": (
        re.compile(r"^def shell_tree\(.*?^def dotted\(", re.DOTALL | re.MULTILINE),
        PYTHON_ACCESSORS,
    ),
}


def on_ci_runner() -> bool:
    """scripts/lib/ci-runner.sh decides, never the generic CI variable an agent shell exports."""
    probe = 'source "$1" && is_ci_runner'
    return (
        subprocess.run(["bash", "-c", probe, "_", str(ROOT / "scripts/lib/ci-runner.sh")], check=False).returncode == 0
    )


def pinned_version() -> str:
    return tomllib.loads((ROOT / "home/dot_mise/config.toml").read_text())["tools"]["http:shfmt"]["version"]


def captures() -> dict[str, str]:
    """The captured tree text of each fixture, by the fixture's name."""
    return {fixture.name: capture.read_text() for fixture, capture in CAPTURES.items()}


def table_names() -> set[str]:
    """Every kind and every field name (each step of a dotted path) TABLE writes down, and Type, the discriminator."""
    names = set(contract.TABLE) | {"Type"}
    for row in contract.TABLE.values():
        names.update(step for path in row.fields for step in path.split("."))
        names.update(step for path in row.values for step in path.split("."))
    return names


def module_check(*trees: str) -> subprocess.CompletedProcess[str]:
    """The module's CLI over captured tree files."""
    with tempfile.TemporaryDirectory() as temp:
        args = []
        for n, text in enumerate(trees):
            path = Path(temp) / f"tree-{n}.json"
            path.write_text(text)
            args += ["--tree", str(path)]
        return subprocess.run([sys.executable, "-I", str(MODULE), *args], capture_output=True, text=True, check=False)


class ContractTableTest(unittest.TestCase):
    """The table against the captured trees: no shfmt needed."""

    def loaded(self, **altered: str) -> dict[str, object]:
        texts = {**captures(), **altered}
        return {name: json.loads(text) for name, text in texts.items()}

    def test_the_captured_trees_satisfy_every_row(self) -> None:
        trees = self.loaded()
        self.assertIsNone(contract.check(trees))
        counts = sum((contract.count(tree) for tree in trees.values()), contract.Counter())
        self.assertEqual(set(contract.TABLE), {kind for kind in counts if counts[kind]})
        self.assertGreaterEqual(contract.count(trees[FIXTURE.name])["CmdSubst"], 2, "a nested substitution needs two")

    def test_renaming_type_in_the_capture_fails_the_contract(self) -> None:
        renamed = captures()[FIXTURE.name].replace('"Type"', '"type"')
        self.assertEqual(
            f"the root of {FIXTURE.name} is no node with Type File",
            contract.check(self.loaded(**{FIXTURE.name: renamed})),
        )
        result = module_check(renamed, captures()[BACKQUOTES.name])
        self.assertEqual(2, result.returncode, result.stdout + result.stderr)
        self.assertRegex(
            result.stderr, r"^shfmt-json-contract: the root of \S+/tree-0.json is no node with Type File\n$"
        )
        self.assertEqual("", result.stdout)

    def test_a_missing_field_or_a_changed_spelling_is_named(self) -> None:
        where = f"{FIXTURE.name}, {BACKQUOTES.name}"
        cases = {
            ('"Backquotes"', '"Backquote"'): f"no CmdSubst node of {where} has the field Backquotes",
            ('"Op": "|"', '"Op": "pipe"'): f"no BinaryCmd node of {where} has Op = '|'",
            ('"Type": "CmdSubst"', '"Type": "CommandSubstitution"'): f"{where} holds no CmdSubst node",
            ('"Hdoc"', '"Heredoc"'): f"no Redirect node of {where} has the field Hdoc",
            ('"Cmd"', '"Command"'): f"{where} holds no Stmt node",
        }
        for (old, new), expected in cases.items():
            with self.subTest(change=f"{old} -> {new}"):
                altered = {name: text.replace(old, new) for name, text in captures().items()}
                self.assertNotEqual(altered, captures())
                self.assertEqual(expected, contract.check(self.loaded(**altered)))

    def test_a_tree_that_is_no_json_object_is_refused(self) -> None:
        for tree in ("not-json", "null", "[]", '{"Type": "Word"}'):
            with self.subTest(tree=tree):
                result = module_check(tree, captures()[BACKQUOTES.name])
                self.assertEqual(2, result.returncode, result.stdout + result.stderr)
                self.assertTrue(result.stderr.startswith("shfmt-json-contract: "), result.stderr)
                self.assertEqual("", result.stdout)

    def test_every_field_name_a_walker_reads_is_in_the_table(self) -> None:
        known = table_names()
        for path, (region, accessors) in WALKERS.items():
            with self.subTest(walker=path.relative_to(ROOT).as_posix()):
                match = region.search(path.read_text())
                self.assertIsNotNone(match, "the walker's source region was not found")
                source = match.group(0)
                found = {name for pattern in accessors for name in re.findall(pattern, source) if name}
                self.assertTrue(found, "the walker reads no field by name")
                self.assertEqual(set(), found - known, f"names outside TABLE: {sorted(found - known)}")


@unittest.skipUnless(shutil.which("shfmt") or on_ci_runner(), "needs shfmt off the CI runner (CI puts the pin on PATH)")
class ContractRunTest(unittest.TestCase):
    """The pinned parser on PATH against the fixtures, and the walkers that run the contract first."""

    def setUp(self) -> None:
        self.temp = Path(tempfile.mkdtemp(prefix="shfmt-json-contract-"))
        self.addCleanup(shutil.rmtree, self.temp)

    def test_the_pinned_shfmt_satisfies_the_contract(self) -> None:
        result = subprocess.run([sys.executable, "-I", str(MODULE)], capture_output=True, text=True, check=False)
        self.assertEqual((0, "", ""), (result.returncode, result.stdout, result.stderr))

    def test_the_captured_trees_are_the_pinned_parsers_output(self) -> None:
        for fixture, capture in CAPTURES.items():
            with self.subTest(fixture=fixture.name):
                run = subprocess.run(
                    ["shfmt", "-ln", "bash", "--to-json"], input=fixture.read_bytes(), capture_output=True, check=True
                )
                self.assertEqual(json.loads(run.stdout), json.loads(capture.read_text()), f"regenerate {capture.name}")

    def test_each_fixture_yields_one_finding_at_its_nested_substitution(self) -> None:
        for fixture, line in ((FIXTURE, NESTED_LINE), (BACKQUOTES, BACKQUOTES_LINE)):
            with self.subTest(fixture=fixture.name):
                result = subprocess.run(["bash", str(CHECK), str(fixture)], capture_output=True, text=True, check=False)
                self.assertEqual(1, result.returncode, result.stdout + result.stderr)
                self.assertEqual(f"{fixture}:{line}: {MESSAGE}\n", result.stdout)
                self.assertEqual("", result.stderr)

    def test_the_heredoc_caveats_keep_their_status(self) -> None:
        # An ANSI-C escaped delimiter is a heredoc shfmt cannot terminate: refused, as ShellCheck refuses it. A
        # partly quoted delimiter makes the body literal in bash, so its nested substitution is no finding.
        ansi = subprocess.run(
            ["bash", str(CHECK), str(FIXTURES / "heredoc-ansi-c-delimiter")],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(2, ansi.returncode, ansi.stdout + ansi.stderr)
        self.assertIn("shfmt cannot parse", ansi.stderr)
        self.assertEqual("", ansi.stdout)
        partly = subprocess.run(
            ["bash", str(CHECK), str(FIXTURE), str(FIXTURES / "heredoc-partly-quoted-delimiter")],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(1, partly.returncode, partly.stdout + partly.stderr)
        self.assertEqual(f"{FIXTURE}:{NESTED_LINE}: {MESSAGE}\n", partly.stdout, "the literal bodies add nothing")

    def path_with_fake_shfmt(self, fixture_trees: dict[str, str], other_tree: str) -> dict[str, str]:
        """An environment whose PATH holds the tools the walkers need and a shfmt that reports the pinned version,
        answers each fixture its tree from fixture_trees (by fixture name) and other_tree to any other input."""
        bin_dir = self.temp / "bin"
        bin_dir.mkdir()
        for tool in ("bash", "sh", "awk", "python3", "jq", "sed", "xargs", "cat"):
            (bin_dir / tool).symlink_to(shutil.which(tool))
        answers = ""
        for fixture in CAPTURES:
            (self.temp / f"{fixture.name}.json").write_text(fixture_trees[fixture.name])
            answers += f'[ "$input" = "$(/bin/cat "{fixture}")" ] && exec /bin/cat "{self.temp}/{fixture.name}.json"\n'
        (self.temp / "other.json").write_text(other_tree)
        fake = bin_dir / "shfmt"
        fake.write_text(
            "#!/bin/sh\n"
            f'[ "$1" = --version ] && {{ echo v{pinned_version()}; exit 0; }}\n'
            f'input=$(/bin/cat)\n{answers}exec /bin/cat "{self.temp}/other.json"\n'
        )
        fake.chmod(0o755)
        return {"PATH": str(bin_dir), "HOME": str(self.temp)}

    def walkers(self, env: dict[str, str]) -> dict[str, subprocess.CompletedProcess[str]]:
        """One run of each walker over a small conforming input, under env."""
        script = self.temp / "lever.sh"
        script.write_text('#!/usr/bin/env bash\ndir=$(dirname "$0")\necho "$dir"\n')
        payload = json.dumps({"tool_name": "Bash", "tool_input": {"command": "python script.py"}})
        return {
            "masked-dirname-check": subprocess.run(
                ["bash", str(CHECK), str(script)], capture_output=True, text=True, check=False, env=env
            ),
            "enforce-uv": subprocess.run(
                ["bash", str(HOOK)], input=payload, capture_output=True, text=True, check=False, env=env
            ),
            "lint-comparisons": subprocess.run(
                [sys.executable, "-I", str(LINT), "--baseline", str(self.temp / "none.tsv"), "lever.sh", "--changed"],
                cwd=self.temp,
                capture_output=True,
                text=True,
                check=False,
                env=env,
            ),
        }

    def test_each_walker_refuses_a_parser_whose_output_does_not_match(self) -> None:
        renamed = {name: text.replace('"Type"', '"type"') for name, text in captures().items()}
        results = self.walkers(self.path_with_fake_shfmt(renamed, renamed[FIXTURE.name]))
        for name, result in results.items():
            with self.subTest(walker=name):
                self.assertEqual(2, result.returncode, result.stdout + result.stderr)
                self.assertIn("does not match the pinned node table", result.stderr)
                self.assertEqual("", result.stdout, "no finding and no decision stands in for the refusal")

    def test_each_walker_refuses_a_run_that_saw_no_node_the_fixture_holds(self) -> None:
        # The parser satisfies the contract, then hands every real file a tree whose statements the walk cannot
        # read: "no findings" would be "saw nothing", so each walker exits 2 naming what it did not see.
        results = self.walkers(self.path_with_fake_shfmt(captures(), json.dumps(UNREADABLE_TREE)))
        expected = {
            "masked-dirname-check": "the walk visited no command substitution",
            "enforce-uv": "lists 1 statement(s) but the walk saw none",
            "lint-comparisons": "saw no statement in 1 shell file(s)",
        }
        for name, result in results.items():
            with self.subTest(walker=name):
                self.assertEqual(2, result.returncode, result.stdout + result.stderr)
                self.assertIn(expected[name], result.stderr)
                self.assertEqual("", result.stdout)

    def test_the_walkers_judge_a_conforming_tree_as_before(self) -> None:
        results = self.walkers({**os.environ})
        check = results["masked-dirname-check"]
        self.assertEqual((0, "", ""), (check.returncode, check.stdout, check.stderr))
        hook = results["enforce-uv"]
        self.assertEqual(0, hook.returncode, hook.stderr)
        self.assertIn('"permissionDecision":"deny"', hook.stdout)
        lint = results["lint-comparisons"]
        self.assertEqual((0, "", ""), (lint.returncode, lint.stdout, lint.stderr))

    def test_the_sandbox_guard_refuses_what_the_other_walkers_refuse(self) -> None:
        # tests/unit/test_sandbox_portability.py walks the same JSON in process: a contract mismatch and a run whose
        # shell files held no statement node are errors there, never an empty hit list.
        sandbox.shfmt.cache_clear()
        self.addCleanup(sandbox.shfmt.cache_clear)
        with mock.patch.object(contract, "verify", side_effect=contract.ContractError("injected")):
            with self.assertRaisesRegex(RuntimeError, "does not match the pinned node table: injected"):
                sandbox.findings("a.sh", "#!/usr/bin/env bash\necho\n")
        sandbox.shfmt.cache_clear()
        tracked = [("scripts/a.sh", "#!/usr/bin/env bash\necho\n")]
        with mock.patch.object(sandbox, "tracked", return_value=tracked):
            with mock.patch.object(sandbox, "shell_tree", return_value=UNREADABLE_TREE):
                with self.assertRaisesRegex(RuntimeError, "saw no statement in 1 shell file"):
                    sandbox.guard(ROOT)
            self.assertEqual([], sandbox.guard(ROOT))


if __name__ == "__main__":
    unittest.main()
