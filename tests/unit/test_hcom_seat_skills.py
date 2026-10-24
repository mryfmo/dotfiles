"""Pin the hcom seat skills' text hygiene sentences (U30): what a seat may type in one bash call, what a bus
line carries, and who hands the audit findings to the worker."""

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SKILLS = ROOT / "home/dot_agents/skills"
AUDIT = SKILLS / "hcom-audit/SKILL.md"
WORKER = SKILLS / "hcom-worker/SKILL.md"
ORCHESTRATION = SKILLS / "hcom-orchestration/SKILL.md"
POLICIES = ROOT / "home/dot_agents/omp/policies/README.md"

ONE_COMMAND = (
    "One command per bash call: your allow rows match a whole simple command, so `a && b`, `a; b`, `a | b` and "
    "a `$(…)` are refused by the catch-all. Run `git rev-parse HEAD` and `git status --porcelain` as two calls."
)
QUOTED_DENY = (
    "a deny row matches the whole command or any one segment of it, quoted text included: never put a denied "
    "command's name inside a quoted argument"
)
BUS_LINE = (
    "A bus line carries the kind, `task_id`, `brief=` path, `head=`, `pr=` and a `note=` of at most one sentence "
    "without command names; any instruction longer than that goes into a brief or addendum file the line points "
    "at. A deny row of your own policy matches text inside the line."
)
HAND_OFF = (
    "After a VERDICT with findings, copy the audit seat's `status=findings` PONG text into "
    "`verdicts/U<n>-<head>.md` before you send the fix TASK, and name that file in the TASK "
    "(`brief=<verdicts path>` or `findings=<path>`) by its absolute path in your checkout"
)
# The findings file is uncommitted in the orchestrator's checkout, so the worker's worktree lacks it (PR #487
# review 4366101582); the worker reads it by absolute path, never from its clone.
WORKER_READS = "an absolute path under the program's `verdicts/` in the orchestrator's checkout"
WORKER_WAITS = (
    "A `verdict=incorrect` row is not addressed to you; wait for the orchestrator's fix TASK, never question the "
    "audit seat on the bus."
)
FINDINGS_ONCE = (
    "send the findings PONG once, immediately after the VERDICT line, with every finding's `file:line`, priority "
    "and the required fix in one message"
)


def section(text: str, heading: str) -> str:
    """The body of a `## <heading>` section, up to the next `## ` heading."""
    match = re.search(rf"^## {re.escape(heading)}\n(.*?)(?=^## |\Z)", text, re.MULTILINE | re.DOTALL)
    assert match, heading
    return match.group(1)


def step(text: str, heading: str, number: int) -> str:
    """Numbered step `<number>.` of a section, one line in these skills."""
    match = re.search(rf"^{number}\. .*$", section(text, heading), re.MULTILINE)
    assert match, (heading, number)
    return match.group(0)


class HcomSeatSkillsTest(unittest.TestCase):
    def test_the_audit_seat_runs_one_command_per_bash_call(self):
        self.assertIn(ONE_COMMAND, step(AUDIT.read_text(), "Audit", 1))

    def test_the_worker_keeps_denied_command_names_out_of_quoted_arguments(self):
        self.assertIn(QUOTED_DENY, section(WORKER.read_text(), "Blocked"))

    def test_a_bus_line_carries_ids_paths_and_a_short_note(self):
        self.assertIn(BUS_LINE, step(ORCHESTRATION.read_text(), "The loop", 2))

    def test_the_orchestrator_hands_the_findings_to_the_worker_in_a_file(self):
        text = ORCHESTRATION.read_text()
        self.assertIn(HAND_OFF, step(text, "The loop", 4))
        worker = step(WORKER.read_text(), "Receive", 4)
        self.assertIn(WORKER_WAITS, worker)
        self.assertIn(WORKER_READS, worker)
        reply = section(AUDIT.read_text(), "Reply")
        self.assertIn(FINDINGS_ONCE, reply)
        self.assertIn("Scope questions are answered by the orchestrator, not by you.", reply)

    def test_the_policies_readme_records_the_measured_cases(self):
        text = section(POLICIES.read_text(), "Text that policies see")
        for evidence in ("bus row 467", "pane read 2026-10-24T02:33Z", "`*gh pr comment*`", "&& git status"):
            self.assertIn(evidence, text)


if __name__ == "__main__":
    unittest.main()
