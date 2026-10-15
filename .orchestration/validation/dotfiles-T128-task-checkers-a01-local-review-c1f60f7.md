---
task: dotfiles-T128-task-checkers-a01
head: c1f60f7358b84e28d74f19bb8b1506da6179ab77
pr: 352
base: 28eec93c9a78e6a56d1f5f60ded675f521edb96f
started: 2026-10-14T06:02:13Z
finished: 2026-10-14T06:03:25Z
findings: 3
engine: codex review --base main (profile review, read-only)
---

- [P1] Restrict ledger comments to the Codex bot — scripts/orchestrator/ledger-check.py:23-24
- [P1] Verify the default ledger checker before executing it — scripts/orchestrator/orch-audit.sh:52-54
- [P2] Probe the actual task-consistency checker path — scripts/orchestrator/task-consistency-check.py:115-118

```text
The new mandatory ledger check diverges from the merge gate and executes an unverified local checker, which can either block valid audits or undermine the gate. C9 also probes the wrong landed script path.

Full review comments:

- [P1] Restrict ledger comments to the Codex bot — scripts/orchestrator/ledger-check.py:23-24
  When another bot such as CodeRabbit leaves an inline review comment, `bot` is also true, so this adds its ID to the required ledger even though `require-crit-review.py::swept_finding_ids()` only counts comments whose author is `chatgpt-codex-connector[bot]`. The default audit then refuses a record that is complete according to the actual merge gate; compare `item.get("author")` to `BOT` here as the review-body branch already does.

- [P1] Verify the default ledger checker before executing it — scripts/orchestrator/orch-audit.sh:52-54
  With the default path, the tracked-file check is skipped, and unlike the validator this script is not checked against `HEAD`; therefore an untracked or locally modified `scripts/orchestrator/ledger-check.py` is executed as part of the audit gate and can falsely approve an incomplete ledger. This is trust-boundary code governing a required check, so the default checker should be required to be tracked and unchanged just like an explicit override and the validator.

- [P2] Probe the actual task-consistency checker path — scripts/orchestrator/task-consistency-check.py:115-118
  For a docs task quoting a phrase such as `task-consistency-check C4`, this rewrite probes `origin/main:scripts/task-consistency-check.py`, but the checker introduced by this patch lives at `scripts/orchestrator/task-consistency-check.py`. Consequently C9 always reports that such a rule names an unlanded check unless it includes an `once`/`until` escape, rejecting valid documentation after this checker lands.
The new mandatory ledger check diverges from the merge gate and executes an unverified local checker, which can either block valid audits or undermine the gate. C9 also probes the wrong landed script path.

Full review comments:

- [P1] Restrict ledger comments to the Codex bot — scripts/orchestrator/ledger-check.py:23-24
  When another bot such as CodeRabbit leaves an inline review comment, `bot` is also true, so this adds its ID to the required ledger even though `require-crit-review.py::swept_finding_ids()` only counts comments whose author is `chatgpt-codex-connector[bot]`. The default audit then refuses a record that is complete according to the actual merge gate; compare `item.get("author")` to `BOT` here as the review-body branch already does.

- [P1] Verify the default ledger checker before executing it — scripts/orchestrator/orch-audit.sh:52-54
  With the default path, the tracked-file check is skipped, and unlike the validator this script is not checked against `HEAD`; therefore an untracked or locally modified `scripts/orchestrator/ledger-check.py` is executed as part of the audit gate and can falsely approve an incomplete ledger. This is trust-boundary code governing a required check, so the default checker should be required to be tracked and unchanged just like an explicit override and the validator.

- [P2] Probe the actual task-consistency checker path — scripts/orchestrator/task-consistency-check.py:115-118
  For a docs task quoting a phrase such as `task-consistency-check C4`, this rewrite probes `origin/main:scripts/task-consistency-check.py`, but the checker introduced by this patch lives at `scripts/orchestrator/task-consistency-check.py`. Consequently C9 always reports that such a rule names an unlanded check unless it includes an `once`/`until` escape, rejecting valid documentation after this checker lands.
```
