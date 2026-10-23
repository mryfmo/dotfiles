# Plan 025 review round 5: dispositions (v6)

- 対象: `.orchestration/plans/025-regime-cutover-plan.md` v5（sha256 prefix `9ce32b71`、326 行）への round 5 の審査 4 本: verification M-01..M-12（`025-review-r5-verification.md`）、leg-1 handout dry run N1-01..N1-15（`025-review-r5-leg1.md`）、leg-2 handout と srt settings N2-01..N2-15（`025-review-r5-leg2.md`）、red team O-01..O-14（`025-review-r5-redteam.md`）。計 56 件。処分は v6（同ファイルを in place で改訂）と handout（`.agents/worklog/orchestrator-glue/pilot/`）の必要分に反映する。書くのは本ファイル、v6、handout のうち所見が要るものだけ。
- 処分の語: `fixed-in-v6` = v6 の該当節（または handout）に反映、`accepted-residual` = owner と測るコマンドを名指しして残す、`rejected` = 一次資料か決定行で退ける、`operator-decision` = v6 が既定と代替を §9 の決定に置き、操作者の決定行で閉じる。
- 手順の指し方は番号と名前（第 1 脚 #n、第 2 脚 #n）。直し方は散文で書き、資格情報を扱うコマンド行と settings の JSON は本ファイルに貼らない（handout 本体にある）。
- 集計と取った決定は末尾「集計」節。

