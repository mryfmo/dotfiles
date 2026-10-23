# Plan 025 review round 5, perspective N2: 第 2 脚 handout と srt settings の操作者ドライラン

- 対象: `.agents/worklog/orchestrator-glue/pilot/leg2.md`（75 行）、`srt-worker.json`、`srt-audit.json`、`srt-orchestrator.json`。文脈: plan v5（`shasum` prefix `9ce32b71` は round-5 M の実測値を引用、本文脈では `wc -l` 326 行のみ再計測）§1 役割表・§1.3 allow-list・§4 第 2 脚・§7、round-3 H-01/02/09/12/15/16/19/20/24/25、round-4 L-01/02/15/19、round-5 M-01..M-03。
- 読み取り専用（Read/`cat`/`sed -n`/`grep`/`wc`/`jq`/`python3 -c` だけ。`omp`/`hcom`/`herdr`/`gh`/`git`/`log`/`security`/`npm`/`srt` と `--help` は実行していない。席・store・pane には触れていない）。ツール事実は `srt-facts.md`、`b2-c2-facts.md`、r2〜r5 のレビューからだけ取り、それ以外は 未確認 と書く。
- 人格: 第 1 脚を終え A-2 で srt を入れた操作者が、herdr の pane・repo root で handout を上から貼る。記法: `~` = ホーム、`<main>` = repo root の実パス、`$PILOT` = `~/pilot-20261022`。

## 1. leg2.md の逐行ウォーク

