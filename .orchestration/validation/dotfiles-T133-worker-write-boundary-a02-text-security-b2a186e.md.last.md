- [P1] High confidence `.orchestration/tasks/dotfiles-T133-worker-write-boundary-a02.md:427` — K01 inventories hook commands but omits non-command handlers: a pre-existing `type: "http"` hook has no command to reject, yet can POST tool inputs/results or interpolated credentials to an attacker-controlled URL after startup; command-payload fixtures cannot establish refusal of this path. Require handler-type validation, corresponding threat coverage and a command-free HTTP-hook fixture. [HTTP hook behavior](https://code.claude.com/docs/en/hooks#http-hook-fields).

- [P2] High confidence `.orchestration/tasks/dotfiles-T133-worker-write-boundary-a02.md:972` — The deferred ledger contract fixes repository paths but leaves the API host implicit: inherited `GH_HOST` can redirect both requests, so a valid-looking SHA and ledger need not originate from github.com’s canonical main. Bind both requests explicitly to `--hostname github.com` and test hostile host selection. [GitHub CLI environment selection](https://cli.github.com/manual/gh_help_environment).

All 22 allowed-file entries have threat rows; all 79 rows are residuals, with no closure claims. Explicitly transferred executable binding, same-UID races and shared capabilities were not re-reported.

📝 まとめ: Completed the read-only task, threat-table and cited-context review; findings remain for orchestrator disposition.

Not checked: implementation tests, CI or live enforcement. No files changed; the identified design gaps remain.
Verdict: incorrect