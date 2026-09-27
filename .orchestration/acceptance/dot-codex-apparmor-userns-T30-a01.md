# AGMSG-ACCEPTANCE dot-codex-apparmor-userns-T30-a01

RESULT 2026-09-27T05:08:58Z from claude-standard-dot-a005 (worker-c, claude-opus-5-5 high, --advisor fable): status=ready_for_review, PR #192 head 74b517b4331a7283b165610ceb89895dff14845c, branch feat/codex-apparmor-userns from origin/main c326c73 (task revision 2).

## Adversarial review (orchestrator, from origin refs)

- task_rev sha256 match confirmed (46979774…, revision 2, verified against c326c73).
- Diff scope: 9 files (+335/−2) against the merge base, all within allowed files.
- Investigation quality: worker traced the full exec chain (mise shim → codex.js → vendored musl codex → codex-linux-sandbox → **`/usr/bin/bwrap` by absolute path**, strace evidence) and correctly showed level (a) can never attach and the vendored bwrap path would be WEAKER (user-writable); the level-(b) ruling was applied as approved. The profile documents its own ceiling (`ponytail`-style: any bwrap caller gets userns; upgrade path = stacked bwrap-userns-restrict).
- Profile: Ubuntu stock per-app shape (`abi 4.0`, `flags=(unconfined) { userns, include if exists <local/…> }`), parses with `apparmor_parser -Q -K`, negative control fails (check is real).
- Installer: idempotent (`install -m 0644` + `apparmor_parser -r`), three no-op gates (restriction≠1 / no parser / no bwrap), sysctl untouched, env seams for tests, chezmoi run_onchange wrapper keyed on the profile's sha256.
- Doctor: effective-probe design (unprivileged `bwrap --ro-bind / / true`) instead of the root-only loaded-profile list — honest and testable; currently reports the required failure truthfully on this host (profile not yet deployed).
- OpenSandbox vocabulary: exactly the 2 lines replaced with neutral wording; record contract intact; history untouched.
- AGENTS.md Code Review Rules: byte-identical to the operator-provided block (worker diffed against the task file).
- Tests: 7 new tests; mutation baseline pasted (all FAIL/ERROR against origin/main export; worker self-tightened one vacuously-passing test). Full suite: one disclosed UNRELATED permgate benchmark flake (failures=1), isolated 3/3 and full rerun 469 OK (skipped=1) — de-flake recorded as a learning candidate.
- effects=apparmor-bwrap-userns-profile with the option-A reverse mapping (README + shdoc removal commands); NOT activated in-task (no sudo run — verified by the forbidden-actions contract and CI, where both Ubuntu bootstrap jobs hit the no-bwrap skip gate).
- Evidence: CI 13 checks pass on 74b517b; CompactionDB decision id 891736ee-64fb-41ff-b9be-37616b2ffd8e pasted.
- Refutation attempts found no correctness, regression, security, or omission issue.

## Review guard

make require-crit-review satisfied via AGENT_REVIEWED=1 with REVIEW_EVIDENCE=.orchestration/validation/dot-codex-apparmor-userns-T30-a01-receipt.md (resolved review-scope approval record r_72c78f, crit session 871550a2379c, exported JSON at .orchestration/validation/dot-codex-apparmor-userns-T30-a01-crit.json).

## Audit-lane disposition

Codex audit of this changeset is DEFERRED (the audit lane is exactly what this task repairs); queued with the e6ebd32 and 076f9e9 audits to run immediately after deploy.

**Decision: ACCEPTED.** Merge #192 --squash (no --delete-branch while worker-c holds the branch). Deploy requires ONE operator sudo (`chezmoi apply` runs the run_onchange profile install) — the orchestrator's shell is correctly denied sudo, so the operator runs the apply; then `make doctor` must show the bwrap probe found, and the deferred audits complete the T28 addendum-2 E2E.

[memory:decision] T30 accepted 2026-09-27: bwrap-userns AppArmor profile shipped (run_onchange + doctor effective-probe; sysctl untouched; documented removal), OpenSandbox vocabulary removed, operator Code Review Rules landed in AGENTS.md. PR #192 squash-merged; activation is a one-sudo operator deploy.

cost: n/a (worker report gives no token figures)

### Audit addendum (2026-09-27, orchestrator disposition of the deferred audit)
`codex --profile audit review --commit ad5f95d` (evidence: .orchestration/validation/dot-codex-apparmor-userns-T30-a01-audit.md) returned 2 findings; orchestrator dispositions:
1. P2 permanent skip (run_onchange hash covers only repo files, so a bwrap-absent first apply never retries) — ACCEPTED; T31 rev2 embeds prerequisite state in the rendered trigger.
2. P2 doctor severity (missing bwrap with codex present is only warn_optional) — ACCEPTED; T31 rev2 makes it a required failure.
Neither finding affects the deployed host (bwrap present, profile loaded, probe green); acceptance stands, fixes flow through T31 revision 2.
