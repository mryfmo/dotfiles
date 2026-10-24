---
task_id: dotfiles-T133-result-precheck-a04
round: 1
reset_of: dotfiles-T133-result-precheck-a03
status: result
---

# Report

Worker `claude-standard-dot-a009` (Claude Code, worker-c).

- Branch `tools/result-precheck-a01`, PR #411, continued from ddf262dec0db404ffc4ba5e1095842f2f17c7e6d. Merge base with `origin/main`: 740772ef.
- Commits:
  - a495ec55: the reset bookkeeping. `git rm` of the a03 task copy and the a04 copy.
  - af30d4a6: the eight hardening items and their regressions.
  - bf1bce63: amendment 1, the checker argv `--root <root> --premises-sha <sha> <task-file>` and the two `test_orchestrator_tools.py` expectations. It also carries amendment 1's task copy (sha256 `e52afb631043154c08f3bda8d217edd299ccd6d97b6fb72aa88b8e12f7328700`).
  - 9f6ec7c9: the one correction round after the worker's pre-push review. It is the code head.
  - The evidence commit is last.
- INV-6 for a04: amendments=1, which answered the blocked PONG of 01:20:05Z; questions=0; revises=0. The one pre-push correction round counts toward INV-6, as the Completion directs. The a01 to a03 history and counters stay as recorded.
- Parked PR of a01's item 0: #406.

Inherited, not re-derived here: the a01 to a03 records and their red baselines. Fresh: everything in this directory.

## Hardening

1. **Masking fails closed (security P1, `result-precheck.sh:251`).**
   - Each check's output is captured in the private work directory, then masked with both masker streams sent to `/dev/null`. Only the masked copy is published.
   - A failed masking lists the capture in `maskfail`, deletes it, and writes only `masking failed: exit <n>`. The check is recorded `ok: false`, and `result.txt` says `status=blocked`.
   - If that failure branch itself fails, nothing is published and the run stops.
   - Regression: `test_precheck_fails_closed_when_masking_fails`.
2. **No evidence through a symlink (security P1, `result-precheck.sh:278`).**
   - `evidence_ok` refuses when `.orchestration`, the task directory or any destination is a symlink, dangling included.
   - It runs before the startup cleanup, which now also removes a stale `precheck.json`, `result.txt` and `.publish.*` leftovers, and before every write.
   - `publish` writes through a `mktemp` file in the checked directory and renames it into place. This covers check logs, selector logs, `precheck.json` and `result.txt`.
   - Regression: `test_precheck_refuses_symlinked_evidence`.
3. **Bus identities (security P2, `dispatch.sh:171`).**
   - The prechecker receives the seat and the orchestrator, this ACCEPTANCE's own `to` and `from`.
   - A same-task RESULT counts only from the seat to the orchestrator; any other same-task line counts only from the orchestrator to the seat. Other rows are ignored, and a `dispatch: note:` gives only their count.
   - The orchestrator's newest TASK row for the task, if the window holds it, must name the same seat. Without one, a note says the pair is the ACCEPTANCE's own.
   - Filtering precedes ordering, status, selectors and baseline.
   - Regression: `test_dispatch_ignores_messages_from_unregistered_identities`.
4. **The fixture's own HOME (security P2, the test module's setUp).**
   - `setUp` sets HOME to a directory inside the fixture's temporary directory, sets `GIT_CONFIG_NOSYSTEM=1`, and drops inherited `GIT_*`, `XDG_CONFIG*` and `UV_*` variables before adding its own.
   - Regression: `test_precheck_fixtures_isolate_home`. It probes the committed fixture through `git show HEAD:…`, so copying the module into another tree cannot repair it.
5. **Blob paths confined (audit P2, `result-precheck.sh:103`).**
   - `scan_one` refuses an empty path, a leading `/` or any `..` segment before any directory exists.
   - The correction round also refuses a `--blob` rev starting with `-` and passes `--end-of-options` to `git show`.
   - Regression: `test_blob_scan_rejects_paths_outside_scan_directory`.
