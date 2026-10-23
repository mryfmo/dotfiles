# Plan 025 round 11 処分表（v11 `eb4e3192` → v12）

- 対象: `025-review-r11-verification.md`（Z-01〜Z-07）、`025-review-r11-redteam.md`（Z-11〜Z-24）の 21 件。処分は D-024-127 の決定を転記したもので、本表で再決定はしていない。
- 反映先: `.orchestration/plans/025-regime-cutover-plan.md` v12（356 行、sha256 prefix `674cf254`）。handout `pilot/*` は別文脈が直す（handout 側の項目は「how」列に書く; 本 round の handout 側 4 点（`leg2.md` #7 `pgrep_pos`、#8 `pgrep -f 'profile pilot-[w]orker'` と `lsof -t -- $PILOT/clone`、#10 `sleep 2`）は反映済で両脚の見出しは v12、行数 111/115）。
- 処分の型: `fixed-in-v12 <節>` / `residual <owner, 測定>` / `handout-only <file 手順>` / `not-applicable <事実>`。
- 根拠の出所: `Makefile` L55〜L95（`update` は旧 Makefile で `git fetch` → `git pull --ff-only`、その後 `$(MAKE) update-tree` が pull 後の Makefile を読む）、【gh F5】= `gh-actions-facts.md` F5（code owners は base branch の file で評価）。

