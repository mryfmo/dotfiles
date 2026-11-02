# ADR-002: Sandbox layering, srt for the omp seats and the Claude Bash sandbox, Codex on its own

Status: accepted
Date: 2026-11-02

## Context

Anthropic's sandbox-runtime (srt) is an Apache-2.0 process sandbox in beta research preview, built on `sandbox-exec` on macOS and bubblewrap on Linux, with a host-side HTTP and SOCKS proxy that decides by hostname (research/anthropics-sandbox-runtime.md, Summary and section 1). Claude Code's Bash sandbox is the same engine compiled into the binary; every `sandbox.filesystem`, `sandbox.network` and `sandbox.credentials` key of the managed settings is an srt key, and `enabled`, `failIfUnavailable`, `autoAllowBashIfSandboxed`, `allowUnsandboxedCommands` and `excludedCommands` are Claude Code's own (section 3.1, 3.2).

The repository already uses srt in two places. The Claude Bash sandbox in `claude.sandbox` is enabled, fails closed, refuses the unsandboxed retry and excludes exactly `git push *` and `gh *`, each behind an identical ask rule (`home/dot_agents/agent-config.yaml:896-919`, `home/dot_agents/README.md:33`). The omp seats run under srt: `hcom-seat` writes per-seat settings and a shim that runs a canary under them and refuses to start omp unless a write into the sandbox directory and reads of the settings file and `~/.ssh` all fail inside (`scripts/orchestrator/README.md:141-149`; research section 4.1). omp has no sandbox of its own, and its seat policies say approval is not containment (research section 4.1; `home/dot_agents/omp/policies/orchestrator.yml:7-10`).

Codex cannot be wrapped. Under srt, Codex's own Seatbelt profile fails with `sandbox_apply: Operation not permitted`, measured on this host; on Linux srt's seccomp helper refuses the `unshare` Codex's bubblewrap needs (research section 4.2). The audit lever already runs Codex under its own `audit` permission profile from the coordinator (`home/dot_local/bin/common/executable_pr-audit.sh`, header; research section 4.2).

The gap for the yolo seats was closed by unit U85 and gate G17 (research section 5.1). What remains is recorded in the research and in `scripts/orchestrator/README.md:171-173`: same-user host processes read seat-writable files, srt's own temporary directory is writable to every seat, a resumed or forked seat runs uncontained, the seats act with the operator's GitHub token until U88, allowed domains are exfiltration paths, Linux is unmeasured, and mise tracks `latest` of the srt package (`home/dot_mise/config.toml:24`) while `hcom-seat` encodes 0.0.81 behaviours (research section 5.2).

## Decision

srt stays the OS boundary for the omp seats and the engine behind the Claude Bash sandbox. Codex keeps its own sandbox. The kit pins the srt version in mise instead of `latest` and adds no sandbox of its own.

Concrete rules:

1. Every omp seat starts through `hcom-seat`, under srt, behind the fail-closed canary. A seat started any other way is uncontained and is not a seat of the kit.
2. The Claude Bash sandbox keeps `enabled: true`, `failIfUnavailable: true`, `allowUnsandboxedCommands: false`, exactly the two excluded commands, hostnames only in `network.allowedDomains`, no Unix socket listed and no `allowAllUnixSockets`, and every credential store denied with `mode: deny` (`validate-agent-assets.py:643-795`).
3. Codex runs under its own Seatbelt or bubblewrap sandbox and its permission profiles. No lever wraps Codex in srt.
4. `home/dot_mise/config.toml` names one srt version. A bump is a reviewed change whose pull request re-reads the behaviours `hcom-seat` relies on: the own-write paths, paths read as patterns, `*` as `[^/]*`, a deeper deny under an allow, `allowLocalBinding` as `*:*`, writes only to existing paths on Linux (research section 4.1).
5. No second sandbox engine, container runtime or VM layer enters the kit for the seats. The residuals of research section 5.2 are recorded as accepted or as units, never closed by a new tool.

Forbidden: `allowAllUnixSockets`, `allowLocalBinding`, `allowAppleEvents` and `enableWeakerNestedSandbox` in any seat or Claude settings; a `mask` credential entry, because the proxy would inject the real value into any request to an inject host (`scripts/validate-agent-assets.py:677-680`); `latest` for the srt package once the pin lands.

## Alternatives considered

- Wrap Codex in srt for a whole-process boundary. Rejected: measured failure on macOS, inferred failure on Linux, and the trade would drop Codex's per-command boundary (research section 4.2).
- Follow `latest` of srt as today. Rejected: the authors say the configuration format may evolve, an unknown key is silently ignored (issue #434), and a release that changed the `*:*` rendering or the own-write paths would move the boundary with no change in this repository (research section 5.2).
- A container or VM per seat instead of srt. Rejected: U85 and G17 accepted srt as the boundary with conditions, and nothing in the research shows a seat need srt cannot meet; the cost would be a new runtime on both hosts.
- Add `strictAllowlist`, `deniedDomains` or `credentials.files` masking to the seat settings now. Held as options: `strictAllowlist` changes nothing for the CLI, and a mask is Linux-only for files and carries the echo-back risk (research section 5.3).

## Consequences

Positive:

- One engine for the Claude Bash sandbox and the seats, already landed and measured on macOS.
- The pin makes the boundary a reviewed artifact instead of whatever npm serves.
- Codex keeps the per-command boundary and the permission profiles the audit lever already probes.
- No new runtime on either host.

Negative:

- A pinned beta package lags upstream fixes until someone reviews the bump.
- Linux is unmeasured, and the open Ubuntu issues of research section 2.2 may surface as canary refusals on the first run.
- The residuals of section 5.2 stay open until their units land: same-user host processes, srt's temporary directory, resumed seats, the operator's GitHub token, allowed domains, the trustd mach service.

Units created:

- Pin the srt version in mise (rollout phase 1).
- Record the residuals as decisions rows (phase 1).
- The first Linux seat run, measured (phase 3).

## Verification

`bdd/sandbox.feature`, run by `check.py --holds-today` for the scenarios that hold today:

- `@R-06`: the Claude Bash sandbox is strict and fails closed; no Unix socket switch is set (both hold today).
- `@R-07`: a seat starts only after its canary holds; seat approval is not containment (both hold today).
- `@R-08`: the srt version is pinned in mise (target).
- `@R-09`: the Codex audit runs under Codex's own permission profile, never under srt (holds today).
- `@R-10`: sandboxed commands cannot read the SSH keys (holds today); the first Linux seat run is measured (target).