| # | 手順 | 判定 | 根拠と備考 |
| --- | --- | --- | --- |
| 前書き | 前提（第 1 脚の `$PILOT` 5 本、`M` の値、`tee -a` 記録、JSON は repo のもの、`@pilot2-` の tag 送り、`/usr/bin/log`） | 通過 | H-09（builtin `log` 回避）、H-15（tag fan-out 形）、H-24（tee で記録、貼るのは exit と判断）が本文にある。`M` は「第 1 脚 #6b の値」と定義 |
| #0 | 前書き: repo root へ移動、`PILOT`/`PILOT_LOG` の export、`OWNER_REPO`/`MAIN`/`SRT`/`OMP`/`M` の定義、`srt-worker.json`/`srt-audit.json` の `__MAIN__` を `sed` で実パスに、5 本の存在表示 | 通過（P3 1 件、P2 1 件） | placeholder `__MAIN__` は 2 本ともここ 1 回で埋まり、`srt-orchestrator.json` は #8 で別ファイルへ埋める（再実行しても無害）。`M` は山括弧の手置換で、置換し忘れると zsh が行全体を parse できず #0 は何も走らない = fail-closed だが原因が読めない（N2-12）。`SRT`/`OMP` は realpath を取るだけで、それが本物の entrypoint か launcher 用 wrapper かは出さない（N2-11、未確認）。`OWNER_REPO`〜`M` と後述の `mkshim` は export されない shell 変数・関数: 同じ pane で続ける限り全手順で定義済み、pane を開き直すと消える（前書きに再実行指示が無い、N2-04 に含む） |
| #1 | `srt --help` と不在 settings の exit | 通過 | srt-facts Q1: `--settings` の file は存在必須でエラー終了。cwd は `<main>` のまま（下記 #2b と同じ注意、ただし settings 不在なので sandbox 前に終わる） |
| #2 | worker 設定の表示 | 通過 | §2 と一致（JSON 検証は §2 表） |
| #2b | `--` が commander の終端であることの echo 試験 | 通過（cwd 注意） | A-04。worker 設定の下で cwd = `<main>`（denyRead）で bash/`sandbox-exec` が立つかは facts に無い（N2-01 の派生、未確認） |
| #3 | `/usr/bin/log stream` を background にして pid を file へ、`lsof` の LISTEN 棚卸し | 通過 | H-09 済。pid file を #10 が `kill` に使う。`kill %1` は無い |
| #3b 資格情報 | `pilot-audit` は OAuth login、`pilot-worker` は `M` に応じて 0600 file 経由の `auth import` + `rm` か OAuth login | 通過（P3 1 件） | §1.9 どおり profile ごと別。鍵は command 引数にも history にも入らないが、素の `cat` に打つので pane に echo され scrollback に残る（N2-13）。`rm` は import の成否に関わらず走る |
| #3b throwaway | worker 設定の下で `-p` 1 語応答、`Connection blocked to` の集計、profile root の `ls` | **P1**（M-02 未処置） | #0 で `<main>` に移動したまま打つ。`srt-worker.json` の denyRead に `__MAIN__`（= 実パス）があるので omp は読めない cwd で起動し、第 1 の問い（allow-list の下で応答が出るか）が cwd 起因と区別できない。第 1 脚 #7 は `$PILOT` へ移動してから打っている（N2-01）。debug log は操作者 shell の redirect なので allowWrite 外でも書ける。TMPDIR は `CLAUDE_CODE_TMPDIR` 無しなので `/tmp/claude`（常時書込可） |
| #3b 再試行文 | 応答が出ないとき allowWrite を 1 path 足して 1 回だけ再実行 | 通過（P2/P3） | 足す対象は「実行入力でない path だけ」と限定済（L-02）。`jq` の出力先（#4c の tmp → mv 形）が書かれていない（N2-14）。provider ホストが拒否されたときの再試行は無い（N2-10） |
| #3c | clone を作り `commit.gpgsign false`、`.git` の存在表示 | 通過 | H-02 済: #4 の `--dir` と allowWrite の先が起動前にできる |
| #4 shim | `mkshim`: `bin/` に 9 tool の realpath symlink、template を heredoc で書き 6 placeholder（`__SETTINGS__`/`__SRT__`/`__OMP__`/`__SEAT__`/`__TMP__`/`__LOG__`）を `sed` で埋め `chmod +x` | 通過（P1 2 件） | shim の置き場 `$PILOT/seat/omp` は worker allowWrite（`clone`、`seat/tmp`、profile allow-list、`~/.omp/run`、`~/.hcom`、`~/.cache/uv`）の外 = 席は自分の shim を書けない。audit は `seat` 全体を denyRead。HCOM_* 7 名の名前列挙、`env -i`、`CLAUDE_CODE_TMPDIR` = `seat/tmp`（srt の TMPDIR 差し替え先 = allowWrite 内）、`--debug` の stderr を `seat/tmp/srt-debug.log` に追記（I-04/J-01: allowWrite 内、fd は shim の shell が sandbox 前に開く）。**`GIT_CONFIG_NOSYSTEM=1` は無い**（M-03 未処置、N2-02）。9 tool の解決は `command -v` → realpath で、解決できない tool は `for` の終了値に埋もれて dangling link のまま shim が書かれる（N2-11）。`bun`/`node` を入れているのは omp が Bun で走るため（A-14）に合う |
| #4 起動 | `PATH` 先頭に `seat` を置いて `hcom omp --tag pilot2 --dir <clone> --terminal herdr`、tool 引数に profile・`-e events.ts`・`--config policy.yml`・model | **P1**（fail-open） | srt-facts Q2: hcom は起動側 PATH の `omp` を `--hcom-tool-path` に焼くので shim が刺さる。ただし `mkshim` と起動は `;` で繋がれ、shim が無い/作れないときも本物の omp で席が立つ（yolo・sandbox 無しで #5 の push/PR TASK を受ける）。shim 実在の `&&` ガードが無い（N2-04）。`events.ts` の `PILOT_LOG` 先は allowWrite 外（M-09 既知、P3） |
| #4a | runner の `--hcom-tool-path`、`instances` 3 列、`hcom list`、`ps`、debug log 末尾、`violations.log`、`hcom.log`、`~/.omp/run`、omp pid の `lsof` | 通過（P2 2 件） | runner の選別は launch script 内の `--dir <clone>` 文字列を前提にするが、srt-facts Q2 の runner template は `cd <dir>` と tool 引数しか持たない。一致 0 本なら `--hcom-tool-path` 行が空で S-08 (1) の判定ができない（N2-05、runner 原文は未確認）。`lsof -p` の対象は `dist/cli.js` の先頭 pid = srt の node（proxy 側）か別 npm CLI で、omp の pid ではない（N2-06）。I-16（継承 fd への write 拒否）はここで測る設計どおり |
| #4b | TASK 1 本: env 名、TMPDIR、`id -un`、`ps`、`omp … config get modelRoles` | 通過（P2 1 件） | 席の PATH は `seat/bin:/usr/bin:/bin` で `bin` に `omp` は無い → 最後の項目は command not found になり F-32 が測れない（N2-07）。`@pilot2-`・`--json`・`--` の順は第 1 脚 #11 と同形 |
| #4c | `hcom kill tag:pilot2` → binding を `false` に jq（tmp → mv）→ 同じ行で再起動 → `hcom list`・`notify_server` 行; 立たないときだけ `true` に戻して 3 起動目 | 通過 | H-19 済: 殺す→編集→再起動→判定→戻す、の順がある。`kill tag:` 形（F-08） |
| #5 | canary TASK 14 項目（`~/…` と `<main>` 実パス）、各 exit を報告させる、180 秒後に `events_v` と `Connection blocked to` | 通過（P3） | 期待出力は plan §4 #5 表に揃う: 1/3/4/7/8/9/11/14 拒否、2 成功、5 拒否、6 repo 名、10 keychain 2 種別 exit 0 + helper 2 段、12 push → PR → close、13 fallback 文言。H-12 済（`mkdir .omp`、`ls ~/.ssh`）。10 の「helper 2 段」は shim に `GIT_CONFIG_NOSYSTEM=1` が無いときだけ成り立つ = handout 内は整合、plan §1.2 と矛盾（N2-02）。`gh auth status` は token を伏せて出す、`security` の stdout は捨てる = 秘密は leg2.out に出ない。12 の push は keychain の token（securityd は基本 profile で許可）に依存。RESULT が直近 2 行に無いこともある（再 select で足りる） |
| #5 再試行文 | push が Username/keychain 系で落ちたら最初に動かす鍵は `allowMachLookup` | 通過（P3） | H-25 済だが候補値が無い（N2-14） |
| #6 | pane で 2 行打つ、通らなければ `--headless` で #4 を再実行し `transcript` | 通過（P3） | 打つ文字列と期待する echo が無い（N2-14） |
| #7 準備 | 2 本目の clone `review` に植え付け 4 種、`out/{cwd,sessions,tmp}`、`hcom-audit`、audit shim（log は `out/tmp`）、nonce、`launch_ts` | 通過（N2-04 と同根） | `mkshim` の再利用: 関数が無い shell なら shim 無しで audit 席が本物の omp で立ち、`--hcom-prompt` の forbidden touch 等を sandbox 無しで実行する（N2-04）。`seat-audit` は audit allowWrite 外、`out/tmp` は allowWrite 内 |
| #7 起動 | 私設 `HCOM_DIR` を付けて `hcom omp --tag pilot-audit --dir out/cwd --terminal herdr --hcom-prompt …`、`--profile pilot-audit --session-dir --skills='planted*' --max-time 300`、openai model | 通過（P1 1 件、P2 1 件） | `--hcom-prompt`・`--session-dir`・`--max-time` は hcom の拒否引数（A-08: `-p`/`--print`/`--mode`/`--no-extensions`/`acp`）に無い。prompt の `$N`/`$MAIN` は操作者 shell で展開、`\$PI_TEST_PLANTED` は席で展開。cwd `out/cwd` は `srt-audit.json` の allowWrite `out` の内側で書ける（M-01 未処置、N2-03）。`srt-audit.json` は binding `false` 先行（L-15 済）。openai 3 ホストは仮置きで、拒否時の再試行文は binding 分しか無い（N2-10） |
| #7 読み取り | store 4 file の taint 検査、`hcom list` 2 系統、`ANAME` 抽出、`events --idle --wait 300 --after`、`ls`、`verdict.md`、`transcript`、`list --json`、`pid`、`kill`、errno probe、`pgrep`、debug log | 通過（P2 2 件） | taint 検査は最初の `hcom list` より前（L-01 の順）。`ANAME` は `hcom list --json` の外形（配列か `agents` 鍵か）を推測しており、外れると空になり以降の 5 コマンドが失敗して席は #10 まで残る（N2-09、外形は未確認）。`--after` は I 確認 2 の `timestamp >=` 比較に乗る。`pgrep` の「残骸無し」は #4c で再起動した pilot2 が生きているので満たせず、audit の孤児と区別できない（N2-08） |
| #8 | `srt-orchestrator.json` を別 file に埋め、生きている pilot2 の pid を `instances` から取り、orchestrator 設定の下で 1 本の `sh -c`: fetch・`gh pr view 406`・`herdr pane list`・`hcom list`/`send @pilot2-`・errno probe・私設 store で `hcom omp --tag pilot3` → `hcom list` → `hcom kill tag:pilot3` | 通過 | `<main>` は orchestrator の allowWrite（fetch の `.git` 書込可、`.git/config` は mandatory deny だが fetch は触れない）。herdr socket は allowUnixSockets、TLS は trustd、token は securityd。`@pilot2-` は H-15 済。pid は `created_at desc` の先頭 = #4c の生きている席（`status` の値は未確認でも新しい順で足りる）。`pilot3` は shim（`seat-audit`）経由で herdr の下に立ち入れ子にならない。errno probe は 3 結果とも exit 0 で `&&` 鎖が切れない。`srt-debug-8.log` は操作者側 redirect |
| #9 | 入れ子 probe | 通過（cwd 注意） | どちらの出力でも設計不変（S-05）。cwd は `<main>`（N2-01 の派生） |
| #10 | 3 tag の `hcom kill`、log stream の `kill`、open PR と remote branch の一覧、canary file の有無、`hcom list`、`pgrep`、終了刻; 残り物の処分文と最後の `rm -rf` | 通過（P3） | H-20 済（GitHub の branch/PR）。`~/.hcom` と `hcom.db` の行は意図して残す（H-23）。`pgrep` は全席を殺した後なので判定可。`$PILOT` 配下（`review` の植え付け、`clone/ok`、`tmp.json`、`srt-orch.json`、debug log）は最後の `rm -rf` で消える。残るのは `~/.omp/run/session-owners` の sidecar、`~/.hcom/integrations/omp/<digest>`、draft PR の CI 実行履歴（消せない）。`hcom kill` が pane を閉じるかは preset の close argv（facts）に依り未実測 |
| 末尾 | 所要 100〜120 分、期待出力は plan §4 表 | 通過（P3） | handout 自身に期待出力が無く plan を並べて読む前提。見出しは「v4 §4」のまま（M-08） |

