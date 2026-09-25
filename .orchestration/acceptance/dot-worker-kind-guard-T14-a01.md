# AGMSG-ACCEPTANCE dot-worker-kind-guard-T14-a01

## Round 1 — status: revise (2026-09-25 ~09:45Z)

PR #180 (3be8b86, 3326e83), CI green, scope exactly the allowed files.

### Orchestrator process
- Independent adversarial review in a separate context (general-purpose agent, parent model tier, fresh context) against the worktree branch: ran validator (`ok`), unit tests (120 OK), shellcheck/shfmt (Makefile flags) clean, a live-state simulation of the SessionStart `--attach` hook (rc=2, zero herdr calls), and a mutation test (guard call removed → refusal test fails in full and attach modes).
- Findings recorded as Crit comments on the branch review session (`~/.crit/reviews/361c2c352e4f/review.json`): r_6ab5e6 (review), c_c66d4e (herdr-agents L543), c_9b609b (herdr-agents L613), c_c6c17e (README L315). Evidence JSON will be saved under `.agents/worklog/claude/crit/` at resolution.
- Integration guard note: `scripts/require-crit-review.py` inspects only the uncommitted working tree, so it reports "not required" for a committed PR branch. The PR touches a HIGH_RISK file (herdr-agents) and HIGH_RISK tokens (agmsg, herdr, hook), so agent-side review evidence is treated as required for this integration.

### Should-fix (sent as next_action)
1. Guard message and README imply that registering a second claude-code identity yields distinct routing. It does not: `whoami.sh` returns `multiple=true`, `check-inbox.sh` takes the first name for both sessions, `watch.sh` subscribes both sessions to all pairs. Reword: the guard stops the silent collision; distinct routing arrives with the agmsg role model (plan Phase 3).
2. `--bootstrap-agmsg` prints nothing when worker_kind=claude and exactly one claude-code identity exists, while full/attach then refuse. Add a count==1 hint and a test.
3. PR body and README must state the live consequence: after merge + `make update`, the SessionStart `herdr-agents --attach` hook exits 2 (log only, `|| true`) on every session start until a worker identity is registered or worker_kind is codex.
- Nits: message cites the gitignored `.agents/worklog/...` plan (point to README instead), `join.sh` unqualified, workdir unquoted; `--bootstrap-agmsg` skips the worker_kind value check.

### Live evidence of the defect this PR guards against
Worker PONG 09:31:37Z: its Stop hook (`check-inbox.sh claude-code /home/moriya/Workspace/dotfiles`) delivered and marked read message 255 (the worker's own RESULT addressed to the orchestrator). The orchestrator received it through its Monitor stream anyway. This is the (path, type) identity collision in production.

### Operator preconditions before Phase 1.4 (`make update`)
Register a worker identity or set `worker_kind: codex` (after `codex login`), otherwise the attach hook becomes a no-op on this machine.

cost: n/a

## Round 2 — status: accepted (2026-09-25 ~10:35Z)

- Revision commits 01b38be (message/README/PR body reworded; bootstrap count==1 hint) and aa17407 (test compares resolved workdir). Orchestrator verified each should-fix against origin/fix/worker-kind-guard (message L544-545, hint L617-619, README L314-321, PR body "Live consequence"), no gitignored path cited, CI 12 pass.
- Full-suite permgate failure in the worker's validation (`test_bench_runs_five_layer_two_fixtures`, 10/10 locally at the time) did not reproduce for the orchestrator in the main checkout or the worktree with `uv run python` (3.13) or `python3` (3.14); the PR does not touch permgate; CI green. Recorded as a flake to watch (plan Phase 5).
- Crit evidence: `.agents/worklog/claude/crit/pr-180-review.json` (4/4 resolved); receipt `.agents/worklog/claude/crit/pr-180-receipt.md`; `AGENT_REVIEWED=1 REVIEW_EVIDENCE=<receipt> make require-crit-review` exit 0 (guard itself reports "not required" for a committed branch — limitation noted, follow-up in Phase 5).
- Merged: squash into main. CompactionDB decision 43e60fb8 present.
- Not yet applied to $HOME: `make update` (Phase 1.4) waits for the operator's Codex login and worker_kind decision, because the guard makes the SessionStart attach hook exit 2 in the current single-identity state.

cost: n/a
