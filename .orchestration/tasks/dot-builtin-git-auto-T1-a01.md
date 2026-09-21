# dot-builtin-git-auto-T1-a01 — setup.sh の --use-builtin-git を auto へ是正

## Objective

`setup.sh` が chezmoi の init/update で `--use-builtin-git true` を無条件強制して
いるのを、upstream デフォルトと同じ `auto` へ是正する。

## 根拠(調査済み事実)

- chezmoi 公式: `useBuiltinGit` のデフォルトは `auto` =「`git` が PATH に
  ない時のみ内蔵 git を使う」。CLI flag も `bool|auto`。
- 内蔵 git(go-git)には fast-forward 可能でも「non-fast-forward update」を
  返す既知バグがある(go-git#358 ほか)。chezmoi メンテナも issue #4647 で
  内蔵 git は実 git より能力が劣ると明言。
- 実観測: Ubuntu 26.04 VM で setup.sh 再実行時に builtin git の
  non-fast-forward エラーを 1 回観測(behind 1 の単純 fast-forward 状態)。

## Work items

1. `setup.sh` の 2 箇所(`chezmoi init` / `chezmoi update`)の
   `--use-builtin-git true` を `--use-builtin-git auto` へ変更。
   周辺コメントがあれば意図(git 不在マシンでの bootstrap 継続)を 1 行で維持。
2. tests/install/common/setup.bats 等で `--use-builtin-git true` を検証している
   assert があれば `auto` へ追随(grep で全参照を確認)。
3. VM 検証(`limactl shell adh-test`、scratch user、終了時 userdel -r):
   (a) git が PATH にある状態で README スニペット(main ではなく
   本 branch は未 push のため、`chezmoi init` 相当の直接実行で可:
   worktree の setup.sh を VM から読める場合はそれを bash 実行、
   DOTFILES_REPO_URL は公開 repo のまま)→ 完走を確認。
   (b) git を PATH から隠した状態(PATH 制限シェル)で同じ init 経路 →
   内蔵 git フォールバックで clone 成功を確認(auto の退行なし)。
   両方の逐語出力を validation へ。
4. shellcheck / shfmt / bash -n。bats はローカル実行禁止(CI で検証)。

## Scope

allowed_files: `setup.sh`, `tests/**`,
`.orchestration/{tasks,reports,validation,sandboxes,learning,autoskill/runs}/dot-builtin-git-auto-T1-a01.md`,
`.agents/worklog/codex/**`

forbidden_actions: git commit 禁止、push 禁止、bats ローカル実行禁止、
VM は `limactl shell adh-test` のみ(credential 持込み禁止、scratch user は
削除)、他ファイルへの変更禁止、新規トップレベルディレクトリ作成禁止。

## 完了

done_signal=AGMSG-RESULT。max_turns=25。CompactionDB memory add + ID。
