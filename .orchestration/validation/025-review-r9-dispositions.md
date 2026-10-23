# Plan 025 round 9 処分表（v9 `cc0eac8e` → v10）

- 対象: `025-review-r9-verification.md`（V-01〜V-12）と `025-review-r9-redteam.md`（W-01〜W-12）の 24 件。処分は D-024-122 の決定を転記したもので、本表で再決定はしていない。
- 反映先: `.orchestration/plans/025-regime-cutover-plan.md` v10（349 行、sha256 prefix `782f9024`）。handout `pilot/*` は別文脈が直す（handout 側の項目は「how」列に書く）。
- 処分の型: `fixed-in-v10 <節>` / `residual <owner, 測定>` / `handout-only <file 手順>` / `not-applicable <事実>`。

| id | priority | disposition | how |
| --- | --- | --- | --- |
| V-01 | P1 | fixed-in-v10 §1.6、§1.9、§3 前書き・X 手順 0/2 (b)/5、§7 | W0b 前は除外だけの PR 以外の全 merge（W-step の code PR 全部、§3 に列挙）を、chain が証跡を出した後に操作者が自分の端末で `gh pr merge --squash --match-head-commit <audited head>`; X 手順 0 は操作者 merge、2 (b) と DoD11 は records-only PR か操作者 merge を数える; §7 に W0b 前の行 1 本 |
| V-02 | P1 | fixed-in-v10 §1.6、§7、§11 #19 | W0b 後は操作者の `APPROVED` が監査済の最終 head に乗ってから orchestrator（B）が merge; §7 L234 系の「merge は変わらず操作者」を W0b 後の行で「merge は orchestrator」に揃えた |
| V-03 | P2 | fixed-in-v10 §1.6、§3 W6a、§9 決定 (6)、Status log | `.project-map/**` を除外から落とし除外は 4 項; 理由（追跡 0 本、`.gitignore` L26、`.agents/worklog/**` と同形）を §1.6 に; validate が `git ls-files .project-map` の空を固定、`git add -f` の fixture PR は `refuse 10` |
| V-04 | P2 | fixed-in-v10 §1.1、§1.2、§1.3、§1.9、§7 B-3 行 | 役割表の注（`audit.json` が描画する profile は `audit`・`review`・`security`・`audit-r2`、表と `srt.roles` は 5 行のまま）、`<P>` の定義（model profile 名の大文字、`audit-r2` は `AUDIT`）、denyRead の「4 profile」→「自役割以外の profile」、§1.9/§7 の認証行に `audit-r2`、`hcom-seat` 構文に profile 名 `audit-r2` |
| V-05 | P2 | fixed-in-v10 §1.6、§1.10 (f) | push 文を「PR branch に push するのは machine account だけ: worker PR は A、boundary PR は B、操作者は決して push しない」に（W-01 で boundary PR の author が B になったので v9 の矛盾は消える） |
| V-06 | P2 | fixed-in-v10 §1.6、§3 W6a | chain の保護パス検査は sweep・task-level audit・記録・gate の後、最終 step（merge 可否）で `refuse 10`（証跡は残る; exit 10 の意味を「merge 不可」に広げる）; 操作者が approve/merge するのは監査済の head |
| V-07 | P2 | fixed-in-v10 §3 X 手順 2 (b)、§7 X 手順 2 | リハーサルは records-only の実 PR 1 本; 保護パス PR なら verdict 行は出るが最終 step で `refuse 10` と明記 |
| V-08 | P2 | fixed-in-v10 §4 前書き、#2 | pilot の worker/orchestrator JSON は W0a 前の形で `~/.config/gh` を denyRead に持たず gh は keychain で通る、W0a で足す、の 1 句（leg 2 前書きの同文は別文脈が置いた） |
| V-09 | P2 | fixed-in-v10 §1.6、冒頭の用語行 | `machine account` の初出に「（§1.10 (b)）」; 用語行に A/B を定義; `reviewer store` は v10 で廃止（W-01）なので初出の指示は不要 |
| V-10 | P3 | fixed-in-v10 §3 W0a/W0b 行 | W0b 欄に「操作者の admin token を keychain から `~/.config/gh` の file store へ」 |
| V-11 | P3 | fixed-in-v10 §1.9 | 「PR ごとには何もしない（例外）」を「W0b 前は除外だけの PR 以外の全 merge、W0b 後は保護パス PR の approve、それ以外は何もしない」に |
| V-12 | P3 | fixed-in-v10 §7 L213、§4 前書き/L123/#10、§7 W1 行 | 「v8 の採択」「v8 で更新」→ v10; 第 1 脚の所要を 60〜75 分に統一（handout の値）; §4 #10 の kill 一覧に `tag:pilot3u`（leg 2 #10 は別文脈） |
| W-01 | P1 | fixed-in-v10 §1.3、§1.6、§1.10 (a)(b)(f)、§3 W0a、§7 W0a (1)(2)(3)/X 手順 5b、§8 W0、§9、§11 #18、決定 (5)、Status log | orchestrator 席の merge store は machine account **B** の fine-grained token（Contents rw、Pull requests rw、Metadata read; Administration/Actions/Workflows/Secrets/Environments/Variables 無し）; worker は A のまま; 操作者 account の token は操作者自身の `~/.config/gh` だけで全席 denyRead; v9 の reviewer store `gh-reviewer` は置かない（席の store に PR write の第 2 login があると ruleset はその approve を数える）; worker PR は A 作、boundary PR は B 作、approve は操作者だけ; B の A 作 PR への approve は ruleset が数えるので chain は approver の login = 操作者 account を見る; B は自作 PR を approve できない（self-approval 禁止）; W0a 受理に「席の 2 store に操作者 account の login が無い」、(f3) に B の self-approve 拒否; 代替 = GitHub App の installation token（決定 (5) の副選択）; U-06/U-08 行に「両経路を閉じる理由」と残る経路（B approve + merge = chain の login 検査と `make update` の停止） |
| W-02 | P1 | fixed-in-v10 §1.6、§1.10 (c)(f)、§2（+1 行）、§3 W0a/W6a、§6 記録、§7 X 手順 5b、§11 #14/#21、決定 (6) | `.orchestration/plans/**` を名指し保護（操作者が §7 の行をそこから写す）; `scripts/orchestrator/ruleset-main.json` を W6a が README の payload から新設し README は pointer、`scripts/**` 配下で保護; W0b の受理 = `gh api rulesets/<id>` の `jq -S` 射影と正本 file の `diff` が空; 5b の PUT はその file を `--input` に |
| W-03 | P2 | fixed-in-v10 §1.10 (d)、§11 #18 | file store + denyRead は srt 席に対しては Seatbelt の path 規則で keychain より強い（基本 profile は securityd を常に許す【srt facts L59】）; hold 中の Claude pane と J-N2 の chain は X 手順 4 まで srt 外で、そこでは設定であって統制ではない（操作者自身のプロセスと同じ信頼）; 手順 4 が 5b の admin-token 移動より先にある理由として書いた |
| W-04 | P2 | residual（owner = W0a (3) の開いた測定、測定 = `.github/workflows/**` を触る PR の push と merge が B の token で通るか） | 開いた測定は残す; 行を追加: 要るなら W0b 後の `.github/workflows/**` の変更（W0c-late、D、E2 の `regime.yml` 除去、`agent-assets.yml` の pin 更新）は全部操作者 author + 操作者 merge、操作者 author の PR は approver = B（§1.10 (a)、§3 W9/D/経路外、§7 +1 行）; 否定 3 本は補助で token 設定画面が正本 |
| W-05 | P2 | fixed-in-v10 §1.7 (4)、§3 W6a | 前提を `pgrep -f -- '--profile audit( \|$)'` と `pgrep -f -- '<results dir>/'` の 3 分岐（両方 exit 1 → 再試行、どちらか 0 → block、pgrep 不能 → block = fail-closed）に; 「検知であって封じ込めではない、封じ込めは profile 分離」を 1 文; W6a に fixture |
| W-06 | P3 | fixed-in-v10 §1.7 (4) | canary が測るのは pane 閉鎖の経路だけ（`trap '' HUP` の子と srt が kill しない孤児は別経路）を 1 句（pid file を書かせる prompt は別文脈が handout に置く） |
| W-07 | P2 | fixed-in-v10 §1.6、§3 W6a、§11 #19 | chain 規則: author = A の PR が `.orchestration/` に触れてよいのは file 名に自 task id を含む file だけ、`.orchestration/tasks/<自 id>.md` は不可（W0b 後は `gh pr view --json author`、前は head の committer）; task 本文と記録は B の boundary PR; W6a に fixture 1 本 |
| W-08 | P2 | fixed-in-v10 §8 STOP、§3 W0c `threat_table`、§3 W6a validate | STOP を base 文脈 trigger（`pull_request_target`・`workflow_run`・`issue_comment`）と `uses: ./.github/workflows/` で到達する reusable workflow に広げ、validate は `uses:` を 1 段たどる; 今日の inventory は `regime.yml` の `pull_request_target` だけで `environment:`・`workflow_call`・`uses: ./` は 0 と明記 |
| W-09 | P2 | fixed-in-v10 §1.7 (1)、§4 #8b、§9 Q-08 行 | `omp-run.sh` は `env -i PATH=<seat dir>:<seat dir>/bin:<herdr binary の dir>:/usr/bin:/bin HOME HCOM_DIR TMPDIR HERDR_SOCKET_PATH` で hcom を呼ぶ（`form=envi`; hcom の実体が持つ他の marker 名に依存しない）; #8b の第 2 形は `form=envi`（tag `pilot3u`）で合格基準は `form=envi Q08-PASS-shim`、起動失敗は `LAUNCH-FAIL`; `launched_by` の帳簿の損失は verdict が file と nonce で届くので無害（handout の loop 本体は別文脈） |
| W-10 | P2 | fixed-in-v10 §1.6、§3 前書き・W6a・X、§7 | V-01/V-06 と同じ文: 保護パス検査は証跡の後の最終 step（報告）、W0b 前の code PR は操作者 merge、X 2 (b) と DoD11 は records-only PR か操作者 merge を数える |
| W-11 | P3 | fixed-in-v10 §1.10 (f)、§9（+1 行） | merge token（B）の余剰を 1 行に: `gh-pages` への push、PR の title/body 編集、review の dismiss、`--auto` の有効化、branch/tag の作成・削除、release 作成 = どれも main には届かない |
| W-12 | P3 | fixed-in-v10 §1.6、§3 W6a、決定 (6) | V-03 と同じ処分（`.project-map/**` を落とす、`git add -f` の fixture PR は `refuse 10`、validate の空検査） |

集計: fixed-in-v10 23、residual 1（W-04）、handout-only 0、not-applicable 0。operator-decision: W-01（決定 (5) の既定の書き換えと副選択）。
