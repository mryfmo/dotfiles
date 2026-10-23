---
task: dotfiles-T128-chain-glue-finish-a02
head: 2b5866370d3796c90b9b9a96499f20fe8dd4d4fe
pr: 378
base: 7da0cdfab9de9fbea673b82379acd4e317115065
started: 2026-10-21T22:30:15Z
finished: 2026-10-21T22:34:00Z
findings: 1
engine: codex review --base main (profile review, read-only)
---

- [P2] Preserve the source SHA for inherited audit dispositions — scripts/orchestrator/chain-finish.sh:122-123

```text
The new finish command rejects already-dispositioned inherited audits produced by the existing integration command. Syntax checks and comparison lint passed; the full test suite was not run in the read-only environment.

Review comment:

- [P2] Preserve the source SHA for inherited audit dispositions — scripts/orchestrator/chain-finish.sh:122-123
  When `chain-integrate.sh` inherits an audit after an update-branch merge, the summary contains `inherited-from: <oldsha7>`, and the gate's `swept_finding_ids()` deliberately retains that original finding identity. This lookup instead requires the current head's SHA, so an inherited audit whose findings already have valid dispositions exits 12 and cannot complete integration. Honor the inheritance marker when looking up disposition lines, and add a test covering both chain halves.
The new finish command rejects already-dispositioned inherited audits produced by the existing integration command. Syntax checks and comparison lint passed; the full test suite was not run in the read-only environment.

Review comment:

- [P2] Preserve the source SHA for inherited audit dispositions — scripts/orchestrator/chain-finish.sh:122-123
  When `chain-integrate.sh` inherits an audit after an update-branch merge, the summary contains `inherited-from: <oldsha7>`, and the gate's `swept_finding_ids()` deliberately retains that original finding identity. This lookup instead requires the current head's SHA, so an inherited audit whose findings already have valid dispositions exits 12 and cannot complete integration. Honor the inheritance marker when looking up disposition lines, and add a test covering both chain halves.
```