secrets と識別子: 貼る command に鍵・token は無い。`leg2.out` に入るのは `OWNER_REPO`、`id -un` の user 名、`ps` の command 行、`gh auth status`（token は伏せ字）で、orchestrator が写す時に mask する（H-24）。

## 2. srt settings 3 ファイルの検証

| file | check | result |
| --- | --- | --- |
| 3 本 | `jq -e .` | 有効 |
| 3 本 | top-level 鍵 | `network`、`filesystem`、`allowPty` のみ（schema 外の鍵無し） |
| 3 本 | 必須 5 配列（`network.allowedDomains`/`deniedDomains`、`filesystem.denyRead`/`allowWrite`/`denyWrite`）と入れ子 | 全部 array で正しい階層（H-01 済）。`allowRead`/`allowUnixSockets`/`allowMachLookup` も array |
| 3 本 | boolean | `network.allowLocalBinding`（worker true、audit false、orchestrator true）、`allowPty`（3 本 false）は bool |
| 3 本 | placeholder | `__MAIN__` だけ（worker/audit は denyRead、orchestrator は allowWrite と denyWrite）。`__HCOM_DIR__` 等の本番 7 placeholder は pilot では使わず、HCOM_DIR は shim が環境から前置する設計 |
| 3 本 | `$TMPDIR`、home 実パス、user 名 | いずれも 0 件（`~` 形のみ） |
| worker | §1.3 allow-list（`agent/{sessions,blobs,cache,history.db,agent.db}`、`run`） | 6 項すべて allowWrite にあり、profile root と `agent` 直下は allowWrite に無い（L-02 済） |
| worker | `agent/cache/eval-js` の denyWrite | あり |
| worker | denyRead `<main>`、`~/.hcom/env`、`~/.omp/logs`、他 profile | `__MAIN__`、`~/.hcom/env`（L-19 済）、`~/.hcom/config.toml`、`~/.omp/logs`（L-16 済）、`~/.omp/agent`、`pilot-audit`、`$PILOT/{out,hcom-audit,review}` あり。`allowRead` は空: pilot の `seat` と `clone` は `<main>` の外なので §1.3 の allowRead 例外は不要（整合）。`~/.config/gh` は意図して読める（#5 (10) の穴の実測） |
| worker | network | manifest 7 + provider 仮置き 4、`allowUnixSockets` 空、trustd 1 件 |
| worker | 結論 | **有効**。shim の `seat/omp` と `seat/bin` は allowWrite 外 |
| audit | allow-list と `eval-js` | 6 項あり、`eval-js` denyWrite あり、profile root は allowWrite 外 |
| audit | denyRead | `~/.hcom`、`~/.config/gh`、`__MAIN__`、`pilot-worker`、`$PILOT/{seat,clone}`、基本 8 項あり。`allowRead` 空（`out`/`hcom-audit` は deny 対象外なので不要） |
| audit | 私設 store の実行入力 denyWrite | `hcom-audit/{config.toml,env,config.env,scripts,integrations,.tmp/launch}` 6 項あり（L-01 済） |
| audit | `<results dir>/cwd` の denyWrite | **無し**（M-01 未処置、N2-03）: allowWrite `out` が `out/cwd` を含む |
| audit | network | openai 3 ホストだけ、socket 無し、trustd 無し、binding false 先行（L-15 済） |
| audit | 結論 | schema としては有効。M-01 の 1 項が欠ける |
| orchestrator | allowWrite/denyWrite/denyRead | `__MAIN__`・`$PILOT`・`~/.omp/run`・`~/.hcom`・`~/.cache/uv`; denyWrite に `uv-tools`、`<main>/{.omp,.claude/hooks,.claude/extensions,.agents/skills,.agent,.env}`、`seat`/`seat-audit`/`clone`、`~/.hcom` 4 項; denyRead に `~/.hcom/env`、`~/.omp/logs`、両 pilot profile。profile 行は #8 が omp を立てない 1 コマンド形なので無し（整合） |
| orchestrator | network | 11 ホスト、herdr socket、trustd、binding true |
| orchestrator | 結論 | **有効** |

