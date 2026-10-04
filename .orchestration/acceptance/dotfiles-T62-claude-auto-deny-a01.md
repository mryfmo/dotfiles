# Acceptance: dotfiles-T62-claude-auto-deny-a01

- **Decision:** ACCEPTED. PR #254 squash-merged to `main` as `c6b348ba` (head `de8b8b2e`, one commit on main 6de95167). Merged without `--delete-branch`; worker-e holds `chore/claude-auto-deny`.
- **Worker:** `codex-standard-dot-a007` (Codex seat in `.claude/worktrees/worker-e`, seated 2026-10-04 with `herdr-agents --add-worker --kind codex` after the Claude worker a007 was removed; re-seated once after its first pane disappeared). task_rev verified by the worker (stated in its PONG). Routed to a Codex seat because a Claude seat may not edit the source of its own permission policy (T88); the first Claude attempt (a006, 2026-10-03) was refused by the auto-mode classifier as Self-Modification.
- **Exemption declared:** acceptance and final integration; evidence sync (the worker's artifacts moved from its worktree to the main checkout; the Codex sandbox cannot write the main checkout); control-plane hygiene (worktree reset to 3371cc81 after an interrupted `git switch` left a byte-identical copy of main's content staged).
- **Plan reference:** Phase 1, dotfiles-T62 (principle 2: plan approval only; user-level `auto`).

## What was accepted (3 files, +19/−9)

- `claude.permissions.defaultMode: plan → auto` with the comment that it must be user-level (project settings do not honour `auto`; the Stop gate and the deny list are the boundaries).
- `gh release`, `npm publish`, `uv publish`, `terraform apply`, `kubectl apply` move from `ask` to `deny`; `Bash(git push:*)` leaves `ask` (the `main` ruleset is the guard); `ask: []` stays, generator unchanged.
- Rendered `claude-settings-managed.json` follows; generator tests assert the rendered policy.

## Orchestrator re-derivation

- Read the whole diff and the rendered template; `jq` on the rendered file in the worker's validation shows `auto`, `[]`, and the deny list with the five publish rules. render-check, 69 focused tests, full unit suite and asset validation pass (worker). CI green (12 checks), no Codex thread, thumbs-up at 10:50:51Z, mergeable CLEAN.
- Operator consequence: after `make update` in the canonical clone, every Claude seat starts in `auto` and the Yes/No prompts the operator has been answering (git push, unsandboxed gh) stop; the classifier decides, the deny list refuses publish-class commands, and the Stop gate is the completion boundary.

## Audit / Bot / sweep / gate

| scope | verdict |
|---|---|
| task-level, final head de8b8b2e | incorrect (2, evidence only) → dispositions below |

audit-finding: 1 the validation asserts full-suite success without captured output and rewrites the jq output → not-applicable:evidence-only finding with no code defect; the Codex sandbox truncated the suite transcript and the orchestrator re-derived the rendered policy from the diff and the rendered template; the worker is asked to paste the exit status and raw output as an artifact correction that does not move the head
audit-finding: 2 the validation omits the diff-stat, PR and head identification, checks, mergeability and Bot outcome → not-applicable:evidence-only finding; those facts are in the orchestrator's sweep JSON (12 checks pass at de8b8b2e), the GraphQL thread listing (none) and the reactions query (thumbs-up 10:50:51Z), and the worker adds them to its validation as an artifact correction

- Sweep (head de8b8b2e): 5 items, 0 failure/warning, all dispositioned. Gate at de8b8b2e with `AUDIT_EVIDENCE` and `AUDIT_DISPOSITIONS=<this record>`: exit 0, evidence copies removed.

## Follow-ups

- `make update` in the canonical clone (orchestrator, machine lifecycle) deploys `auto`; the Codex seat profile moves to gpt-6.1-sol/high in T96; T90 (account separation) is next on the Codex security profile.
- The Codex worker's first seat vanished after its linkage PONG (cause unobserved; the pane was gone when the TASK wake arrived); the SKILL's add-worker guidance should say to send the first TASK only after a second liveness PING.

## CompactionDB

- Worker decision `6edcac14-a57c-4af6-8719-3d907abff970`; cited.
