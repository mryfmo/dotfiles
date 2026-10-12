---
format: 2
task_id: dotfiles-T128-playbook-rules-redesign-a02
kind: review
security: false
---

# AGMSG-TASK dotfiles-T128-playbook-rules-redesign-a02 — write the successor task file `dotfiles-T128-playbook-rules-a03` (plan 009 option A, the operator's choice at 14:0xZ)

Drafted 2026-10-12 by the orchestrator seat. `dotfiles-T128-playbook-rules-a02` (amendment 1, sha `07b78f64…`, head `c4e0bb72` on PR #328) drew two Bot P1s (4248711363, 4248711371) of one class, a rule sentence stating an unlanded mechanism as present; with 4248319926 that class reached three on the artifact, the second S1 cycle, and the operator chose plan 009 option A. The change is task text, so it would be amendment 2 and INV-6's count: a02 is withdrawn and the redesign is yours. The worker `claude-standard-dot-a003` holds at `c4e0bb72` and continues under a03 on the same branch and PR.

## Inputs

- `.orchestration/tasks/dotfiles-T128-playbook-rules-a02.md` (amendment 1), `.orchestration/plans/009-resume-t703-pr328.md` (option A's sentences), the two threads (`gh api repos/mryfmo/dotfiles/pulls/328/comments --jq '.[]|select(.id==4248711363 or .id==4248711371)|.body'`, quoted in plan 009 and M-20261012-19), C-21, the SKILL on `main` (its `schemas/task.json` sentence is the form), and the orchestrator's checker with C9 (`task-consistency-check.py`; on a02 it names items 2 and 4; item 3's gate sentence is the third, caught by the Bot).

## What the successor says (everything else verbatim from a02 amendment 1)

1. Front matter: `task_id: dotfiles-T128-playbook-rules-a03`, `reset_of: [dotfiles-T128-playbook-rules-a01, dotfiles-T128-playbook-rules-a02]`, the a03 evidence directory in `allowed_files` (a02's no longer), copy rows for the a01, a02 and a03 task copies (C3), `design_review.receipt` round 22.
2. Item 2 (the amendment rule): "… travels as a task amendment (hashed, checked by the task-consistency check C1 to C6 once plan 007 T704 lands it and by hand until then, confirmed by the review seat), never as a PONG answer."
3. Item 3 (the three-repeat procedure), last sentence: "Once `dotfiles-T128-gate-evidence-a02` lands, the gate refuses the action without the paste; until then the orchestrator refuses it by rule. Every `not-applicable` disposition carries `; evidence=<command>` with the output pasted in the record."
4. Item 4 (the row unit), last clause: "… one row per orchestrator effect from the fixed list (forced removal, merge, update-branch); C4 of the task-consistency check (plan 007 T704) verifies the path half once it lands, and the task-file review checks it by hand until then."
5. Item 6 unchanged (it already says "required in PR mode once `dotfiles-T128-gate-evidence-a01` lands"; replace that id with `dotfiles-T128-gate-evidence-a02`, the successor that carries the change).
6. The heading carries the reset; the intro names the two S1 cycles, plan 009 option A and the a02 head `c4e0bb72`; the worker's commits 4486dbdd, 4b62feda and c4e0bb72 stay; one Completion clause (PR #328 stays open, `update-branch` is the orchestrator's after the a03 head).
7. Nothing else changes: not items 1, 5, 7, 8, not the premises (re-paste premise 1 with `/usr/bin/grep -n` from a worktree at `origin/main` `7cbe5405`, per C-18).

## Stop condition

`task-consistency-check.py` C1 to C9 pass on a03 (state what you re-derived: the three copy rows, C7's names, and C9 by reading every double-quoted sentence for a mechanism named as present without its landing condition); the differences from a02 amendment 1 are exactly items 1 to 6; every quoted sentence of a03 names a mechanism only with "once … lands" or "until" unless it exists on `origin/main` (`git ls-tree`/`git grep` it).

## Output

Write `.orchestration/tasks/dotfiles-T128-playbook-rules-a03.md` (through the permission gate, the main checkout) and the receipt `.orchestration/validation/dotfiles-T128-playbook-rules-redesign-a02.md` (header; diff summary; checks; the successor's sha256), then `AGMSG-RESULT v1 task_id=dotfiles-T128-playbook-rules-redesign-a02 status=ready_for_review verdict=accept design_sha256=<sha256 of the a03 file> receipt=<path> receipt_sha256=<sha256>` via `agmsg-dispatch dotfiles-conformance claude-review-dot-a001 claude-deep-dot w5:p1`. max_turns=3. Forbidden: editing any other tracked file; branches; PRs.
