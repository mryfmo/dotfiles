# Plan 025 v4 — round-4 review, perspective J (verification)

- 対象: `.orchestration/plans/025-regime-cutover-plan.md` v4（sha256 prefix `33285429`、`shasum -a 256` 実測 `332854296e52…`、325 行）。読み取り専用（Read/`sed`/`grep`/`jq`/`python3 -I`/`shasum`/`wc`/`awk`/`git grep` のみ。omp/hcom/herdr/gh/npm/srt/`log` は実行していない。席も store も触れていない）。書いたのは本ファイル 1 本。
- 読んだもの: v4 全文、`025-review-r3-dispositions.md`（80 行）、`025-review-r3-{redteam,dryrun,consistency}.md`、handout 7 本、`srt-facts.md`、`decisions.tsv` D-024-01/02/18/21/22/22a/23/79/81/82/85/86/87/88/88b/89/90/91 と D-024-92〜107、4 本文の front matter と amendments、`scripts/{update-agent-assets.sh,validate-agent-assets.py}` の該当行、README の ruleset payload、manifest の `worker_cap`/`allowedDomains`。
- 記法: `~` = ホーム。`<main>` 等は v4 の語。行番号は v4 の `cat -n`。

## 1. Dispositions

**fixed-in-v4（74 + round 2 の部分 4 = 78 行）**: 全行について名指しの節（または handout）に本文を見つけた。欠落 0。部分・矛盾は次の 3 行だけ:

| id | 節 | 何が足りない／矛盾するか |
| --- | --- | --- |
| I-04（P2） | §1.2 shim、§1.7 中身一覧、handout `leg2.md` #7 | 本文は「audit 系 `<results dir>/srt-debug.log`」と書くが、同じ段落の shim 式 `2>><役割の tmp>/srt-debug.log` は audit では `<results dir>/tmp/srt-debug.log` になる。handout はその式どおり `out/tmp/` に書き、読み取り行は `out/srt-debug.log` を読む（J-01） |
| I-08（P1） | §3 X 手順 0、§7「X 手順 0」 | `<main>` 側の `update_hcom_private` 行と実パスは入ったが、順序が C-1 の squash merge の**前**。`update_hcom_private` は C-1 amendment 2 の新 target で main に無い（`grep update_hcom_private scripts/update-agent-assets.sh` → 0 件）。§1.5 は merge を先に書く（J-02） |
| I-02（P2） | §1.2 署名、§3 X 手順 2 (a)/5、§7 | 5 役割の署名は入ったが、worker の `<dir>` 既定 `<seats root>/<name>` の `<name>` を渡す引数が無い。§3/§7 は `hcom-seat worker rehearsal-1`／`hcom-seat worker <name>` と名を渡す（J-04） |

そのほか全行は一致（§5 に id 列挙）。shim の HCOM_* 7 名（G-18/H-28）、`/usr/bin/log`（H-09）、#3c の clone 先行（H-02）、5 配列の srt 設定（H-01）、`OMP_PROFILE=` 形（H-11）、`kill -0` 不使用と errno probe（I-09/F-12）、`launch_ts=+%FT%T` と lookback の句（I-17/V-18）、`git revert <sha>`（I-19: 本文に `-m 1` は 0 件）、update-branch の禁止（I-07: 全出現が否定か conflict 限定）、placeholder 5 つ（I-03/E-08）、`find … -name '*.jsonl'`（I-22）、§11 全 20 行の既定（H-31）を個別に確認した。

**operator-decision（G-01）**: §9 決定 (5) に既定（§1.10 の形 = file store + machine account の token 2 本 + ruleset approval 1）と代替 B（P0 残余の受容）・C（fork 流）がある。§3（W0 行、X の依存「W0、X-1、X-2 merge」、手順 2 (f)）と §7（W0 (1)〜(4)、X 手順 2 の (f)）は既定で書かれている。ただし W0 の**時期**が W2〜W6 と両立しない（J-03）、W0 (c) の `require_last_push_approval` が conflict 時の update-branch と衝突する（J-06）。

