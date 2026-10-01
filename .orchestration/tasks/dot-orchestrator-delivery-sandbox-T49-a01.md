# AGMSG-TASK dot-orchestrator-delivery-sandbox-T49-a01

## Objective

Operator correction 2026-10-01: the orchestrator must receive worker
messages without being prompted. In session e7734322 (Herdr pair wN,
Claude Code 2.1.284 with the T39 sandbox active) both delivery paths were dead
and the orchestrator found every RESULT (msgs 546–564) by reading
`messages.db` directly. Root causes, verified in that session:

1. **Monitor path.** The SessionStart directive starts
   `watch.sh <sid>.<pid> <repo> claude-code` through the Monitor tool, which
   runs the command inside the Bash sandbox. The sandbox has its own pid
   namespace (4 processes visible; the shell is pid 2), so `kill -0 <claude pid>`
   fails with ESRCH and `agmsg_instance_alive` reports the session dead;
   `watch.sh` exits at once with "session … is no longer alive; stopping". The
   stale pidfiles it leaves hold the namespace pid `4`.
2. **Turn path.** `actas-claim.sh … <sid>` run from sandboxed Bash cannot
   resolve the claude pid ("instance-id falling back to bare session_id") and
   writes the **bare** sid as the lock owner. The Stop hook
   (`check-inbox.sh`, run by Claude Code outside the sandbox) normalises the
   payload's `session_id` to the **composite** `<sid>.<pid>`, so
   `actas_lock_state` returns `other:<bare sid>` and the hook exits 97 silently:
   it ran at every turn end (the `.lastcheck-<agent>` marker was touched) and
   delivered nothing. Re-creating the lock with the composite id made the same
   hook deliver the backlog (`decision: block` with 2 messages).

`~/.agents/skills/agmsg/**` is upstream and out of scope. Fix it in this
repository's launcher, docs and checks:

1. `home/dot_local/bin/common/executable_herdr-agents`: when it starts the
   orchestrator pane (full mode and the `--attach` heal), and when the
   SessionStart `--attach` runs inside the pane, claim the orchestrator seat
   **outside any sandbox** with the composite instance id: resolve the claude
   pid of the pane (the `herdr agent start` result / `herdr agent list` session
   mapping, or `pgrep` on the pane's process tree — verify which the real CLI
   offers with a safe command, not `--help` alone) and run
   `actas-claim.sh <repo> claude-code <orchestrator identity> <sid>.<pid>`. If
   the pid cannot be resolved, print one line `seat_claim=unresolved` and do
   not write a bare-sid lock. Print `seat_claim=ok owner=<sid>.<pid>` on success.
2. `home/dot_agents/skills/agmsg-orchestration/SKILL.md` and
   `home/dot_config/claude/rules/agmsg-orchestration.md`: one bullet each —
   the orchestrator seat lock must carry the composite id; a claim from
   sandboxed Bash writes a bare id and makes turn delivery skip silently; the
   check is `lock owner == <sid>.<pid>` (`cat ~/.agents/skills/agmsg/run/actas.<team>__<name>.session`),
   and a `watch.sh` Monitor cannot run under a pid-namespaced sandbox (it exits
   "no longer alive"); until upstream accepts a liveness override, turn
   delivery is the working path and an idle orchestrator is woken by the
   worker's `agmsg-dispatch` to the orchestrator pane, which the worker SKILL
   section must say (RESULT/PONG to a herdr-paned orchestrator go through
   `agmsg-dispatch <team> <worker> <orchestrator> <socket>:<pane>`, not bare
   `send.sh`).
3. `scripts/check-regime-boundary.sh` (T46 creates it; if T46 is not merged
   yet, add the check to `scripts/check-agent-runtime.py` doctor output
   instead): WARN when an orchestrator actas lock for the registered identity
   holds a bare session id (no `.<pid>` suffix) while a live claude session
   exists for that project.
4. Tests: `tests/unit/test_herdr_agents.py` — the pane start emits
   `seat_claim=…` with a fake `actas-claim.sh` capturing the composite id
   (one test ok, one unresolved); doctor/boundary check test for the bare-id
   WARN.
5. `make unit-test`, `make validate-agent-assets` green; PR (English) from
   `fix/orchestrator-delivery-sandbox`.

Out of scope: upstream agmsg (`watch.sh`, `check-inbox.sh`,
`actas-claim.sh`), the Claude Code sandbox manifest (a pid-namespace opt-out
is a T39 follow-up for the operator), model/profile values.

