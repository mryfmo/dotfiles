# U355: the omp-gateway plugin's environment boundary carries `CLAUDE_CONFIG_DIR`, so the dsh role's gateway child finds the seat login inside the sandbox

GOAL
Table row g6 of `tests/dsh-login-route.tsv` (the dsh role's real turn, `hcom-seat dsh --profile thak -- 'Reply with the single word pong.'`) is NG on the laptop at main 6ad1be23 after `make deploy-kit` (measured 2026-11-07T08:38:24Z to 08:39:24Z, /tmp/g6-run.txt): the profile config is placed (U310 holds), the gateway child starts (`~/.omp/profiles/dsh/logs/omp.2026-11-07.1503.log`: two `auth-gateway request` lines at 08:38:25, `claude-bridge/claude-opus-5-5`, peer stdio), and no answer follows; at 60 s DSH aborts the turn and the plugin reports `omp-gateway: request aborted; the gateway child was killed`. The same route outside the sandbox answers in 6 s (`OMP_PROFILE=dsh node ~/.dsh/plugins/omp-gateway/proof/run-proof.mjs --command omp --args '["auth-gateway","stdio"]' --case loop3`, 08:45:37Z to 08:45:43Z, a full turn with two tool calls). The difference is the login directory. hcom-seat hands dsh `CLAUDE_CONFIG_DIR=<seats-root>/.state/claude` (hcom-seat:2810, the shared seat login of U318) and denies the operator's `~/.claude` to the role, but the plugin's environment boundary for the gateway child, `DEFAULT_ENV_NAMES` in `home/dot_dsh/plugins/omp-gateway/config.mjs:10-13` (HOME, PATH, USER, LOGNAME, SHELL, LANG, LC_ALL, TERM, TMPDIR, the four XDG names, OMP_PROFILE), does not name `CLAUDE_CONFIG_DIR`, and its own comment says a name absent there never reaches `omp auth-gateway stdio`. So inside the sandbox the bridge's Claude child looks for a login under the denied `~/.claude` and never answers; outside the sandbox `~/.claude` is readable and holds the operator's login, which is why the proof passes. U318 moved the login and missed this boundary. The fix is one name in the list and the test that pins it.

SCOPE
A new branch `fix/omp-gateway-env-carries-claude-config-dir` from main 6ad1be23; the tree is `/tmp/dotfiles-wt/U355`. May write: `home/dot_dsh/plugins/omp-gateway/config.mjs` (the name and the comment sentence naming U318 and this row), the plugin's tests under `home/dot_dsh/plugins/omp-gateway/test/` (the boundary test: a child spawned by the client receives `CLAUDE_CONFIG_DIR` when the launcher exported it and nothing else new; a `config.env` row that omits it still wins, as today), `scripts/generate-agent-configs.py` and the rendered `home/dot_dsh/profiles/thak/cordis.yml` only if the thak row renders an explicit `env:` list that must gain the name (grep first; today neither names it), the manifest pin of the plugin if one exists (through the generator), and the body. Not: hcom-seat; the bridge extension; the srt settings.

CONTEXT
The plugin's child environment is built in `index.mjs:60-76` from `config.env` (default `DEFAULT_ENV_NAMES`) by copying only those names from `process.env`; the stub gateway and `gateway-client.test.mjs` show how a child is spawned under test and how its environment is observed (`stub-gateway.mjs`). The seats login directory on this host is `~/.local/state/omp-seats/dotfiles/.state/claude` (seat-login-preflight --check: `dsh claude-bridge: login present`). The plugin is deployed to `~/.dsh/plugins/omp-gateway` by `make deploy-kit`; the g6 command is the proof after deploy and is the coordinator's.

DATA SHAPE
One more name in one frozen list, `CLAUDE_CONFIG_DIR`, and one test that fails without it.

CHANGE
1. The boundary test first, red at 6ad1be23: with `CLAUDE_CONFIG_DIR=/scratch/login` in the plugin's process environment and the default config, the spawned child's environment holds it; with `config.env` set to a list without it, the child's does not. 2. The one name and the comment. 3. `node --test home/dot_dsh/plugins/omp-gateway/test/` OK (the plugin's own runner; read `package.json` for the exact form), and `uv run --with pyyaml python -m unittest tests.unit.test_dsh_profile tests.unit.test_generate_agent_configs -v` OK. 4. `make render-check`; prettier in the CI form over the changed files; `scripts/lint-comparisons.py --changed`. 5. Commit `fix(omp-gateway): the gateway child's environment boundary carries CLAUDE_CONFIG_DIR, the seat login U318 moved (regime-cutover U355)` with the trailer. 6. The body: Summary (the g6 measurement, the proof outside the sandbox, the boundary), Contract, Threat table (the plugin file row citing the test; the login directory's secrecy unchanged: the name carries a path, not a token), Verification; `Program-Unit: regime-cutover/U355` once.

ACCEPTANCE
1. The boundary test named with its red line at 6ad1be23 and its green line at the head. 2. `grep -c CLAUDE_CONFIG_DIR home/dot_dsh/plugins/omp-gateway/config.mjs` is 1 or more. 3. The plugin tests and the two Python modules OK with counts. 4. render-check 0; prettier 0; lint-comparisons 0. 5. `git diff --stat 6ad1be23 HEAD` pasted.

VERIFY
ACCEPTANCE pasted into the body's Verification section and the report; the coordinator runs the g6 row after the merge and `make deploy-kit`, which is the real-surface proof (expected `pong`).

CLOSURE
remove

TRUST
TRUST: the unit trusts the seat login design of U318 (one login directory per seats root, named by CLAUDE_CONFIG_DIR) and the plugin's documented boundary; it widens the boundary by one name and no value.

TIMEBOX
30 minutes.

FORBIDDEN
No other name added to the boundary; no change to hcom-seat or the bridge; no network; no push; no `gh` call; no pipe `|` in any bash command (standing order 46: output to a file under `/tmp/u355/`, then read it).

WORKER RULES (standing orders 21, 27, 29, 31, 34, 44, 46, 49; read `~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` lines 23 to 56)
- Never run git or edit files in `~/Workspace/dotfiles`, never push, never open or edit a PR, never edit the live store; you stop at a committed head in `/tmp/dotfiles-wt/U355`. The worktree is yours alone; your final line is the Task return.
- Progress line at `../U355-progress.txt`; final report to `../U355-report.txt`; body at `../U355-pr-body.md`.
- Commit unsigned: `git -c commit.gpgsign=false commit`. The commit message ends with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.

REPORT
Status, head sha (40 hex), the test's name with its red and green lines, the ACCEPTANCE lines. Under 8 lines, ending with `head=<40 hex>`.

STANDING
`preferences.md` (standing orders 21, 24, 27, 29, 34, 44, 46, 49); the U318 brief; `tests/dsh-login-route.tsv` row g6; `home/dot_dsh/plugins/omp-gateway/config.mjs:1-24`.
