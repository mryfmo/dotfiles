---
format: 2
task_id: dotfiles-T128-process-rules-a05
kind: docs
security: false
reset_of: [dotfiles-T128-process-rules-a01, dotfiles-T128-process-rules-a02, dotfiles-T128-process-rules-a03, dotfiles-T128-process-rules-a04]
design_review:
  receipt: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round16.md
  design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md
allowed_files:
  - home/dot_agents/skills/agmsg-orchestration/SKILL.md
  - AGENTS.md
  - tests/unit/test_agmsg_orchestration_docs.py
after: []
threat_table:
  - control: the PR edits AGENTS.md "Code Review Rules", which the Codex Bot reads from the PR tree, so a PR can rewrite the Bot's rules for its own review
    disposition: "residual: the Bot's review of a PR that edits its own rules is swept feedback with no gate authority (INV-7: the Bot's review of a PR is swept feedback, never a design receipt; design R8); the task-level audit runs with main's AGENTS.md as its instruction root (INV-5) and the orchestrator's review reads the diff; a change to Code Review Rules is review tier with one schema audit (INV-1)"
  - control: the PR edits the SKILL that Claude seats follow once it is applied
    disposition: "residual: the applied copy changes only after the merge and the operator's make update; before the merge the orchestrator's diff review and the audit from main judge every sentence, and tests/unit/test_agmsg_orchestration_docs.py pins each rule sentence with a token that fails when the sentence is removed"
  - control: the task-file copies on the branch (.orchestration/dotfiles-T128-process-rules-a01/task.md, -a02/task.md, -a03/task.md, -a04/task.md and -a05/task.md)
    disposition: "residual: each copy is byte-identical to the dispatched task file (sha256 in the worker's validation file, compared by the orchestrator at acceptance); the reset record names the a05 file's hash and the review seat's verdict=accept on it"
  - control: the PR edits tests/unit/test_agmsg_orchestration_docs.py, the module that pins its own rule sentences, so it controls the oracle as well as the text
    disposition: "residual: the orchestrator's diff review and the task-level audit from main read the test diff beside the prose diff; main-tests is no control here, because the module is declared in allowed_files and would run only in dormant-contract mode"
premises:
  - claim: "on PR 318 the Codex Bot raised the same finding class on three heads (4240290387 on 9a46c3c4: the disposition regex accepts an empty payload; 4240321113 on ac3794f9: residual none; 4240334094 on 6635030f: out-of-scope none or a wrong owner), which is plan 006 S1, and P1 on two heads after the first RESULT 9a46c3c4, which is INV-6; the other three ids in the output are the first revise round's P2s (fixed) and the stop-criteria P2"
    command: "gh api --paginate repos/mryfmo/dotfiles/pulls/318/comments --jq '.[]|select(.in_reply_to_id==null and (.original_commit_id[0:8]|IN(\"9a46c3c4\",\"ac3794f9\",\"6635030f\")) and (.body|test(\"P0 Badge|P1 Badge|P2 Badge\")))|[.id,.original_commit_id[0:8]]|@tsv'"
    output: |-
      4240290382	9a46c3c4
      4240290387	9a46c3c4
      4240290391	9a46c3c4
      4240321113	ac3794f9
      4240334094	6635030f
      4240334098	6635030f
  - claim: "the redesign RESULT INV-6 names comes from an identity other than the abandoned task's author (the orchestrator claude-deep-dot wrote dotfiles-T128-process-rules-a01)"
    command: "~/.agents/skills/agmsg/scripts/history.sh dotfiles-conformance --limit 1000 | grep 'AGMSG-RESULT v1 task_id=dotfiles-T128-process-rules-redesign-a01' | cut -c1-140"
    output: "  ○ [2026-10-11T05:10:11Z] claude-review-dot-a001 → claude-deep-dot: AGMSG-RESULT v1 task_id=dotfiles-T128-process-rules-redesign-a01 status"
  - claim: "the redesign receipt is the file whose hash the RESULT names"
    command: "sha256sum .orchestration/validation/dotfiles-T128-process-rules-redesign-a01.md"
    output: "b95b4eacb3b7ef3f8cc8f0da438062e4a794a1e96139268b9cecc6b4df0b40e4  .orchestration/validation/dotfiles-T128-process-rules-redesign-a01.md"
