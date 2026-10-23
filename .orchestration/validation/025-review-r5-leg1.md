# plan 025 review round 5 — N1: leg-1 pilot handout の操作者ドライラン

対象: `.agents/worklog/orchestrator-glue/pilot/leg1.md`（69 行）と、それが #6 で写す `events.ts`（54 行）・`policy.yml`（10 行）。plan v5 `.orchestration/plans/025-regime-cutover-plan.md`（sha256 prefix `9ce32b71`、326 行）§4 第 1 脚と §7「今（W1）」。読み取り専用。フラグと挙動の事実は `b2-c2-facts.md`、`srt-facts.md`、`025-review-r1-accuracy.md`、`025-review-r2-sources.md`、`025-review-r3-dryrun.md`、`025-review-r3-consistency.md` の引用だけから取り、そこに無いものは 未確認 と書いた。`omp`・`hcom`・`gh`・`git` は打っていない。

歩き方: 操作者（herdr の pane、`<main>` に cd 済み、`omp` と `hcom` は `~/.local/bin`）として #0a〜#18 を順に貼る前提で、各ブロックについて (a) コマンドとフラグが facts にあるか、(b) 変数と前提ファイルがそれより前で作られているか、(c) 期待出力が決められるか（hook の block と policy の deny が区別できるか）、(d) 機械に何を残し #18 がそれを名指すか、(e) 止め方と再試行、(f) `leg1.out` 経由で `025-pilot-facts.md` に秘密・home パス・account 名が落ちないか、を見た。

状態: 完了（全 6 節）

## 1. 歩行表