| id | P | disposition | where in v6 (section) or the reason |
| --- | --- | --- | --- |
| M-01 | P1 | fixed-in-v6 | §1.3 audit 行の denyWrite に `<results dir>/cwd` を 1 項; handout `srt-audit.json` の denyWrite に pilot の results cwd を 1 項。第 2 脚 #7 がその下で `listening` に達するかを同時に測る |
| M-02 | P1 | fixed-in-v6 | handout `leg2.md` #3b throwaway・#2b・#9 の先頭で `$PILOT` へ移動し終わりで戻す; §4 第 2 脚 #3b/#2b/#9 の「測るもの」に cwd を明記 |
| M-03 | P1 | fixed-in-v6 | 選択 (a): pilot の shim も `GIT_CONFIG_NOSYSTEM=1` を持つ。§1.2（本番形と同じ）、§4 第 2 脚 #4 と #5 (10)（席内の helper は user の 1 段、操作者端末の #0b が 2 段 = 穴の実測）、handout `leg2.md` の shim 雛形と #5 の期待 |
| M-04 | P2 | fixed-in-v6 | §1.3 audit 行の network 欄「binding は #7 の判定（L-15）」 |
| M-05 | P2 | fixed-in-v6 | §1.3 audit 行の network 欄: `audit.json` 1 本に両 provider のホストを並べ、audit/security は openai 側、review は anthropic 側だけを使う; openai 側は第 2 脚 #7、anthropic 側は #3b で確定。§3 W5a の完了条件に同じ 1 句 |
| M-06 | P2 | fixed-in-v6 | 前書きの用語行に C-80、J10、S-M の gloss |
| M-07 | P3 | fixed-in-v6 | §1.2: audit/review/security の `<name>` = `<role>-<task id>-<head40>`（`<results dir>` と同じ鍵） |
| M-08 | P3 | fixed-in-v6 | handout 3 本の見出し・末尾を v6 に; §4 前書き「v6 で更新」; §4 第 1 脚 #6 を「handout 5 本」に |
| M-09 | P3 | fixed-in-v6 | handout `leg2.md` の shim 雛形: `PILOT_LOG` を役割の tmp（worker `seat/tmp`、audit `out/tmp`）の `events.log` に |
| M-10 | P3 | fixed-in-v6 | §1.3 worker/orchestrator 行の denyWrite 欄から `~/.local/share/uv/tools` を削除（allow の外、G-13 のとおり） |
| M-11 | P3 | fixed-in-v6 | handout `leg2.md` #4a: 席名を `instances` から取り `hcom list <name> --json` の `session_id` を出す; §4 第 2 脚 #4a に同じ 1 句 |
| M-12 | P3 | fixed-in-v6 | §1.10 末尾と §9「読取の残余」行: 席の gh config dir は allow-list 外で読取専用、X 手順 2 (f1) で `gh auth status` と push と debug log の `gh` 行を貼る、書込が要るならその dir だけ allowWrite（token file は denyRead のまま）。O-13 と同じ処置 |
| N1-01 | P1 | fixed-in-v6 | handout `leg1.md` #6: 複製側 `events.ts` の fallback 文字列を `$PILOT` の絶対パスに `sed`; #15: 空なら既定の fallback path も見る; §4 前書きの `events.ts` 仕様に 1 句（起動側 env の伝播は未確認） |
| N1-02 | P1 | fixed-in-v6 | handout `leg1.md` #6b: #4b で出た `omp auth --help` を読んで import の形を確かめてから進む、import/login の exit を記録、import が落ちたら openai-codex の login に倒す; §1.9 と §4 #6b に import file の形は未確認と明記 |
| N1-03 | P2 | fixed-in-v6 | handout `events.ts` `taskOf`: 後ろから走査して `task_id=` を含む最初の user message を採る（無いときだけ `none`）; §4 前書きの仕様 |
| N1-04 | P2 | fixed-in-v6 | handout `leg1.md` #7 と §4 #7: `cap` も `agent_end` も無く max-time で切れたら `--max-time 600` で 1 回だけ再実行; `session_stop block n=1` が 1 行でもあれば発火の事実は取れている |
| N1-05 | P2 | fixed-in-v6 | handout `leg1.md` #7 と §4 #7: どのモデルで走ったかは `turn_start` 行の `contextWindow` を #4 の `models find` と突き合わせて決める |
| N1-06 | P2 | fixed-in-v6 | handout `leg1.md` #12/#13/#14 と `leg2.md` #4b/#5: 固定 sleep を「RESULT が出るまで 30 秒おきに最大 5 回の select」に; §4 の該当行 |
| N1-07 | P2 | fixed-in-v6 | handout `leg1.md` #17: transcript を file に落とし、その command の exit で `transcript_path` の file に代替、最後に `tail`; §4 #17 |
| N1-08 | P2 | fixed-in-v6 | handout `leg1.md` #18 と §4 #18: hcom 自身の成果物 5 つを名指しして「消さない」、`herdr pane list` で pane の残骸を 1 回見る |
| N1-09 | P2 | fixed-in-v6 | handout `leg1.md` #6b: import と login の exit を記録（N1-02 と同じ行） |
| N1-10 | P3 | fixed-in-v6 | handout `leg1.md` #5 のコメントを「席で hcom が拒むのは `-p`/`--print`/`--mode`/`--no-extensions`」に、regex に `--no-extensions`; §4 #5 |
| N1-11 | P3 | fixed-in-v6 | handout `leg1.md` #0: ruleset id を名前の `select` で変数に取り、空なら止まる |
| N1-12 | P3 | fixed-in-v6 | handout `leg1.md` の見出し v6、各ブロックのコメント行に期待出力の要点、末尾に plan v6 §4 の表の参照 |
| N1-13 | P3 | fixed-in-v6 | handout `leg1.md` 前書き: 端末を替えたら #0a と #6b の `M=` を打ち直す; §4 前書き |
| N1-14 | P3 | fixed-in-v6 | §4 前書きと handout `leg1.md` 前書きの mask 規則に「GitHub login → `<login>`（repo owner と同じなら残す）」 |
| N1-15 | P3 | fixed-in-v6 | handout `leg1.md` #10: `NAME` の空判定（空なら `NAME-EMPTY` を記録して止まる） |
| N2-01 | P1 | fixed-in-v6 | M-02 と同じ処置（#3b/#2b/#9 の cwd は `$PILOT`） |
| N2-02 | P1 | fixed-in-v6 | M-03 と同じ処置（選択 (a)） |
| N2-03 | P1 | fixed-in-v6 | M-01 と同じ処置 |
| N2-04 | P1 | fixed-in-v6 | handout `leg2.md` #4/#4c/#7/#8: 各起動行の直前に席 shim の実行可否を検査し、無ければ `NO-SHIM` を出して止まる; 前書きに「pane を開き直したら #0 と #4 の shim 定義を再実行」; §4 第 2 脚 #4/#7/#8 |
| N2-05 | P2 | fixed-in-v6 | handout `leg2.md` #4a: runner の選別を `--dir` 文字列に依らず、launch dir の全 script から `--hcom-tool-path` 値を抜いて `sort -u`; §4 #4a |
| N2-06 | P2 | fixed-in-v6 | handout `leg2.md` #4a: `lsof` の対象を `--profile pilot-worker` を command 行に持つ全 process に; §4 #4a |
| N2-07 | P2 | fixed-in-v6 | handout `leg2.md` の shim 雛形: 席 `bin` に `omp` の link を足し、#4b の `modelRoles` probe が通る; §4 #4b |
| N2-08 | P2 | fixed-in-v6 | handout `leg2.md` #7: `pgrep` の pattern を audit 席に絞る（`pilot-audit`）、#10 は全席 kill 後に今の pattern; §4 #7 |
| N2-09 | P2 | fixed-in-v6 | handout `leg2.md` #7: 席名を私設 store の `instances` から `sqlite3 -readonly` で取る（#8 の pid と同じ形）; §4 #7 |
| N2-10 | P2 | fixed-in-v6 | handout `leg2.md` #3b/#7 と §4 #3b/#7: `Connection blocked to <host>` が出たらそのホストを allowedDomains に 1 回だけ足して同じ行で再実行し、値を §9 の provider 行へ |
| N2-11 | P2 | fixed-in-v6 | handout `leg2.md` #0 で `$SRT`/`$OMP` の先頭行（shebang か binary）を出し、shim 雛形で 9 tool + `omp` の解決結果と種別を 1 行ずつ出して空なら止まる; §4 #0/#4 |
| N2-12 | P3 | fixed-in-v6 | handout `leg2.md`: `M=` を #0 の前の独立行に（第 1 脚の値を写す注記付き） |
| N2-13 | P3 | fixed-in-v6 | handout `leg1.md` #6b と `leg2.md` #3b: 鍵の読み取りを echo 無しの `read -rs` に（pane の scrollback に残さない） |
| N2-14 | P3 | fixed-in-v6 | handout `leg2.md`: #3b 再試行の `jq` を tmp → `mv` 形に、#5 (12) の `allowMachLookup` 候補値は `violations.log` の `deny mach-lookup` 行の service 名、#6 に打つ 2 行と期待する echo |
| N2-15 | P3 | fixed-in-v6 | M-08/M-09/M-11 の処置 + handout `leg2.md` の末尾に「期待出力は plan v6 §4 第 2 脚の表、#4b/#5 は RESULT が見えるまで select を再実行」、select の `limit` に依らない loop |
| O-01 | P0 | fixed-in-v6 | §1.6 保護パス一覧に `scripts/lib/**`; §1.9/§2 Makefile 行/§3 W3: installer の計画は Makefile が manifest から並べる静的一覧で、pull した木の `update-agent-assets.sh`（と `scripts/lib` の `source`）を停止前に実行しない; 停止は第 2 の統制、chain 規則が第 1（§9 G-07 行、決定 (6)(7) の代替欄） |
| O-02 | P0 | fixed-in-v6 | §1.6 に 2 規則: `home/**` の basename `modify_*`/`run_*`/`create_*` は置き場所を問わず保護; `home/**/*.tmpl` の追加行に template 関数 `output`/`exec`/`lookPath`/`include`/`joinPath`（外部入力付き）の呼び出しを含む差分は保護。§1.9/W3: 停止の表示自体が template 関数と modify script を実行すると明記; §3 W6a の fixture |
| O-03 | P1 | fixed-in-v6 | §1.6 に `install/**`; §3 W6a の fixture（`install/common/*.sh` に触れる PR が `refuse 10`） |
| O-04 | P1 | fixed-in-v6 | §1.6 の repo root 列を `.claude/settings*.json`・`.claude/hooks/**`（`.py` を含む）・`.claude/contextdb/**`・`.claude/extensions` に広げる（project hook は `<main>` で開いた Claude pane が sandbox 外で実行する; E3 で一覧から外す） |
| O-05 | P1 | fixed-in-v6 | §1.7 (5)/§2 validator 行/§3 W6a: PEM は BEGIN から END までのブロックを 1 regex（`re.S`）で伏せる、fixture の PEM は本体 2 行以上を含む |
| O-06 | P1 | fixed-in-v6 | §1.7 (4): 先に `hcom kill`、transcript は `hcom transcript` ではなく `<results dir>/sessions/**/*.jsonl` から作る; §4 第 2 脚 #7 と handout `leg2.md` #7: kill の前に `transcript_path` が `out/sessions` 配下であることを出し、kill の後に session JSONL を読む |
| O-07 | P2 | fixed-in-v6 | §1.10 (e): 統制は操作者の system helper 行除去、shim の変数は便宜; `make doctor` に system の `credential.helper` が空である検査（§2 A-2 行、W3 の完了条件）; 順序 (d) → (e) → push 1 回 → 受理検査 |
| O-08 | P2 | fixed-in-v6 | §9「読取の残余」行: 自役割 `agent.db` の書込残余の帰結を provider account の差替え（席をまたぐ持出し路、D9 の上限が効かない）と書き、boundary 記録に役割ごとの account 識別子 1 行、不一致なら第 1.3 項の fallback（profile 再生成）; 決定 (8) 代替 B がこれも閉じると明記 |
| O-09 | P2 | fixed-in-v6 | §7 保護パス PR 行と §1.9: `Makefile`・`scripts/lib`・`update-agent-assets.sh`・`.chezmoiscripts`・`install`・template 関数行・`modify_*` に触れる PR は操作者が差分本文を読んでから merge（`make update` の停止は pull 後の Makefile で外せる） |
| O-10 | P3 | fixed-in-v6 | §4 第 2 脚 #5 と handout `leg2.md` #5: canary に 15（allow 内から deny 先への symlink 経由の書込）と 16（`agent/sessions` の改名）を足し、どちらも拒否を期待 |
| O-11 | P3 | fixed-in-v6 | §1.7 (4)(5): `hcom kill` の前に `herdr pane list` の label が `<name>` と一致することを確かめる; §9 共有 store 行に pane/pid 偽造による DoS を残余として 1 句 |
| O-12 | P3 | fixed-in-v6 | §1.7 (5)/§2 validator 行: hex 形 2 つ（既知 prefix の hex と 40 桁以上の hex 列の復号）を足す; 残りの符号化は §9 の既存の残余のまま |
| O-13 | P3 | fixed-in-v6 | M-12 と同じ処置（§1.10 末尾、§3 X 手順 2 (f1)、§9） |
| O-14 | P3 | fixed-in-v6 | §3 W5b の Behaviour 行「`hcom-seat` は DB の `instances` 行から argv も path も取らない（同名の残骸は `hcom kill <name>` → 再試行）」 |

