# U251 DSH runs under srt through a kit launcher with the worker seat's containment

GOAL
The goal sentence puts everything inside Anthropic's sandbox. omp seats run under srt through `hcom-seat` (U85); DSH today runs uncontained, and M-21 proved only by hand that a `dsh` start under srt works (decisions rows of 2026-11-06T03:50:31Z: hand-written settings in a disposable `DSH_HOME`, the credential denies of a worker seat kept, the settings file read-denied, no `allowNestedUserNamespaces`; the canary printed `write-denied read-denied ssh-denied`; `dsh --version` and `--dump-config` ran under it; a start with cwd inside a read-denied checkout died on `uv_cwd EPERM`). This unit turns that measurement into a lever: `dsh-srt`, a launcher that renders the settings from the same lists `hcom-seat` builds for a worker seat, runs the canary, and starts `dsh` under srt with the login route's child (`omp auth-gateway stdio`, which spawns the Claude Agent SDK and Claude Code) able to reach its login, so the DSH control host of the goal is contained like the seats it will drive.

SCOPE
A new branch `feat/dsh-srt-profile` from `origin/main` b49be338 (your tree is `/tmp/dotfiles-wt/U251`). May write: a new `scripts/orchestrator/dsh-srt` and its deployed copy `home/dot_local/bin/common/executable_dsh-srt` (find how the other levers keep source and copy in step and pin them in the manifest; one lever, one copy), a new `tests/unit/test_dsh_srt.py`, the manifest pin rows for the new lever only, `scripts/generated-agent-outputs.json` if the generator rewrites it, `docs/deepseek-harness.md` or the document that describes the DSH route (one paragraph; find it by grepping `DSH_HOME` under `docs/`), and the body `../U251-pr-body.md`. Not: `hcom-seat` itself (read it, do not change it), the DSH profile rows (U227b), the plugin (U240), the updater.

CONTEXT
Read-only sources. `scripts/orchestrator/hcom-seat:1349-1760` builds a seat's `srt-settings.json`: `allowedDomains` (`:1744` adds the ChatGPT hosts; read what precedes it for the Anthropic hosts), the `denyRead` list (`:1711`, `~/.ssh`, `~/.gnupg`, cloud credentials), the `denyWrite` list (`:1684-1710`, the operator's Claude state, `.omp`, `.codex`, git state), `allowWrite` (the seat's own roots), `allowPty`, and the Linux tool rows; the canary and the `omp` shim at `:46-49`. srt's own documentation: `~/.local/lib/node_modules/@anthropic-ai/sandbox-runtime/README.md` (or wherever `srt` is installed; `hcom-seat:1597` finds it on PATH) for the settings schema. The M-21 rows in `decisions.tsv` (grep `\tM-21\t`, 2026-11-06T03:50:31Z and 03:51:20Z) for the measured DSH-specific facts: the cwd must be a scratch root, not the read-denied checkout; `DSH_HOME` is the write root; the settings file itself is read-denied; `agentsHome` resolves to `~/.agents` so `~/.agents/skills` must stay readable. The login route's child: `omp auth-gateway stdio` reads omp's settings (`~/.omp` or `~/.config/omp`; measure which with the installed omp 18.12.6) and the `pi-claude-bridge` extension spawns Claude Code, which reads the operator's Claude login (keychain on macOS, measured in U190: the seat bridge child uses `CLAUDE_CONFIG_DIR` and the explicit denies of the operator's Claude state; read `docs/pi-claude-bridge.md` and the U190b body in `briefs/U190b-*.md` for the per-seat Claude state rule). The DSH install: `~/.dsh` (`DSH_HOME`), `~/.dsh/bin/dsh`, profiles under `~/.dsh/profiles/`.

DATA SHAPE
One launcher, one settings file, one canary. `dsh-srt [--profile <name>] [--home <DSH_HOME>] -- <dsh args>` renders `<DSH_HOME>/.sandbox/srt-settings.json` from a table of rows (write roots: `DSH_HOME`, a scratch cwd under `$TMPDIR`, the per-run Claude state directory for the bridge child; read denies: the worker seat's list verbatim plus `<DSH_HOME>/.sandbox`; write denies: the worker seat's list verbatim; domains: the worker seat's list verbatim; no listener, no unix sockets beyond what the worker seat allows), runs the canary (`write-denied read-denied ssh-denied` as `hcom-seat`'s shim does; refuse to start on any other answer), then `exec srt --settings <file> -- <DSH_HOME>/bin/dsh --profile <name> <args>` with cwd the scratch root and the environment reduced to the names the launcher lists (`HOME`, `PATH`, `DSH_HOME`, `TMPDIR`, `LANG`, `TERM`, and the Claude state variable the bridge child needs). Every list lives in one table at the top of the script with a comment naming its `hcom-seat` line, so a reviewer can diff the two by eye until a later unit shares the code. Refusals before any start: srt not found or not the pinned line (`hcom-seat:1600`), `dsh` not under `DSH_HOME`, cwd inside a read-denied path, a settings render that fails to parse as JSON (`python3 -c json.load`), a canary that does not answer the three words.

