# Security audit: dotfiles at 7992f1f58e75deb9e6d5493fbdbe00e2641ebae9 (U224 head)

## 1. Run, scope and limits

**This is a partial and incomplete pass.**

| Item | Value |
| --- | --- |
| Profile | `standard` |
| Scope | Scoped to the diff `c4195463..7992f1f5`: 27 changed paths, measured with `git diff --name-only`. The brief states 29, which does not match the measurement. |
| Out of scope | Every other top-level directory and the root files are recorded `out_of_scope` in the coverage ledger. |
| Source ref | `7992f1f5` on `feat/remove-understand-anything-graphify-in`, clean worktree. |
| Budget | None set. |
| Execution | Source review only. The brief forbids building, testing or executing target code, so no target-controlled process ran and every check is `method: source`. |
| Prior runs | None. The seat had no earlier output directory, so nothing was carried and no exclusion applied. |

**Incomplete, `run_status: "incomplete"`, reason `independent_agents_unavailable`.** The seat's tool policy denies the Task tool (`tools.approval.task: deny`). As a result:

- No reconnaissance, hunter, post-wave critic, final-clean critic, Phase 3 verifier or Phase 5 verifier agent ran. The parent did reconnaissance and hunting itself.
- Neither critic ran, so this report makes no clean-coverage claim.
- The skill requires a candidate to be validated by a fresh agent that did not hunt it. That was impossible here, so findings.json holds no record.

One candidate stays **unvalidated** in the coverage ledger and is **not a finding**:

| Fingerprint | Linked ledger unit (surface, boundary, class) | Status |
| --- | --- | --- |
| `retire-understand-anything:project-scope-cwd` | `scripts/update-agent-assets.sh#retire_understand_anything`, `scripts/update-agent-assets.sh#claude_outside_projects`, Chained vulnerabilities and trust boundaries | Unvalidated candidate |

**What the candidate claims (unvalidated):**

- For a project- or local-scope record of `understand-anything@understand-anything`, the new step runs `claude plugin uninstall ... --scope project|local` with its working directory set to the recorded `projectPath` (update-agent-assets.sh:2403-2408).
- Every other `claude` call of the updater runs from an empty directory, so that no project's `.claude` settings take part (update-agent-assets.sh:349-361).
- The repository documents that `make update` manages user-scope installations only (update-agent-assets.sh:566-567, 594-596; agent-config.yaml:1461-1463; README.md:1253-1257).
- If that CLI call reads and executes a code-running setting from the project's `.claude/settings.json` or `.claude/settings.local.json` (for example `apiKeyHelper`, hooks, `statusLine` or `env`) without the workspace-trust prompt, then repository content of that project runs with the operator's authority during `make update`.

**Why it stays unvalidated:**

- The decisive fact is Claude Code CLI behaviour. It is not in this repository.
- Independent validation could not run.

**Next steps:**

- A bounded local check: run the step against a fixture project whose `.claude/settings.json` sets a marker-writing `apiKeyHelper` and hook, with a scratch `HOME` and no network, and see whether the marker appears.
- An owner-observed check: confirm from the Claude Code documentation for the installed version which settings `claude plugin` subcommands load.
- A smallest fix if positive: drop the project and local branches (the repository manages user scope only, and `claude plugin marketplace remove` already uninstalls every plugin installed from that marketplace), or run them through `claude_outside_projects`.

## 2. Security posture

The change mostly removes attack surface:

- an upstream install script fetched and executed by `make update`
- a third-party plugin and its pin
- one removable root of a deletion lever

The new retirement step fails closed on every read and command, takes values from a strict record reader, and verifies the marketplace identity before removing it. Its one unresolved question is the project-directory working directory above.

## 3. Confirmed findings

None.

## 4. Confirmed finding details

None.

## 5. Needs validation

No `needs_validation` record. The only open lead is the unvalidated candidate in section 1. It is not a record, because independent validation could not run.

## 6. Hardening notes and positive patterns

These are not findings.

Hardening notes (parent hunt):

- A `managed`-scope record, which the reader accepts (pin_records.py:60), makes `retire_understand_anything` fail with `unexpected installation scope` on every `make update` until the record changes. Consider reporting managed scope as not ours.
- `make update` deletes the plugin cache and marketplace clone through chezmoi before the uninstall runs (Makefile:124, 133). If the CLI refuses to uninstall a plugin whose files are gone, every `make update` fails on that host. The coordinator's post-merge host proof observes this.
- `claude plugin marketplace remove` also uninstalls any other plugin the operator installed from the same marketplace by hand. The step names only understand-anything in its output.
- If the retirement step fails or is skipped (no `claude`), nothing disables the plugin any more, now that its pin is gone. Disabling it at user scope before the uninstall would keep the fail-closed property the pin convergence had.

Positive patterns:

- Every read in the new step is captured with its status checked.
- Scope is an enum from the strict reader.
- Plugin id and marketplace name are constants.
- The arithmetic loop bound comes from `jq length` over trusted output.
- The marketplace is removed only when registered from the recorded source.
- `.chezmoiremove` rows are literal, with no globs.
- The deletion lever's allowlist only shrinks.
- No secret, `eval` or new download is added.

## 7. Coverage summary (coverage-ledger.json, 26 units)

| Ledger status | Count | Units |
| --- | --- | --- |
| covered | 13 | All in scope. |
| candidate | 1 | The unvalidated candidate above. |
| blocked | 0 | — |
| deferred | 0 | — |
| out_of_scope | 12 | `.claude`, `.github`, `.orchestration`, `.ua`, `docs`, `install`, `plans`, `vendor`; the unchanged paths of `home`, `scripts` and `tests`; the repository root files. |

- **Excluded companions:** AI-AND-LLM, DESKTOP-MOBILE-AND-LOCAL-IPC, CLOUD-AND-DEPLOYMENT and WEB-PROTOCOL-AND-AUTH. None of their boundaries is in the changed paths.
- **Critic result:** no independent critic ran. A parent self-review added one unit (the test and lint-data edits) and widened the paths of the obvious-things unit. That self-review is not a critic pass.
