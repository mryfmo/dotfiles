# dot-docs-align-T1-a01 — 文書監査 8 件の整合修正(同一ブランチ続行)

## Objective

読み取り専用文書監査(origin/main=788ba3b 時点)で確定した 8 所見を、
dot-herdr-sheldon-T1-a01 と同じブランチ上で修正する(1 PR に統合)。

## Work items(監査番号順)

1. README.md:310 付近 — `herdr agent start <agent-name> --cwd <worktree>` は
   実在しない用法。実装(executable_herdr-agents)どおり
   「pane 作成時に cwd を与え(`herdr pane split ... --cwd <worktree>`)、
   `herdr agent start <name> --kind codex --pane <id>` で起動」へ書き換え。
2. README.md:292 / :338 — `--split right` を実実装
   (`pane split --direction right` + `agent start --kind codex --pane`)へ。
   agent 名の記述(codex-worker-${workspace_id})は維持。
3. scripts/update-agent-assets.sh:6-9 の @description を現職務
   (marketplace/plugin 更新に加え、gh 拡張収束、pinned release バイナリ
   (crit/tode/terminal-browser)、CompactionDB 同期、herdr 統合)へ更新。
4. README.md:198-201 の Crit 段落へ #169 の 2 挙動を追記:
   `~/.local/bin/crit` を権威パスとして直接検査+PATH 前置+hash -r すること、
   `REPAIR=1 make doctor` が欠損 crit を修復できること。
5. README.md:146-160 の make update ステップ列挙へ 3 工程を追加:
   gh CLI 拡張の収束、CompactionDB 同期、最後の `make agmsg-bootstrap`。
   README.md:184 の「agent-managed assets」文にも gh 拡張と CompactionDB を反映。
6. README.md:129 のコードブロック注釈を「without advancing tool pins」系の
   正確な文言へ(prose 側と整合)。
7. Dockerfile — `FROM ubuntu:22.04` → `ubuntu:24.04`。apt の `bats` を削除
   (mise pin と AGENTS.md の bats ローカル禁止方針により死荷重)。
   検証: adh-test VM 内の docker で `docker build` が成功すること
   (`limactl shell adh-test -- docker build ...` — repo は VM から読める。
   build のみ、run は不要)。イメージ/中間物は build 後に削除。
8. home/dot_agents/README.md:37 — Parity policy の番号飛び(…7,9)を連番へ。

## 検証

- README/Dockerfile の変更は validate-agent-assets.py の必須トークンを壊さない
  こと(`uv run --with pyyaml python scripts/validate-agent-assets.py` green)。
- 変更した herdr 記述が tests/unit/test_herdr_agents.py の実引数 assert と
  一致すること(該当 assert の行を validation に引用)。
- Dockerfile: VM 内 docker build の逐語末尾(成功行)+ cleanup 確認。
- shellcheck/shfmt(触れたシェル)、既存 unit の green。

## Scope

allowed_files: `README.md`, `Dockerfile`, `scripts/update-agent-assets.sh`
(ヘッダコメントのみ), `home/dot_agents/README.md`, `tests/**`,
`.orchestration/{tasks,reports,validation,sandboxes,learning,autoskill/runs}/dot-docs-align-T1-a01.md`,
`.agents/worklog/codex/**`

forbidden_actions: git commit 禁止、push 禁止、bats ローカル実行禁止、
VM は `limactl shell adh-test` のみ(docker build/後片付けに限定、login 禁止)、
mise config/lock 変更禁止、実装ロジックの変更禁止(文書とコメントと
Dockerfile のみ。#3 はコメントのみ)。

## 完了

done_signal=AGMSG-RESULT。max_turns=25。CompactionDB memory add + ID。
