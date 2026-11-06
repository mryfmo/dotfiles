# U250 the DSH login route's test items: use cases from the official documents and the kit's intent, each run and judged OK or NG

GOAL
Standing orders 41 and 44: a built capability is judged by executed test items derived from the official documentation of each component and from the kit's stated purpose, not by its pull request. The capability under test is the DSH login route of U238 shape (d): a DSH turn on provider `claude-bridge` reaches a child `omp auth-gateway stdio` and the operator's Claude login, with no API key (the frame row of 05:46:33Z), the adapter plugin of U240 and U240b at `home/dot_dsh/plugins/omp-gateway/`. This unit writes the test items as a table, automates every item that can run against the stub gateway, and writes the exact commands for the items that need the real login, a seat or the kit profile, which the coordinator runs and judges. Every row ends OK or NG with pasted output; an NG is a fix unit, not a note.

SCOPE
A new branch `feat/dsh-login-route-tests` from the U240 head dc336b67ebe6456c976716288b9587555d802922 (your tree is `/tmp/dotfiles-wt/U250`). U240b is changing `translate.mjs` on the adapter branch in parallel (the system text moves into the first user turn as a `<dsh-system>` block and `body.system` disappears; the two shebang lines go); write the group (c) items against that intended behaviour and mark them `pending-rebase` in `verdict` when the current tree fails them for that reason alone; the coordinator rebases your branch onto the round-2 head and re-runs. May write: `home/dot_dsh/plugins/omp-gateway/test/use-cases.test.mjs` (new; the automated items), `home/dot_dsh/plugins/omp-gateway/proof/run-proof.mjs` only to add a `--case <id>` selector if the real-route items need one, the table `../U250-test-items.tsv` beside your tree (the coordinator copies it into the store as `tests/dsh-login-route.tsv`), and the body addendum `../U250-body-section.md` (a `## Test items` section the coordinator appends to the PR body). Not: `translate.mjs`, `gateway-client.mjs`, `config.mjs`, `index.mjs` (a defect you find is an NG row naming the file and line, fixed by the next round, not by you), anything outside the plugin directory.

CONTEXT
Sources, read-only on this host. DSH: `~/.dsh/dsh/dsh-v0.2.1-rc.5.CaRLjX/docs/config-catalog.md` (the `llm` seam, `agent-default-model`, the routes), `packages/llm/llm/src/types.ts:470-585` (chunk kinds and request fields), `packages/llm/llm/README.md` if present, `docs/cordis-tutorial/*.md` (plugin loading). omp: `omp auth-gateway --help` (the stdio form), `~/.local/lib/node_modules/@oh-my-pi/pi-coding-agent/src/cli/auth-gateway-stdio.ts`, the bridge's `prompt-capture.ts:148-211` (no `system` runs on Claude Code's preset prompt; an unmatched `system` is refused). The kit's intent: `AGENTS.md` (Test Policy), `docs/pi-claude-bridge.md`, the PRD rows R-24 and R-25 as amended on 2026-11-06 (login-only, no API key, hooks mounted), `home/dot_dsh/profiles/thak/cordis.patch.yml`. The measured facts: the U239 and U240 rows of `decisions.tsv` (text turn 1.9 s, tool turn 2.1 s, the 502 on an unmatched `system`, the multi-request child).

DATA SHAPE
One table, `U250-test-items.tsv`, columns `id	use_case	source	kind	command	expected	observed	verdict	ts`. `kind` is `auto` (runs in `node --test` against the stub), `real` (the coordinator runs it on the operator's login), `seat` (runs under srt in a seat, M-21's unit, left `pending` here) or `profile` (needs the kit's thak profile rows, U227's re-render, left `pending`). `source` cites the document and section or the intent clause. `verdict` is `OK`, `NG` or `pending`, never blank for an `auto` row. Use cases are the rows' groups; cover each from more than one side (a happy path, a boundary, a failure, an abuse).

