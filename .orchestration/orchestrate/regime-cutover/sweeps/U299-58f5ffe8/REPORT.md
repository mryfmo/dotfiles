# Security audit report: dotfiles at 58f5ffe87aa5dc49330499eaf9c4b0da09377cdd

## 1. Run, scope and limits

**Candidate validation is incomplete, so this is a partial pass.** Four leads stand at this head, one of them new, and no independent verifier could run.

| Fingerprint | Coverage unit (surface) | State |
|---|---|---|
| `dsh-profile:thak-fs-tool-writes-workspace-git-unguarded` | `home/dot_dsh/profiles/thak/cordis.patch.yml#tool-fs-workspace-writes` | `candidate`, new, proposed needs_validation (section 5a) |
| `dsh-profile:web-search-routes-to-the-official-api` | `…/cordis.patch.yml#web-search-deepseek-and-web-deepseek-api` | `candidate`, carried, proposed needs_validation (section 5b) |
| `dsh-profile:thak-runs-without-command-sandbox` | `…/cordis.patch.yml#bash-sandbox-and-the-shell-tool` | `candidate`, carried, proposed rejected (section 5c) |
| `records-sync/redaction/account-identity-residue-in-published-row` | `.orchestration/orchestrate/regime-cutover#records-sync-43-copies` | `candidate`, carried, proposed confirmed (section 5d) |

Per the skill's rule, an unvalidated candidate goes into `findings.json` under no verdict, and the run is `incomplete`.

**Profile and scope.** The profile is `standard`, scoped to the U298 change 1878b569..58f5ffe8 (branch `fix/session-start-hook-under-bridge`): `tests/unit/test_dsh_hook_coverage.py` only. Because that test states the thak profile's security posture, the scope includes that posture: the store's two prior leads on it, and one lead its facts expose. The carried identity candidate is also in scope. Every other path is carried `out_of_scope`.

