import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RULE = ROOT / "home/dot_config/claude/rules/agmsg-orchestration.md"
SKILL = ROOT / "home/dot_agents/skills/agmsg-orchestration/SKILL.md"


class AgmsgOrchestrationDocsParityTest(unittest.TestCase):
    """The rule and the SKILL must teach the same agmsg registration and delivery invariants."""

    def test_rule_and_skill_share_the_registration_and_delivery_invariants(self) -> None:
        for path in (RULE, SKILL):
            text = path.read_text()
            for invariant in (
                "AGMSG_RESOLVE_PROJECT=0 join.sh <team> <name> <type> <worktree>",
                "poke.sh",
                "send.sh",
                "--body-file",
                "agmsg-dispatch",
                "exit 13" if path == RULE else "13 =",
                "inbox.sh",
                "gh pr merge --squash",
                "never pushes a repository change to `main` directly",
                "is never an implicit opt-out",
            ):
                with self.subTest(path=path.name, invariant=invariant):
                    self.assertIn(invariant, text)

    def test_rule_and_skill_share_the_parallel_execution_and_routing_invariants(self) -> None:
        for path in (RULE, SKILL):
            text = path.read_text()
            for invariant in (
                "pairwise-disjoint",
                "--add-worker",
                "re-tasked immediately",
                "acceptance follows RESULT arrival order",
                "gh pr update-branch",
                "Self-Modification",
                "home/dot_claude/modify_private_settings.json",
                "`claude.sandbox`",
                "home/dot_agents/permgate-policy.yaml",
                "PermissionRequest hook of both seats, goes to the operator",
                "AGMSG-PONG v1 status=blocked",
                "--ask-for-approval never",
            ):
                with self.subTest(path=path.name, invariant=invariant):
                    self.assertIn(invariant, text)

    def test_rule_and_skill_share_the_audit_gate_and_bot_wait_invariants(self) -> None:
        for path in (RULE, SKILL):
            text = path.read_text()
            for invariant in (
                "--audit",
                "--task",
                "-audit-<sha7>.md",
                "AUDIT_EVIDENCE",
                "in_reply_to_id",
                "until a review of the final head appears or 15 minutes pass",
            ):
                with self.subTest(path=path.name, invariant=invariant):
                    self.assertIn(invariant, text)

    def test_docs_no_longer_name_codex_review_commit(self) -> None:
        for path in (
            ROOT / "AGENTS.md",
            ROOT / "README.md",
            RULE,
            SKILL,
            ROOT / "home/dot_config/claude/rules/model-selection.md",
        ):
            lines = [line for line in path.read_text().splitlines() if "review --commit" in line]
            with self.subTest(path=path.name):
                # README keeps one sentence explaining why `codex review --commit` is not used.
                self.assertEqual(
                    [line for line in lines if not line.startswith("`codex review --commit` is not used")], []
                )

    def test_rule_drops_the_worker_network_escalation(self) -> None:
        self.assertNotIn("network access stays off", RULE.read_text())

    def test_skill_drops_the_pane_status_gate_and_raw_pane_wakes(self) -> None:
        text = SKILL.read_text()
        for stale in (
            "isn't already `working`",
            "wake or prompt a worker with `herdr pane run",
            "upstream's own default) and Claude Code",
        ):
            with self.subTest(stale=stale):
                self.assertNotIn(stale, text)


if __name__ == "__main__":
    unittest.main()