[memory:decision] T49: the orchestrator seat lock must hold the composite
`<sid>.<pid>`; a claim from sandboxed Bash writes a bare sid and the Stop-hook
delivery then skips silently (`other:`), and a `watch.sh` Monitor cannot run
under the pid-namespaced sandbox — herdr-agents claims the seat outside the
sandbox at pane start and a herdr-paned orchestrator is woken by worker
`agmsg-dispatch` (operator correction 2026-10-01).

## Repo / branch

- Work ONLY in `/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c`,
  sequentially after the task in flight there; branch
  `fix/orchestrator-delivery-sandbox` from `origin/main` (`git fetch` first).
- Sandbox deny-mount stubs are not dirt; explicit-path `git add`; push without
  `-u`; never remove `.git/*.lock`; ignore the Understand-Anything hook.

## Allowed files

- `home/dot_local/bin/common/executable_herdr-agents`
- `home/dot_agents/skills/agmsg-orchestration/SKILL.md`
- `home/dot_config/claude/rules/agmsg-orchestration.md`
- `scripts/check-regime-boundary.sh` (if present) or `scripts/check-agent-runtime.py`
- `tests/unit/test_herdr_agents.py`, `tests/unit/test_check_agent_runtime.py`
- `.orchestration/{reports,validation,sandboxes,learning,autoskill/runs}/dot-orchestrator-delivery-sandbox-T49-a01.md` (main checkout)
- `.agents/worklog/codex/**` waived.

## Forbidden actions

- Editing anything under `~/.agents/skills/agmsg/`; sandbox settings;
  model/profile values; pane reads; merge; force-push; `--delete-branch`;
  `.orchestration/acceptance/**`; local `bats`; claiming or touching the live
  orchestrator lock (`run/actas.dotfiles__claude-remediation-dot.session`).
- Escalating outside the sandbox/allowlist for approval: fail, PONG blocked
  with the exact command and boundary.

## Validation commands (verbatim output into the validation file)

- `make unit-test`
- `make validate-agent-assets`
- `shellcheck home/dot_local/bin/common/executable_herdr-agents`
- the real-CLI probe you used to resolve the pane's claude pid (safe form)
- `gh pr view <n> --json url,headRefOid,mergeStateStatus`
- `python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content "<the [memory:decision] above>"`

## Expected artifacts

- report/validation/sandbox/learning/autoskill at the paths above; report
  carries `cost:`, PR URL, head sha, the CompactionDB command.

max_turns=40. done_signal=AGMSG-RESULT v1.

## Orchestrator amendment r2 (2026-10-01; dispatched as AGMSG-ACCEPTANCE status=revise)

r1 (4452516) reviewed: the launcher-side resolution (`herdr agent list` →
`agent_session.value`, `herdr pane process-info --pane` → `claude` pid) is
grounded by your probe and matches the pane JSON the orchestrator saw; guards,
`AGMSG_SELF_NAME=off`, doctor check and docs are in place; 639 tests, CI
green. Four findings (Codex GitHub P1 `:408`; audit of 4452516: P2 `:421`,
P1 SKILL `:146`, P2 tests/live). Fix in one commit on
`fix/orchestrator-delivery-sandbox`:

1. **`--self` must not depend on `CLAUDE_CODE_SESSION_ID`/`CLAUDE_PID`**
   (`:408`). Orchestrator evidence: `/proc/<claude pid>/environ` of the live
   orchestrator process carries neither variable; the Bash-tool shell child
   has both (Claude Code injects them for the Bash tool), the `socat` child
   has none — so a SessionStart hook very likely has none and the `--self`
   path would print `seat_claim=unresolved` on every restore. Resolve the
   session id from the hook payload on stdin (`"session_id"` in the JSON Claude
   Code passes to hooks — upstream `session-start.sh` reads it the same way;
   bounded read, `[ ! -t 0 ]` guard, 2 s timeout as `check-inbox.sh` does),
   with the env variable only as a secondary source; resolve the pid by
   walking `ppid` from `$$` to the first ancestor whose `comm` is `claude`
   (as upstream `agmsg_agent_pid` does; `ps -o ppid=,comm= -p`), env
   secondary; if either is still missing, fall back to the launcher-side
   herdr lookup with `$HERDR_PANE_ID`. Never write a bare id.
