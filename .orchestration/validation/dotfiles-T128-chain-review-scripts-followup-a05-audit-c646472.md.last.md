[P2] high evidence .orchestration/dotfiles-T128-chain-review-scripts-followup-a05/sandbox.md:18 The sandbox ledger lists planned `gh` commands with placeholders and conditional execution, rather than completed calls. The report still describes stopping before PR creation, while acceptance records say the orchestrator created PR #402. Record the actual calls and actors so permission-gated activity can be reconciled.

[P2] high orchestration .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a05-pr-feedback.json:141 The CodeRabbit “review skipped” status is dispositioned as a failed `regime` annotation, citing an unrelated run. This disposition does not explain its item; replace it with the actual skipped-review rationale and matching evidence.

Implementation assessment: the prefix fix is correct. ShellCheck and 28 read-only filename probes passed; [PR #402’s CI](https://github.com/mryfmo/dotfiles/pull/402) confirms all 18 chain-review tests passed. The task-copy hash matches dispatch.

Task invariants: no `INV-n` entries are declared in the task. Its explicit caps hold: 4/200 script lines and 23/1000 test additions.

Orchestration findings: 1

Not rerun: the full local suite. Nothing modified; the evidence discrepancies remain unresolved.
Verdict: incorrect