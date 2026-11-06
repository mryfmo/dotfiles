# Security audit: dotfiles at d1fd54ba5f5772eee06693d3f44182d4ae7c1427 (U244 head)

## 1. Run, scope and limits

**This is a partial and incomplete pass.**

| Item | Value |
| --- | --- |
| Profile | `standard` |
| Scope | Scoped to the U244 change, `d1ecd495..d1fd54ba`: 9 paths, +214 −798. |
| Out of scope | Every other area is recorded `out_of_scope` in the coverage ledger. |
| Source ref | `d1fd54ba`, clean worktree. |
| Budget | None set. |
| Execution | Source review only. The brief forbids executing target code, so every check is `method: source`. |

**Brief corrections.**

- The brief's CONTEXT line names `git diff --name-only c4195463 HEAD` (29 paths). That is the U224 sweep's text, and it measures 10 paths here. This run follows the GOAL and CHANGE (the U244 change against `d1ecd495`).
- The brief names the prior run as run-4, but this seat's previous run is run-3 (U236, the U224 head `dfb763ce`); this run is run-4.

**Prior run.**

- run-3's 26 units are carried with the same IDs as `out_of_scope`. Its 14 U224 units cover source that is not in this head, and its 12 area units are unchanged.
- There is no prior record.

**Incomplete, `run_status: "incomplete"`, reason `independent_agents_unavailable`.**

- The seat's tool policy denies the Task tool, so no reconnaissance, hunter, critic or verifier agent ran. The parent did reconnaissance and hunting itself.
- The hunt produced no candidate, so no validation was owed. But the mandatory critics did not run, so this report makes **no clean-coverage claim**.

## 2. Security posture

U244 makes the merge gate strictly stronger.

**Before:** the lever read the unit's brief and let a unit whose brief had no `TRUST` section merge without a sweep row.

**Now:** every unit needs the exact sweep row of the Audit rule at the audited head. That means:

- verifier `security-audit-skill <pin>`, with the pin word a prefix of the manifest pin
- a findings file `sweeps/<path>.json` that is a regular file of this user under the store

The deleted reading also removes the lever's execution of the checkout's `brief-check.py` code. No input lost a refusal:

- The body's `Program-Unit:` line, the ledger reader, the pin probe, the findings-file stat and the CI reads are unchanged.
- A body cannot borrow another unit's sweep, because the verdict row's unit must be the body's unit or a fix unit of it.

## 3. Confirmed findings

None.

## 4. Confirmed finding details

None.

## 5. Needs validation

None.

## 6. Hardening notes and positive patterns

These are not findings.

- **Hardening:** none from this change.
- **Positive patterns:**
  - Every reader's status is mapped 0/2/other, and a failed read is never "no row".
  - The answer is read by its shape.
  - Store paths are checked for no symlink and same owner.
  - The findings file is stat'ed, never opened.
  - The one write is `gh pr merge --squash --match-head-commit`.
  - Both lever copies are byte-identical (`git hash-object` `4c832922…`), and their sha256 `5e235e90…` is the manifest's levers pin.
  - Only brief-probe tests were removed. Every sweep-row, pin and findings-file test remains (test_pr_merge.py:164-366), and two tests pin the new rule (132, 150).

## 7. Coverage summary (coverage-ledger.json, 34 units)

| Ledger status | Count | Units |
| --- | --- | --- |
| covered | 8 | All in scope: the sweep gate, the body's store and unit selection, the pin probe, the removed brief reading, the deployed copy and its pin, the policy text, the tests, and obvious things over the diff. |
| candidate | 0 | — |
| blocked | 0 | — |
| deferred | 0 | — |
| out_of_scope | 26 | Carried from run-3: 14 U224 units and 12 area units, namely `.claude`, `.github`, `.orchestration`, `.ua`, `docs`, `install`, `plans`, `vendor`, the unchanged paths of `home`, `scripts` and `tests`, and the root files. |

- **Excluded companions:** AI-AND-LLM, DESKTOP-MOBILE-AND-LOCAL-IPC, CLOUD-AND-DEPLOYMENT and WEB-PROTOCOL-AND-AUTH.
- **Critic result:** no independent critic ran. No clean-coverage claim is made.
