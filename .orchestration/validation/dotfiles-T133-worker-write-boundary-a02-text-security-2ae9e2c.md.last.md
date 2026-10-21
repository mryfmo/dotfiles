[P1] High confidence `.orchestration/tasks/dotfiles-T133-worker-write-boundary-a02.md:481` — Startup screening covers only four settings files, leaving executable MCP configuration in `<worktree>/.mcp.json` unchecked: existing settings can retain `enableAllProjectMcpServers: true`, and after workspace trust is accepted Claude can execute the unchecked server command; denying subsequent writes does not validate existing content. Item 11 inventories MCP fields but requires checking them only in the covered settings files, so its fixtures and threat row miss the actual execution source. Require screening or disabling that source before launch, with a pre-existing malicious-server fixture. [MCP loading and approval rules](https://code.claude.com/docs/en/mcp#project-server-approvals-and-workspace-trust).

All allowed-file entries have threat rows; none claims `closed`. I treated explicitly transferred executable-binding work, same-UID races, shared capabilities and ledger consumption as disclosed residuals.

📝 まとめ: タスク本文・threat_table・参照された受け入れ記録とレビューを確認し、起動前検査の対象漏れを P1 として報告しました。判断は orchestrator に委ねます。

Not checked: implementation tests, CI or live enforcement; no files changed. Unscreened MCP execution remains a design risk.
Verdict: incorrect