"""The weighted finding rule on its three text surfaces, and the number the thread check reads (regime-cutover U124).

AGENTS.md "Audit" scores every finding (frequency and severity, 1 to 10) and names the threshold once in its verdict
bullet; "Code Review Rules" tells every reviewer to rate and every coding agent not to design for cases nobody asked
for; home/dot_config/claude/rules/regime.md carries the coding rule to every repository through chezmoi; and
pr-threads-check.sh reads the number as WEIGHT_THRESHOLD. These tests pin the sentences and keep the numbers equal,
so the rule the reviewer reads and the rule the lever enforces never drift apart.
"""

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
AGENTS = ROOT / "AGENTS.md"
REGIME = ROOT / "home/dot_config/claude/rules/regime.md"
LEVERS = ROOT / "scripts/orchestrator"
DESIGN_RULE = (
    "Do not design for rare or future cases nobody has asked for. A case is real when a test, an incident, a user or "
    "a measured run names it; otherwise state it in the Contract's Left out and move on."
)
FILED = "`filed: f=<n> s=<n> <reason>`"
VERDICT_BULLET = "- A finding's weight is its frequency times its severity."
REVIEWER_BULLET = "- The Codex Bot and every reviewer rate each finding's frequency and severity 1 to 10 in the finding text"


def section(text, heading):
    """The `## <heading>` section of `text`, up to the next `## ` heading."""
    start = text.index(f"\n## {heading}\n") + 1
    end = text.find("\n## ", start)
    return text[start : end if end != -1 else len(text)]


def bullet(text, prefix):
    """The one bullet line of `text` that starts with `prefix`."""
    lines = [line for line in text.splitlines() if line.startswith(prefix)]
    assert len(lines) == 1, lines
    return lines[0]


def lever_thresholds(name):
    """Every `WEIGHT_THRESHOLD=<n>` line of the lever, so a test can say it is named once."""
    return re.findall(r"^WEIGHT_THRESHOLD=(\d+)$", (LEVERS / name).read_text(), re.MULTILINE)


class ReviewRulesTest(unittest.TestCase):
    def setUp(self):
        self.agents = AGENTS.read_text()
        self.audit = section(self.agents, "Audit")
        self.review = section(self.agents, "Code Review Rules")

    def test_the_audit_finding_list_scores_frequency_and_severity_after_confidence(self):
        match = re.search(r"^- Report each finding with:\n((?:  - .*\n)+)", self.audit, re.MULTILINE)
        assert match is not None, self.audit
        items = match.group(1).splitlines()
        confidence = items.index("  - confidence;")
        self.assertEqual(
            items[confidence + 1 : confidence + 3],
            [
                "  - frequency 1..10: how often the case arises in this repository's real runs, 1 for a case no run, "
                "test, incident or user has produced, 10 for every run;",
                "  - severity 1..10: what the case costs when it arises, 1 for cosmetic, 10 for data loss, a secret "
                "leaving the host, or a wrong merge;",
            ],
        )

    def test_the_verdict_bullet_is_the_weighted_rule_and_names_the_number_once(self):
        verdict = bullet(self.audit, VERDICT_BULLET)
        self.assertIn("A P0 or P1 finding with weight 10 or more makes the verdict `incorrect`.", verdict)
        self.assertIn("A finding of any priority with weight under that threshold is `filed`", verdict)
        self.assertIn(f"the code left as it is, and closed in its review thread as {FILED}", verdict)
        self.assertIn("A P2 or P3 finding at or above the threshold", verdict)
        self.assertEqual(verdict.count("10"), 1, verdict)

    def test_the_number_in_agents_md_equals_the_lever_constant(self):
        match = re.search(r"with weight (\d+) or more", bullet(self.audit, VERDICT_BULLET))
        assert match is not None
        number = match.group(1)
        # Named once in the lever (the brief's `WEIGHT_THRESHOLD=10`), and in the resolve lever, whose `disposition`
        # is the same text (DispositionDriftTest).
        self.assertEqual(lever_thresholds("pr-threads-check.sh"), [number])
        self.assertEqual(lever_thresholds("pr-thread-resolve.sh"), [number])
        reviewer = bullet(self.review, REVIEWER_BULLET)
        self.assertIn(f"A finding whose product is under {number} is filed, not fixed", reviewer)

    def test_code_review_rules_hold_the_reviewer_bullet_and_the_design_sentence(self):
        reviewer = bullet(self.review, REVIEWER_BULLET)
        self.assertIn("on the scales of the Audit section", reviewer)
        self.assertIn(f"its thread is closed as {FILED}", reviewer)
        self.assertIn(f"\n- {DESIGN_RULE}\n", self.review)

    def test_the_claude_regime_rule_carries_the_design_sentence(self):
        self.assertIn(f"\n- **Cases.** {DESIGN_RULE}\n", REGIME.read_text())


if __name__ == "__main__":
    unittest.main()
