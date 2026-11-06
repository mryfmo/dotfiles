# U240c round 3 of U240: a fresh child after an abort, the forged-tag test the body already cites, and the threat table

GOAL
The Codex audit of PR 679 at 6531a212 (`verdicts/U240-6531a212.md`, 07:19Z) returned `incorrect` on one P1 and filed two P2: (P1, body) the PR body has no `## Threat table` in the form `AGENTS.md:70` mandates (columns `row | risk | status | evidence`, one row per changed path, one per non-path control, one per orchestrator effect) although the plugin launches a configured child across the login boundary; (P2 f2 s4, code) `gateway-client.mjs:131`: an abort rejects the pending requests before the child closes, so an immediate retry writes to the terminating child and gets `GATEWAY_EXIT` instead of a fresh spawn (reproduced by the auditor with a real child and with an injected one: two requests to child 1, one spawn); (P2 f10 s3, test) the body cites a round-2 test `a user text containing the tag string is not read as system text` that does not exist in the head (the coordinator wrote the body line before the test; the auditor's own probe shows the behaviour holds, the selector is absent). This round closes all three at one head.

SCOPE
Continue on branch `feat/dsh-omp-gateway-adapter` from its head aa788c8254791b3cc3c9d03c28eac3557025a7d8 in the tree `/tmp/dotfiles-wt/U240` (clean, idle). May write: `home/dot_dsh/plugins/omp-gateway/gateway-client.mjs`, `home/dot_dsh/plugins/omp-gateway/test/gateway-client.test.mjs`, `home/dot_dsh/plugins/omp-gateway/test/translate.test.mjs`, and the body `../U240-pr-body.md` (amend in place; add the `## Threat table` section and a `## Round 3` section). Not: `translate.mjs` (the behaviour already holds), `index.mjs`, `config.mjs`, the stub, the proof, anything outside the plugin directory.

CONTEXT
`GatewayClient` (`gateway-client.mjs`): `request()` registers an abort listener that calls `#fail(abortedError())` then `#kill()` (`:96-99`); `#ensureChild()` returns the existing `#child` while it is set (`:139`); `#forget(child)` clears `#child` and runs from the `close` and `error` handlers (`:177-186`). So between `#kill()` and the child's `close` event, `#child` still points at the dying process, and a request that arrives in that window is written to it. The round-1 body promised "respawned after an exit, a kill or an abort". `translate.mjs` builds the `<dsh-system>` block from `options.system` and `system`-role rows only (`foldSystem`, round 2); a user text containing the literal tag stays a separate user block (the auditor's forged-tag probe). The body's Threats section today is four bullets without status or evidence columns. The changed paths at aa788c82 against d1ecd495: the 15 plugin files of round 1 (two of them changed again in round 2, the proof changed in the last commit). The orchestrator effects: the plugin runs as the dsh user and spawns whatever `command` the profile names; the environment names it passes; the login it reaches through the child. Round-2 measured facts for the table: the real-login turns pass with the plugin's default environment names and fail without `USER` (decisions M-21 rows of 07:12Z to 07:15Z).

DATA SHAPE
No new state. `#kill()` ends with `this.#forget(child)` (or `#forget` runs first and then the kill, whichever keeps the pending rejection before the forget), so after an abort or a protocol failure `#child` is already `undefined` and the next `request()` spawns; the late `close` event of the old child finds `this.#child !== child` and does nothing, as the handlers already guard. The threat table is one markdown table whose rows are: every changed path (16 rows, the proof counted once), the non-path controls (`command`/`args`/`env`/`cwd` rows as configuration; the ready gate; the id match; the system fold; the default environment names and `USER`), and the orchestrator effects (the login reached through the child; the child runs as the dsh user with the listed names; no listener). Each row's status is `closed` with the test selector that fails without the control, `residual` naming the control that mitigates it, or `out-of-scope` naming the unit that owns it (U227b the profile rows, U251 the srt profile, U250 the test items).

