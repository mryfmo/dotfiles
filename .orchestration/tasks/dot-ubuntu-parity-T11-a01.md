# dot-ubuntu-parity-T11-a01 — herdr-agents に worker-kind スイッチを追加

## Objective(操作者指摘 2026-09-23)

`home/dot_local/bin/common/executable_herdr-agents` の管理された lifecycle
(専用 workspace 作成 --focus 付き、claude-orchestrator + ワーカーのペイン対、
プロンプト待ち、ペイン順序/比率修復、attach 修復、bootstrap_agmsg)は
**ワーカー種別 = codex のみハードコード**。Codex が使えない環境(未ログイン等)で
Claude Code ワーカーへ切り替えられるよう、既存機構を**継承したまま**スイッチを追加する。
今セッションで手動実装により再発明した問題(画面不可視・trust ダイアログ・規約外ペイン)を
機構側で恒久解消するのが目的。

## Work item(1 コミット: `feat(herdr-agents): support a claude worker kind alongside codex`)

- 新 env `HERDR_AGENTS_WORKER_KIND`(`codex`|`claude`、**既定 codex** — env 未設定時の挙動は
  現行とバイト単位で同一に保つ)。
- 一般化(既存関数の最小改名/引数化。挙動保存を最優先):
  - `resolve_codex_profile` → worker 共通の profile 解決(既存 env 名
    `HERDR_AGENTS_CODEX_PROFILE` は後方互換で維持しつつ、kind 非依存の
    `HERDR_AGENTS_WORKER_PROFILE` を優先追加)。
  - `start_codex_agent` → `start_worker_agent`: kind=codex は現行どおり
    `--sandbox workspace-write --profile <p>`。kind=claude は
    `~/.agents/model-profiles.env` の `MODEL_PROFILE_<PROFILE大文字>_CLAUDE_ARGS` を
    読んで引数化し、追加引数は `HERDR_AGENTS_CLAUDE_WORKER_ARGS` で注入可能に。
  - agent 名/ペインラベル `codex-worker`(`agent_name_for_workspace codex-worker …`、
    `live_codex_pane_id`、rename)を `<kind>-worker` に一般化。attach 修復
    (`attach_panes_are_unambiguous` 等)が claude ワーカーのペインも managed と
    認識することを含めて整合させる。
  - `require_command codex` を kind に応じて `require_command "$kind"` に。
  - claude ワーカー起動時の workspace 信頼ダイアログ(デフォルト No, exit)への対処:
    既存の wait/prompt 機構の流儀で、ダイアログ検出時に Down+Enter で
    「Yes, I trust this folder」を選ぶ処理を start_worker_agent(claude 分岐)に追加。
    検出は `herdr pane wait-output --match 'trust this folder'` を短 timeout で。
- `bootstrap_agmsg` の identity 案内メッセージが kind を反映すること(現行は
  codex/claude-code 両方チェックしており変更最小のはず — 確認のみで可)。
- shdoc コメント更新、`--help`/usage に env を 1 行追記。
- テスト: `tests/unit/test_herdr_agents.py`(存在すれば)に kind スイッチの
  引数組立てケースを追加。bats があれば追従。モックベース新規テストは
  `bats -f` / unittest 個別実行で逐語検証。
- `make format` / `make validate-agent-assets` / `make unit-test` green。

## Scope

allowed_files: `home/dot_local/bin/common/executable_herdr-agents`,
`home/dot_agents/model-profiles.env`(読み取りのみ・変更禁止), `tests/**`, `README.md`,
`.orchestration/{reports,validation,sandboxes,learning,autoskill/runs}/dot-ubuntu-parity-T11-a01.md`,
`.agents/worklog/codex/**`

forbidden_actions: push 禁止、PR 作成禁止、chezmoi apply 禁止、`$HOME` 配下の変更禁止、
main への直コミット禁止、herdr の実セッション操作禁止(このマシンの稼働中 herdr に触れない —
検証はモック/ドライで)、対象外 bats 実行禁止。
agmsg は自分の inbox(claude-standard-dot)読みと最後の send.sh 1 通のみ。

## 手順

git fetch origin && git checkout -b feat/herdr-agents-worker-kind origin/main で開始。
done_signal=AGMSG-RESULT。max_turns=40。cost 行を report に。
