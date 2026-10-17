---
task: dotfiles-T128-chain-glue-finish-a01
head: f4d86ee5c061cf329480fa8ccff239897d29faeb
pr: 378
base: f7847616970d6bd83739a75a65ad8f7c35e91462
started: 2026-10-17T02:17:00Z
finished: 2026-10-17T02:20:33Z
findings: 3
engine: codex review --base main (profile review, read-only)
---

- [P1] Pin the cost script's tools before fast-forwarding — scripts/orchestrator/chain-finish.sh:147-148
- [P2] Measure the trimmed disposition reason — scripts/orchestrator/chain-finish.sh:111-112
- [P2] Read the last nonblank audit verdict line — scripts/orchestrator/chain-finish.sh:101-102

```text
Post-merge tool resolution can cross the intended trust boundary, and audit parsing disagrees with existing gate validation. Syntax checks passed; filesystem-writing unit tests were not run in the read-only environment.

Full review comments:

- [P1] Pin the cost script's tools before fast-forwarding — scripts/orchestrator/chain-finish.sh:147-148
  With the normal mise-shim PATH, a PR changing tool configuration can affect this post-merge call. The saved `pr-cost.sh` invokes bare `git`, `gh`, `jq`, and `date` from the newly fast-forwarded checkout, allowing PR-controlled configuration to select executables under the orchestrator's credentials. Snapshotting the script does not pin those dependencies. Supply a safe PATH resolved before fast-forwarding, as `orch-gate.sh` does; the threat table's environment-input mitigation otherwise remains ineffective ([AGENTS.md:78](AGENTS.md#L78)).

- [P2] Read the last nonblank audit verdict line — scripts/orchestrator/chain-finish.sh:101-102
  When an audit summary ends with blank or whitespace-only lines, this rejects a valid audit with exit 12. The gate and acceptance writer explicitly read the last nonblank line, and `test_audit_gates_on_the_concluding_line_of_the_last_message` already covers this valid output. Use the same verdict extraction rule so such audits can complete integration.

- [P2] Measure the trimmed disposition reason — scripts/orchestrator/chain-finish.sh:111-112
  For an incorrect audit, a reason containing 20 spaces, or a short reason padded to 20 characters, passes this check. The acceptance writer subsequently rejects it because the gate validates the stripped reason. Consequently, the chain can reply to and resolve GitHub threads before discovering this invalid input at the record step. Validate the trimmed reason before thread resolution; a correct verdict otherwise leaves the whitespace-only reason unchecked altogether.
Post-merge tool resolution can cross the intended trust boundary, and audit parsing disagrees with existing gate validation. Syntax checks passed; filesystem-writing unit tests were not run in the read-only environment.

Full review comments:

- [P1] Pin the cost script's tools before fast-forwarding — scripts/orchestrator/chain-finish.sh:147-148
  With the normal mise-shim PATH, a PR changing tool configuration can affect this post-merge call. The saved `pr-cost.sh` invokes bare `git`, `gh`, `jq`, and `date` from the newly fast-forwarded checkout, allowing PR-controlled configuration to select executables under the orchestrator's credentials. Snapshotting the script does not pin those dependencies. Supply a safe PATH resolved before fast-forwarding, as `orch-gate.sh` does; the threat table's environment-input mitigation otherwise remains ineffective ([AGENTS.md:78](AGENTS.md#L78)).

- [P2] Read the last nonblank audit verdict line — scripts/orchestrator/chain-finish.sh:101-102
  When an audit summary ends with blank or whitespace-only lines, this rejects a valid audit with exit 12. The gate and acceptance writer explicitly read the last nonblank line, and `test_audit_gates_on_the_concluding_line_of_the_last_message` already covers this valid output. Use the same verdict extraction rule so such audits can complete integration.

- [P2] Measure the trimmed disposition reason — scripts/orchestrator/chain-finish.sh:111-112
  For an incorrect audit, a reason containing 20 spaces, or a short reason padded to 20 characters, passes this check. The acceptance writer subsequently rejects it because the gate validates the stripped reason. Consequently, the chain can reply to and resolve GitHub threads before discovering this invalid input at the record step. Validate the trimmed reason before thread resolution; a correct verdict otherwise leaves the whitespace-only reason unchecked altogether.
```
