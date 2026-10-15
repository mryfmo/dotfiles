---
reviewed_at: 2026-10-14T05:33Z
reviewer: claude-review-dot-a001 (review seat; the Codex half runs the same check in parallel)
profile: review
session: 2089b04f
task: dotfiles-T128-project-map-reload-hook-a01-amend-review-a01
round: 1
task_file: .orchestration/tasks/dotfiles-T128-project-map-reload-hook-a01-amend-review-a01.md@9eda4a8f07358a2a0f8adde453439d9a5e08788a03dcabbb5f23b5ee635b4936
amended_task: .orchestration/tasks/dotfiles-T128-project-map-reload-hook-a01.md@452a344479136254b1cfa266204827e4a715a4e26489bc751c5b7ee33d8e2b07 (untracked; previous_amended_task_sha256 cc6ac23f, the pair-confirmed round-3 text, this seat's saved copy)
diff_base: this seat's round-3 copy (cc6ac23f); same bytes as the orchestrator's by hash
diffstat: "1 file changed, 5 insertions(+), 1 deletion(-) (git diff --no-index --stat): one changed sentence and one new section, as the brief states"
consistency_check: "dotfiles-T128-project-map-reload-hook-a01.md: OK (checker fdab23e0 on a copy named by the task id, run from the main checkout)"
amend_sweep: "no leftover of: outside `tests/` (plan 021 (the superseded cap sentence)"
sources: the design INV-2 (.orchestration/tasks/dotfiles-T128-regime-v3-a01.md line 56: 500 added lines outside tests/, .orchestration/ and scripts/legacy-task-ids.txt), plan 021 step 7.2, the a05 and a06 acceptance records (lines 301 and 92: "3 files outside .orchestration, … added non-test"), the sibling tasks' Check sentences
verdict: confirm
---

# Amendment review: dotfiles-T128-project-map-reload-hook-a01 (the project-map reload hook), amendment 1

Both hashes of the 05:30:54Z TASK line recomputed and equal; the previous hash equals this seat's round-3 copy. The diff against that copy is exactly the brief's two changes: the Check's cap sentence now reads "outside `tests/` and outside `.orchestration/`" with the reason in its parenthesis (line 106), and the `## Change of 2026-10-14 (amendment 1 …)` section states it (lines 111 to 114). Nothing else differs; the threat table, the items, the premises and the Completion are byte-identical.

## Stop conditions

1. The two hunks are the list and nothing more.
2. The amendment adds no behaviour to any script or procedure: it names what the cap counts. No row is due.
3. The two closed rows and their tests are unchanged (each name once in the table and once in item 5). The wording agrees with INV-2, whose line-count cap already excludes `.orchestration/` (and `scripts/legacy-task-ids.txt`), and with how a05 and a06 reported their caps ("files outside .orchestration", "added non-test"); plan 021 step 7.2's "≤ 200 changed lines outside tests" is the practice cap the sentence applies, and the exclusion makes it count the same tree INV-2 counts.
4. Checker OK on 452a3444; sweep clean (header); no `reset_of`; the task-copy row and the evidence directory are unchanged. Count words: "110 lines" is the brief's figure for the task copy (the file is 114 lines after this amendment, 110 before it); the only times are bus times (05:29Z, 05:29:15Z, 05:23Z).

## Findings

- P3 (high) `.orchestration/tasks/dotfiles-T128-gate-wrapper-path-a01.md:91`, `.orchestration/tasks/dotfiles-T128-task-checkers-a01.md:144` — the two sibling tasks carry the same literal cap sentence ("outside `tests/`", no `.orchestration/` exclusion); the pair-confirmed gate wrapper task is not yet dispatched and T704 is in flight, so the same question can recur there. One amendment each with this sentence, or the step-7 template (plan 021 7.1) carrying it, closes the recurrence.
- P3 (high) `.orchestration/tasks/dotfiles-T128-project-map-reload-hook-a01-amend-review-a01.md:10` — the brief again says the pre-amendment copy "is on `main`" and then quotes "not on main; …" (the same slip as the two T704 amendment briefs; brief only).

## Derivations

1. The worker's PONG of 05:29:15Z is between the worker and the orchestrator and not in this seat's history; the brief's account is taken as pasted, and the cap convention it cites is verified in INV-2 and the a05/a06 records.

Amendment verdict: dotfiles-T128-project-map-reload-hook-a01: confirm
