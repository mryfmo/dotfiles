# U130 brief-check refuses a brief that rewrites more than two levers at once

GOAL
P-41 measured (decisions row plan-P-41, 2026-10-31T08:46:11Z): the four units of the loop rebuild whose one brief rewrote several levers (U119, U120, U122, U123) took 6.5 audits and 7.8 hours each (medians), the eight single-surface units of the same period 2 audits and 0.95 hours; U125, split into four sequenced rounds after its whole-task owner stalled, landed in one audit. The cost is the brief's shape, and the judge of a brief is `scripts/orchestrator/brief-check.py` (U121), which every program PR runs through before its audit. This unit makes it refuse a brief whose SCOPE names more than two lever sources, with the instruction to split the work into sequenced units, one or two levers each.

SCOPE
One branch `feat/brief-check-splits-multi-lever-briefs` from `origin/main`. May write: `scripts/orchestrator/brief-check.py`, `tests/unit/test_brief_check.py` (or the module that tests it; `ls tests/unit | grep brief`), `scripts/orchestrator/README.md` (the brief-check row), `home/dot_agents/skills/hcom-orchestration/SKILL.md` step 1 (one sentence), and the one brief of this unit if the check would refuse it.

CHANGE
1. The lever set is the closed list the repository already holds: the files `scripts/generate-agent-configs.py` installs under `home/dot_local/bin/common/` from `scripts/orchestrator/` (read how the manifest names them: `grep -n 'levers' home/dot_agents/agent-config.yaml`); brief-check reads that list from the manifest beside the checkout (status read, a manifest that cannot be read refuses the check, standing order 21), never a second spelling of the list.
2. A brief's SCOPE section is scanned for backticked paths; the distinct lever sources among them are counted (the installed copy `home/dot_local/bin/common/executable_<name>` counts as its source, not twice). More than two is exit 1 with the line `SCOPE names <n> levers (<names>); split into sequenced units of at most two levers each (plan P-41: multi-lever briefs took 6.5 audits, single-surface ones 2)`. Tests, README and generated copies named in SCOPE never count.
3. Every existing brief under `.orchestration/orchestrate/regime-cutover/briefs/` is run through the new check and the exit codes are listed in the PR body (merged units are not re-audited, so a refusal there is a record, not a blocker; say so in the Contract).
4. SKILL step 1 gains one sentence: a brief naming more than two levers is split before it is sent.

ACCEPTANCE
1. `uv run --no-project --with pyyaml python -m unittest tests.unit.test_brief_check tests.unit.test_hcom_seat_skills tests.unit.test_scratch_git` OK, with tests: three lever sources refused naming them; two accepted; a source and its installed copy count once; tests and README paths never count; an unreadable manifest refuses. 2. ruff format check; `scripts/lint-comparisons.py --changed` exit 0; the generator check up to date. 3. The PR body's Contract states the rule, its source list and its number, and what is left out: a unit may still touch many files that are not levers.

CLOSURE
allowlist: the lever set is the manifest's closed list read in one place; the count and the threshold are the only rule, no judgement of a brief's prose.

TRUST
TRUST: the unit trusts the manifest `home/dot_agents/agent-config.yaml` as the one list of levers and the SCOPE section's backticked paths as the brief's declaration of what it writes; it does not read the diff of a PR to second-guess a brief, and it trusts the coordinator to split a refused brief rather than rename paths.

TIMEBOX
45 minutes.

FORBIDDEN
No change to the trigger-term table or the CLOSURE and TRUST rules of brief-check; no exemption flag; no `codex` or `gh` write.

WORKER RULES (standing orders 27, 29, 31, 34; read `preferences.md` lines 23 to 45 in the store)
- Never run git or edit files in `~/Workspace/dotfiles` (the coordinator's checkout; no `git worktree add`, no commit there), never push, never open or edit a PR, never edit the live store; you stop at a committed head in your tree and the coordinator fetches it by path and pushes. Your tree is the one the coordinator names in your task, a repository of its own under `$TMPDIR/dotfiles-wt/`; every command runs with it as cwd; if you believe it is absent, stop and report, never make another. Never `git stash`. No `/tmp` literal in tracked files.
- Run every test in the foreground with a timeout and paste its result line; progress line beside your tree (`../U130-progress.txt`) every ten minutes at most; `grep -n` then bounded reads; first edit within fifteen minutes.
- Commit unsigned: `git -c commit.gpgsign=false commit`. Every commit message ends with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.
- Before you report: the modules named in ACCEPTANCE; `scripts/ci/run-on-lint-files.sh python ruff format --config ruff.toml --check`; `uv run --no-project --with pyyaml scripts/lint-comparisons.py --changed`; `uv run --no-project --with pyyaml scripts/generate-agent-configs.py --check`.
- Write the PR body beside your tree (`../U130-pr-body.md`) with `## Summary`, `## Contract` (with a `Trusted:` sentence), `## Threat table` (`row | risk | status | evidence`, one row per changed path), `## Verification` (the result lines and the exit-code list over the existing briefs), the line `Program-Unit: regime-cutover/U130`, a blank line, then `🤖 Generated with [Claude Code](https://claude.com/claude-code)`.

REPORT
Status, head sha (40 hex), files changed, the result lines, the red proof (a three-lever brief passes on origin/main), deviations. Under 15 lines, ending with `head=<40 hex>`.

STANDING
`~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md`; decisions rows plan-P-41 (06:49:11Z and 2026-10-31T08:46:11Z); U121 (brief-check) and U125 (the split that worked).
