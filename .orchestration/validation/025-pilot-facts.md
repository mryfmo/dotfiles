# Plan 025 pilot facts (leg 1). Every block is pasted output; masked where the plan requires.

## #S0 official Sign in with ChatGPT probe (2026-10-23T00:01:47Z, operator's terminal via the `!` prefix, outside the agent sandbox)

Command: `uv run --no-project siwc_probe.py --test-instructions` (a throwaway probe kept outside the repository: its strings match the committed-secret scan; its request shapes now live in the openai-siwc extension's tests, PR #458).

Run 1 (bare uuid4 as `ext_agent_host_id`): the authorize endpoint answered `{"error":{"message":"Invalid authorize request","type":"invalid_request_error","param":"ext_agent_host_id","code":"invalid_authorize_request"}}` (pasted by the operator). Fix: `ext_agent_host_id` = `urn:uuid:<uuid4>` (the only format hint on the sign-in page is the sample credential placeholder `"urn:uuid:..."`).

Run 2 (`urn:uuid:` form), masked report (authorize URL with one-time state/nonce/challenge omitted; no token printed):

```json
{
  "callback_keys": ["client_id", "code", "scope", "state"],
  "issued_client_id_present": true,
  "issued_client_id_prefix": "oaiapp",
  "token": {"status": 200, "expires_in": 3600,
            "scope": "chatgpt.tokens.use.direct email offline_access openid profile resource.invoke",
            "has_refresh": true, "has_id_token": true, "access_len": 2105},
  "plan_usage_scope_granted": true,
  "models_listed": [], "models_total": 0,
  "model_used": "gpt-6.1-sol",
  "responses": {"completed": true, "n_events": 11, "text": "PONG", "response_id_present": true,
                "event_types": ["response.completed", "response.content_part.added", "response.content_part.done",
                                "response.created", "response.in_progress", "response.metadata",
                                "response.output_item.added", "response.output_item.done",
                                "response.output_text.delta", "response.output_text.done"],
                "usage": {"input_tokens": 14, "output_tokens": 6, "total_tokens": 20,
                          "input_tokens_details": {"cache_write_tokens": 0, "cached_tokens": 0},
                          "output_tokens_details": {"reasoning_tokens": 0}, "attribution": "per-message items (omitted)"}},
  "responses_with_instructions": {"completed": true, "n_events": 11, "text": "PONG", "response_id_present": true,
                "usage": {"input_tokens": 23, "output_tokens": 6, "total_tokens": 29,
                          "attribution": {"request_fields": {"instructions": {"input_tokens": 9}}}}}
}
```

Readings:
- Dynamic client registration works for a personal local app with `client_id=dynamic_agent_client`, `ext_agent_host_id=urn:uuid:<uuid4>`, `agent_name_hint=omp-dotfiles-probe`; the callback carries the issued `client_id` (prefix `oaiapp`), `code`, `scope`, `state`.
- Token exchange (form-encoded, no client secret) returns a 1 h access token, a refresh token, an ID token, and the granted scope set including `chatgpt.tokens.use.direct`.
- `POST /v1/responses` with `store:false`, `stream:true`, full `input`, model `gpt-6.1-sol` completes (`response.completed`) with usage; the top-level `instructions` field is accepted (attributed 9 input tokens), so system text goes through `instructions`.
- `GET /v1/models` with the SIWC bearer returned no entries (`models_total` 0): model discovery through that endpoint is NOT available on this route as probed; model ids come from the manifest (`model_profiles`) and `fetchDynamicModels` is optional. Follow-up measurement: the raw response body of `/v1/models` (shape, status) inside the extension's first run.
- Side effect: an agent registration named `omp-dotfiles-probe` now exists in the operator's ChatGPT account (deletable in ChatGPT settings); the production extension registers under decision (28)'s name with its own stable host id.

## #B1 bridge install under omp 18.11.3 (2026-10-23T00:2xZ, operator terminal, `omp install pi-claude-bridge@0.9.3 --json`)

Result (pasted): `✘ Failed to install pi-claude-bridge@0.9.3: Error: Plugin pi-claude-bridge extension validation failed: ~/.omp/plugins/node_modules/pi-claude-bridge/src/index.ts: Failed to load extension: Export named 'formatSkillsForPrompt' not found in module 'omp-legacy-pi-bundled:@oh-my-pi/pi-coding-agent'.`
Readings: omp's plugin root is `~/.omp/plugins/` (not `~/.omp/agent/plugins/`); omp rewrote the bridge's `@earendil-works/pi-coding-agent` import to its bundled legacy shim (`omp-legacy-pi-bundled:@oh-my-pi/pi-coding-agent`) and the shim lacks `formatSkillsForPrompt`; the install rolled the package back (`plugins/package.json` dependencies `{}`, no `pi-claude-bridge` dir) but left the resolved dependency tree in `~/.omp/plugins/node_modules` (`@anthropic-ai`, `@earendil-works`, `@modelcontextprotocol`, …). STOP A7 fix round 1 = measure the full import gap against the three legacy shims (below) and patch the bridge locally.

### #B1 fix round 1 (orchestrator, 2026-10-23T00:3xZ): import gap and local patch

Value imports of pi-claude-bridge 0.9.3 from `@earendil-works/pi-*` (grep of `src/`): pi-ai `calculateCost`, `createAssistantMessageEventStream`, `StringEnum`, `Message as PiMessage`, `ProviderResponse`; pi-coding-agent `buildSessionContext`, `CONFIG_DIR_NAME`, `formatSkillsForPrompt`, `getAgentDir`, `keyHint`, `Skill`; pi-tui `Text`. omp 18.11.3 legacy shims (`src/extensibility/legacy-pi-{ai,tui,coding-agent}-shim.ts`): pi-ai shim `export * from "@oh-my-pi/pi-ai"` (+ `calculateCost`, `StringEnum`), pi-tui shim `export * from "@oh-my-pi/pi-tui"` (`Text` = `components/text.ts`), coding-agent shim exports `getAgentDir` (line 37), `keyText` (line 434), `CONFIG_DIR_NAME` (line 1604) but NOT `formatSkillsForPrompt`, `keyHint`, `buildSessionContext` (only a comment at line 1561).
Patch (`.orchestration/validation/025-pilot-bridge-omp-compat.patch`, 69 lines, applied to the copy at `/tmp/claude-501/pcb-patched1/package`): `src/skills.ts` gets Pi's `formatSkillsForPrompt` + `escapeXml` as local functions (same output, MIT); `src/index.ts` imports `keyText` instead of `keyHint` and renders the expand hint as `theme.fg("dim", keyText("app.tools.expand")) + theme.fg("muted", " to expand")`; the deprecated AskClaude tool's non-isolated session context (`buildSessionContext(...)`) becomes `context: undefined` with a `shortcut:` comment. No other file changed. Remaining value imports all exist in omp. Next: operator installs from the patched local path (B1').

### #B1' (operator, 2026-10-23T00:3xZ): `omp install /tmp/claude-501/pcb-patched1/package --json`

Result (pasted): `{"name":"pi-claude-bridge","version":"0.9.3","path":"/tmp/claude-501/pcb-patched1/package","manifest":{"extensions":["./src/index.ts"],"version":"0.9.3"},"enabledFeatures":null,"enabled":true}`. The patched bridge passes omp's extension validation (fix round 1 of STOP A7 consumed; no second gap appeared). The plugin is linked from the local path, so W2d must stage the patched package under the trusted path with its dependencies.

### #B2 (operator, 2026-10-23T00:3xZ): `omp plugin list --json && omp plugin doctor`

Result (pasted): list `npm: [{"name":"pi-claude-bridge","version":"0.9.3","path":"~/.omp/plugins/node_modules/pi-claude-bridge","manifest":{"extensions":["./src/index.ts"],"version":"0.9.3"},"enabled":true}]`, `marketplace: []`; doctor `✔ plugins_directory: Found at ~/.omp/plugins`, `✔ package_manifest`, `✔ node_modules`, `✔ plugin:pi-claude-bridge: v0.9.3 …`, `Summary: 4 ok, 0 warnings, 0 errors`. Reading: the local-path install was copied into omp's plugin store at `~/.omp/plugins/node_modules/pi-claude-bridge` (the install receipt earlier named the source path).

### #B3 (operator, 2026-10-23T00:4xZ): `omp --profile pilot-bridge models claude-bridge`

Result (pasted): `No models matching "claude-bridge"`. Cause (source, `src/extensibility/plugins/installer.ts:8`): `const PLUGINS_DIR = path.join(getAgentDir(), "plugins")`, and `--profile` changes the agent dir, so the plugin installed in the default profile's store (`~/.omp/plugins`, #B2) is not loaded under `pilot-bridge`. The bridge's model list itself comes from pi-ai's Anthropic catalog (`src/index.ts:2435` `applyLongContext(MODELS, …)`; omp's `@oh-my-pi/pi-catalog` carries `claude-fable-5-1*`, `claude-fable-5` …), so an empty list for that reason is not expected. Next: B3b (`-e <package dir>` form, profile-independent = decision 30), fallback = install into the profile (`omp --profile pilot-bridge install <dir>`).

### #B3b (operator, 2026-10-23T00:4xZ): `omp --profile pilot-bridge -e /tmp/claude-501/pcb-patched1/package --no-extensions models claude-bridge`

Result (pasted): `No models matching "claude-bridge"`. Two facts bear on it: `omp models --help` says `-e` loads "an extension file"; the loader (`src/extensibility/extensions/loader.ts:527,652`) resolves a directory through `indexNames: ["index.ts","index.js"]` at the directory root, and the bridge's entry is `src/index.ts` (declared in package.json `pi.extensions`), so a package directory root carries no index. Also `/tmp/claude-501/pcb-patched1/package` has no `node_modules` (dependencies were installed hoisted into `~/.omp/plugins/node_modules` by the plugin install), so a file loaded from the scratch path cannot resolve `@anthropic-ai/claude-agent-sdk`. Next: `-e` on the plugin-store copy's `src/index.ts` (deps resolve by walking up to `~/.omp/plugins/node_modules`).

### Correction to the #B3b reading (orchestrator, 2026-10-23T01:0xZ)

The installed 18.11.3 resolves an `-e` directory manifest-first (`src/extensibility/extensions/directory-resolution.ts:5-9`: `readDeclaredManifestEntries(dir)` → declared `omp.extensions`/`pi.extensions`, else `index.ts`/`index.js`, else a one-level scan), and the upstream doc `docs/extension-loading.md` (main) says the same. So `-e /tmp/claude-501/pcb-patched1/package` did resolve `./src/index.ts`; the earlier reading ("resolves only a root index.ts") was wrong, and the v14 disposition of R12R-10 that relied on it must be revised. The remaining candidate cause for the empty listing is that the module failed to import (that path has no `node_modules`; the plugin store copy has them hoisted) and `omp models` does not print extension load errors (`loader.ts:431-457` return the error to the caller; `commands/models.ts` has no print of it). Unverified until an instrument that shows extension load results is run (`omp extensions` listing or a session log); this is the pilot unit's first job, not an operator step.

### U1 unit (pstack orchestrate, 2026-10-23T01:28:20Z): see `.orchestration/validation/025-pilot-bridge-unit-report.md`

Corrections it establishes: #B2 'copied into omp's plugin store' is wrong (the install is a symlink to the local path); #B3/#B3b used an instrument (`omp models`) that never evaluates extension modules; the load gap after the 69-line patch is `contentText` (pi-ai shim), closed by patch v2; dependencies resolve upward from the entry realpath, so the staged directory needs its own `node_modules`.

### #G1 bridge turn with the host Claude login (operator terminal, 2026-10-23T01:31:20Z)

Command: `CLAUDE_BRIDGE_DEBUG=1 perl -e 'alarm 180; exec @ARGV' omp --profile pilot-bridge -e /tmp/claude-501/u1-work/pkg-probe --no-session --model claude-bridge/claude-haiku-4-5 -p "Reply with the single word PONG."`
Result (pasted): stdout `Working...` then `PONG`; stderr empty (no `Failed to load extension`). Reading: omp 18.11.3 → patched pi-claude-bridge (patch v1 + contentText) loaded from a directory with its own node_modules via `-e <dir>` → Agent SDK child → Claude Code with the host's claude.ai login → model answered. The Claude route of D-024-129 is proven end to end for a text turn; the bridged tool call, env check and process tree are the next rows of `.orchestration/orchestrate/regime-cutover/handouts/U1-operator-steps.md`.

### #G1-2 bridged tool call (operator terminal, 2026-10-23T01:34:54Z; saved event stream 71.8 KB, 362 lines)

Command: `perl -e 'alarm 180; exec @ARGV' omp --profile pilot-bridge -e /tmp/claude-501/u1-work/pkg-probe --no-session --model claude-bridge/claude-haiku-4-5 --approval-mode write --mode json -p "Use the bash tool to run exactly: echo bridged-tool-ok"`
Observed (grep of the saved stream): `toolcall_end` with `"name":"bash","arguments":{"command":"echo bridged-tool-ok","i":"verify bash tool","timeout":120}` (line 218; the `timeout: 120` injection of R12R-04 / decision 38 is confirmed on the wire); `tool_execution_start` for omp's `bash` tool (line 220); `tool_execution_end` result text `Tool "bash" requires approval but no interactive UI available. Options: 1. Set tools.approvalMode: yolo in /settings 2. Add tools.approval.bash: allow …` (line 221); second assistant turn explains the approval error; `agent_end`. No `Failed to load extension`. The model's thinking mentions "system reminders about using superpowers", i.e. the child Claude Code loaded the host's `~/.claude` settings and hooks (settingSources default), which supports U2's `settingSources: []` default.
Reading: the bridge delivered the model's tool call to omp's tool executor and omp's approval gate stopped it, because `--approval-mode write` does not cover `bash` in print mode. The gate is omp's own containment (U6's policy configures it per role: `tools.approval.bash: allow` for the worker, deny for audit). Next measurement: the same command with `--approval-mode yolo` (pilot only) to observe the tool output returning to the model.

### #G1-3 bridged tool call with `--approval-mode yolo` (operator terminal, 2026-10-23T01:36:53Z)

Pasted: `tool_execution_start` `{"toolName":"bash","args":{"command":"echo bridged-tool-ok","timeout":120},"intent":"verify tool bridge"}`; `tool_execution_end` `result.content[0].text = "bridged-tool-ok\n"`, `details.timeoutSeconds: 120`, `wallTimeMs: 25.5`, `isError: false`; two `turn_end` events, the second's thinking: "the bash tool is working correctly and the bridge is set up properly". The thinking also lists "Ponytail mode is active" and "AGMSG monitor would be set up if the Monitor tool were available": the host's Claude Code SessionStart hooks ran inside the bridge child and their text reached the model (settingSources default). Reading: omp executed the model's tool call and returned the output through the bridge; the Claude route is proven for text and tools. The `timeout: 120` injection is on the wire (decision 38). Handout rows 3 (env check) and 4 (process tree) are dropped: U2's `settingSources: []` default removes the hook question, and the process tree is not on the frontier.
