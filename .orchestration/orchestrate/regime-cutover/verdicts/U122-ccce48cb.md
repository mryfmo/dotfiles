## Findings

- P1 (high) scripts/orchestrator/audit-carry.py:316: Ignoring the current head's existing incorrect audit lets the lever emit carried evidence from an older correct head; the merge gate then reads the older verdict and bypasses the current head's unresolved P1 without a fix.
- P2 (high) scripts/orchestrator/audit-carry.py:508: A regular-file-to-symlink change produces two patch sections for one raw T record, so this check rejects a valid diff with exit 2 and prevents the next audit from running.
- P3 (high) scripts/orchestrator/audit-carry.py:425: If git init fails after mkdtemp succeeds, scratch_repository raises before main receives the path, leaving the scratch directory behind despite the cleanup guarantee.

## Reproduced

- Git diff/status inspection: reviewed the specified 14-file changeset at ccce48cbcee9ca75780869b976ab2841b25e0e67; the repository remained clean.
- python3 -m unittest tests.unit.test_audit_carry: all 21 tests passed.
- python3 -m unittest tests.unit.test_audit_carry tests.unit.test_pr_levers: 115 tests ran; runtime failures included the sandbox-blocked system Perl library and unavailable masking dependencies.
- python3 -m unittest tests.unit.test_pr_audit: 72 tests ran, with 199 failures, one error and two skips; system Perl failed before the relevant audit paths could execute.
- Targeted carried-row merge test with fail-fast: also stopped because the sandbox blocked libperl.dylib.
- python3 -m unittest tests.unit.test_hcom_seat_skills tests.unit.test_regime_init.AuditSectionTest: all 12 tests passed.
- Chronological-ledger probe: an already incorrect current head with an unresolved P1 still received carried evidence; extracted merge gates accepted the older correct verdict after equivalent process substitutions replaced sandbox-blocked here strings.
- File-to-symlink fixture: --render exited 2 with '2 patch sections for 1 raw records'.
- Injected git-init failure: scratch_repository raised Malformed and left an audit-carry.* directory behind.
- Alternate-ref-command and shallow-source probes: unequal heads remained not carried, and rendering succeeded.
- Out-of-order-ledger probe: the merge gate accepted the last physical correct row despite a newer incorrect timestamp; this selection behavior predates the changeset and is excluded from findings.
- ShellCheck, bash -n, shfmt, source/install cmp checks and git diff --check: passed.
- scripts/generate-agent-configs.py --check: could not run because PyYAML is unavailable.
- Standard-library integrity checks: changed lever sources, installed copies, manifest pins and generated digests agree; the Audit section matches its template.

## Notes

No network or CI checks were performed. Broader runtime verification was limited by sandbox and dependency failures; the findings were reproduced with focused local fixtures.

Blocking: 1
Verdict: incorrect