6. **Masking on an early exit (audit P2, `result-precheck.sh:235`).**
   - The EXIT trap, installed before any capture, masks and publishes the captures by the same rules when the normal path has not, then removes the proof worktree and the work directory. A nonzero status is kept.
   - Regression: `test_precheck_masks_logs_when_proof_worktree_creation_fails`, with a working and a failing masker, starting from a complete earlier record.
7. **The code head (the shared P2).**
   - `precheck.json` adds `code_head`, equal to `head`, and `result.txt` adds `precheck_head=`.
   - The acceptance check requires one 40-hex `precheck_head=`, both commits present, the record's `head` and `code_head` equal to it, and its `tree` equal to that commit's tree.
   - It then walks the first-parent chain from the code head to the RESULT head. A single-parent commit must change only `.orchestration/<task>/`.
   - A merge passes only when all of these hold:
     - its tree equals `git merge-tree --write-tree` of its parents;
     - its second parent is an ancestor of `origin/main`;
     - its diff from the first parent leaves the task's code entries alone. The entries are the non-`.orchestration/` `allowed_files` of the task copy at the code head.
   - Regression: `test_dispatch_binds_precheck_to_code_head_across_update_branch`.
8. **C14 wiring (the P1-12 a02 RESULT).**
   - The TASK-side checker call is `--root <root> --premises-sha <the line's task_sha256> <task-file>` (amendment 1), and a passing checker's `C14:` lines go to stderr.
   - A `task_sha256` mismatch keeps its refusal and adds `dispatch: C14: not run (no trusted sha)`.
   - Regression: `test_dispatch_passes_the_task_sha_to_c14_and_forwards_warnings`, using a fake checker that keeps P1-12's C14 contract.

Files items 1 to 7 are retained from a03: per-blob scanning, staged checks, revise ordering, home-path scope, exact-id proofs and the clean-tree query.

## Tests

`tests/unit/test_result_precheck.py` adds the eight named regressions above. Each is red against ddf262de with this head's test source: exact id, `Ran 1 test`, failures only, no error. Each is green on 9f6ec7c9 (validation.md).

The correction round's cases are red against bf1bce63: the evil merge, the narrowed task copy, the stale record, the rev option and the intruder's TASK row.

Retained regressions, replayed with this head's source:
- a03's four item 5 to 7 tests, red against 4ed1b27a;
- the three revise-1 tests, red against 9cd5514a;
- a03's revise-1 tests keep their red evidence against bccb2dea in a03's validation;
- all green here.

`tests/unit/test_orchestrator_tools.py` (amendment 1): its two expected argv strings gain `--premises-sha <sha of the task file>`. Its stub, unchanged, still reads the file as the last argument.

Consolidated so the eight regressions fit the cap, without dropping an assertion:
- the `git()`, `run_script()` and setUp environment helpers in short forms;
- one `proofs()` helper for the two previous-head proof tests;
- a `UNITS` constant for the four malformed `ok` cases;
- `gated()` reused;
- a `TOKEN` constant;
- `write()` takes bytes, for `push()`;
- single-line provenance comments, and trailing comments in place of helper docstrings.

## Caps

`git diff --numstat` against the merge base 740772ef, on the code head 9f6ec7c9: 482 changed lines outside `tests/` and `.orchestration/` (cap 500) and 617 under `tests/` (cap 640), with amendment 1's caps. The changed files outside `.orchestration/` are:
- `.githooks/pre-commit`
- `.githooks/pre-push`
- `scripts/orchestrator/dispatch.sh`
- `scripts/orchestrator/result-precheck.sh`
- `tests/unit/test_orchestrator_tools.py`
- `tests/unit/test_result_precheck.py`

## Feedback dispositions

