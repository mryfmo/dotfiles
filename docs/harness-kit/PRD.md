# TechnoPro Harness Agent Kit (THAK): product requirements

## Summary

THAK turns the dotfiles repository mryfmo/dotfiles into a reproducible harness kit for AI coding agents. The kit composes Claude Code, Codex and the omp seats from one manifest, contains them with one sandbox engine, gates every merge behind a fresh read-only audit, keeps a records trail, and adds optional seats and tools only under written provenance rules. This document states the requirements. Seven architecture decision records (ADR-001 to ADR-007) hold the one-way doors, and seven Gherkin features under `bdd/` hold the scenarios that verify them. `check.py` keeps the three in step and runs the scenarios that already hold against the repository.

The decisions came from a research pass over eight open-source repositories, recorded under `research/` and in `decisions.tsv`. Four are integrated or ported (sandbox-runtime, knowledge-work-plugins skills, graphify as a per-project tool, DeepSeek Harness as an optional seat). Three are deliberately not adopted (the cybersecurity skills pack, the Shiguredo fork, tester-army/e2e). One, the dsh-superagent prototype, is design reading. The audit ADR keeps the Codex gate unchanged and admits the security audit skill only as a pinned sweep lens behind a flag.

## Problem

An engagement team that puts coding agents on a client's code needs five things from a harness. It needs the agents to share one configuration so that a rule written once binds Claude Code, Codex and the seats alike. It needs an OS boundary around an agent that approves its own tool calls, because approval rules see command text and nothing else. It needs a merge gate that no agent can talk its way past, with the auditor's rules taken from the trunk and not from the change under review. It needs a trail of who decided what, so that a later reviewer can read the program without the operator. And it needs a way to add a third-party skill, tool or model route without taking on an unreviewed supply chain.

The dotfiles repository already is most of this. `home/dot_agents/agent-config.yaml` is the single source for the three agents, rendered by `scripts/generate-agent-configs.py` and checked by `scripts/validate-agent-assets.py` and `scripts/check-agent-runtime.py` (`home/dot_agents/README.md`). The Claude Bash sandbox and the omp seats run on Anthropic's sandbox-runtime, the seats behind a fail-closed canary (`scripts/orchestrator/README.md`, "OS containment of the seat"). Every merge goes through `pr-merge.sh` at a head the ledger records as correct, after a fresh Codex audit whose rules come from the main branch's `AGENTS.md` (`AGENTS.md`, "Audit"). The records are `.orchestration/orchestrate/<program>/` with `units.tsv`, `ledger.tsv` and `decisions.tsv`. Every third-party asset carries a pin and a verification (`agent-config.yaml`, `assets:`).

What the repository is not yet is a kit: the decisions that make it one are spread over unit briefs, and the question of which outside components to bring in has not been answered in one place. THAK answers it.

## Personas

- Operator: owns the hosts and the manifest, runs `make update` and `make doctor`, decides the open questions named below, and commits the records. The operator's shell is outside every sandbox and is the trust root.
- Engagement lead: starts a program for a client repository, writes unit briefs, reads verdicts and the ledger, and reports to the client. Reads the PRD and the ADRs; never edits a generated file.
- Worker seat: an omp process under srt in its own worktree, approving its own tool calls under the worker policy, pushing its own branch only. The seat needs a skill set, a model route and a bounded boundary.
- Auditor: one fresh, read-only Codex run per head with the trunk's rules, ending in one verdict line. Needs isolation from the caller and from the head's own instruction files.
- Reviewer: a person or a bot reading a pull request, the threat table and the ledger rows. Needs the records to be readable without the orchestrator's context.

## Goals

1. One manifest composes every agent the kit runs, and one validator refuses what the manifest forbids.
2. Every agent that approves its own commands runs inside an OS boundary that fails closed.
3. No merge without a fresh read-only audit at the exact head, with rules from the trunk.
4. Every third-party component in the kit has a named publisher, a pinned version or commit, and a verification.
5. Optional capabilities (a knowledge graph, a fourth seat vendor, end-to-end skills) can be added per project or per engagement without changing the managed trees.
6. The design is testable: every requirement has a scenario, and the scenarios that hold today are run by a script.

## Non-goals

- Replacing omp, the pi-claude-bridge or the hcom bus with another runtime.
- A hosted service of any kind: no graph service, no proactive GitHub agent, no telemetry endpoint.
- A general plugin marketplace of the kit's own.
- Benchmarking models. Nothing in the eight candidates is a model benchmark harness.
- Browser or device testing. The kit has no such surface.
- Changing any runtime behaviour in this pull request. The deliverable is the documents and the check script.

