# T49: `contextdb probe` — deterministic probe generation (P4)

task_id: T49
repo: /Users/mryfmo/Workspace/dotfiles
team: dotfiles-conformance
worker: codex-deep-dot
plan: .orchestration/tasks/PLAN-compactiondb-research-integration.md (Phase 4)
analysis: .orchestration/analysis/compactiondb-compaction-research.md (P4)
depends: T47 (accepted)

[memory: decision — CompactionDB gains a read-only zero-token `probe` subcommand producing recall/artifact/decision/continuation probes with ledger-derived ground truth; grading is an orchestrator-side procedure on the review profile, never part of the CLI.]

## Goal

Port Factory.ai's probe-based evaluation to a deterministic, LLM-free CLI:
generate probe questions WITH ground truth from the ledger so recovery
packet quality becomes measurable. Grading stays outside the CLI.

## Allowed files (edit boundary)

- vendor/compactiondb/.claude/contextdb/contextdb/cli.py (new subcommand)
- vendor/compactiondb/.claude/contextdb/contextdb/probe.py (NEW module;
  put the generation logic here, cli.py only wires it)
- vendor/compactiondb/tests/test_probe.py (NEW)
- vendor/compactiondb/README.md (probe section incl. the 2-line grading
  operations note)
- vendor/compactiondb/docs/ (the most fitting doc for CLI reference)
- vendor/compactiondb/CHANGELOG.md (append to 2.0.0+dotfiles.4)
- vendor/compactiondb/MANIFEST.sha256
- Your artifact paths (T49 five artifacts)

## Forbidden actions

git commit; git push; chezmoi apply; bats; dependency changes; any LLM
call or network access; any DB write from the probe path; changes to
recovery.py/storage.py/spool.py/hook.py.

## Work order (exact; ambiguity -> ask via agmsg)

1. Add `probe --session <id> [--json]`. Output JSON:
   `{"probes": [{"type": ..., "question": ..., "ground_truth": ...}]}`
   (text mode may render the same data line-based; --json is canonical).
2. Generation rules (skip a probe type entirely when its source is empty;
   never emit empty ground truth):
   - recall: ground truth = summary of the session's FIRST
     PostToolUseFailure event (fall back to first failure-classified
     event); question = "What was the first error in this session?".
   - artifact: ground truth = the deduplicated write/edit file list with
     last-op and counts, derived from the SAME query logic T47 uses for
     File modifications (reuse the recovery.py helper if importable
     without modifying it; otherwise mirror the query in probe.py and add
     a test asserting probe ground truth == the packet's File
     modifications content); question = "Which files were modified in this
     session?".
   - decision: ground truth = kind=decision memories (this session +
     project scope actives); question = "What decisions were made?".
   - continuation: ground truth = T47's Open tasks derivation (open_task
     memories + TaskCreated−TaskCompleted); question = "What remains to be
     done?".
3. Read-only guarantee: no INSERT/UPDATE/DELETE; open the store the same
   read path other query subcommands use.
4. Tests (test_probe.py): (a) each type generates with populated fixture;
   (b) each type skipped when its source is empty; (c) JSON schema (keys,
   types) pinned; (d) cross-session isolation (other session's data never
   in ground truth); (e) artifact ground truth consistency with the T47
   File modifications section; (f) read-only: DB content hash identical
   before/after probe run.
5. README probe section: usage + the operations note that grading runs on
   the review profile at low effort in a separate context, only when
   recovery logic changes.
6. CHANGELOG bullet (2.0.0+dotfiles.4); MANIFEST regeneration per the
   established method.

## Validation (record in validation artifact)

1. `make -C vendor/compactiondb clean && make -C vendor/compactiondb test`
   -> all green (state totals).
2. `make -C vendor/compactiondb clean && make -C vendor/compactiondb validate`
   -> 0 fail.
3. `git status --porcelain` / `git diff --stat` -> only Allowed files.
4. One full probe JSON output from a populated fixture pasted for
   orchestrator cross-check against the T47 example packet.

## Completion / RESULT contract

- Five artifacts at .orchestration/{reports/T49.md, validation/T49.txt,
  sandboxes/T49.md, learning/T49.md, autoskill/runs/T49.md}.
- Report uses `[memory:...]` markers; no `memory add` here.
- Reply `AGMSG-RESULT v1 task_id=T49 status=ready_for_review ...`.
  max_turns=20.
