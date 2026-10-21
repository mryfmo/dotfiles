---
task: dotfiles-T129-audit-inherit-replan-json-a01
head: 741e24272fd64b6a36c0d6725c53265de1c94982
pr: 390
base: 99a4a80f5a5b32a70cf7eb4f4d0db5a02d113841
started: 2026-10-18T04:44:33Z
finished: 2026-10-18T04:48:46Z
findings: 2
engine: codex review --base main (profile review, read-only)
---

- [P1] Verify merge content before inheriting the parent audit — scripts/orchestrator/chain-integrate.sh:181-188
- [P2] Update the pre-audit ledger reader for inherited audit IDs — scripts/orchestrator/chain-integrate.sh:191-192

```text
Audit inheritance can reuse a review despite changed PR-side behavior. Inherited finding IDs also conflict with the existing pre-audit ledger validator, blocking later audits.

Full review comments:

- [P1] Verify merge content before inheriting the parent audit — scripts/orchestrator/chain-integrate.sh:181-188
  If a merge resolution relocates an edit between repeated-context blocks in the same file, `git patch-id --verbatim` still returns identical IDs because it discards hunk coordinates and function headers. For example, enabling a flag in a production block instead of the audited development block can pass this comparison and inherit an audit of different behavior. The inheritance threat row is therefore not closed ([AGENTS.md:78](AGENTS.md#L78)). Verify that the merge contains no additional PR-side edits before reusing the audit.

- [P2] Update the pre-audit ledger reader for inherited audit IDs — scripts/orchestrator/chain-integrate.sh:191-192
  After an audit with findings is inherited, a subsequent content-changing head cannot complete its fresh audit. `orch-audit.sh` passes every lineage summary to `scripts/orchestrator/ledger-check.py`, which still derives finding IDs from filenames. An inherited summary named for B therefore demands `audit:B:1`, while its marker, preserved ledger, and updated gate use `audit:A:1`. This produces a ledger gap and aborts the audit. Update that reader to honor the inheritance marker too, rather than requiring duplicate finding rows.
Audit inheritance can reuse a review despite changed PR-side behavior. Inherited finding IDs also conflict with the existing pre-audit ledger validator, blocking later audits.

Full review comments:

- [P1] Verify merge content before inheriting the parent audit — scripts/orchestrator/chain-integrate.sh:181-188
  If a merge resolution relocates an edit between repeated-context blocks in the same file, `git patch-id --verbatim` still returns identical IDs because it discards hunk coordinates and function headers. For example, enabling a flag in a production block instead of the audited development block can pass this comparison and inherit an audit of different behavior. The inheritance threat row is therefore not closed ([AGENTS.md:78](AGENTS.md#L78)). Verify that the merge contains no additional PR-side edits before reusing the audit.

- [P2] Update the pre-audit ledger reader for inherited audit IDs — scripts/orchestrator/chain-integrate.sh:191-192
  After an audit with findings is inherited, a subsequent content-changing head cannot complete its fresh audit. `orch-audit.sh` passes every lineage summary to `scripts/orchestrator/ledger-check.py`, which still derives finding IDs from filenames. An inherited summary named for B therefore demands `audit:B:1`, while its marker, preserved ledger, and updated gate use `audit:A:1`. This produces a ledger gap and aborts the audit. Update that reader to honor the inheritance marker too, rather than requiring duplicate finding rows.
```