---

# AGMSG-TASK dotfiles-T128-process-rules-a05 — the fourth continuation of PR #318 (A1, A2, A4), after plan 006 S1 on the counters bullet

Written 2026-10-11 by the orchestrator seat from the review seat's redesign (source task `dotfiles-T128-process-rules-redesign-a04`), under the reset records `.orchestration/acceptance/dotfiles-T128-process-rules-a01-design-reset.md`, `…-a02-design-reset.md`, `…-a03-design-reset.md` and `…-a04-design-reset.md`, and the S1 cause record `.orchestration/learning/plan-006-s1-process-rules-counters-bullet-2026-10-11.md`. a05 continues a04 on the same branch and PR (`docs/regime-pattern`, #318) from the worker's current head `7800ef92`, same worker (`claude-standard-dot-a003`), same worktree (`.claude/worktrees/worker-f`); items 1 to 8 below (items 6 to 8 already on the branch), the a02 revise round's five checks, the three Bot P2 fixes of `21c160c8` and the a03 revise round's three fixes are carried over unchanged; item 9 is this stop's one change, the counters bullet restated by reference, and it supersedes the sentences of items 4 and 8 that live inside that bullet. Review tier by INV-1; `kind: docs`. Everything `dotfiles-T128-process-rules-a01` asked for stays as it is on the branch except the threat-table rule, which this task replaces as written below; no further fix of that rule's payload grammar is in scope, whatever a review says.

## What to do (verbatim from the redesign receipt)

1. In `home/dot_agents/skills/agmsg-orchestration/SKILL.md`, "Review and integration invariants", replace the whole `threat_table` bullet (the one that now carries a pattern and "`none`") with:

```markdown
- A task that touches a trust boundary (anything the design tier lists, CI that decides a required check, code that executes PR-controlled input) carries a `threat_table` in its front matter: one `{control, disposition}` row per thing the PR or the orchestrator controls (the tree and its tests, task.md, workflow files, interpreter and environment files, in-process effects, new or renamed scripts, metadata separators). A disposition takes one of three forms: `closed: tests/<file>::<name>`, the test that closes the row; `residual: <sentence>`, the compensating control; `out-of-scope: <task id>`, the task that owns the row. Shape is `schemas/task.json`'s (wave V1): a `closed` selector names a test present in the PR tree, an `out-of-scope` owner is a task id in the design's `implementing_tasks`, a `residual` payload is a sentence of at least 20 characters (the gate's minimum for a reason). Substance is the reviewers': the task-file review, the Bot and the auditor judge each row against the diff. The table is the task's completion condition: a missing row is added once, counted as an amendment, never fixed finding by finding.
```

2. In `AGENTS.md`, "### Orchestration records and trust-boundary code", replace the second bullet with:

```markdown
- Judge from the diff, whatever the task's metadata says, whether a change touches a trust boundary (anything the design tier lists, CI that decides a required check, code that executes PR-controlled input). Review such code against the task's `threat_table`: report a missing table or a missing row; report a `closed` row whose test does not close it, a `residual` row whose control does not mitigate the risk, and an `out-of-scope` row whose owner does not own it. Do not re-raise a `residual` row whose control mitigates the risk. Shape (the test selector, the sentence, the owning task id) is the schema's to check, not the review's.
```

   The first and third bullets stay. The bullet is replaced as it stands on head `aeb6c5ad` (fix-round-2 commit `77953979` added a placeholder clause to it; the replacement supersedes that clause too).

3. In `tests/unit/test_agmsg_orchestration_docs.py`, replace `test_a_trust_boundary_task_carries_a_threat_table` and remove `test_threat_table_dispositions_carry_a_payload`; add the negative test:

```python
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
```

## Also: the two P1 threads of the third Bot round on `aeb6c5ad` (orchestrator contract decisions, fixed here, not a fourth fix round of the old class)

