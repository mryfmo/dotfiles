# dot-ubuntu-parity-T13-a01 — CI 修正: macOS bash 3.2 の空配列 unbound

## Objective(CI aeb45d0、Unit test / macos-14 のみ失敗)

`executable_herdr-agents:273` の `worker_args[@]: unbound variable`。
macOS の /bin/bash 3.2 は `set -u` 下で **空配列の `"${arr[@]}"` 展開を unbound エラー**にする
(bash 4.4+ は合法 — Ubuntu では再現しないため T11 検証をすり抜けた)。

## Work item(1 コミット: `fix(herdr-agents): expand worker args portably for bash 3.2`)

- 該当展開を bash 3.2 互換のイディオム `${worker_args[@]+"${worker_args[@]}"}` へ
  (同ファイル内に既存の同種イディオムがあればそれに合わせる。他の配列展開にも
  同じ罠がないか T11 追加分を全数点検し、点検結果を report へ)。
- `tests/unit/test_herdr_agents.py`: 空 args(プロファイル env が空/未定義で
  worker_args が空になる)ケースを bash 3.2 でなくても検出できる形で追加
  (`bash -u` で… Linux bash では再現不可のため、少なくとも「args 空でも起動成功」を
  現行 bash で担保。macOS 固有再現は CI に委ねる旨を明記)。
- `make format` / `make unit-test` green。

## Scope

allowed_files: `home/dot_local/bin/common/executable_herdr-agents`, `tests/unit/test_herdr_agents.py`,
`.orchestration/{reports,validation,sandboxes,learning,autoskill/runs}/dot-ubuntu-parity-T13-a01.md`,
`.agents/worklog/codex/**`

forbidden_actions: push 禁止、PR 作成禁止、chezmoi apply 禁止、実 `$HOME` 変更禁止、
main への直コミット禁止、live herdr 操作禁止。agmsg は自分の inbox と最後の RESULT 1 通のみ。

## 手順

git fetch origin && git checkout -b fix/bash32-empty-array origin/main。
done_signal=AGMSG-RESULT。max_turns=15。cost 行を report に。
