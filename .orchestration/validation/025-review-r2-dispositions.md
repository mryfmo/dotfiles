# Plan 025 review round 2: dispositions (v3)

- 対象: `.orchestration/plans/025-regime-cutover-plan.md` v2（sha256 prefix `7c5a7a1c`、244 行）への round 2 の 3 審査（failure F-01..F-33、consistency E-01..E-36、sources V-01..V-19、計 88 件）と、failure 審査が「部分」と判定した round 1 の 8 行（A-04、R1B-01、R1B-15、R1B-20、S-04、S-18、S-20、S-13）。処分は v3（同ファイルを in place で改訂、294 行、sha256 prefix `4ebb70d7`）に反映済み。書いたのは本ファイルと v3 の 2 本だけ。
- 処分の語: `fixed-in-v3` = v3 の該当節に反映、`accepted-residual` = owner の作業項目と測るコマンドを名指しして残す、`rejected` = 引用した一次資料か決定行で退ける。
- 集計（round 2 の 88 件）: fixed 87、residual 1（F-32）、rejected 0。優先度別 fixed/residual/rejected: P0 3/0/0、P1 23/0/0、P2 37/0/0、P3 24/1/0。round 1 の部分 8 行: fixed 7、residual 1（S-13）、rejected 0（P0 1/0/0、P1 1/0/0、P2 4/1/0、P3 1/0/0）。
- 設計級の決定（v3 で取った 13 点、代替は v3 §9）: (1) worker 席は独立 clone（F-10）; (2) `bus:` seam 無し、C-1 は置換型のまま X-0 で merge、rollback は `git revert -m 1`（V-04/E-04/R1B-01）; (3) A-2 は使い捨てプロジェクトで `npm audit signatures`、tarball を `-g` で導入（V-01）; (4) `--no-session` を使わない、audit 席は `--session-dir`（V-02）; (5) 席ごとのディレクトリ（shim + settings + bin）と shim の `env -i`、鍵は profile store（V-03/S-18/F-15）; (6) B-3 は加算型で Codex 席 a012、5 席目無し（E-02/E-03）; (7) ruleset strict/thread resolution は OFF（E-01）; (8) J-N2 は X 手順 4 まで（F-05/F-14/S-13）; (9) stop-gate の上限 N=3（F-11）; (10) `omp-run.sh` の poll/timeout/孤児検査、provider allowlist は第 2 脚 #5 の 1 タスクで `srt --debug`（F-12/F-13）; (11) 役割表・席ごとの描画・X-0・`<results dir>`・`--resume`・W8 の条件（E-06..E-09/E-25..E-28）; (12) §11 新設（E-11..E-23/E-29/E-30 と D/F の P2）; (13) skills 既定・`instances` の sqlite 読み・`allowLocalBinding: true`・`events --wait --after`・handout の訂正群（V-06..V-12、F-16..F-24、A-04、S-20、F-01、F-02、R1B-15）。

