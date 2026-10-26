[P1] high .orchestration/tasks/dotfiles-T129-hcom-dispatch-bus-a02.md:122 Amendment 1 still executes hcom from the shared uv directory forbidden by design item 9: hashing before invocation leaves replacement between verification and execution possible, while the prescribed fixture replaces the file before verification; consume a verified, protected executable and test that handoff before marking this boundary closed.

[P2] high .orchestration/tasks/dotfiles-T129-hcom-dispatch-bus-a02.md:153 The Checks show owner-writable filesystem modes, not worker write denial or protection of the executable namespace, snapshots and cache; they do not supply the item 1/2/9 deployment measurements required before review/anchor.

[P2] high .orchestration/tasks/dotfiles-T129-hcom-dispatch-bus-a02.md:132 The generated command still loses the argument boundary around `sh -c`’s command string: replaying the printed `sh -c exec …` does not execute the recorded Git command, so separate exit statuses have not resolved the previous evidence-reproducibility finding.

The installed hcom currently matches the executable inside the pinned wheel; the first finding concerns the subsequent execution handoff.

📝 まとめ: Reviewed all 42 threat rows and cited acceptance/review context; three findings remain for orchestrator disposition. No files changed.

Not checked: implementation, CI or live Linux/race execution; same-UID isolation and credential separation remain declared residual risks.
Verdict: incorrect