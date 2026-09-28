# AGMSG-ACCEPTANCE dot-audit-pane-visibility-T32-a01

## Revision 1 — REVISE (2026-09-27T23:47Z)

RESULT 2026-09-27T23:43:25Z from claude-standard-dot-a005 (worker-c, claude-opus-5-5 high, --advisor fable): status=ready_for_review, PR #194 head 8af8d116d5e75343f529dc15a1cd19e286f2d0e2, branch feat/audit-pane-visibility from origin/main 7f3164e.

### Adversarial review (orchestrator, from origin refs and the orchestrator-review worktree)

- task_rev f3e9313e… matches the task file at origin/main 7f3164e; the PR does not touch `.orchestration/tasks/`.
- Diff scope: 5 files (+407/−6), exactly the allowed files (herdr-agents, rules bullet, SKILL carve-out, README paragraph, test_herdr_agents.py).
- Independent re-derivation: the 11 new `-k audit` tests were re-run at 8af8d11 in `.claude/worktrees/orchestrator-review` (detached) — `Ran 11 tests … OK`. PR CI 12/12 green (nix skipped). herdr 0.9.1 flags the mode depends on were verified against the live CLI help: `tab create --workspace/--cwd/--label/--no-focus`, `tab list --workspace`, `pane wait-output --regex/--source/--timeout` ("searched immediately, including existing output" — confirms the nonce rationale), `pane rename <pane> [LABEL]`, and `pane list` carrying `tab_id`.
- Injection surface: sha (`^[0-9a-fA-F]{7,40}$`), timeout (positive integer) and `--out` (no `'`/control chars) are validated before any herdr call; args from `MODEL_PROFILE_AUDIT_CODEX_ARGS` are `%q`-quoted. Marker regex requires `:[0-9]+` so the echoed `:%s` command line cannot self-match.
- Worker-declared deviations 1–7 all ACCEPTED: pipefail exit status (the task's literal `| tee; $?` would report tee's status), per-run nonce (wait-output searches existing output), `empty_pane_id`/split-source exclusion of the `audit` label (mutation baseline proved full-mode heal would start the worker in the audit pane — a strengthening, no guard weakened), `tab create --label`, args from model-profiles.env, `--timeout`, `--no-focus`.
- Process notes: (8) the AGMSG-PING (23:30:34Z) reached the worker only via inbox.sh — third occurrence of the delivery miss for the a005 identity (the worker session's own watcher resolves the main path, not worker-c; structural, see [[herdr-worker-worktree-identity]]); one read-only `pane wait-output --match` probe against the orchestrator pane wJ:p1 (timed out, no mutation) — disclosed, tolerated once, not to be repeated.
- CompactionDB: 7091c219-a3da-4732-888c-7b08a8e1b4f7 present in the main-checkout DB (`memory list`), as the report claims.

### Pre-merge Codex audit (head 8af8d11, gpt-6-astra, read-only, headless)

Evidence: `.orchestration/validation/dot-audit-pane-visibility-T32-a01-audit.md`. Two P2 findings, both independently confirmed by the orchestrator and ACCEPTED as defects:

1. Reused audit pane may have `cd`'d elsewhere; `tab create --cwd` only applies at creation → the review command must set its working directory on every run.
2. A DIR containing `'` breaks the single-quoted `bash -c` (validation runs on the raw `--out` before `workdir` is prepended) → validate the resolved absolute evidence path and workdir (fail closed) or quote the whole command.

**Decision: REVISE (one consolidated round).** next_action: revision 2 on the same branch — cd prefix in the inner command; validation of the resolved path and workdir; one test per fix with a mutation baseline against 8af8d11; test (b) expectation updated; inbox.sh at each milestone.

cost: n/a (worker report gives no token figures)

## Revision 2 — ACCEPTED (2026-09-28)

RESULT 2026-09-28T00:11:16Z from claude-standard-dot-a005: revision=2, PR #194 head 969187082eb056c4cdca06f279362a76d3a30a74, one fix commit on the same branch (no rebase; origin/main still 7f3164e).

### Adversarial review of the delta (8af8d11..9691870, from origin refs)

- Delta: 2 files (+51/−6), both within allowed files. Finding 1: the inner command is now `cd -- <%q workdir> && set -o pipefail && codex … | tee -- <out>; printf "<marker>:%s\n" "$?"` — every run executes in DIR, and a failed cd still reaches the marker with a nonzero status. Finding 2: the quote/control-char check now runs on the RESOLVED `workdir` + absolute evidence path (after `cd`/`pwd -P`, before any herdr call), fail closed with usage/exit 2; the raw `--out` check was removed as redundant (the concatenation covers it).
- Independent re-derivation: 13 `-k audit` tests re-run OK at 9691870 in the orchestrator-review worktree; PR CI 12/12 pass (nix skipped). Mutation baseline rev2 3/13 FAIL against the 8af8d11 script (the two new tests + updated (b)); 488 unit tests OK.
- Runtime check the worker could not perform (permission-denied locally, disclosed): the orchestrator executed the generated command string in a scratch directory — real `codex` exited 1 outside a git repo and the marker read `:1` through pipefail with the output tee'd to the evidence path; a failed `cd` produced marker `:1`. The rev2 Codex audit independently confirmed success, failure, and failed-cd marker semantics by isolated execution.
- Omissions: sandbox/learning records were not extended for revision 2 (nothing new to record: same worktree, no host mutation) — tolerated.

### Pre-merge Codex audit (head 9691870)

"No actionable regressions" — appended to `.orchestration/validation/dot-audit-pane-visibility-T32-a01-audit.md`. Both revision-1 P2 findings closed.

### Review guard

`make require-crit-review` satisfied via AGENT_REVIEWED=1 with REVIEW_EVIDENCE=.orchestration/validation/dot-audit-pane-visibility-T32-a01-receipt.md (resolved review-scope approval record r_d126a2, crit session 16eb550d49a7, exported JSON at .orchestration/validation/dot-audit-pane-visibility-T32-a01-crit.json).

**Decision: ACCEPTED.** Merge #194 --squash (no --delete-branch while worker-c holds the branch); deploy the script to this host with a single-target `chezmoi apply ~/.local/bin/common/herdr-agents` from the canonical clone after its ff pull (full `make update` already ran for T31 under operator sudo); then the live E2E `herdr-agents --audit <merge-sha>` in this pair workspace (wJ) — acceptance criterion: exactly one `audit` tab created, evidence tee'd, `Audit exit: 0` printed, and a second run reuses the tab. Live E2E result recorded below.

[memory:decision] T32 accepted 2026-09-28: `herdr-agents --audit <sha> [--out PATH] [--timeout SECONDS] [DIR]` runs `codex <MODEL_PROFILE_AUDIT_CODEX_ARGS> review --commit <sha>` visibly in the pair workspace's dedicated `audit` tab (created once, reused, left open; cd into DIR every run; nonce exit marker; pipefail exit propagation; evidence tee'd to .orchestration/validation/audit-<sha>.md by default; fail-closed validation of sha/timeout/resolved paths); the auditor stays identity-less, read-only, orchestrator-invoked; headless `codex --profile audit review` remains the no-herdr fallback. PR #194 squash-merged.

