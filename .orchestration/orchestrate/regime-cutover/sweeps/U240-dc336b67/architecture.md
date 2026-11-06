# Architecture: dotfiles at dc336b67 (scoped to unit U240)

## Product, principals and resources

A personal dotfiles repository. chezmoi deploys `home/` into the operator's `~`, so `home/dot_dsh/plugins/omp-gateway/` lands at `~/.dsh/plugins/omp-gateway/` on every host. Nothing in `home/.chezmoiignore` excludes it.

U240 adds a DSH (DeepSeek harness) `LlmAdapter` plugin, `dsh-omp-gateway`. It turns a DSH model turn into one JSON line for a long-lived child process, by default `omp auth-gateway stdio`. That child holds the operator's Claude login inside omp. The plugin reads, stores and passes no credential (`index.mjs:1-11`).

The principals are:
- the operator, who writes DSH profiles and patch rows and owns `~`;
- the DSH process and its other plugins, which share one Node process with the adapter;
- the model, whose replies come back as text, reasoning and tool calls;
- the omp gateway child, a same-user process.

The protected resources are the operator's Claude login and quota (inside omp), the environment handed to the child, and the files the proof runner writes.

## Loading

DSH loads the plugin only through a profile `package.json` dependency (`link:`) plus a patch row `name: dsh-omp-gateway` (`index.mjs:9-10`). I read the installed upstream tree as context: it shows no automatic loading from `DSH_HOME/plugins`.

At this head no profile in the repository references the plugin. A repository-wide search for `omp-gateway` finds only the plugin's own files. The only loader is the proof runner's scratch profile (`proof/run-proof.mjs:32-47`).

## Comparable baseline

The gateway pattern resembles a credential-holding local helper (an ssh-agent-like process) that answers a same-user client over private pipes. That pattern's boundary is the OS user. A same-user client with the pipe has the helper's authority by design.

## Stack and limits

Plain ESM for Node 22+, with node:test tests (`package.json:6-20`). A peer dependency on `@deepseek-ai/dsh-llm` is provided by the DSH host. No build step and no dependency fetch.

No target code ran, by task rule. Every check is a source check.

## Entry surfaces and paths

1. **Patch-row config to spawn.** The config row (`command`, `args`, `env` names, `cwd`, `providers`, `models`, `maxTokens`, `readyTimeoutMs`; `config.mjs:25-50`) flows through `apply` (`index.mjs:68-79`) to `GatewayClient` and `spawn(command, args, {cwd, env, stdio: pipes})` (`gateway-client.mjs:132`). There is no shell. `env` is the allowlist `pickEnv` (`:26-33`; defaults at `config.mjs:4-7`). `cwd` defaults to `homedir()`.
2. **DSH request to the request line.** `toMessagesBody` (`translate.mjs:12-54`) builds the body, which is written as `JSON.stringify({id, path, body})` plus a newline (`gateway-client.mjs:107`). `path` is the constant `/v1/messages` (`index.mjs:47`).
3. **Child stdout to replies.** `readline` delivers lines (`:177-179`) to `#onLine` (`:183-212`): a JSON object, a ready gate first, then an integer `id` and `status` matched to a pending entry. Any violation is a protocol failure that kills the child.
4. **Reply to DSH chunks.** `toChunks` (`translate.mjs:62-92`) yields text, reasoning and tool-call blocks; tool arguments are `JSON.stringify(input)`. `toError` (`:100-109`) maps non-200 replies.
5. **Lifecycle.** Abort kills the child and rejects every pending request (`:91-94`, `:219-224`). A ready timeout (`:143-147`), child `close` (`:166-170`) and stdin EOF on `close()` (`:121-128`) end it.
6. **Error text.** Errors can carry the child's stderr tail of up to 4096 bytes (`:9`, `:174-176`, `:168`, `:237-240`) and the first 200 characters of an unparseable stdout line (`:189`). These reach `LlmError` (`index.mjs:49`).
7. **Proof runner.** By default it works in a scratch `DSH_HOME` from `mkdtemp` (`run-proof.mjs:19`), or in `--home`. Under that directory it writes the profile, the patch, `stub.log` and the turn transcripts (`:27-47`, `:64-66`), with symlinks via `link()` (`:75-78`). Its scratch profile disables `bash-sandbox` and session-log upload (`:42-43`). The gateway child gets only `HOME` and `PATH` (`:45`); `dsh` gets the full environment plus `DSH_HOME` (`:64`).
8. **Test fixtures.** The stub gateway, fixtures and node tests write only under `mkdtemp` scratch (`test/gateway-client.test.mjs:12`).

## Trust boundaries and strongest controls

- **Profile author to child process.** Same principal (the operator). Controls: argv spawn without a shell, an environment allowlist, and refusal of malformed rows (`config.mjs:52-72`).
- **Plugin to gateway child (stdio).** The pipes are private to the spawned child; peer identity is the spawn itself. Request IDs increase monotonically, and each reply must match an outstanding ID or the child is killed.
- **Model output to DSH tool calls.** The adapter only translates. Tool dispatch, approval and sandboxing belong to DSH, outside this diff.
- **Child output to error messages.** Bounded tails; whether they ever hold secrets depends on omp, which is outside the target.

## Prior coverage

run-1 (`~/.local/state/omp-seats/dotfiles/.state/sweep-2/security-audit/run-1`, source 0b475694) swept U226. This head descends from d1ecd495, which does not contain U226. So run-1's six covered units carry as changed-source, out-of-scope units, and its 13 out-of-scope units stay out of scope. run-1 has no finding of any verdict.

## Companion selection

Selected:
- `DESKTOP-MOBILE-AND-LOCAL-IPC.md`: the child is a local credential-holding helper reached over stdio.
- `PROTOCOLS-RPC-AND-MESSAGING.md`: a custom JSON-line protocol with reply correlation.
- `AI-AND-LLM.md`: model replies become DSH tool calls.
- `SUPPLY-CHAIN-AND-RELEASE.md`: the plugin is loaded into DSH through a profile.

Each unit records its excluded blocks with reasons.

## Execution and independence limits of this run

The platform's delegation tool (Task) and eval kernel are denied by policy on this seat. Reconnaissance, hunting and both coverage-critic passes ran in the parent, and no fresh independent agent ran. `run-metadata.json` records the run as incomplete for that reason.
