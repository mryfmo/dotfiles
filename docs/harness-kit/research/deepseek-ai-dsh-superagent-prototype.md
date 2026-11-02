# deepseek-ai/dsh-superagent-prototype

| Field                          | Value                                                                                                                                                                                           |
| ------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Repository                     | https://github.com/deepseek-ai/dsh-superagent-prototype                                                                                                                                         |
| Tagline                        | "Towards a More Autonomous Agent System"                                                                                                                                                        |
| Researched                     | 2026-11-02 (repo cloned at commit `6337fc8`)                                                                                                                                                    |
| Owner                          | GitHub organization `deepseek-ai` (the same org as `deepseek-ai/deepseek-harness`)                                                                                                              |
| Created / last push            | 2026-10-31 09:32 UTC / 2026-10-31 12:05 UTC                                                                                                                                                     |
| History                        | One commit: `feat: add the dsh-superagent research prototype`, author "DeepSeek Harness Team <team@dsh.dev>"                                                                                    |
| License                        | MIT                                                                                                                                                                                             |
| Language / size                | TypeScript, 216 tracked files, ~15.6k lines under `src/`, ~15k lines under `tests/`                                                                                                             |
| Package                        | `dsh-superagent` 0.1.0, `private: true` (not published to npm; installed as a linked DeepSeek Harness bundle)                                                                                   |
| Stars / forks                  | 9,015 / 910 at research time                                                                                                                                                                    |
| Issues, PRs, Discussions, Wiki | All disabled                                                                                                                                                                                    |
| Companion article              | "Super-agent 设计探索：迈向更自主的 Agent 系统" (Exploring Super-agent Design: Towards a More Autonomous Agent System), DeepSeek Harness Team on DeepSeek's official WeChat account, 2026-10-31 |

**Method note.** The assignment refers to a "shared method", but `$TMPDIR/hk-research/` was empty when this research started, no method file exists in the workspace, and no prior session in the archive mentions one. The sibling notes that appeared in the same directory during the work (`shiguredo-deepseek-harness.md`, `tester-army-e2e.md`, and others) record the same finding and converge on one shape: verdict first, vitals, what the thing is, relation to its siblings, runtime, reusable parts, fit with this dotfiles repository's agent kit, risks, and sources with first-hand verification marked. This report follows that shape.

## 1. Verdict in brief

- **It is a DeepSeek artifact, but not a DeepSeek product.** Published in the official `deepseek-ai` org, committed by the "DeepSeek Harness Team", and announced on DeepSeek's official WeChat account. The README's first line says: "Research prototype for reference only, not an official DeepSeek product."
- **"Superagent" is defined by the maintainers as an agent form, not a model or a product**: a continuous entity that breaks the binding between an agent and a single manually started session, with four properties (continuity, efficiency, proactivity, persistence) and five architectural modules (two-layer Router/Worker, event-driven operation, human-centered interaction, compute/state/environment separation, Watchdog).
- **What ships is a proactive GitHub coding agent** packaged as a DeepSeek Harness bundle: it watches one GitHub repository (and optionally Feishu), turns allowed requests into Tickets, runs each in its own harness Session and git worktree, replies in the original conversation (often with a pull request), and exposes a web panel showing only what needs a person.
- **About half of the article's design is in the code.** Router/Worker split, event filtering, subscriptions with direct delivery, Router batching, Inline & Spill context cards, and rule-gated proactive work are implemented. The asynchronous ReAct loop (only a 5-second-to-background approximation), compute/state separation, remote execution daemons ("Bring Your Own Machine"), and a model-driven Watchdog are not.
- **Relation to `shiguredo/deepseek-harness`: none directly.** That repository is a one-commit-ahead fork of the upstream harness by the Japanese company Shiguredo. Its README is byte-identical to upstream's and says nothing about the fork. The prototype does not reference it, and the fork's diff does not mention "superagent".
- **The most reusable parts are the domain model, the prompt corpus, and the design article**, not the runnable code. The code is tightly bound to pre-release DeepSeek Harness packages and to the `gh` and `lark-cli` CLIs. There is no evaluation harness in the repository; the experiments exist only as numbers in the article.

## 2. Provenance: how official, and what "prototype" commits them to

Evidence that this comes from DeepSeek:

