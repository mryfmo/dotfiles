# dot-ubuntu-parity-T3-a01 — Ubuntu パリティ MEDIUM 修正(B7–B12)

## Objective(操作者決定 2026-09-23)

T2 に続き、同じ `feat/ubuntu-parity` ブランチ上で MEDIUM 6 件を項目ごとにコミットする。
push / PR 作成は禁止(T4 完了後にオーケストレータが承認)。

## Work items(各項目 1 コミット、Conventional Commits、末尾に Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>)

### B7. client bashrc ガード + server 残骸の宣言的除去(`fix(ubuntu): guard server sourcing in client bashrc and remove stale server bin`)

- `home/dot_bash/client/bashrc` の無ガード `source ~/.local/bin/server/...` 行
  (:130 history.sh、:150 cache.sh、および :154/:158 に同種があれば全て)を、
  隣接行(:127/:142)と同じ `[ -r "…" ] && source "…"` パターンへ統一。
  shellcheck source ディレクティブは保持。
- `home/.chezmoiremove` に追記:
  `{{ if and (eq .chezmoi.os "linux") (eq .system "client") }}` ガードで `.local/bin/server`。
  (server として初回ブートストラップ後 client へ切替えた機体の残骸
  `~/.local/bin/server/{cache,cuda,history,ssh_agent}.sh` を宣言的に除去。
  bashrc ガードが先に入るため安全)。
- `tests/files/ubuntu.bats` の既存アサーション(:24 の cache.sh absent)と矛盾しないこと確認。

### B8. zshenv PATH ガード(`fix(zsh): only add existing homebrew dirs to PATH`)

- `home/dot_zshenv`(:16-19)の `/opt/homebrew/bin` `/opt/homebrew/sbin`
  `/usr/local/bin` `/usr/local/sbin` に zsh の `(N-/)` グロブ修飾子を付与し、
  存在するディレクトリのみ path へ載せる。dot_zprofile は既ガードのため変更しない。
- Codex の PATH literal(agent-config.yaml)は据え置き(実害ゼロ、コミットメッセージに明記不要 — report に記載)。

### B9. usage-snapshot の Linux スケジューラ + plist 可搬化(`feat(usage): schedule usage snapshot via systemd user timer on linux`)

- 新規 `home/dot_config/systemd/user/usage-snapshot.service.tmpl`:
  `[Unit] Description=...`、`[Service] Type=oneshot`、
  `ExecStart=/usr/bin/make -C {{ .chezmoi.workingTree }} usage-snapshot usage-report`、
  `Environment=PATH={{ .chezmoi.homeDir }}/.local/share/mise/shims:/usr/local/bin:/usr/bin:/bin`。
- 新規 `home/dot_config/systemd/user/usage-snapshot.timer.tmpl`:
  `OnCalendar=Mon 09:00`、`Persistent=true`、`[Install] WantedBy=timers.target`
  (launchd plist の Weekday=1/Hour=9 と等価)。
- 新規 `home/.chezmoiscripts/ubuntu/run_onchange_60-enable-usage-snapshot-timer.sh.tmpl`
  (client ゲート、unit 2 ファイルの `{{ include … | sha256sum }}` ハッシュコメント埋め込み、
  `systemctl --user daemon-reload && systemctl --user enable --now usage-snapshot.timer`、
  user systemd 不在(CI コンテナ)では graceful skip)。
- `home/.chezmoitemplates/chezmoiignore.d/macos` に `.config/systemd` を追加。
- `home/Library/LaunchAgents/com.mryfmo.dotfiles.usage-snapshot.plist` → `.plist.tmpl` 化し、
  `/Users/mryfmo/Workspace/dotfiles` → `{{ .chezmoi.workingTree }}`、
  `/Users/mryfmo` → `{{ .chezmoi.homeDir }}`(計 4 箇所)。
- `tests/files/ubuntu.bats` に unit 存在、`tests/files/macos.bats` 側は不存在アサーション
  (スイートの流儀に従う)。

