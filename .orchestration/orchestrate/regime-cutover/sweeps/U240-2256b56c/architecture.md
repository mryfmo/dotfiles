# Architecture: dotfiles at 2256b56c (scoped to unit U240, round 3)

## Product, principals and resources

A personal dotfiles repository. chezmoi deploys `home/`, so `home/dot_dsh/plugins/omp-gateway/` lands at `~/.dsh/plugins/omp-gateway/`.

U240 adds a DSH `LlmAdapter` plugin, `dsh-omp-gateway`. It turns a DSH model turn into one JSON line for a long-lived child, by default `omp auth-gateway stdio`. That child holds the operator's Claude login inside omp. The plugin reads, stores and passes no credential (`index.mjs:1-11`).

The principals are:
- the operator, who writes profiles and patch rows;
- the DSH process and its other plugins;
- the model;
- the omp gateway child, a same-user process.

The protected resources are the operator's Claude login and quota, the child's environment, and the proof runner's files.

## Changes since the run-3 sweep (6531a212..2256b56c)

- **aa788c82, `proof/run-proof.mjs:44`.** The proof's patch row drops its `env: ['HOME', 'PATH']` override, so the gateway child gets the plugin's default allowlist (`config.mjs:4-7`: HOME, PATH, USER, LOGNAME, SHELL, LANG, LC_ALL, TERM, TMPDIR, XDG dirs). None of those is a credential variable.
- **2256b56c, `gateway-client.mjs:226-233`.** `#kill` now forgets the child before sending SIGTERM. A request in the window before the old child's `close` event therefore spawns a fresh child instead of being written to the dying one.
  - Every `#kill` runs after a `#fail` that has already rejected the pending requests and the gate, which clears the ready timer (`:155-158`).
  - The old child's `error`, `close` and stdout handlers check that the child is still current (`:161`, `:167`, `:178`).
  - The stderr handler (`:174-176`) does not check.
- **2256b56c, `translate.mjs:72-76`.** A 200 reply with an empty content array throws `EMPTY_RESPONSE`.
- **2256b56c, tests.** Forged-tag tests (`test/translate.test.mjs:129-153`); failure-injection tests with in-process fake children for respawn after abort, respawn after a protocol failure, and a reply before the ready line (`test/gateway-client.test.mjs:53-86`, `:142-203`); an `EMPTY_RESPONSE` test (`test/translate.test.mjs:201-207`).

## Loading

DSH loads the plugin only through a profile `link:` dependency plus a patch row (`index.mjs:9-10`). No profile in the repository loads it at this head; the only loader is the proof's scratch profile.

## Entry surfaces and paths, with lines at this head

1. **Config to spawn.** `config.mjs:25-50` → `index.mjs:68-79` → `gateway-client.mjs:132`. No shell; environment allowlist at `:26-33`.
2. **Request line.** `toMessagesBody` (`translate.mjs:18-60`), with `<dsh-system>` fold (`:185-190`), → one `JSON.stringify` line (`gateway-client.mjs:107`).
3. **Replies.** `readline` (`:177-179`) → `#onLine` (`:183-212`): ready gate, ID correlation, kill on violation.
4. **Chunks.** `toChunks` (`translate.mjs:68-103`) and `toError` (`:111-120`).
5. **Lifecycle.** `gateway-client.mjs:80-128`, `:143-170`, `:219-240`.
6. **Error text.** `:168`, `:189`, `:242-245`; `index.mjs:49`.
7. **Proof runner.** `proof/run-proof.mjs:18-46`, `:63-65`, `:74-77`.
8. **Stub, fixtures, tests.** These write only under `mkdtemp`, or use in-process fakes.

## Trust boundaries and strongest controls

- **Profile author to child.** Same principal. Argv spawn without a shell, an environment allowlist, and validated config rows.
- **Plugin to child.** Private pipes, monotonically increasing IDs, strict correlation, kill on violation, and (since round 3) forget-before-kill with identity-guarded handlers.
- **System text to model.** The block is built only from system sources. With no `system` field, it carries user-turn provenance, so a forged block gains nothing; the round-3 tests pin that.
- **Model output to tool calls.** Translated only.

## Prior coverage

run-4 (`~/.local/state/omp-seats/dotfiles/.state/sweep-2/security-audit/run-4`, source effff558) swept U249, which is absent here. Its five brief-check units carry as changed-source, out-of-scope units. run-4 held the nine U240 units out of scope (carried from run-3), and they are re-checked here. Its other 19 out-of-scope units carry. No prior run holds any finding.

## Companion selection

The same as run-3:
- `DESKTOP-MOBILE-AND-LOCAL-IPC.md`
- `PROTOCOLS-RPC-AND-MESSAGING.md`
- `AI-AND-LLM.md`
- `SUPPLY-CHAIN-AND-RELEASE.md`

Each unit records its exclusions.

## Execution and independence limits of this run

No target code ran, by task rule. The delegation tool (Task) and eval kernel are denied by policy on this seat, so every phase ran in the parent. `run-metadata.json` records the run as incomplete for that reason.