## Capabilities

### Seats and model routes

The kit runs three seat vendors today: Claude Code, Codex and omp, each with model profiles `express`, `standard`, `review`, `deep`, `security` and `audit` in `model_profiles` (`agent-config.yaml:536-582`); the validator requires the six and refuses a model set anywhere else. omp seats take their model route from a per-role profile overlay (`docs/omp-skills.md`, "Per-role overlays"). ADR-006 adds DeepSeek Harness as an optional fourth vendor for engagements where Anthropic and OpenAI endpoints are not allowed, pinned to an upstream tag, routed to Ollama Cloud or on-prem servers by default, with its model ids still in `model_profiles`.

- Today: three vendors, six profiles, model ids in `model_profiles` only, omp routes through the pi-claude-bridge and the SIWC extension (`docs/pi-claude-bridge.md`, `docs/openai-siwc.md`).
- The kit adds: an optional dsh seat vendor with a rendered profile, for engagements that cannot use the Anthropic or OpenAI endpoints.
- Decided in: ADR-006.

### Skills and plugins

Shared workflows are skills under `home/dot_agents/skills`, each with a `skills.audience` entry, rendered per agent (`home/dot_agents/README.md:8-13`). Plugins are pinned under `assets.claude-plugins` and `assets.codex-plugins`, by version or by content digest. ADR-001 fixes skills first and plugins only for semantics a skill cannot provide. ADR-004 fixes how a third-party skill enters: verified publisher, pin with digest or a copy recording its upstream commit, curated subset, validator-clean frontmatter, review cadence. The engineering and operations skills of anthropics/knowledge-work-plugins are the first port; the mukul975 cybersecurity pack is held.

- Today: nine shared skills with audience entries, seven pinned Claude plugins, one Codex plugin, the pstack tree pinned by commit and digest.
- The kit adds: a curated port of the knowledge-work engineering and operations skills with a drift test, and a written rule for every later third-party skill.
- Decided in: ADR-001 and ADR-004.

### Sandbox and permissions

Anthropic's sandbox-runtime is the engine behind the Claude Bash sandbox and the boundary around every omp seat; Codex keeps its own sandbox and permission profiles (ADR-002). The command policy renders one deny list to three consumers (`agent-config.yaml:199-234`). The kit pins the srt version in mise and adds no sandbox of its own.

- Today: the Claude Bash sandbox is strict and fails closed; every omp seat runs under srt behind a canary; Codex runs its own sandbox; srt follows `latest` in mise.
- The kit adds: a pinned srt version, a recorded residual list, and a measured first Linux seat run.
- Decided in: ADR-002.

### Audit and merge gate

Every unit's pull request merges only through `pr-merge.sh` at a head with a `correct` verdict row and green checks. Each audit is one fresh read-only Codex run per head under the `audit` permission profile with the trunk's `AGENTS.md` as rules, ending in one verdict line; a trust-boundary change carries a threat table; the fourth round needs a closing decision (`AGENTS.md`, "Audit"). ADR-003 keeps this gate unchanged and admits the security-audit skill only as a periodic sweep lens behind a flag, whose findings are advisory rows and never a verdict.

- Today: `pr-audit.sh` and `pr-merge.sh` are the gate; the audit profile is Codex gpt-6-astra at xhigh, read-only; the rules are the trunk's `AGENTS.md`.
- The kit adds: the security-audit skill as a pinned, flagged sweep lens beside the gate, with advisory findings and no verdict (ADR-003).
- Decided in: ADR-003.

### Records and orchestration

A program's records live under `.orchestration/orchestrate/<program>/`: units, ledger rows per audited head, verdict files, decisions. The orchestrator seat runs the loop from the `hcom-orchestration` skill, with the stop gate that keeps it from ending a turn while it owes the bus a reply (`docs/orchestrator-seat.md`). The dsh-superagent prototype's vocabulary of Mandate, Ticket and Subscription is cited as a cleaner statement of what the records already do by hand (research/deepseek-ai-dsh-superagent-prototype.md, section 8); no part of it runs. This capability has no ADR of its own in this set because no candidate changes it.

