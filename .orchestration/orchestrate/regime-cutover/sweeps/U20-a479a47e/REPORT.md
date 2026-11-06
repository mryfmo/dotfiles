# Security audit report: dotfiles at a479a47e9fe86bd6c45a16d66def1e821d74b842

## 1. Run, scope and limits

**Candidate validation is incomplete, so this is a partial pass.** The candidate carried from run-2 still stands at this head, and no independent verifier could run.

| Fingerprint | Coverage unit | State |
|---|---|---|
| `records-sync/redaction/account-identity-residue-in-published-row` | `.orchestration/orchestrate/regime-cutover#records-sync-43-copies` × `…/redact-words.txt#redact-word-and-identity-scan` | `candidate`, unvalidated (carried) |

Per the skill's rule, an unvalidated candidate is not a finding and is not in `findings.json`, and the run is `incomplete`. Section 5a describes it so the owner can act on it.

**Profile and scope.** The profile is `standard`, scoped to the U20 change: records sync 44, commit a479a47e on origin/main cf68daf6. The commit changes 226 masked copies under `.orchestration/orchestrate/regime-cutover/`: 216 added and 10 modified. Sync 44 rebuilds sync 43 on the same base and adds:
- the U263 and U264 briefs;
- this seat's run-2 sweep files (`sweeps/U20-4631bdfc`);
- the sync-43 verdict (`verdicts/U20-4631bdfc.md`);
- row edits, including withdrawing the API-key step of `handouts/m21-one-turn-rerun.md` and hardening the g7 probe in `tests/dsh-login-route.tsv`.

Every other path is carried `out_of_scope`.

**Brief discrepancies.** The brief is U263's template, so the same mismatches apply:
- The base is cf68daf6, not d1ecd495.
- The `c4195463` diff named in CONTEXT is stale.
- The hunt questions are U240's, and that plugin is absent at this head.
- The carry set `sweeps/U20-2256b56c` does not exist.

I followed the GOAL and carried this seat's run-2.

**Source ref.** The checkout was clean at the head both before and after the run.

**Budget.** None was set. Planned: four reconnaissance agents, one hunter wave, two critics, and two verifiers per candidate. Spent: zero delegated agents.

**Execution.** Sandboxed source-and-local-only policy. No target code ran. The parent's scan read git blobs and printed counts and locations, never matched values (`agents/parent-hunter/scratch/scan-sync.cjs`).

**Independence gap.** The delegation tool (Task) and eval kernel are denied by policy on this seat. Every phase ran in the parent (`parent-hunter`), and no Phase 3 or Phase 5 verifier ran.

**Prior runs.** I carried run-2 (records sync 43 at 4631bdfc: 40 units, 0 findings, 1 unvalidated candidate).
- **Store units.** Its five are re-checked here as changed source.
- **Candidate.** It keeps its fingerprint, because its source row is unchanged.
- **Out of scope.** Its 35 out-of-scope units carry over.

**Deferred.** Nothing.

## 2. Security posture

The lever's structural controls hold:
- all 226 paths are under the store, as regular non-executable text;
- no symlinks or binaries;
- `redact-words.txt` is not published.

No credential value is published. The scan found no token, key, private key, bearer value, JWT, secret assignment or user-home path. Sync 44 removes the one handout step that read an API key into a command's environment.

The identity gap from sync 43 is unchanged. `decisions.tsv:509` still publishes the logged-in account's identifiers past the literal redact-word scan (section 5a). The coordinator's audit of sync 43 (`verdicts/U20-4631bdfc.md`) judged record format and did not address it.

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

**`records-sync/redaction/account-identity-residue-in-published-row`**, carried from run-2. Proposed verdict confirmed, proposed severity low. Neither has been independently verified.

- **Where.** `.orchestration/orchestrate/regime-cutover/decisions.tsv:509` at a479a47e. The row is byte-identical to sync 43's. It quotes `claude auth status` output and keeps four account fields:
  - an email address whose redact-word part was replaced by `<redacted>`, leaving a local part that is a component of the multi-part redact word on line 5 of `redact-words.txt`, and the employer's domain;
  - the organisation UUID;
  - the organisation name;
  - the subscription type.

  Of the email-shaped strings in the 226 blobs, it is the only personal address. The others are `noreply@anthropic.com` co-author lines and one `git@github.com` SSH remote form (`preferences.md:21`). None of these values is quoted in this report.
