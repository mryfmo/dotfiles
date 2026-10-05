# Changelog

## 2.0.0+dotfiles.9

- Generated instruction snippets and recovery verification commands use `uv run --no-project` so the stdlib CLI does not synchronize the target project environment.

- Reclaim orphaned project session rows before evicting newer events and after every size-cap batch.
- Preserve installed hook positions and leave settings bytes, timestamps and backups untouched on a no-op reinstall.
- Run vendor test discovery from the dotfiles repository root as well as the vendor directory.
- Find enclosing opted-in projects from nested session working directories, stopping at the nearest Git directory or worktree gitfile. Explicit project roots keep their meaning.
- Apply configured error-log and quarantine retention from explicit `prune` and existing SessionEnd maintenance. Validate retention configuration before pruning, preserve malformed log records, and refuse symlinked or non-regular health logs using a no-follow file descriptor.
- Construct storage directories using descriptor-relative `mkdir`, `open(O_NOFOLLOW)` and `fchmod` on POSIX. This closes directory symlink races during construction. Residual: subsequent pathname-based I/O, including `sqlite3.connect`, can still follow a same-user swap after construction; portable stdlib SQLite cannot bind a directory fd. Storage remains in the workspace.

## 2.0.0+dotfiles.8

- Added `ingest --no-maintenance`: the event is normalised, spooled and committed, but the SessionEnd retention pass (expired-event pruning and error-log/quarantine cleanup) is skipped, so a caller with a short budget, such as Codex's 3-second `SessionEnd` hook, only records the event. Retention still runs on the explicit `prune` command and on Claude Code's own `SessionEnd` hook.

## 2.0.0+dotfiles.7

- Normalised the Codex `notify` payload: an `agent-turn-complete` object without `hook_event_name` is recorded as a `Stop` hook (`turn_stop`) with `thread-id` as the session, `client` as the agent and `last-assistant-message` as `last_assistant_message`, instead of an `unknown` event; `thread-id` and `turn-id` derive a stable `event_uuid`, so a repeated delivery of one turn is stored once. Hook payloads are unchanged.
- Bounded the ledger on the explicit `prune` command only: a new `capture.max_db_bytes` setting (default 512 MiB) first deletes unpromoted memory candidates whose source events retention already removed, then the oldest events in batches of 100 (with their unpromoted candidates; durable memories and promoted candidates stay) until the in-use pages fit, merging the FTS index before the first measurement and after every batch so dead segment pages never count as in use; `prune` then forces `VACUUM` whenever retention or the cap deleted rows or the file is still over the cap, and otherwise runs it when free pages exceed 64 MiB. The SessionEnd hook still only deletes expired events and never vacuums.
- Added a `make manifest` target that regenerates `MANIFEST.sha256` from the tracked files.

## 2.0.0+dotfiles.6

- Defaulted the hook interpreter stored in `.claude/settings.json` to the bare `python3` command (PATH lookup at hook time) instead of the installing machine's `sys.executable`, so settings committed from one machine keep working on another. `--python` still accepts an explicit path. Verified on Ubuntu: Claude Code resolves the bare command via PATH, and the hooks run under both the system and mise interpreters.

## 2.0.0+dotfiles.5

- Recorded each injected recovery packet as a best-effort `recovery_injected` spool event so model-visible recovery context is replayable from the ledger without adding a synchronous database write.

## 2.0.0+dotfiles.4

- Raised the default recovery packet budget to 12,000 characters.
- Added a configurable 2,000-character file-section budget.
- Rebuilt recovery packets as fixed-order sections with ledger-derived evidence authoritative over compact summaries.
- Added a deterministic write/edit artifact trail and active-task projection without LLM calls.
- Added validated local-source attribution for CLI-ingested events without changing hook-spool defaults.
- Added read-only deterministic recovery probes with ledger-derived ground truth.
- Added read-only query-conditioned recall with lexical/semantic fusion and event closure.

## 2.0.0+dotfiles.3

- Preserved sentence boundaries when removing inline explicit memory markers.

## 2.0.0+dotfiles.2

- Restructured explicit marker extraction to process all markers with bounded content and isolated heuristics.

## 2.0.0 — 2026-07-31

- session-isolated compaction recovery
- durable redacted spool and single-writer SQLite ingestion
- WAL/FULL synchronous and idempotent event UUIDs
- PostToolUseFailure, PermissionDenied, PostCompact, StopFailure, SubagentStart/Stop, TaskCreated/Completed, SessionEnd support
- secret redaction and sensitive path suppression
- structured durable memories, candidates, supersession, retraction, validity metadata
- rebuildable hierarchical project-memory projection
- FTS5 trigram search with fallback
- optional external semantic embedding adapter
- raw-event retention and verification CLI
- safe installer and legacy DB migration
- persistent project identity that survives directory moves and concurrent first-run hooks
- session-scoped automatic heuristic memories; explicit/manual promotion required for cross-session project memory
- bounded valid JSON detail encoding and embedding-model mismatch rejection
- idempotent installer that preserves unrelated hooks and supports self-root upgrades
- 39-test standard-library suite plus release validator and installed-project smoke test

## 2.0.0+dotfiles.1

- Hardened redaction, retention, and explicit memory marker parsing.
