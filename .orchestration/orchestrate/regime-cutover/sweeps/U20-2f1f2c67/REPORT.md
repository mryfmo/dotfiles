# Security audit report: dotfiles at 2f1f2c6772ec56fb7eb7a1574411cb0d166d6e48

## 1. Run, scope and limits

**Candidate validation is incomplete, so this is a partial pass.** The candidate carried since run-2 still stands at this head, and no independent verifier could run.

| Fingerprint | Coverage unit | State |
|---|---|---|
| `records-sync/redaction/account-identity-residue-in-published-row` | `.orchestration/orchestrate/regime-cutover#records-sync-43-copies` × `…/redact-words.txt#redact-word-and-identity-scan` | `candidate`, unvalidated (carried) |

Per the skill's rule, an unvalidated candidate is not a finding and is not in `findings.json`, and the run is `incomplete`. Section 5a describes it for the owner.

**Profile and scope.** The profile is `standard`, scoped to the U20 change: records sync 45, commit 2f1f2c67. The commit changes 250 masked copies under `.orchestration/orchestrate/regime-cutover/`: 243 added and 7 modified. Its base is origin/main d2389a05, which has merged U224 (15d37d0e) and U226 (d2389a05) since cf68daf6. Each has its own store sweep, and neither changes a control of the publish boundary:
- The lever, the workflows and `AGENTS.md` are unchanged.
- `scripts/validate-agent-assets.py` loses only `validate_understand_anything_assets`, so its scanner lines shift by −60.

Every other path is carried `out_of_scope`.

**Brief discrepancies.** The brief is U263's template:
- The base is d2389a05, not d1ecd495.
- The `c4195463` diff named in CONTEXT is stale.
- The hunt questions are U240's, and that plugin is absent here.
- The carry set `sweeps/U20-2256b56c` does not exist.

I followed the GOAL and carried this seat's run-3.

**Source ref.** The checkout was clean at the head both before and after the run.

**Budget.** None was set. Planned: four reconnaissance agents, one hunter wave, two critics, and two verifiers per candidate. Spent: zero delegated agents.

**Execution.** Sandboxed source-and-local-only policy. No target code ran. The parent's scan read git blobs and printed counts and locations only (`agents/parent-hunter/scratch/scan-sync.cjs`).

**Independence gap.** The delegation tool (Task) and eval kernel are denied by policy on this seat. Every phase ran in the parent (`parent-hunter`), and no Phase 3 or Phase 5 verifier ran.

**Prior runs.** I carried run-3 (records sync 44 at a479a47e: 40 units, 0 findings, 1 unvalidated candidate).
- **Store units.** Its five are re-checked here as changed source.
- **Candidate.** It keeps its fingerprint, because its source row is unchanged.
- **Out of scope.** Its 35 out-of-scope units carry over. Those the new base touches note U224 and U226.

**Deferred.** Nothing.

## 2. Security posture

The lever's structural controls hold:
- all 250 paths are under the store, as regular non-executable text;
- no symlinks or binaries;
- `redact-words.txt` is not published.

No credential value is published. The scan found no token, key, private key, bearer value, JWT, secret assignment or user-home path. Two changes improve on sync 44:
- The path corruption of syncs 43 and 44 is repaired.
- The seat-identity handout now reads the GitHub token from the terminal with `read -s` instead of a `printf` argument.

The identity gap is unchanged. `decisions.tsv:509` still publishes the logged-in account's identifiers (section 5a). Neither the coordinator's records nor the sync-44 audit (`verdicts/U20-a479a47e.md`: correct, 5 filed) address it.

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

- **Where.** `.orchestration/orchestrate/regime-cutover/decisions.tsv:509` at 2f1f2c67. The row is byte-identical in syncs 43, 44 and 45. It quotes `claude auth status` output and keeps four account fields:
  - an email address whose redact-word part was replaced by `<redacted>`, leaving a local part that is a component of the multi-part redact word on line 5 of `redact-words.txt`, and the employer's domain;
  - the organisation UUID;
  - the organisation name;
  - the subscription type.

  It is the only personal address among the email-shaped strings in the 250 blobs. The others are `noreply@anthropic.com` co-author lines and two `git@github.com` SSH remote forms. None of these values is quoted in this report.
