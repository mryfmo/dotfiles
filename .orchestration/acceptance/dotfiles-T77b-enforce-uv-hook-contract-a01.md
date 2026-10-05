# Acceptance: dotfiles-T77b-enforce-uv-hook-contract-a01

- **Decision:** ACCEPTED. PR #266 squash-merged to `main` as `8ba3c8bc`; final head `43d45ff43d4f67781866aab3dc2fc8cd506dc7c2`. Gate passed at the head in the orchestrator-review worktree with the PR-feedback, audit (`incorrect`, one evidence disposition below) and crit evidence (`BASE=origin/main … make require-crit-review` rc=0, 2026-10-04 19:43Z).
- **Worker:** `codex-security-dot-a007` (worker-e, wT:p8). task_rev verified at dispatch and after the PONG-decision append.
- **Exemption declared:** acceptance and final integration; evidence sync (seven worker artifacts copied from worker-e); the orchestrator's own `gh pr update-branch 266` onto `main` 36ffe6ca after the T80 merge.
- **Plan reference:** item 5 of Phase 4 dotfiles-T77, routed to a Codex seat because the file is a Claude PreToolUse hook (seat-capability rule).

## What was accepted (PR #266, diff head `908ba61a7d3d0222a6003c55fe5d9e944ede6c5c`, final head `43d45ff43d4f67781866aab3dc2fc8cd506dc7c2`; 2 files, +142/−88)

- VERIFY: the official hooks reference (code.claude.com/docs/en/hooks, PreToolUse decision control, read 2026-10-05) deprecates the top-level `decision`/`reason` form for PreToolUse and maps approve/block to allow/deny; the conversion branch applied.
- `home/dot_claude/hooks/executable_enforce-uv.sh`: a `deny_command` helper encodes the existing multiline guidance with `jq -Rsc` into `hookSpecificOutput {hookEventName: PreToolUse, permissionDecision: deny, permissionDecisionReason}`; every block emission uses it; allowed input exits 0 with no output; detection logic unchanged; header names the contract and the reference. Authorized lint-only cleanups: split `local` declarations (SC2155), unused `file_path`/`current_dir` reads dropped (SC2034), redundant `python3*` case arm removed (SC2221/2222), two `sed` substitutions replaced by parameter expansion (SC2001).
- `tests/unit/test_enforce_uv.py` (new): every blocking branch emits the current deny JSON with exact reason parity; non-blocking input exits 0 silently. 785 unit tests pass; shellcheck and shfmt clean; `make validate-agent-assets` ok.

## Decisions taken during the task

- PONG 1: conversion confirmed against the official reference; the five named baseline shellcheck diagnostics may be cleaned behaviour-preservingly; a new direct test file is in scope (none existed).
- The orchestrator ran `gh pr update-branch 266` after merging T80 (PR #264), then audited the updated head; the diff is unchanged.

## Orchestrator re-derivation

- Read the hook diff in full: each former `cat <<- EOF { "decision": "block", "reason": "…" }` block became `deny_command <<- EOF …` with the same text; the heredoc tab-indentation style is preserved; no detector or parser changed; the old multiline-string JSON was in fact invalid JSON, so the conversion also fixes that latent defect.
- CI 13/13 green on 908ba61a; no Bot review within the worker's 15-minute window; no threads.

## Audit / Bot / sweep / gate

| scope | verdict |
|---|---|
| task-level, final head 43d45ff4 | incorrect (1) → disposition below |

audit-finding: 1 the validation evidence and the feedback sweep covered the diff head 908ba61a, not the audited update-branch head 43d45ff4; the sweep JSON was absent at audit time → not-applicable:orchestrator evidence sequencing; the update-branch merge carries no diff, CI on 43d45ff4 finished 13/13 SUCCESS at 19:40Z after the audit started, and the sweep was then taken on 43d45ff4 (masked copy in the validation dir; no threads, no Bot review); the worker's report legitimately ends at the diff head it produced

- CI on the final head 43d45ff4: 13/13 SUCCESS at 19:40Z; PR `clean`.
- Sweep (head 43d45ff4): see the masked copy `.orchestration/validation/dotfiles-T77b-enforce-uv-hook-contract-a01-pr-feedback.json`.
- Crit evidence `…-crit.json` (one resolved review-scope record), receipt `…-review-receipt.md`; worker `…-worker-crit.json` / `…-worker-review-receipt.md` kept.

## Live follow-up

- The next `make update` on each host deploys the converted hook into `~/.claude/hooks/`.

## CompactionDB

- Orchestrator consolidation `434cbadb-0897-4763-b062-316db8da9b17` (the Codex seat cannot write the main-checkout DB).

## Post-deploy observation (orchestrator host, 2026-10-04 23:10Z)

- After `make update` deployed the converted hook, the orchestrator's own `python3 - <<EOF` and `python3 .claude/hooks/contextdb_cli.py health` were denied with the uv guidance; the legacy hook had been silently ignored by Claude Code, so this is the first time the policy bites. `uv run .claude/hooks/contextdb_cli.py …` works. User-visible impact: every Claude seat (orchestrator and workers) must call Python through `uv run`; CLAUDE.md's `python3 .claude/hooks/contextdb_cli.py` examples and the task-file completion steps need the same wording (T83 docs; workers adapt per the hook's message meanwhile).
