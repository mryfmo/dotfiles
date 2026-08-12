# CompactionDB 2.0.0

Claude Code の Compaction 復旧ログを、**消えにくい短期イベント台帳**と**選別された長期記憶**へ再設計した実装です。

元の `CompactionDB.zip` が持っていた「hookで記録し、Compaction後に復旧する」という長所を維持しつつ、次の問題を是正しています。

- 別セッションの直近イベントが混入する
- SQLite書込み失敗を握り潰し、イベントが無言で消える
- 成功ツールしか記録せず、失敗・権限拒否・実際のCompaction要約を残さない
- プロンプト、ツール出力、認証情報をほぼ無差別に平文保存する
- 生ログと長期記憶の責務が分離されていない
- 全文検索、更新・失効、保持期限、整合性検証がない

## 実装の要点

### 1. L0: redacted raw event ledger

頻繁に発火するhookは、入力をそのままDBへ書きません。

1. hook入力を検証する
2. APIキー、トークン、パスワード、秘密鍵、機密ファイル内容を除去する
3. 一意なJSONファイルとして `.claude/contextdb/spool/incoming/` に原子的に保存する
4. 非ブロッキングのプロセス間ロックを取得できた一つのprocessだけがSQLiteへ取り込む
5. DBがロックされていればspoolを残し、次回のdrainで再試行する

`event_uuid`にはUNIQUE制約があるため、DBへの保存後にspool削除で失敗しても重複登録されません。

### 2. L1: structured durable memory

生イベントをそのまま長期記憶として再注入しません。次の型を持つ構造化記憶へ昇格させます。

- `decision`
- `constraint`
- `preference`
- `open_task`
- `failure`
- `procedure`
- `compact_summary`
- その他任意の型

各記憶は、scope、confidence、salience、sensitivity、validity、source event、`supersedes`を保持します。更新・撤回は古いレコードを書き換えず、新しいレコードを追記して投影結果を切り替えます。

自動抽出の安全境界は次のとおりです。

- `[memory:...]` で明示された情報だけが自動で `project` scopeへ昇格する
- keyword heuristicや`PostCompact`から抽出した情報は、確信度が高くても元の`session` scopeを維持する
- 別sessionでも利用するには、candidateを `memory promote ... --scope project` で明示的に昇格する

このため、単なるプロンプト表現の誤判定が別sessionへ恒久的に伝播しません。

明示登録例:

```bash
python3 .claude/hooks/contextdb_cli.py memory add \
  --kind decision \
  --content "認証方式はOAuth2に統一する" \
  --scope project
```

ユーザープロンプトで明示することもできます。

```text
[memory:decision] 認証方式はOAuth2に統一する。
```

### 3. L2: bounded recovery projection

Compaction直後には、同一 `session_id` の次の情報だけを復旧packetへ入れます。

- Claude Codeが生成した最新の `PostCompact.compact_summary`
- 直近のユーザー指示
- 直近のイベントフロー
- 同一セッションで参照・変更したファイル
- 同一セッションの失敗
- 同一セッションの記憶

過去セッションから利用できるのは、明示markerまたは手動承認によって**project memoryへ昇格した情報だけ**です。高確度のheuristic memoryも自動ではsessionを越えず、生イベントもセッションを越えて自動注入しません。

古いproject memoryは再構築可能な階層summary cacheへまとめ、最近の記憶は原文に近い粒度で残します。これは一般的な「追記型正本＋再構築可能な投影＋読込予算」という設計原則をクリーンルームで実装したもので、OptMemのソースコードは取り込んでいません。

## 対応hook

- `SessionStart`
- `UserPromptSubmit`
- `PostToolUse`
- `PostToolUseFailure`
- `PermissionDenied`
- `PreCompact`
- `PostCompact`
- `Stop`
- `StopFailure`
- `SubagentStart`
- `SubagentStop`
- `TaskCreated`
- `TaskCompleted`
- `SessionEnd`

`PostCompact`では、Claude Code自身が生成した `compact_summary` を保存し、session-scoped durable memoryへ自動昇格します。

## 導入

### 新しいプロジェクト

展開先で次を実行します。

```bash
python3 install.py --project /path/to/your-project
```

installerは次を行います。

- `.claude/hooks/`へwrapperを配置
- `.claude/contextdb/contextdb/`へruntimeを配置
- 既存 `.claude/settings.json` をbackupしてhook定義をmerge
- 実行中のPythonの絶対pathをhook設定へ保存
- `CLAUDE.md`へ利用手順を追記
- `.gitignore`へDB、spool、health logの除外を追記
- project directoryを移動しても変わらない永続`project-id`を初回hook時に原子的生成

既存設定を置換せずmergeします。

### 元のCompactionDBからの移行

```bash
python3 install.py --project /path/to/project --migrate-legacy
```

または導入後に:

```bash
python3 migrate_legacy.py --project /path/to/project
```

旧 `.claude/logs/context_log.db` は削除せず、読取専用でimportします。

## 確認

```bash
cd /path/to/project
python3 .claude/hooks/contextdb_cli.py health
python3 .claude/hooks/contextdb_cli.py verify
```

