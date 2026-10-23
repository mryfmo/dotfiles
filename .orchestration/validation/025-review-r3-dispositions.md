# Plan 025 review round 3: dispositions (v4)

- 対象: `.orchestration/plans/025-regime-cutover-plan.md` v3（sha256 prefix `4ebb70d7`、294 行）への round 3 の 3 審査（red team G-01..G-20、operator dry run H-01..H-34、consistency/sources I-01..I-22、計 76 件）と、consistency 審査が「部分」と判定した round 2 の 4 行（F-12、E-07、E-08、V-18）。処分は v4（同ファイルを in place で改訂）と、v4 §4 から再生成した handout 7 本（`.agents/worklog/orchestrator-glue/pilot/{leg1.md,leg2.md,events.ts,policy.yml,srt-worker.json,srt-audit.json,srt-orchestrator.json}`）に反映済み。書いたのは本ファイル、v4、handout 7 本だけ。
- 処分の語: `fixed-in-v4` = v4 の該当節（または handout）に反映、`accepted-residual` = owner の作業項目と測るコマンドを名指しして残す、`rejected` = 引用した一次資料か決定行で退ける、`operator-decision` = v4 が既定と代替を §9 の決定に置き、操作者の決定行で閉じる。
- 集計（round 3 の 76 件）: fixed 74、residual 1（G-19）、rejected 0、operator-decision 1（G-01）。優先度別 fixed/residual/rejected/operator-decision: P0 3/0/0/1、P1 27/0/0/0、P2 22/0/0/0、P3 22/1/0/0。round 2 の部分 4 行: fixed 4（P1 3、P3 1）。
- 設計級の決定（v4 で取った 9 点、代替は v4 §9）: (1) GitHub identity の分離を X の前提 W0 にし、既定 = orchestrator の token を file store へ・席は別 identity の fine-grained token・ruleset に approval 1（G-01、決定 (5)）; (2) 全 profile の `agent/{hooks,extensions,config.yml,.env,secrets.yml,skills,prompts}` を denyWrite、`security` profile を分離、起動前の空検査（G-02/G-03）; (3) audit/review/security 席は私設 `HCOM_DIR`（G-04）; (4) `hcom-seat` の植え付け拒否、`skills.enableAgentsProject: false`、`chain-integrate.sh` の main 側保護パス検査、`make update` の差分停止、masker の `gh[opsur]_`、`omp-run.sh` の nonce 付き verdict file（G-05..G-08/G-12/G-14）; (5) handout を v4 から再生成（schema 完全な srt 設定、clone 先行、資格情報を #7 の前、probe 語、`hcom list <name> status`、`/usr/bin/log`、`tag:` kill、両脚の片付け、0600 ファイル経由の鍵、J-N2 の字面、`--from`）（H-01..H-34）; (6) `kill -0` を捨て sqlite + `hcom list` + pane で残骸を見る、`launch_ts` は `+%FT%T`（I-09/I-17）; (7) X-0 の `<main>` 側 private hcom 導入行と実パス（I-08）; (8) update-branch 無し、`git revert <sha>`（I-07/I-19）; (9) 5 役割の起動器署名、placeholder 5 つ、log は allowWrite の中（I-02/I-03/I-04/I-16）。

