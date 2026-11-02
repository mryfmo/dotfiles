# ADR-006: DeepSeek harness seat, an optional fourth seat vendor

Status: accepted
Date: 2026-11-02

## Context

DeepSeek Harness (DSH) is a full agent runtime built on the Cordis plugin framework: agent loop, tool registry, session log, sandbox, subagents, Web and desktop UI, SDK and ACP servers, all as plugins (research/shiguredo-deepseek-harness.md, sections 1 and 3). It targets the official DeepSeek API first and any other provider or local server through a pi-ai based adapter with `openai-completions`, `openai-responses` and `anthropic-messages` protocols (section 4). It is a developer preview with breaking changes promised and no security audit; with the official route, shipped profiles upload the session log and the plugin inventory with each request, default on (section 7).

shiguredo/deepseek-harness is a fork: upstream `master` plus one squashed commit by one author, rebased at will, with no npm package and no CI of its own (section 2). Its substantive changes are a bundled Ollama Cloud catalog, peak-hour routing, session-log upload off by default and a `git push` guard (section 2.1). Upstream's adapter already accepts a hand-declared Ollama Cloud route (section 8.2).

deepseek-ai/dsh-superagent-prototype is a DSH bundle, not a fork or a port: a proactive GitHub agent with a Router and Worker split, Tickets with immutable Mandates, Subscriptions and an `off` / `observe` / `auto` accept ladder (research/deepseek-ai-dsh-superagent-prototype.md, sections 1 and 4). Running it needs a pinned pre-release harness, tmux, a dedicated GitHub user account with write access and workers under `danger-full-access` as the operator's OS user (section 6). It is a one-commit research prototype with issues and pull requests disabled (section 2).

This repository has no DeepSeek, Ollama or local-model route (research/shiguredo-deepseek-harness.md, section 8). Model ids live in `model_profiles` only, and the validator refuses a model set elsewhere (`scripts/validate-agent-assets.py:1510-1511`). The seats are contained by srt (ADR-002), and the command policy denies the dangerous GitHub writes (`home/dot_agents/agent-config.yaml:199-234`). Upstream ships `dsh-hooks-claude-code` and `dsh-hooks-codex`, experimental plugins that run a Claude Code `hooks.json` or Codex hook points inside a DSH session (section 8.1).

## Decision

DSH becomes an optional fourth seat vendor pinned to an upstream tag, never the one-commit fork, with a rendered profile patch: session-log upload off, Ollama Cloud or on-prem routes, the kit's Claude hooks mounted. The superagent prototype is design reading (Mandate, Ticket, Subscription, observe before auto), not a service.

Concrete rules:

1. Pin: a `dsh` `assets:` entry names `deepseek-ai/deepseek-harness` at a release tag with a sha256. The shiguredo fork is never a dependency; its fourteen changes are a watch list (section 8.3).
2. Profile: the kit renders `$DSH_HOME/profiles/<kit-profile>/cordis.patch.yml` from `agent-config.yaml`, as the omp overlays are rendered, with `session-log-deepseek.enabled: false`, an `ollama-cloud` route and any on-prem vLLM route under `llm-pi-ai`, `dsh-hooks-claude-code` pointed at the rendered Claude hooks, and the `headless` or `sdk` profile for automation (section 8.3).
3. Routes: seats default to Ollama Cloud or on-prem; the official DeepSeek API is opt-in per engagement because of the request metadata it carries (section 8.3).
4. Models: every model id the dsh seat uses is a `model_profiles` entry; the renderer copies it into the profile patch.
5. Containment: a dsh seat runs under the same srt boundary as an omp seat or not at all; the runtime's own sandbox is not the boundary (research section 7, `SAFETY.md` as quoted).
6. The prototype: its domain model and prompt corpus are cited as design; nothing of it runs. If a proactive seat is ever added, it starts in `observe` mode and moves to `auto` only by a decisions row (research/deepseek-ai-dsh-superagent-prototype.md, section 8).

Forbidden: the shiguredo fork as a source; a profile with the session-log upload on; `danger-full-access` workers; a dedicated agent GitHub user account created for the prototype; Node 24.9 or newer installed outside mise for it (section 7).

## Alternatives considered

- Adopt DSH as the primary harness in place of omp and the bridge. Rejected: developer preview, breaking changes promised, no security audit, and its Anthropic route is API-key only, so it cannot take over the subscription-based seats (research/shiguredo-deepseek-harness.md, sections 1 and 8.2).
- Track the shiguredo fork for its Ollama Cloud catalog and push guard. Rejected: a one-commit personal fork rebased at will with nothing on npm; the catalog is one hand-declared route upstream, and the push guard's policy is already expressed by the command policy (section 8.2).
- Run the superagent prototype as a service on a disposable host. Deferred: it needs `danger-full-access`, a dedicated GitHub user and tmux, all against the sandbox stance; treat it as reading material until a disposable host exists (research/deepseek-ai-dsh-superagent-prototype.md, section 8).
- No DeepSeek route at all. Rejected: on-prem or client-restricted engagements where Anthropic and OpenAI endpoints are not allowed have no other credible route in the kit (research/shiguredo-deepseek-harness.md, section 8.1).

## Consequences

Positive:

- One config surface for DeepSeek V4.1 Flash, V4 Pro, GLM, Kimi, GPT-OSS and self-hosted vLLM or Ollama (research/shiguredo-deepseek-harness.md, section 8.1).
- The existing Claude hooks gate the seat without new code, if `dsh-hooks-claude-code` covers the hook set.
- Cross-harness delegation in both directions becomes possible through the ACP profile and the Claude Code and Codex subagent plugins (section 8.1).
- The kit gains a published vocabulary for authorised work: Mandate, Ticket, Subscription (research/deepseek-ai-dsh-superagent-prototype.md, section 8).

Negative:

- A fourth runtime to pin, render and doctor, on Node 24.9 or newer (section 6).
- Not tested: whether upstream builds on these hosts, whether `dsh-hooks-claude-code` covers this repository's hook set, and whether DSH's ACP profile interoperates with omp (section 9).
- Shiguredo's performance claims are one data point, not a benchmark (section 8.1); the prototype's experiment numbers are self-reported through secondary sources (research/deepseek-ai-dsh-superagent-prototype.md, section 7).

Units created:

- The dsh asset pin and the rendered profile (rollout phase 4).
- A hook-coverage check of `dsh-hooks-claude-code` against `home/dot_claude` before the seat is relied on (phase 4).

## Verification

`bdd/dsh-seat.feature`, run by `check.py --holds-today` for the scenarios that hold today:

- `@R-24`: no DeepSeek or Ollama route exists today (holds today); the dsh asset is pinned to an upstream release tag (target).
- `@R-25`: the rendered profile turns session-log upload off; seats default to Ollama Cloud or on-prem routes; the kit's Claude hooks gate the seat (all target).
- `@R-26`: model ids live in `model_profiles` only (holds today).
- `@R-27`: the superagent prototype is not deployed (holds today); a proactive seat, if ever added, starts in observe mode (target).