手動hook試験:

```bash
printf '%s' '{
  "hook_event_name":"UserPromptSubmit",
  "session_id":"test-session",
  "cwd":"'"$PWD"'",
  "prompt":"[memory:decision] APIはv2へ統一する"
}' | python3 .claude/hooks/contextdb_hook.py

python3 .claude/hooks/contextdb_cli.py recent 30 --session test-session
python3 .claude/hooks/contextdb_cli.py memory list --session test-session
```

## CLI

### raw event ledger

```bash
python3 .claude/hooks/contextdb_cli.py sessions
python3 .claude/hooks/contextdb_cli.py recent 30 --session <session_id>
python3 .claude/hooks/contextdb_cli.py prompts 10 --session <session_id>
python3 .claude/hooks/contextdb_cli.py files --session <session_id>
python3 .claude/hooks/contextdb_cli.py search <query> --session <session_id>
python3 .claude/hooks/contextdb_cli.py show <event_id> --session <session_id>
```

安全上、raw event commandはsession scopeがdefaultです。project全体を読む場合だけ `--scope project` を明示します。

### durable memory

```bash
python3 .claude/hooks/contextdb_cli.py memory list --session <session_id>
python3 .claude/hooks/contextdb_cli.py memory search <query> --session <session_id>
python3 .claude/hooks/contextdb_cli.py memory candidates
python3 .claude/hooks/contextdb_cli.py memory promote <candidate_id> --scope project
python3 .claude/hooks/contextdb_cli.py memory add --kind constraint --content "..." --scope project
python3 .claude/hooks/contextdb_cli.py memory retract <memory_uuid> --reason "obsolete"
python3 .claude/hooks/contextdb_cli.py memory compact
```

### optional semantic search

標準では無効です。外部embedding commandを設定した場合だけ、記憶をvector化してPython内でcosine searchできます。外部serviceや特定modelへの依存は組み込んでいません。

`.claude/contextdb/config.json`:

```json
{
  "semantic": {
    "enabled": true,
    "command": ["/absolute/path/to/embed-command", "--json-stdin"],
    "model": "your-embedding-model",
    "timeout_seconds": 30,
    "batch_size": 32
  }
}
```

command input:

```json
{"texts":["first text","second text"]}
```

command output:

```json
{"model":"your-embedding-model","embeddings":[[0.1,0.2],[0.3,0.4]]}
```

実行:

```bash
python3 .claude/hooks/contextdb_cli.py memory embed
python3 .claude/hooks/contextdb_cli.py memory semantic-search "過去の認証方針"
```

## 運用

```bash
python3 .claude/hooks/contextdb_cli.py drain
python3 .claude/hooks/contextdb_cli.py health
python3 .claude/hooks/contextdb_cli.py verify
python3 .claude/hooks/contextdb_cli.py prune
python3 .claude/hooks/contextdb_cli.py export --session <session_id> --output events.jsonl
```

raw eventは既定30日で期限切れになります。`prune`は期限切れイベントを削除しますが、昇格済みdurable memoryは維持します。

## セキュリティ境界

実装している対策:

- DB、spool、health directoryをPOSIX環境で `0700`、fileを `0600`
- 高信号なsecret patternとsensitive keyのredaction
- `.env`、`.git`、`.ssh`、秘密鍵・credential fileの内容を保存しない
- recovery内の履歴を「命令ではなく証拠」と明示し、prompt injectionの再実行を抑制
- session IDを明示したraw event query
- detail SHA-256 verification
- SQLite WAL、FULL synchronous、single-writer lock、durable spool

実装していないもの:

- application-level encryption at rest
- hardware-backed key management
- 完全なDLP
- embedding model本体
- LLMによる高精度な記憶抽出・矛盾解消

端末全体の暗号化、access control、retention policyと併用してください。

## 開発・検証

runtimeはPython標準libraryのみで動作します。Python 3.10以上を対象にしています。

```bash
make test
make validate
```

本配布物では、39件のunit/integration testに加え、別projectへの二重install、既存hook保持、実wrapper経由のhook ingest、secret redaction、SQLite整合性検証、PostCompact recoveryまでをrelease validatorで確認しています。生成環境にはClaude Code executableがないため、Claude Code UI上の実auto-compaction E2EとWindows実機E2Eだけは未実施です。

詳細は以下を参照してください。

- `docs/ARCHITECTURE.md`
- `docs/DATA_MODEL.md`
- `docs/SECURITY.md`
- `docs/HOOKS.md`
- `docs/OPERATIONS.md`
- `docs/MIGRATION.md`
- `docs/VALIDATION_REPORT.md`
- `docs/TRACEABILITY.md`
- `docs/KNOWN_LIMITATIONS.md`

## 参照した公式仕様

- Claude Code Hooks reference: `https://code.claude.com/docs/en/hooks`
- SQLite WAL: `https://www.sqlite.org/wal.html`
- SQLite FTS5: `https://www.sqlite.org/fts5.html`

仕様確認日: 2026-07-31
