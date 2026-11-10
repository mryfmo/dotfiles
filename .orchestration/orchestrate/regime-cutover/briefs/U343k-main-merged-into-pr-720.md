# U343k the merge of main into PR 720's round-8 head: the conflicts in hcom-seat, its copy, the manifest, the generated outputs and the hcom-seat test module resolved so both sides' changes stand

GOAL
PR 720 (U343, the acp-broker lever) is at its round-8 head 62c10228 with a correct audit (verdicts/U343j-62c10228.md) and a 0-finding sweep (run-67), but it conflicts with main af601a97 (`git merge-tree`: `home/dot_agents/agent-config.yaml`, `scripts/orchestrator/hcom-seat` and `home/dot_local/bin/common/executable_hcom-seat`, `scripts/generated-agent-outputs.json`, `tests/unit/test_hcom_seat_dsh.py`), so GitHub ran no pull_request workflow on the head and `pr-merge.sh` refuses (no required check). Main moved since the merge base 6ad1be23 through today's merged units (U413 PR 747, U416 PR 751, U418 PR 752 and the records syncs): the manifest's pins and keys, the generator and the hcom-seat lines they touched. This unit merges main into the branch and resolves each conflict so that both sides' changes stand, with the pins regenerated, never typed.

SCOPE
The worker repository `/private/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/dotfiles-wt/U343j` on branch `fix/acp-broker-round8` at 62c10228 (the round-8 head; the coordinator pushes the merge commit onto `feat/acp-broker-lever`). The tree's `origin` is the GitHub URL and the tree has no network; main comes from the coordinator's checkout by path: `git fetch ~/Workspace/dotfiles main` (its main is af601a97, a read of the checkout), then merge `FETCH_HEAD` into the branch. May write: the conflict resolutions in `scripts/orchestrator/hcom-seat` and `home/dot_local/bin/common/executable_hcom-seat` (the copy is regenerated from the source by the generator, never resolved by hand), `tests/unit/test_hcom_seat_dsh.py`, `home/dot_agents/agent-config.yaml` (the pin block through the generator; any other hunk by taking both sides), `scripts/generated-agent-outputs.json` (regenerated), and the merge commit. Non-goals: any change beyond the resolution of the conflicts and the regeneration; no edit of the PR body (the coordinator keeps it); no new behaviour.

CONTEXT
`git log --oneline 6ad1be23..FETCH_HEAD -- scripts/orchestrator/hcom-seat tests/unit/test_hcom_seat_dsh.py` (after the fetch) names the commits of main: #724 (U353, the router row's credential root and the Source settings) and #733 (U219, the store root rows), both of which edit `seat_settings_render` and the hcom-seat test module near the router row that touched the two files; read each conflict's two sides with `git diff` on the conflicted file and `git log -p` of those commits before choosing. The branch's side in hcom-seat is the round-7 change (the `broker_dir` cell of the role table, `broker_dir_make`, the tagged denyWrite row in `seat_settings_render`, the make in `seat_sandbox_write`, the dry-run line); main's side is whatever those commits changed in the same regions. The copy `executable_hcom-seat` and the pins: run `scripts/generate-agent-configs.py` (the `make render-check` form) after the source conflicts are resolved, so the copy, the pin block and `scripts/generated-agent-outputs.json` are the generator's output. The test module's conflict: both sides' tests stand (main's new tests and the round-7 tests), the imports and helpers merged once.

DATA SHAPE
One merge commit on `fix/acp-broker-round8` whose first parent is 62c10228 and second parent is af601a97, whose tree equals, for every non-conflicting path, what `git merge` produced, and for every conflicting path holds both sides' changes with the generated files regenerated.

