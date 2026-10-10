---
format: 2
task_id: dotfiles-T124-wave1b-redesign-profile-a01
kind: code
superseded_by: dotfiles-T126-w3-headless-design-review-a01
security: true
design_review:
  receipt: .orchestration/validation/dotfiles-T124-design-gate-and-reset-rule-a01-design-review-canonical.md
  design: .orchestration/tasks/dotfiles-T124-design-gate-and-reset-rule-a01.md
allowed_files:
  - home/dot_agents/agent-config.yaml
  - home/dot_config/claude/rules/model-selection.md
  - home/dot_agents/skills/agmsg-orchestration/SKILL.md
  - home/dot_local/bin/common/executable_herdr-agents
  - tests/unit/test_generate_agent_configs.py
  - tests/unit/test_herdr_agents.py
  - README.md
  - home/dot_config/claude/rules/pr-integration.md
  - AGENTS.md
invariants:
  INV-5: the reset rule counts from history and main-checkout files (two revises or repeated TASKs, two audits with P0-P2 specification or implementation findings named by audit= shas, four amendments, Bot P1 on two heads) and blocks the orchestrator's stop and the merge until a design reset record or an operator waiver exists; re-dispatch under a new id is a boundary violation
---

# AGMSG-TASK dotfiles-T124-wave1b-redesign-profile-a01 — T124 wave 1b: the `redesign` profile and the reset procedure text

Drafted 2026-10-10 by the orchestrator seat. Dispatched after wave 1 merges (SKILL overlap). Implements the manifest and prose parts of the redesign-seat addition (design file, "v4 addition"; addendum `…-design-review-addendum-redesign-seat.md` items 1 and 5).

1. `home/dot_agents/agent-config.yaml` `model_profiles.redesign`: `claude: { model: claude-fable-5-1, effort: xhigh }`; codex: `deep`'s codex model at `model_reasoning_effort: xhigh`. Run the renderer; `~/.agents/model-profiles.env` and the Codex profile config gain the `redesign` entries; `herdr-agents --add-worker … --profile redesign` must accept it (check the profile list the launcher validates against; if it is derived from the manifest nothing changes, otherwise add it). `tests/unit/test_generate_agent_configs.py` asserts the rendered entries.
2. `home/dot_config/claude/rules/model-selection.md`: add "A design redo after an INV-5 reset runs on a `redesign` profile seat (`herdr-agents --add-worker .claude/worktrees/redesign --kind claude --profile redesign`); the orchestrator's model and effort never change mid-session." Correct the cache sentence to "a mid-session model switch invalidates the prompt cache (an effort change keeps it on Fable 5.1)".
3. SKILL Orchestrator Playbook: the reset procedure once (the stop-gate reason, the reset record's fields, seating the redesign seat, the `kind: design` task, the design RESULT, INV-3's review of the new design, removing the seat); the rule cites it. README: one paragraph.
4. Absorbed from T122 (superseded by this wave): the Bot/CI root-cause rule in Worker Playbook step 15 and Orchestrator step 10 (every finding fixed at its root cause in the PR; `not-applicable` only for a factually wrong finding with the refuting command and output pasted; out of scope is a scope gap, never a disposition; the orchestrator verifies a proposed `not-applicable` by its own reproduction per named sub-case and alone replies on and resolves threads), the one-line pointer in `home/dot_config/claude/rules/pr-integration.md` and `AGENTS.md` "Agent Review Evidence", the boundary-commit lesson (an untracked `.orchestration` file leaves the main working tree between the boundary branch and the merge; never append to a file `git status` shows absent; pull right after the boundary merge), the T119 sandbox example in Worker Playbook step 4, and the documented push form in step 4 (`GIT_CONFIG_GLOBAL=/dev/null git -c credential.helper= -c 'credential.helper=!gh auth git-credential' push https://github.com/mryfmo/dotfiles <branch>`). `home/dot_config/claude/rules/pr-integration.md` and `AGENTS.md` join `allowed_files` for those sentences.
5. Validation: `make render-check`, `uv run --no-project --with pyyaml scripts/validate-agent-assets.py`, the two unit modules, `make unit-test`, prettier on the three prose files, `uv run --no-project scripts/validate-task.py` on this file, `invariant: INV-5 → …` lines (the prose parts only; the counting is wave 2b/3a).

Forbidden: anything else; the gate scripts; `make update`; thread resolution. Standing instruction on Bot/CI findings and the sandbox-conduct section of wave 1 apply verbatim.

## Repo / branch

`.claude/worktrees/worker-c` after wave 1 merged: `git fetch origin`; `git switch -c feat/redesign-profile --no-track origin/main`.

## Completion

PR to `main` (English title `feat(regime): add the redesign profile and the design-reset procedure`), CI green, Bot wait, artifacts, memory add, `AGMSG-RESULT v1 task_id=dotfiles-T124-wave1b-redesign-profile-a01` via `agmsg-dispatch … claude-deep-dot w4:p1`. max_turns=10.
