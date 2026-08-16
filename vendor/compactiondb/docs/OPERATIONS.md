# Operations

## 日常確認

```bash
python3 .claude/hooks/contextdb_cli.py health
python3 .claude/hooks/contextdb_cli.py verify
```

見るべき項目:

- `integrity=ok`
- `pending_spool=0`または継続的に減少している
- `quarantined_spool=0`
- `event_hashes.ok=true`
- DB sizeとevent countが想定範囲

## spoolが残る場合

```bash
python3 .claude/hooks/contextdb_cli.py drain
```

それでも残る場合:

1. `.claude/contextdb/health/errors.jsonl`を確認
2. filesystem容量・permissionを確認
3. DBを開いている長時間transactionを終了
4. `verify`を実行

spool fileはredacted済みですが、解決前に削除しないでください。

## quarantine

不正JSONまたはschema不整合のspoolは `.claude/contextdb/spool/quarantine/` へ移動します。内容を確認して不要なら削除します。

## retention

```bash
python3 .claude/hooks/contextdb_cli.py prune
```

既定30日です。緊急削除例:

```bash
python3 .claude/hooks/contextdb_cli.py prune --days 0
```

これはraw eventだけを削除し、durable memoryは残します。memoryの撤回は `memory retract` を使用します。

## recovery config

`.claude/contextdb/config.json` の `recovery` sectionには次のキーがあります。

| key | default | purpose |
|---|---:|---|
| `max_chars` | 12000 | recovery packet全体の最大文字数 |
| `files_budget_chars` | 2000 | file sectionの最大文字数 |
| `recent_events` | 12 | 取得する直近event数 |
| `recent_prompts` | 4 | 取得する直近prompt数 |
| `recent_files` | 12 | 取得する直近file数 |
| `recent_failures` | 5 | 取得する直近failure数 |
| `include_project_memories` | `true` | project memoryを含めるか |

## deterministic recovery probes

`probe` は指定sessionの台帳を読み、利用可能なrecall / artifact / decision / continuation probeだけをground truth付きで返します。LLM・network・DB writeは実行しません。

```bash
python3 .claude/hooks/contextdb_cli.py probe --session <session_id> --json
```

JSON schema:

```json
{"probes":[{"type":"artifact","question":"Which files were modified in this session?","ground_truth":"src/app.py (edit, 2x)"}]}
```

## query-conditioned recall

```bash
python3 .claude/hooks/contextdb_cli.py recall "query" --session <session_id> --k 5 --json
```

`recall.rho`はlexical scoreの重み、`recall.k`は既定出力件数です。semantic embeddingが無効または未保存なら、外部commandを呼ばずlexical scoreだけを使います。recall自体はDBへ書き込みません。

| key | default | constraint |
|---|---:|---|
| `recall.rho` | 0.6 | 0以上1以下のnumber |
| `recall.k` | 5 | 0以上のinteger |

workerはタスク開始時のcontext再取得に使い、orchestratorはacceptance時の過去failure照合に使います。

## backup

Claude Code停止後、次をbackupできます。

- `.claude/contextdb/state/context.db`
- `.claude/contextdb/state/project-id`
- `.claude/contextdb/config.json`

WAL mode中のonline copyはDB、`-wal`、`-shm`の整合が必要です。確実性を優先する場合はClaude Codeを停止してcopyします。`project-id`を失うと同じDBを新しいproject identityとして参照できなくなるため、必ず同じbackup setへ含めます。

## upgrade

新しいpackageの `install.py --project ...` を再実行します。既存configは上書きせず、runtimeとhook wrapperを更新します。

## release validation

展開前またはupgrade前にpackage rootで実行します。

```bash
PYTHONDONTWRITEBYTECODE=1 python3 validate.py
```

required checkが一つでも失敗すると終了code 1です。Claude Code executableがない環境では、その実機E2E checkだけがoptional skipとなります。
