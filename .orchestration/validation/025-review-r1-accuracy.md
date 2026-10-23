# Plan 025 review, round 1, perspective A: technical accuracy against primary sources

- 対象: `.orchestration/plans/025-regime-cutover-plan.md`（sha256 `79addac8c0a0…`、206 行）。読み取り専用の別文脈（Claude Code、xhigh、Bash sandbox 内）。席・`omp`/`hcom` の store・リポジトリ本体には触れていない。実行したのは `--help` 系と `wc`/`git grep`/`sed` だけ。
- 方法: 計画の第三者ツールに関する主張を、まず 2 本の facts 文書（S2、S3）と照合し、facts が支えない箇所と facts 行が疑わしい箇所は、固定版の一次資料（omp v18.11.3 の docs と導入済み `src/`、hcom v0.7.30 の source、srt main @ v0.0.81、Claude Code docs、Codex source、gh manual、chezmoi reference、npm registry JSON）を取得して照合した。引用は逐語、`~` はホーム。
- 優先度: P0 = 作業項目を不可能または危険にする主張、P1 = 計画が前提にする誤ったツール挙動、P2 = 根拠無しに事実として書かれた主張、P3 = 表現。

## Sources

| id | url / source | fetched_at (UTC, `date -u`) |
| --- | --- | --- |
| S1 PLAN | `.orchestration/plans/025-regime-cutover-plan.md` @ sha256 `79addac8…` | 2026-10-22T10:12:51Z |
| S2 FACTS-B2C2 | `.agents/worklog/orchestrator-glue/b2-c2-facts.md` | 2026-10-22T10:12Z |
| S3 FACTS-SRT | `.agents/worklog/orchestrator-glue/srt-facts.md` | 2026-10-22T10:12Z |
| S4 OMP-HELP | `~/.local/bin/omp --help`, `omp models --help`, `omp config --help`（`omp v18.11.3`、help のみ） | 2026-10-22T10:12:51Z |
| S5 HCOM-HELP | `~/.local/bin/hcom --help` と `config`/`kill`/`status`/`list`/`events`/`send`/`transcript`/`omp` の `--help`（`hcom 0.7.30`、help のみ、store は開かない） | 2026-10-22T10:12:51Z |
| S6 OMP-SRC | 導入済み `~/.local/lib/node_modules/@oh-my-pi/pi-coding-agent/` 18.11.3: `src/session/agent-session.ts`, `src/extensibility/extensions/{runner,types}.ts`, `src/cli/{args,flag-tables}.ts`, `src/modes/print-mode.ts`, `src/config/model-resolver.ts`, `dist/cli.js` 先頭行 | 2026-10-22T10:13Z |
| S7 OMP-CLI | `https://raw.githubusercontent.com/can1357/oh-my-pi/v18.11.3/docs/cli-reference.md` | 2026-10-22T10:14:19Z |
| S8 OMP-SKILLS | `https://raw.githubusercontent.com/can1357/oh-my-pi/v18.11.3/docs/skills.md` | 2026-10-22T10:14:20Z |
| S9 OMP-CONFIG-USAGE | `https://raw.githubusercontent.com/can1357/oh-my-pi/v18.11.3/docs/config-usage.md` | 2026-10-22T10:14:20Z |
| S10 OMP-ENV | `https://raw.githubusercontent.com/can1357/oh-my-pi/v18.11.3/docs/environment-variables.md` | 2026-10-22T10:14:20Z |
| S11 OMP-SETTINGS | `https://raw.githubusercontent.com/can1357/oh-my-pi/v18.11.3/docs/settings.md` | 2026-10-22T10:23:32Z |
| S12 OMP-RELEASE | `https://api.github.com/repos/can1357/oh-my-pi/releases/latest`（`v18.12.6`, published 2026-10-21T21:02:53Z） | 2026-10-22T10:14:21Z |
| S13 HCOM-LAV | `https://raw.githubusercontent.com/aannoo/hcom/v0.7.30/src/tools/launch_arg_validation.rs` | 2026-10-22T10:14:23Z |
| S14 HCOM-PLUGIN-RS | `https://raw.githubusercontent.com/aannoo/hcom/v0.7.30/src/hooks/omp/plugin.rs` | 2026-10-22T10:14:24Z |
| S15 HCOM-EVENTS | `https://raw.githubusercontent.com/aannoo/hcom/v0.7.30/src/commands/events.rs` | 2026-10-22T10:14:24Z |
| S16 HCOM-LAUNCHER | `https://raw.githubusercontent.com/aannoo/hcom/v0.7.30/src/launcher.rs` | 2026-10-22T10:14:24Z |
| S17 HCOM-LAUNCH | `https://raw.githubusercontent.com/aannoo/hcom/v0.7.30/src/commands/launch.rs` | 2026-10-22T10:14:25Z |
| S18 HCOM-CONFIG | `https://raw.githubusercontent.com/aannoo/hcom/v0.7.30/src/commands/config.rs` | 2026-10-22T10:14:25Z |
| S19 HCOM-RELEASE | `https://api.github.com/repos/aannoo/hcom/releases/latest`（`v0.7.31`, published 2026-10-21T03:55:43Z） | 2026-10-22T10:14:26Z |
| S20 SRT-NPM | `https://registry.npmjs.org/@anthropic-ai/sandbox-runtime` | 2026-10-22T10:14:27Z |
| S21 SRT-README | `https://raw.githubusercontent.com/anthropics/sandbox-runtime/main/README.md`（repo `pushed_at` 2026-10-21T21:50:19Z、最新 tag `v0.0.81` = `c40cf14a65`） | 2026-10-22T10:14:27Z |
| S22 SRT-CLI | `https://raw.githubusercontent.com/anthropics/sandbox-runtime/main/src/cli.ts` | 2026-10-22T10:14:28Z |
| S23 SRT-UTILS | `https://raw.githubusercontent.com/anthropics/sandbox-runtime/main/src/sandbox/sandbox-utils.ts` | 2026-10-22T10:14:28Z |
| S24 SRT-MACOS | `https://raw.githubusercontent.com/anthropics/sandbox-runtime/main/src/sandbox/macos-sandbox-utils.ts` | 2026-10-22T10:14:28Z |
| S25 SRT-DEBUG | `https://raw.githubusercontent.com/anthropics/sandbox-runtime/main/src/utils/debug.ts` | 2026-10-22T10:22:32Z |
| S26 SRT-VSTORE | `https://raw.githubusercontent.com/anthropics/sandbox-runtime/main/src/sandbox/sandbox-violation-store.ts` | 2026-10-22T10:22:32Z |
| S27 SRT-HTTPPROXY | `https://raw.githubusercontent.com/anthropics/sandbox-runtime/main/src/sandbox/http-proxy.ts` | 2026-10-22T10:23:30Z |
| S28 SRT-PKG | `https://raw.githubusercontent.com/anthropics/sandbox-runtime/main/package.json`（`"version": "0.0.81"`, `"commander": "^12.1.0"`） | 2026-10-22T10:23:31Z |
| S29 COMMANDER | `https://raw.githubusercontent.com/tj/commander.js/master/Readme.md` | 2026-10-22T10:23:31Z |
| S30 CC-SANDBOX | `https://code.claude.com/docs/en/sandboxing.md` | 2026-10-22T10:17:25Z |
| S31 CC-ENVS | `https://code.claude.com/docs/en/sandbox-environments.md` | 2026-10-22T10:17:25Z |
| S32 CODEX-EXEC | `https://raw.githubusercontent.com/openai/codex/main/codex-rs/exec/src/cli.rs` | 2026-10-22T10:18:44Z |
| S33 GH-MERGE | `https://cli.github.com/manual/gh_pr_merge` | 2026-10-22T10:17:26Z |
| S34 CHEZMOI-ATTR | `https://raw.githubusercontent.com/twpayne/chezmoi/master/assets/chezmoi.io/docs/reference/source-state-attributes.md` | 2026-10-22T10:18:44Z |
| S35 REPO | この checkout（main `d06d94fd` + 未コミットの記録差分）: `README.md`, `scripts/orchestrator/orch-audit.sh`, `scripts/update-agent-assets.sh`, `scripts/check-tools.sh`, `scripts/generate-agent-configs.py`, `git grep`, `wc -l` | 2026-10-22T10:12Z |
| S36 DECISIONS | `.orchestration/decisions.tsv` D-024-86〜D-024-98 | 2026-10-22T10:12Z |