## 3. round-3/4/5 所見の処置状況

| id | 要点 | leg2.md / JSON での処置 |
| --- | --- | --- |
| H-01 | 必須 5 配列と入れ子 | 処置済（§2 表: 3 本とも array、入れ子正、余分な鍵無し） |
| H-02 | clone を #4 より前に | 処置済（#3c が独立行、`.git` の存在を出力） |
| H-09 | `/usr/bin/log` | 処置済（#3 と前書き） |
| H-12 | `mkdir <clone>/.omp`、`ls ~/.ssh` | 処置済（#5 の 3 と 7） |
| H-15 | `@pilot2-`、生きている pid | 処置済（#4b/#5/#8 の宛先、#8 の `instances` から pid） |
| H-16 | J-N2 の字面 | 第 2 脚の範囲外（plan §7 の行、leg2.md は触れない） |
| H-19 | binding false の手順化 | 処置済（#4c: kill → 編集 → 再起動 → 判定 → 戻す） |
| H-20 | GitHub の残り物 | 処置済（#10 の PR 一覧と `ls-remote`、処分文） |
| H-24 | tee で記録、貼るのは exit と判断 | 処置済（全ブロック `tee -a leg2.out`） |
| H-25 | push 失敗時の最初の鍵 | 処置済（#5 の注記）。候補値は無し（N2-14） |
| L-01 | 私設 store の実行入力 denyWrite と taint 検査 | 処置済（`srt-audit.json` 6 項、#7 の 4 file 検査が `hcom list` より前） |
| L-02 | profile 書込を allow-list に反転 | 処置済（worker/audit とも 6 項、`eval-js` deny、root は allow 外） |
| L-15 | audit の binding を別に測る | 処置済（`srt-audit.json` false 先行、#7 の戻し文） |
| L-19 | worker/orchestrator の denyRead `~/.hcom/env` | 処置済（2 本とも） |
| M-01 | `<results dir>/cwd` の denyWrite | **未処置**（`srt-audit.json` に無し → N2-03） |
| M-02 | #3b の cwd | **未処置**（#3b に移動無し → N2-01） |
| M-03 | shim の `GIT_CONFIG_NOSYSTEM=1` と #5 (10) の期待 | **未処置**（`mkshim` に無し、plan §1.2 の「同じ template の本番形」と矛盾 → N2-02） |
| M-08/M-09/M-11 | 見出し v4、`PILOT_LOG` の allowWrite 外、session id の抽出 | 未処置のまま（P3、round-5 M の行を再掲するだけ: N2-15） |

