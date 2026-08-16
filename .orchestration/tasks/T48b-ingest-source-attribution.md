# T48b: Vendored ingest — explicit trusted ingestion source (prerequisite for T48)

task_id: T48b
repo: /Users/mryfmo/Workspace/dotfiles
team: dotfiles-conformance
worker: codex-deep-dot
plan: .orchestration/tasks/PLAN-compactiondb-research-integration.md (Phase 3, risk clause "T48b")
depends: T48 blocked report (.orchestration/reports/T48.md)

[memory: decision — CompactionDB ingest gains an optional validated --ingested-from token carried in the spool envelope and honored by drain_spool; default behavior without the flag is byte-identical to today.]

## Goal

Allow `contextdb ingest` to attribute events to an explicit trusted source
(e.g. `codex`) so the T48 receiver can produce `events.ingested_from='codex'`
without changing spool/drain semantics for every other path.

## Allowed files (edit boundary)

- vendor/compactiondb/.claude/contextdb/contextdb/cli.py (ingest parser only)
- vendor/compactiondb/.claude/contextdb/contextdb/spool.py
- vendor/compactiondb/.claude/contextdb/contextdb/hook.py ONLY if the
  process_payload signature change requires a call-site update (keep hook
  behavior identical; state it in the report)
- vendor/compactiondb/tests/ (test_cli.py and/or test_spool.py)
- vendor/compactiondb/docs/ (the section documenting ingest)
- vendor/compactiondb/CHANGELOG.md (append to 2.0.0+dotfiles.4)
- vendor/compactiondb/MANIFEST.sha256
- Your artifact paths (T48b five artifacts)

## Forbidden actions

git commit; git push; chezmoi apply; bats; dependency changes;
storage.py changes (insert_event already accepts ingested_from);
changing default ingested_from behavior for non-flagged paths;
receiver/profile work (that remains T48).

## Work order (exact)

1. CLI: add `--ingested-from <token>` to the ingest subcommand. Validate
   the token against `^[a-z0-9][a-z0-9_-]{0,31}$`; reject otherwise with
   the CLI's existing error style. No other subcommand changes.
2. Spool envelope: when the flag is provided, record it in the spooled
   JSON envelope under a reserved key (follow the envelope's existing
   naming style; e.g. an `ingested_from` sibling of the payload). Events
   spooled by hooks (no flag) carry no such key.
3. drain_spool: if the envelope carries the key, pass its value to
   `insert_event(..., ingested_from=<value>)`; otherwise keep today's
   exact behavior (source.name). Quarantine/validation behavior for
   malformed envelopes must remain unchanged; an envelope key with an
   invalid token is treated as a schema violation -> quarantine (pin by
   test).
4. Tests: (a) `ingest --ingested-from codex` end-to-end -> events row has
   ingested_from='codex'; (b) no flag -> behavior byte-identical to
   today (existing tests must pass unchanged); (c) invalid CLI token ->
   error; (d) tampered envelope token -> quarantined, error logged.
5. Docs: document the flag where ingest is documented; note the trust
   model (the flag is trusted local input; hook-spooled events cannot
   carry it).
6. CHANGELOG bullet in 2.0.0+dotfiles.4; MANIFEST regeneration per the
   established method.

## Validation (record in validation artifact)

1. `make -C vendor/compactiondb clean && make -C vendor/compactiondb test`
   -> all green (state totals).
2. `make -C vendor/compactiondb clean && make -C vendor/compactiondb validate`
   -> 0 fail.
3. `git status --porcelain` / `git diff --stat` -> only Allowed files.
4. Full `git diff` of cli.py/spool.py in the validation artifact.

## Completion / RESULT contract

- Five artifacts at .orchestration/{reports/T48b.md, validation/T48b.txt,
  sandboxes/T48b.md, learning/T48b.md, autoskill/runs/T48b.md}.
- Report uses `[memory:...]` markers; no `memory add` here.
- Reply `AGMSG-RESULT v1 task_id=T48b status=ready_for_review ...`.
  max_turns=20. After T48b acceptance, T48 resumes under its original task
  file with the receiver using `--ingested-from codex`.
