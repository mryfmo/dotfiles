# U140 the documents say who relaunches a dead worker: only the orchestrator is supervised

GOAL
Three texts say the orchestrator seat starts the worker seats and relaunches one that died: the `regime-start` description ("that seat starts the others", `scripts/orchestrator/regime-start:5-6`), the seat document ("it relaunches the other seats itself", `docs/orchestrator-seat.md:95`) and the top-level README ("It starts the worker seats itself, relaunches a seat that died", `README.md:770`). The code says otherwise: `regime-start --supervise` relaunches only a dead orchestrator (`regime-start:19-26`), `hcom-seat` refuses to run inside any seat (`home/dot_local/bin/common/executable_hcom-seat:210-215`), and the skill's step 0 says the seat never launches a seat and a missing worker is the operator's or the coordinator's step from a terminal outside every seat (`home/dot_agents/skills/hcom-orchestration/SKILL.md:25`). The decisions row `worker relaunch:` of the store (2026-11-03, phase `truth`) decides: the documents follow the code. After this unit the three texts say only the orchestrator is supervised and a dead worker is relaunched by an operator or coordinator command, the `regime-start` copy and its pin follow the edited comment, and the lever's behaviour is unchanged.

SCOPE
One branch `docs/worker-relaunch-follows-code` from `origin/main` (rebased by the coordinator onto main after U138 lands, since U138 edits the audit clause of the same README paragraph). May write: `scripts/orchestrator/regime-start` (the description comment at lines 5 to 6 only) and its copy `home/dot_local/bin/common/executable_regime-start` with its `claude.levers.sha256` pin line in `home/dot_agents/agent-config.yaml` (through the generator write run only), `docs/orchestrator-seat.md` (the supervision sentence at line 95 only), `README.md` (the orchestrator paragraph at lines 769 to 773 only; the audit clause of that paragraph is U138's and stays as U138 left it). No other file; no lever behaviour change.

CONTEXT
The sentence to write: the operator starts the orchestrator seat; worker seats are started and relaunched by an operator or coordinator command from a terminal outside every seat (the skill's step 0); only the orchestrator is supervised. `regime-start` is a lever: the generator write run (`uv run --with pyyaml scripts/generate-agent-configs.py`) refreshes its copy under `home/dot_local/bin/common` and its pin; `make render-check` proves both; `tests/unit/test_lever_self_check.py` and `tests/unit/test_regime_start.py` prove the lever still refuses foreign bytes and still supervises the orchestrator alone.

CHANGE
1. Rewrite the `regime-start` description comment as CONTEXT says; run the generator write run; `make render-check` exit 0; `cmp` the source and the copy.
2. Rewrite the seat document's supervision sentence.
3. Rewrite the README's orchestrator paragraph, keeping U138's audit clause.
4. Run `uv run --no-project --with pyyaml python -m unittest tests.unit.test_lever_self_check tests.unit.test_regime_start`.

ACCEPTANCE
1. `grep -c 'only the orchestrator is supervised' scripts/orchestrator/regime-start` prints 1 and `grep -c 'that seat starts the others' scripts/orchestrator/regime-start` prints 0. 2. `grep -c 'relaunched by an operator or coordinator command' docs/orchestrator-seat.md` prints 1 and `grep -c 'relaunches the other seats itself' docs/orchestrator-seat.md` prints 0. 3. `grep -c 'relaunches a seat that died' README.md` prints 0 and `grep -c 'relaunched by an operator or coordinator command' README.md` prints 1 or more. 4. `make render-check` exit 0 and `cmp scripts/orchestrator/regime-start home/dot_local/bin/common/executable_regime-start` exit 0. 5. The two test modules OK (paste the Ran lines). 6. The PR body's Contract states what is left out: no supervisor extension, no lever behaviour change (a comment and its pin only).

VERIFY
The commands of ACCEPTANCE in the worker's tree with their result lines pasted into the PR body's Verification section; `scripts/ci/run-on-lint-files.sh shell shellcheck` is CI's; `prettier --check` on the two changed Markdown files; `uv run --no-project --with pyyaml scripts/lint-comparisons.py --changed`.

CLOSURE
remove: the three sentences that give the orchestrator a relaunch it does not have are removed; one sentence names who relaunches.

TRUST
TRUST: the unit trusts the decisions row `worker relaunch:` of the store and the lever's existing supervisor loop; it does not read or change the lever's behaviour, the seat launcher or the skill.

TIMEBOX
20 minutes.

FORBIDDEN
No lever behaviour change; no edit to the skill or the seat launcher; no edit outside SCOPE; no `gh` call; no mention of any private design directory in files, commits or the PR body.

WORKER RULES (standing orders 27, 29, 31, 34; read `preferences.md` lines 23 to 45 in the store)
- Never run git or edit files in `~/Workspace/dotfiles` (the coordinator's checkout; no `git worktree add`, no commit there), never push, never open or edit a PR, never edit the live store; you stop at a committed head in your tree and the coordinator fetches it by path and pushes. Your tree is the one the coordinator names in your task, a repository of its own under `$TMPDIR/dotfiles-wt/`; every command runs with it as cwd; if you believe it is absent, stop and report, never make another. Never `git stash`. No `/tmp` literal in tracked files.
- Run every test in the foreground with a timeout and paste its result line; progress line beside your tree (`../U140-progress.txt`) every ten minutes at most; `grep -n` then bounded reads; first edit within fifteen minutes.
- Commit unsigned: `git -c commit.gpgsign=false commit`. Every commit message ends with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.
- Before you report: the modules named in ACCEPTANCE; `scripts/ci/run-on-lint-files.sh python ruff format --config ruff.toml --check`; `uv run --no-project --with pyyaml scripts/lint-comparisons.py --changed`.
- Write the PR body beside your tree (`../U140-pr-body.md`) with `## Summary`, `## Contract` (with a `Trusted:` sentence), `## Threat table` (`row | risk | status | evidence`, one row per changed path; the lever comment and the pin refresh are rows), `## Verification` (the result lines), the line `Program-Unit: regime-cutover/U140`, a blank line, then `🤖 Generated with [Claude Code](https://claude.com/claude-code)`.

REPORT
Status, head sha (40 hex), files changed, the result lines, deviations. Under 10 lines, ending with `head=<40 hex>`.

STANDING
`~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md`; the store's decisions row `worker relaunch:` (2026-11-03); `scripts/orchestrator/regime-start:19-26`; `home/dot_agents/skills/hcom-orchestration/SKILL.md:25`.
