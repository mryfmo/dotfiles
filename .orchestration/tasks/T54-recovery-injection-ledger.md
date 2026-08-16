# T54: Record the injected recovery packet in the ledger (H2, vendor dotfiles.5)

task_id: T54
repo: /Users/mryfmo/Workspace/dotfiles
team: dotfiles-conformance
worker: codex-deep-dot
plan: .orchestration/tasks/PLAN-harness-composability-integration.md (Phase 1)
analysis: .orchestration/analysis/harness-composability-research.md (H2)

[memory: decision — Every recovery packet CompactionDB injects after compaction is itself recorded as a recovery_injected ledger event (summary + full detail + sha256), best-effort and non-blocking, so what the model saw is replayable (dsh model-visible=logged principle).]

## Goal

Port the DeepSeek Harness "model-visible = logged" invariant to the
recovery path: the packet returned as additionalContext must be
reconstructible from the ledger.

## Allowed files (edit boundary)

- vendor/compactiondb/.claude/contextdb/contextdb/recover_hook.py
- vendor/compactiondb/.claude/contextdb/contextdb/hook.py and/or
  normalize.py ONLY if a new event_type token must be admitted — do not
  widen anything else; if the change looks larger than a token admission,
  STOP and ask via agmsg
- vendor/compactiondb/tests/test_recovery.py or NEW tests/test_recover_hook.py
  (state which and why in the report)
- vendor/compactiondb/docs/ (HOOKS.md or the fitting doc section)
- vendor/compactiondb/CHANGELOG.md (NEW section `2.0.0+dotfiles.5`)
- vendor/compactiondb/MANIFEST.sha256 (regenerate per the established method)
- Your artifact paths (T54 five artifacts)

## Forbidden actions

git commit; git push; chezmoi apply; bats; dependency changes; changes to
recovery.py/storage.py/spool.py beyond what is allowed above; any change
to the additionalContext JSON envelope; any synchronous DB write added to
the recovery response path (spooling only); weakening redaction.

## Work order (exact; ambiguity -> ask via agmsg)

1. In recover_hook.py, AFTER the recovery context string is fully built
   and IMMEDIATELY BEFORE returning the hook response, spool one event:
   - event_type: `recovery_injected` (admit the token minimally if the
     normalize/schema layer requires it; report exactly what was needed)
   - session_id: the recovering session
   - summary: first 240 chars of the packet (existing summary cap)
   - detail: the full packet text, subject to the EXISTING capture
     detail-size cap (do not raise caps); detail_sha256 via the existing
     mechanism, computed over the FULL packet before any cap truncation
     if the existing mechanism allows, otherwise over the stored detail —
     state which in the report and pin it in a test
   - Use the existing spool_event() path; DO NOT drain blocking in the
     response path. The existing blocking drain that runs BEFORE building
     recovery is untouched; the new spool entry may be drained by any
     later drain.
2. Failure isolation: wrap the recording in the same best-effort pattern
   as other non-critical paths — on any exception, write one health
   error record and return the recovery response unchanged.
3. No recursion hazard: the record happens after the packet is built, so
   the packet never contains its own record. Pin with a test that builds
   recovery twice and asserts the second packet's Recent activity may
   contain the first `recovery_injected` event as a normal event (no
   special-casing).
4. Tests (required):
   (a) after a recover_hook invocation, exactly one new ledger event of
   type recovery_injected exists whose detail equals the injected
   packet (or capped per the documented rule) and sha256 matches;
   (b) spool failure (mocked) -> recovery response identical, one health
   error line;
   (c) envelope unchanged (existing envelope test extended or reused);
   (d) all existing recovery/recover_hook tests pass unchanged.
5. Docs: add the event to the hook/event documentation. CHANGELOG: new
   `2.0.0+dotfiles.5` section. MANIFEST regenerated.

## Validation (record in validation artifact)

1. `make -C vendor/compactiondb clean && make -C vendor/compactiondb test`
   -> all green (state totals and new-test count).
2. `make -C vendor/compactiondb clean && make -C vendor/compactiondb validate`
   -> 0 fail.
3. `git status --porcelain` / `git diff --stat` -> only Allowed files.
4. Full `git diff` of recover_hook.py (and any token admission) pasted.

## Completion / RESULT contract

- Five artifacts at .orchestration/{reports,validation,sandboxes,learning,
  autoskill/runs}/T54.\*
- This repo IS CompactionDB-opted-in: before completion run
  `python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project`
  with the durable fact above, and include the exact command in the report
  (T45 contract).
- Reply `AGMSG-RESULT v1 task_id=T54 status=ready_for_review ...` with all
  artifact paths. max_turns=20.
