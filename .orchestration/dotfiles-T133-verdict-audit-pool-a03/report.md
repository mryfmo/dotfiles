---
task_id: dotfiles-T133-verdict-audit-pool-a03
seat: claude-standard-dot-a008
branch: tools/verdict-audit-pool-a01
pr: 410
reset_of: dotfiles-T133-verdict-audit-pool-a02
previous_head: b8998de162afc72d53d07679b8f0a194fcc480ff
base: 3e41e36a
split_commit: 0e16d7eb
test_commit: f8f5da79
fix_commit: 8f22dd9d
review_commit: 8b0b5bb4
code_head: cac07914
revise_1_previous_head: 513e5d0532ec3c21484ab215ef77fea440329749
revise_1_commits: 51abdb1c a19a0eba 32e4d2fb cac07914
parked_pr: 407
task_sha256: 2f0493944badef8294dc691e87fba7ab6cc84ed2d6e135454a34b1219f724c42
---

# Report: dotfiles-T133-verdict-audit-pool-a03 (INV-6 reset of a02, the verdict half of the P1-4a split)

- **Seat and task file:** `claude-standard-dot-a008` in `.claude/worktrees/worker-f`. The AGMSG-TASK arrived at 2026-10-19T00:39:47Z with `task_sha256=2f049394…`. The dispatched file and the branch copy `.orchestration/dotfiles-T133-verdict-audit-pool-a03/task.md` are byte-identical (validation §1). The task-consistency check passes (§1a).
- **Branch:** PR #410 continues on `tools/verdict-audit-pool-a01` from `b8998de1`. It was fetched as one command and switched to locally; sandbox.md records the refused upstream write.
  - No new branch or PR was made. Draft PR #407 stays parked, and the parking step was not repeated.
  - This seat's branches for #423, #418 and #415, and the other seat's `verdict-audit-pool-a02-a011`, are untouched.

## The split (first push; §3, §3a)

`0e16d7eb` makes these changes:

- deletes `.orchestration/dotfiles-T133-verdict-audit-pool-a02/task.md`;
- adds the byte-identical a03 copy;
- removes `scripts/orchestrator/audit-pool.sh`, `.schemas/classes.yaml` and `tests/unit/test_audit_pool.py`;
- restores `scripts/orchestrator/orch-audit.sh` to origin/main.

These are the task's named split-bookkeeping exceptions. Every later edit is within `allowed_files`.

Outside `.orchestration/`, the cumulative diff now holds exactly the four allowed files (§3a): `scripts/orchestrator/verdict.sh`, `.schemas/verdict.json`, `.schemas/audit.json` and `tests/unit/test_verdict.py`.

The a01 and a02 record directories, other than the a02 task copy, are still in the PR diff with their original identifiers and tested heads. The task gives their removal from the cumulative diff to the orchestrator as reset bookkeeping, so this seat leaves them in place.

## Items 6 and 7: the two b8998de findings, each red at b8998de1 and green after the fix

| Item | Change in `scripts/orchestrator/verdict.sh` | Regression (red: §4; green: §5) |
|---|---|---|
| 6 (P1) | After accept and the four-distinct-PR shadow unlock, `--apply` runs the trusted `"${here}/orch-gate.sh" <task> <head> <pr>` before any effect. A missing gate (exit 127), a refusal (exit 2) or any nonzero exit turns the verdict into `hold` with exit 20, writes the verdict JSON as `hold`, and calls neither `dispatch.sh` nor `gh pr merge`. The gate interface is unchanged. The real wrapper takes a PR worktree in its second position and so refuses the head form, which keeps live application on hold, as the task states. | `test_verdict_apply_runs_the_integration_gate_before_dispatch_or_merge_and_holds_on_failure`. Its cases: a fake gate's failure, a refusal, a gate missing from origin/main and the checkout alike (so past the `--apply` guard), and a zero-exit control. Each failing case asserts no dispatch and no merge, exit 20 and a `hold` verdict JSON. The control asserts the exact order `gate t1-a01 <head> 9`, then dispatch, then `gh pr merge 9 --squash --match-head-commit <head>`. |
| 7 (P2) | Each cap limit is its last declaration in the task text (`tail -n 1`, with the greedy sed taking the last one on a line): `at most <n> changed lines outside` and `<n> under tests/`. The exclusions come from the last `at most` sentence. A later test-only amendment therefore replaces the test limit and keeps the outside limit. | `test_verdict_condition_5_honors_the_latest_amended_caps`. The fixture has 531 changed test lines, with the precheck and head rebuilt so every other condition stays green. Its cases: the original 500 alone revises; a later amendment allowing 550 accepts; the a02 test-only amendment wording accepts; a later lower limit (550, then 520) revises; the effective sentence's exclusions accept; the effective sentence's outside limit revises. |

