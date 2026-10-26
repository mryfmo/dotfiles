[P2] High confidence [.orchestration/tasks/dotfiles-T133-worker-write-boundary-slice1-a01.md:143](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-worker-write-boundary-slice1-a01.md:143) — Switching tracked hooks alongside a rendered `.tmpl` does not install their target: `~/.claude/hooks/orchestrator-only.sh` is absent on this host, while line 187 prohibits application; sessions loading these settings therefore lose the stop gate, and `onFailure: block` cannot protect `Stop`—require guard provisioning before activating tracked references. [Hook failure semantics](https://code.claude.com/docs/en/hooks#block-the-action-when-a-hook-fails)

Checked all 37 threat rows and cited acceptance/review context. All eight allowed paths and required non-path controls have rows; none claims `closed`. Explicitly retained shim, same-user, Git-environment, alias, ledger and descendant-binding risks were not re-reported as new findings.

📝 まとめ: Completed the read-only design review; one P2 finding is submitted for orchestrator disposition.

Not checked: implementation, tests, CI or live enforcement; no files changed. Deferred execution-binding risks remain.
Verdict: incorrect