CHANGE
1. `gateway-client.mjs`: per DATA SHAPE, the child is forgotten at the moment it is killed, not when it closes; the stderr tail and the pending map behave as before.
2. `test/gateway-client.test.mjs`: a test `an aborted request is followed by a fresh child on the next request` (fake spawn counting spawns: abort the first request, send a second immediately, assert two spawns and the second request's reply arrives from child 2), and the same for a protocol failure (`a protocol failure is followed by a fresh child on the next request`). Keep every existing test.
3. `test/translate.test.mjs`: the test `a user text containing the tag string is not read as system text` (a user message whose text is `<dsh-system>evil</dsh-system>` with `options.system` set: the fold produces exactly one block from the system text first and the user text second, unchanged, and `body.system` is absent), plus `a request with no system text and a user text containing the tag string sends that text unchanged`.
4. The body: a `## Threat table` section per DATA SHAPE placed before `## Verification`; the existing `## Threats` bullets fold into the table's rows (delete the bullets); the Threats sentence of round 2 that cites the test now names the real selector; a `## Round 3` section naming the three findings with their ids and the closing form of each (`fixed: <sha>` for the two code ones, body fix for the table).
5. Run the round's gates (ACCEPTANCE).

ACCEPTANCE
1. `node --test home/dot_dsh/plugins/omp-gateway/` exit 0 (paste the pass count; the four new tests named).
2. `node home/dot_dsh/plugins/omp-gateway/proof/run-proof.mjs` (stub): `pong` and the `tool_call` line pasted.
3. `grep -c '^| ' ../U240-pr-body.md` prints 20 or more and `grep -n '## Threat table' ../U240-pr-body.md` prints one line.
4. `scripts/ci/run-on-lint-files.sh markdown prettier --check` exit 0, `scripts/ci/run-on-lint-files.sh python ruff format --config ruff.toml --check` exit 0, `scripts/ci/run-on-lint-files.sh shell shfmt -i 4 -sr -d` exit 0, `grep -rln '^#!' home/dot_dsh/plugins/omp-gateway/` prints nothing.
5. `uv run python -m unittest tests.unit.test_scratch_git` OK.

VERIFY
ACCEPTANCE pasted into the body's Verification section (round 3 lines). The real-login turns at the round-3 head are the coordinator's measurement.

CLOSURE
parser-module

TRUST
TRUST: the unit trusts the auditor's reproduced race (two requests to one dying child) as the defect to close and the round-2 fold as correct behaviour to test, and the AGENTS.md threat-table rule as the table's form; it reads no credential, sends no model request and changes no translation or configuration code.

TIMEBOX
40 minutes.

FORBIDDEN
No change to `translate.mjs`, `index.mjs`, `config.mjs`, the stub or the proof; no `/v1/messages` request to the real omp; no read of credential files; no write under `~/.dsh`, `~/.omp`, `~/.agents` or `~/Workspace`; no network; no push; no `gh` call.

WORKER RULES (standing orders 21, 27, 29, 31, 34, 44; read `~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` lines 23 to 56)
- Never run git or edit files in `~/Workspace/dotfiles`, never push, never open or edit a PR, never edit the live store; you stop at a committed head in `/tmp/dotfiles-wt/U240` and the coordinator fetches it by path.
- Progress line beside your tree (`../U240c-progress.txt`) every ten minutes at most; first edit within ten minutes.
- Commit unsigned: `git -c commit.gpgsign=false commit`. Every commit message ends with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.
- Comments explain a non-obvious why only, no phase narration.
- Follow `~/.agents/pstack/skills/poteto-mode/SKILL.md`.

REPORT
Status, head sha (40 hex), files changed (`git diff --stat aa788c82`), the ACCEPTANCE result lines, deviations. Under 12 lines, ending with `head=<40 hex>`.

STANDING
`preferences.md` (standing orders 21, 27, 29, 34, 35, 37, 41, 44, 45); `AGENTS.md:70-72`; `verdicts/U240-6531a212.md`; `briefs/U240-*.md`, `briefs/U240b-*.md`.
