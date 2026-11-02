# shiguredo/deepseek-harness

Research note for the TechnoPro harness agent kit. Written 2026-11-02 from primary
sources (GitHub API, repository files at the named refs, the fork author's gist and
blog). No shared-method document existed in `hk-research/` when this note was written,
so it follows the structure: identity, provenance, what the thing is, what it targets,
relation to the sibling repository, runtime, risk, what this dotfiles repository would
gain, open questions, sources. Every claim names the file or page it came from.

## 1. Verdict in five lines

- `shiguredo/deepseek-harness` is a **GitHub fork** of `deepseek-ai/deepseek-harness`
  (DSH), not an independent project. Its default branch `shiguredo` is upstream
  `master` at `ce7073d5` (2026-10-29) plus **one squashed commit** (`60b345ce`,
  300 files, +17,721/-1,179) by voluntas (Shiguredo Inc., Tokyo).
- "Harness" here means a **full agent runtime**: agent loop, tool registry, session
  log, sandbox, subagents, Web/Desktop UI, SDK and ACP servers, all as Cordis plugins.
  It is not a benchmark harness and not a thin tool runtime.
- It targets the **DeepSeek official API first** (`deepseek-official` route, Anthropic
  Messages wire format at `api.deepseek.com/anthropic`, V4.1 Flash and V4 Pro), and any
  other provider or local server through a **pi-ai based multi-provider adapter**
  (`openai-completions`, `openai-responses`, `anthropic-messages`, vLLM hints).
- `deepseek-ai/dsh-superagent-prototype` is **neither a fork nor a port** of the
  harness. It is a **DSH bundle** (`dsh.bundle` in its `package.json`, peer range
  `dsh ^0.2.1-alpha.2`) that runs on top of the harness as a router/worker GitHub agent.
- For this repository the realistic gains are (a) a DeepSeek/Ollama-Cloud/local-model
  seat beside Claude Code, Codex and omp, (b) reuse of the existing Claude Code and
  Codex `hooks.json` inside that seat, (c) a reference design for the long-running
  "Ticket per work item" pattern. Adopting DSH as the primary harness is not
  recommended now: developer preview, breaking changes promised, no security audit.

## 2. Identity and provenance

| Fact            | Value                                                                                                                                         | Source                                        |
| --------------- | --------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------- |
| Fork?           | Yes. `fork: true`, `parent` and `source` = `deepseek-ai/deepseek-harness`                                                                     | GitHub API `repos/shiguredo/deepseek-harness` |
| Fork created    | 2026-09-14                                                                                                                                    | same                                          |
| Default branch  | `shiguredo` (upstream uses `master`)                                                                                                          | same                                          |
| Divergence      | `compare/master...shiguredo:shiguredo`: ahead 1, behind 0, 300 files                                                                          | GitHub API compare                            |
| The one commit  | `60b345ce`, author voluntas <nakai@shiguredo.jp>, committer date 2026-10-30, parent `ce7073d512` (upstream master head of 2026-10-29)         | GitHub API commit                             |
| Commit message  | Only a link to the author's gist describing the fork                                                                                          | same                                          |
| Version in tree | `@deepseek-ai/dsh-root` 0.2.2-alpha.2; the branch contains both 0.2.2-alpha.2 and 0.2.1-rc.5 per the gist                                     | `package.json`, gist                          |
| Upstream size   | 268,596 stars, 32,600 forks, created 2026-08-13, topics `ai-agents cordis dsh dsh-plugin`                                                     | GitHub API                                    |
| Fork size       | 113 stars, 8 forks, 13 issues, no topics                                                                                                      | GitHub API                                    |
| README          | Identical to upstream (same text; still says `git clone deepseek-ai/deepseek-harness`)                                                        | both READMEs                                  |
| License         | MIT (both)                                                                                                                                    | LICENSE                                       |
| npm             | `@deepseek-ai/dsh` latest 0.2.1-rc.5 (2026-10-29), tag `alpha` 0.2.2-alpha.2. Shiguredo publishes nothing to npm; the fork is run from source | `npm view`                                    |