CHANGE
1. `git -C <tree> fetch ~/Workspace/dotfiles main`; `git merge --no-ff --no-commit FETCH_HEAD` (no rebase); list the conflicted paths. 2. Resolve `scripts/orchestrator/hcom-seat` and `tests/unit/test_hcom_seat_dsh.py` by hand so both sides stand; then run the generator (`make render-check` form, or the generator's write mode as the Makefile's `render` target runs it) so `home/dot_local/bin/common/executable_hcom-seat`, the pin block of `home/dot_agents/agent-config.yaml` and `scripts/generated-agent-outputs.json` are regenerated; resolve any remaining manifest hunk by taking both sides; `cmp` of every lever and its copy is 0. 3. `uv run --with pyyaml python -m unittest tests.unit.test_hcom_seat_dsh tests.unit.test_hcom_seat tests.unit.test_acp_broker tests.unit.test_acp_record_place tests.unit.test_lever_self_check tests.unit.test_generate_agent_configs -v` OK; `scripts/ci/run-on-lint-files.sh` exit 0; `make render-check` exit 0; `make validate-agent-assets` exit 0. 4. Commit the merge unsigned with the message `merge: main af601a97 into feat/acp-broker-lever (round 8 head 62c10228); conflicts in hcom-seat, its copy, the manifest, the generated outputs and test_hcom_seat_dsh.py resolved, both sides kept, pins regenerated` ending with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.

ACCEPTANCE
1. `git -C <tree> log -1 --format='%P'` prints `62c10228335bb822a87d054be4ad4755cdeeeb2b af601a97567f1f07e9337cad899506f601f419f1`, pasted. 2. The six-module unittest run OK with counts, pasted. 3. `scripts/ci/run-on-lint-files.sh` exit 0, `make render-check` exit 0, `make validate-agent-assets` exit 0, `cmp` of each lever and its copy exit 0, pasted. 4. `git diff --name-only af601a97 HEAD` pasted (the pull request's paths after the merge; nothing outside the pull request's 18 paths plus what the generator touched). 5. `git diff 62c10228 HEAD --stat -- scripts/orchestrator/hcom-seat tests/unit/test_hcom_seat_dsh.py` pasted with one sentence per file on what main's side added.

VERIFY
ACCEPTANCE pasted into the report; the coordinator fetches the merge commit by path, pushes it onto `feat/acp-broker-lever`, and the sweep, CI and the audit under `--cyber-program daybreak_blue` re-run at the merged head (the digest changes, no carry); then `pr-merge.sh`.

CLOSURE
allowlist

TRUST
TRUST: the unit trusts `git merge` for every non-conflicting path, the generator as the one writer of the copies, the pins and the generated outputs, and the six test modules plus the lints as the proof that both sides stand; it adds no behaviour and reads no store.

TIMEBOX
60 minutes.

FORBIDDEN
No rebase; no `git stash`; no edit outside the conflicted paths and the generator's outputs; no pin typed by hand; no push; no `gh` call; no network beyond the fetch from the checkout by path; no pipe `|` in any bash command (standing order 46: output to a file under `/tmp/u343k/`, then read it); write the first progress line within five minutes of starting.

WORKER RULES (standing orders 21, 27, 29, 31, 34, 44, 46, 49; read `~/.local/state/regime-store/dotfiles/regime-cutover/preferences.md` lines 23 to 56)
- Never run git or edit files in `~/Workspace/dotfiles` (fetching from it by path is a read), never push, never open or edit a PR, never edit the program store; you stop at the committed merge in `/private/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/dotfiles-wt/U343j`. Your final line is the Task return.
- Progress line at `/tmp/dotfiles-wt/U343k-progress.txt` after each CHANGE step; final report to `/tmp/dotfiles-wt/U343k-report.txt`.
- Commit unsigned: `git -c commit.gpgsign=false commit`.

REPORT
Status, the merge commit's sha (40 hex), the ACCEPTANCE lines, the one-sentence-per-file resolution notes, deviations. Under 12 lines, ending with `head=<40 hex>`.

STANDING
`preferences.md` (standing orders 21, 27, 29, 32, 44, 46, 49); the U406c precedent (a merge of main as round 3 of U406, decisions 2026-11-09T05:42:57Z); `verdicts/U343j-62c10228.md`.
