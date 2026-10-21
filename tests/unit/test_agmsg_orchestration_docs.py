import json
import os
import re
import shlex
import subprocess
import sys
import tempfile
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
OLD_ACCEPTANCE = (
    "Acceptance review, adversarial RESULT review, and review-profile work remain orchestrator-side; "
    "never delegate them to a worker, and keep `make require-crit-review` as the final integration step. "
    "Revisit only if worker-side model capability surpasses the orchestrator tier."
)
ACCEPTANCE = (
    "Only acceptance decisions and final merge stay orchestrator-side. Seats and scripts handle "
    "integration, adversarial RESULT review, review-profile work, gate and records through `verdict.sh`, "
    "`audit-pool.sh`, `result-precheck.sh`, `acceptance-front-matter.py` and `dispatch.sh --next`. "
    "Pending each mechanism, Delegation's interim exemption permits manual orchestrator execution. "
    "Every code-changing RESULT gets one task-level audit of its final head; findings are input, never "
    'approval (the "Task-level audit" bullet).'
)
CONTRACT_ADDITIONS = {
    "\n`AGMSG-RESULT v1` fields:": (
        "\nTask front matter's optional `requires_decision:` lists decision ids without which the task may not "
        "proceed. The task-consistency checker verifies each id exists in `.orchestration/decisions.tsv` "
        "with a result other than `pending`.\n"
    ),
    "\nTasks that create persistent side effects": (
        "\nBefore sending, the worker writes the RESULT line's `key=value` pairs to "
        "`.orchestration/<task>/result.txt`; `result-precheck.sh` reads that file.\n"
    ),
    "\nRESULT reports must mark durable facts": (
        "\nThe RESULT field `precheck=<sha256 of precheck.json>` is the digest of the precheck evidence "
        "already emitted by P1-5.\n"
    ),
    "\n`question`: the worker holds and asks; INV-6 counts it.": (
        "\nThe optional PONG field `context=<percent>` reports the seat's context usage. "
        "`dispatch.sh --next` reads it and refuses a seat above its context threshold.\n"
    ),
}


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
            "adversarial RESULT review",
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

    def test_boundary_cadence_is_stated_between_integrations(self) -> None:
        self.assertIn("records reach `main` only between integrations (plan 020 step 3)", RULE.read_text())
        invariants = SKILL.read_text().split("## Review and integration invariants", 1)[1].split("\n## ", 1)[0]
        self.assertIn("queued only while no other PR is between its final head and its merge", invariants)

    def acceptance_paragraphs(self) -> tuple[str, str]:
        rule = RULE.read_text().split("- **Acceptance.** ", 1)[1].split("\n", 1)[0]
        invariants = AgmsgRegimePatternTest.section(SKILL.read_text(), "## Review and integration invariants")
        paragraphs = re.findall(r"(?m)^- (?:Acceptance review,|Only acceptance decisions).*", invariants)
        self.assertEqual(len(paragraphs), 1)
        return rule, paragraphs[0].removeprefix("- ")

    def test_acceptance_paragraph_names_the_seat_mechanisms(self) -> None:
        for name, paragraph in zip(("rule", "skill"), self.acceptance_paragraphs(), strict=True):
            with self.subTest(document=name):
                self.assertEqual(paragraph, ACCEPTANCE)
        for obsolete in ("are never delegated", "never delegate them to a worker", "Revisit only if worker-side"):
            with self.subTest(obsolete=obsolete):
                self.assertNotIn(obsolete, RULE.read_text() + SKILL.read_text())

    def test_acceptance_paragraph_matches_skill(self) -> None:
        self.assertEqual(*self.acceptance_paragraphs())

    def test_delegation_lists_the_interim_integration_exemption(self) -> None:
        delegation = RULE.read_text().split("- **Delegation.** ", 1)[1].split("\n", 1)[0]
        for token in (
            "declared exemptions",
            "interim manual",
            "integration",
            "reviews",
            "gate",
            "records",
            "pending",
            "mechanisms",
            "agmsg/herdr control plane",
            "evidence-sync bookkeeping",
            "acceptance decision",
            "final merge",
            "repository-free hygiene",
            "the operator's explicit opt-out for the current task",
        ):
            with self.subTest(token=token):
                self.assertIn(token, delegation)

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
            "Complete every worker command, including gh, git push and authenticated git fetch, inside the sandbox and allowlist without forbidden actions or escalation",
            "-worker-crit.json",
            "main-checkout artifact writes and masking under evidence-sync",
            "exact expected relative paths in the worker's own worktree",
            "never run `git worktree prune` from a sandboxed seat",
            "`git worktree remove <path>` only",
            "the orchestrator moves them into the main checkout",
            "uv run --no-project .claude/hooks/contextdb_cli.py memory candidates --limit 20",
            "uv run --no-project .claude/hooks/contextdb_cli.py memory promote <id> --scope project",
        ):
            with self.subTest(token=token):
                self.assertIn(token, text)

    def test_worker_playbook_has_no_sandbox_exceptions(self):
        text = SKILL.read_text()
        worker = text.split("## Worker Playbook\n", 1)[1].split("\n## ", 1)[0]
        orchestrator = text.split("## Orchestrator Playbook\n", 1)[1].split("\n## Worker Playbook", 1)[0]
        sentence = "Complete every worker command, including gh, git push and authenticated git fetch, inside the sandbox and allowlist without forbidden actions or escalation; anything that cannot complete there is `AGMSG-PONG v1 status=blocked` naming the exact command and boundary."
        self.assertIn(sentence, worker)
        for escape in (
            "only the push leaves the sandbox",
            "runs three commands outside",
            "Three documented cases run outside",
            "writes them through the permission gate",
            "a Claude worker runs it outside",
            "runs it outside the sandbox from the first attempt",
            "main-checkout CompactionDB `memory add`",
        ):
            self.assertNotIn(escape, worker)
        for operation in (
            "main-checkout artifact writes and masking",
            "CompactionDB consolidation",
            "agmsg-dispatch control-plane delivery",
        ):
            self.assertIn(operation, orchestrator)
        self.assertIn("orchestrator-only", orchestrator)

    def test_deferred_ledger_calls_bind_github_host_under_hostile_gh_host(self):
        task = ROOT / ".orchestration/dotfiles-T133-worker-write-boundary-a02/task.md"
        paragraph = task.read_text().split("## Out of scope\n", 1)[1].split("## Check\n", 1)[0]
        templates = [shlex.split(c) for c in re.findall(r"`(gh api --hostname github.com [^`]+)`", paragraph)]
        self.assertEqual(len(templates), 2)
        self.assertIn("--repo github.com/mryfmo/dotfiles", paragraph)
        sha = "a" * 40
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            stub, log = root / "gh", root / "argv.jsonl"
            stub.write_text(
                f"#!{sys.executable}\nimport json,sys\nfrom pathlib import Path\np=Path({str(log)!r})\nwith p.open('a') as f: f.write(json.dumps(sys.argv[1:])+'\\n')\nprint({sha!r} if sys.argv[-1]=='.object.sha' else 'nonsecret-ledger-fixture')\n"
            )
            stub.chmod(0o755)
            env = dict(os.environ, GH_HOST="example.invalid", PATH=str(root))

            def invoke(words, *, available=True):
                self.assertEqual(words[:4], ["gh", "api", "--hostname", "github.com"])
                self.assertEqual(words.count("--hostname"), 1)
                self.assertFalse(any(word.startswith("--hostname=") for word in words))
                self.assertTrue(words[4].startswith("repos/mryfmo/dotfiles/"))
                try:
                    return subprocess.run(
                        words,
                        env=env | {"PATH": str(root if available else root / "empty")},
                        text=True,
                        capture_output=True,
                        check=False,
                    )
                except FileNotFoundError:
                    return subprocess.CompletedProcess(words, 2, "", "cannot bind github.com: gh unavailable")

            reference = invoke(templates[0])
            self.assertEqual(reference.returncode, 0)
            actual = reference.stdout.strip()
            self.assertRegex(actual, r"\A[0-9a-f]{40}\Z")
            content = [word.replace("<sha40>", actual) for word in templates[1]]
            self.assertEqual(content[4], f"repos/mryfmo/dotfiles/contents/.orchestration/decisions.tsv?ref={actual}")
            ledger = invoke(content)
            self.assertEqual(ledger.returncode, 0)
            self.assertEqual(ledger.stdout.strip(), "nonsecret-ledger-fixture")
            calls = [json.loads(line) for line in log.read_text().splitlines()]
            self.assertEqual(calls, [templates[0][1:], content[1:]])
            print(json.dumps({"hostile_GH_HOST": "example.invalid", "recorded_argv": calls}))
            for words in (
                templates[0][:2] + templates[0][4:],
                templates[0] + ["--hostname", "github.com"],
                templates[0][:3] + ["example.invalid"] + templates[0][4:],
            ):
                with self.assertRaises(AssertionError):
                    invoke(words)
            stub.unlink()
            refused = invoke(templates[0], available=False)
            self.assertNotEqual(refused.returncode, 0)
            self.assertIn("cannot bind github.com", refused.stderr)
            self.assertEqual(refused.stdout, "")
            print(f"no-gh: exit={refused.returncode}; {refused.stderr}; no approval output")
            self.assertEqual(len(log.read_text().splitlines()), 2)
            print(
                "hostile GH_HOST: both fixed-host argv bound to one validated SHA; no-gh: named refusal, no approval or retry; contract only"
            )


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
        ("orchestrator-step-6", SKILL, ("## Orchestrator Playbook", "\n## "), ("\n6. ", "\n7. ")),
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
                expected = fixture.read_text()
                replacements = {OLD_ACCEPTANCE: ACCEPTANCE} if name == "invariants" else {}
                if name == "message-contract":
                    replacements = {anchor: addition + anchor for anchor, addition in CONTRACT_ADDITIONS.items()}
                for anchor, replacement in replacements.items():
                    self.assertEqual(expected.count(anchor), 1, f"fixture anchor drift: {name}: {anchor}")
                    expected = expected.replace(anchor, replacement, 1)
                self.assertEqual(
                    self.normalized(start + self.section(text, start, end)),
                    self.normalized(expected),
                    f"regime rule section {name} changed outside its declared fixture replacements",
                )

    def test_contract_names_context_decisions_result_file_and_precheck(self) -> None:
        contract = self.section(SKILL.read_text(), "## Message Contract v1")
        for anchor, addition in CONTRACT_ADDITIONS.items():
            with self.subTest(anchor=anchor):
                self.assertIn(addition.strip(), contract)

    def test_skill_names_no_unlanded_mechanism(self) -> None:
        pattern = (
            r"Until .schemas/task.json. lands|Once plan 007 T718 lands|"
            r"Once .dotfiles-T128-gate-evidence-a02. lands|until a checker lands|"
            r"On Linux, .gh. backed by the host keyring|AUDIT_DISPOSITIONS"
        )
        for path in (SKILL, ROOT / "AGENTS.md"):
            with self.subTest(path=path.name):
                self.assertEqual(re.findall(pattern, path.read_text()), [])

    def test_skill_sandbox_text_names_both_platforms(self) -> None:
        step = self.section(self.section(SKILL.read_text(), "## Worker Playbook"), "\n4. ", "\n5. ")
        for platform in ("Seatbelt", "bubblewrap"):
            with self.subTest(platform=platform):
                self.assertIn(platform, step)

    def test_step_10_states_the_advisory_p2_policy(self) -> None:
        skill = SKILL.read_text()
        step = self.section(self.section(skill, "## Orchestrator Playbook"), "\n10. ", "\n11. ")
        self.assertEqual(step.count("not-applicable:advisory P2 owned by"), 1)
        self.assertEqual(step.count("while INV-6's counts allow it"), 1)
        self.assertIn("bot_rounds=2", self.section(skill, "\n15. After the final push"))

    def test_advisory_rows_are_excluded_from_the_class_counts(self) -> None:
        self.assertEqual(self.invariants().count("non-advisory rows only"), 1)

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
            # Plan 006 B0: design v20 removed contract PRs, so the check names the implementing_tasks entry;
            # thread 4247933561: a task without an `invariants` key (a docs or review task) needs no entry;
            # thread 4257278283: matching ids is not enough, so each sentence is compared with the design's.
            "one invariant check (for a task that carries an `invariants` key: the task id maps to its "
            "`implementing_tasks` entry, the invariant ids match, and each invariant's sentence equals the design's "
            "byte-for-byte, the design read from main (INV-2), checked by hand in the review; "
            "a task without the key needs no entry)",
        ):
            with self.subTest(token=token):
                self.assertIn(token, text)
        self.assertNotIn("-contract-a01", text)

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
            "The task-file review checks the three shape rules by hand",
            "Substance is the reviewers'",
            "The table is the task's completion condition",
            "a missing row is added once, counted as an amendment",
        ):
            with self.subTest(token=token):
                self.assertIn(token, text)

    def test_threat_table_rule_carries_no_grammar(self) -> None:
        # The reset of PR 318: shape checks carry no grammar pattern in prose.
        text = self.invariants()
        self.assertNotIn("^(closed|residual|out-of-scope)", text)
        self.assertNotIn("`none`", text)

    # Thread 4240348412 is closed by a05's counters bullet: the script reads the whole history (scripts/regime-counters.sh:85), no by-hand read remains.
    def test_surviving_fix_round_threads_stop_for_the_operator(self) -> None:
        # Thread 4240348414: an open: item needs a path through steps 10.1 and 10.5.
        playbook = self.section(SKILL.read_text(), "## Orchestrator Playbook")
        for token in (
            "follows Worker Playbook step 15's operator-decision path",
            "the PR is not merged, never with the thread open",
        ):
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
            "at most one worker-side fix round before RESULT",
            "`AGMSG-RESULT … bot_rounds=2`",
            "in the background and the Bot wait below at the same time",
            "listed as `open:<thread id>`",
            "this stops the PR for the operator's decision",
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
            "The task-file review checks the three shape rules (the test selector, the sentence, the owning task id) by hand",
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

    def test_shape_is_checked_by_hand(self) -> None:
        # Shape checks stay in the review; no unlanded schema is promised.
        sentence = "The task-file review checks the three shape rules"
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
            "a `closed` selector names a test present in the PR tree at acceptance",
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

    def test_workers_open_the_pr_as_a_draft(self) -> None:
        # Thread 4240566266: step 15's `gh pr ready` starts the Bot timer only on a draft PR.
        step = self.section(SKILL.read_text(), "\n2. Switch to the `repo`", "\n3. ")
        self.assertIn("`gh pr create --draft --head <branch>`", step)

    def test_workers_commit_inside_the_sandbox(self) -> None:
        step = self.section(SKILL.read_text(), "\n2. Switch to the `repo`", "\n3. ")
        for token in (
            "Commit inside the sandbox, with `git -c commit.gpgsign=false` when the signing key is unreadable there",
            "All Git operations remain inside the sandbox (step 4)",
        ):
            with self.subTest(token=token):
                self.assertIn(token, step)

    def test_dispatches_are_recorded_from_the_bus(self) -> None:
        # Plan 007 T703 item 1 (C-12): a seat's status comes from a bus line, never from memory; plan 010 option D:
        # the obligation stays here, and the commands move to plan 007 T718's scripts.
        step = self.section(self.section(SKILL.read_text(), "## Orchestrator Playbook"), "\n6. ", "\n7. ")
        for token in (
            "Every dispatch (TASK, ACCEPTANCE, PING) is recorded in the current acceptance record under a "
            "`dispatch:` key as the bus line with its read marker, "
            # Row local:65a3d71:1 (the a04 record's owned section): dispatch.sh refuses a missing record, so the rule
            # says who creates it and when.
            "so the orchestrator creates that record, `.orchestration/acceptance/<task>.md`, before the task's first "
            "dispatch (`scripts/orchestrator/dispatch.sh` refuses a record that does not exist or that names another "
            "task); a seat is reported as working only from such a "
            # The local review of 7771082f: the merged bus-read.sh refuses a read at its limit; nothing reads all.
            "line, and after a context compaction the open TASK list is re-derived from a bus read that is refused "
            "when it reaches its limit (`bus-read.sh` exits when the history reaches `BUS_READ_LIMIT`; the "
            "orchestrator raises the limit and reads again), never from a default-limited one and never from a read "
            "whose truncation went unnoticed.",
            # Threads 4248319936 and 4249303426: the clock runs from the seat's latest event for the task;
            # thread 4257278271: INV-10's idle figure is 20 minutes, its 30 minutes the first-push deadline.
            "A seated worker idle for 20 minutes since its latest bus event for the task while a dispatchable task "
            "exists (INV-10's idle figure; its 30 minutes is the first-push deadline) gets a bus read, then a PING; "
            "a longer silent wait is never the answer.",
            # Thread 4249303413: history.sh shows the latest 20 rows unless given a limit.
            "`scripts/orchestrator/dispatch.sh` writes the line and `scripts/orchestrator/bus-read.sh` performs the "
            "read and prints the minutes since each open task's latest event (both on main since a03c1daa, plan 007 "
            "T718); the orchestrator applies the 20-minute figure to the minutes the script prints (the script's own "
            "silence flag still uses 30 minutes, a recorded residual of the tools lineage).",
        ):
            with self.subTest(token=token[:40]):
                self.assertIn(token, step)
        for stale in (
            "expected duration",
            "the bus line `history.sh <team>` prints",
            "no bus event from its seat since",
            "complete bus read",
            "silent for thirty minutes",
        ):
            with self.subTest(stale=stale):
                self.assertNotIn(stale, step)

    def test_rule_changes_travel_as_task_amendments(self) -> None:
        # Plan 007 Phase 0: a rule sentence changed through a PONG answer bypasses the hash and C1 to C6;
        # plan 007 T704: the checker has landed, so the sentence names it instead of its landing condition.
        self.assertIn(
            "A change to a rule sentence requested of a worker travels as a task amendment (hashed, checked by "
            "`scripts/orchestrator/task-consistency-check.py` (C1 to C10 and C7b) before dispatch and at acceptance, "
            "confirmed by the review seat), never as a PONG answer.",
            self.invariants(),
        )
        self.assertNotIn("C1 to C6 once plan 007 T704 lands it and by hand until then", self.invariants())

    def test_three_repeats_start_with_a_pasted_correction_search(self) -> None:
        # Plan 007 S6: the third repeat of a class is answered by a recorded correction, never by another fix round;
        # plan 010 option D: the obligation stays here, and the commands move to plan 007 T718's three-repeat.sh.
        bullet = self.section(self.invariants(), "\n- When a finding class reaches three on one artifact", "\n- ")
        for token in (
            # Threads 4247933574 and 4249303398: the records search, and a correction applied mechanism by mechanism.
            " (the record's ledger) or `scripts/regime-counters.sh` prints an S1 candidate, the next acceptance "
            "action is the records search for that class, pasted into the record as the line "
            "`search: <class> -> <the matching mistake records or none>`, and the matching correction is applied "
            "when its mechanism is landed, or landed first when it is pending, mechanism by mechanism, before any "
            "dispatch; a class is a slug of `[a-z0-9-]` assigned at disposition time, never text taken from a review "
            "title.",
            # Thread 4249303433: review-derived text never reaches a shell.
            "`scripts/orchestrator/three-repeat.sh <class>` validates the slug, runs the records search and the "
            "CompactionDB search without a shell and prints the line.",
            "The gate (`scripts/require-crit-review.py`, S6) refuses the merge for a ledger class at three or more "
            "rows whose `searches` entry does not equal the mistake records naming the class; "
            "`acceptance-front-matter.py` writes the entry from the same lookup.",
            "Pasting the `search:` line and applying the correction before any dispatch remain the orchestrator's rule.",
            "Every `not-applicable` disposition carries `; evidence=<command>` with the output pasted in the record.",
        ):
            with self.subTest(token=token[:40]):
                self.assertIn(token, bullet)
        for stale in (
            "`grep -rl <class slug> .orchestration/learning/corrections/`",
            "`grep -l 'classes:",
            "gate-evidence-a01",
            "memory search <class slug>",
        ):
            with self.subTest(stale=stale):
                self.assertNotIn(stale, bullet)

    def test_threat_table_rows_have_a_fixed_unit(self) -> None:
        # Plan 007 T703 item 4: without a unit, a missing row is a judgment call for each reviewer.
        bullet = self.section(self.invariants(), "\n- A task that touches a trust boundary", "\n- ")
        self.assertIn(
            "metadata separators). The row unit is one row per `allowed_files` entry, one row per listed control "
            "that is not a path (task metadata, workflow and interpreter or environment inputs, in-process effects, "
            "new or renamed scripts, metadata separators), carried by the declared test module's row where that is "
            "where the control acts, and one row per orchestrator effect from the fixed list (forced removal, merge, "
            # Thread 4257278276: an executed wildcard entry gets a row per changed file; a data wildcard keeps one.
            # Plan 007 T704: C4 and C7b have landed, so the clause names the script instead of its landing condition.
            "update-branch); under a wildcard `allowed_files` entry whose files are executed or applied (scripts, "
            "workflows, hooks, settings, the rules seats follow), one row per concrete file the PR changes; a "
            "wildcard over test fixtures or other data files keeps one row; C4 and C7b of "
            "`scripts/orchestrator/task-consistency-check.py` verify the path half before dispatch, and the task-file "
            "review checks the rest.",
            bullet,
        )
        for stale in (
            "C4 verifies the path half before dispatch",
            "C4 of the task-consistency check (plan 007 T704) verifies the path half once it lands",
        ):
            with self.subTest(stale=stale):
                self.assertNotIn(stale, bullet)
        rules = self.section((ROOT / "AGENTS.md").read_text(), "## Code Review Rules")
        subsection = self.section(rules, "### Orchestration records and trust-boundary code", "\n### ")
        self.assertIn(
            "report a missing table or a missing row; a row's unit is the SKILL threat-table bullet's (one per "
            "`allowed_files` entry, one per non-path control, one per orchestrator effect), so review a missing "
            "row at that unit; report a `closed` row",
            subsection,
        )

    def test_the_gate_reads_the_acceptance_record(self) -> None:
        # Plan 007 T703 item 6: the gate reads the acceptance record's ledger and searches.
        step = self.section(self.section(SKILL.read_text(), "## Orchestrator Playbook"), "\n10. ", "\n11. ")
        # Row audit:71eb920:1 (the a04 record's owned section): the gate retired AUDIT_DISPOSITIONS and reads an
        # incorrect audit's dispositions from the record's audit_findings, so step 10 no longer names the variable.
        for token in (
            "`AUDIT_EVIDENCE=<audit> AGENT_REVIEWED=1 REVIEW_EVIDENCE=<receipt> ACCEPTANCE_EVIDENCE=<acceptance record> "
            "BASE=origin/main PR_FEEDBACK_EVIDENCE=<json> make require-crit-review`",
            "with every audit finding dispositioned as the task-level audit bullet says: for an `incorrect` verdict "
            "the record's JSON `audit_findings`, which the gate reads through `ACCEPTANCE_EVIDENCE`.",
            "must be `correct`, or `incorrect` with an `audit_findings` entry in the acceptance record for each of its "
            "findings.",
        ):
            with self.subTest(token=token[:40]):
                self.assertIn(token, step)
        for stale in ("[AUDIT_DISPOSITIONS=", "through `AUDIT_DISPOSITIONS`", "`incorrect` with `AUDIT_DISPOSITIONS`"):
            with self.subTest(stale=stale):
                self.assertNotIn(stale, step)

    def test_an_incorrect_audit_is_dispositioned_in_audit_findings(self) -> None:
        # Row audit:71eb920:1, amendment 1: the task-level audit bullet and AGENTS.md's gate sentence named the retired
        # gate input (the audit-finding: prose the gate read through AUDIT_DISPOSITIONS); the gate reads audit_findings.
        bullet = self.section(
            self.invariants(), "\n  - The orchestrator dispositions every `[P0-P3]` finding", "\n  - "
        )
        for token in (
            "For an `incorrect` verdict the dispositions are the record's JSON `audit_findings`, the only form the gate "
            "reads: one `{n, reason, evidence}` entry per finding, `n` the number as a string and `reason` at least 20 "
            "characters, written with `scripts/orchestrator/acceptance-front-matter.py --audit-dispositions <tsv>`; an "
            "entry never cites a fix, since a fix moves the head and needs its own audit.",
            "A finding under `Verdict: correct` is dispositioned all the same, as an `audit-finding: <n> …` line in the "
            "record's prose: `fixed:<sha>` with a fresh audit of that sha, otherwise `not-applicable:<reason of at "
            "least 20 characters>`.",
        ):
            with self.subTest(token=token[:40]):
                self.assertIn(token, bullet)
        for stale in ("The gate enforces these lines only for an `incorrect` verdict", "or the gate skips it"):
            with self.subTest(stale=stale):
                self.assertNotIn(stale, bullet)
        agents = (ROOT / "AGENTS.md").read_text()
        self.assertIn(
            "then the gate with `PR_FEEDBACK_EVIDENCE`, `AUDIT_EVIDENCE` and `ACCEPTANCE_EVIDENCE` (the record's "
            "`audit_findings` disposition an `incorrect` verdict).",
            agents,
        )
        self.assertNotIn("`AUDIT_DISPOSITIONS` for an `incorrect` verdict", agents)


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