| id | P | disposition | where in v3 (section) or the reason |
| --- | --- | --- | --- |
| F-01 | P1 | fixed-in-v3 | §4 第 2 脚 #4（`git clone … $PILOT/clone` + `commit.gpgsign false`）、#5（clone の中で switch → commit → push → PR → close、`<main>` に触れない）; §8「`<main>/.git` を allowWrite に足す方向は取らない」 |
| F-02 | P1 | fixed-in-v3 | §4 前書き（各脚の冒頭で `export PILOT PILOT_LOG`、handout は orchestrator が本節から再生成）、第 1 脚 #6（`events.ts` の仕様: 既定ログ `${PILOT}/events.log`、`line()` の try/catch、`session_stop` の 1 回目 block と 4 回目の cap）、第 2 脚 #4（shim が `PILOT_LOG` を渡す）; §7「今（W1）」 |
| F-03 | P2 | fixed-in-v3 | seam を置かないので消滅: §1.5（B-1 ‖ C-1 の allowed_files は互いに素）、§3 W2a/W2b、§5 C-1 行 |
| F-04 | P2 | fixed-in-v3 | §1.3 orchestrator 行の `denyWrite` に `<main>/.agents/worklog/uv-tools`; §2 A-2 行（doctor は dispatch が実行する private hcom の realpath を検査） |
| F-05 | P1 | fixed-in-v3 | §3 X 手順 4、§7「今」と「X 手順 4」、§9 J-N2 行、§10.3: J-N2 は orchestrator が omp 席になる手順 4 まで保ち、測り方は `jq '.sandbox.excludedCommands // []'`; §3 W6a の live は手順 2（J-N2 下の Claude 席）と手順 5（omp 席） |
| F-06 | P2 | fixed-in-v3 | §1.2 shim の `env -i` と allowlist（pane shell の rc は届かない）; §9「席の環境」行; §4 第 2 脚 #4b/#7 で名前を貼る |
| F-07 | P2 | fixed-in-v3 | §4 第 2 脚 #1（`--help` と不在 settings だけ）、#2b（`--` の probe を #2 の後に）、前書きの `export PILOT` |
| F-08 | P3 | fixed-in-v3 | §4 第 2 脚 #3（`echo $! > logstream.pid`）、#7/#8（`cat > … <<EOF` の作成行）、#10（`hcom kill tag:pilot2 tag:pilot-audit`、`kill "$(cat logstream.pid)"`） |
| F-09 | P3 | fixed-in-v3 | §1.2/§1.9: worker/orchestrator 席は操作者、audit/review/security 席は `omp-run.sh`（X でだけ操作者も） |
| F-10 | P0 | fixed-in-v3 | §1.1（独立 clone: `<seats root>/<name>`、`git clone` from origin、`--reference` 不採用、orchestrator は GitHub から fetch、agmsg 席は X まで worktree のまま）、§1.3 worker 行（`<clone>`）、§3 W5b、§4 第 2 脚 #5（clone での commit/push/PR）、§6 5.14 表 item 0/8、§9「worker の作業場所」行（代替 (b)） |
| F-11 | P1 | fixed-in-v3 | §1.8（上限 N=3、4 回目は許可 + marker + `status=blocked` PONG）、§3 W6b の単体テスト「4 回目は許可」、§4 第 1 脚 #6/#15（cap の測定） |
| F-12 | P1 | fixed-in-v3 | §1.7 (2)〜(5)（`--after <launch_ts>`、poll、timeout は transcript + `Verdict: blocked` + 1 回再試行、`hcom kill` 後の sqlite + `kill -0`）、§3 W6a の fixture、§4 第 2 脚 #7/#8 |
| F-13 | P1 | fixed-in-v3 | §1.2（本番 shim も `--debug`、`<seat dir>/srt-debug.log`、boundary/doctor が `Connection blocked to` を報告）、§4 第 2 脚 #5（1 タスク分のホスト集合）、§9 provider 行（refresh ホストは X の 24 時間で観測） |
| F-14 | P1 | fixed-in-v3 | §3 X 手順 4/5（orchestrator を先に omp 席へ、DoD11 の dispatch は新 orchestrator）、手順 2 (a)（PING は操作者端末から）、§4 第 2 脚 #8（srt 下の orchestrator から `hcom list`/`hcom send`）、§8/§9/§11 #15（代替 (b) = 一時付与） |
| F-15 | P1 | fixed-in-v3 | §3 X 手順 2（`hcom-seat worker` と `omp-run.sh` の live リハーサル）、§1.2（hcom-seat は private hcom を絶対パスで呼び `PATH=<seat dir>:$PATH`、席の PATH は `<seat dir>/bin`）、§4 第 2 脚 #4（本番形の shim で起動） |
| F-16 | P2 | fixed-in-v3 | §1.2（祖先検査に頼らない: `instances.launch_args` の一致、canary PONG、`SANDBOX_RUNTIME=1`）、§2 `check-regime-boundary.sh` 行、§4 第 2 脚 #4b（席内 `ps -p $$` の可否） |
| F-17 | P2 | fixed-in-v3 | §7 見出し（`make update` は `<canonical>` で、`git -C <canonical> log -1 --oneline` を貼る）、§3 X 手順 2 (c)（revert の形の確認、PR は作らない）、§8「X」（rollback PR は凍結の対象外） |
| F-18 | P2 | fixed-in-v3 | §3 X 手順 2 (d)（Claude pane の hold → resume → inbox）と (e)、W6b（agmsg identities ∪ `instances`、旧側は warning）、§2 `check-regime-boundary.sh` 行、§11 #6 |
| F-19 | P2 | fixed-in-v3 | §3 W9 の依存「X 手順 6（24 時間経過、旧 pane を閉じた後）」、§7「X 手順 6」「E1/E2/E3」行 |
| F-20 | P2 | fixed-in-v3 | §1.9（profile ごとに別に入れる: `omp --profile audit login openai-codex`、Anthropic は `auth import -`; 複製は jq で provider を絞る）、§9 provider 行（観測項目: 役割ごとの `omp --profile <role> auth`） |
| F-21 | P2 | fixed-in-v3 | §4 第 1 脚 #2（status が出る、`hcom.db` は #9 で現れるので続行、停止は権限エラー文だけ） |
| F-22 | P2 | fixed-in-v3 | §4 第 2 脚 #3b（`omp --profile pilot-audit login openai-codex` を先に）、§7「今（W1）」（`omp login openai-codex` は第 2 脚で必須） |
| F-23 | P2 | fixed-in-v3 | V-01 の形に置換: §2 A-2 行の 4 手順（使い捨てプロジェクトで `npm audit signatures`、integrity 比較、tarball を `-g`、`npm ls -g` receipt）、§3 W3 |
| F-24 | P2 | fixed-in-v3 | §3 X 手順 3（handoff 1 枚 + boundary PR、新席の最初の turn が読む）、§1.2（`--resume <omp session id>` = `hcom list <name> --json` の `session_id`）、§1.8 |
| F-25 | P3 | fixed-in-v3 | §8「X」（`MODEL_PROFILE_AUDIT_OMP_MODEL` の provider 側 = openai-codex の値に替えて再起動） |
| F-26 | P3 | fixed-in-v3 | §1.9 と §7（B-1 merge だけ既定 profile の対話用 omp を閉じる; 席は profile 別で対象外; srt template/shim を変えた merge の後だけ席を再起動） |
| F-27 | P3 | fixed-in-v3 | §3 W6b の完了条件（`hcom-orchestration` が出て agmsg 系が出ない） |
| F-28 | P3 | fixed-in-v3 | §9「信頼側（orchestrator 席）の残余」行（`~/.hcom/integrations`・`.tmp/launch`・`<main>/.agents/worklog/srt-seats/` を書ける） |
| F-29 | P3 | fixed-in-v3 | §3 W9（Routing の目的、E1 の permgate/manifest/renderer は操作者適用）、§7 E1 前の確認行、§11 #8 |
| F-30 | P3 | fixed-in-v3 | §4 第 1 脚 #6（repo 相対の `.agents/worklog/orchestrator-glue/pilot/`） |
| F-31 | P3 | fixed-in-v3 | §4 第 1 脚 #4b（固定コマンド 2 本、期待は「行が出る」） |
| F-32 | P3 | accepted-residual | owner: B-3（W5a）。測るコマンド: 第 2 脚 #4b の `omp --profile pilot-worker config get modelRoles --json`（役割 profile の既定）。不可なら B-3 で profile の `config.yml` にも `modelRoles` を描く。D9 の上限が費用の上限（§9 行） |
| F-33 | P3 | fixed-in-v3 | §1.2 S-08 (1)（`instances` 行と `--dir <dir>` を含む runner で照合、「最新」は使わない）; 席ごとの shim なので `SRT_ROLE` は無く、settings が無ければ shim が exit 2 |
| E-01 | P1 | fixed-in-v3 | §2 keep 行（strict=false・thread resolution=false、D-024-01/02、DoD9）、§1.6、§4 第 1 脚 #0（`gh api … rulesets/<id>` の貼り付け）、§11 #14（README/SKILL の訂正は E2、新 SKILL に古い文を持ち込まない） |
| E-02 | P1 | fixed-in-v3 | §1.3 冒頭と §3 W5a（B-3 は top-level `srt:` 節の加算のみ、`claude.sandbox` 不変、描画結果 byte 不変のテスト、席は a012） |
| E-03 | P1 | fixed-in-v3 | §3 前文（4 席のまま、5 席目無し、a009 = A-2 → B-1 → B-2 → X-2、a008 = C-1 → C-2' → X-1、a012 = B-3、a011 = anchor）、§10.3 |
| E-04 | P1 | fixed-in-v3 | §1.5（seam 無し、C-1 は item 6 どおり `storage.sh` の source をやめる、X-0 まで旧コードが main にある）、§2 dispatch 行、§5 C-1 行 |
| E-05 | P2 | fixed-in-v3 | §3 W2b と §5 C-1 行（orchestrator が dispatch 時に `after: []`（D-024-87 J-P）と `dispatch_status` を更新; amendment の内容ではなく記録作業） |
| E-06 | P1 | fixed-in-v3 | §1.2/§1.9（実行主体を 1 か所で定義）; R1B-20 の処分文も同じ |
| E-07 | P1 | fixed-in-v3 | §1.1 役割表（5 行 × omp profile / srt template / policy / `MODEL_PROFILE_<P>` / `--skills` / TMPDIR）、§1.7（review/security は audit の template と policy、model だけ違う）、§3 W5b（hcom-seat は表を manifest の `srt.roles` から読む） |
| E-08 | P1 | fixed-in-v3 | §1.2（hcom-seat が起動ごとに `<main>/.agents/worklog/srt-seats/<name>/` に settings/bin/shim を描画、template の placeholder、worker は `tmp` だけ書ける）、§3 W5a（render テストは template の鍵集合と placeholder 集合を固定）、W5b（埋め込みのテスト） |
| E-09 | P1 | fixed-in-v3 | §1.2（`<seat dir>/bin` の symlink 群 node/bun/git/gh/uv/jq/sqlite3/hcom/python3、shim の PATH、`PATH=<seat dir>:$PATH` で hcom を起動）、§4 第 2 脚 #4（同形の shim で測る） |
| E-10 | P2 | fixed-in-v3 | §1.2 shim 3 行（settings 不在で exit 2、`env -i` の名前列挙に `UV_CACHE_DIR`、`SRT_ROLE` は廃止）、§6 5.14 表 item 9 |
| E-11 | P2 | fixed-in-v3 | §6 anchor 行、§8 S-M、§11 #1（決定行と `classes.yaml` への追加） |
| E-12 | P2 | fixed-in-v3 | §6 本文の形（160 行 = J7 からの変更）、C-80 行（1 round = D-024-82 からの変更）、§11 #2 |
| E-13 | P2 | fixed-in-v3 | §2「phase-1 の統合機構」行（捨てる、本文 3 本は `frozen-superseded-by-phase-2`）、§11 #3 |
| E-14 | P2 | fixed-in-v3 | §2 rules 行（体制規則 4 本 E2、`compactiondb` E3、個人用途 7 本は残す）、§7 E1 前の確認行、§11 #4 |
| E-15 | P2 | fixed-in-v3 | §2「project-map-reload hook と `home/dot_claude/**` の個人用途分」行（残す、omp 側 shim は経路外）、§9 決定 (4)、§11 #5 |
| E-16 | P2 | fixed-in-v3 | §3 W6b 完了条件と X 手順 2 (e)/6、§2 `check-regime-boundary.sh` 行、§11 #6（hold 窓の例外の決定行） |
| E-17 | P2 | fixed-in-v3 | §2 AGENTS.md 行（X-1 で参照先、E2 で語の削除）、§3 W6b、§11 #7 |
| E-18 | P2 | fixed-in-v3 | §3 W9（E1 の manifest/renderer/permgate は操作者が適用）、§2 generator 行、§11 #8 |
| E-19 | P2 | fixed-in-v3 | §3 依存の鎖と経路外（D は X 後、D-024-87; S-10 は D に同梱; #404 は close して carry）、§2 D 行、§11 #9 |
| E-20 | P2 | fixed-in-v3 | §6 5.14 読み替え表（項目 0〜10、design への追補は boundary PR、INV-2）、§11 #10/#11 |
| E-21 | P2 | fixed-in-v3 | §1.3 worker 行の `denyWrite`（`<clone>/.omp`、`.claude`、`.agents`）、§4 第 2 脚 #2/#5（`touch <clone>/.omp/x` の拒否） |
| E-22 | P2 | fixed-in-v3 | §6 anchor 行（X-2 まで a011、X-2 後は `omp-run.sh --role review`）、§11 #12 |
| E-23 | P2 | fixed-in-v3 | §9 決定 (4)（DoD12 の waive、根拠は DoD 改訂 = 操作者の決定） |
| E-24 | P3 | fixed-in-v3 | §2 `.orchestration/**` 行、§11 #13（checklist の退役、2c は決定 (2) で不要） |
| E-25 | P1 | fixed-in-v3 | §3 前文（X-0 の定義、鎖は E ← X ← (X-1 ‖ X-2) ← …、drill は X 手順 2 に吸収） |
| E-26 | P1 | fixed-in-v3 | §1.2 署名 `hcom-seat <role> [<dir>] [--prompt <file>] [--resume <omp session id>]` と `<dir>` の既定 |
| E-27 | P1 | fixed-in-v3 | §1.7（`<results dir>` = `<main>/.agents/worklog/omp-run/<task id>-<head40>/`、`cwd/`、`out.last.md` を SKILL の `<out>` に写す） |
| E-28 | P1 | fixed-in-v3 | §3 W8 完了条件（`/bin/ls` が「No such file」、統合記録が追跡パスだけ） |
| E-29 | P2 | fixed-in-v3 | seam を置かないので消滅（§1.5） |
| E-30 | P2 | fixed-in-v3 | §6 2 番目の箇条（threat_table = 5 本、5.14 行 + 4 テスト = 席の実行路の 4 本、A-2 は threat_table のみ）、§3 W3 |
| E-31 | P3 | fixed-in-v3 | 前書きの用語行（DoD/D9/J の出所、J-L の A/B/C）、§3 の行 id W2a/W2b/W2c/W5a/W5b/W6a/W6b、「P1/P2」は第 1 脚/第 2 脚に統一 |
| E-32 | P3 | fixed-in-v3 | §4 前書き（#14 を最後の送信にし、#15 の読み取りの後に #16） |
| E-33 | P3 | fixed-in-v3 | §7 の各行に期待の字面（`orchestrator.yml worker.yml`、`sandbox-runtime 0.0.81 ok`、`audit.json omp.shim orchestrator.json worker.json` など） |
| E-34 | P3 | fixed-in-v3 | §1.1 役割表の注（provider は B-1 item 0b の導出 = deep/review/standard が anthropic、audit/security が openai-codex【実測】manifest）、§1.9（鍵を入れる profile = orchestrator/worker/review） |
| E-35 | P3 | fixed-in-v3 | §2 skills 行（`project-map` は個人用途の Claude 側 skill）、manifest 行（X〜E1 は `worker_kind` を誰も読まない） |
| E-36 | P3 | fixed-in-v3 | §2 DoD5 行（`.ua/**` は範囲外）、§3 経路外、§10.6 |
| V-01 | P0 | fixed-in-v3 | §2 A-2 行（使い捨てディレクトリで `npm install --ignore-scripts --save-exact @anthropic-ai/sandbox-runtime@0.0.81 && npm audit signatures` → integrity 比較 → tarball を `npm install -g --prefix ~/.local --ignore-scripts` → `npm ls -g` receipt）、§3 W3 |
| V-02 | P0 | fixed-in-v3 | §1.2（どの席も `--no-session` を付けない）、§1.7 (6)（usage は `sessions/*.jsonl` か `hcom list <name> --json`）、§4 第 1 脚 #9/#17、第 2 脚 #7（`--session-dir $PILOT/out/sessions`） |
| V-03 | P1 | fixed-in-v3 | §1.2（役割も環境も席ごとのディレクトリに焼く、shim が `CLAUDE_CODE_TMPDIR` を export、鍵は store、`--hcom-tool-path` の文字列一致）、§4 第 2 脚 #7（audit 席の `env \| cut -d= -f1`） |
| V-04 | P1 | fixed-in-v3 | §1.5/§5 C-1 行（seam 無し、置換型のまま、X-0 で merge、rollback は revert）、§9「C-1 の PR が X-0 まで open」行、§11 #16 |
| V-05 | P1 | fixed-in-v3 | §1.2（祖先検査に固定しない、`SANDBOX_RUNTIME=1` と canary）、§4 第 2 脚 #3（`log stream` が空でも結論にしない）、#4（`ps` は記録） |
| V-06 | P2 | fixed-in-v3 | §1.4（`skills.enableAgentsUser` 既定 `true`、walk-up）、§2 validator 行と D 行（repo root の `.agents/skills` を CI で拒む）、§4 第 1 脚 #4b は確認のみ |
| V-07 | P2 | fixed-in-v3 | §1.9（`omp login anthropic` は API key を受けない; `auth import -` の JSON 形）、§4 第 2 脚 #3b、§7 |
| V-08 | P2 | fixed-in-v3 | §1.3 表（allowWrite の単位を profile root `~/.omp/profiles/<role>` に）、§4 第 2 脚 #2/#3b、§9 |
| V-09 | P2 | fixed-in-v3 | §1.3 worker 行（読めなくても hcom は既定値で動く、denyRead は残す）、§9 |
| V-10 | P2 | fixed-in-v3 | §2 A-2 行（`npm ls -g --prefix ~/.local --json …`） |
| V-11 | P2 | fixed-in-v3 | §1.2 S-08 (1)（`sqlite3 -readonly … select name,pid,launch_args from instances`）、§4 第 1 脚 #10（一覧 JSON と名前指定 JSON の鍵、sqlite の列） |
| V-12 | P2 | fixed-in-v3 | §1.3 表（`allowLocalBinding: true` を既定、残余）、§4 第 2 脚 #2/#4（`false` は 1 回だけ確認） |
| V-13 | P3 | fixed-in-v3 | §1.9（`auth import -`、複製は jq で provider を絞る） |
| V-14 | P3 | fixed-in-v3 | §1.3「暗黙に書ける場所」（`~/.claude/debug` は denyRead 下で落ちる） |
| V-15 | P3 | fixed-in-v3 | §1.7（引用元は environment-variables.md の読取順）、§9 読取の残余行（`~/.env` は全席が読む、秘密を置かない） |
| V-16 | P3 | fixed-in-v3 | §1.7（hooks・extensions・settings は cwd-only、skills と `SYSTEM.md`/`RULES.md`/`.omp/AGENTS.md`/`.agents/skills` は walk-up）、§4 第 2 脚 #7（`.agents/skills/planted` の植え付け）、§2 D 行 |
| V-17 | P3 | fixed-in-v3 | §1.7 (1)（末尾の reply 指示は無視してよい、と prompt の契約に） |
| V-18 | P3 | fixed-in-v3 | §1.7 (2)/(3)（`--after <launch_ts>` を起動直後に、終了判定は poll）、§4 第 2 脚 #7、§9 |
| V-19 | P3 | fixed-in-v3 | 前書き（help の行番号は書かない）; §1.2/§1.9 から行番号を削除 |
| A-04 | P2 | fixed-in-v3 | §4 第 2 脚 #1/#2b（settings を作った後に `--` の probe） |
| R1B-01 | P1 | fixed-in-v3 | §1.5（空白期間 = X-0 まで agmsg の scripts と席、C-1 の merge は X-0、rollback は revert; seam は V-04 で却下）、§3 X 手順 0 |
| R1B-15 | P2 | fixed-in-v3 | §4 第 2 脚 #5（clone での push → PR → close）、#8（srt 下の orchestrator 形に `hcom list`/`hcom send` を追加） |
| R1B-20 | P2 | fixed-in-v3 | §1.2/§1.9（worker/orchestrator 席 = 操作者、audit 系 = `omp-run.sh`、X でだけ操作者も） |
| S-04 | P0 | fixed-in-v3 | §1.3 orchestrator 行（`<main>/.agents/worklog/uv-tools` の denyWrite）、§2 A-2 行（private hcom の realpath を検査） |
| S-18 | P2 | fixed-in-v3 | §1.2 shim の `env -i` allowlist（渡る名前の列挙）、§4 第 2 脚 #4b/#7 |
| S-20 | P3 | fixed-in-v3 | §4 前書き（各脚で export）、第 2 脚 #3/#10（pid file）、#10（`hcom kill tag:…`、`review` は clone なので `rm -rf` だけ） |
| S-13 | P2 | accepted-residual | owner: X 手順 4（§3）。J-N2 の 3 本は orchestrator が omp 席になるまで残り、その間 `chain-integrate.sh` の鎖全体が sandbox 外で走る（§6 C-80、§9 行）。測るコマンド: `jq '.sandbox.excludedCommands // []' .claude/settings.local.json` が手順 4 後に `[]` |
