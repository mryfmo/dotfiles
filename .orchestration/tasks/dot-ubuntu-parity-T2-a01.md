# dot-ubuntu-parity-T2-a01 — Ubuntu パリティ HIGH 修正(B1–B6)

## Objective(操作者決定 2026-09-23)

Ubuntu 24.04 arm64 client(spark-9e8d)で実害のある 6 件のリポジトリバグを、
feature ブランチ `feat/ubuntu-parity` 上で項目ごとにコミットして修正する。
push / PR 作成は禁止(T4 完了後にオーケストレータが承認)。
計画全文はオーケストレータ側で承認済み。以下が本タスクの範囲。

## Work items(各項目 1 コミット、Conventional Commits、末尾に Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>)

### B1. docker グループ(`fix(ubuntu): add user to docker group on client install`)

- `install/ubuntu/client/docker.sh`: `main()` に `configure_docker_group()` を追加し
  `install_docker_engine` の後に呼ぶ。中身は `sudo usermod -aG docker "$(id -un)"`。
  docker-ce パッケージが docker グループを作るため groupadd 不要。冪等。
- `tests/install/ubuntu/client/docker.bats`(既存スイートの流儀に合わせる)に
  `getent group docker | grep -q "$(id -un)"` 相当のアサーションを追加。
- 注: `run_once_10-install-docker.sh.tmpl` は内容ハッシュ変更で自動再実行されるため
  state 操作・リネーム不要 [memory:decision] chezmoi run_once の再トリガはスクリプト内容変更で行う(state 削除やリネームは不要)。

### B2. yq を aqua バックエンドへ + watchexec 追加(`fix(mise): normalize yq shim via aqua and adopt watchexec`)

- `home/dot_mise/config.toml`: `"github:mikefarah/yq" = "4.53.6"` → `"aqua:mikefarah/yq" = "4.53.6"`
  (github バックエンドは arm64 で `yq_linux_arm64` というシム名を生成し `yq` が起動不能)。
- 同ファイルに `"aqua:watchexec/watchexec"` を追加(最新安定版をピン。`make watch` の
  Linux 対応。prebuilt バイナリで 4 プラットフォーム対応)。
- `install/macos/common/misc.sh` の brew リストから `watchexec` を削除。
- リポジトリ文脈で `mise lock` を実行し、`mise.lock` に lockfile_platforms 4 種
  (linux-x64, linux-arm64, macos-x64, macos-arm64)のエントリが揃うことを確認、逐語で validation へ。
- `uv run python -m unittest tests.unit.test_supply_chain_policy` green を確認。

### B3. Codex project trust のテンプレート化(`fix(agents): key codex project trust to the chezmoi working tree`)

- `home/dot_agents/agent-config.yaml` の projects キー `/Users/mryfmo/Workspace/dotfiles` を
  `{{ .chezmoi.workingTree }}` に置換。
- `home/dot_codex/modify_private_config.toml` の `render_managed_template()`(:29-32)に
  `{{ .chezmoi.workingTree }}` 置換を追加。値は env `CHEZMOI_WORKING_TREE` を優先、
  フォールバックは `source_dir().parent`(.chezmoiroot=home のため source dir の親が working tree)。
- `python3 scripts/generate-agent-configs.py` で再生成(レンダリング産物の手編集禁止)。
- `scripts/validate-agent-assets.py` の既存 `/Users/mryfmo/` shell_path ガード(:360 付近)の隣に、
  `[projects]` キーに `/Users/mryfmo/` を含まないこと+managed projects キーが
  `{{ .chezmoi.workingTree }}` を使うことのガードを追加。
- `scripts/check-agent-runtime.py` がテンプレートを chezmoi 経由でレンダリングするか確認し、
  ローカル文字列置換の場合は同じ置換をミラー。
- `tests/unit/test_codex_config_merge.py`, `tests/unit/test_generate_agent_configs.py`,
  `tests/unit/test_validate_agent_assets.py` の期待値更新。

### B4. sheldon 死参照削除(`fix(sheldon): drop dead ubuntu-command local plugin`)

