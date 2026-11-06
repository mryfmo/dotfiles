# Security audit: dotfiles at 56985c8909a53b53c4d49678b7b4f67d06ea2edc (U224 round-4 head)

## 1. Run, scope and limits

**This is a partial and incomplete pass.**

| Item | Value |
| --- | --- |
| Profile | `standard` |
| Scope | Scoped to the diff `c4195463..56985c89`: 27 changed paths, measured with `git diff --name-only`. The brief states 29, which does not match the measurement. |
| Out of scope | Every other top-level directory and the root files are recorded `out_of_scope` in the coverage ledger. |
| Source ref | `56985c89` on `feat/remove-understand-anything-graphify-in`, clean worktree. |
| Budget | None set. |
| Execution | Source review only. The brief forbids building, testing or executing target code, so every check is `method: source`. |

**Prior run.** The brief names the prior run as run-2, but this seat's only prior run is run-1 (U230, head `7992f1f5`); this run is run-2. From run-1:

- All 26 ledger units are carried with the same coverage IDs.
- Its findings.json held no record.
- Only `scripts/update-agent-assets.sh` and `tests/unit/test_update_agent_assets.py` changed since `7992f1f5`. Units touching them are changed-source revalidations. Every in-scope unit was re-read at this head.

**Carried lead.** run-1's one unvalidated candidate, `retire-understand-anything:project-scope-cwd`, ran `claude plugin uninstall` inside a recorded project directory. It is **resolved by the source change**:

- At this head the project and local branches only print a WARN (update-agent-assets.sh:2440-2443).
- Every `claude` call of the step goes through `claude_outside_projects` (2395, 2426, 2452, 2471).

**Incomplete, `run_status: "incomplete"`, reason `independent_agents_unavailable`.**

- The seat's tool policy denies the Task tool. This was probed again in this run.
- No reconnaissance, hunter, post-wave critic, final-clean critic or verifier agent ran. The parent did reconnaissance and hunting itself.
- The hunt produced no candidate, so no validation was owed. But the mandatory critics did not run, so this report makes **no clean-coverage claim**.

## 2. Security posture

The change removes attack surface:

- an upstream install script that `make update` fetched and executed
- a third-party plugin and its pin
- one removable root of a deletion lever

The new retirement step reads all its inputs (marketplace list, installation records, settings) before its first change. It acts only at user scope and only from an empty working directory. It uninstalls or removes only what the marketplace check proves is from the recorded source. When it cannot read the marketplace list, it changes nothing and warns.

## 3. Confirmed findings

None.

## 4. Confirmed finding details

None.

## 5. Needs validation

None.

## 6. Hardening notes and positive patterns

These are not findings.

Hardening notes (parent hunt):

- A `managed`-scope record, which the reader accepts (pin_records.py:60), still makes `retire_understand_anything` fail with `unexpected installation scope` (update-agent-assets.sh:2444-2447) on every `make update` until the record changes. Reporting it like project and local scope would match the step's own boundary.
- When the marketplace list cannot be read, the step changes nothing, including no disable (2402-2405). With the pin gone, nothing else disables an installed understand-anything on that host until the list works. The WARN says so, and `make doctor` warns for an enabled plugin without a pin (check-agent-runtime.py:928-929).
- `claude plugin marketplace remove` also uninstalls every other plugin the operator installed from the same marketplace by hand. The step names only understand-anything in its output.

Positive patterns:

- Every read is captured with its status checked, and every case has an error default.
- Constant plugin id, marketplace name and source.
- The scope enum comes from the strict reader.
- `projectPath` only reaches a WARN text.
- The arithmetic loop bound comes from `jq length` over trusted output.
- `.chezmoiremove` rows are literal, with no globs.
- The deletion lever's allowlist only shrinks.
- No secret, `eval` or new download is added (a scan of the diff's added lines).
- The 16 `RetireUnderstandAnythingTest` cases cover every failure branch except managed scope, which fails closed.

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
