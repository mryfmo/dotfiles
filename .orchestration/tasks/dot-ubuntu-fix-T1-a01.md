# dot-ubuntu-fix-T1-a01 — Ubuntu bootstrap failures + Japanese environment

## Objective

README の Ubuntu 手順(setup.sh → chezmoi apply)がフレッシュな Ubuntu で失敗する
問題群と、日本語環境が整わない問題を修正する。全て実ログで再現済み
(server 実走: VM adh-test の /tmp/dotf-server-run.log、Ubuntu 26.04 aarch64)。

## 確定済み findings(修正対象)

F1(blocking) — `install/common/gh_extensions.sh`:
未認証時に `gh auth login -h github.com -p https` を実行し、ワンショット
ブートストラップ内で対話デバイスコードフローを起動する(pipe 実行では永久
ハング、tty でも突然の対話ログイン。中断で `chezmoi apply` が exit 143 失敗)。
→ ブートストラップでは絶対にログインを起動しない。`gh auth status` 失敗時は
「setup-gh 後に再実行」の警告を出して return 0(拡張インストールは認証済みの
時のみ)。tests/install/common の対応 bats を更新。

F2(major) — `install/common/mise.sh` 経由の uv / yazi 破損:
mise が lock の linux-arm64 gnu アーティファクト
(`uv-aarch64-unknown-linux-gnu` / `yazi-aarch64-unknown-linux-gnu`)を展開する
一方、shim 解決は musl パスを期待し
「mise WARN bin path does not exist: .../uv-aarch64-unknown-linux-musl/uv」で
uv/uvx/yazi/ya のコマンドが生成されない(mise ls は installed 表示)。
→ VM で root cause を特定(pinned MISE_VERSION v2026.7.5 の aqua backend の
bin path 解決 vs lock の asset 選択)。再現は
`limactl shell adh-test -- sudo -i -u dotftest ...`(既存環境あり)か新規
scratch user で。修正候補: mise 版 pin 更新 / lock の platform asset 修正 /
tool オプション。macOS を壊さないこと(lock diff は最小)。修正後 VM で
uv --version / yazi --version の実出力を証拠化。

F3(major) — `install/ubuntu/common/dependencies.sh`:
`busybox` 指定が Ubuntu 26.04 で `busybox-static ubuntu-standard` の REMOVE を
誘発(実機ではシステム標準メタパッケージ破壊)。busybox はリポ内で未使用。
→ PACKAGES から busybox を削除し、tests/install/ubuntu/common の
dependencies.bats / dependencies_unit.bats を追随更新。

F4(major) — 日本語環境:
(a) `home/dot_config/sheldon/plugin_sources/common.toml` の [plugins.lang] が
LANG を無条件 en_US.UTF-8 に上書き → 既に LANG が設定済みならそれを尊重し、
未設定時のみ en_US.UTF-8 を設定する形へ。
(b) ja_JP.UTF-8 locale がどの経路でも生成されない →
`install/ubuntu/server/setup_locale.sh` を en_US.UTF-8 + ja_JP.UTF-8 の両方を
生成する形に拡張し、client でも locale 生成が走るよう chezmoiscripts の配置を
見直す(server 限定を common 化 or client 用スクリプト追加。既存の命名規約に
従い、新ディレクトリは作らない)。
(c) Ubuntu client に日本語フォント・IME がない →
`install/ubuntu/client/misc.sh` の PACKAGES に `language-pack-ja`,
`fonts-noto-cjk`, `fonts-noto-color-emoji`, `ibus-mozc` を追加(GNOME 既定の
ibus に合わせる。im-config の強制切替や GNOME 設定の自動変更はしない)。
README に入力ソース追加の 1 行手順を追記。

F5(minor) — `home/.chezmoiscripts/common/run_once_before_01-decrypt-private-key.sh.tmpl`:
pipe 実行で `chezmoi age decrypt --passphrase` が
「could not read passphrase: could not open a new TTY」→ 現状警告スキップだが、
CI 判定に加えて stdin が tty でない場合も早期 return する guard を追加
(tty ありの対話 prompt は現行維持)。

F6(minor) — `install/common/chezmoi_private.sh` の SSH clone が
`Host key verification failed`(known_hosts 未登録)で失敗 → 警告スキップ自体は
設計どおりだが、`install/ubuntu/common/ssh.sh`(または適切な既存スクリプト)で
github.com の公式 host key を known_hosts へ追加(公式公開 fingerprint を
ハードコードし ssh-keyscan の盲信はしない)。

F7(docs) — README.md: フレッシュマシンでの対話要素(age passphrase、gh 認証は
setup-gh で後から)の説明を Setup 節に短く追記。Dockerfile の ubuntu:22.04 は
今回は変更しない(別タスク)。

## 検証

- shellcheck / shfmt(mise 管理版)を全変更スクリプトに。
- bats はローカル実行禁止(リポ方針)。テスト更新のみ行い、CI で検証する。
- F2 は VM で実修正の前後証拠(コマンド実出力)を
  `.orchestration/validation/dot-ubuntu-fix-T1-a01.md` に逐語で。
- 変更スクリプト単体の静的確認(bash -n)と、chezmoi template の
  `chezmoi execute-template` での構文確認。

## Scope

allowed_files: `install/**`, `home/.chezmoiscripts/**`,
`home/dot_config/sheldon/plugin_sources/common.toml`, `home/dot_mise/**`
(F2 で必要な場合のみ・最小 diff), `scripts/lib/**`(F2 で必要な場合のみ),
`tests/**`, `README.md`,
`.orchestration/{tasks,reports,validation,sandboxes,learning,autoskill/runs}/dot-ubuntu-fix-T1-a01.md`,
`.agents/worklog/codex/**`

forbidden_actions: git commit 禁止(統合はオーケストレータ)、push 禁止、
bats ローカル実行禁止、VM は `limactl shell adh-test` のみ(credential 持込み
禁止)、reviews/ 配下・main worktree への書込み禁止、新規トップレベル
ディレクトリ作成禁止、network はパッケージ取得と VM 検証に必要な範囲のみ。

## 完了

done_signal=AGMSG-RESULT(report/validation/sandbox/learning/autoskill を
expected パスへ)。max_turns=40。
