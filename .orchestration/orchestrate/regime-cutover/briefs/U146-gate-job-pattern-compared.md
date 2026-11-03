# U146 the gate-job pattern compared for the two platform workflows, recorded, no workflow change

GOAL
The e2e research decision of 2026-11-02 left one question for the platform workflows: should `ubuntu.yaml` and `macos.yaml` become required checks of `main` through a `changes` job and a `<workflow> gate` job, or stay optional checks behind their workflow-level `paths:` filters? Default: stay optional, the comparison is a records row, any workflow change is its own later unit. This unit is records only. It measures the two workflows, the ruleset of `main` and the merge lever, writes the comparison table below, and lands two `decisions.tsv` rows: the outcome per workflow with its reason, and the answer to the open question. No file outside the store changes.

SCOPE
No branch. Writes: `decisions.tsv` (two rows) and `units.tsv` (this unit's row) in the program store, carried to `main` by the next records sync. Nothing else.

CONTEXT
Measured 2026-11-04 on `origin/main` a64fe727 by the coordinator.

| workflow | trigger filter today | required by the `main` ruleset today | gate-job cost | outcome |
| --- | --- | --- | --- | --- |
| `ubuntu.yaml` | workflow-level `paths:` on `push` and `pull_request` (lines 6 to 14 and 18 to 26): the workflow file, `setup.sh`, `install/common/**`, `install/ubuntu/**`, the common and ubuntu chezmoiscripts, the common and ubuntu install tests | no (the ruleset `main integration gate`, id 24397953, requires `public-bootstrap` three cells, `regime`, `test` three cells, `validate`; neither `Ubuntu` nor `MacOS` is named) | a `changes` job (a third-party action such as dorny/paths-filter, pinned by sha and reviewed, or a copy of the `decide` step `test.yaml` lines 71 to 152 use) deciding the build job, a `ubuntu gate` job with `if: always()` failing on a failed or cancelled need, the `paths:` filter removed so the gate always reports, and a ruleset edit naming the gate; two full `setup.sh` runs and the Bats file suites in the build job (60-minute job timeout, line 72) | stays an optional check with its `paths:` filter |
| `macos.yaml` | the same `paths:` set with `macos` for `ubuntu` (lines 6 to 14 and 18 to 26) | no (same ruleset) | the same three jobs plus the benchmark push the `build` job already serialises (`max-parallel: 1`, the `macos-benchmark` concurrency group of U110), on macOS runners | stays an optional check with its `paths:` filter |

Three facts decide the outcome. First, gate G13 of the store's `gates.md` (operator): both workflows' `build` job is skipped on every run because the repository secrets `EMAIL_ADDRESS` and `PRIVATE_DOTFILES_PRIVATE_DEPLOY_KEY` are not available to the runs (`ubuntu.yaml:49-65`; the `secrets` job of run 41619303506 printed `HAS_EMAIL_ADDRESS: false` and `HAS_PRIVATE_DOTFILES_KEY: false` on a push to `main` by the operator, `BOT_ACTOR: false`), and none of the last 200 `Ubuntu` runs lasted over 120 seconds; the operator's decision was to keep the workflows and make the skip visible. A gate job passes over a skipped need, so a required `ubuntu gate` or `macos gate` would report green on every pull request and verify nothing until the secrets exist. Second, the merge lever `pr-merge.sh` reads every check reported on the head through `gh pr checks` and exits 2 unless at least one check exists and every bucket is `pass` or `skipping` (its header, lines 65 to 68), so on a program pull request whose paths match the filter, a red `Ubuntu` or `MacOS` run already blocks the merge, and a run the filter skips reports nothing and blocks nothing; the ruleset adds no gate the lever lacks. Third, the hazard the `test.yaml` comment names (lines 4 to 8: a required check that never reports leaves the merge pending) is exactly what the `paths:` filters would cause if the two were required as they are, so requiring them is never a ruleset edit alone; it is the three-job workflow change above, which is its own unit when the operator asks for it. The patterns the research lists beyond the gate job (committed recordings replayed read-only, a definition of done, repository-only skills, the escalation ladder, a behaviour-first benchmark, a written trust model) were compared in the decision of 2026-11-02 and create no unit here.

CHANGE
1. Row one (phase `records`, decision starting `M-11 gate-job comparison:`): for `ubuntu.yaml` and for `macos.yaml`, the outcome `stays an optional check with its workflow-level paths filter` and the three reasons above in one sentence each, naming `pr-merge.sh`'s check read, gate G13 and the `test.yaml` comment; evidence names the ruleset id and its eight required contexts, run 41619303506, and the 200-run measurement; result names the default applied and that a workflow change is its own later unit.
2. Row two (phase `records`, decision starting `open question 8:`): the answer, both workflows stay optional, with the row-one timestamp as its evidence and the note that the design document's text changes by the coordinator's hand outside this repository.
3. The `units.tsv` row for U146 (`track` records, state `done` once both rows are written, pr `-`, head `-`).

ACCEPTANCE
1. `awk -F'\t' '$3 ~ /^M-11 gate-job comparison:/' .orchestration/orchestrate/regime-cutover/decisions.tsv` prints one row naming both workflows, their outcome and the three reasons. 2. `awk -F'\t' '$3 ~ /^open question 8:/' .orchestration/orchestrate/regime-cutover/decisions.tsv` prints one row. 3. `awk -F'\t' 'NR>1 && NF!=6' .orchestration/orchestrate/regime-cutover/decisions.tsv` prints nothing. 4. `grep -c '^    paths:' .github/workflows/ubuntu.yaml .github/workflows/macos.yaml` prints 2 for each file (the two trigger blocks), unchanged by this unit. 5. The next records sync carries the rows to `main` and is audited and merged through the levers.

VERIFY
The commands of ACCEPTANCE 1 to 4 run by the coordinator in the checkout, their output pasted into the unit's REPORT line in `units.tsv`.

TIMEBOX
20 minutes.

FORBIDDEN
No change to any workflow, test, document or ruleset; no `gh api` write; no row naming a private design directory or any word of `redact-words.txt`.

REPORT
The `units.tsv` note: the two row timestamps, the ruleset facts (id 24397953; `Ubuntu` and `MacOS` absent from its eight required contexts, read through `gh ruleset view` because the agent tool policy blocks the `gh api` form the plan named), the run id and the 200-run measurement.

STANDING
`~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md`; `gates.md` row G13 in the same store; `.github/workflows/test.yaml:4-8`; `scripts/orchestrator/pr-merge.sh:65-68`.
