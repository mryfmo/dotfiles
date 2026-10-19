---
task_id: dotfiles-T129-assets-omp-hcom-followup-a04
seat: claude-standard-dot-a009
branch: tools/assets-omp-hcom-followup-a04
pr: 430
base: 51ba580149fcace54a912358e7e87c5b07cd8760
copy_commit: ecea1a45
test_commit: 42414b6d
code_head: 42414b6df9983dcb99aeb411843e3a65bd7dbd44
task_sha256: fc324db78e16cdc8f0601d88a0c7755453b76ee63af916eafd99f5a0434a6efe
cost: n/a (the seat's token and time usage is not visible to the worker)
---

# Report: dotfiles-T129-assets-omp-hcom-followup-a04 (the assets lineage's owner of the a03 audit's advisory P2)

- **Seat and task file:** `claude-standard-dot-a009` in `.claude/worktrees/worker-c`, from the AGMSG-TASK of message 2509. The dispatched file and the branch copy are byte-identical (validation §1). The task-consistency check passes (§1a).
- **Branch:** a fresh `tools/assets-omp-hcom-followup-a04` from `origin/main` `51ba5801`, PR #428's squash merge (§2). `ecea1a45` adds the task copy.
- **Scope:** the one row under `## Owned by dotfiles-T129-assets-omp-hcom-followup-a04` in `.orchestration/acceptance/dotfiles-T129-assets-omp-hcom-followup-a03.md` (§3). Neither owned script changes (§7). The fix the row asks a test for, round 2's `mktemp` templates (`92d39f00`), is already on main.

## Item 1: the owned row

| Row id | Change in `42414b6d` | Red-then-green test |
|---|---|---|
| `audit:9e30542:1` (revise-check-grammar): one red-then-green test runs the updater's `mktemp` path with `TMPDIR` set to a sandbox-like directory and asserts the temporary directory is created under it; and the a03 revise round's `revise.yaml` is written into this evidence directory from the a03 record's facts | **The test:** `update_omp_in` takes an optional `tmpdir`, which it passes as `TMPDIR`. The other callers are unchanged. The new test runs `update_omp` with `TMPDIR=<home>/sandbox-tmp`. It reads the `-o` path the fixture `curl` logs, and asserts its parent is an `update-agent-assets.*` directory directly under that `TMPDIR`, and that the run succeeds. **The record:** `revise.yaml` gives the round's facts from the a03 record: message 2490 of 09:40:27Z, `round: 2`, `previous_head: 725b25bf…`, `result_head: 9e305424…`, and the audit reason. Because that revise line's `check=` was prose, a comment says so, and `checks:` names this test as the selector for its check (1). | `tests/unit/test_update_agent_assets.py::test_update_omp_makes_its_download_directory_under_tmpdir`. It is red at `725b25bf`, the head before `92d39f00`, inside the sandbox and by assertion (`[PosixPath('…/sandbox-tmp')] != []`). There, the untemplated `mktemp -d` ignored `TMPDIR`, and the sandbox refused the per-user default it picked (§4r). It is green here (§6b), and within the Check, 36 of 36 (§6). |

- **On Linux:** GNU `mktemp` without a template honours `TMPDIR`. Even so, the old code fails the test there by assertion: its directory is `tmp.*` under `TMPDIR`, not `update-agent-assets.*`. The pre-push reviewer showed this with a GNU-style shim, so the test is red on both platforms.
- **`revise.yaml`** parses with PyYAML, and its selector runs one test (§5). Its shape follows the existing records: the header comment, `previous_head`, `reason` and `checks`, plus the `task_id`, `round` and `revise` keys some carry.

## Check (§6 to §8)

- **The Check's tests:** `uv run python -m unittest tests/unit/test_remove_agent_asset.py tests/unit/test_update_agent_assets.py -v` exits 0 inside the sandbox, 36 tests (§6).
- **ShellCheck:** `shellcheck -x` is clean on both owned scripts, which this task does not change (§7). ruff format and ruff check are clean on the test module.
- **Caps, `origin/main...HEAD` (§8):**
  - outside `tests/` and `.orchestration/`: 0 of 120;
  - under `tests/`: 25 of 400.

## Review

- **The one pre-push round** covered `51ba5801..42414b6d`. It was a fresh, read-only general-purpose subagent of this seat, working inside its sandbox, and returned `Verdict: correct` with no P0, P1 or P2 (the worker-crit JSON and its receipt).
- **Its two P3 needed no change:**
  - the helper's `tmpdir` parameter leaves the other callers' environment as it was;
  - `revise.yaml` has one selector for five findings. The other four are record defects, and the row asks for one test.
- **Its evidence note corrected the Linux claim** (above). No code change, so the code head stays `42414b6d`.

## Completion

- **PR:** #430, opened ready for review, not as a draft, at 2026-10-19T11:51:20Z on `81b1cd90`, inside the sandbox (validation §10). No `@codex review` comment is posted.
- **CI on `81b1cd90`:** 11 of 11 checks pass, and the 10 check runs all succeeded (§11).
- **The Bot:** the PR's opening triggered Codex's code review (completed 11:52:41Z) and security review (11:54:22Z) of `81b1cd90`, both with `has_any_findings: false`. There are no review threads and no review comments (§12). The window from 11:51:20Z closed at 12:06:20Z.
- **The final head** adds only this directory's records on top of `81b1cd90`. The Bot does not re-review on a push, and the RESULT carries that head's CI.
- **Open items:** no Bot thread, no advisory row and no open question. Any advisory P2 belongs to `dotfiles-T129-assets-omp-hcom-followup-a05`.
- **The parallel order:** the rebase repair of PR #411 (the ACCEPTANCE `status=rebase-repair` of 11:51:18Z, `dotfiles-T133-result-precheck-a04`) ran on `tools/result-precheck-a01` after this branch's first push. This branch was committed and pushed before the switch.