**Brief discrepancies.** The brief gives the base as 8f31cf5c and asks for run-7 to be carried.
- The merge base is 1878b569 (U276d, U280, U283 merged).
- I carried this seat's latest run, run-13.
- U227f (run-13's fix) is not merged into this base.

**Upstream context.** I read the installed, pinned harness (`~/.dsh/dsh/current`, dsh-v0.2.1-rc.5), package sources only.

**Source ref.** The checkout was clean at the head both before and after the run.

**Budget.** None was set. Planned: four reconnaissance agents, one hunter wave, two critics, and two verifiers per candidate. Spent: zero delegated agents.

**Execution.** Sandboxed source-and-local-only policy, and in practice source only. By task rule, dsh was neither composed nor run.

**Independence gap.** The delegation tool (Task) and eval kernel are denied by policy on this seat. Every phase ran in the parent (`parent-hunter`). The post-wave pass accepted one unit (the file tool), which was hunted in the same parent pass. No Phase 3 or Phase 5 verifier ran.

**Deferred.** Nothing.

## 2. Security posture

**The U298 change.** It is accurate and test-only. It models plugin activation and pins that none of the kit's Claude hooks runs under the deployed thak profile:
- PreToolUse Bash;
- the permgate PermissionRequest hook;
- PostToolUse Write|Edit;
- SessionStart.

The reason is that `hooks-claude-code` injects the `shell` service, and the profile disables its only provider, `bash-sandbox` (`home/dot_dsh/profiles/thak/cordis.patch.yml:9-10`). The constants match the pinned upstream (`experimental/hooks-claude-code/src/index.ts:48`; `bundle/base/cordis.patch.yml:249-257`). The test reads files in memory and runs nothing.

**What that leaves active.** That is the question for the sweep:

- **No shell tool.** `tool-bash` and `tool-pwsh` also wait for `shell`, so the model has no command tool. `permission-presets` waits for it too.
- **The file tool runs.** `tool-fs` does not wait for `shell`. Its writes and edits are fenced only by `fs-sandbox`'s `workspace-write`, which covers anything under the working directory or temp, with no `.git` exception.
- **No guard on it.** No kit hook sees those writes, and nothing on main launches dsh under srt (section 5a).
- **Web rows.** The base bundle's DeepSeek web rows are still mounted at this base, because U227f is unmerged (section 5b).

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

## 5a. New lead: the thak file tool can write a checkout's `.git` (not a finding)

**`dsh-profile:thak-fs-tool-writes-workspace-git-unguarded`**. Proposed verdict needs_validation. Not independently verified.

- **Claimed root cause.** Under the thak profile, the model's write and edit tools stay active while every kit hook and the permission presets are pending. Their only fence is `fs-sandbox`'s `workspace-write`, which admits a write anywhere under the working directory, `.git/hooks` and `.git/config` included. Nothing on main runs dsh inside srt.
- **Trace, all in the pinned upstream except the kit patch.**
  1. `tool-fs` injects `tools`, `fs`, `systemPrompt` and `workingDirectory`, and no shell (`fs/tool-fs/src/index.ts:23`).
  2. Its write resolves the sandbox policy and the `fs/write-intent` waterfall, then calls `ctx.fs.writeText`. "No policy means an unconditional atomic create-or-overwrite" (`fs/tool-fs/src/write.ts:1-4`, `:113-131`).
  3. The fs provider is `fs-sandbox` (`bundle/base/cordis.patch.yml:516-519`), under `sandbox-policy`: `DSH_PERMISSION_MODE`, default `workspace-write`, with `workspaceRoot: process.cwd()` (`:243-247`). Nothing in the kit sets `DSH_PERMISSION_MODE`.
  4. `workspace-write` allows a mutation that canonicalizes under the workspace or temp root (`fs/fs-sandbox/src/index.ts:20-24`, `:113-143`). The sandbox packages show no `.git` or protected-subpath exception.
  5. The kit patch disables `bash-sandbox` (`home/dot_dsh/profiles/thak/cordis.patch.yml:9-10`), so `hooks-claude-code` and `permission-presets` are pending (`tests/unit/test_dsh_hook_coverage.py`).
- **Lower-trust input.** Content the model reads: web fetch is mounted (`bundle/base/cordis.patch.yml:483-490`), and the model reads repository files.
- **Possible result.** A turn writes `<cwd>/.git/hooks/<name>` or `<cwd>/.git/config`. The operator's next git command in that checkout then runs it with the operator's authority, outside srt.
- **Blockers.**
  1. Whether `tool-fs` registers under the composed tree, and whether a write under `<cwd>/.git` succeeds with the presets pending. This is upstream runtime behaviour, read and not observed.
  2. Whether the operator runs dsh with a git checkout as its working directory.
- **Local plan.** In the required sandbox:
  1. In a scratch HOME and DSH_HOME with the pinned harness and loopback only, make a scratch git repository the working directory.
  2. Point the model route at a loopback stub that answers one write call to `.git/hooks/post-checkout` with a harmless marker.
  3. Run one headless turn, check whether the file exists and is executable, and stop without running git.
- **Owner-observed.** Where dsh is run, and whether the profile should keep `bash-sandbox` off while `tool-fs` stays on.
- **Smallest fix to consider once confirmed.** Pin `DSH_PERMISSION_MODE=read-only` for the kit's dsh runs until an srt launcher lands, or disable `tool-fs` in the thak patch. Either way, add a test that composes the profile and asserts no write tool is active outside srt.

## 5b. Carried lead: web search to the official API (not a finding)

**`dsh-profile:web-search-routes-to-the-official-api`** (`sweeps/U227-785658d1`). Proposed verdict needs_validation, as the store recorded it.

At this base, U227f is unmerged, so the thak patch still mounts `web-search-deepseek` and `web-deepseek-api` (upstream `bundle/base/cordis.patch.yml:467-481`). `tool-web` needs no shell, so a model-chosen `web_search` can reach the official DeepSeek API whenever `DEEPSEEK_API_KEY` is in the launch environment. The fix exists on `fix/thak-profile-no-api-key-rows`, which run-13 swept.

## 5c. Carried lead: commands without a sandbox (not a finding)

**`dsh-profile:thak-runs-without-command-sandbox`** (`sweeps/U227-785658d1`). Proposed verdict rejected, for the shell path. Not independently verified.

`tool-bash` injects `shell` (upstream `shell/tool-bash/src/index.ts:34`), and the profile disables its only provider (`cordis.patch.yml:9-10`). So no shell tool activates, which matches the measured "3 entries did not activate". The lead's file-tool residue is the separate root cause in section 5a.

## 5d. Carried lead: account identity in a published row (not a finding)

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
1. Reduce the row, then publish it with the next sync. Its history stays in aabee966, so removing it from history needs the owner's decision.
2. Add email and account-key rules to `identifier_reasons`.
3. Treat each component of a multi-part redact word as a word.

## 6. Hardening notes and positive patterns

These are not findings.

1. **The test pins zero hook coverage and passes.** `EXPECTED_COVERAGE` is all `inactive`, and the suite stays green as long as `bash-sandbox` stays off. Nothing in it fails when no other guard exists for the tools that remain active. Section 5a's proposed test would close that.
2. **Carried records-sync notes.** Hand redaction passes are not a control (`decisions.tsv:521`, `:525`), and the masker truncated the published credential handout's `read -s` line.

### Positive patterns

- Activation is modelled from measured upstream constants and the kit's own patch.
- The test fails by name when the patch enables a shell provider or an injected service loses its provider row.

## 7. Coverage summary

From `coverage-ledger.json` (48 units):

| Status | Units |
|---|---|
| covered | 1 |
| candidate | 4 |
| blocked | 0 |
| deferred | 0 |
| out_of_scope | 43 |

- **Covered (1):** the U298 activation test.
- **Candidate (4):** the file-tool lead (new); the web-search lead and the command-sandbox lead (both `prior_needs_validation`); the identity unit.
- **Out of scope (43):** every other top-level directory and unchanged path, run-13's U227f generator unit, and the earlier carried units.

**Critic results.** The post-wave critic accepted one missing unit (the file tool), and the final-clean critic found no work. Both ran in the parent, so this is a single-reviewer coverage statement.
