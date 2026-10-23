# U1 pilot-bridge — brief

GOAL
Prove, with pasted output, whether omp 18.11.3 on this machine can run one non-interactive turn through the patched pi-claude-bridge (`claude-bridge/<model>`) from a named profile, and document the exact loading form that works (or the exact failure), so that U2 (W2d) can stage the asset without guessing.

SCOPE
May write: `$TMPDIR/u1-home/**` (scratch HOME for every omp run), `$TMPDIR/u1-work/**` (copies of the bridge package), `.orchestration/validation/025-pilot-bridge-unit-report.md` (your report), `.orchestration/orchestrate/regime-cutover/handouts/U1-operator-steps.md` (operator-only steps, if any).
May read: everything under `~/.local/lib/node_modules/@oh-my-pi/pi-coding-agent/` (omp 18.11.3 source, `src/` and `dist/`), `~/.omp/plugins/node_modules/pi-claude-bridge/` (the patched bridge copy the operator installed, with hoisted deps in `~/.omp/plugins/node_modules/`), `/tmp/claude-501/pcb-x/package` (pristine 0.9.3), `/tmp/claude-501/pcb-patched1/package` (patched copy without node_modules), the facts files named in STANDING line 16, `.orchestration/validation/025-pilot-bridge-omp-compat.patch`.
Must NOT write: the real `~/.omp/**`, `~/.claude/**`, any repo path outside the two files above. Exclusive branch: none (no code lands in this unit).

CONTEXT
- Measured so far (pilot-facts #B1..#B3b): `omp install pi-claude-bridge@0.9.3` fails on the shim export gap; the 69-line compat patch fixes the gap and `omp install <patched local dir>` succeeds (plugin store `~/.omp/plugins`, per agent dir); `omp --profile pilot-bridge models claude-bridge` and `omp --profile pilot-bridge -e /tmp/claude-501/pcb-patched1/package --no-extensions models claude-bridge` both print `No models matching "claude-bridge"`; `omp models` prints no extension load errors (`src/extensibility/extensions/loader.ts:431-457` return them to the caller; `src/commands/models.ts` does not print them). `-e <dir>` is manifest-first (`src/extensibility/extensions/directory-resolution.ts:5-9`), so the package dir did resolve `src/index.ts`; the suspected cause is dependency resolution (no `node_modules` at the /tmp path) but it is unverified.
- Upstream docs on `main`: `docs/extension-loading.md` (scan roots `<cwd>/.omp/extensions`, `~/.omp/agent/extensions`, profile `~/.omp/profiles/<name>/agent/extensions`; `-e` file or directory; manifest `omp.extensions` over `pi.extensions`; load order; failure isolation), `docs/extensions.md`, `docs/user-facing-packages.md`, `docs/plugin-manager-installer-plumbing.md`, `docs/providers.md`, `docs/models.md`. Fetch them from `https://raw.githubusercontent.com/can1357/oh-my-pi/main/docs/<name>` (WebFetch); the installed version is 18.11.3, so confirm each behaviour you rely on in the installed `src/` and cite `file:line`.
- The bridge registers its provider in `src/index.ts` around line 2590-2615 (`pi.registerProvider("claude-bridge", { baseUrl: "claude-bridge", <redacted:secret-pattern>, api: "claude-bridge", models, streamSimple })`), models from pi-ai's Anthropic catalog via `applyLongContext(MODELS, …)` (line ~2435). The child Claude Code is launched by `@anthropic-ai/claude-agent-sdk` with `tools: []`, `permissionMode: "bypassPermissions"`, `settingSources` default; the host's claude.ai login is what the SDK uses (facts §1, §2b).
- The Claude login lives with the operator's Claude Code (`~/.claude`, Keychain). Reading `~/.claude` is allowed; writing is not. A run that needs the Keychain or a login prompt is operator-only (STANDING 4).

ACCEPTANCE (each with pasted output)
1. An instrument that shows extension load results and errors is identified from docs/source and used (candidates: `omp extensions` listing, `omp doctor`, `--mode json` startup events, a log level flag, the `~/.omp/logs` files under the scratch HOME). Its citation is in the report.
2. For each loading form, the load result and any error text are recorded: (a) plugin store install into the scratch HOME's default profile (`omp install <dir>`), (b) `omp --profile pilot-bridge install <dir>`, (c) `-e <package dir with node_modules>`, (d) `-e <package dir>/src/index.ts`, (e) `~/.omp/agent/extensions/<copy>` under the scratch HOME. Use the patched copy; stage `node_modules` by copying the hoisted deps from `~/.omp/plugins/node_modules/` into your scratch package dir when a form needs them (no network needed), or run Bun install only with `registry.npmjs.org` named in `allowed_domains`.
3. Root cause of the earlier `No models matching` is stated with evidence (load error text, or the models filter), not inferred.
4. One of: (i) a successful non-interactive turn `omp --profile pilot-bridge --model claude-bridge/<id> -p "Reply with the single word PONG."` under the scratch HOME with `CLAUDE_CONFIG_DIR=~/.claude` so the child finds the host login, output pasted; or (ii) the exact point where it needs the operator (Keychain prompt, login) with the exact operator command written to the handout file with `source` and `dry-run` columns (STANDING 5).
5. If (i) succeeds: also one bridged tool call (`--approval-mode write --mode json -p "Use the bash tool to run exactly: echo bridged-tool-ok"`), the child's env check through the tool (`env | grep -c PI_CODING_AGENT_DIR`), and the process tree (`pgrep -fl claude`) during the turn, each pasted.
6. The report names the loading form U2 should ship (which directory, which manifest key, whether `node_modules` must be staged, which omp flag or config line the seat launcher uses), with `file:line` for each claim.

VERIFY
Everything runs with `HOME=$TMPDIR/u1-home` exported, `perl -e 'alarm 120; exec @ARGV'` around every omp call, and `2>&1 | tee` into `$TMPDIR/u1-home/run-<n>.log`. Network: `api.anthropic.com` and `claude.ai` only for step 4(i) (name them in `allowed_domains`), `registry.npmjs.org` only if you must Bun-install, `raw.githubusercontent.com` for the docs. omp's catalog probes to other hosts will be denied by the sandbox; that is expected noise, not a finding.

TIMEBOX
60 minutes. On expiry, write the report with what is proven and stop.

FORBIDDEN
No edits to the repo outside SCOPE. No `omp install` into the real `~/.omp`. No login attempts. No changes to the patch (report needed changes as follow-ups). No second theory without a pasted observation that refutes the first (M-20261023-01).

REPORT
Write `.orchestration/validation/025-pilot-bridge-unit-report.md`: status, the instrument, a table of loading forms with results, root cause, the turn output or the operator handout, the shipping form for U2, deviations, follow-ups. Reply to the coordinator with the same in ≤ 250 words plus the report path.

STANDING
Read and obey `.orchestration/orchestrate/regime-cutover/preferences.md` (16 lines) before any command.
