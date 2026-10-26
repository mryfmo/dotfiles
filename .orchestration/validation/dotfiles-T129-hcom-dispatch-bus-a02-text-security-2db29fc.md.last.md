[P2] high .orchestration/tasks/dotfiles-T129-hcom-dispatch-bus-a02.md:126 The claimed worker write-boundary measurements are absent from Checks: the generator puts those probes in its non-hcom branch; filesystem modes—and even allowWrite lists alone—cannot establish protection against Claude’s unsandboxed file tools, so the private executable and adjacent digest remain unproven until actual denial controls are measured.

[P2] high .orchestration/tasks/dotfiles-T129-hcom-dispatch-bus-a02.md:28 Setting only `UV_TOOL_DIR` leaves executable publication at `~/.local/bin`; the prescribed `uv tool install --force` therefore replaces the existing public hcom entry, an unmodelled effect the named private-install/drift test need not detect—bind `UV_TOOL_BIN_DIR` privately and assert the public entry remains unchanged. [uv documentation](https://docs.astral.sh/uv/reference/cli/#uv-tool-install)

📝 まとめ: Reviewed all 43 threat rows and referenced acceptance/review context; two findings remain for orchestrator disposition. No files changed.

Not checked: implementation, CI or live Linux/race execution; same-UID isolation and credential separation remain declared residual risks.
Verdict: incorrect