4. Thread 4240348412 (`history.sh` prints 20 rows by default, so the by-hand counts can undercount): in the SKILL counters bullet ("Review and integration invariants"), replace "the orchestrator counts the same things by hand from `history.sh`" with "the orchestrator counts the same things by hand from `history.sh` with an explicit `--limit 1000` (its default prints 20 rows; the storage facade `agent-stop-gate.sh --read-history <team>` is the other complete read)". Test: `test_manual_counts_read_the_whole_history` asserts the token "with an explicit `--limit 1000`" in the invariants section.
5. Thread 4240348414 (an `open:<id>` third-round P0/P1 has no path through Orchestrator Playbook step 10.1 and 10.5): append to step 10.1 the sentence "An `open:<thread id>` item from a worker's third Bot round is a sweep item like any other: it becomes `fixed:<sha>` through a revise round that carries its `check=` (a round that counts toward INV-6 like any other), or `not-applicable:<reason>` with a pasted refutation; until one of those exists the PR is not merged, never with the thread open." Test: `test_open_third_round_threads_have_an_integration_outcome` asserts the tokens "is a sweep item like any other" and "the PR is not merged, never with the thread open" in the Orchestrator Playbook section.

The RESULT lists `4240348412-fixed:<sha>` and `4240348414-fixed:<sha>`.

## Also: the two P1 threads of the a03 revise's Bot round on `781e6ef8` (this reset's cause: two A1 sentences against the hashed design)

