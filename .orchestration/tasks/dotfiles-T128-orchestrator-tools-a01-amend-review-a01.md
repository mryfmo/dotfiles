---
format: 2
task_id: dotfiles-T128-orchestrator-tools-a01-amend-review-a01
kind: review
security: false
---

# AGMSG-TASK dotfiles-T128-orchestrator-tools-a01-amend-review-a01 — confirm amendment 1 of `dotfiles-T128-orchestrator-tools-a01` (review seat half; Codex headless runs the same check)

Drafted 2026-10-13 02:5xZ by the orchestrator seat. The Codex Bot's review of PR #336 (worker-c, heads `61290da8`, `4843ccb6`, `5b6d5f24`) raised 4253994704 on this task's threat row (one `closed` row covered three scripts with one test) and four threads on the scripts (4253994697 three-repeat.sh runs the caller checkout's CLI; 4254107304 a line file with trailing blank lines; 4254107312 the dispatched line is not recorded in the acceptance record; 4254163604 a TASK without `task_sha256=` is sent). The row and the omitted behaviours are task text. Amended file: `.orchestration/tasks/dotfiles-T128-orchestrator-tools-a01.md`, sha256 `204a7e300f7f2028d60909f6deca96beb81fc38dc84e95f2a4784e56644971f3`; the pre-amendment copy is on `main` (`ce0af5d0`, sha256 aaf02188…).

## What changed (amendment 1)

- Threat table: the one closed row for three scripts becomes four rows, one per script plus one for dispatch.sh's omission paths, each closed by a named test.
- Item 1: `dispatch.sh` takes an optional `<acceptance-record>` and appends `<line> read_at=<…>` to the `dispatch` list of the record's JSON block after the send (the literal `dispatch:` key of the a04 rule); it reads exactly one physical line; it refuses an `AGMSG-TASK` without `task_file=` and `task_sha256=`. `three-repeat.sh` resolves the records directory and the CompactionDB CLI from its own checkout, never the caller's cwd.
- Item 2: the four test names of the rows.
- An "Amendment 1" section at the end. Context: thread bodies via `gh api repos/mryfmo/dotfiles/pulls/336/comments --jq '.[]|select(.in_reply_to_id==null)|.body'`; the a04 rule text on PR #328 head `2276a365` (`git show 2276a365:home/dot_agents/skills/agmsg-orchestration/SKILL.md`, step 6: the dispatch line "as the bus line with its read marker").

## Stop condition

1. The diff of the task file against its copy on `main` contains only what the list above says.
2. Each closed row names a test that closes its risk (the test names appear verbatim in item 2); the record entry matches the a04 sentence's form (`dispatch:` key); the own-checkout resolution closes 4253994697 by construction.
3. The file passes C1 to C10 and C7b (the orchestrator pasted OK); `reset_of`, the copy rows and the a01 directory are unchanged.

## Output

`.orchestration/validation/dotfiles-T128-orchestrator-tools-a01-amend-review-a01.md`: the usual header with the file's sha256, findings (`P0`–`P3`, confidence, `file:line`, one line), one line `Amendment verdict: dotfiles-T128-orchestrator-tools-a01: confirm|revise`. Forbidden: editing tracked files, branches, commits, pushes, PRs. RESULT: `AGMSG-RESULT v1 task_id=dotfiles-T128-orchestrator-tools-a01-amend-review-a01 verdict=confirm|revise amended_task_sha256=204a7e300f7f2028d60909f6deca96beb81fc38dc84e95f2a4784e56644971f3 validation=<path>`.

## Round 2 (orchestrator, 2026-10-13 02:5xZ)

Round 1: the seat confirmed `204a7e30…`; the Codex half's one P1: the record form was a prose bullet while the a04 rule stores each line under a literal `dispatch:` key. Item 1 now appends the sent line with its read marker to the `dispatch` list of the record's JSON block (standard library json; the key created when absent), item 2's happy-path test re-reads the block with the gate's loader; `dotfiles-T128-gate-evidence-a04` (round 2 of its redesign) names `dispatch` as an optional list of strings the gate does not validate beyond its type. PING lines go through dispatch.sh too (the worker's decision), and a TASK needs a 64-hex `task_sha256=`. The TASK line carries the file's sha256.
