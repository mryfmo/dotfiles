# U288 the host rows of the test tables are judged on the laptop after the first deploy

GOAL
Standing order 47 runs the verify-and-fix cycle on the macOS laptop first. U274 wrote nine tables under the store's `tests/` (154 macOS rows: 98 `auto` rows judged OK in the worktree, 44 `host` rows and 2 `operator` rows left `pending`, 10 `not-started` rows). The first `make deploy-kit` (2026-11-06T13:33Z) deployed the merged levers and assets to the laptop (understand-* skills retired, the dsh omp-gateway plugin and thak profile, brief-check.py, pr-merge.sh; Codex and Claude settings untouched). This unit judges every `host` row against the deployed kit: run each row's command as written, record `observed`, `verdict` and `ts`, and leave `operator` and `not-started` rows as they are. Every NG is a fix unit for the coordinator; nothing is rewritten to pass.

SCOPE
A scratch copy of the tables: `/tmp/dotfiles-wt/U288-tables/` (the coordinator copies `tests/*.tsv`, `tests/check-tables.py` and `tests/00-derivation-u274.md` there before you start; you never write into the store). A worktree `/tmp/dotfiles-wt/U288` of `origin/main` for the rows whose commands run inside a repository checkout. Not: any repository file, any host file; no seat launch unless a row's command is one (then run it exactly as the row says, once).

CONTEXT
The table form: `id use_case source kind host command expected observed verdict ts`; `check-tables.py` refuses malformed tables (run it before and after). A `host` row's command is to be run from the worktree root unless the command names another cwd; the observed cell is the command's exit status and its output, trimmed to one line of 300 characters with tabs and newlines replaced by spaces; the verdict is `OK` when the observed matches the `expected` cell's statement (judge it as the row's author would, and when the expectation is ambiguous write `NG` with the ambiguity named rather than `OK`). Rows that need a credential the sandbox denies, a seat that is not running, or network are `NG` with the reason, not skipped; the coordinator decides whether the row or the kit is wrong. The seat rows (`hcom list -v`, seat state) read the live seats: `HCOM_DIR=$HOME/.local/state/hcom-regime HCOM_TEAM=regime` is the environment the coordinator's seats use; read, never send.

DATA SHAPE
One runner script `U288-tables/run-host-rows.py` (stdlib, `python3 -I`): reads every table, selects `kind=host host=macos verdict=pending` rows, runs each command with `bash -lc` from the worktree, a 120 s timeout per row, records observed, verdict (from a per-row judge: the expected cell's `exit N` and quoted literals must appear; a row with neither is judged by you and the judgement written into the observed cell as `judged: <why>`), and ts; writes the tables back in place; prints a summary per table (OK, NG, still pending).

CHANGE
1. The runner per DATA SHAPE; run it once over all tables.
2. For every NG, one line in `U288-tables/ng.md`: id, table, command, observed, and your reading of whether the row or the kit is at fault, with the evidence (a file, a line, an exit code).
3. `check-tables.py` over the tables after the run, exit 0.
4. Progress line every ten minutes; the report.

ACCEPTANCE
1. `python3 -I U288-tables/check-tables.py U288-tables/*.tsv` exit 0 before and after; paste both summaries.
2. The runner's per-table summary pasted (OK, NG, pending counts); no `host` row of `host=macos` left `pending` (or each named with why it could not run).
3. `U288-tables/ng.md` pasted (or `none`).
4. `scripts/ci/run-on-lint-files.sh markdown prettier --check` over `ng.md` exit 0 (copy it into the worktree's scratch for the check and remove it after; the worktree stays clean: `git status --porcelain` empty).

VERIFY
The coordinator copies the judged tables back into the store's `tests/` and opens one fix unit per NG that is the kit's fault.

CLOSURE
allowlist

TRUST
TRUST: the unit trusts the rows' commands and expectations as written by U274 and runs them read-only against the deployed kit; it sends nothing on the hcom bus, launches no seat unless a row is a launch, writes nothing outside its scratch directories.

TIMEBOX
60 minutes.

FORBIDDEN
No edit of any row's command or expected cell; no write under `~/Workspace`, `~/.dsh`, `~/.omp`, `~/.agents`, `~/.local`; no `hcom send`; no `gh` call; no push; no `make update` or `make deploy-kit`; no pipe `|` in any bash command you run yourself (standing order 46: output to a file under `/tmp/u288/`, then read it); the row commands run as written.

WORKER RULES (standing orders 21, 27, 29, 31, 34, 44, 46; read `~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` lines 23 to 62)
- Never run git write commands or edit files in `~/Workspace/dotfiles`, never push, never open or edit a PR, never edit the live store; you stop with the judged tables under `/tmp/dotfiles-wt/U288-tables/`.
- Progress line at `/tmp/dotfiles-wt/U288-progress.txt`; final report to `/tmp/dotfiles-wt/U288-report.txt` before you end.
- Follow `~/.agents/pstack/skills/poteto-mode/SKILL.md` (Prove It Works: the real artifact is the deployed kit; Build the Lever: the runner is rerun by the coordinator after every deploy).

REPORT
Status, the per-table counts, the NG list in one line each, deviations. Under 16 lines, ending with `head=<40 hex>` (the origin/main sha of the worktree).

STANDING
`preferences.md` (standing orders 21, 27, 29, 34, 41, 42, 44, 46, 47, 48); `tests/00-derivation-u274.md`; the deploy row of 2026-11-06T13:33Z in `decisions.tsv`.
