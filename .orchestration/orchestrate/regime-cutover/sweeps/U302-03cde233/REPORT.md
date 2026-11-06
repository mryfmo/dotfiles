# Security audit report: dotfiles at 03cde233ff84847ca9177a795cbf0e232e84eea1

## 1. Run, scope and limits

**Candidate validation is incomplete, so this is a partial pass.** Four leads carried from run-14 stand at this head, which has the same base, and no independent verifier could run.

| Fingerprint | Coverage unit (surface) | State |
|---|---|---|
| `dsh-profile:thak-fs-tool-writes-workspace-git-unguarded` | `home/dot_dsh/profiles/thak/cordis.patch.yml#tool-fs-workspace-writes` | `candidate`, proposed needs_validation (section 5a) |
| `dsh-profile:web-search-routes-to-the-official-api` | `…/cordis.patch.yml#web-search-deepseek-and-web-deepseek-api` | `candidate`, proposed needs_validation (section 5b) |
| `dsh-profile:thak-runs-without-command-sandbox` | `…/cordis.patch.yml#bash-sandbox-and-the-shell-tool` | `candidate`, proposed rejected (section 5c) |
| `records-sync/redaction/account-identity-residue-in-published-row` | `.orchestration/orchestrate/regime-cutover#records-sync-43-copies` | `candidate`, proposed confirmed (section 5d) |

Per the skill's rule, an unvalidated candidate goes into `findings.json` under no verdict, and the run is `incomplete`.

**Profile and scope.** The profile is `standard`, scoped to the U297 and U297c change 1878b569..03cde233 (branch `ci/public-bootstrap-chromium-snap`), four files:
- `install/ubuntu/client/misc.sh`;
- its chezmoi `run_once` template;
- `tests/install/ubuntu/client/misc.bats`;
- `tests/unit/test_ci_runner.py`.

The scope also includes run-14's four leads, re-checked on unchanged source. Every other path is carried `out_of_scope`.

**Brief discrepancies.** The brief's GOAL is the U227b template (a DSH profile renderer change, branch from d1ecd495), and it asks for run-6 to be carried.
- The head is U297 and U297c on origin/main 1878b569, and I swept that.
- I carried this seat's latest run, run-14, which is on the same base.
- U297 alone (cf951b62) was swept by another seat, as its run-16.

**Source ref.** The checkout was clean at the head both before and after the run.

**Budget.** None was set. Planned: four reconnaissance agents, one hunter wave, two critics, and two verifiers per candidate. Spent: zero delegated agents.

**Execution.** Sandboxed source-and-local-only policy, and in practice source only. By task rule, the installer and tests were read, not run.

**Independence gap.** The delegation tool (Task) and eval kernel are denied by policy on this seat. Every phase ran in the parent (`parent-hunter`), and no Phase 3 or Phase 5 verifier ran.

**Deferred.** Nothing.

## 2. Security posture

**The U297 and U297c change.** No candidate.

- **The snap skip.** `install_chromium` now skips the snap with one printed line on a GitHub Actions runner (`install/ubuntu/client/misc.sh:86-90`).
  - The gate is `is_ci_runner`, which requires `GITHUB_ACTIONS=true` and a non-empty `RUNNER_TEMP` and never reads `CI` (`scripts/lib/ci-runner.sh:24-26`). So an agent shell's `CI=true` still installs the snap, and the tests pin both directions.
  - The skipped step installs a browser and gates nothing else. On an operator host, a process able to set both variables could at most leave Chromium uninstalled.
- **The helper load.**
  - Under chezmoi, the helper is included inline before the installer (`home/.chezmoiscripts/ubuntu/run_once_50-client-install-misc.sh.tmpl:9-10`).
  - On a direct run, it is sourced from a `BASH_SOURCE`-relative path built by parameter expansion, or from the working directory for a bare-name invocation. It is refused with exit 2 when it is unreadable or fails to source (`misc.sh:19-30`).
  - Both locations are the operator's checkout or working directory.
- **Tests.** They run under `BATS_TEST_TMPDIR` and `tempfile` scratch trees with a fake `snap`, with no real install or network call.

