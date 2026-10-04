# Acceptance: dotfiles-T78-dead-docs-adh-a01

- **Decision:** ACCEPTED. PR #261 squash-merged to `main` as `feab6452`; head `8d536a3860044eee629da063ca1ce08eae050c31`. Gate passed at the head in the orchestrator-review worktree with the PR-feedback, audit (`correct`) and crit evidence (`BASE=origin/main … make require-crit-review` rc=0, 2026-10-04 17:14Z).
- **Worker:** `claude-standard-dot-a006` (worker-d, wY:p2). task_rev matched at dispatch and after the PONG-decision append.
- **Exemption declared:** acceptance and final integration.
- **Plan reference:** Phase 4, dotfiles-T78 (principle 9; operator decision that ADH leaves dotfiles). Depends on T88 (merged); serialized after T69 and T97 on SKILL.md.

## What was accepted (PR #261, head `8d536a3860044eee629da063ca1ce08eae050c31`; one commit on `main` 6534df0f; 209 files, +16/−114242)

- `AGENTS.md`: the ADH section is gone; nothing else changed. `reviews/ADH_Integrated_Plan/**` (198 files) deleted; `reviews/` is empty, so the `.coderabbit.yaml` `!reviews/**` exclusion and the `.prettierignore` `reviews/` line are dropped (PONG 1).
- `home/dot_agents/skills/agmsg-orchestration/SKILL.md`: Hermes description clause, the "adopts only the Hermes Skill Subset ideas" bullet, the "Do not install Hermes Agents runtime" bullet and the `learn_index.md` maintenance obligation removed; the learn-file content rule (`Date`, `Learnings`, `Plan Updates`) stays. `home/dot_config/codex/AGENTS.md`: the whole "セッション開始時の learn 確認" section removed as the minimal coherent unit (PONG 2).
- `.github/copilot-instructions.md` deleted. `home/dot_claude/commands/commit.md` (103 lines of duplicated Conventional Commit rules) and `plans/README.md` now point at `home/dot_agents/skills/gh-first-workflow/references/gh-git-rules.md`.
- `docs/plans/nix-first-architecture.md`, `docs/plans/nix-migration.md`, `plans/004-harden-and-lock-the-supply-chain.md`: one dated note each that the flake left in #247; bodies untouched (T83 decides their fate).

## Decisions taken during the task

- PONG 1: `.prettierignore` allowed for the one dead line. PONG 2: delete the whole learn section rather than one dangling bullet.
- Codex P2 4178539979 ("retain Copilot instructions"): not applicable; the deletion is task item 4 by operator decision, Copilot is not part of this harness and nothing in the repository reads the file; `AGENTS.md` is the canonical instruction file. Replied and resolved by the orchestrator.

## Orchestrator re-derivation

- At the head: `grep -ci 'Hermes\|learn_index\|ADH'` is 0 in `AGENTS.md`, the SKILL and the Codex AGENTS.md; no `reviews/` or `copilot-instructions` path remains in the tree; both pointer files name `gh-git-rules.md`; the three dated notes are present. The SKILL diff touches no Playbook step, so T90's step-10 edit (in flight) does not overlap.
- CI 13/13 green on 8d536a38; PR `clean` after the thread resolution.

## Audit / Bot / sweep / gate

| scope | verdict |
|---|---|
| task-level, head 8d536a38 | correct (no actionable findings) |

- Sweep (head 8d536a38): see the masked copy `.orchestration/validation/dotfiles-T78-dead-docs-adh-a01-pr-feedback.json`; every item `not-applicable`.
- Crit evidence `…-crit.json` (one resolved review-scope record), receipt `…-review-receipt.md`.

## Follow-ups

- T79 (adh model profile removal) is now unblocked.
- T83 owns the nix plan documents' fate and the remaining duplicated prose.

## CompactionDB

- Worker decision `86309afa`; orchestrator consolidation `61582424-6241-46ae-92e7-a5bab1aef5fa`.
