# dot-ubuntu-parity-T4-a01 — GUI パリティ・GNOME defaults・掃除(B13–B15)+ 最終検証

## Objective(操作者決定 2026-09-23)

T2/T3 に続き、同じ `feat/ubuntu-parity` ブランチで macOS 専用レイヤの Linux 移植と
掃除を項目ごとにコミットし、ブランチ全体の最終検証を行う。push / PR 作成は禁止
(完了後にオーケストレータが承認)。

## Work items(各項目 1 コミット、Conventional Commits、末尾に Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>)

### B13a. Zed(`feat(ubuntu): install zed on client from pinned release`)

- 新規 `install/ubuntu/client/zed.sh`: 公式 GitHub リリースの linux tarball
  (x86_64 / aarch64 両対応)を `scripts/lib/installer-pins.sh` の新設
  `ZED_PIN_VERSION` + アーチ別 sha256 でピンし(crit の Linux インストーラと同一規約)、
  `~/.local` 配下へ展開して `~/.local/bin/zed` を提供。冪等(同版ならスキップ)。
- 新規 `home/.chezmoiscripts/ubuntu/run_once_52-client-install-zed.sh.tmpl`(client ゲート)。
- `scripts/upgrade-tools.sh::bump_terminal_tool_pins` に Zed の pin 更新を組み込む
  (tode/terminal-browser/crit と同じ流儀)。
- pin の sha256 は実リリースから取得し、取得コマンドと値を validation に逐語で。
- bats を `tests/install/ubuntu/client/` に追加。

### B13b. Chromium + Tailscale(`feat(ubuntu): install chromium and tailscale on client`)

- `install/ubuntu/client/misc.sh` に `command -v snap` ガード付き
  `sudo snap install chromium`(Ubuntu 24.04 の chromium は snap のみ。
  Google Chrome は linux-arm64 ビルド不在のため代替 — この根拠を report へ)。
- 新規 `install/ubuntu/client/tailscale.sh`: 公式 apt リポジトリ
  (`pkgs.tailscale.com/stable/ubuntu`、keyring 方式、arm64 対応)+ `tailscale` パッケージ。
  `tailscale up`(ログイン)は手動のまま。docker.sh の keyring パターンを踏襲。
- 新規 `home/.chezmoiscripts/ubuntu/run_once_53-client-install-tailscale.sh.tmpl`(client ゲート)。
- bats 追加。

### B14. GNOME defaults フル対応(`feat(ubuntu): port macos defaults to gnome gsettings on client`)

- 新規 `install/ubuntu/client/gnome_settings.sh` +
  `home/.chezmoiscripts/ubuntu/run_once_99-client-gnome-defaults.sh.tmpl`
  (macos/run_once_99 のミラー。`command -v gsettings` と DBUS_SESSION_BUS_ADDRESS /
  DISPLAY の存在ガードで CI・ヘッドレスは graceful skip)。
- `install/macos/common/defaults.sh` の全項目を走査し、GNOME 相当があるものは全て移植:
  - キーリピート: `org.gnome.desktop.peripherals.keyboard repeat-interval 30` / `delay 375`
    (KeyRepeat=2×15ms / InitialKeyRepeat=25×15ms 換算)
  - 入力ソース: `org.gnome.desktop.input-sources sources "[('xkb','us'),('ibus','mozc-jp')]"`
  - Dock 相当: `org.gnome.shell.extensions.dash-to-dock` autohide 等(スキーマ存在チェック付き)
  - 隠しファイル表示: `org.gtk.Settings.FileChooser show-hidden true`、
    `org.gnome.nautilus.preferences show-hidden-files true`
  - スクリーンショット保存先、スクリーンセーバー/ロック、ナチュラルスクロール、
    トラックパッド tap-to-click(`org.gnome.desktop.peripherals.touchpad tap-to-click`)等、
    defaults.sh にあり GNOME スキーマが存在するもの全部。
  - **GNOME 相当が存在しない項目(Finder 固有、Siri、symbolic hotkeys 等)は
    スクリプト末尾コメントに「対応不能一覧」として明文化**(暗黙に落とさない)。
