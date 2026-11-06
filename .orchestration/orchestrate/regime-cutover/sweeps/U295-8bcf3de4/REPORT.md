# Security audit report: dotfiles at 8bcf3de4cc773a6d4ad428ac92c27c0233df4818

## 1. Run, scope and limits

**Candidate validation is incomplete, so this is a partial pass.** Two carried leads stand at this head, and no independent verifier could run.

| Fingerprint | Coverage unit | State |
|---|---|---|
| `records-sync/redaction/account-identity-residue-in-published-row` | `.orchestration/orchestrate/regime-cutover#records-sync-43-copies` × `…/redact-words.txt#redact-word-and-identity-scan` | `candidate`, unvalidated, proposed confirmed (carried; on main since aabee966) |
| `dsh-profile:web-search-routes-to-the-official-api` | `home/dot_dsh/profiles/thak/cordis.patch.yml#web-search-deepseek-and-web-deepseek-api` × `…#disabled-by-base-bundle-id` | `candidate`, unvalidated, proposed rejected (carried from `sweeps/U227-785658d1`) |

Per the skill's rule, an unvalidated candidate goes into `findings.json` under no verdict, and the run is `incomplete`. Sections 5a and 5b describe the two leads.

**Profile and scope.** The profile is `standard`, scoped to the U227f change 29439083..8bcf3de4 (branch `fix/thak-profile-no-api-key-rows`), three files:
- `home/dot_dsh/profiles/thak/cordis.patch.yml`;
- `scripts/generate-agent-configs.py`;
- `tests/unit/test_dsh_profile.py`.

The scope also includes the store's prior lead on this surface and the carried identity candidate. Every other path is carried `out_of_scope`.

**Brief discrepancies.** The brief gives the base as 8f31cf5c and asks for run-7 to be carried.
- The merge base is 29439083.
- I carried this seat's latest run, run-12.

**Upstream context.** I read the installed, pinned harness tree (`~/.dsh/dsh/current`, dsh-v0.2.1-rc.5), package sources only, to check the ids the change disables and how the web seam behaves.

**Source ref.** The checkout was clean at the head both before and after the run.

**Budget.** None was set. Planned: four reconnaissance agents, one hunter wave, two critics, and two verifiers per candidate. Spent: zero delegated agents.

**Execution.** Sandboxed source-and-local-only policy, and in practice source only. By task rule, the harness was not composed or run.

**Independence gap.** The delegation tool (Task) and eval kernel are denied by policy on this seat. Every phase ran in the parent (`parent-hunter`), and no Phase 3 or Phase 5 verifier ran.

**Prior runs.**
- **run-12.** Carried: its brief-check units are out of scope (U280 not merged), and its identity candidate is kept.
- **`sweeps/U227-785658d1`.** Another seat's run-51 at 785658d1. Its `needs_validation` lead on this surface is carried by fingerprint. Its other records concern surfaces this change does not touch.

**Deferred.** Nothing.

## 2. Security posture

**The U227f change.** It closes the API-key route the store's prior lead described, and no new candidate arises.

- **The ids match.** The base bundle mounts `web-search-deepseek` and `web-deepseek-api` under exactly those ids, each with `apiKeyEnv: DEEPSEEK_API_KEY` (upstream `packages/bundle/base/cordis.patch.yml:473-481`).
- **The disable.** The kit patch now disables both by id (`home/dot_dsh/profiles/thak/cordis.patch.yml:9-12`), the same mechanism it already uses for the two official LLM adapters (`:5-8`).
- **Search fails closed.**
  - With both rows off, no row in the composed tree registers a search provider. The headless bundle mounts none, the other upstream providers are mounted by no composed bundle, and the kit inserts only omp-gateway and hooks-claude-code (`:19-35`).
  - The `web` seam, still configured with `searchProvider: deepseek-official`, throws `WEB_PROVIDER_CONFIGURED_MISSING` for an unregistered configured provider, with no fallback chain (upstream `packages/web/web/src/index.ts:68-74`, `:181`).
  - So a model-chosen `web_search` fails closed, and no enabled row reads `DEEPSEEK_API_KEY`.
- **Generator and test.** The generator emits the same rows (`scripts/generate-agent-configs.py:2286-2289`), and the new test pins them (`tests/unit/test_dsh_profile.py:133-137`) beside the existing no-`apiKeyEnv` check on the patch text (`:124`).

**The identity candidate** is unchanged: `decisions.tsv:509` is on main (section 5a).

## 3. Confirmed findings

None. Both carried leads are unvalidated (section 1).

| Severity | Title | Affected boundary | Observed result |
|---|---|---|---|
| — | none | — | — |

## 4. Confirmed finding details

None.

## 5. Needs validation

None in `findings.json`. The two carried leads are unvalidated candidates (sections 5a and 5b).

| Title | Trace | Blocker | Local next step | Owner-observed check |
|---|---|---|---|---|
| — | — | — | — | — |

## 5a. Unvalidated candidate: account identity in a published row (not a finding)

**`records-sync/redaction/account-identity-residue-in-published-row`**, carried since run-2. Proposed verdict confirmed, proposed severity low. Neither has been independently verified.

