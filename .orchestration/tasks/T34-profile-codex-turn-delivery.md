# Orchestration task: T34 restore turn delivery for profile-launched codex

## Assignment

- Task ID: `T34-profile-codex-turn-delivery`
- Repo: `/Users/mryfmo/Workspace/dotfiles`（main worktree。開始時に `git checkout main && git pull --ff-only origin main` の後、ブランチ `fix/t34-profile-hooks-parity` を作成）
- 発行: claude-deep-dot（orchestrator）2026-08-07
- 担当: codex-standard-dot（herdr pane w1C:pE, `codex --profile standard` = gpt-5.6-terra / reasoning medium）
- レビュー・受入: claude-deep-dot（orchestrator）。**delivery hooks に関わる変更のため、受入には
  orchestrator 実施の live E2E（fresh profile session での turn 配送実証）を含める**
- max_turns: 30

## 観測された欠陥（2026-08-07 実測）

`codex --profile deep` / `--profile standard` で起動した resident worker は、リポジトリ tree-scoped
`.codex/hooks.json` の Stop フック（agmsg `check-inbox.sh`）が一切発火せず、**turn 配送が無効**。
ターン終了後も worker 宛メッセージの `read_at` が付かないことで確認した。素の `codex`
（`~/.codex/config.toml`）では 7月に turn 配送が機能していた。

状態の非対称（実測）:

- `~/.codex/config.toml`: `[features] hooks = true` があり、`[hooks.state]` に
  `/Users/mryfmo/Workspace/{ai-ops-platform,dotfiles}/.codex/hooks.json:stop:0:0` の
  trusted_hash エントリが存在する
- `~/.codex/standard.config.toml`: `[hooks.state]` は permission_request 1件のみ。repo hooks の trust なし
- `~/.codex/deep.config.toml`: hooks 関連の記述なし（`hooks = true` すら無い可能性）

## Scope

1. **調査を先に行い、結果を validation に記録する**（推測で実装しない）:
   - codex 0.146 が `--profile <name>` 時にどの config をどう解決するか（`<name>.config.toml` の
     読み込み実態、`~/.codex/config.toml` とのマージ有無）
   - 未 trust の tree-scoped フックを 0.146 が「無言でスキップ」するのか「trust プロンプトを出す」のか
   - trusted_hash の算出対象（何の hash か）
2. 調査結果に基づき、**プロファイル起動セッションでも default config と同等の hooks 有効化・
   trust 状態が保たれる**ようにする。実装先は既存の生成/保全パターンに従う
   （`scripts/generate-agent-configs.py` / `home/dot_codex/modify_*.config.toml` /
   必要なら `home/dot_agents/agent-config.yaml` の manifest 項目追加）。
   **trust の意味を弱める変更（hash 検証の無効化・全フック自動信頼など）は禁止**。
3. ユニットテストで生成物の対称性（プロファイル config にも hooks 有効化＋trust 保全が乗ること）を固定。

## 判断が必要になったら（status=blocked で報告）

- 0.146 の仕様上、プロファイル config に trust を安全に供給する経路が存在しない場合
- 解決に codex 本体のバージョン変更や approval policy の変更が必要と判明した場合（これは operator 裁定事項）

## Allowed files

```
scripts/generate-agent-configs.py
scripts/validate-agent-assets.py
home/dot_agents/agent-config.yaml
home/dot_codex/modify_deep.config.toml
home/dot_codex/modify_express.config.toml
home/dot_codex/modify_review.config.toml
home/dot_codex/modify_standard.config.toml
tests/unit/test_generate_agent_configs.py
tests/unit/test_validate_agent_assets.py
```

## Forbidden actions

- allowed_files 以外の編集
- `chezmoi apply` / `make update`（live 反映は orchestrator 側）
- `~/.codex/` 配下（HOME の実ファイル）の直接編集
- trust/hash 検証を弱める変更、approval_policy の変更
- 依存関係の追加・更新、merge、force push

## Validation

- 調査結果（config 解決・trust 挙動・hash 対象）を根拠付きで validation ファイルに記録
- `make unit-test` などリポジトリ標準ゲート green
- 生成物の再生成が決定的であること（2回実行で差分なし）
- push → PR（base=main）→ checks green。merge はしない

## 完了報告

```
AGMSG-RESULT v1 task_id=T34-profile-codex-turn-delivery status=ready_for_review|blocked report=.orchestration/reports/T34-profile-codex-turn-delivery.md validation=.orchestration/validation/T34-profile-codex-turn-delivery.md sandbox=.orchestration/sandboxes/T34-profile-codex-turn-delivery.md learning=.orchestration/learning/T34-profile-codex-turn-delivery.md autoskill=.orchestration/autoskill/runs/T34-profile-codex-turn-delivery.md
```
