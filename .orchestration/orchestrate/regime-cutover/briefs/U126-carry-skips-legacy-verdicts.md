# U126 The carry lever treats an earlier verdict of a reader before U125 as nothing to carry, not as a malformed store

GOAL
`audit-carry.py` (U122) reads the unit's earlier audited head's verdict file to carry its findings into the next audit as data. It refuses a file without a `## Findings` section as a malformed store (exit 2) and `pr-audit.sh` then refuses the audit. The store holds 220 verdict files of the omp-run route (retired 2026-10-25, no `## Findings` section) and 24 of the reader before U125 (unscored lines), and two open units, U107 (PR 582) and U114 (PR 588), have such a file as their earlier verdict, so their re-audit cannot run (refusal on PR 588 at 2026-10-31T03:29Z). `filed-findings.py` (U125 round d) already names the rule: a verdict without the `Filed: <n>` line is an earlier reader's and carries nothing to read. The carry lever applies the same rule, so a legacy earlier verdict means no carried block, and the audit runs.

SCOPE
One branch `fix/carry-skips-legacy-verdicts` from `origin/main`. May write: `scripts/orchestrator/audit-carry.py` (the earlier-verdict read in the carry and `--render` paths), `tests/unit/test_audit_carry.py`, `scripts/orchestrator/README.md` (the audit-carry row), `scripts/orchestrator/filed-findings.py` only to import the shared predicate instead of its own copy. Not `pr-audit.sh`, not `pr-merge.sh`.

CHANGE
1. One predicate, `scored(verdict_file)` in `audit-carry.py` (moved from `filed-findings.py`, which imports it): the file holds the `Filed: <n>` line the scored reader writes. The carry decision and `--render` read the earlier head's verdict through it first: a file the predicate rejects is a legacy verdict; the lever prints `not carried: <file> is a verdict of a reader before U125, nothing to carry` on stderr and exits 1 (the status `pr-audit.sh` reads as no earlier audited head), writes no row and renders no block. A file the predicate accepts is read as today, strictly. A file that cannot be read at all (OSError) stays exit 2 naming it (standing order 21: a failed read is never an absence; a legacy file is read and judged by its content, which is an absence of scores, not a failed read).
2. Tests: an earlier verdict with no `## Findings` section (the omp-run shape, a copy of a real one's lines) is exit 1 with the message and no row, in the carry path and in `--render`; an earlier verdict in the pre-U125 reader shape (`Blocking:` without `Filed:`) likewise; a scored one still carries; an unreadable file is still exit 2; `filed-findings.py` behaviour unchanged with the shared predicate. Red proof on `git archive` of origin/main: the two legacy shapes exit 2 today.

ACCEPTANCE
1. `uv run --no-project --with pyyaml python -m unittest tests.unit.test_audit_carry tests.unit.test_filed_findings tests.unit.test_scratch_git` OK. 2. ruff format check; `scripts/lint-comparisons.py --changed` exit 0; the generator check up to date. 3. The PR body's Contract states the rule (a legacy verdict carries nothing and blocks nothing; a failed read still refuses) and what it leaves out (findings of a legacy verdict are never carried as data; the next audit of such a unit is a census).

CLOSURE
parser-module: one predicate in `audit-carry.py` decides what a scored verdict is, read by the carry lever and `filed-findings.py` alike; no second spelling of the `Filed:` marker.

TRUST
TRUST: the unit trusts the `Filed: <n>` line as the one mark of the scored reader (U125 round a writes it and nothing before did), and it trusts the store's verdict files as the coordinator's own records; it does not read ledger rows to guess a verdict's shape.

TIMEBOX
40 minutes.

FORBIDDEN
No change to `pr-audit.sh` or `pr-merge.sh`; no edit of any stored verdict file; no `codex` or `gh` write.

WORKER RULES (standing orders 27, 29, 31, 34; read `preferences.md` lines 23 to 45 in the store)
- Never run git or edit files in `~/Workspace/dotfiles` (the coordinator's checkout), never push, never open or edit a PR, never edit the live store; you stop at a committed head in your tree and the coordinator fetches it by path and pushes. Your tree is made by the coordinator with `worker-worktree.sh`; every command runs with it as cwd. Never `git stash`. No `/tmp` literal in tracked files.
- Run every test in the foreground with a timeout and paste its result line; write a progress line beside your tree (`../U126-progress.txt`) every ten minutes at most; read only the ranges you need (`grep -n`, then bounded reads; never `audit-carry.py` whole) and make your first edit within ten minutes.
- Commit unsigned: `git -c commit.gpgsign=false commit`. Every commit message ends with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.
- Write the PR body beside your tree (`../U126-pr-body.md`) with `## Summary`, `## Contract` (with a `Trusted:` sentence), `## Threat table` (`row | risk | status | evidence`), `## Verification`, the line `Program-Unit: regime-cutover/U126`, a blank line, then `🤖 Generated with [Claude Code](https://claude.com/claude-code)`.

REPORT
Status, head sha (40 hex), files changed, the result lines, the red proof, deviations. Under 15 lines, ending with `head=<40 hex>`.

STANDING
`~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` (orders 35 to 39); decisions row audit-loop-2026-10-31 on the legacy verdicts.
