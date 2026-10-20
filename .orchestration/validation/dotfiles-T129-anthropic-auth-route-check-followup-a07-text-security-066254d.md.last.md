- [P1] High confidence [.orchestration/tasks/dotfiles-T129-anthropic-auth-route-check-followup-a07.md:106](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T129-anthropic-auth-route-check-followup-a07.md:106) — The omission decision authenticates a `.gitignore` pathname, not its contents: an uncommitted `~` rule in the tracked root `.gitignore` authorizes skipping an untracked credential-bearing file because Git reads working-tree patterns; every specified metadata check still passes, without a race or inherited `GIT_*` override. Bind exclusion rules to independently verified bytes or inspect omitted files. ([Git documentation](https://git-scm.com/docs/gitignore#_description))

All allowed-file entries, listed non-path controls, orchestrator effects and §5.14 items 1–10 have rows; none claims `closed`. Executable identity, shared caches, later consumption and hostile same-UID processes are explicitly residual. The Codex-only task prohibits an out-of-sandbox Linux `gh` fallback. Those limitations do not resolve the new exclusion-authority gap above.

📝 まとめ: Read-only design review completed with one P1 for orchestrator disposition; no files changed.
Not run: implementation tests, live CI or deployment checks. The exclusion bypass remains a design finding.

Verdict: incorrect