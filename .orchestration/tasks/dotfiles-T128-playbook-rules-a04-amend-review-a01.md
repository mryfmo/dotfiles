---
format: 2
task_id: dotfiles-T128-playbook-rules-a04-amend-review-a01
kind: review
security: false
---

# AGMSG-TASK dotfiles-T128-playbook-rules-a04-amend-review-a01 — confirm amendment 1 of `dotfiles-T128-playbook-rules-a04` and the owner task `dotfiles-T128-playbook-rules-followup-a01` (review seat half; Codex headless runs the same check)

Drafted 2026-10-13 10:20Z by the orchestrator seat (plan 017, the G′ pattern applied to PR #328). The Codex Bot's review 5501887212 of PR #328's update-branch head `7771082f` left three threads on the a04 rule text (4257278283 P1: the task-file review's invariant check compares ids only where the design requires byte-for-byte sentence equality; 4257278271 P2: "thirty minutes" where the design limits worker idleness to 20; 4257278276 P2: the row unit lets one wildcard row cover several trust-boundary scripts) and the orchestrator's local review (C-32, `.orchestration/validation/dotfiles-T128-playbook-rules-a04-local-review-7771082.md`) one more (SKILL.md:164: `history.sh --limit 1000` is not a complete read after compaction). All four are sentences the a04 task text dictates (items 1, 4, 5), so the fix is amendment 1 of a04 plus one revise round; the residual findings of the final head need an owner on main first: the new task file. Amended file: `.orchestration/tasks/dotfiles-T128-playbook-rules-a04.md` (the pre-amendment copy is on `main` `a03c1daa`); new file: `.orchestration/tasks/dotfiles-T128-playbook-rules-followup-a01.md`. The TASK line carries both hashes.

## What changed (amendment 1 of a04)

1. Item 1: "thirty minutes … (INV-10's figure)" → the design's 20-minute idle figure (INV-10, design line 64: "a seated worker is not idle for 20 minutes while a dispatchable task exists"; 30 minutes is the first-push deadline), applied by the orchestrator to the minutes `bus-read.sh` prints (the script's own silence flag still uses 30, a recorded residual of the tools lineage); "a complete bus read, never from a default-limited one" → a read refused when it reaches its limit (what the merged `bus-read.sh` does), never a default-limited one nor one whose truncation went unnoticed; the "Once plan 007 T718 lands … until then" clause → the scripts are on main since a03c1daa.
2. Item 4: one row per concrete file the PR changes under a wildcard `allowed_files` entry at a trust boundary.
3. Item 5: the invariant check also compares each invariant's sentence byte-for-byte with the design read from main (INV-2, design line 56), by hand until a checker lands.
4. Completion: the one revise round with the local review's findings; residual P2 of the final head owned by `dotfiles-T128-playbook-rules-followup-a01`; no boundary between the amendment's dispatch and the merge. An "Amendment 1" section records the four findings and the design lines. Nothing else: items 2, 3, 6, 7, 8, the threat table and the premises are unchanged.

## The owner task (new)

`dotfiles-T128-playbook-rules-followup-a01`: a04's front matter (the same `allowed_files` and rows, its own task-copy and evidence rows, `after: [dotfiles-T128-playbook-rules-a04]`, two premises with pasted outputs), one item defined by the owned rows of a04's acceptance ledger (closed at a04's acceptance; an empty list is a no-op), Validation and Completion as a04's on a fresh branch after a04 merges.

## Stop condition

1. The diff of the a04 file against its copy on `main` contains only what the list above says; each changed sentence follows the design's words (paste `sed -n '56p;64p'` of the design on main) and not only the Bot's.
2. No sentence states an unlanded mechanism as present (the invariant check is by hand; the 20-minute figure is the orchestrator's reading of the script's minutes; the read is refused at its limit, not paginated).
3. The owner task passes C1 to C10 and C7b (the orchestrator pasted OK) and its item 1 is closed (no finding outside the named rows can be claimed); its premises' outputs match a fresh run.
4. `amend-sweep.sh` on the a04 file for `thirty minutes` and `complete bus read` hits only the Amendment 1 section (which quotes them); the checker's C10 hit on a04's item 3 (`regime-counters.sh` beside `; evidence=<command>`) predates the amendment (it is on main's copy) and is not in scope.

## Output

`.orchestration/validation/dotfiles-T128-playbook-rules-a04-amend-review-a01.md`: the usual header with both files' sha256, findings (`P0`–`P3`, confidence, `file:line`, one line), one line `Amendment verdict: dotfiles-T128-playbook-rules-a04: confirm|revise` and one line `Task-file verdict: dotfiles-T128-playbook-rules-followup-a01: confirm|revise`. Forbidden: editing tracked files, branches, commits, pushes, PRs. RESULT: `AGMSG-RESULT v1 task_id=dotfiles-T128-playbook-rules-a04-amend-review-a01 verdict=confirm|revise amended_task_sha256=<a04 sha> owner_task_sha256=<followup sha> validation=<path>`.

## Round 2 (orchestrator, 2026-10-13 10:31Z)

Round 1 (seat: one P2, two P3; Codex: one P2) applied: (1) the owner task's premise 2 is a presence check that holds on `origin/main` (`git cat-file -e … && echo present`), and its item 1 is defined by a greppable section of a04's acceptance record (`## Owned by dotfiles-T128-playbook-rules-followup-a01`, `<id>\t<class>` rows) landed by the boundary after a04's merge, with the dispatch condition stated; a04's Completion names that section. (2) a04 line 74's history paragraph carries the parenthetical "(superseded by amendment 1 of a04: INV-10's idle figure is 20 minutes)". (3) Item 4's clause is scoped to wildcard entries whose files are executed or applied; a wildcard over test fixtures or other data keeps one row (so a04's and the follow-up's fixture rows stand). Item 3's stale "Once plan 007 T718 lands" clause stays out of scope, as round 1 noted. Stop condition 4 now reads: `amend-sweep.sh` for `thirty minutes` hits only the Amendment 1 section and the superseded parenthetical. RESULT with `round=2` and both hashes.
