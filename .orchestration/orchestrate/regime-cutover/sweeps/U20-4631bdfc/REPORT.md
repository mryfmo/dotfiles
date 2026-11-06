# Security audit report: dotfiles at 4631bdfcc83d120653bb9aac8fb6ad2556eac57b

## 1. Run, scope and limits

**Candidate validation is incomplete, so this is a partial pass.** One candidate survived the hunt, and no independent verifier could run.

| Fingerprint | Coverage unit | State |
|---|---|---|
| `records-sync/redaction/account-identity-residue-in-published-row` | `.orchestration/orchestrate/regime-cutover#records-sync-43-copies` × `…/redact-words.txt#redact-word-and-identity-scan` | `candidate`, unvalidated |

Per the skill's rule, an unvalidated candidate is not a finding and is not in `findings.json`, and the run is `incomplete`. The candidate is described in section 5a so the owner can act on it.

**Profile and scope.** The profile is `standard`, scoped to the U20 change: records sync 43, commit 4631bdfc on origin/main cf68daf6. The commit changes 214 masked copies under `.orchestration/orchestrate/regime-cutover/`: 204 added and 10 modified. Every other path is carried `out_of_scope`.

**Brief discrepancies.** I followed the GOAL's description of the change. Where the brief disagrees with this head:
- The branch's base is cf68daf6, not d1ecd495. cf68daf6 adds U241 and U254 since d1ecd495, and each has its own store sweep.
- The `c4195463` diff named in CONTEXT lists more than one file.
- The hunt questions are U240's. The omp-gateway plugin is absent here, so they have no surface; the hunt targeted the store-to-repository publish boundary instead.
- The carry set `sweeps/U20-2256b56c` does not exist. This seat's run-1 is carried instead.

**Source ref.** The checkout was clean at the head both before and after the run.

**Budget.** None was set. Planned: four reconnaissance agents, one hunter wave, two critics, and two verifiers per candidate. Spent: zero delegated agents.

**Execution.** Sandboxed source-and-local-only policy. No target code ran. The parent's own script read git blobs and printed counts and locations, never matched values (`agents/parent-hunter/scratch/scan-sync.cjs`).

**Independence gap.** The delegation tool (Task) and eval kernel are denied by policy on this seat. Reconnaissance, hunting and both critics ran in the parent, and no Phase 3 or Phase 5 verifier ran.

**Prior runs.** I carried this seat's run-1 (6bc0c2cb, 35 units, 0 findings). Its U240 units are out of scope here, because the plugin is absent. No prior record of any verdict exists, so there are no carried confirmations or revalidations.

**Deferred.** Nothing.

## 2. Security posture

The lever's structural controls hold for this change:
- every path is under the store;
- every file is regular, non-executable text;
- no symlinks;
- the redact list is not published;
- the change set equals the copy set.

No credential value is published. The parent's scans found no token, key, private key, bearer value, JWT or secret assignment, and no user-home path (a Users or home root followed by a user name).

The gap is identity rather than secrets. The scan's redact-word test is literal, and nothing tests for emails or account fields. So one new row publishes the logged-in account's identifiers, which the hand redaction pass only partly removed (section 5a).

## 3. Confirmed findings

None. The one candidate is unvalidated (section 1).

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

**`records-sync/redaction/account-identity-residue-in-published-row`.** Proposed verdict confirmed, proposed severity low. Neither has been independently verified.

- **Where.** `.orchestration/orchestrate/regime-cutover/decisions.tsv:509` at 4631bdfc. The row is new in this sync and byte-identical to the store's row. It quotes `claude auth status` output, and the published text keeps four account fields:
  - an email address whose redact-word part was replaced by `<redacted>`, leaving a local part that is a component of the multi-part redact word on line 5 of `redact-words.txt`, and the employer's domain;
  - the organisation UUID;
  - the organisation name;
  - the subscription type.

  None of these is quoted in this report.
- **Lower-trust principal.** Any reader of the origin repository's branches. The lever has already pushed `records/sync-43`, and merging it would put the row on main. Whether the repository is public is not source-visible, and this run had no network.
- **Intended control.** The redaction policy: `redact-words.txt` ("Words records-sync.sh refuses to publish") plus `--scan-identifiers` (`records-sync.sh:30-33`, `:425-431`).
- **Why it passes.**
  - `--scan-identifiers` tests only secret patterns, home paths, and each literal redact word bounded by non-alphanumerics (`scripts/validate-agent-assets.py:2494-2500`, `:2503-2525`).
  - The hand pass (`decisions.tsv:521`) replaced exactly the listed words, so the remaining name fragment, the domain, the UUID and the organisation name match nothing.
  - Neither the masker nor CI's scan on the pull request (`.github/workflows/agent-assets.yml:69-70`) has an email or account-identity rule.
  - The sync contract excludes content review (`records-sync.sh:511-515`).