取得できなかった資料: `https://developers.openai.com/codex/cli/reference`（HTTP 403、2 回）→ S32 の source で代替。`https://bun.sh/docs/api/fetch.md` と `https://raw.githubusercontent.com/oven-sh/bun/main/docs/api/fetch.md`（HTTP 404）→ omp 自身の docs（S10）で代替。

## Findings

`id | priority | plan section and line | the plan's claim | what the source says | fix`

| id | P | 節・行 | 計画の主張 | 一次資料 | 直し方 |
| --- | --- | --- | --- | --- | --- |
| A-01 | P1 | §4 第 2 脚 #3/#4（L125-126）、§9「provider のホスト名」（L180）、§1.3 残る未検証（L11） | `log stream --predicate 'process == "sandbox-exec"'` で取った `violations.log` の拒否行が「本当に要るホスト」= B-3 の `allowedDomains` の実値になる | ホスト名の許否は Seatbelt ではなく srt のホスト側 proxy が決める。omp の provider 通信は proxy 環境変数を読む: S10 L153-158「Provider HTTP fetches resolve proxies in this order after applying `NO_PROXY` / `no_proxy`: 1. `PI_PROXY_<PROVIDER>` … 2. `PI_PROXY` 3. `HTTPS_PROXY` / `https_proxy` for HTTPS and WebSocket targets … 4. `ALL_PROXY` / `all_proxy`」。srt はそれを子に渡す: S23 L841-842 `envVars.push(\`HTTP_PROXY=http://${auth}localhost:${httpProxyPort}\`)`, `HTTPS_PROXY=…`, L869 `ALL_PROXY=…`, L837 `NO_PROXY=…`。macOS profile は proxy の localhost ポートだけを開ける: S24 L1326 `(allow network-outbound (remote ip "localhost:${httpProxyPort}"))`。許可外ホストは proxy が 403 で拒み、CLI では `SRT_DEBUG` 時だけ stderr に出る: S27 L698 `logForDebugging(\`Connection blocked to ${requestedHost}:${port}\`, {`; S25 L8-11「Only log if SRT_DEBUG environment variable is set」L18「Always use stderr」; S22 に violation を端末へ出すコードは無い（`grep -i violation` 0 件）。`log stream` に出るのは kernel 側の拒否（書込、proxy を介さない直接接続）だけ | 第 2 脚に #3b を足す: `srt --debug --settings $TMPDIR/pilot/srt-worker.json -- omp -p --no-session --model <第 1 脚 #9 の値> 'reply with one word' 2>$TMPDIR/pilot/srt-debug.log; grep 'Connection blocked to' $TMPDIR/pilot/srt-debug.log` → この行の集合が provider ホストの実値（席と headless で同じ）。#4 の shim にも `--debug` を付け stderr を別ファイルへ。`log stream` は書込パスの測定だけに使う。§9 の行の「閉じる場所」を #3b に直す |
| A-02 | P1 | §4 第 2 脚 #5（L127） | TASK の `touch $TMPDIR/pilot/ok` が成功する（= `allowWrite` の証拠） | srt は子プロセスの `TMPDIR` を書き換える: S23 L794-805「TMPDIR is overridden so temp-file writers land in a path the FS sandbox …」`process.env.CLAUDE_CODE_TMPDIR \|\| process.env.CLAUDE_TMPDIR \|\| '/tmp/claude'` → `envVars.push(\`TMPDIR=${tmpdir}\`)`; S21「A few paths are writable without being listed: the child's stdio and `/tmp/claude`」。席の中で `$TMPDIR/pilot/ok` は `/tmp/claude/pilot/ok` になり、ディレクトリが無いので `touch` は ENOENT で失敗し、あっても常時書込可なので成功する。どちらも `allowWrite: ["$TMPDIR/pilot"]` を測っていない | TASK には操作者の shell で展開した絶対パスを文字列で書く（または `$PWD/ok`: 席の cwd は `--dir`）。TASK に `echo $TMPDIR` を加え、srt の書き換え値を pilot-facts に残す（§9「`TMPDIR=/tmp/claude` の影響」の一部が閉じる） |
| A-03 | P2 | §4 第 1 脚 #3（L103） | `hcom config terminal --info` が「herdr preset の template 文字列」を出す | S18 `terminal_help_text`（L1405-1600）は `Current: …`、「Managed (open + close on kill):」に `[+]`/`[-]` 付きの名前と説明、「Variants:」、「Other (opens window only):」、「Custom presets (config.toml):」を出すだけで、argv template は出さない。template は S3 Q2 で引用済み（`terminal_presets.rs`: `herdr tab create --cwd {cwd} --no-focus --label {instance_name}`） | 期待出力を「`herdr` が `[+]` で列挙される（PATH にある証拠）」に直し、template は S3 Q2 の行を Facts にする |
| A-04 | P2 | §1.2（L10）、§4 第 2 脚 #1（L123） | shim の `--` の受理は「第 2 脚 #1 の `srt --help` で確認」 | srt は commander: S28 `"commander": "^12.1.0"`; S22 L333 `.argument('[command...]', 'command to run in the sandbox')`, L349 `.allowUnknownOption()`, L562 `command = quote(commandArgs)`。`--` は commander の標準: S29 L200「You can use `--` to indicate the end of the options, and any remaining arguments will be used without being interpreted.」L362「The special argument `--` stops option processing entirely.」`srt --help` はこれを表示しない。なお S22 L340 `.option('-c <command>', …)` があるので、`--` 無しでは omp 側の `-c`（`--continue`）を srt が食う | #1 を直接の probe に替える: `srt --settings $TMPDIR/pilot/srt-worker.json -- /bin/echo -c --model x; echo exit=$?` → `-c --model x` と `exit=0`。Facts に S29 の行を置く |
| A-05 | P2 | §4 第 2 脚 #2/#4（L124, L126）、§3 W5（L84） | shim を `$TMPDIR/pilot/bin` に置き、同じ `$TMPDIR/pilot` を `allowWrite` に入れる。W5 の `hcom-seat` は shim の置場を言わない | S21 Security Limitations「Allowing writes to directories containing executables in `$PATH`, system configuration directories, or user shell configuration files … can lead to code execution in different security contexts」、「Where This Package Is Installed: Install it outside every allowed write path」。計画は srt 本体には従う（`~/.local/lib` を除外）が、同じ PATH 先頭の shim には適用していない | パイロット: shim を `allowWrite` 外（例: `~/.local/libexec/hcom-seat/`）に置くか `denyWrite` に `$TMPDIR/pilot/bin` を足す。W5: shim ディレクトリを固定し、全役割の `allowWrite` 外にあることを Behaviour 表の 1 行にする |
| A-06 | P2 | §4 第 2 脚 #2（L124）、#7（L129） | JSON に `"$TMPDIR/pilot"` / `"$TMPDIR/pilot/out"` と書く | S21 L579-580「Paths can be absolute … or relative to the current working directory」「`~` expands to the user's home directory」。環境変数の展開は文書に無い | 操作者に「heredoc は非クォート（`<<EOF`）か `printf` で、shell が展開した絶対パスを書く」と明記し、生成した JSON を `cat` で貼る |
| A-07 | P2 | §1.4（L12）、§2 skills 行（L31）、§4 第 1 脚 #4（L104）、W5（L83） | `~/.agents/skills` は omp の agents provider が読み、`enabledProviders` で opt-in | S8 L122「The `agents` provider (`.agent[s]/skills`) has its own `enableAgentsUser`/`enableAgentsProject` toggles — disabling Claude/Codex/Pi does **not** turn it off. Foreign user-level providers are opt-in through `enabledProviders`」; S11 L344「`enabledProviders` opts foreign user-level configuration sources into discovery. Its default is empty, so user roots from Cursor, Codex, Claude, Claude marketplace plugins, Gemini, OpenCode, Windsurf, and GitHub are normally excluded until their provider id is listed」— この列挙に `agents` は無く、`enableAgentsUser` は settings.md に項目が無い（grep 0 件）。どちらの鍵（または両方）が `~/.agents/skills` を admit するかは docs で決まらない | 第 1 脚 #4 に `omp config list --json` を加えて `enableAgentsUser`/`enabledProviders` の実在と既定を貼る。B-3 の item 0 は「読み込まれた skill 一覧」で鍵を確定し、`enabledProviders` を先に決め打ちしない |
| A-08 | P2 | §1.7（L15）、S3 Q2 の facts 行 | hcom が席の起動引数として拒むのは `-p`/`--print` | S13 `OMP_REJECTED_ARGS`: `-p`、`--print`（"runs non-interactively and exits"）、`--mode`（"can disable the interactive extension host used by hcom delivery"）、`--no-extensions`（"prevents hcom's delivery extension from loading"）、root subcommand `acp`。S16 L2765 `LaunchTool::Omp => validate_rejected_args("Oh My Pi", "hcom omp", args, OMP_REJECTED_ARGS)` で席の argv に適用 | facts 行を全リストに直す。B-2/C-2' の argv 検査（W5「`omp_args` 非空の拒否」）はこの 5 件を鏡にする。第 1 脚 #9 / 第 2 脚 #4 はどれも渡していないので今日の手順は影響無し。`--no-extensions` で worktree の `.omp/extensions` 混入を防ぐ案は hcom 席では不可能、と設計側に 1 行 |
| A-09 | P3 | §1.7（L15）、§9（L188）、W6（L85） | omp の非対話実行フラグと出力形式は【未検証】 | S7 L188-192「`--print` / `-p` runs `omp` non-interactively: it processes the prompts, writes the last assistant response to stdout, and exits without entering the TUI. Text output is emitted after the turn completes, not token-by-token; a `Working...` indicator goes to stderr.」L214-217「`--mode json` emits a session header followed by events as JSON lines … completed messages arrive in `message_end` … Terminal turn failures produce a nonzero exit status in both text and JSON modes.」L64「`--` ends flag parsing; everything after it is literal message text」。S4 も `-p, --print Non-interactive mode: process prompt and exit`、`--mode=<value> Output mode: text (default), json, rpc, or rpc-ui` を出す。Codex 側: S32 L72-79「Specifies file where the last message from the agent should be written.」`--output-last-message` | 未検証を Facts 行（S7）に格上げし、第 1 脚 #5/#7 は「フラグの有無」でなく「出力の形」の測定にする。W6 の `omp-run.sh` の対は `-p … > <out>.last.md`（最後の応答）+ `--mode json > <out>.jsonl`（全事象）か、1 回の `--mode json` から最後の `message_end` を抜く形 |
| A-10 | P3 | §4 第 1 脚 #5, #16、第 2 脚 #4（L105, L116, L126） | `grep -n -E -- '^\s+(-p\|--print\|…)'` のように ERE 内に `\|` | Markdown 表のエスケープがコマンドに混入している。POSIX ERE で `\|` は未定義、macOS の grep は literal 扱いになり一致しない | パイロットの貼付元を表の外の fenced block（D-024-97 の `pilot/leg1.md`）にし、表には「leg1.md の #n」とだけ書く |
| A-11 | P3 | §1.3（L11） | 「Claude 専用 5 キーが落ちる」 | S3 Q5 の列挙は 7（`enabled`, `failIfUnavailable`, `autoAllowBashIfSandboxed`, `allowUnsandboxedCommands`, `excludedCommands`, `allowManagedDomainsOnly`, `allowManagedReadPathsOnly`）、manifest の `claude.sandbox` に srt 対応の無い鍵は 6（上の 5 + `linux_excluded_commands`） | 数を書かず鍵名を列挙する |
| A-12 | P3 | §4 第 1 脚 #1（L101） | 期待出力「`hcom 0.7.30`（0.7.31 の通知付き）」 | S5 は 10:12Z 時点で「→ hcom v0.7.31 available — run `hcom update`」; S19 最新は v0.7.31（2026-10-21T03:55:43Z）。次版が出ると通知文が変わる | 「新版通知付き（版は問わない）」にする |
| A-13 | P3 | §9 版ずれ行（L190）、§2 asset 行（L32） | 版ずれの行は hcom 0.7.31 だけ | S12: omp 最新 `v18.12.6`（2026-10-21T21:02:53Z）、print mode の挙動変更（「`omp -p '/compact'`, `/handoff`, and `/retry` given as CLI arguments now run the command … and exit 1 when the command fails」）。固定 tarball 導入なので `make update` では動かないが、S4 に `update Check for and install updates` があり、席が `omp update` を打てば `~/.local/lib` へ書く → srt の `allowWrite` 外で拒まれる（計画に有利な帰結） | §9 に omp の行を足し、「`omp update` は srt が拒む」を B-3 の Facts/Behaviour に 1 行 |
| A-14 | P3 | §1.2（L10）、§4 第 2 脚 #4（L126） | `readlink -f ~/.local/bin/omp` の実体を srt の下で exec する | S6 `dist/cli.js` の 1 行目は `#!/usr/bin/env bun`（node ではない）。srt の中で `bun` が PATH で解決できる必要がある（読み取りは既定で開いている: S21「By default, read access is allowed everywhere」） | 第 2 脚 #4 の貼付に `command -v bun; readlink -f "$(command -v bun)"` を足し、Facts に「omp は Bun で走る」を置く |
| A-15 | P3 | §9（L187） | 「runner は起動側 hcom のディレクトリを PATH 先頭に置く」 | S16 L846-886 `resolve_runner_binaries`: 先頭は `node` の dir、次に `current_exe()` の dir（S16 L1060-1068）、次に tool・hcom・python の dir。`warn_if_agent_hcom_differs(&binaries.path_dirs)` が差異を警告する | 「node の dir、起動側 hcom の dir の順で PATH 先頭に置く」に直す |
| A-16 | P3 | §4 第 1 脚 #10（L110） | 期待出力「1 行 `[OMP] <name> listening`」 | S5 `hcom list --help` は Status icons（`◉ listening`）と Tool labels（`[OMP] … hcom-launched, automatic delivery`）を別々に示し、1 行の並びは文書化していない | 「`[OMP]` と `listening` を含む 1 行」にする |
| A-17 | P3 | §2 generator 行（L37） | `expected_outputs()` の「4+N 出力」 | S35 `scripts/generate-agent-configs.py:1342-1364`: 固定 4 + profile ごとの modify N + base modify + `model-profiles.env` + Claude agents 2 + codex plugin manifest + skill symlink 群 + asset constants | 「codex/claude/plugins 由来の出力」とだけ書く |
| A-18 | P3 | §4 第 1 脚 #12（L112） | thread 列の実名は `pragma table_info(events_v)` で確認（`msg_thread` は review の呼称） | S5 `hcom events --help`「SQL reference (events_v view): … msg_* from, text, scope, sender_kind, delivered_to[], mentions[], intent, thread, reply_to」→ 列名は `msg_thread` | Facts に S5 の行を置き、#12 の pragma は確認として残してよい |

