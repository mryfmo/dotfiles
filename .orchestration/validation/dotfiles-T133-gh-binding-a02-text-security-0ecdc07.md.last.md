- [P1] High confidence `.orchestration/tasks/dotfiles-T133-gh-binding-a02.md:126` — The canonical measurements execute bare `git` and `shasum` without a measured executable namespace; line 130 confirms the trusted parent is undeployed, so substituted executables can forge main and the design digest before anchoring. “gh-free” does not establish executable provenance.

- [P1] High confidence `.orchestration/tasks/dotfiles-T133-gh-binding-a02.md:126` — The recorded clone/read commands lack constructed environments and explicit binding of subsequent reads to the private clone; inherited `GIT_CONFIG_*` can rewrite the fixed URL, while `GIT_DIR` or the current directory can select another repository. A network-free probe confirmed the URL rewrite; require sanitized, explicitly rooted commands throughout. [Git configuration](https://git-scm.com/docs/git-config#ENVIRONMENT)

📝 まとめ: Reviewed all 41 threat rows and cited review/acceptance history; two findings remain for orchestrator disposition. No files edited.

Not checked: future implementation, CI or live Linux/race behavior; same-UID replacement and credential separation remain acknowledged residual risks.
Verdict: incorrect