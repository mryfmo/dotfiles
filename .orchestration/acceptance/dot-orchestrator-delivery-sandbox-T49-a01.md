# Acceptance: dot-orchestrator-delivery-sandbox-T49-a01

Dispatched 2026-10-01T03:31:52Z (msg 574, task_rev 00ba4a20…). PONG alive
03:53Z after a liveness PING (worker waiting on PR CI). RESULT 04:02:50Z (msg
577): PR #219, head 4452516, CI all pass, CLEAN.

## Round 1 review (orchestrator, from git objects)

- `claim_orchestrator_seat`: guards (scripts present, main checkout, exactly
  one non-worker claude-code identity) before any herdr call; launcher side
  resolves sid via `herdr agent list` (`agent_session.value`, the field the
  orchestrator saw in its own pane JSON) and pid via `herdr pane process-info
  --pane` (`foreground_processes[].name == claude`), probed by the worker on
  its own pane only; `AGMSG_SELF_NAME=off` prevents renaming the caller's
  pane; outputs ok/unresolved/failed; never a bare lock. Call sites: end of
  `start_claude_in_pane` and the `--attach` block before the managed early
  exit. Doctor check `orchestrator_seat_lock_warnings` (bare id + live claude
  in the repo via /proc). SKILL/rule bullets. 5 tests with negative check. 639
  tests OK; CI green.
- Codex GitHub P1 `:408`: the `--self` path relies on
  `CLAUDE_CODE_SESSION_ID`/`CLAUDE_PID`. Orchestrator verification:
  `/proc/14375/environ` (the live orchestrator claude) has neither variable;
  the Bash-tool shell child has both (injected for the tool), the socat child
  none → a SessionStart hook very likely has none → restore path would be
  `unresolved`. Confirmed → r2 (stdin `session_id` + ppid walk + herdr
  fallback).
- Codex audit of 4452516 (`…-audit-4452516.md`, gpt-6-astra): **incorrect**,
  three findings, all confirmed: P2 a live bare lock makes the composite claim
  `held` (exactly what the orchestrator hit this session and fixed by
  removing the lock) → r2 same-sid replace; P1 the SKILL text tells workers to
  use the unsandboxed retry, contradicting the no-escalation rule → operator
  decision: add `agmsg-dispatch` to `claude.sandbox.excludedCommands` with
  E2E evidence, docs rewritten → r2; P2 the claim stub always succeeds and no
  live fresh/restore verification exists → r2 tests + live legs after the
  operator's `make update` and relaunch (rule: live desktop behaviour is
  accepted only after both legs).
- Worker deviations accepted: real `agmsg-dispatch` argument form (pane id,
  not `<socket>:<pane>`) corrected in the docs; full-mode timing
  (`unresolved` right after `agent start`, then the SessionStart `--self`
  claim lands) documented; `/clear`/`/compact` new-sid case documented as an
  upstream liveness limitation.

**Decision (round 1): REVISE r2** (task_rev 3c71b553d2c11749…). Final acceptance
waits for the live legs.

## Round 2 review (2026-10-01, RESULT msgs 583/587, final head 9dc4e53)

Commits 50ebfdc (r2), 68ac54d (r2-b allow rule), 99d734b (CI: bash `read -t`
instead of GNU timeout), 1fa2a48 (r2-c per-team loop), e4903a1 (r2-d open-pipe
test), 63d4e03 (r2-e same-sid composite), 9dc4e53 (r2-f dead-pid only), each
read from git objects; audits: 50ebfdc incorrect (P1 allow rule → 68ac54d; P2
per-team loop → 1fa2a48), 99d734b incorrect (P2 bash 3.2 discard → e4903a1
documents the herdr fallback), 63d4e03 incorrect (P1 live sibling's lock →
9dc4e53), the rest correct. 649 tests OK, render-check, validate, shellcheck;
CI green Linux+macOS; CLEAN. Operator decisions recorded: `agmsg-dispatch`
in `claude.sandbox.excludedCommands` and the first managed
`permissions.allow` rule `Bash(agmsg-dispatch:*)` — **user-visible impact:
every Claude session on the managed settings runs `agmsg-dispatch` outside
the sandbox without confirmation.** Orchestrator verification: Claude Code
docs (permissions, "Compound commands"): "Claude Code is aware of shell
operators, so a rule like `Bash(safe-cmd *)` won't give it permission to run
`safe-cmd && other-cmd` … A rule must match each subcommand independently" →
the Codex P1 "allow rule authorises command chains" is **not applicable**.
Remaining Codex comments on 9dc4e53, both valid: P2 any main-checkout pane's
SessionStart can claim the orchestrator seat; P1 on macOS an open hook pipe
plus a herdr lookup that is not ready yet ends `unresolved`.
**Decision (round 2): REVISE r3** (pane gating, byte-wise payload read + herdr
retry, docs quote in the manifest comment; task_rev bcea585968bc1314…).

