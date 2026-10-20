---
task_id: dotfiles-T133-regime-ci-fixture-grammar-a01
seat: claude-standard-dot-a009
amendment: 1
branch: tools/regime-ci-fixture-grammar-a01
pr: 441
base: 60a6fb2b324d0381c4a6e539b37c650105154a7e
copy_commit: 53c9e23f
code_head: 15bc046ef0bc50476879e92cfaa42e5952f6878b
task_sha256: c2bfda037d2012e3703f12b7eedc2e976f79f5259ec5e47798248d544a69cc2b
cost: n/a (the seat's token and time usage is not visible to the worker)
---

# Report: dotfiles-T133-regime-ci-fixture-grammar-a01 (the regime-ci fixtures use the disposition grammar)

- **Seat and task:** `claude-standard-dot-a009` in `.claude/worktrees/worker-c`. The AGMSG-TASK of 04:34:08Z had sha `2fc20d23…`. Amendment 1, sha `c2bfda03…` at 04:47:06Z, answered my question of 04:40Z. The branch copy is byte-identical to amendment 1, at 66 lines against the cap of 90 (validation §1), and the task-consistency check passes (§1a).
- **Branch:** a fresh `tools/regime-ci-fixture-grammar-a01` from the dispatch branch point `60a6fb2b` (§2).

## The question round (before any edit)

Two conflicts in round 1's text were measured and asked about, and amendment 1 answered both.

1. **The dispatched Check command failed on the unmodified module inside the sandbox, with 22 errors (§4h):**
   - `uv` was not on `PATH`, because the module shells out to `uv run --with pyyaml python -I` as `regime.yml` does.
   - `git init` exited 128 because `TMPDIR` was unset under `env -i`, so `tempfile` fell back to the worktree.
   - Amendment 1 keeps `uv`'s directory on `PATH` and `TMPDIR` set.
2. **The 12-line cap could not hold a sentence in each row.** Ruff format, at 120 columns, splits lines 127 and 276 once a sentence is inline: 11 insertions and 5 deletions, or 16 changed lines. Amendment 1 allows one module constant.
- **A third point, taken into amendment 1:** the `src/tool.sh` row that line 276 removes is written by line 27's `ROWS`, not by line 127.
- **An addendum, sent at 04:50Z after amendment 1 had already gone out:** `env -i` also strips the sandbox's proxy variables. Whenever `uv` has to revalidate pyyaml against pypi.org, the amended command then fails with a DNS error (§4h). §4 and §6 therefore run it twice: as amended, and with the three proxy variables passed by name.

## Item 1: the five rows

| Row (line at `60a6fb2b`) | Before | After (`15bc046e`) |
|---|---|---|
| 27, `ROWS` (the eleven threat rows of `TASK`) | `f"  - control: {name}\n    disposition: residual\n"` | `f"  - control: {name}\n    disposition: {RESIDUAL}\n"` |
| 127, the verifier and checker rows | `… the PR edits {path}\n    disposition: residual\n` | `… the PR edits {path}\n    disposition: {RESIDUAL}\n` |
| 276, `no_row` | `TASK.replace("  - control: the PR edits src/tool.sh\n    disposition: residual\n", "")` | `TASK.replace(f"  - control: the PR edits src/tool.sh\n    disposition: {RESIDUAL}\n", "")`, now an f-string, still removing exactly the `src/tool.sh` row `ROWS` writes |
| 372, the predecessor copy row | `… disposition: residual\n` | `… disposition: {RESIDUAL}\n` |
| 373, the task copy row | `… disposition: residual\n` | `… disposition: {RESIDUAL}\n` |

- **The constant:** `RESIDUAL = '"residual: the fixture row is test data for this control"'`, one new line at 26. PyYAML reads it as `residual: the fixture row is test data for this control`. That passes the a05 checker's C13, the `residual: ` form, and C11, a 45-character payload where 20 is the minimum (§7, using PR #417's rules at `7a201eab`).
- **Nothing else changes:** no bare row is left (§5), and there is no test logic, new test or renamed test.
- **The pre-push reviewer's checks:** it evaluated `no_row`. The target occurs once in `TASK`, 113 characters are removed, and the rows go from 11 to 10.
- **Runs:**
  - Before, on the unmodified module at `60a6fb2b`: 16 tests OK, as amended and with the proxy variables (§4).
  - After, at `15bc046e`: 16 tests OK both ways (§6).
  - Ruff format and ruff check are clean (§8).
- **Caps (§9):** 0 changed lines outside `tests/` and `.orchestration/`, and 11 of 12 under `tests/` (6 insertions, 5 deletions).
- **Not run here:** the migrated module against PR #417's checker. #417's copy of the module differs from main's by 60 lines, and the a05 checker's environment guards refused a direct run. Per the task, #417's CI after its update-branch decides.

## Review

- **The one pre-push round:** a fresh, read-only general-purpose subagent of this seat, working inside its sandbox, reviewed `60a6fb2b..15bc046e` and returned `Verdict: correct`, with no P0, P1 or P2 (the worker-crit JSON and its receipt).
- **Its two P3:**
  - the shared sentence is generic, which amendment 1 allows;
  - the records were missing at `15bc046e`, which this commit resolves.
- **Its note:** run as written, the amended Check depends on uv's cache because the proxy variables are stripped (§4, §6).
- No code change followed.

## Completion

- **PR:** https://github.com/mryfmo/dotfiles/pull/441, opened ready for review, not as a draft, at 2026-10-20T05:09:57Z on `56faa442`, inside the sandbox (validation §10). No `@codex review` comment is posted.
- **CI on `56faa442`:** 11 of 11 checks pass, and the merge state is CLEAN (§11).
- **The Bot, unavailable:** both Codex reviews the PR's opening triggered failed on Codex usage limits. The code review failed at 05:10:00Z and the security review at 05:10:07Z, as on PR #433. There are no review threads or comments (§12). Raising the limit is outside this seat; the orchestrator decides at the gate.
- **The final head** adds only this directory's records on top of `56faa442`.
- **Open items:** none.
