# Data model

## events

短期のredacted event ledgerです。

主要field:

| field | purpose |
|---|---|
| `event_uuid` | replay-safe idempotency key |
| `project_id` | `state/project-id`に永続化したrandom stable ID |
| `session_id` | raw event隔離の境界 |
| `hook_event_name` / `event_type` | source eventとnormalized type |
| `tool_use_id` | Claude tool call correlation |
| `summary` / `detail_json` | bounded redacted representation |
| `detail_sha256` | stored detailの整合性検証 |
| `input_sha256` / `output_sha256` | sanitized input/output fingerprint |
| `sensitivity` | `internal` / `restricted` |
| `expires_at_utc` | raw retention |

## event_files

file pathとoperationのprojectionです。recoveryのfile listはこのtableを同一sessionでqueryします。

## memory_candidates

heuristic extractorが作成した候補です。高確度候補は自動昇格しますが、heuristicとPostCompact由来は元sessionのscopeを維持します。明示markerだけが自動でproject scopeとなり、それ以外を別sessionでも使う場合は人間・agentが `memory promote <id> --scope project` で昇格します。

## memories

長期記憶の追記型正本です。

| field | purpose |
|---|---|
| `memory_uuid` | stable identity |
| `scope` | `project` / `session` |
| `kind` | decision, constraint, preference, open_task等 |
| `confidence` / `salience` | retrieval prioritization metadata |
| `valid_from_utc` / `valid_until_utc` | validity window |
| `supersedes_memory_uuid` | replacement/retraction link |
| `status` | `active` / `retraction` |
| `source_event_uuids_json` | evidence lineage |
| `generator` | manual, heuristic, PostCompact等 |

current memoryは「activeかつ、別recordからsupersedeされていないもの」というquery projectionです。既存recordをUPDATEして内容を書き換えません。

## memory_blocks

project memoryだけを対象とする再構築可能なbinary hierarchy cacheです。session memoryをblockに含めないため、別session由来の一時情報は混ざりません。

## FTS tables

SQLiteが対応していれば`trigram` tokenizerを使用し、日本語を含むsubstring searchを可能にします。利用できない環境では`unicode61`、さらに作成できない場合は`LIKE`へfallbackします。

## memory_embeddings

optional external embedding adapterのcacheです。model、dimension、vector JSON、content hashを保持します。標準では無効です。

## project-id file

`.claude/contextdb/state/project-id`はDB外のproject identity正本です。project directoryを移動しても同じIDを維持するため、backup、cloneの意図、restore方針に応じてDBと一緒に管理します。通常は`.gitignore`対象であり、repositoryをcloneした別machineは別identityとして初期化されます。
