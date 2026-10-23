# openai-siwc: omp provider for Sign in with ChatGPT

Design for the omp 18.11.3 extension at `home/dot_agents/omp/extensions/openai-siwc/`. It gives the audit-side omp profiles ChatGPT plan inference through OpenAI's official Sign in with ChatGPT (SIWC) route, which omp does not ship (issue `can1357/oh-my-pi#13974`, facts §3). The package loads in omp 18.11.3 and registers the provider; it has not yet run a real login or completion (gate G2). The points that still need a real-endpoint measurement carry `TODO(gate G2)` and are listed under open questions.

Sources: `.orchestration/validation/025-v13-facts-20261023.md` (facts §3, §3b, §4), `.orchestration/validation/025-pilot-facts.md` #S0, the probe `.orchestration/validation/025-pilot-s0-siwc-probe.py`, red-team row R12R-07, the installed omp source under `~/.local/lib/node_modules/@oh-my-pi/pi-coding-agent` (paths below are relative to it), and upstream `docs/extensions.md` and `docs/provider-compat-reference.md` (main, fetched 2026-10-23).

## Problem

omp's built-in `openai-responses` transport already streams the Responses API, parses SSE, retries, and surfaces `response.completed`. The SIWC preview accepts a narrower request than omp builds. Measured against omp's real builder with a fake HTTP layer (the test `tests/requests.test.ts`), a provider named `openai-siwc` on `https://api.openai.com/v1` sends `prompt_cache_retention: "24h"`, `max_output_tokens`, and the system prompt as an `input` item with `role: "developer"`. The preview rejects all three, and it needs `store: false`, `stream: true`, and full history instead of `previous_response_id`.

Login is the other gap. SIWC registers each host dynamically: the first authorize request uses `client_id=dynamic_agent_client` plus `ext_agent_host_id`, and the callback returns the issued `client_id` that every later exchange and refresh must use. pi-ai's `OAuthCallbackFlow` cannot carry that value, because its callback handler keeps only `code` and `state` (`node_modules/@oh-my-pi/pi-ai/src/registry/oauth/callback-server.ts:560-576`).

## Usage

The operator installs the package once and logs in once per profile:

```text
omp --profile audit -e ~/.agents/omp/extensions/openai-siwc
/login openai-siwc
/model openai-siwc/gpt-6.1-sol
```

What the extension does at load:

```ts
export default function openaiSiwc(pi: ExtensionAPI): void {
  pi.registerProvider("openai-siwc", {
    baseUrl: "https://api.openai.com/v1",
    api: "openai-responses",
    compat: SIWC_COMPAT,
    oauth: createSiwcOAuth({
      agentDir: pi.pi.getAgentDir(),
      agentName: "omp-dotfiles",
    }),
    models: MODELS,
  });
  pi.on("before_provider_request", (event, ctx) =>
    ctx.model?.provider === "openai-siwc"
      ? rewriteResponsesRequest(event.payload)
      : undefined,
  );
}
```

## Shape

### Modules

| Module            | Owns                                                                                                                                      |
| ----------------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| `src/index.ts`    | The `registerProvider` call, the static model rows, and the `before_provider_request` hook.                                               |
| `src/oauth.ts`    | The `oauth` block: authorize URL, PKCE, loopback receiver, code exchange, refresh, scope and nonce checks.                                |
| `src/requests.ts` | `SIWC_COMPAT` and `rewriteResponsesRequest`, the only place that knows the preview's request rules.                                       |
| `src/store.ts`    | The per-profile registration record: its path, validation, and atomic 0600 write. It is the record's single writer, called by `oauth.ts`. |

The package has no runtime dependencies. It imports omp only as types (`import type`), which Bun erases.

### Registration record

