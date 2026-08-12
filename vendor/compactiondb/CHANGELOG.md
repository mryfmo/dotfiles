# Changelog

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