**The four carried leads** are unchanged at this head (sections 5a to 5d).

## 3. Confirmed findings

None. All four leads are unvalidated (section 1).

| Severity | Title | Affected boundary | Observed result |
|---|---|---|---|
| — | none | — | — |

## 4. Confirmed finding details

None.

## 5. Needs validation

None in `findings.json`. The four leads are unvalidated candidates (sections 5a to 5d). They are carried from run-14 on unchanged source; their text follows as run-14 recorded it, re-checked at this head.

## 5a. Carried lead (new in run-14): the thak file tool can write a checkout's `.git` (not a finding)

**`dsh-profile:thak-fs-tool-writes-workspace-git-unguarded`**. Proposed verdict needs_validation. Not independently verified.

- **Claimed root cause.** Under the thak profile, the model's write and edit tools stay active while every kit hook and the permission presets are pending. Their only fence is `fs-sandbox`'s `workspace-write`, which admits a write anywhere under the working directory, `.git/hooks` and `.git/config` included. Nothing on main runs dsh inside srt.
- **Trace, all in the pinned upstream except the kit patch.**
  1. `tool-fs` injects `tools`, `fs`, `systemPrompt` and `workingDirectory`, and no shell (`fs/tool-fs/src/index.ts:23`).
  2. Its write resolves the sandbox policy and the `fs/write-intent` waterfall, then calls `ctx.fs.writeText`. "No policy means an unconditional atomic create-or-overwrite" (`fs/tool-fs/src/write.ts:1-4`, `:113-131`).
  3. The fs provider is `fs-sandbox` (`bundle/base/cordis.patch.yml:516-519`), under `sandbox-policy`: `DSH_PERMISSION_MODE`, default `workspace-write`, with `workspaceRoot: process.cwd()` (`:243-247`). Nothing in the kit sets `DSH_PERMISSION_MODE`.
  4. `workspace-write` allows a mutation that canonicalizes under the workspace or temp root (`fs/fs-sandbox/src/index.ts:20-24`, `:113-143`). The sandbox packages show no `.git` or protected-subpath exception.
  5. The kit patch disables `bash-sandbox` (`home/dot_dsh/profiles/thak/cordis.patch.yml:9-10`), so `hooks-claude-code` and `permission-presets` are pending. That is the upstream injection facts cited in this run's shell-tool unit; U298's test, which records them, is not merged into this base.
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

1. **The CI gate is environment-only, and it guards security-relevant skips** (context, predating this change). `is_ci_runner` reads only `GITHUB_ACTIONS` and `RUNNER_TEMP` (`scripts/lib/ci-runner.sh:24-26`). Besides this change's snap skip, it turns off:
   - the dirty-source guard (`home/.chezmoiscripts/common/run_before_00-refuse-dirty-source.sh.tmpl:53`);
   - the age-key decrypt (`run_before_01-decrypt-private-key.sh.tmpl:33`);
   - brew tap trust (`install/macos/common/brew.sh:77`).

   On an operator host, any process that sets both variables in a chezmoi apply's environment turns those off. The repository documents this as the deliberate CI definition. A CI-only path that weakens a control could also require a runner-only fact, such as `RUNNER_TEMP` being a real directory owned by the runner user.
2. **Carried.** Run-14's notes on the thak profile's hook-coverage test, and the records-sync notes, still apply.

### Positive patterns

- One CI definition that ignores the generic `CI` variable, with a test that keeps its three copies equal.
- A helper load that refuses by name instead of running the snap decision without the helper.
- Tests for runner, host and agent-shell cases.

## 7. Coverage summary

From `coverage-ledger.json` (51 units):

| Status | Units |
|---|---|
| covered | 3 |
| candidate | 4 |
| blocked | 0 |
| deferred | 0 |
| out_of_scope | 44 |

- **Covered (3):** all new: the CI snap skip; the helper load; the tests.
- **Candidate (4):** the leads carried from run-14.
- **Out of scope (44):** every other top-level directory and unchanged path, run-14's U298 unit (not merged), and the earlier carried units.

**Critic results.** Neither the post-wave critic nor the final-clean critic found work. Both ran in the parent, so this is a single-reviewer coverage statement.
