# Report: dotfiles-T81-compactiondb-vendor-a01

- **Worker and branch:** `claude-standard-dot-a005` in worker-c, branch `feat/compactiondb-codex-ingest` from `origin/main` 62d0771f with `--no-track`. Earlier branches are untouched.
- **task_rev:** `sha256:06b2e5ae…d77b`, matched in the main checkout.
- **PR:** #268, https://github.com/mryfmo/dotfiles/pull/268.
- **Commits:** `726b9129` (the change), `f9f4b916` (Codex P2 4179179554: capped batches delete their unpromoted candidates), `8c8cf691` (Codex P2s 4179234161, 4179234158, 4179234164: idempotent notify UUID, orphaned candidates before newer events, FTS optimize).
- **Final head:** `8c8cf691`. CI, branch and bot state are in the validation file.
- **Status:** ready_for_review.

## 1. What changed

1. **Notify normalisation:** `normalize.py` `_codex_notify_as_hook()` runs first in `normalize_hook_payload`. A payload with `type == "agent-turn-complete"` and no `hook_event_name` gets:
   - `hook_event_name: Stop`, so `event_type` becomes `turn_stop`;
   - `session_id` from `thread-id`;
   - `agent_id` from `client`;
   - `last_assistant_message` from `last-assistant-message`.

   The original fields stay in the sanitized payload. When `thread-id` and `turn-id` are both present, `event_uuid` is `uuid5(NAMESPACE_URL, "codex-notify:<thread>:<turn>")`, so a repeated delivery of one turn hits the `event_uuid` UNIQUE constraint and is stored once (Codex P2 4179234161). Any payload with `hook_event_name` is returned unchanged.
   - VERIFY: see the validation file. The official reference lists `type`, `thread-id`, `turn-id`, `cwd`, `input-messages` and `last-assistant-message`. `client` is not among the documented common fields; it is mapped when present, and an absent value leaves the agent empty.
2. **Bounded ledger:**
   - `storage.py`:
     - `_delete_event_ids` is extracted from `prune_expired`, with unchanged batching and FTS-first order;
     - `enforce_size_cap(conn, project, max_bytes)` deletes the oldest events in batches of 100 while `(page_count - freelist_count) * page_size` exceeds the cap. Before deleting any event, it removes the unpromoted `memory_candidates` whose source events retention already deleted (Codex P2 4179234158), and each event batch removes its own unpromoted candidates (Codex P2 4179179554). After any capped deletion it merges the FTS5 index (`optimize`) so the deleted rows' segment pages are freed (Codex P2 4179234164). Durable memories and promoted candidates are never deleted;
     - `vacuum_if_fragmented(conn, threshold_bytes, force)` runs `VACUUM`.
   - `cli.py` `prune` runs `prune_expired` and `enforce_size_cap` in one transaction, then (outside it) `VACUUM` when the cap removed events or free pages exceed `VACUUM_FREE_BYTES` (64 MiB). It reports `size_cap_removed_events` and `vacuumed`.
   - `config.py`: `capture.max_db_bytes` defaults to 512 MiB and is validated as an int of at least 1. The vendor `config.json` default dump gains the key. Project configs without it get the default through `load_config`'s merge.
   - The SessionEnd hook path (`hook.py`) is unchanged: it still only runs `prune_expired` and never vacuums.
3. **Vendor tests:**
   - `test_cli`:
     - a Codex notify payload ingests as `Stop`/`turn_stop` with session, agent and message;
     - `prune` with `max_db_bytes: 1` removes all 4 events and the unpromoted `session_outcome` candidate, vacuums, and keeps the memory and its promoted candidate. Against `726b9129` it fails, because the candidate survives.
     - a repeated delivery of the same turn stores one event.
   - `test_storage`:
     - the size cap removes exactly one batch of the oldest events and keeps the newest;
     - `VACUUM` runs only over the free-page threshold or when forced;
     - orphaned candidates are reclaimed before any newer event (0 events removed, 10 kept);
     - capping every event returns the database to its fresh size (FTS pages freed).
4. **Release bookkeeping:**
   - CHANGELOG `2.0.0+dotfiles.7`.
   - VERIFY: the vendor Makefile had no manifest target. I derived the rule from the existing file (every tracked vendor file except `MANIFEST.sha256`, `./`-relative, `LC_ALL=C` order) and proved it reproduces origin/main's manifest byte for byte. I added it as `make manifest` (the Makefile is allowed "only if the manifest target needs a fix") and regenerated with `make -C vendor/compactiondb manifest`: 9 lines change, and `sha256sum -c` gives rc=0.
   - `assets.compactiondb.pin: 2.0.0+dotfiles.7`.
