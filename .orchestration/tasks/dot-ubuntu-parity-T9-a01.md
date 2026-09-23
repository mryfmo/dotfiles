# dot-ubuntu-parity-T9-a01 — CI 修正: timer enable を実 HOME 配下の unit 存在でガード

## Objective(2026-09-23、CI run(95bd97c の Snippet install / public-bootstrap ubuntu client)再失敗)

T5(after_ 化)後も同じ失敗が再発:
```
Failed to enable unit: Unit file usage-snapshot.timer does not exist.
```
根本原因(2 つ目): Snippet install の public-bootstrap は setup.sh の CI ガードにより
**RUNNER_TEMP 配下の仮 destDir** へ適用する。unit ファイルは仮 HOME に書かれるが、
`systemctl --user` は実ユーザーの `${XDG_CONFIG_HOME:-$HOME/.config}/systemd/user` しか
読まないため、after_ でも enable が失敗する。実マシン(destDir == $HOME)では T5 の
after_ で十分だが、CI の temp-dest 適用では unit が systemd から永遠に見えない。

## Work item(1 コミット: `fix(usage): only enable the timer when its unit is visible to the user manager`)

- `home/.chezmoiscripts/ubuntu/run_onchange_after_60-enable-usage-snapshot-timer.sh.tmpl` の
  ガードに、systemd が実際に読む場所での unit 存在チェックを追加:
  `[ -f "${XDG_CONFIG_HOME:-${HOME}/.config}/systemd/user/usage-snapshot.timer" ]` を満たさない
  場合は「unit not visible to the user manager (temp destDir apply?); skipping」を echo して exit 0。
  既存の systemctl/XDG_RUNTIME_DIR ガードは保持。sha256 埋め込みコメントも保持。
- なぜ file 存在チェックが temp-destDir と将来の順序退行の両方を安全に覆うかを
  スクリプトコメント 1〜2 行と report に明記。
- 検証: `chezmoi execute-template` でレンダリングし bash -n、さらに
  (a) unit が実在する場合と (b) HOME を仮ディレクトリにした場合の両方で
  レンダリング済みスクリプトを直接実行して exit 0 を逐語確認(systemctl enable の
  実行は (a) では発生してよい — このマシンでは timer は既に enable 済みで冪等)。
- ブランチ: main から `fix/usage-timer-visibility`(fetch してから)。
  `git -c commit.gpgsign=false commit`、Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>。
- CompactionDB decision: 「Snippet install CI は RUNNER_TEMP destDir へ適用するため、
  実 HOME 前提の副作用スクリプト(systemctl 等)は『効果対象が実際に見える場所に
  存在するか』でガードする」を登録、ID を逐語で。

## Scope

allowed_files: `home/.chezmoiscripts/ubuntu/run_onchange_after_60-enable-usage-snapshot-timer.sh.tmpl`,
`tests/**`,
`.orchestration/{reports,validation,sandboxes,learning,autoskill/runs}/dot-ubuntu-parity-T9-a01.md`,
`.agents/worklog/codex/**`

forbidden_actions: push 禁止、PR 作成禁止、chezmoi apply 禁止、`$HOME` 配下の変更禁止
(検証 (b) は仮 HOME で行う)、main への直コミット禁止、対象外 bats 実行禁止。

## 完了

done_signal=AGMSG-RESULT。max_turns=20。cost 行を report に。
