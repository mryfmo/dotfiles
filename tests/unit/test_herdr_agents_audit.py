#!/usr/bin/env python3
"""Exercise the herdr-agents task-level audit prompt and its format 2 warning (T124 INV-4, INV-7)."""

from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

HARNESS_PATH = Path(__file__).resolve().parent / "test_herdr_agents.py"
# Loaded under a private name and never bound as a class here, so discovery
# does not collect the harness's own tests a second time.
_spec = importlib.util.spec_from_file_location("herdr_agents_audit_harness", HARNESS_PATH)
assert _spec and _spec.loader
_harness = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_harness)

GRAMMAR = (
    "`[P<0-3>] <high|medium|low> <specification|implementation|evidence|orchestration|conformance> "
    "<path:line|-> <rationale>`"
)
CATEGORIES = ("specification (", "implementation (", "evidence (", "orchestration (", "conformance (")
FORMAT_2_TASK = "---\nformat: 2\ntask_id: T1\nkind: code\ninvariants:\n  INV-1: x\n---\n# T1\n"
INVARIANT_RULE = "write one line per invariant id of the task front matter, `INV-n: holds|violated <path:line>`"
COUNT_RULE = "then the line `Orchestration findings: <count>`"
INV_WARNING = "WARN: herdr-agents: format 2 task T1: the audit output has no INV-n: holds|violated line."
COUNT_WARNING = "WARN: herdr-agents: format 2 task T1: the audit output has no Orchestration findings: line."


class HerdrAgentsAuditTest(_harness.HerdrAgentsTest):
    def audit_task(self, task: str = "x\n", last: str = "Verdict: correct\n", *extra: str):
        """Run `--audit <head> --task T1` with the given task file, last message and extra .orchestration files."""
        self.write_audit_pair_state(self.audit_tab_pane())
        _, head = self.write_task_audit_repo()
        orchestration = self.workdir.resolve() / ".orchestration"
        for path, text in (("tasks/T1.md", task), *((name, "x\n") for name in extra)):
            (orchestration / path).parent.mkdir(parents=True, exist_ok=True)
            (orchestration / path).write_text(text)
        self.write_audit_evidence(last, orchestration / f"validation/T1-audit-{head[:7]}.md.last.md")
        # audit_inner_command reads the first pane run, so each run starts a fresh call log.
        self.calls_path.unlink(missing_ok=True)
        result = self.run_helper("--audit", head, "--task", "T1")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        return result, self.audit_codex_words(self.audit_inner_command())[-1]

    def test_prompt_states_the_finding_grammar_and_the_five_categories(self) -> None:
        _, prompt = self.audit_task()

        self.assertIn(f"Report each finding on one line in exactly this grammar: {GRAMMAR};", prompt)
        for category in CATEGORIES:
            self.assertIn(category, prompt)
        self.assertNotIn("confidence dimension file:line", prompt)

    def test_prompt_puts_the_orchestrator_artifacts_in_scope(self) -> None:
        _, prompt = self.audit_task()

        self.assertIn(
            "Your scope covers the orchestrator as well as the worker: the task file with its amendments,", prompt
        )
        self.assertIn(
            "the design task file and review receipts the task front matter names under design_review", prompt
        )
        self.assertIn("orchestration (task wording, scope decisions, dispositions or acceptance claims)", prompt)
        self.assertIn("conformance (a deviation from the regime process)", prompt)

    def test_prompt_names_the_acceptance_record_only_when_it_exists(self) -> None:
        _, prompt = self.audit_task()
        self.assertNotIn("acceptance record `", prompt)

        _, prompt = self.audit_task("x\n", "Verdict: correct\n", "acceptance/T1.md")

        self.assertIn(
            "; the acceptance record `.orchestration/acceptance/T1.md` as it stands (earlier rounds' dispositions "
            "and the PR-feedback dispositions); the final head ",
            prompt,
        )

    def test_prompt_names_the_permgate_extract_only_when_present(self) -> None:
        _, prompt = self.audit_task()
        self.assertNotIn("permgate", prompt)

        _, prompt = self.audit_task("x\n", "Verdict: correct\n", "validation/T1-permgate.jsonl")

        self.assertIn(
            "; the permgate decision extract `.orchestration/validation/T1-permgate.jsonl` "
            "(the permission prompts in the task window); the final head ",
            prompt,
        )

    def test_format_2_prompt_requires_the_invariant_lines_and_the_count_before_the_verdict(self) -> None:
        _, prompt = self.audit_task(FORMAT_2_TASK, "INV-1: holds a.py:1\nOrchestration findings: 0\nVerdict: correct\n")

        self.assertIn(f"This is a format 2 task: before the verdict line, {INVARIANT_RULE}, {COUNT_RULE}.", prompt)
        self.assertLess(prompt.index(COUNT_RULE), prompt.index("End your final message"))

    def test_legacy_prompt_has_no_invariant_or_count_requirement(self) -> None:
        for task in ("x\n", "# T1\n\nformat: 2\n", "---\nformat: '2'\n---\n", "---\nkind: code\n---\nformat: 2\n"):
            with self.subTest(task=task):
                _, prompt = self.audit_task(task)

                self.assertNotIn("format 2 task", prompt)
                self.assertNotIn("Orchestration findings", prompt)

    def test_wrapper_warns_when_a_format_2_last_message_lacks_the_lines(self) -> None:
        cases = (
            ("Verdict: correct\n", [INV_WARNING, COUNT_WARNING]),
            ("Orchestration findings: 0\nVerdict: correct\n", [INV_WARNING]),
            ("INV-1: violated a.py:1\nVerdict: correct\n", [COUNT_WARNING]),
        )
        for last, warnings in cases:
            with self.subTest(last=last):
                result, _ = self.audit_task(FORMAT_2_TASK, last)

                self.assertEqual([line for line in result.stderr.splitlines() if "format 2 task" in line], warnings)
                # The warning never changes the verdict-only gate.
                self.assertIn("Audit verdict: correct\n", result.stdout)

    def test_wrapper_is_silent_when_the_lines_are_present_or_the_task_is_legacy(self) -> None:
        for task, last in (
            (
                FORMAT_2_TASK,
                "[P3] low evidence - x\nINV-1: holds a.py:1\nOrchestration findings: 0\nVerdict: correct\n",
            ),
            ("x\n", "Verdict: correct\n"),
        ):
            with self.subTest(task=task):
                result, _ = self.audit_task(task, last)

                self.assertNotIn("format 2 task", result.stderr)


def load_tests(loader: unittest.TestLoader, tests: unittest.TestSuite, pattern: str | None) -> unittest.TestSuite:
    """Run only this file's tests, not the inherited harness suite."""
    names = sorted(name for name in vars(HerdrAgentsAuditTest) if name.startswith("test_"))
    return unittest.TestSuite(HerdrAgentsAuditTest(name) for name in names)


if __name__ == "__main__":
    unittest.main()
