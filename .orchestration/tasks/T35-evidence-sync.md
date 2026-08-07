# Orchestration task: T35 sync T33/T34 evidence

- Task ID: `T35-evidence-sync`
- Repo: `/Users/mryfmo/Workspace/dotfiles`（main worktree。`git checkout main && git pull --ff-only origin main` の後、ブランチ `chore/t35-evidence-sync` を作成）
- 発行: claude-deep-dot（orchestrator）2026-08-07
- 担当: codex-standard-dot（herdr pane w1C:pF, `codex --profile standard`）
- 受入: claude-deep-dot

## Scope

1コミット `chore(orchestration): sync T33/T34 evidence` に、現在 untracked の証跡をすべて含める:

- `.orchestration/tasks/T33-*.md` `.orchestration/tasks/T34-*.md` `.orchestration/tasks/T35-evidence-sync.md`（本ファイル）
- `.orchestration/reports/T33-*.md` `.orchestration/reports/T34-*.md`
- `.orchestration/validation/T33-*.md` `.orchestration/validation/T34-*.md`
- `.orchestration/sandboxes/` `.orchestration/learning/` `.orchestration/autoskill/runs/` の T33/T34 ファイル
- `.orchestration/learning/ORCH-2026-08-05-regime-breach.md`
- `.agents/worklog/claude/T33-review-receipt.md`（gitignore されている場合は除外し、report で言及のみ）

内容の書き換えは禁止（バイトそのままコミット）。push → PR（base=main）→ checks green → AGMSG-RESULT。merge はしない。

## Forbidden actions

- 証跡ファイルの内容変更、上記以外の編集、依存変更、merge、force push

## 完了報告

```
AGMSG-RESULT v1 task_id=T35-evidence-sync status=ready_for_review|blocked report=.orchestration/reports/T35-evidence-sync.md validation=.orchestration/validation/T35-evidence-sync.md sandbox=.orchestration/sandboxes/T35-evidence-sync.md learning=.orchestration/learning/T35-evidence-sync.md autoskill=.orchestration/autoskill/runs/T35-evidence-sync.md
```

（T35 自身の証跡5ファイルは converged tail として次回 sync に残る）
