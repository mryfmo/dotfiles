---
reviewed_at: 2026-10-13T01:25:21Z
reviewer: claude-review-dot-a001
profile: review
session: 2089b04f-f9c7-498b-86c5-76f2140048d5
design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md@20d0937b9f7c6adebe6e4d5e6ad26ceb3578ae9b050bdce4f353b0a00ce9504a
task: dotfiles-T128-task-review-t718-a01
round: 2
previous_round: dotfiles-T128-orchestrator-tools-a01@9f33e1dec7496bceef2b5f0c2dd498244842e77e5a3062c9a89e570da72ef110 (revise, three findings)
files:
  - dotfiles-T128-orchestrator-tools-a01@aaf02188d4ea60606f07a08379ba5184582c190c79ab431ee9587be599e5a908
verdicts:
  dotfiles-T128-orchestrator-tools-a01: confirm
---

# Task-file review: dotfiles-T128-orchestrator-tools-a01 (plan 007 T718, first slice under plan 012 B), round 2

Read against the design on main (v22, 3709a6d8), plan 012 B, plan 013 A′ (the operator's choice) and the a03 task file's Amendment 1 as it stands on disk (686806a1 on main; the amended copy carries the JSON-between-`---` contract at its item 2 and Amendment 1), main's scripts/regime-counters.sh and its test, and C-20, C-23, C-25, C-26. Premises replayed with the executor's binaries (/usr/bin/grep, git grep against origin/main, /bin/ls): every output byte-equal to the pasted one; the new premise (test_regime_counters.py line 451, the review-title S1 candidate) replays. Checker: OK (C1 to C10, C7b: scripts/regime-counters.sh and tests/unit/test_regime_counters.py now have one row each, lines 20 and 22).

Round-1 findings, each against the revised file:

- P2 (item 3, slug source): closed. Line 83 names the format and the reader: the acceptance record's machine-readable block between its first two `---` lines is a JSON object (the a03 contract as plan 013 A′ amends it; `ledger` a list of {id, class}), read with jq; a record-backed class prints `S1: class=<slug> count=<n> source=record` with the slug matched against ^[a-z0-9-]+$, and without a record the title grouping stays a candidate printing class=unclassified with the title as a JSON string, a field no procedure substitutes into a command (plan 010 D). This agrees with the amended a03 (the JSON block is valid YAML, so the gate's json.loads and the counters' jq read one object); line 451's expectation and the two fixtures are named in the test clause.
- P2 (item 1, complete read): closed. Line 81 reads "history.sh --limit 1000 or lib/storage.sh's storage_history, never the database file".
- P3 (environment row): closed. Line 37 names git (rev-parse --show-toplevel), /usr/bin/grep, shasum, jq, sort, date (coreutils), agmsg-dispatch, history.sh or lib/storage.sh, and uv run --no-project for three-repeat.sh; the tests stub every host binary on PATH.

Correction to the round-1 receipt's tier sentence, as my PONG of round 1 stated: scripts/ is a high-risk prefix of scripts/require-crit-review.py (HIGH_RISK_PREFIXES), so the gate's review requirement applies to this PR; the design tier stays review (INV-1, by the precedent of regime-counters-a02 "Review tier by path"), the gate and the audit runner are outside allowed_files, and after: [] fits plan 012 B. Round-1 findings were unaffected by that sentence.

Note, not a finding (P3 0.6, line 83): "read with jq only, never with grep or sed over the prose" is a parse rule for the JSON; slicing the lines between the first two `---` markers before jq needs a line tool (awk or sed on the markers), which is not a read of the prose. The implementer may do that without an amendment; the audit reads it as the contract intends.

Task-file verdict: dotfiles-T128-orchestrator-tools-a01: confirm