## 正しいと確認できた主張（claim, source）

- `session_stop` は `agent_end` より前に await される（§1.8「ゲートはその前に走る」）: S6 `src/session/agent-session.ts:4706-4707` `const sessionStopWillContinue = await this.#emitSessionStopEvent(activeMessages, msg); await emitAgentEndNotification(sessionStopWillContinue ? { willContinue: true } : undefined);`。main 限定と handler 有無のゲート: `:5254` `if (this.#agentKind === "sub" || !this.#extensionRunner?.hasHandlers("session_stop")) { return false; }`。`decision: "block"` が上限を消費しない: `if (result?.decision !== "block") this.#sessionStopContinuationCount++;`。S2 Q1 の Implications は推論だったが source で裏が取れた。計画は S-M に従いこの行を Facts にできる。
- `-e` の extension から `pi.on("session_stop", …)` が登録できる: S6 `src/extensibility/extensions/types.ts:1661` `on(event: "session_stop", handler: ExtensionHandler<SessionStopEvent, SessionStopEventResult>): void;`。
- omp の provider 通信は srt の proxy を通る（§1.3「網はホスト側 proxy 経由」の前提）: S10 L153-158（A-01 の引用）、L235「Honored via Bun's native fetch proxy support」; srt 側 S23 L837-869; macOS profile S24 L1317-1341。
- `--model <provider>/<id>:<level>` の接尾辞は CLI でも解釈される: S6 `src/config/model-resolver.ts` 冒頭「`parseModelPatternWithContext`/`parseModelPattern` layer the selector grammar on top: trailing `:level` thinking suffixes (`splitThinkingSuffix`) … `resolveCliModel` … adapts inputs — … CLI flags … — onto that pipeline.」（S7 の `--model` 行自体は接尾辞に触れない）。
- `hcom [N] omp` の `--` 以降は全部ツール引数: S17 L578-580 `if args[i] == "--" { tool_args.extend_from_slice(&args[i + 1..]); break; }`。
- 利用者の `-e <path>` は hcom に剥がされない: S14 L98-121 `strip_managed_extension_args` は hcom 所有・legacy のパスだけを除く（「only exact-current and hcom-owned files are removed when present」）; hcom は `-e <HCOM_DIR>/integrations/omp/<digest>/hcom.ts` を `insert_before_separator` で足す（L57-69）。
- `hcom events --idle <name> --wait <sec>` の exit: 一致 0、timeout 1: S15 L868-869 `println!(...); return 0;`、L895-897 `println!("{}", json!({"timed_out": true})); break 1;`。
- runner script が絶対パスを `--hcom-tool-path` で固定し、PATH を node → 起動側 hcom → tool → hcom → python の dir で前置する: S16 L846-886, L1052-1073。script は `~/.hcom/.tmp/launch/` に書かれ（L974-976）、実行時の `remove_file(&script)` は test 関数内（L3840 以降、`#[test]`）にしかない → 第 2 脚 #4 の `grep -c hcom-tool-path ~/.hcom/.tmp/launch/*.sh` は成立しうる（後片付けの有無は未検証）。
- `hcom status`（"Installation status and diagnostics", `--json`）、`hcom kill <name>`（"Kill one or more processes (+ close terminal panes)"）、`hcom transcript <name>`、`hcom config <key> --info`、`hcom list --json`、`hcom send --from/--thread/--json`、`hcom omp --headless`、`hcom omp` の exit 0/1/2: S5。
- `omp -p`、`--mode text|json|rpc|rpc-ui`（source は `acp` も受ける: S6 `cli/flag-tables.ts:128-136`）、`--max-time`、`--no-session`、`--no-extensions`（"explicit -e paths still work"）、`-e` 反復可（S7 L154 "repeatable"）、`--config` 反復可、`omp models find <pattern> --json`（S4「PATTERN … required for find」）、`omp config get|path --json`: S4、S7。
- srt: `-s, --settings <path>`、`[command...]`、`-c <command>`、`allowUnknownOption`（S22 L333-349）; stdio 継承と TUI（S3 Q1 + S31 L122 `srt claude`）; 存在しない `--settings` はエラー終了（S21 L184、S31 L136「It also refuses to start if the `--settings` file doesn't exist.」）; `allowPty` の意味（S21 L595）; 必須 5 配列（S3 Q1 の schema 引用）; `log stream --predicate 'process == "sandbox-exec"' --style syslog`（S21 L1232）; 「許可書込パスの外に置く」（S21 L1277）; Beta Research Preview（S21 L7）。
- srt は SIGINT/SIGTERM を子へ転送する（`hcom kill` が shim/srt の pid を殺しても omp が残らない根拠）: S22 L643-648 `process.on('SIGINT', () => { child?.kill('SIGINT') })`, `process.on('SIGTERM', () => { child?.kill('SIGTERM') })`。
- W3 が貼るべき registry 値（S20）: `dist-tags.latest = 0.0.81`、`time["0.0.81"] = 2026-10-20T01:13:23.926Z`、`engines.node = >=22.12.0`、`bin.srt = dist/cli.js`、`license = Apache-2.0`、tarball `https://registry.npmjs.org/@anthropic-ai/sandbox-runtime/-/sandbox-runtime-0.0.81.tgz`、`shasum 0e88d497adf13c85636274e3b8b4dfb16eb523b6`、`integrity sha512-bjHDu87gjIR7+Oxy9jPiK3v8CvSELCzfpXa3fjqfSKdvlZET2iF51xcXILWPayTpowB3xtZeQVf2JR916nVW/w==`。この機械の node は v26.12.0（S3 LOCAL）。
- `npm install -g --prefix ~/.local` は `update_omp` と同形: S35 `scripts/update-agent-assets.sh:981` `npm_config_min_release_age=0 npm install -g --prefix "${HOME}/.local" "${tarball}"`。
- ruleset の必須 7 チェック: S35 `README.md:1176-1194` の context は `validate`、`test (ubuntu-24.04, server|client)`、`test (macos-14, client)`、`public-bootstrap (ubuntu-24.04, server|client)`、`public-bootstrap (macos-14, client)`。
- `orch-audit.sh` の 1 行: S35 `scripts/orchestrator/orch-audit.sh:72` `codex --profile audit exec --sandbox read-only -C "${review}" -c approval_policy=never -o "${review}/${out}.last.md" "${prompt}" < /dev/null > "${review}/${out}" 2>&1`。
- `gh pr merge --squash --match-head-commit <SHA>`: S33 に `--match-head-commit <SHA>`。
- chezmoi の `modify_private_config.yml` の接頭辞順: S34「Modify file ／ File ／ `modify_`, `encrypted_`, `private_`, `readonly_`, `executable_`, `dot_`」。
- 【実測】の数: `executable_herdr-agents` 2292 行、`agmsg-orchestration/SKILL.md` 267 行、`home/dot_config/claude/rules/*.md` 12 本、`git grep -l agmsg -- ':!.orchestration'` 69、agmsg を参照する `tests/unit/*.py` 19、`update_omp()`/`update_hcom()` は `scripts/update-agent-assets.sh:945,996`、`check_omp()`/`check_hcom()` は `scripts/check-tools.sh:172,187`（S35）。
- Claude 設定の鍵名（`filesystem.allowWrite/denyWrite/denyRead/allowRead`, `network.allowedDomains/deniedDomains`, `excludedCommands`, `allowUnsandboxedCommands`, `failIfUnavailable`, `autoAllowBashIfSandboxed`）: S30。「Claude Code builds the sandbox on the open source `@anthropic-ai/sandbox-runtime` package」: S30 L36。
- `enabledProviders` という設定鍵の実在と既定 `[]`: S11 L454。rules の置場（§2 の【未検証】を狭める）: S9 L294「Rules: `rules/*.{md,mdc}` plus top-level `RULES.md`」（user root は S2 Q1 の `<agentDir>` = `~/.omp/agent/` の下、つまり `~/.omp/agent/rules/`）。
- `events_v` の thread 列は `msg_thread`（A-18）。
- herdr preset の 2 段（`tab create` → `pane run`）、`--kind omp`、`HCOM_LAUNCHED`/`HCOM_TAG`/`HCOM_DIR`、`instances.launch_args`/`pid`、`config.yml.lock`、`--config` overlay の strict（「a missing file, invalid YAML, or a top-level array/scalar is a hard error」）、`bash.patterns` の deny が yolo でも絶対、`compaction.methodOrder`/`handoffSaveToDisk`: S2/S3 の引用どおり（再取得はしていない）。