Shiguredo's own description (blog, 2026-10-06, and the gist updated 2026-10-30): they
adopted DSH as the company harness, found the official build "a little hard to use",
and keep **one commit** on top which they rebase ("積極的に追従"). They say they did not
package the changes as plugins because the fork is for internal use. The company's
LLM setup (blog, 2026-10-03): Ollama Cloud Team plan for everyone, DeepSeek V4.1 Flash
and GLM 5.3 Flash as daily models, Codex for research, Claude Code cancelled for all but
the author, two DGX-Spark-class boxes running DeepSeek V4 Flash under vLLM for
self-hosted GitHub Actions review. They state "long runs are overwhelmingly DSH's
strength; long investigations are DSH only."

### 2.1 What the Shiguredo commit changes (from the gist, spot-checked in the tree)

| #   | Change                                                                                                                                                                                                                                                                                         | Where                                                           | Verified                                                        |
| --- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------- | --------------------------------------------------------------- |
| 1   | Japanese UI (`locale/ja.json` per package) and font defaults that do not pin CJK families                                                                                                                                                                                                      | `packages/client/ui-theme`, many `locale/` dirs                 | `packages/client/ui-chat/locale/ja.json` exists on `shiguredo`  |
| 2   | Composer chip showing `owner/repo:branch`, detached id or worktree name                                                                                                                                                                                                                        | `packages/api/workspace-git`, `packages/client/ui-git-branch`   | both dirs appear only in the fork diff                          |
| 3   | Workspace name on flat Session rows                                                                                                                                                                                                                                                            | `packages/client/ui-workspace`                                  | diff                                                            |
| 4   | **Bundled Ollama Cloud provider catalog**: endpoint `https://ollama.com/v1`, protocol `openai-responses`, 21 models incl. `deepseek-v4.1-flash:1017`, V4 Pro, GLM 5.x, Kimi K2/K3, GPT-OSS, Nemotron 3, Mistral                                                                                | `packages/llm/llm-pi-ai/src/bundled-catalog.ts`                 | file is 14,207 bytes on `shiguredo`; **404 on upstream master** |
| 5   | **Peak-hour routing**: DeepSeek models on Ollama Cloud have a declared peak (UTC Mon-Fri 12:00-18:00 = JST 21:00-03:00); during it the adapter can switch to a configured fallback provider/model, logs still show the configured route                                                        | `llm-pi-ai/src/peak.ts`, `ui-settings-models`                   | diff                                                            |
| 6   | Ollama Cloud web search and fetch providers                                                                                                                                                                                                                                                    | `packages/web/web-ollama-api`, `ui-settings-web-search-ollama`  | diff                                                            |
| 7   | Provider name shown in the model selector; "自動" while peak routing is active                                                                                                                                                                                                                 | `ui-model-selection`                                            | diff                                                            |
| 8   | Message timestamps with a JST/UTC/local setting                                                                                                                                                                                                                                                | `ui-chat` (44 files in diff)                                    | diff                                                            |
| 9   | Change a Session's working directory without changing process cwd                                                                                                                                                                                                                              | `packages/session/working-directory`                            | diff                                                            |
| 10  | Per-instance state under `$DSH_HOME/instances/<port>/` for several Web servers                                                                                                                                                                                                                 | `home-paths`, `web-app`, `app-boot`                             | diff                                                            |
| 11  | **Session-log upload to the official DeepSeek API is opt-in** (`session-log-deepseek.enabled` default `false`; upstream default is `true`)                                                                                                                                                     | `packages/session/session-log-deepseek`                         | upstream README confirms default `true`                         |
| 12  | "1017" release badge for the Ollama-hosted Flash build, via catalog `badge`                                                                                                                                                                                                                    | `llm-pi-ai`                                                     | diff                                                            |
| 13  | **Git push guard** plugin: `tools/pre-execute` detects `git push` in `bash`/`pwsh`/`terminal_send` including `sh -c`, `eval`, `cmd /c`, `pwsh -Command` nesting; asks a human question, only "Allow" proceeds; fail-closed when nobody can answer; scripts, aliases, `gh pr merge` not covered | `packages/guard/git-push-guard`, `ui-git-push-guard` (28 files) | both dirs exist on `shiguredo`                                  |
| 14  | "時雨堂組み込みプラグイン設定" group on the Plugins page hosting 6 and 13                                                                                                                                                                                                                      | `ui-plugin-manager`                                             | diff                                                            |

