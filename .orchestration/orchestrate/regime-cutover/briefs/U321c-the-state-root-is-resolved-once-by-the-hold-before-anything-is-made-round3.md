# U321c round 3 of U321: the Router state root is resolved once, by the hold, before anything of the launch is made

GOAL
The round-2 audit of PR 715 (`verdicts/U321b-7dfaa839.md`, incorrect, class containment-boundary, the second strike) found that `state_root_hold` holds `<DSH_HOME>/router-state` physical and then `seat_write_roots` (`hcom-seat:1567`) resolves the row's path a second time; a swap of `router-state` to an outside link between the two reads, restored before the final check, rendered `~/.config/autostart` as `allowWrite[6]` and the launch succeeded. The decisions row `mechanism-change` of 2026-11-07T02:25:00Z closes the class by removal: the state root is resolved exactly once, by the hold, into a value the write-root rendering consumes verbatim; nothing in the launch reads that path again. The same verdict's P3 (`scripts/orchestrator/README.md:145`): the README says the router refuses before tool resolution, but an invalid-state-root dry run made eight private tool links and ran host git three times before refusing; the hold moves to where the role and argument checks run, before any directory, link or tool of the launch is made, so the sentence becomes true. The P2 (`hcom-seat:292`, weight 20): both documentation threat-table rows are out-of-scope without an owning unit; they name U333 (reserved, the docs-read-by-tests unit) as owner.

SCOPE
The same branch `feat/hcom-seat-router-role` and PR 715; the tree is `/tmp/dotfiles-wt/U321` at 7dfaa839 (two commits on main 247d890d). May write: `scripts/orchestrator/hcom-seat` and its byte-identical copy `home/dot_local/bin/common/executable_hcom-seat`, `tests/unit/test_hcom_seat_dsh.py`, `tests/unit/test_hcom_seat.py`, the regenerated `home/dot_agents/agent-config.yaml` and `scripts/generated-agent-outputs.json` (by `uv run --with pyyaml python scripts/generate-agent-configs.py` only), `scripts/orchestrator/README.md` (the router paragraph only), and the body `../U321c-pr-body.md` (the round-2 body `/tmp/dotfiles-wt/U321b-pr-body.final.md` plus `## Round 3` and the corrected table). Not: the omp or dsh rows' rendered settings, any other lever or doc.

