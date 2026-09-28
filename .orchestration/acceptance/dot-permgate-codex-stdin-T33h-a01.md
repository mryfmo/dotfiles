# AGMSG-ACCEPTANCE dot-permgate-codex-stdin-T33h-a01

RESULT 2026-09-28T19:48:11Z from claude-standard-dot-a005 (worker-c): status=ready_for_review, PR #203 head 6bc5918808b71b802c74bc35064e78079f7b9712, branch fix/permgate-codex-stdin from origin/main a4bddfc.

## Adversarial review (orchestrator, from origin refs and the orchestrator-review worktree)

- Scope: 2 files (+52): `stdin=subprocess.DEVNULL` on the codex `subprocess.run` in `classify()` only (claude branch untouched; bench and the hook share `classify()`, so no second change — stated in the report), plus one test that runs `permgate bench` with an open `os.pipe()` as stdin while the fake codex reads stdin to EOF.
- Orchestrator re-derivation at 6bc5918: full `tests.unit.test_permgate` module under `sleep 20 |` (open stdin pipe) → `OK (skipped=1)`; the pasted mutation baseline shows the new case failing on the unmodified script with `status_counts: {"timeout": 5}` and passing after the fix; PR CI 12/12 pass.
- Product behavior: hook classification no longer depends on the caller's stdin; timeouts, prompts and policy unchanged.
- CompactionDB: T33h decision present in the main-checkout DB. The worker also deleted its merged local branch `fix/ua-core-build-shim` as permitted; the remote copy was removed by the orchestrator.
- Refutation attempts found no correctness, security, or omission issue.

## Pre-merge Codex audit (head 6bc5918, VISIBLE LANE via codex exec)

`Audit verdict: correct` — "No actionable findings … correctly supplies EOF to the Codex classifier while preserving argv prompts, timeouts, and permission policy … an independent pipe/EOF probe passed." Evidence `.orchestration/validation/dot-permgate-codex-stdin-T33h-a01-audit.md` (+ `.last.md`).

## Review guard

`make require-crit-review` satisfied via AGENT_REVIEWED=1 with REVIEW_EVIDENCE=.orchestration/validation/dot-permgate-codex-stdin-T33h-a01-receipt.md (resolved review-scope approval record r_861445, crit session 16eb550d49a7, exported JSON at .orchestration/validation/dot-permgate-codex-stdin-T33h-a01-crit.json).

**Decision: ACCEPTED.** Merge #203 --squash (no --delete-branch while worker-c holds the branch); deploy the hook script with a single-target `chezmoi apply ~/.local/bin/common/permgate`; then dispatch T33i.

[memory:decision] T33h accepted 2026-09-29: permgate runs the codex classifier with `stdin=subprocess.DEVNULL`, so hook classification never depends on the caller's stdin. PR #203 squash-merged.

cost: n/a (worker report gives no token figures)
