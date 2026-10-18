---
task_id: dotfiles-T133-verdict-audit-pool-a02
seat: claude-standard-dot-a011
reset_of: dotfiles-T133-verdict-audit-pool-a01
branch: tools/verdict-audit-pool-a01
pr: 410
base: 68f8a70a (the merge base with origin/main)
previous_head: 85a472294d0c10835bd7235e3c76d045846a6ed9 (a01's revise-1 head, locally reviewed: 2 P1, 4 P2)
code_commit: e2092549 (the red tests f760acff, the fix dc83dabd, the refinement e2092549)
task_sha256: 6d2e0a42995f2cdb3a290d61c5a32c36ddf8360a33dc21ad409e799f2f298505
---

# Report: dotfiles-T133-verdict-audit-pool-a02

- Seat: `claude-standard-dot-a011` in `.claude/worktrees/worker-d`. The local branch `verdict-audit-pool-a02-a011` was created with `--no-track` from `origin/tools/verdict-audit-pool-a01` at `85a47229`, and it is pushed to `tools/verdict-audit-pool-a01`, so PR #410 continues. The seat's stale local `tools/verdict-audit-pool-a01` (at `0db5f175`) and the #413 branch were left untouched. No PR was created and nothing was parked again.
- Task file: copied byte-identical to `.orchestration/dotfiles-T133-verdict-audit-pool-a02/task.md`, sha256 `6d2e0a42…8505` (validation §1). The a01 copy stays: removing it and relocating inherited evidence is the orchestrator's reset bookkeeping, outside this task's `allowed_files`.
- Historical evidence: a01's records remain under `.orchestration/dotfiles-T133-verdict-audit-pool-a01/`, with their own task id and tested heads. Nothing in this task's `validation.md` is inherited; every block ran for a02.

## Retained behaviour

The nine conditions, the accept, revise and hold mapping, the exit codes 0, 10, 20 and 2, the verdict JSON and its schema check, `--shadow`, `--loop` and the `--apply` guard and ordering are unchanged except where items 6 to 11 say otherwise. `--admin` and `--auto` anywhere in the arguments are still refused (exit 2) before any tool runs. The ERR trap now applies from the start of the script, so a failure during pinning is an internal error (exit 2, treated as hold). audit-pool.sh's and orch-audit.sh's behaviour is unchanged. The only other change in orch-audit.sh is that `--validate` runs `python3 -I` from PATH.

The seven retained verdict tests and eight retained pool tests run unchanged in substance. Both test modules were compacted to fit the 500-line test cap: one-line imports, `TestCase.enterContext`, fakes as one-line strings, and merged helper lines. No case or assertion was dropped. `test_audit_pool.py` has 25 assertion calls before and after, and every retained `breaks`, `refusals` and subtest tuple is still present.

## The six fixes (items 6 to 11), each red against 85a47229 and green at the head

6. **Pinned execution context** (`verdict.sh`, and `orch-audit.sh --validate`).
   - Before reading any checkout, verdict.sh resolves bash, uv, python3, gh, git and jq into a private `mktemp -d` directory of links. agmsg-dispatch and herdr are linked too when present, because `--apply`'s dispatch.sh needs them.
   - Each tool is resolved from `/` with `mise which` under `env -i`, falling back to `command -v`. A path under a `shims` directory, a relative path or no path holds (exit 20) before anything else runs.
   - The script then re-runs itself under `env -i` with only HOME, TMPDIR, PRECHECK_REQUIRED, `VERDICT_BIN` and `PATH=<links>:/usr/bin:/bin`, and removes the link directory afterwards.
   - The re-run is skipped only when PATH is exactly that shape, which is how `--loop`'s children inherit the context. An inherited `VERDICT_BIN` alone does not skip it.
   - Python runs as `${VERDICT_BIN}/python3 -I`: the fresh sweep, the condition-4 checker, and orch-audit.sh's `--validate` schema checker through PATH. The front matter is read through `uv run --no-config --no-project --offline --python ${VERDICT_BIN}/python3 --with pyyaml`.
   - Result: a checkout's `.python-version`, `.venv`, uv or mise configuration, and an inherited `UV_PYTHON` or `VIRTUAL_ENV`, cannot pick an interpreter or tool. Resolution runs from `/`, not the root, because the root itself can be the checkout whose `mise.toml` sits outside the `--apply` guard's directories. Shell utilities come only from `/usr/bin` and `/bin`.
   - Test `test_verdict_pins_tools_interpreter_and_environment_before_reading_a_pr_checkout` plants a working interpreter that leaves a marker. It does so under `--apply`, where the old tracked-code guard passes because the planted files lie outside `scripts/`, `.schemas/` and the task files. The four selectors are `.python-version`, a checkout `.venv`, `UV_PYTHON` and `VIRTUAL_ENV`. For each, it asserts that the merge still happens and that no marker is written.
7. **Open P0/P1 count** (conditions 3 and 7).
   - Both use `[P0/P1 findings whose status is new, still-open or absent] | length`. Condition 3 fails on a nonzero count before it looks at the verdict and scopes. Condition 7 fails (hold) on a nonzero count.
   - Test `test_verdict_counts_open_p0_p1_findings_even_when_the_id_is_empty` uses an incorrect audit with an empty-id, records-scope P1, and the record's audit hash is refreshed. The old code accepts it. The new code fails conditions 3 and 7 and holds. P0 and `still-open` behave the same. A `fixed` P1 fails condition 3 alone (an incorrect audit with nothing left open), so it revises.
8. **Feedback heads** (condition 4).
   - Both the fresh sweep's and the saved document's `head_sha` must equal the accepted head.
   - Test `test_verdict_condition_4_requires_saved_and_fresh_heads_to_equal_the_accepted_head` has a green control, then a stale head and a removed `head_sha` in each document. Each of these fails condition 4 alone.
9. **Null URL** (condition 4).
   - Gaps are decided by the validators and printed one per line with a fixed prefix. A URL only labels the line.
   - Test `test_verdict_condition_4_rejects_an_undispositioned_status_with_a_null_url`: a status item with `url: null` and no disposition fails condition 4. A valid disposition for the same identity accepts.
10. **Identity and multiplicity** (condition 4).
    - Matching uses `require-crit-review.py`'s own `missing_feedback()`, keyed by `feedback_key()` over source, url, level, path, line, body and author, with its masked-body and masked-path equivalence and multiplicity. The module is loaded from the root by path and is not modified.
    - Test `test_verdict_condition_4_preserves_complete_item_identity_and_multiplicity` covers three cases. Two annotations share a URL and only the last is dispositioned: fail. Two identical fresh items have one saved: fail. One saved item per fresh item: accept.
11. **Disposition and commit validators** (condition 4).
    - Every saved item must pass `parse_disposition()`. A `fixed:` commit must satisfy `commit_in_range(root, commit, base, head)`, where base is `git merge-base origin/main <head>`; an empty base holds instead of making every commit "in range". A not-applicable reason must reach `FAILURE_REASON_MIN_CHARS` at a `STRICT_REASON_LEVELS` level. Evidence commands are never executed.
    - The checker runs with `-B`, so no bytecode lands in the checkout that the `--apply` guard inspects.
    - Test `test_verdict_condition_4_uses_the_existing_disposition_and_commit_validators` has eight negative cases, each failing condition 4 alone: `not-applicable:; evidence=`, a whitespace-only reason, an empty evidence command, a repeated delimiter, the unknown `fixed:abcdef1`, the base commit, a commit outside the head's ancestry (`git commit-tree`), and a 5-character reason at the failure level. Its positive controls, a real fix commit inside base..head and a complete not-applicable, both accept.

Red: on `f760acff` (`85a47229`'s scripts plus the a02 tests) the Check's command fails 22 subtests across exactly the six new tests, while the 15 retained tests pass (validation §3, `unittest exit status: 1`). Green: 21 tests at the head (§4).

## The Check

All results were obtained at `e2092549` unless stated otherwise; the section numbers refer to `validation.md`.

- `uv run python -m unittest tests.unit.test_verdict tests.unit.test_audit_pool -v`: 21 tests pass (§4). The retained tests include both revise-1 regressions, the RFC 3339 offset test and the offline PyYAML hold.
- `shellcheck` on the three scripts: clean. `shfmt -d`: the repository form `shfmt -i 4 -sr -d` (the one `make format` and CI run) is clean. A bare `shfmt -d` asks for tabs on these files and on every tracked script, because `.editorconfig` sets `indent_size = 4` without `indent_style` (§5). `ruff format --check` on the two test modules: clean.
- `make format`: exit 2 (§6). Its whole-tree shfmt step flags 12 files, and every one is unchanged from the merge base `68f8a70a` (§6a). Because make stops at that step, its other two steps were run on their own: `ruff format --check` (64 files) and `prettier --check` are both clean (§6a).
- `make render-check`: clean (§7).
- `make unit-test` (§8): 1204 tests at the head with 194 failures and 107 errors; 1183 tests at the unchanged base with the same 194 failures and 107 errors. No test fails at the head that does not also fail at the base. The failures come from the sandbox, mainly the global SSH commit signing that cannot read `~/.ssh`, which breaks fixture commits. With that limit and the `mktemp` limit neutralized identically on both sides (§8a), the results are as follows.
  - Base: 38 failures and 10 errors, in `test_agent_stop_gate` (4), `test_gh_auth` (5), `test_herdr_agents` (31) and `test_runtime_health` (8).
  - Head: the same 48, plus `test_slow_store_blocks_within_the_budget` (`5.31 not less than 4.5`). That is a wall-clock assertion in a test whose files this PR does not change. It passed in the first neutralized head run and passes three of three times run alone (§8a).
  - These are reported as inherited failures and one timing flake, not as passing. The first neutralized head block printed `exit status: 0` because its `echo` read `$?` after a command substitution. It was rerun with the status captured first, and only the rerun is kept.
- Shadow run (§10): `scripts/orchestrator/verdict.sh --shadow 410 --task dotfiles-T133-verdict-audit-pool-a02`, run outside the sandbox because gh reads GitHub. It exited 20 (`hold`), as the Check expects before the audit exists. The tested head is PR #410's GitHub head at the time, `85a47229`, because this task's push had not happened yet; the script was `e2092549`'s. Conditions 2 (all seven required checks SUCCESS) and 6 (`revises=0`) were read live through the pinned tools. Conditions 3, 4, 5, 7, 8 and 9 failed because this checkout has no a02 record, audit, saved feedback document or task file, so the result is hold.
- Caps (§9), against the merge base: 500 changed lines outside `tests/`, `.orchestration/` and `.schemas/`: verdict.sh 264, audit-pool.sh 124, orch-audit.sh 101 + 11 (cap 500). `tests/`: 499 (cap 500). The schema data is counted separately: `.schemas/audit.json` 33, `.schemas/verdict.json` 29 and `.schemas/classes.yaml` 140 lines, unchanged in this task.
- After the push, the final head's CI, its check-run and commit-status counts and the Bot window go in the RESULT, because a record cannot hold its own commit's CI.

## Worker-side review (one round, on e2092549, no fix round)

A fresh read-only subagent was given the commit range and the task file, not my conclusions. Its verdict was `correct`: no P0, P1 or P2, and six P3, each declared in `dotfiles-T133-verdict-audit-pool-a02-worker-crit.json`. It reproduced red on 85a47229's scripts and green at e2092549, compared the retained tests case by case, and measured the caps. The P3 that matter for acceptance:

- **The `command -v` fallback.** When `mise which` has no answer, the fallback reads the caller's PATH. An activated virtualenv's `bin/python3` on that PATH is therefore what gets linked. This is the orch-gate.sh pattern that item 6 prescribes. The `VIRTUAL_ENV` variable itself never reaches the run, and a checkout's files reach it only through a PATH entry that the operator added.
- **A preset pinned PATH.** A caller who presets both `VERDICT_BIN` and the exact pinned PATH keeps the rest of their environment. Only the caller can do this, and it is how `--loop` children keep the context.
- **`env -i` drops agent auth and cache relocations.** `--loop`'s `git fetch` then fails, and a relocated uv cache leaves PyYAML unavailable. Both fail closed.

Live `--apply`, `--loop` and dispatch were not exercised, as the task states.

## Changed files (cumulative PR diff against the merge base)

`scripts/orchestrator/verdict.sh`, `scripts/orchestrator/audit-pool.sh`, `scripts/orchestrator/orch-audit.sh`, `.schemas/audit.json`, `.schemas/verdict.json`, `.schemas/classes.yaml`, `tests/unit/test_verdict.py`, `tests/unit/test_audit_pool.py`, and `.orchestration/dotfiles-T133-verdict-audit-pool-a02/**` (this task's copy and records). The a01 records under `.orchestration/dotfiles-T133-verdict-audit-pool-a01/` came from earlier rounds; this task did not change them. In this task: the three scripts, the two test modules and this task's directory.

## Evidence, review, cost

- Evidence in `.orchestration/dotfiles-T133-verdict-audit-pool-a02/`: `task.md`, `report.md`, `validation.md`, `sandbox.md`, `learning.md`, `dotfiles-T133-verdict-audit-pool-a02-worker-crit.json` and `dotfiles-T133-verdict-audit-pool-a02-worker-review-receipt.md`. No `revise.yaml`: this is the first round of a02.
- PR feedback: this task posted no `@codex review` comment. The final head's feedback, its dispositions and the Bot window (`bot: none` if nothing arrives in 15 minutes) are in the RESULT.
- No Understand-Anything hook prompt fired, and no Plan Mode was used.
- cost: n/a (the runtime exposes no token or cost figure to the seat).
