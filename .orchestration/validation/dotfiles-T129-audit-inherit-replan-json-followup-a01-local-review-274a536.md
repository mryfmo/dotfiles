---
task: dotfiles-T129-audit-inherit-replan-json-followup-a01
head: 274a5361c14fa75c0ad43a5eceeec2d99f789fac
pr: 413
base: 61231cd99c23ccb69ecbe4eef9374ebc1dde5248
started: 2026-10-18T10:29:01Z
finished: 2026-10-18T10:34:10Z
findings: 2
engine: codex review --base main (profile review, read-only)
---

- [P2] Apply the gate's exact re-plan schema in the counters — scripts/regime-counters.sh:175-177
- [P2] Re-audit instead of inheriting a blocked parent result — scripts/orchestrator/chain-integrate.sh:197-201

```text
Audit inheritance can perpetuate a blocked result instead of retrying, and re-plan validation differs between the counters and gate. Syntax checks passed; full unit tests were not run in the read-only sandbox.

Full review comments:

- [P2] Re-audit instead of inheriting a blocked parent result — scripts/orchestrator/chain-integrate.sh:197-201
  If the parent audit ended with `Verdict: blocked`, `orch-audit.sh` still creates both receipt files and the matching chain-log line, so this branch inherits the unusable result. The gate rejects it, while the `head already audited` precondition prevents retrying the new head; subsequent unchanged update-branch merges inherit it again. Require a usable parent verdict before inheritance and otherwise run a fresh audit, following the retry procedure referenced by [AGENTS.md:44](AGENTS.md#L44).

- [P2] Apply the gate's exact re-plan schema in the counters — scripts/regime-counters.sh:175-177
  For a class with three ledger rows, a re-plan containing all four valid parts plus an extra key such as `notes` produces `re-plan=present` here. However, `record_field_errors()` and the front-matter writer reject that same object because they require exactly four keys. This makes the acceptance-time counters report a satisfied re-plan requirement that the gate rejects. Apply the same exact-key validation here and cover this malformed-object case in the counter tests.
Audit inheritance can perpetuate a blocked result instead of retrying, and re-plan validation differs between the counters and gate. Syntax checks passed; full unit tests were not run in the read-only sandbox.

Full review comments:

- [P2] Re-audit instead of inheriting a blocked parent result — scripts/orchestrator/chain-integrate.sh:197-201
  If the parent audit ended with `Verdict: blocked`, `orch-audit.sh` still creates both receipt files and the matching chain-log line, so this branch inherits the unusable result. The gate rejects it, while the `head already audited` precondition prevents retrying the new head; subsequent unchanged update-branch merges inherit it again. Require a usable parent verdict before inheritance and otherwise run a fresh audit, following the retry procedure referenced by [AGENTS.md:44](AGENTS.md#L44).

- [P2] Apply the gate's exact re-plan schema in the counters — scripts/regime-counters.sh:175-177
  For a class with three ledger rows, a re-plan containing all four valid parts plus an extra key such as `notes` produces `re-plan=present` here. However, `record_field_errors()` and the front-matter writer reject that same object because they require exactly four keys. This makes the acceptance-time counters report a satisfied re-plan requirement that the gate rejects. Apply the same exact-key validation here and cover this malformed-object case in the counter tests.
```
