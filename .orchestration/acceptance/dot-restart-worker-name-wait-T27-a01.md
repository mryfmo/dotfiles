# AGMSG-ACCEPTANCE dot-restart-worker-name-wait-T27-a01

RESULT 2026-09-27T02:43:14Z from claude-standard-dot-a005 (worker-c, claude-opus-5-5 high, --advisor fable): status=ready_for_review, PR #189 head fcc188c9f882dc5b512712dc3b712c89bba525c2, branch fix/restart-worker-name-wait from origin/main 02a0069.

## Adversarial review (orchestrator, from origin refs)

- task_rev sha256 match confirmed (ac90ed83…, verified in worker validation against origin/main and branch base).
- Diff scope: exactly the 4 allowed files (+139/−1).
- Fix location as specified: `start_agent_in_pane` gains an `*agent_name_taken*` case arm (first arm; single-arm `case` semantics prevent fall-through into the timeout arm). New `wait_for_agent_name_release` polls `herdr agent list` with jq `type == "array" and all(.[]; .name != $name)`; herdr/jq failure, empty output, or non-array shape count as still-taken. Bound 30×1s via `HERDR_AGENTS_NAME_RELEASE_POLLS`/`_INTERVAL` test seams (production defaults per spec). Single retry; on wait timeout the original `agent_name_taken` output reaches the unchanged truthful failure message; on retry failure the retry's output does. `restart_worker_in_pane` untouched.
- Observability: stderr line `Waited for herdr agent registration <name> to clear.` only when at least one poll elapsed — live E2E can distinguish race-absorbed from no-race.
- Refutation attempts: a legitimately live same-name agent keeps the wait failing → truthful failure (no clobbering); nested case arm ordering safe; normal path proven poll-free by test (c); one cosmetic extra sleep after the final failed poll (no correctness impact). No correctness, regression, security, or omission issue found.
- Tests: (a) restart path asserts rc 0, ≥3 `agent list` calls, exactly 2 identical starts, and the wait line; (b) bounded give-up asserts exactly 3 polls, 1 start, truthful message, no wait line, milliseconds runtime; (c) normal path asserts zero polling and no line. Mutation baseline pasted verbatim (2 FAIL on unmodified script, reproducing the live failure text).
- Evidence: 458 unit tests OK (skipped=1), validator ok, shellcheck/shfmt clean, CI 12 checks pass on fcc188c, CompactionDB decision id dcadc0c4-a62c-4d12-af4e-372b9fd87a8b pasted in validation.
- Disclosed deviations accepted: harness-forced plan file written untracked at the main checkout worklog (not committed); `.ua/` hook skip (graph refresh remains a separate worker task); live E2E deliberately orchestrator-side.

## Review guard

make require-crit-review satisfied via AGENT_REVIEWED=1 with REVIEW_EVIDENCE=.orchestration/validation/dot-restart-worker-name-wait-T27-a01-receipt.md (resolved review-scope approval record r_23886b, crit session 871550a2379c, exported JSON at .orchestration/validation/dot-restart-worker-name-wait-T27-a01-crit.json).

**Decision: ACCEPTED.** Merge #189 --squash (no --delete-branch while worker-c holds the branch); deploy (chezmoi apply both clones); live E2E `herdr-agents --restart-worker` on the wH pair — acceptance criterion: first-try success AND either the wait stderr line appeared or the registration was already clear; argv must remain `claude --model claude-opus-5-5 --effort high --advisor fable`.

[memory:decision] T27 accepted 2026-09-27: start_agent_in_pane absorbs the agent_name_taken race with a bounded herdr agent list wait plus one retry, stderr-observable; the herdr-worker-relaunch rule candidate carries no open tooling gap. PR #189 squash-merged.

[memory:decision] Operator 2026-09-27: Codex CLI is re-authenticated with the same account as Claude Code (moriya.fumio@technopro.com); the remediation-plan "Codex login" operator blocker is cleared. worker_kind stays claude until the operator says otherwise.

cost: n/a (worker report gives no token figures)

### Live E2E addendum (2026-09-27 ~11:5x+09:00, orchestrator)

Deployed via canonical-clone ff pull to ed49550 + `chezmoi apply` (fix confirmed present in the installed script). `herdr-agents --restart-worker` on the wH pair succeeded on the FIRST try and printed `Waited for herdr agent registration claude-worker-wh to clear.` — the agent_name_taken race actually fired on this run and the bounded wait absorbed it, satisfying the acceptance criterion (first-try success AND wait-line evidence). Post-restart: `claude-worker-wh` registered on wH:p2 (idle), process argv verified as `claude --model claude-opus-5-5 --effort high --advisor fable` (no T26 regression). The T26 addendum's follow-up candidate is closed.