- Today: `units.tsv`, `ledger.tsv`, `decisions.tsv` and `verdicts/` per program; the hcom bus with the six line kinds; the stop gate and the supervisor.
- The kit adds: nothing that runs. The prototype's Mandate, Ticket and Subscription vocabulary and its observe-before-auto ladder are cited for any future proactive seat.
- Decided in: ADR-006, as design reading only.

### Knowledge and code navigation

Agents navigate code with grep, read and the project-map skill today. ADR-005 adds graphify as an optional per-project tool: a pinned `uv tool install`, a project-scoped install that leaves the generated trees untouched, code-only extraction, no manifest MCP entry and no hosted service.

- Today: no code graph; the parity policy keeps every MCP server Codex-only and disabled.
- The kit adds: a per-project trial recipe that touches no managed file and declares no MCP server.
- Decided in: ADR-005.

### Testing

The bootstrap and the seats are covered by Bats, Python unittest and throwaway containers in CI. ADR-007 declines tester-army/e2e as a test tool, compares its CI gate-job pattern against the platform workflows, and lists its skill for a future web or mobile project.

- Today: `setup.sh` runs end to end on Ubuntu and macOS in CI; the apply check runs offline in a container; Bats runs in CI only; the unit-test workflow is never path-filtered at the workflow level.
- The kit adds: a recorded comparison of the gate-job pattern for the platform workflows, and a per-project install path for the e2e skill.
- Decided in: ADR-007.

## Requirements

| Id   | Requirement                                                                                                                                                                           | Source ADR | Verification |
| ---- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------- | ------------ |
| R-01 | Every shared workflow is a skill under `home/dot_agents/skills` with a `skills.audience` entry, and a ported skill reaches every agent in its audience and no other.                  | ADR-001    | `@R-01`      |
| R-02 | A manifest MCP server is Codex-only and `enabled: false`; the validator refuses an enabled server. Today the manifest declares none.                                                  | ADR-001    | `@R-02`      |
| R-03 | A Claude plugin is enabled only through a pin in `assets.claude-plugins`, by version or by content digest when upstream has no version.                                               | ADR-001    | `@R-03`      |
| R-04 | A Claude Code MCP server is the operator's `claude mcp add --scope user`; the validator refuses a Claude-targeted server in the manifest.                                             | ADR-001    | `@R-04`      |
| R-05 | A plugin is adopted only when its brief names the namespace or hook semantics a skill cannot provide; the knowledge-work-plugins engineering plugin is not pinned.                    | ADR-001    | `@R-05`      |
| R-06 | The Claude Bash sandbox is enabled, fails closed, refuses the unsandboxed retry, excludes exactly `git push *` and `gh *`, and sets no Unix socket switch.                            | ADR-002    | `@R-06`      |
| R-07 | Every omp seat runs under srt behind a fail-closed canary; approval is not containment.                                                                                               | ADR-002    | `@R-07`      |
| R-08 | The srt version is pinned in `home/dot_mise/config.toml`, and a bump re-reads the behaviours `hcom-seat` relies on.                                                                   | ADR-002    | `@R-08`      |
| R-09 | Codex runs under its own sandbox and permission profiles; no lever wraps it in srt.                                                                                                   | ADR-002    | `@R-09`      |
| R-10 | The kit adds no sandbox of its own: credential stores stay denied, and the first Linux seat run is measured before Linux seats are relied on.                                         | ADR-002    | `@R-10`      |
| R-11 | A pull request merges only through `pr-merge.sh` at a head the ledger records as `correct`, with CI passed, by `--match-head-commit`.                                                 | ADR-003    | `@R-11`      |
| R-12 | Each audit is a fresh read-only Codex run with the trunk's `AGENTS.md` as rules, a scratch HOME, and the pinned read-only audit profile.                                              | ADR-003    | `@R-12`      |
| R-13 | Every audit ends in one verdict line, a trust-boundary change carries a threat table, and the fourth round needs a closing decision.                                                  | ADR-003    | `@R-13`      |
| R-14 | An advisory review lens, if adopted, reports findings into the thread and never writes a verdict row or changes a gate decision.                                                      | ADR-003    | `@R-14`      |
| R-15 | Every third-party asset declares its upstream, release or pin, and verification; a vendored skill tree is pinned by commit and archive digest.                                        | ADR-004    | `@R-15`      |
| R-16 | A skill's frontmatter holds only the six Agent Skills fields the validator admits.                                                                                                    | ADR-004    | `@R-16`      |
| R-17 | The mukul975 cybersecurity skills pack is not installed, pinned, vendored or referenced, and the committed-secret scan covers every tracked file.                                     | ADR-004    | `@R-17`      |
| R-18 | A ported knowledge-work skill records its upstream path and commit in `metadata`, keeps the licence notice, and holds no Claude Code command substitutions or connector placeholders. | ADR-004    | `@R-18`      |
| R-19 | A unit test diffs each ported skill against its recorded upstream text, so drift is visible.                                                                                          | ADR-004    | `@R-19`      |
| R-20 | No graphify server is declared in the manifest, the hosted route is refused without a review, and a manifest server must be exposed to Codex only.                                    | ADR-005    | `@R-20`      |
| R-21 | A graphify trial installs a release named in an `assets:` entry with a checksum, through `uv tool install`.                                                                           | ADR-005    | `@R-21`      |
| R-22 | A graphify trial uses the project-scoped install, and the runtime doctor shows the generated trees unchanged afterwards.                                                              | ADR-005    | `@R-22`      |
| R-23 | A graphify trial extracts code only, reads no provider key, and commits no graph file without the secret scan.                                                                        | ADR-005    | `@R-23`      |
| R-24 | DSH, when added, is pinned to a deepseek-ai/deepseek-harness release tag with a sha256 and never to the shiguredo fork. Today no DeepSeek or Ollama route exists.                     | ADR-006    | `@R-24`      |
| R-25 | The rendered dsh profile turns session-log upload off, defaults to Ollama Cloud or on-prem routes with the official API opt-in, and mounts the kit's Claude hooks.                    | ADR-006    | `@R-25`      |
| R-26 | Every model id lives in `model_profiles`, and the manifest defines the six base profiles and no others.                                                                               | ADR-006    | `@R-26`      |
| R-27 | The dsh-superagent prototype is not deployed; a proactive seat, if ever added, starts in observe mode and moves to auto only by a decisions row.                                      | ADR-006    | `@R-27`      |
| R-28 | tester-army/e2e is not a dependency of the manifest, the scripts, the installers, the Makefile, mise or the workflows.                                                                | ADR-007    | `@R-28`      |
| R-29 | The bootstrap runs end to end in CI, the apply check runs offline in a container, and Bats runs in CI only.                                                                           | ADR-007    | `@R-29`      |
| R-30 | A required check is never path-filtered at the workflow level, and the gate-job pattern is compared for the platform workflows.                                                       | ADR-007    | `@R-30`      |
| R-31 | The e2e skill is installed only for a project with a browser or device surface, with an audience entry, and nothing in this repository changes for it.                                | ADR-007    | `@R-31`      |

