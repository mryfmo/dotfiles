# Architecture: dotfiles at 6bc0c2cb (scoped to unit U240, round 4)

## Product, principals and resources

This is a personal dotfiles repository. chezmoi deploys `home/`, so `home/dot_dsh/plugins/omp-gateway/` lands at `~/.dsh/plugins/omp-gateway/`.

U240 adds a DSH `LlmAdapter` plugin, `dsh-omp-gateway`. It turns a DSH model turn into one JSON line for a long-lived child process, by default `omp auth-gateway stdio`. That child holds the operator's Claude login inside omp. The plugin reads, stores and passes no credential (`index.mjs:1-11`).

The principals are:
- the operator, who writes profiles and patch rows;
- the DSH process and its other plugins;
- the model;
- the omp gateway child, a same-user process.

The protected resources are the operator's login and quota, the child's environment, and the files the proof runner and tests write.

## Changes since the U240-2256b56c sweep (2256b56c..6bc0c2cb)

Every other plugin file is byte-identical to 2256b56c.

- **5f159044 (U250): `test/use-cases.test.mjs`.** 47 automated items run against the stub or an inline scripted gateway that `process.execPath -e` starts (`:46-79`).
  - They import DSH's installed `@deepseek-ai/dsh-llm` through a `registerHooks` resolve hook. The path comes from `DSH_LLM_PACKAGE`, or from `~/.dsh/dsh/current/...` (`:29-38`). Without the package, the adapter items skip (`:148`).
  - They write only under one `mkdtemp` scratch directory (`:23`).
- **6bc0c2cb: `proof/run-proof.mjs`.**
  - A repeatable `--case` flag, allowlisted with `Object.hasOwn(CASES)` (`:123-125`).
  - Four constant cases, each with an expected-output predicate (`:21-26`). The exit code now needs every predicate to pass (`:80`).
  - A per-case model overlay with a fixed name (`:82-86`).
  - The scratch profile's patch row registers the adapter for both `claude-bridge` and `openai-siwc` (`:57`).

## Loading

DSH loads the plugin only through a profile `link:` dependency plus a patch row (`index.mjs:9-10`). `git grep omp-gateway` outside the plugin directory finds nothing, so no profile in the repository loads it at this head. The only loader is the proof's scratch profile (`proof/run-proof.mjs:43-59`).

## Entry surfaces and paths, with lines at this head

1. **Config to spawn.** `config.mjs:25-50` → `index.mjs:68-79` → `gateway-client.mjs:132`. No shell; environment allowlist at `:26-33`, default names at `config.mjs:4-7`.
2. **Request line.** `toMessagesBody` (`translate.mjs:18-60`), with the `<dsh-system>` fold (`:185-190`), → one `JSON.stringify` line (`gateway-client.mjs:107`).
3. **Replies.** `readline` (`:177-179`) → `#onLine` (`:183-212`): ready gate, ID correlation, kill on violation.
4. **Chunks.** `toChunks` (`translate.mjs:68-103`) and `toError` (`:111-120`).
5. **Lifecycle.** `gateway-client.mjs:78-128`, `:130-181`, `:219-240`.
6. **Error text.** `:168`, `:189`, `:242-245`; `index.mjs:49`, `:53`.
7. **Proof runner.** `proof/run-proof.mjs:28-105`, flags at `:111-129`.
8. **Stub, fixtures, tests.**
   - `stub-gateway.mjs` logs to `--log` or stderr.
   - The tests write under `mkdtemp`.
   - `use-cases.test.mjs` resolves DSH's llm package from the environment or `~/.dsh`.

## Trust boundaries and strongest controls

- **Profile author to child.** Same principal. Argv spawn without a shell, an environment allowlist, and validated config rows.
- **Plugin to child.** Private pipes, increasing IDs, strict correlation, and kill on violation. The child is forgotten before it is killed, and the handlers are identity-guarded.
- **System text to model.** The block is built only from system sources. No `system` field is sent, so the block carries user-turn provenance and a forged block gains nothing. Pinned by `test/translate.test.mjs` and U250 item c5.
- **Model output to tool calls.** Translated only. DSH's loop owns dispatch.
- **Test process to DSH's install.** The operator's own environment variable or installed tree, imported into the operator's test run.
- **Proof selectors.** A constant case table. The extra route lives only in the proof's scratch profile.

## Prior coverage

No earlier run of this seat exists. The U240-2256b56c sweep records (dotfiles-run-5, from the store) are carried:
- **Covered units.** Its seven same-source covered units are re-checked as `prior_covered_same_source`. The proof-runner and stub/fixtures/tests units are `prior_covered_changed_source`, with their lines re-mapped.
- **New units.** Two: the test's dsh-llm resolution, and the proof's cases and provider routes.
- **Out of scope.** Its 24 out-of-scope units carry over.
- **Findings.** It holds no finding of any verdict.

## Companion selection

The same four companions as the carried run, each because the plugin crosses the named boundary:
- `DESKTOP-MOBILE-AND-LOCAL-IPC.md`: the child process and its pipes, and local files.
- `PROTOCOLS-RPC-AND-MESSAGING.md`: JSON-line framing and correlation.
- `AI-AND-LLM.md`: system-text provenance and tool calls.
- `SUPPLY-CHAIN-AND-RELEASE.md`: plugin loading, and the test's package resolution.

Each unit records its exclusions.

## Execution and independence limits

No target code runs, by task rule, so every check is a source check. The delegation tool (Task) and the eval kernel are denied by policy on this seat. Reconnaissance, the hunter wave and both critics therefore ran in the parent, with agent ID `parent-hunter`.
