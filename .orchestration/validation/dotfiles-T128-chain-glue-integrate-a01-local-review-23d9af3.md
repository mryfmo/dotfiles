---
task: dotfiles-T128-chain-glue-integrate-a01
head: 23d9af37b135faad5d5a63094eae37ad14c56fff
pr: 372
base: 1d41812678366506151579ce3e2ac96b20e8d4b5
started: 2026-10-16T22:50:56Z
finished: 2026-10-16T22:57:18Z
findings: 2
engine: codex review --base main (profile review, read-only)
---

- [P2] Recheck the PR head after the waits — scripts/orchestrator/chain-integrate.sh:120-122
- [P2] Register main-script contents in the threat table — scripts/orchestrator/chain-integrate.sh:73-76

```text
Concurrent pushes can produce stale review evidence before the chain detects the head mismatch. The required threat table also omits the main-script content control. Syntax checks passed; unit tests were not run in the read-only sandbox.

Full review comments:

- [P2] Recheck the PR head after the waits — scripts/orchestrator/chain-integrate.sh:120-122
  If another push lands during the checks or Bot wait, this guard checks only the base and proceeds with the old `head`. Consequently, local review examines the old commit, while `pr-feedback.py` collects the new head; the chain then writes an approved receipt before `acceptance-front-matter.py` rejects the mismatch. Recheck `headRefOid` after the waits and refuse or restart before reviewing and generating evidence.

- [P2] Register main-script contents in the threat table — scripts/orchestrator/chain-integrate.sh:73-76
  These checks establish a distinct trusted-input control: repository scripts executed with orchestrator credentials must be tracked and unchanged from HEAD. The authoritative task's `threat_table` covers the main checkout's branch and binary resolution, but still lacks a row for its executable contents. Add a row describing this guard and its negative test, as required by [AGENTS.md:78](AGENTS.md#L78); describing the control in the report does not add it to the required front matter.
Concurrent pushes can produce stale review evidence before the chain detects the head mismatch. The required threat table also omits the main-script content control. Syntax checks passed; unit tests were not run in the read-only sandbox.

Full review comments:

- [P2] Recheck the PR head after the waits — scripts/orchestrator/chain-integrate.sh:120-122
  If another push lands during the checks or Bot wait, this guard checks only the base and proceeds with the old `head`. Consequently, local review examines the old commit, while `pr-feedback.py` collects the new head; the chain then writes an approved receipt before `acceptance-front-matter.py` rejects the mismatch. Recheck `headRefOid` after the waits and refuse or restart before reviewing and generating evidence.

- [P2] Register main-script contents in the threat table — scripts/orchestrator/chain-integrate.sh:73-76
  These checks establish a distinct trusted-input control: repository scripts executed with orchestrator credentials must be tracked and unchanged from HEAD. The authoritative task's `threat_table` covers the main checkout's branch and binary resolution, but still lacks a row for its executable contents. Add a row describing this guard and its negative test, as required by [AGENTS.md:78](AGENTS.md#L78); describing the control in the report does not add it to the required front matter.
```
