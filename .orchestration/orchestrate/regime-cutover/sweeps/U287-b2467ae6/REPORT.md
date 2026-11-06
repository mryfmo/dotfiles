# Security audit report: dotfiles at b2467ae6ac7ad375d124165cbb461b11d12c2cc8

## 1. Run, scope and limits

**Candidate validation is incomplete, so this is a partial pass.** The carried candidate is still on origin/main, and no independent verifier could run.

| Fingerprint | Coverage unit | State |
|---|---|---|
| `records-sync/redaction/account-identity-residue-in-published-row` | `.orchestration/orchestrate/regime-cutover#records-sync-43-copies` × `…/redact-words.txt#redact-word-and-identity-scan` | `candidate`, unvalidated (carried; on main since aabee966) |

Per the skill's rule, an unvalidated candidate is not a finding and is not in `findings.json`, and the run is `incomplete`. Section 5a describes it for the owner.

**Profile and scope.** The profile is `standard`, scoped to the U283 change a23e4541..b2467ae6 (branch `fix/updater-single-function-fails-closed`): `scripts/update-agent-assets.sh` (+102/−13) and `tests/unit/test_update_agent_assets.py` (+265). The scope also includes the carried candidate, because this base holds its row. Every other path is carried `out_of_scope`.

**Brief discrepancies.** The brief gives the base as 8f31cf5c and calls the change "no production code".
- The merge base is a23e4541.
- The updater deletes and syncs into `~/.agents` and `~/.local` with the operator's authority, so I swept it as the boundary.

**Source ref.** The checkout was clean at the head both before and after the run.

**Budget.** None was set. Planned: four reconnaissance agents, one hunter wave, two critics, and two verifiers per candidate. Spent: zero delegated agents.

**Execution.** Sandboxed source-and-local-only policy, and in practice source only. By task rule, the script and tests were read, not run.

**Independence gap.** The delegation tool (Task) and eval kernel are denied by policy on this seat. Every phase ran in the parent (`parent-hunter`), and no Phase 3 or Phase 5 verifier ran.

**Prior runs.** I carried run-9 (U234c at 90db4721: 43 units, 0 findings, 1 unvalidated candidate).
- **U234c units.** Out of scope, because that branch is not merged.
- **Harness units.** Its carried DeepSeek-harness units (pin, DSH_COMMIT sinks, control flow) stay out of scope, since U283 does not change what they cover.
- **New units.** Four, for the updater change.
- **Candidate.** It keeps its fingerprint on unchanged source.

**Deferred.** Nothing.

## 2. Security posture

**The U283 change.** No candidate survives. It closes two real gaps from verdicts/U276b: a linked destination that let `rsync --delete` reach outside the asset tree, and exit-0 runs that hid failures.

- **The destination proof.** `assert_asset_destination` (`scripts/update-agent-assets.sh:127-157`) refuses:
  - a path outside `~/.agents` or `~/.local` (`:129-135`);
  - a parent that is a link or no directory (`:136-140`);
  - a parent whose physical path is not its spelling under the physical HOME (`:141-152`). That one comparison catches a link at any component, and any `..`;
  - a destination that is itself a link (`:153-156`).
- **Where it runs.** It runs before every delete, move-aside, staging or sync: `:1511`, `:1648`, `:1728`, `:2817`. Inside a checked destination, `rsync -a` replaces a linked subdirectory rather than following it.
- **Exit status.**
  - Under `set -Eeuo pipefail` (`:11`), a single step that fails exits non-zero, and one that counts a failure now fails at `fail_on_pin_failures` (`:2850`).
  - A failed CompactionDB `rsync` is counted and records nothing; it used to be `|| true` and was recorded anyway (`:2809-2824`).
  - The prune counts its failure instead of swallowing it (`:2833-2835`; `scripts/lib/asset-manifest.sh:151`, `:190-194`).
- **Harness build.** `MISE_EXEC_AUTO_INSTALL=false` on the harness's three `mise exec` runs (`:2142`, `:2151`) stops the build from fetching a tool into mise's trees.
- **The remaining race.** A check-to-use window remains: a link swapped in after the check and before the `rsync`. No sandboxed principal can write any asserted destination, because the sandbox write roots are elsewhere (`home/dot_agents/agent-config.yaml:943-952`). Only the operator's own unsandboxed processes could race it (section 6).
- **Tests.** They run in `TemporaryDirectory` HOMEs with stub tools, and pin each refusal and exit rule.

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