Changes 4, 5, 11 and 13 are the ones with substance for anyone else. Everything else is
UI polish for a Japanese team.

## 3. What "harness" means in this project

The upstream `docs/architecture.md` is explicit: Cordis is the framework; "every part
of the product is a plugin, including the model adapter, the tool registry, the session
log, and the agent loop itself". So "harness" is the whole **agent runtime**:

- **Agent loop** (`core/agent-loop`): turn = zero or more steps; step = one model
  request plus its tool calls. Durable session events (`turn/*`, `step/*`,
  `user/message`, `assistant/message`, `tool/*`) are the only source of model
  context ("model-visible means logged"; every request must be reconstructable from
  the log). Live extension points are `agent/*` and `tools/*` events.
- **Tool runtime** (`core/tools`, `shell/*`, `fs/*`, `sandbox/*`, `terminal`, `jobs`,
  `mcp-client`, `skill/*`): a scoped registry with `tools/pre-execute` and
  `tools/post-execute` seams. "Seams" (service definition + provider + consumer) are
  how filesystem, subprocess, shell and LSP can be pointed at a remote sandbox
  together.
- **Not a benchmark harness.** `benchmarks/` and `test:bench` exist but measure the
  harness itself (memory pressure, npm resolution), not models.
- **Surfaces**: `dsh web` (Web UI on 3080), Electron desktop, `headless` (one-shot
  CLI with `--json`), `sdk` (JSON-RPC stdio, plus a Python SDK wheel) and `acp`
  (Agent Client Protocol stdio) are **profiles**, i.e. ordered stacks of bundle patch
  files over `cordis.patch.yml`.
- **Composition model**: profile -> bundles -> `cordis.patch.yml` -> home patch ->
  `--patch` overlays. Any row can be replaced from configuration;
  `dsh --profile web --dump-config` prints the tree. HMR recomposes on YAML edits.
- Theory: Cordis is described in arXiv 2608.25512 (Shi, Zhang, Cui, 2026-08-26),
  "revertible effects" and "reactive coeffects" for hot plug/unplug of components.

## 4. Model and provider targets

Two adapters are shipped against one `StreamChunk` vocabulary (agent note
`2026-06-13-twin-llm-adapters.md`):

| Adapter                                       | Route                  | Protocol                                                                                                                                                                                                                               | Notes                                                                                                                                                                                                                                                                                       |
| --------------------------------------------- | ---------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `dsh-llm-deepseek` (+ `-api-key`, `-account`) | `deepseek-official`    | Anthropic Messages format at `https://api.deepseek.com/anthropic`; `DEEPSEEK_API_KEY` or DeepSeek account sign-in                                                                                                                      | Defaults advertise `deepseek-flash` (text+image) and `deepseek-v4-pro`; 1,048,576-token context; reasoning effort off/low/high/max; Files API for images. Official requests also carry `dsh_session_log` (session log upload, default on) and `dsh_plugin_packages` (plugin inventory)      |
| `dsh-llm-pi-ai`                               | any name you configure | `@earendil-works/pi-ai` ^1.3.0 catalogs and wire protocols: `openai-completions`, `openai-responses`, `anthropic-messages`; catalog providers `anthropic`, `openai`, `moonshotai`, `zai`, Azure, Bedrock, Vertex, Codex OAuth and more | `apiKeyEnv` credential references, `baseURL` override, hand-declared gateways, `thinkingTokenBudgetField` and `vllmPriority` for self-hosted Chat Completions servers, `compat.thinkingFormat: deepseek`. Keyless local servers need a placeholder `apiKeyEnv` or an `Authorization` header |

