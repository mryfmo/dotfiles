# Plan 024 設計 2/5: 第 2 段階の PR A〜H と切替 X（各項目: 目的 / やること / 順番と前提 / 完了条件 / リスク / ユーザー）

> 読む時機: 第 2 段階のタスク文を書くとき。1 項目ずつ読めばよく、依存は「順番と前提」の行にある。

## 4. 本体: PR A〜H と切替（各項目: 目的 / やること / 順番と前提 / 完了条件 / リスク / ユーザーが必要なこと）

### A. 資産固定（済み、仕上げのみ）
- 目的: omp と hcom を固定版で `make update` から入れる（方向性 1・4）。
- やること: #398（hcom wheel を uv の receipt が指す場所に置く）と #405（dangling `~/.local/bin/omp` の除去、wheel 固定の hcom を `uv tool upgrade` が飛ばす件）をマージ。spark では `make update` を切替（第 4 節 X）で実施。
- 順番と前提: Wave 0〜1。前提なし。
- 完了条件: `make doctor` が omp 18.11.3 と hcom 0.7.30 を報告（DoD1）。`make update` を 2 回続けて実行しても差分 0。
- リスク: `make update` の herdr 更新がサーバーと不整合（08:1x に 0.9.5 へ更新済み。サーバー再起動の有無は X で確認）。
- ユーザー: なし。

### B. omp 設定を manifest から生成（最優先）
- 目的: 役割別モデルと provider、rules、skills、hooks、監査役・レビュー役の omp 実行を dotfiles から生成し、`.claude`/`.codex` の生成を段階撤去する（方向性 1・2・5）。
- やること（タスク `dotfiles-T129-omp-config-render-a01`、a009）: (1) 41da91ce を push し report.md / validation.md を書いて RESULT。中身: `model_profiles.<name>.omp.model` 6 キー（D-omp-model-mapping）、generator と validator と renderer、`omp-config-managed.yml`、`model-profiles.env` 再生成、`home/dot_omp/agent/modify_config.yml`、README 1 行。a009 の item 0 実測（役割 15、reasoning は `:level` 接尾辞、omp は `config.yml.lock` 下で書き換えるが未知キーは保持、エイリアス表なし、apply 側 python3 に PyYAML 無し）を validator の前提に写す。(2) stage 2（新タスク a02）: omp の hooks と permission を manifest から描画する。要件: 生の `gh pr merge|create|update-branch|edit|api` は `scripts/orchestrator/` の統合スクリプト経由以外を拒否、文脈 600k 超で handoff 強制、Stop 相当のゲート（S1 revise で `re-plan:` 行が無ければターンを終えられない）、project-map の reload hook。omp の hook は docs/hooks.md（2026-10-18 取得）で確認済み: TypeScript/JS モジュールを `~/.omp/agent/hooks/pre/*.ts`（または `<cwd>/.omp/hooks/pre/`）に置き、default export の factory が `pi.on(...)` で登録する。`tool_call` ハンドラが `{ block: true, reason }` を返すと実行が止まり、ハンドラが throw しても fail-closed で止まる。イベントに `session_before_compact`、`turn_start` / `turn_end`、`agent_end`、`context` があるので、gh 書込の拒否は `tool_call`、文脈 600k の handoff は `session_before_compact` と `context`、Stop ゲート相当は `turn_end` で実装する。item 0 では導入済み 18.11.3 でこの 3 点を実測してから書く（security: true、脅威表必須）。(3) stage 3: `.claude`/`.codex` renderer を hooks → settings → ディレクトリの順に外す（E と分担。切替後）。
- 順番と前提: stage 1（B-1）は第 1 段階の空き枠で draft と監査まで前倒し可（execution 0e）、マージは P1-14 の後（validator 系列）、第 2 段階では D-W0。stage 2（B-2）は D-W1、C-2 と並行（ファイルが素: B は generator/validator/templates/dot_omp、C は scripts/orchestrator と hcom-dispatch と herdr-agents）。
- 完了条件: `make render-check` 緑で、Claude と Codex 向けの生成物（settings、config.toml、hooks）の差分が 0（evidence V6。Claude 席が manifest を編集するので監査が確認）。`~/.omp/agent/config.yml` が manifest から再生成され、6 役割の provider が `openai-codex` か `anthropic` のどちらかで、anthropic は `ANTHROPIC_API_KEY` 参照のみ（validator が OAuth 参照を拒否）。stage 2: 生の gh 書込を omp 席から叩くと拒否されるテスト、handoff 強制のテスト。
- リスク: omp の hook/permission API が足りない（→ 拡張の security review）。`config.yml.lock` 下の書き換えと chezmoi の modify が競合（a009 の実測: 未知キーは保持されるので manifest 由来キーだけを管理）。
- ユーザー: stage 1 マージ + `make update` の後に `/login openai-codex`。`ANTHROPIC_API_KEY` を環境へ（`ANTHROPIC_OAUTH_TOKEN` は置かない）。D9 の 1 日上限額。

