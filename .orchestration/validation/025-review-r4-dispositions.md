# Plan 025 review round 4: dispositions (v5)

- 対象: `.orchestration/plans/025-regime-cutover-plan.md` v4（sha256 prefix `33285429`、325 行）への round 4 の審査: red team L-01..L-20（`025-review-r4-redteam.md`、閉じた経路 10 群）、verification の部分 J-01/J-02/J-03/J-04/J-10/J-20/J-21（`025-review-r4-verification.md` §1〜§2 のみ; J-06/J-14 は同文書の本文に現れるので追加で処分）、orchestrator の機械検査（`025-review-r4-orchestrator-checks.md`）。処分は v5（同ファイルを in place で改訂）と handout（`.agents/worklog/orchestrator-glue/pilot/`）の必要分に反映する。書くのは本ファイル、v5、handout のうち所見が要るものだけ。
- 処分の語: `fixed-in-v5` = v5 の該当節（または handout）に反映、`accepted-residual` = owner と測るコマンドを名指しして残す、`rejected` = 一次資料か決定行で退ける、`operator-decision` = v5 が既定と代替を §9 の決定に置き、操作者の決定行で閉じる。
- 集計と設計級の決定は末尾「集計」節。

| id | P | disposition | where in v5 (section) or the reason |
| --- | --- | --- | --- |
| L-01 | P0 | fixed-in-v5 | §1.3 audit 行（`denyWrite` に `<HCOM_DIR>/{config.toml,env,config.env,scripts,integrations,.tmp/launch}`）、§1.7 (0)（`omp-run.sh` は最初の `hcom` 呼び出しより前に `HCOM_DIR` を export し、store を新規作成）、§1.7 (2)(4)(5)（`events`/`transcript`/`kill` の前に store の 4 file 不在を確かめ、あれば `Verdict: blocked (store tainted)`）、§1.2 検査 (2)（`omp_args` 空検査を私設 store にも）、§4 第 2 脚 #7（席からの `config.toml` 書込が拒否、片付け前の store 検査）、handout `srt-audit.json`/`leg2.md` #7 |
| L-02 | P0 | fixed-in-v5 | 決定 (8)。§1.3（profile の書込は allow-list: `agent/{sessions,blobs,cache,history.db,agent.db}` と `run`; `agent/cache/eval-js` は denyWrite; 実行入力の列挙は denyWrite から消え、profile root の残りは allow 外）、§1.3 表 3 行、§3 W5a（render テストが allow-list を固定）、§4 第 2 脚 #3b/#7（第 1 の問い: この allow-list の下で `listening`）、§8（fallback）、§9 決定 (8)、handout `srt-worker.json`/`srt-audit.json` |
| L-03 | P0 | fixed-in-v5 | §1.6 保護パス一覧（`make update` が sandbox 外で実行する 8 パスと `scripts/check-*.{sh,py}`、`tests/**` の gate 分、`.pre-commit-config.yaml`、`.githooks/**`）、§3 W6a（fixture PR は `scripts/update-agent-assets.sh` に触れる形で `refuse 10`）、§9 決定 (6) |
| L-04 | P1 | fixed-in-v5 | §1.9/§3 W3/§7 前書き（`make update` は `update-tree` の先頭で**全体**の `chezmoi diff` と installer の計画（`update-agent-assets.sh --plan`、表示のみ）を出し、apply にも installer にも進まず止まる; `CONFIRM=1` で続行）、§2 Makefile 行、§11 #20、W3 の完了条件（範囲外の新規 template が差分に出る fixture） |
| L-05 | P1 | fixed-in-v5 | §1.10 (a)（keychain の 2 種別: generic `gh:github.com` と internet `github.com`、`-a <操作者 login>` で引き、どちらも exit 44）、§3 W0 完了条件、§4 第 1 脚 #0b（「前」の値 2 本）と第 2 脚 #5 (10)（席から 2 種別）、§7 W0b 行、handout `leg1.md` #0b、`leg2.md` #5 |
| L-06 | P1 | fixed-in-v5 | §1.10 (a)（shim が `GIT_CONFIG_NOSYSTEM=1` を渡し system gitconfig の `osxkeychain` を席から外す; user config の `!gh auth git-credential` だけが残り file store を読む; 操作者端末は system gitconfig の helper 行を外す）、§1.2 shim の `env -i` 列、§4 第 2 脚 #5 (10)（席内 `git config --show-origin --get-all credential.helper`）、W0b の受理検査「push 1 回後も 2 種別が exit 44」、handout `leg1.md` #0b、`leg2.md` #5 |
| L-07 | P1 | fixed-in-v5 | §1.3 worker 行（`denyRead` に `<main>`; `allowRead` は `<clone>` と `<seat dir>`; G-17 の 2 行を畳む）、audit 行（`denyRead` に `<main>`; `allowRead` は `<results dir>`、`<HCOM_DIR>`、`<seat dir>`、review worktree、`<main>/.git`）、§1.2 placeholder 7 つ（`__MAIN__`、`__HCOM_DIR__` を追加）、§4 第 2 脚 #5 (14)/#7（`<main>/README.md` の読取拒否）、§9「読取の残余」行（audit が `<main>/.git` を読む残余）、handout `srt-worker.json`/`srt-audit.json`/`leg2.md` #0/#5/#7 |
| L-08 | P1 | fixed-in-v5 | §1.2（空検査は残骸の検知であって封じ込めではない; 封じ込めは L-02 の allow-list で、検査通過後に file が現れても席の書込は OS が拒む。窓を突けるのは sandbox 外のプロセスだけ）、§3 W5b Behaviour 行 |
| L-09 | P1 | fixed-in-v5 | §1.7 (4)（再試行は nonce を作り直し `out.last.md`・`transcript.txt` を truncate してから起動; 旧 nonce の行は不一致 = `blocked`）、§3 W6a fixture（古い verdict 行が残った再試行が `blocked`） |
| L-10 | P1 | fixed-in-v5 | §1.7 (5)（masker に URL 埋め込み `://[^/@\s]+:[^/@\s]+@`、PEM `-----BEGIN [A-Z ]*PRIVATE KEY-----`、JWT `eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.`、長さ 40 以上の base64 列は復号して同じ pattern に掛け当たれば列ごと伏せる; fixture 1 本に 4 形）、§2 validator 行、§9 S-07 行 |
| L-11 | P2 | fixed-in-v5 | §1.10 (c)（Actions の `can_approve_pull_request_reviews` が `false`）、§4 第 1 脚 #0、§3 W0 完了条件、handout `leg1.md` #0 |
| L-12 | P2 | fixed-in-v5 | §9 決定 (5) の代替欄（App 流は installation token の期限・再発行の担い手・permission の 3 検査を先に書き、W0 をやり直す） |
| L-13 | P2 | fixed-in-v5 | §1.7 (3) と §6（nonce が閉じるのは worker と敵対的 PR による偽造だけ; audit 席自身の verdict は今日と同じく orchestrator が内容を審査する untrusted input） |
| L-14 | P2 | accepted-residual | owner: B-3（W5a）。§4 第 2 脚 #4a（`~/.omp/run/session-owners` の所有者と席の session id の対応を貼る）、§9「`~/.omp/run`」行を「可用性の残余（他席が lease file を先取りできる）、profile 別に分けられるなら B-3 の 1 行」に具体化。閉じる手段が source に無いので残余 |
| L-15 | P2 | fixed-in-v5 | §1.3 audit 行（binding は役割ごとに測る）、§4 第 2 脚 #7（`srt-audit.json` は `false` 先行、`listening` が立たなければ `true` に戻して記録）、handout `srt-audit.json`（`allowLocalBinding: false`）、`leg2.md` #7 |
| L-16 | P3 | fixed-in-v5 | §1.3 表 3 行（`denyRead` に `~/.omp/logs`）、§2 A-2 行（`~/.omp/natives` は実行体 = allowWrite 外、doctor の realpath 述語）、handout `srt-*.json` 3 本 |
| L-17 | P3 | fixed-in-v5 | §1.7 (5)（`.orchestration/` に写すのは `out.last.md` だけ; `transcript.txt` と `sessions/` は `<results dir>` に留める） |
| L-18 | P3 | fixed-in-v5 | §1.6 一覧（`.pre-commit-config.yaml`、`.githooks/**`） |
| L-19 | P3 | fixed-in-v5 | §1.3 worker/orchestrator 行（`denyRead` に `~/.hcom/env`）、§4 第 2 脚 #8（orchestrator 形が `~/.hcom/env` を読めなくても `hcom omp` が通るかを測る）、handout `srt-worker.json`/`srt-orchestrator.json` |
| L-20 | P3 | accepted-residual | owner: §9「読取の残余」行に「自役割の `agent.db` は書込も可能（同 profile の次の席が消費する）」と明記。allow-list（L-02）でも `agent.db` は書けなければ資格情報の refresh が止まるので閉じない。統制は D9 の上限と profile 別の資格情報（F-20） |
| J-01 | P2 | fixed-in-v5 | §1.2（audit 系の log は `<results dir>/tmp/srt-debug.log` = shim 式 `<役割の tmp>/srt-debug.log` どおり）、§1.7（`<results dir>` の中身一覧も `tmp/srt-debug.log`）、handout `leg2.md` #7（読み取り行 2 本を `out/tmp/` に） |
| J-02 | P1 | fixed-in-v5 | §3 X 手順 0 と §7「X 手順 0」行（C-1 の squash merge → `<main>` を main に合わせて `update_hcom_private` → `<canonical>` の `make update`; §1.5 と同順） |
| J-03 | P0 | fixed-in-v5 | 決定 (5) の時期を分割: W0a（準備: machine account、token 2 本、file store 3 つ、ruleset payload の下書き; いつでも）と W0b（切替: keychain の 2 項目の削除、system helper 行の除去、ruleset の approval 1、Actions switch の確認; **X 手順 5 の最後の agmsg 席の撤去後 = 手順 5b**）。§1.10、§3 W0 行と X 手順 2 (f)/5b、§7 W0a/W0b 行、§8 W0 行、§9 決定 (5)、§11 #18。W2〜W6 は今日の席で keychain の token のまま動く |
| J-04 | P2 | fixed-in-v5 | §1.2 署名（`hcom-seat worker <name> [<dir>] …` / `hcom-seat orchestrator|audit|review|security [<dir>] …`）、前書きの `<name>` の定義、§3 X 手順 2 (a)/5、§7 |
| J-06 | P2 | fixed-in-v5 | §1.6（conflict 時の update-branch の後は最終 push 者が orchestrator になるので、sweep と audit のやり直しに加え reviewer store の approve が要る; W0b 後だけ） |
| J-10 | P2 | fixed-in-v5 | 前書き「用語の出所」に `<name>`、W5a/W5b、C-2'、J-N2、J-P、`<base40>`/`<head40>`、`<HCOM_DIR>`、review worktree の定義を初出より前に置いた |
| J-14 | P3 | fixed-in-v5 | §1.2 (a)（role template は `~/.agents/srt/<template>.json`、review/security は `audit.json`） |
| J-20 | P2 | fixed-in-v5 | §3 X 手順 2 (b)（Claude 席からは `chain-integrate.sh` を実 PR 1 本に走らせ、その子として `omp-run.sh --role audit` が立つ; J-N2 の 3 本は不変）、§7 X 手順 2 行 |
| J-21 | P3 | fixed-in-v5 | §11 #17（D-024-97 は投入の 3 本だけを定め、除去時期は定めていない、と書き直し）、Status log v5（round 3 の処分表は 80 行・operator-decision 1 で、D-024-106 の「82 rows, 4 operator-decision rows」は誤記; 訂正は次の decisions 行 = orchestrator 側） |

