# Security audit report: dotfiles at fa969db6b9ba7d5d0b8fe26171760e51634765a2

## 1. Run, scope and limits

**Candidate validation is incomplete, so this is a partial pass.** The carried candidate is still on origin/main, and no independent verifier could run.

| Fingerprint | Coverage unit | State |
|---|---|---|
| `records-sync/redaction/account-identity-residue-in-published-row` | `.orchestration/orchestrate/regime-cutover#records-sync-43-copies` × `…/redact-words.txt#redact-word-and-identity-scan` | `candidate`, unvalidated (carried; on main since aabee966) |

Per the skill's rule, an unvalidated candidate is not a finding and is not in `findings.json`, and the run is `incomplete`. Section 5a describes it for the owner.

**Profile and scope.** The profile is `standard`, scoped to the U283 and U283b change a23e4541..fa969db6 (branch `fix/updater-single-function-fails-closed`), four files:
- `scripts/update-agent-assets.sh`;
- `scripts/lib/asset-manifest.sh`;
- `tests/unit/test_update_agent_assets.py`;
- `tests/unit/test_asset_manifest.py`.

Since run-10, U283b adds `mark_sync_failed`, the CompactionDB payload check, a stricter pruner, and tests for every producer and call site. The scope also includes the carried candidate, because this base holds its row. Every other path is carried `out_of_scope`.

