# T47: Recovery packet — fixed sections + deterministic artifact trail (P1+P2)

task_id: T47
repo: /Users/mryfmo/Workspace/dotfiles
team: dotfiles-conformance
worker: codex-deep-dot
plan: .orchestration/tasks/PLAN-compactiondb-research-integration.md (Phase 2)
analysis: .orchestration/analysis/compactiondb-compaction-research.md (P1, P2)
depends: T46 (accepted)

[memory: decision — The CompactionDB recovery packet becomes a fixed-order sectioned plain-text document (Header, Goal, File modifications, Recent activity, Decisions, Open tasks, Failures, Compact summary) rebuilt deterministically from the ledger on every recovery; empty sections still print their heading with "(none)"; ledger-derived sections are authoritative over the compact summary.]

## Goal

Restructure `build_recovery_context()` into fixed sections with a
deterministic write/edit artifact trail, per the Factory.ai finding that
LLM summaries cannot preserve the artifact trail (all methods 2.19-2.45/5)
and its recommendation of explicit file-state tracking in scaffolding.
Zero LLM calls; plain text; existing redaction and session-isolation
invariants unchanged.

## Allowed files (edit boundary)

- vendor/compactiondb/.claude/contextdb/contextdb/recovery.py
- vendor/compactiondb/tests/test_recovery.py
- vendor/compactiondb/docs/ARCHITECTURE.md (recovery-path description)
- vendor/compactiondb/README.md (recovery packet example section)
- vendor/compactiondb/CHANGELOG.md (append bullets to the existing
  2.0.0+dotfiles.4 section; do NOT create a new section)
- vendor/compactiondb/MANIFEST.sha256 (regenerate as in T46)
- Your artifact paths (T47 five artifacts)

If implementing a section requires reading data that recovery.py does not
already query (e.g. Task events), you may ADD read-only queries in
recovery.py using existing storage helpers; you may NOT modify storage.py,
normalize.py, or any other module. If that proves impossible, stop and ask
via agmsg.

## Forbidden actions

git commit; git push; chezmoi apply; bats; dependency changes; any LLM or
external-process call added to the recovery path; changes to modules other
than recovery.py; changing the additionalContext JSON envelope emitted by
recover_hook.py; weakening redaction or cross-session isolation.

## Specification (exact; ambiguity -> ask via agmsg)

Rebuild the packet in this fixed section order. Every section prints its
heading even when empty, with `(none)` as the body (checklist principle).
Plain text, same envelope as today.

1. Header (required, first): project/session identification and the
   existing evidence disclaimer, plus this added sentence:
   "If the compact summary conflicts with the sections below, the
   ledger-derived sections are authoritative."
2. Goal: the summary of the session's FIRST user_prompt event (existing
   240-char capture limit applies) plus, if present, the newest explicit
   kind=decision memory candidate or memory recorded in THIS session.
3. File modifications (deterministic artifact trail): all distinct file
   paths from this session's event_files with operation in {write, edit},
   deduplicated; one line per file:
   `<path> (<last operation>, <count of write/edit ops>x)`;
   ordered by most recent operation first; fitted to the
   `recovery.files_budget_chars` budget (T46); on overflow drop the oldest
   entries and append `... and N more modified files (see contextdb files)`.
   read/search operations are excluded from this section.
4. Recent activity: the existing recent-files rendering (recent_files
   config, all operations) moved here, unchanged in content.
5. Decisions: the existing hierarchical project-memory rendering moved
   into this section, plus kind=decision session memories of THIS session.
6. Open tasks: active kind=open_task memories plus the difference
   (TaskCreated events minus TaskCompleted events) of this session,
   matched by task identifier from event detail; if the ledger has no task
   events, just the memories.
7. Failures: existing rendering (recent_failures config), unchanged.
8. Compact summary: the existing latest PostCompact summary (3000-char cap
   unchanged), LAST, labeled as reference material.

Budgeting: Header and File modifications are allocated first; remaining
sections share the rest of `recovery.max_chars` (12000) using the existing
truncate-middle behavior. Total output must never exceed max_chars
(boundary-pinned by test).

## Tests (extend tests/test_recovery.py; each is required)

(a) write/edit mix with repeated edits to one file -> dedup + last-op +
count rendering, ordering by recency;
(b) files sub-budget overflow -> oldest dropped + "N more" tail line;
(c) empty session -> all headings present, each `(none)`, within budget;
(d) compact summary + sections coexistence -> section order and the added
authoritative-disclaimer sentence;
(e) cross-session isolation: another session's files/memories never appear
(extend the existing isolation test to the new sections);
(f) TaskCreated/TaskCompleted difference appears in Open tasks;
(g) total length <= max_chars at the boundary (construct data that would
overflow without truncation).
Existing tests that assert the old packet layout may be updated to the new
layout with a one-line comment referencing T47; tests unrelated to layout
must pass unchanged.

## Validation (record in validation artifact)

1. `make -C vendor/compactiondb clean && make -C vendor/compactiondb test`
   -> all green; state total and new test counts.
2. `make -C vendor/compactiondb validate` -> all checks pass, 0 fail
   (run after clean; note the pycache false-positive pattern from T46).
3. `git status --porcelain` / `git diff --stat` -> only Allowed files.
4. Paste ONE full example packet (generated from a test fixture with all
   sections populated) into the validation artifact for orchestrator
   review.

## Completion / RESULT contract

- Five artifacts at .orchestration/{reports/T47.md, validation/T47.txt,
  sandboxes/T47.md, learning/T47.md, autoskill/runs/T47.md}.
- Report states durable facts with `[memory:...]` markers. Repo is not
  CompactionDB-opted-in; do not run `memory add`.
- Reply `AGMSG-RESULT v1 task_id=T47 status=ready_for_review ...` with all
  artifact paths. max_turns=25.