## 確認できなかった主張（理由）

- `hcom status` が `~/.hcom/hcom.db` と `config.toml` を作る（第 1 脚 #2）: store を開くコマンドは本レビューの禁止範囲。help は「Installation status and diagnostics」としか言わない。
- `hcom list --json` が `pid`/`launch_args` を出すか、`hcom list` の 1 行の並び: 実行が要る（列の存在は S2 Q5）。
- thread の membership（外部送信者 → `@<name> --thread` で受信者が member になるか、席からの `--thread` 返信、未 seed の thread のエラー）: source 引用のみ、実機 0（計画の §9 と同じ評価）。
- `bash.patterns` の deny と `tool_call` の `{ block: true }` が実機で効くか、拒否理由が返答に現れるか: 実行が要る。
- `session_stop` が print mode と hcom 配送下で実際に発火するか: 静的には agent-end の settle 経路にあり mode に依存しない（S6）が、runtime は未測定。
- provider のホスト名: omp docs に無い（S3 Q3）。A-01 の #3b で測る。
- omp が `~/.omp/agent`、`~/.omp/run`、`~/.hcom` だけ書込可で起動し `listening` に達するか、`TMPDIR=/tmp/claude` の影響、macOS の入れ子: 計画どおり未検証。
- `enableAgentsUser` の鍵の正式パスと既定: S11 に項目が無い（A-07）。
- `hcom config terminal --info` の実出力: source（S18）からの推定で、実行はしていない。
- C-2 の Checks にある lint baseline の行数（R1 10、R3 3、R6 1）: 未照合。
- `hcom config omp_args --info` の既定が空か: 実行が要る（S3 Q2 の `HcomConfig.omp_args: String` は型だけ）。
- Codex 公式 docs ページ（403）と Bun docs（404）: 代替資料で確認（S32、S10）。