### C. hcom-dispatch とバス（最優先、B と並行）
- 目的: 送信・履歴・計数・着席を hcom に移し、agmsg を読まない（方向性 3・5）。
- やること: stage 1（タスク `dotfiles-T129-hcom-dispatch-bus-a01`、a008。先に amendment 1 で a008 の指摘 3〜7 を確定: revise は `status=revise` か `verdict=revise`、`check=` は 1 つ、`bus-history.sh --marks` は display form を出す、`tests/unit/test_check_regime_boundary.py` を allowed_files に加える、`hcom-dispatch` の excludedCommands/allow は a02 か operator）: `bus-history.sh`（hcom の read command、schema guard、store 不在は拒否）、`hcom-dispatch`（agmsg-dispatch と同じ引数、`--`、受領確認、1 回だけ nudge）、`dispatch.sh` の送信と revise 拒否 4 条件、`bus-read.sh`、`regime-counters.sh`（RESULT−1 と revise 行の大きい方）。**stage 1 は追加型（evidence V1）**: `bus-history.sh` と `hcom-dispatch` は新規ファイルとして置き、`dispatch.sh`・`bus-read.sh`・`regime-counters.sh` は manifest の `bus: agmsg|hcom`（既定 agmsg、`BUS` env で上書き）で経路を選ぶ。既定が agmsg なので、マージしても agmsg 席で動いている現運用は変わらず、hcom 経路はテストと切替 X のパイロットだけが使う。stage 2（a02、D4 と D8 の要件を含む）: `herdr-agents --add-worker` が `hcom omp --tag <team> --dir <worktree>` で着席し `<run>/<seat>.launch.json`（argv, pid, started_at）を書く、`--attach` の live-arguments 行、seat check が live process と比較、`dispatch.sh` が live process の違う席を拒否、RESULT JSON から受け入れ記録と decisions 行を書く補助、`chain-integrate.sh` のバックグラウンド実行と完了通知、worker 側 hcom hook（S1 revise の `re-plan:` 強制）、`--remove-worker` と `--stale` を hcom の member list で。第 1 段階で作った仕組みの hcom への移植もここ: `result-precheck.sh`（P1-5）の実行を worker 側 hcom/omp hook から呼ぶ、`dispatch.sh --next`（P1-6）の idle 検知を `hcom events --idle <seat> --wait <sec>`（README: "Block until match for scripting"）に差し替える、`integrate-seat.sh`（P1-4）はそのまま（gh/git のみ）、`worker_cap`（P1-7）の強制を `hcom omp` 着席経路に通す。manifest の `bus` の既定を stage 2 で agmsg から hcom に変え（agmsg 経路は 1 リリースだけ残す）、E で seam ごと消す（切替の rollback 経路）。
- 順番と前提: C-1a（新規ファイルのみ）は第 1 段階の空き枠で前倒し可（execution 0e）。C-1b（配線）は P1-13 のマージ後、第 2 段階 D-W0。counters と test は #390 と共有するので #390 の後に rebase。C-2 は D-W1、C-1 のマージ後。
- 完了条件: stage 1: `grep -c agmsg` が 5 ファイルで引数説明と E 注記のみ、fixture store でテスト緑、agmsg store 不在でテスト緑。stage 2: `herdr-agents --add-worker` が `hcom omp` の席を立て、hcom 越しに PING/PONG が `bus-history.sh` に出る（DoD11 の前段）。
- リスク: hcom が `instances` 行を席の終了時に消すので tag で絞ると undercount → 全 store 読みに決定済み。hcom 0.7 系の変化。`~/.hcom` への書込は Claude 席の sandbox が拒む（a008 の指摘 7）→ 切替まで `hcom-dispatch` を agmsg-dispatch と同じ excludedCommands に（a02、Claude 境界なので Codex 席か operator）。
- ユーザー: なし（stage 2 の excludedCommands 変更は権限拡張なので承認 1 回）。

