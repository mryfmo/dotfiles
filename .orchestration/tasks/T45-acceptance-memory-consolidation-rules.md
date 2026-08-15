# T45: Acceptance-time memory consolidation + AGMSG-TASK marker contract (rules only)

task_id: T45
repo: /Users/mryfmo/Workspace/dotfiles
team: dotfiles-conformance
worker: codex-standard-dot
plan: .orchestration/tasks/PLAN-compactiondb-research-integration.md (Phase 1)
analysis: .orchestration/analysis/compactiondb-compaction-research.md (P6)

## Goal

Codify proposal P6 as documentation-only changes (NO code changes): under the
agmsg parallel-worktree regime, CompactionDB databases are never shared across
worktrees; instead the orchestrator consolidates accepted decisions into the
main worktree DB at ACCEPTANCE time, and AGMSG-TASK/RESULT gain an explicit
`[memory:...]` marker contract.

## Allowed files (edit boundary)

- home/dot_config/claude/rules/compactiondb.md
- home/dot_config/claude/rules/agmsg-orchestration.md
- home/dot_agents/skills/agmsg-orchestration/SKILL.md
- home/dot_claude/skills/agmsg-orchestration/ (ONLY if step 1 shows it is a
  separate real file, not a symlink/render of the dot_agents source; if it is
  derived, do not touch it and say so in the report)
- Your artifact paths (report/validation/sandbox/learning/autoskill for T45)

## Forbidden actions

git commit; git push; chezmoi apply; running bats; dependency changes;
editing any file outside Allowed files; changing vendor/compactiondb;
changing any code or config semantics (this task is prose-only).

## Work order (follow exactly; ambiguity -> ask via agmsg, do not interpret)

1. Determine the relationship between
   `home/dot_claude/skills/agmsg-orchestration` and
   `home/dot_agents/skills/agmsg-orchestration` (symlink template, duplicate
   real files, or chezmoi-managed rendering). Record the finding and the
   single source of truth you will edit in the report.
2. Append to `home/dot_config/claude/rules/compactiondb.md` (English, match
   existing bullet style, 1-2 bullets max) the P6 rule:
   - Under the agmsg parallel-worktree regime, never share a CompactionDB
     across worktrees. At ACCEPTANCE time the orchestrator consolidates
     adopted decisions into the main worktree DB with
     `python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project`.
     Worker-worktree DBs are disposable with their worktrees.
3. Append one bullet to the evidence-sync clause area of
   `home/dot_config/claude/rules/agmsg-orchestration.md`: during the
   `.orchestration` sync batch, verify no accepted task is missing its
   consolidated decision record (only for CompactionDB-opted-in projects).
4. In the agmsg-orchestration SKILL.md task-file/RESULT contract sections,
   add the marker contract:
   - Task files/RESULTs must state durable facts with `[memory:decision]` /
     `[memory:failure]` markers using the vendored CompactionDB marker syntax
     (tag form and bracket form, kind aliases per vendor README after T44).
   - In CompactionDB-opted-in projects, the worker runs
     `contextdb_cli.py memory add` before completion and includes the exact
     command(s) in the RESULT report.
5. Keep every addition consistent with existing rules (parallel regime,
   identity rules, store rules) and with
   `vendor/compactiondb/README.md` marker documentation. Quote nothing that
   contradicts them; if you find a contradiction, stop and report it.

## Validation (record outputs in the validation artifact)

1. `git status --porcelain` and `git diff --stat` -> only Allowed files.
2. `git diff` full text included in validation file.
3. `make validate-agent-assets` -> green.
4. A 4-way consistency check (manual, listed in validation file):
   compactiondb.md / agmsg-orchestration.md / SKILL.md / vendor README agree
   on marker forms, command names, and scope names.

## Completion / RESULT contract

- Write all five artifacts:
  - report: .orchestration/reports/T45.md
  - validation: .orchestration/validation/T45.txt
  - sandbox: .orchestration/sandboxes/T45.md
  - learning: .orchestration/learning/T45.md
  - autoskill: .orchestration/autoskill/runs/T45.md (record "not-used" if so)
- The report must state durable facts with `[memory:...]` markers per the
  very contract this task introduces (dogfooding). This repo is NOT
  CompactionDB-opted-in, so do NOT run `memory add` here; note that in the
  report.
- Reply `AGMSG-RESULT v1 task_id=T45 status=ready_for_review ...` with all
  artifact paths. max_turns=15.
