# T60: AGMSG RESULT `effects` clause (H6, docs only)

task_id: T60
repo: /Users/mryfmo/Workspace/dotfiles
team: dotfiles-conformance
worker: codex-deep-dot
plan: .orchestration/tasks/PLAN-harness-composability-integration.md (Phase 6)
analysis: .orchestration/analysis/harness-composability-research.md (H6)
depends: T57/T58 (accepted — the reverse-mapping the clause references)

[memory: decision — AGMSG RESULTs for tasks with persistent out-of-repo side effects declare them in an optional effects field, and the report states each effect's reverse mapping (installed-manifest step, removal procedure, or explicitly irreversible); the orchestrator verifies this at acceptance.]

## Goal

Make persistent side effects first-class in the worker contract (the
operational port of the paper's coeffect declarations): what a task did to
the world outside the repo must be declared, and its reverse mapping named.

## Allowed files (edit boundary)

- home/dot_agents/skills/agmsg-orchestration/SKILL.md
- home/dot_config/claude/rules/agmsg-orchestration.md (ONE bullet)
- Your artifact paths (T60 five artifacts)
- (home/dot_claude/skills/agmsg-orchestration is a symlink template — do
  not touch, per the T45 finding)

## Forbidden actions

git commit; git push; chezmoi apply; bats; any code change; changing
existing v1 message fields or breaking backward compatibility (effects is
OPTIONAL).

## Work order (exact)

1. SKILL.md, AGMSG-RESULT contract section, append:
   - RESULTs for tasks that created persistent side effects OUTSIDE the
     repository working tree (global asset installs, $HOME writes,
     external service registrations) include
     `effects=<semicolon-list-of-short-ids>`.
   - For each effect the report must state its reverse mapping: the
     `~/.agents/.installed-manifest.json` step name (removable via
     `remove-agent-asset`), a documented removal procedure, or an
     explicit `irreversible:` statement with rationale.
   - In-repo edits within allowed_files are NOT effects.
2. SKILL.md, Orchestrator Playbook: one numbered-step addition — on
   RESULTs carrying effects, verify each declared reverse mapping exists
   before acceptance; record irreversible effects in the acceptance note.
3. rules/agmsg-orchestration.md: ONE bullet mirroring step 2 at rule
   granularity (match existing bullet style, English).
4. Consistency: wording must align with T58's remover semantics and T45's
   marker contract; quote nothing that contradicts them.

## Validation (record in validation artifact)

1. `make validate-agent-assets` green.
2. `git diff` full text; 4-way consistency check (SKILL / rules / plan /
   analysis) listed in the validation file.
3. `git status --porcelain` -> only Allowed files + artifacts.

## Completion / RESULT contract

- Five artifacts (T60 set); T45-contract memory add executed and quoted.
- Dogfood: this task itself has NO out-of-repo effects — state
  `effects=none` explicitly in the report as the first example of the
  clause.
- Reply `AGMSG-RESULT v1 task_id=T60 status=ready_for_review ...`.
  max_turns=12.
