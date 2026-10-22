---
task: dotfiles-T128-chain-glue-finish-a02
head: b8013697dad0c316c1e578a38439ea739ca7845d
pr: 378
base: 7da0cdfab9de9fbea673b82379acd4e317115065
started: 2026-10-22T01:15:29Z
finished: 2026-10-22T01:22:04Z
findings: 1
engine: codex review --base main (profile review, read-only)
---

- [P2] Preserve the source prefix for inherited audit dispositions — scripts/orchestrator/chain-finish.sh:127-128

```text
The finish command rejects inherited audits with existing finding dispositions, breaking the audit-reuse flow. Shell syntax, ShellCheck, and a focused reproduction were checked; the full test suite was not run in the read-only sandbox.

Review comment:

- [P2] Preserve the source prefix for inherited audit dispositions — scripts/orchestrator/chain-finish.sh:127-128
  When `chain-integrate.sh` inherits an audit after an update-branch-only merge, the summary's `inherited-from: <old-sha7>` marker preserves the original finding IDs, as `swept_finding_ids()` and `ledger-check.py` already recognize. This lookup instead requires the current head's prefix, rejecting an existing disposition with exit 12 and blocking the finish flow. Read the inheritance marker and use its prefix for these lookups.
The finish command rejects inherited audits with existing finding dispositions, breaking the audit-reuse flow. Shell syntax, ShellCheck, and a focused reproduction were checked; the full test suite was not run in the read-only sandbox.

Review comment:

- [P2] Preserve the source prefix for inherited audit dispositions — scripts/orchestrator/chain-finish.sh:127-128
  When `chain-integrate.sh` inherits an audit after an update-branch-only merge, the summary's `inherited-from: <old-sha7>` marker preserves the original finding IDs, as `swept_finding_ids()` and `ledger-check.py` already recognize. This lookup instead requires the current head's prefix, rejecting an existing disposition with exit 12 and blocking the finish flow. Read the inheritance marker and use its prefix for these lookups.
```