CONTEXT
Read the two verdict files whole (`verdicts/U321-fec87e14.md`, `verdicts/U321b-7dfaa839.md`; the round-2 Reproduced section describes the DEBUG-trap race probe and the instrumented dry run that counted the tool links and git calls), the mechanism-change row, and `hcom-seat` whole: the role table and its new `state_root` cell, `state_root_hold`, `seat_write_roots` (where the row's roots are rendered, and where `:1567` resolves the state root again), `physical_path`, the launch order (argument parsing, the role checks, the passthrough selector refusal of round 2, the private tool directory, the host git reads, `settings_judge`, the sandbox write, the slots), and the dry run's path through it. The round-2 report `/tmp/dotfiles-wt/U321b-report.txt` and body name the tests of rounds 1 and 2.

DATA SHAPE
One value, `STATE_ROOT_PHYS`, set once by `state_root_hold` (the physical path of the held directory, or empty for a row without a state root) and consumed verbatim by `seat_write_roots` for that row; no other function reads the row's `state_root` cell or the path under DSH_HOME after the hold. The hold is one of the pre-launch checks: it runs after the arguments and the role are known and before the first `mkdir`, `ln`, tool copy or host `git` call of the launch (a dry run included), so a bad state root makes nothing. The hold's result is a directory of this user, no link, inside the physical DSH_HOME (both compared in `pwd -P` form); the absent case makes the directory 0700 at the hold itself (the one write before the launch's own writes, inside DSH_HOME, which the dsh row already owns) and re-holds it, so the rendered path always names a directory that existed when it was held. The settings carry `STATE_ROOT_PHYS`; srt enforces the physical directory, and a later swap of the spelled path grants nothing.

CHANGE
1. In `hcom-seat`: `seat_write_roots` takes the held value and resolves nothing for the state-root row (delete the second resolution at `:1567`); `state_root_hold` sets the one variable and moves to the pre-launch checks, before the private tool directory and every host git call, for the dry run too; the passthrough selector refusal of round 2 stays beside it. 2. Tests in `test_hcom_seat_dsh.py`: (a) the auditor's race, as a test: a DEBUG trap or a wrapped `physical_path` that swaps `router-state` to an outside link after the hold and restores the directory before the render; the rendered `allowWrite` row equals the held physical path and nothing outside DSH_HOME appears in the settings (fails against 7dfaa839, passes on the head); (b) a hold whose directory is removed after the hold: the launch refuses at the sandbox write naming the state root (no outside grant); (c) an invalid state root in a dry run: exit 2 with the private tool directory absent, no link made, and zero host git calls (count them with a fake `git` on PATH that records its invocations; fails against 7dfaa839, passes on the head); (d) the round-1 and round-2 tests keep passing; the structural-diff test and the byte-identical tests of the dsh and omp roles keep passing. 3. README router paragraph: the sentence states what the code does after this change (the hold before anything is made; the one resolution). 4. The body's table: the README row and the deepseek-harness row `out-of-scope` naming U333 as owner (its row in `units.tsv`), or `closed` by a test that reads the paragraph if the worker writes one; every other closed row names a selector; statuses only closed, residual, out-of-scope. 5. `cmp`; generator; `make render-check`; `uv run --with pyyaml python scripts/validate-agent-assets.py`; `make shellcheck`; `shfmt -i 4 -sr -d scripts/orchestrator/hcom-seat`; `uv run ruff format --check` in the CI form; `scripts/lint-comparisons.py --changed`. 6. Commit `fix(hcom-seat): the Router state root is resolved once by the hold before anything of the launch is made (regime-cutover U321c)` with the trailer. 7. The body: the round-2 body plus `## Round 3` (the mechanism-change row named, the two verdicts' class, what was removed), the corrected table, ACCEPTANCE pasted; `Program-Unit: regime-cutover/U321` once and the footer.

ACCEPTANCE
1. `uv run --with pyyaml python -m unittest tests.unit.test_hcom_seat_dsh tests.unit.test_hcom_seat -v` OK (count pasted; the new tests named). 2. Tests (a) and (c) of CHANGE 2 fail against 7dfaa839's lever (the `earlier_lever` form) and pass against the head (outputs pasted). 3. `grep -n 'state_root' scripts/orchestrator/hcom-seat` shows the cell read in one place, the hold, and the rendering reading the held variable (pasted). 4. `cmp` 0; `make render-check` 0; validate-agent-assets 0. 5. shellcheck 0; shfmt 0; ruff 0; lint-comparisons 0. 6. The dsh and omp roles' rendered settings byte-identical to 7dfaa839 (the existing test, pasted). 7. The table's statuses are closed, residual or out-of-scope only, and every out-of-scope row names an owning unit (grep pasted).

VERIFY
ACCEPTANCE pasted into the body's Verification section and the report.

CLOSURE
remove

TRUST
TRUST: the unit trusts `physical_path` as the one resolver and srt's enforcement of the physical directory named in the settings; it trusts the dsh row's containment rules (U272, U306) for everything but the state root; it runs no real dsh, reads no credential.

TIMEBOX
60 minutes.

FORBIDDEN
No second read of the state root path after the hold anywhere in the launch; no change to the omp or dsh rows' rendered settings; no rebase or merge; no network; no push; no `gh` call; no pin edited by hand; no pipe `|` in any bash command (standing order 46: output to a file under `/tmp/u321c/`, then read it).

WORKER RULES (standing orders 21, 27, 29, 31, 34, 44, 46; read `~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` lines 23 to 62)
- Never run git or edit files in `~/Workspace/dotfiles`, never push, never open or edit a PR, never edit the live store; you stop at a committed head in `/tmp/dotfiles-wt/U321`.
- Progress line at `../U321c-progress.txt`; final report to `../U321c-report.txt`.
- Commit unsigned: `git -c commit.gpgsign=false commit`. The commit message ends with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.

REPORT
Status, head sha (40 hex), `git diff --stat 7dfaa839 HEAD`, the ACCEPTANCE lines with their outputs, deviations. Under 12 lines, ending with `head=<40 hex>`.

STANDING
`preferences.md` (standing orders 21, 24, 27, 29, 34, 36, 44, 46); `decisions.tsv` row 2026-11-07T02:25:00Z (mechanism-change, remove); `verdicts/U321-fec87e14.md`, `verdicts/U321b-7dfaa839.md`; the U321 brief `briefs/U321-router-role-of-hcom-seat-with-the-loopback-grant.md`; the U321b brief.