CHANGE
1. Read `hcom-seat:1349-1760` and the M-21 rows; write the table of lists with its line citations (CONTEXT) and a one-paragraph design in `../U251-progress.txt` within the first 15 minutes (what is shared verbatim, what differs for DSH and why); then build.
2. `scripts/orchestrator/dsh-srt` per DATA SHAPE, shdoc header stating the contract and its refusals, `set -Eeuo pipefail`, every producer's exit status read (standing order 21).
3. `tests/unit/test_dsh_srt.py`: the rendered settings parse and carry the worker seat's deny lists (read them from `hcom-seat`'s source text in the test, so a drift fails the test), the refusals (no srt, srt of another line, dsh missing, cwd denied, canary wrong), the argv `srt` receives (a fake `srt` on PATH records it), the environment names passed (nothing else), idempotence of the render.
4. Measurement on this host, no login needed: `dsh-srt --home <scratch DSH_HOME copied from ~/.dsh with bin/ and the pinned dsh tree linked> -- --version` prints `0.2.1-rc.5` under srt; `-- --profile thak --dump-config` prints the composed tree (or the refusal that names the missing profile dependency); the canary line; a write attempt into `~/.ssh` from inside (`-- bash -c 'touch ~/.ssh/u251'` if `dsh` cannot run a shell, use the canary form `hcom-seat` uses) is denied. Paste each.
5. The body `../U251-pr-body.md`: Summary, Contract (guarantee: `dsh` started by `dsh-srt` runs under srt with the worker seat's read and write denies and domain list, writes only under `DSH_HOME` and its scratch cwd, and never starts when the canary fails; leaves out: the real-login turn under srt (the coordinator's item in `tests/dsh-login-route.tsv`, kind `seat`), the ACP delegation to omp seats (M-22), sharing the list code with `hcom-seat`), Threat table (one row per list, the canary, the environment, the cwd rule, the settings file's read deny), Verification (ACCEPTANCE pasted).

ACCEPTANCE
1. `uv run python -m unittest tests.unit.test_dsh_srt tests.unit.test_scratch_git` OK (paste the count; the tests named).
2. `make shellcheck` exit 0; `scripts/ci/run-on-lint-files.sh shell shfmt -i 4 -sr -d` exit 0; `scripts/ci/run-on-lint-files.sh python ruff format --config ruff.toml --check` exit 0; `scripts/ci/run-on-lint-files.sh markdown prettier --check` exit 0.
3. `cmp scripts/orchestrator/dsh-srt home/dot_local/bin/common/executable_dsh-srt` exit 0; if the manifest pins levers by sha256, `uv run --with pyyaml scripts/generate-agent-configs.py && make render-check` exit 0 and the pin row pasted.
4. The CHANGE 4 measurements pasted (the version under srt, the canary words, the denied write).
5. `uv run --no-project --with pyyaml scripts/lint-comparisons.py --changed` exit 0.

VERIFY
ACCEPTANCE pasted into the body's Verification section. The real-login turn under `dsh-srt` is the coordinator's `seat` item in `tests/dsh-login-route.tsv`.

CLOSURE
allowlist

TRUST
TRUST: the unit trusts `hcom-seat`'s worker-seat lists as the reviewed containment and copies them verbatim with citations, srt at the pinned line as the enforcement, and the M-21 measurements as the DSH-specific facts; it reads no credential, opens no network of its own, changes no seat lever and does not decide the profile rows or the plugin.

TIMEBOX
90 minutes. If the first 15 minutes show that the worker seat's lists cannot be reused without changing `hcom-seat`, report that design finding alone with citations and stop.

FORBIDDEN
No edit of `hcom-seat`, the plugin or the profile rows; no `/v1/messages` request to the real omp; no read of `~/.ssh`, `~/.gnupg`, `~/.omp` credentials, `~/.claude` or `~/.codex` beyond the measured denial; no write under `~/.dsh`, `~/.omp`, `~/.agents` or `~/Workspace` (the measurement uses a scratch copy under `/tmp`); no `allowNestedUserNamespaces`; no local bats; no network; no push; no `gh` call.

WORKER RULES (standing orders 21, 27, 29, 31, 34, 44; read `~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` lines 23 to 54)
- Never run git or edit files in `~/Workspace/dotfiles`, never push, never open or edit a PR, never edit the live store; you stop at a committed head in `/tmp/dotfiles-wt/U251` and the coordinator fetches it by path.
- Progress line beside your tree (`../U251-progress.txt`) every ten minutes at most; first edit within ten minutes, the design paragraph within fifteen.
- Commit unsigned: `git -c commit.gpgsign=false commit`. Every commit message ends with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.
- Comments explain a non-obvious why only, no phase narration. Shell comments are English shdoc.
- Follow `~/.agents/pstack/skills/poteto-mode/SKILL.md` (Boundary Discipline: the lists are the boundary; the launcher adds no logic beyond rendering, the canary and the exec).

REPORT
Status, head sha (40 hex), files changed (`git diff --stat origin/main`), the design paragraph in two lines, the ACCEPTANCE result lines, deviations. Under 16 lines, ending with `head=<40 hex>`.

STANDING
`preferences.md` (standing orders 21, 27, 29, 34, 35, 37, 41, 44, 45); `AGENTS.md` (threat table rule); the `decisions.tsv` M-21 rows of 2026-11-06; `briefs/U85-*.md` and `briefs/U190b-*.md` for the seat containment and the per-seat Claude state.