## 集計

- round 4 の L 20 件: fixed 18、residual 2（L-14、L-20）、rejected 0、operator-decision 0。優先度別 fixed/residual/rejected/operator-decision: P0 3/0/0/0、P1 7/0/0/0、P2 4/1/0/0（residual L-14）、P3 4/1/0/0（residual L-20）。
- verification の部分 J 7 件（J-01/02/03/04/10/20/21）: fixed 7（P0 1、P1 1、P2 4、P3 1）。追加 2 件（J-06 P2、J-14 P3）: fixed 2。
- 設計級の決定（v5 で取った 7 点、代替は v5 §9 決定 (5)〜(9)）: (1) profile の書込を allow-list に反転（L-02、決定 (8)）; (2) 私設 `HCOM_DIR` の実行入力を audit の denyWrite にし、`omp_args` 検査と store 不在検査を私設 store にも（L-01）; (3) 保護パス一覧を `make update` の sandbox 外実行物まで広げ、`make update` は全体の `chezmoi diff` と installer 計画で `update-tree` の先頭で止まる（L-03/L-04、決定 (6)(7)）; (4) W0 を W0a（準備）と W0b（切替 = X 手順 5b）に分け、keychain 2 種別・helper 2 段・`GIT_CONFIG_NOSYSTEM=1`・worker/audit の `denyRead <main>`・`~/.hcom/env` を足す（L-05/L-06/L-07/L-19、J-03、決定 (5)）; (5) 空検査は検知、再試行は nonce と出力対を作り直す、nonce の意味を限定（L-08/L-09/L-13）; (6) masker 4 形、binding は役割ごとに測る、`~/.omp/logs` denyRead、`natives` は doctor 述語、`agent.db` 書込残余（L-10/L-15/L-16/L-20、決定 (9)）; (7) 用語と順序の訂正（J-01/02/04/10/20/21）。
- 本ファイル以外に書いたもの: v5、handout `leg1.md`、`leg2.md`、`srt-worker.json`、`srt-audit.json`、`srt-orchestrator.json`。`events.ts` と `policy.yml` は所見が無く不変。
- v5 の実測: `shasum -a 256` prefix `9ce32b71`、326 行（v4 と同じ行数、行内の改訂）。handout 3 本の JSON は `jq -e .` で構文を確認。
