---
format: 2
task_id: dotfiles-T128-gate-evidence-a03-amend-review-a01
kind: review
security: false
---

# AGMSG-TASK dotfiles-T128-gate-evidence-a03-amend-review-a01 — confirm amendment 1 of `dotfiles-T128-gate-evidence-a03` (review seat half; Codex headless runs the same check)

Drafted 2026-10-13 01:4xZ by the orchestrator seat under plan 013 option A′ (operator). The Codex Bot's review 5493539294 of PR #329 head `c36fcd35` raised three P1s (4250238714 pr not compared with the swept PR; 4250238721 the gate's uv/PyYAML/grep inputs absent from the environment row; 4250238729 duplicate YAML keys kept). Amended file: `.orchestration/tasks/dotfiles-T128-gate-evidence-a03.md`, sha256 `e8cfe390315dc3053d271a4e849febb896ff60f3a19ca5f2959f4644178935a4`; the pre-amendment copy is on `main` (`3709a6d8`, sha256 686806a1…).

## What changed (amendment 1)

- Item 2: the machine-readable part is a JSON object between the first two `---` lines, loaded with the standard library (`object_pairs_hook` refuses a duplicate key, `parse_constant` refuses NaN/Infinity), no uv, no subprocess, no online retry; the identity triple `task`/`head`/`pr` checked together, `pr` against `PR_FEEDBACK_EVIDENCE`'s; the S6 record set recomputed with `pathlib` (same match as the grep).
- Item 3: seven acceptance fixtures (three added: wrong pr, duplicate key, NaN); caps 120 lines, at least nine new tests.
- Threat rows: the ACCEPTANCE_EVIDENCE control says "JSON block"; the environment-inputs row says "none" with the reason, naming C11.
- An "Amendment 1" section at the end. Context: thread bodies via `gh api repos/mryfmo/dotfiles/pulls/329/comments --jq '.[]|select(.id==4250238714 or .id==4250238721 or .id==4250238729)|.body'`; plan 013; M-20261012-24 and C-26.

## Stop condition

1. The diff of the task file against its copy on `main` (`3709a6d8`) contains only what the list above says.
2. The amended contract closes the three threads by construction (a duplicate key cannot pass the loader; `pr` is a compared field; the gate's runtime has no third-party package or host binary) and does not contradict the design (INV-1: no hand-written parser; INV-12) or plan 011 F's field checks.
3. The file passes C1 to C10 (the orchestrator pasted OK) and C7b; `reset_of`, the copy rows and the a03 directory are unchanged.

## Output

`.orchestration/validation/dotfiles-T128-gate-evidence-a03-amend-review-a01.md`: the usual header with the file's sha256, findings (`P0`–`P3`, confidence, `file:line`, one line), one line `Amendment verdict: dotfiles-T128-gate-evidence-a03: confirm|revise`. Forbidden: editing tracked files, branches, commits, pushes, PRs. RESULT: `AGMSG-RESULT v1 task_id=dotfiles-T128-gate-evidence-a03-amend-review-a01 verdict=confirm|revise amended_task_sha256=e8cfe390315dc3053d271a4e849febb896ff60f3a19ca5f2959f4644178935a4 validation=<path>`.

## Round 2 (orchestrator, 2026-10-13 01:3xZ)

Round 1 was the Codex half alone (`…-amend-review-a01-codex.md`, 01:27Z): one P1, a test for the `parse_constant` refusal (INV-12). Applied once: item 3 adds `acceptance-nan.md` (refused with `acceptance record: non-finite number`), the fixture cap is 120 lines and the test count grows by at least nine; item 2 names the refusal text. The seat's TASK line of 01:26:03Z (bus 791) carried empty hash fields (M-20261012-26) and is void; the round-2 line that follows carries this file's sha256. Same stop condition.
