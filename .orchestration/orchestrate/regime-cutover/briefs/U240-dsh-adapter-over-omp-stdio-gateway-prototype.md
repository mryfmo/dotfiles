# U240 DSH reaches Claude through omp's stdio gateway: an adapter plugin, proven against a stub gateway

GOAL
The operator ruled on 2026-11-06 (decisions row of phase `frame`, 05:46:33Z) that the kit holds no model API key: every model route goes through the Claude login or Sign in with ChatGPT, and the Ollama Cloud route the DSH profile named (M-14) is withdrawn. U238 compared five shapes and chose (d): a DSH `LlmAdapter` plugin that spawns `omp auth-gateway stdio` as a child and translates its JSON-line replies into DSH stream chunks, so the login stays inside omp and DSH consumes it. U239 measured the gateway on this host (replies below). This unit builds the plugin and proves it end to end against a stub gateway that replays the measured replies, so no login and no model call is needed to test it. The real-login turn is the coordinator's measurement after your head is in.

SCOPE
A new branch `feat/dsh-omp-gateway-adapter` from `origin/main` d1ecd495 (your tree is `/tmp/dotfiles-wt/U240`; if it is absent, wait 30 s and look again). May write: a new directory `home/dot_dsh/plugins/omp-gateway/` (the plugin, its stub gateway, its fixtures and its tests), a new scratch DSH profile under your tree only if the composition proof needs a file the kit profile cannot supply (name it in the report), and the body file `../U240-pr-body.md` beside your tree. Not: `scripts/generate-agent-configs.py`, `home/dot_agents/agent-config.yaml`, the rendered `home/dot_dsh/profiles/thak/cordis.patch.yml`, the updater, `hcom-seat`. Those are the next unit's, which renders your plugin into the kit profile once its loading mechanism is known.