5. **Project copy:**
   - `compactiondb-install` runs `~/.agents/compactiondb/install.py`, the copy `make update` installed, which lacks this change. The documented equivalent from this tree is `python3 vendor/compactiondb/install.py --project . --skip-instructions` (verbatim in the validation file).
   - It refreshed the four runtime files; the hooks were already identical.
   - It also reordered the two Stop hooks in `.claude/settings.json` and wrote a backup next to it. `.claude/settings.json` is forbidden, so I restored it with `git checkout` and removed the backup.
   - **Parity check:** `validate_compactiondb_project_copy` requires every file under `.claude/contextdb/contextdb/` and `.claude/hooks/contextdb_*.py` to be byte-identical to the vendor counterpart, and names any differing, missing or project-only path. The task said "the two hook scripts", but there are three `contextdb_*.py` hooks; the glob covers all three, matching allowed_files. A unit test covers identical, edited, missing and extra files.
6. **Checks** (verbatim in the validation file):
   - `make render-check`, `make validate-agent-assets`, `make unit-test` (791 OK), ruff (42 formatted) and the manifest check (rc=0) pass.
   - The vendor suite passes with `make -C vendor/compactiondb test` (86 OK).
   - Live check: the Codex payload is stored as `turn_stop|t1`, and `prune` exits 0.

## 2. Deviations and pre-existing failures

- **The task's vendor-test command fails at import, before and after this change.** `uv run python -m unittest discover -s vendor/compactiondb/tests` from the repository root fails on a clean `origin/main` export the same way (`Ran 20 tests`, `FAILED (errors=14)`), because `contextdb` and `tests` are not on the path. The vendor Makefile's `test` target sets `PYTHONPATH` and is the working invocation; I pasted both.
- **Vendor `validate.py` fails two checks on origin/main and on this branch alike:**
  - `unittest_suite`: its regex wants a bare final `OK`;
  - `release_tree_clean`: `__pycache__` from local runs, which I removed afterwards.
  - It is not part of the task's validation list.
- **A file outside allowed_files.** `tests/unit/test_asset_manifest.py` reads the installed CompactionDB version from the vendor CHANGELOG's first heading, so its two expected `2.0.0+dotfiles.6` literals had to move to `.7` (as with T72's test edit). I decided, recorded and continued under the standing directive.
- **Not changed: the retention path.** `prune_expired`, which the SessionEnd hook also runs, still leaves candidates of expired events. Candidates are the promotion queue, so outliving their raw event is existing design. The cap reclaims them first when size requires it, and the hook path stays untouched (SessionEnd is capped at 3 seconds). This answers the harm named in 4179234158 without changing hook behaviour.
- **The size-cap batch is 100, not 500.** The first test showed a 500-row batch deleting a whole small ledger at once. The round-0 claim of a 99-event overshoot ceiling was wrong under FTS and is withdrawn in revise round 1.

## 3. Codex bot

| Head | Result |
|---|---|
| `726b9129` | Review at 20:24:09Z. P2 4179179554, "Prune unpromoted candidates with capped events": `fixed:f9f4b916`. |
| `f9f4b916` | Review at 20:40:35Z with three P2s: |
| | 4179234161, "Use `turn-id` as the Codex idempotency key": `fixed:8c8cf691`. |
| | 4179234164, "Optimize FTS before completing a capped prune": `fixed:8c8cf691`. It was measured first (2.9 MB residual without `optimize`, fresh size with it). |
| | 4179234158, "Delete candidates when retention prunes their source event": `fixed:8c8cf691` for the harm it names. Orphaned candidates are now reclaimed before any newer event, and the retention and SessionEnd paths are deliberately unchanged; see section 2. If the orchestrator wants candidates deleted on retention too, that changes the hook path and is a follow-up. |
| `8c8cf691` (final) | `bot: none`. No review or finding of this head within 15 minutes after CI; the wait ended at 21:15:53Z (SKILL step 15). |

I did not reply to or resolve any thread.

## Revise round 1 (task_rev `sha256:bcc629ca…dbd`): FTS-aware cap and file-state VACUUM