| step | command ok? | prerequisites ok? | expected output decidable? | leftovers | note |
| --- | --- | --- | --- | --- | --- |
| 前書き | — | herdr pane と `HERDR_SOCKET_PATH` の注意あり（H-29） | — | — | 「出すべき出力は plan §4 の表」と末尾にあり、handout 単体には期待出力が無い。操作者は §4 の表を並べて読む必要がある（N1-12） |
| #0a 前書き（cd、`PILOT`/`PILOT_LOG` の export、`OWNER_REPO`） | `git rev-parse` ok。`gh repo view --json … -q` は facts に引用が無い: 未確認（§4 前書きが値の定義に使うだけ） | 新規変数を全部ここで定義。`PILOT`/`PILOT_LOG` は export、`OWNER_REPO` は同じ shell 内でのみ有効（#7/#14 が使う。別端末なら #0a からやり直しと明記されていない、N1-13） | `OWNER_REPO=` の 1 行が出る: 決定可 | `$PILOT` ディレクトリ | 公開値（repo owner）だけが `leg1.out` に入る |
| #0 ruleset 2 段 + Actions switch | `gh api --jq` は r3 で確認済み。`--jq` のオブジェクト構築は jq 文法で問題なし | `RULESET_ID` は操作者が角括弧を手で置換する前提。置換せず貼ると zsh が `<` をリダイレクトと読んで止まる（N1-11） | 7 本の required checks と 3 値（§4 #0）: 決定可。`exit=` は 2 段目にだけ付く | 無し | 出力に account 名は出ない（`bypass_actors` が空なら） |
| #0b GitHub 資格情報の置き場 | `gh auth status`、keychain 2 種別の検索、`git config --show-origin --get-all`、`/bin/ls -la`、`grep -c`: 全部実在（r4 L-05/L-06 の LOCAL 実測） | 無し | 2 種別とも exit 0、helper 2 段、`0`: 決定可。`grep -c` が 0 件のとき exit 1 を返すがブロック内なので続く | 無し | `gh auth status` は token を自分で伏せる。GitHub login と、`ls -la` の所有者列の OS user 名が `leg1.out` に入る → mask 規則（user 名 → `<user>`）の範囲。GitHub login が OS user 名と違う場合の mask は規則に無い（N1-14） |
| #1 版 | ok | 無し | 2 行: 決定可 | 無し | — |
| #2 店の初期化 | `hcom status` 実在（r1）。`~/.hcom` は `.tmp` だけ（r3 実測） | 無し | 「権限エラー文が出たときだけ止める」が書かれている: 決定可 | `~/.hcom/hcom.db`、おそらく `config.toml`（`hcom status` が作るかは facts に無い: 未確認） | 止め方あり |
| #3 設定の既定値 | `hcom config <key> --info` 実在 | 無し | `omp_args` 空、terminal 一覧に `herdr`、`auto_approve` の既定: 決定可（A-03: template は出ない、と期待を下げてある） | 無し | — |
| #4 omp の実値 | `omp config path|get --json`、`omp models find <pattern> --json`: 実在（r1） | cwd は `<main>`。repo に `.omp/` は無いので project 層は無関係 | 7 鍵の実値と 4 モデルの `contextWindow`: 決定可（未設定鍵は既定か error が出る; どちらも記録対象） | 無し | `omp config path` の home パスは mask 対象 |
| #4b 起動フラグと auth の形 | `omp --help`、`omp config list --json`、`omp auth --help`、`omp login --help`、`sqlite3 -readonly … .schema`: 実在（r2 T3、r3） | `agent.db` はこの機械に在る（H-32 の実測） | 「これらの行が出る」: 決定可 | 無し | `config list --json` は skills 行だけ grep で抜くので秘密は通らない。**ここで出る `omp auth --help` を #6b の前に読む指示が無い**（N1-02 に関係） |
| #5 非対話フラグ | `grep -n -E` の regex は Markdown の `\|` 混入が無い（A-10 解消）。`\s` は BSD grep での受理が facts に無い: 未確認（r3 は #5 を「通る」と評価） | 無し | 行が出る: 決定可 | 無し | コメント「席では使えない: hcom の拒否引数」は不正確。A-08 で拒否されるのは `-p`/`--print`/`--mode`/`--no-extensions`/`acp` で、regex 中の `--max-time`/`-e`/`--config`/`--skills`/`--thinking` は #9 で席に渡している。拒否される `--no-extensions` が regex に無い（N1-10） |
| #6 ファイル配置 | `cp`、`: >`、`/bin/ls`: ok | 5 本の source は repo にある（確認済み: `events.ts`、`policy.yml`、`srt-audit.json`、`srt-orchestrator.json`、`srt-worker.json`）。cwd が `<main>` であること（#0a）に依存 | 一覧が出る: 決定可 | `$PILOT/{events.ts,policy.yml,srt-*.json,events.log}` = 意図的（#18 が名指す） | plan §4 #6 は「7 本」と言うが handout は 5 本（M-08、本 round では再掲のみ） |
| #6b 資格情報 | `omp auth import <FILE>` は FILE か `-` を取る（V-13）。`umask 077` の subshell で 0600 ファイルを作り、import 後に消す形は H-21 のとおり。`omp login openai-codex` 実在 | #7 の前に置かれている（H-03 解消）。**import するファイルの JSON の形（`version`/`credentials`/`provider`/`credential.type`/`source` の鍵）は facts のどこにも引用が無い: 未確認**。形が違えば import が落ち、#7 は鍵無しで走る（N1-02） | `M=` の 1 行: 決定可。ただし「import が通ったか」の判定行が無い（exit を出していない） | 既定 profile の `agent.db` に資格情報（意図的、#18 が名指す）。`anthropic.json` は `rm -f` で消える（import が失敗しても消える: `;` 区切り） | 鍵は stdin（Ctrl-D）経由で history に乗らない。import の stdout は `tee` に入れていないので `leg1.out` にも乗らない。良い |
| #7 非対話 1 回（hook の block と `session_stop` の cap） | `--no-session`、`--no-extensions`（明示 `-e` は生きる）、`-e`、`-p`、`--max-time`、`--model`: 実在（facts Q1/Q3、r1）。`--thinking` も `omp --help` に在る（H-04） | `events.ts`（#6）、`M`（#6b）、`OWNER_REPO`（#0a）、`PILOT_LOG`（#0a、#6 で空に）: 全部先に在る。`PILOT_STOP_N=3` は omp のプロセス環境に乗るので in-process の extension から読める | 期待（§4 #7）: `tool_call block probe` → `session_stop block n=1..3` → `allow n=4 cap` → `agent_end`、返答に `pilot deny`。行の有無で決まる。ただし (a) `--max-time 180` は xhigh の 5 ターン分には短い可能性があり、途中で切れると「cap に届かない」と「`session_stop` が発火しない」が区別できない（N1-04）; (b) 再実行条件「model not found 系」は、fuzzy match が黙って別モデルを選ぶ場合に成立せず、どのモデルで走ったかを出す行が無い（N1-05） | `~/.omp/agent/history.db` の 1 行（`--no-session` で session file は無し）。`$PILOT_LOG` に行が溜まる（#9 の前に空にする） | 止め方: 1 回だけの再実行指示あり。hook が効かなくても実行される実コマンドは存在しない repo への `gh pr merge` + 未知フラグなので無害 |
| #8 方針ファイル | `cat` | #6 | 字面一致: 決定可 | 無し | — |
| #9 hcom で omp 席を 1 つ | `hcom omp --tag/--dir/--terminal herdr`、`--` で hcom のフラグが終わる（srt-facts: `if args[i] == "--"` ends hcom's flags）、以降は omp へ転送。`-e`/`--config`/`--model` は A-08 の拒否リスト外。`--no-session` を外してある（V-02 解消） | `events.ts`/`policy.yml`（#6、`--config` は missing file が hard error なので順序が要る: 満たす）、`M`、`PILOT_LOG`。**環境変数 `PILOT_LOG=` を `hcom omp` の前置で渡しているが、席は herdr サーバが開く pane の中で runner script から起動され、runner が export するのは `HCOM_*` + PATH + cwd だけ、外部 env の経路は `~/.hcom/env`（srt-facts 87 行）。起動側の env が席に届くかは facts に無い: 未確認。届かなければ `events.ts` は `PILOT` も無いので `/tmp/claude/events.log` に落ち、そのディレクトリが無ければ try/catch で黙って捨てる**（N1-01） | 「pane が開く、exit=0」: 決定可。起動失敗時の死骸の消し方（`hcom kill tag:pilot`）あり（H-22 解消） | herdr の tab/pane、`~/.hcom/.tmp/launch/*.sh`、`~/.hcom/integrations/omp/<digest>/`、instances 行、既定 profile の session file（cwd=`$PILOT`） | `launch_args` に `$PILOT` の絶対パスが入る → mask 対象 |
| #10 席の確認 | `hcom list`、`hcom list --json`、`hcom list <name> --json`、`hcom list <name> <field>`（`status`、`transcript_path`）、`hcom events --idle <name> --wait 90`: 実在（facts Q5、H-05 の help 引用）。`sqlite3 -readonly` の `instances` 3 列は schema どおり（facts Q5） | `NAME` は python で `hcom list --json` の `tag == "pilot"` の最後の行から取る。一覧 payload に `tag` は在る（V-11）。top-level が配列か `{"agents": …}` かは python が両対応。該当行が無いと IndexError で `NAME` が空になり以降が全部空名で走る（#9 成功が前提なので P3、N1-15） | `listening` なら `--wait` を打たない分岐あり（H-05 解消）: 決定可。`hcom list <name> --json` に `pid`/`launch_args` が無いことは V-11 で既知で、sqlite 側で読んでいる | `$PILOT/transcript_path` | `directory`/`transcript_path` に home パス → mask 対象 |
| #11 TASK を 1 本 | `hcom send --from <ext> @<name> --json -- <text>`: help どおり（`--` の前にフラグ） | `NAME`（#10） | 受領 JSON（`id`）: 決定可。席への指示「`hcom send @orch -- …` で返す」は `orch` が local instance でないので拒否されうるが、それ自体が C-1 の返信経路の測定で、#13 に代替がある | events 行 | — |
| #11b thread 付き | `--thread` 実在 | 同上。席に送る文中の `$HCOM_TAG` は single quote 内で literal のまま届き、席の shell が `pilot` に展開する（facts Q5: `HCOM_TAG` は席の env）: 意図どおり | 受領 JSON: 決定可 | events 行 | — |
| #12 店の中身 | `pragma table_info(events_v)`、`events_v` の `msg_from`/`msg_thread`/`msg_scope`/`msg_text`: schema どおり（facts Q5） | #11/#11b | TASK 2 行 + RESULT 行。**`sleep 30` 固定で、xhigh の席が 30 秒で RESULT まで至らないと「RESULT 無し」と読まれ #13 に進む。再 select の回数・間隔の指示が無い**（N1-06） | 無し | `msg_text` 60 字: 指示文の一部だけ。秘密なし |
| #13 返信の別形 2 つ（条件付き） | `@pilot-` の tag fan-out、broadcast `send --`: help どおり | #12 で RESULT 無しのときだけ、と明記 | select 再実行あり: 決定可 | events 行 | — |
| #14 policy の deny（最後の送信） | 同上 | `NAME`、`OWNER_REPO` | probe 語無しなので hook は `tool_call bash keys=…` を記録するだけで block せず（events.ts 47 行）、policy の `*gh pr merge*` deny が omp の層で拒む。RESULT の拒否文は hook の `pilot deny` とは別文言 → **2 層は区別できる**。さらに #15 の log に `tool_call block probe` が無いことで二重に確認できる。`sleep 30` の固定は #12 と同じ（N1-06） | events 行 | 失敗しても実行される実コマンドは存在しない repo への merge なので無害 |
| #15 配送下のイベント | `cat`、`events_v` の `status_val`/`status_context`: schema どおり | `PILOT_LOG` | **N1-01 により `cat "$PILOT_LOG"` が空でも「`session_stop` が hcom 配送下で発火しない」とは言えない。現状の handout にはその注意が無い** | 無し | — |
| #16 停止 | `hcom kill --help`、`hcom kill tag:<tag>`: help どおり（F-08、H-22） | — | pane が閉じ一覧が空: 決定可（killed 行が `hcom list` に残るかは未確認だが、残っても判断はつく） | instances 行（killed）、session file | — |
| #17 席側の原文 | `hcom transcript <name>`: 実在。kill 後も session file は残る（V-02、#9 は `--no-session` 無し） | `$PILOT/transcript_path`（#10） | **代替の `\|\|` がパイプライン末尾の `tail` の exit に掛かる。zsh の既定（pipefail 無し）では `hcom transcript` が失敗しても `tail` が 0 を返し、代替は走らず出力が空になる**（N1-07） | 無し | transcript に席の cwd（home パス）→ mask 対象 |
| #18 片付け | `ls`、`date` | — | — | 名指しあり: `$PILOT` 全体、hcom.db の pilot 行、既定 profile の session file と資格情報。**名指し無し**: `~/.hcom/.tmp/launch/*.sh`、`~/.hcom/integrations/omp/<digest>/`、`~/.hcom/config.toml`（#2 が作る場合）、`history.db` の行、N1-01 のときの `/tmp/claude/events.log`、kill に失敗したときの herdr tab（N1-08） | 第 2 脚 #10 が消すのは `$PILOT` と 2 profile だけなので、上の残骸は誰も消さない |

