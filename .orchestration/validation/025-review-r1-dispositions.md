# Plan 025 review round 1: dispositions (v2)

- 対象: `.orchestration/plans/025-regime-cutover-plan.md` v1（sha256 `79addac8…`、206 行）への round 1 の 3 審査（accuracy A-01..A-18、completeness R1B-01..R1B-33、security S-01..S-23、計 74 件）。処分は v2（同ファイルを in place で改訂）に反映済み。書いたのは本ファイルと v2 の 2 本だけ。
- 処分の語: `fixed-in-v2` = v2 の該当節に反映、`accepted-residual` = owner の作業項目と測るコマンドを名指しして残す、`rejected` = 引用した一次資料か決定行で退ける。
- 集計: fixed 73、residual 1（S-13）、rejected 0。優先度別: P0 4/0/0、P1 14/0/0、P2 31/1/0、P3 24/0/0（fixed/residual/rejected）。

| id | P | disposition | where in v2 (section) or the reason |
| --- | --- | --- | --- |
| A-01 | P1 | fixed-in-v2 | §4 第 2 脚 #3（`log stream` は書込と直接接続の拒否だけ）、#3b（`srt --debug` の `Connection blocked to` 行 = provider ホストの実値）、#4（shim に `--debug`、stderr を別ファイル）; §1.3 と §9「provider のホスト名」の閉じる場所を #3b に |
| A-02 | P1 | fixed-in-v2 | §4 冒頭（`$PILOT=$HOME/pilot-20261022`、srt は子の `TMPDIR` を書き換える）、第 2 脚 #4b（`echo TMPDIR=$TMPDIR`）、#5（TASK は絶対パス）; §1.3 で `CLAUDE_CODE_TMPDIR` を役割別に |
| A-03 | P2 | fixed-in-v2 | §4 第 1 脚 #3: 期待出力を「`herdr` が Managed（`[+]`）として出る」に、template は【srt Q2】の行が Facts |
| A-04 | P2 | fixed-in-v2 | §4 第 2 脚 #1: `srt --settings … -- /bin/echo -c --model x` の直接 probe; §1.2 に commander の終端として記載 |
| A-05 | P2 | fixed-in-v2 | §1.2: shim は `~/.agents/srt/bin/omp`（どの役割の `allowWrite` にも入らない）; §4 第 2 脚 #2/#4: pilot の shim は `$PILOT/bin` で `denyWrite` に入れ、#5 で `touch $PILOT/bin/should-fail` が拒まれることを測る; §3 W5 B-3 の Behaviour 行「実体 realpath は allowWrite 外」 |
| A-06 | P2 | fixed-in-v2 | §4 第 2 脚 #2: 非クォート heredoc で shell が展開した絶対パスを書き、`cat` で貼る。JSON 内の `$TMPDIR`/`$PILOT` は無し |
| A-07 | P2 | fixed-in-v2 | §1.4: opt-in 鍵は【未検証】と明記; §4 第 1 脚 #4b（`omp config list --json`、skill 一覧コマンド）; §3 W5 B-3 は W1 #4b の実値で鍵を決める; §9 に行 |
| A-08 | P2 | fixed-in-v2 | §1.7 と §4 第 1 脚 #5: hcom の拒否 5 件（`-p`、`--print`、`--mode`、`--no-extensions`、`acp`）; §3 W5 C-2' の argv 検査は 5 件の鏡; 席で `--no-extensions` が使えない帰結は §1.7（cwd を scratch に） |
| A-09 | P3 | fixed-in-v2 | §1.7: `-p`（最後の応答を stdout）と `--mode json` を Facts に格上げし、席では使えないので第 1 脚 #7 の throwaway だけに使う; W6 の出力対は席が書く `.last.md` + `hcom transcript` |
| A-10 | P3 | fixed-in-v2 | §4 冒頭: 貼付元は handout の fenced block（`pilot/leg1.md`、`leg2.md`）で、表は `leg1.md #n` を指す; orchestrator が本節から再生成 |
| A-11 | P3 | fixed-in-v2 | §1.3: 数を書かず鍵名 7 + `linux_excluded_commands` を列挙 |
| A-12 | P3 | fixed-in-v2 | §4 第 1 脚 #1:「新版通知付き（版は問わない）」 |
| A-13 | P3 | fixed-in-v2 | §2 asset 行と §9: omp 18.12.6 の存在、pin 不変; §3 W5 B-3 の Behaviour 行「`omp update` は srt が拒む」 |
| A-14 | P3 | fixed-in-v2 | §1.2: omp は Bun で走る; §4 第 2 脚 #4 に `command -v bun; readlink -f "$(command -v bun)"` |
| A-15 | P3 | fixed-in-v2 | §9「plugin 内の `spawn("hcom")`」行: 「node の dir、起動側 hcom の dir の順で PATH 先頭」 |
| A-16 | P3 | fixed-in-v2 | §4 第 1 脚 #10:「`[OMP]` と `listening` を含む 1 行」 |
| A-17 | P3 | fixed-in-v2 | §2 generator 行: 「codex plugin manifest の出力」など名で書き、「4+N」を削除 |
| A-18 | P3 | fixed-in-v2 | §1.5 と §4 第 1 脚 #12: 列名 `msg_thread`（`hcom events --help` の SQL reference）、pragma は確認として残す |
| R1B-01 | P1 | fixed-in-v2 | §1.5 と §3 W2 C-1: amendment で seam `bus: agmsg\|hcom`（既定 `agmsg`、`BUS=` 描画、3 スクリプトの reader 選択、fixture テスト「agmsg 席への revise 送信と counters が通る」）; X で `bus: hcom`、E2 で削除; 代替（merge を X-0 まで持ち越し）は §9 |
| R1B-02 | P1 | fixed-in-v2 | §3 W6b（drill: `bus:` の 2 往復）、W7（旧席と旧 orchestrator pane を DoD11 + 24 時間残す）、§8「X」（戻すのは `bus: agmsg` + `make update` + 旧 pane の再開）; §2 の seam 行は「E2 で捨てる」に整理 |
| R1B-03 | P1 | fixed-in-v2 | §3 W6 X-2 の依存に B-3 merge と C-2' merge; §1.4(b) audit の overlay `audit.yml` は B-3 の出力 |
| R1B-04 | P1 | fixed-in-v2 | §3 W6 X-1 に `hcom-orchestration` SKILL ≤ 80 行; §1.4 と §2: 役割別 `--skills=<glob 列>` で agmsg 系 skill を X 時点から除外、E2 は旧 SKILL と rules の削除だけ; 完了条件に skill 一覧の確認 |
| R1B-05 | P1 | fixed-in-v2 | §1.3 表: worker/audit は `allowUnixSockets: []`、orchestrator だけ herdr socket（残余 §9）; §4 第 2 脚 #2/#7/#8 |
| R1B-06 | P1 | fixed-in-v2 | §1.7: audit 席の cwd は空 scratch、checkout は絶対パスで prompt へ; 植え付け試験（`.omp/hooks/pre`、`.claude/hooks/pre`、`.env`）を §4 第 2 脚 #7 と §3 W6 X-2 の fixture に |
| R1B-07 | P2 | fixed-in-v2 | §7「今」J-N2: D-024-97 の 3 本（`text-security-review.sh`、`security-review.sh`、`chain-integrate.sh`）+ X-2 直後に外す行 |
| R1B-08 | P2 | fixed-in-v2 | §3 W9 の条件を DoD5 の文字どおり（`.ua/**` 除外、今日 67 ファイル）; §2「DoD5 の残り」行に E1/E2/E3 のどれが何を消す・書き換えるかを列挙 |
| R1B-09 | P2 | fixed-in-v2 | §2 tests（変える）行に 8 module を時期付きで追加; apparmor は「残す」行 |
| R1B-10 | P2 | fixed-in-v2 | §2 に `agent-assets.yml`、`Makefile` doctor/update-tree/agmsg-bootstrap、`check_agmsg`/`check_claude_sandbox`、`templates/task-short.md`、CompactionDB 行の拡張（vendor、`update_compactiondb`、CLAUDE.md ブロック、validator fragment）、plugins + `openai.yaml`、`remove-agent-asset`/`uv-format`/herdr integration、apparmor の各行 |
| R1B-11 | P2 | fixed-in-v2 | §2 glue 行: 41 本、昇格 16（`ff-main-safe.sh` を含む）、X-2 差替え 2、捨てる 18、旧形 5 本は今日から追跡版（`cmp`/`diff` で glue が古い形と確認）; §10.8 |
| R1B-12 | P2 | fixed-in-v2 | §6: 行数上限を `self_cap` が読む形「at or under 160 lines」（Checks 込み）に; `allowed_files ≤ 8` は anchor が手で数え機械検査は足さない; template の節名は次の boundary PR（§2 の行） |
| R1B-13 | P2 | fixed-in-v2 | §6 第 2 項: orchestrator 側 `security: true` 本文は 5.14 項目 1〜10 の行と `trusted_exec_contract.py` の 4 テスト（D-024-18）; §3 W5/W6 の完了条件にも明記 |
| R1B-14 | P2 | fixed-in-v2 | §4 第 1 脚 #6（`session_stop` 1 回目だけ `decision: block`）、#7、#15（block 行と `listening` の時刻順を `events_v` の status 行で）; §8 に否定時の扱い |
| R1B-15 | P2 | fixed-in-v2 | §4 第 2 脚 #5（scratch branch の push → `gh pr create --draft` → close）、#8（orchestrator 形: `git fetch` + `gh pr view` + herdr socket） |
| R1B-16 | P2 | fixed-in-v2 | §4 第 1 脚 #11（C-1 の形、`--thread` 無し）と #11b（`--thread` 形）; §5 C-1「送信側 item 2 の形を含みうる」 |
| R1B-17 | P2 | fixed-in-v2 | §2 `check-regime-boundary.sh` 行と §3 W6 X-1: identities の差替えは X-1（X 直前 merge）へ移動、W5 C-2' から外す |
| R1B-18 | P2 | fixed-in-v2 | §1.8: `stop-gate.ts` は `~/.agents/omp/hooks/` に描画し hcom-seat が worker と orchestrator に `-e` で渡す; §1.3: profile 分離で `~/.omp/agent` は書かない、`~/.hcom` の実行入力は denyWrite; §4 第 2 脚 #4 で測る |
| R1B-19 | P2 | fixed-in-v2 | §3 冒頭と表: 席は kind で記述、a012 は Codex（#456 hold）なので使わず「Claude 席 3」を新 worktree に、a011 は anchor 専任、X-1 は a008、X-2 は Claude 席 3 |
| R1B-20 | P2 | fixed-in-v2 | §1.2/§1.9/§7「X」: `hcom-seat` は常に操作者が実行（X でも定常でも）、audit 席だけ `omp-run.sh` が herdr 経由で立てる |
| R1B-21 | P2 | fixed-in-v2 | §1.6: merge を拒むのは omp policy の deny（approval）、srt はドメイン単位、GitHub 境界は検知（D-024-21/23）; §9 に残余行 |
| R1B-22 | P2 | fixed-in-v2 | §3 W1 と §6「記録」: `pilot-facts.md` は `.orchestration/validation/025-pilot-facts.md`; facts 2 本は次の boundary PR で `.orchestration/analysis/` へ |
| R1B-23 | P2 | fixed-in-v2 | §1.9: D9 は `hcom list <seat> --json` の usage 項目から boundary 記録に 1 行（W8）、X の 24 時間は手貼り; §4 第 1 脚 #10 で鍵名; §2 の ccusage 行は E3 で捨てる |
| R1B-24 | P3 | fixed-in-v2 | §10.1: B-2 は W1 の確認後の amendment 1 本だけ行う |
| R1B-25 | P3 | fixed-in-v2 | §2 残す行: `replay.sh:15` のコメント例示 1 件を除き 0、E2 で消える |
| R1B-26 | P3 | fixed-in-v2 | §1.7/§2/§3 W6: 呼び出し元は 6 本（`codex-review.sh` と `author-loop.sh` を含む） |
| R1B-27 | P3 | fixed-in-v2 | `.claude/hooks/*.ts` → §4 第 2 脚 #7 の植え付け; TMPDIR → #4b; `agent.db` schema → 第 1 脚 #4b; handoff 配送下 → §9「測らない、X の 24 時間で記録」 |
| R1B-28 | P3 | fixed-in-v2 | §6 anchor 項: `classes.yaml` に `unmeasured-tool-claim` を次の boundary PR で |
| R1B-29 | P3 | fixed-in-v2 | §7: E1/E2/E3 の各 merge 直後の `make update` 行、「omp を閉じて」を config.yml を書く apply 全部（B-1、B-3/C-2'、E）に |
| R1B-30 | P3 | fixed-in-v2 | §2 project-map 行と §9: DoD12 は J9 で waive（既定）、subagent 相当は H 系 |
| R1B-31 | P3 | fixed-in-v2 | §1.5: ai-native-platform との往復は X 後は操作者経由の手貼り |
| R1B-32 | P3 | fixed-in-v2 | §1.2: shim の固定 path `~/.agents/srt/bin/omp`（chezmoi 描画、どの役割の allowWrite にも含めない） |
| R1B-33 | P3 | fixed-in-v2 | §9: hcom store は同一 UID 共有、証跡 of record は貼り付けと GitHub |
| S-01 | P0 | fixed-in-v2 | §1.3 表: worker/orchestrator/audit の `denyWrite` に `~/.hcom/{env,config.toml,config.env,scripts,integrations}`（worker/audit は `.tmp/launch` も）; §4 第 2 脚 #2/#4（この deny の下で `listening` と配送が動くか、`hcom.log`）; §1.3 本文に「実行入力」の説明 |
| S-02 | P0 | fixed-in-v2 | §1.1/§1.2: 役割 = omp `--profile <role>`、各役割の allowWrite は自 profile dir だけ; §1.4(b): policies は `~/.agents/omp/policies/`（B-2 のパス移動、§5）; §1.8: hook は `~/.agents/omp/hooks/` から `-e`; §1.9/§7: 役割 profile の認証（`auth export/import`）; 残余「自役割の `agent.db` は読める」は §9 |
| S-03 | P0 | fixed-in-v2 | §1.3 表: `allowUnixSockets` は役割別、worker/audit は `[]`; §2 B-3 行: manifest `claude.sandbox` の流用ではなく役割別 `srt.<role>` 節に構造変更; §4 第 2 脚 #4（socket 無しで `listening`）、#8 |
| S-04 | P0 | fixed-in-v2 | §1.3 表: 全役割 `denyWrite: ~/.local/share/uv/tools`; §2 A-2 行: doctor が srt・omp・hcom・node の realpath がどの役割の allowWrite にも無いことを検査、B-3 の render テストで固定 |
| S-05 | P1 | fixed-in-v2 | §1.1/§1.7: 監査は herdr の下に立つ席（`omp-run.sh` → `hcom-seat audit` → `hcom events --idle` → `kill`）、orchestrator の sandbox の子ではない; §4 第 2 脚 #9 の入れ子 probe と #4/#7 の `ps` 祖先; fallback（操作者が統合ごとに `hcom-seat audit`）を #9 と §9 に |
| S-06 | P1 | fixed-in-v2 | §1.3 表: 役割別 `denyRead`（`~/.ssh`、`~/.aws`、`~/.netrc`、`~/.npmrc`、`~/.codex`、`~/.claude`、`~/.omp/agent`、他役割の profile、`~/.hcom/config.toml`、audit は `~/.config/gh` も）; §4 第 2 脚 #5 の読取 canary; §9「読取の残余」3 項; 環境は S-18 の `env -i` で絞る |
| S-07 | P1 | fixed-in-v2 | §1.3 audit 行: 網は provider ホストだけ、trustd 無し、binding false; §1.7: cwd は空 scratch、checkout は絶対パス、植え付け試験; §4 第 2 脚 #7; §9 に provider エンドポイントの残余 |
| S-08 | P1 | fixed-in-v2 | §1.2: shim に絶対パスを焼き込み、起動後に runner の `--hcom-tool-path` を照合し不一致で `kill` + exit 2、席 canary を最初の PONG で、`check-regime-boundary.sh` が `sandbox-exec` 祖先を辿る; §3 W5 C-2' の Behaviour 3 行 |
| S-09 | P1 | fixed-in-v2 | §1.3: `allowLocalBinding` は `false` で先に測る; §4 第 2 脚 #4（false で `listening`、立たなければ true に直して記録）; §9 |
| S-10 | P1 | fixed-in-v2 | §3 W3 D と §2 validator 行: `validate` が repo root の `.omp/`、`.env`、`.env.*` を拒む 1 関数 + fixture（`.omp/hooks/pre/x.ts` で赤）; orchestrator 席の cwd は main checkout なので PR + この検査が境界 |
| S-11 | P2 | fixed-in-v2 | §2 A-2 行と §3 W3: pin に `integrity`/`shasum`/attestation、`--ignore-scripts`、`npm audit signatures`、依存木 receipt と doctor 比較、`min_release_age` の理由行 |
| S-12 | P2 | fixed-in-v2 | §1.2/§1.3: hcom-seat が役割別 `CLAUDE_CODE_TMPDIR`（worker `<worktree>/.tmp`、audit `<results>/tmp`、orchestrator `.agents/worklog/tmp`）; §4 第 2 脚 #4/#4b; §9 に `/tmp/claude` 共有の残余 |
| S-13 | P2 | accepted-residual | owner: X-2（W6）。J-N2 の一覧は D-024-97 の 3 本のまま（§6 C-80、§7）; 除外中は `chain-integrate.sh` の鎖全体が sandbox 外で走る残余を §6/§9 に明記し、X-2 merge 直後に外す行を §7 に追加。葉だけの除外（`--skip-codex`）は短命の暫定に機構を足さないため採らない。測るコマンド: `jq .sandbox.excludedCommands .claude/settings.local.json` が X-2 後に `[]` |
| S-14 | P2 | fixed-in-v2 | §3 W2 C-1（seam の fixture テスト）、W6b（drill）、W7（rollback の前提: C-1 merge 済み、E1 未着手、旧席と旧 pane を残す）、§8「X」; X-1 の完了条件に「kill → `--resume <id>` で続きが読める（未検証、live は X）」 |
| S-15 | P2 | fixed-in-v2 | §4 冒頭: 原本は `.orchestration/validation/025-pilot-facts.md`（scan 対象）、貼る前の `sed` マスクと `ps` の `cut -c1-200`、`--mask-secrets` を通す; §6「記録」 |
| S-16 | P2 | fixed-in-v2 | §1.3 表: trustd は worker/orchestrator だけ、audit は無し（第 2 脚 #7 で Bun の TLS を確認）; §9 に OCSP/AIA の残余 |
| S-17 | P2 | fixed-in-v2 | §1.3: `allowPty` は `false` で先に測る; §4 第 2 脚 #5 に `pty: true` の bash 呼び出しと fallback 文言; §9 |
| S-18 | P2 | fixed-in-v2 | §1.2: hcom-seat は `/usr/bin/env -i PATH=… HOME=… LANG=… HERDR_SOCKET_PATH=… CLAUDE_CODE_TMPDIR=… [ANTHROPIC_API_KEY=…] hcom omp …` で起動し渡す名前を Behaviour 表に列挙; §4 第 2 脚 #4b で席の環境名一覧 |
| S-19 | P2 | fixed-in-v2 | §1.9/§7: `omp login anthropic` で API key を store に入れられるかを第 1 脚 #4b（`omp login --help; omp auth --help`）で確かめ、可能なら env に置かない; 不可能なら hcom-seat の環境で orchestrator 役割だけに渡す（§7「X の直前」） |
| S-20 | P3 | fixed-in-v2 | §4: `$PILOT=$HOME/pilot-20261022` に統一、`PILOT_LOG` を export、`mkdir ~/.agents/srt` を削除（B-3 の `make update` が作る）、第 2 脚 #10 の片付け（`hcom kill`、`kill %1`、worktree と profile の削除、canary の確認）、deny canary は `--repo github.com/mryfmo/does-not-exist` |
| S-21 | P3 | fixed-in-v2 | §4 第 1 脚の前書き: sandbox 無し・yolo・操作者権限、#14 を最後にし終わり次第 #16 |
| S-22 | P3 | fixed-in-v2 | §1.3 本文: 暗黙に書ける場所（`/tmp/claude`、stdio、`~/.npm/_logs`、`~/.claude/debug`） |
| S-23 | P3 | fixed-in-v2 | §2 A-2 行: `check_sandbox_runtime` の恒久 probe 2 本（`curl example.com` が非 0、`touch ~/.agents/.doctor-canary` が失敗） |

