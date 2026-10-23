# U3 openai-siwc design + skeleton — brief

GOAL
Design and scaffold the omp extension `openai-siwc` (official Sign in with ChatGPT route for the audit-side seats) as a buildable TypeScript package in this repo with behaviour tests against a fake authorization server and a fake Responses stream, so that a follow-up unit can finish the implementation against the real endpoints. Design before code: types, signatures, module structure, test plan (the pstack **architect** skill, single-runner form; read `~/.claude/plugins/cache/cursor-plugins/pstack/0.15.30/skills/architect/SKILL.md` first and apply its sketch step; skip the arena).

SCOPE
Exclusive worktree (the harness gives you one; branch name `feat/openai-siwc-extension`). May write only: `home/dot_agents/omp/extensions/openai-siwc/**` (package: `package.json` with `omp.extensions: ["./src/index.ts"]`, `src/*.ts`, `tests/**`, `README.md`), and `docs/openai-siwc.md` (design doc, English). Nothing else in the repo. No installs into the real `~/.omp`.

CONTEXT (read all before designing)
- `.orchestration/validation/025-v13-facts-20261023.md` §3, §3b (omp 18.11.3 `registerProvider(name, ProviderConfigInput)` shape: `api`, `baseUrl`, `apiKey`, `headers`, `compat`, `authHeader`, `oauth: { name, login(callbacks), refreshToken?, getApiKey?, modifyModels? }`, `fetchDynamicModels?`, `models[]`; `OAuthCredentials { refresh, access, expires, email?, accountId?, … }`; pi-ai's `OAuthCallbackFlow` loopback helper at `node_modules/@oh-my-pi/pi-ai/src/registry/oauth/callback-server.ts`; `openai-responses.ts:548-567` `compat.storeResponses` and `PI_OPENAI_STATEFUL`), §4 (official SIWC endpoints, dynamic registration `client_id=dynamic_agent_client`, `ext_agent_host_id`, `agent_name_hint`, PKCE S256, loopback `127.0.0.1`, scopes, `resource`, token exchange, refresh, limitations list).
- `.orchestration/validation/025-pilot-facts.md` #S0: measured on 2026-10-23: registration needs `ext_agent_host_id=urn:uuid:<uuid4>`; issued `client_id` prefix `oaiapp`; token `expires_in 3600` with `chatgpt.tokens.use.direct`; Responses `store:false stream:true` completed; `instructions` accepted; `GET /v1/models` returned 0 entries (model ids come from the manifest, `fetchDynamicModels` optional).
- `.orchestration/validation/025-pilot-s0-siwc-probe.py`: the Python probe that worked (authorize URL, token exchange, SSE parse). Port its exact request shapes.
- `.orchestration/validation/025-review-r12-redteam.md` row R12R-07: omp's `openai-responses` request builder sends `prompt_cache_retention`, `max_output_tokens`, and `role: developer` items that the SIWC preview rejects; confirm in `node_modules/@oh-my-pi/pi-ai/src/providers/openai-responses.ts` which fields are emitted and design the strip/rewrite (system or developer text → top-level `instructions`).
- omp source for extension authoring: `~/.local/lib/node_modules/@oh-my-pi/pi-coding-agent/src/extensibility/**`, `src/config/model-registry.ts:3453-3500` (`registerProvider`), `node_modules/@oh-my-pi/pi-ai/src/registry/oauth/*`, `node_modules/@oh-my-pi/pi-ai/src/providers/openai-responses*.ts`. Upstream docs (fetch, `main` branch; confirm against installed source): `https://raw.githubusercontent.com/can1357/oh-my-pi/main/docs/adding-a-provider.md`, `…/docs/extensions.md`, `…/docs/providers.md`, `…/docs/provider-compat-reference.md`.
- Repo conventions: `home/dot_agents/omp/policies/` is the sibling location named by plan 025 for omp policy files; TypeScript packages in this repo: none yet, so keep the toolchain minimal (Bun test runner, which omp itself uses; no new dependencies unless the omp SDK requires one).

ACCEPTANCE
1. `docs/openai-siwc.md`: data shapes (registration record per profile `{ hostId: "urn:uuid:…", clientId, accountId? }` persisted under the profile's agent dir, `OAuthCredentials` mapping, request rewrite table), the `registerProvider` call shape, the login flow (loopback on 127.0.0.1, PKCE, dynamic registration first time, reuse of the issued client_id, scope check `chatgpt.tokens.use.direct`), refresh (1 h access, 30 d rotating refresh, `grant_type=refresh_token` with the saved client_id and `resource`), the strip/rewrite list with `file:line` for each omp-emitted field, error mapping for `subscription_sharing_usage_limit_exceeded` and `subscription_sharing_usage_unavailable`, and a threat table (token store 0600, loopback port, redirect validation, log redaction, hosts `auth.openai.com` and `api.openai.com`).
2. `src/` skeleton with the real module boundaries and typed signatures (`index.ts` registering the provider; `oauth.ts`; `requests.ts` for the rewrite; `store.ts` for the registration record), bodies implemented where the design is settled, `TODO(unit U3b)` markers only where a real-endpoint measurement is needed.
3. Tests runnable with `bun test` inside the package: a fake authorization server (loopback) proving PKCE + dynamic registration + token exchange + refresh rotation; a fake Responses SSE stream proving `store:false`, `stream:true`, no `previous_response_id`, rejected fields stripped, system text moved to `instructions`, `response.completed` handling. Tests must pass in your worktree; paste the `bun test` output.
4. No secret appears in any log line or fixture; `README.md` names the operator steps (`/login openai-siwc` per profile) with `source` lines.
5. Commit on your branch, push, open a draft PR titled `feat(omp): openai-siwc provider extension (design + skeleton)` with an English description per STANDING 14. Do not merge.

VERIFY
`bun test` in the package dir (paste), `bun build --no-bundle` or `bunx tsc --noEmit` if a tsconfig exists (paste), `git diff --stat main...HEAD` (paste). Network: `raw.githubusercontent.com` for docs; `registry.npmjs.org` only if Bun needs the omp type packages (prefer importing types from the installed omp path via a `paths` alias in a local `tsconfig.json`, documented as a shortcut).

TIMEBOX
90 minutes. On expiry, commit what passes and report.

FORBIDDEN
No real OpenAI calls, no login attempts, no writes outside SCOPE, no edits to the compat patch or to other units' files, no new runtime dependency without naming it in the report.

REPORT
≤ 250 words: branch, head sha, PR link, test output summary, the strip list with citations, open design questions with your default.

STANDING
Read and obey `.orchestration/orchestrate/regime-cutover/preferences.md` (16 lines) before any command.
