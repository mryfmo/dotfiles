# U272g round 6 of U272: an exemption names one rendered row by identity, and a failed existence read is not an absence

GOAL
The round-5 audit of PR 697 (U272f, head d1919112; `verdicts/U272f-d1919112.md`) found one P1 at `hcom-seat:1863`: the structural exemption tags of the judge are keyed by path, so a launch with `DSH_HOME=~/.omp/profiles`, or a `~/.omp/run` linked to `~/.omp/profiles`, inherits the own-profile exemption and the whole profiles directory is rendered into `allowWrite`, letting dsh overwrite other roles' state; and one P2 at `:2347`: an unsearchable `.state` parent makes both existence tests false, so the cleanup reads an inaccessible slot as absent and the launch exits 0 with the slot left. This round keys every exemption to the exact identity of the one rendered row it exempts: the exempted grant must be byte-equal to the row the lever itself rendered for that purpose (the own profile directory `~/.omp/profiles/dsh`, the own slot, the cwd's project files) and equal by (device, inode) where it exists; a grant that merely lies under the same deny is judged like any other and refuses. The cleanup's existence reads distinguish a failed read (EACCES, ENOTDIR, EPERM) from an absence and treat a failed read as a remaining slot (exit 2 naming the path).

SCOPE
The existing branch `feat/hcom-seat-dsh-role` at d191911256d88f4a71ebde559500353dbc4d1e19 in `/tmp/dotfiles-wt/U272` (the PR is 697). May write: `scripts/orchestrator/hcom-seat` and the deployed copy `home/dot_local/bin/common/executable_hcom-seat` (identical), the pin rows by regeneration, `tests/unit/test_hcom_seat_dsh.py`, `../U272-design.md` (the exemption rule), and the body `../U272-pr-body.md` (a Round 6 section, the Contract's exemption sentence, the threat rows). Not: the omp roles' rendered settings (byte-identical to d1919112, the comparison test extended).

CONTEXT
Read the verdict whole, the judge and its tags (how a tag is attached at render time and how the judge reads it), the three exempted rows and where each is rendered, the cleanup's existence tests. The exemption's source of truth is the render site: the lever renders the own-profile row from its own computed path, so the tag can carry that exact path (or its identity) and the judge compares the grant to it by equality, never by prefix. A `DSH_HOME` that equals or contains an exempted row's path is itself a grant under a deny and refuses. Existence reads: `[ -e ]` is false for both an absent path and an unreadable parent; use `stat` (or `ls -d`) with its status and stderr read, or test the parent's searchability first, so that EACCES refuses.

DATA SHAPE
Each tag carries the exact path (and, when it exists, the identity) of the single row it exempts; the judge exempts a grant only when its path equals the tag's path (and its identity matches when both exist); every other grant under a deny refuses. The cleanup reads each slot through a status-checked producer: 0 means present, a documented "no such file" means absent, anything else is a failed read and a refusal naming the path.

CHANGE
1. The exemption keying and the cleanup reads per DATA SHAPE; the design file's rule; the Contract sentence.
2. Tests: `DSH_HOME=<fixture>/.omp/profiles` refuses naming the profiles deny; a `~/.omp/run` linked to the profiles directory refuses; the own profile row still passes; an unsearchable `.state` parent at cleanup exits 2 naming the slot (not 0); the three round-5 cases and the omp roles' byte-identical settings stay.
3. Measurement on this host (scratch `HOME` and `DSH_HOME` under `/tmp`): a launch with `DSH_HOME=<scratch>/.omp/profiles` is refused by name and nothing is created; `--version` with a normal `DSH_HOME` still prints `0.2.1-rc.5`; a cleanup with the scratch `.state` made mode 000 exits 2 naming the slot; paste.
4. The body's Round 6 section quoting the two findings with each one's change and test; ACCEPTANCE pasted.

ACCEPTANCE
1. `uv run python -m unittest tests.unit.test_hcom_seat tests.unit.test_hcom_seat_dsh tests.unit.test_generate_agent_configs` OK (paste the count; the new tests named).
2. `make shellcheck` exit 0; `scripts/ci/run-on-lint-files.sh shell shfmt -i 4 -sr -d` exit 0; `scripts/ci/run-on-lint-files.sh python ruff format --config ruff.toml --check` exit 0; `scripts/ci/run-on-lint-files.sh markdown prettier --check` exit 0.
3. `cmp scripts/orchestrator/hcom-seat home/dot_local/bin/common/executable_hcom-seat` exit 0; `make render-check` exit 0.
4. The CHANGE 3 measurements pasted.
5. `uv run --no-project --with pyyaml scripts/lint-comparisons.py --changed` exit 0.

VERIFY
ACCEPTANCE pasted into the body's Verification section. The coordinator runs the audit at the new head.

CLOSURE
allowlist

TRUST
TRUST: the unit trusts the rendered rows as the boundary and narrows the exemptions to exact rows; it changes no omp role's rendered settings, reads no credential and opens no network.

TIMEBOX
45 minutes.

FORBIDDEN
No prefix or ancestor match in any exemption; no change to the omp roles' rendered settings; no write under `~/.dsh`, `~/.omp`, `~/.agents`, `~/.aws`, `~/.local/state/omp-seats` or `~/Workspace`; no `/v1/messages` request; no local bats; no network (no `git fetch`); no push; no `gh` call; no pipe `|` in any bash command (standing order 46: output to a file under `/tmp/u272g/`, then read it).

WORKER RULES (standing orders 21, 27, 29, 31, 34, 44, 46; read `~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` lines 23 to 62)
- Never run git or edit files in `~/Workspace/dotfiles`, never push, never open or edit a PR, never edit the live store; you stop at a committed head in `/tmp/dotfiles-wt/U272` and the coordinator fetches it by path.
- Progress line at `../U272g-progress.txt` after every step; first edit within ten minutes. Final report to `../U272g-report.txt` before you end; deliverables beside the worktree, never in the store.
- Commit unsigned: `git -c commit.gpgsign=false commit`. Every commit message ends with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.
- Comments explain a non-obvious why only, no phase narration. Shell comments are English shdoc.
- Follow `~/.agents/pstack/skills/poteto-mode/SKILL.md` (Type System Discipline: an exemption is a reference to one row, not a pattern; Fix Root Causes).

REPORT
Status, head sha (40 hex), files changed (`git diff --stat` against d1919112 and against the merge base, no fetch), the exemption rule in one line, the ACCEPTANCE result lines, deviations. Under 14 lines, ending with `head=<40 hex>`.

STANDING
`preferences.md` (standing orders 21, 27, 29, 33, 34, 36, 44, 46); `verdicts/U272f-d1919112.md`; the mechanism-change row of 2026-11-06T15:29:24Z; `../U272-design.md`.
