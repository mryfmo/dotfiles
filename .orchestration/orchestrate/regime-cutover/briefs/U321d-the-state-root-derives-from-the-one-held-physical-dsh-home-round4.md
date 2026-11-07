# U321d round 4 of U321: the Router state root derives from the one held physical DSH_HOME, after its deny judgement, before any write

GOAL
The round-3 audit of PR 715 (`verdicts/U321c-b80a4794.md`, incorrect, class containment-boundary, the first strike after the mechanism-change row of 02:25:00Z) found the parent alias: `state_root_hold` (`hcom-seat:630`) resolves `<DSH_HOME>/router-state` once, but `DSH_HOME` itself is a path the seat's user can retarget (a link at the seat-writable physical home); the auditor retargeted the `DSH_HOME` link during the hold and restored it afterwards, and the launch carried `allowWrite[3]` at the real home and `allowWrite[6]` at `~/.config/autostart/router-state`. The fix the verdict names: retain one physical home and derive both the DSH_HOME grant and the state root from it. The filed P2 (`hcom-seat:635`, f2 s3): the `mkdir` of `router-state` runs before `DSH_HOME`'s deny judgement, so `router --home ~/.ssh --dry-run` creates `~/.ssh/router-state` before refusing the denied home, where the dsh role refuses without a write; the hold must run after the home is judged and must make nothing in a dry run.

SCOPE
The same branch `feat/hcom-seat-router-role` and PR 715; the tree is `/tmp/dotfiles-wt/U321` at b80a4794 (three commits on main 247d890d). May write: `scripts/orchestrator/hcom-seat` and its byte-identical copy `home/dot_local/bin/common/executable_hcom-seat`, `tests/unit/test_hcom_seat_dsh.py`, the regenerated `home/dot_agents/agent-config.yaml` and `scripts/generated-agent-outputs.json` (by `uv run --with pyyaml python scripts/generate-agent-configs.py` only), `scripts/orchestrator/README.md` (the router paragraph only, if a sentence becomes untrue), and the body `../U321d-pr-body.md` (the round-3 body `/tmp/dotfiles-wt/U321c-pr-body.final.md` plus `## Round 4`). Not: the omp or dsh rows' rendered settings, any other lever or doc.

