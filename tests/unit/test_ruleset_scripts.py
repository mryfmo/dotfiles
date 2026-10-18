"""Ruleset helpers read GitHub and update only the two verified progress rows."""

from __future__ import annotations

import json
from copy import deepcopy
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

from tests.unit.test_workflow_orchestration_skip import REQUIRED_CONTEXTS

ROOT = Path(__file__).resolve().parents[2]
GH = """#!/usr/bin/env python3
import json, os, sys
with open(os.environ['RULESET_ARGS'], 'a') as out: out.write(json.dumps(sys.argv[1:])+'\\n')
if sys.argv[1:] == ['repo','view','--json','nameWithOwner','--jq','.nameWithOwner']: print('o/r')
elif sys.argv[1:] == ['api','repos/o/r/rulesets/24397953']: print(open(os.environ['RULESET_LIVE']).read())
else: raise SystemExit(9)
"""


class RulesetScriptsTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.scripts = self.root / "scripts/orchestrator"
        self.scripts.mkdir(parents=True)
        for name in ("ruleset-request.sh", "ruleset-verify.sh"):
            shutil.copyfile(ROOT / "scripts/orchestrator" / name, self.scripts / name)
        (self.root / "bin").mkdir()
        gh = self.root / "bin/gh"
        gh.write_text(GH)
        gh.chmod(0o755)
        parameters = dict(strict_required_status_checks_policy=False, do_not_enforce_on_create=False)
        parameters["required_status_checks"] = [
            dict(context=x, integration_id=15368) for x in sorted(REQUIRED_CONTEXTS)
        ]
        self.expected = {
            "id": 24397953,
            "name": "main integration gate",
            "target": "branch",
            "enforcement": "active",
            "conditions": {"ref_name": {"exclude": [], "include": ["~DEFAULT_BRANCH"]}},
            "bypass_actors": [],
            "rules": [
                {"type": "deletion"},
                {"type": "non_fast_forward"},
                {"type": "required_status_checks", "parameters": parameters},
            ],
        }
        self.live = self.root / "live.json"
        self.live.write_text(json.dumps(self.expected))
        self.expected_path = self.root / "expected.json"
        self.expected_path.write_text(json.dumps(self.expected))
        self.progress = self.root / ".orchestration/plans/024-progress.tsv"
        self.progress.parent.mkdir(parents=True)
        self.original = "id\tkind\ttitle\tstate\tevidence\tupdated_jst\nP1-1\tphase\tkeep\tactive\told\tyesterday\nD1\tdecision\tstrict\tdefault\told\tyesterday\nD2\tdecision\tthreads\tdefault\told\tyesterday\n"
        self.progress.write_text(self.original)
        self.env = dict(
            os.environ,
            PATH=f"{self.root / 'bin'}:{os.environ['PATH']}",
            RULESET_LIVE=str(self.live),
            RULESET_ARGS=str(self.root / "argv.jsonl"),
        )

    def run_script(self, name: str, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["bash", str(self.scripts / name), *args],
            cwd=self.root,
            env=self.env,
            text=True,
            capture_output=True,
        )

    def assert_get_only(self) -> None:
        calls = {tuple(json.loads(x)) for x in (self.root / "argv.jsonl").read_text().splitlines()}
        self.assertTrue(calls)
        self.assertLessEqual(
            calls,
            {
                ("repo", "view", "--json", "nameWithOwner", "--jq", ".nameWithOwner"),
                ("api", "repos/o/r/rulesets/24397953"),
            },
        )

    def test_ruleset_request_prints_the_diff_and_never_writes(self) -> None:
        self.expected["rules"][-1]["parameters"]["strict_required_status_checks_policy"] = True
        self.live.write_text(json.dumps(self.expected))
        result = self.run_script("ruleset-request.sh", "--expected", str(self.expected_path))
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn("main integration gate", result.stdout)
        self.assertIn("--- expected", result.stdout)
        self.assertIn("+++ live", result.stdout)
        self.assertEqual(self.original, self.progress.read_text())
        self.assert_get_only()

    def test_ruleset_comparison_preserves_duplicate_rule_types(self) -> None:
        rules = []
        for context in ("expected-a", "expected-b"):
            rule = deepcopy(self.expected["rules"][-1])
            rule["parameters"]["required_status_checks"][0]["context"] = context
            rules.append(rule)
        self.expected["rules"] = rules
        self.expected_path.write_text(json.dumps(self.expected))
        for collapse in (False, True):
            live = deepcopy(self.expected)
            if collapse:
                live["rules"] = [rules[-1]]
            else:
                for i, rule in enumerate(live["rules"]):
                    rule["parameters"]["required_status_checks"][0]["context"] = f"live-{i}"
            self.live.write_text(json.dumps(live))
            for name in ("ruleset-request.sh", "ruleset-verify.sh"):
                with self.subTest(collapse=collapse, script=name):
                    result = self.run_script(name, "--expected", str(self.expected_path))
                    self.assertEqual(0 if name == "ruleset-request.sh" else 1, result.returncode, result.stderr)
                    differences = [line for line in result.stdout.splitlines() if line.startswith("ruleset.rules[")]
                    self.assertEqual(2, len(differences), result.stdout)
                    self.assertEqual(self.original, self.progress.read_text())
        self.live.write_text(self.expected_path.read_text())
        self.assertEqual(0, self.run_script("ruleset-verify.sh", "--expected", str(self.expected_path)).returncode)
        self.assertEqual(self.original.splitlines()[:2], self.progress.read_text().splitlines()[:2])
        for line in self.progress.read_text().splitlines()[2:]:
            self.assertTrue(line.split("\t")[4].startswith("verified "))
        self.assert_get_only()

    def test_ruleset_verify_reports_each_difference_and_writes_progress_only_on_match(self) -> None:
        self.expected["rules"][-1]["parameters"]["strict_required_status_checks_policy"] = True
        self.expected["rules"].append({"type": "pull_request"})
        self.live.write_text(json.dumps(self.expected))
        red = self.run_script("ruleset-verify.sh", "--expected", str(self.expected_path))
        self.assertEqual(1, red.returncode, red.stderr)
        self.assertIn("strict_required_status_checks_policy", red.stdout)
        self.assertIn("pull_request", red.stdout)
        self.assertEqual(self.original, self.progress.read_text())
        self.live.write_text(self.expected_path.read_text())
        green = self.run_script("ruleset-verify.sh")
        self.assertEqual(0, green.returncode, green.stderr)
        lines = self.progress.read_text().splitlines()
        self.assertEqual(self.original.splitlines()[:2], lines[:2])
        for line in lines[2:]:
            fields = line.split("\t")
            self.assertTrue(fields[4].startswith("verified "))
            self.assertTrue(fields[5].endswith("Z"))
        self.progress.write_text(self.original + self.original.splitlines(keepends=True)[2])
        before = self.progress.read_bytes()
        self.assertNotEqual(0, self.run_script("ruleset-verify.sh").returncode)
        self.assertEqual(before, self.progress.read_bytes())
        self.assert_get_only()