| id | P | disposition | where in v4 (section) or the reason |
| --- | --- | --- | --- |
| G-01 | P0 | operator-decision | §1.10（W0: token の file store 化、席の別 identity、ruleset の approval 1 + `require_last_push_approval`、残余、測るもの）、§3 W0 と X 手順 2 (f)、§4 第 1 脚 #0/#0b と第 2 脚 #5 (10)、§7 W0 行、§9 決定 (5)（既定 = W0 の形; 代替 B = P0 残余の受容決定行、C = fork 流）、§11 #18 |
| G-02 | P0 | fixed-in-v4 | §1.1 表（security は profile `security`）、§1.3 表（全役割の `denyWrite` に profile の 7 パス）、§1.2（起動前の空検査で exit 2）、§4 第 2 脚 #3b/#7（この deny の下で応答と `listening`; 第 1 の問い）、§8（否定時の fallback = 起動ごとの profile 再生成）、handout `srt-worker.json`/`srt-audit.json` |
| G-03 | P1 | fixed-in-v4 | G-02 と同じ行（worker profile も同じ 7 パス）; §9「profile の植え付け」行に席ごとの profile の代替 |
| G-04 | P1 | fixed-in-v4 | §1.7 (0)（`HCOM_DIR=<main>/.hcom-audit/<task id>-<head40>`、launch/events/transcript/kill が同じ値）、§1.3 audit 行（allowWrite は私設 store、`~/.hcom` は denyRead）、§2 `.gitignore` 行、§4 第 2 脚 #7/#8/#10、§6 SKILL の「bus 本文は data」、handout `srt-audit.json`/`leg2.md` |
| G-05 | P1 | fixed-in-v4 | §1.2（`hcom-seat` の拒否一覧: `.omp/`、`.env`、`.env.*`、`.claude/hooks/**/*.{ts,js}`、`.claude/extensions`、`.agents/skills`、`.agent/skills`）、§1.4/§5（overlay の `skills.enableAgentsProject: false`、B-2 amendment）、§1.6/§3 W6a（`chain-integrate.sh` の main 側検査）、§2 D 行の一覧、handout `policy.yml` |
| G-06 | P1 | fixed-in-v4 | §1.6 と §3 W6a（`chain-integrate.sh`: `git diff --name-only <base40>...<head40>` が保護パスに触れたら `refuse 10`、操作者が merge）、§9「GitHub 境界」行、§11 #19 |
| G-07 | P1 | fixed-in-v4 | §1.9/§3 W3/§7（`make update` は `home/dot_agents/{srt,omp}` と manifest の `chezmoi diff` を表示し、非空なら `CONFIRM=1` 無しで停止; §7 の各 `make update` 行に期待字面）、§9 信頼側の行、§11 #20 |
| G-08 | P1 | fixed-in-v4 | §1.7（masker に `gh[opsur]_[A-Za-z0-9]{20,}` と `sk-ant-`、X-2 の allowed_files）、§1.10（根治 = token の file store 化） |
| G-09 | P2 | fixed-in-v4 | §1.3 表（`allowLocalBinding` は第 2 脚 #4c の判定で決める）、§4 第 2 脚 #3（`lsof -nP -iTCP -sTCP:LISTEN`）/#4c、§9 行 |
| G-10 | P2 | fixed-in-v4 | §1.3 表の役割別 `denyRead`（自役割を含まない）、§4 第 2 脚 #5 (9)/#7（他 profile の読取 canary）、handout `srt-*.json` |
| G-11 | P2 | fixed-in-v4 | §4 第 2 脚 #4a（`find ~/.omp/run -maxdepth 3`、`lsof -p`）、§9「`~/.omp/run`」行 |
| G-12 | P2 | fixed-in-v4 | G-05 の行 + §3 W6a（植え付け fixture に `<cwd>/.agents/skills/gh-first-workflow/SKILL.md`） |
| G-13 | P2 | fixed-in-v4 | §1.3 表（allowWrite から `~/.local/share/uv`、`~/.local/state/mise`、`~/Library/Caches/mise` を外し `~/.cache/uv` だけ）、§3 W5b Behaviour 行（`<seat dir>/bin/*` の realpath はどの allowWrite にも無い）、§4 第 2 脚 #5 (11) |
| G-14 | P2 | fixed-in-v4 | §1.7 (3)/(6)（終了判定は nonce 付き `Verdict:` 行だけ、usage は `sessions/**/*.jsonl` だけ）、§9「hcom store」行（消費側の列挙） |
| G-15 | P3 | fixed-in-v4 | §9 S-13 行（J-N2 期間の local review/audit は PR の `AGENTS.md` を読む） |
| G-16 | P3 | fixed-in-v4 | §1.2（log は役割の allowWrite の中）、§9「`srt-debug.log`」行（席が追記できる記録、証跡にしない） |
| G-17 | P3 | fixed-in-v4 | §1.3 worker 行の `denyRead`（`<seats root>` + `allowRead: <clone>`、`<main>/.agents/worklog/omp-run`、`<main>/.hcom-audit`）、handout `srt-worker.json` |
| G-18 | P3 | fixed-in-v4 | §1.2 shim（HCOM_* 7 名を名前で列挙、空は渡さない）、handout `leg2.md` #4 |
| G-19 | P3 | accepted-residual | owner: X 手順 6 の 24 時間観測。§9 行「自席 pty への端末エスケープ」; 測るコマンドは無い（herdr のエスケープ処理は資料に無い）。操作者が pane の異常表示を見たら記録 |
| G-20 | P3 | fixed-in-v4 | G-14 と同じ（poll は verdict file だけ; `hcom kill` の DB 記録に頼らない） |
| H-01 | P0 | fixed-in-v4 | handout `srt-worker.json`/`srt-audit.json`/`srt-orchestrator.json`（skeleton の 5 配列 + `allowPty`、`~` 形）、§4 第 2 脚 #2（ファイルをそのまま使う、値を直すのは #4c だけ） |
| H-02 | P0 | fixed-in-v4 | §4 第 2 脚 #3c（clone を #4 の前に独立行、`/bin/ls -d $PILOT/clone/.git`）、handout `leg2.md` |
| H-03 | P1 | fixed-in-v4 | §4 第 1 脚 #6b（資格情報を #7 の前）、#7/#9 に `--model "$M:xhigh"`、§7「今（W1）」 |
| H-04 | P1 | fixed-in-v4 | §4 第 1 脚 #7（不一致なら `--model "$M" --thinking xhigh` で 1 回、どちらが通ったかを記録 = B-3 の `:<level>` の根拠） |
| H-05 | P1 | fixed-in-v4 | §4 第 1 脚 #10（`hcom list <name> status` を先に読み、`listening` でないときだけ `--wait`） |
| H-06 | P1 | fixed-in-v4 | handout `events.ts`（`--pilot-hook-probe` を含むときだけ block）、§4 第 1 脚 #7（probe 語あり）/#14（無し、拒否文は policy 層） |
| H-07 | P1 | fixed-in-v4 | handout `events.ts`（task id = 直近 user message の `task_id=`、`PILOT_STOP_N` 既定 1、N+1 回目に allow、N=3 のとき `cap`）、§4 第 1 脚 #6/#7（`PILOT_STOP_N=3 --max-time 180`）/#9（既定 1）/#15 |
| H-08 | P1 | fixed-in-v4 | §4 第 1 脚 #0（2 段: 一覧 → id で `.rules[]`） |
| H-09 | P1 | fixed-in-v4 | §4 第 2 脚 #3（`/usr/bin/log stream …`）、handout `leg2.md` |
| H-10 | P1 | fixed-in-v4 | §4 第 2 脚 #3b（M が openai-codex なら `pilot-worker` にも `login openai-codex`） |
| H-11 | P1 | fixed-in-v4 | §1.9、§4 第 2 脚 #3b、§7（`OMP_PROFILE=<p> omp login openai-codex` / `OMP_PROFILE=<p> omp auth import <file>`; `--profile` 前置も pre-parser で効く【I 確認 4】） |
| H-12 | P1 | fixed-in-v4 | §4 第 2 脚 #5（3 = `mkdir <clone>/.omp`、7 = `/bin/ls ~/.ssh`） |
| H-13 | P1 | fixed-in-v4 | §4 第 2 脚 #5 (12)（`b=pilot/srt-$(date +%s)` の 1 行鎖、`gh pr close --delete-branch "$b"`） |
| H-14 | P1 | fixed-in-v4 | §4 第 2 脚 #7（`--skills='planted*'`; `--no-skills` は #8 の pilot3 と本番） |
| H-15 | P1 | fixed-in-v4 | §4 第 2 脚 #8（`@pilot2-`、signal probe は生きている pilot2 席の pid に errno で） |
| H-16 | P1 | fixed-in-v4 | §7「今」(J-N2) の jq 1 行（repo 相対パス 3 本の字面）と確認の `jq '.sandbox.excludedCommands'`; 効き目の測り方 = codex の初期化（D-024-86 の失敗が消える） |
| H-17 | P1 | fixed-in-v4 | §3 X 手順 2 (a)、§7「X 手順 2」（`hcom send --from operator @<name> -- 'AGMSG-PING v1'`） |
| H-18 | P1 | fixed-in-v4 | §3 X 手順 1、§7「X 手順 1」（D9: console の上限画面の見出しと金額、J10: `caffeinate -dimsu` + `pmset -g assertions`） |
| H-19 | P2 | fixed-in-v4 | §4 第 2 脚 #4c（kill → jq → 再起動 → 記録 → 立たなければ戻して再起動、3 起動を所要に） |
| H-20 | P2 | fixed-in-v4 | §4 第 2 脚 #10（`gh pr list --search 'head:pilot/srt'`、`git ls-remote --heads origin 'pilot/srt-*'`、close/delete） |
| H-21 | P2 | fixed-in-v4 | §1.9、§4 第 1 脚 #6b/第 2 脚 #3b（0600 ファイルに貼って `auth import <file>` → `rm`）、§7 |
| H-22 | P2 | fixed-in-v4 | §4 第 1 脚 #9（失敗時 `hcom kill tag:pilot`）/#16（`hcom kill tag:pilot`） |
| H-23 | P2 | fixed-in-v4 | §4 第 1 脚 #18（`$PILOT` は残す、残すものの名）、第 2 脚 前書き（無ければ第 1 脚 #6 を再実行） |
| H-24 | P2 | fixed-in-v4 | §4 前書き（各ブロックを `tee -a $PILOT/leg{1,2}.out`、操作者は exit と判断だけ、mask は orchestrator）、handout 両脚 |
| H-25 | P2 | fixed-in-v4 | §4 第 2 脚 #5 の注（keychain 系の文言なら最初に動かす鍵は `allowMachLookup`）、§8 |
| H-26 | P3 | fixed-in-v4 | §4 第 2 脚 #10（`hcom kill tag:` を 1 つずつ） |
| H-27 | P3 | fixed-in-v4 | §4 第 1 脚 #10（`transcript_path` を取る）/#17（代替 `tail -n 40 "$(cat …)"`） |
| H-28 | P3 | fixed-in-v4 | handout `leg2.md` #4（unescape、`COLORTERM`、HCOM_* は名前で）、§1.2 |
| H-29 | P3 | fixed-in-v4 | §4 前書きと handout 前書き（herdr の pane、他端末なら `HERDR_SOCKET_PATH`） |
| H-30 | P3 | fixed-in-v4 | §7 見出し（orchestrator が「#<pr> merge 後: …」と 1 手ずつ名指す; 再起動の要否も orchestrator が言う） |
| H-31 | P3 | fixed-in-v4 | §11 の全行に「既定: …」 |
| H-32 | P3 | fixed-in-v4 | §4 第 1 脚 #4b（`.schema` を無条件に） |
| H-33 | P3 | fixed-in-v4 | §1.7（throwaway = 第 1 脚 #7、第 2 脚 #3b） |
| H-34 | P3 | fixed-in-v4 | §4 第 1 脚 #3（期待「一覧に `herdr` が出る」）、第 2 脚 #5 (13)（命令文の形） |
| I-01 | P1 | fixed-in-v4 | §1.3 表（audit/review/security の `denyRead` は他の 4 profile、自役割は含まない; template は `__PROFILE__`）、§3 W5a の render テスト行 |
| I-02 | P2 | fixed-in-v4 | §1.2（`hcom-seat <orchestrator\|worker\|audit\|review\|security>`、`srt.roles` 5 行、`omp-run.sh --role <r>` → `hcom-seat <r>`）、§3 W5b の argv テスト 3 役割分 |
| I-03 | P2 | fixed-in-v4 | §1.2 (a)（placeholder 5 つ `__SEAT_DIR__`/`__RESULTS_DIR__`/`__TMPDIR__`/`__DIR__`/`__PROFILE__`）、§1.4（chezmoi は `.tmpl` でなければそのまま配る【I 確認 10】）、§3 W5a |
| I-04 | P2 | fixed-in-v4 | §1.2（log = worker `<seat dir>/tmp/srt-debug.log`、audit `<results dir>/srt-debug.log`、orchestrator `<main>/.agents/worklog/tmp/srt-debug.log`）、§1.7 の中身一覧に `tmp/` |
| I-05 | P2 | fixed-in-v4 | §1.2（orchestrator は `<main>` 配下なので `<seat dir>` を書ける）、§9 信頼側の行（自席の settings/shim は次回起動まで効かない） |
| I-06 | P1 | fixed-in-v4 | §1.5（code は互いに素、manifest だけ両方にあり J-M で並走、【実測】は 2 本文の allowed_files 行） |
| I-07 | P1 | fixed-in-v4 | §3 W2b、§9「C-1 の PR」行（update-branch 無し、audit 済 head を `--match-head-commit` で merge; conflict のときだけ update-branch → sweep と audit のやり直し） |
| I-08 | P1 | fixed-in-v4 | §1.5/§3 X 手順 0/§7（`<main>` で `scripts/update-agent-assets.sh update_hcom_private` を X-0 の前に、期待 `/bin/ls <main>/.agents/worklog/uv-tools/hcom/bin/hcom`; `<canonical>` の `make update` が入れるのは public hcom だけ） |
| I-09 | P1 | fixed-in-v4 | §1.2（pid の意味）、§1.7 (5)（`kill -0` 無し: `instances.status`、`hcom list`、`herdr pane list` の 3 つ + process 残骸は操作者側 `make doctor` の行）、§4 第 2 脚 #7（操作者端末の errno）/#8（srt 下の errno は EPERM の記録） |
| I-10 | P2 | fixed-in-v4 | §4 第 2 脚 #8（srt 下から `hcom omp --tag pilot3` と `hcom kill tag:pilot3` を 1 往復）、§8（通らなければ X 手順 4/5 を §9 代替 (b)） |
| I-11 | P2 | fixed-in-v4 | §1.1（fetch + switch は clone 作成時と clean かつ detached のときだけ） |
| I-12 | P2 | fixed-in-v4 | §2 D 行（拒否一覧に `.claude/hooks/**/*.{ts,js}`、`.claude/extensions`、`.agent/skills`）、§1.3 orchestrator 行の `denyWrite`（`<main>/.omp`、`.claude/hooks`、`.claude/extensions`、`.agents/skills`、`.agent`、`.env`） |
| I-13 | P3 | fixed-in-v4 | §3 前文（a012 の根拠 = omp/srt 描画部と `srt:`/`omp.skills` 節は両境界の source ではない; Claude 描画部に触れるなら操作者） |
| I-14 | P3 | fixed-in-v4 | §3 前文の鎖 `P2 ← (A-2 ‖ P1)` |
| I-15 | P3 | fixed-in-v4 | 前書きの用語行（E1/E2/E3、`hcom-seat` の配備先、`<seat dir>`/`<results dir>` の定義先） |
| I-16 | P2 | fixed-in-v4 | §1.2（log を allowWrite の中に、継承 fd への write は【未検証】）、§4 第 2 脚 #4a（omp の stderr 行の行き先と violations.log の拒否行） |
| I-17 | P3 | fixed-in-v4 | §1.7 (2)（`launch_ts=$(date -u +%FT%T)`、`--wait` は 10 秒の lookback + 以後の新イベント）、§4 第 2 脚 #7、§9 |
| I-18 | P2 | fixed-in-v4 | §2 A-2 行の手順 (4)（global 木の name@version を使い捨て側 `.package-lock.json` と比較、差があれば refuse） |
| I-19 | P3 | fixed-in-v4 | §1.5、§3 X 0/2(c)、§8、§9、§11 #16（squash commit の `git revert <sha>`、`-m` 無し） |
| I-20 | P3 | fixed-in-v4 | §3 X 手順 2 (a)（操作者端末で `bus-history.sh <team>`） |
| I-21 | P3 | fixed-in-v4 | §3 W3（`npm view` は orchestrator が `allowed_domains` 宣言付きで取るか操作者が貼る） |
| I-22 | P3 | fixed-in-v4 | §1.7 (6)（`find <results dir>/sessions -name '*.jsonl'`） |
| F-12 | P1 | fixed-in-v4 | I-09 の行（`kill -0` を捨てた 3 検査 + doctor） |
| E-07 | P1 | fixed-in-v4 | I-02 の行（5 役割の起動器署名、`omp-run.sh --role review\|security`） |
| E-08 | P1 | fixed-in-v4 | I-03/I-05 の行（placeholder 5 つ、`<seat dir>` の文の限定） |
| V-18 | P3 | fixed-in-v4 | I-17 の行（lookback の句） |
