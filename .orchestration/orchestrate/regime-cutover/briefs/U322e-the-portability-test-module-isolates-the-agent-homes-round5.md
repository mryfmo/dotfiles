# U322e round 5 of U322: the portability test module gains the module hooks the harness-coverage test demands

GOAL
PR 718's Unit test run 42342689355 (the round-3 head 0fc4740b) fails all three Ubuntu test legs on one test: `test_agent_home_isolation.HarnessCoverageTest.test_every_python_harness_isolates_the_agent_homes_for_the_whole_module` reports `test_sandbox_portability.py: setUpModule does not call isolate_agent_homes` and `tearDownModule does not call restore_agent_homes`. Round 3 added the literal `scripts/update-agent-assets.sh` to that module's `ALLOWED_TMP` table, which makes `harness_modules()` (the coverage test's regex over module text) classify it as a harness module, and a harness module must isolate the agent homes for the whole module. The round-4 head 39f75cc8 carries the same module text, so its CI will fail the same way. The macOS workers did not run `test_agent_home_isolation`, which is why rounds 3 and 4 passed locally.

SCOPE
The same branch `fix/dsh-harness-build-under-srt` and PR 718; the tree is `/tmp/dotfiles-wt/U322` at 39f75cc8. May write: `tests/unit/test_sandbox_portability.py` (the two module hooks and the import they need, in the form the other harness modules use; read `tests/unit/test_update_agent_assets.py`'s `setUpModule` and `tearDownModule` and `tests/unit/agent_home_isolation.py`), and the body `../U322e-pr-body.md` (the round-4 body `/tmp/dotfiles-wt/U322d-pr-body.final.md` plus a `## Round 5` paragraph and a row for the changed test module if the table lacks one). Not: any other file; no behaviour change.

CONTEXT
`tests/unit/test_agent_home_isolation.py:19-56` at 39f75cc8: `SCRIPTS` is the regex that classifies a module as a harness module; `module_hook_calls` reads the module's `setUpModule` and `tearDownModule` by AST and lists the function names they call; the coverage test wants `isolate_agent_homes` in the first and `restore_agent_homes` in the second. Alternative considered and rejected: removing the literal from `ALLOWED_TMP` (it is the allowance round 3 needs); or changing the coverage test's regex (a repository rule outside this unit).

DATA SHAPE
Two module-level functions in `tests/unit/test_sandbox_portability.py`, `setUpModule()` calling `isolate_agent_homes()` and `tearDownModule()` calling `restore_agent_homes()`, with the module's import of `agent_home_isolation` in the form its siblings use; nothing else in the module changes.

CHANGE
1. Add the two hooks and the import. 2. `uv run --with pyyaml python -m unittest tests.unit.test_agent_home_isolation tests.unit.test_sandbox_portability tests.unit.test_network_bounds -v` OK (the coverage test included). 3. `uv run ruff format --check` in the CI form; `scripts/lint-comparisons.py --changed`. 4. Commit `test(portability): the module isolates the agent homes as the harness-coverage test requires (regime-cutover U322e)` with the trailer. 5. The body: the round-4 body plus `## Round 5` (the CI failure, the cause, the two hooks); the test module's row names the coverage test as its selector; `Program-Unit: regime-cutover/U322` once and the footer.

ACCEPTANCE
1. The three test modules OK (counts pasted; the coverage test named as passing). 2. `git diff --stat 39f75cc8 HEAD` shows the one test module (pasted). 3. ruff 0; lint-comparisons 0.

VERIFY
ACCEPTANCE pasted into the body's Verification section and the report; CI on the pushed head is the coordinator's check.

CLOSURE
remove

TRUST
TRUST: the unit trusts the harness-coverage test as the repository's rule for test modules that name a script; it changes two module hooks and nothing of the lever.

TIMEBOX
15 minutes.

FORBIDDEN
No change to the updater or to the coverage test's regex; no behaviour change; no network; no push; no `gh` call; no pipe `|` in any bash command (standing order 46: output to a file under `/tmp/u322e/`, then read it).

WORKER RULES (standing orders 21, 27, 29, 31, 34, 44, 46; read `~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` lines 23 to 62)
- Never run git or edit files in `~/Workspace/dotfiles`, never push, never open or edit a PR, never edit the live store; you stop at a committed head in `/tmp/dotfiles-wt/U322`. The worktree is yours alone; your final line is the Task return.
- Progress line at `../U322e-progress.txt`; final report to `../U322e-report.txt`.
- Commit unsigned: `git -c commit.gpgsign=false commit`. The commit message ends with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.

REPORT
Status, head sha (40 hex), the two hooks as written, the ACCEPTANCE lines. Under 8 lines, ending with `head=<40 hex>`.

STANDING
`preferences.md` (standing orders 21, 24, 27, 29, 34, 44, 46); the U322c and U322d briefs; `tests/unit/test_agent_home_isolation.py` (the rule).