- Hosted under the `deepseek-ai` GitHub organization alongside `deepseek-harness`.
- The sole commit is authored "DeepSeek Harness Team <team@dsh.dev>".
- The companion article was published on DeepSeek's official WeChat account (byline "DeepSeek 产品部 / DeepSeek Harness 团队") and on DeepSeek's verified Zhihu account the same evening. The translated article credits Yujia Qiao as implementer and author, with sixteen named reviewers from the team.
- The article's conclusion says an internal Super-agent instance "is already running continuously" and "participates in everyday issue reproduction and fixes, responses to code reviews, and development of DeepSeek Harness itself."

What the maintainers explicitly disclaim (README, verbatim):

> Research prototype for reference only, not an official DeepSeek product. This code grew out of our team's day-to-day development work, with much of the engineering done by coding agents. Treat it as research code, not production-ready software. It may still contain bugs, and its coding style and engineering practices may be inconsistent. Review and adapt it before using it in your own environment.
>
> We have adapted it for publication, so it is not identical to our internal version or the implementation described in _Exploring Super-agent Design: Towards a More Autonomous Agent System_. Some designs discussed in the article are directions for future development and are not implemented in this prototype.

What "prototype" commits them to in practice:

- **Nothing beyond the snapshot.** Issues, pull requests and discussions are switched off. There is no changelog, no release, no roadmap, no versioning promise, and no public bug channel. The only commit is the publication commit.
- **Divergence from the internal system is declared up front.** The public code was "adapted for publication", so behaviour and edge cases may differ from what the team actually runs.
- **The underlying harness is itself pre-release.** The prototype's `engines.dsh` range is `^0.2.1-alpha.2`; the docs pin `@deepseek-ai/dsh@0.2.1-rc.3`. The upstream harness README states "THERE WILL BE COMPATIBILITY-BREAKING CHANGES", and its `SAFETY.md` says it "has not undergone a security audit and must not be treated as secure or production-ready."
- **Engineering by coding agents is acknowledged.** The repository's own conventions (one sentence per line in prompt files, a `docs.spec.ts` that enforces that numbered documents only link backwards, a `class-docs.spec.ts` requiring a JSDoc block on every class) read as rails for agent authorship.

Treat it as a dated reference implementation that may never receive a second commit.

## 3. What "superagent" means in the maintainers' words

From the design article (section 1):

> To move beyond these limitations, we need to break the binding between an agent and a single manually initiated session. The agent should become a continuous entity that can retain context across sessions and advance several complex tasks at once without interference. We call this form of agent, and its system architecture, a Super-agent.

The motivating claim is that the bottleneck has moved from model capability to human attention: "one person can usually keep track of only three to five active Sessions at a time. Under this design, the ceiling for a single task is set by model capability; the ceiling for multiple tasks is set by human attention."

Four defining characteristics, in their words:

| Characteristic | Their gloss                                                                                                                                                                                     |
| -------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Continuity     | Users interact in familiar channels (IM, GitHub comments) and "it feels as though there is always just one agent". A plan changed in IM then revised in a PR comment is understood as one task. |
| Efficiency     | Responds quickly, runs multiple complex tasks in parallel, "can accept the next instruction without waiting for the previous command or task to finish".                                        |
| Proactivity    | Observes environmental events and acts "without waiting for users to issue every instruction. When no intervention is needed, it stays quiet."                                                  |
| Persistence    | "Always online", connected to real working environments, auto-recovers from failures during long-running operation.                                                                             |

Five modules they say form the basic framework: (2) a two-layer architecture, (3) event-driven operation, (4) human-centered interaction, (5) separation of compute, state and environments, (6) a Watchdog. They stress this is systems engineering, not new theory: "we have applied classic engineering ideas from computer systems to building agent systems." The article leans on fast path / slow path, batching, cache inline/spill, speculative execution, compute-storage separation and external control loops as its vocabulary.

The repository's own philosophy document narrows this into one operating principle for the shipped agent: **"Take as little human attention as possible, and give as much value as possible."** Everything in the design is judged by the attention it costs. The agent "acts only when asked, or when a written rule allows it", "speaks only when a person must act or can use a result", "asks one concrete question at a time", "stops by impact, not by effort", and "reports honestly".

A useful distinction the article draws against "agent teams": a team lead decomposes one task and carries a heavy reasoning load, whereas the Super-agent Router "handles only high-level relationships and assignments between tasks; it does not need to break down individual tasks internally." They note "a lighter model can often provide both speed and good results" for the Router, while Workers "usually need the most capable model available."

## 4. Architecture

### 4.1 Conceptual (from the article)