## 判断の要約（v2 で取った選択）

1. omp/hcom の状態は実行入力（S-01/S-02/R1B-18）: 役割 = omp `--profile`、allowWrite は自 profile dir、hcom の実行入力は denyWrite、srt 設定・shim・policy overlay・stop-gate は `~/.agents/{srt,omp}/` に chezmoi が描画（どの席も書けない）。
2. herdr socket と uv tools（S-03/S-04/R1B-05）: worker/audit は socket 無し、全役割で `~/.local/share/uv/tools` を deny、socket は orchestrator だけ（席の起動と project-map hook）。
3. 入れ子（S-05/R1B-06/R1B-03）: 監査は herdr の下に立つ席（`omp-run.sh` → `hcom-seat audit`）、cwd は空 scratch、植え付け fixture; 入れ子 probe は第 2 脚 #9、fallback は操作者が `hcom-seat audit` を打つ操作者行。
4. C-1 と rollback（R1B-01/R1B-02/S-14）: seam `bus: agmsg|hcom`（既定 agmsg）を C-1 の測定済み amendment で戻し、X-0 に drill、rollback は `bus: agmsg` + 旧 pane の再開。代替（C-1 の merge を X-0 まで持ち越し `git revert`）は §9。
5. SKILL（R1B-04）: `hcom-orchestration` は X-1 に、agmsg 系 skill は役割別 `--skills` で X 時点から除外、E2 で削除。
6. パイロット（A-01..A-06、R1B-14..16、S-15、S-20）: 第 1 脚 17 + #4b/#11b、第 2 脚 10 行（`srt --debug`、絶対パス、shim は denyWrite 内、`--` probe、`session_stop` block、push/PR、auditor 席形 + 植え付け、orchestrator 形、入れ子 probe、片付け）、原本は `.orchestration/validation/025-pilot-facts.md`。
7. 供給網と CI（S-06/S-07/S-09/S-10/S-11/S-12）: 役割別 denyRead、binding/pty は false 先行、役割別 TMPDIR、`.omp`/`.env` の CI 拒否（D）、A-2 は integrity + attestation + `--ignore-scripts` + 依存木。
8. 棚卸しと儀式（R1B-07..13, 17, 19..23, A-03/07/08, S-13, S-16..23, P3）: 残す 10 / 変える 18 / 捨てる 12 / 新規 7、DoD5 の 67 ファイルを E1/E2/E3 に割付、160 行 cap（Checks 込み）、`allowed_files ≤ 8` は手で、席は kind、`hcom-seat` は操作者、D9 は `hcom list --json`、J-N2 は D-024-97 の 3 本で X-2 後に除去。
