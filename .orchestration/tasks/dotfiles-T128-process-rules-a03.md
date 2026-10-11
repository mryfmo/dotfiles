---
format: 2
task_id: dotfiles-T128-process-rules-a03
kind: docs
security: false
reset_of: [dotfiles-T128-process-rules-a01, dotfiles-T128-process-rules-a02]
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
  - control: the task-file copies on the branch (.orchestration/dotfiles-T128-process-rules-a01/task.md, -a02/task.md and -a03/task.md)
    disposition: "residual: each copy is byte-identical to the dispatched task file (sha256 in the worker's validation file, compared by the orchestrator at acceptance); the reset record names the a03 file's hash and the review seat's verdict=accept on it"
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

# AGMSG-TASK dotfiles-T128-process-rules-a03 — the second reset continuation of PR #318 (A1, A2, A4)

Written 2026-10-11 by the orchestrator seat from the review seat's redesign (source task `dotfiles-T128-process-rules-redesign-a02`), under the reset records `.orchestration/acceptance/dotfiles-T128-process-rules-a01-design-reset.md` and `.orchestration/acceptance/dotfiles-T128-process-rules-a02-design-reset.md`. a03 continues a02 on the same branch and PR (`docs/regime-pattern`, #318) from the worker's current head, same worker (`claude-standard-dot-a003`), same worktree (`.claude/worktrees/worker-f`); items 1 to 5 below, the revise round's five checks and the three Bot P2 fixes of `21c160c8` are carried over unchanged. Review tier by INV-1; `kind: docs`. Everything `dotfiles-T128-process-rules-a01` asked for stays as it is on the branch except the threat-table rule, which this task replaces as written below; no further fix of that rule's payload grammar is in scope, whatever a review says.

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

## History

a01 was reset under INV-6 and plan 006 S1 when the Codex Bot found the same finding class three times on one artifact, a disposition grammar stated in prose that admitted a vacuous payload, and the review seat's redesign (`dotfiles-T128-process-rules-redesign-a01`, RESULT 431) became a02. a02 was reset under INV-6's amendment threshold when its relay carried no `threat_table` (Bot P1 4240566259; amendment 1 added three rows) and that table missed the PR's control of its own oracle, and the review seat's redesign (`dotfiles-T128-process-rules-redesign-a02`) is this file, with the fourth row and the corrected citation of row 1.

## Validation

`prettier --check` on the two prose files; `uv run python -m unittest tests.unit.test_agmsg_orchestration_docs -v`; removal proofs: each new token (items 1 to 5) removed in a scratch copy fails its test, and the old pattern pasted back into the bullet fails `test_threat_table_rule_carries_no_grammar`; the premises re-run and pasted (the gh one from outside the sandbox).

## First commit

Copy this task file byte-identical to `.orchestration/dotfiles-T128-process-rules-a03/task.md` (the `…-a01/` and `…-a02/` directories stay as history); evidence for this task beside it.

## Completion

One content commit after the task copy; CI; the PR is already ready, so the Bot wait starts at the push (`@codex review` if nothing in 10 minutes); at most two P0/P1 fix rounds, none of them touching the threat-table rule's payload wording (a Bot finding there is reported, not fixed: it is the class the reset closed, and the orchestrator dispositions it); then `AGMSG-RESULT v1 task_id=dotfiles-T128-process-rules-a03 … reset_of=dotfiles-T128-process-rules-a01,dotfiles-T128-process-rules-a02 bot_rounds=<n>` with every open thread id, via `agmsg-dispatch dotfiles-conformance claude-standard-dot-a003 claude-deep-dot w5:p1`. Artifacts at the `expected_*` paths of the TASK message. max_turns=6. Forbidden: anything outside `allowed_files`; `make update`; thread resolution.
