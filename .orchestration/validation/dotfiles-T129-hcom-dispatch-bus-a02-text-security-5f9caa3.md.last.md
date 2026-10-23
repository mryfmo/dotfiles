[P2] high .orchestration/tasks/dotfiles-T129-hcom-dispatch-bus-a02.md:118 The selected hcom Checks generator omits the required executable provenance and item 1/2/9 protection measurements; `hcom --version` does not establish them, and this host’s `~/.local/bin/hcom` resolves into `~/.local/share/uv/tools/`, which item 9 excludes—resolve that deployment conflict and supply the measurements before anchoring.

[P2] high .orchestration/tasks/dotfiles-T129-hcom-dispatch-bus-a02.md:129 The design-digest pipeline reports only the final `shasum` status, so a failed `git show` can produce an empty-input digest with exit 0; the printed command also loses the quoting around `sh -c`’s argument, preventing faithful replay—preserve argument boundaries and record both stages’ statuses.

📝 まとめ: Reviewed all 42 threat rows and cited acceptance/review context; two evidence-binding findings remain for orchestrator disposition. No files changed.

Not checked: future implementation, CI or live Linux/race execution; same-UID isolation and credential separation remain declared residual risks.
Verdict: incorrect