- `home/dot_config/sheldon/plugin_sources/client/ubuntu.toml` の `[plugins.ubuntu-command]`
  ブロックを削除(`~/.local/bin/client/ubuntu.sh` は git 全履歴に存在しない死参照)。
  ファイルが空になる場合はファイル自体と、それを参照する仕組みの扱いを既存の
  マージ/テンプレート機構に合わせて判断し、判断根拠を report へ。

### B5. doctor の Cowork synced 除外 + crit スキル所有化(`fix(doctor): tolerate cowork-synced skills and own crit codex skills`)

- `scripts/check-agent-runtime.py::compare_claude_skills`(:331)の `ignored_paths` に
  `~/.claude/skills/synced` サブツリーを追加(Cowork 同期バケットは chezmoi 非所有)。
- 同ファイルに `CRIT_PLUGIN_SKILLS = {"crit", "crit-cli", "crit-story"}` を定義し、
  `orphaned_asset_warnings()`(:512)の skill allowlist(:531)へ union。
- `scripts/update-agent-assets.sh::update_codex_crit` の `manifest_record` に
  `${HOME}/.agents/skills/{crit,crit-cli,crit-story}` を記録対象として追加。
- `tests/unit/test_check_agent_runtime.py` に synced 存在時に fail しないケースと
  crit allowlist ケースを追加。

### B6. herdr hook 絶対パス化(`fix(claude): invoke herdr-agents attach hook by absolute path`)

- `home/dot_claude/modify_private_settings.json`(:180)の
  `'herdr-agents --attach >> …'` を `home_dir()` ベースの絶対パス
  `"<home>/.local/bin/common/herdr-agents" --attach >> …` に変更(重複排除ロジックとの
  整合に注意 — 旧文字列エントリが残る場合の移行も処理)。
- `tests/unit/test_claude_settings_merge.py` の期待値更新。

## 仕上げ(このタスク内)

- `make format` → 差分があれば該当コミットへ amend か追加コミット。
- `make validate-agent-assets` green、`make unit-test` green(逐語出力を validation へ。
  長い場合は各スイートの末尾サマリ+失敗全文)。
- `git log --oneline main..HEAD` を validation へ。
- CompactionDB: 上記 [memory:decision] を `python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project` で登録し、コマンドと ID を report・validation に逐語で。

## Scope

allowed_files: `install/ubuntu/client/docker.sh`, `tests/install/ubuntu/client/docker.bats`,
`home/dot_mise/config.toml`, `home/dot_mise/mise.lock`, `install/macos/common/misc.sh`,
`home/dot_agents/agent-config.yaml`, `home/dot_codex/modify_private_config.toml`,
`home/.chezmoitemplates/codex-config-managed.toml`(generate-agent-configs.py 経由のみ),
`home/.chezmoitemplates/claude-settings-managed.json`(同上),
`scripts/generate-agent-configs.py`(必要な場合のみ最小変更),
`scripts/validate-agent-assets.py`, `scripts/check-agent-runtime.py`,
`scripts/update-agent-assets.sh`,
`home/dot_config/sheldon/plugin_sources/client/ubuntu.toml`,
`home/dot_claude/modify_private_settings.json`,
`tests/unit/test_codex_config_merge.py`, `tests/unit/test_generate_agent_configs.py`,
`tests/unit/test_validate_agent_assets.py`, `tests/unit/test_check_agent_runtime.py`,
`tests/unit/test_claude_settings_merge.py`,
`.orchestration/{reports,validation,sandboxes,learning,autoskill/runs}/dot-ubuntu-parity-T2-a01.md`,
`.agents/worklog/codex/**`

forbidden_actions: push 禁止、PR 作成禁止、chezmoi apply 禁止、`$HOME` 配下の変更禁止
(mise lock はリポジトリ文脈で実行)、main への直コミット禁止(feat/ubuntu-parity 上で作業)、
allowed_files 外の変更禁止(出たら revert して報告)、依存追加禁止(mise pin 追加は B2 のみ可)。

## 完了

done_signal=AGMSG-RESULT。max_turns=60。cost 行を report に。
ブロックされたら AGMSG-RESULT status=blocked で report に理由を。
