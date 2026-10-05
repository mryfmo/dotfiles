# Report: dotfiles-T80-codex-command-hooks-a01

- **Worker and branch:** `claude-standard-dot-a005` in worker-c, branch `feat/codex-command-hooks` from `origin/main` 4c38dea0 with `--no-track`. Earlier branches are untouched.
- **task_rev:** `sha256:98072a9c…00af7`, matched in the main checkout.
- **PR:** #264, https://github.com/mryfmo/dotfiles/pull/264.
- **Commits:**
  - `b07ec485`: the change.
  - `9c2f82e5`: Codex P2 4178802802.
  - `b24ce965`: Codex P2 4178832150.
  - `8a4cf128`: `gh pr update-branch`, merging main b13132d0 (#265). The bot wait covered the diff head `b24ce965`; CI was re-run on this merge head.
- **Final head:** `8a4cf128`. CI, branch and bot state are in the validation file.
- **Status:** ready_for_review.

## 1. What changed

- **Generator:**
  - `codex_command_hook_lines(event, hook)` renders one `[[hooks.<Event>]]` matcher group: `matcher = "*"`, then `[[hooks.<Event>.hooks]]` with `type = "command"`, `command`, `timeout` and `statusMessage`, via `quote_toml` and `quote_toml_key`.
  - The PermissionRequest block now uses the same emitter, and `make render-check` stays clean (byte-identical).
  - Each `codex.hooks.command_hooks` entry renders in manifest order, after PermissionRequest and before `[hooks.state]`; same-event entries each get their own table.
- **Validator:** `validate_codex_command_hooks`, called from `validate_codex_config`, checks that:
  - `command_hooks`, when present, is a list (missing means none);
  - each entry is a mapping with `event` in `CODEX_HOOK_EVENTS`, a non-empty string `command`, a positive integer `timeout` (bool rejected) and a string `status_message`;
  - `SessionEnd` and `Interrupt` have a `timeout` of at most 3 seconds, per the Codex hooks reference (verified; see the validation file).
  - Instead of a bare count, it compares the parsed template's hook tables (everything except `state`) with the exact tables the manifest declares. A stray hand-edited table, a changed field, or an undeclared event table fails, and the message names rendered against declared counts.
- **Event list (VERIFY):**
  - **Source:** the `HooksToml` properties of the official Codex config schema, https://developers.openai.com/codex/config-schema.json (sha256 `7ce31bde…b023` at fetch time). The schema lists Interrupt, PermissionRequest, PostCompact, PostToolUse, PreCompact, PreToolUse, SessionEnd, SessionStart, Stop, SubagentStart, SubagentStop and UserPromptSubmit, plus `state`.
  - **Dropped:** `Notification`, which is in the task's list but not in the reference.
  - **Added, a recorded decision:** `Interrupt` and `SubagentStart`, which the reference has but the task's list lacks. Leaving them out would reject valid Codex events, which is the opposite of validating against the reference.
- **Tests (generator):**
  - `test_codex_command_hooks_render_after_permission_request_in_manifest_order`: exact TOML for PreCompact, PostCompact and SessionEnd, the ordering, and that the result parses;
  - `test_empty_or_missing_codex_command_hooks_render_no_table`: identical to the baseline.
- **Tests (validator):**
  - `test_codex_command_hooks_accept_the_declared_tables`;
  - `test_codex_command_hooks_reject_bad_entries_and_stray_tables`: unknown event (`Notification`), empty command, string and boolean timeouts, a stray extra table, an undeclared rendered table, and `{}`, `false` or `null` instead of a list, and SessionEnd over 3 seconds.
  - The new tests fail against `origin/main` (1 failure, 11 errors), against `b07ec485` (4 failures) and against `9c2f82e5` (1 failure, the 3-second cap).
  - `make unit-test` passes with 782 tests.
- **Untouched:** `agent-config.yaml`, `codex-config-managed.toml` (byte-identical, render-check clean), Claude-side rendering, `permission_request` behaviour, and permgate.

## 2. Codex bot

| Head | Result |
|---|---|
| `b07ec485` | Review at 18:30:04Z with P2 4178802802, "Reject falsey non-list command_hooks values": `fixed:9c2f82e5`. Only a missing key defaults to no hooks, and `{}`, `false` or `null` fail. |
| `9c2f82e5` | Review at 18:39:43Z with P2 4178832150, "Cap SessionEnd and Interrupt hook timeouts at 3 seconds": `fixed:b24ce965`. The cap was verified against developers.openai.com/codex/hooks before the fix. |
| `b24ce965` (final) | `bot: none`. There was no review or finding of this head within 15 minutes after CI: the loop started after `gh pr checks --watch` finished and ended at 19:11:52Z (SKILL step 15). |

I did not reply to or resolve any thread.

## CompactionDB

```
$ cd /home/moriya/Workspace/dotfiles && python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content 'dotfiles-T80 (operator 2026-10-03): the Codex renderer emits generic `[[hooks.<Event>]]` command hooks from `codex.hooks.command_hooks` in the manifest, validated against the official Codex hook event list, so lifecycle hooks (PreCompact/PostCompact/SessionEnd for CompactionDB) are declared in the manifest, never hand-written into the rendered TOML.'
9db1c3e0-3d2e-4b62-8633-05ddd6f8d5d2
[exit 0]
```

[memory:decision] dotfiles-T80 (operator 2026-10-03): the Codex renderer emits generic `[[hooks.<Event>]]` command hooks from `codex.hooks.command_hooks` in the manifest, validated against the official Codex hook event list, so lifecycle hooks (PreCompact/PostCompact/SessionEnd for CompactionDB) are declared in the manifest, never hand-written into the rendered TOML.

## Artifacts

- validation: `.orchestration/validation/dotfiles-T80-codex-command-hooks-a01.md`
- sandbox: `.orchestration/sandboxes/dotfiles-T80-codex-command-hooks-a01.md`
- learning: `.orchestration/learning/dotfiles-T80-codex-command-hooks-a01.md`
- autoskill: `.orchestration/autoskill/runs/dotfiles-T80-codex-command-hooks-a01.md`

cost: n/a (no subagents, no model-driven runs; the runtime does not expose session totals).