## 2. events.ts / policy.yml

**events.ts**（54 行）

- モジュール形: `node:fs` の named import、トップレベルは定数と関数定義のみ（top-level await 無し）、`export default function hook(pi)` の factory（facts Q1 の docs 例と同形）。型注釈は `any` と `Map<string, number>` で、TypeScript として妥当。Bun 上の omp が `node:fs` を解決することは facts Q1 の例（import 無し）からは直接は言えないが、`appendFileSync` は標準 API なので問題視しない。
- 全 handler が try/catch で包まれ、`line()` 自体も try/catch（throw すると fail-closed で全 bash が止まる、facts Q1）。良い。
- `session_stop`: 直近の user message の `task_id=` を key に数え、`n <= PILOT_STOP_N` で `{ decision: "block", reason }`、超えたら allow を記録し `stopN === 3` のときだけ ` cap` を付ける。§4 前書きの仕様（H-07）どおり。`event.messages`/`stop_hook_active` は facts Q1 の `SessionStopEvent` の鍵と一致。
- **key の取り方の弱点**: `taskOf` は「最後の user message」だけを見て、そこに `task_id=` が無ければ `none` を返す。r3-consistency 6 項によると block 後の次の settle は hidden な `session-stop-continuation` message を queue して同じ hook を呼ぶ。その message が user role で `task_id=` を含まなければ、2 回目以降の計数は key `none` に移り、#9 の席（N=1）で TASK ごとに「1 回 block」のはずが 2 回 block になりうる。#7 は最初から `none` なので影響しない。直し方は 1 行: 後ろから走査して `task_id=` を**含む**最初の user message を採る（当たりが無いときだけ `none`）。N1-03。
- `tool_call`: `event.toolName === "bash"` かつ `event.input.command` に `--pilot-hook-probe` を含むときだけ `{ block: true, reason: "pilot deny" }`（facts Q1 の `ToolCallEvent` の鍵と一致）。それ以外は `tool_call <tool> keys=…` を記録するだけ。policy の deny とは層も文言も別（H-06 解消）。
- ログの既定パス: `PILOT_LOG` → `${PILOT}/events.log` → `/tmp/claude/events.log` の順。最後の fallback は `/tmp/claude` が無ければ黙って落ちる（try/catch）。#9 で env が届かない場合に #15 が空になる根（N1-01）。
- `turn_start` の `ctx.getContextUsage()` は facts Q1/Q3 の handler context にある。

