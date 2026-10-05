# Acceptance: dotfiles-T79-remove-adh-profile-a01

- **Decision:** ACCEPTED. PR #267 squash-merged to `main` as `62d0771f`; final head `123bf10476c85911e55eabc7f1795fa597f13195`. Gate passed at the head in the orchestrator-review worktree with the PR-feedback, audit (`incorrect`, one process disposition below) and crit evidence (`BASE=origin/main … make require-crit-review` rc=0, 2026-10-04 20:05Z).
- **Worker:** `claude-standard-dot-a006` (worker-d, wY:p2). task_rev matched at dispatch.
- **Exemption declared:** acceptance and final integration.
- **Plan reference:** Phase 4, dotfiles-T79 (operator decision: ADH leaves dotfiles). Depends on T78 (merged); serialized after T80 on the generator and validator.

## What was accepted (PR #267, diff head `c86eb99a`, final head `123bf10476c85911e55eabc7f1795fa597f13195`; 8 files, +13/−230)

- `home/dot_agents/agent-config.yaml`: the `adh` profile and its two comment lines are gone; no other profile changed.
- `scripts/generate-agent-configs.py` and `scripts/validate-agent-assets.py`: `ADH_PROFILE`, `validate_adh_profile` and their calls are gone; the profile-set check now requires exactly the six base profiles ("and no others"). `scripts/check-agent-runtime.py`: `ADH_PROFILE_BLOCK` and `manifest_policy_failures` are gone (the check starts from an empty failure list).
- `home/dot_codex/modify_private_adh.config.toml` deleted; `home/.chezmoiremove` gains `.codex/adh.config.toml`, so the deployed profile file disappears on the next apply.
- `home/dot_agents/model-profiles.env`: regenerated; the two `MODEL_PROFILE_ADH_*` lines are gone and the six other profiles are byte-identical.
- Tests: `test_agent_manifest_rejects_the_retired_adh_profile` added; 788 (diff head) / 790 (merged head) pass; `make render-check` clean; `make validate-agent-assets` ok; ruff clean.

## Decisions taken during the task

- No README edit: it names no `adh` profile (nothing for T83).
- The worker ran `gh pr update-branch` itself after T77b (#266) merged; CI reran green on the merged head.

## Orchestrator re-derivation

- Read the full diff; `git grep -i 'adh\b\|ADH' 123bf104 -- home scripts tests` returns only the `.chezmoiremove` entry and the new rejection test.
- CI 13/13 green on 123bf104; PR `clean`; no Bot review or thread on either head within the worker's window.

## Audit / Bot / sweep / gate

| scope | verdict |
|---|---|
| task-level, final head 123bf104 | incorrect (1) → disposition below |

audit-finding: 1 the worker ran `git fetch`, `git push` and `git merge --ff-only` outside its sandbox, and the Worker Playbook's exception does not list a local merge → not-applicable:process deviation recorded; the fast-forward only moved the worktree branch to the GitHub-made update-branch commit it had just fetched (no content was authored outside the sandbox), it ran through the permission gate like the fetch and push it accompanied, and the worker reported it in its sandbox record; the lesson (fetch and fast-forward belong inside the sandbox, which worked for a005 in T95) goes to T83 with the other Playbook step-4 wording

- Sweep (head 123bf104): see the masked copy `.orchestration/validation/dotfiles-T79-remove-adh-profile-a01-pr-feedback.json`; every item `not-applicable` (no finding).
- Crit evidence `…-crit.json` (one resolved review-scope record), receipt `…-review-receipt.md`.

## Live follow-up

- The next `make update` on each host removes `~/.codex/adh.config.toml` and the `MODEL_PROFILE_ADH_*` lines from `~/.agents/model-profiles.env`.

## CompactionDB

- Worker decision `bc88afea`; orchestrator consolidation `dd7fe9a9-15e9-4a0b-bc16-bd20718c2391`.
