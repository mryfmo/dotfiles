# U240b round 2 of U240: the adapter sends no system prompt; DSH's instructions ride in the first user turn

GOAL
U240's head dc336b67 (PR 679) passes its stub proof, and the coordinator's real-login measurement at 06:30Z failed both turns with HTTP 502 from pi-claude-bridge: `prompt-capture: no capture for this 1-char system prompt, and it embeds none of the 0 known`. The bridge's rule (`~/.local/lib/omp-extensions/pi-claude-bridge/src/prompt-capture.ts:148-211`, `resolveOrDerive`): a request with no `system` resolves to no capture and runs on Claude Code's own preset prompt (U239's bare probe passed this way); a request whose `system` matches no capture recorded from a pi session throws, by design, because Claude Code's Anthropic path cannot take an arbitrary harness prompt and the bridge refuses to drop instructions silently. A DSH client has no pi session and never will have a capture, so the adapter must not send `system`. This round folds the system text into the first user turn as a marked block, so Claude Code's preset prompt governs the child and DSH's instructions still reach the model as the first thing it reads. The bridge is not changed.

SCOPE
Continue on branch `feat/dsh-omp-gateway-adapter` from its head dc336b67ebe6456c976716288b9587555d802922 in the tree `/tmp/dotfiles-wt/U240` (the U240 worker's tree, idle). May write: `home/dot_dsh/plugins/omp-gateway/translate.mjs`, `home/dot_dsh/plugins/omp-gateway/test/translate.test.mjs`, `home/dot_dsh/plugins/omp-gateway/index.mjs` only if the doc comment names the system prompt, `home/dot_dsh/plugins/omp-gateway/stub-gateway.mjs` and `fixtures.json` only if the selector must read the new block, and the body `../U240-pr-body.md` (amend in place: Summary, Contract, Verification, Threats, and a `## Round 2` section naming the measurement and the change). Not: `gateway-client.mjs`, `config.mjs`, the proof runner, anything outside the plugin directory, the bridge.

CONTEXT
`toMessagesBody` (`translate.mjs:12-43` at dc336b67) collects `options.system` and every `system`-role message into `system[]` and emits `body.system` when non-empty. DSH's loop sends its assembled system prompt there on every step, so every real turn throws at the bridge. The measured 1-char prompt came from the scratch proof profile; the kit's thak profile sends DSH's full prompt, which the bridge refuses the same way. Claude Code's preset prompt (`systemPrompt: {type: "preset", preset: "claude_code", append}` at `index.ts:2061-2064`) is what the child runs under when no capture resolves. The bridge's other guard (`prompt-capture.ts:384-388`) refuses a prompt that carries pi's harness text or the subscription-gate phrase pair; DSH's text is not pi's, and this round changes nothing there.

DATA SHAPE
`toMessagesBody` gains one rule and loses one field. The collected system text becomes the leading text block of the first `user` message: `{type: "text", text: "<dsh-system>\n" + system.join("\n\n") + "\n</dsh-system>"}` prepended to that message's content blocks; when the first message is not a user message (a replayed history starting with an assistant turn), a new user message holding only that block is inserted at index 0. `body.system` is never set. The tag name is one constant exported from `translate.mjs` so the test and any later reader share it. Nothing else in the body changes; `toChunks` and `toError` are untouched.

CHANGE
1. `translate.mjs`: the rule of DATA SHAPE, with the constant `SYSTEM_BLOCK_TAG = "dsh-system"`. Keep the per-message `system`-role collection (those texts join the same block, in order).
2. `test/translate.test.mjs`: replace the test that asserts `body.system` with tests that (a) a request with `system` and a first user text message produces a first user message whose first block is the tagged system text and whose second block is the user text, and no `body.system`; (b) a request whose first message is an assistant turn gets a new user message at index 0 holding the block alone; (c) a request with no system text and no `system`-role message sends the user message unchanged and no `body.system`; (d) a `system`-role message in the middle of the history is folded into the same leading block, in order, and does not appear in `messages`.
3. The stub and fixtures: unchanged unless the stub's `lastUserText` selector no longer finds the ping sentence because the block now precedes it; if so, make the selector read the last text block of the last user message, and say so.
4. The body `../U240-pr-body.md`, amended: Summary (one paragraph on the fold and why), Contract guarantee adds "the adapter never sends a `system` field; DSH's system text reaches the model as the first block of the first user turn under Claude Code's preset prompt", Leaves out adds "a bridge-side append mode for non-pi clients (the residual that would restore system authority to DSH's prompt)", Threats adds the fold (a user-authored message cannot be mistaken for the block: the block is built by the adapter from `options.system` and `system`-role messages only, never from user content), Verification re-run (the three ACCEPTANCE items below), and a `## Round 2` section: the measurement (quote the 502 line), the bridge rule with its `file:line`, the change.

ACCEPTANCE
1. `node --test home/dot_dsh/plugins/omp-gateway/` exit 0 (paste the pass count; the four new tests named).
2. `node home/dot_dsh/plugins/omp-gateway/proof/run-proof.mjs` (the stub): both turns pass as in round 1 (paste the `pong` line and the `tool_call` line).
3. `grep -n 'body.system' home/dot_dsh/plugins/omp-gateway/translate.mjs` prints nothing.

4. `scripts/ci/run-on-lint-files.sh shell shfmt -i 4 -sr -d`, `scripts/ci/run-on-lint-files.sh python ruff format --config ruff.toml --check` and `scripts/ci/run-on-lint-files.sh markdown prettier --check` exit 0 (the Makefile `format` target), run in the tree after the last edit. (added 2026-11-06T07:20Z under standing order 44; the heads of these units were checked by the coordinator with the same commands.)
VERIFY
ACCEPTANCE pasted into the body. The real-login turn is the coordinator's measurement after your head is in (`run-proof.mjs --command omp --args '["auth-gateway","stdio"]'`), recorded in `decisions.tsv`.

CLOSURE
parser-module

TRUST
TRUST: the unit trusts the bridge's documented rule that a request without a system field runs on Claude Code's preset prompt, and the adapter's own construction of the block from the request's system text alone; it reads no credential, sends no model request, changes no file outside the plugin directory and does not change the bridge.

TIMEBOX
30 minutes.

FORBIDDEN
No `/v1/messages` request to the real omp; no read of `~/.omp`, `~/.claude`, `~/.codex`, `~/.config/omp` or any credential file; no write under `~/.dsh`, `~/.omp`, `~/.agents` or `~/Workspace`; no change to the bridge; no API key, token or `apiKeyEnv` row; no network; no push; no `gh` call.

WORKER RULES (standing orders 21, 27, 29, 31, 34; read `~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` lines 23 to 50)
- Never run git or edit files in `~/Workspace/dotfiles`, never push, never open or edit a PR, never edit the live store; you stop at a committed head in `/tmp/dotfiles-wt/U240` and the coordinator fetches it by path.
- Progress line beside your tree (`../U240b-progress.txt`) every ten minutes at most; first edit within ten minutes.
- Commit unsigned: `git -c commit.gpgsign=false commit`. Every commit message ends with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.
- Comments explain a non-obvious why only, no phase narration.
- Follow `~/.agents/pstack/skills/poteto-mode/SKILL.md`.

REPORT
Status, head sha (40 hex), files changed (`git diff --stat dc336b67`), the ACCEPTANCE result lines, deviations. Under 12 lines, ending with `head=<40 hex>`.

STANDING
`preferences.md` (standing orders 21, 27, 29, 34, 35, 37, 41); `AGENTS.md`; `briefs/U240-dsh-adapter-over-omp-stdio-gateway-prototype.md` (round 1, still the unit's brief); the `decisions.tsv` row of phase `M-21` at 06:32:06Z (the measurement).
