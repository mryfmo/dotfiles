# U364: the omp-gateway plugin's environment boundary carries every variable srt injects into its child (the proxy, its CA trust names, the runtime mark), so the bridge's Claude child reaches the network through srt's proxy

GOAL
Table row g6 is still NG after U355 deployed (/tmp/g6-run2.txt, 10:55:56Z to 10:56:56Z: the gateway child logs two `auth-gateway request` lines and answers nothing; DSH aborts at 60 s). The macOS unified log names what the sandbox denied the bridge's Claude child (`claude(68905)`, 19:55:56 JST): `network-outbound /private/var/run/mDNSResponder` and `mach-lookup com.apple.SystemConfiguration.DNSConfiguration`, that is, direct DNS resolution, which a process under srt cannot do; srt's sandbox reaches the network through the proxy it starts, and it tells its child so by injecting `HTTP_PROXY`, `HTTPS_PROXY`, `http_proxy`, `https_proxy`, `NO_PROXY`, `no_proxy`, `SANDBOX_RUNTIME=1`, the CA trust names when TLS termination is on (`CA_TRUST_VARS`), `GIT_CONFIG_PARAMETERS` when the proxy has auth, and `TMPDIR` (@anthropic-ai/sandbox-runtime 0.0.81, `dist/sandbox/sandbox-utils.js:680-760`, `generateProxyEnvVars`). The omp seats inherit them because omp runs directly under srt; the dsh role's gateway child does not, because the omp-gateway plugin's `DEFAULT_ENV_NAMES` (`home/dot_dsh/plugins/omp-gateway/config.mjs`) names HOME, PATH, USER, LOGNAME, SHELL, LANG, LC_ALL, TERM, TMPDIR, the XDG names, OMP_PROFILE and (U355) CLAUDE_CONFIG_DIR, and nothing srt injects for the network. The same class U322b fixed in `build_under_srt`. The fix: the boundary carries exactly the names srt injects, read from srt's source at the pin and listed once with that citation, and a test pins them.

SCOPE
A new branch `fix/omp-gateway-env-carries-srt-proxy-names` from main dba01803; the tree is `/tmp/dotfiles-wt/U364`. May write: `home/dot_dsh/plugins/omp-gateway/config.mjs` (the names and the comment citing srt's file and lines), the plugin's tests under `home/dot_dsh/plugins/omp-gateway/test/` (the boundary test of U355 extended: a child spawned under the default config receives every listed name when the launcher's environment holds it, and a `config.env` row without them still wins), `scripts/generate-agent-configs.py` and the rendered `home/dot_dsh/profiles/thak/cordis.patch.yml` only if the thak row renders an explicit `env:` list (U355 found none), the manifest pin through the generator if one exists, and the body. Not: hcom-seat; the bridge extension; the srt settings.

CONTEXT
srt's injected list: `sandbox-utils.js:680` (`SANDBOX_RUNTIME=1`), `:687-692` (`TMPDIR`), `:696-700` (`CA_TRUST_VARS`: read the constant's definition in the same file and list each name), `:720-727` (the six proxy names), `:732` (`GIT_CONFIG_PARAMETERS`), and the lines after `:743` for anything else the function pushes (read to the function's end). The plugin's child environment is built in `index.mjs:60-76` from `config.env`; `stub-gateway.mjs` and `gateway-client.test.mjs` show how a spawned child's environment is observed (U355's test is the model). The other denials of the same run are recorded in decisions.tsv 2026-11-07T11:05:49Z (`<seats-root>/.state/claude.lock`, `/private/tmp/cc-socks/<pid>.sock`, `/private/tmp/claude-501/fswatch-probe-*`, FSEvents, analyticsd); they are not this unit's: the g6 rerun after this deploy says whether any of them stops a request.

DATA SHAPE
The frozen name list gains srt's injected names, each cited; one test fails without them.

CHANGE
1. The test first, red at dba01803. 2. The names and the comment. 3. The plugin's tests (`node --test`, the form `package.json` gives) OK; `uv run --with pyyaml python -m unittest tests.unit.test_dsh_profile tests.unit.test_generate_agent_configs -v` OK. 4. `make render-check`; prettier in the CI form; `scripts/lint-comparisons.py --changed`. 5. Commit `fix(omp-gateway): the gateway child's environment carries every variable srt injects, so the bridge child uses srt's proxy instead of direct DNS (regime-cutover U364)` with the trailer. 6. The body: Summary (the denial lines, the srt citation), Contract, Threat table (the plugin file row citing the test; the names carry a loopback proxy URL with a per-process auth token srt minted for this child, no operator secret), Verification; `Program-Unit: regime-cutover/U364` once.

ACCEPTANCE
1. The test named with its red line at dba01803 and its green line at the head. 2. `grep -c HTTPS_PROXY home/dot_dsh/plugins/omp-gateway/config.mjs` is 1 or more; every name of srt's list present (pasted). 3. The plugin tests and the two Python modules OK with counts. 4. render-check 0; prettier 0; lint-comparisons 0. 5. `git diff --stat dba01803 HEAD` pasted.

VERIFY
ACCEPTANCE pasted into the body's Verification section and the report; the coordinator runs the g6 row after the merge and `make deploy-kit` (expected `pong`), and reads the unified log for the next denial if it still aborts.

CLOSURE
remove

TRUST
TRUST: the unit trusts srt's source at the pin as the list of what its child needs (cited line by line) and the plugin's documented boundary; it widens the boundary by names srt itself sets and by no value of the launcher's.

TIMEBOX
30 minutes.

FORBIDDEN
No name outside srt's injected list and the existing ones; no change to hcom-seat or the bridge; no network; no push; no `gh` call; no pipe `|` in any bash command (standing order 46: output to a file under `/tmp/u364/`, then read it).

WORKER RULES (standing orders 21, 27, 29, 31, 34, 44, 46, 49; read `~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` lines 23 to 56)
- Never run git or edit files in `~/Workspace/dotfiles`, never push, never open or edit a PR, never edit the live store; you stop at a committed head in `/tmp/dotfiles-wt/U364`. The worktree is yours alone; your final line is the Task return.
- Progress line at `../U364-progress.txt`; final report to `../U364-report.txt`; body at `../U364-pr-body.md`.
- Commit unsigned: `git -c commit.gpgsign=false commit`. The commit message ends with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.

REPORT
Status, head sha (40 hex), the names added with srt's lines, the test's red and green lines, the ACCEPTANCE lines. Under 10 lines, ending with `head=<40 hex>`.

STANDING
`preferences.md` (standing orders 21, 24, 27, 29, 34, 44, 46, 49); the U355 and U322b briefs; `decisions.tsv` 2026-11-07T11:05:49Z; `~/.local/share/mise/installs/npm-anthropic-ai-sandbox-runtime/0.0.81/lib/node_modules/@anthropic-ai/sandbox-runtime/dist/sandbox/sandbox-utils.js` (read only).
