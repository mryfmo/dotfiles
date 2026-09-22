# dot-ubuntu-parity-T1-a01 — make upgrade 残骸の chore コミット(main 直、push は承認後)

## Objective(操作者決定 2026-09-23)

spark-9e8d 上の `make upgrade` 産物 3 ファイルが dirty のままで、`Makefile:53` の
ガードにより `make update` が git pull しない状態を解消する。これは #168 マージ後に
このマシンで走った新しい upgrade の産物であり(dotenvx 2.24.1→2.26.1, uv
0.12.13→0.12.15, gh 2.100.0→2.101.0, claude-code 2.1.278→2.1.280 — いずれも実機で
稼働中のバージョンと一致)、破棄ではなく chore コミットが正
[memory:decision] spark の 2026-09-23 時点 dirty mise pair は #168 後の新規 upgrade 産物であり commit する(旧「破棄」決定は pre-#168 pair にのみ適用)。

## Work items

1. `git status -sb` で dirty が対象 3 ファイルのみであることを確認(逐語で validation へ)。
2. `uv run python -m unittest tests.unit.test_supply_chain_policy` を実行し green を確認
   (config と lock の整合検証)。逐語出力を validation へ。
3. main 上でコミット 2 件を作成(push はしない):
   - `chore(mise): sync live tool pins from make upgrade` — `home/dot_mise/config.toml` + `home/dot_mise/mise.lock`(先例: 5aaaafb)
   - `chore(ccstatusline): migrate settings to v4 schema` — `home/dot_ccstatusline/settings.json`
     各コミットメッセージ末尾に `Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>` を付ける。
4. `git log --oneline -3` と `git show --stat` 2 件分を逐語で validation へ。
5. コミット後 `git status -sb` がクリーン(.orchestration / worklog を除く)であることを確認。
6. CompactionDB: `python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project` で
   上記 [memory:decision] を登録し、実行コマンドと出力(ID を含む)を report と validation に逐語で残す。

## Scope

allowed_files: `home/dot_mise/config.toml`, `home/dot_mise/mise.lock`,
`home/dot_ccstatusline/settings.json`(いずれも既存差分のコミットのみ、内容変更禁止),
`.orchestration/{reports,validation,sandboxes,learning,autoskill/runs}/dot-ubuntu-parity-T1-a01.md`,
`.agents/worklog/codex/**`

forbidden_actions: push 禁止(オーケストレータ承認後)、対象 3 ファイルの内容変更禁止、
上記以外のファイル変更禁止(出たら revert して報告)、ブランチ作成禁止(main 直)、
`make upgrade` 再実行禁止、chezmoi apply 禁止。

## 完了

done_signal=AGMSG-RESULT。max_turns=15。cost 行を report に。

## 追記(2026-09-23 オーケストレーター)

Codex 未ログインでワーカー起動不能のため、本タスクはグローバルルール
「make upgrade の mise config/lock ペアはセッション内で独自 chore コミット」に基づき
オーケストレーターが直接実施(統合ブックキーピング免除)。ワーカー委譲は撤回。