| id | priority | disposition | how |
| --- | --- | --- | --- |
| Z-01 | P1 | fixed-in-v12 §4 #8、§1.7 (4) | `pgrep_exit` の pattern を自分を包む `sh -c` の argv に当たらない `pgrep -f 'profile pilot-[w]orker'`（#4 の pilot2 席 `--profile pilot-worker` に当たる）にし、期待を「0 = 他 sandbox の pilot2 が列挙できた、1 = 見えない = §1.7 (4) の第 3 分岐が実在、それ以外 = 拒否」に直して `wpid` の `ps -p` と並べて読む; `leg2.md` #8 は同じ pattern に更新済 |
| Z-02 | P2 | fixed-in-v12 §1.10、§3 W0a/W0b 行、§9 Y-09 行・決定 (5) | W0b 前の手 merge は ≒ 11 本（W-step の code PR 10 本 + `ruleset-main.json` の PR）; W0b の記録 PR は PUT と受理の後に書くので W0b 後の規則（操作者 approve → B merge）に従い手 merge に数えない; §3 W0a/W0b 行の完了条件を「訂正 PR は PUT 前・操作者 merge、記録 PR は PUT 後・approve → B merge」に分けた |
| Z-03 | P3 | fixed-in-v12 §7 採択行 | 「本計画 v10 の採択」を `v12` に |
| Z-04 | P3 | fixed-in-v12 §8 W0 | 「固定値一覧 10 項と `codeowners/errors` 空を含む」を「固定値一覧 12 項（`allow_auto_merge: false`・`codeowners/errors` 空・CODEOWNERS 本文・`rules[].type` の集合を含む）」に（二重計数を解消、項数は Z-11/Z-12 で 12） |
| Z-05 | P2 | fixed-in-v12 §4 #10 | 計画側を handout に揃え「`pgrep` の前に `sleep 2`（2 秒の settle）」に; `leg2.md` #10 は `sleep 2` のまま |
| Z-06 | P3 | fixed-in-v12 §4 前書き | handout 一覧の「v10 で更新」を「v12 で更新」に（両脚の見出しは v12） |
| Z-07 | P3 | handout-only `leg2.md` #8b L102/L103/L105/L111 | 所見 id `Y-12`/`Y-15`/`Y-18`/`Y-19`/`Y-20` を処分表どおり `Y2-` 前置に揃える; 計画側に変更無し |
| Z-11 | P1 | fixed-in-v12 §1.10 (f)、§3 W0a/W0b 行、§7 5b、§8 W0 | 5b の固定値一覧に 11 項目め: PUT の直前に操作者端末で `gh api repos/<o>/<r>/contents/.github/CODEOWNERS?ref=main --jq .content \| base64 -d` が `* @<操作者 login>` の 1 行ちょうど、かつ `git log --oneline <W6a の merge sha>..origin/main -- .github/CODEOWNERS` が空（W6a〜5b の窓で B が owner 行を書き換えた merge を受理が見る） |
| Z-12 | P3 | fixed-in-v12 §1.10 (f)、§3 W0a/W0b 行、§7 5b、§8 W0 | 12 項目め: `rules[].type` の集合 = `{deletion, non_fast_forward, pull_request, required_status_checks}` ちょうど（禁じる側の 2 規則が落ちていないことを目で見る） |
| Z-13 | P1 | fixed-in-v12 §1.6、§1.9、§2 Makefile 行、§3 W3、§7 見出し・W0b 前の行、§9 G-07 行・決定 (7)、§11 #20 | 停止の第 1 段（source 側 `git log --oneline HEAD..origin/main`/`git diff --stat`、操作者 token の `gh pr list … --json number,mergeCommit,mergedBy,files,changedFiles`、sha 突合、`mergedBy` 規則）を `update` target の `git fetch` 後・`git pull` 前に移し、既に適用済みの Makefile が実行して不一致なら pull せず非 0 終了（`Makefile` を含む敵対 merge でも外せない）; 第 2 段（`chezmoi diff` + installer 計画 + `CONFIRM=1`）は `update-tree` 先頭のまま; §1.9 の「orchestrator に依存しない統制」の句を落とし、O-09 の「Makefile の変更は停止を外せる」を「第 2 段だけ外せる」に; W3 に第 1 段が pull 前に止まる fixture 1 本と完了条件 1 句 |
| Z-14 | P2 | fixed-in-v12 §1.9、§7 W0b 前の行 | CONFIRM 拒否後の次手: `<canonical>` は fetch 済み・未 pull のまま（Z-13 の移設後は戻す操作が無い）、操作者が `gh pr view <n> --json mergeCommit` の sha を取り B に `git revert <sha>` の PR を作らせ、W0b 前は操作者が手 merge、W0b 後は操作者 approve → B merge の後に `make update` をやり直す |
| Z-15 | P2 | fixed-in-v12 §1.9、§3 W3、§7 見出し、§9 G-07 行・決定 (7)、§11 #20 | 第 1 段の一覧に `changedFiles` を足し、各 PR で `changedFiles == length(files)` でなければ一覧が不完全（GraphQL の `files` は 1 ページ分）として拒む |
| Z-16 | P2 | fixed-in-v12 §1.10 (a)、§3 X 5b、§7 5b | 5b の前提: 操作者端末で `gh pr list --state open --author <操作者 login> --json number` が `[]`（残る PR は close して B が同じ head を別 branch から再 author; 5b 後は操作者 author の PR を誰も approve できない） |
| Z-17 | P3 | fixed-in-v12 §1.10 (a) | Y-04 の文を「操作者は W0b 後は PR を author しない」にし、W0b 前の agmsg 席の PR（author = 操作者 account）は Z-16 の前提で掃く、と 1 句 |
| Z-18 | P3 | fixed-in-v12 §9 W-11 行 | chain 外の merge 自動化（merge queue は Administration の規則で B は作れず、Dependabot の auto-merge は `allow_auto_merge: false` が閉じ、PR 側 workflow の `GITHUB_TOKEN` の merge は approval 1 + code owner で止まる）は W0b 後に main へ届かない、と 1 句 |
| Z-19 | P3 | fixed-in-v12 §9 W-11 行、決定 (11) | Workflows write を足した B は保護の無い branch に `on: push` の workflow を push して走らせ repository secret を読める（environment secret は branch rule `main` で届かない; 今日は `CODECOV_TOKEN` だけ = 決定 (11) の残余と同 class）を W-11 の余剰列挙と決定 (11) に |
| Z-20 | P2 | fixed-in-v12 §4 #8、§1.7 (4) | #8 の srt 形に `lsof -t -- $PILOT/clone; echo lsof_exit=$?`（pilot2 が `--dir` = cwd として開いている dir; `out/sessions` と私設 `hcom.db` はその時点で誰も開いていない）を足し、`pgrep_exit` と同じ 3 読み（0 = 列挙できた、1 = 見えない → §1.7 (4) の `lsof` 前提は「常に block」に倒す、それ以外 = 拒否）; `leg2.md` #8 は反映済 |
| Z-21 | P2 | fixed-in-v12 §4 #7 | kill の前に正一致 `pgrep -fl 'profile pilot-[a]udit'; echo pgrep_pos=$?` を打ち、期待は 1 行以上かつ `pgrep_pos=0`; 出なければ §1.7 (4) の再試行前提は残骸を見られない = 記録し、pattern を席が実際に受ける argv に合わせる; `leg2.md` #7 は反映済 |
| Z-22 | P3 | fixed-in-v12 §9 読取の残余行 | L-20 の残余文を「自役割の `agent/{cache,agent.db,sessions}` は読めて書ける（次の席が `agent.db`、`cache`（eval-js 以外）、`sessions`（`handoffSaveToDisk` の置き場）を消費する）」に |
| Z-23 | P2 | fixed-in-v12 §1.10、§3 X 4/5b/6、§7 X 手順 4/6・5b、§8 X | X 手順 4 で旧 Claude pane を閉じ以後 resume しない（rollback は Claude pane の新規起動 + J-N2）; 5b の前提に `pgrep -fl claude` が空（Claude pane の process が無い）; 手順 6 は「旧 pane は手順 4 で閉じ済み、DoD11 + 24 時間の観測」 |
| Z-24 | P2 | fixed-in-v12 §1.9、§1.10 (a)(e)(f)、§7 W0a (3)・5b・W0b 前の行 | fail 路の次手 4 つ: (a) `mergedBy` 不一致は CONFIRM を打たず Z-14 の revert PR; (b) push 後の keychain 2 本が 44 でなければ止め、項目を再度消して helper 行を確かめ 44/44 まで (f) に進まない; (c) `codeowners/errors` 非空は PUT の前に B の PR で file を直して操作者が手 merge し再確認; (d) 席の store に操作者 login があればその store を消して token を入れ直し、席を再起動して再検査 |

集計: fixed-in-v12 20、residual 0、handout-only 1（Z-07）、not-applicable 0。operator-decision: 無し（決定 (5)(7)(11) は既定の字面だけ更新、新設の決定行無し）。
