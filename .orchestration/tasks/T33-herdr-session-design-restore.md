# Orchestration task: T33 restore the herdr-session lazy-attach design

## Assignment

- Task ID: `T33-herdr-session-design-restore`
- Repo: `/Users/mryfmo/Workspace/dotfiles`（main worktree で作業。開始時に
  `git checkout main && git pull --ff-only origin main` の後、
  ブランチ `fix/t33-herdr-session-restore` を作成）
- 発行: claude-deep-dot（orchestrator）2026-08-07
- 担当: codex-standard-dot（herdr pane w1C:pE, `codex --profile standard` = gpt-5.6-terra / reasoning medium）
- レビュー・受入: claude-deep-dot（orchestrator。merge はタスクに含めない）
- max_turns: 20

## 背景（なぜ戻すのか）

PR #75（`cab6de1`）は「lazy single-terminal start」を意図的に採用した:
`herdr-session` は素の端末で attach するだけで、エージェント pane は Claude の
SessionStart hook が遅延追加する。PR #105（`57bcfde`）はこの設計を
T番号タスク・証跡なしで反転させ、`focus_launch_workspace()`（起動ディレクトリごとに
workspace を focus/create してから attach）を追加した。live desktop 挙動を変える変更に
必要な fresh session + persisted-session restore の E2E 検証も記録されていない。
本タスクは #75 の設計へ復元する。

## Scope

1. `home/dot_local/bin/common/executable_herdr-session` を **`57bcfde^` 時点の内容へ復元**する
   （`git show 57bcfde^:home/dot_local/bin/common/executable_herdr-session` とバイト一致させる。
   `focus_launch_workspace()` と呼び出し、およびヘッダ/usage 文言の変更をすべて戻す）。
2. `tests/unit/test_herdr_agents.py` のうち **#105 が focus_launch_workspace のために追加した
   テストのみ**を除去する（`git show 57bcfde -- tests/unit/test_herdr_agents.py` で追加分を特定し、
   無関係な既存テストは残す）。
3. コミットメッセージに「#75 の lazy-attach 設計への復元であり、#105 が
   タスク・検証記録なしに反転させた挙動を戻す」旨を書く。

## Allowed files

```
home/dot_local/bin/common/executable_herdr-session
tests/unit/test_herdr_agents.py
```

## Forbidden actions

- allowed_files 以外の編集（#105 の他の内容 — mise バンプ、CI 修正、statusline pin — には触れない）
- `chezmoi apply` / `make update` の実行（live 反映は orchestrator 側で行う）
- 依存関係の追加・更新
- merge、force push、他ブランチへの push

## Validation

- 復元ファイルが `57bcfde^` 版とバイト一致することを `git diff --no-index` で示す
- リポジトリ標準ゲート（`make unit-test` 等、Makefile にある検証ターゲット）を実行し、
  出力を validation ファイルへ記録
- push → PR（base=main）→ checks green。**merge はしない**

## 完了報告

```
AGMSG-RESULT v1 task_id=T33-herdr-session-design-restore status=ready_for_review|blocked report=.orchestration/reports/T33-herdr-session-design-restore.md validation=.orchestration/validation/T33-herdr-session-design-restore.md sandbox=.orchestration/sandboxes/T33-herdr-session-design-restore.md learning=.orchestration/learning/T33-herdr-session-design-restore.md autoskill=.orchestration/autoskill/runs/T33-herdr-session-design-restore.md
```