## The split's schema checker (item 2)

The stdlib checker that `b8998de1` kept in the sibling's `orch-audit.sh --validate` moves into `verdict.sh`. It is the same predicates over the same JSON Schema 2020-12 subset, run as `"${VERDICT_BIN}/python3" -I` after the pinned re-exec, with no new file or dependency.

- **Coverage:** required keys, types, booleans as non-integers, enums, bounds, `$`-anchored patterns read as `\Z`, `maxLength`, additional properties, and RFC 3339 date-times with an offset.
- **Equivalence:** validation §6 runs b8998de1's checker and this one on 35 cases: valid records, each kind of schema violation, date-only, naive and impossible-date timestamps, unreadable JSON, and `format` without `type`. The exit status and message are identical on every case.
- **`--validate <schema> <json>`:** the checker's entry point, the inherited one's replacement. It runs after the pinned re-exec and the `--admin`/`--auto` refusal. The output-schema test calls it.
- **Test double:** the tests supply a minimal `orch-audit.sh` double, used only when the test file runs against b8998de1 (§4), so each regression reaches its named defect there.

## Retained fixes (items 3 to 5)

Every retained test name is present, and the whole module is green at the code head (§5): 17 tests, the 14 retained, the two regressions and the worker review's per-rule test. Their historical red results stay with their original heads in the a01 and a02 records. They are rerun here only for green.

- **Interpreter and tool pinning:** `test_verdict_pins_tools_interpreter_and_environment_before_reading_a_pr_checkout`.
- **Numeric open P0/P1 count:** `…counts_open_p0_p1_findings_even_when_the_id_is_empty`.
- **Condition 4:** the head equality, null-URL, identity and multiplicity, and disposition-validator tests.
- **The loop refresh.**

## Schemas and caps (§7, §10)

- **Schemas:** `.schemas/audit.json` (13 lines) and `.schemas/verdict.json` (12 lines) are reformatted with fewer line breaks. Their parsed content equals b8998de1's (§7), so the class enum keeps the b8998de1 vocabulary.
- **Size, over merge-base 3e41e36a...HEAD (§10):**
  - Outside `tests/` and `.orchestration/`: 298 of 300 (`verdict.sh` 273, `audit.json` 13, `verdict.json` 12).
  - `tests/`: 393 of 400.
  - `verdict.sh` alone: 273 of 300 lines.
- **Compaction:** `verdict.sh` was compacted only by joining lines (the argument parsing, the record lookup, the numstat loop, merged declarations, one-line Python ifs). No check, condition, case or assertion was removed.

## Check (§8, §9)

