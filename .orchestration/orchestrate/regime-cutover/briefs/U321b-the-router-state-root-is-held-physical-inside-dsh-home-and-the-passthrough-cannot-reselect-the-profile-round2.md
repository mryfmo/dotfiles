# U321b round 2 of U321: the Router state root is held physical inside DSH_HOME, the passthrough cannot reselect the profile, and the threat table carries every changed file

GOAL
The round-1 audit of PR 715 (`verdicts/U321-fec87e14.md`, verdict incorrect, class containment-boundary) found two blocking defects and one body defect in the U321 head fec87e14 of `scripts/orchestrator/hcom-seat`. P1 (`hcom-seat:1551`): the router role's write root `<DSH_HOME>/router-state` is taken from the path as spelled, so a link at `router-state` pointing outside DSH_HOME (the auditor used a scratch `HOME/.config/autostart`) becomes the physical `allowWrite[6]` and the launch succeeds; the containment guarantee of the role (every write root inside the role's own roots, physical, no link) does not hold, and the body claimed a link refusal that the code does not make. P1 (`hcom-seat:316`): the fixed `--profile router` of the role is not enforced against the passthrough dsh arguments: `router -- --profile thak` forwards `--profile router --profile thak`, and `--profile=thak` and `-p thak` reach dsh too, so the restriction depends on dsh's option precedence instead of a refusal. P2 (`hcom-seat:292`, weight 20): the PR threat table has no row for either changed test file, uses the status word `by design` for the binding and orchestrator-effect rows (the permitted statuses are closed, residual and out-of-scope), and closes the documentation row with prettier, which cannot judge a stale containment claim. This unit fixes the three in one new head on the same branch.

SCOPE
The same branch `feat/hcom-seat-router-role` and PR 715; the tree is `/tmp/dotfiles-wt/U321` at fec87e14 (one commit on main 247d890d). May write: `scripts/orchestrator/hcom-seat` and its byte-identical copy `home/dot_local/bin/common/executable_hcom-seat`, `tests/unit/test_hcom_seat_dsh.py`, `tests/unit/test_hcom_seat.py`, the regenerated `home/dot_agents/agent-config.yaml` and `scripts/generated-agent-outputs.json` (by `uv run python scripts/generate-agent-configs.py` only), `scripts/orchestrator/README.md` (the router paragraph, only where it states the two guarantees), and the body `../U321b-pr-body.md` (the round-1 body `/tmp/dotfiles-wt/U321-pr-body.final.md` plus a `## Round 2` section and the corrected table). Not: any other lever, doc or test.

CONTEXT
Read the verdict file whole (`~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/verdicts/U321-fec87e14.md`; its Reproduced section names the two probes, `test_state_root_link_escapes_dsh_home` and `test_forwarded_profile_selectors_are_not_refused`, which this unit turns into refusals). Read `hcom-seat` whole: the role table (`:272`), `seat_write_roots` and the dsh row's physical-path rule (every root resolved by `physical_path`, judged against the protected set and the role's roots before the settings are rendered), `settings_judge`, the dsh launch line where `--profile <role_profile>` is placed before the verbatim dsh args, and `omp_inputs_check` for the shape of an argument refusal. The U310c head on PR 708 (`792604f9`, branch `feat/dsh-role-profile-route`) changes the same lever's profile config write and will merge first or after; do not merge or rebase onto it, the coordinator resolves the order.