## 集計

- 56 件: fixed-in-v6 56、accepted-residual 0、rejected 0、operator-decision 0。優先度別 fixed/residual/rejected/operator-decision: P0 2/0/0/0（O-01、O-02）、P1 13/0/0/0（M-01〜03、N1-01/02、N2-01〜04、O-03〜06）、P2 20/0/0/0（M-04〜06、N1-03〜09、N2-05〜11、O-07〜09）、P3 21/0/0/0（M-07〜12、N1-10〜15、N2-12〜15、O-10〜14）。
- 重複の束: M-01 = N2-03、M-02 = N2-01、M-03 = N2-02、M-12 = O-13、M-08/M-09/M-11 ⊂ N2-15、N1-02 ⊃ N1-09。
- 取った決定（代替は v6 §9 決定 (6)(7)(8) の代替欄）: (1) 保護パス規則を `scripts/lib/**`、`install/**`、repo の `.claude/settings*.json`・`.claude/hooks/**`・`.claude/contextdb/**`、`home/` 配下の `modify_*`/`run_*`/`create_*`、`home/**/*.tmpl` の template 関数追加行まで広げ、`make update` の停止は第 2 の統制（表示自体が template と modify script を実行する）、installer 一覧は静的、`Makefile` を含む保護パス PR は操作者が差分本文を読んでから merge（O-01/02/03/04/09）; (2) audit の results cwd を denyWrite、throwaway と srt 呼び出しの cwd は `$PILOT`、pilot shim は `GIT_CONFIG_NOSYSTEM=1` を持ち席内の helper は 1 段（M-01/02/03）; (3) 第 1 脚: `events.ts` の fallback を複製時に `$PILOT` へ、import の形は `omp auth --help` を読むまで未確認で exit を記録し login に倒せる、計数 key・長い `--max-time` の再実行・`contextWindow` によるモデル判定・select の loop・transcript の exit 判定・hcom の成果物の名指し（N1）; (4) 第 2 脚: shim 無しでは起動しないガード、runner と `lsof` と席名の取り方、`omp` link、`pgrep` の絞り込み、ホスト拒否時の再試行、tool 解決の検査（N2）; (5) masker は PEM ブロックと hex、`omp-run.sh` は kill → session JSONL、helper 行除去が統制で doctor が検査、`agent.db` 残余は account 差替えと書く（O-05/06/07/08）; (6) P3 群は各 1 句〜1 行。
- 本ファイル以外に書いたもの: v6、handout `leg1.md`、`leg2.md`、`events.ts`、`srt-audit.json`。`policy.yml`、`srt-worker.json`、`srt-orchestrator.json` は所見が無く不変。
