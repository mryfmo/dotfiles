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
            "--match-head-commit <audited head sha>",
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

    def test_claude_worker_merge_denials_and_prefix_limits_are_documented(self) -> None:
        for path in (ROOT / "README.md", SKILL):
            text = " ".join(path.read_text().split())
            with self.subTest(path=path.name):
                for token in (
                    "Bash(gh pr merge:*)",
                    "Bash(gh api -X PUT:*)",
                    "Bash(gh api --method PUT:*)",
                    "Bash(gh api graphql:*)",
                    "herdr-agents",
                    ".claude/settings.local.json",
                    "deny rules",
                    "nested subcommands",
                    "permission mode",
                    "flag after the path",
                    "integration gate",
                    "https://code.claude.com/docs/en/permissions",
                ):
                    self.assertIn(token, text)
                self.assertNotIn("Claude worker seats have no such denial yet", text)
                self.assertNotIn("Claude seats get their deny rules in a separate task", text)

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
            "--match-head-commit <audited head sha>",
            "never pushes a repository change to `main` directly",
            "is never an implicit opt-out",
            "actas.<team>__<name>.session",
            "`<common>/objects`",
            "messages.db `read_at`/PONG query",
            "Never run full mode from inside an existing managed workspace",
            "`--restart-worker` is retired and exits 2",
            "herdr-agents --add-worker [<worktree>]",
            "remove every worker with `herdr-agents --remove-worker <worktree>`",
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
            "So a Claude seat runs three commands outside the sandbox through the permission gate:",
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


