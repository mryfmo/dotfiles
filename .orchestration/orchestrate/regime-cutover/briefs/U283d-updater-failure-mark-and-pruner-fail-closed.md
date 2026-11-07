# U283d the updater's failure mark and the manifest pruner fail closed under an unwritable or unsearchable ~/.agents

GOAL
The four filed findings of `verdicts/U283b-fa969db6.md` (lines 3-6), re-read against `origin/main` 2b2415f6 (U283c, PR 701, changed the pruner since: `scripts/lib/asset-manifest.sh:158-194` now refuses a linked manifest and reads `compgen` through a status-checked substitution):
1. `scripts/update-agent-assets.sh:2811-2814` `mark_sync_failed`: when `manifest_record` cannot write the failure mark (the probe: `~/.agents` mode 0555 after a failed partial sync), `record_claude_failure` logs one line, the older readable record stays, and both `make doctor` manifest checks report nothing although the payload is missing.
2. `scripts/lib/asset-manifest.sh:167` `[ -e "${manifest_path}" ] || return 0`: an unsearchable `~/.agents` (the probe: mode 000) makes `-e` false, so pruning returns 0 silently and keeps a retired record, against the failed-read guarantee (standing order 21: a failed read is never an absence).
3. The `compgen -A function` producer at `:169` has no committed failure-injection test; the pruning tests cover corrupt JSON and path shapes only.
4. `tests/unit/test_update_agent_assets.py` (the test the PR 701 threat table cites as closing failure-mark write failures, around line 4949 on fa969db6) runs a successful rsync and never exercises an unwritable failure mark.

SCOPE
Branch `fix/updater-failure-mark-fails-closed` from `origin/main`; the tree is `/tmp/dotfiles-wt/U283d` (created by the coordinator). May write: `scripts/update-agent-assets.sh` (`mark_sync_failed`, its callers' handling, and the doctor-side check that reads the record), `scripts/lib/asset-manifest.sh` (`_manifest_prune_retired`'s presence test), `tests/unit/test_update_agent_assets.py`, the asset-manifest test module if one exists (`rg -n '_manifest_prune_retired' tests`), one README sentence if the README states the behavior, and the body `../U283d-pr-body.md`. Not: the single-step whitelist, any other updater step, the manifest `home/dot_agents/agent-config.yaml`.

CONTEXT
Read `mark_sync_failed` and `update_compactiondb` (`scripts/update-agent-assets.sh:2805-2850`), `manifest_record`, `record_claude_failure`, `fail_on_pin_failures`, and the doctor's manifest checks (`rg -n 'installed_manifest_error|manifest' scripts/update-agent-assets.sh` and the doctor target in the Makefile); `_manifest_prune_retired` whole (`scripts/lib/asset-manifest.sh:140-206`); the U283 verdict files under `verdicts/U283*.md` for the earlier rounds' findings and the mechanism the rounds settled on (status-checked producers, no here-strings). The probes in the verdict's Reproduced section are the tests to write.

DATA SHAPE
A producer whose status is unknown is a failure, never an absence: (a) the failure mark that cannot be written is itself a counted failure that ends the run non-zero and leaves a doctor-visible state (the doctor reads the payload's presence for an rsync-recorded step, or the record carries the mark, whichever the worker measures as the smaller change that makes `make doctor` name the step); (b) the pruner distinguishes "the manifest's directory cannot be searched" (refused, named on stderr, return 1) from "the manifest is absent" (return 0).

CHANGE
1. `_manifest_prune_retired`: before the `-e` test, an existing `${HOME}/.agents` that is not searchable (`[ -d ] && [ ! -x ]`) is refused naming the directory, return 1; the absent case keeps return 0.
2. `mark_sync_failed` and the doctor: when the mark write fails, the run still fails at `fail_on_pin_failures` and `make doctor` names the step (the worker measures which of the two shapes in DATA SHAPE is the smaller change and states why in the body).
3. Tests (each a failure injection, standing order 21): `compgen` failing makes pruning return 1 and keep the manifest; `~/.agents` mode 000 makes pruning refuse naming the directory; `~/.agents` mode 0555 after a failed partial sync makes the run exit non-zero and the doctor name the step; the cited threat-table test now exercises an unwritable failure mark.
4. The body: Summary (the four findings quoted with their new line numbers), Contract (the failed-read guarantee restated; Left out: other steps), Threat table per changed path (the updater writes under `~/.agents`, a trust boundary of the kit), Verification (ACCEPTANCE pasted).

ACCEPTANCE
1. `uv run python -m unittest tests.unit.test_update_agent_assets <the asset-manifest module if any> tests.unit.test_scratch_git -v` OK (counts pasted; the new tests named).
2. `make shellcheck` exit 0; `scripts/ci/run-on-lint-files.sh shell shfmt -i 4 -sr -d` exit 0; `scripts/ci/run-on-lint-files.sh python ruff format --config ruff.toml --check` exit 0; `scripts/ci/run-on-lint-files.sh markdown prettier --check` exit 0.
3. `uv run --no-project --with pyyaml scripts/lint-comparisons.py --changed` exit 0.
4. The two scratch probes of the verdict (mode 0555 after a failed partial sync; mode 000) re-run against the new code under a scratch HOME, their output pasted: the first ends the run non-zero and the doctor names the step, the second prints the refusal and returns 1.

VERIFY
ACCEPTANCE pasted into the body's Verification section.

CLOSURE
remove

TRUST
TRUST: the unit trusts the installed manifest the updater itself wrote under `~/.agents` and the shell's own function table; it reads no other state and no credential, and every filesystem read's status decides the branch.

TIMEBOX
60 minutes.

FORBIDDEN
No change to the manifest `home/dot_agents/agent-config.yaml` or to any other updater step; no write under the real `~/.agents`, `~/.claude`, `~/.omp`, `~/Workspace` (scratch HOME under `/tmp/u283d/` only); no local bats; no network; no push; no `gh` call; no pipe `|` in any bash command (standing order 46: output to a file under `/tmp/u283d/`, then read it).

WORKER RULES (standing orders 21, 27, 29, 31, 34, 44, 46; read `~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` lines 23 to 62)
- Never run git or edit files in `~/Workspace/dotfiles`, never push, never open or edit a PR, never edit the live store; you stop at a committed head in `/tmp/dotfiles-wt/U283d` and the coordinator fetches it by path.
- Progress line at `../U283d-progress.txt` after every step; first edit within ten minutes. Final report to `../U283d-report.txt` before you end.
- Commit unsigned: `git -c commit.gpgsign=false commit`. Every commit message ends with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.
- Comments explain a non-obvious why only; shell comments are English shdoc.
- Follow `~/.agents/pstack/skills/poteto-mode/SKILL.md` (Fix Root Causes: the silent branch goes, no guard that hides it; Test Behavior: each test injects the failure the user would hit).

REPORT
Status, head sha (40 hex), files changed (`git diff --stat` against the merge base, no fetch), the shape chosen for CHANGE 2 and why, the ACCEPTANCE result lines, deviations. Under 12 lines, ending with `head=<40 hex>`.

STANDING
`preferences.md` (standing orders 21, 27, 29, 34, 41, 42, 44, 46, 47); `verdicts/U283b-fa969db6.md`; `units.tsv` rows U283, U283b, U283c, U283d; the PR 701 body's threat table.
