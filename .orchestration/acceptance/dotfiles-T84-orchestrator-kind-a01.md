# Acceptance: dotfiles-T84-orchestrator-kind-a01

- **Decision:** ACCEPTED. PR #272 squash-merged to `main` as `51c57f19`; final head `26e748e2`. Gate passed at the head in the orchestrator-review worktree with the PR-feedback, audit (`correct`) and crit evidence (`BASE=origin/main … make require-crit-review` rc=0, 2026-10-05 02:19Z).
- **Worker:** `claude-standard-dot-a005` (worker-c, wT:p2). task_rev matched at dispatch.
- **Exemption declared:** acceptance and final integration.
- **Plan reference:** Phase 7, dotfiles-T84 (principle 4). Depends on T80 (merged); serialized after T82 on the manifest; T85 and T86 (merged) consume the rendered variable.

## What was accepted (PR #272, final head `26e748e28bb0314dea0a7a801afd18bcb120a357` after revise round 1; commits 25f5079f, 55f4d43f update-branch, 26e748e2; 7 files)

- `home/dot_agents/agent-config.yaml`: `orchestrator_kind: claude` with a comment mirroring `worker_kind`'s (`codex` hands the pair to `codex-orchestrate`; an explicit `HERDR_AGENTS_ORCHESTRATOR_KIND` still overrides).
- `scripts/generate-agent-configs.py`: `orchestrator_kind(manifest)` (default `claude`, validated against the kind set); `render_model_profiles_env` emits `HERDR_AGENTS_ORCHESTRATOR_KIND="claude"`; `home/dot_agents/model-profiles.env` regenerated.
- `scripts/validate-agent-assets.py`: rejects an invalid or missing `orchestrator_kind` (like `worker_kind`), requires the README `(currently \`<kind>\`;` statements anchored on their key names for both `orchestrator_kind` and `worker_kind` (26e748e2 closed the regression where the new orchestrator sentence satisfied the unanchored worker-kind check), and lists the env token.
- README: one sentence next to the `worker_kind` one.
- Tests: default, env line, invalid value, manifest rejection, README statement, worker-kind check ignores the orchestrator sentence; 854 unit tests; `make render-check` clean; `make validate-agent-assets` ok; ruff clean.

## Decisions taken during the task

- Worker decisions accepted: the validator treats a missing key as invalid (same as `worker_kind`), and the README check is anchored on the key name so wording elsewhere cannot satisfy it by accident.
- The worker ran `gh pr update-branch` after T86 merged; CI reran green. Revise round 1 (audit of 55f4d43f): anchored worker-kind check with regression test; the real `memory add` command and a `memory search` readback pasted in the validation file.

## Orchestrator re-derivation

- Read the full diff; the manifest key sits next to `worker_kind`; `herdr-agents` (T85) resolves the same variable with the same default, and `codex-orchestrate` (T86) requires `codex`, so the three agree.
- CI 13/13 green on 55f4d43f and 26e748e2; PR `clean`; no Bot review or thread on any head within the worker's windows (01:13:05Z–01:27:59Z; 01:57:16Z–02:12:12Z).

## Audit / Bot / sweep / gate

| scope | verdict |
|---|---|
| task-level, 55f4d43f (round-0 head) | incorrect (2) → the unanchored worker-kind README check (satisfied by the new orchestrator sentence) is anchored in revise round 1 with a regression test; the CompactionDB command evidence is pasted |
| task-level, final head 26e748e2 | correct (no findings) |

- Sweep (head 26e748e2): see the masked copy `.orchestration/validation/dotfiles-T84-orchestrator-kind-a01-pr-feedback.json`; every item `not-applicable` (no finding).
- Crit evidence `…-crit.json` (one resolved review-scope record), receipt `…-review-receipt.md`.

## Follow-ups

- T87 flips `orchestrator_kind` through the environment for the codex legs; the manifest stays `claude`.

## CompactionDB

- Worker decision `14be3cdb`; orchestrator consolidation `7c1110b0-e938-4bce-81f5-cdb8031baaa8`.
