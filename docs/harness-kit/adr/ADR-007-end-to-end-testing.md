# ADR-007: End-to-end testing without tester-army/e2e

Status: accepted
Date: 2026-11-02

## Context

tester-army/e2e is a framework: an SDK, a test runner and a CLI, published to npm, with an engine contract behind it. It drives browsers through Playwright and iOS and Android devices through agent-device, and nothing else; there is no engine for a terminal, a shell script or a coding agent as the system under test (research/tester-army-e2e.md, Verdict, "What it drives"). Claude Code and Codex appear in it only as the executor that drives a browser or device over the Agent Client Protocol ("The execution model"). It is pre-1.0, telemetry is on by default, test files and engines run with the runner's full OS authority, and its CI toolchain needs Node 22.22.3 or newer, pnpm, a Chromium download and a model key or an ACP login ("Vitals", "Risks and caveats", "The CI jobs").

Nothing in this repository has a browser or device surface. The bootstrap is `setup.sh` and the chezmoi apply; the agent stack is terminal, socket and file driven; the only HTTP listeners are two loopback helpers ("Fit against this repository"). Coverage today is `ubuntu.yaml` and `macos.yaml`, which run `setup.sh` from the checkout twice and then the Bats file suites; `apply-check.yml` and `make apply-check`, which apply the working tree in a container with `--network none` (`Makefile:65`); and `test.yaml`, which runs Python unittest and Bats across the matrix ("The bootstrap"). `AGENTS.md:35-36` keeps Bats in CI. `test.yaml` says a required check must always report a final status and carries no workflow-level path filter (`.github/workflows/test.yaml:4-8`); `ubuntu.yaml` and `macos.yaml` filter by `paths:` at the workflow level and are therefore not required checks (`ubuntu.yaml:6-18`; research "Patterns worth comparing").

The research names patterns worth comparing: one gate job per workflow with a `changes` job for path filtering, committed recordings replayed read-only with a strict-cache failure, a written trust model, and a benchmark that lists behaviour differences before timings ("Patterns worth comparing").

## Decision

tester-army/e2e is not adopted as a test tool. Its CI patterns are compared, and its skill is listed for a future web or mobile project.

Concrete rules:

1. No `e2e` package, Playwright download, PostHog telemetry or `AI_GATEWAY_API_KEY` enters the repository, its Makefile, mise configuration or workflows.
2. The bootstrap and the seats stay covered by Bats, Python unittest and throwaway containers; Bats runs in CI only (`AGENTS.md:35-36`).
3. A comparison unit records, for `ubuntu.yaml` and `macos.yaml`, whether each stays an optional check with its workflow-level `paths:` filter or gains a `changes` job and a `<workflow> gate` job so it can be required; the record is a decisions row, and any change is its own unit.
4. The recorded-replay idea is noted as a cost control the verdict loop has no analogue for; no unit is created for it until a measured run shows the cost.
5. When a project with a browser or device surface starts, the `e2e` skill is installed for that project with a `skills.audience` entry, under ADR-004's provenance rules, and nothing in this repository changes for it.

Forbidden: an `e2e` dependency on a CI hot path; `npx ...@latest` for it (`AGENTS.md` supply-chain rule as cited by the research); a browser suite against the loopback helpers, which the Python unit tests already cover.

## Alternatives considered

- Adopt `e2e` for the bootstrap or the agent stack. Rejected: there is no screen to observe, its natural-language steps have no vocabulary for "the apply left `.zprofile` unchanged", and the toolchain cost is real with no payoff (research/tester-army-e2e.md, "The bootstrap", "The CI jobs").
- Use its API-only mode against the loopback helpers. Rejected: the Python unit tests already do that without Node, Playwright or a model key ("The agent stack").
- Write a terminal engine for its engine protocol. Rejected: a from-scratch project with no user ("What it drives").
- Install the `e2e` skill in this repository now for future projects. Rejected: a skill nobody here invokes costs listing budget in Codex and a provenance review; it is a per-project install decision ("Fit against this repository").

## Consequences

Positive:

- No new toolchain, no telemetry, no model cost in CI.
- The CI patterns comparison gives the required-check question for the platform workflows a recorded answer.
- The trust-model sentence the research praises ("enqueueing is the trust decision") is available as a model for the kit's own threat tables.

Negative:

- A future web or mobile project gets no end-to-end tooling from the kit until it installs the skill itself.
- The recorded-replay cost control stays an idea with no owner.
- The platform workflows stay optional checks until the comparison unit decides otherwise.

Units created:

- The CI gate-pattern comparison (rollout phase 3).
- No unit for the skill.

## Verification

`bdd/e2e-testing.feature`, run by `check.py --holds-today` for the scenarios that hold today:

- `@R-28`: tester-army/e2e is not a dependency of the kit (holds today).
- `@R-29`: the bootstrap is run end to end in CI; the apply check runs offline in a container; Bats runs in CI, not on the operator's host (all hold today).
- `@R-30`: the unit-test workflow is never path-filtered at the workflow level (holds today); the gate-job pattern is compared for the platform workflows (target).
- `@R-31`: the e2e skill is installed only for a web or mobile project (target).