- **Commit:** `a1c69c4e`. `main` had not moved, so no update-branch was needed.
1. **Merge before measuring:**
   - `ContextStore.optimize_fts()` merges the FTS5 index when the tokenizer is not `none`.
   - `enforce_size_cap` calls it before the first size check and after every deleted batch, before re-measuring, and stops as soon as the in-use pages fit.
   - The ponytail comment now names the real ceiling: one index merge per 100-event batch, bounded by how far the ledger is over the cap.
   - The wrong "99-event overshoot" claim is withdrawn.
2. **VACUUM from file state:** `prune` forces `VACUUM` when retention or the cap deleted rows, or when `page_count * page_size` still exceeds `max_db_bytes`; otherwise the 64 MiB free-page threshold applies.
3. **Retention-emptied table:** because `enforce_size_cap` always merges the index first, rows that retention deleted are reclaimed even when the cap then deletes nothing.
4. **Tests** (vendor; 89 OK with `make -C vendor/compactiondb test`):
   - `test_size_cap_under_fts_keeps_events_that_fit`;
   - `test_prune_vacuums_after_a_retention_only_shrink`;
   - `test_prune_reclaims_the_fts_pages_when_retention_empties_the_table`.
   - The orphan-candidate test now measures after the initial merge, as `enforce_size_cap` does.
   - Against the `8c8cf691` runtime, the two VACUUM tests fail (`vacuumed` False), as the audit reproduced.
   - **Honest limitation:** in this environment (SQLite 3.53.1) I could not reproduce the audit's over-deletion. The `8c8cf691` runtime removed exactly what the new code removes in all three fixture shapes I tried: a bulk insert pre-merged, a bulk insert unmerged, and per-event transactions like hook ingestion. At 1,000 events with the audit's 3,500,000-byte cap, both kept 300; the sweeps are verbatim in the validation file. So the FTS test asserts the required outcome but also passes on the old code here; the regression evidence for item 1 is the auditor's. The new code merges before each measurement regardless, which can only reduce what is counted as in use.
5. **Evidence:**
   - the timestamped Bot-wait loop (start, each poll, end) for this head;
   - the task's vendor-test command (the import failure is pre-existing and accepted) and `make -C vendor/compactiondb test`.
- **Project copy and manifest:** the project copy was refreshed with the vendor installer, unsandboxed again (see the sandbox file); `.claude/settings.json` was restored again. `make manifest`, `sha256sum -c` rc 0.
- **Checks:** `make render-check`, `make validate-agent-assets` and `make unit-test` (791 OK) pass; ruff reports 42 files formatted.
- **Codex bot on `a1c69c4e`:** `bot: none`. There was no review or finding of this head in the 15 minutes after CI (timestamped loop in the validation file, 21:42:08Z to 21:57:10Z).

## CompactionDB

```
$ cd /home/moriya/Workspace/dotfiles && python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content 'dotfiles-T81 (operator 2026-10-03): CompactionDB normalises the Codex `notify` payload (`agent-turn-complete` → `Stop`/`turn_stop`, `thread-id` → session, `client` → agent), bounds the ledger (`capture.max_db_bytes` 512 MiB, VACUUM over 64 MiB of free pages, both only on the explicit `prune`), ships as vendored `2.0.0+dotfiles.7`, and the project copy is validated byte-identical to the vendor tree.'
d9f34450-0001-4e36-a2bc-c5cda89c798d
[exit 0]
```

[memory:decision] dotfiles-T81 (operator 2026-10-03): CompactionDB normalises the Codex `notify` payload (`agent-turn-complete` → `Stop`/`turn_stop`, `thread-id` → session, `client` → agent), bounds the ledger (`capture.max_db_bytes` 512 MiB, VACUUM over 64 MiB of free pages, both only on the explicit `prune`), ships as vendored `2.0.0+dotfiles.7`, and the project copy is validated byte-identical to the vendor tree.

## Artifacts

- validation: `.orchestration/validation/dotfiles-T81-compactiondb-vendor-a01.md`
- sandbox: `.orchestration/sandboxes/dotfiles-T81-compactiondb-vendor-a01.md`
- learning: `.orchestration/learning/dotfiles-T81-compactiondb-vendor-a01.md`
- autoskill: `.orchestration/autoskill/runs/dotfiles-T81-compactiondb-vendor-a01.md`

cost: n/a (no subagents; two WebFetch calls for the VERIFY; the runtime does not expose session totals).
