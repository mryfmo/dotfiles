import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RULES = ROOT / "home/dot_config/claude/rules"
RULE = RULES / "agmsg-orchestration.md"
SKILL = ROOT / "home/dot_agents/skills/agmsg-orchestration/SKILL.md"
# The always-loaded Claude rules; gpu.md, latex.md and python.md load only for matching paths.
ALWAYS_LOADED_RULES = (
    "agmsg-orchestration.md",
    "ask-user-question.md",
    "compactiondb.md",
    "crit-review.md",
    "model-selection.md",
    "ponytail.md",
    "pr-integration.md",
    "understand-anything.md",
)
PAIR_AUDIT = "herdr-agents --audit <head-sha> --task <id>"
HEADLESS_AUDIT = "codex <MODEL_PROFILE_AUDIT_CODEX_ARGS> exec --sandbox read-only -C <repo> -o <out>.last.md"


def words(path: Path) -> int:
    return len(path.read_text().split())


class AgmsgOrchestrationRuleTest(unittest.TestCase):
    """The rule carries the regime's invariants within its word budget; the SKILL carries the procedure."""

    def test_rule_states_the_invariants(self) -> None:
        text = RULE.read_text()
        for invariant in (
            "invoke the `agmsg-orchestration` skill",
            "Only the operator opts out",
            "is never an implicit opt-out",
            "Every repository mutation goes to a seated worker of the manifest's `worker_kind`",
            "or after the operator's explicit opt-out for the current task",
            "`make require-crit-review` stay with the orchestrator and are never delegated",
            "one task-level audit of its final head",
            "AGMSG-PONG v1 status=blocked",
            "except the few commands Worker Playbook step 4 sends through the permission gate",
            "Agent-to-agent permission approval is forbidden",
            "never pushes a repository change to `main` directly",
            "gh pr merge --squash",
            "AGMSG_RESOLVE_PROJECT=0 join.sh <team> <name> <type> <worktree>",
            "pairwise-disjoint",
            "disjoint code tasks run concurrently while overlapping code files run serially",
            "gh pr update-branch",
            "never edits the source of its own execution boundary",
            "make check-regime-boundary",
            # Pinned registration and wake tokens; their procedure is in the SKILL.
            "agmsg-dispatch",
            "poke.sh",
            "send.sh",
            "--body-file",
            "inbox.sh",
            "exit 13",
        ):
            with self.subTest(invariant=invariant):
                self.assertIn(invariant, text)

    def test_rule_pointers_name_real_skill_sections(self) -> None:
        rule = RULE.read_text()
        skill = SKILL.read_text()
        # Quoted capitalised names are SKILL headings, except the task-level audit bullet checked below.
        for heading in set(re.findall(r'"([A-Z][^"]+)"', rule)) - {"Task-level audit"}:
            with self.subTest(heading=heading):
                self.assertIn(f"\n## {heading}\n", skill)
        playbooks = {
            "Orchestrator": skill.split("## Orchestrator Playbook", 1)[1].split("\n## ", 1)[0],
            "Worker": skill.split("## Worker Playbook", 1)[1].split("\n## ", 1)[0],
        }
        for playbook, step in re.findall(r"(Orchestrator|Worker) Playbook step (\d+)", rule):
            with self.subTest(playbook=playbook, step=step):
                self.assertRegex(playbooks[playbook], rf"(?m)^{step}\. ")
        self.assertIn('the "Task-level audit" bullet', rule)
        self.assertIn("\n- Task-level audit:", skill)

    def test_word_budgets(self) -> None:
        self.assertLessEqual(words(RULE), 450)
        self.assertLessEqual(sum(words(RULES / name) for name in ALWAYS_LOADED_RULES), 1800)


