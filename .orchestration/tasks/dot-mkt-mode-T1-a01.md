# dot-mkt-mode-T1-a01 — marketplace.json の two-writer mode drift 解消

## Objective

操作者の spark-9e8d 実ログで再現した恒久 drift を解消する:
`~/.agents/plugins/marketplace.json` は chezmoi 管理(mode 644)だが、毎回の
`make update` で `crit install codex-plugin --force` が umask で再書込みする
ため、Ubuntu(umask 002)では 664 になり、chezmoi apply が毎回
「has changed since chezmoi last wrote it?(old mode 100644 / new mode 100664)」
を出す。内容差分はゼロ、mode のみ。

## Work items

F1 — `scripts/update-agent-assets.sh` の `update_codex_crit`:
`crit install codex-plugin --force` の直後に
`chmod 644 "${HOME}/.agents/plugins/marketplace.json"`(ファイル存在時のみ)を
追加し、chezmoi の期待 mode へ正規化する。crit が書く他ファイル
(`~/.codex/plugins/**` 等)は chezmoi 非管理のため対象外。
併せて、crit が marketplace.json の**内容**を chezmoi source と異なる形に
書き換えるケースがないか確認(操作者ログでは内容差分ゼロだったが、
`crit install` 後の内容と `home/dot_agents/plugins/marketplace.json` を
diff して validation に逐語記録。差分が出る場合は方針を報告して blocked)。

F2 — 回帰検証(今回の見逃しの直接対策):
adh-test VM の scratch user で、fresh 状態から `make update` 相当の
agent-assets 実行(crit install 含む)を **2 回連続**実行し、2 回目の
`chezmoi apply --verbose --exclude=scripts`(または `chezmoi status`)が
marketplace.json の drift を報告しないことを逐語で実証。umask 002 を明示設定
して Ubuntu 既定を再現。

F3 — 単体 test: update_codex_crit の chmod 実行を既存 mock パターン
(test_runtime_health)で 1 ケース追加。

## Scope

allowed_files: `scripts/update-agent-assets.sh`, `tests/**`,
`.orchestration/{tasks,reports,validation,sandboxes,learning,autoskill/runs}/dot-mkt-mode-T1-a01.md`,
`.agents/worklog/codex/**`

forbidden_actions: git commit 禁止、push 禁止、bats ローカル実行禁止、
VM は `limactl shell adh-test` のみ(scratch user 削除、credential 持込み禁止、
codex login 禁止)、mise config/lock 変更禁止、home/ 配下の変更禁止
(chezmoi source 側は動かさない)、新規トップレベルディレクトリ作成禁止。

## 完了

done_signal=AGMSG-RESULT。max_turns=25。CompactionDB memory add + ID。