**residual（G-19）**: §9 行「自席 pty への端末エスケープ」に owner = X 手順 6 の 24 時間観測がある。測るコマンドは処分表の宣言どおり無し（「pane の異常表示を記録」）。処分表の宣言と一致。

**処分表の集計**: 76 件 = fixed 74 / residual 1 / rejected 0 / operator-decision 1、優先度別 P0 3+1 / P1 27 / P2 22 / P3 22+1 は表の行数と一致。Status log v4 の id 集合も表と一致。`decisions.tsv` D-024-106 の「82 rows, 4 operator-decision rows」だけが表（80 行、operator-decision 1）と合わない（J-21）。

## 2. Whole-plan consistency

**役割と profile**: 5 役割（orchestrator=deep/anthropic、worker=standard/anthropic、audit=audit/openai-codex、review=review/anthropic、security=security/openai-codex）は §1.1 表、§1.9 の認証先（`login openai-codex` = audit/security、file import = orchestrator/worker/review）、§7 B-3 行、§9「読取の残余」行で一致。template 3 本 × `__PROFILE__` は §1.1/§1.2/§2/W5a/§7 で一致（§1.2 の「role template `~/.agents/srt/<role>.json`」だけ review/security では `audit.json` を指す、J-14）。席数 4（a008/a009 Claude、a011 anchor、a012 Codex）は §3 前文・§5・§9 で一致、manifest `worker_cap: 4`【実測一致】。資格情報: `GH_CONFIG_DIR` は orchestrator shim = `~/.omp/profiles/orchestrator/gh`、worker shim = `~/.omp/profiles/worker/gh`、reviewer store = `gh-reviewer`（§1.10、§1.2、§7 W0 (2)(3)）で一致; audit 系は `~/.config/gh` を denyRead し `GH_CONFIG_DIR` を持たない（意図どおり）。

**パス**: `<seats root>`（manifest `srt.seats_root`、既定 `<main>` の親の `seats`）§1.1/§2/W5a/§6 item 3 一致; `<seat dir>` = `<main>/.agents/worklog/srt-seats/<name>/` §1.2/§9 一致; shim `<seat dir>/omp` と template `~/.agents/srt/omp.shim` §1.2/§1.4/§2/W5a/§7 一致; settings `<seat dir>/settings.json` 一致; policies `~/.agents/omp/policies/<role>.yml` と source `home/dot_agents/omp/policies/` §1.3/§1.4/W2c/§7 一致; `<results dir>` = `<main>/.agents/worklog/omp-run/<task id>-<head40>/` と中身（`cwd/ sessions/ tmp/ out.last.md srt-debug.log transcript.txt`）§1.7、worker denyRead、§6 item 5 一致; `HCOM_DIR=<main>/.hcom-audit/<task id>-<head40>` §1.7 (0)/§1.3/§2 `.gitignore`/worker denyRead/§6 item 5 一致。**不一致 1 件**: audit の `srt-debug.log` の置き場（§1.2 の式 vs §1.2 の文・§1.7、J-01）。worker（`<seat dir>/tmp/`）と orchestrator（`<main>/.agents/worklog/tmp/`）は式と文が一致。

**X の順序と X-0**: X-0 = C-1 の squash merge + `<main>` の `update_hcom_private` + `<canonical>` の `make update`、rollback = `git revert <sha>` は §1.5/§3/§7/§9/§11 #16 で同じ集合。ただし手順の**順**が §1.5（merge 先）と §3・§7（`update_hcom_private` 先）で違い、§3/§7 の順は main に無い関数を呼ぶので実行できない（J-02）。orchestrator 先（手順 4）→ worker（手順 5）は §3/§7/§9/§11 #15 で一致。

**J-N2**: 投入は §7「今」の jq 1 行、除去は X 手順 4（§3、§6 C-80、§7、§9、§10.3、§11 #17）で一致。§11 #17 が「D-024-97『X-2 merge 直後』」と引くが D-024-97 の本文に除去時期の語は無い（J-21）。X 手順 2 (b)「Claude 席から `omp-run.sh --role audit`」は J-N2 の 3 本に `omp-run.sh` が無いので `chain-integrate.sh` 経由のときだけ hcom が動く（J-20）。

