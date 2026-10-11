# Report: dotfiles-T128-process-rules-a05

- Seat: `claude-standard-dot-a003` in `.claude/worktrees/worker-f`, branch `docs/regime-pattern`, PR #318, from `7800ef92`. Fourth continuation of PR #318 (`reset_of: [a01, a02, a03, a04]`). a04 stopped under plan 006 S1, not INV-6, when the sixth Codex Bot P1 of one class landed on the counters bullet. The cause record is `.orchestration/learning/plan-006-s1-process-rules-counters-bullet-2026-10-11.md`.
- Task file sha256 `de2897da…` checked against the TASK at 23:32:05Z and copied byte-identical in `5f2a331d` to `.orchestration/dotfiles-T128-process-rules-a05/task.md`; the a01 to a04 directories stay as history. Content commit `dfdee38b`, then this evidence.

## Carried over

Items 1 to 8 are already on the branch (items 6 to 8 in `28d728c5` and `2a3f52e9`), together with the a02 revise round's five checks, the three Bot P2 fixes of `21c160c8` and the a03 revise round's fixes, all unchanged. Item 9 supersedes the sentences of items 4 and 8 that lived inside the counters bullet.

## Item 9 (`dfdee38b`, verbatim from the task file)

- SKILL "Review and integration invariants": the whole counters bullet as it stood on `7800ef92` is replaced, exactly, by the task's fenced bullet. It states three obligations by reference:
  - the script's output goes into the acceptance record;
  - S2 is decided from INV-6's counts, and an `unknown` component is read from the source INV-6 names (or the interim record, said so);
  - S1 is decided from the record's finding-class table over every swept and audited finding.

  It names no endpoint, badge, grouping, hand count or pre-A3 fallback. Item 4's `--limit 1000` sentence and item 8's review-body sentences go with the old bullet.
- Tests (`tests/unit/test_agmsg_orchestration_docs.py`), the task's four edits:
  - `test_counters_run_before_every_acceptance_action` keeps its two tokens and loses the three old-bullet tokens and their comments;
  - `test_manual_counts_read_the_whole_history` is removed, and the task's one comment line stands in its place;
  - `test_shape_rules_and_the_decision_sentence_are_pinned` pins "S2 is decided from INV-6's counts" in place of the old decision sentence;
  - `test_counters_add_review_body_findings` becomes `test_counters_bullet_names_owners_not_sources`. It slices the bullet, asserts the two new tokens, and asserts that "review bodies", "by hand", "gh api --paginate" and "until it is on `main`" are absent, one subTest each.

  No other old-bullet literal remains in the module. The threat-table bullet's own "by hand" (the pre-V1 shape check) is outside the slice.

Proofs (validation §3): each new token removed fails the new test; each forbidden phrase pasted into the bullet fails it; the old bullet pasted back fails it on all six subTests (both tokens and the four phrases); and removing the new decision-sentence pin fails `test_shape_rules_and_the_decision_sentence_are_pinned`. The docs module runs 40 tests, OK. The premises hold (validation §4).

## Bot threads

| Thread | Disposition |
|---|---|
| 4240250137, 4240348412, 4240382519, 4243516879, 4243537278, 4243631335 (the counters-bullet class) | `fixed:dfdee38b` (item 9) |
| 4243537279, 4243537281 | `fixed:28d728c5` (items 6 and 7) |
| 4243516880 | `fixed:114d5b91` (the CI watcher's no-checks race) |

The final head's CI and Bot wait, and any thread opened on it, are in the RESULT and the main-checkout copy of this report. The worker resolves no thread, and makes no fix round on the counters bullet: a Bot finding there is reported with its class.

## Notes

- Nothing here touches the threat-table rule's payload wording.
- Understand-Anything hook: did not fire. plan-mode-used: no.

## CompactionDB

`memory add` printed `546ec858-f8ac-4761-9189-3d288ba7c4e5` (validation §5).

cost: n/a
