[P2] high orchestration `.orchestration/tasks/dotfiles-T128-model-profiles-xhigh-a01.md:47` — The task still permits only the original seven files and four profile changes. Final head also changes `README.md` and `review.claude.effort`, contradicting `allowed_files` and the explicit restriction at lines 20–21. Amend the task to cover these intended fixes.

[P2] high orchestration `.orchestration/tasks/dotfiles-T128-model-profiles-xhigh-a01.md:22` — The grouped rendering row does not provide the required per-path threat coverage. The read-only task-consistency check exits 1 with seven C4 missing-path failures and five C7 missing-control failures. Add the individual path and control rows before acceptance.

INV-7: holds `home/dot_agents/agent-config.yaml:42` — Review and deep profiles have matching models and efforts for both runtimes.

Premise: holds `.orchestration/tasks/dotfiles-T128-model-profiles-xhigh-a01.md:31` — All stated previous values match the merge base; the recorded count of 5 reproduces.

Orchestration findings: 2

📝 まとめ: Audited `707ed3a`; all 43 generated outputs match, preserved profiles are unchanged, and [PR #370](https://github.com/mryfmo/dotfiles/pull/370) CI passed. No files modified; two task-record issues remain.

Not checked: live CLI activation or local Bats execution. The fixed README review thread remains unresolved on GitHub.
Verdict: incorrect