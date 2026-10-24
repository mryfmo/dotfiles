"""The standing Claude rules after the regime cutover (U32): one short regime rule, no agmsg-era rule, and the
deployed copies of the retired rules removed by chezmoi."""

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RULES = ROOT / "home/dot_config/claude/rules"
SYMLINKS = ROOT / "home/dot_claude/rules"
REGIME = RULES / "regime.md"
RETIRED = ("agmsg-orchestration", "crit-review", "pr-integration")
RETIRED_TEXT = re.compile(r"agmsg|require-crit-review|pr-feedback|Crit")


class RulesCutoverTest(unittest.TestCase):
    def test_no_retired_rule_or_its_symlink_remains(self):
        names = {path.name for path in (*RULES.iterdir(), *SYMLINKS.iterdir())}
        for rule in RETIRED:
            with self.subTest(rule=rule):
                self.assertFalse({n for n in names if rule in n}, names)

    def test_no_rule_names_the_retired_regime(self):
        for rule in sorted(RULES.glob("*.md")):
            with self.subTest(rule=rule.name):
                self.assertEqual(RETIRED_TEXT.findall(rule.read_text()), [])

    def test_the_regime_rule_is_short_and_points_at_the_living_documents(self):
        text = REGIME.read_text()
        self.assertLessEqual(len(text.splitlines()), 15)
        self.assertTrue(text.startswith("## "), text[:20])
        for token in ("hcom-orchestration", "hcom-worker", "hcom-audit", "AGENTS.md", "--match-head-commit"):
            with self.subTest(token=token):
                self.assertIn(token, text)
        # The Routing invariant of the retired rule, kept word for word.
        self.assertIn(
            "A seat never edits the source of its own execution boundary: Claude-boundary changes go to a Codex "
            "seat, Codex-boundary changes to a Claude seat, and shared sources or permgate to the operator.",
            text,
        )

    def test_the_regime_rule_is_linked_like_the_others(self):
        self.assertEqual(
            (SYMLINKS / "symlink_regime.md.tmpl").read_text(),
            "{{ .chezmoi.sourceDir }}/dot_config/claude/rules/regime.md\n",
        )

    def test_chezmoi_removes_the_deployed_retired_rules(self):
        entries = (ROOT / "home/.chezmoiremove").read_text().splitlines()
        for rule in RETIRED:
            for target in (f".config/claude/rules/{rule}.md", f".claude/rules/{rule}.md"):
                with self.subTest(target=target):
                    self.assertIn(target, entries)


if __name__ == "__main__":
    unittest.main()
