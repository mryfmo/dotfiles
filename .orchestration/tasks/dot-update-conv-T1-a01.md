# dot-update-conv-T1-a01 — make update の完全収束化 + superpowers stderr 畳み込み

## Objective(操作者決定)

「`make update` で問題なく完了する(単体でマシンが完全収束する)ことが要件。
ツールの pin 前進は `make upgrade` の専任のまま」。前タスクで判明した
ライフサイクル欠陥(`--exclude=scripts` により新しい run_once installer が
make update 経路のマシンに永遠に届かない — 操作者実機で実証)を解消する。

## Work items

F1 — Makefile `update`: `chezmoi apply --verbose --exclude=scripts` から
`--exclude=scripts` を外す(public 側)。private 側の apply も同様に外す
(chezmoi の run_once 状態は private config で独立管理されるため同じ機構で
ガードされる)。設計根拠を Makefile コメント 1 行と README Lifecycle 節に
明記: run_once はコンテンツハッシュで一度きり = update は「コミット済み
pinned 状態への収束」であり、pin の前進(upgrade)は make upgrade の専任、
という契約は不変。

F2 — `update_codex_superpowers` の stderr 畳み込み: `codex plugin add` の
stderr/stdout を捕捉し、失敗時は codex の生 `Error:` 行を出さず、既存の
案内 2 行(unavailable + codex login 手順)のみを表示。成功時は成功 1 行。
捕捉した生出力は debug 用に DOTFILES_DEBUG 時のみ表示。

F3 — テスト追随: tests/install/common/lifecycle.bats の
`--exclude=scripts` を前提とする assert を新仕様へ(update が exclude なしで
apply を 1 回呼ぶこと)。test_runtime_health に superpowers 失敗時
「Error: を含まず案内 2 行を含む」ケースを追加。

## 検証(ユーザーと同一経路で行うこと — 必須)

- VM(adh-test)scratch user で「既に bootstrap 済みのマシン」を再現:
  (1) 旧 main 相当で setup 済み状態を作る(chezmoi init + apply 済み、
  run_once 記録あり)、(2) 本 worktree の変更を含むソースへ更新、
  (3) **文字どおり `make update` を実行**し、新規 run_once(例: 51-client-
  default-shell)が実行されること・exit 0 で完走することを逐語で実証。
  (4) 続けて 2 回目の `make update` で run_once が再実行されず、chezmoi
  drift 警告ゼロで完走することを逐語で実証(冪等ゲート)。
- F2: 未認証 codex での make update 相当実行で、出力に `Error:` が含まれず
  案内 2 行のみであることを逐語で。
- shellcheck / shfmt / bash -n。bats はローカル実行禁止(CI)。
- `.orchestration/validation/dot-update-conv-T1-a01.md` へ全て記録。

## Scope

allowed_files: `Makefile`, `README.md`, `scripts/update-agent-assets.sh`,
`tests/**`,
`.orchestration/{tasks,reports,validation,sandboxes,learning,autoskill/runs}/dot-update-conv-T1-a01.md`,
`.agents/worklog/codex/**`

forbidden_actions: git commit 禁止、push 禁止、bats ローカル実行禁止、
VM は `limactl shell adh-test` のみ(scratch user 削除、credential 持込み禁止、
codex login 禁止)、mise config/lock 変更禁止、home/ 配下の変更禁止、
新規トップレベルディレクトリ作成禁止。

## 完了

done_signal=AGMSG-RESULT。max_turns=30。CompactionDB memory add + ID。
