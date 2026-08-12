# Validation report — CompactionDB 2.0.0

検証日: 2026-07-31  
検証環境: Linux 6.12.13 x86_64 / Python 3.13.5 / SQLite 3.46.1

## 判定

**必須検証はすべて合格しました。**

- required checks: 9 passed / 0 failed
- optional checks: 1 skipped
- standard-library unit/integration tests: 39 passed
- `ResourceWarning`: error扱いで0件
- installed-project smoke: passed

機械可読な全結果は `docs/validation-results.json` に保存しています。

## 実施した検証

| 区分 | 結果 | 内容 |
|---|---:|---|
| Python runtime | PASS | Python 3.10以上を確認 |
| source syntax | PASS | 34 Python fileをAST parse |
| JSON | PASS | configと3種類のsettingsをparse |
| hook settings | PASS | 3 settings document、45 command handlerのevent、command、args、timeoutを検査 |
| runtime import | PASS | `contextdb` 2.0.0と主要moduleをimport |
| unit/integration | PASS | 39 tests |
| installer | PASS | 別projectへ2回installし、冪等性と既存unrelated hook保持を確認 |
| hook ingest | PASS | 実wrapper経由でUserPromptSubmitとPostCompactを投入 |
| security | PASS | test secretがspool、DB、recovery contextへ残らないことを確認 |
| integrity | PASS | SQLite quick checkと全event detail SHA-256を確認 |
| compaction recovery | PASS | exact sessionのPostCompact summaryとdurable memoryをstructured SessionStart outputへ復旧 |
| release cleanliness | PASS | DB、WAL、lock、pycache、bytecodeを配布treeへ含めないことを確認 |
| Claude Code executable | SKIP | 検証環境に`claude` executableが存在しないため、UI上のauto-compaction E2Eは未実施 |

## 主要な退行テスト

テストsuiteでは少なくとも次を直接再現しています。

1. 別sessionのraw eventがCompaction recoveryへ混入しない
2. SQLiteが排他lock中でもeventがspoolに残り、後続drainで保存される
3. 32個の並行hook processが全eventを保存する
4. duplicate `event_uuid`が二重登録されない
5. invalid spoolがquarantineされる
6. PostToolUseFailureのerror情報を保持する
7. PostCompact summaryをsession memoryへ昇格する
8. heuristic memoryがproject scopeへ自動流出しない
9. project directory移動後もproject identityが変わらない
10. 初回の並行起動が一つのproject identityへ収束する
11. API token、private key、sensitive file内容を永続化前に除去する
12. 大きなdetailを制限してもJSONが壊れない
13. 日本語substringをFTS5 trigramまたはfallbackで検索できる
14. raw retentionでeventを削除してもdurable memoryを維持する
15. supersession/retractionが追記型履歴として残る
16. legacy DB importが冪等かつredactedである
17. installerが従来のCompactionDB hookだけを置換し、他のhookを維持する
18. 同一内容のsession memoryをsession間で誤deduplicateしない
19. SQLiteの保守的な変数上限を超える1,005件のraw eventをbatch pruneできる
20. StopFailureの`error_details`と表示messageを失わない
21. SubagentStartとTaskCreated/TaskCompletedを公式fieldで正規化する

## 未検証・残存制約

- Claude Code executableがないため、`/hooks`表示、実auto-compaction、resumeを含むUI E2Eは未実施
- Windows native code pathとACLはLinux上の自動testでは未実行
- secret redactionはbest effortであり、完全なDLPではない
- application-level encryption at restは未実装
- semantic searchは外部embedding commandを設定した場合のみ有効
- memory extractionはheuristicであり、LLMによるentity resolutionや矛盾判定は行わない

これらは配布物の `docs/KNOWN_LIMITATIONS.md` と `docs/SECURITY.md` にも明記しています。