## 報告（15 行）

1. 件数: P0 0、P1 2、P2 6、P3 10（計 18）。正しいと確認できた主張 25 群、確認できなかった主張 12 件。
2. 最重要 A-01（P1）: 第 2 脚 #3/#4 の「violations.log の拒否行 = allowedDomains の実値」は成り立たない。omp は `HTTPS_PROXY`/`ALL_PROXY` を読んで srt の localhost proxy に行き、ホストの許否は proxy の 403 で、CLI では `SRT_DEBUG`/`--debug` の stderr にしか出ない。`log stream` は書込と直接接続の拒否だけ。
3. 次に A-02（P1）: 第 2 脚 #5 の `touch $TMPDIR/pilot/ok` は、srt が子の `TMPDIR` を `/tmp/claude` に書き換えるため `allowWrite` を測らない。絶対パスか `$PWD` に直す。
4. 三つ目 A-05/A-04（P2）: shim を `allowWrite` の中（`$TMPDIR/pilot/bin`）に置くのは srt README の禁止形で、W5 にも置場の規定が無い。`--` の受理は `srt --help` では確認できず、直接 probe が要る（`-c` が srt の option と衝突する）。
5. 計画の核心は source で裏が取れた: `session_stop` は `agent_end` より前に await され（agent-session.ts:4706-4707）、X-1 のゲートは hcom の `listening` 書込より前に走る。
6. 同じく裏が取れた: hcom の `--` 分離、利用者 `-e` の温存、`--hcom-tool-path` の固定と runner PATH、`events --wait` の exit 0/1、srt の信号転送、`--model …:xhigh` の解釈、chezmoi の `modify_`→`private_` 順、ruleset 7 チェック、`orch-audit.sh:72`、registry の 0.0.81 と sha。
7. W6 の【未検証】は緩められる: cli-reference.md が `-p` は「writes the last assistant response to stdout」、`--mode json` は JSON lines、失敗は非 0 終了と明記し、`codex exec -o`（`--output-last-message`、「last message」）の対応物になる（A-09）。
8. hcom が席で拒む omp 引数は `-p`/`--print` だけでなく `--mode`、`--no-extensions`、`acp` も（A-08）。今日の手順は抵触しないが、B-2/C-2' の argv 規則に要る。
9. `~/.agents/skills` の opt-in 鍵は `enabledProviders` と決め打ちできない（skills.md は `enableAgentsUser` を別に挙げる、A-07）。第 1 脚 #4 に `omp config list --json` を足す。
10. 表現の修正: `hcom config terminal --info` は template を出さない（A-03）、JSON 内の `$TMPDIR` は srt が展開しない（A-06）、表セルの `\|`（A-10）、「Claude 専用 5 キー」（A-11）、omp 18.12.6 の存在（A-13）、omp は Bun で走る（A-14）。
11. 第 1 脚のコマンド名（`hcom status`/`kill`/`transcript`/`config --info`/`list --json`/`send --from --thread --json`、`omp models find --json`、`omp config get --json`、`--max-time`）は全部実在し、第 1 脚 #9/#4 の argv は hcom の拒否リストに触れない。
12. 届かなかった資料: Codex の公式 docs ページ（403）と Bun の fetch docs（404）。前者は GitHub の `codex-rs/exec/src/cli.rs`、後者は omp の environment-variables.md で代替した。
13. 実行しなかった検証: store を開く hcom/omp コマンド全部（`hcom status`、`config --info`、`list`、`omp config get`、`models find`）、席の起動、srt の導入。これらは計画どおり第 1・2 脚の測定に残る。
14. facts 文書への差し戻し: S3 Q2 の「拒否は `-p`/`--print`」（A-08）と、S2 Implications の「ゲートが先に走る」は推論から source 確認に格上げできる。
15. 本文脈の書込は本ファイル 1 本。提案の直し方はいずれも計画の形（測定を第 4 節に足す）に沿うもので、新しい機構は要らない。
