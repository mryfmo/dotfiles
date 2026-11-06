# Security audit report: dotfiles at 2e36449450c22f80ed98346bdf2f855bee1349f6

## 1. Run, scope and limits

**Candidate validation is incomplete, so this is a partial pass.** The carried candidate is now on origin/main, and no independent verifier could run.

| Fingerprint | Coverage unit | State |
|---|---|---|
| `records-sync/redaction/account-identity-residue-in-published-row` | `.orchestration/orchestrate/regime-cutover#records-sync-43-copies` × `…/redact-words.txt#redact-word-and-identity-scan` | `candidate`, unvalidated (carried; on main since aabee966) |

Per the skill's rule, an unvalidated candidate is not a finding and is not in `findings.json`, and the run is `incomplete`. Section 5a describes it for the owner.

**Profile and scope.** The profile is `standard`, scoped to the U241b change 8f31cf5c..2e364494 (branch `fix/late-holder-test-handshake`): one test in `tests/unit/test_trusted_exec_contract.py` (+34/−5). The harness it exercises, `tests/unit/trusted_exec_contract.py`, is unchanged. The scope also includes the re-verification of the carried candidate, because main now holds its row. Every other path is carried `out_of_scope`.

**Base.** origin/main moved from d2389a05 to 8f31cf5c and merged:
- U240 (#679);
- records sync 45 (#694, aabee966);
- U249 (#683);
- U227b (#686);
- U244 (#680).

Each has its own store sweep. Records sync 45's `.orchestration` tree equals the 2f1f2c67 tree run-4 swept.

**Source ref.** The checkout was clean at the head both before and after the run.

**Budget.** None was set. Planned: four reconnaissance agents, one hunter wave, two critics, and two verifiers per candidate. Spent: zero delegated agents.

**Execution.** Sandboxed source-and-local-only policy, and in practice source only. By task rule, the tests were read, not run.

**Independence gap.** The delegation tool (Task) and eval kernel are denied by policy on this seat. Every phase ran in the parent (`parent-hunter`), and no Phase 3 or Phase 5 verifier ran.

**Prior runs.** I carried run-5 (U234b at 179de4db, 42 units, 0 findings).
- **U234b units.** Out of scope, because that branch is not merged into this base.
- **Store units.** Out of scope, except the identity unit. Run-5 held it out of scope because the row wasn't on its branch; it is re-opened here.

**Deferred.** Nothing.

## 2. Security posture

**The U241b change.** It is test-only, and it strengthens the meta-test of the harness's holder scan:
- **Deterministic first pass.** The scan's first listing of the fake `/proc` root (`trusted_exec_contract.py:247`) is held until the late holder has been renamed in, so the first pass ends on an empty tree and only the rescan (`HOLDER_WAIT_S`, `:160`) can name pid 4242.
- **Fails closed.** The test asserts that record plus both handshake events, so a scan that stops rescanning fails, and so does one that stops listing the root (`tests/unit/test_trusted_exec_contract.py:690-694`).
- **Narrow wrapper.** It intercepts only that first root listing; the fd-table listings at `:255` pass through.
- **Bounded and scoped.** Every wait is bounded (30 s each, a 5 s join), and the patch is undone when the `with` block exits. No candidate survives.

**The carried candidate is no longer only on pull-request branches.** Records sync 45 has been merged, and `decisions.tsv:509` is on main (section 5a).

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

- **Where.** `.orchestration/orchestrate/regime-cutover/decisions.tsv:509` at 2e364494. The row reached origin/main through records sync 45 (aabee966, #694), and it is byte-identical to the row run-2 to run-4 checked. It quotes `claude auth status` output and keeps four account fields:
  - an email address whose redact-word part was replaced by `<redacted>`, leaving a local part that is a component of the multi-part redact word on line 5 of `redact-words.txt`, and the employer's domain;
  - the organisation UUID;
  - the organisation name;
  - the subscription type.

  None of these values is quoted in this report.
- **Lower-trust principal.** Any reader of the origin repository's main branch. Repository visibility is not source-visible, and this run had no network.
- **Intended control.** `redact-words.txt` plus `--scan-identifiers` (`scripts/orchestrator/records-sync.sh:30-33`, `:425-431`).
- **Why it passed.** None of these changed since 2f1f2c67:
  - `--scan-identifiers` tests only secret patterns, home paths, and literal redact words bounded by non-alphanumerics (`scripts/validate-agent-assets.py:2434-2440`, `:2443-2465`).
  - The hand pass (`decisions.tsv:521`) replaced only the listed words.
  - Neither the masker nor CI's scan (`.github/workflows/agent-assets.yml:69-70`) has an email or account rule.
  - The sync contract excludes content review (`records-sync.sh:511-515`).
- **Impact.** The operator's account identity and their enterprise organisation's identifier and name are disclosed on the default branch. They are not credentials: there is no account access.
- **Smallest fix, now on main.**
  1. Reduce the store row to "`claude auth status` exit 0, logged in" and publish it with the next sync. The row's history stays in aabee966, so removing it from history needs the owner's decision.
  2. Add an email rule (allowlisting `noreply@anthropic.com` and GitHub noreply) and `claude auth status` account-key rules (`orgId`, `orgName`, the email key) to `identifier_reasons` in `scripts/validate-agent-assets.py`.
  3. Treat each component of a multi-part redact word as a word, or have the owner list the components. Add a regression copy.
- **To verify independently.** Re-read `decisions.tsv:509` and `:521` at 2e364494. Confirm that aabee966's `.orchestration` tree equals 2f1f2c67's, and that `identifier_reasons` has no email or account rule. Owner-observed: the repository's visibility.

## 6. Hardening notes and positive patterns

These are not findings.

1. **The patch is process-wide.** `mock.patch.object(tec.os, "listdir", …)` replaces `os.listdir` for the whole process while `holder_scan` runs, because `tec.os` is the `os` module (`tests/unit/test_trusted_exec_contract.py:688-689`). That is safe at this head, since only the holder thread runs then and it lists no directory. Scoping the patch to the harness module's name, or passing the listing function into the scan, would keep a future concurrent test from seeing the wrapper.
2. **Carried notes.** Run-2 to run-4's records-sync notes still apply to the merged store: hand redaction passes are not a control (`decisions.tsv:521`, `:525`), and the masker truncated the published credential handout's `read -s` line.

### Positive patterns

- A scheduler-independent handshake replaces a sleep, as U241 did for the FIFO test.
- The test asserts both handshake events, so the instrumentation fails closed.
- The harness module is untouched.

## 7. Coverage summary

From `coverage-ledger.json` (43 units):

| Status | Units |
|---|---|
| covered | 1 |
| candidate | 1 |
| blocked | 0 |
| deferred | 0 |
| out_of_scope | 41 |

- **Covered (1):** the late-holder handshake (`DESKTOP-MOBILE-AND-LOCAL-IPC.md#IPC peer-authentication gaps`), new and owned by `parent-hunter`.
- **Candidate (1):** the carried identity unit, re-opened.
- **Out of scope (41):** every other top-level directory, the unchanged `tests/` paths, the root files, the other store units, run-5's U234b units and the earlier carried units.

**Critic results.** Neither the post-wave critic nor the final-clean critic found work. Both ran in the parent, so this is a single-reviewer coverage statement.
