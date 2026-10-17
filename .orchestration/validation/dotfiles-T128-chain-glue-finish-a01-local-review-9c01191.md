---
task: dotfiles-T128-chain-glue-finish-a01
head: 9c011913e178432fa820e2c2da22cb74312832f1
pr: 378
base: 35ab0e95a7fe27c501db3478d4f37e69a514d532
started: 2026-10-17T11:18:10Z
finished: 2026-10-17T11:23:45Z
findings: 2
engine: codex review --base main (profile review, read-only)
---

- [P1] Pin launcher and cleanup commands before fast-forwarding — scripts/orchestrator/chain-finish.sh:114-114
- [P2] Verify that the merged PR still has the audited head — scripts/orchestrator/chain-finish.sh:166-167

```text
The post-merge tail can execute PR-controlled commands, and the merge wait can accept a different head from the audited one. Syntax checks passed; filesystem-writing tests were not run in the read-only sandbox.

Full review comments:

- [P1] Pin launcher and cleanup commands before fast-forwarding — scripts/orchestrator/chain-finish.sh:114-114
  If PATH contains `.` or the checkout directory, a PR can add an executable `env` that becomes visible after the fast-forward. This function resolves bare `env` through the inherited PATH before the restricted PATH takes effect, executing PR-controlled code with orchestrator credentials. The EXIT trap has the same problem with `rm`. Resolve these commands before merging or use trusted absolute paths; the current implementation defeats the threat table's environment-input control ([AGENTS.md:78](AGENTS.md#L78)).

- [P2] Verify that the merged PR still has the audited head — scripts/orchestrator/chain-finish.sh:166-167
  If a queued PR is updated and subsequently re-queued or merged by another actor during this wait, any `MERGED` response is accepted without checking its head. `--match-head-commit` protected the earlier enqueue request, not that subsequent merge. The chain therefore fast-forwards, records cost, and prints acceptance for the old audited head even though another head landed. Request and compare `headRefOid` before finalization to preserve the threat table's audited-head invariant ([AGENTS.md:78](AGENTS.md#L78)).
The post-merge tail can execute PR-controlled commands, and the merge wait can accept a different head from the audited one. Syntax checks passed; filesystem-writing tests were not run in the read-only sandbox.

Full review comments:

- [P1] Pin launcher and cleanup commands before fast-forwarding — scripts/orchestrator/chain-finish.sh:114-114
  If PATH contains `.` or the checkout directory, a PR can add an executable `env` that becomes visible after the fast-forward. This function resolves bare `env` through the inherited PATH before the restricted PATH takes effect, executing PR-controlled code with orchestrator credentials. The EXIT trap has the same problem with `rm`. Resolve these commands before merging or use trusted absolute paths; the current implementation defeats the threat table's environment-input control ([AGENTS.md:78](AGENTS.md#L78)).

- [P2] Verify that the merged PR still has the audited head — scripts/orchestrator/chain-finish.sh:166-167
  If a queued PR is updated and subsequently re-queued or merged by another actor during this wait, any `MERGED` response is accepted without checking its head. `--match-head-commit` protected the earlier enqueue request, not that subsequent merge. The chain therefore fast-forwards, records cost, and prints acceptance for the old audited head even though another head landed. Request and compare `headRefOid` before finalization to preserve the threat table's audited-head invariant ([AGENTS.md:78](AGENTS.md#L78)).
```
