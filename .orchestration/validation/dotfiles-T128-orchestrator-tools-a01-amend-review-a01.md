---
reviewed_at: 2026-10-13T02:53:25Z
reviewer: claude-review-dot-a001
profile: review
session: 2089b04f-f9c7-498b-86c5-76f2140048d5
design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md@20d0937b9f7c6adebe6e4d5e6ad26ceb3578ae9b050bdce4f353b0a00ce9504a
task: dotfiles-T128-orchestrator-tools-a01-amend-review-a01
round: 2
task_file: dotfiles-T128-orchestrator-tools-a01-amend-review-a01@9b534064842277dd147638a41198b5b77c7812f9899112e13e02cbef2327518d
files:
  - dotfiles-T128-orchestrator-tools-a01@91eb1ebe246f76e138ce8f3bf108adff844f5acf303bcfecc2b7bc62eb0130ee
previous: round 1 confirm on 204a7e30 (receipt fe77b118103d73bde3b60393abe9da66638d4a8cb46cd08d761fbf7f16cfe94f, two P3 text notes); main ce0af5d0 copy aaf02188 (as dispatched)
verdicts:
  dotfiles-T128-orchestrator-tools-a01: confirm
---

# Amendment review: dotfiles-T128-orchestrator-tools-a01 amendment 1 (PR #336 Bot threads), review-seat half, round 2

Both hashes of the 02:52:22Z TASK line recomputed and equal. Diff against 204a7e30: lines 85, 88 and 104 only; against main: the same five hunks as round 1 (18, 20 to 25, 85 to 86, 88, 101 to 104). Checker OK (C1 to C10, C7b); the four test names still appear exactly twice each.

The Codex half's round-1 P1 and my round-1 P3s, judged against 91eb1ebe:

- Record form: closed. dispatch.sh appends "<the line as sent> read_at=<read_at from the bus through history.sh, or unread>" to the dispatch list of the record's JSON block (the object between the first two --- lines), read and written with the standard library's json (object_pairs_hook refusing duplicate keys, sort_keys, indent=2), the key created when absent. This is the literal dispatch: key the a04 rule sentence names, and it matches dotfiles-T128-gate-evidence-a04 (13d2ca48, redesign round 2) item 2: dispatch, optional, a list of strings each a sent bus line followed by " read_at=<timestamp or unread>", validated by the gate only as a list of strings. Item 2's happy-path test re-reads the block with the gate's loader. The sort_keys and indent=2 convention is the one acceptance-front-matter.py (T718 a02) writes with, so the two writers produce one block form.
- Wording of the TASK refusal: closed. "refuses an AGMSG-TASK line without a task_file= and a 64-hex task_sha256=" (the 64-hex bound also refuses the empty field of M-20261012-26 before any recomputation).
- The Amendment 1 section (line 104) names the JSON block dispatch key; PING lines go through dispatch.sh too.

Stop condition 1 to 3 as in round 1, with point 2's record-form clause now met.

Note, not a finding: "a record without a block gets one holding only dispatch" is a record the gate would refuse until acceptance-front-matter.py fills the identity triple and the ledger; that is the intended order (dispatch lines first, the record completed at acceptance), and the gate runs only at acceptance.

## Findings

None.

Amendment verdict: dotfiles-T128-orchestrator-tools-a01: confirm