CONTEXT
Read the three verdict files whole (`verdicts/U321-fec87e14.md`, `verdicts/U321b-7dfaa839.md`, `verdicts/U321c-b80a4794.md`; the round-3 Reproduced section describes the two DEBUG-trap probes that moved `DSH_HOME` during the hold, one through a link inside the seat-writable physical home, and the denied-home probe). Read `hcom-seat` whole at this head: where `DSH_HOME` is read, resolved physically and judged against the deny table (the dsh row's `settings_judge` and the DSH_HOME refusal of U272d and U272e, "a DSH_HOME at or inside an exempted row's path is judged like any row"), `state_root_hold` (`:611-646`), `seat_write_roots`, `seat_sandbox_write`, and the pre-launch check order. The dsh row already holds one physical `DSH_HOME` for its own grant; the router row must use that same value, never re-read the variable or the spelled path.

DATA SHAPE
One physical home, `DSH_HOME_PHYS`, resolved once by the dsh-row code path that judges the home against the deny table, held in a variable; every later use of the home (the DSH_HOME grant, the environment line, the state root) reads that variable. The state root is `${DSH_HOME_PHYS}/router-state`, held by `state_root_hold` from the held physical home (opened relative to it, never through the spelled `DSH_HOME`), a directory of this user and no link, inside the held home by prefix on physical forms; absent, it is made 0700 only in a real launch, after the home's deny judgement passed, and never in a dry run (a dry run reports what would be made). A `DSH_HOME` whose physical form changes between the judgement and the render cannot change the render, because the render reads the variable; a test moves the link between the two and asserts the rendered rows all name the held physical home.

CHANGE
1. Hold `DSH_HOME_PHYS` once where the dsh row resolves and judges the home; make the DSH_HOME grant, the environment line and the router state root read it (delete every later resolution or re-read of `DSH_HOME` for those uses). 2. Order: the home's deny judgement, then `state_root_hold`, then the private tool directory and the rest; the hold makes the directory only in a real launch after the judgement (a dry run makes nothing and prints the would-make line). 3. Tests in `test_hcom_seat_dsh.py`: (a) the auditor's parent-alias race (a DEBUG trap or wrapped `physical_path` retargets the `DSH_HOME` link after the judgement and restores it before the render): every `allowWrite` row under the home names the held physical home and nothing outside it appears (fails against b80a4794, passes on the head); (b) `router --home ~/.ssh --dry-run` on the fixture refuses the denied home with no directory made under it (fails against b80a4794: the directory appears; passes on the head); (c) the dry run with an absent state root makes nothing and prints the would-make line; (d) the round-1 to round-3 tests keep passing; the structural-diff and byte-identical tests of the dsh and omp roles keep passing. 4. README: the router paragraph's sentences true of the code. 5. The body's table: statuses closed, residual or out-of-scope only, every out-of-scope row naming its owner (U333), every closed row a selector; `## Round 4` naming the class, the three verdicts and what was removed. 6. `cmp`; the generator; `make render-check`; `uv run --with pyyaml python scripts/validate-agent-assets.py`; `make shellcheck`; `shfmt -i 4 -sr -d scripts/orchestrator/hcom-seat`; `uv run ruff format --check` in the CI form; `scripts/lint-comparisons.py --changed`. 7. Commit `fix(hcom-seat): the Router state root derives from the one held physical DSH_HOME after its deny judgement, and a dry run makes nothing (regime-cutover U321d)` with the trailer. 8. The body: `Program-Unit: regime-cutover/U321` once and the footer; under 64 KiB.

ACCEPTANCE
1. `uv run --with pyyaml python -m unittest tests.unit.test_hcom_seat_dsh tests.unit.test_hcom_seat -v` OK (count pasted; the new tests named). 2. Tests (a) and (b) fail against b80a4794's lever (the `earlier_lever` form) and pass on the head (outputs pasted). 3. `grep -n 'DSH_HOME' scripts/orchestrator/hcom-seat` pasted with one line per use, each use reading the held variable after the judgement or being the judgement itself. 4. `cmp` 0; `make render-check` 0; validate-agent-assets 0. 5. shellcheck 0; shfmt 0; ruff 0; lint-comparisons 0. 6. The dsh and omp roles' rendered settings byte-identical to b80a4794 (the existing test, pasted), the dsh row's own DSH_HOME behaviour unchanged. 7. The table's statuses and owners (grep pasted); body under 64 KiB (`wc -c` pasted).

VERIFY
ACCEPTANCE pasted into the body's Verification section and the report.

CLOSURE
remove

TRUST
TRUST: the unit trusts `physical_path` as the one resolver and srt's enforcement of the physical directories named in the settings; it trusts the dsh row's deny judgement of the home (U272d, U272e) as the gate the router row runs behind; it runs no real dsh, reads no credential.

TIMEBOX
60 minutes.

FORBIDDEN
No read of `DSH_HOME` or the spelled state root after the judgement other than the held variable; no write in a dry run; no change to the omp or dsh rows' rendered settings; no rebase or merge; no network; no push; no `gh` call; no pin edited by hand; no pipe `|` in any bash command (standing order 46: output to a file under `/tmp/u321d/`, then read it).

WORKER RULES (standing orders 21, 27, 29, 31, 34, 44, 46; read `~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` lines 23 to 62)
- Never run git or edit files in `~/Workspace/dotfiles`, never push, never open or edit a PR, never edit the live store; you stop at a committed head in `/tmp/dotfiles-wt/U321`.
- Progress line at `../U321d-progress.txt`; final report to `../U321d-report.txt`.
- Commit unsigned: `git -c commit.gpgsign=false commit`. The commit message ends with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.

REPORT
Status, head sha (40 hex), `git diff --stat b80a4794 HEAD`, the ACCEPTANCE lines with their outputs, deviations. Under 12 lines, ending with `head=<40 hex>`.

STANDING
`preferences.md` (standing orders 21, 24, 27, 29, 34, 36, 44, 46); `decisions.tsv` row 2026-11-07T02:25:00Z (mechanism-change, remove); `verdicts/U321-fec87e14.md`, `verdicts/U321b-7dfaa839.md`, `verdicts/U321c-b80a4794.md`; the U321c brief; the U272d and U272e rows of units.tsv (the DSH_HOME deny judgement).
