---
reviewed_at: 2026-10-14T04:41Z
reviewer: claude-review-dot-a001 (review seat; the Codex half runs the same check in parallel)
profile: review
session: 2089b04f
task: dotfiles-T128-gate-wrapper-path-review-a01
round: 3
task_file: .orchestration/tasks/dotfiles-T128-gate-wrapper-path-review-a01.md@756627355dde04a7b1482661c92950ed274e5451be005f4a4b238f91390a1247
path_task: .orchestration/tasks/dotfiles-T128-gate-wrapper-path-a01.md@3ccbc7bf90f4318cc807a2e14759d60e67ede8d7a0a0ae2d561a9b4c46fb0977 (untracked; previous_path_task_sha256 c06406bc, this seat's round-2 copy; round-1 hash 4d35fce0, both superseded)
previous_receipt: 571601887be988a070ca08e1cb6b8b11360af5bfd0e10c027e2d28955a8af53c (round 2, revise on c06406bc with one P2 and one P3, both applied here; superseded by this file at the same path)
sources: origin/main 28eec93c (scripts/orchestrator/orch-gate.sh lines 49 and 58 to 74; tests/unit/test_orchestrator_tools.py lines 26 to 42 and 1041 to 1056), the round-1 sources unchanged
consistency_check: "dotfiles-T128-gate-wrapper-path-a01.md: OK (checker fdab23e0 on a copy named by the task id, run from the main checkout)"
premises: all four re-run through each premise's own command and compared whole: EQUAL, EQUAL, EQUAL, EQUAL (premise 2 through its round-3 command, four lines; premises 3 and 4 from a shell with the keyring, outside the sandbox: 1, and the mise ERROR line)
verdict: confirm
---

# Task-file review: dotfiles-T128-gate-wrapper-path-a01 (the gate wrapper's PATH), round 3

Both hashes of the 04:40:34Z TASK line recomputed and equal; the previous hash equals this seat's round-2 copy. The diff against that copy is exactly the brief's Round 3 list: the test-module row says three places and three edits (lines 22 to 23), premise 2 sets both PATH orders in its command (lines 51 to 52), item 2's stubs record with builtins or absolute paths and its first test asserts the resolution's cwd and order (lines 79 to 80), item 3 names the third edit (the `RUN` body) (line 83), out of scope, Check and Completion say three edits (lines 87, 91, 95). Nothing else differs. The round-2 P2 and P3 are answered as written, and the Codex half's round-2 P1 and P2 too. No finding remains.

## Stop conditions, round 3

1. Unchanged: nothing contradicts the audit line, decision C, a06 item 10 or plan 021 step 7. Premise 2's new command replays EQUAL in this shell (the pasted four lines; the command fixes both PATH orders itself, so the output no longer depends on the caller's order). Premises 3 and 4 replayed EQUAL again from a shell with the keyring (`1`; `mise ERROR gh is a mise bin however it is not currently active …`). Premise 1 is byte-identical to round 1 (EQUAL then).
2. Unchanged from round 2: four touch points, all in `allowed_files`, nothing else; the one overlap with T704 is serialized by `after:`.
3. The three closed rows name the three tests, each exactly once in the table and once in item 2 (counts 2, 2, 2). Row one's test now also proves where and when the resolution ran: the stubs log `<name> <argv> <cwd>`, the `mise which` lines must carry the trusted root as cwd and precede the stub git's checkout, which matches orch-gate.sh on main (`cd -- "${root}"` at line 49 precedes everything the new code adds, and the checkout at line 61 follows). Rows two and three unchanged. The explicit-environment test and the gate-inputs test of the existing module can now pass: the third edit makes `RUN` record with `export -p` or `/usr/bin/env` and `/bin/cat`, the exact gap the round-2 replay showed. The Completion matches plan 020 rows 1, 2 and 4 as before.
4. Checker OK on 3ccbc7bf (header). Count words agree: "three edits" (item 3, the row, out of scope, Check, Completion), "three closed rows", "two symlinks", "fourth P1"; the only times are bus times. Caps by construction: one script, one new test module, three edits in an existing one.

## Findings

None. Approval: the task text can now pass its own Check inside its `allowed_files` (the round-1 P1 and the round-2 P2 were the two ways it could not), each added behaviour has its closed row with its test named verbatim in item 2, and the four premises replay equal.

Task-file verdict: dotfiles-T128-gate-wrapper-path-a01: confirm
