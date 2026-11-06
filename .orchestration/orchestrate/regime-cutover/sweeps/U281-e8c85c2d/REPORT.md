# Security audit report: dotfiles at e8c85c2d56791e0cf47ba7e95d9e35329f369b02

## 1. Run, scope and limits

**Candidate validation is incomplete, so this is a partial pass.** The carried candidate is still on origin/main, and no independent verifier could run.

| Fingerprint | Coverage unit | State |
|---|---|---|
| `records-sync/redaction/account-identity-residue-in-published-row` | `.orchestration/orchestrate/regime-cutover#records-sync-43-copies` × `…/redact-words.txt#redact-word-and-identity-scan` | `candidate`, unvalidated (carried; on main since aabee966) |

Per the skill's rule, an unvalidated candidate is not a finding and is not in `findings.json`, and the run is `incomplete`. Section 5a describes it for the owner.

**Profile and scope.** The profile is `standard`, scoped to the U280 change 4525d339..e8c85c2d (branch `fix/brief-check-records-gate`), six files:
- `scripts/orchestrator/brief-check.py`;
- its deployed copy and its two pins;
- `tests/unit/test_brief_check.py`;
- one README sentence.

The scope also includes the carried candidate, because this base holds its row. Every other path is carried `out_of_scope`.

**Brief discrepancies.** The brief gives the base as 8f31cf5c and calls the change "no production code".
- The merge base is 4525d339 (U234b merged).
- `brief-check.py` is a pinned lever that `pr-audit.sh` runs as the brief gate, so I swept it as the boundary.

**Source ref.** The checkout was clean at the head both before and after the run.

**Budget.** None was set. Planned: four reconnaissance agents, one hunter wave, two critics, and two verifiers per candidate. Spent: zero delegated agents.

**Execution.** Sandboxed source-and-local-only policy, and in practice source only. By task rule, the tests were read, not run.

**Independence gap.** The delegation tool (Task) and eval kernel are denied by policy on this seat. Every phase ran in the parent (`parent-hunter`), and no Phase 3 or Phase 5 verifier ran.

**Prior runs.** I carried run-7 (U241c at 44003e57: 43 units, 0 findings, 1 unvalidated candidate).
- **Brief-check units.** Four have been held out of scope since the U249 sweep: gate terms, SCOPE paths, deployed copy and pin, and tests and README. They are re-opened here.
- **Late-holder unit.** Out of scope, because U241b/c is not merged.
- **Candidate.** It keeps its fingerprint on unchanged source.

**Deferred.** Nothing.

## 2. Security posture

**The U280 change.** No candidate survives.

- **The new row.** `("test", "records-check", RECORDS_CHECK)` accepts `python3 -I <path>/check-<name>.py` as a test gate (`scripts/orchestrator/brief-check.py:252-259`).
  - The pattern is case-sensitive inside the case-insensitive alternation, so `-i` (the interactive interpreter), a missing `-I`, `python -I`, a non-`check-*.py` name and a `check-*/` directory are refused. The new tests cover each.
  - `word_pattern` (`:273-289`) takes a compiled term as written, and only the gate table uses one.
- **Who trusts the gate.**
  - `pr-audit.sh` runs the checkout's `brief-check.py` only to refuse an audit round for a failing brief (`scripts/orchestrator/pr-audit.sh:965-981`).
  - A merge still needs a `correct` verdict, green CI and the sweep row (`AGENTS.md:40-43`, `:71`).
  - CI runs the unit tests for any diff that is not records-only, whatever the brief names (`.github/workflows/test.yaml:97-146`).
  - So a brief that names a weak test gate weakens the coordinator's own check, not the merge gate.
- **Deployed copy and pins.** The copy is byte-identical to the script, both are 100755, and its sha256 equals the `agent-config.yaml` pin (`:883`) and the generated-outputs entry (`:393-397`).
- **Tests.** They write briefs only into the module's `TemporaryDirectory` scratch (`tests/unit/test_brief_check.py:134`, `:142-145`).

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