## Rollout

Each phase is a set of units the regime can run as unit briefs, one pull request each, audited and merged through the gate.

### Phase 1: pins and records (no behaviour change for the agents)

| Unit                         | ADR     | Files                                                             | Risk                                                                                         |
| ---------------------------- | ------- | ----------------------------------------------------------------- | -------------------------------------------------------------------------------------------- |
| Pin the srt version in mise  | ADR-002 | `home/dot_mise/config.toml`, `scripts/orchestrator/README.md`     | A pinned beta lags upstream fixes; the bump review must re-read the `hcom-seat` assumptions. |
| Record the sandbox residuals | ADR-002 | `decisions.tsv` of the program                                    | None; a record.                                                                              |
| Hold the cybersecurity pack  | ADR-004 | `decisions.tsv` of the program                                    | None; a record with three reopening conditions.                                              |
| Pin the security audit skill | ADR-003 | an `assets:` entry, a `skills.audience` line, a validator dry run | An unmaintained upstream snapshot; every fix is a local patch.                               |

### Phase 2: the skills port

| Unit                                  | ADR     | Files                                                                                                            | Risk                                                                                                          |
| ------------------------------------- | ------- | ---------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| Port the knowledge-work skills subset | ADR-004 | `home/dot_agents/skills/kwp-<name>/SKILL.md`, `skills.audience` in the manifest, a drift test under `tests/unit` | Name collisions with crit, superpowers and shdoc; Codex listing budget; the operator must confirm the subset. |

### Phase 3: measurements and CI comparison

| Unit                           | ADR     | Files                                                                            | Risk                                                                                    |
| ------------------------------ | ------- | -------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------- |
| First Linux seat run, measured | ADR-002 | the program's records; possibly `install/ubuntu/**`                              | The open srt Ubuntu issues may surface as canary refusals.                              |
| Compare the gate-job pattern   | ADR-007 | `decisions.tsv` of the program; possibly `.github/workflows/{ubuntu,macos}.yaml` | A workflow made required that cannot report blocks every merge; decide before changing. |