- **Where.** `.orchestration/orchestrate/regime-cutover/decisions.tsv:509` at 8bcf3de4. The row is on origin/main since records sync 45 (aabee966, #694). It quotes `claude auth status` output and keeps four account fields:
  - an email address whose redact-word part was replaced by `<redacted>`, leaving a local part that is a component of the multi-part redact word on line 5 of `redact-words.txt`, and the employer's domain;
  - the organisation UUID;
  - the organisation name;
  - the subscription type.

  None of these values is quoted in this report.
- **Lower-trust principal.** Any reader of the origin repository's main branch. Repository visibility is not source-visible, and this run had no network.
- **Intended control.** `redact-words.txt` plus `--scan-identifiers` (`scripts/orchestrator/records-sync.sh:30-33`, `:425-431`).
- **Why it passed.** None of these is changed by U227f:
  - `--scan-identifiers` tests only secret patterns, home paths, and literal redact words bounded by non-alphanumerics (`scripts/validate-agent-assets.py:2434-2440`, `:2443-2465`).
  - The hand pass (`decisions.tsv:521`) replaced only the listed words.
  - Neither the masker nor CI's scan (`.github/workflows/agent-assets.yml:69-70`) has an email or account rule.
  - The sync contract excludes content review (`records-sync.sh:511-515`).
- **Impact.** The operator's account identity and their enterprise organisation's identifier and name are disclosed on the default branch. They are not credentials: there is no account access.
- **Smallest fix.**
  1. Reduce the store row to "`claude auth status` exit 0, logged in" and publish it with the next sync. The row's history stays in aabee966, so removing it from history needs the owner's decision.
  2. Add an email rule (allowlisting `noreply@anthropic.com` and GitHub noreply) and `claude auth status` account-key rules (`orgId`, `orgName`, the email key) to `identifier_reasons` in `scripts/validate-agent-assets.py`.
  3. Treat each component of a multi-part redact word as a word, or have the owner list the components. Add a regression copy.
- **To verify independently.** Re-read `decisions.tsv:509` and `:521` at 8bcf3de4, and confirm that `identifier_reasons` has no email or account rule. Owner-observed: the repository's visibility.

## 5b. Unvalidated candidate: the carried web-search lead (not a finding)

**`dsh-profile:web-search-routes-to-the-official-api`**, carried from the store's `sweeps/U227-785658d1` (`needs_validation` at 785658d1). Proposed verdict rejected. That has not been independently verified.

- **The lead.** The thak profile left the base bundle's DeepSeek web-search provider mounted, so a model-chosen search would go to the official DeepSeek API whenever `DEEPSEEK_API_KEY` is in the launch environment. That would cross the kit's login-only route decision.
- **Why the current source refutes it.** U227f disables both rows under their base-bundle ids (`home/dot_dsh/profiles/thak/cordis.patch.yml:9-12`). The seam then fails closed on the unregistered configured provider, and no other composed row registers one (section 2).
- **What remains unobserved.** Two facts are upstream source read locally, not runs: that cordis applies a `disabled: true` patch row by id (the profile already relies on that for `llm-deepseek` and `llm-deepseek-account`), and the seam's selection rule. The prior record's own bounded local plan would confirm both, with its loopback search stub receiving no request.
- **To verify independently.**
  1. Re-read the two disabled rows at 8bcf3de4.
  2. Re-read upstream `packages/bundle/base/cordis.patch.yml:467-481`, `packages/bundle/headless/cordis.patch.yml` and `packages/web/web/src/index.ts:68-74`, `:143`, `:181`.
  3. Confirm that no composed row registers a search provider.

## 6. Hardening notes and positive patterns

These are not findings.

1. **A failing tool instead of no tool.** The `web` seam stays mounted with `searchProvider: deepseek-official`, so `web_search` now fails with `WEB_PROVIDER_CONFIGURED_MISSING` instead of being absent. Disabling `tool-web` (or `web`) would take the tool away from the model. A test that composes the profile and asserts no enabled row carries `apiKeyEnv` would pin the property against an upstream bundle that adds a new key row.
2. **Carried records-sync notes.** Hand redaction passes are not a control (`decisions.tsv:521`, `:525`), and the masker truncated the published credential handout's `read -s` line.

### Positive patterns

- Rows are addressed by the exact upstream ids, with the reason recorded in the generator docstring (`scripts/generate-agent-configs.py:2248-2249`).
- A test per disabled row, beside the patch-wide check for key references.

## 7. Coverage summary

From `coverage-ledger.json` (45 units):

| Status | Units |
|---|---|
| covered | 1 |
| candidate | 2 |
| blocked | 0 |
| deferred | 0 |
| out_of_scope | 42 |

- **Covered (1):** the generator and its committed render (new).
- **Candidate (2):**
  - the thak web rows, carrying the prior lead (`prior_needs_validation`);
  - the identity unit.
- **Out of scope (42):** every other top-level directory and unchanged path, the brief-check units and the earlier carried units.

**Critic results.** Neither the post-wave critic nor the final-clean critic found work. Both ran in the parent, so this is a single-reviewer coverage statement.
