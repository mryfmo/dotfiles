# openai-siwc

omp provider extension for OpenAI's official Sign in with ChatGPT route. It registers the provider `openai-siwc` on omp's built-in `openai-responses` transport, logs in through dynamic client registration with a `127.0.0.1` loopback callback, and rewrites each request into the shape the SIWC preview accepts. The design, strip list and threat table are in `docs/openai-siwc.md` at the repository root.

Status: skeleton. The points that need a real-endpoint measurement carry `TODO(unit U3b)`.

## Operator steps

Each omp profile that uses this provider needs one interactive login in the operator's own terminal. The login opens the system browser, so an agent never runs it.

| Step                                                                       | source                                                                                                                                | dry-run                                                                                            |
| -------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| Start omp on the profile with the extension loaded                         | `src/extensibility/extensions/directory-resolution.ts:5-9` in omp 18.11.3 resolves `-e <dir>` through `package.json` `omp.extensions` | operator-only: the worktree guard refuses a scratch `HOME` for agents, so the load was not dry-run |
| Run `/login openai-siwc`, then name and authorize the agent in the browser | `src/config/model-registry.ts:3479` registers the `oauth` block for `/login`; the flow is `src/oauth.ts` `createSiwcOAuth().login`    | operator-only: needs a browser login; `tests/oauth.test.ts` runs the flow against a fake server    |
| Select the model with `/model openai-siwc/gpt-6.1-sol`                     | `src/index.ts` `MODELS`                                                                                                               | operator-only: needs the login above                                                               |

The first login per profile creates `<agentDir>/openai-siwc/registration.json` (mode 0600) with the host id and the issued `client_id`, and adds one agent entry to the ChatGPT account. Later logins reuse that `client_id`. Tokens are stored by omp in `<agentDir>/agent.db`.

## Tests

```sh
bun test
```

`tests/requests.test.ts` imports omp's own Responses transport from the installed omp package to prove the rewritten request end to end. It reads `OMP_PACKAGE_DIR`, defaulting to `~/.local/lib/node_modules/@oh-my-pi/pi-coding-agent`.

The loopback bind test is skipped, with a printed reason, where the sandbox refuses binding `127.0.0.1`.
