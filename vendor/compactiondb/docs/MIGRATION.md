# Migration from the original CompactionDB

## 対象

旧DB:

```text
.claude/logs/context_log.db
```

旧schemaの `events(id, ts, session_id, event_type, tool_name, summary, detail)` を読みます。

## 実行

```bash
python3 install.py --project /path/to/project --migrate-legacy
```

または:

```bash
python3 migrate_legacy.py --project /path/to/project
```

## mapping

| legacy type | new hook representation |
|---|---|
| `user_prompt` | `UserPromptSubmit` |
| `tool_use` | `PostToolUse` |
| `compact` | `PreCompact` legacy marker |
| unknown | `LegacyEvent` |

旧DBには`PostCompact.compact_summary`がないため、過去のCompaction summaryは復元できません。import後の新しいCompactionから保存されます。

旧timestampはdetail内の`legacy_ts`として保持します。旧DBがlocaltime without timezoneだったため、new ledgerのordering timestampとして無理にUTC変換しません。

## rollback

migrationは旧DBを変更・削除しません。new `.claude/contextdb/`を削除し、settings backupを戻せばrollbackできます。