## Round 3 review and acceptance for merge (2026-10-01, RESULTs msgs 594/600, final head 00268f1)

Commits since 9dc4e53: 9b658a9 (r3: claim only from the orchestrator-labelled
pane, byte-wise payload read, herdr lookup retry 3×, docs quote in the manifest
comment), 229896a (r3-b: overall 2 s read deadline; audit measured 2.0 s vs
6.0 s on the parent), 11d87f3 (r3-c: a same-session composite lock is live
only when its pid is a running `claude`, so a recycled pid is stale),
00268f1 (test: `copyfile` + `chmod` — `copy2` of `/bin/sleep` fails on macOS
chflags; the orchestrator read the failed macOS job log). Each read from git
objects; audits: 9b658a9 incorrect (P2 per-byte timeout reset → 229896a), the
other three correct. 652 tests OK; render-check, validate, shellcheck; CI
green Linux+macOS; CLEAN.

Full-PR audit ledger (12 non-merge commits): 4452516, 50ebfdc, 99d734b,
63d4e03, 9b658a9 incorrect — every finding fixed by the following commit;
68ac54d, 1fa2a48, e4903a1, 9dc4e53, 229896a, 11d87f3, 00268f1 correct.

PR #219 sweep on 00268f1 (27 items): six Codex inline comments fixed
(50ebfdc, 99d734b, 63d4e03, 9b658a9 ×2, 11d87f3); "allow rule authorises
command chains" not-applicable — refuted by the permissions docs the
orchestrator fetched ("Claude Code is aware of shell operators … A rule must
match each subcommand independently"; `excludedCommands` matches the first
word only, so a chained command leaves the sandbox but still prompts for the
unmatched subcommand); 20 non-review items not-applicable.

Operator decisions carried: `agmsg-dispatch` in `claude.sandbox.excludedCommands`
and the first managed `permissions.allow` rule `Bash(agmsg-dispatch:*)`.
**User-visible impact: every Claude session on the managed settings runs
`agmsg-dispatch` outside the sandbox without confirmation** (first word only;
chained subcommands still prompt).

CompactionDB (main): 2b18cc6f (r1), ea6729a4 (r2), 5e42e6d7 (r2-b) stand.

**Decision: ACCEPTED FOR MERGE; acceptance final after the live legs.** Merge
PR #219 (squash, no `--delete-branch`). Then the operator runs
`make -C ~/.local/share/chezmoi update` and relaunches the pair; the
orchestrator records leg A (fresh start) and leg B (persisted restore) per the
worker's checklist: `seat_claim=ok owner=<sid>.<pid>` in `herdr-agents.log`,
composite lock file, Stop-hook delivery of a worker message, a worker
`agmsg-dispatch` wake with no prompt, `seat_claim=skipped` for a non-orchestrator
main-checkout pane, and `replaced_stale_lock=yes` once if a stale lock was
left. Residual, documented: a `watch.sh` Monitor still cannot run under the
pid-namespaced sandbox (upstream); turn delivery plus the worker wake is the
working path.

cost: worker ~85k+45k+35k+30k context tokens across rounds (session counters; no per-task figure)
