# Report: dotfiles-T128-settings-hook-dedupe-followup-a01

- **Seat and branch.** `claude-standard-dot-a003` in `.claude/worktrees/worker-c`, on the fresh branch `tools/settings-hook-dedupe-followup`, cut with `--no-track` from `origin/main` at `5fd4fe0c`. The earlier branches are left as they are.
- **Task copy.** Byte-identical to the dispatched main-checkout file, sha256 `23b1cef3…`, the TASK's `task_sha256` (validation).
- **Commits.** `9659ac97`: the change, its test and the task copy; then this evidence.
- **Routing note.** `home/dot_claude/modify_private_settings.json` renders Claude Code's settings, so this is a Claude-boundary source edited from a Claude seat. The orchestrator routed it here after pair review; the edit changes the source tree only, not the seat's running settings.
- cost: n/a (the runtime exposes no token or cost figures to the seat).

## The owned row: `audit:ca892e4:1`

- **The defect.** `is_managed_post_tool_use_hook` split the command with `shlex` before comparing it with the two renderings of the managed path (`~/.claude/hooks/<name>` and the absolute home path). `'~/.claude/hooks/format-edited-files.py'` and `\~/.claude/hooks/format-edited-files.py` name a path under a literal `~` directory in a shell, but `shlex` unquoted them to the managed path, so the entry was deleted.
- **The fix.** The predicate compares the whole command, stripped of surrounding whitespace only, with the two renderings; `shlex` is no longer used there (the permission and SessionStart predicates still use it). It still recognises exactly the two renderings of the managed path.
- **The test.** `test_managed_post_tool_use_keeps_a_quoted_or_escaped_tilde_path`: the quoted and the escaped command are each kept as unmanaged, with the managed entry appended. The lineage's cases are unchanged. With `origin/main`'s predicate both cases fail.
- **Checks.** 21 tests pass; `make render-check` passes (validation).
- **Size.** 7 changed lines outside `tests/` and `.orchestration/` (of 200), 14 added under `tests/` (of 1000), 2 files.

## Bot and CI (main-checkout copy only)

- **CI.** All 13 checks pass on `3a952537`, the final head; `mergeStateStatus` is `BEHIND`, since `main` moved (validation §3).
- **The Bot.** Its code and security reviews of `3a952537` completed with no finding and a 👍 reaction: no thread, no fix round.
- **The memory add:**

```text
$ uv run --no-project .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content 'dotfiles-T128-settings-hook-dedupe-followup-a01 (PR #380, head 3a952537): is_managed_post_tool_use_hook in home/dot_claude/modify_private_settings.json compares the whole command string (stripped) with the two renderings of the managed path instead of shlex words, so a quoted or escaped ~ path (a literal ~ directory) is kept as unmanaged; closes audit:ca892e4:1; test test_managed_post_tool_use_keeps_a_quoted_or_escaped_tilde_path. Bot: code and security reviews clean, no thread. Routing note: a Claude-boundary source edited from a Claude seat, as the orchestrator routed it.'
1b968766-74ea-4323-a1a7-a6f4824ed4f4
rc=0
```
