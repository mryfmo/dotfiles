# Security audit: dotfiles at dfb763ce526b6cb2119ffa286b297fba5b289ed3 (U224 round-5 head)

## 1. Run, scope and limits

**This is a partial and incomplete pass.**

| Item | Value |
| --- | --- |
| Profile | `standard` |
| Scope | Scoped to the diff `c4195463..dfb763ce`: 27 changed paths, measured with `git diff --name-only`. The brief states 29, which does not match the measurement. |
| Out of scope | Every other top-level directory and the root files are recorded `out_of_scope` in the coverage ledger. |
| Source ref | `dfb763ce` on `feat/remove-understand-anything-graphify-in`, clean worktree. |
| Budget | None set. |
| Execution | Source review only. The brief forbids building, testing or executing target code, so every check is `method: source`. |

**Prior run.** The brief names the prior run as run-3, but this seat's previous run is run-2 (U233, head `56985c89`); this run is run-3. From run-2:

- All 26 ledger units are carried with the same coverage IDs.
- Its findings.json held no record and its ledger no candidate.
- Only `scripts/update-agent-assets.sh` and `tests/unit/test_update_agent_assets.py` changed since `56985c89`. The marketplace removal gained `--scope user --json`, and three tests were added.
- Units touching those files are changed-source revalidations, re-read with their lines re-mapped. Every other in-scope unit was re-read too.

**Incomplete, `run_status: "incomplete"`, reason `independent_agents_unavailable`.**

- The seat's tool policy denies the Task tool (probed in run-2, unchanged).
- No reconnaissance, hunter, post-wave critic, final-clean critic or verifier agent ran. The parent did reconnaissance and hunting itself.
- The hunt produced no candidate, so no validation was owed. But the mandatory critics did not run, so this report makes **no clean-coverage claim**.

## 2. Security posture

The change removes attack surface:

- an upstream install script that `make update` fetched and executed
- a third-party plugin and its pin
- one removable root of a deletion lever

The retirement step reads all its inputs before its first change. Every `claude` call runs from an empty directory, and every command that changes state names `--scope user`. The round-5 head closes the earlier gap where an unscoped `marketplace remove` dropped project and local declarations and installation records. The step removes only what the marketplace check proves is from the recorded source, and changes nothing when it cannot read the marketplace list.

## 3. Confirmed findings

None.

## 4. Confirmed finding details

None.

## 5. Needs validation

None.

## 6. Hardening notes and positive patterns

These are not findings.

Hardening notes (parent hunt):

- A `managed`-scope record, which the reader accepts (pin_records.py:60), still makes `retire_understand_anything` fail with `unexpected installation scope` (update-agent-assets.sh:2447-2450) on every `make update` until the record changes. Reporting it like project and local scope would match the step's own boundary.
- When the marketplace list cannot be read, the step changes nothing, including no disable (2405-2408). With the pin gone, nothing else disables an installed understand-anything on that host until the list works. The WARN says so, and `make doctor` warns for an enabled plugin without a pin (check-agent-runtime.py:928-929).
- A marketplace declared only at project or local scope is listed like a user one, so it gets a refused `remove --scope user` and a WARN (2458-2459). The stale-entry disable (2471) then does not run, because the state is `registered`, not `absent`. A stale user `enabledPlugins` entry beside such a declaration is left for `make doctor` to report.
- `claude plugin marketplace remove` also uninstalls every other plugin the operator installed from the same marketplace by hand. The step names only understand-anything in its output.

Positive patterns:

- Every read is captured with its status checked, and every case has an error default.
- Constant plugin id, marketplace name and source.
- The scope enum comes from the strict reader.
- `projectPath` only reaches a WARN text.
- The removal's `--json` result line is read only for `failureCode` against the literal `not_configured`.
- A structural test asserts the `--scope user` allowlist over the function's text (test_update_agent_assets.py:4162).
- `.chezmoiremove` rows are literal, with no globs.
- The deletion lever's allowlist only shrinks.
- No secret, `eval` or new download is added (a scan of the diff's added lines).

## 7. Coverage summary (coverage-ledger.json, 26 units)

| Ledger status | Count | Units |
| --- | --- | --- |
| covered | 14 | All in scope. |
| candidate | 0 | — |
| blocked | 0 | — |
| deferred | 0 | — |
| out_of_scope | 12 | `.claude`, `.github`, `.orchestration`, `.ua`, `docs`, `install`, `plans`, `vendor`; the unchanged paths of `home`, `scripts` and `tests`; the repository root files. |

- **Excluded companions:** AI-AND-LLM, DESKTOP-MOBILE-AND-LOCAL-IPC, CLOUD-AND-DEPLOYMENT and WEB-PROTOCOL-AND-AUTH. None of their boundaries is in the changed paths.
- **Critic result:** no independent critic ran. No clean-coverage claim is made.