- **Impact.** The operator's account identity and their enterprise organisation's identifier and name are disclosed. These are not credentials: there is no account access. The organisation UUID and name appear nowhere on origin/main. Commit author emails there already carry the same domain with a different local part.
- **Same sync, related.** The employer's name is newly published in the program goal text (`decisions.tsv:473`; `handoff/08-purpose-and-goal.md:5`). It reads as an intentional product name.
- **Smallest fix.**
  1. Rewrite `decisions.tsv:509` in the store so it keeps only the facts the decision needs ("`claude auth status` exit 0, logged in"), drop the account fields, and re-run the sync.
  2. Close or replace the `records/sync-43` branch and pull request, because the bytes are already on the remote.
  3. In `scripts/validate-agent-assets.py`'s `identifier_reasons`, flag email addresses outside an allowlist (`noreply@anthropic.com`, GitHub noreply) and the `claude auth status` account keys (`orgId`, `orgName` and the email key).
  4. Treat each component of a multi-part redact word as a word, or have the owner list the components. Add a regression copy that holds such a row.
- **To verify independently.** Re-read `decisions.tsv:509` and `:521` at 4631bdfc. Confirm that origin/main holds neither the organisation UUID nor the organisation name. Confirm that `identifier_reasons` has no email or account rule. Owner-observed: the origin repository's visibility.

## 6. Hardening and integrity notes

These are not findings.

1. **Masking corrupted published records (integrity).** The sync rewrote repository paths `…/home/dot_mise/config.toml` and `${BASH_SOURCE[0]%/*}/../home/dot_mise/config.toml` as `…~/config.toml`, in four files already on main:
   - `briefs/U116-mise-lock-evaluation.md:15`, where the store's copy differs, so the rewrite happened in masking;
   - `verdicts/U116-31be35ac.md`, `verdicts/U141-8acca573.md` and `verdicts/U141-cfbcfbfd.md`, where the store's copies already carry it, so it came from the hand pass of `decisions.tsv:521`.

   `home/dot_mise` exists on main. A home-path mask should not touch `<repo>/home/<entry>` paths.
2. **A hand redaction pass is not a control.** `decisions.tsv:521` records that a hand pass rewrote the store's files, and once also rewrote `redact-words.txt` itself, so that the scan would pass. The scan then proves only that the listed words are gone. A store-side check run before the sync, with the same rules the fix above adds, would catch the residue the pass leaves.
3. **macOS per-user temp paths.** `/var/folders/<2>/<id>/T/` paths appear in new rows (`tests/dsh-login-route.tsv:40-41`). The same per-user identifier is already on main (`ledger.tsv`, `handoff/m13-*.txt`). It is a machine-local path, not a home path or a secret.
4. **Token metadata.** `decisions.tsv:471` publishes a token file's path, mode, size and mtime, and records that its value was pasted into a terminal and that rotation is recommended. No value is published. The rotation note is an operator action outside this audit.
5. **Records-only pull requests.** They skip the unit tests (`.github/workflows/test.yaml:97-146`) and pass regime-ci (`regime.yml:3-8`). The committed-secret scan in `agent-assets.yml` still runs. Identity checks would have to live there or in the lever.

### Positive patterns

- The lever builds the commit in an isolated scratch repository, hashes the scanned bytes themselves, and refuses unless the change set equals the copy set.
- Its scan reports withhold every match.
- The copy set refuses symlinks, `..`, control characters and paths outside the store.
- `redact-words.txt` is never published.

## 7. Coverage summary

From `coverage-ledger.json` (40 units):

| Status | Units |
|---|---|
| covered | 4 |
| candidate | 1 |
| blocked | 0 |
| deferred | 0 |
| out_of_scope | 35 |

The five in-scope units (all `new`, owned by `parent-hunter`, with source checks over the sync's 214 blobs):
- **Covered (4):** secrets in the copies; copy-set paths and modes; home and host paths; records as CI and agent inputs.
- **Candidate (1):** identity residue.

The 35 out-of-scope units:
- the top-level directories `.claude`, `.github`, `.ua`, `docs`, `home`, `install`, `plans`, `scripts`, `tests` and `vendor`;
- the unchanged `.orchestration` records;
- the repository root files;
- run-1's 11 U240 plugin units (the plugin is absent here);
- the earlier units' carried surfaces.

**Critic results.** Neither the post-wave critic nor the final-clean critic found work. Both ran in the parent and neither was independent, so this is a single-reviewer coverage statement.