- **Router layer**: one persistent LLM Session that handles all human interaction and task assignment, "may not even have a Bash tool", and acts as the global sequence point and memory. Events arriving during one inference round accumulate and are processed together next round, giving natural batching.
- **Worker layer**: one isolated Session per task with full tools. Workers never talk to humans directly; they report to the Router, which replies. Workers may themselves spawn subagents or be an agent team.
- **Triggers and two-stage filtering**: deterministic code (allowlists, source scope, bot lists) is the fast path; the LLM judging against prompt-written policies is the slow path.
- **Threads, Subscriptions, direct delivery**: once a Worker owns a Thread (a PR, an IM topic), later events on it are delivered by code straight to that Worker, bypassing the Router. Subscription is many-to-many.
- **Inline & Spill and Chain of Recall**: inject summaries plus IDs of related objects; spill long content behind a read pointer; every retrieved object carries the IDs for the next hop.
- **Speculative execution**: e.g. a "silently reproduce and fix" rule that works in the background and only speaks if it finds a simple fix.
- **Asynchronous ReAct loop**: tool calls become `start()`/`stop()`, results arrive later as events, so the session stays full-duplex.
- **Compute / state / environment separation**: stateless cloud agent loop, session state in a database, execution via a lightweight daemon on the user's own machine.
- **Watchdog**: an independent agent Session on a schedule that judges whether Workers make substantive progress, repairs failures, and can be asked in natural language to change the main system's prompts or rules.

### 4.2 Implemented (from the repository)

The code renames the layers: the Router is the **main Session** (`orchestrator` in code and prompts) and a Worker is an **Executor Session** (`worker`). The domain model in `docs/001-domain.md` is the real spine of the implementation.

**Domain concepts** (all persisted in one SQLite file): Source, Trigger, Thread, Correlation, Channel, Policy, Eval (two layers: a deterministic gate and a model assessment), Mandate (immutable grant recording policy version, scope, strength, matched rules and sender identity), Ticket, Assignment, Subscription. Decisions are `accept`, `stop`, `ignore`, `unavailable`. Strength is `explicit` or `inferred`. Worker reports are `progress`, `waiting`, `ready`, `blocked`, `failed`, `dropped`.

**Flow**: a Source polls GitHub (notifications, subscribed issues/PRs, CI) or Feishu (events, history, topic polls) and emits Triggers. A Trigger fans out as context to Tickets subscribed to its Threads. A human message that reached a Ticket stays with that Ticket's Executor. Everything else enters Eval on its primary Thread, batched. Accepting creates a Ticket with a Mandate, subscribes its Threads, posts an acknowledgement, and creates an Assignment to the Executor.

**Planner / Router**: the main Session runs the `dsh-superagent-router` agent preset. It has 14 application tools (`orchestrator_route` taking 1 to 20 decisions in one call, `orchestrator_eval` / `orchestrator_eval_read` / `orchestrator_eval_decide` for proactive assessment, `orchestrator_reply`, settings and prompt saves, etc.) plus the harness's `bash`, `read`, `skill` and job tools. Its preset disables file write and edit, subagents, web, todo and any tool that asks or presents to a person. A `noWait` guard refuses `sleep`, shell timeouts over 30 s and job waits over 5 s so the Router never blocks. Prompts tell it to make no technical decisions and to write routing notes of at most 30 words.

