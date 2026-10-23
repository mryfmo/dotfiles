# Plan 025 round 7 の処分表（v7 → v8）

- 対象: `.orchestration/plans/025-regime-cutover-plan.md` v7（sha256 prefix `3496490d`、335 行）→ v8（341 行、sha256 は本表の末尾）。所見の出所: `025-review-r7-verification.md`（R-01〜R-13）、`025-review-r7-redteam.md`（S-01〜S-13）。処分は orchestrator が決めたもの（D-024-117、D-024-118）で、本表はそれを書き写した。
- 実測の前提【実測 D-024-117】: repository secret は `CODECOV_TOKEN` 1 本だけ、environment は 0、`macos.yaml`/`ubuntu.yaml` の直近の PR run と push run はどちらも skip step だけを実行した。よって S-01/S-02 の経路は潜在で、W0c は設計として臨界路の外に出る。
- 分類: `fixed-in-v8 <節>` / `residual <owner、測定>` / `handout-only <file 手順>` / `not-applicable <貼った事実>`。handout（`.agents/worklog/orchestrator-glue/pilot/*`）は別文脈が直した（`leg1.md` 111 行、`leg2.md` 114 行）。【gh Fn】= `.agents/worklog/orchestrator-glue/gh-actions-facts.md`。

| id | priority | disposition | one-line how |
| --- | --- | --- | --- |
| R-01 | P1 | handout-only `leg2.md` #8b（新設） | `HCOM_LAUNCHED=1` を export した pilot3 の 2 回目と私設 store `$PILOT/hcom-audit/.tmp/launch/` の最新 script の `--hcom-tool-path` grep、`Q08-PASS-shim`/`Q08-FAIL-real-omp` を出す; 計画側は §4 第 2 脚に #8b 行を足し、§9 Q-08 行の owner を #8b に、launch dir を `<HCOM_DIR>/.tmp/launch`【srt Q2】と名指し |
| R-02 | P1 | fixed-in-v8 §1.6、§3 W5a/W5b/W6a、§7、§9 決定 (6)、§11 #19/#21 | 保護パスを反転: `scripts/orchestrator/protected-paths.txt` は**除外一覧**（`.orchestration/**`、`docs/**`、`home/` の外の `*.md`、`tests/**`、`.ua/**`、`.project-map/**`、`.agents/worklog/**`）で、それ以外の全パスが保護; v7 の列挙は例文 1 文に残す; W6a の fixture に `home/dot_config/git/**`・`home/dot_ccstatusline/**` の 2 PR |
| R-03 | P2 | fixed-in-v8 §3 W0c (2)、§2 Makefile 行、§7 W0c の PR 行 | `Makefile` L189 `UV_PYYAML` の `uv run` 3 箇所全部（probe と 2 分岐）に `--no-project`; 完了条件に `grep -c -- '--no-project' Makefile` = 3 |
| R-04 | P2 | handout-only `leg2.md` #7 | `N` と `launch_ts` を起動ブロックの前の main shell の独立行に; 計画 §4 #7 行に「main shell の独立行（pipeline の外）」の 1 句 |
| R-05 | P2 | residual 操作者、測定 = boundary ごとの `gh secret list --app actions` が `CODECOV_TOKEN` 以外を示さない | 決定 (11) 新設（既定: 受容 = 低権限の upload token、rotate 可、疑いがあれば rotate; 代替: upload を push 限定 = PR の coverage を失う）; §2 `test` 行は「残す」+ 残余、§9 に行、§11 #22、W0c `threat_table` に `residual` 行 |
| R-06 | P3 | handout-only `leg1.md`/`leg2.md` の import 直後 | 両脚が `sk_ant_count`（鍵 prefix の `grep -c`、期待 0）を出す; 計画 §4 前書きは orchestrator がそれを見てから写すと書く |
| R-07 | P3 | handout-only `leg2.md` #7 読み取り | handout の `-exec ls -t {} + \| head -1` の形に揃える（r6 処分表の `sort` 形は handout を正とする; 期待文は「JSONL は参考情報」で変わらない） |
| R-08 | P3 | fixed-in-v8 §4 前書き、Status log v7 行 | §4 前書きを「v8 で更新」、Status log v7 の「forbidden 3 本と席 shim canary」を「forbidden 4 本（席 shim canary を含む）」に; handout の見出しは別文脈 |
| R-09 | P3 | fixed-in-v8 §3 前書き、§7 採択行 | W0c が臨界路から外れたので hold を解く順は「W1 ‖ W3 → W2、W0a は並走; W0c は W2 の後（または操作者が private 統合を望む時）」 |
| R-10 | P3 | fixed-in-v8 §1.2、§1.7 (4)、§3 W6a | `<name>`（= `<seat dir>`）にも `-r2` を付ける; W6a の fixture 名を「再試行で旧 nonce の行しか無い = `blocked`」に |
| R-11 | P3 | handout-only `leg2.md` #7/#10 | 私設 store の 4 file 検査を events/kill ブロック先頭でも繰り返し、#10 の `ls` に `hcom-audit/config.toml`; 計画 §4 #7 行に 1 句 |
| R-12 | P3 | handout-only `leg2.md` #0f | `wait_result` の pattern を `task_id=$1 %` に揃える |
| R-13 | P3 | fixed-in-v8 §3 W0c `threat_table` | `workflow_dispatch` を攻撃者 ref に打つ経路の行: `closed` by environment の deployment branch rule【gh F3】と W0a (2) の token に `actions`/`workflow` が無いこと |
| S-01 | P0 | fixed-in-v8 §3 W0c、§2、§7、§8、§9 行と決定 (10)、§11 #21 | 統制を repository setting に移す: environment `private-dotfiles`、deployment branch rule「Selected branches and tags」= `main` のみ、required reviewers 無し（規則は `GITHUB_REF` に照合され `refs/pull/<n>/merge` は入らない【gh F3】; file 内の門は PR が持つ file で評価されるので便宜【gh F1】）; secret は environment secret だけ; PR job は `environment:` 無し、main-push job は `environment:` + `if: push`; 検証に否定の測定 1 本（拒否行）。事実: 今日は秘密が無く経路は潜在【実測 D-024-117】 |
| S-02 | P0 | fixed-in-v8 §3 W0c (0)(3)、§8 STOP、§9 行 | W0c の PR run に積む secret が今日は無い【実測 D-024-117】ので S-02 は空; 以後は §8 の STOP「repository-level の secret は足さない、secret は environment に、要する job は `environment:` を宣言」と「W0c の merge 前に private 統合の secret を設定しない」で固定; v7 の「W0c だけ例外」文は削除 |
| S-03 | P1 | fixed-in-v8 §1.10 (b)、§7 W0a (2)、§3 W0c (2)、§9 GitHub 境界行 | W0a (2) の受理検査に「token に `workflow` scope 無し、permission に `actions` 無し」; `docs.yml` の `contents: write` job も同じ branch rule の environment の後ろ; §9 行: W0b 前に席が操作者の token に届くのは既知の W0 の弱点で、environment 設計の下では「secret 無し、ruleset が許す以上の書込無し」に限られる |
| S-04 | P2 | residual 操作者、測定 = boundary ごとの `gh secret list --app actions` | R-05 と同じ 1 行（決定 (11)、既定: 受容）; W0c `threat_table` に `test.yaml` の `residual` 行 |
| S-05 | P1 | fixed-in-v8 §1.6、§7 保護パス PR 行、§9 決定 (6) | 反転で `home/dot_config/{git,herdr}/**`、starship、gnupg、ssh、ccstatusline、systemd、`executable_*` の置き場所を問わず全部が保護; §7 の「必ず読む」一覧に `*.tmpl` と `home/dot_config/git/**` |
| S-06 | P1 | fixed-in-v8 §1.6、§3 W6a | `home/dot_npmrc`、`home/dot_config/uv/**`、`home/dot_config/mise/**` は反転で保護; 既存 `*.tmpl` の 1 行変更も fixture で `refuse 10`（語一致に依らない） |
| S-07 | P1 | fixed-in-v8 §1.6、§3 W6a | repo root の `.chezmoiroot`・`mise.toml` は除外に無いので保護（basename 規則の「`home/**` のうち」限定も消える）; W6a fixture に `.chezmoiroot` の PR; mise の trust 挙動は未測のまま（反転で経路自体が保護 PR になる） |
| S-08 | P2 | fixed-in-v8 §1.6、§3 W6a | template 関数の語一致を廃止: `home/**` の変更は全部保護パスなので語一致は何も足さず、語一覧（`outputList`、`keyring` 等を欠く）は完全にできない |
| S-09 | P2 | fixed-in-v8 §1.7 (4)、§3 W6a、§4 #7（測定の名指し） | `-r2` は `hcom kill <name>` の後に `ps -p <pid>` が exit 1 のときだけ; 0 なら再試行せずその task の X を block; pid が消えていれば同じ profile の再利用は安全; 第 2 脚 #7 が `ps_exit` を出す（handout 側は別文脈） |
| S-10 | P3 | fixed-in-v8 §1.9 | 停止の第 1 段は subject でなく sha: 一覧の各 sha を名指しの PR の `gh pr view <n> --json mergeCommit` と突き合わせる |
| S-11 | P3 | fixed-in-v8 §1.9 | 停止自身の `git pull`/`git log` が操作者の git 設定（hooksPath、pager、credential helper）を実行するので、`home/dot_config/git/**` が保護パス（反転）であることを前提として明記 |
| S-12 | P3 | fixed-in-v8 §4 #7 | `srt-audit.json` で `seat-audit` を本番の `<seat dir>` と同じ denyRead の内側の `allowRead` に置いて同じ canary を打つ（設定 2 行）; JSON の変更は別文脈 |
| S-13 | P2 | fixed-in-v8 §3 W0c `threat_table`、§9 行 | `schedule` は default branch の file だけで `closed`; `contains(github.actor,'[bot]')` は統制ではないと明記; `agent-assets.yml`/`remote.yaml` は secret を持たない（`GITHUB_TOKEN` のみ、`contents: read`、確認済） |

集計: 26 行 = fixed-in-v8 18（R-02 R-03 R-08 R-09 R-10 R-13 S-01 S-02 S-03 S-05 S-06 S-07 S-08 S-09 S-10 S-11 S-12 S-13）、residual 2（R-05 S-04、同じ残余 = 決定 (11)）、handout-only 6（R-01 R-04 R-06 R-07 R-11 R-12）、not-applicable 0。priority: P0 2、P1 6、P2 7、P3 11。操作者決定: 決定 (10) の書き換え（S-01/S-02）と決定 (11) の新設（S-04/R-05）。

v8 の数: 341 行、§2 は 50 行、§9 は 11 決定、§11 は 22 行、§4 第 2 脚に #8b。sha256 prefix は Status log v8 の採択記録（D-024 次行）に貼る。