Carry-over to T33 (rules task): third occurrence of the a005 delivery miss (worker session's watcher resolves the main path, not worker-c) — codify "inbox.sh at each milestone" for workers acting under a non-session identity until the role/seat model (T34) lands; revision/PING dispatches assume pickup at the worker's next inbox check.

cost: n/a (worker report gives no token figures)

### Live E2E (orchestrator, pair workspace wJ, 2026-09-28, script deployed via single-target chezmoi apply after merge 6b9babc)

- Run 1: `herdr-agents --audit 6b9babc --out .orchestration/validation/dot-audit-pane-visibility-T32-a01-live-e2e.md --timeout 560 ~/Workspace/dotfiles` → tabs before {t1, t2}; after {t1, t2, t3=audit} with exactly one new pane wJ:p4 labeled `audit`; the real gpt-6-astra audit ran visibly in that tab, 3m42s wall clock, `Audit exit: 0`, evidence tee'd (3586 lines). Pair panes p1/p2 untouched.
- Run 2: `herdr-agents --audit 0000000 …` (unknown commit) → no new tab (still exactly one `audit` tab), 17s, `Audit exit: 0` because codex itself exits 0 on "Review blocked: 0000000 does not resolve to a commit" — a codex behavior, not a launcher defect. Nonzero propagation is proven separately: orchestrator scratch execution of the generated chain (real codex exit 1 → marker `:1`; failed cd → marker `:1`), the rev2 Codex audit's isolated execution, and the unit tests.
- Acceptance criterion met: one tab created, reused on the second run, evidence tee'd, exit marker propagated, pair modes unaffected.

### Post-merge live audit findings (6b9babc, first audit produced by the new lane) — dispositioned

1. [P2] Under `LC_ALL=C`, non-ASCII path characters make `%q` emit `$'…'` quoting that breaks the single-quoted `bash -c` argument (the fail-closed check only covers `'` and control characters). ACCEPTED as a real edge defect — not reachable on this host (ja_JP.UTF-8, ASCII paths) but fixable by building the inner command first and `%q`-quoting it once as a single `bash -c` argument. → follow-up task dot-audit-pane-hardening-T32b-a01.
2. [P2] A pane narrower than the exit marker wraps it across rendered lines in the `recent` snapshot, so the regex misses completion and reports a timeout. ACCEPTED — `herdr pane wait-output`/`pane read` support `--source recent-unwrapped` (verified in the live CLI help). → same follow-up task.

Neither finding blocks acceptance: both are P2 edge cases outside the operator's environment, the merged lane already works end to end, and the fix is a bounded worker task.
