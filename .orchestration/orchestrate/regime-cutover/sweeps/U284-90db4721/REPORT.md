# Security audit report: dotfiles at 90db472140e98b83beb0618acfb71129e7df6f52

## 1. Run, scope and limits

**Candidate validation is incomplete, so this is a partial pass.** The carried candidate is still on origin/main, and no independent verifier could run.

| Fingerprint | Coverage unit | State |
|---|---|---|
| `records-sync/redaction/account-identity-residue-in-published-row` | `.orchestration/orchestrate/regime-cutover#records-sync-43-copies` × `…/redact-words.txt#redact-word-and-identity-scan` | `candidate`, unvalidated (carried; on main since aabee966) |

Per the skill's rule, an unvalidated candidate is not a finding and is not in `findings.json`, and the run is `incomplete`. Section 5a describes it for the owner.

**Profile and scope.** The profile is `standard`, scoped to the U234c change a23e4541..90db4721 (branch `test/linear-time-cpu-min-of-repeats`): one file, `tests/unit/test_validate_agent_assets.py` (+112/−106). The scanner is unchanged. The scope also includes the carried candidate, because this base holds its row. Every other path is carried `out_of_scope`.

**Brief discrepancies.** The brief gives the base as 8f31cf5c. The merge base is a23e4541, where U241b and U241c have merged (#696).

**Source ref.** The checkout was clean at the head both before and after the run.

**Budget.** None was set. Planned: four reconnaissance agents, one hunter wave, two critics, and two verifiers per candidate. Spent: zero delegated agents.

**Execution.** Sandboxed source-and-local-only policy, and in practice source only. By task rule, the tests were read, not run.

**Independence gap.** The delegation tool (Task) and eval kernel are denied by policy on this seat. Every phase ran in the parent (`parent-hunter`), and no Phase 3 or Phase 5 verifier ran.

**Prior runs.** I carried run-8 (U280 at e8c85c2d: 43 units, 0 findings, 1 unvalidated candidate).
- **Linear-time units.** The two first swept in run-5 (U234b) are re-opened and re-checked.
- **Brief-check units.** Run-8's four are out of scope, because U280 is not merged.
- **Candidate.** It keeps its fingerprint on unchanged source.

**Deferred.** Nothing.

## 2. Security posture

**The U234c change.** No candidate survives. It keeps the guard's strength and changes only how time is measured.

- **CPU time.** `LinearGrowth` times the process's CPU time (`time.process_time_ns`, `tests/unit/test_validate_agent_assets.py:166`), the least of five interleaved runs of each workload (`:185-214`). Descheduled slices on a shared runner no longer count.
- **Calibration.** The reference's round count comes from least-of-three CPU times of the scan and of one reference round (`:200-202`). It is constant over both sizes, so the reference's growth stays the size factor.
- **Unchanged judgement.** The judged ratio (`:170`) and its bound of 3 (`:2895`, `:3030`, asserted at `:2935-2940` and `:3056-3057`) are unchanged. A linear scan judges about 1 and a quadratic one about 8, so a quadratic regression of the secret scan still fails.
- **The cap.** It is still 20 s, now of CPU time (`:2896`, `:3031`, asserted at `:2933-2934` and `:3049`). Correctness assertions are unchanged.
- **Fixtures.** The planted tokens are concatenated dummies (`:3028`), written under a `mkdtemp` root that `module.ROOT` points at (`:218-229`, `:538-542`). U234c adds no file write, subprocess, network call or environment read.

**The carried candidate** is unchanged: `decisions.tsv:509` is on main (section 5a).

## 3. Confirmed findings

None. The carried candidate is unvalidated (section 1).

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

## 5a. Unvalidated candidate (not a finding)

**`records-sync/redaction/account-identity-residue-in-published-row`**, carried since run-2. Proposed verdict confirmed, proposed severity low. Neither has been independently verified.

- **Where.** `.orchestration/orchestrate/regime-cutover/decisions.tsv:509` at 90db4721. The row is on origin/main since records sync 45 (aabee966, #694). It quotes `claude auth status` output and keeps four account fields:
  - an email address whose redact-word part was replaced by `<redacted>`, leaving a local part that is a component of the multi-part redact word on line 5 of `redact-words.txt`, and the employer's domain;
  - the organisation UUID;
  - the organisation name;
  - the subscription type.

  None of these values is quoted in this report.
- **Lower-trust principal.** Any reader of the origin repository's main branch. Repository visibility is not source-visible, and this run had no network.
- **Intended control.** `redact-words.txt` plus `--scan-identifiers` (`scripts/orchestrator/records-sync.sh:30-33`, `:425-431`).
- **Why it passed.** None of these is changed by U234c:
  - `--scan-identifiers` tests only secret patterns, home paths, and literal redact words bounded by non-alphanumerics (`scripts/validate-agent-assets.py:2434-2440`, `:2443-2465`).
  - The hand pass (`decisions.tsv:521`) replaced only the listed words.
  - Neither the masker nor CI's scan (`.github/workflows/agent-assets.yml:69-70`) has an email or account rule.
  - The sync contract excludes content review (`records-sync.sh:511-515`).
- **Impact.** The operator's account identity and their enterprise organisation's identifier and name are disclosed on the default branch. They are not credentials: there is no account access.
- **Smallest fix.**
  1. Reduce the store row to "`claude auth status` exit 0, logged in" and publish it with the next sync. The row's history stays in aabee966, so removing it from history needs the owner's decision.
  2. Add an email rule (allowlisting `noreply@anthropic.com` and GitHub noreply) and `claude auth status` account-key rules (`orgId`, `orgName`, the email key) to `identifier_reasons` in `scripts/validate-agent-assets.py`.
  3. Treat each component of a multi-part redact word as a word, or have the owner list the components. Add a regression copy.
- **To verify independently.** Re-read `decisions.tsv:509` and `:521` at 90db4721, and confirm that `identifier_reasons` has no email or account rule. Owner-observed: the repository's visibility.

## 6. Hardening notes and positive patterns

These are not findings.

1. **The cap no longer counts a blocking wait.** The 20 s cap is now CPU time (`:166`, `:2933-2934`, `:3049`). The cap was always checked after the call returned, so it never stopped a true hang; the CI job's timeout does. A wall-clock cap beside the CPU judgement would keep a slow-but-sleeping regression visible.
2. **The fixture write is still timed** (run-5's note). The one-finding-per-line test writes its fixture inside the timed scan (`:3036-3042`). Under CPU time only the write's CPU share dilutes a quadratic report: smaller than before, but not zero. Timing only `validate_no_obvious_secrets` would remove it.
3. **Carried records-sync notes.** Hand redaction passes are not a control (`decisions.tsv:521`, `:525`), and the masker truncated the published credential handout's `read -s` line.

### Positive patterns

- The measurement rule is stated as data (clock, repeats) and printed in the failure message, together with the chosen rounds and the reference-to-scan ratio.
- The calibration is a least-of-three, not a single sample.
- The lineage of every earlier form's failure on healthy code is recorded in the docstrings.

## 7. Coverage summary

From `coverage-ledger.json` (43 units):

| Status | Units |
|---|---|
| covered | 2 |
| candidate | 1 |
| blocked | 0 |
| deferred | 0 |
| out_of_scope | 40 |

- **Covered (2):** the linear-time guard and the planted fixtures, re-opened and owned by `parent-hunter`.
- **Candidate (1):** the carried identity unit.
- **Out of scope (40):** every other top-level directory and unchanged path, run-8's brief-check units, the merged late-holder unit and the earlier carried units.

**Critic results.** Neither the post-wave critic nor the final-clean critic found work. Both ran in the parent, so this is a single-reviewer coverage statement.