## 4. 所見

| id | P | step or file | 操作者を止めるもの | 根拠 | 直し |
| --- | --- | --- | --- | --- | --- |
| N2-01 | P1 | leg2 #3b throwaway（派生: #2b、#9） | #0 で `<main>` に移動したまま worker 設定の srt を打つ。worker の denyRead に `<main>` があるので omp は読めない cwd で起動し、第 1 の問い（profile allow-list の下で応答が出るか）の失敗が cwd のせいか allow-list のせいか決められない = 判定不能。#2b/#9 も同じ cwd で、bash/`sandbox-exec` が読取拒否の cwd で立つかは facts に無い | M-02 未処置; `srt-worker.json` denyRead の `__MAIN__`; 第 1 脚 #7 は `$PILOT` へ移動してから打つ | #3b の先頭で `$PILOT` へ移動し終わりで戻す（#2b と #9 も同じ）。plan §4 #3b の「測るもの」に cwd を 1 語 |
| N2-02 | P1 | leg2 #4 `mkshim` の `env -i` 列; #5 (10) の期待 | plan §1.2 は本番 shim に `GIT_CONFIG_NOSYSTEM=1` を置き「第 2 脚 #4 の shim は同じ template の本番形」と言うが handout に無い。#5 (10) の「helper 2 段」はそれが無いときの値なので、操作者はどちらが正しい観測か決められない | M-03 未処置; `grep` で leg2.md に 0 件 | M-03 の (a)（shim に足し、#5 (10) の期待を「席内は user の 1 段、操作者端末 #0b が 2 段」に）か (b)（#4 の注記に「pilot shim は W0 前の穴を測るため `GIT_CONFIG_NOSYSTEM=1`/`GH_CONFIG_DIR` を渡さない」）のどちらか 1 つを本文に |
| N2-03 | P1 | `srt-audit.json` denyWrite; leg2 #7 | plan §1.3 audit 行「`<results dir>/cwd` は読めるが書けない」に対し allowWrite `out` が #7 の `--dir out/cwd` を含み denyWrite に無い。audit 席が自分の cwd-only 実行入力を置ける（経路は細い）。#7 はこの denyWrite の下で `listening` に達するかを測る機会でもある | M-01 未処置; §2 表「`out/cwd` の denyWrite 無し」 | `srt-audit.json` の denyWrite に results cwd を 1 項（§1.3 も同じ 1 項）。書けなくする気が無いなら plan の文を「読める」だけに |
| N2-04 | P1 | leg2 #4 起動、#4c 再起動、#7 起動（+ 前書き） | `mkshim` は対話 shell の関数で、shim 作成と `hcom omp` が `;` で繋がる。pane を開き直した／heredoc の貼付が崩れた／tool が解決できず shim が無い、のどれでも hcom は本物の omp を焼いて **sandbox 無しの yolo 席**が立ち、#5 の push/PR TASK や #7 の forbidden touch をそのまま実行する。#4a の shim 確認は runner の grep（N2-05）に依り当てにならない | srt-facts Q2（PATH の `omp` を焼く）; leg2 #4/#4c/#7 の `;` 連結; 前書きに shell 再開時の指示無し | 各起動行の直前に `<seat dir>/omp` の実行可否を `&&` で検査し、無ければ `NO-SHIM` を出して止める。前書きに「pane を開き直したら #0 と #4 の `mkshim` 定義を再実行」を 1 行 |
| N2-05 | P2 | leg2 #4a runner の選別 | launch script の選別が `--dir <clone>` の文字列一致を前提にするが、srt-facts Q2 の runner template は `cd <dir>` と tool 引数しか持たず `--dir` は hcom 側の flag で転送されない。一致 0 本なら `--hcom-tool-path` 行は空で、S-08 (1) の「shim が焼かれた」が判定不能 | srt-facts Q2 の runner body 引用; 未確認: 実 runner の全文 | `~/.hcom/.tmp/launch` の全 `.sh` から `--hcom-tool-path` 値を抜いて `sort -u`（`<seat>/omp` が 1 行出ればよい）か、`cd <clone>` で選ぶ |
| N2-06 | P2 | leg2 #4a `lsof -p` | 対象 pid を `dist/cli.js` の先頭一致で取る = srt の node（proxy の listener）か `dist/cli.js` を持つ別 npm CLI。G-11（omp の `~/.omp/run/daemons` の種別と LISTEN）は omp の process で見るべき | srt-facts Q1（`srt` の bin は `dist/cli.js`、proxy は host 側で listen） | `--profile pilot-worker` を command 行に持つ process（sandbox-exec の子の bun/omp）を `pgrep -f` で取り、その全 pid に `lsof` |
| N2-07 | P2 | leg2 #4b TASK 最終項目 | 席に `omp … config get modelRoles` を打たせるが、shim の PATH は `<seat>/bin:/usr/bin:/bin` で `bin` に `omp` は無い → command not found。F-32 の値が取れず、操作者は sandbox 起因と読み違える | `mkshim` の 9 tool 一覧に `omp` 無し; shim の `env -i PATH` | TASK 本文に `$OMP` の実パスを `$MAIN` と同じ形で差し込む（か `bin` に `omp` の link を足す） |
| N2-08 | P2 | leg2 #7 読み取りの `pgrep`; plan §4 #7 期待 | 「kill 後に `pgrep` に残骸無し」は、#4c で再起動した pilot2 席が #10 まで生きているので満たせず、audit の孤児と pilot2 の process を区別できない | #4c → #7 → #10 の順; `pgrep` の pattern が `sandbox-exec\|dist/cli.js` | #7 の pattern を `pilot-audit`（sandbox-exec の command 行に profile 名が入る）にし、#10 では全席 kill 後に今の pattern |
| N2-09 | P2 | leg2 #7 `ANAME` 抽出 | `hcom list --json` の外形（配列か `agents` 鍵の dict か）を python で推測。外れると `ANAME` が空になり `events --idle`、`transcript`、`list <name>`、`pid` の select、`kill <name>` が全部失敗し、席は #10 の `kill tag:` まで残る | b2-c2 facts は field 名だけで外形無し（未確認） | `hcom-audit/hcom.db` の `instances` から `tag='pilot-audit'` の最新 `name` を `sqlite3 -readonly` で取る（#8 の `wpid` と同じ形、schema は b2-c2 に実在） |
| N2-10 | P2 | leg2 #3b と #7 の再試行文 | provider ホスト（worker 4、audit 3）は仮置き（srt-facts Q3「Provider hosts: Not stated」）。ホストが拒否されて `listening`／応答が出ないとき、#3b の再試行は allowWrite の path だけ、#7 は binding だけを扱い、`Connection blocked to` の行は block 末尾に出るだけで次の一手が無い。`M` が anthropic のとき openai ホストの初回実測は #7 | srt-facts Q3; leg2 L30/L58 | 両方に 1 行: 「`Connection blocked to <host>` が出たら、そのホストを allowedDomains に 1 回だけ足して同じ行で再実行し、値を記録（§9 の provider ホスト行へ）」 |
| N2-11 | P2 | leg2 #0 `SRT`/`OMP`、#4 `mkshim` の `bin` | shim は realpath を `env -i` + PATH `<seat>/bin:/usr/bin:/bin` で実行する。`~/.local/bin/srt`／`omp` や 9 tool の `command -v` 先が mise 等の wrapper だと、realpath は wrapper 自身で `env -i` 下で動かない。解決できない tool は `for` の終了値に埋もれ dangling link のまま進む。A-2 の配置は未確認 | `mkshim` の `for … ln -sfn` と `&&` 鎖; srt-facts Q1（bin は `dist/cli.js`、node 22+） | #0 で `$SRT`/`$OMP` の先頭行（shebang）を出力、`mkshim` で 9 tool の解決結果を 1 行ずつ出し、空か wrapper なら止める |
| N2-12 | P3 | leg2 #0 `M=` | 山括弧の手置換が 1 行の `&&` 鎖の中にあり、置換し忘れると zsh の parse error で #0 全体が走らない（fail-closed）が、原因が「M の置換」だと読めない | 前書きに定義あり、行内の形 | `M=` を #0 の前の独立行にし、`leg1.out` の値を写す旨を注記 |
| N2-13 | P3 | leg2 #3b anthropic 分岐 | 鍵を素の `cat` に打つので pane に echo され scrollback に残る（history と `leg2.out` には入らない） | 行の形 | echo を切って読む形（`read -rs`）か、エディタで 0600 file を書いてから `auth import` |
| N2-14 | P3 | leg2 #3b 再試行、#5 (12) 再試行、#6 | `jq` の出力先（#4c の tmp → mv 形）が無い; `allowMachLookup` の候補値が無い; #6 で打つ 2 行と期待する echo が無い | 各行 | 各 1 句 |
| N2-15 | P3 | leg2 見出し・末尾; `mkshim` の `PILOT_LOG`; #4a | 見出しが「v4 §4」（M-08）; `PILOT_LOG` 先が worker allowWrite 外で hook 記録が空（M-09）; `session-owners` と session id の対応を出さない（M-11）; handout に期待出力が無く plan §4 表を並べる前提; #5 の `limit 2` に RESULT が入らないことがある | round-5 M; leg2 L75 | M-08/09/11 の直し + 「期待出力は plan §4 第 2 脚の表、#5 は RESULT が見えるまで select を再実行」を末尾に |

