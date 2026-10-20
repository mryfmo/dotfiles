# Plan 024 チェックリスト（作業終了時に読むもの）: 第 1 段階の退出条件 DoD-P1 と全体の完了の定義 DoD

> 読み方: 各波の終わりと boundary で orchestrator が上から順に確かめ、結果（コマンドと出力）を `024-progress.tsv` と boundary 記録に書く。満たさない行があれば第 2 段階に進まない。

## 第 1 段階の退出条件（DoD-P1。a〜p をすべて満たしてから第 2 段階へ）

| # | 確認 | 期待 |
| --- | --- | --- |
| P1-a | plan 第 3 節の分類表 | merge は全部マージ済み、close は閉じている、hold は #395 のみ |
| P1-b | `gh api repos/mryfmo/dotfiles/rulesets/24397953` と main の push CI | strict false、thread resolution false、必須チェック 7、HEAD 緑 |
| P1-c | `chezmoi verify`、`git -C ~/.local/share/chezmoi rev-parse HEAD` | rc 0、origin/main に一致 |
| P1-d | 連続 2 波（3〜5 時間）の bus 履歴（`history.sh` を `timeout 60` で）。24 時間の統計は第 2 段階中に監視として続ける | 席の idle ≤ 15 分、orchestrator の PONG 待ち ≤ 20 分 |
| P1-e | 統合ログと verdict | 席が完走した統合 ≥ 2、Bot 待ちの行 0、verdict.sh が判定した PR ≥ 4、orchestrator の 1 PR あたりの処理（verdict 読みからマージまで）≤ 5 分 |
| P1-f | 受け入れ記録 | `precheck=` のある RESULT のみ受理、直近 10 PR の revise 率 ≤ 20% |
| P1-g | `.github/workflows/{test,remote,agent-assets}.y*ml` | `concurrency` あり、`private-bootstrap` に `pull_request` なし、bootstrap パス非変更 PR の macOS ジョブ ≤ 1 |
| P1-h | 並列稼働の実証 | 1 つの波で 4 席が互いに素なタスクを同時に進め、全 RESULT が同日中に受け入れられる。同時に design-quality 5.8 の計測（受け入れ待ち、マージ/時、CI の queued 時間、監査待ち、rate-limit 停止、`gh api rate_limit`、CPU/メモリ）を boundary 記録に残す |
| P1-i | 監査 | `audit-<head>.json` が schema 緑、revise 後の差分監査 ≤ 5 分、同時 2 本の実績 |
| P1-j | 品質の校正（design-quality 5.11 Q-C） | `.orchestration/validation/verdict-shadow.tsv` で機械判定と手判定の一致が連続 4 件、差分監査と全差分監査の所見差 0 が 2 件。満たすまで `--apply` と差分監査は無効 |
| P1-k | 品質指標（design-quality 5.11 Q-D） | 連続 2 波で main の push CI 赤 ≤ 1 回かつ根本原因記録済み、escaped defect 0、監査 P0/P1 のマージ後検出 0、not-applicable 比率 ≤ 30% |
| P1-l | 仕組みの監査 | P1-3、P1-4a、P1-4、P1-5、P1-6、P1-7、P1-10〜P1-14 の各 PR に task-level audit と security review（`--profile security`）の両方の verdict=correct、threat_table 全行 disposition 済み |
| P1-m | precheck の強制 | `PRECHECK_REQUIRED=1` に切り替え済み（4 席すべてが P1-5 を含む main 由来のブランチであることを `git merge-base --is-ancestor` で確認した記録付き）、progress.tsv に時刻 |
| P1-n | `make update` 後の再着席 | `herdr agent list` で 4 席の起動引数が新 launcher（P1-7 の `herdr-agents`）、`.githooks` が各 worktree の `core.hooksPath` |
| P1-o | 記録 | boundary 23 の記録 PR がマージ済み、decisions.tsv に D-024-01〜D-024-12 の 12 行（既定値採用は result=default）、CompactionDB に同じ決定が `memory add --kind decision --scope project` で統合済み |
| P1-p | 境界規則 | `make check-regime-boundary` rc 0 |

## 1. 完了の定義（機械的に確かめる。順に）

| # | 確認 | 期待 |
| --- | --- | --- |
| DoD1 | `make doctor`（main checkout と `~/.local/share/chezmoi` の両方） | `ERROR:` 0 行。omp と hcom の導入版 = manifest の固定版 |
| DoD2 | `chezmoi verify` と `git -C ~/.local/share/chezmoi rev-parse HEAD` = `git rev-parse origin/main` | rc 0、一致（手作業で入れた設定が残っていない） |
| DoD3 | `herdr agent list` の全席のコマンド | 全席が `hcom … omp …` で起動。`claude` / `codex` の席が 0 |
| DoD4 | PR D の run-time probe（check-tools）: omp の auth store に `provider=anthropic` かつ `credential_type=oauth` の行が 0、`ANTHROPIC_OAUTH_TOKEN` 未設定 | 緑。CI 側の grep も緑 |
| DoD5 | `rg -l agmsg --glob '!.orchestration/**' --glob '!.ua/**'` | 0 ファイル（PR E） |
| DoD6 | `home/dot_claude/`、`home/dot_codex/`、`home/dot_config/claude/`、`home/dot_config/codex/`、`.chezmoitemplates/claude-*`、`codex-*` の有無と `.chezmoiremove` の該当行 | 無い。`.chezmoiremove` が旧生成物を消す |
| DoD7 | `uv run --offline --with pyyaml scripts/validate-agent-assets.py` | rc 0。`assets.pstack` の固定 sha = 取得物のハッシュ、allowlist 全存在 |
| DoD8 | `make unit-test` と `make render-check` | 緑。H1〜H9 の各テストを含む |
| DoD9 | `gh api repos/mryfmo/dotfiles/rulesets/24397953` | 必須チェック 7 本は残る。`strict_required_status_checks_policy=false`、`required_review_thread_resolution=false`（決定 D1/D2） |
| DoD10 | `gh pr list --state open` と plan 第 3 節の分類表 | 分類 merge の PR は全部マージ済み、stop/close は閉じている。main の push CI が HEAD で緑 |
| DoD11 | hcom 越しに TASK → RESULT → ACCEPTANCE が 1 往復し、その PR がマージされる（切替の実証） | `bus-history.sh` の 3 行と `gh pr view --json mergedAt` |
| DoD12 | `.project-map/state.json` の `head` | `origin/main` に一致 |