One JSON file per omp profile at `<agentDir>/openai-siwc/registration.json`, where `agentDir` is `getAgentDir()` and therefore follows `--profile` (pilot facts #B3):

```ts
interface Registration {
  hostId: `urn:uuid:${string}`; // uuid4; a bare uuid was refused (pilot facts #S0 run 1)
  clientId?: string; // issued by the registration callback (prefix "oaiapp" measured)
  accountId?: string; // from the id_token account claim, when present
}
```

The record holds no secret. `clientId` is a public client identifier, and tokens never enter this file. Load rejects a malformed record instead of re-registering over it.

### OAuthCredentials mapping

Tokens live in omp's own credential store, `<agentDir>/agent.db`, which omp creates with directory mode 0700 and file mode 0600 (`node_modules/@oh-my-pi/pi-ai/src/auth/sqlite-credential-store.ts:587-594`).

| `OAuthCredentials` field | Source                                                                                 |
| ------------------------ | -------------------------------------------------------------------------------------- |
| `access`                 | `access_token`; `getApiKey` returns it and omp sends it as the bearer.                 |
| `refresh`                | `refresh_token`, replaced on every refresh.                                            |
| `expires`                | `now + expires_in × 1000`; `expires_in` measured as 3600.                              |
| `accountId`              | id_token claim `https://api.openai.com/auth` → `chatgpt_account_id` (`TODO(gate G2)`). |
| `email`                  | id_token claim `email`.                                                                |
| issued `client_id`       | Not in `OAuthCredentials`, which has no field for it; kept in the registration record. |

### Login flow

1. Load the registration record. When none exists, create one with a fresh `urn:uuid:` host id and save it before opening the browser, so a retried first login reuses the same host id.
2. Create a PKCE S256 pair, a fresh `state`, and a fresh OIDC `nonce`.
3. Bind the loopback receiver on `127.0.0.1` (never `localhost`), port 1455 when free, otherwise a random port. The redirect URI is `http://127.0.0.1:<port>/auth/callback`.
4. Build the authorize URL on `https://auth.openai.com/api/accounts/authorize` with `response_type=code`, the scopes `openid profile email offline_access resource.invoke chatgpt.tokens.use.direct`, `resource=https://api.openai.com/v1`, the PKCE challenge, `state`, `nonce`, and `ext_agent_host_id`. A first login sends `client_id=dynamic_agent_client` and `agent_name_hint=omp-dotfiles`. A later login sends the saved `client_id` and no name hint.
5. Hand the URL to omp through `callbacks.onAuth`; omp opens the system browser.
6. The receiver answers only `GET /auth/callback`. A callback whose `state` is not ours gets a 400 page and is ignored, because any local process can send one. A callback with our `state` and `error` ends the login. A callback with our `state` and `code` resolves it. The wait honours `callbacks.signal` and a 5-minute timeout.
7. Save the callback's `client_id` into the record when it differs from the saved one. The server is authoritative, and saving before the exchange keeps a failed exchange from causing a second registration.
8. Exchange the code at `https://auth.openai.com/api/accounts/oauth/token`, form-encoded, with `grant_type=authorization_code`, the issued `client_id`, `code`, `code_verifier`, the same `redirect_uri`, and the same `resource`. No client secret.
9. Refuse the grant unless its `scope` contains `chatgpt.tokens.use.direct`. A valid ID token alone does not authorize plan usage (sign-in page, facts §4). Refuse an id_token whose `nonce` differs from ours.

### Refresh

The access token lives 1 hour; the refresh token lives 30 days and rotates on every refresh (token reference, facts §4). `refreshToken` posts `grant_type=refresh_token` with the saved `client_id`, the stored `refresh_token`, and `resource`. It returns the replacement refresh token and keeps the old one only when a response omits it. Without a saved `client_id` it fails with an instruction to run `/login openai-siwc`. When a refresh response carries `scope`, the plan scope is checked again; an absent `scope` is accepted on refresh only (`TODO(gate G2)`).

### Request rewrite

Two layers, both on omp's own transport. `SIWC_COMPAT` stops omp from building most rejected shapes. `rewriteResponsesRequest` runs on every payload through `before_provider_request`, which omp passes to the transport as `onPayload` (`src/sdk.ts:4345-4346`), and the transport calls it for the first request and for both retry paths (`node_modules/@oh-my-pi/pi-ai/src/providers/openai-responses.ts:852-859`, `:1008`, `:1055`). Line references below are in `node_modules/@oh-my-pi/pi-ai/src/providers/`.

| omp-emitted field or item                                    | Where omp emits it                                                              | Handling                                                                                                                                                                                                                                                                                                                                                                             |
| ------------------------------------------------------------ | ------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `role: "developer"` system items in `input`                  | `openai-responses.ts:1640`, when `supportsDeveloperRole` resolves true          | Compat `supportsDeveloperRole: false` sends the system prompt as `instructions` (`:1660`). The rewrite folds any remaining `system` or `developer` message item into `instructions`, which also covers the Juice item (`:1779-1782`).                                                                                                                                                |
| `prompt_cache_retention: "24h"`                              | `openai-responses.ts:1663`                                                      | Compat `supportsLongPromptCacheRetention: false`; the rewrite deletes the field.                                                                                                                                                                                                                                                                                                     |
| `max_output_tokens`                                          | `openai-responses.ts:1677`, `openai-shared.ts:4082`                             | The rewrite deletes it. No compat key turns it off, and `omitMaxOutputTokens` is not accepted on an extension model row.                                                                                                                                                                                                                                                             |
| `temperature`, `top_p`                                       | `openai-shared.ts:4091-4092`, only when sampling params are supported           | The rewrite deletes them.                                                                                                                                                                                                                                                                                                                                                            |
| `store`                                                      | `openai-responses.ts:1671`, true only with `compat.storeResponses` (`:548`)     | The rewrite forces `store: false`.                                                                                                                                                                                                                                                                                                                                                   |
| `previous_response_id` with delta-only input                 | `openai-responses.ts:567` (`PI_OPENAI_STATEFUL`), `:836` forces `store: true`   | Compat `statefulResponses: false` turns chaining off. `PI_OPENAI_STATEFUL` outranks compat, so the extension refuses to load when it is truthy (`src/index.ts`). The rewrite still throws on the field, but that only reports: omp's runner catches a hook throw and sends the unrewritten payload (`src/extensibility/extensions/runner.ts:1590-1591`, `:1627-1632`, `:2121-2131`). |
| `configuration_update` input items                           | Stable-effort policy (`supportsConfigurationUpdate`, provider-compat-reference) | Compat `supportsConfigurationUpdate: false`.                                                                                                                                                                                                                                                                                                                                         |
| Other preview-rejected fields                                | Not emitted by the 18.11.3 builder for this provider                            | The rewrite deletes `background`, `conversation`, `max_tool_calls`, `metadata`, `moderation`, `multi_agent`, `prompt`, `safety_identifier`, `top_logprobs`, `truncation`, `user` in case a hook or a later omp adds them.                                                                                                                                                            |
| `prompt_cache_key`, `include`, `reasoning`, `stream_options` | Emitted (measured in the test's captured body)                                  | Kept. The preview does not list them as rejected. `TODO(gate G2)`: confirm on the real endpoint.                                                                                                                                                                                                                                                                                     |

`stream: true` is forced too. The rewrite copies the payload and never mutates omp's object.

### Error mapping

The preview reports `subscription_sharing_usage_limit_exceeded` when the plan's shared usage is spent and `subscription_sharing_usage_unavailable` when plan usage is not available to the account (models-and-inference page, facts §4). The wire status is unmeasured. The extension adds no error code of its own: omp's classifier already handles both, and `tests/requests.test.ts` proves it through omp's real transport with a fake 403 and a fake 429 body.

| Code                                        | Fake response | What omp 18.11.3 does                                                                                                                                                                                                                                                                                                                               | omp hook                                                                                                                                                 |
| ------------------------------------------- | ------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `subscription_sharing_usage_unavailable`    | HTTP 403      | One request, then an `error` event naming the code. `AIError.retriable` is false, so the session does not retry the turn.                                                                                                                                                                                                                           | `isTransientStatus` excludes 403 (`pi-ai/src/error/retryable.ts:20-22`); `isProviderRetryableError` treats every 4xx but 408/429 as terminal (`:44-49`). |
| `subscription_sharing_usage_limit_exceeded` | HTTP 429      | Classified `Flag.UsageLimit` (the code matches `usage.?limit`, `pi-ai/src/error/rate-limit.ts:337`), so `isProviderRetryableError` is false (`retryable.ts:46`) and the session hands it to omp's usage-limit recovery (wait for a reset within `retry.maxDelayMs`, or rotate to a sibling credential). The transport still sends 6 requests first. | none reachable, see below                                                                                                                                |

The transport retry is the gap. `postOpenAIStream` sends through `fetchWithRetry` with 6 attempts (`pi-ai/src/utils/openai-http.ts:33`, `:100-117`), which retries every 429 unless the response carries a retry hint above 60 s or a proxy concurrency marker (`pi-utils/src/fetch-retry.ts:375-382`). The only caller gate, `shouldRetryResponse`, is built from omp-internal state (`openai-responses.ts:903-905`), and the `fetch` override reaches the transport only through `SimpleStreamOptions.fetch` (`pi-ai/src/types.ts:716-723`), which the session never sets for a built-in api. A `before_provider_request` hook sees only the payload, and `after_provider_response` fires only after a 2xx (`openai-responses.ts:914`, after `postOpenAIStream` has thrown on any other status). So on the built-in `openai-responses` transport no extension hook stops those 5 resends. With omp's default backoff they take about 15 s and spend nothing, because the server refuses each one. The custom-api candidate below would own the `fetch`; it is not taken, because it renames the session's `model.api` and so silently changes every omp branch keyed on `"openai-responses"` (`src/utils/tool-choice.ts:17-23`, `src/tools/think.ts:31-36`, `src/session/agent-session.ts:11043`, `:11090-11094`, `src/sdk.ts:1610-1612`). The test pins the 6 requests, so an omp release that adds a gate fails it.

## Synthesis decision

The architect skill's single-runner form was used, with the arena skipped by the brief. Two whole shapes were sketched. The base is the payload-hook shape (built-in `openai-responses` transport, compat, and a `before_provider_request` rewrite). The rejected candidate registered a custom `api` with `streamSimple`, wrapping pi-ai's `streamSimple` with its own `fetch`. It would own error mapping at the HTTP layer, but built-in api ids are reserved (`node_modules/@oh-my-pi/pi-ai/src/api-registry.ts:65-69`), so it needs a new api id and must re-target each model to `openai-responses` before delegating, which ties the extension to omp's internal model shape. U3b confirmed it is the only shape that reaches the transport's 429 retry, and kept it rejected: renaming the session's `model.api` changes more omp behaviour than five refused resends cost (Error mapping above).

## Tradeoffs accepted

- We accept depending on `before_provider_request` reaching every request in exchange for reusing omp's transport, SSE parsing, and retries unchanged. Upstream documents that transports must invoke `onPayload` and that `devin-agent` does not; `openai-responses` does.
- We accept a hand-written loopback receiver of about 40 lines in exchange for capturing the issued `client_id`, which `OAuthCallbackFlow` drops.
- We accept static model rows in exchange for no discovery call, since `GET /v1/models` returned no entries on this route.
- We accept one registration per profile, so three audit profiles mean three agent entries in the ChatGPT account (red-team R12R-06 proposed one shared record). The brief fixes the record per profile.

## Threat table

| Asset or boundary   | Threat                                                     | Control                                                                                                                                                                                                                 | Test                                                                    |
| ------------------- | ---------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------- |
| Token store         | Another local user reads access or refresh tokens.         | Tokens stay in omp's `agent.db` (dir 0700, file 0600, `sqlite-credential-store.ts:587-594`). The extension writes no token anywhere.                                                                                    | `tests/oauth.test.ts`: tokens only in returned credentials.             |
| Registration record | Tampering or a half-written file causes a re-registration. | Atomic write (temp file, rename) with 0600 file and 0700 directory; strict validation on load and save.                                                                                                                 | `tests/store.test.ts`: modes 0600 and 0700, bare uuid refused.          |
| Loopback port       | Another process holds 1455 or listens on `::1`.            | Bind `127.0.0.1` only, as the docs require; fall back to a random port, which the docs allow.                                                                                                                           | `tests/oauth.test.ts` loopback test (skipped where binding is refused). |
| Redirect validation | A forged local request injects a code (login CSRF).        | Only `GET /auth/callback`; `state` must match; a foreign state is ignored, not fatal; the first accepted callback settles the wait; PKCE S256 binds the code to this process; id_token `nonce` must match when present. | `tests/oauth.test.ts`: foreign state ignored, PKCE checked by the fake. |
| Grant scope         | An identity-only grant is used for inference.              | Login refuses a grant without `chatgpt.tokens.use.direct`.                                                                                                                                                              | `tests/oauth.test.ts`: scope refusal.                                   |
| Log redaction       | Tokens or codes reach logs or error messages.              | The extension logs nothing. Token errors carry only the OAuth `error` and `error_description`, capped at 200 characters; request bodies are never echoed. The callback page shows no parameters.                        | Review only.                                                            |
| Hosts               | Traffic leaves the two named hosts.                        | Constants only: `auth.openai.com` for authorize and token, `api.openai.com` for inference. No discovery or telemetry call.                                                                                              | `tests/fake-auth-server.ts` asserts both URLs.                          |

## Open questions and risks

- Does a later sign-in with the issued `client_id` accept `ext_agent_host_id`? Default: send it, because the sign-in page marks it required. G2's second login per profile measures it.
- Does a refresh response carry `scope`, and does the SIWC id_token carry the Codex account claim? Defaults: accept an absent scope on refresh; leave `accountId` empty when the claim is absent.
- Is `gpt-6-astra` served on this route? Assumption (【仮定】): yes. It ships as a static row next to the measured `gpt-6.1-sol`, both text-only, with the limits of omp's `openai/<id>` catalog rows. `fetchDynamicModels` is not registered, because `GET /v1/models` returned no entries (#S0).
- What HTTP status carries each subscription error? Default: rely on omp's classifier, which handles a 403 and a 429 as the table above shows.
- Should three profiles share one registration (R12R-06)? Default: one per profile, as the brief specifies.
- Are `prompt_cache_key`, `include`, `reasoning` and `stream_options` accepted? Default: keep them.

## Next step

Gate G2: the operator runs `/login openai-siwc` and one `-p` turn in each audit-side profile (`audit`, `audit-r2`, `security`), as the package README lists, which answers the first four questions.
