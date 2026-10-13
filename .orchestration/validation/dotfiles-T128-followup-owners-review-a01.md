---
reviewed_at: 2026-10-13T14:02Z
reviewer: claude-review-dot-a001 (review seat; the Codex half runs the same check in parallel)
profile: review
session: 2089b04f
task: dotfiles-T128-followup-owners-review-a01
round: 2
task_file: .orchestration/tasks/dotfiles-T128-followup-owners-review-a01.md@4cfc7129cda376edaa1c682cdefdc155dfe64d83ce3409fe0bac7eccd140d67d
tools_task: .orchestration/tasks/dotfiles-T128-orchestrator-tools-followup-a01.md@ae208befe121d754018f311d42c0be996942264e5348b34440dd9c88c522d910 (untracked; lineage a02 on origin/main @a4c929b1)
gate_task: .orchestration/tasks/dotfiles-T128-gate-evidence-followup-a01.md@51c983df7768d8f3641ebe156d99cc96efa0f1295e673864b08e02114953ec2c (untracked; lineage a04 on origin/main @be659392)
rules_task: .orchestration/tasks/dotfiles-T128-playbook-rules-followup-a01.md@e22e0cc45de6fe70ac9be9b3e7b710055b7cd8b8c50767d7a832a9335f392c51 (on main as 72c74cea; the diff is item 1's two sentences)
previous_round: seat round 1 confirm on tools b1ec1421 / gate a2d301c8 with one P2 and two P3 (receipt 2c830f6e); Codex round 1 two P1 (missing section), Codex round 2 confirm on 44f746ce / 4f68d63c / cb1d918a; this round's hashes carry the seat's three findings as well (Round 2 addendum 13:47Z)
design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md on origin/main a1d33849 (disk byte-equal; implementing_tasks still lists gate-evidence-a01 to -a04 only)
consistency_check: all three files C1 to C10 and C7b OK (checker sha256 fdab23e0, copies named by task_id)
premises: all six replay as pasted (five `git cat-file -e origin/main:` → present; the playbook's `grep -c` → 1)
---

# Task-file review: the three owner tasks of plan 020 step 1 (round 2)

## Round 1 findings, re-checked on the new hashes

1. Seat P2 (gate task without an `implementing_tasks` entry): closed by a stated dispatch condition at `…gate-evidence-followup-a01.md:66`: the task is dispatchable only after plan 020 step 8's design amendment adds its id to the INV-6 entry, and stays a file on main until then. That satisfies INV-2 at dispatch time (the design on main before the implementing TASK); the entry rides the step-8 amendment rather than boundary (12), which is the orchestrator's choice and consistent. INV-6 remains byte-equal to design line 60.
2. Seat P3 (disposition prefix): closed; item 1 of all three files quotes the gate's full form `not-applicable:advisory P2 owned by <id>; evidence=git show origin/main:<task file> | grep -n 'item 1'` (lines 94, 70, 61).
3. Seat P3 (rows describing the lineage PR): closed for every path row; tools 15 rows and gate 5 rows now read "the PR edits <path> only within the owned rows (item 1)" with the owned-rows residual (the fixtures row: "edits or adds files under"). The non-path rows (task metadata, separators, in-process effects, workflow and interpreter inputs, new or renamed scripts, the three orchestrator effects, the gate's ACCEPTANCE_EVIDENCE and AUDIT_EVIDENCE rows) are byte-identical to the lineage's and in the same order (PyYAML comparison).
4. Codex P1 (missing section): closed in all three; item 1 reads "a missing or empty section at dispatch makes this task a no-op … the section is created at the lineage's acceptance, so it does not exist before that"; no `## Owned by` heading exists in any record yet, as expected.

## Stop conditions

1. Front matter: the differences from the lineage are the listed exceptions plus the path rows' owned-rows text (finding 1 below); nothing else.
2. Item 1 closed to the named section in all three, with the missing-or-empty no-op and the dispatch condition.
3. Completions unchanged and matching plan 020 step 4; the Bot's single review is a landed operator setting (plan 021 line 121); no unlanded mechanism stated as present.
4. Checker OK on all three (header).

## Findings

1. P3, confidence high, `.orchestration/tasks/dotfiles-T128-followup-owners-review-a01.md:14`. Stop condition 1's exception list does not name the path rows' rewrite that the Round 2 addendum (item 3) applied, so a literal reading of "front matter equals its lineage task's except …" fails on 15 tools rows and 5 gate rows. The owner files are right; the stop-condition sentence is one clause short ("…and the path rows in the owned-rows form"). No verdict weight.
2. P3, confidence high, inherited non-path rows, carried from round 1: the tools workflow-inputs row (`…orchestrator-tools-followup-a01.md:69`) lists a02's scripts and binaries, and the gate's two `closed:` rows (`…gate-evidence-followup-a01.md:42,44`) name tests that arrive with PR #329. True once the lineage merges, which precedes every dispatch here. No verdict weight.

Task-file verdict: dotfiles-T128-orchestrator-tools-followup-a01: confirm
Task-file verdict: dotfiles-T128-gate-evidence-followup-a01: confirm
Task-file verdict: dotfiles-T128-playbook-rules-followup-a01: confirm