### D. CI と実行時の認証検査
- 目的: Anthropic OAuth の不在と、API キーの非コミットを機械的に保証（方向性 2・5）。
- やること: #389 をマージ → #396（JSON/TOML/YAML を実パーサーで読む）を ready にしてマージ → #404（`sqlite3 -readonly ~/.omp/agent/agent.db` で `auth_credentials` の anthropic/oauth 行を数え、`ANTHROPIC_OAUTH_TOKEN` を拒否、確認不能なら失敗）を B stage 1 の後に rebase してマージ。
- 順番と前提: Wave 0〜2。#396 は a010、#404 は a009。
- 完了条件: DoD4。`make doctor` の runtime が probe を含む。
- リスク: omp の auth store のスキーマ変更（固定版 18.11.3 の `sqlite-credential-store.ts` に根拠あり。版上げ PR で再確認）。
- ユーザー: なし。

### X. 切替（cutover）
- 目的: 席とオーケストレーターを omp + hcom に移し、Claude Code と Codex の席を 0 にする（方向性 1・3）。
- やること: (1) B stage 1・2 と C stage 1・2 のマージ後、`make update`（Mac）。(2) ユーザーの `/login openai-codex` と `ANTHROPIC_API_KEY`。(3) パイロット: Claude 席 1 つを `--remove-worker` → `--add-worker`（hcom omp）で置き換え、小さな実タスク（例: #402 の仕上げ）を hcom 越しに TASK → RESULT → ACCEPTANCE → マージまで通す（DoD11）。(4) 成功したら残り 3 席を順に置き換え、最後にオーケストレーター自身を handoff ファイルから `hcom omp` で再起動（モデルは D9）。(5) 失敗時は manifest `bus: agmsg` に戻し、agmsg 席で続行（C の rollback 経路）。(6) spark: `make update`、`hcom relay`（D11）、`herdr machine add spark-9e8d`、2 席目（D10 で上限 6）。
- 順番と前提: B と C の後。E の前。
- 完了条件: DoD3、DoD11。切替から 24 時間、main のマージ間隔と revise 率を boundary 記録に残す。
- リスク: omp 席の権限層が未検証（B stage 2 で閉じる）。Anthropic API 費用（D9）。herdr 0.9.5 との互換。
- ユーザー: (2) と (6) の `hcom relay connect <token>`（SSH 上で入力、チャットに貼らない）。

### E. 撤去
- 目的: agmsg と Claude/Codex 専用物を消し、`rg agmsg` 0 件（方向性 1・3）。
- やること: 3 PR に分ける。E1: `home/dot_claude/hooks`、`home/dot_codex/*hooks*`、Claude/Codex の settings 描画と `.chezmoitemplates/claude-*`・`codex-*`、`.chezmoiremove` 追記（`~/.claude/settings.json` の管理分、`~/.codex/*.config.toml`、hooks）。E2: agmsg skill、`home/dot_config/claude/rules/*`、`home/dot_config/codex/*`、agmsg-orchestration SKILL と rules を hcom 版 1 本に置換（文章は判断が要る部分のみ。「受け入れ・RESULT 審査・review・gate は委任しない」条項は「受け入れ判定と最終マージだけが orchestrator、統合・review・記録は席とスクリプト」に縮め、「Claude 境界は Codex 席へ」のルーティング規則と「席上限 3」の文言は削除。第 5.0 節 B1・B5）、Makefile の `agmsg-bootstrap` 等、`herdr-agents` の agmsg 経路と `bus:` キー、`agent-stop-gate.sh`、`gh-merge-gate.sh`。E3: `.chezmoiremove` の agmsg 本体、`tests/` の agmsg 系、ドキュメント。#395 と #403 を閉じる。
- 順番と前提: X の後、1 本ずつ。
- 完了条件: DoD5、DoD6、DoD8。`make update` 後に `~/.claude/hooks/gh-merge-gate.sh` と agmsg の hooks が存在しない。
- リスク: ユーザーが個人用途で Claude Code を使う場合、`~/.claude/settings.json` の管理分削除で挙動が変わる → E1 の前に 1 行で確認（既定: 管理分のみ削除、未管理ファイルは触らない）。
- ユーザー: 上記確認 1 回。