CHANGE
1. Derive the use cases. At least these groups, each with items from more than one side: (a) a text turn (reply text, usage chunk, finish reason, model id as sent); (b) a tool turn (tool_use to tool_call, arguments intact, multi-tool reply, a tool the agent never declared, a tool_result round trip in the history); (c) the system text (folded into the first user turn as the `<dsh-system>` block, a history that starts with an assistant turn, no system at all, a `system`-role message mid-history, user text that itself contains the tag string); (d) the child process (ready line, no ready line within the bound, exit before reply, mismatched id, unparseable line, abort mid-request, two concurrent requests, respawn after exit); (e) errors (404 unknown model, 404 unknown path, 5xx, the 502 prompt-capture text surfaces whole); (f) configuration (defaults, `env` names only and no values, `cwd`, a `command` that does not exist, `providers` list of two); (g) the kit's intent (no credential name in any file or in the child's environment, no listener, no network from the plugin itself, kwp skills visible to a turn once the route works, the Claude hooks the thak profile mounts still fire); (h) the real login (`real`: the proof's two turns with `--command omp`, a turn whose system text is DSH's full thak prompt, a 3-step tool loop, the SIWC model id answering 404 until omp serves it).
2. Automate every `auto` item in `test/use-cases.test.mjs` against the stub (extend `fixtures.json` through the stub's selector only if an item needs a reply shape the fixtures lack; say which). Each test's name is its `id`.
3. For every `real`, `seat` and `profile` item write the exact command and the expected output in the table; the coordinator runs `real` items after your head is in and fills `observed` and `verdict`.
4. Run the `auto` items; fill `observed`, `verdict`, `ts` from the run. An NG row stays NG with the file and line of the defect in `observed`.
5. `../U250-body-section.md`: the table rendered as markdown with the counts per kind and per verdict, and one sentence per NG.

ACCEPTANCE
1. `node --test home/dot_dsh/plugins/omp-gateway/` exit 0 or, when an NG item exists, the failing test names equal the NG ids in the table (paste the summary lines).
2. `awk -F'\t' 'NR>1 && $4=="auto" && $8!="OK" && $8!="NG"' ../U250-test-items.tsv` prints nothing (every auto row judged).
3. `awk -F'\t' 'NR>1 {print $2}' ../U250-test-items.tsv | sort -u | wc -l` prints 8 or more (the groups above), and `wc -l ../U250-test-items.tsv` prints 40 or more.
4. `scripts/ci/run-on-lint-files.sh markdown prettier --check` exit 0, `scripts/ci/run-on-lint-files.sh python ruff format --config ruff.toml --check` exit 0, `scripts/ci/run-on-lint-files.sh shell shfmt -i 4 -sr -d` exit 0, and `grep -rln '^#!' home/dot_dsh/plugins/omp-gateway/` prints nothing.
5. `uv run python -m unittest tests.unit.test_scratch_git` OK.

VERIFY
ACCEPTANCE pasted into `../U250-body-section.md` under its own heading. The `real` rows are the coordinator's measurement, recorded in the store's `tests/dsh-login-route.tsv` and in `decisions.tsv`.

CLOSURE
allowlist

TRUST
TRUST: the unit trusts the documents it cites as the source of the use cases and the stub gateway's measured fixtures as the auto items' counterpart; it reads no credential, sends no model request, changes no plugin source file and decides no fix.

TIMEBOX
75 minutes.

FORBIDDEN
No `/v1/messages` request to the real omp; no read of `~/.omp`, `~/.claude`, `~/.codex`, `~/.config/omp` or any credential file; no write under `~/.dsh`, `~/.omp`, `~/.agents` or `~/Workspace`; no edit of the plugin's source modules; no API key or token anywhere; no network; no push; no `gh` call.

WORKER RULES (standing orders 21, 27, 29, 31, 34, 44; read `~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` lines 23 to 52)
- Never run git or edit files in `~/Workspace/dotfiles`, never push, never open or edit a PR, never edit the live store; you stop at a committed head in `/tmp/dotfiles-wt/U250` and the coordinator fetches it by path.
- Progress line beside your tree (`../U250-progress.txt`) every ten minutes at most; first edit within ten minutes.
- Commit unsigned: `git -c commit.gpgsign=false commit`. Every commit message ends with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.
- Comments explain a non-obvious why only, no phase narration; a test's name documents the item.
- Follow `~/.agents/pstack/skills/poteto-mode/SKILL.md` (Test Behavior, Not Implementation: every item asserts what a DSH turn's reader can observe).

REPORT
Status, head sha (40 hex), files changed (`git diff --stat dc336b67`), the counts per kind and per verdict, the NG ids with one clause each, the ACCEPTANCE result lines, deviations. Under 16 lines, ending with `head=<40 hex>`.

STANDING
`preferences.md` (standing orders 21, 27, 29, 34, 41, 44); `AGENTS.md`; `briefs/U240-*.md` and `briefs/U240b-*.md`; the `decisions.tsv` rows of phase `M-21` for U239 and U240 and the frame rows of 05:46:33Z and order 44.
