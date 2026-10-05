# AGMSG-TASK dotfiles-T86-codex-orchestrate-a01

Drafted 2026-10-05 by the orchestrator seat from the approved correction plan (Phase 7, dotfiles-T86). Depends on T85 (`herdr-agents --directive`, `orchestrator_kind`). New files plus a README section; disjoint from everything else once T85 merges.

## Objective

Principle 4 and 5 (codex→codex / codex→claude): a Codex orchestrator driven by a `codex exec` loop, equivalent in protocol (not in TUI) to the Claude pair.

1. **`home/dot_local/bin/common/executable_codex-orchestrate`** (bash, ≤ 150 lines, shdoc comments): usage `codex-orchestrate [--max-turns N] [--timeout SECONDS] [--team T] "<operator task>"`, run from the repository root.
   - Requires `HERDR_AGENTS_ORCHESTRATOR_KIND=codex` (from `~/.agents/model-profiles.env`, as `herdr-agents` resolves it); otherwise exit 2 naming `herdr-agents`.
   - **Seat exchange (idempotent):** in the main checkout, `leave.sh` every `claude-code` identity registered there that is not the worker seat, then `AGMSG_RESOLVE_PROJECT=0 join.sh <team> codex-<profile>-<suffix> codex <repo>` where `<profile>` is the interactive Codex profile and `<suffix>` the project suffix `herdr-agents` derives; record the previous Claude identity so `--restore` (or exit) can re-join it.
   - **Turn 1:** `codex $MODEL_PROFILE_<INTERACTIVE>_CODEX_ARGS exec -C <repo> -o <out>.last.md "$(herdr-agents --directive)"$'\n'"<operator task>"`, with the interactive profile args sourced from `~/.agents/model-profiles.env` (never ad-hoc model flags).
   - **Loop:** poll `inbox.sh <team> <name>` every 15 seconds (default timeout 1800 s, `--timeout`); on a delivered body, `codex … exec resume --last -o <out>.last.md "<body>"`; stop on `ORCHESTRATION-DONE` in the last message or at `--max-turns`.
   - **Transcript:** append each prompt and final message to `.orchestration/validation/codex-orchestrate-<YYYY-MM-DD>-<n>.md` (the `<n>` increments per run).
   - Workers reach it with `send.sh --body-file` (pane-less member convention).
   - **VERIFY gate:** whether the project `.codex/hooks.json` Stop hook (`check-inbox.sh codex`) fires under `codex exec` and consumes deliveries inside the turn; if so, replace the poll with `exec resume --last` on an empty prompt after each exec and document the finding. Paste the probe.
2. **`tests/unit/test_codex_orchestrate.py`:** fake `codex`, `herdr-agents`, `inbox.sh`, `join.sh`, `leave.sh` that record argv; assert the argv sequence (exec → resume --last), the identity exchange calls and their idempotence, the poll/timeout and `--max-turns` stop, and that the model args come from the env file (no literal model token in the script; `make validate-agent-assets` must not find one).
3. README: a `codex-orchestrate` usage section next to the herdr-agents one (how to launch, what it exchanges, how workers answer).

Forbidden: panes/tmux/Herdr topology; ad-hoc `--model`/`--profile` flags; parallel `codex exec`; changes to `herdr-agents`.

[memory:decision] dotfiles-T86 (operator 2026-10-03): `codex-orchestrate` runs a Codex orchestrator as a `codex exec` loop (first turn seeded with `herdr-agents --directive`, then `exec resume --last` per delivered agmsg body), exchanging the main-checkout seat identity idempotently and logging each turn under `.orchestration/validation/`; model args come only from `~/.agents/model-profiles.env`.

## Repo / branch

- Work ONLY in your own worktree. `git fetch origin`; `git switch -c feat/codex-orchestrate --no-track origin/main`. Verify the dispatched task_rev; else stop and PONG blocked.
- Strict status checks: if `main` moves, `gh pr update-branch <pr>` and wait for CI again before RESULT.

## Allowed files

- `home/dot_local/bin/common/executable_codex-orchestrate` (new), `tests/unit/test_codex_orchestrate.py` (new), `README.md` (the new section), `scripts/validate-agent-assets.py` only if the launcher inventory must list the new executable
- `.orchestration/{reports,validation,sandboxes,learning,autoskill/runs}/dotfiles-T86-codex-orchestrate-a01.md` (main checkout)

## Validation commands (paste verbatim output)

```
git diff origin/main --stat
mise x shfmt -- shfmt -i 4 -sr -d home/dot_local/bin/common/executable_codex-orchestrate; shellcheck home/dot_local/bin/common/executable_codex-orchestrate
wc -l home/dot_local/bin/common/executable_codex-orchestrate
uv run python -m unittest tests.unit.test_codex_orchestrate -v 2>&1 | tail -5
make unit-test 2>&1 | tail -3
make validate-agent-assets
gh pr checks <pr-number>
gh api repos/mryfmo/dotfiles/pulls/<pr-number> --jq '.mergeable_state'
```