### F. ハーネス非依存の是正（先行分は仕上げ、残りは C へ）
- 目的: 再監査・再ラウンドの機械的削減（方向性 5）。
- やること: F1 #390 マージ。F2 #387 の CI 赤と 6 スレッドを a011 が 1 ラウンドで直し、follow-up 445c32dd を同じ PR に畳む（caps 内なら）。F3 は D8 で第 1 段階の P1-4/P1-6 へ。F4 は D4 で stop（要件は P1-4/P1-5/P1-7）。AGENTS.md Audit 節の判定分離（コード/記録）は既に本文にあり、追加の文章は書かない。F5（第 1 段階 P1-3、CI の効率化。evidence 付録 A の C2〜C5）: `test.yaml`・`remote.yaml`・`agent-assets.yml` に `concurrency: { group: <workflow>-${{ github.event.pull_request.number || github.ref }}, cancel-in-progress: true }` を入れて旧 head の run を止める。`remote.yaml` の `private-bootstrap` は必須チェックでないので `pull_request` では走らせず `push`/`schedule` のみにする（PR ごとに macOS 1 ジョブ減）。`public-bootstrap` の既存 decide step を広げ、PR が `setup.sh`、`install/**`、`home/**`、`scripts/lib/**`、`scripts/update-agent-assets.sh`、`scripts/gh-auth.sh`、`tests/install/**` のどれにも触れないときは後続 step を `if:` で飛ばして job は success で終える（path filter で workflow ごと skip すると必須チェックが Pending のまま merge を塞ぐ、GitHub docs の注意に従う）。`test.yaml` の bats と unit test の並列化は、`bats --jobs` と `unittest` の並列 runner が入っているかを item 0 で確かめてから（未確認）。workflows は trust boundary なので threat_table 付き、a011 が W1〜W2 で。
- 順番と前提: F1 は Wave 0。F2 は Wave 2。
- 完了条件: #390 マージ後、update-branch のみの head で監査が再実行されない記録が 1 件以上。#387 マージで `make lint` に正規化 lint が入り、baseline 73 件が CI で固定。
- リスク: #387 の 6 スレッドが同一クラスなら S1（3 回目で停止）。
- ユーザー: なし。

### G. pstack を固定資産として取り込む
- 目的: 方向性 4・7 の土台。
- やること: タスク `dotfiles-T129-pstack-asset-a01` を a010 に dispatch（Codex 可、Claude 境界ではない）。`assets.pstack` を cursor/plugins の commit sha + `plugin.json` 版で固定、as_is 群はリンク、rewritten 群は `vendor/pstack/<name>/` に LICENSE と UPSTREAM、excluded 群、`THIRD-PARTY-NOTICES.md`、allowlist テスト（存在、front matter、ハッシュ一致）。
- 順番と前提: B stage 1 マージ後（manifest と updater を共有するため直列）。
- 完了条件: DoD7。omp のスキル一覧に as_is 群が出る（B の skills root 実測に依存）。
- リスク: 上流にタグが無い（sha 固定で解決済み）。pstack 内の第三者物（未確認、取得時に scan）。
- ユーザー: なし。

### H1〜H9. Cursor 専用スキルの書き直し（B の後、優先順）
- 目的: レビュー席の置換（H3）、判断記録と復元（H1、H5）、報告（H6、H7、H8）、役割別モデル（H9 は B で実現済みなら確認のみ）。
- やること: 各 1 PR、固定 commit、`vendor/<name>/` に LICENSE と UPSTREAM、動かすテスト、文章最小。H1 show-me-your-work → omp の session JSONL と `decisions.tsv`（列は lint）。H2 verification-skill → omp のスキル置場に dotfiles 検証スキルを生成。H3 interrogate/reflect → hcom 経由で OpenAI と Anthropic の両モデルがレビューし verdict ファイルを返す（受け入れは orchestrator）。H4 architect/swarm → hcom タグへの並列配分を手順化。H5 recall → omp/hcom 履歴から再開。H6 watch-pr → gh で統合停滞を機械検知（Grok ルーティンの代替）。H7 session-report → omp ログを HTML に（project-map の隣。人向け報告の実体）。H8 Review Canvas の考えを project-map に。H9 setup-pstack → B の役割別モデルで置換（確認のみ）。
- 順番と前提: B stage 1・2 の後。H3 と H6/H7 を先に（品質と報告に直結）。
- 完了条件: DoD8。H3 のレビューが実 PR 1 本で回る。H7 の HTML が boundary ごとに更新される。
- リスク: omp のセッション形式の変更（固定版で緩和）。
- ユーザー: なし。