**policy.yml**（10 行）: `tools.approvalMode: yolo`、`tools.approval.eval: deny`、`bash.patterns` の `*gh pr merge*` deny、`skills.enableAgentsProject: false`。YAML mapping なので `--config` の strict 検査（mapping 必須、facts Q2）を通る。pattern は空白を潰した全文か segment に一致する（facts Q2）ので #14 の命令文（`gh pr merge 1 --squash --repo …`）に当たる。`eval` の deny で `bash.patterns` を迂回する経路も閉じている。§4 #8 の期待字面と一致。所見なし。

## 3. round-3 leg-1 所見の扱い

| id | 内容 | leg1.md / events.ts での扱い |
| --- | --- | --- |
| H-03 | 資格情報を #7 の前に、#7 に `--model` | handled: #6b が #7 の直前、#7/#9 とも `--model "$M:xhigh"` |
| H-04 | `:xhigh` 接尾辞の fallback | handled: #7 のコメント行に `--thinking xhigh` での 1 回再実行と記録、#9 にも「#7 で通った形」。ただし再実行の**条件**が決められない場合がある（N1-05） |
| H-05 | `events --wait` の timeout を失敗と読む | handled: #10 が `status` を先に読み、`listening` でないときだけ `--wait`、前書きに「timeout は失敗ではない」 |
| H-06 | hook と policy の層の判別 | handled: events.ts は probe 語だけ block、#7 に probe 語あり、#14 に無し |
| H-07 | `session_stop` 仕様の自己矛盾 | handled: events.ts の task_id 計数 + `PILOT_STOP_N`、#7 は N=3 で cap、#9 は既定 1。残る弱点は key の取り方（N1-03） |
| H-08 | ruleset id の出所 | handled: #0 が 2 段（一覧 → id） |
| H-10 | 第 2 脚 #3b の profile 資格情報 | leg 1 の対象外（leg2.md の範囲） |
| H-11 | `OMP_PROFILE=` 形 | leg 1 は既定 profile だけを使うので該当なし（#6b に `--profile` 無し） |
| H-13 | 第 2 脚 #5 の `<ts>`/`<pr>` | leg 1 の対象外 |
| H-14 | 第 2 脚 #7 の `--no-skills` | leg 1 の対象外 |
| H-17 | §7 X 手順 2 の `--from` | leg 1 の対象外。leg 1 の送信 4 本は全部 `--from orch` 付き |
| H-18 | §7 X 手順 1 の D9/J10 | leg 1 の対象外 |
| H-21 | 鍵を history に残さない | handled: #6b は stdin → 0600 ファイル → import → `rm`、前書きに「`gh auth token` は打たない」 |
| H-22 | 鍵無しで死んだ instance が残る | handled: #9 のコメントと #16 が `tag:pilot` |
| H-23 | 第 1 脚の片付け行と残すものの名 | handled: #18 が残すものを名指し。名指し漏れが別に残る（N1-08） |
| H-27 | #17 の transcript 代替 | handled のつもりだが代替が走らない（N1-07） |
| H-29 | herdr pane と `HERDR_SOCKET_PATH` | handled: 前書き 1 行目 |
| H-32 | #4b の `.schema` 無条件 | handled |
| H-34 | #3 の期待字面 | handled（plan §4 側） |