## 5. 通過した手順とファイル

- 手順: 前書き、#0（placeholder `__MAIN__` の 1 回置換、5 本の存在）、#1、#2、#3（`/usr/bin/log`、pid file、`lsof`）、#3b 資格情報（profile 別、0600 file + `rm`）、#3c（clone が起動前）、#4 shim の中身（allowWrite 外・`chmod +x`・HCOM_* 7 名・`env -i`・TMPDIR と debug log が allowWrite 内）、#4c（binding の順序）、#5（14 項目の絶対パス、拒否/成功/網/GitHub の期待が plan 表で区別可、`@pilot2-`）、#7 の私設 `HCOM_DIR`・taint 検査・binding false 先行・植え付け 4 種・nonce、#8（`instances` から pid、`&&` 鎖の成立、入れ子無し、操作者側 redirect）、#9、#10（3 tag の `kill tag:`、log stream の pid、GitHub の一覧、処分文、`~/.hcom` 温存）。`kill %1` は無い。貼る command に秘密は無い。
- ファイル: `srt-worker.json`（有効、§1.3 worker 行と一致、allow-list 6 項 + `eval-js` deny、denyRead `<main>`/`~/.hcom/env`/`~/.omp/logs`）、`srt-orchestrator.json`（有効、§1.3 の #8 用近似と一致）、`srt-audit.json`（schema 有効、§1.3 audit 行と一致、L-01/L-15 済; M-01 の 1 項だけ欠く）。3 本とも placeholder は `__MAIN__` のみ、`$TMPDIR`・home 実パス・user 名 0 件。
- 操作者が持ち越す 未確認: runner script の原文に `--dir` が含まれるか（N2-05）; `hcom list --json` の外形（N2-09）; 読取拒否の cwd で bash/`sandbox-exec` が立つか（N2-01 派生）; provider ホストの実値（N2-10）; `~/.local/bin/srt`/`omp` と 9 tool の realpath が wrapper でないか（N2-11）; `instances.status` の kill 後の値（#8 の select は順序で救われる）; 継承 fd 2 への write が Seatbelt を通るか（I-16、#4a で測る）; `hcom kill` が herdr pane を閉じるか; trustd 無しで Bun の TLS が通るか（#7）。

