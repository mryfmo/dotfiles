# U363: `build_under_srt` makes pnpm's store operation lock directory before the run and grants it, so a pnpm install inside srt gets past its first lock

GOAL
After U354 landed and deployed, `DSH_HOME=~/.dsh scripts/update-agent-assets.sh update_dsh_superagent` on the laptop passes the canary and fails inside `pnpm install --frozen-lockfile`: `ERR_PNPM_STORE_DIR_OPEN_OPERATION_LOCK … Failed to open the store operation lock at "pnpm-store-operation-locks": Operation not permitted` (/tmp/u317-stageA-install3.txt, 10:55:46Z). The macOS unified log names the denial: `Sandbox: pnpm(67566) deny(1) file-write-create /private/tmp/pnpm-store-operation-locks-501` (19:55:48 JST): pnpm 12.8.1 keeps its store operation lock in the system temporary directory, `/tmp/pnpm-store-operation-locks-<uid>`, whatever `TMPDIR`, `XDG_STATE_HOME` or `store-dir` say, and no write root of `build_under_srt` covers it (its `denyWrite` names `/tmp/claude` and `/private/tmp/claude`; `/tmp` itself is neither granted nor denied, and the sandbox denies by default). Every `build_under_srt` caller fails this way on a real host (`update_deepseek_harness`'s build included); CI's fake pnpm never locks. The fix: before the run, the function makes `<tmp physical>/pnpm-store-operation-locks-<uid>` (0700, `mkdir` refusing an existing entry that is not a directory of this user, a link refused by name) and renders it as one more `allowWrite` row, so pnpm's lock lands in a directory this user made; the directory is left in place (pnpm reuses it; it holds lock files and nothing else).

SCOPE
A new branch `fix/build-under-srt-grants-pnpm-operation-lock-dir` from main dba01803; the tree is `/tmp/dotfiles-wt/U363`. May write: `scripts/update-agent-assets.sh` (`build_under_srt`: the directory and the row; the header's write-root sentence), `tests/unit/test_update_agent_assets.py` (the regression test and the settings expectation), and the body. Not: pnpm's configuration; the denyWrite list; anything outside `build_under_srt`.

CONTEXT
`build_under_srt` at main (scripts/update-agent-assets.sh, from :1786): `tmp_real` is the `pwd -P` of `/tmp` (already read for the `/tmp/claude` deny), `store_real` the store, `write_json` the allowWrite list (`dir_real`, `store_real`), the settings JSON at :1983-1984, every producer with its status (standing order 21). The uid: `id -u` with its status read, held to `^[0-9]+$`. The directory's path is built from `tmp_real` (no literal `/tmp` enters the file, so the portability guard reads it as before; check `tests/unit/test_sandbox_portability.py`'s rule on `${TMPDIR...}` words and `pwd -P` forms before writing). The regression test: the fake srt records the settings; the test asserts the row `<tmp physical>/pnpm-store-operation-locks-<uid>` in `allowWrite` and the directory present with mode 0700 after the run; a pre-planted link at that path makes the step refuse by name before srt runs. pnpm's behaviour is measured, not read from its source: the log line above.

DATA SHAPE
One more write root, made by the lever, owned by this user, named from the physical temporary directory and the uid.

CHANGE
1. The regression test first, red at dba01803. 2. The directory and the row. 3. `uv run --with pyyaml python -m unittest tests.unit.test_update_agent_assets tests.unit.test_sandbox_portability tests.unit.test_network_bounds -v` OK. 4. `make shellcheck`; `shfmt -i 4 -sr -d scripts/update-agent-assets.sh`; `uv run ruff format --check` in the CI form; `scripts/lint-comparisons.py --changed`; `make render-check`. 5. Commit `fix(updater): build_under_srt makes pnpm's store operation lock directory and grants it, so a pnpm install inside srt gets past its first lock (regime-cutover U363)` with the trailer. 6. The body: Summary (the measured denial), Contract, Threat table (the new root's row: a directory this user makes under the system temporary directory, a planted entry refused), Verification; `Program-Unit: regime-cutover/U363` once.

ACCEPTANCE
1. The regression test named with its red line at dba01803 and its green line at the head. 2. The three modules OK with counts. 3. The lints 0. 4. `git diff --stat dba01803 HEAD` pasted.

VERIFY
ACCEPTANCE pasted into the body's Verification section and the report; the coordinator reruns the superagent install on the laptop after the merge and the deploy, which is the real-surface proof (the next failure, if any, is the next unit).

CLOSURE
remove

TRUST
TRUST: the unit trusts the unified log's denial line as the measurement of where pnpm 12.8.1 locks, and srt's path grants as the boundary; the directory is this user's own (mkdir, 0700, a foreign entry refused) so no other process plants a lock the build follows.

TIMEBOX
40 minutes.

FORBIDDEN
No literal `/tmp` word in the lever (the physical temporary directory variable alone); no change to the deny lists; no network; no push; no `gh` call; no pipe `|` in any bash command (standing order 46: output to a file under `/tmp/u363/`, then read it).

WORKER RULES (standing orders 21, 27, 29, 31, 34, 44, 46, 49; read `~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` lines 23 to 56)
- Never run git or edit files in `~/Workspace/dotfiles`, never push, never open or edit a PR, never edit the live store; you stop at a committed head in `/tmp/dotfiles-wt/U363`. The worktree is yours alone; your final line is the Task return.
- Progress line at `../U363-progress.txt`; final report to `../U363-report.txt`; body at `../U363-pr-body.md`.
- Commit unsigned: `git -c commit.gpgsign=false commit`. The commit message ends with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.

REPORT
Status, head sha (40 hex), the test's red and green lines, the ACCEPTANCE lines. Under 8 lines, ending with `head=<40 hex>`.

STANDING
`preferences.md` (standing orders 21, 24, 27, 29, 34, 44, 46, 49); the U322, U322b and U354 briefs; `decisions.tsv` 2026-11-07T11:05:49Z (the measured denial).