## Completion

1. PR to `main`, English title/description ending with `🤖 Generated with [Claude Code](https://claude.com/claude-code)`. CI green on the final head, branch up to date.
2. After the final push: Bot wait per the agmsg-orchestration SKILL Worker Playbook (diff head only, timestamped); fix P0/P1 inline findings; do not resolve threads.
3. Artifacts at the exact expected paths; validation with verbatim outputs, PR number, head SHA, the VERIFY probe.
4. CompactionDB `memory add --kind decision --scope project` with the `[memory:decision]` text (Claude seat) or say the orchestrator records it (Codex seat).
5. `AGMSG-RESULT v1 task_id=dotfiles-T86` via `agmsg-dispatch dotfiles <your identity> claude-remediation-dot wT:p1 "<single line>"`. `cost:` line. max_turns=40.

## Dispatch

- 2026-10-05 07:25Z to `codex-security-dot-a007` (worker-e, wT:p8), in parallel with T85 (a005): new files only, disjoint from everything in flight; the README section is its own. The dependency on T85 is soft: call `herdr-agents --directive` as the T85 task file specifies (one `agmsg-orchestration:` line, exit 0, no Herdr needed) and cover it with the fake CLI; the live run of `codex-orchestrate` waits for T85 and T84 on `main` and is T87 work. Branch from `origin/main` 2527be54 or later with `--no-track`. Artifacts in your worktree; the orchestrator transfers them.

### PONG decision (orchestrator, 2026-10-05 07:40Z) — VERIFY probe deferred to T87

The in-process `codex exec` probe cannot run from the Codex worker sandbox (read-only runtime home); do not escalate. Implement the poll loop as specified (inbox.sh every 15 s, `exec resume --last` per delivered body) and make the delivery mode a one-line switch in the script (`CODEX_ORCHESTRATE_DELIVERY=poll|hook`, default `poll`) so T87's live run can flip it if the Stop hook turns out to consume deliveries under `codex exec`. Record the probe attempt (exact command, exit, boundary) in the validation file as the VERIFY outcome and list the open question for T87 in the report. The worker-side `-worker-crit.json` / `-worker-review-receipt.md` are authorized as in your previous tasks. Proceed to PR, CI, Bot wait, RESULT.

### PONG decision 2 (orchestrator, 2026-10-05 07:50Z) — seat exchange via reset.sh

