# Security audit report: dotfiles at 6af872f66a104aaa7d0e45c7119621b1163df0bc

## 1. Run, scope and limits

**Candidate validation is incomplete, so this is a partial pass.** The carried candidate is still on origin/main, and no independent verifier could run.

| Fingerprint | Coverage unit | State |
|---|---|---|
| `records-sync/redaction/account-identity-residue-in-published-row` | `.orchestration/orchestrate/regime-cutover#records-sync-43-copies` × `…/redact-words.txt#redact-word-and-identity-scan` | `candidate`, unvalidated (carried; on main since aabee966) |

Per the skill's rule, an unvalidated candidate is not a finding and is not in `findings.json`, and the run is `incomplete`. Section 5a describes it for the owner.

**Profile and scope.** The profile is `standard`, scoped to the U280 and U280b change 4525d339..6af872f6 (branch `fix/brief-check-records-gate`): `scripts/orchestrator/brief-check.py`, its deployed copy and pins, `tests/unit/test_brief_check.py`, and one README sentence. Since run-8, U280b changes only the gate pattern's tail, the pin and the tests. The scope also includes the carried candidate, because this base holds its row. Every other path is carried `out_of_scope`.

**Brief discrepancies.** The brief gives the base as 8f31cf5c, and asks for run-7 to be carried.
- The merge base is 4525d339.
- This branch's previous sweep is run-8 (U280 at e8c85c2d), so I carried that; run-9 to run-11 swept other branches.

**Source ref.** The checkout was clean at the head both before and after the run.

**Budget.** None was set. Planned: four reconnaissance agents, one hunter wave, two critics, and two verifiers per candidate. Spent: zero delegated agents.

**Execution.** Sandboxed source-and-local-only policy. No target code ran. The parent ran its own Python on the old and new pattern literals to confirm which forms each accepts.

**Independence gap.** The delegation tool (Task) and eval kernel are denied by policy on this seat. Every phase ran in the parent (`parent-hunter`), and no Phase 3 or Phase 5 verifier ran.

**Prior runs.** I carried run-8 (43 units, 0 findings, 1 unvalidated candidate).
- **Brief-check units.** Its four are re-checked here as changed source.
- **Candidate.** It keeps its fingerprint on unchanged source.

**Deferred.** Nothing.

## 2. Security posture

**The U280b change.** No candidate survives. It tightens the records-check gate term.

- **The new tail.** `RECORDS_CHECK` (`scripts/orchestrator/brief-check.py:254`) now ends at `.py` followed by the end of the text, whitespace or a closing backtick, instead of a word boundary.
  - The old `\b` accepted `check-tables.py.bak`, `check-tables.py.sh` and `check-tables.py/run.py`, because a word boundary falls before `.` and `/`. The new tail refuses all three.
  - The parent's own run on the two pattern literals confirms this, and the new tests cover the refused and the bare forms.
  - Sentence punctuation after `.py` is now refused too, which fails closed.
- **Unchanged.** The case-sensitive `-I` and the `check-*.py` name.
- **Deployed copy and pins.** The deployed copy equals the script, and its sha256 (4a596cbe…) equals the `agent-config.yaml` pin (`:883`) and the generated-outputs entry (`:393-397`).
- **Who trusts the gate.** It is still the coordinator's own pre-audit check:
  - `pr-audit.sh` runs it only to refuse an audit round (`scripts/orchestrator/pr-audit.sh:965-981`);
  - merging needs a `correct` verdict, green CI and the sweep row (`AGENTS.md:40-43`, `:71`);
  - CI runs the unit tests on any code diff (`.github/workflows/test.yaml:97-146`).

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

- **Where.** `.orchestration/orchestrate/regime-cutover/decisions.tsv:509` at 6af872f6. The row is on origin/main since records sync 45 (aabee966, #694), and still there at 29439083. It quotes `claude auth status` output and keeps four account fields:
  - an email address whose redact-word part was replaced by `<redacted>`, leaving a local part that is a component of the multi-part redact word on line 5 of `redact-words.txt`, and the employer's domain;
  - the organisation UUID;
  - the organisation name;
  - the subscription type.

  None of these values is quoted in this report.
- **Lower-trust principal.** Any reader of the origin repository's main branch. Repository visibility is not source-visible, and this run had no network.
- **Intended control.** `redact-words.txt` plus `--scan-identifiers` (`scripts/orchestrator/records-sync.sh:30-33`, `:425-431`).
- **Why it passed.** None of these is changed by U280b:
  - `--scan-identifiers` tests only secret patterns, home paths, and literal redact words bounded by non-alphanumerics (`scripts/validate-agent-assets.py:2434-2440`, `:2443-2465`).
  - The hand pass (`decisions.tsv:521`) replaced only the listed words.
  - Neither the masker nor CI's scan (`.github/workflows/agent-assets.yml:69-70`) has an email or account rule.
  - The sync contract excludes content review (`records-sync.sh:511-515`).
- **Impact.** The operator's account identity and their enterprise organisation's identifier and name are disclosed on the default branch. They are not credentials: there is no account access.
- **Smallest fix.**
  1. Reduce the store row to "`claude auth status` exit 0, logged in" and publish it with the next sync. The row's history stays in aabee966, so removing it from history needs the owner's decision.
  2. Add an email rule (allowlisting `noreply@anthropic.com` and GitHub noreply) and `claude auth status` account-key rules (`orgId`, `orgName`, the email key) to `identifier_reasons` in `scripts/validate-agent-assets.py`.
  3. Treat each component of a multi-part redact word as a word, or have the owner list the components. Add a regression copy.
- **To verify independently.** Re-read `decisions.tsv:509` and `:521` at 6af872f6, and confirm that `identifier_reasons` has no email or account rule. Owner-observed: the repository's visibility.

## 6. Hardening notes and positive patterns

These are not findings.

1. **The records-check row isn't limited to records briefs** (carried from run-8, not addressed). `gates()` accepts any test-class term (`scripts/orchestrator/brief-check.py:427-436`) for every brief whose SCOPE names a repository path (`:465-466`). A code brief can therefore meet the test class with `python3 -I …/check-*.py`.
   - **Fix.** Accept the row only when every SCOPE repository path is under the store, or is the branch ref.
   - **Missing test.** One for a code brief that names only a check script would pin the fix. That would match the comment (`:243-253`) and the README.
2. **Sentence punctuation is refused.** A brief that writes `check-x.py,` or `check-x.py.` in prose now gets a refusal. That fails closed: the coordinator sees the reason line and rewrites the brief.
3. **Carried records-sync notes.** Hand redaction passes are not a control (`decisions.tsv:521`, `:525`), and the masker truncated the published credential handout's `read -s` line.

### Positive patterns

- A gate term that ends where a path ends.
- Tests for each refused suffix.
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

- **Covered (4):** the brief-check units, re-checked: ACCEPTANCE gate terms; SCOPE repository paths; deployed copy and pin; tests and README.
- **Candidate (1):** the carried identity unit.
- **Out of scope (38):** carried from run-8.

**Critic results.** Neither the post-wave critic nor the final-clean critic found work. Both ran in the parent, so this is a single-reviewer coverage statement.