- **Where.** `.orchestration/orchestrate/regime-cutover/decisions.tsv:509` at e8c85c2d. The row is on origin/main since records sync 45 (aabee966, #694). It quotes `claude auth status` output and keeps four account fields:
  - an email address whose redact-word part was replaced by `<redacted>`, leaving a local part that is a component of the multi-part redact word on line 5 of `redact-words.txt`, and the employer's domain;
  - the organisation UUID;
  - the organisation name;
  - the subscription type.

  None of these values is quoted in this report.
- **Lower-trust principal.** Any reader of the origin repository's main branch. Repository visibility is not source-visible, and this run had no network.
- **Intended control.** `redact-words.txt` plus `--scan-identifiers` (`scripts/orchestrator/records-sync.sh:30-33`, `:425-431`).
- **Why it passed.** None of these is changed by U280:
  - `--scan-identifiers` tests only secret patterns, home paths, and literal redact words bounded by non-alphanumerics (`scripts/validate-agent-assets.py:2434-2440`, `:2443-2465`).
  - The hand pass (`decisions.tsv:521`) replaced only the listed words.
  - Neither the masker nor CI's scan (`.github/workflows/agent-assets.yml:69-70`) has an email or account rule.
  - The sync contract excludes content review (`records-sync.sh:511-515`).
- **Impact.** The operator's account identity and their enterprise organisation's identifier and name are disclosed on the default branch. They are not credentials: there is no account access.
- **Smallest fix.**
  1. Reduce the store row to "`claude auth status` exit 0, logged in" and publish it with the next sync. The row's history stays in aabee966, so removing it from history needs the owner's decision.
  2. Add an email rule (allowlisting `noreply@anthropic.com` and GitHub noreply) and `claude auth status` account-key rules (`orgId`, `orgName`, the email key) to `identifier_reasons` in `scripts/validate-agent-assets.py`.
  3. Treat each component of a multi-part redact word as a word, or have the owner list the components. Add a regression copy.
- **To verify independently.** Re-read `decisions.tsv:509` and `:521` at e8c85c2d, and confirm that `identifier_reasons` has no email or account rule. Owner-observed: the repository's visibility.

## 6. Hardening notes and positive patterns

These are not findings.

1. **The records-check row isn't limited to records briefs.** `gates()` accepts any test-class term (`scripts/orchestrator/brief-check.py:425-434`), and `judge` calls it for every brief whose SCOPE names a repository path (`:463-464`). A code brief can therefore meet the test class with an arbitrary `python3 -I …/check-*.py`, although the row's comment (`:243-251`) and the README (`scripts/orchestrator/README.md:118`) present it as a records brief's gate.
   - **Fix.** Accept that row only when every SCOPE repository path is under the store (`.orchestration/...`) or is the branch ref.
   - **Missing test.** None of the tests covers a code brief that names only a check script; one would pin the fix.
   - **Quirk to account for.** A backticked `origin/main` counts as a repository path for `in_repository` (`:416-422`), and that is how records briefs reach the gate check at all.
   - **Why this isn't a finding.** CI still runs the unit tests on code diffs, so the effect is confined to the coordinator's own pre-audit check.
2. **Carried records-sync notes.** Hand redaction passes are not a control (`decisions.tsv:521`, `:525`), and the masker truncated the published credential handout's `read -s` line.

### Positive patterns

- The new gate form is strict: case-sensitive `-I`, a named `check-*.py` file, and a word boundary on `.py`.
- Both accepted and refused forms are tested.
- The deployed copy and both pins move together.

## 7. Coverage summary

From `coverage-ledger.json` (43 units):

| Status | Units |
|---|---|
| covered | 4 |
| candidate | 1 |
| blocked | 0 |
| deferred | 0 |
| out_of_scope | 38 |

- **Covered (4):** the brief-check units, re-opened and owned by `parent-hunter` with source checks: ACCEPTANCE gate terms; SCOPE repository paths; deployed copy and pin; tests and README.
- **Candidate (1):** the carried identity unit.
- **Out of scope (38):** every other top-level directory and unchanged path, the late-holder unit, the malformed-brief exit-code unit (unchanged by U280), and the earlier carried units.

**Critic results.** Neither the post-wave critic nor the final-clean critic found work. Both ran in the parent, so this is a single-reviewer coverage statement.