class AgmsgOrchestrationSkillTest(unittest.TestCase):
    """The SKILL holds the mechanics the rule points at."""

    def test_skill_carries_the_registration_and_delivery_mechanics(self) -> None:
        text = SKILL.read_text()
        for token in (
            "AGMSG_RESOLVE_PROJECT=0 join.sh <team> <name> <type> <worktree>",
            "poke.sh",
            "send.sh",
            "--body-file",
            "agmsg-dispatch",
            "13 =",
            "inbox.sh",
            "gh pr merge --squash",
            "never pushes a repository change to `main` directly",
            "is never an implicit opt-out",
            "actas.<team>__<name>.session",
            "`<common>/objects`",
            "messages.db `read_at`/PONG query",
            "Never run full mode from inside an existing pair workspace",
            "machine-state hygiene that touches no repository",
        ):
            with self.subTest(token=token):
                self.assertIn(token, text)

    def test_skill_carries_the_parallel_execution_and_routing_mechanics(self) -> None:
        text = SKILL.read_text()
        for token in (
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
            with self.subTest(token=token):
                self.assertIn(token, text)

    def test_codex_worker_profile_defaults_to_standard(self) -> None:
        text = SKILL.read_text()
        parallel = text.split("## Parallel workers", 1)[1].split("\n## ", 1)[0]
        for token in (
            "For Codex, seat ordinary tasks with `--profile standard`",
            "use `--profile security` only for trust-boundary tasks",
            "permgate, redaction or secret handling, sandbox or permission policy",
            "`codex-security-dot-aNNN`",
        ):
            with self.subTest(token=token):
                self.assertIn(token, parallel)
        routing = text.split("## Orchestrator Playbook", 1)[1].split("\n4. ", 1)[0]
        self.assertIn("records it and the chosen worker profile in the task file", routing)

    def test_skill_carries_the_audit_gate_and_bot_wait_mechanics(self) -> None:
        text = SKILL.read_text()
        for token in (
            "--audit",
            "--task",
            "-audit-<sha7>.md",
            "AUDIT_EVIDENCE",
            "in_reply_to_id",
            "until a review of the final head appears or 15 minutes pass",
            "needs green CI but no new Bot wait",
            "CI on the new head, then the sweep, then the audit",
            "audit-finding: <n>",
            "Such a review-body finding is listed alongside the top-level inline comments and fixed or dispositioned the same way.",
            "A `review` sweep item whose body carries a `P0`–`P3` badge is a finding with its own `fixed:<commit>` or `not-applicable:<reason>` disposition, never a container for its inline threads.",
            "Deferral",
            "is not a disposition",
        ):
            with self.subTest(token=token):
                self.assertIn(token, text)

    def test_skill_carries_the_session_lessons(self) -> None:
        text = SKILL.read_text()
        for token in (
            "WebFetch tool, not Bash `curl`",
            "Fetch and fast-forward inside the sandbox",
            "until the worker gh credential is provisioned on this host (README operator phase, T90/T90b)",
            "`gh`, `git push`, and an authenticated `git fetch`",
            "-worker-crit.json",
            "writing the task's artifacts at their expected main-checkout paths and masking them with the repository masker, through the permission gate because the main checkout is not writable from a worktree sandbox",
            "(a Claude seat writes them through the permission gate, step 4)",
            "never run `git worktree prune` from a sandboxed seat",
            "`git worktree remove <path>` only",
            "the orchestrator moves them into the main checkout",
            "uv run --no-project .claude/hooks/contextdb_cli.py memory candidates --limit 20",
            "uv run --no-project .claude/hooks/contextdb_cli.py memory promote <id> --scope project",
        ):
            with self.subTest(token=token):
                self.assertIn(token, text)


class AgmsgOrchestrationSingleSourceTest(unittest.TestCase):
    """The audit command appears once, in the SKILL's task-level audit bullet; everything else points there."""

    POINTERS = (
        ROOT / "AGENTS.md",
        ROOT / "README.md",
        RULE,
        RULES / "model-selection.md",
        RULES / "pr-integration.md",
        ROOT / "home/dot_config/codex/AGENTS.md",
        ROOT / "home/dot_agents/skills/gh-first-workflow/SKILL.md",
    )

    def test_audit_command_lives_only_in_the_task_level_audit_bullet(self) -> None:
        skill = SKILL.read_text()
        bullet = skill.split("\n- Task-level audit:", 1)[1].split("\n- ", 1)[0]
        for command in (PAIR_AUDIT, HEADLESS_AUDIT):
            with self.subTest(command=command):
                self.assertEqual(skill.count(command), 1)
                self.assertIn(command, bullet)
                for path in self.POINTERS:
                    with self.subTest(path=path.name):
                        self.assertNotIn(command, path.read_text())
        for path in self.POINTERS:
            with self.subTest(path=path.name):
                self.assertNotIn("exec --sandbox read-only", path.read_text())

    def test_codex_agents_points_at_the_worklog_section(self) -> None:
        codex = (ROOT / "home/dot_config/codex/AGENTS.md").read_text()
        self.assertIn("「Codex seat worklogs」", codex)
        self.assertIn("\n## Codex seat worklogs\n", SKILL.read_text())

    def test_skill_masks_evidence_with_a_runnable_command(self) -> None:
        # The validator is not executable (mode 100644), so the SKILL names it only through uv run.
        text = SKILL.read_text()
        runnable = "`uv run --no-project --with pyyaml scripts/validate-agent-assets.py --mask-secrets"
        self.assertGreaterEqual(text.count(runnable), 3)
        self.assertEqual(text.count("scripts/validate-agent-assets.py --mask-secrets"), text.count(runnable))

    def test_contextdb_cli_is_invoked_with_uv_run(self) -> None:
        paths = [
            ROOT / "CLAUDE.md",
            ROOT / "AGENTS.md",
            SKILL,
            ROOT / "home/dot_config/codex/AGENTS.md",
            *sorted(RULES.glob("*.md")),
        ]
        for path in paths:
            text = path.read_text()
            with self.subTest(path=path.name):
                self.assertNotIn("python3 .claude/hooks/contextdb_cli.py", text)
                # Without --no-project, uv would create or sync the target project's environment first.
                self.assertNotIn("uv run .claude/hooks/contextdb_cli.py", text)
        for path in (ROOT / "CLAUDE.md", SKILL, RULES / "compactiondb.md", ROOT / "home/dot_config/codex/AGENTS.md"):
            with self.subTest(path=path.name):
                self.assertIn("uv run --no-project .claude/hooks/contextdb_cli.py", path.read_text())


class AgmsgOrchestrationForbiddenPhrasesTest(unittest.TestCase):
    def test_docs_no_longer_name_codex_review_commit(self) -> None:
        for path in (
            ROOT / "AGENTS.md",
            ROOT / "README.md",
            RULE,
            SKILL,
            RULES / "model-selection.md",
        ):
            text = path.read_text()
            lines = [line for line in text.splitlines() if "review --commit" in line]
            with self.subTest(path=path.name):
                self.assertNotIn("audit review --commit", text)
                # README keeps one sentence explaining why `codex review --commit` is not used.
                self.assertEqual(
                    [line for line in lines if not line.startswith("`codex review --commit` is not used")], []
                )

    def test_rule_and_skill_name_worker_seats_not_codex_workers(self) -> None:
        # The worker kind comes from the manifest; model-selection.md's security-profile sentence is exempt.
        for path in (RULE, SKILL):
            with self.subTest(path=path.name):
                self.assertNotIn("Codex worker", path.read_text())

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