## 4. 所見

| id | P | step | what blocks the operator | evidence | fix |
| --- | --- | --- | --- | --- | --- |
| N1-01 | P1 | #9 席の起動 → #15 配送下のイベント | `PILOT_LOG` を `hcom omp` の前置 env で渡しているが、席は herdr サーバが開く pane の runner script から立つ。runner が export するのは `HCOM_*` + PATH + cwd だけで、外部 env の文書化された経路は `~/.hcom/env`。起動側の env が席に届くかは facts に無い（未確認）。届かなければ `events.ts` は `PILOT` も無いので `/tmp/claude/events.log` に落ち、無ければ黙って捨てる。#15 の `cat` が空のとき「`session_stop` が hcom 配送下で発火しない」と誤読し、X-1 の設計根拠が偽陰性になる | srt-facts 87 行（runner script の export 範囲、`~/.hcom/env`）; events.ts 4 行・8 行; leg1.md 45 行・60 行 | #6 で写した直後に、コピー側 `events.ts` の fallback 文字列（`"/tmp/claude"`）を `sed` で `$PILOT` の絶対パスに置換する 1 行を足す（env に依存しない）。#15 に「空なら `/tmp/claude/events.log` も見る」の 1 行。pilot-facts には「env の伝播: 届いた/届かず」を 1 行記録 |
| N1-02 | P1 | #6b 資格情報（Anthropic 側） | import するファイルの JSON の形（`version`、`credentials[]`、`provider`、`credential.type/key/source`）は facts・各 review のどこにも引用が無く 未確認。形が違えば import が落ち、`rm -f` は走り、`M` は anthropic のまま #7 が鍵無しで走って失敗する。import の exit を記録する行も無い | V-13（import は FILE か `-`、形は未引用）; V-07（Anthropic は login で API key を受けない）; leg1.md 35 行 | #4b で出る `omp auth --help` を読んで import の形（export の出力形）を確かめてから #6b に進む 1 行; import の直後に `echo import_exit=$?` を `leg1.out` に残す; import が落ちたら openai-codex 側に倒して `M` を切り替える、と明記 |
| N1-03 | P2 | events.ts `taskOf`（#9/#15 の計数） | 最後の user message だけを見るので、block 後の hidden continuation message が user role で `task_id=` を含まなければ 2 回目以降が key `none` に移り、N=1 の席で TASK ごとに 2 回 block しうる。#15 の `block n=1` の期待が 2 行になり、X-1 の「N 回で許可」の根拠が揺れる | events.ts 9-18 行; r3-consistency 6 項（continuation message の queue と再呼出し） | 後ろから走査して `task_id=` を含む最初の user message を採る（無いときだけ `none`）。`stop_hook_active` も既に記録しているので、pilot-facts で key の遷移を確認できる |
| N1-04 | P2 | #7 非対話 1 回 | `--max-time 180` は xhigh の 5 ターン（block 3 回 + 許可 1 回 + 最初の tool 呼び出し）には短い可能性がある。切れたとき `agent_end` も `cap` も出ず、「cap に届かない」と「`session_stop` が発火しない」が区別できない。再試行の指示は model 不一致の 1 条件だけ | leg1.md 40-41 行; facts Q1（`session_stop` は settle ごとに再呼出し） | 「`cap` も `agent_end` も無く exit が max-time 由来なら `--max-time 600` で 1 回だけ再実行」の 1 行。log に `session_stop block n=1` が 1 行でもあれば発火の事実は取れている、と判断基準を書く |
| N1-05 | P2 | #7 のコメント行（model 不一致の再実行条件） | `--model` は fuzzy match（H-04 の help 引用）で、`:xhigh` 付きが拒否されず別モデルに**黙って**倒れる場合、「model not found 系」の条件が成立せず、どのモデルで走ったかを出す行も無い。B-3 の `:<level>` の根拠が決まらない | leg1.md 41 行; H-04 | `turn_start` 行の `contextWindow` を #4 の `models find` の値と突き合わせる判断基準を 1 行書く（既存の出力だけで決まる）。events.ts に model 名を記録する API は facts に無い（未確認）ので追わない |
| N1-06 | P2 | #12 店の中身、#14 policy の deny | `sleep 30` 固定。xhigh の席が 30 秒で RESULT まで至らないと #12 は「RESULT 無し」と読まれて #13 に進み、#14 も RESULT 前の 3 行を貼って終わる。再 select の回数・間隔・打ち切りが無い | leg1.md 54 行・58 行 | 「RESULT が無ければ同じ select を 30 秒おきに最大 5 回、それでも無ければ #13」の 1 行を #12 に、#14 にも「最大 5 回」の 1 行。または `hcom events --idle "$NAME" --wait 120` を select の前に置く（席が `listening` に戻る = 返信済みか諦めた） |
| N1-07 | P2 | #17 席側の原文 | 代替の `\|\|` がパイプライン末尾 `tail` の exit に掛かる。zsh の既定（pipefail 無し）では `hcom transcript` が失敗しても `tail` が 0 を返し、代替は走らず出力が空。H-27 の直しが機能しない | leg1.md 64 行 | transcript コマンドの出力を一度ファイルに落とし、その**コマンドの exit** に代替（`transcript_path` のファイルを同じファイルへ）を掛け、最後に `tail -n 40` をそのファイルに打つ形にする |
| N1-08 | P2 | #18 片付け | 名指し無しの残骸: `~/.hcom/.tmp/launch/*.sh`（runner script、絶対パス入り）、`~/.hcom/integrations/omp/<digest>/`、`~/.hcom/config.toml`（#2 が作る場合）、`history.db` の行、N1-01 のときの `/tmp/claude/events.log`、kill に失敗したときの herdr tab。第 2 脚 #10 も消さない | leg1.md 65-66 行; leg2.md #10; srt-facts 87-88 行 | #18 の括弧に上の 5 つを足し「hcom 自身の成果物なので消さない」と書く。herdr tab は `hcom list` が空でも `herdr pane list` で 1 回見る 1 行 |
| N1-09 | P2 | #6b（判定行） | import / login の成否を `leg1.out` に残す行が無く、`M=` だけが記録される。#7 が失敗したとき資格情報の問題か model の問題かが後から判別できない | leg1.md 35-38 行 | import の `exit=`、login の `exit=` を `tee` に通す（token は出さない） |
| N1-10 | P3 | #5 非対話フラグ | コメント「席では使えない: hcom の拒否引数」は不正確。拒否は `-p`/`--print`/`--mode`/`--no-extensions`/`acp`（A-08）で、regex 中の `--max-time`/`-e`/`--config`/`--skills`/`--thinking` は #9 で席に渡している。拒否される `--no-extensions` が regex に無い | A-08; leg1.md 29-30 行 | コメントを「非対話実行のフラグ（席で拒否されるのは `-p`/`--print`/`--mode`/`--no-extensions`）」に、regex に `--no-extensions` を足す |
| N1-11 | P3 | #0 ruleset | `RULESET_ID=<…>` の角括弧を置換せず貼ると zsh が `<` をリダイレクトと読んで止まる | leg1.md 16 行 | 行頭に「id を手で入れてから貼る」の注記、または 1 段目の `--jq` で `select(.name=="main integration gate").id` を取り変数に入れる |
| N1-12 | P3 | 前書き / 末尾 | handout 単体に期待出力が無く「plan §4 の表」を並べて読む前提。見出しと末尾が「plan 025 v4 §4」のまま（M-08 再掲） | leg1.md 1 行・69 行 | 見出しを v5 に。各ブロックの `#` コメント行に期待出力の要点を 1 語ずつ（既に #2/#7/#9/#10 にはある） |
| N1-13 | P3 | #0a | `OWNER_REPO`・`M`・`NAME` は export されず、別端末や shell の再起動で消える。「他端末なら `HERDR_SOCKET_PATH`」の注意はあるが「#0a からやり直す」が無い | leg1.md 5 行・13 行 | 前書きに「端末を替えたら #0a と #6b の `M=` を打ち直す」の 1 行 |
| N1-14 | P3 | #0b | `gh auth status` の GitHub login が `leg1.out` に入る。mask 規則は「user 名 → `<user>`」で、GitHub login が OS user 名と違う場合の扱いが無い（この repo では owner 名 = 公開値なので実害は小） | leg1.md 6 行・18 行 | mask 規則に「GitHub login → `<login>`（repo owner と同じなら残す）」の 1 語 |
| N1-15 | P3 | #10 | `tag == "pilot"` の行が無いと python が IndexError で `NAME` が空になり、以降が空名で走る（#9 成功が前提なので実害は小） | leg1.md 48 行 | python の後に `NAME` の空判定を 1 語（空なら `NAME-EMPTY` を記録して止まる） |

