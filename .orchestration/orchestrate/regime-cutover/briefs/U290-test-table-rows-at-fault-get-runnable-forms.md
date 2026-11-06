# U290 the test rows at fault get the kit's real expectation and a runnable form

GOAL
The first judgment of the host rows on the laptop (U288, `tests/ng-u288.md`) left thirteen NG rows; eight of them are the tables' fault, not the kit's: `k10` expects directory symlinks under `~/.claude/skills` while the kit links one `SKILL.md` per skill by design (`scripts/generate-agent-configs.py:1118`, manifest comment `home/dot_agents/agent-config.yaml:74`); `o15` expects an orchestrator seat on the bus while the program's coordinator is this Claude Code chat by the operator's standing decision; `f12` is a placeholder sentence and a TASK send, not a command; `d22` needs a hook written into the operator's Claude settings; `s17`, `s18` and `s19` must be typed into a live seat pane; `f23`'s wording names "lint jobs" that do not exist as CI contexts (lint runs inside the `test` job). This unit rewrites those rows so that each has the kit's real expectation and a command the runner (`tests/run-host-rows.py`) can run without sending on the bus, launching a seat or editing a host file, then re-runs them.

SCOPE
A scratch copy of the tables at `/tmp/dotfiles-wt/U290-tables/` (the coordinator copies `tests/*.tsv`, `tests/check-tables.py`, `tests/run-host-rows.py`, `tests/ng-u288.md` and `tests/00-derivation-u274.md` there). A worktree `/tmp/dotfiles-wt/U290` of `origin/main` for commands that run inside a checkout. Not: the store, any repository or host file, the rows that are the kit's fault (`d20`, `d21`, `d24`, `g13`, `k13`), which stay NG as judged.

DATA SHAPE
Each corrected row keeps its id and use case; its `source` cites the kit file and line that defines the behaviour; its `command` is a shell command the runner can run read-only (for a seat's containment, `srt --settings <the seat's rendered srt-settings.json> -- <probe>`, with the settings path read from the seats root, or the lever's dry-run form; for the intake rung, the dry form of `hcom-dispatch` if it has one, else a read of the bus listing that proves the rung's precondition and a second row marked `operator` for the live send); its `expected` states the observable; `observed`, `verdict`, `ts` are cleared to `pending` and then filled by the runner. `o15`'s expectation becomes the roster the program runs today (the sweep and worker seats listening; the coordinator as the bus's coordinator name, read from `hcom list -v`) and a second `not-started` row names the orchestrator seat as the M-24 item. The `f23` row's wording names the CI contexts that exist (`test (...)`, `validate`, `regime`, `public-bootstrap (...)`).

CHANGE
1. The eight rows rewritten per DATA SHAPE in the scratch tables; the `sweep-lira active: ask` observation of `o15` recorded as a note in `ng.md` for the coordinator (a possibly blocked seat), not as a row.
2. `python3 -I check-tables.py` over the nine tables exit 0; `python3 -I run-host-rows.py` over the eight rows (the runner selects `pending` host rows) and their verdicts pasted; a rewritten row that is NG stays NG with its observed cell.
3. `U290-tables/changes.md`: one line per rewritten row (id, what was wrong, the new expectation's source).

ACCEPTANCE
1. `python3 -I U290-tables/check-tables.py <the nine tables>` exit 0, summaries pasted.
2. The runner's summary over the eight rows pasted; each row's verdict named.
3. `U290-tables/changes.md` pasted.
4. `scripts/ci/run-on-lint-files.sh markdown prettier --check` over `changes.md` exit 0 (as U288 did: git-add a copy under the worktree's scratch, check, reset and remove; the worktree stays clean).

VERIFY
The coordinator copies the corrected tables back into the store's `tests/`.

CLOSURE
allowlist

TRUST
TRUST: the unit trusts the kit's sources as the definition of each expectation and the runner as the judge; it sends nothing on the bus, launches no seat, writes nothing outside its scratch directories.

TIMEBOX
45 minutes.

FORBIDDEN
No change to a row that is the kit's fault; no `hcom send`; no seat launch; no edit under `~/Workspace`, `~/.claude`, `~/.dsh`, `~/.omp`, `~/.agents`, `~/.local`; no `gh` write; no push; no pipe `|` in any bash command you run yourself (standing order 46: output to a file under `/tmp/u290/`, then read it).

WORKER RULES (standing orders 21, 27, 29, 31, 34, 44, 46; read `~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` lines 23 to 62)
- Never run git write commands or edit files in `~/Workspace/dotfiles`, never push, never open or edit a PR, never edit the live store; you stop with the corrected tables under `/tmp/dotfiles-wt/U290-tables/`.
- Progress line at `/tmp/dotfiles-wt/U290-progress.txt`; final report to `/tmp/dotfiles-wt/U290-report.txt` before you end.
- Follow `~/.agents/pstack/skills/poteto-mode/SKILL.md` (Test Behavior, Not Implementation: a row asserts what the kit's user observes; Build the Lever).

REPORT
Status, the eight rows with their new verdicts, deviations. Under 14 lines, ending with `head=<40 hex>` (the origin/main sha of the worktree).

STANDING
`preferences.md` (standing orders 21, 27, 29, 34, 41, 42, 44, 46, 47); `tests/ng-u288.md`; `tests/00-derivation-u274.md`.
