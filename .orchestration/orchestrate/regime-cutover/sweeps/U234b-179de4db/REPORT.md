# Security audit report: dotfiles at 179de4dbf984617d48e823ca2123de59dea6d9d3

## 1. Run, scope and limits

**This is a partial pass.** It is a scoped run, and it ran without independent agents.

**Profile and scope.** The profile is `standard`, scoped to the U234b change d2389a05..179de4db (branch `test/linear-time-tests-judge-against-a-baseline`): one file, `tests/unit/test_validate_agent_assets.py` (+115/−52). The scanner it exercises, `scripts/validate-agent-assets.py`, is unchanged. Every other top-level directory and the root files are carried `out_of_scope`, with no coverage claim.

**Brief discrepancies.** The brief calls run-4 "the U234b head", but run-4 swept records sync 45. It is this seat's previous run, and I carried it as asked.

**Source ref.** The checkout was clean at the head both before and after the run.

**Budget.** None was set. Planned: four reconnaissance agents, one hunter wave, two critics, and one verifier per candidate. Spent: zero delegated agents.

**Execution.** Sandboxed source-and-local-only policy, and in practice source only. By task rule, the tests were read, not run.

**Independence gap.** The delegation tool (Task) and eval kernel are denied by policy on this seat. Reconnaissance, the hunter wave and both critics ran in the parent (`parent-hunter`). `run-metadata.json` records `run_status: "incomplete"` with reason `independent_agents_unavailable`. No candidate survived, so no verifier was needed.

**Prior runs.** I carried run-4 (records sync 45 at 2f1f2c67: 40 units, 0 findings, 1 unvalidated candidate).
- **Store units.** Its five store units are out of scope, because the records sync commits are not on this branch.
- **Candidate.** Its unit records that the `claude auth status` row is absent here and on origin/main d2389a05. The candidate stays open on the pushed `records/sync-43`, `-44` and `-45` branches, and nothing in this head carries it.
- **Out of scope.** Its other units carry over; `tests#unchanged-paths` now excludes only the changed module.

**Deferred.** Nothing.

## 2. Security posture

No candidate survives. The change is test-only, and it keeps the property the tests guard. The committed-secret scan runs over pull-request text in CI and over store copies in the records lever, and must stay linear in its input.

- **Sensitivity.**
  - The judged value is the scan's growth divided by a linear reference's growth over the same 8x step (`tests/unit/test_validate_agent_assets.py:155-160`, `:171-205`).
  - A linear scan judges about 1 and a quadratic one about 8, against the bound of 3 (`:2881`, `:3023`, asserted at `:2921-2926` and `:3049-3050`). A quadratic scan would pass only if the linear reference grew 21x or more over an 8x step.
  - In units of the size factor this matches the old bound of 24 on the raw ratio (3x linear). The new form cancels runner load that hits the scan and the reference alike.
- **Hang cap.** The 20 s cap still applies to both judged sizes (`:2918-2920`, `:3041-3042`).
- **Correctness.** The assertions for every size and form are unchanged. The untimed 2,000 size keeps its assertions (`:2894-2906`).
- **Fixtures.** The planted tokens are dummies built by concatenation (`:3021`). Every write goes under a `mkdtemp` root that `module.ROOT` points at during the test (`:209-220`, `:529-533`). The diff adds no subprocess, network call, environment read or new file write.

## 3. Confirmed findings

None.

| Severity | Title | Affected boundary | Observed result |
|---|---|---|---|
| — | none | — | — |

## 4. Confirmed finding details

None.

## 5. Needs validation

None.

| Title | Trace | Blocker | Local next step | Owner-observed check |
|---|---|---|---|---|
| — | — | — | — | — |

## 6. Hardening notes and positive patterns

These are not findings.

1. **The report test now times the fixture write.** The one-finding-per-line test runs `path.write_text` inside the scan that `linear_growth` judges (`:3029-3035`); the old test wrote the fixture outside the timed region. A linear write that costs several times the report scan at 8,000 findings dilutes a quadratic report: with a write four times the scan, a fully quadratic report judges about 2.4, under the bound. Timing only `validate_no_obvious_secrets`, or writing both fixtures to separate paths before timing, would keep the guard's full sensitivity.
2. **Calibration happens on first calls.** The reference's round count comes from the test's first timed calls (`:193`). A cold first call changes only the reference's absolute time, not its growth ratio, so the judged value is unaffected.
3. **Records-sync candidate, outside this head.** `records-sync/redaction/account-identity-residue-in-published-row` (run-2 to run-4) is not carried by this branch. It stays open on the `records/sync-*` branches.

### Positive patterns

- A complexity guard that judges against a reference measured alongside, interleaved, least-of-five, and documented with its measured idle and loaded ranges.
- The hang cap and every correctness assertion are kept.
- Dummy secrets are built by concatenation, and scans run in a `mkdtemp` root.

## 7. Coverage summary

From `coverage-ledger.json` (42 units):

| Status | Units |
|---|---|
| covered | 2 |
| candidate | 0 |
| blocked | 0 |
| deferred | 0 |
| out_of_scope | 40 |

The two covered units are new, owned by `parent-hunter` with source checks:
- the linear-time guard (`RESOURCE-EXHAUSTION-AND-AVAILABILITY.md#Superlinear parsing, matching, or evaluation`);
- the planted fixtures (`ATTACK-CLASSES.md#Obvious things`).

The 40 out-of-scope units are every other top-level directory, the unchanged `tests/` paths, the root files, run-4's five store units, and the earlier carried units.

**Critic results.** Neither the post-wave critic nor the final-clean critic found work. Both ran in the parent, so this is a single-reviewer coverage statement.
