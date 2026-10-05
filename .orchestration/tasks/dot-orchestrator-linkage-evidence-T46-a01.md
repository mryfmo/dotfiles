# AGMSG-TASK dot-orchestrator-linkage-evidence-T46-a01

## Objective

Operator correction 2026-09-30: lessons must live in skills, rules, and
checks in this repository, never only in Claude auto-memory. Codify the two
failures of session fc905758 so the tooling and the shared skill prevent them:

- The orchestrator reported "operator action needed (trust dialog)" from an
  inference: `poke.sh` exit 15 ("input box could not be located") plus a
  spawn readiness timeout. The real cause was an unviewed Herdr workspace
  whose pane is 18x41, which defeats poke's TUI input locator. The path that
  had always worked, `agmsg-dispatch … <pane> '<msg>'` (herdr agent prompt
  wake), delivered the PING at once (read_at) and got a PONG.
- `herdr-agents --add-worker` stops at "did not signal ready within 90s"
  without telling the caller whether the worker is reachable at all.

Deliver:

1. `home/dot_local/bin/common/executable_herdr-agents` `--add-worker`: after
   spawn.sh returns (ready or timeout), run a linkage check the orchestrator
   would otherwise improvise: send `AGMSG-PING v1 task_id=bringup
reason=add-worker-linkage` through `agmsg-dispatch <team> <orchestrator>
<worker> <socket>:<pane>` and report one final line
   `linkage=ok read_at=<ts> pong=<yes|no>` or `linkage=unreached rc=<n>
hint=<agmsg-dispatch|poke|attach-a-client>`. Exit non-zero only when the
   PING was not read. Never read the worker pane.
