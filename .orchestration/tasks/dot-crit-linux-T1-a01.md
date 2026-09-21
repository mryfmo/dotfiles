# dot-crit-linux-T1-a01 — Linux 向け Crit CLI インストール経路 + make update の pull 挙動改善

## Objective

操作者指摘の 2 点を解消する:
(1) Crit CLI が brew 前提のため Linux で常にスキップされる。
(2) `make update` はローカルソースを pull しないため、リモートの修正を
取り込んだつもりで古いスクリプトが走る(実機で発生)。README にも
pull 手順の記載がない。

## 背景(調査済み事実)

- crit(tomasz-tomczyk/crit)は GitHub Releases で各プラットフォームの
  ビルド済みバイナリを配布(brew / go install / nix も可)。
- 本リポの前例: zenbu-labs ツールは `scripts/lib/installer-pins.sh` の
  version+sha pin、mise `github:` backend は herdr/ghq 等。
  ただし mise config/lock は操作者の Mac に未コミット dirty ペアがあるため
  **本タスクでは mise config/lock に触れない**(installer-pins 方式を採る)。

## Work items

F1 — Linux での Crit CLI インストール:

- `scripts/lib/installer-pins.sh` に crit の pin を追加:
  `CRIT_PIN_VERSION`(最新安定リリースを worker が確認して選定)と
  linux-arm64 / linux-x64 それぞれの release バイナリ(または tar.gz)の
  sha256(worker が実ダウンロードして計算、GitHub Releases の checksums が
  あればそれとの一致も確認して validation に逐語記録)。
- `ensure_crit_cli` を拡張: macOS は現行どおり brew。Linux では pin された
  release アーティファクトをダウンロード → sha256 検証 → `~/.local/bin/crit`
  へ install -m 0755(mktemp 経由、失敗時は既存を変更しない —
  terminal-code/terminal-browser と同じ流儀)。既に正しい version が入って
  いれば no-op(`crit --version` 照合)。
- `make upgrade` の pin 更新経路(terminal 系 pin を rewrite している既存
  関数)に crit も追随させる。
- manifest_record の reverse mapping を追加(`rm ~/.local/bin/crit` 相当)。

F2 — `make update` の pull 挙動 + README:

- Makefile `update` ターゲットの冒頭に条件付き fast-forward pull を追加:
  「現在 branch が main」かつ「upstream が origin/main」かつ
  「tracked ファイルに staged/unstaged 変更なし」の場合のみ
  `git pull --ff-only`(失敗時は警告して続行)。条件を満たさない場合は
  `Notice: local source not pulled (…reason…); run 'git -C <repo> pull'
to fetch remote updates.` の 1 行を出して従来どおり apply。
- README.md の Lifecycle 節に、この挙動(いつ自動 pull されるか、されない
  場合の手動手順)を追記。
- 既存の Makefile 系 bats/unit test(tests/install/common/setup.bats の
  Makefile 検証群 or tests/unit)に、clean-on-main で pull が走ること/
  dirty では pull せず Notice を出すことの検証を既存パターンで追加。

## 検証

- shellcheck / shfmt / bash -n(変更シェル)。bats ローカル実行禁止(CI)。
- F1: Linux バイナリの実ダウンロードと sha 計算の逐語出力(実行はローカル
  Mac 上で hash のみ。crit バイナリの起動確認は adh-test VM の scratch user
  で `crit --version` まで、削除して撤収)。
- F2: mock repo での make update 相当の駆動トレース(pull 実施/スキップ両分岐)。
- `.orchestration/validation/dot-crit-linux-T1-a01.md` へ全て記録。

## Scope

allowed_files: `scripts/lib/installer-pins.sh`, `scripts/update-agent-assets.sh`,
`Makefile`, `README.md`, `tests/**`,
(pin rewrite が別スクリプトなら `scripts/**` の該当ファイル),
`.orchestration/{tasks,reports,validation,sandboxes,learning,autoskill/runs}/dot-crit-linux-T1-a01.md`,
`.agents/worklog/codex/**`

forbidden_actions: git commit 禁止、push 禁止、bats ローカル実行禁止、
mise config/lock 変更禁止、VM は `limactl shell adh-test` のみ(scratch user
削除)、credential 持込み禁止、新規トップレベルディレクトリ作成禁止。

## 完了

done_signal=AGMSG-RESULT。max_turns=35。CompactionDB memory add + ID。
