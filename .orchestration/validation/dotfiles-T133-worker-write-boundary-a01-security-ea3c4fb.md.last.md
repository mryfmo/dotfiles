Found one security issue in [PR #431](https://github.com/mryfmo/dotfiles/pull/431), head `ea3c4fb84bbcf2419a17946fdd1ea68b2355102e`.

- **P1 · High confidence · `home/dot_local/bin/common/executable_herdr-agents:355`** — Startup validates only legacy local command hooks, allowing an existing worktree’s tracked settings to execute unguarded commands with operator authority.

An existing worktree can contain a PR-supplied `.claude/settings.json` with a `SessionStart` command such as `/bin/sh ./payload.sh`. Preparation never validates that file, and the launcher subsequently accepts the workspace-trust dialog. Claude loads shared settings from the worktree; their hooks run outside the Bash sandbox. Dedicated user settings and Edit denies prevent neither consumption nor execution of already-present hooks. [Settings loading](https://code.claude.com/docs/en/settings#where-claude-code-keeps-the-local-file-in-a-git-repository), [sandbox scope](https://code.claude.com/docs/en/sandboxing).

The same incomplete screening preserves executable legacy settings: a read-only probe confirmed that `--legacy` accepts and retains `apiKeyHelper`. The threat table covers guarded tracked hooks and legacy migration, but does not account for these alternate configuration entrypoints. This is separate from the deferred interpreter-binding and agmsg-sourcing risks.

Validate or exclude repository-controlled executable configuration before launch, and add a reused-worktree fixture containing an unguarded tracked hook.

Python and shell syntax checks, static policy assertions, and `git diff --check` passed. No files changed.

📝 まとめ: 指定 head のセキュリティレビューを完了し、起動時の設定検証に P1 を1件報告しました。受け入れ判断は orchestrator に委ねます。

Not checked: full tests, live enforcement, or CI; GitHub access failed. The startup execution risk remains unresolved.
Verdict: incorrect