# U139 the orchestration skill and the orchestrator README name the terminal that runs the audit lever

GOAL
Step 4 of the orchestration skill tells the orchestrator seat to run every audit as one fresh `~/.local/bin/common/pr-audit.sh <n> --records .orchestration/orchestrate/<program>` "run from your checkout for that head" (`home/dot_agents/skills/hcom-orchestration/SKILL.md:29`). The seat cannot: every seat's srt settings deny reading `~/.codex` (`home/dot_local/bin/common/executable_hcom-seat:1691-1693`), and the lever refuses unless `${CODEX_HOME:-~/.codex}/auth.json` is a readable regular file (`executable_pr-audit.sh:842-843`). The orchestrator README states the consequence once, in its Limits paragraph: the codex audit "runs from the coordinator outside the seat" (`scripts/orchestrator/README.md:173`). The decisions row `pr-audit.sh terminal:` of the store (2026-11-03, phase `truth`) decides the terminal: the operator's terminal outside every seat, the coordinator asking for the run and reading the ledger row; the alternative (an `excludedCommands` entry for the lever) is not taken. After this unit the skill's step 4 and the README's two sentences say the same thing, the test that quotes the step-4 sentence quotes the new one, and no sentence tells a seat to run the lever from its checkout.

SCOPE
One branch `docs/audit-lever-terminal` from `origin/main`. May write: `home/dot_agents/skills/hcom-orchestration/SKILL.md` (the step-4 sentence only), `tests/unit/test_hcom_seat_skills.py` (the quoted constant around lines 57 to 60 only), `scripts/orchestrator/README.md` (the Limits paragraph at line 173 and the `pr-audit.sh` section's run-from sentence around line 301 only). No manifest change: the audience entry `hcom-orchestration: [omp-orchestrator]` stays. No other file.

CONTEXT
The sentence to write in the skill: the lever runs from the operator's or the coordinator's terminal outside every seat, never from the seat's checkout; the seat reads the verdict file and the ledger row the run produces. The README's Limits paragraph keeps the phrase `runs from the coordinator outside the seat` exactly (a design check elsewhere greps it) and adds that the terminal is outside every seat; the `pr-audit.sh` section's run-from sentence says the same. `tests/unit/test_hcom_seat_skills.py:57-60` holds the step-4 sentence as a constant (`AUDIT_RUN` or its neighbour); move the quoted text with the edit and nothing else. The skill is deployed as `~/.agents/skills/hcom-orchestration/SKILL.md` to the orchestrator seat only (`home/dot_agents/agent-config.yaml:90`); `make validate-agent-assets` checks its frontmatter and `make render-check` the rendered audience.

CHANGE
1. Rewrite the one step-4 sentence in the skill as CONTEXT says; keep the rest of step 4 byte for byte.
2. Rewrite the two README sentences; keep the phrase `runs from the coordinator outside the seat` in the Limits paragraph.
3. Move the quoted constant in the test; run the module.
4. Run `make validate-agent-assets` and `make render-check`.

ACCEPTANCE
1. `grep -c 'outside every seat, never from the seat' home/dot_agents/skills/hcom-orchestration/SKILL.md` prints 1. 2. `grep -c 'outside every seat' scripts/orchestrator/README.md` prints 1 or more and `grep -c 'runs from the coordinator outside the seat' scripts/orchestrator/README.md` prints 1. 3. `uv run --no-project --with pyyaml python -m unittest tests.unit.test_hcom_seat_skills` OK (paste the Ran line). 4. `make validate-agent-assets` and `make render-check` exit 0. 5. The PR body's Contract states what is left out: the managed Claude settings are unchanged (the alternative was not taken), and the lever itself is unchanged.

VERIFY
The commands of ACCEPTANCE in the worker's tree with their result lines pasted into the PR body's Verification section; `scripts/ci/run-on-lint-files.sh python ruff format --config ruff.toml --check`; `uv run --no-project --with pyyaml scripts/lint-comparisons.py --changed`; `prettier --check` on the two changed Markdown files.

CLOSURE
remove: the sentence that sends a seat to run the lever from its checkout is removed; one sentence names the terminal instead.

TRUST
TRUST: the unit trusts the decisions row `pr-audit.sh terminal:` of the store and the seat sandbox's existing deny of `~/.codex`; it does not read or change the lever, the sandbox settings or the managed Claude settings.

TIMEBOX
25 minutes.

FORBIDDEN
No edit to the manifest, the lever, the sandbox settings or the Claude settings template; no edit outside SCOPE; no `gh` call; no mention of any private design directory in files, commits or the PR body.

WORKER RULES (standing orders 27, 29, 31, 34; read `preferences.md` lines 23 to 45 in the store)
- Never run git or edit files in `~/Workspace/dotfiles` (the coordinator's checkout; no `git worktree add`, no commit there), never push, never open or edit a PR, never edit the live store; you stop at a committed head in your tree and the coordinator fetches it by path and pushes. Your tree is the one the coordinator names in your task, a repository of its own under `$TMPDIR/dotfiles-wt/`; every command runs with it as cwd; if you believe it is absent, stop and report, never make another. Never `git stash`. No `/tmp` literal in tracked files.
- Run every test in the foreground with a timeout and paste its result line; progress line beside your tree (`../U139-progress.txt`) every ten minutes at most; `grep -n` then bounded reads; first edit within fifteen minutes.
- Commit unsigned: `git -c commit.gpgsign=false commit`. Every commit message ends with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.
- Before you report: the modules named in ACCEPTANCE; `scripts/ci/run-on-lint-files.sh python ruff format --config ruff.toml --check`; `uv run --no-project --with pyyaml scripts/lint-comparisons.py --changed`.
- Write the PR body beside your tree (`../U139-pr-body.md`) with `## Summary`, `## Contract` (with a `Trusted:` sentence), `## Threat table` (`row | risk | status | evidence`, one row per changed path), `## Verification` (the result lines), the line `Program-Unit: regime-cutover/U139`, a blank line, then `🤖 Generated with [Claude Code](https://claude.com/claude-code)`.

REPORT
Status, head sha (40 hex), files changed, the result lines, deviations. Under 10 lines, ending with `head=<40 hex>`.

STANDING
`~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md`; the store's decisions row `pr-audit.sh terminal:` (2026-11-03); `scripts/orchestrator/README.md:173`.