- **Lower-trust principal.** Any reader of the origin repository's branches. The lever pushed `records/sync-43`, `-44` and `-45`, and merging any of them would put the row on main. Repository visibility is not source-visible, and this run had no network.
- **Intended control.** `redact-words.txt` plus `--scan-identifiers` (`scripts/orchestrator/records-sync.sh:30-33`, `:425-431`).
- **Why it passes.** None of these is changed by the new base:
  - `--scan-identifiers` tests only secret patterns, home paths, and literal redact words bounded by non-alphanumerics (`scripts/validate-agent-assets.py:2434-2440`, `:2443-2465`).
  - The hand pass (`decisions.tsv:521`) replaced only the listed words.
  - Neither the masker nor CI's scan (`.github/workflows/agent-assets.yml:69-70`) has an email or account rule.
  - The sync contract excludes content review (`records-sync.sh:511-515`).
- **Impact.** The operator's account identity and their enterprise organisation's identifier and name are disclosed. They are not credentials: there is no account access. The organisation UUID and name are absent from origin/main.
- **Related.** The employer's name also appears in the program goal text (`decisions.tsv:473`; `handoff/08-purpose-and-goal.md:5`), apparently as an intentional product name.
- **Smallest fix.**
  1. Reduce the store row to "`claude auth status` exit 0, logged in" and re-run the sync.
  2. Close or replace the pushed sync branches and their pull requests.
  3. Add an email rule (allowlisting `noreply@anthropic.com` and GitHub noreply) and `claude auth status` account-key rules (`orgId`, `orgName`, the email key) to `identifier_reasons` in `scripts/validate-agent-assets.py`.
  4. Treat each component of a multi-part redact word as a word, or have the owner list the components. Add a regression copy.
- **To verify independently.** Re-read `decisions.tsv:509` and `:521` at 2f1f2c67. Confirm that origin/main d2389a05 holds neither the organisation UUID nor the name. Confirm that `identifier_reasons` has no email or account rule. Owner-observed: the repository's visibility.

## 6. Hardening and integrity notes

These are not findings.

1. **A masker false positive truncates a credential procedure (integrity, new).** `handouts/operator-steps-dsh-route-and-seat-identity.md:19` is a safe `read -r -s` step, and the store's line holds no token-shaped string. The generic secret-assignment rule still replaced the rest of the published line with `<redacted:secret-pattern>`, so the published command is cut short. That fails closed and nothing leaks. Rephrasing the prompt text, or an allowlist row for that line, would keep the published procedure whole.
2. **The path corruption is repaired.** The U116 brief and the two U141 verdicts read `home/dot_mise/config.toml` again. `decisions.tsv:525` records the cause: a hand home-path pass matched the repository segment. It quotes the corrupted forms as text.
3. **A hand redaction pass is not a control** (carried). Hand passes (`decisions.tsv:521`, `:525`) both leave residue and damage it. A store-side check with the fix's rules, run before the sync, would catch both.
4. **macOS per-user temp paths and token metadata** (carried). Both are unchanged and hold no secret (`tests/dsh-login-route.tsv:40-41`; `decisions.tsv:471`).

### Positive patterns

- The token handout now uses a silent terminal read, a 0600 file and `unset`.
- The path corruption was repaired from main's copies by context.
- The lever's isolated build, scanned-bytes commit, change-set equality and withheld scan output are unchanged.

## 7. Coverage summary

From `coverage-ledger.json` (40 units):

| Status | Units |
|---|---|
| covered | 4 |
| candidate | 1 |
| blocked | 0 |
| deferred | 0 |
| out_of_scope | 35 |

The five in-scope store units are carried from run-3 and re-checked here as changed source:
- **Covered (4):** secrets in the copies; copy-set paths and modes; home and host paths; records as CI and agent inputs.
- **Candidate (1):** identity residue.

The 35 out-of-scope units are every other top-level directory, the unchanged `.orchestration` records, the root files, and the carried U240 and earlier units. The base's U224 and U226 changes are swept in their own store records.

**Critic results.** Neither the post-wave critic nor the final-clean critic found work. Both ran in the parent, so this is a single-reviewer coverage statement.
