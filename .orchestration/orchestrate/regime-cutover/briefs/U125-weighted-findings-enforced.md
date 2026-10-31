# U125 The audit lever enforces the weighted finding rule

GOAL
U124 wrote the rule as text. A rule holds when the tool refuses what the sentence forbids (U123). This unit makes `pr-audit.sh` require a frequency and a severity score on every finding, apply the decision rule from the scores, write them into the verdict line, and makes the merge gate and the carry lever read the scored line form; a finding under the threshold is `filed` and needs no disposition for a merge.

SCOPE
One branch `feat/weighted-findings-enforced` from `origin/main`, after U122 lands (both touch `pr-audit.sh`, `pr-merge.sh`, `audit-carry.py`). May write: `scripts/orchestrator/pr-audit.sh` (the schema, the prompt's finding sentence, the reader), `scripts/orchestrator/pr-merge.sh` (the finding line grammar and the filed skip), `scripts/orchestrator/audit-carry.py` (FINDINGS_GRAMMAR), `scripts/orchestrator/rounds-check.py` only if it reads finding lines, a new `scripts/orchestrator/filed-findings.py`, `home/dot_agents/skills/hcom-orchestration/SKILL.md` step 4 sentence, `scripts/orchestrator/README.md` rows, the tests of each lever, generated copies through the generator.

CHANGE
1. Data shape first. A finding is `(priority, confidence, frequency, severity, path, line, rationale)`; `weight = frequency * severity`; `WEIGHT_THRESHOLD = 10`, named once in the reader and once in `pr-merge.sh`, with a test that both equal the number in the AGENTS.md verdict bullet (U124's test extended). The verdict schema gains `frequency` and `severity` as required integers 1 to 10 (`additionalProperties: false` keeps the shape closed); the prompt's finding sentence defines both scores as AGENTS.md does. The reader's rule: blocking = priority in (P0, P1) and weight >= 10; filed = weight < 10 (any priority); a `verdict` that contradicts the derived one is refused as today. The line form becomes `- P<n> (<confidence>) [f<n> s<n>] <path>:<line>: <rationale>`; after `Blocking: <n>` the reader writes `Filed: <n>`; `Verdict:` stays last.
2. `pr-merge.sh`: the finding regex reads the `[f<n> s<n>]` token (a line without it is refused naming the line, since the reader of this head always writes it); a P0 or P1 line with weight >= 10 under a `correct` row is refused as today; a line with weight < 10 is filed and needs no `dispositions.tsv` row; a P2 or P3 with weight >= 10 needs its row as today. `audit-carry.py` FINDINGS_GRAMMAR reads the same token and carries the scores as data in the rendered block.
3. `scripts/orchestrator/filed-findings.py <store>`: lists every filed finding of every verdict file (unit, head, priority, f, s, path:line, rationale) as a table, the issue list the operator reads; `rounds-check.py --all` style status reading, exit 2 on a malformed verdict file.
4. Residuals of U122 round 6 carried here: (a) `audit-carry.py` imports `ledger.py` through a read that exits 2 naming the file on any `OSError` (an unreadable module is a failed read, never no earlier audited head; test with a mode-000 copy); (b) `ledger.py carry-source` prints the source row's unit beside its head and verdict, and `pr-merge.sh` names the verdict file and the disposition rows by that unit, so a carry whose source is a fix-unit head (`U71b` under a `U71` body) merges on the fix unit's correct row (test red on main: refused today).
5. Filed findings of U124 round 3 (weights 4 and 1): the thread levers accept a `filed:` reason that begins with whitespace (the reason is the text after `s=<n>` with surrounding whitespace trimmed, one non-whitespace character required), and a reply whose first line is blank is judged by its first non-blank line, with the login and association named in the `open` diagnostic.
6. SKILL step 4 names the scores and `Filed:`; README rows. Tests: red proofs on origin/main for the schema (a finding without scores is refused by the reader), the rule (P1 with f=1 s=9 is `correct` with `Filed: 1`; P1 with f=2 s=5 is `incorrect`), the merge gate (a filed P1 line under a correct row merges; a P1 with weight 10 refuses), the carry grammar.

ACCEPTANCE
1. `uv run --no-project --with pyyaml python -m unittest tests.unit.test_pr_audit tests.unit.test_pr_levers tests.unit.test_audit_carry tests.unit.test_review_rules tests.unit.test_scratch_git` OK. 2. The lints of the WORKER RULES. 3. The PR body's Contract states the rule as applied from the data, the number and its one source, and what is left out: the scores are the auditor's judgment, read by value but not second-guessed; a `blocked` verdict carries no scores.

CLOSURE
parser-module: the verdict schema and the reader of `pr-audit.sh` are the one parser of a finding; `pr-merge.sh` and `audit-carry.py` read the line form that reader writes, with one regex each asserted equal to the writer by a test.

TRUST
TRUST: the unit trusts the auditor's two scores as data the schema bounds; it does not re-derive them from the code, and it trusts the U119 reader as the one place the decision rule lives.

TIMEBOX
90 minutes.

FORBIDDEN
No change to the prompt's isolation or the permission profile; no `codex` or `gh` write; no start before U122 is merged.
WORKER RULES (standing orders 27, 29, 31, 34; read `preferences.md` lines 23 to 45 in the store)
- Never push, never open or edit a PR, never run pr-body-edit.sh, never edit the live store; the coordinator fetches your head by path and pushes. Your tree is made by the coordinator with `~/.local/bin/common/worker-worktree.sh U125 <branch> origin/main` (a repository of its own under the default root; it cannot push). Never write under `~/Workspace`, under `$HOME` config directories, or on any other host. Never `git stash`. No local Bats as evidence.
- Run every test command in the foreground with a timeout and paste its result line; write a progress line beside your tree (`../U125-progress.txt`) at least every ten minutes of wall time; read only the line ranges you need (`grep -n`, then a bounded read) and make your first edit within fifteen minutes.
- Commit unsigned: `git -c commit.gpgsign=false commit`. Every commit message ends with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.
- Before you report, run on the committed head: the test modules your change touches plus `uv run --no-project --with pyyaml python -m unittest tests.unit.test_scratch_git`; ShellCheck 0.11.0, `shfmt -i 4 -sr -d`, and `scripts/ci/masked-dirname-check.sh` on every touched shell file; `scripts/ci/producer-status-check.sh` over the adopted levers (exit 0); `scripts/ci/run-on-lint-files.sh python ruff format --config ruff.toml --check`; `uv run --no-project --with pyyaml scripts/lint-comparisons.py --changed`; `uv run --no-project --with pyyaml scripts/generate-agent-configs.py --check` (regenerate and commit if stale; never hand-edit a generated file). CI runs the full suite.
- Shell comments are English shdoc. Tests assert behaviour the user observes. Comments explain a non-obvious why only. No `/tmp` literal in any tracked file.
- A producer's status is read (standing order 21): a `$(...)` whose status is unchecked is a defect, a failed read is never treated as an absence, and every such decision has a failure-injection test.
- Write the PR body beside your tree (`../U125-pr-body.md`) with `## Summary` (under 12 lines), `## Contract` (what this change guarantees, what it leaves out, a `Trusted:` sentence), `## Threat table` (`row | risk | status | evidence`), `## Verification` (commands and pasted result lines), the line `Program-Unit: regime-cutover/U125`, a blank line, then `🤖 Generated with [Claude Code](https://claude.com/claude-code)`. No absolute home path, no credential-shaped literal.
- Conventions: `~/.agents/pstack/skills/poteto-mode/SKILL.md` (Comments, Writing the reply), `~/.agents/pstack/skills/technical-writing/SKILL.md` for the PR body and the rule sentences.

REPORT
Status, branch, head sha (40 hex), files changed (`git diff --stat origin/main`), the commands with result lines, the red proof, deviations, anything not verified. Facts only. Under 30 lines.

STANDING
`~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` (orders 35 to 39); the decisions row of phase `operator-2026-10-30` on the weighted finding rule.