- **The Check's script commands:** `shellcheck scripts/orchestrator/verdict.sh` and `shfmt -i 4 -sr -d scripts/orchestrator/verdict.sh` are clean. `uv run python -m unittest tests.unit.test_verdict -v` is green (§5). `make render-check` exits 0.
- **`make format` exits 2 here.** The cause is inherited. It flags the same 12 files at the merge-base `3e41e36a` as at HEAD, with shfmt v3.14.1 (§8a): ten `.orchestration/tasks/*-input/*.sh` files, `executable_project-map-reload.sh` and `brew.bats`. None of them is this PR's, and `verdict.sh` is clean.
- **`make unit-test` exits 2 in this seat's sandbox, at HEAD and at the merge-base alike, so the failures are inherited, not passing.**
  - Both runs end with `failures=195, errors=111`: 1224 tests at HEAD (§9b) and 1207 at the base (§9a). The difference of 17 is the verdict module.
  - The per-module failure lists differ in only two timing tests, one in each run: `test_agmsg_dispatch…test_timeout_is_one_shared_budget` at HEAD and `test_herdr_agents…test_session_start_attach_bounds_a_trickling_hook_payload` at the base. They ran while two full suites shared the machine, and each passes alone at HEAD (§9d).
  - The failing modules are environment-bound in this sandbox: commit signing whose key read the sandbox denies, `mktemp` and `TMPDIR`, herdr and network. §9c reruns the suite at HEAD with signing off and `init.defaultBranch=main`. `test_require_crit_review` and `test_ua_symbol_coverage` then pass, and 91 failures and 10 errors remain in the other sandbox-bound modules.
  - CI's `test` jobs run the suite in their own environment.
- **The shadow invocation (§11):** `scripts/orchestrator/verdict.sh --shadow 410 --task dotfiles-T133-verdict-audit-pool-a03` ran at `8b0b5bb4`, which was then PR #410's head. It returned hold, exit 20, as the Check expects before the audit and the acceptance evidence exist. The JSON is pasted in §11. The later records-only commit changes no code.

## Worker review

The worker review is recorded in `dotfiles-T133-verdict-audit-pool-a03-worker-crit.json` and its receipt. There was one pre-push round, the task's limit, covering `b8998de1..8f22dd9d`. It returned `Verdict: correct`, with one P2 and three P3.

- **P2, fixed in `8b0b5bb4`:** the split had left the moved checker's rejecting cases behind in the deleted `test_audit_pool.py`, and eight one-rule mutants of the checker survived. `test_verdict_validate_refuses_each_rule_the_moved_schema_checker_holds` runs `verdict.sh --validate` on a valid audit and on one violation per rule, and kills all ten mutants (§6a).
- **P3, fixed in `8b0b5bb4`:** the usage line now names `--validate`.
- **P3, residual (cap declarations ignore the range a cap names):** item 7 prescribes the last declaration in text order. The reviewer's scan of 562 task files finds one text where this is stricter than intended: the T129 audit-inherit re-plan's 60/120, which names its own range. That case revises; it never accepts falsely. PR #410's own Check parses to 300/400 under both rules.
- **P3, residual (hour 24):** the retained checker accepts `T24:00:00Z` through `fromisoformat`, exactly as b8998de1's did. Item 2 retains the existing behaviour.
- **Note for the orchestrator:** the a01 and a02 record directories are still in the cumulative diff, outside `allowed_files`. The task gives their removal to the orchestrator.

## CI and Bot

- **CI on `8b0b5bb4`:** all seven required checks pass, along with `test (ubuntu-26.04, client)`, CodeRabbit (its review is skipped by the repository setting) and GitGuardian.
- **The new, non-required `regime` check fails:**
  - **Cause:** #418, merged as `0e496ce7` after this PR's recorded base `3e41e36a`, runs from main but checks out the PR's base sha. `regime-ci.py` does not exist at `3e41e36a`, so the job exits 2 with "can't open file …/scripts/orchestrator/regime-ci.py" (run 39188822522). It is not this PR's code.
  - **Remedy:** either of two, both outside this task's `allowed_files` and effects. The orchestrator's `gh pr update-branch 410` gives the PR a base that has the verifier. Or the #418 lineage makes the job skip, with a warning, a base that predates its verifier.
- **Bot:** none. PR #410 was already ready when pushed, and only the CodeRabbit skip notice appeared in the 15 minutes after the push at 02:11Z.

## Revise 1 (AGMSG-ACCEPTANCE status=revise round=2, 2026-10-19T05:34:59Z; previous head 513e5d05)