### B10. フォント統一(`fix(fonts): ship JetBrainsMono on both OS and LINE Seed JP on linux`)

- `home/.chezmoitemplates/chezmoiexternal.d/common.yaml.tmpl` に JetBrainsMono Nerd Font
  v3.4.0 の archive エントリを追加(既存 RobotoMono/Hack と同一パターン、
  URL/sha256 は実在リリースから取得し validation に取得コマンドと値を逐語で)。
- LINE Seed JP のエントリを `macos.yaml.tmpl` から `common.yaml.tmpl` へ移動
  (`$fontsPath` が linux → `.local/share/fonts` を既にマップ)。

### B11. timezone スクリプト配線(`fix(ubuntu): wire orphaned server timezone setup script`)

- 新規 `home/.chezmoiscripts/ubuntu/run_once_50-server-setup-timezone.sh.tmpl`
  (server ゲート、他の server スクリプトと同一のテンプレート構造で
  `install/ubuntu/server/setup_timezone.sh` を include)。
- `tests/install/ubuntu/server/` に最小 bats(Asia/Tokyo 確認)を既存流儀で追加。

### B12. pinentry(`fix(gpg): configure pinentry on linux`)

- `install/ubuntu/common/dependencies.sh` の `PACKAGES` に `pinentry-curses` を追加。
- `home/private_dot_gnupg/gpg-agent.conf.tmpl` に linux 分岐で
  `pinentry-program /usr/bin/pinentry-curses` を追加(darwin 分岐は不変)。
- dependencies 系 bats の期待パッケージリスト更新。

## 仕上げ(このタスク内)

- `make format` / `make validate-agent-assets` / `make unit-test` green(逐語 or 末尾サマリ+失敗全文を validation へ)。
- `git log --oneline main..HEAD` を validation へ。
- CompactionDB memory add(本タスクで下した設計判断があれば decision として登録、コマンドと ID を逐語で)。

## Scope

allowed_files: `home/dot_bash/client/bashrc`, `home/.chezmoiremove`, `home/dot_zshenv`,
`home/dot_config/systemd/user/**`, `home/.chezmoiscripts/ubuntu/**`,
`home/.chezmoitemplates/chezmoiignore.d/macos`,
`home/Library/LaunchAgents/**`,
`home/.chezmoitemplates/chezmoiexternal.d/{common,macos,ubuntu}.yaml.tmpl`,
`install/ubuntu/common/dependencies.sh`, `home/private_dot_gnupg/gpg-agent.conf.tmpl`,
`tests/**`,
`.orchestration/{reports,validation,sandboxes,learning,autoskill/runs}/dot-ubuntu-parity-T3-a01.md`,
`.agents/worklog/codex/**`

forbidden_actions: push 禁止、PR 作成禁止、chezmoi apply 禁止、`$HOME` 配下の変更禁止、
main への直コミット禁止、allowed_files 外の変更禁止(出たら revert して報告)、
`systemctl` の実行禁止(unit の enable は適用フェーズでオーケストレータ側)。

## 完了

done_signal=AGMSG-RESULT。max_turns=60。cost 行を report に。
ブロックされたら AGMSG-RESULT status=blocked で report に理由を。

## 環境注意(2026-09-23 追記)

- 作業場所はあなたの登録 worktree(`git worktree`)。main への checkout はしない。
  ブランチ `feat/ubuntu-parity` は worktree 作成時に済んでいる。
- このマシンには SSH 署名鍵がないため、コミットは必ず
  `git -c commit.gpgsign=false commit ...` で作成する(署名試行は fail する)。
- `mise lock` は必ず `MISE_CONFIG_DIR="$PWD/home/dot_mise" mise lock` で実行する
  (素の実行は ~/.config/mise → main worktree へのシムリンクを書き換えてしまう)。
- push・PR 作成・gh での書き込み操作は禁止(このマシンに書き込み権限がない)。
