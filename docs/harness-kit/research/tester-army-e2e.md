# tester-army/e2e

Researched 2026-11-02 against `main` (pushed 2026-11-01) and the published
docs at e2e.tester.army. Method note: `$TMPDIR/hk-research/` held no shared
method file when this note was written, so it follows the structure the other
notes are expected to share: verdict first, vitals, what it is, what it drives,
fit against this repository (agent stack, bootstrap, CI), risks, sources.

## Verdict

`e2e` is a **framework**: an SDK, a test runner and a CLI, published to npm,
with an engine contract behind it. It is not a harness you point at an
existing system, and not a corpus of tests. It drives **browsers** (through
Playwright) and **iOS/Android simulators, emulators and devices** (through
agent-device), and nothing else. Natural-language steps are executed by a
model-driven agent; the ACP package lets Claude Code or Codex be that agent.

For this repository it is **not applicable as a test tool**. Nothing here has
a browser or device surface worth a UI suite: the bootstrap (`setup.sh`, the
chezmoi apply) is shell; the agent stack (Claude Code, Codex, omp, hcom seats,
herdr panes, permgate) is terminal and socket driven; the CI jobs already test
those with Bats, Python unittest and throwaway containers. `e2e` has no engine
for a terminal, a shell script or a coding agent as the system under test. The
relationship runs the other way: `e2e` consumes Claude Code and Codex as the
driver for _its_ tests of _web and mobile apps_.

Two things from it are worth keeping in mind:

- As a **plugin for the agent stack**, if the operator starts a web or mobile
  project: the `e2e` skill installs with `npx skills add tester-army/e2e`, and
  `plugins/e2e` is a marketplace for Claude Code, Codex and Cursor.
- As a **source of CI and review patterns**, several of which this repository
  has arrived at independently (see "Patterns worth comparing").

## Vitals

| Item                        | Value                                                                                            |
| --------------------------- | ------------------------------------------------------------------------------------------------ |
| Repository                  | https://github.com/tester-army/e2e                                                               |
| Owner                       | TesterArmy (commercial agentic testing platform), contributors Oskar Kwaśniewski, Szymon Rybczak |
| Created                     | 2026-07-22                                                                                       |
| Stars / forks / open issues | 12,466 / 646 / 77                                                                                |
| Language                    | TypeScript 7, pnpm monorepo, ESM only                                                            |
| License                     | Apache-2.0, no CLA, no DCO                                                                       |
| Latest release              | `e2e@0.22.0`, 2026-10-30 (changesets, GitHub-Actions bot, npm Trusted Publishing)                |
| Node floor                  | `^22.22.3                                                                                        |     | >=24.8.0`; Windows only under WSL |
| Status                      | pre-1.0; "APIs and config can still change between minor releases"                               |
| Telemetry                   | on by default to `eu.i.posthog.com`; opt out with `E2E_TELEMETRY_DISABLED=1` or `DO_NOT_TRACK=1` |

Published packages: `e2e` (SDK, runner, CLI, MCP server), `@e2e-dev/web`,
`@e2e-dev/mobile`, `@e2e-dev/decision`, `@e2e-dev/acp`, `@e2e-dev/github`
(PR-comment reporter), and hosted-browser/device providers `kernel`,
`lightpanda`, `smol`, `testmu`, `browserstack`, `limrun`, `eas`.

## What it is

### Framework, harness or corpus