Authorized. `leave.sh` removes the whole identity (every team), and `team.sh --json` reads worker panes (forbidden), so the seat exchange uses the project-scoped `AGMSG_RESOLVE_PROJECT=0 reset.sh <repo> <type> <name>`: snapshot every team/name row of the identity to exchange (from the store's metadata, no pane read) before the reset, join the Codex orchestrator identity, and on exit (or `--restore`) reset it and re-join the snapshotted rows. The existing worker seat and any other project's registrations are never touched. Document the snapshot/restore file location (under `~/.agents/skills/agmsg/run/`, matching the launcher's conventions) in the README section. Keep the script within the line budget; if the restore logic pushes it over 150 lines, say so in the report rather than cutting error handling.

### Scope note from T85 (orchestrator, 2026-10-05 08:30Z)

The seat exchange also sets agmsg delivery for the Codex orchestrator identity (`delivery.sh set turn codex <repo>`) and restores the Claude identity's delivery mode (`both`) on exit/`--restore`; cover it in the fake-CLI argv assertions. Reason: `herdr-agents --bootstrap-agmsg` configures delivery for the Claude pair only (Codex Bot thread 4179731976 on PR #270).

## Revise round 1 (orchestrator, 2026-10-05 08:50Z) — task-level audit of 567c8d17 is `incorrect` (3)

1. **Global name collision (P2).** Before joining `codex-<profile>-<suffix>`, search every `~/.agents/skills/agmsg/teams/*/config.json` (the SKILL's identity rule) for that name; if it is registered at a project other than this checkout, refuse with exit 2 naming the conflicting project (inboxes are team/name addressed, so a shared name would let two sessions consume each other's messages). Replace the test that accepts a same-name registration elsewhere with one that asserts the refusal.
2. **Completion protocol in the prompt (P2).** Append one fixed sentence to the first-turn prompt (after the directive and the operator task): "When the orchestration is complete, end your final message with the line `ORCHESTRATION-DONE`; otherwise end the turn and wait for the next agmsg delivery." Assert it in the argv tests.
3. **Existing seat in several teams (P2).** The reuse check must compare distinct identities, not the whole TSV listing against one row: an existing `codex-<profile>-<suffix>` registered at this checkout in one or more teams is the same seat and is reused (its team memberships preserved, `--team` selects the team to listen on); a different Codex name at this checkout is the refusal case. Test both.

One commit, then CI, Bot wait on the new diff head (timestamped), RESULT; `gh pr update-branch 271` if `main` moved. Keep the line budget note honest (report the count).

### PONG decision 3 (orchestrator, 2026-10-05 09:15Z) — round-1 Bot findings

1. **4179854338 (marker as the final non-blank line):** authorized; a second fix commit in round 1 is fine. `ORCHESTRATION-DONE` counts only as the last non-blank line of the final message; regression tests for a marker mentioned mid-message.
2. **4179854340 (raw transcripts under `.orchestration/validation/`):** keep the transcripts there (they are the evidence the task requires and the boundary commit tracks them); do **not** gitignore them. Instead, mask them the way the audit lane masks its transcripts: after each turn, run `uv run --with pyyaml scripts/validate-agent-assets.py --mask-secrets <out>.md <out>.last.md` (the repository's masker; the orchestrator runs the same before every boundary commit) and record the masker's line in the transcript footer. If the masker is unavailable the launcher refuses to start (exit 2 naming the script), so an unmasked transcript is never left behind. Tests: a fake masker records the argv per turn.

### PONG decision 4 (orchestrator, 2026-10-05 09:25Z) — supersedes decision 3 on transcript location

Authorized, third fix commit in round 1. The Bot is right that the known-pattern masker is not a secret scanner, so raw prompts and final messages do not belong in the repository:
1. Raw prompts and final messages go to a private, user-only directory outside every child writable root: `${XDG_STATE_HOME:-$HOME/.local/state}/codex-orchestrate/<date>-<n>/` (mode 0700; `umask 077` already), never under `~/.agents/skills/agmsg/run` (child-writable) and never under the repository.
2. The repository transcript `.orchestration/validation/codex-orchestrate-<date>-<n>.md` keeps only the non-secret turn status: turn number, timestamps, exit code, byte count of prompt and final message, whether `ORCHESTRATION-DONE` ended it, and the private file paths; no `.last.md` in the repository.
3. Prompts and resumes are piped to `codex exec … -` / `codex exec resume --last -` on stdin, never as an argv word (a 140 KiB inbox body must not hit the argv limit).
4. `CODEX_ORCHESTRATE_DELIVERY=hook` is refused with exit 2 ("not validated; T87") instead of spinning on empty resumes; the switch stays so T87 can enable it after the live VERIFY.
5. Tests updated for all four; README section updated (private location, what the repository file contains, the stdin contract, the hook refusal). Then CI, Bot wait on the diff head, RESULT.

### PONG decision 5 (orchestrator, 2026-10-05 09:30Z) — bounded contract for the private directory

Do not try to prove coverage of every effective Codex writable root (system, profile, managed config, CLI layers). The contract is bounded and documented: the private directory lives under `${XDG_STATE_HOME:-$HOME/.local/state}/codex-orchestrate/`, a path this repository's managed Codex config and `herdr-agents` never grant as a writable root (the granted roots are the repository/worktree, the agmsg store directories under `~/.agents/skills/agmsg/`, the git common-dir subpaths and the temp dir). The launcher asserts only the three negatives it can check (not under the repository top level, not under `~/.agents/skills/agmsg`, not under `${TMPDIR:-/tmp}`), refuses otherwise, and the README states the assumption in one sentence ("an operator who adds `~/.local/state` to Codex's writable roots re-exposes the transcripts"). No Codex permission overrides, no manifest edit. Capturing stdout/stderr privately is approved.

### PONG decision 6 (orchestrator, 2026-10-05 10:00Z) — three round-1 Bot threads on c3bd7af0

1. **4179976124 (lock):** move the launcher lock into the private state directory (`${XDG_STATE_HOME:-$HOME/.local/state}/codex-orchestrate/locks/<repo-hash>/`, keyed by the canonical repository path), created before any identity change; the repository holds no lock file.
2. **4179976127 (snapshot):** the recovery snapshot (`registrations.tsv`, `context.txt`) moves to the same private state directory (`…/codex-orchestrate/<date>-<n>/`), as decision 4 already does for the raw transcripts; nothing under `~/.agents/skills/agmsg/run`. README recovery steps follow.
3. **4179976130 (teams):** join the replacement Codex identity to every team the exchanged Claude registrations had (so workers in each team can address it); `--team` selects only the inbox to poll (default: the single team when there is one, required when there are several); restore re-joins every snapshotted row as before. Tests for the multi-team exchange and for `--team` selection.

Fourth fix commit in round 1, then CI, Bot wait on the diff head (timestamped), RESULT. The six earlier threads are resolved by the orchestrator at acceptance against the final head.
