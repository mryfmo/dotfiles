# Acceptance: dotfiles-T66-permgate-dead-lanes-a01

- **Decision:** ACCEPTED after one revise round. PR #240 squash-merged to `main` as `a5c30b6d` (final head `a31dcf868d06103564d9ff643dc928e20f8c62b2`; substantive commits 8ae3fdc9, a93fcb94, a31dcf86; base `523fda06`, update-branch merges onto `3a0816e6`, `40d9eb6c`, `57885db1`). Merged without `--delete-branch`; worker-d holds `chore/permgate-dead-lanes`.
- **Worker:** `claude-standard-dot-a006` (worker-d). task_rev `ee8185bc…` → `0b77e4e6…` (PONG decision 1) → `b7fa55fe…` (revise round 1); all matched. Parallel wave with T89/T73/T67 (a005) and T65 (a007).
- **Exemption declared:** acceptance and final integration; the orchestrator mutated no repository code.
- **Plan reference:** Phase 1, dotfiles-T66 (principles 1 and 9: permgate deterministic-only).

## What was accepted (9 files, +109/−1427)

- `executable_permgate` 788 → 252 lines: deny_patterns, then allow_patterns for non-Bash tools or a bounded single command; `hook_output` for both hook schemas; append-only 0600 decisions log; `PERMGATE_INNER` guard; fail-closed to the native prompt on invalid JSON, policy errors (schema_version 3 required, non-object rejected) and `decide` exceptions (incl. `AttributeError`). Shadow LLM classifier lane, cli lane, bench and their validation deleted.
- `permgate-policy.yaml`: schema_version 3; the unchanged 9 allow / 1 deny patterns; `providers`, `cli`, `enablement`, `categories`, `classifier_*`, `metrics` dropped (PONG decision 1(3): nothing read `metrics`).
- `validate-agent-assets.py`: `validate_permgate_policy` requires a JSON object with exactly `{schema_version, allow_patterns, deny_patterns}`, schema_version 3 and pattern entries as objects with string tool/regex. `lifecycle.bats`: the four classifier pins dropped (decision 1(1)). Docs: README, `model-selection.md`, `codex/AGENTS.md:55` (decision 1(2)) say deterministic-only; the stale "classifier model pinned in the security policy" sentence removed (a93fcb94).
- Tests: 17 permgate tests remain (golden bytes, undecided → empty stdout), plus the validator cases.

## Orchestrator re-derivation

- Probe of the head executable against the head policy: `gh pr view 1`, `git status` → allow (deterministic); `rm -rf /` → deny; `ls`, `gh pr merge 1` → empty stdout (fallthrough). Deterministic behaviour unchanged.
- Deploy note: until `chezmoi apply` delivers both files, the new executable logs `config-error` on the schema-2 live policy and falls through (fails closed).

## Audit / Bot / sweep / gate

| commit | verdict |
|---|---|
| 8ae3fdc9, a93fcb94, a31dcf86 | correct |

- Codex Bot: no finding on 8ae3fdc9; three P2s on the update-branch heads (stale classifier sentence; validator accepting a non-object policy; null pattern entry → unhandled AttributeError) all fixed in-PR (a93fcb94, a31dcf86), replied and resolved; thumbs-up on a31dcf86. Sweep (head a31dcf86): 17 items, 0 failure/warning, all dispositioned. Gate at a31dcf86 exit 0 with evidence copies, copies removed.

## Procedure lesson (to T69)

- The Codex Bot reviews the `update-branch` merge heads too, so the acceptance order is: update-branch → CI → Bot review complete → sweep → gate → merge. A first merge attempt here was refused by the strict policy because T73 landed in between.

## CompactionDB

- Worker decision `151d0f98-0bd5-4d65-a43d-ebebcd3004ed`; cited.

## Operator follow-up

- `make update` deploys the executable and policy together; the live `decisions.jsonl` keeps its old shadow records (no action).
