---
task_id: dotfiles-T129-anthropic-auth-runtime-check-a01
round: 1
status: pushed-pr-not-opened
---

# Report

Worker `claude-standard-dot-a009` (Claude Code, worker-c worktree), branch `tools/anthropic-auth-runtime-check` from `origin/main` a8a747af, code commit 8cb93567. Task copy `.orchestration/dotfiles-T129-anthropic-auth-runtime-check-a01/task.md` is byte-identical to the dispatched file: sha256 `92fe88b948b753ef5b84502ea157c2c9193c8183fb221d95e4412a464290e52a`, the TASK line's `task_sha256`.

## What changed

- `scripts/check-tools.sh` (+34/-0): `check_anthropic_auth_route()` after `check_hcom`, with a shdoc block, called from `main` right after `check_hcom` in the "Agent tools" section. Rule (E): `${ANTHROPIC_OAUTH_TOKEN+set}` (an empty value counts) is a required failure, otherwise `found:   ANTHROPIC_OAUTH_TOKEN -> unset`. Rule (S): store `"${PI_CODING_AGENT_DIR:-${HOME%/}/.omp/agent}/agent.db"`; absent (`[ ! -e ]`) is `not applicable` and returns 0; present runs one `sqlite3 -readonly` count of `auth_credentials` rows with `provider='anthropic' and credential_type='oauth'`, stderr discarded, `|| n=` keeping `set -Eeuo pipefail`; a result that is not all digits is a required failure ("could not be verified"), 0 is `found:`, above 0 is a required failure naming the count and the path. Both rules always run. Nothing prints a value, a row or the query's output beyond the count.
- `tests/install/common/check_tools.bats` (+38/-0): the `@test` the threat table names, five runs in the module's `run env -u ANTHROPIC_OAUTH_TOKEN -u PI_CODING_AGENT_DIR HOME=... bash -c 'source "$1"; ...' bash "${SCRIPT_PATH}"` form, each asserting `required_failures`, the expected line, and that `never-printed` is absent from the merged output. The thirteen existing `@test` blocks are unchanged (the diff only adds lines after the last one).
- `tests/unit/test_runtime_health.py` (+1/-1): `doctor_environment` spreads `os.environ` without `ANTHROPIC_OAUTH_TOKEN` and `PI_CODING_AGENT_DIR`; nothing else in the module changed.

Caps: 34 changed lines in the script (cap 60), 38 in the bats module (cap 120), 2 in the unit module (cap 10); 34 outside `tests/` and `.orchestration/` (standing 200), 39 added under `tests/` (1000).

## Two choices the task text left open