**stop-gate の上限**: N=3 は §1.8、W6b、§4 前書き（events.ts 仕様）、第 1 脚 #7、handout `events.ts`（`stopN === 3` で `cap`）で一致。

**§2 の数**: 表を数え直し 残す 10（L43-51,53）／残す・変える 1（L42）／変える 16（L54-66,68-70）／捨てる 13（L67,71-82; うち書換 L81・昇格 L82）／新規 8（L83-90）／混合 1（L52）= 49 で本文と一致。【実測】の再計測: agmsg 参照 67 ファイル、test module 19、`herdr-agents` 2292 行、rules 12 本、未追跡 glue 41 本、manifest `allowedDomains` 7、`scripts/orchestrator/` に `verdict.sh`/`audit-pool.sh`/`result-precheck.sh`/`handoff.sh` 無し、`.claude/hooks` は `.py` 4 本のみ、repo root に `.omp`/`.env`/`.agents/skills`/`.agent`/`.claude/extensions` 無し、masker は `ghp_`/`github_pat_` のみ、README の `dismiss_stale_reviews_on_push: true`・`required_approving_review_count: 0`・`require_last_push_approval: false`・`strict…: true`（古い値、E-01 どおり）— すべて本文と一致。

**§5 と 4 本文の記録**: B-1 = allowed_files の 1 行目が manifest、`after: []`、draft #406、amendment 2 まで（「anchor 済」と整合）。C-1 = `dispatch_status: blocked-pre-anchor`、`after: [dotfiles-T133-gh-binding-a02]`（W2b「dispatch 時に `after: []` と `dispatch_status` を更新」と整合）、manifest は allowed_files の 10 番目、本文に `thread` 0 回【実測一致】、amendment 1〜3 あり（amendment 2 = `update_hcom_private`、3 = lint baseline）。B-2 = `after: [B-1]`。C-2 = `after: [C-1]`、amendment 3 が「C-1 amendment 3 の reply-route fixture」を引くが C-1 の amendment 3 は lint 行で `thread` 0 件 — §5 が C-2 を破棄する理由（bus 契約の未測定）と合致。

**§11 と決定**: #2 D-024-82 (2)（J7 = 8 allowed_files・C-80 2 round）一致; #3 D-024-79（frozen-superseded-by-phase-2）一致; #9 D-024-87/81 一致; #13 D-024-89（cutover checklist）一致; #14 D-024-01/02 一致; #18 D-024-22a（not-applicable-on-one-macos-user）/D-024-23 一致; J-L の既定 = D-024-85「waive both counts for #456 only」= 「A 免除して merge」一致; #17 は J-21。

**定義前の語**: `<name>`（§1.1、定義無し）、W5a/W5b（§1.2、定義は §3）、C-2'（§2 L66、定義は §3/§5）、J-N2（§3 W2a、字面は §7）、J-P（W2b、gloss 無し）、`<base40>`（§1.6）— J-10。`<seat dir>`/`<results dir>`/E1〜E3/X-0 は前書きか初出節で閉じている（I-15 の直しは有効）。

**W0 と進行中の席**: W0 は「全項目と並走」（§3 前文）で §7 は (1)〜(4) を W1 直後に置くが、(3) は keychain の項目を消し、(4) は approval 1 を要求する。今日の全席（a008/a009/a012、Claude orchestrator）は keychain の token で push/`gh` を通し（H-25 の実測: `credential.helper = !gh auth git-credential`、keyring）、`GH_CONFIG_DIR` は X 後の shim だけが渡す。したがって (3) の直後から W2〜W6 の席は push も PR も出せず、(4) の直後から X 前の PR（操作者 identity が author）は操作者 account では approve できない（§1.10 は reviewer store を boundary PR にしか割り当てない）— J-03。

## 3. Handout agreement

in progress

## 4. Findings

in progress

## 5. Confirmed rows and agreeing files

in progress

## 6. Report

in progress