**Base.** The brief gives the base as 8f31cf5c. The merge base is a23e4541. origin/main has since moved to 29439083 (U234c #700, U276 #698), and still holds the identity row.

**Source ref.** The checkout was clean at the head both before and after the run.

**Budget.** None was set. Planned: four reconnaissance agents, one hunter wave, two critics, and two verifiers per candidate. Spent: zero delegated agents.

**Execution.** Sandboxed source-and-local-only policy. No target code ran. The parent ran its own `jq` on a literal to confirm the pruner's select expression.

**Independence gap.** The delegation tool (Task) and eval kernel are denied by policy on this seat. Every phase ran in the parent (`parent-hunter`), and no Phase 3 or Phase 5 verifier ran.

**Prior runs.** I carried run-10 (U283 at b2467ae6: 47 units, 0 findings, 1 unvalidated candidate).
- **Updater units.** Its four are re-checked here as changed source.
- **New unit.** One, for the pruner.
- **Candidate.** It keeps its fingerprint on unchanged source.

**Deferred.** Nothing.

## 2. Security posture

**The U283b change.** No candidate survives. It closes the gaps the U283 audit raised, and it fails closed in two more places.

- **CompactionDB payload check.**
  - A failed `rsync` now counts the failure and replaces the step's record with a failure mark.
  - So does a completed `rsync` whose synced `CHANGELOG.md` does not name the source version (`scripts/update-agent-assets.sh:2828-2851`).
  - The mark comes from `mark_sync_failed` (`:2811-2814`). Its path, `<destination>/.sync-incomplete`, is one no sync writes, so `make doctor` reports the step until a sync completes. The older record no longer survives a partial sync.
  - `manifest_record` returns 1 when its write fails (`scripts/lib/asset-manifest.sh:136-143`), so a failed mark is counted too.
- **The pruner.** `_manifest_prune_retired` (`scripts/lib/asset-manifest.sh:158-194`):
  - refuses a manifest path that is a link or no regular file (`:163-166`);
  - takes the defined functions from a status-checked `compgen -A function` (`:169`);
  - decides the retired set in one `jq` program (`:171-175`) instead of a here-string loop that could keep every record and return 0.

  The parent's own `jq` run on a literal selects exactly the record whose step is undefined.
- **Unchanged.** `assert_asset_destination` and its four call sites (`:127-157`, `:1511`, `:1648`, `:1728`, `:2836`), the single-step exit (`:11`, `:2874-2878`), and `MISE_EXEC_AUTO_INSTALL=false` (`:2142`, `:2151`) are as run-10 checked them. U283b adds tests for linked parents at the omp aside and pi-claude-bridge sites, and for an unreadable physical path.
- **Tests.** They run in `TemporaryDirectory` HOMEs or a scratch manifest.

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

- **Where.** `.orchestration/orchestrate/regime-cutover/decisions.tsv:509` at fa969db6. The row is on origin/main since records sync 45 (aabee966, #694), and still there at 29439083. It quotes `claude auth status` output and keeps four account fields:
  - an email address whose redact-word part was replaced by `<redacted>`, leaving a local part that is a component of the multi-part redact word on line 5 of `redact-words.txt`, and the employer's domain;
  - the organisation UUID;
  - the organisation name;
  - the subscription type.

  None of these values is quoted in this report.
- **Lower-trust principal.** Any reader of the origin repository's main branch. Repository visibility is not source-visible, and this run had no network.
- **Intended control.** `redact-words.txt` plus `--scan-identifiers` (`scripts/orchestrator/records-sync.sh:30-33`, `:425-431`).
- **Why it passed.** None of these is changed by U283b:
  - `--scan-identifiers` tests only secret patterns, home paths, and literal redact words bounded by non-alphanumerics (`scripts/validate-agent-assets.py:2434-2440`, `:2443-2465`).
  - The hand pass (`decisions.tsv:521`) replaced only the listed words.
  - Neither the masker nor CI's scan (`.github/workflows/agent-assets.yml:69-70`) has an email or account rule.
  - The sync contract excludes content review (`records-sync.sh:511-515`).
- **Impact.** The operator's account identity and their enterprise organisation's identifier and name are disclosed on the default branch. They are not credentials: there is no account access.
- **Smallest fix.**
  1. Reduce the store row to "`claude auth status` exit 0, logged in" and publish it with the next sync. The row's history stays in aabee966, so removing it from history needs the owner's decision.
  2. Add an email rule (allowlisting `noreply@anthropic.com` and GitHub noreply) and `claude auth status` account-key rules (`orgId`, `orgName`, the email key) to `identifier_reasons` in `scripts/validate-agent-assets.py`.
  3. Treat each component of a multi-part redact word as a word, or have the owner list the components. Add a regression copy.
- **To verify independently.** Re-read `decisions.tsv:509` and `:521` at fa969db6, and confirm that `identifier_reasons` has no email or account rule. Owner-observed: the repository's visibility.

## 6. Hardening notes and positive patterns

These are not findings.

1. **The manifest writer isn't as strict as the pruner (new).** `_manifest_record` (`scripts/lib/asset-manifest.sh:45-123`) reads the manifest through `[ -f ]` and `jq`, which follow a link, and ends with `mv "${temporary_path}" "${manifest_path}"` (`:119`). If `manifest_path` were a link to a directory, that `mv` would move the temporary file into the link's target. U283b refuses this case in the pruner (`:163-166`) but not in the writer. No sandbox write root covers `~/.agents`, so only the operator could plant such a link; the same refusal in the writer would make the two consistent.
2. **The accepted roots are wider than the updater's** (carried, not addressed). `assert_asset_destination` accepts all of `~/.agents` and `~/.local` (`scripts/update-agent-assets.sh:129-135`). That includes the sandbox-writable `~/.local/state` roots (`home/dot_agents/agent-config.yaml:943-950`).
3. **Check and use are separate commands** (carried, not addressed). The CompactionDB assert and `rsync` are separate commands (`:2836-2837`). Staging and renaming, as the other three sites do, would close the window.
4. **A cross-reference** (carried). Another seat's U272 candidate concerns the unsandboxed `pnpm install` in `DSH_HOME/profiles/thak` (`:2151`). `--ignore-pnpmfile` there would close it whatever the write roots.
5. **Carried records-sync notes.** Hand redaction passes are not a control (`decisions.tsv:521`, `:525`), and the masker truncated the published credential handout's `read -s` line.

### Positive patterns

- A failure mark that the doctor reports, instead of a stale record.
- Payload verification after `rsync`.
- The pruner's link refusal and one-decision `jq`, with each command substitution's status checked.
- A test for every producer and call site.

## 7. Coverage summary

From `coverage-ledger.json` (48 units):

| Status | Units |
|---|---|
| covered | 5 |
| candidate | 1 |
| blocked | 0 |
| deferred | 0 |
| out_of_scope | 42 |

- **Covered (5):** all owned by `parent-hunter`:
  - the four U283 units re-checked: destination writes; single-step exit and recorded failures; harness `mise exec`; tests;
  - the new pruner unit.
- **Candidate (1):** the carried identity unit.
- **Out of scope (42):** carried from run-10.

**Critic results.** Neither the post-wave critic nor the final-clean critic found work. Both ran in the parent, so this is a single-reviewer coverage statement.
