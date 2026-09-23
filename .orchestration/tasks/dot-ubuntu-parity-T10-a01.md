# dot-ubuntu-parity-T10-a01 — identity/所有者レイヤの構造是正

## Objective(操作者決定 2026-09-23)

監査で確定した構造的ギャップの是正。前提: 運用者は同一人物 Fumio Moriya で、
GitHub は個人 `mryfmo`(リポジトリ所有)と業務 `moriya-fumio-thd`(spark 等)の 2 アカウント。
作業ブランチは checkout 済みの `fix/identity-provisioning`(この worktree)。
push/PR 禁止(受入後にオーケストレータ)。各項目 1 コミット、
`git -c commit.gpgsign=false commit`、末尾 Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>。

## Work items

### T10-1. git user.name の chezmoi データ化(`fix(git): source user.name from chezmoi data like email`)

- 根本原因はハードコーディング(誤値が入り込めた機構そのもの)。email と同一パターンで是正:
  - `home/.chezmoi.yaml.tmpl`: 冒頭の email 処理(hasKey ガード+promptString)と**完全に同型**の
    `$name` 処理を追加し、`data:` に `name: {{ $name | quote }}` を出力。
  - `home/dot_config/git/config.tmpl`: `name = Fumio Moriya` →
    `name = {{ get . "name" | default "Fumio Moriya" }}`(chezmoi は missingkey=error のため、
    `name` キー未追加の既存マシン config でも壊れないよう sprig `get`+`default` でフォールバック。
    フォールバック値は現行値 = 運用者本人名で、再 init 後はプロンプト値が優先)。
  - 検証: `chezmoi execute-template` で (a) data に name あり、(b) なし、の両ケースの
    レンダリング結果を逐語で validation へ。
- 関連 unit テストがあれば追従(`grep -rn 'Fumio Moriya\|user.name' tests/`)。

### T10-2. 個人レイヤ(private/age)の opt-in フラグ(`feat(chezmoi): gate the private layer behind an init-time flag`)

- `home/.chezmoi.yaml.tmpl` に email/system と同型の `$usePrivate`(bool)を追加:
  hasKey ガード+`promptBool "Use the private dotfiles layer (age key + dotfiles-private)"`。
  darwin では既存の system 同様デフォルト true、それ以外はプロンプト
  (既存マシンの config には(キーがないので)hasKey フォールバックで **true** を採用 —
  所有者の既存マシンの挙動を変えないため)。data に `usePrivate: {{ $usePrivate }}`。
- ゲート適用(いずれもテンプレートの `{{ if .usePrivate }}` 相当。get+default true で安全に):
  - `home/.chezmoiscripts/common/run_once_before_01-decrypt-private-key.sh.tmpl`(復号)
  - `home/.chezmoiscripts/common/run_once_after_01-setup-chezmoi-private.sh.tmpl`(private init)
  - `scripts/check-tools.sh` の private config optional warning(usePrivate=false のマシンでは
    警告を出さない — 判定は rendered config の読み取り等、既存の実装流儀に合わせ、逐語根拠を report へ)
- 検証: execute-template で usePrivate true/false 両方のレンダリングを逐語で。

### T10-3. マシン鍵プロビジョニングの導線(`feat(setup): provision a per-machine ssh key for signing and push`)

- 新規 `home/dot_local/bin/common/executable_provision-machine-key`:
  `~/.ssh/id_ed25519` が無ければ `ssh-keygen -t ed25519 -C "<email> (<hostname>)" -f ~/.ssh/id_ed25519 -N ""`
  で生成し、公開鍵と「GitHub の運用アカウントに **auth 用と signing 用の両方**で登録せよ」
  という手順(gh コマンド例 `gh ssh-key add --type authentication|signing` を含む)を表示。
  既存鍵があれば表示のみ。冪等。shdoc コメント。
- `scripts/check-tools.sh` に鍵の存在チェックを追加(なければ optional warning +
  `provision-machine-key` を案内 — commit.gpgsign=true 環境でコミット不能になる構造の可視化)。
- README のセットアップ手順に 1 節追加(このリポジトリ既存の文体で簡潔に)。
- bats/unit の追従(check-tools のテストがあれば)。

### T10-4. tailscale ゲートの一貫化(`fix(install): align tailscale gating across platforms`)

- macOS は `whoami == mryfmo` ゲート、Ubuntu(T4)は無条件、という非対称を解消。
  方針: **無条件に統一**(tailscale はマシン共通ツールで、ログイン=tailscale up は手動のまま)。
  `install/macos/common/misc.sh:89` のゲートを外し tailscale を通常の brew パッケージへ。
  コミットメッセージに方針を明記。関連 bats/unit 追従。

## 仕上げ

- `make format` / `make validate-agent-assets` / `make unit-test` green(末尾サマリ+失敗全文を validation へ)。
- 新規/変更テンプレートは execute-template で全ケース逐語検証。
- モックベースの新規 bats があれば **`bats -f` で個別実行**して逐語(T7 の教訓)。
- CompactionDB decision 登録(T10-1/2 の設計判断)、コマンドと ID を逐語で。
- `git log --oneline origin/main..HEAD` を validation へ。

## Scope

allowed_files: `home/.chezmoi.yaml.tmpl`, `home/dot_config/git/config.tmpl`,
`home/.chezmoiscripts/common/**`, `scripts/check-tools.sh`,
`home/dot_local/bin/common/executable_provision-machine-key`(新規),
`install/macos/common/misc.sh`, `README.md`, `tests/**`,
`.orchestration/{reports,validation,sandboxes,learning,autoskill/runs}/dot-ubuntu-parity-T10-a01.md`,
`.agents/worklog/codex/**`

forbidden_actions: push 禁止、PR 作成禁止、chezmoi apply 禁止、`$HOME` 配下の変更禁止
(鍵生成スクリプトは作るだけで実行しない)、main への直コミット禁止、
対象外 bats 実行禁止、`mise lock` 不要(依存変更なし)。

## 環境注意

- このマシンには SSH 署名鍵がないため、コミットは必ず `git -c commit.gpgsign=false commit ...`。
- push・PR 作成・gh 書き込みは禁止。

## 完了

done_signal=AGMSG-RESULT。max_turns=50。cost 行を report に。
ブロックされたら AGMSG-RESULT status=blocked で理由を。