2. `home/dot_agents/skills/agmsg-orchestration/SKILL.md`:
   - Orchestrator Playbook step 6: add the seating case "worker in an
     unviewed/headless Herdr workspace (no client attached, pane rect small)":
     `poke.sh` exits 14/15 from its input locator; use `agmsg-dispatch` and
     verify `read_at`. Exit 14/15 is a locator refusal, not evidence about the
     worker's state.
   - New invariant under "Regime activation and progress": a blocker report
     to the operator requires attached evidence — the exact command, its exit
     code, and the messages.db `read_at`/PONG query — after trying the wake
     path that worked in earlier sessions. Inferences (for example "trust
     dialog") are not reportable blockers.
   - Regime boundary bullet: lessons are codified in this repository (rule,
     skill, or check) through a task; Claude auto-memory is not a durable
     store for regime procedure.
3. `home/dot_config/claude/rules/agmsg-orchestration.md`: two bullets mirroring
   the invariant (evidence before blocker reports; codify lessons in repo, not
   auto-memory) and one on `agmsg-dispatch` for headless workspaces.
4. `home/dot_local/bin/common/executable_agmsg-dispatch` `@description`: state
   that it is also the wake path for headless/unviewed Herdr workspaces where
   `poke.sh` cannot locate the input box.
5. Tests: `tests/unit/test_herdr_agents.py` — add-worker emits the `linkage=`
   line on both spawn outcomes using a fake `agmsg-dispatch` (one test each
   for ok and unreached). Keep the existing fakes; never touch a live pane.
6. `make unit-test`, `make validate-agent-assets` green. PR (English) from
   `fix/orchestrator-linkage-evidence`.

7. Session start/stop checklists, codified in `SKILL.md` ("Regime activation
   and progress" + the boundary bullet) and mirrored in
   `home/dot_config/claude/rules/agmsg-orchestration.md`:
   - **Start** (operator or orchestrator, repo cwd, plain shell or Herdr):
     `herdr-agents <DIR>` full mode is the only way to create the pair;
     inside a Herdr pane the SessionStart `--attach` heals it. A Claude that
     finds itself outside Herdr does not improvise a pane-less regime: it
     reports the one-line state (T45) and the operator relaunches the pair.
     `--add-worker` is for additional worktrees only, never a substitute for
     the pair's own worker seat.
   - **Stop** (every regime/session boundary, in this order): pending
     acceptance records written; `make validate-agent-assets` (real exit);
     `.orchestration` boundary commit with zero untracked tail; every
     additional worker removed with `herdr-agents --remove-worker <worktree>`
     (which despawns, turns delivery off, leaves, closes the workspace);
     stale identities checked with `identities.sh <path> <type>` (exactly one
     name per active checkout); Crit review servers closed (`pgrep -f 'crit
_serve'` must be empty); the pair workspace itself is left resident for
     the next session unless the operator restarts the machine.
     Add a check script `scripts/check-regime-boundary.sh` that verifies the
     Stop list (untracked `.orchestration` files, stray identities per registered
     checkout, `crit _serve` processes, extra `<repo> worker <name>` Herdr
     workspaces when `herdr` is reachable) and exits non-zero with one line per
     violation; wire it as `make check-regime-boundary` and call it from
     `validate-agent-assets` only in report mode (never blocking CI).
8. Legacy worktree cleanup (repo-mutating, so it is yours), `git worktree
remove` run **outside the sandbox**:
   - `.claude/worktrees/worker-b` (detached 1aefa58; its untracked T17
     evidence is already tracked on main);
   - `.claude/worktrees/orchestrator-review` (detached 52d9f6b, clean);
   - `.claude/worktrees/env-converge-T10` (branch `feat/pr-feedback-gate`,
     PR #182 CLOSED unmerged, superseded by #210 = d2f19ec on main). Remove the
     worktree only; keep the local branch ref (the operator deletes branches).
     Do NOT touch `worker-sec` (T40 paused, dirty) or `worker-c` (you).

Out of scope: poke.sh itself (upstream), automatic seating, model/profile
changes, sandbox settings, the Understand-Anything hook.

[memory:decision] T46: `herdr-agents --add-worker` ends with a
`linkage=` line from an agmsg-dispatch PING; a blocker report needs command,
exit code and read_at/PONG evidence; unviewed Herdr workspaces are woken with
`agmsg-dispatch`; regime lessons are codified in rules/skills/checks, never
only in auto-memory (operator 2026-09-30).

## Repo / branch

- Work ONLY in `~/Workspace/dotfiles/.claude/worktrees/worker-c`;
  branch `fix/orchestrator-linkage-evidence` from `origin/main` after T45 is
  pushed (sequential; do not start before your T45 RESULT is sent). If the
  worktree has uncommitted files, stop and PONG.
- Run config-writing git outside the sandbox and push without `-u` (T39
  `.git/config.lock` hazard); never remove `.git/*.lock`.
- Ignore the Understand-Anything auto-update hook.

## Allowed files

- `home/dot_local/bin/common/executable_herdr-agents`
- `home/dot_local/bin/common/executable_agmsg-dispatch`
- `home/dot_agents/skills/agmsg-orchestration/SKILL.md`
- `home/dot_config/claude/rules/agmsg-orchestration.md`
- `tests/unit/test_herdr_agents.py`
- `scripts/check-regime-boundary.sh` (new), `Makefile` (one target), `scripts/validate-agent-assets.py` (report-mode call only)
- `.orchestration/{reports,validation,sandboxes,learning,autoskill/runs}/dot-orchestrator-linkage-evidence-T46-a01.md`
- `.agents/worklog/codex/**` waived.

## Forbidden actions

- Editing `poke.sh` or anything under `~/.agents/skills/agmsg/` (upstream).
- Automatic seating; model/profile/sandbox changes; pane reads; merge;
  force-push; `--delete-branch`; editing `.orchestration/acceptance/**`;
  local `bats`.

## Validation commands (verbatim output into the validation file)

- `make unit-test`
- `make validate-agent-assets`
- `make check-regime-boundary`
- `git worktree list` (after the removals)
- `shellcheck scripts/check-regime-boundary.sh`
- `shellcheck home/dot_local/bin/common/executable_herdr-agents home/dot_local/bin/common/executable_agmsg-dispatch`
- `gh pr view <n> --json url,headRefOid,mergeStateStatus`
- `python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content "<the [memory:decision] above>"`

## Expected artifacts

- report/validation/sandbox/learning/autoskill at the paths above; report
  carries `cost:`, PR URL, head sha, the CompactionDB command.

max_turns=40. done_signal=AGMSG-RESULT v1.

## Orchestrator amendment before dispatch (2026-10-01; main is 119fdc3 after T47/T49/T45 merged)

- Base: branch `fix/orchestrator-linkage-evidence` from `origin/main` (119fdc3);
  `executable_herdr-agents` now carries T47 (profile args for p1), T49
  (`claim_orchestrator_seat`, `seat_claim=` lines, `--attach` payload read)
  and T45 (plain-start summary, `--add-worker` socket derivation, trust-dialog
  watcher, `--ready-timeout`, spawn exit-code reporting). Build the linkage
  check on that code; do not undo any of it.
- Deliverable 1: the real wake form is `agmsg-dispatch <team> <from> <to>
<pane_id> "<message>"` (pane id like `wP:p2`, not `<socket>:<pane>`); the
  final line stays `linkage=ok read_at=<ts> pong=<yes|no>` or
  `linkage=unreached rc=<n> hint=<agmsg-dispatch|poke|attach-a-client>`.
- Deliverable 8 (worktree cleanup): remove **only** `.claude/worktrees/worker-b`
  and `.claude/worktrees/env-converge-T10`. **Keep
  `.claude/worktrees/orchestrator-review`**: it is the orchestrator's live
  review worktree (the integration gate runs there at each PR head).
- Deliverable 2/3 wording must agree with the T49 bullets already in the SKILL
  and rule (composite seat lock, `agmsg-dispatch` excluded from the sandbox
  with the managed allow rule); add, do not duplicate or contradict.
- Deliverable 7's `scripts/check-regime-boundary.sh` also WARNs on a bare-id
  orchestrator lock by calling the T49 doctor check (import or reuse
  `orchestrator_seat_lock_warnings` from `scripts/check-agent-runtime.py`);
  one check, not two implementations.

## Orchestrator answer to the worker's question (2026-10-01 12:2xZ, PONG msg 611)

The merged T45 SKILL bullet (pane-less orchestrator brings the regime up on
demand) supersedes the stricter wording drafted in deliverable 7's Start
checklist. Reconcile, do not contradict: the **pair via `herdr-agents` full
mode is the normal form** and the operator creates/relaunches it; a Claude
that finds itself outside Herdr is a **pane-less orchestrator (T45)**: its
SessionStart hook prints the one-line state, and it may bring the regime up
on demand exactly as the T45 bullet says (composite seat claim outside the
sandbox, `--add-worker` for the manifest worktree, PING/PONG before any task,
headless auditor). `--add-worker` therefore serves both additional worktrees
and the pane-less on-demand worker; what remains forbidden is improvising
anything the two bullets do not describe. Write the Start checklist in those
terms and cross-reference the T45 bullet.

## Orchestrator answer on deliverable 8 (2026-10-01 12:3xZ, PONG msg 613)

`.claude/worktrees/env-converge-T10` holds uncommitted tracked changes to
`scripts/pr-feedback.py` (+59/−3: `--require-codex-review`, Codex review
summary parsing) that are not on main (verified: main's `pr-feedback.py` has
no Codex-review parsing). Preserve, then remove: commit them on the worktree's
own branch `feat/pr-feedback-gate` (PR #182 is closed; the branch is the
record) with an English message naming the origin (T10 WIP, not reviewed),
push without `-u`, then `git worktree remove` the worktree outside the sandbox.
Do not open a PR; the operator decides the branch's fate. Report the commit
sha. `orchestrator-review` stays, as amended.

## Orchestrator answer on the rejected push (2026-10-01 12:3xZ, PONG msg 615)

No force-push (forbidden). Push the local WIP commit 0c12c6a to a **new**
branch `wip/pr-feedback-codex-review-T10` (`git push origin
0c12c6a:refs/heads/wip/pr-feedback-codex-review-T10`, no `-u`), leave
`feat/pr-feedback-gate` as it is on origin, then remove the worktree outside
the sandbox. Report both the sha and the branch name; the operator decides
the branch's fate.

## Orchestrator amendment r2 (2026-10-01 12:4xZ; audit of 7d0c585 — fold into one more commit before the RESULT)

Audit of 7d0c585 (`…-audit-7d0c585.md`), three P2s, all confirmed by the
orchestrator reading the diff:

1. `check_worker_linkage` resolves the pane with `team.sh --json`, which in
   agmsg 1.5.0 observes Codex members through `terminal_peek → herdr pane
read` — a worker-pane read the regime forbids. Resolve the pane from the
   spawn placement record instead: `~/.agents/skills/agmsg/run/spawn.<team>__<worker>`
   holds `herdr:<socket>:<pane>\t<project>\t<type>` (take the `<ws>:<pN>` tail of
   field 1); fall back to the workspace's new pane as today. No `team.sh` call
   in the linkage check. (The merged T45 summary also calls `team.sh --json`
   for the seated worker's placement — out of scope here, note it in the
   learning file as a follow-up candidate.)
2. The PONG query matches any historical `AGMSG-PONG v1 task_id=bringup` row.
   Correlate to this PING: read `max(id)` of our PING row right after the
   dispatch and count only PONGs with `id > <that id>` (and `read_at` from
   that same row).
3. `check-regime-boundary.sh` derives the workspace label prefix from the
   script's checkout basename, so from a worktree it filters for
   `worker-c worker ` while labels are `dotfiles worker …`. Use the main
   checkout's basename: `git rev-parse --path-format=absolute --git-common-dir`,
   strip `/.git`, `basename`.

Tests: one per item (placement-record pane resolution with no `team.sh` call
in the fake log; an old PONG before the PING → `pong=no`; the boundary script
run from a fake worktree still finds `dotfiles worker x`). Then the RESULT
when CI is green on both OSes.

## Orchestrator amendment r3 (2026-10-01 13:3xZ; dispatched as AGMSG-ACCEPTANCE status=revise)

r2 (b91f949) reviewed: placement record instead of `team.sh`, PONG correlated
by `id > ping_id`, label prefix from the main checkout — all as asked; bec48d4
(shfmt) correct. Audit of b91f949 leaves one P2: the placement record path is
hard-coded as `run/spawn.<team>__<worker>`, but agmsg 1.5.0 also writes
id-keyed records (`spawn.<team_id>__<member_id>`), resolved by upstream
`agmsg_spawn_path` in `lib/actas-lock.sh:369`. Fix in one commit: resolve the
record through `agmsg_spawn_path` (source `lib/actas-lock.sh` with
`SKILL_DIR` exported, in a subshell as `claim_orchestrator_seat` already does
for `actas_lock_release`), keep the workspace-new-pane fallback, and add one
test with an id-keyed record (`hint=poke` on a dispatch failure). Then the
RESULT when CI is green on both OSes.

## Orchestrator amendment r3-b (2026-10-01 13:5xZ; audit of 91cc85f P2 — fold into one more commit before the RESULT)

The `|| record=<legacy path>` fallback also runs when upstream
`agmsg_spawn_path` **refuses** (both an id-keyed and a legacy record exist:
"refusing to resolve a single path; remove the stale one"), so a stale legacy
pane can be dispatched to. Fix: fall back to the legacy path only when the
library or the function is unavailable (`lib/actas-lock.sh` unreadable, or
`declare -F agmsg_spawn_path` fails in that bash); when the resolver runs and
fails, print `linkage=unreached rc=<its rc> hint=placement-conflict` with the
resolver's stderr line, dispatch nothing, and return that rc. Tests: both
records present → `unreached … hint=placement-conflict`, no `agmsg-dispatch`
call; library missing → legacy path still used. Then the RESULT when CI is
green on both OSes.

## Orchestrator amendment r4 (2026-10-01 14:3xZ; dispatched as AGMSG-ACCEPTANCE status=revise)

Head 63c993b reviewed; audits: 7d0c585, b91f949, 91cc85f incorrect (each
fixed by the next commit), bec48d4, 63c993b correct; 669 tests; CI green on
both OSes. Codex GitHub review of 63c993b leaves two valid comments (the
"resident pair matched" one is wrong — the prefix is already `<repo> worker `;
the PONG-correlation one is fixed by b91f949). Fix both in one commit:

1. `:889` — `HERDR_AGENTS_LINKAGE_PONG_WAIT` is used in arithmetic unvalidated;
   a non-numeric value aborts the `set -u` shell after the PING was read, so
   the required `linkage=` line never prints. Validate it (`^[0-9]+$`, else
   fall back to 30 and warn once on stderr) before computing the deadline.
   Test: `HERDR_AGENTS_LINKAGE_PONG_WAIT=foo` → `linkage=ok … pong=no` still
   printed, exit 0.
2. `:1820` — the orchestrator identity for the PING is `head -n 1` of the
   team's non-`-aNNN` claude-code identities; with two leaders the PING could
   be routed through the wrong one while `pong=yes` is reported. Require
   exactly one leader (the same rule `claim_orchestrator_seat` applies);
   otherwise print `linkage=unreached rc=2 hint=agmsg-dispatch` with a stderr
   line naming the ambiguity and dispatch nothing. Test: two leaders → that
   line, no dispatch.

Then the RESULT when CI is green on both OSes.

## Orchestrator amendment r4-b (2026-10-01 14:5xZ; audit of 00573f3 P2 — fold into one more commit before the RESULT)

`^[0-9]+$` accepts `08`, which bash arithmetic reads as octal ("value too
great for base"), and `010` as eight. Normalise to decimal:
`deadline=$((SECONDS + 10#${wait_seconds}))`. One regression test with
`HERDR_AGENTS_LINKAGE_PONG_WAIT=08` → the `linkage=` line still prints and the
wait is eight seconds (set the PONG early so the test stays fast). Then the
RESULT when CI is green on both OSes.

## Orchestrator amendment r5 (2026-10-02; dispatched as AGMSG-ACCEPTANCE status=revise)

Head b29ef04 reviewed; all seven commits audited (b29ef04 correct). The Codex
GitHub review of b29ef04 leaves four valid P2s; fix all in one commit:

1. `:897` — a delayed PONG from an earlier worker instance written after the
   new PING still counts. Make the PING unique per invocation: `task_id=bringup-<nonce>`
   (e.g. `$(date +%s)-$$`) and match the PONG body on that exact `task_id`
   (workers echo the PING's task_id), in addition to `id > ping_id`. Update
   the docstring/SKILL/rule text that names `task_id=bringup`.
2. `:857` — a retained placement record may name a pane in an older
   workspace. Accept the record only when its `<ws>` part equals the new
   `workspace_id`; otherwise fall back to the new-pane lookup (and say so on
   stderr).
3. `:37` — `check-regime-boundary.sh` scans untracked `.orchestration` files
   only in its own checkout. Run that probe for every path from
   `git worktree list --porcelain`.
4. `:45` — zero identity names are not flagged. Flag `0` names for the active
   seats: the main checkout (type claude-code) and the manifest
   `worker_worktree` (either type, at least one); other worktrees (for example
   `orchestrator-review`) are not seats and stay exempt.

Tests: one per item (delayed-old-PONG with a different task_id → `pong=no`;
record in another workspace → new-pane dispatch; untracked file in a second
worktree → reported; zero identities at the main checkout → reported, at an
unrelated worktree → not). Then the RESULT when CI is green on both OSes.

## Orchestrator amendment r6 (2026-10-02; dispatched as AGMSG-ACCEPTANCE status=revise)

Head 9e36e63 reviewed; all eight commits audited (9e36e63 correct). One valid
Codex comment remains (`check-regime-boundary.sh:88`): the leftover-worker
check matches workspaces by the `<basename> worker ` label alone, so a
second clone with the same basename makes this repository's boundary check
fail. Fix in one commit: for each label-matched workspace, require that at
least one of its panes has a `cwd` under the main checkout path (`herdr pane
list --workspace <ws>` → `.result.panes[].cwd`, prefix `<main>/`), the same
disambiguation `find_managed_workspaces` in `executable_herdr-agents` uses;
skip workspaces whose panes are elsewhere. One test: a fake `herdr workspace
list` with two `dotfiles worker x` workspaces, one whose pane cwd is under the
checkout (reported) and one under `/elsewhere/dotfiles` (not reported). Then
the RESULT when CI is green on both OSes.

## Orchestrator amendment r7 (2026-10-02; dispatched as AGMSG-ACCEPTANCE status=revise)

Head 2721f0c reviewed; all nine commits audited (2721f0c correct). The Codex
GitHub review of 2721f0c leaves three valid P2s; fix all in one commit:

1. `check-regime-boundary.sh:75` — the active-seat check counts per runtime
   type, so one claude-code plus one codex identity at the main checkout or
   the manifest worker worktree passes. For the two active seats, count the
   distinct names across both types and require exactly one (0 → "no
   identity", >1 → "stray identities"); keep the per-type ">1" check for the
   other worktrees.
2. `executable_herdr-agents:864` — a retained placement record for an exited
   pane in the _same_ workspace is still preferred, and `agmsg-dispatch` then
   fails on a pane that no longer exists. Before using the record, require
   that its pane id is present in `herdr pane list --workspace <ws>`;
   otherwise fall back to the new-pane lookup (stderr line as for the
   other-workspace case).
3. `check-regime-boundary.sh:111` — `orchestrator_seat_lock_warnings` is
   called with `root`; from a linked worktree that is the worker checkout and
   the main checkout's bare lock is missed. Pass `main` (keep `root` only to
   locate the module).

Tests: one per item (claude-code + codex at the manifest worktree → reported;
record naming a pane absent from the workspace → new-pane dispatch; script run
from a worktree with a fake module that records the path it was given →
`main`). Then the RESULT when CI is green on both OSes.

## Orchestrator amendment r8 (2026-10-02; dispatched as AGMSG-ACCEPTANCE status=revise)

Head d806a3d reviewed; all ten commits audited (d806a3d correct); CI green.
The Codex GitHub review of d806a3d leaves three valid P2s, and the r7 report
discloses two residuals. Fix all five in one commit on d806a3d:

1. `executable_herdr-agents` `check_worker_linkage` (record validation,
   ~:856-871): a placement pane that is present in the workspace but was
   already listed before this spawn (member of the `known` JSON array) cannot
   be the pane this invocation created; a retained record from an earlier
   spawn can name such a pane while the fresh worker sits in the new pane.
   Treat it as stale: stderr line in the same form as the other two cases
   (`… names pane %s, which existed before this spawn; using the new pane.`),
   then the new-pane lookup.
2. `executable_herdr-agents` `check_worker_linkage` (dispatch, ~:887-893):
   when `agmsg-dispatch` fails, the caller currently gets only
   `linkage=unreached rc=<n> hint=<…>`, so the blocker evidence the SKILL
   requires (exact command, exit code, `read_at`/PONG query) cannot be
   reconstructed. Before the final line, print to stderr the exact invocation
   (`agmsg-dispatch <team> <orchestrator> <worker> <pane> 'AGMSG-PING v1
task_id=<task_id> reason=add-worker-linkage'`) and the `read_at`/PONG
   query against the resolved db path (or one line saying the db path could
   not be resolved). Stop swallowing agmsg-dispatch's own stderr (keep stdout
   silenced). The stdout `linkage=` line is unchanged.
3. `SKILL.md` pane-less bullet (line 22): it still says "send `AGMSG-PING`
   through `poke.sh <team> <worker> --body-file <path>`", which contradicts
   the headless-workspace bullet (poke 14/15 is a locator refusal) and the
   `--add-worker` linkage line this task added. Rewrite that clause: the
   `linkage=` line printed by `--add-worker` is the PING evidence; on
   `pong=no` or `linkage=unreached`, wake again with `agmsg-dispatch <team>
<orchestrator> <worker> <pane>` and verify `read_at`; `poke.sh` only for a
   viewed workspace. Keep "dispatch no AGMSG-TASK before its PONG arrives".
4. `scripts/check-regime-boundary.sh` shdoc `@description` (lines 7-12):
   describe the r7 rules — exactly one identity name across claude-code and
   codex at each active seat (main checkout and manifest `worker_worktree`,
   an empty seat reported), more than one name per type elsewhere.
5. `SKILL.md` teardown bullet (line 35) `identities.sh` verification: state
   that "one distinct name per type is healthy" is the rule for non-seat
   worktrees, and that an active seat holds exactly one name across both
   types (what `make check-regime-boundary` enforces). Check the rule file
   for the same wording (none found at d806a3d; confirm).

Tests: one each for items 1 and 2 (record pane in `known` and present in the
workspace → stderr line, PING dispatched to the new pane; failed dispatch →
stderr contains the invocation and the query, stdout line unchanged) with the
negative check against d806a3d. `make render-check`, `make unit-test`,
`make validate-agent-assets`, shfmt, shellcheck as before. Push without `-u`,
no force-push. Then the RESULT when CI is green on both OSes.

## Orchestrator amendment r9 (2026-10-02; dispatched as AGMSG-ACCEPTANCE status=revise)

Head 98ea49f reviewed: the five r8 items are in place (diff verified), 681
tests OK, CI green. The Codex audit of 98ea49f is **incorrect** with one P2,
and your r8 observation is accepted as a second item. Fix both in one
commit on 98ea49f; both are in `SKILL.md` line 22 (pane-less bullet):

1. Audit P2: the recovery command `agmsg-dispatch <team> <orchestrator>
<worker> <pane>` has only four arguments; `agmsg-dispatch` requires the
   message as the fifth and exits 1 with usage (reproduced by the auditor).
   Write it as `agmsg-dispatch <team> <orchestrator> <worker> <pane>
'AGMSG-PING v1 task_id=<id> reason=<reason>'`.
2. The clause "confirm that `team.sh <team> --json` shows the worker's
   `run/spawn.*` placement in its `terminal`/`pane` fields" tells the
   orchestrator to use the call `check_worker_linkage` dropped because
   `team.sh --json` observes Codex members by reading their pane. Replace it
   with the placement record itself (the `herdr:<socket>:<pane>` row that
   `agmsg_spawn_path` resolves) and the `--add-worker` `linkage=` line.

No test pins either sentence (confirm with grep and say so). `make
render-check`, `make validate-agent-assets` as before; push without `-u`;
RESULT when CI is green on both OSes. If a Codex GitHub review of 98ea49f
posts before you push, leave its items to the orchestrator's sweep.