未確認（操作者が leg 1 冒頭の `--help` で確かめるもの）: (1) `gh repo view --json nameWithOwner -q`（#0a）; (2) `omp auth import <FILE>` のファイル形式（N1-02、`omp auth --help` と、可能なら export の出力形の説明）; (3) `hcom omp` が起動側の環境変数を席に渡すか（N1-01、`hcom config --help` の `name_export`/`~/.hcom/env` の説明）; (4) `hcom list --json` の top-level が配列かオブジェクトか（#10、python は両対応）; (5) 操作者側 grep の `\s`（#5、BSD grep なら `[[:space:]]` に）; (6) `hcom status` が `config.toml` を作るか（#2 の残骸）。

## 5. 通過した手順

- #1 版、#2 店の初期化（止め方あり）、#3 設定の既定値、#4 omp の実値、#4b 起動フラグと auth の形、#8 方針ファイル、#11 TASK、#11b thread 付き、#13 返信の別形（条件と再 select あり）、#16 停止（`tag:pilot`）: コマンド・フラグとも facts にあり、前提は先に満たされ、期待出力は字面か有無で決まる。
- #0 ruleset（置換の注記を除く）、#0b GitHub 資格情報（token は出ない、2 種別の exit と helper 2 段は r4 の実測形と同じ）。
- #6 ファイル配置: 5 本とも repo に在り、`--config` の strict 検査を満たす順序。
- #14 policy の deny: hook の block（probe 語）と policy の deny（probe 語無し）は層も文言も別で、#15 の log（`tool_call block probe` の不在）で二重に確認できる。`sleep 30` の固定だけが N1-06。
- 資格情報の順序と置き場: #6b は最初のモデル呼び出し #7 の前、0600 ファイルか OAuth login、history と `leg1.out` のどちらにも鍵は通らない。`gh auth token` は打たない。
- 前書きの約束事（herdr pane、`tee -a` の記録と mask の担い手、#14 が最後の送信、repo に書かない）は §4 前書きと一致。
- `policy.yml` は所見なし。`events.ts` は仕様どおりで、所見は N1-01（既定パス）と N1-03（key の取り方）の 2 点だけ。