The security review of the update-branch head `513e5d05` found two P1 and one P2. They are fixed in one round, the INV-6 cap with the pre-push round (C-61).

| Item | Fix | Check (red: validation R2; green: R3; mutants: R4) |
|---|---|---|
| (1) P1 `verdict.sh:36`: a caller-supplied `VERDICT_BIN` and matching `PATH` bypassed `env -i`, so inherited functions and tool-selection variables ran with the operator's authority | **Before any command:** every inherited function is unset (`compgen -A function`). **The pinned state** is honoured only when it is exactly what the re-run builds: `PATH` is `VERDICT_BIN:/usr/bin:/bin`, no exported name outside HOME, TMPDIR, PATH, VERDICT_BIN, PRECHECK_REQUIRED and bash's own, and every entry of `VERDICT_BIN` a link to an absolute path outside a shims directory. **Otherwise** it is rebuilt under `env -i`. The resolution's search path then drops the caller's `VERDICT_BIN` and any empty entry, so a caller's bin never selects a tool. | `test_verdict_ignores_caller_bin_and_path_overrides`, with three cases. **An exported `git` function** beside a clean caller-made pinned state is unset, and the run accepts. **A tool-selection variable (`UV_PYTHON`)** with a caller's bin linking a planted `python3` forces a rebuild without that bin, and holds. **A copied (not linked) planted `python3`** in a clean caller's bin is no pinned state, and holds. None leaves the planted marker. At `513e5d05` all three fail: the function and the planted interpreter both ran. |
| (2) P1 `verdict.sh:168`: the condition-4 import of `require-crit-review.py`, and of the validator it loads, could execute cached bytecode from the ignored `scripts/__pycache__` (`-B` stops writes, not reads) | Condition 4 holds while `scripts/__pycache__` exists; both modules load from that one directory. The import snippet sets `sys.dont_write_bytecode` beside `-I -B`. `PYTHONDONTWRITEBYTECODE` is not added: `-I` makes Python ignore it, and every Python run here is `-I`. | `test_verdict_never_imports_cached_bytecode`: an unchecked-hash `.pyc` for `require-crit-review.py`, compiled by the interpreter verdict pins, never runs, and the verdict holds, naming `scripts/__pycache__`. At `513e5d05` the planted bytecode ran. |
| (3) P2: 17 predecessor artifacts in the PR tree | `cac07914` deletes `.orchestration/dotfiles-T133-verdict-audit-pool-a01/` and `-a02/` (16 files; the a02 task copy left in the first push). The orchestrator keeps the records. | R6: the cumulative diff is the four allowed files and this task's records. |

- **Caps (R7):** outside `tests/` and `.orchestration/`, 299 of 300: `verdict.sh` 278, `audit.json` 11, `verdict.json` 10. `tests/`: 399 of 400.
  - **How they fit:** the new code and tests fit by honest compaction, with every case and assertion kept:
    - a `sh` helper for the repeated `verdict.sh` invocation;
    - tuples written to fit one line;
    - two `verdict.sh` blocks (condition 8, the required-check list) written shorter with the same behaviour;
    - four line breaks fewer in the schemas, whose parsed content still equals b8998de1's (R5).
  - **Kept:** the 17 tests of the reset stay green at the code head (R3). Before the fix, a local run of the whole compacted file against 513e5d05's script at `51abdb1c` failed only the revise's three new cases. That run is not pasted; R2 pastes the two checks.
- **Residual for P1 (1):** the host is not a trust boundary (plan 024 §5.14 item 0), and two cases remain:
  - A caller who builds the complete pinned environment itself (clean names, links to absolute non-shim paths) chooses its tools, exactly as its `PATH` already does for the resolution.
  - An inherited function named after a bash builtin (`unset`, `compgen`, `read`) could shadow the cleanup.
- **Not run locally:** `make unit-test` this round; the PR's CI `test` jobs run it. The verdict module, shellcheck and shfmt are green here.

cost: n/a
