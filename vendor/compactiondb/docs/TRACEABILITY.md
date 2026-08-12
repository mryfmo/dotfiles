# Analysis-to-implementation traceability

| analysis finding | implementation | verification |
|---|---|---|
| identical memoryのdedupでsession境界が消え得る | scopeとsessionを含むdedup key | `test_identical_session_memories_are_deduplicated_only_within_session` |
| 大量pruneがSQLite変数上限を超え得る | 500件単位のevent/FTS batch delete | `test_prune_batches_more_than_sqlite_variable_limit` |
| StopFailureのofficial fieldsを落とす | error, error_details, rendered messageを保持 | `test_stop_failure_preserves_official_error_fields` |
| subagent/task lifecycleが欠落 | SubagentStart, TaskCreated, TaskCompleted hooksと正規化 | `test_subagent_and_task_lifecycle_fields_are_normalized` |
| project path変更でidentityが変わり得る | atomic persistent `state/project-id` | `test_identity_is_persistent_when_project_directory_moves`, `test_concurrent_first_run_uses_one_identity` |
| 大きなdetail切詰めでJSONが壊れ得る | bounded canonical JSON encoder | `test_large_detail_remains_valid_bounded_json` |
| installerが既存hookを壊し得る | ContextDB groupだけ置換し、unrelated hooksを保持 | installer tests and release smoke |
| heuristic memoryが別sessionへ汚染し得る | heuristic/PostCompact memoryはsession scope、project昇格は明示 | `test_heuristic_memory_stays_session_scoped`, recovery tests |
| Compaction recovery mixed all sessions | all raw recovery queries require exact `project_id + session_id` | `test_raw_recovery_never_mixes_sessions` |
| DB lock silently lost events | pre-DB atomic spool, single-writer lock, retryable drain, error log | `test_database_lock_does_not_drop_event`, `test_writer_lock_leaves_durable_spool_for_later` |
| concurrent hooks could collide | cross-process lock + unique event UUID | `test_parallel_hook_processes_preserve_all_events`, `test_duplicate_event_uuid_is_idempotent` |
| only successful tools were logged | `PostToolUseFailure` and `PermissionDenied` hooks | `test_post_tool_failure_fields_are_persisted` |
| actual compact summary was not stored | `PostCompact.compact_summary` capture and durable promotion | `test_postcompact_summary_becomes_durable_memory` |
| raw logs and durable memory were conflated | separate `events`, `memory_candidates`, `memories`, `memory_blocks` | storage and recovery tests |
| no correction/supersession model | append-only memory replacement/retraction link | `test_superseding_memory_is_append_only_projection` |
| no Japanese-capable search | FTS5 trigram with LIKE fallback | `test_fts_search_supports_japanese_substrings` |
| no semantic extension point | disabled-by-default external embedding adapter | `test_external_semantic_embedding_adapter` |
| secrets stored in DB and spool | pre-spool redaction, sensitive path suppression | redaction tests |
| local files could be world-readable | POSIX 0700/0600 best effort | `test_private_file_modes` |
| log text could reinject commands | recovery evidence boundary warning | recovery tests inspect packet |
| no retention | event expiry + `prune`; memory survives | `test_prune_removes_raw_event_but_keeps_memory` |
| no integrity check | detail SHA-256 + SQLite quick_check | CLI `verify`, test suite |
| no migration path | legacy DB importer | `test_legacy_database_import_is_idempotent_and_redacted` |