**Sub-agents / Workers**: one Executor Session named `worker-<ticket id>` and one directory per Ticket (by default a `git worktree` created by an operator-defined prepare command). Workers run under the `dsh-superagent-worker` preset with full tools, shell commands moved to a background job after 5 seconds, and the ability to spawn harness subagents (which run under the harness's `standard` preset). Workers have six application tools (`orchestrator_ack`, `orchestrator_report`, `orchestrator_read`, `orchestrator_thread_follow`, `orchestrator_thread_unrelated`, `orchestrator_trigger_handback`). Concurrency is a slot count (`maxWorkers`) with one extra slot reserved so a human message can always wake a Ticket. Background work after a turn has 30 minutes before jobs are killed.

**Tools to the outside world** are CLIs, not SDKs: GitHub via a `gh` wrapper signed in as a dedicated agent account, Feishu via `lark-cli` in bot-only strict mode. Setup writes command shims and a replacement git config so workers can only use the agent's credentials by default (the docs are explicit that this is a default, "not a security boundary").

**Memory / state**: there is no long-term semantic memory. State is one SQLite database (`triggers`, `dispositions`, `threads`, `tickets`, `decisions`, `effects`, `outbox`, `kv`), a durable effects queue with backoff, and the harness's own session persistence. `src/core/memory.ts` is only an in-memory repository implementation for tests. Recall is implemented as the article's Chain of Recall: every card shows IDs, every ID is readable through `orchestrator_read` resources (`ticket/<id>`, `thread/<key>`, `trigger/<id>`, `github/pulls/<n>/thread/<comment id>`, paged lists with `next_offset`), and long content is truncated with a read pointer. The article itself names long-term memory as the main open scalability problem. Nothing deletes old records yet.

**Human interface**: a React panel inside the harness Web UI with tabs Overview, Source, Trigger, Eval, Execution, Settings, designed around three questions ("Does anything need me now? Is the system healthy? What is the history of one piece of work?"). A local HTTP management API at `/orchestrator/api/` (loopback only, custom header required) drives the panel and is also what `SETUP.md` tells a coding agent to call.

**Code structure**: `src/core` (pure, synchronous, transactional Engine split into Intake, Evals, Tickets, Assignments, Replies; no I/O), `src/app` (Runtime composition root, Store, Effects, Settings, Prompts, Sessions, MasterAssessor, tools, HTTP, views), `src/sources` (a `SourceKind` protocol plus GitHub and Feishu implementations), `src/executor` (the harness-backed executor and background-job handling), `src/client` (panel). Role interfaces are `Pick`s of the Engine (`EngineForSources`, `EngineForMainSession`, `EngineForPeople`, `EngineForSettings`, `EngineForExecutor`). One-writer-per-state is a stated rule.

### 4.3 Design article vs. shipped code

| Article module                            | In the prototype? | Notes                                                                                                                                                                                                                                               |
| ----------------------------------------- | ----------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Two-layer Router / Worker                 | Yes               | Main Session + Executor Sessions, separate presets, Router cannot write files or spawn subagents                                                                                                                                                    |
| Router batching                           | Yes               | Evals batch per Thread; `orchestrator_route` takes up to 20 decisions per call                                                                                                                                                                      |
| Two-stage event filtering                 | Yes               | Source scope + allowlist + admission table + bot list in code; rule assessment by the model                                                                                                                                                         |
| Subscriptions and direct delivery         | Yes               | Fan-out to subscribed Tickets bypasses Eval; Workers hand back out-of-scope messages                                                                                                                                                                |
| Inline & Spill, Chain of Recall           | Yes               | Cards with char limits and read pointers; ID-walkable resources                                                                                                                                                                                     |
| Proactive / speculative work              | Partly            | Rule-gated, with accept modes `off` / `observe` (default, records only) / `auto`; no background pre-computation beyond this                                                                                                                         |
| Asynchronous ReAct loop                   | Approximation     | Shell commands become background jobs after 5 s and completion wakes the session; the article says the real mechanism "has already been implemented in DeepSeek Harness, but it is not yet enabled by default"                                      |
| Channel-specific communication            | Yes               | 100-word hard ceiling on IM, GitHub disclosure line, review-handling rules, all in prompts                                                                                                                                                          |
| Compute / state separation                | No                | Single process, SQLite in `stateDir`, worktrees on the same machine                                                                                                                                                                                 |
| Execution-environment daemons (BYOM)      | No                | Workers run as the operator's OS user on the same host                                                                                                                                                                                              |
| Watchdog                                  | Reduced           | A Python service script (`scripts/dsh-superagent`) with exit codes, plus a suggested hourly scheduled prompt in the operator's own harness profile that restarts the service. No model judging Worker progress, no natural-language reconfiguration |
| Sharded Router, A2A, credential isolation | No                | Listed as open questions in the article                                                                                                                                                                                                             |

## 5. Relation to shiguredo/deepseek-harness

**What it is.** `shiguredo/deepseek-harness` is a GitHub fork of `deepseek-ai/deepseek-harness`, the harness that the prototype runs on. Shiguredo (時雨堂) is a Japanese company known for the WebRTC SFU "Sora"; the fork's only author is `voluntas` (Nakai, `nakai@shiguredo.jp`).

| Field                                                    | Value                                                           |
| -------------------------------------------------------- | --------------------------------------------------------------- |
| Fork created                                             | 2026-09-14                                                      |
| Default branch                                           | `shiguredo`                                                     |
| Position vs upstream `master` (at `ce7073d`, 2026-10-29) | 1 commit ahead, 0 behind                                        |
| Divergent commit                                         | `60b345c`, 2026-10-30, message is only a gist URL, GPG-verified |
| Stars / forks / open issues                              | 113 / 8 / 13 (upstream: 268,597 / 32,600 / 0)                   |

**Both READMEs.** The fork's README on its `shiguredo` branch is identical to upstream's: it describes DeepSeek Harness as "an open-source agent harness developed by DeepSeek AI", built on the Cordis "everything-is-a-plugin" architecture, in developer preview with breaking changes, started via `npx @deepseek-ai/dsh web`, and it still tells readers to clone `deepseek-ai/deepseek-harness`. It contains no mention of Shiguredo or of the fork's changes. The prototype's README mentions DeepSeek Harness only as the thing it is "packaged as a bundle for" and links to `deepseek.com/en/harness/`, not to any GitHub repository.

**What the fork actually changes** (from the gist the commit message points to, titled "DeepSeek Harness 時雨堂 fork 変更情報", last updated 2026-10-30): Japanese UI locale and CJK-safe font stacks; a git branch chip in the composer; workspace names on session rows; a bundled Ollama Cloud provider catalog of 21 models with peak-hour routing for the DeepSeek entries; Ollama Cloud web search and fetch plugins; provider display in the model picker; message timestamps with a timezone setting; changing a Session's working directory; per-instance persistent state for multiple web servers; making upload of session logs to the official DeepSeek API opt-in (default off); a "1017" release badge; a built-in `git push` guard that asks for confirmation; and a "Shiguredo built-in plugin settings" group. The diff touches `packages/client/*`, `packages/llm/llm-pi-ai`, `packages/api/workspace-git`, docs and agent notes. Searching the diff for "superagent" returns nothing.

**Conclusion.** The two repositories share only a dependency: the prototype consumes upstream `@deepseek-ai/dsh-*` packages from npm, and the fork is a downstream customization of the same harness aimed at Japanese users and Ollama Cloud. Nothing in the prototype requires or references the fork. Whether the prototype would even load on the fork is untested. The prototype's `engines.dsh` is `^0.2.1-alpha.2`; the fork's base master carries `0.2.2-alpha.2` in its root `package.json` and, per the gist, also `0.2.1-rc.5`. Under npm's default semver rules a prerelease such as `0.2.2-alpha.2` does not satisfy `^0.2.1-alpha.2` (prerelease versions only match a comparator with the same major.minor.patch), while `0.2.1-rc.5` does; how `dsh` itself checks `engines.dsh` was not verified. If the research interest is "what would running the prototype on a Japanese-localised harness look like", that is a porting project, not something either repository offers.

## 6. Runtime and the API it needs

**Host requirements** (from `SETUP.md`, `docs/006-deployment.md`, `package.json`):

| Requirement              | Detail                                                                                                                                                                                            |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Node.js                  | `^22.19.0 \|\| >=24.0.0`                                                                                                                                                                          |
| DeepSeek Harness (`dsh`) | `^0.2.1-alpha.2`; docs install `@deepseek-ai/dsh@0.2.1-rc.3` globally; a dedicated profile named `superagent` cloned from the Web profile                                                         |
| pnpm                     | Needed to build the bundle (`pnpm install && pnpm build`), then `dsh plugin --profile superagent add "link:$PWD"`                                                                                 |
| git                      | 2.32+ (credential-helper config the setup writes); `git-lfs` if the repo uses it                                                                                                                  |
| Python                   | 3.8+ for `scripts/dsh-superagent` (start/stop/status; uses `fcntl`, `ps`, `tmux`, so Linux/macOS)                                                                                                 |
| tmux                     | The service runs `dsh --profile superagent --no-open` inside a tmux session                                                                                                                       |
| GitHub CLI               | `gh` 2.48+, signed in as a **dedicated GitHub user account** for the agent (not a GitHub App, because the Source reads the account's notifications); github.com only, no GitHub Enterprise Server |
| Feishu (optional)        | `lark-cli` (tested 1.0.90) configured in bot-only strict mode                                                                                                                                     |
| Disk / state             | An absolute `stateDir` holding SQLite, lock, command shims, worker git config and Ticket worktrees                                                                                                |
| Panel                    | Loopback web server, default port 3082                                                                                                                                                            |

**Privileges.** Both presets run with the harness permission `danger-full-access` as the operator's OS user; workers execute commands without approval. The docs recommend a dedicated OS account for isolation. The `cordis.patch.yml` carries `pwsh` entries for Windows, but the service script and setup checks are POSIX-only.

**Model API.** The prototype has no model code of its own and names no vendor anywhere in `src/`, `docs/` or prompts. It calls the harness's `ctx.llm` service. The profile's default model is used unless the Eval or Execution settings name another, so the Router and Workers can run different models (the article recommends a lighter model for the Router). What the harness supports, per its provider guide: the official DeepSeek API (key entered in Settings → Models), a signed-in DeepSeek account, built-in third-party providers shipped via `pi-ai` (ids such as `anthropic`, `openai`, `moonshotai`, `zai`), and any custom endpoint speaking OpenAI Chat Completions, OpenAI Responses or Anthropic Messages. So the prototype needs **some** chat-completion-style API with tool calling configured in the harness, not specifically DeepSeek's.

**External APIs.** GitHub REST and GraphQL via `gh` (comments, review-thread replies via `resolveReviewThread`, checks, notifications), and Feishu via `lark-cli`. A local HTTP management API (`GET state`, `GET/PUT settings/<block>`, `GET/PUT prompts`, `POST executor/pause`, `POST tickets/<id>/retry|stop`, etc.) is the operator surface and is documented as stable enough for agents to script against.

## 7. Reusable design versus code to run

**Reusable as design (strong):**

- **The domain model and its rejected alternatives** (`docs/001-domain.md`). Source / Trigger / Thread / Eval / Mandate / Ticket / Assignment / Subscription, with explicit rules such as "only Eval creates a Ticket", "a Mandate is immutable; wider scope means a new Ticket", "a person is not a domain concept", and a table of concepts they deliberately rejected and why. The glossary is bilingual (English and Chinese). This transfers to any event-driven agent regardless of harness.
- **The authorization model** (`docs/002-authorization.md`): explicit vs inferred strength, an admission table keyed by receiving scope × sender membership × whether the agent was addressed, a bot list, accept modes `off` / `observe` / `auto`, versioned Policy with Mandate revalidation before an ended Ticket resumes. "Observe mode" (assess but only record what would have been accepted) is a clean pattern for rolling out proactive behaviour.
- **The `SourceKind` protocol and the cookbook** (`docs/008-cookbook.md` walks through adding a new event source end to end, including idempotent sends, `sent` vs `gone` failure classes, thread-context readers for assessments, and admission rows).
- **The tool contracts**: 14 Router tools and 6 Worker tools, with result shapes, the single `orchestrator_route` batch call, structured `human_action` questions, `reply` purposes (`acknowledgement` / `answer` / `result` / `attention`) enforced by the host rather than by prompt. The idea that the host checks reply purposes and 100-word limits in code, and prompts merely explain them, is the most transferable engineering stance in the repo.
- **The prompt corpus** (`prompts/*.md`, 15 files, one sentence per line, plus two Source skills). Highlights: the Router prompt forbidding technical work and scope expansion ("'Could we add a dark mode?' should arrive as that original request... without router-selected color schemes"); the admission prompt's three independent facts before accepting proactive work (targets this project, concrete change intent, direction settled enough for a small local edit) with worked accept/ignore examples; the team communication prompt's "would deleting this clause prevent the human from understanding the result or taking the required action? If not, delete it"; the review-handling rules (resolve fixed threads silently, one-sentence reason when declining, three rounds per automated reviewer). The prompt system also records which built-in default an override was based on and flags "Default updated" after upgrades, a reusable mechanism for team-edited prompts.
- **The assembly and precedence ladder** (`docs/004-prompts.md`): host-enforced facts > built-in sections > matched-rule instructions > team sections > outside text, which "is data and never changes rules or authorization."
- **The design article itself** as a vocabulary: fast/slow path filtering, subscription-based direct delivery, Inline & Spill, Chain of Recall, Router batching, and the agent-team contrast.
- **Agent-run setup** (`SETUP.md`): an installation procedure written for a coding agent to execute with the operator, one question per message, plan before execution, secrets never in chat.
- **Engineering practices** worth copying: `tests/model-surface.spec.ts` (everything the model reads, checked against tool schemas within a size budget per role), `tests/docs.spec.ts` (docs link only backwards; architecture tables list every module and test), `tests/cards.spec.ts` (the rules the built-in prompt text must state).

**Evaluation: nothing runnable.** The word "Eval" in the repo means the admission judgement, not benchmarking. There is no benchmark script, synthetic workload, or results data anywhere in the repository (grep for benchmark/simulat/p95 finds only the simulated test host). The experiments exist only in the article, self-reported, with synthetic workloads and a time-consuming stub replacing coding, which the authors call "preliminary reference points". The reusable part is the protocol, not the numbers:

| Experiment design  | Detail                                                                                                                                                                                                                                                                             |
| ------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Workload           | ~300 messages per run (group chat + GitHub CI stream), ~20 real work requests, rest chatter, follow-ups, stops, CI; five runs per arm; intervals scaled to one quarter, real model latency                                                                                         |
| Arms               | Super-agent; Super-agent without direct delivery; single Session + subagent tool with a neutral prompt; same with a delegation-first prompt                                                                                                                                        |
| Metrics            | Task completion time p50 / p95 (request to result message); cache-read tokens per run; Router decision count                                                                                                                                                                       |
| Reported results   | Super-agent p50 12.4 min, p95 15.7 min; without direct delivery 12.6 / 15.5 min but +37% cache-read tokens (23.23M to 31.77M) and +30% Router decisions; single-session neutral 20.4 / 29.5 min and zero subagent calls in 5 runs; single-session delegation-first 13.8 / 29.0 min |
| Router stress test | Arrival 1 to 40 triggers/min: batch size 1.0 to 2.8, request duration 2.5 to 3.9 s, amortized time per decision 6.4 to 1.6 s                                                                                                                                                       |

**Code to run (weak reuse outside DeepSeek Harness):** the ~15k lines of TypeScript import 28 distinct `@deepseek-ai/*` packages (Cordis plugin context, `dsh-agent`, `dsh-session`, `dsh-llm`, `dsh-subprocess`, client UI packages) at `0.2.1-alpha.2`. The Engine in `src/core` is pure and portable in principle, but everything around it (sessions, tools, presets, panel) is harness-specific. Porting the Engine plus SQLite store to another harness is feasible; running the bundle anywhere but a pinned pre-release DeepSeek Harness is not what it is for.

## 8. Fit with this dotfiles repository

Context from the repository itself: `home/dot_agents/agent-config.yaml` is the single source for Claude Code, Codex and omp seats, with `model_profiles` (express, standard, review, deep, security, audit), a `command_policy` deny list, permgate hooks, a strict Bash sandbox, and an hcom "regime" that runs an orchestrator seat, worker seats in their own worktrees under `~/.local/state/omp-seats/<slug>/`, and a read-only audit run; the PR levers `pr-audit.sh`, `pr-merge.sh --match-head-commit`, `pr-thread-*.sh` live under `home/dot_local/bin/common/`. There is no DeepSeek, Ollama or local-model route in the kit, and no GitHub-event-driven agent: work enters the regime through `hcom-dispatch`, not through issue comments.

**What transfers as design, without running anything:**

- **The Mandate / Ticket / Subscription vocabulary** is a cleaner statement of what the regime's `units.tsv` and `ledger.tsv` already do by hand: one unit of authorized work, an immutable record of who authorized it and under which standing orders, follow-up messages routed to the seat that owns the unit. Citing `docs/001-domain.md` in a future ADR costs nothing and gives the kit a shared vocabulary with a published design.
- **Router rules as seat policy.** The orchestrator prompt's prohibitions (no technical decisions, no scope expansion, routing notes capped at 30 words, never wait with `sleep` or long job waits) and the `noWait` guard are directly comparable to the kit's orchestrator-seat levers and stop gate (`docs/orchestrator-seat.md`). The host-enforced reply purposes (`acknowledgement` / `answer` / `result` / `attention`) are a pattern the kit's `pr-thread-reply.sh` lever could adopt: code decides whether a message is allowed, prompts only explain why.
- **Observe-before-auto rollout** for any proactive behaviour. The kit has no proactive agent today; if one is ever added (for example, a seat that reacts to Dependabot or CI), the `off` / `observe` / `auto` ladder with recorded "would accept" decisions is the right first design.
- **Review-handling rules** (resolve fixed threads silently, one sentence when declining, at most three rounds per automated reviewer, record the round count so a later worker continues it) map onto the kit's `pr-threads-check.sh` and `pr-thread-resolve.sh` levers and onto the existing standing rule that every bot thread is handled before `Ready for Human Review`.
- **`SETUP.md` as an agent-executed runbook** (one question per message, plan before executing, secrets never in chat) is a format the kit's operator handouts could borrow.
- **`tests/model-surface.spec.ts`**: a size-budgeted test of everything the model reads is a check the kit's `validate-agent-assets.py` does not have for its rendered prompts, rules and skills.

**What does not transfer, or not yet:**

- **Running the bundle.** It needs a pinned pre-release DeepSeek Harness profile, tmux, Python, a dedicated GitHub user account with write access, and workers running with `danger-full-access` as the OS user. That contradicts the kit's strict-sandbox stance (sandbox mandatory, `allowUnsandboxedCommands: false`, `git push *` and `gh *` always ask). Treat it as reading material until there is a disposable host, as the sibling note on the harness also concludes.
- **Model route.** The prototype is model-agnostic through the harness, so it adds no DeepSeek-specific dependency, but the kit would still need a `dsh` seat vendor first (covered in `shiguredo-deepseek-harness.md`, which recommends an upstream pin and `session-log-deepseek.enabled: false`).
- **Feishu.** Dead weight for this kit. The GitHub `SourceKind` is the only Source of interest, and even that reads a user account's notifications rather than webhooks or a GitHub App.
- **Evaluation.** Nothing to reuse as code; the experiment design in section 7 could inform a future benchmark of the kit's orchestrator seat against a single-session baseline, but it would have to be rebuilt from the description.

## 9. Risks and caveats for anyone evaluating it

- **Security posture is explicitly weak.** Full OS-user access, no sandbox, CLI wrappers are "defaults, not a security boundary", a worker "can execute programs by path and read the operator's home directory." The architecture doc lists "which Trigger fields are trusted" as an open question. The article's own section 8.4 says a compromised cloud loop "could potentially" take over every connected device in the fuller design.
- **Prompt-injection surface is the product.** The agent reads public GitHub comments and chat; defence rests on the gate (allowlists), Mandate scope and repeated prompt statements that outside text is data. Default `observe` mode and a short allowlist are the mitigations the docs recommend ("start narrow").
- **Unbounded growth.** Nothing deletes triggers, decisions, receipts or settings versions.
- **Maintenance cliff.** Single commit, no issue tracker, pre-release harness dependency with declared breaking changes; the docs already warn about `agent-preset/not-found` if preset rows are removed and about database migrations that cannot roll back.
- **Operational footprint.** A dedicated GitHub user account with write access, a dedicated harness profile, tmux, an hourly scheduled check in another profile, and (optionally) a Feishu app. The Feishu path is clearly the team's internal reality and will be dead weight for most readers.

## 10. Sources and verification

Verified first-hand (read the files or API responses directly):

- Repository clone at `6337fc8`: `README.md`, `SETUP.md`, `package.json`, `cordis.patch.yml`, `examples/profile.cordis.patch.yml`, `scripts/dsh-superagent`, all nine `docs/00x-*.md`, all 15 `prompts/**/*.md`, both `skills/*/SKILL.md`, `src/core/memory.ts`, `src/app/role-models.ts`; `git log`; line counts; grep for vendor names and benchmark terms.
- GitHub API: repository metadata for `deepseek-ai/dsh-superagent-prototype` and `shiguredo/deepseek-harness` (including `parent`/`source`), and the `compare/master...shiguredo:shiguredo` endpoint (ahead 1, behind 0, first 100 changed files).
- `raw.githubusercontent.com`: the fork's `shiguredo` branch `README.md` (identical to upstream) and root `package.json` (`@deepseek-ai/dsh-root` 0.2.2-alpha.2, Node `>=24.9.0`); upstream `SAFETY.md`.
- The gist referenced by the fork's commit, https://gist.github.com/voluntas/34ac1f8ced7052d69dc37f54fc57155c (Japanese).
- DeepSeek Harness docs: quickstart and "Configure models" provider guide at deepseek-harness.github.io; the product page https://www.deepseek.com/en/harness/.
- This repository, for section 8: `home/dot_agents/agent-config.yaml` (`model_profiles`, `command_policy`, `omp.roles`, `claude.sandbox`), `home/dot_agents/README.md`, `AGENTS.md`, `README.md` (hcom regime section), `docs/orchestrator-seat.md`, and the lever scripts under `home/dot_local/bin/common/`.

Primary source located but read via a third-party translation:

- Original article: https://mp.weixin.qq.com/s/zoS7GlReWPhfCjENGxXCdg (WeChat, "DeepSeek 产品部 / DeepSeek Harness 团队", 2026-10-31); also on Zhihu https://zhuanlan.zhihu.com/p/2099987320443237060. Quotations in this report come from the English translation at https://offloop.org/learn/exploring-deepseek-super-agent-design (third party, published 2026-10-31). A second translation exists as an X article by @teortaxesTex. Experiment numbers were cross-checked against secondary coverage (MarkTechPost, 2026-11-01; InfoQ via Sina; IT之家; 量子位) and agree.

Not verified: the fork's full changed-file list beyond the first API page; whether the prototype loads on the fork's harness build; how `dsh` evaluates `engines.dsh` against prerelease versions; the design article in its original Chinese (quotations rely on the third-party translation). None of these affects the conclusions above.