CONTEXT
Read-only sources on this host. DSH `dsh-v0.2.1-rc.5` source: `~/.dsh/dsh/dsh-v0.2.1-rc.5.CaRLjX` (call it `$DSH`); the installed binary `~/.dsh/bin/dsh` (0.2.1-rc.5). omp 18.12.6 at `~/.local/lib/node_modules/@oh-my-pi/pi-coding-agent`.
- The seam. A provider adapter is an in-process class extending the abstract `LlmAdapter` and implementing `stream(options): AsyncIterable<StreamChunk>` (`$DSH/packages/llm/llm/src/index.ts:208,302`), registered with `ctx.llm.registerAdapter(providers, adapter)` (`:401`). Chunk kinds are `block-start`, `text-delta`, `reasoning-delta`, `tool-call-delta` (raw JSON argument deltas), `block-end`, `usage`, `finish` (`types.ts:470-481`). The request carries `provider`, `model`, `messages`, `system`, `tools` (JSON-schema `ToolSchema`) and `signal` (`types.ts:529-585`). `subagent-acp` (`$DSH/packages/subagent/subagent-acp/src`) spawns a child through the `subprocess` seam; `llm-pi-ai` (`$DSH/packages/llm/llm-pi-ai`) is the reference provider plugin for how a plugin package is named, configured and registered. `agent-default-model` (`provider`, `model`) is consulted by every DSH entry point; the headless turn in M-21 ended with `NO_ADAPTER: no adapter registered for provider "deepseek-official"` because the kit profile never pointed the agent at a registered route.
- The gateway protocol, measured 2026-11-06 05:56Z to 05:58Z with `omp auth-gateway stdio` (omp 18.12.6, cwd `$HOME`, the operator's omp settings loading the `pi-claude-bridge` extension). One JSON object per stdin line, `{"id":<n>,"path":"/v1/messages","body":<Anthropic messages body>}`; stdout line 1 is `{"ready":true,"version":"18.12.6"}`; then one line per request, `{"id":<n>,"status":<http>,"body":<Anthropic message or error>}`; the process exits at stdin EOF.
  Text turn, 1.9 s wall including omp boot, request body `{"model":"claude-bridge/claude-haiku-5-5","max_tokens":32,"messages":[{"role":"user","content":"Reply with the single word pong."}]}`:
  `{"id":1,"status":200,"body":{"id":"msg_40c424f8df3e4ca3a3baa84f","type":"message","role":"assistant","model":"claude-bridge/claude-haiku-5-5","content":[{"type":"text","text":"pong"}],"stop_reason":"end_turn","stop_sequence":null,"usage":{"input_tokens":2,"output_tokens":4,"cache_read_input_tokens":0,"cache_creation_input_tokens":2453}}}`
  Tool turn, 2.1 s, one declared tool `{"name":"ping","description":"Answer with the current host name of the caller.","input_schema":{"type":"object","properties":{"word":{"type":"string"}},"required":["word"]}}` and the user text `Call the ping tool with word=pong and nothing else.`:
  `{"id":2,"status":200,"body":{"id":"msg_b5543bab5a494b128b58b5c8","type":"message","role":"assistant","model":"claude-bridge/claude-haiku-5-5","content":[{"type":"tool_use","id":"toolu_01HEFTqeaFVnJLV8YpvEypFV","name":"ping","input":{"word":"pong"}}],"stop_reason":"tool_use","stop_sequence":null,"usage":{"input_tokens":2,"output_tokens":57,"cache_read_input_tokens":0,"cache_creation_input_tokens":2923}}}`
  Unknown model: `{"id":3,"status":404,"body":{"error":{"message":"No available model matches \"openai-siwc/gpt-6-astra\"","type":"invalid_request_error"}}}`. Unknown path: `{"id":0,"status":404,"body":{"error":"No route: POST /v1/models"}}`.
  `stream: true` returns the whole SSE text as one line (pi-ai `auth-gateway/stdio.ts:14-16`), so there are no incremental tokens either way. Use the non-streaming body and emit the chunks from the final message.
- Unmeasured and yours to measure without a model call: whether one gateway child answers many request lines in sequence (send two `/v1/models` lines and count the reply lines; that path touches no login and no model). Decide one child per request or one long-lived child from that measurement and say so in the body. A model turn (`/v1/messages`) is not yours to send.

DATA SHAPE
Three pure translations and one process boundary. `toMessagesBody(options)` maps DSH `messages`, `system`, `tools`, `model` (strip the `claude-bridge/` prefix only if the gateway needs it; the measured turns kept it) into the Anthropic body. `toChunks(message)` maps one Anthropic message into the chunk sequence (text block: `block-start`, `text-delta`, `block-end`; tool_use block: `block-start`, one `tool-call-delta` holding the whole JSON arguments, `block-end`; then `usage`, then `finish` with the stop reason). `toError(status, body)` maps a non-200 line into the adapter's error. The boundary is a `GatewayClient` that owns the child process, writes one line per request keyed by an increasing id, and resolves the matching reply line; it parses the gateway's JSON at the boundary and nothing downstream re-checks it. Configuration rows: `command` (default `omp`), `args` (default `["auth-gateway","stdio"]`), `env` pass-through list, `providers` (default `["claude-bridge"]`), `models`.

CHANGE
1. Find the loading mechanism. From `$DSH` (bundle and cordis loader code, `docs/config-catalog.md`, how `llm-pi-ai` is named by a patch row and resolved), establish how a cordis patch row loads a plugin that is not an npm package in `node_modules`: a file path, a file URL, a `DSH_HOME` plugins directory, or only an installed package name. Record the finding with `file:line` citations in the body. If only installed package names load, the plugin is still built here and the body says what the next unit must install.
2. Write the plugin under `home/dot_dsh/plugins/omp-gateway/` in the form the loader accepts with the least build machinery (plain ESM JavaScript with the `package.json` fields the loader reads is preferred over a TypeScript build; if TypeScript is unavoidable, say why and keep the compiled output out of the tree unless the loader needs it). The three pure translations live in their own module with no process code in it.
3. Write `stub-gateway.mjs` beside it: reads JSON lines from stdin, prints the ready line, and answers each request from a fixtures file (the four measured replies above, keyed by a selector you choose: the first user text, or the presence of `tools`). It is the gateway the tests and the composition proof run against.
4. Tests with `node --test` under the plugin directory: the translations against the fixtures (text, tool_use, 404 model, 404 path), the client against the stub (request id matching, ready line consumed, child exit on EOF, an aborted `signal` kills the child), and the multi-request behaviour you measured in CONTEXT.
5. The composition proof: with `DSH_HOME` under `/tmp` and a scratch profile (or the kit's thak profile plus one overlay) that loads your plugin with `command` pointing at the stub, `agent-default-model` set to `claude-bridge` / `claude-haiku-5-5`, run one headless `dsh` turn with the user text `Reply with the single word pong.` and paste the output showing `pong` reached the agent loop. Then a second turn whose scratch agent declares a `ping` tool, showing the `tool_use` reply became a tool call in the loop. Both under `~/.dsh/bin/dsh`, cwd a scratch directory, no srt (the srt profile is M-21's unit).
6. The body `../U240-pr-body.md`: Summary (the operator's rule, shape (d), what the plugin is), Loading mechanism (CHANGE 1 with citations), Contract (guarantee: a DSH turn on provider `claude-bridge` reaches a child `omp auth-gateway stdio` and no credential, token or key is read, stored or passed by the plugin; leaves out: the kit profile rows, the srt wrapper, incremental streaming, the SIWC route until omp serves it), Verification (ACCEPTANCE lines pasted), Threats (the child command is configuration: who may set it; a reply line with a mismatched id; a child that never prints the ready line; a tool name the agent did not declare).

ACCEPTANCE
1. `node --test home/dot_dsh/plugins/omp-gateway/` exit 0 (paste the pass count).
2. The headless `pong` turn of CHANGE 5 pasted, with the stub's log line showing the request it answered.
3. The tool turn of CHANGE 5 pasted, showing the loop called the tool with `{"word":"pong"}`.
4. `grep -rn -iE 'api[_-]?key|OLLAMA|bearer|token' home/dot_dsh/plugins/omp-gateway/` prints nothing except lines in the Threats-related test names you can justify in the body.
5. The multi-request measurement pasted (the two `/v1/models` lines and the reply lines, with the exit code).
6. `make shellcheck` exit 0 if you added any shell file; otherwise state that none was added.

7. `scripts/ci/run-on-lint-files.sh shell shfmt -i 4 -sr -d`, `scripts/ci/run-on-lint-files.sh python ruff format --config ruff.toml --check` and `scripts/ci/run-on-lint-files.sh markdown prettier --check` exit 0 (the Makefile `format` target), run in the tree after the last edit. (added 2026-11-06T07:20Z under standing order 44; the heads of these units were checked by the coordinator with the same commands.)
VERIFY
The ACCEPTANCE commands in your tree with their result lines pasted into the body's Verification section. The real-login turn (the same two turns with `command` = `omp`) is the coordinator's measurement after your head is in and is recorded in `decisions.tsv`, not in your body.

CLOSURE
parser-module

TRUST
TRUST: the unit trusts the installed omp's `auth-gateway stdio` protocol as measured on 2026-11-06 and DSH's `LlmAdapter` seam at the pinned tag; it reads no credential, opens no listener, sends no model request, and does not decide the srt profile, the kit renderer rows or the install path of the plugin.

TIMEBOX
90 minutes. If CHANGE 1 shows no way to load a plugin from outside `node_modules` within the first 30 minutes, report that alone with citations and stop.

FORBIDDEN
No `/v1/messages` request to the real omp; no read of `~/.omp`, `~/.claude`, `~/.codex`, `~/.config/omp` or any credential file; no write under `~/.dsh`, `~/.omp`, `~/.agents` or `~/Workspace`; no API key, token or `apiKeyEnv` row anywhere in the plugin; no network; no edit of the renderer, the manifest or the rendered profile; no push; no `gh` call; no local bats.

WORKER RULES (standing orders 21, 27, 29, 31, 34; read `~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` lines 23 to 50)
- Never run git or edit files in `~/Workspace/dotfiles`, never push, never open or edit a PR, never edit the live store; you stop at a committed head in `/tmp/dotfiles-wt/U240` and the coordinator fetches it by path.
- Progress line beside your tree (`../U240-progress.txt`) every ten minutes at most; first edit within ten minutes.
- Commit unsigned: `git -c commit.gpgsign=false commit`. Every commit message ends with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.
- Comments explain a non-obvious why only, no phase narration. Shell comments are English shdoc.
- Follow `~/.agents/pstack/skills/poteto-mode/SKILL.md` for code shape (name the data shape first; the DATA SHAPE section above is the starting point, change it if the seam disagrees and say so).

REPORT
Status, head sha (40 hex), files changed (`git diff --stat origin/main`), the loading mechanism in one line with its citation, the ACCEPTANCE result lines, deviations. Under 16 lines, ending with `head=<40 hex>`.

STANDING
`preferences.md` (standing orders 21, 27, 29, 34, 35, 37, 41); `AGENTS.md` (Comment Policy, Test Policy, Audit); the `decisions.tsv` rows of phase `frame` (05:46:33Z), `design` (U238, 05:56:15Z) and `M-21` (U239, 05:58:16Z); the scout report at `agent://ScoutDshLoginRoute` is the coordinator's and is summarised in CONTEXT.