- **Lower-trust principal.** Any reader of the origin repository's branches. The lever pushed both `records/sync-43` and `records/sync-44`, and merging either would put the row on main. Whether the repository is public is not source-visible, and this run had no network.
- **Intended control.** The redaction policy: `redact-words.txt` plus `--scan-identifiers` (`scripts/orchestrator/records-sync.sh:30-33`, `:425-431`).
- **Why it passes.** None of these is changed at this head:
  - `--scan-identifiers` tests only secret patterns, home paths, and literal redact words bounded by non-alphanumerics (`scripts/validate-agent-assets.py:2494-2500`, `:2503-2525`).
  - The hand pass (`decisions.tsv:521`) replaced only the listed words.
  - Neither the masker nor CI's scan (`.github/workflows/agent-assets.yml:69-70`) has an email or account rule.
  - The sync contract excludes content review (`records-sync.sh:511-515`).
- **Impact.** The operator's account identity and their enterprise organisation's identifier and name are disclosed. They are not credentials: there is no account access. The organisation UUID and name are absent from origin/main.
- **Related.** The employer's name also appears in the program goal text (`decisions.tsv:473`; `handoff/08-purpose-and-goal.md:5`), apparently as an intentional product name.
- **Smallest fix.**
  1. Reduce the store row to the facts the decision needs ("`claude auth status` exit 0, logged in") and re-run the sync.
  2. Close or replace both pushed branches and their pull requests.
  3. Add an email rule (allowlisting `noreply@anthropic.com` and GitHub noreply) and `claude auth status` account-key rules (`orgId`, `orgName`, the email key) to `identifier_reasons` in `scripts/validate-agent-assets.py`.
  4. Treat each component of a multi-part redact word as a word, or have the owner list the components. Add a regression copy.
- **To verify independently.** Re-read `decisions.tsv:509` and `:521` at a479a47e. Confirm that origin/main holds neither the organisation UUID nor the name. Confirm that `identifier_reasons` has no email or account rule. Owner-observed: the origin repository's visibility.

## 6. Hardening and integrity notes

These are not findings.

1. **Corrupted repository paths (integrity), unchanged since sync 43.** `home/dot_mise/config.toml` paths are still rewritten as `…~/config.toml` in `briefs/U116-mise-lock-evaluation.md:15`, `verdicts/U141-8acca573.md:60` and `verdicts/U141-cfbcfbfd.md:63`, and also, per run-2, in `verdicts/U116-31be35ac.md`. All are files already on main.
2. **A hand redaction pass is not a control.** `decisions.tsv:521` records one. A store-side check with the fix's rules, run before the sync, would catch its residue.
3. **macOS per-user temp paths.** Unchanged, and already on main (`tests/dsh-login-route.tsv:40-41`, `ledger.tsv`).
4. **Token metadata.** `decisions.tsv:471` keeps a token file's path, mode, size and mtime, with a rotation recommendation and no value.
5. **The sync-43 audit's blocking items were not re-assessed.** They are the `decisions.tsv` closing-form row and the glued `units.tsv` rows. They concern record format for `rounds-check.py` and `pr-merge.sh`, not a security boundary.

### Positive patterns

- Sync 44 withdraws the handout step that read an API key, in line with the login-only rule.
- It makes the g7 listener probe fail when `pgrep` finds no gateway child.
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

The five in-scope store units are carried from run-2 and re-checked here as changed source:
- **Covered (4):** secrets in the copies; copy-set paths and modes; home and host paths; records as CI and agent inputs.
- **Candidate (1):** identity residue.

The 35 out-of-scope units are every other top-level directory, the unchanged `.orchestration` records, the root files, and the carried U240 and earlier units.

**Critic results.** Neither the post-wave critic nor the final-clean critic found work. Both ran in the parent, so this is a single-reviewer coverage statement.
