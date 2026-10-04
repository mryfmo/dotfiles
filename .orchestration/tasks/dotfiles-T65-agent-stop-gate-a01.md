# AGMSG-TASK dotfiles-T65-agent-stop-gate-a01

Drafted 2026-10-04 by the orchestrator seat from the approved correction plan (Phase 1, dotfiles-T65). Runs in parallel with T62/T64; allowed files are disjoint. Worker: the identity named in the dispatch, in its own worktree.

## Objective

Principle 2: completion after plan approval is guaranteed by a Stop hook gate, not by prompts. Add a project-level Stop hook that blocks an agent seat from idling with work pending. Project level because `.claude/settings.json` (tracked) already carries a Stop hook (contextdb, ~line 125) and is shared by the main checkout and the `.claude/worktrees/*` worker seats; no merge-script change.

1. New `scripts/agent-stop-gate.sh` (bash, shdoc comments, ≤150 lines). Behaviour, in order:
   1. Read the hook JSON on stdin. If `stop_hook_active` is true, skip the dirty-tree check (nag once) but still run the pending-message checks. Reuse the stdin/JSON handling pattern of `~/.agents/skills/agmsg/scripts/check-inbox.sh:75-77` (read it; do not copy agmsg internals you do not need).
   2. Resolve the main checkout as `scripts/check-regime-boundary.sh:28-33` does (`git rev-parse --git-common-dir`); determine whether cwd's toplevel is the main checkout (orchestrator seat) or a worktree under `.claude/worktrees/` (worker seat). Anything else → exit 0.
   3. Orchestrator seat: (a) `git status --porcelain --untracked-files=all` entries outside `.orchestration/` and `.agents/worklog/` → block (unless `stop_hook_active`); (b) identity = `AGMSG_RESOLVE_PROJECT=0 ~/.agents/skills/agmsg/scripts/identities.sh <main> claude-code` row without `-aNNN` suffix (team, name); from the agmsg store (`~/.agents/skills/agmsg/scripts/history.sh <team>` or a read-only sqlite query on `~/.agents/skills/agmsg/db/messages.db`, whichever is documented in that skill's README; name the source), compute task_ids of `AGMSG-RESULT v1 task_id=X` addressed to the identity minus task_ids of `AGMSG-ACCEPTANCE v1 task_id=X` sent by it (also minus `AGMSG-TASK v1 task_id=X revision=…` re-dispatches after that RESULT, which mean a revise round is in flight); non-empty → block regardless of `stop_hook_active`.
   4. Worker seat: identity = the `-aNNN` claude-code identity registered at this worktree; if the latest `AGMSG-TASK` addressed to it is newer than the latest `AGMSG-RESULT`/`AGMSG-PONG` it sent → block.
   5. Block = `exit 2` with one reason line per violation on stderr (what is pending and the command that clears it); otherwise exit 0 silently. Budget < 2 s, no network, never writes. Add a `ponytail:` comment naming the ceiling (an unreachable store would block every turn; upgrade path: a timestamp cap).
2. `.claude/settings.json`: add the hook to the existing `Stop` array with the same `${CLAUDE_PROJECT_DIR}/…` shape as the contextdb entries, timeout 5.
3. New `tests/unit/test_agent_stop_gate.py`: fixture git repo with a nested `.claude/worktrees/x` worktree, a fake `identities.sh` and a fake message source (a small sqlite DB or fake `history.sh`, matching what the script reads); cases: clean orchestrator → 0; untracked file outside `.orchestration` → 2 with path; pending RESULT without ACCEPTANCE → 2; RESULT followed by revision TASK → 0; worker with TASK newer than its RESULT → 2; worker after RESULT → 0; `stop_hook_active` skips only the dirty-tree check.

VERIFY (record with sources): the Stop hook stdin fields (`stop_hook_active`, `cwd`, `session_id`), the meaning of exit 2 (blocks the stop, stderr shown to Claude), and whether adding a project hook needs a one-time trust confirmation in Claude Code 2.1.x.

[memory:decision] dotfiles-T65 (operator 2026-10-03): a project-level Stop hook `scripts/agent-stop-gate.sh` blocks the orchestrator seat from stopping with repository changes outside .orchestration or with a RESULT lacking an ACCEPTANCE, and blocks a worker seat from stopping with a TASK lacking a RESULT/PONG; exit 2 with reasons, no prompt.

## Repo / branch

- Work ONLY in your own worktree. `git fetch origin`; `git switch -c feat/agent-stop-gate origin/main`. Verify the dispatched task_rev; else stop and PONG blocked.
- Strict status checks: if `main` moves, `gh pr update-branch <pr>` and wait for CI again before RESULT.

## Allowed files

- `scripts/agent-stop-gate.sh` (new), `tests/unit/test_agent_stop_gate.py` (new)
- `.claude/settings.json` (one Stop entry)
- `.orchestration/{reports,validation,sandboxes,learning,autoskill/runs}/dotfiles-T65-agent-stop-gate-a01.md` (main checkout)

## Forbidden actions

- `home/**` (the merge script, manifest, templates), `scripts/check-regime-boundary.sh`, agmsg skill files under `~/.agents`, `.claude/settings.local.json`; running the hook against the live store in a way that writes; `make update`/`make apply`; local bats; merging; force push; pushing `main`.

## Validation commands (paste verbatim output)

```
git diff origin/main --stat
bash -n scripts/agent-stop-gate.sh; shellcheck scripts/agent-stop-gate.sh; mise x shfmt -- shfmt -i 4 -sr -d scripts/agent-stop-gate.sh
uv run python -m unittest tests.unit.test_agent_stop_gate 2>&1 | tail -3
make unit-test
make validate-agent-assets
python3 -c 'import json;json.load(open(".claude/settings.json"))' && jq '.hooks.Stop' .claude/settings.json
echo '{"stop_hook_active":false,"cwd":"'"$PWD"'"}' | scripts/agent-stop-gate.sh; echo "exit=$?"   # in your worktree: exercises the worker branch read-only
gh pr checks <pr-number>
gh api repos/mryfmo/dotfiles/pulls/<pr-number> --jq '.mergeable_state'
```

## Completion

1. PR to `main`, English title/description ending with `🤖 Generated with [Claude Code](https://claude.com/claude-code)`. CI green on the final head, branch up to date.
2. After the final push: `gh pr checks <pr> --watch`; wait (≤15 min) for the Codex Bot review; fix P0/P1 inline findings and repeat; do not resolve threads.
3. Artifacts at the exact expected paths; validation with verbatim outputs, PR number, head SHA, VERIFY results with sources.
4. CompactionDB `memory add --kind decision --scope project` with the `[memory:decision]` text from the main checkout; paste command and output.
5. `AGMSG-RESULT v1` via `agmsg-dispatch dotfiles <your identity> claude-remediation-dot wT:p1 "<single line>"` (outside the sandbox). `cost:` line. max_turns=35.

## Revise round 1 (2026-10-03T23:37Z RESULT on 13340185): the two open Codex findings are fixed, not deferred

1. **P2 fail closed when the identity lookup cannot run.** Distinguish "agmsg not installed" from "lookup failed": if `${scripts}/identities.sh` does not exist → exit 0 (not a regime machine). If it exists and exits non-zero → add a reason (`agmsg identity lookup failed for <top>; check identities.sh`) and block unless `stop_hook_active` is true (same treatment as an unreadable store). Capture the status explicitly (run it into a variable first, not through the process substitution).
2. **P3 JSON-escaped `cwd`.** Parse the hook input with `jq -r '.cwd // empty'` (jq is already a dependency of the script) instead of `sed`; keep the `${PWD}` fallback. Same for `stop_hook_active` (`jq -r '.stop_hook_active // false'`).
3. Tests: one case per fix (lookup script present but failing → exit 2 with the reason; a cwd containing a quote or backslash resolves correctly).

One commit; push; wait for the Codex review of the new head; new RESULT; do not resolve threads. The pre-merge blockers you reported (operator's `references/`, legacy T13/T31 RESULTs) are the orchestrator's; they are being closed in parallel.

## Revise round 2 (2026-10-04T00:01Z RESULT on 1ee605c6): staged rename rows

Codex P2 4175454186 is a real hole in a mechanical control (a staged `R  .orchestration/x -> src/y` row is exempted by its old name), and "the orchestrator never stages renames" is policy, not a control. Fix it: read `git status --porcelain -z`, and for a rename/copy row exempt it only when **both** endpoints are under the exempt prefixes; otherwise report the destination path. One test with a staged rename out of `.orchestration/`. One commit; push; wait for the Codex review of the new head; new RESULT; do not resolve threads.

## Revise round 3 (2026-10-04T01:17Z RESULT on 2da17946): last two Codex findings and the withdrawn-task state

1. **4175647971 (`GIT_DIR`/`GIT_WORK_TREE`):** fix at the root, one line: `unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE` is **not** wanted for `GIT_INDEX_FILE` (the test uses it); unset only `GIT_DIR` and `GIT_WORK_TREE` before the `rev-parse` probes. One test with an invalid `GIT_DIR` in the environment → the seat is still classified from `cwd`.
2. **4175647967 (missing store for a registered team):** `not-applicable`, with the reason the worker gave (agmsg's `history.sh` treats a missing store as the ordinary state of a freshly joined team; a deleted store is indistinguishable and recovering lost messages is not this gate's job). Do not change the code; the orchestrator replies on the thread.
3. **Withdrawn tasks (pre-merge item):** the orchestrator withdraws a task by sending the worker an `AGMSG-ACCEPTANCE` whose status is not `revise` (`withdrawn`, `accepted`, `closed-historical`). On the worker seat, such an ACCEPTANCE addressed to the worker closes that task_id (one awk branch); `status=revise` keeps reopening it. One test (TASK → ACCEPTANCE withdrawn → exit 0; TASK → ACCEPTANCE revise → exit 2). The orchestrator will then send `AGMSG-ACCEPTANCE v1 task_id=<id> status=withdrawn` for `dot-ua-incremental-T20-a01` and `dot-orchestrator-guardrails-T21-a01` to a005.

One commit; push; wait for the Codex review of the new head; new RESULT; do not resolve threads. If the Bot raises further P2/P3 that are variants of classes already handled, list them with a proposed `not-applicable` and stop.

## Revise round 3 addendum (audit of a62fce9d: incorrect, three findings)

Fold these into the round-3 commit (or a second commit in the same push if round 3 is already pushed):

- **P2 budget (gate.sh:97):** `AGMSG_BUSY_TIMEOUT=1000` is per sqlite call, so several contended memberships can exceed the 5 s hook timeout before any reason is printed (a timed-out hook's output is discarded, so it fails open). Bound the whole message phase: run the identity loop's reads under one overall budget (`timeout 3` around `read_history`, or a deadline check between teams); when the budget is hit, append one reason (`agmsg history read exceeded the hook budget; retry`) and exit 2 immediately. Test: a fake storage that sleeps makes the gate block with that reason within the budget.
- **P3 test (test_agent_stop_gate.py:32):** the fake storage rejects stale revisions itself, so removing the production preflight would still pass. Make the fake record whether `storage_history` was called and assert it was **not** called when the revision mismatches.
- **P2 preflight race (gate.sh:102):** `storage_history` → `storage_init` can still write if its own schema read fails under `SQLITE_BUSY`. Upstream agmsg exposes no read-only history API, and the skill forbids reading the database directly, so this is `not-applicable` to this task: record it in the report as an upstream limitation mitigated by the preflight read and the busy timeout, and name the upstream API that would close it (a non-initializing `storage_history`). The orchestrator will answer the audit finding with that disposition.

## Revise round 4 (orchestrator, 2026-10-04 03:08Z) — six open Codex threads, one reporting error

The round-3 RESULT said "codex=clean-on-9f27743b, no-response-on-cb3ded43". That is wrong: the Codex Bot reviewed every pushed head, including cb3ded43 at 02:21:40Z (thread 4175816307) and the merge head cd612f62 at 02:46:49Z (threads 4175883202 P1 and 4175883204). Six unresolved threads have no disposition in the report: 4175687782, 4175723390, 4175723393, 4175816307, 4175883202, 4175883204. Fix the four that are still open in the head in one commit on `feat/agent-stop-gate`; the orchestrator dispositions the rest.

1. **Peer correlation (4175883202, P1).** `pending[id]` must remember the counterparty: on the worker seat the sender of the `AGMSG-TASK`/revise `ACCEPTANCE`; on the orchestrator seat the sender of the `AGMSG-RESULT`. Clear the entry only when the closing message's other endpoint is that peer (worker: my RESULT/`PONG status=blocked` addressed to the peer, or an ACCEPTANCE from the peer to me; orchestrator: my ACCEPTANCE/TASK addressed to the peer). Test: a RESULT the worker sends to another member leaves the task pending; the same RESULT to the dispatching orchestrator clears it.
2. **All Git repository overrides (4175723393, 4175816307).** `unset GIT_DIR GIT_WORK_TREE GIT_COMMON_DIR GIT_INDEX_FILE GIT_OBJECT_DIRECTORY GIT_ALTERNATE_OBJECT_DIRECTORIES` before the probes. The round-3 instruction to keep `GIT_INDEX_FILE` was the orchestrator's mistake: a test that builds fixtures with it is unaffected by the script unsetting it in its own process. Test: an inherited alternate index that matches HEAD while the real index holds a staged source change → the orchestrator seat blocks.
3. **Main worktree without a `.git` suffix assumption (4175883204).** Derive it from `git -C "${cwd}" worktree list --porcelain | sed -n '1s/^worktree //p'` (the first entry is the main worktree) instead of `${common%/.git}`. `scripts/check-regime-boundary.sh` keeps its own resolution (outside this task); note the parity gap in the report for a follow-up.
4. **Portable timeout runner (4175723390, completing cb3ded43).** `runner="$(command -v timeout || command -v gtimeout || true)"` and use it for both the stdin read and the history read; the uncapped fallback stays only when neither exists. Homebrew coreutils provides `gtimeout` on macOS.

Allowed files for this round: `scripts/agent-stop-gate.sh`, `tests/unit/test_agent_stop_gate.py`. Then `gh pr update-branch 237` (main is 138e6a72), wait for CI, and wait for the Codex Bot on the final head by listing `gh api repos/mryfmo/dotfiles/pulls/237/reviews --jq '.[]|select(.user.type=="Bot")|[.commit_id,.submitted_at]|@tsv'` and the top-level `pulls/237/comments` rows (`in_reply_to_id == null`), not by a 👍 reaction alone. The RESULT must name every unresolved thread id with `fixed:<sha>` or a proposed `not-applicable:<reason>`; reply inline on the ones you fix, resolve none.

### Round 4 addendum (orchestrator, 2026-10-04 03:35Z) — item 4 must not depend on coreutils

`grep -rn coreutils home/ install/` is empty: the macOS Brewfile does not install coreutils, so a `gtimeout` runner alone leaves the Mac on the uncapped read, which is the exact failure 4175723390 describes (hook past 5 s → output discarded → the seat stops). Replace item 4 with a dependency-free bound: when neither `timeout` nor `gtimeout` exists, run the history read as a background child with a watchdog (`sleep <remaining>` then `kill` the child, in a subshell) and map an expiry to rc 124 exactly like `timeout(1)`; keep `timeout`/`gtimeout` when present. The uncapped fallback and its `ponytail:` ceiling go away; the macOS skip in the slow-store test goes away too (the test exercises the watchdog path with `timeout` removed from PATH). The thread's final disposition will be `fixed:<this round's sha>`, not cb3ded43.

## Revise round 5 (orchestrator, 2026-10-04 05:30Z) — the last open thread, same class as the overrides

Fourteen of the fifteen threads are dispositioned and resolved (seven `fixed:` bc636cb7/3568b7e2, seven `not-applicable` as you proposed). The one left open is 4176068448: injected Git configuration (`GIT_CONFIG_COUNT`/`GIT_CONFIG_KEY_n`/`GIT_CONFIG_VALUE_n`, `GIT_CONFIG_PARAMETERS`) can hide a dirty tree from the `git status` probe (`status.showUntrackedFiles=no`, `core.worktree`, …), which is the same fail-open class as the overrides you already unset, so it is fixed, not accepted.

1. Unset `GIT_CONFIG_PARAMETERS` and `GIT_CONFIG_COUNT` alongside the other overrides (with `GIT_CONFIG_COUNT` unset, Git ignores the numbered KEY/VALUE pairs; say so in the comment). The hook runs in Claude Code's own process environment, not in the sandboxed Bash, so the sandbox's injected credential helper is not needed by the probes and clearing it there costs nothing; if you can show the hook environment carries `GIT_CONFIG_PARAMETERS`, prefer `env -u` on the two probes instead and paste the evidence.
2. Test: with `GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=status.showUntrackedFiles GIT_CONFIG_VALUE_0=no` inherited and an untracked source file present, the orchestrator seat blocks; the same with `GIT_CONFIG_PARAMETERS="'status.showUntrackedFiles=no'"`.
3. One commit; `gh pr update-branch 237` only if `main` moved (it is 8922f13b); CI; the Bot on the final head (paginated listing); RESULT with the fix sha, final head and the remaining thread's disposition. The round-4 audits are running now; if they add a finding, an addendum follows before you push.

## Revise round 6 (orchestrator, 2026-10-04 07:20Z) — task-level audit of 92cad328 is `incorrect`

Findings (`.orchestration/validation/dotfiles-T65-agent-stop-gate-a01-audit-92cad32.md.last.md`) and dispositions:

1. **P2, protocol version ignored (a v2 or versionless RESULT clears a v1 TASK).** `not-applicable`, same as Bot thread 4176012060: `v1` is the only contract and senders are authenticated peers; the gate is a completion check, not a message validator. No change.
2. **P2, "never writes".** The watchdog path creates a private temp file, so the header's "The hook never writes" and the task's wording are false. Fix the claim, not the mechanism: the `@description` says the hook never writes to the agmsg store or the repository and that the watchdog fallback uses one private `mktemp` file under `TMPDIR`, removed before exit. One line.
3. **P3, 243 lines against the ≤150 target.** Task amendment: the orchestrator waives the line limit; every line past 150 came from the five review rounds it required. No change.
4. **P3, report says "no shellcheck disable".** False: `# shellcheck disable=SC1091` precedes the `source` of the storage facade. Correct the report (the disable is intended: the facade path is runtime-resolved) and the validation note.

One commit for item 2; artifact edits for item 4; CI; Bot (paginated listing); RESULT with the fix sha and final head. The task-level audit is re-run on the new head.
