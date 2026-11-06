# U276d deploy-kit verifies what remains managed, re-checks its roots after status, and applies without recursing

GOAL
The first real `make deploy-kit` on the laptop (2026-11-06T13:33Z, chezmoi source clone at 29439083) applied its 39 pending kit targets and left the Codex and Claude configurations untouched, then exited 2: its post-apply `chezmoi verify` over the applied names met a deleted target (`~/.agents/skills/understand`, retired by the graphify replacement) and chezmoi answered `not managed`. That is the filed P2 at `scripts/deploy-kit.sh:215` of the round-3 verdict (`verdicts/U276c-114b974b.md`), met on the first run; the same verdict filed two more P2 the lever carries: a root replaced by a symlink between the `managed` and `status` reads bypasses the boundary (`:174`, the root's own `MM` status row is discarded by the filter), and `chezmoi apply` recurses into a pending directory, so a child added after `status` is installed although it was never in the managed listing (`:211`). This unit closes the three, so the lever exits 0 on a retirement and keeps its membership and boundary guarantees under a race.

SCOPE
A new branch `fix/deploy-kit-verify-and-recheck` from `origin/main` (your tree is `/tmp/dotfiles-wt/U276d`). May write: `scripts/deploy-kit.sh`, `tests/unit/test_deploy_kit.py`, `README.md` (the deploy-kit paragraph, if a sentence changes), and the body `../U276d-pr-body.md`. Not: the Makefile target, any `home/` file, the updater.

CONTEXT
Read the lever whole, its tests, the three findings' text in the verdict, and the run output pasted below. chezmoi: `chezmoi verify <target>` on a target the source no longer manages exits with `not managed`; a deleted name's verified state is its absence (`! -e` after a `D` row, or `chezmoi managed` no longer listing it). `chezmoi apply --recursive=false <dir>` applies the directory entry alone (confirm the flag on this host's chezmoi, `chezmoi apply --help`). The roots are read physically once at the start; the finding is that a root can be replaced between the reads; the fix is to re-read the roots' physical paths after `status` and before `apply` and refuse on any change, and to refuse an `MM` row on a root itself instead of discarding it.

The run output (13:33Z): the apply printed the diffs of the 39 targets, then `chezmoi: ~/.agents/skills/understand: not managed`, `deploy-kit: chezmoi verify finds an applied target still differing from the source.`, exit 2; a second dry run then printed `pending: 0`.

DATA SHAPE
The pending set is a table of (status letters, name) rows; the post-apply check iterates it by kind: a `D` row is verified by absence (`[ ! -e name ]`, with a link-aware test), every other row by `chezmoi verify` over the names still in the managed listing read once more after the apply (one `managed` read, one `verify` call). The roots are a table of (spelling, physical path) read twice, before `managed` and after `status`, compared row by row. `apply` is called with `--recursive=false` and the names; a directory name whose children are pending appears in the set as its own rows (the filter keeps every pending row under the roots, so children are named explicitly).

CHANGE
1. The three rules per DATA SHAPE.
2. Tests with the recorder fake: a `D` row leaves the run at exit 0 and `verify` is not called for it; a root swapped for a link between `managed` and `status` refuses naming the root; an `MM` row on a root refuses; `apply` receives `--recursive=false`; a pending directory with a child not in the managed listing applies the directory only (the recorder's apply argv has no child); the existing tests stay.
3. Measurement on this host, read-only: `scripts/deploy-kit.sh --dry-run` from your tree (pending expected 0 after the 13:33Z deploy); paste.
4. The body: Summary (the first-run failure quoted), Contract (the verified state of a retired target is its absence), Threat table, Verification (ACCEPTANCE pasted).

ACCEPTANCE
1. `uv run python -m unittest tests.unit.test_deploy_kit tests.unit.test_scratch_git` OK (paste the count; the new tests named).
2. `make shellcheck` exit 0; `scripts/ci/run-on-lint-files.sh shell shfmt -i 4 -sr -d` exit 0; `scripts/ci/run-on-lint-files.sh markdown prettier --check` exit 0; `scripts/ci/run-on-lint-files.sh python ruff format --config ruff.toml --check` exit 0.
3. The CHANGE 3 dry run pasted.
4. `uv run --no-project --with pyyaml scripts/lint-comparisons.py --changed` exit 0.

VERIFY
ACCEPTANCE pasted into the body's Verification section. The coordinator runs `make deploy-kit` after the merge (expected: pending 0, exit 0) and records it.

CLOSURE
allowlist

TRUST
TRUST: the unit trusts chezmoi's target-restricted reads as the oracle and closes three filed findings; it applies nothing on this host (dry run only), reads no credential and opens no network.

TIMEBOX
40 minutes.

FORBIDDEN
No `chezmoi apply` without `--dry-run` on this host; no edit under `home/`; no change to the Makefile; no write under `~/.local`, `~/.agents`, `~/.dsh`, `~/.codex`, `~/.claude`; no local bats; no network; no push; no `gh` call; no pipe `|` in any bash command you run yourself (standing order 46: output to a file under `/tmp/u276d/`, then read it); inside the script a pipe only with `set -o pipefail` and the status read.

WORKER RULES (standing orders 21, 27, 29, 31, 34, 44, 46; read `~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` lines 23 to 62)
- Never run git or edit files in `~/Workspace/dotfiles`, never push, never open or edit a PR, never edit the live store; you stop at a committed head in `/tmp/dotfiles-wt/U276d` and the coordinator fetches it by path.
- Progress line at `../U276d-progress.txt` every ten minutes at most; first edit within ten minutes. Final report to `../U276d-report.txt` before you end.
- Commit unsigned: `git -c commit.gpgsign=false commit`. Every commit message ends with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.
- Comments explain a non-obvious why only, no phase narration. Shell comments are English shdoc.
- Follow `~/.agents/pstack/skills/poteto-mode/SKILL.md` (Fix Root Causes; Model the Domain: the pending set is a table judged by row kind).

REPORT
Status, head sha (40 hex), files changed (`git diff --stat origin/main`), the dry run's pending count, the ACCEPTANCE result lines, deviations. Under 12 lines, ending with `head=<40 hex>`.

STANDING
`preferences.md` (standing orders 21, 27, 29, 30, 34, 44, 46, 48); `verdicts/U276c-114b974b.md` (the three filed P2); `dispositions.tsv` rows of 13:20Z naming U276d; `AGENTS.md` (Test Policy).