### Phase 4: optional capabilities, on request

| Unit                                     | ADR     | Files                                                                                                | Risk                                                                                 |
| ---------------------------------------- | ------- | ---------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------ |
| graphify trial in one project            | ADR-005 | an `assets:` entry; project files only                                                               | Pre-1.0 package releasing every few days; docs drift to re-read at the pin.          |
| dsh seat: asset pin and rendered profile | ADR-006 | `assets:`, `model_profiles`, a renderer for `cordis.patch.yml`, `home/dot_mise/config.toml` for Node | Developer preview with breaking changes; hook coverage untested; Node 24.9 or newer. |
| dsh hook-coverage check                  | ADR-006 | a test comparing `dsh-hooks-claude-code` against `home/dot_claude`                                   | Gaps in coverage leave a seat ungated.                                               |

## Risks and open questions

Operator decisions, each by name:

1. The knowledge-work subset. Which of the nineteen engineering and operations skills does the operator want, given that review, documentation and design workflows already come from crit, superpowers and shdoc (research/anthropics-knowledge-work-plugins.md, "Open questions")?
2. `argument-hint`. Admit it to the validator's field list, or keep the Agent Skills specification and edit every copied skill (same source)?
3. The parity policy. Is a Claude-only remote MCP connector set ever acceptable, or does the policy stay absolute? ADR-001 assumes absolute.
4. The cybersecurity pack's reopening conditions. ADR-004 names three: a second maintainer or an organisation, signed tags or release checksums, and a content review of a chosen subset. The operator may tighten or drop them.
5. The srt pin. Which version, and who owns the bump review (ADR-002)?
6. The Linux seat. When is the first Ubuntu seat run scheduled, and on which host (ADR-002)?
7. The dsh routes. Which Ollama Cloud plan or on-prem server, and is the official DeepSeek API ever acceptable for a client engagement given the request metadata it carries (ADR-006)?
8. The platform workflows. Should `ubuntu.yaml` and `macos.yaml` become required checks with a gate job, or stay optional (ADR-007)?
9. The security audit skill sweep. Upstream has been unmaintained since 2026-09-14, so the pinned snapshot carries every fix locally; the operator decides whether one recorded sweep is worth the asset (ADR-003).

Risks the research names and the kit accepts for now: same-user host processes read seat-writable files (gate G17); allowed domains are exfiltration paths because the proxy decides by hostname without TLS inspection; the trustd mach service is reachable by every seat (research/anthropics-sandbox-runtime.md, section 5.2). Facts the research could not verify are marked as such in each ADR: the DSH build on these hosts, the hook coverage of `dsh-hooks-claude-code`, the prototype's experiment numbers, the cybersecurity pack's branch protection and security advisories, and graphify's build time on this repository.

## References

Research files, under `research/`:

- `anthropics-knowledge-work-plugins.md` (ADR-001, ADR-004)
- `anthropics-sandbox-runtime.md` (ADR-002)
- `mukul975-anthropic-cybersecurity-skills.md` (ADR-004)
- `graphify-labs-graphify.md` (ADR-005)
- `shiguredo-deepseek-harness.md` and `deepseek-ai-dsh-superagent-prototype.md` (ADR-006)
- `tester-army-e2e.md` (ADR-007)
- `cloudflare-security-audit-skill.md` (ADR-003)

Architecture decision records, under `adr/`: ADR-001 composition model, ADR-002 sandbox layering, ADR-003 audit stack, ADR-004 third-party skill provenance, ADR-005 knowledge graph, ADR-006 DeepSeek harness seat, ADR-007 end-to-end testing.

Repository paths cited: `home/dot_agents/README.md`, `home/dot_agents/agent-config.yaml`, `scripts/validate-agent-assets.py`, `scripts/check-agent-runtime.py`, `scripts/orchestrator/README.md`, `docs/orchestrator-seat.md`, `docs/omp-skills.md`, `AGENTS.md`, `home/dot_local/bin/common/executable_pr-audit.sh`, `home/dot_local/bin/common/executable_pr-merge.sh`, `home/dot_local/bin/common/executable_hcom-seat`, `home/dot_mise/config.toml`, `.github/workflows/test.yaml`, `.github/workflows/ubuntu.yaml`, `Makefile`.

The decision trail is `decisions.tsv` in this directory.
