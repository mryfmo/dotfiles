# Security audit report: dotfiles at b2db96b627802c287c4e855bf252309a0d0a298d

## 1. Run, scope and limits

**Candidate validation is incomplete, so this is a partial pass.** Four carried leads are re-checked at this head, and no independent verifier could run.

| Fingerprint | State at this head |
|---|---|
| `dsh-profile:thak-fs-tool-writes-workspace-git-unguarded` | `candidate`, stands, proposed needs_validation (section 5a) |
| `dsh-profile:web-search-routes-to-the-official-api` | `candidate`, refuted here, proposed rejected (section 5b) |
| `dsh-profile:thak-runs-without-command-sandbox` | `candidate`, proposed rejected (section 5c) |
| `records-sync/redaction/account-identity-residue-in-published-row` | `candidate`, stands, proposed confirmed (section 5d) |

Per the skill's rule, an unvalidated candidate goes into `findings.json` under no verdict, and the run is `incomplete`.

**Profile and scope.** The profile is `standard`. The head b2db96b6 merges U227f (8bcf3de4) with origin/main 24c00544, which holds U298 (#704) and U297 (#705). Against its main side, it changes exactly U227f's three files:
- `home/dot_dsh/profiles/thak/cordis.patch.yml`;
- `scripts/generate-agent-configs.py`;
- `tests/unit/test_dsh_profile.py`.

All three are byte-identical to the 8bcf3de4 that run-13 swept. The merged U298 test and U297 files are byte-identical to what run-14 and run-15 swept. So the sweep covers the merge's interaction and the carried leads at this head. Every other path is carried `out_of_scope`.

**Brief discrepancies.** The brief gives the base as 8f31cf5c and asks for run-7 to be carried. I carried this seat's latest run, run-15.

**Upstream context.** I read the installed, pinned harness (`~/.dsh/dsh/current`, dsh-v0.2.1-rc.5), package sources only.

**Source ref.** The checkout was clean at the head both before and after the run.

**Budget.** None was set. Planned: four reconnaissance agents, one hunter wave, two critics, and two verifiers per candidate. Spent: zero delegated agents.

**Execution.** Sandboxed source-and-local-only policy, and in practice source only.

**Independence gap.** The delegation tool (Task) and eval kernel are denied by policy on this seat. Every phase ran in the parent (`parent-hunter`), and no Phase 3 or Phase 5 verifier ran.

**Deferred.** Nothing.

## 2. Security posture

**The merge.** It is clean, and its two halves compose.

- **U227f.** It disables `web-search-deepseek` and `web-deepseek-api` by their base-bundle ids (`home/dot_dsh/profiles/thak/cordis.patch.yml:9-12`; generator `scripts/generate-agent-configs.py:2286-2289`; test `tests/unit/test_dsh_profile.py:133-137`). The only base-bundle rows that read `DEEPSEEK_API_KEY` are therefore off, and the web seam fails closed on its unregistered provider.
- **U298.** Its activation model maps `shell` to `bash-sandbox` alone and asserts that the missing set is exactly `{shell}` (`tests/unit/test_dsh_hook_coverage.py:139-140`, `:170-182`, `:260`). U227f's two new disabled rows provide no injected service, so the set and the all-`inactive` table are unchanged.
- **What stays.** Under the merged profile, the model has no shell tool and no kit hook runs. Its file tool is fenced only by `workspace-write` under the working directory, `.git` included, and nothing on main runs dsh under srt (section 5a).

## 3. Confirmed findings

None. All four leads are unvalidated (section 1).

| Severity | Title | Affected boundary | Observed result |
|---|---|---|---|
| — | none | — | — |

## 4. Confirmed finding details

None.

## 5. Needs validation

None in `findings.json`. The four leads are unvalidated candidates (sections 5a to 5d).

| Title | Trace | Blocker | Local next step | Owner-observed check |
|---|---|---|---|---|
| — | — | — | — | — |

## 5a. Lead: the thak file tool can write a checkout's `.git` (not a finding)

**`dsh-profile:thak-fs-tool-writes-workspace-git-unguarded`**, carried from run-14. Proposed verdict needs_validation. Not independently verified. Neither U227f nor the merged main changes it.

- **Claimed root cause.** `tool-fs` injects no shell (upstream `fs/tool-fs/src/index.ts:23`), so it activates while `hooks-claude-code` and `permission-presets` are pending, which U298 now pins on main. Its write is fenced only by `fs-sandbox`'s `workspace-write` under `process.cwd()`, with no `.git` exception (`fs/tool-fs/src/write.ts:113-131`; `bundle/base/cordis.patch.yml:243-247`, `:516-519`; `fs/fs-sandbox/src/index.ts:20-24`, `:113-143`). Nothing in the kit sets `DSH_PERMISSION_MODE`, and nothing on main runs dsh under srt.
- **Possible result.** Injected content makes a turn write `<cwd>/.git/hooks/<name>` or `<cwd>/.git/config`. The operator's next git command there then runs it as the operator, outside srt.
- **Blockers.**
  1. The runtime write is upstream behaviour, read but not observed.
  2. Whether dsh is run in a git checkout.
- **Local plan.** In the required sandbox: a scratch HOME and DSH_HOME, loopback only, and a scratch git repository as the working directory. A stub model answers one write to `.git/hooks/post-checkout`. Check for the file, and stop without running git.
- **Fix to consider.** `DSH_PERMISSION_MODE=read-only` for the kit's dsh runs until an srt launcher lands, or disable `tool-fs` in the thak patch. Add a composed-profile test that asserts no write tool is active outside srt.

## 5b. Lead: web search to the official API (not a finding)

**`dsh-profile:web-search-routes-to-the-official-api`**, from `sweeps/U227-785658d1`. Proposed verdict rejected at this head. Not independently verified.

This head carries U227f's fix: both rows are disabled under their base-bundle ids (`cordis.patch.yml:9-12`; upstream `bundle/base/cordis.patch.yml:473-481`). No other composed row registers a search provider, and the seam fails closed (upstream `web/web/src/index.ts:68-74`, `:181`).

Two facts behind the refutation are upstream source read locally: the by-id disable and the seam's selection rule. The store record's local plan, with its stub receiving no request, would confirm them.

## 5c. Lead: commands without a sandbox (not a finding)

**`dsh-profile:thak-runs-without-command-sandbox`**, from `sweeps/U227-785658d1`. Proposed verdict rejected for the shell path.

`bash-sandbox` is disabled (`cordis.patch.yml:13-14`), and `tool-bash` injects `shell` (upstream `shell/tool-bash/src/index.ts:34`), so no shell tool activates. U298's test now records this on main. The file-tool residue is section 5a.

## 5d. Lead: account identity in a published row (not a finding)

**`records-sync/redaction/account-identity-residue-in-published-row`**, carried since run-2. Proposed verdict confirmed, proposed severity low.

The row at `.orchestration/orchestrate/regime-cutover/decisions.tsv:509` is on origin/main since records sync 45 (aabee966). It publishes four account fields from `claude auth status`:
- the account email's residue, with its employer domain;
- the organisation UUID;
- the organisation name;
- the subscription type.

None is quoted here. The causes are unchanged:
- the literal redact-word scan (`scripts/validate-agent-assets.py:2434-2440`, `:2443-2465`);
- the hand pass (`decisions.tsv:521`);
- no email or account rule (`.github/workflows/agent-assets.yml:69-70`);
- the sync contract's content-review exclusion (`scripts/orchestrator/records-sync.sh:511-515`).

**Fix.**
1. Reduce the row, and publish it with the next sync. Its history stays in aabee966, so removing it from history needs the owner's decision.
2. Add email and account-key rules to `identifier_reasons`.
3. Treat each component of a multi-part redact word as a word.

## 6. Hardening notes and positive patterns

These are not findings.

1. **A failing tool instead of no tool** (carried from run-13). With the web rows disabled, `web_search` fails with `WEB_PROVIDER_CONFIGURED_MISSING` instead of being absent. Disabling `tool-web` would remove it from the model.
2. **Zero hook coverage passes** (carried from run-14). U298's table is all `inactive`, and the suite stays green; nothing fails when no guard exists for the remaining file tool.
3. **Carried.** The records-sync notes, and run-15's CI-gate context note.

### Positive patterns

- A clean merge whose three changed files are exactly the reviewed U227f.
- Two tests that share one row parser, so the disabled-row set means the same thing to both.

## 7. Coverage summary

From `coverage-ledger.json` (51 units):

| Status | Units |
|---|---|
| covered | 2 |
| candidate | 4 |
| blocked | 0 |
| deferred | 0 |
| out_of_scope | 45 |

- **Covered (2):** both re-opened: the U227f generator and render unit; the U298 activation unit, checked for the merge's interaction.
- **Candidate (4):** the four leads.
- **Out of scope (45):** every other top-level directory and unchanged path, run-15's installer units (merged byte-identical), and the earlier carried units.

**Critic results.** Neither the post-wave critic nor the final-clean critic found work. Both ran in the parent, so this is a single-reviewer coverage statement.
