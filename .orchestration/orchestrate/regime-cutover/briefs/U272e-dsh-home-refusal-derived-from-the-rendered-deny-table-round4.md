# U272e round 4 of U272: the DSH_HOME refusal is derived from the rendered deny table, every path physical, the cleanup fails closed

GOAL
The round-3 audit of PR 697 (U272d, head 5b950a97; `verdicts/U272d-5b950a97.md`) found one P1 and two P2. P1 (`hcom-seat:1660`): the `DSH_HOME` refusal compares against the dsh role's own deny row only, so `DSH_HOME=~/.aws` and `DSH_HOME=~/.omp/agent`, paths the inherited worker denies protect, were accepted and granted allowRead and allowWrite. P2 (`:1635`): the records path is appended to the identity table without physical resolution, so a `<checkout>/.orchestration` that is a link into `DSH_HOME` defeats the overlap check. P2 (`:2215`): a directory of mode 000 left by dsh survives the slot removal and the lever still exits 0. Three rounds have each found one hand-listed boundary piece (grants, denies, refusals) missing a member. This round changes the rule's source: the refusal is computed from the settings the role will run under, after they are rendered: a write root (`DSH_HOME`, the scratch cwd, the state slot) may not equal, contain or lie inside any path of the final `denyRead` or `denyWrite` list, every path compared by physical path and by (device, inode) identity, and the comparison runs before any directory is made. The slot cleanup fails closed.

SCOPE
The existing branch `feat/hcom-seat-dsh-role` at 5b950a97028205f7430a7c9f36f74b91a79e88c8 in `/tmp/dotfiles-wt/U272` (the PR is 697). May write: `scripts/orchestrator/hcom-seat` and the deployed copy `home/dot_local/bin/common/executable_hcom-seat` (identical), the pin rows by regeneration (`uv run --with pyyaml scripts/generate-agent-configs.py`), `tests/unit/test_hcom_seat_dsh.py`, `docs/deepseek-harness.md` (one sentence), `../U272-design.md` (the rule), and the body `../U272-pr-body.md` (a Round 4 section, the Contract's refusal sentence, the threat table rows). Not: the omp roles' rendered settings (byte-identical to 5b950a97, the comparison test extended).

CONTEXT
Read the verdict whole; the lever's settings rendering for the dsh role (the deny rows of round 3, the inherited worker denies, the allow rows) and the current `DSH_HOME` refusal (`:1660`), the records path appending (`:1635`), the slot removal (`:2215`). The rendered settings file exists as text before srt runs; the lever can read its own rendered deny lists back (or hold them in the arrays it renders from) and judge the write roots against them. Physical comparison: `pwd -P` of each path's existing ancestor chain, and the lever's identity table by (device, inode) as the omp roles use for the protected set; a deny path that does not exist on the host is compared by its physical parent plus its name. Cleanup: `chmod -R u+rwX` on the slot before `rm -rf`, then a check that the slot is gone; a slot that remains is a refusal with exit non-zero naming the path, never exit 0.

DATA SHAPE
One function `write_root_outside_denies <root> <deny-list>` (the deny list being the rendered `denyRead` plus `denyWrite` paths of the role's final settings), returning the first overlapping deny path or nothing; called for `DSH_HOME`, the scratch cwd and the state slot before any mkdir; every path physical before comparison, the records path included; one cleanup function that removes the slot with the mode reset and verifies absence.

CHANGE
1. The function and its three call sites; the records path resolved physically before it enters the identity table; the cleanup per DATA SHAPE; the design file's rule and the docs sentence.
2. Tests: `DSH_HOME` at a fixture path that the inherited worker denies cover (the fixture's `.aws` and `.omp/agent` equivalents) refuses naming the deny path, before any mkdir (recorder); a `DSH_HOME` containing a denied path refuses; a `.orchestration` that is a link into `DSH_HOME` refuses; a mode-000 directory inside the slot is removed and the run exits 0, and a slot that cannot be removed (a fixture that makes the removal fail) exits non-zero naming the slot; the omp roles' settings byte-identical to 5b950a97; the existing tests stay.
3. Measurement on this host (scratch `DSH_HOME` under `/tmp` as before): launches with `DSH_HOME=$HOME/.aws` and `DSH_HOME=$HOME/.omp/agent` are refused by name without creating anything (list the scratch seats root before and after); `--version` still prints `0.2.1-rc.5`; a dsh-created mode-000 directory in the slot is cleaned (use a fake dsh that creates one); paste.
4. The body's Round 4 section quoting the three findings with each one's change and test; the Contract's refusal sentence states the rule's source (the rendered deny table); ACCEPTANCE pasted.

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
TRUST: the unit trusts the rendered settings as the one statement of the role's boundary and derives the write-root refusal from it; it changes no omp role's rendered settings, reads no credential and opens no network.

TIMEBOX
60 minutes.

FORBIDDEN
No change to the omp roles' rendered settings; no write under `~/.dsh`, `~/.omp`, `~/.agents`, `~/.aws`, `~/.local/state/omp-seats` or `~/Workspace`; no `/v1/messages` request; no local bats; no network; no push; no `gh` call; no pipe `|` in any bash command (standing order 46: output to a file under `/tmp/u272e/`, then read it).

WORKER RULES (standing orders 21, 27, 29, 31, 34, 44, 46; read `~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` lines 23 to 62)
- Never run git or edit files in `~/Workspace/dotfiles`, never push, never open or edit a PR, never edit the live store; you stop at a committed head in `/tmp/dotfiles-wt/U272` and the coordinator fetches it by path.
- Progress line at `../U272e-progress.txt` every ten minutes at most; first edit within ten minutes. Final report to `../U272e-report.txt` before you end.
- Commit unsigned: `git -c commit.gpgsign=false commit`. Every commit message ends with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.
- Comments explain a non-obvious why only, no phase narration. Shell comments are English shdoc.
- Follow `~/.agents/pstack/skills/poteto-mode/SKILL.md` (Model the Domain: one table, the rendered denies, is the boundary; Fix Root Causes: the hand-listed refusal is the cause, not its missing member).

REPORT
Status, head sha (40 hex), files changed (`git diff --stat origin/main`), the rule in one line, the ACCEPTANCE result lines, deviations. Under 14 lines, ending with `head=<40 hex>`.

STANDING
`preferences.md` (standing orders 21, 27, 29, 33, 34, 36, 44, 46); `verdicts/U272d-5b950a97.md`; `briefs/U272-hcom-seat-dsh-role.md`; `../U272-design.md`.