So the answer to "DeepSeek API or local models" is **both, with DeepSeek official as the
privileged route**: only the official route gets the twin direct-fetch adapter,
account sign-in, the session-log and plugin-inventory request fields, and the
`CLIENT_UPGRADE_REQUIRED` gating. Local models (Ollama local, vLLM, LM Studio) go
through `llm-pi-ai` as a custom provider. The Shiguredo fork adds Ollama **Cloud** as a
bundled catalog because upstream's third-party list lacks it.

Noteworthy overlap with this repository: omp carries legacy `@earendil-works/pi-*`
shims (see `docs/pi-claude-bridge.md`), and DSH's multi-provider adapter is built on
`@earendil-works/pi-ai`. Both sit on the same pi provider catalog lineage.

## 5. Relation to deepseek-ai/dsh-superagent-prototype

| Question                     | Answer                                                                                                                                                                                                                                                                                                                                                                                                                                          | Evidence                                                              |
| ---------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------- |
| Fork of the harness?         | No. `fork: false`, created 2026-10-31, one release commit, 9,015 stars in two days                                                                                                                                                                                                                                                                                                                                                              | GitHub API                                                            |
| Port?                        | No. It contains no agent loop, tools or model adapters of its own                                                                                                                                                                                                                                                                                                                                                                               | file tree: `src/app`, `src/core`, `src/client`, `prompts/`, `skills/` |
| What then?                   | A **DSH bundle**: `package.json` has `dsh.bundle.patch: ./cordis.patch.yml`, `dsh.client.platform: web`, `engines.dsh: ^0.2.1-alpha.2`, and peer-depends on `@deepseek-ai/dsh-*` packages. `cordis.patch.yml` inserts the `dsh-superagent` plugin plus two agent presets (`dsh-superagent-worker`, `dsh-superagent-router`) built from upstream plugins (`dsh-tool-bash`, `dsh-bash-sandbox`, `dsh-tool-subagent`, `dsh-compaction-basic`, ...) | `package.json`, `cordis.patch.yml`                                    |
| Direction of reference       | The prototype references the harness (README links deepseek.com/harness; docs say "Worker subagents use DeepSeek Harness's `standard` preset"). The harness does not reference the prototype                                                                                                                                                                                                                                                    | both READMEs                                                          |
| Relation to Shiguredo's fork | None direct. The prototype needs `dsh` in its `engines.dsh` range; the fork is 0.2.2-alpha.2, which satisfies `^0.2.1-alpha.2`, so it should load on the fork too (not tested)                                                                                                                                                                                                                                                                  | `package.json`                                                        |
| Status                       | "Research prototype for reference only, not an official DeepSeek product", adapted for publication, not identical to the internal version described in the article _Exploring Super-agent Design: Towards a More Autonomous Agent System_ (2026-10-31)                                                                                                                                                                                          | README                                                                |

What the prototype is: a proactive coding agent for **one GitHub repository** (and
optionally Feishu). Domain model (`docs/001-domain.md`): Source -> Trigger -> Thread ->
Eval (gate + assessment) -> Decision -> Ticket with an immutable Mandate -> Assignment
to an Executor Session (`worker-<ticket id>`, own directory, usually a `git worktree`)
-> Channel replies. Authorization (`docs/002-authorization.md`): allowed lists, an
admission table per receiving scope, accept modes `off` / `observe` (default, records
what it would have done) / `auto`. Execution (`docs/003-execution.md`): shell commands
move to background jobs after 5 s so a worker keeps taking messages; concurrency slots;
30-minute background limit; retry/restart semantics; stored-work effects. Both presets
run with `danger-full-access` as the operator's OS user (`docs/006-deployment.md`).
Prerequisites: Node 22.19+ or 24+, pnpm, git 2.32+, Python 3.8+, tmux, `gh` 2.48+, a
dedicated agent GitHub **user** account (a GitHub App cannot be the agent because it
reads notifications). Setup is designed to be driven by a coding agent reading
`SETUP.md`.

