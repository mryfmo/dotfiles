# Claude Code hook mapping

仕様確認日: 2026-07-31

公式reference: `https://code.claude.com/docs/en/hooks`

| hook | mode | stored information |
|---|---|---|
| `SessionStart` | async logger | source, model, title, agent type |
| `SessionStart:compact` | sync recovery | same-session bounded recovery packet |
| `recovery_injected` (internal) | durable spool | injected recovery packet, summary, stored-detail SHA-256 |
| `UserPromptSubmit` | async | redacted prompt |
| `PostToolUse` | async | successful tool input/response, duration, tool_use_id |
| `PostToolUseFailure` | async | failed tool input, error, interrupt flag, duration |
| `PermissionDenied` | async | denied tool/input and reason |
| `PreCompact` | sync | trigger, custom instructions |
| `PostCompact` | sync | trigger, generated compact_summary |
| `Stop` | async | final assistant message |
| `StopFailure` | async | error type, error details, rendered API error message |
| `SubagentStart` | async | agent identity and agent type |
| `SubagentStop` | async | agent identity and final message |
| `TaskCreated` | async | task ID, subject, description, teammate |
| `TaskCompleted` | async | completed task ID, subject, description, teammate |
| `SessionEnd` | sync | end reason |

## output discipline

`contextdb_hook.py`はstdoutへ何も出力しません。`contextdb_recover.py`だけがSessionStartのstructured JSONをstdoutへ一つ出力します。

## async policy

Claude Code hookはdefaultで処理完了までagentをblockします。頻繁なlogging hookは`async: true`にしています。Compaction boundaryは順序を保証するためsyncです。

## matcher policy

match-allには現行仕様の `"*"` を使用しています。matcherをsupportしないeventではmatcher fieldを付けていません。

## scope decision

`PostToolBatch`は各`PostToolUse`/`PostToolUseFailure`と重複し、大きなserialized tool resultを再保存するため既定では登録していません。batch単位の監査が必要なprojectでは、同じlogger wrapperを`PostToolBatch`へ追加できます。

## recovery packet audit event

`SessionStart:compact`はpacketを完全に構築した後、structured responseを返す直前に`recovery_injected` eventをspoolします。`detail.recovery_packet`は既存のcapture detail上限に従い、`detail_sha256`は上限適用後のstored `detail_json`をhashします。response pathはこの新規eventを同期drainせず、後続drainがledgerへ反映します。記録失敗はhealth errorを1行残しますが、注入responseは変更しません。構築後に記録するためpacketは自身を含まず、次回packetでは直前の`recovery_injected`を通常eventとして参照できます。
