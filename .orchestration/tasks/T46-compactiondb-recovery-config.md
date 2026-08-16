# T46: CompactionDB config schema — recovery budgets (P7 + P1 groundwork)

task_id: T46
repo: /Users/mryfmo/Workspace/dotfiles
team: dotfiles-conformance
worker: codex-deep-dot
plan: .orchestration/tasks/PLAN-compactiondb-research-integration.md (Phase 2)
analysis: .orchestration/analysis/compactiondb-compaction-research.md (P1, P7)

[memory: decision — CompactionDB recovery budget defaults become 12000 chars total with a 2000-char files sub-budget, config-overridable, backward compatible with configs missing the new key.]

## Goal

Extend the vendored CompactionDB config schema for the Phase 2 recovery
rework: raise the total recovery budget default and add a files-section
sub-budget key. No recovery.py behavior change in this task (that is T47).

## Allowed files (edit boundary)

- vendor/compactiondb/.claude/contextdb/contextdb/config.py
- vendor/compactiondb/.claude/contextdb/config.json
- vendor/compactiondb/tests/ (the existing test module that covers config
  loading — extend it; create tests/test_config.py ONLY if no such module
  exists, and say which in the report)
- vendor/compactiondb/docs/ (only the doc section that documents recovery
  config keys)
- vendor/compactiondb/CHANGELOG.md
- vendor/compactiondb/MANIFEST.sha256
- Your artifact paths (T46 report/validation/sandbox/learning/autoskill)

## Forbidden actions

git commit; git push; chezmoi apply; running bats; dependency changes;
editing recovery.py or any module other than config.py; changing hook or
CLI behavior; changing redaction/capture/memory config semantics.

## Work order (follow exactly; ambiguity -> ask via agmsg)

1. Read the current recovery config section (budget 8500 chars; prompts 4 /
   events 12 / files 12 / failures 5) and record the exact existing key
   names and validation style in the report.
2. Change the total recovery budget default from 8500 to 12000 chars
   (same key, same type, same validation).
3. Add a new key for the files-section sub-budget, default 2000 chars,
   following the existing recovery key naming convention exactly (e.g. if
   the total is `max_chars`-style, name it accordingly; state your choice
   and the convention evidence in the report). Validation/typing identical
   in style to the sibling keys.
4. Preserve unknown-key and bad-type behavior exactly as today; pin it with
   a test if not already pinned.
5. Tests (unittest, in the vendor test layout): (a) defaults 12000/2000
   load when keys are absent from config.json; (b) explicit values
   override; (c) invalid type raises/behaves exactly like existing sibling
   keys (match current behavior, do not invent stricter handling).
6. Update the recovery-config documentation (docs/) and add a
   `2.0.0+dotfiles.3` CHANGELOG section describing the two config changes.
7. Regenerate MANIFEST.sha256 the same way T44 did (state the command).
8. Backward-compatibility check: run the full vendor suite; all existing
   tests must pass unchanged except any that assert the old 8500 default —
   update those minimally with a one-line comment referencing T46.

## Validation (record outputs in the validation artifact)

1. `make -C vendor/compactiondb test` -> all green (include the summary
   line and the count of new tests).
2. `make -C vendor/compactiondb validate` -> all checks green.
3. `git status --porcelain` / `git diff --stat` -> only Allowed files.
4. Full `git diff` of config.py/config.json included in the validation
   file.

## Completion / RESULT contract

- Five artifacts at .orchestration/{reports/T46.md, validation/T46.txt,
  sandboxes/T46.md, learning/T46.md, autoskill/runs/T46.md}.
- Report states durable facts with `[memory:...]` markers (T45 contract).
  This repo is not CompactionDB-opted-in; do not run `memory add`.
- Reply `AGMSG-RESULT v1 task_id=T46 status=ready_for_review ...` with all
  artifact paths. max_turns=20.