- gsettings はスキーマ不在で fail するため、各 set は
  `gsettings writable <schema> <key>` チェックまたはスキーマ存在チェックでガード。
- bats 追加(ヘッドレス CI では skip になることの確認を含む)。

### B15. LOW 掃除(`chore: drop dead ignore entries and de-hardcode agmsg template home`)

- `home/.chezmoitemplates/chezmoiignore.d/` から死にエントリを削除(各削除前に
  ソース不存在を `git log --all` 等で確認し、確認結果を validation へ):
  - `macos`: `.zsh/server/zshrc`, `.zsh/server/zprofile`
  - `ubuntu/client`: `.zsh/server/zshrc`, `.zsh/server/zshprofile`(typo 込み)
  - `ubuntu/server`: `.zlogin`, `.zpreztorc`, `.zlogout`, `.p10k.zsh`,
    `.config/sheldon/plugin_sources/client.toml`, `.local/bin/client`,
    `.zsh/zshrc_client`, `.zsh/zprofile_client`
  - 保持: `.profile`, `.bashrc`, `.local/bin/server`, `.bash/server/bashrc`,
    `.config/powerlevel10k`, `.bash/client/bashrc` などソース実在分
- `home/dot_agents/skills/agmsg/templates/cmd.claude-code.md`(:109-117)の
  `/Users/<you>` 直書き例を home 非依存(`<absolute home>` 例示: `/home/<you>` と
  `/Users/<you>` 併記)へ。既存の「実際の home に置換せよ」文言は保持。

## 最終検証(このタスク内)

- `make format` / `make validate-agent-assets` / `make unit-test` green。
- `bash -n` を新規/変更 shellscript 全部に。shfmt は make format が担保。
- `git log --oneline main..HEAD`(T2 以降の全コミット)を validation へ。
- `git status -sb` クリーン(.orchestration / worklog 除く)。
- CompactionDB memory add(設計判断を decision として登録、コマンドと ID を逐語で)。

## Scope

allowed_files: `install/ubuntu/client/**`, `install/macos/common/defaults.sh`(読み取りのみ・変更禁止),
`home/.chezmoiscripts/ubuntu/**`, `scripts/lib/installer-pins.sh`, `scripts/upgrade-tools.sh`,
`home/.chezmoitemplates/chezmoiignore.d/**`,
`home/dot_agents/skills/agmsg/templates/cmd.claude-code.md`,
`tests/**`,
`.orchestration/{reports,validation,sandboxes,learning,autoskill/runs}/dot-ubuntu-parity-T4-a01.md`,
`.agents/worklog/codex/**`

forbidden_actions: push 禁止、PR 作成禁止、chezmoi apply 禁止、`$HOME` 配下の変更禁止、
main への直コミット禁止、snap/apt/gsettings の実行禁止(インストールと設定適用は
適用フェーズでオーケストレータ側)、allowed_files 外の変更禁止(出たら revert して報告)。

## 完了

done_signal=AGMSG-RESULT。max_turns=80。cost 行を report に。
ブロックされたら AGMSG-RESULT status=blocked で report に理由を。

## 環境注意(2026-09-23 追記)

- 作業場所はあなたの登録 worktree(`git worktree`)。main への checkout はしない。
  ブランチ `feat/ubuntu-parity` は worktree 作成時に済んでいる。
- このマシンには SSH 署名鍵がないため、コミットは必ず
  `git -c commit.gpgsign=false commit ...` で作成する(署名試行は fail する)。
- `mise lock` は必ず `MISE_CONFIG_DIR="$PWD/home/dot_mise" mise lock` で実行する
  (素の実行は ~/.config/mise → main worktree へのシムリンクを書き換えてしまう)。
- push・PR 作成・gh での書き込み操作は禁止(このマシンに書き込み権限がない)。