Self-reported numbers from the article as relayed by secondary press (MarkTechPost
2026-11-01, citing ifeng and 53ai; not independently verified): simulated streams of
~300 messages with ~20 real requests, p95 completion 15.7 min vs 29.5 min for a single
session with subagents; router batch size 1.0 -> 2.8 as arrivals rose to 40/min.
Only synthetic messages and simulated tools; coding quality was not measured.

## 6. Language and runtime

- **TypeScript**, ESM, pnpm workspaces (`packages/*/*`, `apps/*`, `native/system`,
  `vendor/*`, `website`). Root `package.json` requires **Node >= 24.9.0** and
  `pnpm@11.28.5`; the npm CLI package is launched with `npx @deepseek-ai/dsh web`.
  A native addon lives under `native/system`.
- Build: `tsx scripts/build.ts`, `tsdown`, `tsc -b`; lint `oxlint`; tests `vitest`
  (unit, e2e, snapshot, web, bench, expected); ~100 `verify-*` gates (doc links,
  translation pairing, catalogs, persistence formats). The repository enforces
  bilingual docs (`*.zh.md` with `*.i18n.yaml` hash records) and dated agent notes
  under `.agents/notes/`.
- Desktop: Electron, signed packages for macOS arm64/x64 and Windows x64.
- Python SDK: a wheel that packages the same `dsh` CLI and launches
  `dsh --profile sdk`.
- Operational footprint: Web UI binds `127.0.0.1:3080`; state under `$DSH_HOME`
  (`~/.dsh`): `profiles/<name>/{package.json,cordis.patch.yml}`, `.credentials.yaml`,
  sessions. Plugins install per profile through pnpm (`dsh plugin --profile <name>`).

## 7. Maturity and risk

- `README`: "developer preview ... THERE WILL BE COMPATIBILITY-BREAKING CHANGES."
  Releases are weekly rc/alpha tags (rc.2 on 10-17, rc.3 10-23, rc.4 and alpha.2 10-28,
  rc.5 10-30).
- `SAFETY.md`: not security-audited; executes model-generated commands; sandboxing
  "does not guarantee isolation"; run in a disposable VM or container.
- **Telemetry to the vendor**: with the official DeepSeek route, shipped profiles send
  the canonical session log (`dsh_session_log`, up to 8 MiB per request) and the plugin
  inventory (`dsh_plugin_packages`) with model requests, default on. Shiguredo flipped
  the session-log default to off; the blog calls the upstream default "fairly scary".
  Any TechnoPro profile must set `session-log-deepseek.enabled: false` or avoid the
  official route.
- The fork is one person's squashed commit with no CI of its own visible, rebased onto
  upstream at will. Pinning a fork SHA is the only reproducible way to consume it.
- Node >= 24.9 is newer than what this repository's mise toolchain may pin; check
  before adding a `dsh` asset.

## 8. What this dotfiles repository would gain

Context: this repository manages Claude Code, Codex and omp seats through
`home/dot_agents/agent-config.yaml` (`model_profiles` express/standard/review/deep/
security/audit; omp routes to `claude-bridge/*` or `openai-siwc/*`), installs
`pi-claude-bridge` as a patched omp extension (`docs/pi-claude-bridge.md`), renders
hooks and command policies per vendor, and runs hcom seats for orchestration. There is
no DeepSeek or local-model route anywhere in it today (grep: zero hits).

### 8.1 Gains that are real

