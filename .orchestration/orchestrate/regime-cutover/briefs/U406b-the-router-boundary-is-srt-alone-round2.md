# U406b round 2 of U406: the router profile's boundary is srt alone; bash-sandbox is mounted as the shell provider the presets require and runs in its pass-through mode

GOAL
U406 (PR 744, head da0b4e01) keeps dsh's bash-sandbox on in the router profile and its comment, test docstring and body say the sandbox runs inside srt as a second boundary. Measured 2026-11-09 05:1xZ (decisions row 05:16:19Z): inside the router seat's srt, `sandbox-exec -p '(version 1)(allow default)' /bin/echo` fails with `sandbox_apply: Operation not permitted` (exit 71) while a plain `/bin/echo` runs; dsh-sandbox-local confines on darwin through sandbox-exec, so no second boundary can apply there. Upstream's own deployment guide (dsh-superagent docs/006-deployment.md, "Permissions and isolation") says both superagent presets run with `danger-full-access` and that isolation comes from outside the process, and bash-sandbox's `danger-full-access` mode runs the local executor without sandbox-exec. So the code change of U406 stands (bash-sandbox mounted, presets not restated) and its stated reason is wrong: bash-sandbox is mounted because it is the only shell provider whose executor carries a `sandboxMode`, which upstream's permission presets require to activate, and under the superagent's presets it runs in pass-through mode; the one boundary is srt, as the kit decided on 2026-11-06. This round corrects every sentence that claims two boundaries and adds nothing else.

SCOPE
The worker repository `/private/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/dotfiles-wt/U406` on branch `fix/router-profile-bash-sandbox-on` at da0b4e01 (the U406 head; a fix round, standing order 24). May write: `scripts/generate-agent-configs.py` (the comment block above `DSH_ROUTER_PROFILE` alone), `tests/unit/test_dsh_profile.py` (the docstring of `test_the_router_keeps_the_base_bundles_bash_sandbox_row_on` and the class docstring alone), the regenerated `home/dot_dsh/profiles/router/cordis.patch.yml` if the generator's output changes (it should not), and the PR body `/tmp/dotfiles-wt/U406-pr-body.md` (rewritten in place). Non-goals: any rendered row, any lever, the thak profile, any new test, any sandbox-policy or approval row (upstream's presets select the mode per session; a kit row here would duplicate that and is not measured).

CONTEXT
At da0b4e01: `scripts/generate-agent-configs.py` lines 178-186 carry the sentence "the router keeps the base bundle's bash-sandbox row on (U406): upstream's permission presets refuse a shell executor that does not confine (permission-presets lib/index.js:177, no sandboxMode), and srt stays the seat's outer boundary, so the sandbox runs inside it"; `tests/unit/test_dsh_profile.py` class `DshRouterProfileTest` docstring and `test_the_router_keeps_the_base_bundles_bash_sandbox_row_on` docstring say the same. The body at `/tmp/dotfiles-wt/U406-pr-body.md` has an effect row "the Router's shell commands now run under dsh's bash-sandbox inside srt" and a residual row about the first real command. Evidence files: `/tmp/u406-nest/probe.txt`; `~/.dsh/dsh/current/packages/sandbox/sandbox-local/lib/index.js` (sandbox-exec and the SBPL profile); `~/.dsh/dsh/current/packages/shell/bash-sandbox/lib/index.js` (`if (mode === "danger-full-access") return ... super.execute`); `~/.dsh/plugins/dsh-superagent/docs/006-deployment.md` "Permissions and isolation".

DATA SHAPE
Unchanged from U406: the router patch's rows are the thak-form rows, the webserver row, the superagent stateDir row and the gateway insert; no bash-sandbox row, no preset row.

CHANGE
1. The comment block: replace the two-boundary sentence with: bash-sandbox stays mounted because it is the base bundle's only shell provider whose executor carries a sandboxMode, which upstream's permission presets require to activate (permission-presets lib/index.js:177); under the superagent's presets it runs in `danger-full-access`, the mode that skips sandbox-exec (bash-sandbox lib), and sandbox-exec cannot apply inside srt on macOS in any case (sandbox_apply refused, measured 2026-11-09), so the seat's one boundary is srt, the 2026-11-06 decision unchanged. Two or three sentences.
2. The two docstrings: the same correction, shorter.
3. Regenerate (`make render-check` form); confirm `git status` names only the generator and the test module (the rendered patch unchanged).
4. Rewrite the body's effect and residual rows: effect, the Router's shell service exists and its commands run as plain subprocesses inside srt, bounded by hcom-seat's router row (its deny lists, the state root, the credential root read grant, the loopback binding); residual, no shell command has been run through a Router session yet (observe mode runs none), the first is measured by the i2 row and the M-18 ladder. Add the probe's two lines to Verification. Keep `Program-Unit: regime-cutover/U406` as the last line.

ACCEPTANCE
1. `grep -c 'second boundary\|two boundaries\|runs inside it' scripts/generate-agent-configs.py tests/unit/test_dsh_profile.py` prints 0 for each, pasted. 2. `python -m unittest tests.unit.test_dsh_profile tests.unit.test_generate_agent_configs` OK with counts, pasted. 3. `scripts/ci/run-on-lint-files.sh` (shfmt, ruff format, prettier as the Makefile lint target runs them) exit 0 and `make render-check` exit 0, pasted. 4. `git diff --stat da0b4e01 HEAD` pasted; only `scripts/generate-agent-configs.py` and `tests/unit/test_dsh_profile.py` in it. 5. `grep -c 'sandbox_apply' /tmp/dotfiles-wt/U406-pr-body.md` prints 1 or more, pasted.

VERIFY
ACCEPTANCE pasted into the body's Verification section and the report; the coordinator fetches the head by path, pushes it to the branch of PR 744, edits the body, and the one audit, the sweep and CI follow at this head.

CLOSURE
remove

TRUST
TRUST: the round trusts the 05:1xZ probe, upstream's deployment guide and the two dsh sources named in CONTEXT as the evidence; it changes no rendered row and no lever, and runs no command through a Router session.

TIMEBOX
15 minutes.

FORBIDDEN
No change to any rendered row of any profile; no new test; no sandbox-policy or approval row; no change to any lever; no push; no rebase; no `git stash`; no pipe `|` in any bash command (standing order 46: output to a file under `/tmp/u406b/`, then read it); write the first progress line within five minutes of starting.

WORKER RULES (standing orders 21, 24, 27, 29, 31, 34, 44, 46, 49; read `~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` lines 23 to 56)
- Never run git or edit files in `~/Workspace/dotfiles`, never push, never open or edit a PR, never edit the live store; you stop at a committed head in `/private/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/dotfiles-wt/U406`. The repository is yours alone; your final line is the Task return.
- Progress line at `/tmp/dotfiles-wt/U406b-progress.txt` at every step; final report to `/tmp/dotfiles-wt/U406b-report.txt`.
- Commit unsigned: `git -c commit.gpgsign=false commit`. The commit message ends with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.

REPORT
Status, head sha (40 hex), the ACCEPTANCE lines, deviations. Under 10 lines, ending with `head=<40 hex>`.

STANDING
`preferences.md` (standing orders 21, 24, 27, 29, 34, 44, 46, 49); the U406 brief; the decisions rows 2026-11-06T16:45:37Z, 2026-11-06T23:14:30Z, 2026-11-09T03:52:16Z and 05:16:19Z.