## 6. 報告（8 行）

1. 件数: P0 0、P1 4（N2-01 cwd、N2-02 `GIT_CONFIG_NOSYSTEM`、N2-03 results cwd の denyWrite、N2-04 shim 無しでも席が立つ）、P2 7（N2-05〜N2-11）、P3 4（N2-12〜N2-15）、計 15。うち round-5 M-01/M-02/M-03 の未処置が 3 件（N2-01〜03）。
2. JSON 3 本は schema として全部有効（必須 5 配列・入れ子・boolean・鍵集合・placeholder `__MAIN__` のみ・home 実パス 0）。設定の欠けは `srt-audit.json` の results cwd 1 項だけ。
3. 止まりやすい手順: #3b throwaway（cwd が `<main>` で第 1 の問いが濁る）、#4a（runner の grep が空で shim の確認ができない、`lsof` の pid 違い）、#7 読み取り（`ANAME` 抽出が外れると 5 コマンドが連鎖失敗）、provider ホスト拒否時の #3b/#7（再試行文無し）。
4. 最も危ないのは N2-04: `mkshim` が無い／壊れた状態で #4・#7 の起動が通り、sandbox 無しの yolo 席が push/PR と forbidden touch を実行する。`&&` のガード 1 本で閉じる。
5. 注意時間: #3b の login 2 回、#5 の 3 分待ち、#7 の最長 5 分待ち、#4c/#7 の再起動分岐で、plan の 100〜120 分は妥当。pane を開き直すと #0 の変数と `mkshim` が消えるので 1 pane で通す。
6. srt が入れば第 2 脚は走る: N2-01〜N2-04 は各 1〜2 行の修正で、#1〜#10 の命令形・flag・変数・placeholder は定義済みで未定義は無い。修正無しで走らせると #3b・#5 (10)・#7 の 3 つの測定値が解釈不能になり、B-3 の allow-list と W0 の根拠に誤りが入りうる。
7. 未確認（操作者が実機で見る）: runner の `--dir` 有無、`hcom list --json` の外形、読取拒否 cwd での起動、provider ホスト、`srt`/`omp`/9 tool の realpath、`instances.status`、継承 fd の write、pane の close、Bun の TLS。
8. 推奨: N2-01〜N2-04 と N2-07〜N2-09 を handout に入れてから配る（P2 の残りは注記 1 句ずつ）。JSON は `srt-audit.json` の 1 項追加のみ。