1. **A fourth seat vendor with cheap, fast, non-US-lab models.** A `dsh` seat
   (`dsh --profile headless` for one-shot jobs, `dsh --profile sdk` or `acp` for
   driven sessions) gives the kit DeepSeek V4.1 Flash / V4 Pro, GLM, Kimi, GPT-OSS and
   self-hosted vLLM/Ollama through one config surface. That is the only credible route
   in the kit for on-prem or client-restricted engagements where Anthropic/OpenAI
   endpoints are not allowed. Shiguredo's measured experience (600 tok/s bursts on
   Ollama Cloud, "no particular gap to Opus 4.8 with repeated skill-driven review") is
   one data point, not a benchmark.
2. **Reuse of existing hooks instead of rewriting them.** Upstream ships
   `dsh-hooks-claude-code` (runs a Claude Code `hooks.json` or settings `hooks` key at
   session/prompt/tool/stop/subagent moments, can block with model-visible reasons) and
   `dsh-hooks-codex` (five Codex hook points). Both are `experimental/` but mean the
   kit's rendered Claude and Codex hook files could gate a DSH seat with no new code.
   `dsh-experimental-claude-code-mods` does the same for Claude Code mods.
3. **Cross-harness delegation in both directions.** `dsh-subagent-claude-code` and
   `dsh-subagent-codex` run an unattended native Claude Code or Codex session as a
   DSH subagent tool; `dsh-subagent-acp` spawns any ACP agent as an isolated child;
   `dsh --profile acp` lets an ACP-speaking client (editors, or omp if it gains an ACP
   client) drive DSH. The kit's cross-vendor audit idea (`audit` profile) maps onto
   this directly: a DeepSeek-run audit of a Claude- or Codex-authored changeset.
4. **A written reference for the "proactive repository agent" shape.** The prototype's
   domain model (Mandate, Ticket, Subscription, accept mode `observe`, stop by impact
   not effort, one question at a time) is a clean, documented design the kit can cite
   in its ADRs even if it never runs the bundle. Its `docs/000-philosophy.md` is
   directly reusable as operator guidance.
5. **Specific fork ideas worth copying as policy, not code.** The git push guard
   (pre-execute interception, fail-closed without an answerer, explicit non-coverage
   of aliases and `gh pr merge`) matches this repository's `command_policy` approach
   (`gh-alias` rule). Peak-hour provider routing is a cost pattern the kit's seat
   policies could express for Ollama Cloud. Session-log opt-out is a mandatory default.

### 8.2 Gains that are not real, or not yet

- **Not a replacement for omp/pi-claude-bridge.** The bridge exists to run Claude
  models on the claude.ai login inside omp. DSH's `anthropic` route is API-key only and
  offers no ChatGPT sign-in for OpenAI (README limitation), so it cannot take over the
  subscription-based seats this repository already has.
- **Not a benchmark harness.** If the kit wants model evaluation, DSH gives it nothing
  beyond `headless --json` as a runner.
- **The Shiguredo fork specifically** is not a dependency to take. Its valuable parts
  (Ollama Cloud catalog, push guard, session-log default) are small and should be
  re-expressed as a profile `cordis.patch.yml` plus, if needed, a kit-owned plugin,
  rather than tracking a one-commit personal fork. Upstream `llm-pi-ai` already accepts
  a hand-declared `ollama-cloud` route with `api: openai-responses`,
  `baseURL: https://ollama.com/v1` and a `models` list, which covers change 4 without
  the fork.
- **Superagent prototype as a running service** needs tmux, a dedicated GitHub user
  account with write access, `danger-full-access` workers as the operator's OS user,
  and github.com only (no GHES). Treat it as reading material until the kit has a
  disposable host for it.

### 8.3 Recommended shape (for the ADR)

