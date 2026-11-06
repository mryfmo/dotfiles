# Architecture: dotfiles at 6531a212 (scoped to unit U240, round 2)

## Product, principals and resources

A personal dotfiles repository. chezmoi deploys `home/` into the operator's `~`, so `home/dot_dsh/plugins/omp-gateway/` lands at `~/.dsh/plugins/omp-gateway/`.

U240 adds a DSH `LlmAdapter` plugin, `dsh-omp-gateway`. It turns a DSH model turn into one JSON line for a long-lived child process, by default `omp auth-gateway stdio`. That child holds the operator's Claude login inside omp. The plugin reads, stores and passes no credential (`index.mjs:1-11`).

The principals are:
- the operator, who writes DSH profiles and patch rows;
- the DSH process and its other plugins, in one Node process;
- the model, whose replies come back as text, reasoning and tool calls;
- the omp gateway child, a same-user process.

The protected resources are the operator's Claude login and quota, the environment handed to the child, and the files the proof runner writes.

## Round 2 (U240b, dc336b67..6531a212)

**System text.** `toMessagesBody` no longer sends a `system` field (`translate.mjs:49`). It collects `options.system` (`:20`) and system-role rows (`:24-28`) and `foldSystem` (`:180-185`) prepends them to the first user turn as one text block, `<dsh-system>\n...\n</dsh-system>`. When the history starts with an assistant turn, it inserts a user message holding the block alone instead.

The reason, from the code comment at `:173-179`: the gateway's pi-claude-bridge runs a request that has no `system` field on Claude Code's preset prompt, and throws on a `system` field it does not recognise. So DSH's instructions now travel as user-turn text.

**Other changes.**
- `SYSTEM_BLOCK_TAG` (`:10`) is used only by the writer and the test. No code reads the tag.
- `run-proof.mjs` and `stub-gateway.mjs` each lose their shebang line, so their line numbers shift down by one.
- `test/translate.test.mjs` gains four fold tests (`:62-127`).

## Loading

DSH loads the plugin only through a profile `package.json` `link:` dependency plus a patch row (`index.mjs:9-10`). At this head no profile in the repository references it. The only loader is the proof runner's scratch profile (`proof/run-proof.mjs:31-46`).

## Entry surfaces and paths

1. **Config to spawn.** `config.mjs:25-50` → `apply` (`index.mjs:68-79`) → `spawn(command, args, {cwd, env, stdio: pipes})` (`gateway-client.mjs:132`). There is no shell. `env` is the allowlist `pickEnv` (`:26-33`; defaults at `config.mjs:4-7`).
2. **Request to the request line.** `toMessagesBody` (`translate.mjs:18-60`) builds the body, including the `<dsh-system>` block, which is written as one `JSON.stringify` line (`gateway-client.mjs:107`).
3. **Child stdout to replies.** `readline` (`:177-179`) → `#onLine` (`:183-212`): a ready gate, then integer IDs matched to pending requests, and any protocol failure kills the child.
4. **Reply to DSH chunks.** `toChunks` (`translate.mjs:68-98`) and `toError` (`:106-115`).
5. **Lifecycle.** Abort, ready timeout, exit and close (`gateway-client.mjs:80-128`, `:143-170`, `:219-228`).
6. **Error text.** The stderr tail and the unparseable-line prefix reach `LlmError` (`:168`, `:189`; `index.mjs:49`).
7. **Proof runner.** Writes under `mkdtemp`, or under the operator's `--home` (`proof/run-proof.mjs:18-46`, `:63-65`, `:74-77`).
8. **Stub, fixtures and tests.** These write only under `mkdtemp` scratch.

## Trust boundaries and strongest controls

- **Profile author to child.** Same principal. Controls: argv spawn without a shell, an environment allowlist, and config row validation.
- **Plugin to child (stdio).** Private pipes, monotonically increasing IDs, strict correlation, and the child is killed on any protocol violation.
- **System text to model.** The `<dsh-system>` block is a separate text block built from system sources only, so user text blocks cannot enter or close it. With no `system` field, the block carries user-turn provenance, so a forged block gains nothing that user text lacks. No deterministic control reads the tag.
- **Model output to tool calls.** Translated only. Dispatch, approval and sandboxing belong to DSH, outside the target.

## Prior coverage

run-2 (`~/.local/state/omp-seats/dotfiles/.state/sweep-2/security-audit/run-2`, source dc336b67) is carried. Its eight covered units are re-checked here with re-mapped lines. Five read files that round 2 changed (`prior_covered_changed_source`), and three did not (`prior_covered_same_source`). Its 19 out-of-scope units carry as `prior_out_of_scope`. run-2 holds no finding of any verdict.

## Companion selection

Selected:
- `DESKTOP-MOBILE-AND-LOCAL-IPC.md`: the credential-holding local child over stdio.
- `PROTOCOLS-RPC-AND-MESSAGING.md`: the JSON-line protocol and reply correlation.
- `AI-AND-LLM.md`: tool-call translation, plus the new role and provenance question of the `<dsh-system>` block.
- `SUPPLY-CHAIN-AND-RELEASE.md`: plugin loading.

## Execution and independence limits of this run

No target code ran, by task rule. The platform's delegation tool (Task) and eval kernel are denied by policy on this seat, so reconnaissance, hunting and both critic passes ran in the parent. `run-metadata.json` records the run as incomplete for that reason.
