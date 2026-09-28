# AGMSG-ACCEPTANCE dot-ua-core-build-T33f-a01

RESULT 2026-09-28T10:58:59Z from claude-standard-dot-a005 (worker-c): status=ready_for_review, PR #201 head 3d63f0af0ed52f906c4a60b8a5c930ed601a7765, branch fix/ua-core-build from origin/main 7b42472.

## Adversarial review (orchestrator, from origin refs and the orchestrator-review worktree)

- Scope: 7 files (+343), all allowed (update-agent-assets.sh, check-agent-runtime.py, mise config+lock pnpm pin, two new unit test files, README).
- `build_understand_anything_core <root>`: guarded by `packages/core/dist/index.js` (upstream's exact guard); pnpm from PATH (mise shim of the pinned `npm:pnpm`) else `mise exec npm:pnpm -- pnpm`; install `--frozen-lockfile` with plain-install fallback; WARN with the manual command on missing pnpm or build failure, never failing `make update`. Called on the release artifact before the existing copy loop and on the Codex clone when no artifact matches — matches the verified provisioning design. Deviation initially accepted in review (existence-only guard, staleness only in doctor) — REVERSED by the audit below: doctor's remedy (`run make update`) cannot repair a stale `dist` if the build skips whenever `dist/index.js` exists. Orchestrator error in the adversarial review.
- Doctor: `understand_anything_core_warnings` WARNs when the Codex-clone `dist/index.js` is missing or older than `src`, naming `make update`.
- Pin: `npm:pnpm = 12.4.1` (+ lock entry in the same version/backend shape as other npm tools). Window evidence pasted (`gh api` releases): 12.4.1 published 2026-09-10 (≥7 days old, compliant). Observation, not a defect: the window's "newest eligible" reading would pick 12.5.1 (2026-09-18); `make upgrade`'s `--before 7d` bump path will move it there at the operator's next upgrade.
- Tests: orchestrator re-ran the two new test modules at 3d63f0a → 47 tests OK; mutation baseline 10/11 fail against the unmodified scripts (pasted); 505 unit tests OK; `make validate-agent-assets` ok; plain `shellcheck` shows only pre-existing SC1091 info notes (identical on main), CI-style `shellcheck -x` clean; PR CI 12/12 pass.
- CompactionDB: T33f decision present in the main-checkout DB.
- Refutation attempts found no correctness, security, or omission issue; live behavior (real build through `make update`) is verified below.

## Pre-merge Codex audit (head 3d63f0a, VISIBLE LANE via codex exec) — `Audit verdict: incorrect`

Last message: "[P2] High confidence — `scripts/update-agent-assets.sh:654`: any existing `dist/index.js` skips rebuilding, even after source updates; consequently the new doctor warning's `make update` remedy leaves stale code unchanged when no matching release artifact exists. Check freshness before skipping and test this repair path. … Verdict: incorrect." Orchestrator: CONFIRMED — the task's own item 1 asked for the freshness skip, and the review wrongly accepted the existence-only guard. ACCEPTED → revise: the build guard adopts doctor's freshness rule (missing or older than any `packages/core/src` file or the root lockfile); tests for stale-rebuild, fresh-skip, and the doctor-WARN→build→clear repair path; baseline vs 3d63f0a.

**Decision on revision 1: REVISE.** First `incorrect` verdict produced by the lane; it caught a real inconsistency the orchestrator had let through.

## Revision 2 — ACCEPTED (2026-09-28)

RESULT 11:18:10Z: revision 2, head 657bfe4fef083b0cf4c22bb7bdc34b915eb29ffe (+107/−15 across script, doctor, README, two test files). Build guard and doctor share one freshness rule (dist missing, or older than any `packages/core/src` file or the root `pnpm-lock.yaml`; `find -newer` in bash, mtime comparison in Python). Orchestrator re-ran the two test modules at 657bfe4 → OK; `shellcheck -x` clean; baseline vs 3d63f0a shows `test_rebuilds_a_release_dist_older_than_its_sources` and `test_doctor_stale_warning_is_cleared_by_the_update_build` failing on the old guard; CI 12/12 pass. CompactionDB rev2 decision fff493a7 present.

Visible-lane Codex audit of 657bfe4 (`-audit-rev2.md`): `Audit verdict: correct` — "No findings … the rebuild guard correctly handles stale sources and lockfiles, with matching doctor checks and regression coverage."

### Review guard

`make require-crit-review` satisfied via AGENT_REVIEWED=1 with REVIEW_EVIDENCE=.orchestration/validation/dot-ua-core-build-T33f-a01-receipt.md (resolved review-scope approval record r_ebaee4, crit session 16eb550d49a7, exported JSON at .orchestration/validation/dot-ua-core-build-T33f-a01-crit.json).

**Decision: ACCEPTED.** Merge #201 --squash (no --delete-branch while worker-c holds the branch); live verification: canonical ff pull, then `make update` on this host with the Codex clone's `packages/core/dist` moved aside so the new build path runs for real, followed by `make doctor` (no core WARN) — recorded below.

[memory:decision] T33f accepted 2026-09-28: `make update` builds Understand-Anything `packages/core` (release artifact first, Codex clone otherwise) whenever `dist/index.js` is missing or older than `packages/core/src` or the root lockfile, using the mise-pinned `npm:pnpm` 12.4.1; `make doctor` warns under the same rule; the build never fails `make update` (WARN with the manual command). PR #201 squash-merged.

cost: n/a (worker report gives no token figures)

### Live verification (orchestrator, this host, after merge 48b4009) — FAILED, follow-up tasked

Procedure: canonical clone ff pull → Codex clone `packages/core/dist` moved aside (doctor then WARNed "core not built … run make update", as designed) → `make update` (exit 0) → dist still absent, doctor still WARNs.
Log: in "Codex Understand-Anything skills", `build_understand_anything_core` ran on the release artifact and printed `WARN: Understand-Anything core build failed in ~/.claude/plugins/cache/…/2.9.7; run: …` twice; the underlying error was `mise ERROR No version is set for shim: pnpm`. Root cause: `has_command pnpm` is true because the mise shim exists, but the newly pinned `npm:pnpm 12.4.1` was not installed — `make update` runs `mise install --locked` only for `node` and `npm:ccstatusline npm:ccusage`, there is no mise onchange script, and new pins are installed only by `make upgrade` or on-demand `mise exec`. The `mise exec npm:pnpm` fallback never ran because the shim satisfied the command check. Neither the review nor the audit caught the shim-without-installed-version case (fake CLIs always succeeded).
Recovery: dist restored from the backup; `mise exec npm:pnpm -- pnpm --version` auto-installed 12.4.1 (2.0 s), after which the shim resolves and `make doctor` reports no core WARN. Host state is consistent again.
Disposition: T33f's reviewed deliverables stand (guard, doctor, pin, tests), but the lifecycle does not yet self-heal on a host where the pin is not installed → **dot-ua-core-build-shim-T33g-a01**: prefer `mise exec npm:pnpm -- pnpm` whenever mise is present (it installs the pinned version), fall back to a PATH pnpm only without mise, and add `npm:pnpm` to the explicit `mise install --locked` list in `make update`; tests with a fake shim that fails like mise does.
