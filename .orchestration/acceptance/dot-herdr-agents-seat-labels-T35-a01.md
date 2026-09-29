# AGMSG-ACCEPTANCE dot-herdr-agents-seat-labels-T35-a01

RESULT 2026-09-29T04:50:41Z from claude-standard-dot-a005 (worker-c): status=ready_for_review, PR #207 head 903c9fad9901198acf585465c9b684a820c00994, branch fix/herdr-agents-seat-labels from origin/main b790ee0.

## Adversarial review (orchestrator, from origin refs and the orchestrator-review worktree)

- Diagnosis (worker, verbatim in validation): upstream self-naming (`lib/self-name.sh` on send/inbox actions, herdr `ops.sh`) runs `herdr pane rename <id> <team>:<agent>` and `herdr agent rename <id> a<sha256[0:24]>`; no agmsg script renames workspaces (the `dotfiles` workspace label never carried the managed marker — the workspace was found only through the old orchestrator pane label); self-naming was not disabled. Matches the orchestrator's live observation.
- Fix: `load_seat_labels` reads seats at the repository's main checkout (git common dir): orchestrator = the non-`aNNN` claude-code identity, worker = the pair's own worker-type seat (the `HERDR_AGENTS_WORKER_WORKTREE` seat, or the legacy `-aNNN` at main), other team members are not workers, `$HOME` skipped; `normalize_seat_labels` maps `<team>:<name>` to `claude-orchestrator` / `<kind>-worker` on every pane list so workspace/role detection, attach, restart, heal and the ambiguity refusal work unchanged, legacy labels still work; `rename_pane_unless_seat_named` never relabels a self-named pane; attach falls back to the seat label for the worker; audit tab unchanged.
- Independent re-derivation at 903c9fa: `test_herdr_agents` 136 OK; `shellcheck -x` clean; `make validate-agent-assets` ok; PR CI 12/12 pass. Mutation baselines pasted (6/6 new tests fail on origin/main; 3 of 4 review tests fail on 549b257, one is a guard). Worker-side independent review of 549b257 returned "incorrect" (2 P2: every member mapped to the worker so heal could duplicate a worker; orchestrator attach refused because it used the renamed agent name; 5 P3) — all fixed in 903c9fa with resolved crit records.
- Merge-order fact (worker): with T35 alone, the live worker a005 is recognized only once `HERDR_AGENTS_WORKER_WORKTREE` is rendered (T34's manifest field); T34's branch also carries a stray 100755 mode flip, to be fixed in its revision. Orchestrator plan: merge T35 now, merge the T34 revision when accepted, then one `chezmoi apply`, then live E2E of both (`--audit`, `--restart-worker` re-seat, PING via Stop hook).
- CompactionDB: T35 decision ad0dbc1a present.
- Refutation attempts found no correctness, security, or omission issue.

## Pre-merge Codex audit (head 903c9fa, headless with the lane's prompt and `-o` channel; the visible lane cannot find the relabeled workspace until this very fix lands)

`Verdict: incorrect`, two **P2 (high)**, both reproduced by the auditor with parent/commit functions and confirmed by the orchestrator:
1. `load_seat_labels` selects the worker by the `-aNNN` suffix, so a supported solo worker identity (e.g. `codex-standard-dot`) is not treated as a worker → `--restart-worker` cannot find it and full-mode heal duplicates it; the parent recognized it. ACCEPTED → worker seat = any worker-type seat at the worker worktree, else any non-orchestrator identity at main, suffix-agnostic.
2. `load_seat_labels` sources `~/.agents/model-profiles.env` in the caller's shell scope and overwrites explicit `HERDR_AGENTS_WORKER_KIND`/`_PROFILE` (`express`→`standard`, `codex`→`claude`), so bootstrap skips the Codex hooks while the cached kind still launches Codex. ACCEPTED → read the env in a subshell or function-local scope as `resolve_worker_kind` does.

**Decision on revision 1: REVISE (one round; queued behind the T34 revision on the same worker).**

## Revision 2 — ACCEPTED (2026-09-29)

RESULT 05:17:21Z: head 72a0a14d7459c53ccaff72b27d0c1d6e88ceb7d4 (+67/−13). Worker seat = any worker-type seat at the worker worktree, else any non-orchestrator identity at main (solo and `-aNNN` alike); the profiles env is read in a subshell inside `load_seat_labels`. Orchestrator: 139 herdr-agents tests OK at 72a0a14, `shellcheck -x` clean, baseline 3/3 fail on 903c9fa (solo codex found by restart, not duplicated by heal, explicit kind/profile survive), CI 12/12 pass, file mode 100644 as on main.

Headless Codex audit of 72a0a14 (`-audit-rev2.md`): `Verdict: correct` — "correctly recognize solo Codex workers, exclude orchestrator identities, and preserve explicit worker settings through subshell isolation."

### Review guard

`make require-crit-review` satisfied via AGENT_REVIEWED=1 with REVIEW_EVIDENCE=.orchestration/validation/dot-herdr-agents-seat-labels-T35-a01-orchestrator-receipt.md (resolved review-scope approval record r_77ee9a, crit session 16eb550d49a7, exported JSON at .orchestration/validation/dot-herdr-agents-seat-labels-T35-a01-orchestrator-crit.json).

**Decision: ACCEPTED.** Merge #207 --squash (no --delete-branch while worker-c holds branches); deploy together with T34 (`chezmoi apply` after both merges), then live E2E: `herdr-agents --audit <PR head>` on the relabeled pair, and T34's `--restart-worker` re-seat + PING via Stop hook.

[memory:decision] T35 accepted 2026-09-29: herdr-agents recognizes the managed pair by agmsg seat evidence — `<team>:<name>` self-named pane labels normalized to the role labels from the identities registered at the main checkout and the worker worktree, suffix-agnostic, legacy labels kept, self-named panes never relabeled — so upstream agmsg 1.5.0 self-naming no longer hides the workspace from `--audit`, `--attach`, `--restart-worker` and heal. PR #207 squash-merged.

cost: n/a (worker report gives no token figures)
