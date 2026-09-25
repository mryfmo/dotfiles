# dot-herdr-sheldon-T1-a01 — herdr reload の protocol 不一致耐性 + sheldon client 参照欠落

## Objective

操作者の spark 実機ログで確定した 2 問題を修正する。

## Work items

F1 — Makefile update の herdr reload(実ログ: `protocol_mismatch: client
protocol 20 is older than server protocol 22` で `make update` が最終段で
exit 1):

- herdr の pin 前進直後は稼働中 server と CLI の protocol 不一致が構造的に
  発生する。`running)` 分岐で reload の出力を捕捉し、`protocol_mismatch` を
  検出した場合は「herdr が更新されたため server の再起動が必要。
  `herdr server stop` 後に再起動(または Ghostty セッション再作成)し、
  `herdr server reload-config` を手動実行」という 1 行案内を出して
  **make は成功で継続**。それ以外の reload エラーは従来どおり fail。
- lifecycle.bats の herdr reload 系テストに protocol_mismatch 分岐を追加。
- README の該当記述(reload 失敗時の扱い)を新挙動に追随。

F2 — sheldon client プロファイルの `~/.local/bin/client` 参照(実ログ:
`error: failed to install source '~/.local/bin/client' … matches 0
directories`):

- 公開リポジトリは `dot_local/bin/{server,common}` のみ配布で `client/` は
  存在しない(git 履歴確認: 603a007 で private legacy として削除)。
  private 未適用の Linux client 全機で sheldon が毎回エラーになる。
- 修正: `plugin_sources/client/ubuntu.toml` の `[plugins.ubuntu-command]`
  (local dir 型)を、bashrc の private ガードと同じ思想の inline 型へ変更:
  `[ -r ~/.local/bin/client/ubuntu.sh ] && source ~/.local/bin/client/ubuntu.sh`
  (zsh-defer 併用は同 profile の他 inline と揃える)。private が同 path を
  配布しているマシンでは従来どおり読み込まれることをコメントで明記。
- `client/common.toml` の path/fpath への `${HOME}/.local/bin/client(N-/)`
  追加は zsh の (N-/) glob で存在時のみ展開されるため現状無害 — 変更不要で
  あることを validation で確認・記録。

## 検証

- shellcheck/shfmt(Makefile 内シェル断片は bats 経由)、TOML 構文
  (python tomllib で両ファイル parse)。
- F1: mock herdr で protocol_mismatch を返す fixture → make update 相当が
  案内を出して exit 0、他エラーでは exit 1 の両分岐 trace。
- F2: VM scratch user(private なし)で sheldon lock 相当を実行し
  「matches 0 directories」エラーが出ないこと、`~/.local/bin/client/ubuntu.sh`
  を置いた場合に source されることの trace。
- 関連 unit/bats 更新。bats ローカル実行禁止(CI)。

## Scope

allowed_files: `Makefile`, `README.md`,
`home/dot_config/sheldon/plugin_sources/client/**`, `tests/**`,
`.orchestration/{tasks,reports,validation,sandboxes,learning,autoskill/runs}/dot-herdr-sheldon-T1-a01.md`,
`.agents/worklog/codex/**`

forbidden_actions: git commit 禁止、push 禁止、bats ローカル実行禁止、
VM は `limactl shell adh-test` のみ(scratch user 削除、login 禁止)、
mise config/lock 変更禁止、新規トップレベルディレクトリ作成禁止。

## 完了

done_signal=AGMSG-RESULT。max_turns=30。CompactionDB memory add + ID。
