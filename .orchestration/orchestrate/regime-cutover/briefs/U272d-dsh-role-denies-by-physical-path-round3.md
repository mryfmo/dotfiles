# U272d round 3 of U272: the dsh role denies the host's git, hcom and records paths explicitly, and refuses a DSH_HOME that is a git directory

GOAL
The round-2 audit of PR 697 (U272c, head 976fd6cd; `verdicts/U272c-976fd6cd.md`) found two P1. First (`hcom-seat:1876`): srt's read policy is deny-then-allow over an explicit deny list, with everything not denied readable, so round 2's removal of the dsh role's read grants denied nothing: the program's hcom store (`HCOM_DIR`, here `~/.local/state/hcom-regime`), git common directories outside the checkout, and the orchestration records stayed readable from inside the dsh sandbox. Second (`:1453`): `DSH_HOME=<checkout>/.git` passes the omp roles' common-directory overlap exemption and a reproduced launch granted that directory allowRead and allowWrite, so dsh could alter objects and refs. Two P2: a SIGHUP to the launch's process group ends the launcher and dsh and leaves both per-launch slots behind (`:2123`); the `date` producer that names the slot has no failure-injection test (`:256`). This round states the dsh role's containment as denies: the role's settings deny the physical paths of every git directory the lever knows (the checkout's `.git` and its common directory, every linked worktree's git dir), the hcom store (`HCOM_DIR` resolved, and the default location), the orchestration records directory, and the seats root of every other seat; a `DSH_HOME` that is, contains, or lies inside a git directory, the hcom store or the records refuses; SIGHUP (and SIGTERM, SIGINT) run the slot cleanup; the `date` read fails closed with a test.

SCOPE
The existing branch `feat/hcom-seat-dsh-role` at 976fd6cdb249c76ac397ede1bbfccd931ad824c1 in `/tmp/dotfiles-wt/U272` (the PR is 697). May write: `scripts/orchestrator/hcom-seat` and the deployed copy `home/dot_local/bin/common/executable_hcom-seat` (identical), the pin rows by regeneration (`uv run --with pyyaml scripts/generate-agent-configs.py`), `tests/unit/test_hcom_seat_dsh.py`, `docs/deepseek-harness.md` (the containment paragraph), `../U272-design.md` (the role table rows: deny list, DSH_HOME refusals, signals), and the body `../U272-pr-body.md` (a Round 3 section, the threat table rows, the Contract stated as denies). Not: the omp roles' rendered settings (byte-identical before and after, the existing comparison test extended to this head).

CONTEXT
Read the verdict's Findings and Reproduced sections whole, the srt README's read-policy paragraph as the lever's README quotes it (`scripts/orchestrator/README.md:141-173`), the lever's settings rendering (`denyRead`, `allowRead`, `allowWrite`, the overlap exemption for the common directory used by the omp roles, the worker's deny rows), the per-launch slot code and its cleanup, and the `date` producer. The dsh role has no git worktree, no hcom bus and no store, so every one of those paths is a deny for it; the omp roles keep their exemption and grants untouched. Where the lever already computes a path for the omp roles (common directory, store, records, seats root), the dsh row reuses the computed physical path in a deny; what the lever does not compute (other git directories on the host) is out of reach and stays a named residual in the body, not a claim.

DATA SHAPE
Two more rows in the role table: `deny_read_write` per role (the dsh list: the checkout's git dir and common dir, every linked worktree's git dir the lever can list with `git worktree list --porcelain` from the checkout, `HCOM_DIR` resolved physically and `~/.local/state/hcom-*`, the records directory `<checkout>/.orchestration`, the seats root's other seats) and `home_refusals` for the dsh role (a `DSH_HOME` whose physical path equals, contains or is inside any path of that list refuses before any directory is made). Signal handling is one trap installed once for `HUP TERM INT` that runs the same cleanup the normal exit runs. The `date` read is a producer with a status read and a shape check (`^[0-9]{8}T[0-9]{6}Z$` or the lever's existing shape), refusing otherwise.

CHANGE
1. The rows, the trap and the producer per DATA SHAPE; the deployed copy identical; pins regenerated; the design file and the docs paragraph updated to say denies, not removed grants.
2. Tests: the rendered dsh settings carry a denyRead and denyWrite row for each path of the list (fixture paths); a `DSH_HOME` equal to the checkout's `.git`, inside it, and containing the hcom store each refuse with the path named before any mkdir (recorder: no mkdir); SIGHUP to a held launch removes both slots (a fake dsh that sleeps; send HUP to the lever's process group; assert the slot directories are gone and the exit status names the signal); a failing and a malformed `date` each refuse; the omp roles' settings byte-identical to 976fd6cd (extend the existing archive comparison to this head); the existing tests stay.
3. Measurement on this host (scratch `DSH_HOME` under `/tmp` as U272 did, writes only under `/tmp`): a probe under the role that reads the hcom store directory, the checkout's git common directory and the records directory is denied for each (paste the srt denial lines); `--version` still prints `0.2.1-rc.5`; a launch with `DSH_HOME=<scratch>/.git` is refused by name; paste.
4. The body's Round 3 section quoting the four findings with each one's change and test; the Contract rewritten as denies with the residual (git directories the lever does not know) named; ACCEPTANCE pasted.

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
TRUST: the unit trusts srt's deny-then-allow model as the README states it and hcom-seat's settings rendering; it adds deny rows, a refusal, a trap and a producer check for the dsh role, changes no omp role's rendered settings, reads no credential and opens no network.

TIMEBOX
60 minutes.

FORBIDDEN
No change to the omp roles' rendered settings; no write under `~/.dsh`, `~/.omp`, `~/.agents`, `~/.local/state/omp-seats` or `~/Workspace`; no `/v1/messages` request; no local bats; no network; no push; no `gh` call; no pipe `|` in any bash command (standing order 46: output to a file under `/tmp/u272d/`, then read it).

WORKER RULES (standing orders 21, 27, 29, 31, 34, 44, 46; read `~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` lines 23 to 62)
- Never run git or edit files in `~/Workspace/dotfiles`, never push, never open or edit a PR, never edit the live store; you stop at a committed head in `/tmp/dotfiles-wt/U272` and the coordinator fetches it by path.
- Progress line at `../U272d-progress.txt` every ten minutes at most; first edit within ten minutes. Final report to `../U272d-report.txt` before you end.
- Commit unsigned: `git -c commit.gpgsign=false commit`. Every commit message ends with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.
- Comments explain a non-obvious why only, no phase narration. Shell comments are English shdoc.
- Follow `~/.agents/pstack/skills/poteto-mode/SKILL.md` (Boundary Discipline: containment is a deny list the role owns; Attack the Premise: round 2 assumed a removed grant is a deny).

REPORT
Status, head sha (40 hex), files changed (`git diff --stat origin/main`), the dsh deny list in one line, the ACCEPTANCE result lines, deviations. Under 14 lines, ending with `head=<40 hex>`.

STANDING
`preferences.md` (standing orders 21, 27, 29, 33, 34, 36, 44, 46); `verdicts/U272c-976fd6cd.md`; `briefs/U272-hcom-seat-dsh-role.md`; `../U272-design.md`; `scripts/orchestrator/README.md:141-173`.