## 6. 報告（8 行）

1. 件数: P0 0、P1 2（N1-01 席への `PILOT_LOG` 伝播と #15 の偽陰性、N1-02 import ファイルの形が 未確認）、P2 7（N1-03〜N1-09）、P3 6（N1-10〜N1-15）。計 15。round-3 の leg-1 所見 H-03〜H-08・H-21〜H-23・H-29・H-32 は handout に反映済み、H-27 の代替だけが機能しない（N1-07）。
2. 止まりやすい手順 1: #9 → #15。`PILOT_LOG` が席に届く保証が facts に無く、届かなければ `events.ts` は `/tmp/claude/events.log` に落ちて黙る。#15 が空でも「`session_stop` が配送下で発火しない」とは言えず、X-1 の設計根拠が偽陰性になる。#6 の `sed` 1 行で消える。
3. 止まりやすい手順 2: #6b。Anthropic 鍵の import ファイルの形が未検証で、落ちても判定行が無く、#7 が鍵無しで走って初めて分かる。`omp auth --help` を先に読む 1 行と `exit=` の記録で消える。openai-codex 側に倒す道はある。
4. 止まりやすい手順 3: #7 の `--max-time 180`（xhigh 5 ターン分には短い可能性、切れると cap と不発火が区別できない）と、#12/#14 の `sleep 30` 固定（xhigh の席は 30 秒で RESULT まで至らないことがあり、再 select の指示が無い）。
5. 所要の見積もり: #0a〜#5 で 10 分、#6b 3〜5 分、#7 3〜6 分（再実行なら +10）、#9〜#10 5 分、#11〜#15 10〜15 分（`sleep 30` ×3 と再 select）、#16〜#18 3 分。計 50〜65 分、再実行 1 回を入れて 60〜75 分。注意を離せるのは #7 の待ちと #10 の最長 90 秒だけで、ほかは連続。
6. 書かれたとおりに打てるか: 打てる（P0 無し。全コマンドとフラグは facts にあり、変数と前提ファイルは使う前に作られ、資格情報は最初のモデル呼び出しの前に 0600 ファイルか login で入る）。ただし N1-01 を直さずに打つと、第 1 脚の主目的のひとつ（配送下の `session_stop`）が「測れなかった」ではなく「発火しなかった」と記録される危険がある。N1-01/N1-02 の 2 行を handout に入れてから打つのが最小。
7. hook の block と policy の deny は区別できる（probe 語の有無、`pilot deny` と omp の deny 文言、#15 の log の `tool_call block probe` の有無）。`policy.yml` は所見なし。`events.ts` は有効な TypeScript module（default-export factory、top-level await 無し）で、`session_stop` の計数・cap と probe block を実装しているが、key の取り方（N1-03）で N=1 の席が 2 回 block しうる。
8. 操作者が leg 1 冒頭の `--help` で確かめる 未確認: `gh repo view --json/-q`; `omp auth import <FILE>` のファイル形式; `hcom omp` の起動側 env の伝播（`hcom config --help` の `name_export` と `~/.hcom/env`）; `hcom list --json` の top-level の形; 操作者側 grep の `\s`; `hcom status` が `config.toml` を作るか。

skipped: `omp auth import` の形式と `hcom omp` の env 伝播は一次資料を開かず facts の不在だけを根拠にした（どちらも 未確認 として操作者の `--help` に回した）。risk: N1-03 は continuation message の role と内容が未測定で、実機では問題にならない可能性がある。