- **Where.** `.orchestration/orchestrate/regime-cutover/decisions.tsv:509` at b2467ae6. The row is on origin/main since records sync 45 (aabee966, #694). It quotes `claude auth status` output and keeps four account fields:
  - an email address whose redact-word part was replaced by `<redacted>`, leaving a local part that is a component of the multi-part redact word on line 5 of `redact-words.txt`, and the employer's domain;
  - the organisation UUID;
  - the organisation name;
  - the subscription type.

  None of these values is quoted in this report.
- **Lower-trust principal.** Any reader of the origin repository's main branch. Repository visibility is not source-visible, and this run had no network.
- **Intended control.** `redact-words.txt` plus `--scan-identifiers` (`scripts/orchestrator/records-sync.sh:30-33`, `:425-431`).
- **Why it passed.** None of these is changed by U283:
  - `--scan-identifiers` tests only secret patterns, home paths, and literal redact words bounded by non-alphanumerics (`scripts/validate-agent-assets.py:2434-2440`, `:2443-2465`).
  - The hand pass (`decisions.tsv:521`) replaced only the listed words.
  - Neither the masker nor CI's scan (`.github/workflows/agent-assets.yml:69-70`) has an email or account rule.
  - The sync contract excludes content review (`records-sync.sh:511-515`).
- **Impact.** The operator's account identity and their enterprise organisation's identifier and name are disclosed on the default branch. They are not credentials: there is no account access.
- **Smallest fix.**
  1. Reduce the store row to "`claude auth status` exit 0, logged in" and publish it with the next sync. The row's history stays in aabee966, so removing it from history needs the owner's decision.
  2. Add an email rule (allowlisting `noreply@anthropic.com` and GitHub noreply) and `claude auth status` account-key rules (`orgId`, `orgName`, the email key) to `identifier_reasons` in `scripts/validate-agent-assets.py`.
  3. Treat each component of a multi-part redact word as a word, or have the owner list the components. Add a regression copy.
- **To verify independently.** Re-read `decisions.tsv:509` and `:521` at b2467ae6, and confirm that `identifier_reasons` has no email or account rule. Owner-observed: the repository's visibility.

## 6. Hardening notes and positive patterns

These are not findings.

1. **The accepted roots are wider than the updater's.** `assert_asset_destination` accepts any path under `~/.agents` or `~/.local` (`:129-135`), and that includes the sandbox-writable `~/.local/state/hcom-regime`, `~/.local/state/hcom` and `~/.local/state/omp-seats` (`home/dot_agents/agent-config.yaml:943-950`). No current destination is under them. A future step that targeted one would pass the proof, while a sandboxed seat could swap a link in after it. Naming the updater's own roots instead would keep the proof meaningful: `~/.agents`, `~/.local/share/agent-assets`, `~/.local/lib/omp-extensions` and `~/.local/bin`.
2. **Check and use are separate commands.** The proof and the use are one command apart (for example `:2817-2818`), so a same-user process could swap a link in between, and `rsync` to `"${destination}/"` would follow it. CompactionDB could avoid this the way the other three sites do: `rsync` into a `mktemp` staging directory beside the destination, then rename it into place.
3. **A cross-reference, not this change.** Another seat holds an unvalidated candidate for an unmerged branch (U272) that makes `DSH_HOME` writable under srt. That would turn the updater's unsandboxed `pnpm install` in `DSH_HOME/profiles/thak` (`:2151`) into a sandbox-to-host path through a planted `.pnpmfile.cjs`. U283's `MISE_EXEC_AUTO_INSTALL=false` does not address that. At this head, no sandbox write root covers `DSH_HOME`.
4. **Carried records-sync notes.** Hand redaction passes are not a control (`decisions.tsv:521`, `:525`), and the masker truncated the published credential handout's `read -s` line.

### Positive patterns

- One helper proves physical containment by comparing `pwd -P` with the spelled path, and fails closed when it cannot read a physical path.
- The single-step run now has the full run's exit rule.
- Swallowed failures (`|| true`, a warning-only prune) are now counted.
- Tests cover a linked root, a linked destination, a linked intermediate directory and HOME spelled through a link.

## 7. Coverage summary

From `coverage-ledger.json` (47 units):

| Status | Units |
|---|---|
| covered | 4 |
| candidate | 1 |
| blocked | 0 |
| deferred | 0 |
| out_of_scope | 42 |

- **Covered (4):** all new and owned by `parent-hunter`: destination writes (`DESKTOP-MOBILE-AND-LOCAL-IPC.md#Local file ownership and TOCTOU`); single-step exit and recorded failures; the harness's `mise exec` tool installs; the U283 tests.
- **Candidate (1):** the carried identity unit.
- **Out of scope (42):** every other top-level directory and unchanged path, run-9's U234c units, the carried DeepSeek-harness units and the earlier carried units.

**Critic results.** Neither the post-wave critic nor the final-clean critic found work. Both ran in the parent, so this is a single-reviewer coverage statement.