- Run order in the bats case is (a), (b), (e), then the `command -v sqlite3 || skip` guard, then (c) and (d). Run (e) needs no `sqlite3` (without it the store is unverifiable too, which the local probe's "no sqlite3 on PATH" case shows), and a bats `skip` ends the whole `@test`, so placing (e) after the guard would drop it on a runner without `sqlite3`.
- Run (d) uses the same store path, emptied and refilled with an `openai-codex` `oauth` row and an `anthropic` `api_key` row, reached through `PI_CODING_AGENT_DIR` with an empty HOME. `openai-codex` is omp's OpenAI OAuth provider id in the pinned tree (`packages/ai/src/registry/oauth/index.ts`: "login aliases (`openai-codex-device`) map to their target (`openai-codex`)").

## VERIFY

- VERIFY 1 (closed by the orchestrator): no contradiction. WebFetch of `https://raw.githubusercontent.com/can1357/oh-my-pi/v18.11.3/packages/ai/src/auth/sqlite-credential-store.ts` returned the opening `CREATE TABLE IF NOT EXISTS auth_credentials (` and the columns `id`, `provider`, `credential_type`, `data`, `disabled_cause`, `identity_key`, `created_at`, `updated_at` (the tool quotes at most 125 characters, so the full statement came back as a column list), `credentialType: "api_key",` and `credentialType: "oauth",` in `serializeCredential`, and `import type { Provider } from "../types";`.
- VERIFY 1b (worker): the literal is `anthropic`; no file under `packages/ai/src/` defines it. The chain at tag v18.11.3, each step a WebFetch of a raw GitHub path:
  - `packages/ai/src/types.ts` does not define `Provider`: `import type { Api, FetchImpl, KnownApi, Model, Provider, ThinkingBudgets, Usage } from "@oh-my-pi/pi-catalog/types";`. It compares the literal: `if (model.provider === "anthropic") return true;`.
  - `packages/ai/src/registry/oauth/index.ts` stores an OAuth login under `return getOAuthProviders().find(provider => provider.id === providerId)?.storeCredentialsAs ?? providerId;`, its ids from `PROVIDER_REGISTRY`, which `packages/ai/src/registry/registry.ts` builds as `export const PROVIDER_REGISTRY: readonly ProviderDefinition[] = authProviders().map(policy =>` from `import { authProviders } from "@oh-my-pi/pi-catalog/compat/auth";`, outside `packages/ai/src/`.
  - The two uses under `packages/ai/src/` that tie the literal to Anthropic credentials: `packages/ai/src/auth-storage.ts` line ` * const apiKey = await auth.keys.get("anthropic", sessionId, { modelId });`, and `packages/ai/src/registry/oauth/anthropic.ts`, the Anthropic OAuth module, tagging its errors `provider: "anthropic",` (inside `throw new AIError.OAuthError(` for the bootstrap response).
  - Not read: `@oh-my-pi/pi-catalog` (`compat/auth`), where `authProviders()` and any `storeCredentialsAs` for Anthropic are defined; the task limits the lookup to `packages/ai/src/`. Residual: if the catalog's Anthropic login stored under another id, the count would read 0 and the check would print `found:`; nothing read under `packages/ai/src/` points that way. Not read either: the npm tarball, `curl`, the live `~/.omp` database.
- VERIFY 2: default applied, `PI_CODING_AGENT_DIR` replaces `~/.omp/agent` (store `"${PI_CODING_AGENT_DIR}/agent.db"`); run (d) pins it.
- VERIFY 3: default applied, the hint names no command ("remove the Anthropic login in omp").
- VERIFY 4: still open. On this Mac `~/.local/bin/omp` is a symlink to `~/Library/Application Support/Tern/omp/bin/omp` and is not executable (dangling), so omp was not run; the sqlite3 query stands.
- VERIFY 5: informational; CI's bats log will show whether runs (c) and (d) ran or skipped on `ubuntu-latest`, and the RESULT says which.

## Validation

`validation.md`: `make render-check`, `shellcheck -x scripts/check-tools.sh`, `shfmt --indent 4 --space-redirects --diff scripts/check-tools.sh` and `ruff format --check` exit 0. The full `tests/unit/test_runtime_health.py` run fails 8 of 55, all `test_agmsg_*` installer tests outside this diff, failing on the sandbox's denial of the system temp directory, and the same 8 fail identically on `origin/main` a8a747af; the doctor fixture test passes, also with both variables exported. A plain-bash probe (not bats) runs the five task runs plus an empty token value, no `sqlite3` on PATH and a foreign schema: every case returns the expected `required_failures` and none prints the fixture secret.

## Not done yet

- The PR. Under the night's ask rules every `gh` write prompts a human, so the branch is pushed and the worker stops at `gh pr create --draft --head tools/anthropic-auth-runtime-check` with `AGMSG-PONG v1 status=blocked`.
- The rebase onto `origin/main` after #394 and #398 merge, CI (bats, Python unit tests), the Bot wait and the RESULT. Bats is CI-only.
- The CompactionDB `memory add` of the decision below, at RESULT time.

[memory:decision] check-tools.sh refuses the Anthropic OAuth route at run time: `ANTHROPIC_OAUTH_TOKEN` set, or an `auth_credentials` row with `provider='anthropic'` and `credential_type='oauth'` in omp's store at `${PI_CODING_AGENT_DIR:-~/.omp/agent}/agent.db`, read with `sqlite3 -readonly`; a store that exists but cannot be read is a required failure, never a pass.

effects=none. AutoSkill not used. Understand-Anything hook: not fired in this session. Plan Mode not used. cost: n/a
