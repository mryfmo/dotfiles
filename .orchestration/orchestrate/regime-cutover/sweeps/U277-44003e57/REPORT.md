# Security audit report: dotfiles at 44003e57ebe2eeb8a2b61a54dcbd24bb8426f7a9

## 1. Run, scope and limits

**Candidate validation is incomplete, so this is a partial pass.** The carried candidate is still on origin/main, and no independent verifier could run.

| Fingerprint | Coverage unit | State |
|---|---|---|
| `records-sync/redaction/account-identity-residue-in-published-row` | `.orchestration/orchestrate/regime-cutover#records-sync-43-copies` × `…/redact-words.txt#redact-word-and-identity-scan` | `candidate`, unvalidated (carried; on main since aabee966) |

Per the skill's rule, an unvalidated candidate is not a finding and is not in `findings.json`, and the run is `incomplete`. Section 5a describes it for the owner.

**Profile and scope.** The profile is `standard`, scoped to the U241b and U241c change 8f31cf5c..44003e57 (branch `fix/late-holder-test-handshake`). It touches one test in `tests/unit/test_trusted_exec_contract.py`. Since run-6, U241c adds the first probe's own 30 s `HOLDER_WAIT_S` (+12/−1). The harness, `tests/unit/trusted_exec_contract.py`, is unchanged. The scope also includes the carried candidate, because this base holds its row. Every other path is carried `out_of_scope`.

**Base.** The branch's base is still 8f31cf5c. origin/main has since moved to 4525d339 (U234b, #695). That head still holds the row, and it leaves the scanner unchanged.

**Source ref.** The checkout was clean at the head both before and after the run.

**Budget.** None was set. Planned: four reconnaissance agents, one hunter wave, two critics, and two verifiers per candidate. Spent: zero delegated agents.

**Execution.** Sandboxed source-and-local-only policy, and in practice source only. By task rule, the tests were read, not run.

**Independence gap.** The delegation tool (Task) and eval kernel are denied by policy on this seat. Every phase ran in the parent (`parent-hunter`), and no Phase 3 or Phase 5 verifier ran.

**Prior runs.** I carried run-6 (U241b at 2e364494: 43 units, 0 findings, 1 unvalidated candidate).
- **Late-holder unit.** Re-checked here as changed source.
- **Candidate.** It keeps its fingerprint on unchanged source.
- **Out of scope.** Its 41 out-of-scope units carry over.

**Deferred.** Nothing.

## 2. Security posture

**The U241c change.** It removes the last scheduler premise from the meta-test of the harness's holder scan:
- **The race it closes.** The scan sets its settle deadline before the first pass (`trusted_exec_contract.py:279`). The U241b handshake waits inside that pass, so with the production 0.2 s window a slow holder thread could push the first pass past the deadline.
- **Instance-only setting.** U241c sets `probe.HOLDER_WAIT_S = 30.0` (`tests/unit/test_trusted_exec_contract.py:668`) on the first probe instance only. Each `worker_root_probe()` builds a fresh `WorkerRoot` in its own temporary base (`trusted_exec_contract.py:395-408`, `:473-481`), and the scan reads `self.HOLDER_WAIT_S`.
- **Still fails closed.** A scan that stops rescanning still returns the no-holder record at once and fails, and one that stops listing the root fails on `inside`.
- **Production wait still pinned.** The second probe keeps the production 0.2 s and still requires a wait of at least 0.2 s and under 2 s (`:706-714`), so a scan that never settles fails too.

No candidate survives.

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

- **Where.** `.orchestration/orchestrate/regime-cutover/decisions.tsv:509` at 44003e57. The row is on origin/main since records sync 45 (aabee966, #694), and still there at 4525d339. It quotes `claude auth status` output and keeps four account fields:
  - an email address whose redact-word part was replaced by `<redacted>`, leaving a local part that is a component of the multi-part redact word on line 5 of `redact-words.txt`, and the employer's domain;
  - the organisation UUID;
  - the organisation name;
  - the subscription type.

  None of these values is quoted in this report.
- **Lower-trust principal.** Any reader of the origin repository's main branch. Repository visibility is not source-visible, and this run had no network.
- **Intended control.** `redact-words.txt` plus `--scan-identifiers` (`scripts/orchestrator/records-sync.sh:30-33`, `:425-431`).
- **Why it passed.** None of these is changed:
  - `--scan-identifiers` tests only secret patterns, home paths, and literal redact words bounded by non-alphanumerics (`scripts/validate-agent-assets.py:2434-2440`, `:2443-2465`, byte-identical on 4525d339).
  - The hand pass (`decisions.tsv:521`) replaced only the listed words.
  - Neither the masker nor CI's scan (`.github/workflows/agent-assets.yml:69-70`) has an email or account rule.
  - The sync contract excludes content review (`records-sync.sh:511-515`).
- **Impact.** The operator's account identity and their enterprise organisation's identifier and name are disclosed on the default branch. They are not credentials: there is no account access.
- **Smallest fix.**
  1. Reduce the store row to "`claude auth status` exit 0, logged in" and publish it with the next sync. The row's history stays in aabee966, so removing it from history needs the owner's decision.
  2. Add an email rule (allowlisting `noreply@anthropic.com` and GitHub noreply) and `claude auth status` account-key rules (`orgId`, `orgName`, the email key) to `identifier_reasons` in `scripts/validate-agent-assets.py`.
  3. Treat each component of a multi-part redact word as a word, or have the owner list the components. Add a regression copy.
- **To verify independently.** Re-read `decisions.tsv:509` and `:521` at 44003e57, and confirm that `identifier_reasons` has no email or account rule. Owner-observed: the repository's visibility.

## 6. Hardening notes and positive patterns

These are not findings.

1. **The patch is process-wide** (carried from run-6). `mock.patch.object(tec.os, "listdir", …)` replaces `os.listdir` for the whole process while `holder_scan` runs (`tests/unit/test_trusted_exec_contract.py:699-700`). It is safe at this head, but a future concurrent test would see the wrapper.
2. **A longer wait before a broken test fails.** If the holder thread dies before `placed`, the first probe now waits up to about 60 s before it fails: the hook's 30 s, then a 30 s settle. U241b waited the hook's 30 s plus 0.2 s. That costs time on a regression but hides nothing: the failure still reports.
3. **Carried records-sync notes.** Hand redaction passes are not a control (`decisions.tsv:521`, `:525`), and the masker truncated the published credential handout's `read -s` line.

### Positive patterns

- The probe's own wait is set on its instance and documented, while the production value is still measured by the second probe.
- The handshake fails closed on both events.

## 7. Coverage summary

From `coverage-ledger.json` (43 units):

| Status | Units |
|---|---|
| covered | 1 |
| candidate | 1 |
| blocked | 0 |
| deferred | 0 |
| out_of_scope | 41 |

- **Covered (1):** the late-holder handshake, re-checked here.
- **Candidate (1):** the carried identity unit.
- **Out of scope (41):** carried from run-6.

**Critic results.** Neither the post-wave critic nor the final-clean critic found work. Both ran in the parent, so this is a single-reviewer coverage statement.