- **The security-profile review of ddf262d:**
  - P1 `result-precheck.sh:251` (masking): fixed:af30d4a6, hardening 1. The branch hardened in 9f6ec7c9.
  - P1 `result-precheck.sh:278` (symlinks): fixed:af30d4a6, hardening 2. The stale-record cleanup added in 9f6ec7c9.
  - P2 `dispatch.sh:171` (identities): fixed:af30d4a6, hardening 3. TASK-row parsing in 9f6ec7c9.
  - P2 the test module's HOME: fixed:af30d4a6, hardening 4. The `GIT_*` and `UV_*` filter in 9f6ec7c9.
  - P2 `precheck.json:2` (code head): fixed:af30d4a6, hardening 7. The evil-merge and tested-copy rules in 9f6ec7c9.
- **The task-level audit of ddf262d:**
  - P2 `result-precheck.sh:103` (blob path): fixed:af30d4a6, hardening 5.
  - P2 `result-precheck.sh:235` (early exit): fixed:af30d4a6, hardening 6.
  - P2, the stale precheck after the update-branch merge: hardening 7.
- **The P1-12 a02 RESULT's dispatch wiring:** fixed:af30d4a6 and bf1bce63, hardening 8 with amendment 1.
- **Bot review 5561676646 of a01, on 1763da66, three threads:**
  - 4305945403 [P1] scan every pushed commit: fixed:a7b0da2f.
  - 4305945407 [P1] reject failed precheck records at acceptance: fixed:a7b0da2f.
  - 4305945406 [P2] staged checks read the index: fixed:bdd8ab81.

  Their tests are retained and green here. The orchestrator replies and resolves.
- **The worker's pre-push review of bf1bce63:** the P2 and five of the P3 are fixed in 9f6ec7c9, and one P3 is the orchestrator's (the `-worker-crit.json` here).
- **CI on the first push (bf1bce63), three causes:**
  - `validate`: a `<redacted:secret-pattern> + …` fixture constant from my own test consolidation matched the repository's secret pattern. The precheck's `secrets` check also caught it. fixed:9f6ec7c9, by renaming it to `FAKE_CREDENTIAL`.
  - Ubuntu `test`, the ShellCheck step: CI's ShellCheck 0.9 reports SC2317 for `check_secrets` and `check_local_review`, which `run_check` calls indirectly. The directive named only 0.11's SC2329. fixed:9f6ec7c9, by disabling both codes.
  - `regime`: the job runs the base's `scripts/orchestrator/regime-ci.py`, which the merge base 740772ef predates. Every PR on that base fails it until the orchestrator's planned update-branch.
- **This push:** no `@codex review` is posted. CI on the final head and the 15-minute Bot window are in the RESULT line.

## Observations for the orchestrator (no change made)

- **Merge order:** main's `task-consistency-check.py` rejects `--premises-sha` until PR #417 lands. If #411 merges first, every non-review TASK dispatch is refused. Amendment 1 fixes the order: #417 and #423 before #411.
- **Fresh proof after #423:** the update-branch merge that brings #423's edits to `tests/unit/test_orchestrator_tools.py` changes one of this task's code entries. The acceptance check will then ask for a fresh precheck on the new code head, as designed.
- **Seat registry:** the identity pair is this ACCEPTANCE's own argv, cross-checked with the orchestrator's TASK row when the 200-row window holds it. dispatch.sh reads no seat registry, and a TASK row that has aged out leaves only a note.
- **Git version:** `git merge-tree --write-tree` needs Git 2.38 or later. Seats and CI run 2.39 or later.
- **The trap after a syntax error:** the EXIT trap keeps `$?`. After a bash syntax error that is the last command's status, so a run whose script was edited under it ended `exit=0` with no record. It happened here once, when my edit to `result-precheck.sh` corrupted a running default run. It is reachable only by changing the script mid-run.
- **A leftover private work directory:** `/tmp/claude-501/result-precheck.UsWK1Z`, from the stopped first default run, was not removed. The `rm -rf` was denied at the permission prompt (sandbox.md).

[memory:decision] T133 P1-5 a04: result-precheck.sh captures privately and publishes only masked copies through symlink-checked, same-directory temporary files (a failed masking leaves only `masking failed: exit <n>`), masks in the EXIT trap, confines --blob paths and revs, and records code_head and precheck_head; dispatch.sh counts only the ACCEPTANCE's own sender and recipient pair, binds the precheck to its code head (evidence commits, or clean update-branch merges from origin/main that leave the tested copy's code entries alone), and passes the TASK's task_sha256 to the checker as --premises-sha.

