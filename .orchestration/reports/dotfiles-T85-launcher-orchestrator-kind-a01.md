# Report: dotfiles-T85-launcher-orchestrator-kind-a01

- **Worker and branch:** `claude-standard-dot-a005` in worker-c, branch `feat/launcher-orchestrator-kind` from `origin/main` 2527be54 with `--no-track`. Earlier branches are untouched.
- **task_rev:** `sha256:5c036338…cd37f`, matched in the main checkout.
- **PR:** #270, https://github.com/mryfmo/dotfiles/pull/270.
- **Commits:** `5643ba22` (the change), `f50e6af7` (Codex P1 4179583135, P2 4179583130), `4d210709` (Codex P1 4179629453), `20361c5d` (Codex P1 4179692403, P2 4179692405).
- **Final head:** `20361c5d`. CI, branch and bot state are in the validation file.
- **Status:** ready_for_review.

## 1. What changed (`home/dot_local/bin/common/executable_herdr-agents`)

1. **`resolve_orchestrator_kind`:** mirrors `resolve_worker_kind`. It reads `HERDR_AGENTS_ORCHESTRATOR_KIND` from the environment, then sources `~/.agents/model-profiles.env` (manifest `orchestrator_kind`, which T84 renders), then defaults to `claude`. It validates `claude|codex`; anything else prints `orchestrator_kind must be claude or codex: <value>` and returns 2.
2. **Refusal:**
   - One guard runs right after `--help`, before any mode parsing. Every mode except `--bootstrap-agmsg`, `--add-worker`, `--remove-worker`, `--audit` and `--directive` (that is, full mode, `--attach` and `--restart-worker`) exits 2 under `codex` with `herdr-agents: orchestrator_kind=codex: use codex-orchestrate`.
   - It sits before the parser because `--attach` exits early in a plain shell (its bring-up summary) inside the parser. Under `codex`, that path also refuses, with no Herdr call, seat claim or agmsg join.
   - `--attach` from the manifest worker seat (`is_manifest_worker_seat`: the directory is its repository's `worker_worktree`) passes the guard and keeps its quiet exit, so a Claude worker's own SessionStart hook is not refused (Codex P2 4179583130 in `f50e6af7`).
   - `f50e6af7` first exempted every linked worktree. Codex P1 4179629453 showed that another linked worktree then slipped into the pair attach flow, so `4d210709` narrows the exemption to the manifest seat. The same helper now drives the existing quiet exit, so the two checks cannot diverge; every other attach is refused under codex.
   - In a main checkout the Claude SessionStart `--attach` shows the exit-2 message under `codex`. That follows the task's "attach exits 2"; `codex-orchestrate` (T86) takes over that seat.
3. **`--directive`:** takes no other argument (anything more is usage, exit 2). It prints `print_regime_directive "$(pwd -P)" <type>` and exits 0 before the guard and before any `require_command herdr`, so it works with no Herdr server. `<type>` is the orchestrator identity's agmsg type for the resolved kind: `claude-code`, or `codex` under the codex kind (Codex P1 4179583135, `f50e6af7`). The SessionStart caller keeps the `claude-code` default.
   - In the main checkout (a regime repository) it prints the one directive line, from a read-only run with this branch's script and no `herdr` on PATH. In worker-c, a linked worktree, it prints nothing.
4. **Worker modes under a Codex orchestrator** (Codex P1 4179692403, `20361c5d`): the orchestrator kind is resolved once at start for every mode, and its agmsg type (`claude-code` or `codex`) is the leader that `--add-worker` names and links the worker under and that `--remove-worker` despawns under, error messages included. The Claude seat claim (`claim_orchestrator_seat`) keeps `claude-code`, since a Codex seat claim is forbidden.
5. **Directive from a subdirectory** (Codex P2 4179692405, `20361c5d`): `--directive` resolves `git rev-parse --show-toplevel` before the identity lookup, falling back to `pwd -P` outside git. A start in `docs/` of the main checkout prints the line; a linked worktree's top level is not a main checkout, so it still prints nothing.
6. **Docs:** usage gains `herdr-agents --directive` and a paragraph on the refusal and directive mode; README has two sentences in the herdr-agents section.

## 2. Tests (`tests/unit/test_herdr_agents.py`, fake CLIs)

- `test_codex_orchestrator_kind_refuses_the_claude_pair_before_herdr`: full mode, `--restart-worker`, `--attach` in a pane and `--attach` in a plain shell each give exit 2, exactly the message on stderr, empty stdout, and no fake-CLI call log (no `herdr`, no agmsg join).
- `test_orchestrator_kind_comes_from_the_manifest_env_and_is_validated`: `codex` is read from `model-profiles.env`, and `zed` is rejected.
- `test_codex_orchestrator_kind_keeps_the_non_seating_modes`: `--bootstrap-agmsg` exits 0 under `codex`.
- `test_claude_orchestrator_kind_keeps_the_attach_summary`.
- `test_directive_prints_the_regime_line_without_herdr`: nothing in an unseated fixture, exactly one directive line in a seated one, PATH without `herdr`, and no `herdr` fake call.
- `test_directive_looks_up_a_codex_orchestrator_identity`: under `codex` the line names `codex-deep-dot`; under `claude` with no claude-code identity it prints nothing.
- `test_codex_orchestrator_kind_leaves_a_worker_worktree_attach_quiet`: exit 0, empty stderr, no calls.
- `test_codex_orchestrator_kind_refuses_attach_in_another_linked_worktree`: exit 2 with the refusal and no calls. It fails against `f50e6af7`, which went on into the pair flow.
- `test_add_worker_names_the_seat_from_a_codex_orchestrator_identity`: with only `codex-deep-dot` (codex type) registered, `--add-worker` fails under `claude` (no claude-code orchestrator) and succeeds under `codex`.
- The directive test also runs from a subdirectory and expects the same line.
- Both fail against `4d210709`.
- The two review tests fail against `5643ba22` (verbatim in the validation file).
- Against the `origin/main` launcher, all but the two pin tests fail (6 failures).
- The 229 herdr-agents tests and `make unit-test` (800) pass, along with shfmt, ShellCheck and `make validate-agent-assets`.

## 3. Codex bot

| Head | Result |
|---|---|
| `5643ba22` | Review at 22:20:21Z with three findings: |
| | P1 4179583135, "Select the Codex identity when printing its directive": `fixed:f50e6af7`. |
| | P2 4179583130, "Exclude worker SessionStart hooks from the Codex gate": `fixed:f50e6af7`. |
| | P1 4179583126, "Render the orchestrator-kind setting from the manifest": proposed `not-applicable` (see below). |
| `f50e6af7` | Review at 22:36:34Z. P1 4179629453, "Restrict the Codex attach exception to the actual worker seat": `fixed:4d210709`. |
| `4d210709` | Review at 22:58:24Z with three findings: |
| | P1 4179692403, "Resolve worker lifecycle leaders from the orchestrator kind": `fixed:20361c5d`. |
| | P2 4179692405, "Normalize directive lookups to the repository root": `fixed:20361c5d`. |
| | P1 4179692400, "Provide the advertised Codex orchestrator entrypoint": proposed `not-applicable` (see below). |
| `20361c5d` (final) | Review at 23:13:45Z. P1 4179731976, "Configure Codex delivery when allowing Codex bootstrap": proposed `not-applicable` (see below). |

Proposed `not-applicable`, with reasons:

- **4179583126 (render `orchestrator_kind` from the manifest):** the manifest and generator side is T84's. This task forbids "the manifest; the generator" and names T84 as the soft dependency that lands `HERDR_AGENTS_ORCHESTRATOR_KIND` in `model-profiles.env`. Until then the launcher's default `claude` keeps today's behaviour. T84 had not merged at the final head (no `orchestrator_kind` in the generator or manifest on `origin/main`).
- **4179692400 (the `codex-orchestrate` entrypoint):** that executable, and the Codex startup flow that calls `herdr-agents --directive`, are T86, dispatched in parallel to a007 per the task's Dispatch note. This PR provides the refusal and the directive it consumes.
- **4179731976 (Codex delivery in `--bootstrap-agmsg`):** this PR does not change bootstrap. The task only requires that it keep working, not refused, under either kind, and it does. Configuring turn delivery and identity checks for a Codex orchestrator seat is part of standing that seat up (T86, `codex-orchestrate`), and the task forbids Codex-seat work here.

The timestamped wait for the final head ends at "review found" (verbatim in the validation file). I did not reply to or resolve any thread.

## CompactionDB

```
$ cd ~/Workspace/dotfiles && python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content 'dotfiles-T85 (operator 2026-10-03): `herdr-agents` reads `HERDR_AGENTS_ORCHESTRATOR_KIND` (manifest `orchestrator_kind`); under `codex` the Claude-pair modes refuse with exit 2 and point at `codex-orchestrate`; `--directive` prints the regime directive line without Herdr so a Codex orchestrator'"'"'s first turn can carry it.'
d8bbd1c0-537b-49c9-a9a3-d7278a5be1f8
[exit 0]
```

[memory:decision] dotfiles-T85 (operator 2026-10-03): `herdr-agents` reads `HERDR_AGENTS_ORCHESTRATOR_KIND` (manifest `orchestrator_kind`); under `codex` the Claude-pair modes refuse with exit 2 and point at `codex-orchestrate`; `--directive` prints the regime directive line without Herdr so a Codex orchestrator's first turn can carry it.

## Artifacts

- validation: `.orchestration/validation/dotfiles-T85-launcher-orchestrator-kind-a01.md`
- sandbox: `.orchestration/sandboxes/dotfiles-T85-launcher-orchestrator-kind-a01.md`
- learning: `.orchestration/learning/dotfiles-T85-launcher-orchestrator-kind-a01.md`
- autoskill: `.orchestration/autoskill/runs/dotfiles-T85-launcher-orchestrator-kind-a01.md`

cost: n/a (no subagents, no model-driven runs; the runtime does not expose session totals).