DATA SHAPE
Two invariants of the router row. (1) The Router state root is a path under the physical DSH_HOME: when `<DSH_HOME>/router-state` exists it is a directory of this user and no link (a link, a regular file or another user's directory refuses naming it); when absent it is made 0700 after every check, as the dsh row makes its roots; the root rendered into `allowWrite` is the physical path, and a physical path outside the physical DSH_HOME refuses. (2) The passthrough dsh arguments after `--` carry no profile selector: any argument equal to `--profile` or `-p`, starting with `--profile=` or `-p` followed by a non-empty value, refuses naming the argument and the role's fixed profile; the launch line stays `--profile router` once, before the verbatim args.

CHANGE
1. Hold the state root: resolve `router-state` through `physical_path` with its status read, refuse a link or a non-directory, refuse a physical path not inside the physical DSH_HOME (prefix compare on the physical forms with the trailing slash, the pattern the write-root judge already uses), render the physical path, and make it 0700 when absent after the checks. 2. Refuse profile selectors in the passthrough for every role whose profile is fixed (the router row; the dsh row, if it is fixed too, by the same table flag), before the sandbox write and before any directory is made; the refusal names the argument. 3. Tests in `test_hcom_seat_dsh.py`: a `router-state` link to a directory outside DSH_HOME refuses naming it and writes no settings file; a regular file at `router-state` refuses; the physical path of a linked DSH_HOME still renders inside it (the existing dsh behaviour, unchanged); `-- --profile thak`, `-- --profile=thak`, `-- -p thak` and `-- -pthak` each refuse naming the argument, and a passthrough without a selector keeps the launch line of round 1; the structural-diff test of round 1 still passes. 4. The threat table: one row per changed path including both test files (a test file's row: risk `a test that passes against the defect`, status closed, evidence the selector that fails against fec87e14, run and pasted); the binding row and the orchestrator-effect row restated as `residual` with `unit=U<n> gate=<clause>` or as `closed` with a selector; the documentation row `out-of-scope` with the reason, or `closed` by a test that reads the paragraph. 5. `cmp`; `uv run python scripts/generate-agent-configs.py`; `make render-check`; `uv run python scripts/validate-agent-assets.py`; `make shellcheck`; `shfmt -d scripts/orchestrator/hcom-seat`; `uv run ruff format --check`; `scripts/ci/lint-comparisons.sh --changed`. 6. Commit `fix(hcom-seat): the Router state root is held physical inside DSH_HOME and the passthrough cannot reselect the profile (regime-cutover U321b)` with the trailer. 7. The body: the round-1 body plus `## Round 2` quoting the three findings and what changed, the corrected table, and ACCEPTANCE pasted; `Program-Unit: regime-cutover/U321` once and the footer.

ACCEPTANCE
1. `uv run python -m unittest tests.unit.test_hcom_seat_dsh tests.unit.test_hcom_seat -v` OK (count pasted; the new tests named). 2. The auditor's two probes, rewritten as the tests of CHANGE 3, fail against fec87e14 (run them once against `git show fec87e14:scripts/orchestrator/hcom-seat` extracted to a scratch path, the way the round-1 `earlier_lever` helper compares) and pass against the head (both outputs pasted). 3. `cmp` 0; `make render-check` 0; validate-agent-assets 0. 4. `make shellcheck` 0; shfmt 0; ruff 0; lint-comparisons 0. 5. The dsh and omp roles' rendered settings stay byte-identical to the round-1 head fec87e14 (the round-1 test, pasted). 6. The table has one row per changed path and no status word outside closed, residual, out-of-scope (grep of the body pasted).

VERIFY
ACCEPTANCE pasted into the body's Verification section and the report.

CLOSURE
remove

TRUST
TRUST: the unit trusts the dsh row's containment rules of U272 and U306 as the model the router row must equal but for the loopback grant and the state root; it trusts `physical_path` as the one resolver; it runs no real dsh, reads no credential.

TIMEBOX
60 minutes.

FORBIDDEN
No change to the omp or dsh rows' rendered settings; no rebase or merge of another branch; no network; no push; no `gh` call; no pin edited by hand; no pipe `|` in any bash command (standing order 46: output to a file under `/tmp/u321b/`, then read it).

WORKER RULES (standing orders 21, 27, 29, 31, 34, 44, 46; read `~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` lines 23 to 62)
- Never run git or edit files in `~/Workspace/dotfiles`, never push, never open or edit a PR, never edit the live store; you stop at a committed head in `/tmp/dotfiles-wt/U321`.
- Progress line at `../U321b-progress.txt`; final report to `../U321b-report.txt`.
- Commit unsigned: `git -c commit.gpgsign=false commit`. The commit message ends with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.

REPORT
Status, head sha (40 hex), `git diff --stat fec87e14 HEAD`, the ACCEPTANCE lines with their outputs, deviations. Under 12 lines, ending with `head=<40 hex>`.

STANDING
`preferences.md` (standing orders 21, 24, 27, 29, 34, 44, 46); `verdicts/U321-fec87e14.md`; the U321 brief `briefs/U321-router-role-of-hcom-seat-with-the-loopback-grant.md`; `verdicts/U317-6eac2332.md` (the containment-boundary class of U317 round 1, the same lesson for the Router's stateDir).
