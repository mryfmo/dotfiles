# Plan 025 review round 6: dispositions (v7)

- 対象: `.orchestration/plans/025-regime-cutover-plan.md` v6（sha256 prefix `3524e70d`、327 行）への round 6 の審査 2 本: verification P-01..P-06（`025-review-r6-verification.md`）、red team と handout 机上実行 Q-01..Q-21（`025-review-r6-redteam.md`）= 27 件（D-024-115）。処分は orchestrator の決定を転記したもので、本ファイルは再決定しない。
- 処分の語: `fixed-in-v7` = v7 の該当節に反映、`residual` = owner と測り方を名指しして残す、`handout-only` = 別文脈が `.agents/worklog/orchestrator-glue/pilot/*` を直す（本ファイルは意図した直し方と file 手順を書く; handout 側は同じ一覧を受け取る）。
- 手順の指し方は番号と名前（第 1 脚 #n、第 2 脚 #n）。資格情報を扱うコマンド行と settings の JSON は貼らない。
- 結果: v7 は 335 行、sha256 prefix `3496490d`。集計は末尾。

| id | priority | disposition | one-line how |
| --- | --- | --- | --- |
| P-01 | P2 | fixed-in-v7（§1.3 orchestrator 行、W5a） | §1.3 orchestrator 行の denyWrite に `<main>/.claude/settings*.json`・`<main>/.claude/contextdb`・`<main>/.env.*` を足し、W5a の render テスト行に同じ 3 項（`.env.*` glob の効き目は【未測】、第 2 脚の orchestrator JSON で測る）; pilot の `srt-orchestrator.json` は handout 側（18 項、placeholder 形で反映済み） |
| P-02 | P2 | fixed-in-v7（W3 完了条件、§2 A-2 行、§7 A-2 merge 直後と X 手順 5b 行） | doctor の system `credential.helper` 検査は W0b（X 手順 5b）前は warning で exit に効かず、W0b の記録 PR で failure に切り替える（manifest の 1 鍵）; §7 A-2 行の期待に「warning 1 行で失敗ではない」 |
| P-03 | P3 | fixed-in-v7（§4 第 2 脚 #7） | prompt 要約を forbidden 4 本（`$PILOT` 直下、`review`、`out/cwd`、Q-11 の `seat-audit/forbidden.txt`）に、期待を「4 つの forbidden が無い（`out/cwd` は M-01 の直接の測定）」に; handout `leg2.md` #7 と一致 |
| P-04 | P3 | fixed-in-v7（§1.3 audit 行 network 欄） | 「anthropic 側は `M` が anthropic のときは #3b で確定、openai-codex のときは review 席の #3b 再試行で確定」の 1 句 |
| P-05 | P3 | handout-only（`leg1.md` #0a `wait_result`、#12） | LIKE pattern を `%task_id=$1 %`（空白終端）にするか `wait_result` を `pilot-001`/`pilot-001t` の 2 回に分ける（Q-17 と同じ直し）; 計画に変更無し |
| P-06 | P3 | handout-only（`leg2.md` #5 の 15、#10） | 15 の標的を `pilot-should-fail-15` にし #10 の `ls` に足す; 計画 §4 #5 の 15 は file 名を持たないので変更無し |
| Q-01 | P0 | fixed-in-v7（§3 新行 W0c、§9 新行と決定 (10)、§8 STOP、§11 #21、§2 workflow 行、§6、§7） | W0c = `dotfiles-T133-ci-secrets-push-only-a01`（trust-boundary、`threat_table`、Codex `security` profile、`allowed_files` = `macos.yaml`・`ubuntu.yaml`・`Makefile`）: `HAS_PRIVATE_DOTFILES_KEY` を secret の存在 かつ `github.event_name == 'push'` に、完了条件 = PR run で skip step 実行・ssh-agent skip、merge 後の main の push run で private 統合（run URL 2 本）; 帰結（後続 `dotfiles-T133-ci-public-path-a01` まで PR は skipped-private 経路、`install/**` は push run と `private-bootstrap.yaml`）を §3/§9 に、決定 (10) 既定 A／代替 B（environment + required reviewers、Q-06 class）／代替 C（公開経路 task 先行）; `.github/workflows/**` は §1.6 に既存; §8 に「key が `pull_request` に積まれる間は worker PR を dispatch しない」; 性質 = 以前からの性質、round 6 red team が発見。注: D-024-115 は決定 (8) と呼ぶが、v6 に (8)(9) が既にあるので (10) に置いた |
| Q-02 | P1 | fixed-in-v7（§1.6、§1.9、W3、W6a fixture） | §1.6 に `executable_herdr-agents`（E1 で `agmsg-bootstrap` が消えるまで）と一般則「Makefile の target が pull した木から実行する全パス」; 停止は `update-tree` の先頭 = 末尾の `agmsg-bootstrap` より前なので並べ替え不要と §1.9 と W3（停止の owner）に明記 |
| Q-03 | P1 | fixed-in-v7（§1.6、W6a、§11 #21） | §1.6 を subtree 単位に: `home/dot_claude/**`、`home/dot_codex/**`、`home/dot_agents/**`、`home/dot_local/bin/**`、shell 起動 5 file + `home/dot_bash/**`、`home/dot_config/{sheldon,zsh}/**`（fish は無い【実測】）、`home/dot_mise/**`、`home/Library/**`、`install/**`、`scripts/lib/**`、`Makefile`、`.github/workflows/**`、repo の `.claude/**`; `modify_*`/`run_*`/`create_*` と template 関数の項は維持; 正本 = `scripts/orchestrator/protected-paths.txt`（W6a 新設、`chain-integrate.sh` が読み W5b/W5a のテストが参照）を §1.6/§3/§11 が指す |
| Q-04 | P1 | fixed-in-v7（§1.6、W6a fixture） | 検知を `git diff --no-renames --name-only <base40>...<head40>` + template パス（`*.tmpl`、`.chezmoitemplates/**`、`.chezmoiscripts/**`）の `<head40>` 全文（`git show`）の語一致（`output`/`exec`/`lookPath`/`include`/`includeTemplate`/`joinPath`、pipeline と `{{-` を区別せず）に; template パスへの改名・新規は内容を問わず保護; 回避できた理由（rename 検出で `+` 行 0、pipeline 形）を 1 句; W6a に 2 PR fixture |
| Q-05 | P2 | fixed-in-v7（W0c `allowed_files`、§2 Makefile 行） | `UV_PYYAML` に `--no-project`; `Makefile` は C-1 の `allowed_files` に無い【実測】ので W0c に同乗（W3 とは直列） |
| Q-06 | P2 | fixed-in-v7（§1.9、§7 見出し、W3、§2 Makefile 行、§11 #20） | 停止を 2 段に: 先に source 側 `git log --oneline <old>..<new>` と `git diff --stat <old>..<new>`、次に `chezmoi diff` と計画; 期待形「commit 一覧が名指しの PR の squash だけ、stat がその file だけ、その後に描画差分」; 名指しに無い commit があれば `CONFIRM=1` を打たない; W3 に出力形の fixture 1 本 |
| Q-07 | P2 | fixed-in-v7（§1.7 (4)）+ handout-only（`leg2.md` #7 prompt） | `omp-run.sh` は `<results dir>` を再利用せず、再試行は `<results dir>-r2` と新しい私設 store `<HCOM_DIR>-r2` に nonce を作り直して立てる; 測定は handout `leg2.md` #7 の audit prompt に `out/cwd` → `out/cwd2` の改名 1 項（期待 = 拒否、`out/cwd2` が無い）で、§4 #7 の期待にも書いた（orchestrator の指示文は「#5 item 17」だが handout 側は #7 prompt に置いた、と handout 文脈から受領） |
| Q-08 | P2 | residual（owner = 第 2 脚 #8; 測定 = `HCOM_LAUNCHED=1` を export した内側の `hcom omp` と runner の `--hcom-tool-path`） | §4 #8 に測定と合格基準（pilot3 の runner が `$PILOT/seat-audit/omp` を指す）、§9 に不合格の帰結: hcom が文書化する挿入点は起動側 process の PATH で先に見つかる shim だけで設定の tool path は無い【srt Q2】ので、`omp-run.sh`（`hcom-seat` 経由）が `hcom omp` を打つ process の PATH 先頭に `<seat dir>/bin` を置いた環境を作り直して runner が shim を指すまで X を block; S-08 (1) は検知で代替にならない。注: 機構の出所は `srt-facts.md` Q2（`b2-c2-facts.md` には無い） |
| Q-09 | P3 | fixed-in-v7（§1.7 (6)） | 「usage は記録であって上限でも verdict でもない、上限は provider の spend limit（§1.9 D9）」の 1 句; `find … \| sort \| head -1` は handout 側 |
| Q-10 | P3 | fixed-in-v7（§1.9） | 鍵の経路の残余 (a)「`omp auth import` の stdout が鍵を echo するかは【未検証】、第 1 脚 #6b で pane 出力を目視し `tee` に入れない」の 1 句; `sk-ant-` の `grep -c` = 0 の前置きは handout 側 |
| Q-11 | P3 | handout-only（`leg2.md` #7 prompt） | audit 席 shim の canary `touch …/seat-audit/forbidden.txt` を prompt に 1 項（期待 = できない）; §4 #7 の要約と期待にも 1 句 |
| Q-12 | P2 | handout-only（`leg2.md` #7 読み取り） | `ANAME` 取得と `ANAME-EMPTY` 判定を独立行にし、空なら `hcom events`/`hcom kill ""` に進まず「`HCOM_DIR=… hcom list` を貼って止まる、席は `hcom kill tag:pilot-audit` で畳む」; 計画に変更無し |
| Q-13 | P3 | handout-only（`leg1.md` #10） | `NAME-EMPTY` の行で `hcom list --json \| head -c 1500` も出す; 代替は `sqlite3 -readonly` の `instances` から `tag='pilot'` の最新行 |
| Q-14 | P3 | handout-only（`leg1.md` #15、#18）+ §4 の同期 | #15 の fallback 分岐を消し「空なら測れなかった」だけ残す、#18 の 1 項を外す; 計画 §4 第 1 脚 #15/#18 の「fallback path」の句も同じく削除（`/tmp/claude/events.log` の字面は計画に無かった） |
| Q-15 | P3 | handout-only（`leg1.md` #5） | regex の各語の後ろに `([ =,]\|$)` を置き `--mode` が `--model` の行に当たらないように |
| Q-16 | P3 | handout-only（`leg1.md` #6b、`leg2.md` #3b） | login 行を `IMPORT_EXIT` が 0 でないときだけに、`M=anthropic/…` も 0 のときだけに（ブロック貼りで `M` が上書きされない） |
| Q-17 | P3 | handout-only（`leg1.md` #0a、#12） | pattern を `task_id=$1 %`（空白終端）に（P-05 と同じ直し） |
| Q-18 | P3 | handout-only（`leg2.md` #8 gate） | `where tag='pilot2' and pid is not null order by created_at desc limit 1` にし、`[ -n "$wpid" ] \|\| echo WPID-EMPTY` を先に; 計画に変更無し |
| Q-19 | P3 | handout-only（`leg2.md` #0） | 期待文を「path に `shims`/`mise` を含まないこと（種別は参考）」の順に; 計画に変更無し |
| Q-20 | P3 | handout-only（`leg1.md` #17） | fallback 条件を `[ "$TX" -eq 0 ] && [ -s …/transcript.txt ] \|\|` に（exit 0 で空出力も fallback） |
| Q-21 | P3 | handout-only（`leg2.md` #5 item 16） | 期待文に「16 が通ったら RESULT は pane で読む」の 1 句 |

## 集計

- fixed-in-v7: 13（P-01 P-02 P-03 P-04 Q-01 Q-02 Q-03 Q-04 Q-05 Q-06 Q-07 Q-09 Q-10; Q-07 は handout 側の測定 1 項も持つ）。
- residual: 1（Q-08、owner = 第 2 脚 #8、合格基準は §4 #8、帰結は §9）。
- handout-only: 13（P-05 P-06 Q-11 Q-12 Q-13 Q-14 Q-15 Q-16 Q-17 Q-18 Q-19 Q-20 Q-21; Q-11/Q-14 は §4 の要約にも同期）。
- rejected: 0。operator-decision: Q-01 は §9 の新設決定 (10) に既定 A と代替 B/C を置き、採択の決定行で閉じる。
- 計画側の数の変更: §2 は 50 行（残す／変える 2）、§9 は 10 決定、§11 は 21 行、§6 の `security: true` 本文は 6 本（W0c を含む）、§3 に W0c 行。
