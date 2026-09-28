# AGMSG-ACCEPTANCE dot-ua-core-build-shim-T33g-a01

RESULT 2026-09-28T11:50:06Z from claude-standard-dot-a005 (worker-c): revision 2, status=ready_for_review, PR #202 head 02fdac1bfed4eb40537accd0c24c11beb29d0d59, branch fix/ua-core-build-shim from origin/main 4bc28b7.

## Ruling during the task

PONG blocked 11:27Z (rev1): item 2 (Makefile) would break `tests/install/common/lifecycle.bats`, which asserts the exact `make update` call sequence and is outside allowed files. Ruling: option A — keep item 2 and update the two bats expectations (revision 2, 553038c). Correct fail-closed behavior.

## Adversarial review (orchestrator, from origin refs and the orchestrator-review worktree)

- Scope: 5 files (+77/−10), all allowed: `build_understand_anything_core` now prefers `mise exec npm:pnpm -- pnpm` whenever mise exists (installs the pin on demand; shim presence is not tool presence) and uses a bare PATH pnpm only without mise; `make update` installs `npm:pnpm` on the existing explicit `mise install --locked` line; lifecycle.bats' two call-sequence expectations updated accordingly; README sentence adjusted.
- Orchestrator re-derivation at 02fdac1: unit module OK; `shellcheck -x` clean; `make -n update` shows `mise install --locked npm:ccstatusline npm:ccusage npm:pnpm`; mutation baselines pasted and each fails on the old code (`test_prefers_mise_exec_over_an_unbacked_pnpm_shim`; `test_make_update_installs_the_pinned_pnpm`); PR CI 12/12 pass (bats included).
- CompactionDB: T33g decision present in the main-checkout DB.
- Refutation attempts found no correctness, security, or omission issue; live behavior verified below (the same procedure that failed for T33f).

## Pre-merge Codex audit (head 02fdac1, VISIBLE LANE via codex exec)

`Audit verdict: correct` — "No findings … `Makefile:72` installs the existing locked pnpm pin before agent assets; updated tests preserve ordering and failure handling … Verdict: correct." Evidence `.orchestration/validation/dot-ua-core-build-shim-T33g-a01-audit.md` (+ `.last.md`).

## Review guard

`make require-crit-review` satisfied via AGENT_REVIEWED=1 with REVIEW_EVIDENCE=.orchestration/validation/dot-ua-core-build-shim-T33g-a01-receipt.md (resolved review-scope approval record r_80893a, crit session 16eb550d49a7, exported JSON at .orchestration/validation/dot-ua-core-build-shim-T33g-a01-crit.json).

**Decision: ACCEPTED.** Merge #202 --squash (no --delete-branch while worker-c holds the branch); live verification: canonical ff pull, `mise uninstall npm:pnpm` and the Codex clone's `dist` moved aside (reproducing the T33f failure conditions), then `make update` and `make doctor` — recorded below.

[memory:decision] T33g accepted 2026-09-28: the Understand-Anything core build runs pnpm through `mise exec npm:pnpm` whenever mise exists (a shim can precede its installed version) and `make update` installs `npm:pnpm` explicitly, so a fresh pin is usable on the same run. PR #202 squash-merged.

cost: n/a (worker report gives no token figures)

### Live verification (orchestrator, this host, after merge 2b30a21) — PASSED

Reproduced the T33f failure conditions: `mise uninstall npm:pnpm@12.4.1` (pin shown as missing) and the Codex clone's `packages/core/dist` moved aside. `make update` (exit 0): `mise install --locked npm:ccstatusline npm:ccusage npm:pnpm` installed the pin; the core build ran through `mise exec npm:pnpm` ("already installed" at that point); `dist/index.js` present afterwards in both the Claude plugin cache (release artifact) and the Codex clone; `make doctor` reports 0 Understand-Anything core warnings and 0 chezmoi drift. The lifecycle now self-heals from a fresh pin on the same run.