6. Thread 4243537279 (the freeze rule froze an unreviewed hash, against INV-7, whose receipts both name the hash that is frozen): in the SKILL design-review bullet ("Review and integration invariants"), replace "After at most three revision rounds the design is frozen, and whatever is still open becomes a residual list that is worker input." with "The third revision round is the last: the design is frozen at the hash the pair last accepted, a revision after the third pair is not made, and any later change to a hashed key is a new pair (INV-7); whatever is still open at that hash becomes a residual list that is worker input." Test: in `test_design_review_runs_in_paired_rounds_with_a_cap`, replace the token "After at most three revision rounds the design is frozen" with "frozen at the hash the pair last accepted" and add the token "any later change to a hashed key is a new pair (INV-7)"; the old sentence pasted back fails the test.
7. Thread 4243537281 (a boundary PR "is never a prerequisite of a dispatch", against INV-2's design-on-main precondition; plan 006 corrected the rule at 07:25Z, the SKILL sentence did not): in the SKILL boundary bullet, replace "It carries no task draft under review and is never a prerequisite of a dispatch: any merged boundary that carries the design meets the design-on-main precondition." with "It carries no task draft under review. A design not yet on `main` lands through a merged boundary PR before its implementing TASK is dispatched (INV-2), and any merged boundary that carries the design meets that precondition." Test: rename `test_a_boundary_pr_never_gates_a_dispatch` to `test_a_design_lands_on_main_before_its_task`, asserting the tokens "carries no task draft under review" and "before its implementing TASK is dispatched (INV-2)" in the invariants section and `assertNotIn("is never a prerequisite of a dispatch", ...)`; the old token goes from the test and from the prose.

The RESULT lists `4243537279-fixed:<sha>` and `4243537281-fixed:<sha>` beside `4243516879-fixed:114d5b91`.

## Also: the third P1 thread of the same Bot round on `781e6ef8` (amendment 1, 22:50Z: the orchestrator's omission; PONG 567 and the redesign task named two of the three P1s of review 5485324335)

8. Thread 4243537278 (SKILL.md:72 counts P0/P1 Bot review bodies toward INV-6, but the hashed INV-6 counts Bot heads from `original_commit_id` on `review_comment` items only; review bodies belong to S1's finding classes and the worker's fix-round cap, as plan 006 A7's task states): in the SKILL counters bullet ("Review and integration invariants"), replace "The script reads inline review comments only, so the orchestrator also counts the P0/P1-badged Bot review bodies of `…/pulls/<n>/reviews`, grouped by `commit_id`, by hand and pastes that command and its output beside the script's, until the script reads review bodies too." with "The script reads inline review comments only, and that is INV-6's whole head count (`original_commit_id` on `review_comment` items); the orchestrator also lists the P0/P1-badged Bot review bodies of `…/pulls/<n>/reviews`, grouped by `commit_id`, by hand and pastes that command and its output beside the script's, for S1's finding classes and the worker's fix-round cap only, never as INV-6 heads." and, in the same bullet, replace "which INV-6 and S1 count and history does not hold" with "which S1 and the fix-round cap count, INV-6 does not, and history does not hold". Test: in `test_counters_add_review_body_findings`, replace the asserted sentence with the new first sentence and add `self.assertNotIn("until the script reads review bodies too", self.invariants())` and `self.assertNotIn("which INV-6 and S1 count", self.invariants())`; the existing token "P0/P1-badged Bot review bodies grouped by `commit_id`" is kept, so its test stays satisfied. The worker's own step 15 sentence (review-body findings are "fixed or dispositioned the same way") is the fix-round cap and stays.

The RESULT also lists `4243537278-fixed:<sha>` (if the worker's Bot fix round 1 on `cc9fc785` already fixed it, that commit's sha).

## Also: the S1 stop on the counters bullet (plan 006 S1, 23:13Z: six Codex Bot P1 findings of one class on SKILL.md line 72)

9. Threads 4240250137, 4240348412, 4240382519, 4243516879, 4243537278 and 4243631335 (one class: the acceptance-decision bullet misstates the sources the S1/S2 counts read; cause record `.orchestration/learning/plan-006-s1-process-rules-counters-bullet-2026-10-11.md`: the bullet enumerated sources that three owners define, INV-6 at design line 55, the A3 script's own output and plan 006 S1, and every fix re-enumerated): in the SKILL "Review and integration invariants", replace the whole counters bullet (the one that begins "Before every acceptance action (revise, accept, merge) the orchestrator runs `scripts/regime-counters.sh <task id>`", as it stands on `7800ef92`) with exactly:

```markdown
- Before every acceptance action (revise, accept, merge) the orchestrator runs `scripts/regime-counters.sh <task id>` and pastes its output into the acceptance record. S2 is decided from INV-6's counts: each component the script prints is read from its output, and for each component it prints as `unknown` the record pastes the command and output that read the source INV-6 names for that component, or, while that source has no entry for the task, says so and pastes the reading of the interim record the orchestrator used in its place. S1 (plan 006: the same finding class three times on one artifact, from any reviewer) is decided from the record's finding-class table, which gives a class to every finding the PR-feedback sweep lists, whatever its disposition, and to every task-level audit finding; three rows of one class stop the artifact.
```

   The bullet states the three obligations by reference and names no source: no GitHub endpoint, badge, grouping, "by hand" count or pre-A3 fallback (A3 is on `main`, `52575497`). A finding of the form "the bullet omits source X" cannot apply to it; a finding against INV-6's or the sweep's coverage goes to those owners. Item 4's `--limit 1000` sentence and item 8's review-body sentences were inside the replaced bullet and go with it; their threads are fixed by this item's commit. Tests, in `tests/unit/test_agmsg_orchestration_docs.py`:
   - `test_counters_run_before_every_acceptance_action` keeps its two tokens ("Before every acceptance action (revise, accept, merge) the orchestrator runs `scripts/regime-counters.sh <task id>`" and "and pastes its output into the acceptance record") and loses the three others with their comments ("until it is on `main`, the orchestrator counts the same things by hand", "the PR's GitHub review comments and review bodies", "P0/P1-badged Bot review bodies grouped by `commit_id`").
   - `test_manual_counts_read_the_whole_history` is removed; in its place one comment line: `# Thread 4240348412 is closed by a05's counters bullet: the script reads the whole history (scripts/regime-counters.sh:85), no by-hand read remains.`
   - `test_shape_rules_and_the_decision_sentence_are_pinned` (tests line 428 at `7800ef92`) pins the old decision sentence "S1 (the same finding class three times) and S2 (the INV-6 counts) are decided from that output.", which is inside the replaced bullet: replace that token with "S2 is decided from INV-6's counts" (the new decision-sentence pin; the test's shape-rule tokens stay). Every other old-bullet literal in the module is in the three tests above.
   - `test_counters_add_review_body_findings` becomes `test_counters_bullet_names_owners_not_sources`: it slices the bullet, `bullet = self.section(self.invariants(), "\n- Before every acceptance action", "\n- ")`, asserts in it the `unknown` sentence token "for each component it prints as `unknown` the record pastes the command and output that read the source INV-6 names for that component" and the class-table token "gives a class to every finding the PR-feedback sweep lists, whatever its disposition, and to every task-level audit finding", and asserts `assertNotIn` for "review bodies", "by hand", "gh api --paginate" and "until it is on `main`" in that bullet (the bullet, not the whole section: the threat-table bullet of the same section says "by hand" for the pre-V1 shape check, legitimately). The old `assertNotIn` lines go with the old test.
   Removal proofs: each of the two new tokens removed in a scratch copy fails the new test; any one of the four forbidden phrases pasted into the bullet fails it; the old bullet pasted back fails it on all four.

## History

a01 was reset under INV-6 and plan 006 S1 when the Codex Bot found the same finding class three times on one artifact, a disposition grammar stated in prose that admitted a vacuous payload, and the review seat's redesign (`dotfiles-T128-process-rules-redesign-a01`, RESULT 431) became a02. a02 was reset under INV-6's amendment threshold when its relay carried no `threat_table` (Bot P1 4240566259; amendment 1 added three rows) and that table missed the PR's control of its own oracle, and the review seat's redesign (`dotfiles-T128-process-rules-redesign-a02`) became a03, with the fourth row and the corrected citation of row 1. a03 was reset under INV-6's Bot threshold during its revise round 1 (P1 on two heads after its RESULT `b9a9da7d`: 4243516879 on `386f97ff`, fixed in `114d5b91`; 4243537279 and 4243537281 on `781e6ef8`), the latter two being A1 sentences the orchestrator wrote against INV-7 and INV-2; the review seat's redesign (`dotfiles-T128-process-rules-redesign-a03`) became a04, a03 plus items 6 to 8. a04 stopped under plan 006 S1, not INV-6, when the Codex Bot's sixth P1 of one class landed on the counters bullet (4243631335 on `7800ef92`, after 4240250137, 4240348412, 4240382519, 4243516879 and 4243537278): the bullet enumerated sources owned by INV-6, the A3 script and plan 006 S1, and every fix re-enumerated (`.orchestration/learning/plan-006-s1-process-rules-counters-bullet-2026-10-11.md`); the review seat's redesign (`dotfiles-T128-process-rules-redesign-a04`) is this file, a04 plus item 9, which removes the enumeration.

## Validation

`prettier --check` on the two prose files; `uv run python -m unittest tests.unit.test_agmsg_orchestration_docs -v`; removal proofs: each new token (items 1 to 9) removed in a scratch copy fails its test, the old pattern pasted back into the bullet fails `test_threat_table_rule_carries_no_grammar`, and the old boundary token pasted back fails `test_a_design_lands_on_main_before_its_task`; the premises re-run and pasted (the gh one from outside the sandbox).

## First commit

Copy this task file byte-identical to `.orchestration/dotfiles-T128-process-rules-a05/task.md` (the `…-a01/` to `…-a04/` directories stay as history); evidence for this task beside it.

## Completion

From `7800ef92`, after the task copy, one content commit for item 9 and its tests (items 6 to 8 are on the branch: `28d728c5`, `2a3f52e9`); CI; the PR is already ready, so the Bot wait starts at the push (`@codex review` if nothing in 10 minutes); at most two P0/P1 fix rounds, none of them touching the threat-table rule's payload wording or the counters bullet (a Bot finding there is reported with its class, not fixed: those are the classes the resets and the S1 stop closed, and the orchestrator dispositions it); then `AGMSG-RESULT v1 task_id=dotfiles-T128-process-rules-a05 … reset_of=dotfiles-T128-process-rules-a01,dotfiles-T128-process-rules-a02,dotfiles-T128-process-rules-a03,dotfiles-T128-process-rules-a04 bot_rounds=<n>` with every open thread id and the six bullet threads as `fixed:<item 9's sha>`, via `agmsg-dispatch dotfiles-conformance claude-standard-dot-a003 claude-deep-dot w5:p1`. Artifacts at the `expected_*` paths of the TASK message. max_turns=6. Forbidden: anything outside `allowed_files`; `make update`; thread resolution.