- Add DSH as an **optional seat vendor**, pinned to an upstream release tag (not the
  fork), installed per profile under `$DSH_HOME/profiles/<kit-profile>/`, with a
  kit-rendered `cordis.patch.yml` that: sets `session-log-deepseek.enabled: false`,
  declares `ollama-cloud` and any on-prem vLLM route under `llm-pi-ai`, mounts
  `dsh-hooks-claude-code` pointed at the kit's rendered Claude hooks, and selects the
  `headless`/`sdk` profiles for automation. Render it from `agent-config.yaml` like the
  omp overlays, so model ids live in `model_profiles` only.
- Keep DeepSeek official API as **opt-in per engagement** because of the request
  metadata it carries; default seats to Ollama Cloud or on-prem.
- Record the fork's 14 changes as a watch list; revisit if Shiguredo publishes them as
  `dsh-plugin` packages (they said they will not) or upstream absorbs them.

## 9. Open questions and unverified items

- Not tested locally: whether the `shiguredo` branch builds on this machine (Node
  > = 24.9 required) or whether the superagent bundle loads on 0.2.2-alpha.2.
- The super-agent article's numbers are secondary-source only; the English original
  was not fetched.
- `dsh-hooks-claude-code` coverage of this repository's hook set (which events, matcher
  semantics, `settingSources`) needs a line-by-line check against
  `home/dot_claude/` before relying on it.
- Whether DSH's `acp` profile and omp can interoperate today was not checked; omp's ACP
  client support is unknown from this note's sources.
- The fork's peak-routing window is hard-coded for Ollama Cloud's DeepSeek rows; the
  kit would need its own declaration for other providers.

## 10. Sources

- GitHub API: `repos/shiguredo/deepseek-harness` (fork metadata, branches, commit
  `60b345ce`), `repos/deepseek-ai/deepseek-harness` (metadata, releases, tree,
  contents), `repos/deepseek-ai/deepseek-harness/compare/master...shiguredo:shiguredo`,
  `repos/deepseek-ai/dsh-superagent-prototype` (metadata, contents).
- Upstream files at `master`: `README.md`, `SAFETY.md`, `package.json`,
  `docs/architecture.md`, `docs/user/guide/providers.md`, `apps/cli/README.md`,
  `packages/llm/README.md`, `packages/llm/llm-pi-ai/{README.md,package.json}`,
  `packages/llm/llm-deepseek/README.md`,
  `packages/session/session-log-deepseek/README.md`,
  `packages/experimental/{hooks-claude-code,hooks-codex,claude-code-mods}/README.md`,
  `packages/subagent/{subagent-claude-code,subagent-codex,subagent-acp}/README.md`,
  `packages/bundle/headless/README.md`,
  `.agents/notes/implemented/architecture/2026-06-13-twin-llm-adapters.md`.
- Fork files at `shiguredo`: `README.md`, `packages/llm/llm-pi-ai/src/bundled-catalog.ts`
  (existence/size), `packages/guard/git-push-guard/`, `packages/client/ui-chat/locale/`.
- Prototype files at `main`: `README.md`, `SETUP.md`, `package.json`,
  `cordis.patch.yml`, `docs/000-philosophy.md`, `docs/001-domain.md`,
  `docs/002-authorization.md`, `docs/003-execution.md`, `docs/006-deployment.md`,
  `docs/007-architecture.md`.
- voluntas, "DeepSeek Harness 時雨堂 fork 変更情報" (gist
  34ac1f8ced7052d69dc37f54fc57155c, updated 2026-10-30).
- voluntas, "DeepSeek Harness を fork して使っている話" (voluntas.ghost.io, 2026-10-06);
  "2026 年 10 月前半の LLM 利用状況" (2026-10-03).
- arXiv 2608.25512, "A Programming Paradigm for Spatiotemporal Composability".
- MarkTechPost, "DeepSeek Open-Sources dsh-superagent, a Router-Worker Coding Agent"
  (2026-11-01), for the article's self-reported figures.
- `npm view @deepseek-ai/dsh` (2026-11-02).
- This repository: `docs/pi-claude-bridge.md`, `home/dot_agents/agent-config.yaml`
  (`model_profiles`, `interactive_profile`), `README.md`.