## The Check (validation.md)

- **Shell and render:** shellcheck and `shfmt -d -i 4 -sr` on the four scripts are clean, and `make render-check` exits 0.
- **`make format`:** exits 2 at `shfmt --diff .` with the same twelve pre-existing files as the merge base 740772ef. CI's three formatting commands in their scopes pass (the precheck's `format` check).
- **The default precheck run on 9f6ec7c9:** it exits 1 on `unit-test` alone.
  - Its 322 failing names are the merge base's in the same sandbox, but for two timing tests outside this task's modules.
  - One fails only on the branch and passes alone; the other fails only on the base.
  - render-check, format, shellcheck and secrets pass.
- **The final proof:** `result-precheck.sh dotfiles-T133-result-precheck-a04 --tests tests.unit.test_result_precheck tests.unit.test_orchestrator_tools --previous-head ddf262de… --check` with the eight selectors exits 0, with `precheck=2b921eb17de04c8232f83210a13a278b0147aba13b0a7aedd2d09363638db2cd` and `precheck_head=9f6ec7c9`.
  - The record's head, `code_head` and tree are 9f6ec7c9's.
  - The five executed checks are `true`, and `local-review` is the exact deferred record.
  - Each of the eight selectors has `Ran 1 test` on both heads, exit 1 then 0.

## Still to come

The evidence commit, the push, CI on the final head, the Bot window and the RESULT. Done at the time; see the a04 RESULT of 03:31:54Z.

cost: n/a

## Rebase repair 1 (ACCEPTANCE status=rebase-repair, 2026-10-19T11:51:18Z)

- **What failed:** the orchestrator's update-branch merged main `51ba5801` into the branch (`f461d607` → `15380731`). All four required unit jobs then failed at "Run Python unit tests" (run 39245744533). The failing test is the same in each: `tests/unit/test_lint_comparisons.py::test_the_changed_files_are_clean_against_the_baseline`, `(0, '') != (1, '')`. The one changed-file hit was `scripts/orchestrator/result-precheck.sh:127: R1` (validation R1).
- **The cause is a check that landed on main after `f461d607`:** PR #415's changed-file comparison lint. It applies to this PR's own files, and flagged `scan_one`'s string-form confinement `[[ -n $2 && $2 != /* && /$2/ != */../* ]]`. That makes this order (2), a repair, not order (3).
- **The repair, `d3eb4249`:** the confinement runs through `python3 -I -c` with `os.path.normpath`, a normaliser R1 names. It is as strict as before or stricter. It refuses an empty path, an absolute one, one that normpath would change (any `.` or `..` segment, or a doubled `/`), and one starting with `..`. Ten cases are probed in validation R4. `test_blob_scan_rejects_paths_outside_scan_directory` stays green. No baseline row was added, so `scripts/lint-comparisons-baseline.tsv` is untouched.
- **Red, then green:** the failing selector is red at `15380731`, with the same R1 hit CI printed, and green at `d3eb4249`, both inside the sandbox (R3). The two task modules and the lint tests pass, 97 tests. The lint gate exits 0, and ShellCheck and shfmt are clean (R4).
- **The precheck:** it was re-run at `d3eb4249` with the final proof's arguments and exits 0 with `precheck=b997a902e29140c8fed7b47a5dd71659524346d7b67391d3722838bd4279e531`. The record's head, `code_head` and tree are `d3eb4249`'s, and each of the eight selectors exits 1 at `ddf262de` and 0 here (R5). The regenerated `precheck.json`, `result.txt` and `precheck-*.log` replace the 9f6ec7c9 ones.
- **Caps against the new merge base `51ba5801`:** 484 of 500 and 617 of 640 (R6).
- **Sequencing:** the a04 work (`dotfiles-T129-assets-omp-hcom-followup-a04`, PR #430) was committed and pushed before the switch to this branch.