class AgmsgRegimePatternTest(unittest.TestCase):
    """Plan 006 Phase A: the review and fix pattern, each rule in the section that owns it."""

    @staticmethod
    def section(text: str, start: str, end: str = "\n## ") -> str:
        return text.split(start, 1)[1].split(end, 1)[0]

    def invariants(self) -> str:
        return self.section(SKILL.read_text(), "## Review and integration invariants")

    # Plan 006 S1 on the docs tests (class unpinned): token tests pin only the clauses their author chose, so
    # each regime rule section is also pinned whole; a rule changes only together with its fixture (INV-12).
    PINNED_SECTIONS = (
        # name, file, outer slice or None, (start, end): the start marker is part of the pinned text.
        ("invariants", SKILL, None, ("## Review and integration invariants", "\n## ")),
        ("worker-step-15", SKILL, None, ("\n15. After the final push", "\n## ")),
        ("orchestrator-step-7", SKILL, ("## Orchestrator Playbook", "\n## "), ("\n7. ", "\n8. ")),
        ("message-contract", SKILL, None, ("## Message Contract v1", "\n## ")),
        (
            "code-review-orchestration",
            ROOT / "AGENTS.md",
            None,
            ("### Orchestration records and trust-boundary code", "\n## "),
        ),
    )

    @staticmethod
    def normalized(text: str) -> str:
        return "\n".join(line.rstrip() for line in text.split("\n")).strip()

    def test_regime_rule_sections_are_pinned_whole(self) -> None:
        for name, path, outer, (start, end) in self.PINNED_SECTIONS:
            with self.subTest(section=name):
                text = path.read_text()
                if outer:
                    text = self.section(text, *outer)
                fixture = ROOT / "tests/fixtures/regime" / f"{name}.md"
                self.assertEqual(
                    self.normalized(start + self.section(text, start, end)),
                    self.normalized(fixture.read_text()),
                    f"regime rule section {name} changed: declare the change by updating "
                    f"tests/fixtures/regime/{name}.md in the same commit and listing it in the RESULT",
                )

    def test_design_review_runs_in_paired_rounds_with_a_cap(self) -> None:
        text = self.invariants()
        for token in (
            "get the same design hash at the same time",
            "The orchestrator revises once per pair of results",
            "opens no round while one is still open",
            "frozen at the hash the pair last accepted",
            # Thread 4243537279: a revision after the third pair would freeze an unreviewed hash.
            "any later change to a hashed key is a new pair (INV-7)",
            # Thread 4243732324: a third pair that returns revise or reject has no accepted hash to freeze.
            "on its revise or reject nothing is frozen",
            "becomes a residual list that is worker input",
            "never implementation detail",
        ):
            with self.subTest(token=token):
                self.assertIn(token, text)

    def test_task_file_review_is_one_round_with_a_fixed_stop_condition(self) -> None:
        text = self.invariants()
        for token in (
            "A task-file review is one round with a fixed stop condition",
            "no contradiction with the design",
            "the premises hold",
            "`allowed_files` covers every touch point that grep finds",
            "one invariant check (a `-contract-a01` id maps to its implementing entry)",
        ):
            with self.subTest(token=token):
                self.assertIn(token, text)

    def test_a_design_lands_on_main_before_its_task(self) -> None:
        # Thread 4243537281: a boundary PR carrying the design is INV-2's dispatch prerequisite.
        text = self.invariants()
        for token in ("carries no task draft under review", "before its implementing TASK is dispatched (INV-2)"):
            with self.subTest(token=token):
                self.assertIn(token, text)
        self.assertNotIn("is never a prerequisite of a dispatch", text)

    def test_boundary_merge_sentence_names_the_in_job_decision(self) -> None:
        # PR 320 removes the changes job: a skipped required job reports Success, so each job decides itself.
        text = self.invariants()
        self.assertIn(
            "each required job decides inside itself and reports success on an `.orchestration`-only diff; "
            "a skipped required job would report Success (fail-open), so no required job carries a job-level "
            "`if` or a `needs`.",
            text,
        )
        self.assertNotIn("the ruleset accepts the resulting `skipped` required checks", text)

    def test_a_trust_boundary_task_carries_a_threat_table(self) -> None:
        text = self.invariants()
        for token in (
            "carries a `threat_table` in its front matter",
            "`closed: tests/<file>::<name>`",
            "`residual: <sentence>`",
            "`out-of-scope: <task id>`",
            "Shape is `schemas/task.json`'s",
            "Substance is the reviewers'",
            "The table is the task's completion condition",
            "a missing row is added once, counted as an amendment",
        ):
            with self.subTest(token=token):
                self.assertIn(token, text)

    def test_threat_table_rule_carries_no_grammar(self) -> None:
        # The reset of PR 318: shape lives in schemas/task.json, never as a pattern in prose.
        text = self.invariants()
        self.assertNotIn("^(closed|residual|out-of-scope)", text)
        self.assertNotIn("`none`", text)

    # Thread 4240348412 is closed by a05's counters bullet: the script reads the whole history (scripts/regime-counters.sh:85), no by-hand read remains.
    def test_open_third_round_threads_have_an_integration_outcome(self) -> None:
        # Thread 4240348414: an open: item needs a path through steps 10.1 and 10.5.
        playbook = self.section(SKILL.read_text(), "## Orchestrator Playbook")
        for token in ("is a sweep item like any other", "the PR is not merged, never with the thread open"):
            with self.subTest(token=token):
                self.assertIn(token, playbook)

    def test_counters_run_before_every_acceptance_action(self) -> None:
        text = self.invariants()
        self.assertIn(
            "Before every acceptance action (revise, accept, merge) the orchestrator runs "
            "`scripts/regime-counters.sh <task id>`",
            text,
        )
        # Thread 4240566268: the counts are evidence for the S1/S2 decision.
        self.assertIn("and pastes its output into the acceptance record", text)

    def test_bot_fix_rounds_are_capped_and_the_pr_is_ready_first(self) -> None:
        step = self.section(SKILL.read_text(), "\n15. After the final push", "\n## ")
        for token in (
            # Thread 4240646079: after a fix push the PR is already ready, and `gh pr ready` fails there.
            "Mark the PR ready for review with `gh pr ready <n>` before the first wait, while it is still a draft",
            "within 10 minutes, post `@codex review`",
            "at most twice. The third Bot round is not fixed",
            "`AGMSG-RESULT … bot_rounds=3`",
            "in the background and the Bot wait below at the same time",
            "listed as `open:<thread id>`",
            "an escalated label that the next bullet's",
            "never from the end of CI",
        ):
            with self.subTest(token=token):
                self.assertIn(token, step)

    def test_open_review_body_findings_have_an_identifier(self) -> None:
        # Thread 4240290382: a review-body finding has no thread id.
        step = self.section(SKILL.read_text(), "\n15. After the final push", "\n## ")
        self.assertIn("(`open:review-<review id>` for a review-body finding)", step)

    def test_the_ci_watch_is_joined_before_the_result(self) -> None:
        # Thread 4240290391: the background CI watcher's exit status gates the RESULT.
        step = self.section(SKILL.read_text(), "\n15. After the final push", "\n## ")
        self.assertIn(
            "Wait for that watcher's exit status before the RESULT: a non-zero exit means no RESULT until CI passes.",
            step,
        )

    def test_question_pongs_are_in_the_contract(self) -> None:
        # Thread 4243732330: INV-6 counts AGMSG-PONG status=question, so the contract must allow it.
        contract = self.section(SKILL.read_text(), "## Message Contract v1")
        for token in ("status=alive|blocked|question", "`question`: the worker holds and asks; INV-6 counts it."):
            with self.subTest(token=token):
                self.assertIn(token, contract)

    def test_a_revise_acceptance_names_the_previous_head_and_a_check(self) -> None:
        contract = self.section(SKILL.read_text(), "## Message Contract v1")
        self.assertIn("carries `previous_head=<the RESULT head being revised>`", contract)
        self.assertIn("one failing-test selector per finding (`check=tests/<file>::<name>`)", contract)
        self.assertIn("`.orchestration/<task id>/revise.yaml`", contract)

    def test_code_review_rules_cover_orchestration_records_and_threat_tables(self) -> None:
        rules = self.section((ROOT / "AGENTS.md").read_text(), "## Code Review Rules")
        subsection = self.section(rules, "### Orchestration records and trust-boundary code", "\n### ")
        for token in (
            "review them for secrets and home-directory paths only",
            "Judge from the diff, whatever the task's metadata says, whether a change touches a trust boundary",
            "report a missing table or a missing row",
            "a `residual` row whose control does not mitigate the risk",
            "an `out-of-scope` row whose owner does not own it",
            "Do not re-raise a `residual` row whose control mitigates the risk",
            "Shape (the test selector, the sentence, the owning task id) is the schema's to check, not the review's",
        ):
            with self.subTest(token=token):
                self.assertIn(token, subsection)

    def test_orchestration_records_rule_binds_the_bot_review_only(self) -> None:
        # Audit of 27ea99b2: the secrets-only scope is plan 006 A4's for the Bot, never the auditor's.
        rules = self.section((ROOT / "AGENTS.md").read_text(), "## Code Review Rules")
        bullet = self.section(rules, "### Orchestration records and trust-boundary code", "\n### ").split("\n- ")[1]
        for token in (
            "in the pull-request review by the Codex Bot, review them for secrets and home-directory paths only",
            "The task-level audit keeps the full scope of the Audit section.",
            # Thread 4243732326: the next bullet reviews the threat table inside task.md.
            "except a trust-boundary task's `threat_table`",
        ):
            with self.subTest(token=token):
                self.assertIn(token, bullet)

    def test_shape_is_checked_by_hand_until_the_schema_lands(self) -> None:
        # Audit of 27ea99b2: neither schemas/task.json nor its validator exists yet.
        sentence = (
            "Until `schemas/task.json` lands in wave V1, the task-file review checks the three shape rules by hand."
        )
        rules = self.section((ROOT / "AGENTS.md").read_text(), "## Code Review Rules")
        for name, text in (
            ("SKILL invariants", self.invariants()),
            ("AGENTS.md", self.section(rules, "### Orchestration records and trust-boundary code", "\n### ")),
        ):
            with self.subTest(section=name):
                self.assertIn(sentence, text)

    def test_pattern_rules_pin_their_safeguards(self) -> None:
        # Audit of 27ea99b2: each safeguard could be removed with every other test still passing.
        rules = self.section((ROOT / "AGENTS.md").read_text(), "## Code Review Rules")
        subsection = self.section(rules, "### Orchestration records and trust-boundary code", "\n### ")
        self.assertIn("report a `closed` row whose test does not close it", subsection)
        text = self.invariants()
        for token in (
            "(the tree and its tests, task.md, workflow files,",
            "a fresh Claude context on the `review` profile and a Codex read-only run",
            # Item 7 of a04 reworded the clause; the safeguard is the same sentence.
            "any merged boundary that carries the design meets that precondition",
        ):
            with self.subTest(token=token):
                self.assertIn(token, text)

    def test_closed_selector_existence_is_checked_at_acceptance(self) -> None:
        # Audit of b7ae2d54 and thread 4240646082: a closed row's test does not exist before implementation.
        text = self.invariants()
        for token in (
            "a `closed` selector names a test present in the PR tree at acceptance and in the schema's validation of the PR",
            "For a `closed` row it checks the selector's form only, since the test does not exist before implementation.",
        ):
            with self.subTest(token=token):
                self.assertIn(token, text)

    def test_the_bot_wait_filters_the_codex_bot(self) -> None:
        # Audit of b7ae2d54 and thread 4243369347: a CodeRabbit review matched `.user.type=="Bot"` and ended the wait.
        step = self.section(SKILL.read_text(), "\n15. After the final push", "\n## ")
        for token in (
            '.[]|select(.user.login=="chatgpt-codex-connector[bot]" and .commit_id=="<head-sha>")',
            '.[]|select(.in_reply_to_id == null and .user.login=="chatgpt-codex-connector[bot]" and .original_commit_id=="<head-sha>")',
            "A human comment, a CodeRabbit review or an earlier head's review never ends the wait.",
        ):
            with self.subTest(token=token):
                self.assertIn(token, step)
        self.assertNotIn('.user.type=="Bot"', step)

    def test_shape_rules_and_the_decision_sentence_are_pinned(self) -> None:
        # Audit of b7ae2d54: the S1/S2 decision and the three shape rules could each be removed unnoticed.
        text = self.invariants()
        for token in (
            "S2 is decided from INV-6's counts",
            "a `closed` selector names a test present in the PR tree",
            "an `out-of-scope` owner is a task id in the design's `implementing_tasks`",
            "a `residual` payload is a sentence of at least 20 characters",
        ):
            with self.subTest(token=token):
                self.assertIn(token, text)

    def test_counters_bullet_names_owners_not_sources(self) -> None:
        # Plan 006 S1 on the counters bullet: it states its obligations by reference and names no source.
        bullet = self.section(self.invariants(), "\n- Before every acceptance action", "\n- ")
        for token in (
            "for each component it prints as `unknown` the record pastes the command and output that read the source INV-6 names for that component",
            "gives a class to every finding the PR-feedback sweep lists, whatever its disposition, and to every task-level audit finding",
        ):
            with self.subTest(token=token):
                self.assertIn(token, bullet)
        for phrase in ("review bodies", "by hand", "gh api --paginate", "until it is on `main`"):
            with self.subTest(phrase=phrase):
                self.assertNotIn(phrase, bullet)

    def test_the_ci_watcher_survives_the_no_checks_race(self) -> None:
        # Thread 4243516880: `gh pr checks --watch` exits 1 with "no checks reported" before the first check appears.
        step = self.section(SKILL.read_text(), "\n15. After the final push", "\n## ")
        self.assertIn(
            "Right after a push GitHub can report no checks yet, and the watcher then exits 1 with `no checks reported`: start it once a check is listed, and restart it on that message instead of reading it as a CI failure.",
            step,
        )

    def test_the_worker_stops_itself_on_repeated_findings(self) -> None:
        # Plan 006 A7-1: PR 317's V0 worker kept fixing through seven Bot-reviewed heads and never read its halt.
        step = self.section(SKILL.read_text(), "\n15. After the final push", "\n## ")
        for token in (
            "fixes nothing more",
            # The task lists this token and the --history-only one in backticks; in the prose both sit inside longer code spans.
            "status=blocked note=S1|INV-6",
            "whichever limit comes first ends the fixing",
            "never a disposition",
            "never for a fourth round of the same class",
            "not only the current head's",
            "and the review bodies whose `commit_id`, is at or after the task's first commit on the PR",
            "counted toward the fix cap and the classes, never INV-6's heads",
            "--history-only",
            # Bot fix round 1 on 9d001bcb (threads 4244128846, 4244128851, 4244128854, 4244128857).
            # Revise round 1 (plan S1 on the class-count sentence): the worker counts the Codex Bot's findings only.
            "an early stop",
            "never widens the worker's input beyond the Codex Bot's items",
            "When a stop (heads=2 or three of a class) coincides with the third Bot round",
            "a Bot title never (only its reduced class)",
            "instead of a blocked PONG, and then waits for the ACCEPTANCE: one handoff",
            "pastes its complete output (the count line, the `detail:` line and any `S2:` line)",
        ):
            with self.subTest(token=token):
                self.assertIn(token, step)

    def test_the_orchestrator_watches_from_github_and_history(self) -> None:
        # Plan 006 A7-2: a worker that ignores its PING is seen from GitHub and history, never from panes.
        playbook = self.section(SKILL.read_text(), "## Orchestrator Playbook")
        for token in (
            "at least every 30 minutes after a TASK",
            "`…/pulls/<n>/comments`",
            "never detects completion, which stays the RESULT's arrival",
            "45 minutes without a push, a PONG or a RESULT is a stall",
            "`herdr-agents --remove-worker <worktree> --force`",
            # Bot fix round 1 on 9d001bcb (threads 4244128840, 4244128859).
            "all three with `--paginate`",
            "the next seat is created in a clean worktree",
            # Thread 4244175778: a worker pushing less than 45 minutes apart never stalls.
            "as soon as it first sees a task past the A2 cap or an INV-6 count",
            # Thread 4244203607: a PING the worker reads and ignores still leads to removal.
            "read or unread",
        ):
            with self.subTest(token=token):
                self.assertIn(token, playbook)

    def test_workers_open_the_pr_as_a_draft(self) -> None:
        # Thread 4240566266: step 15's `gh pr ready` starts the Bot timer only on a draft PR.
        step = self.section(SKILL.read_text(), "\n2. Switch to the `repo`", "\n3. ")
        self.assertIn("`gh pr create --draft --head <branch>`", step)

    def test_workers_commit_inside_the_sandbox(self) -> None:
        # Audit of 27ea99b2: only the push is a step 4 exemption, so the commit stays inside.
        step = self.section(SKILL.read_text(), "\n2. Switch to the `repo`", "\n3. ")
        for token in (
            "Commit inside the sandbox, with `git -c commit.gpgsign=false` when the signing key is unreadable there",
            "only the push leaves the sandbox",
            # Thread 4240598179: a Codex seat never leaves its sandbox, push included.
            "a Codex seat pushes from inside it (step 4)",
        ):
            with self.subTest(token=token):
                self.assertIn(token, step)


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