2. **Repair a stale bare lock of the same session** (`:421`). When
   `actas-claim.sh` answers `status=held owner=<X>` and `<X>` equals our bare
   session id (same session, bare token from a sandboxed claim), remove that
   lock file and claim again; print `seat_claim=ok owner=<sid>.<pid>
   replaced_bare_lock=yes`. Any other owner stays `seat_claim=failed`. The
   doctor WARN's repair line becomes: "run `herdr-agents --attach` from the
   orchestrator pane outside the sandbox (it replaces a same-session bare
   lock)".
3. **Wake path without worker escalation** (SKILL `:146`; operator decision
   2026-10-01). Add `agmsg-dispatch` to `claude.sandbox.excludedCommands` in
   `home/dot_agents/agent-config.yaml` with one comment carrying the E2E
   evidence (this session: the herdr socket is `PermissionDenied` from
   sandboxed Bash; `agmsg-dispatch` outside the sandbox delivered msgs
   545–577 with `read_at` within seconds; the script only inserts one agmsg
   row and sends a herdr wake). Verify the exact `excludedCommands` matching
   semantics in the Claude Code sandbox docs
   (code.claude.com/docs/en/sandboxing) and state them in the comment (name
   match vs prefix). Regenerate the template (`make render-check` green);
   extend validator/tests if they pin `excludedCommands: []`. Rewrite the
   SKILL step 11 sentence and the rule bullet: workers send RESULT/PONG to a
   herdr-paned orchestrator with `agmsg-dispatch`, which the sandbox manifest
   excludes from sandboxing, so no retry prompt and no escalation; delete the
   "unsandboxed retry" wording. README sandbox section: one sentence for the
   new entry and its evidence. Codex workers are out of scope (their sandbox
   is Codex's); say so in the docs.
4. **Tests** (audit P2): add the `held` → same-sid replace case and a `held`
   by another owner → `failed` case; a `--self` test with the env unset and a
   stdin payload `{"session_id":"sid-stdin"}` plus the herdr fallback for the
   pid (the ppid walk is not unit-testable; say so); a render test that
   `excludedCommands` contains `agmsg-dispatch`.
5. **Live verification plan** (audit P2; rule "Live verification"): this
   changes herdr pane lifecycle, so acceptance is final only after a fresh
   pair start and a persisted restore show `seat_claim=ok owner=<sid>.<pid>`
   in `herdr-agents.log`, a composite lock file, a Stop-hook delivery, and a
   worker `agmsg-dispatch` wake of p1 from sandboxed Bash with no prompt. The
   orchestrator records both legs after the operator's `make update` and
   relaunch; put the checklist in the report.

allowed_files += `home/dot_agents/agent-config.yaml` (sandbox.excludedCommands
only), `home/.chezmoitemplates/claude-settings-managed.json` (generated),
`README.md` (sandbox section), `scripts/validate-agent-assets.py` and
`tests/unit/test_generate_agent_configs.py` / `test_validate_agent_assets.py`
if they pin the field. Keep PR #219; push without `-u`.

## Orchestrator amendment r2-b (2026-10-01 04:5xZ, before the r2 RESULT; PONG msg 580 flag)

Your flag is right: `excludedCommands` takes `agmsg-dispatch` out of the
sandbox but Claude Code still applies its permission rules, and the managed
settings carry no allow rule (`permissions.allow` is empty; the operator has
been answering the worker's unsandboxed `gh`/`git push` prompts by hand).
The operator's decision (wake without a prompt or an escalation) therefore
also needs the allow rule. Add, in the same PR (one more commit, no force
push):

- `home/dot_agents/agent-config.yaml` `claude.permissions.allow:
  [Bash(agmsg-dispatch:*)]` with a one-line comment: the only managed allow
  rule; `agmsg-dispatch` inserts one agmsg row and sends a herdr wake, and is
  the sanctioned worker→orchestrator wake (T49). Regenerate the template
  (`make render-check`); extend the validator/tests that pin the permissions
  block (the manifest currently has `deny` and `ask` only — check
  `validate-agent-assets.py` for a shape check on `allow`).
- README sandbox section and the SKILL/rule sentences: say that
  `Bash(agmsg-dispatch:*)` is allowed by the managed settings, so the dispatch
  runs without a prompt; **user-visible impact**: this is the first managed
  `permissions.allow` entry; every Claude session using the managed settings
  can run `agmsg-dispatch` without confirmation.
- Report: name the impact line explicitly.

allowed_files += `home/dot_agents/agent-config.yaml` (permissions.allow only).

## Orchestrator amendment r2-c (2026-10-01 05:1xZ, before the RESULT; audit of 50ebfdc P2)

Audit of 50ebfdc (`…-audit-50ebfdc.md`): P1 (no allow rule) is fixed by
68ac54d; P2 remains — the same-session bare-lock repair releases one `held`
team and retries once; an identity registered in two teams with bare locks in
both fails on the second team and upstream rolls back the first claim. Fix in
one more commit on the PR: loop while `actas-claim.sh` answers
`status=held team=<T> owner=<our bare sid>`, releasing that team's lock each
time (bounded by the number of teams the identity is registered in, from
`identities.sh`); any other owner → `seat_claim=failed`. One test with a fake
`actas-claim.sh` that answers `held` for team A then team B before `ok`
(`replaced_bare_lock=yes`), and one where the second owner differs
(`failed`). 99d734b (bash `read -t` instead of GNU `timeout`) is noted; keep
the CI green on macOS and Linux before the RESULT.

## Orchestrator amendment r2-d (2026-10-01 05:2xZ, before the RESULT; audit of 99d734b P2)

Audit of 99d734b: on macOS bash 3.2 `read -t` returns without assigning the
variable on timeout, so a hook runtime that writes the payload but keeps
stdin open for 2 s loses the session id (the earlier `timeout 2 cat` kept the
bytes). Audit of 1fa2a48: correct. Disposition for r2-d, one more commit:

- Keep `read -t` (no GNU `timeout` dependency), but state in the comment that
  on timeout bash 3.2 discards the partial payload and the herdr lookup
  (`herdr agent list` → `agent_session.value`) then supplies the sid, so the
  claim still lands; `seat_claim=unresolved` only when that lookup fails too.
- Add one regression test: a producer that writes the JSON payload without a
  trailing newline and keeps the pipe open for ~3 s; assert
  `seat_claim=ok owner=sid-self.777` either way (payload on bash ≥ 4, herdr
  fallback on bash 3.2; the fake `herdr agent list` must answer the same sid).
  This is the open-pipe check the auditor asked for and it runs on both CI
  OSes.

Then the RESULT, once CI is green on macOS and Linux.

## Orchestrator amendment r2-e (2026-10-01 05:3xZ; Codex GitHub comment at `:464`, fold into the r2-d commit if not yet pushed)

Codex: on a persisted-session restore the new claim is `<sid>.<new pid>` while
the lock still holds `<sid>.<old pid>`; the repair releases only a bare `sid`.
Upstream reclaims a composite owner whose pid is positively dead (`free`), so
the common restore case already succeeds; the gap is a `cannot tell` or reused
pid. Generalise the same-session test: treat a held owner as ours when it is
the bare `sid` **or** `sid.<digits>` with the same `sid` (any pid: a process
with our session id can only be our predecessor), release that exact owner
token with `actas_lock_release <team> <identity> <owner>`, and retry as
today. One test: held `owner=sid-stdin.111` → released, re-claimed,
`replaced_bare_lock=yes` (rename the flag to `replaced_stale_lock=yes` if you
prefer; update the docstring/docs accordingly).

## Orchestrator amendment r2-f (2026-10-01 05:4xZ; audit of 63d4e03 P1 — fold into one more commit before the RESULT)

Audit of 63d4e03: parallel `claude --resume`/`--continue` processes share a
session id (agmsg itself warns "parallel --continue/--resume isolation is
degraded"), so releasing a held `<our sid>.<other pid>` can take a **live**
sibling's seat and break its delivery. Correct: a same-sid composite owner is
stale only when its pid is positively dead. Fix: for owner `<sid>.<digits>`,
release only if `kill -0 <digits>` fails with "No such process" (the hook and
the launcher run outside the sandbox, so pids are visible; EPERM or any other
error counts as alive → `seat_claim=failed`). A bare `<sid>` owner stays
ours (it can only come from a sandboxed claim of this session). Tests: owner
`sid-stdin.<dead pid>` (use a pid you spawn and reap, or 2147483647) →
replaced; owner `sid-stdin.$$` (alive) → `failed`, no release. Docstring and
the doctor message: "stale (bare, or same-session composite whose pid is
dead)". Then the RESULT when CI is green.

## Orchestrator amendment r3 (2026-10-01 06:1xZ; dispatched as AGMSG-ACCEPTANCE status=revise)

Final head 9dc4e53 reviewed: every commit audited (4452516, 50ebfdc, 99d734b,
63d4e03 incorrect → each fixed by the following commit; 68ac54d, 1fa2a48,
e4903a1, 9dc4e53 correct); 649 tests; CI green on both OSes. The Codex GitHub
review of 9dc4e53 leaves two valid items (the third, "the allow rule
authorises command chains", is refuted by the permissions docs: "Claude Code
is aware of shell operators, so a rule like `Bash(safe-cmd *)` won't give it
permission to run `safe-cmd && other-cmd` … A rule must match each subcommand
independently" — quote it in the manifest comment so the next reviewer sees
it). Fix both in one commit:

1. **Gate the SessionStart claim to the orchestrator pane** (P2 `:1432`).
   The managed `--attach` hook runs in every Claude pane of a Herdr
   workspace; today any main-checkout Claude session claims the unsuffixed
   orchestrator identity with its own `<sid>.<pid>` and can win a restore
   race. Before claiming in `--self`, require that `$HERDR_PANE_ID` is the
   pair's orchestrator pane: the pane's label is the orchestrator seat label
   (`<team>:<identity>` after self-naming, or `claude-orchestrator` legacy —
   reuse the existing `load_seat_labels`/`rename_pane_unless_seat_named`
   knowledge in this script), or it is the first pane of the managed
   workspace that `herdr-agents` created. Otherwise print
   `seat_claim=skipped reason=not-orchestrator-pane` and claim nothing. One
   test with a worker-labelled pane in the main checkout → skipped, no claim.
2. **Preserve the payload on macOS** (P1 `:1429`). Replace the single
   `read -t 2 -d ''` with a byte-wise accumulation (`while IFS= read -r -t 2
   -n 1 ch; do payload+=$ch; done`, ending on EOF or the first timeout), so
   bash 3.2 loses at most one byte instead of the whole payload; keep the
   herdr lookup as the fallback, and retry that lookup up to 3× with 1 s
   sleeps when the session is not yet listed (herdr may not have it right
   after start). Test: the open-pipe test must now pass with the fake herdr
   lookup returning **nothing** (payload path only) on both OSes.
3. Manifest comment on `permissions.allow`: add the docs quote above and
   "excludedCommands matches the first word only; the allow rule still
   requires every subcommand to match, so a chained command prompts".

Validation as before; CI green on both OSes; then the RESULT. The live legs
(checklist in your report) remain the acceptance condition after merge.

## Orchestrator amendment r3-b (2026-10-01 06:3xZ; audit of 9b658a9 P2 — fold into one more commit before the RESULT)

Audit of 9b658a9: the byte-wise loop resets the 2 s timeout on every byte, so
a producer that trickles input keeps the hook reading past the SessionStart
hook's 10 s budget (measured 5.01 s at 0.6 s per byte) and the claim never
runs. Keep the per-byte read but add an overall deadline: e.g.
`deadline=$((SECONDS + 2)); while (( SECONDS < deadline )) && IFS= read -r -t 1
-n 1 hook_byte; do hook_payload+=${hook_byte}; done` (EOF still ends early;
total wait ≤ ~3 s). One test: a producer that writes one byte every 0.5 s for
6 s → the hook finishes within ~3 s and the claim still lands via the herdr
fallback (payload incomplete). Then the RESULT when CI is green on both OSes.

## Orchestrator amendment r3-c (2026-10-01 07:1xZ; Codex GitHub comment at `:490` — one more commit, then the RESULT)

Final head 229896a reviewed; all ten commits audited (229896a correct). One
valid Codex comment remains: on a restore, a recycled pid makes `ps -p`
succeed, so a stale `<sid>.<old pid>` lock is kept and the new claim ends
`failed`. The "allow rule authorises chains" comment stays refuted (docs
quoted in the manifest). Fix: a same-session composite owner is live only
when `ps -o comm= -p <pid>` is `claude` (a recycled pid that is not a claude
process is stale → release); keep "live claude with our sid = parallel
sibling → failed". Tests: adjust the live-pid test to use a process whose
comm is `claude` (copy a sleeping binary to `$TMPDIR/claude` and run it), and
add a recycled-pid case (the test's own python pid → comm != claude →
replaced, `replaced_stale_lock=yes`). Docstring/doctor wording: "same-session
composite whose pid is dead or not a claude process". Then the RESULT when CI
is green on both OSes.
