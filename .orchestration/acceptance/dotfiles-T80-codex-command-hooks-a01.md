# Acceptance: dotfiles-T80-codex-command-hooks-a01

- **Decision:** ACCEPTED. PR #264 squash-merged to `main` as `36ffe6ca`; final head `8a4cf1285cfca453bdfcf3a4602301140cc9d9da`. Gate passed at the head in the orchestrator-review worktree with the PR-feedback, audit (`incorrect`, three dispositions below) and crit evidence (`BASE=origin/main … make require-crit-review` rc=0, 2026-10-04 19:32Z).
- **Worker:** `claude-standard-dot-a005` (worker-c, wT:p2). task_rev matched at dispatch.
- **Exemption declared:** acceptance and final integration.
- **Plan reference:** Phase 5, dotfiles-T80 (principle 7). Depends on T71 (merged); serialized after T90 on the generator.

## What was accepted (PR #264, final head `8a4cf1285cfca453bdfcf3a4602301140cc9d9da`; commits b07ec485, 9c2f82e5, b24ce965, 8a4cf128 update-branch onto b13132d0; 4 files, +232/−15)

- `scripts/generate-agent-configs.py`: `codex_command_hook_lines(event, hook)` renders one `[[hooks.<Event>]]` / `[[hooks.<Event>.hooks]]` group; PermissionRequest now uses it, and every `codex.hooks.command_hooks` entry follows in manifest order before `[hooks.state]`.
- `scripts/validate-agent-assets.py`: `CODEX_HOOK_EVENTS` from the official Codex config schema's `HooksToml` properties (Interrupt, PermissionRequest, PostCompact, PostToolUse, PreCompact, PreToolUse, SessionEnd, SessionStart, Stop, SubagentStart, SubagentStop, UserPromptSubmit); `validate_codex_command_hooks` rejects a non-list `command_hooks`, a non-mapping entry, an unknown event, an empty command, a non-positive or non-integer timeout, a `SessionEnd`/`Interrupt` timeout above 3 seconds, a non-string status message, and any mismatch between the rendered hook tables and the declared ones.
- Tests: exact TOML and ordering for PreCompact/PostCompact/SessionEnd, empty/missing `command_hooks`, eight reject cases, stray and undeclared tables; 787 pass; `make render-check` clean (no `command_hooks` declared yet, so the rendered template is unchanged).

## Decisions taken during the task

- Event list against the reference, not the task text: `Notification` dropped (absent from the schema); `Interrupt` and `SubagentStart` added (present). Accepted: the task said to validate against the official reference.
- Codex P2 4178802802 (falsey non-list `command_hooks` coerced to empty) → fixed in 9c2f82e5; Codex P2 4178832150 (`SessionEnd`/`Interrupt` timeouts above 3 seconds) → fixed in b24ce965; both replied and resolved by the orchestrator after confirming the fix commits are ancestors of the head.
- Consequence for T82: its `SessionEnd` hook must declare `timeout: 3` or less (the plan said 10), and the SessionEnd handler must not run `prune` (T81 already keeps pruning on the explicit CLI path).

## Orchestrator re-derivation

- Read the full diff; the emitter is the same text PermissionRequest produced before (render-check clean proves it); the validator's table comparison excludes only `state`; the 3-second cap matches the Codex hooks reference cited in the validation file.
- CI 13/13 green on 8a4cf128; PR `clean` after the thread resolutions; no Bot review on the diff head b24ce965 within the worker's window.

## Audit / Bot / sweep / gate

| scope | verdict |
|---|---|
| task-level, final head 8a4cf128 | incorrect (3) → dispositions below |

audit-finding: 1 the validator's table comparison uses dictionary equality, so a hand-edited rendered `timeout = true` or `1.0` would equal the declared integer `1` → not-applicable:the rendered template is generator output and `make render-check` regenerates it byte-for-byte on every validation run and in CI, so any hand edit (type-coerced or not) already fails before this comparison runs; the table comparison is a second guard whose remaining gap cannot be reached without failing render-check, and the generator only ever emits the manifest's integer
audit-finding: 2 the worker fetched the Codex config schema outside its sandbox, which Worker Playbook step 4 does not list among the permitted exceptions → not-applicable:the task's VERIFY item required reading the official reference and the Claude sandbox allows only GitHub domains; the fetch went through the permission gate (auto-mode classifier), read a public document and wrote nothing; recorded as a process deviation, with the lesson for T83 that reference lookups should use the WebFetch tool rather than sandboxed Bash so no exception is needed
audit-finding: 3 the report says 782 passing unit tests while the final-head validation records 787 with one skipped → not-applicable:evidence-presentation discrepancy; the report's figure predates the two Bot-fix commits that added tests, the validation file (787, 1 skipped) is the authoritative final-head record and CI confirms it; no product file is affected

- Sweep (head 8a4cf128): see the masked copy `.orchestration/validation/dotfiles-T80-codex-command-hooks-a01-pr-feedback.json`; two `fixed:` items, the rest `not-applicable`.
- Crit evidence `…-crit.json` (one resolved review-scope record), receipt `…-review-receipt.md`.

## Follow-ups

- T83 (SKILL Worker Playbook): reference lookups for VERIFY items use the WebFetch tool, not Bash `curl`, so no out-of-sandbox exception is needed.

- T82 (after T81): declare the PreCompact/PostCompact/SessionEnd hooks in the manifest with `timeout: 3` for SessionEnd.
- T84 (`orchestrator_kind`) is unblocked on the generator once this merges; T79 and T81 queue behind it on the validator.

## CompactionDB

- Worker decision `9db1c3e0-3d2e-4b62-8633-05ddd6f8d5d2`; orchestrator consolidation `c5692da0-98eb-4c94-a5e7-7b8613d1cf01`.