| Layer                          | Present?         | Where                                                                                                                                                                                                                                                                                                     |
| ------------------------------ | ---------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Framework (SDK + runner + CLI) | Yes, the product | `packages/e2e`: `test`, `expect`, fixtures `app`, `screen`, `agent`, `browser`, `device`; `e2e run`, `e2e explore`, `e2e mcp`, `e2e init`, `e2e login`                                                                                                                                                    |
| Engine contract                | Yes              | `e2e/engine`: `defineEngine`, plus an LSP-style JSON-RPC engine protocol so an engine can live in another process, machine or language                                                                                                                                                                    |
| Harness for other runners      | Partial          | `openHost` from `e2e/runner` hosts e2e sessions inside Playwright Test, Vitest or Jest; `run`, `explore`, `list` run suites from code                                                                                                                                                                     |
| Test corpora                   | Internal only    | `apps/testbed` (dogfood playground), `apps/web-benchmark` and `apps/mobile-benchmark` (hard-surface scenarios copied from TesterArmy's benchmarks, with committed replay recordings), `examples/` (ten one-screen greeter demos), axe-core conformance fixtures vendored for the web engine's tree reader |

The corpora are private workspace apps that test `e2e` itself. They are not
published and not meant to be reused against another project. So the honest
classification is: a framework, with a small harness surface (`openHost`,
`e2e mcp`) and an internal corpus.

### The execution model

- A test mixes deterministic steps (`app.open`, locators, `expect`) with
  agent steps (`agent.act('upgrade to Pro')`, `agent.assert(...)`,
  `agent.waitFor`, `agent.extract`).
- The agent sees a redacted semantic tree (and optionally masked pixels) and
  calls a closed set of tools; the runner, not the model, authorizes each
  action. Model text is never evaluated as code, selector, shell or config.
- Every agent step is **recorded** into `.e2e/cache/`; later runs replay the
  recorded actions without a model call until the app changes. CI can run
  `--strict-cache` so a stale recording fails with `REPLAY_STALE` instead of
  silently calling the model.
- Executors are pluggable: the built-in AI-SDK agent, `@e2e-dev/decision`
  (a bounded decision model answering multiple-choice questions, plus
  `decisionFilter()` to skip tests a PR cannot affect), or `@e2e-dev/acp`
  which runs the step on **Claude Code or Codex over the Agent Client
  Protocol** using the agent's own login.
- `e2e explore` gives the agent a goal with no test file and reports findings
  (issue/warning with severity and reproduction). `e2e mcp` exposes a live
  session as an MCP server so a coding agent can walk a flow and write the
  test as it goes.
- An API-only mode exists: a target with no engine, `fetch` plus value
  matchers. It still needs a URL, not a process.

## What it drives

| Surface                                | Supported                 | How                                                                                                                   |
| -------------------------------------- | ------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| Web browsers                           | Yes                       | Chromium, Firefox, WebKit via Playwright; hosted via Kernel, Lightpanda, smol microVMs, TestMu                        |
| iOS / Android                          | Yes                       | simulators, emulators and real devices via agent-device; hosted via BrowserStack, TestMu, Limrun, EAS                 |
| HTTP APIs                              | Yes, thin                 | `fetch` with `toMatchSchema`; no engine needed                                                                        |
| CLIs / terminals / shell scripts       | **No**                    | no engine exists; `app.command` only starts the app's server for the run                                              |
| Coding agents as the system under test | **No**                    | Claude Code and Codex appear only as the _executor_ that drives a browser or device                                   |
| Anything else                          | Only by writing an engine | the protocol is documented ("Writing an engine", "Engine servers"); a terminal engine would be a from-scratch project |

## Fit against this repository

### The agent stack

The stack under `home/dot_agents`, `home/dot_claude`, `home/dot_omp` and
`home/dot_local/bin/common` is Claude Code, Codex and omp configuration,
hooks, the permgate policy, hcom seats started in herdr panes, sandboxed by
srt and bwrap, and the orchestration levers (`pr-audit.sh`, `pr-merge.sh`,
`hcom-seat`, `regime-start`). All of it is a terminal, a Unix socket or a
file. `e2e` can observe none of that: its observations are a browser's
accessibility tree or a device's view hierarchy.

The only HTTP listeners in the repository are loopback helpers, and both are
tiny:

- `regime-url-opener` on `127.0.0.1:1456`, a `POST /open` that opens an
  allow-listed sign-in URL in the laptop's browser.
- The `openai-siwc` OAuth callback on `127.0.0.1:1455`, already covered by a
  Vitest file in the extension.

The API-only mode could poke `POST /open`, but the Python unit tests already
do that without Node, Playwright or a model key. There is no case for it.

What `e2e` would actually do for the agent stack is sit **inside** it as a
consumer skill: a Claude Code or Codex session in a web project would get
the `e2e` skill, an MCP server entry, and `claudeCode()`/`codex()` executors.
That is an install decision for a project, not a change to this repository.
If it ever is made, note the stack's own rules: MCP servers are disabled by
default and declared in `agent-config.yaml`, plugins are not enabled from
`settings.json` unless this repository installs the marketplace, and the
Claude sandbox allows no Unix sockets and a fixed set of network hosts, which
would block Playwright's browser download and the PostHog telemetry call.

### The bootstrap: `setup.sh` and the chezmoi apply

`setup.sh` is a 1,200-line Bash program: release resolution with attestation
checks, chezmoi download and verification, external prefetch into chezmoi's
cache, `chezmoi init` then `chezmoi apply`, a drift refusal on rerun. The
existing end-to-end coverage is:

- `ubuntu.yaml` and `macos.yaml`: run `setup.sh` from the PR checkout as
  client and server, rerun it after appending to `~/.zprofile` and require
  the rerun to fail and leave the file byte-identical, then run the Bats
  file-existence suites.
- `apply-check.yml` runs `make apply-check`: the working tree applied as a
  fresh Ubuntu client and server in a container with `--network none` and no
  credential, followed by the doctor checks.
- `test.yaml`: Python unittest and Bats across Ubuntu 24.04 client/server and
  macOS 15 client, with a 26.04 canary.
- `remote.yaml` and `private-bootstrap.yaml`: the snippet install and the
  private layer.

`e2e` adds nothing here. There is no screen to observe, and its natural
language steps would have no vocabulary for "the apply left `.zprofile`
unchanged". The right instruments remain Bats, unittest and containers, which
is what the repository already uses.

### The CI jobs

Adding `e2e` to CI means a Node 22.22.3+ and pnpm toolchain, a Chromium
download with system libraries, an `AI_GATEWAY_API_KEY` or an ACP login, and
an outbound PostHog call unless disabled. This repository's CI is shell,
Python and Bats with pinned tool versions from `home/dot_mise/config.toml`,
and `AGENTS.md` requires supply-chain pinning and refuses dynamic `npx ...@latest`
on hot paths. The cost is real and the payoff is nil, because there is no UI
to test.

### Patterns worth comparing

These are design choices in `tester-army/e2e` that line up with, or sharpen,
things this repository already does. They cost nothing to borrow.

- **One gate job per workflow.** Each workflow ends in a `<workflow> gate`
  job with `if: always()` that fails on any failed or cancelled need and
  passes over skipped ones; the ruleset requires only the gate. Path
  filtering is done by a `changes` job (dorny/paths-filter), never by a
  workflow-level `paths:`, because a required check that never reports
  blocks the merge forever. This repository's `test.yaml` documents the same
  hazard; `ubuntu.yaml` and `macos.yaml` still use workflow-level `paths:`
  and are therefore not required checks.
- **Committed recordings replayed read-only in CI**, with `--strict-cache`
  turning a stale recording into a hard failure. The idea of a deterministic
  replay of an agent's actions, with model calls only for steps with no
  recording, is a cost and flakiness control this repository's verdict loop
  does not have an analogue for.
- **Definition of done** in `AGENTS.md`: verified against the built
  artifacts, reviewed in a fresh context, every bot thread handled, labeled
  `Ready for Human Review`, and a push removes the label. The fresh-context
  self-review and the per-head label mirror this repository's per-head
  verdict row and `pr-merge.sh --match-head-commit`.
- **Repo-only skills** live in `.dev/skills/` with `metadata.internal: true`
  and are symlinked from `.claude/skills/`, so the public skill scan offers
  only `skills/*`. This repository keeps the equivalent split with
  `skills.audience` in `agent-config.yaml`.
- **"When a reviewer corrects the same thing twice, encode it"**: types,
  then lint, then test, then a skill line, in that order. Close to the
  Weighted-findings rule here, but it names the escalation ladder.
- **`bench:ab`** measures a change against the merge base with paired runs
  and a bootstrap interval, and lists behavior differences before timings.
  This repository's macOS benchmark job records timings only.
- **Trust model written down once** (`SECURITY.md`): code-trust for tests,
  config and engines, which run with full OS authority; untrusted model
  input for everything the page shows. The explicit statement that the merge
  queue runs a fork's code with repository secrets, so enqueueing is the
  trust decision, is the kind of sentence this repository's threat tables
  ask for.

## Risks and caveats

- **Pre-1.0.** Minor releases may break config and API; `0.22.0` carried a
  `**Breaking:**` change to screenshot behavior after a secret fill.
- **Code-trust everywhere.** Test files, `e2e.config.ts`, custom tools and
  engines run unsandboxed with the runner's authority. This conflicts with
  the sandbox-first stance of this repository's agent stack.
- **Secrets can reach the model.** Screenshots mask only secure fields; a
  value the app shows elsewhere is in the pixels sent to the provider. The
  project documents this as a limit, not a gap.
- **No origin allowlist** on navigation or secret fills (removed on purpose
  in PR #290). An agent follows the app wherever it goes with the secrets
  the step was given.
- **Telemetry on by default**, including whether the shell is a coding
  agent. Disable in any CI or sandboxed environment.
- **Model cost and flakiness** for agent steps; the project itself runs its
  real-model suites weekly, not per PR, for that reason.
- **Heavy toolchain**: Node, pnpm, Playwright browsers, optional Xcode or
  Android SDK; Windows only under WSL.

## Sources

- Repository and README: https://github.com/tester-army/e2e
- `AGENTS.md` (layout, commands, gotchas, security invariants, CI gate pattern): https://raw.githubusercontent.com/tester-army/e2e/main/AGENTS.md
- `CONTRIBUTING.md` (contract, releases, changesets, Trusted Publishing): https://raw.githubusercontent.com/tester-army/e2e/main/CONTRIBUTING.md
- `SECURITY.md` (trust model, navigation, telemetry, outbound connections): https://raw.githubusercontent.com/tester-army/e2e/main/SECURITY.md
- `.github/workflows/spec.yml` and `agent.yml` (gate job, weekly agent suites): https://raw.githubusercontent.com/tester-army/e2e/main/.github/workflows/spec.yml, https://raw.githubusercontent.com/tester-army/e2e/main/.github/workflows/agent.yml
- `packages/acp/README.md` (Claude Code and Codex as executors): https://raw.githubusercontent.com/tester-army/e2e/main/packages/acp/README.md
- `packages/e2e/package.json` (version 0.22.0, Node engines, exports): https://raw.githubusercontent.com/tester-army/e2e/main/packages/e2e/package.json
- Docs: quickstart, subscriptions (ACP section), explore, api-testing, engines, reference/runner, ci/github-actions at https://e2e.tester.army/docs/
- GitHub API for vitals and releases: https://api.github.com/repos/tester-army/e2e, https://api.github.com/repos/tester-army/e2e/releases
- This repository: `setup.sh`, `Makefile`, `.github/workflows/{ubuntu.yaml,apply-check.yml,test.yaml}`, `AGENTS.md`, `home/dot_agents/README.md`, `home/dot_local/bin/common/executable_regime-url-opener`
