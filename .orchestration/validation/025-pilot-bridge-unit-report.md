# U1 pilot-bridge unit report (2026-10-23, JST 10:08-10:3x)

Status: **done, bridge does not load yet; exact gap and exact operator point measured.** Every omp run below used `HOME=/tmp/claude-501/u1-home`, `perl -e 'alarm 120; exec @ARGV'`, and `2>&1 | tee /tmp/claude-501/u1-home/run-<n>-<label>.log` through the runner `/tmp/claude-501/u1-work/run-form.sh`, which also prints the `Failed to load extension` lines omp wrote to the scratch `~/.omp/logs/omp.<date>.<pid>.log`. The real `~/.omp`, `~/.claude`, the Keychain and the patch file were not touched. Package copies: `/tmp/claude-501/u1-work/pkg-nm` (patched1 + a clone of the hoisted deps as `node_modules`, 484M), `pkg-bare` (patched1 alone), `pkg-probe` (pkg-nm with one scratch-only stub, see §4).

## 1. Instrument

- **Works: the session path.** `omp [--profile X] [-e <path>] --no-session --model claude-bridge/<id> -p "..."` prints `Failed to load extension <path>: <error>` on stderr (`src/extensibility/extensions/load-errors.ts:5-13`, called from `src/main.ts:2378`; the text is truncated to a display width) and writes the full error to `~/.omp/logs/omp.<date>.<pid>.log` (`src/sdk.ts:1102`, `:2727`, `:2735` `logger.error("Failed to load extension", { path, error })`; file level `OMP_LOG_LEVEL`, default `debug`, `node_modules/@oh-my-pi/pi-utils/src/logger.ts:322-329`). A load that succeeds leaves no line, and the run then continues to model resolution.
- **Does not work: `omp models`.** `src/cli/models-cli.ts:354-356` does contain `process.stderr.write("Failed to load extension: ...")`, so the pilot-facts reading "`commands/models.ts` does not print them" was wrong at the file level, but measured: a probe extension whose first line appends to a file and writes to stderr is **never evaluated** under `omp models -e <file>` nor `--extension <file>` (runs 16, 17, 28, 31: no marker on stderr, no marker file), while the same file is evaluated in a session (runs 18, 29: `probe-ext: module evaluated`, `factory ran`, `registerProvider returned`). The cause inside omp was not traced (follow-up F2). Pasted, run 28 then 29:

```
### run-28 probe-models-filemarker: omp --no-extensions -e /tmp/claude-501/u1-work/probe-ext.ts models probe-provider
No models available. Set API keys in environment variables.
exit=0
probe file:
cat: /tmp/claude-501/u1-home/run-28-probe-out.txt: No such file or directory
### run-29 probe-session-filemarker: omp --no-extensions -e /tmp/claude-501/u1-work/probe-ext.ts --no-session --model probe-provider/probe-model --max-time 30 -p hi
probe-ext: module evaluated
probe-ext: factory ran
probe-ext: registerProvider returned
Working...
Deadline exceeded
exit=0
probe file:
probe-ext: module evaluated
```

- The text listing also masks: `models-cli.ts:244-246` prints `No models available. Set API keys in environment variables.` whenever `getAvailable()` is empty, and `:247-249` prints `No models matching "<pattern>"` otherwise. `omp extensions` does not exist in 18.11.3 (`omp --help` COMMANDS list, run-00 log); `omp plugin doctor` checks only the store's presence (run 04).

## 2. Loading forms (session path, `--model claude-bridge/claude-haiku-4-5 -p "Reply with the single word PONG."`)

| form | command (under scratch HOME) | entry omp resolved | result (stderr + omp log) | run |
| --- | --- | --- | --- | --- |
| (a) default-profile store | `omp install /tmp/claude-501/u1-work/pkg-nm --json` then `omp --no-session --model ... -p ...` | symlink `~/.omp/plugins/node_modules/pi-claude-bridge -> /tmp/claude-501/u1-work/pkg-nm` (`/bin/ls -la`), lock `~/.omp/plugins/omp-plugins.lock.json` lists it; loaded `~/.omp/plugins/node_modules/pi-claude-bridge/src/index.ts` | `Export named 'contentText' not found in module 'omp-legacy-pi-bundled:@oh-my-pi/pi-ai'.` | 23, 24 |
| (b) profile store | `omp --profile pilot-bridge install /tmp/claude-501/u1-work/pkg-nm --json` then `omp --profile pilot-bridge --no-session --model ... -p ...` | symlink under `~/.omp/profiles/pilot-bridge/plugins/node_modules/pi-claude-bridge` (`find` output); loaded from that path | same `contentText` error | 25, 26 |
| (c) `-e <package dir with node_modules>` | `omp --no-extensions -e /tmp/claude-501/u1-work/pkg-nm --no-session --model ... -p ...` | `pkg-nm/src/index.ts` via `pi.extensions` (manifest-first, `src/extensibility/extensions/directory-resolution.ts:5-9`) | same `contentText` error | 20 |
| (c') `-e <package dir without node_modules>` | `... -e /tmp/claude-501/u1-work/pkg-bare ...` | `pkg-bare/src/index.ts` | `Cannot find package '@anthropic-ai/claude-agent-sdk' imported from /private/tmp/claude-501/u1-work/pkg-bare/src/index.ts?mtime=...` | 21 |
| (d) `-e <package dir>/src/index.ts` | `... -e /tmp/claude-501/u1-work/pkg-nm/src/index.ts ...` | the file | same `contentText` error | 27 |
| (e) `~/.omp/agent/extensions/<copy>` | `cp -Rc pkg-nm ~/.omp/agent/extensions/pi-claude-bridge` then `omp --no-session --model ... -p ...` | `~/.omp/agent/extensions/pi-claude-bridge/src/index.ts` (found by the `*/package.json` glob, `src/discovery/helpers.ts:845-853`) | same `contentText` error | 22 |
| probe: (c) with `contentText` stubbed | `... -e /tmp/claude-501/u1-work/pkg-probe ...` | `pkg-probe/src/index.ts` | **loads**; `Working...` then `Not logged in · Please run /login` | 30 |

Pasted, run 20 and run 30:

```
### run-20 c-session-dryrun: omp --no-extensions -e /tmp/claude-501/u1-work/pkg-nm --no-session --model claude-bridge/claude-haiku-4-5 --max-time 90 -p Reply with the single word PONG.
Failed to load extension /tmp/claude-501/u1-work/pkg-nm/src/index.ts: Failed to load extension: Export named 'contentText' not found in module 'omp-legacy-pi-bundled:@oh…
Model "claude-bridge/claude-haiku-4-5" not found
exit=0
omp-log: {"timestamp":"2026-10-23T10:19:12.208+09:00","level":"error","pid":94255,"message":"Failed to load extension","path":"/tmp/claude-501/u1-work/pkg-nm/src/index.ts","error":"Failed to load extension: Export named 'contentText' not found in module 'omp-legacy-pi-bundled:@oh-my-pi/pi-ai'."}
### run-30 next-gap-after-contentText: omp --no-extensions -e /tmp/claude-501/u1-work/pkg-probe --no-session --model claude-bridge/claude-haiku-4-5 --max-time 60 -p Reply with the single word PONG.
Working...
Not logged in · Please run /login
exit=0
```

Every form resolves the same entry and reaches the same import, so the loading form is not the blocker. Two facts decide a form: dependencies resolve by walking `node_modules` upward from the **realpath** of the entry (`src/extensibility/plugins/legacy-pi-compat.ts:1518-1534`; `docs/extension-loading.md` "the entry's realpath is resolved"), and `omp install <dir>` is `plugin link`, a symlink, not a copy (`src/commands/install.ts:15-18, 76-82`; `src/extensibility/plugins/manager.ts:863-895`). The install printed five denied `registry.npmjs.org` connections and still succeeded (runs 23, 25 sandbox block), so linking does not need the registry when the package carries its own `node_modules`.

## 3. Root cause of `No models matching "claude-bridge"` (#B3, #B3b)

1. `omp models` never evaluates extension modules in this build (§1, runs 16/17/28/31 vs 18/29). No loading form can make the bridge appear in `omp models`; the listing was the wrong instrument. Measured.
2. Independently, the patched bridge fails to load in a session: `transcript.ts:14` imports `contentText` from `@earendil-works/pi-ai`, the omp legacy pi-ai shim's runtime export list (341 names, dumped with `bun -e "import * as m from './src/extensibility/legacy-pi-ai-shim.ts'"` into `/tmp/claude-501/u1-work/exports-pi-ai.txt`) lacks it, and `@oh-my-pi/pi-ai` has only `messageContentText` at `src/dialect/rendering.ts:221-231`, not exported at the root. The B1 fix round's grep missed it because the import spans lines. Measured (runs 20-27).
3. For #B3 (`--profile pilot-bridge` with the plugin in the default store): a profile reads its own `~/.omp/profiles/<name>/plugins` store (runs 25/26), so the default-store install is invisible there, as pilot-facts said. Measured.
4. The real store entry `~/.omp/plugins/node_modules/pi-claude-bridge` is a symlink to `/tmp/claude-501/pcb-patched1/package` (`/bin/ls -la`, created 09:32), a directory without `node_modules`; pilot-facts #B2 "copied into omp's plugin store" is wrong. By run 21 and the realpath rule, that install would fail first with `Cannot find package '@anthropic-ai/claude-agent-sdk'` and, once deps are staged, with `contentText`. Inferred from run 21 plus `legacy-pi-compat.ts:1518-1534`; not run against the real store.

Full gap inventory (lever `/tmp/claude-501/u1-work/gap-check.py` over the patched `src/`, multi-line imports included, against the runtime export dumps; `pi-ai/compat` maps to `pi-ai` per `legacy-pi-compat.ts:839` whose shim exports `getModels` at `legacy-pi-ai-shim.ts:145`):

```
pi-ai            StringEnum                         askclaude-schema.ts  FOUND
pi-ai            calculateCost                      usage.ts             FOUND
pi-ai            contentText                        transcript.ts        MISSING
pi-ai            createAssistantMessageEventStream  index.ts             FOUND
pi-ai            getCurrentSystemMessage            transcript.ts        FOUND
pi-ai            getCurrentTools                    transcript.ts        FOUND
pi-ai/compat     getModels                          index.ts             FOUND (shim line 145; the script's compat dump failed, see run output)
pi-coding-agent  CONFIG_DIR_NAME                    config.ts            FOUND
pi-coding-agent  getAgentDir                        config.ts            FOUND
pi-coding-agent  getAgentDir                        log-paths.ts         FOUND
pi-coding-agent  keyText                            index.ts             FOUND
pi-tui           Text                               index.ts             FOUND
```

Upstream `contentText` (`~/.omp/plugins/node_modules/@earendil-works/pi-ai/dist/utils/text.js:2-9`, pi-ai 1.4.0, MIT):

```js
export function contentText(content, separator = "\n") {
    if (typeof content === "string")
        return content;
    return content
        .filter((block) => block.type === "text")
        .map((block) => block.text)
        .join(separator);
}
```

Run 30 (the scratch stub, same semantics, in `pkg-probe/src/transcript.ts`) is the evidence that this is the last gap: after it the bridge registered its provider, `claude-bridge/claude-haiku-4-5` resolved, and the SDK child ran up to authentication.

## 4. The turn: operator point reached, not crossed (ACCEPTANCE 4(ii))

The host login is Keychain-only (`~/.claude/.credentials.json` absent; `claude --version` = `2.1.309 (Claude Code)`), so the real turn is operator-only under STANDING 4. Run 30 under the scratch HOME stopped at `Not logged in · Please run /login`, which is the exact point. The operator commands, with `source` and `dry-run` columns, are in `.orchestration/orchestrate/regime-cutover/handouts/U1-operator-steps.md`. ACCEPTANCE 5 (bridged tool call, `PI_CODING_AGENT_DIR` env check, `pgrep -fl claude`) is conditional on (i) and is carried into the handout; `pgrep` is also unavailable inside the sandbox (`sysmond service not found`, run-20-pgrep.log).

## 5. Shipping form for U2 (W2d)

- **Directory:** the patched package as a real directory that carries its own `node_modules` beside `package.json`. Deps resolve only upward from the entry's realpath (`legacy-pi-compat.ts:1518-1534`); a bare package fails (run 21). Staging options: clone the hoisted tree (`cp -Rc ~/.omp/plugins/node_modules <dir>/node_modules`, 484M, no network; runs 20-30 used it) or `bun install --production` in the package dir with `registry.npmjs.org` allowed (not measured).
- **Manifest key:** keep `pi.extensions: ["./src/index.ts"]`; every form resolved it manifest-first (`directory-resolution.ts:5-9`; runs 20, 22, 24, 26). `omp.extensions` is accepted and preferred when both exist (`docs/extension-loading.md` "omp takes precedence over pi"), not required.
- **Launcher line:** `-e <dir>` on the seat's omp command (runs 20, 27, 30). It is explicit, needs no plugin-store state, works for every `--profile`, and `--no-extensions` beside it is optional. The profile-store alternative is `omp --profile <name> install <dir>` once per profile, which writes a symlink and `~/.omp/profiles/<name>/plugins/omp-plugins.lock.json` (runs 25, 26). A `config.yml` `extensions:` entry is documented (`docs/extension-loading.md` "Explicitly configured paths") but was not measured.
- **Patch v2:** add `contentText` to the compat patch (inline the eight lines above into `src/transcript.ts`, drop the import name at `transcript.ts:14`). Everything else in the inventory is FOUND. Re-run `gap-check.py` and the session-path check after any patch change.
- **Verification line for U2:** `omp -e <dir> --no-session --model claude-bridge/claude-haiku-4-5 -p "Reply with the single word PONG."` under a scratch HOME must print no `Failed to load extension` on stderr or in `~/.omp/logs/omp.*.log` and must reach `Not logged in · Please run /login` (or the operator's PONG under the real login).

## 6. Deviations from the brief

- `omp models` was dropped as the instrument after runs 10-17 showed it never evaluates extension modules; every form in §2 was re-measured through the session path (not in the brief's candidate list).
- No `-p` turn with `CLAUDE_CONFIG_DIR=~/.claude` was run (STANDING 4, Keychain). Run 20 carried `ANTHROPIC_API_KEY=invalid-u1-dry-run` for a key-auth dry run; it failed at load before any auth, so the key was never used and `api.anthropic.com` was never contacted (no sandbox line for it).
- One scratch-only edit of a copy (`pkg-probe`) to observe the next gap after `contentText`. The patch file in the repo was not changed (`git status` shows only this report and the handout).
- Of the six upstream docs fetched to `/tmp/claude-501/u1-work/docs/`, only `extension-loading.md` was read and cited.
- `pgrep` cannot run inside the sandbox; the process-tree row is operator-only.

## 7. Follow-ups

- F1 (U2): patch v2 with `contentText`; re-run `gap-check.py` against fresh shim export dumps after every omp upgrade (the shim's export list is the moving part).
- F2 (omp): `omp models -e/--extension <file>` does not evaluate the module in 18.11.3 while the session path does (runs 28/29 are the reproducer; probe at `/tmp/claude-501/u1-work/probe-ext.ts`). Trace `src/cli/models-cli.ts:335-341` → `discoverExtensionPaths` step 4 (`loader.ts:640-655`) → `loadExtensions` before relying on the listing anywhere.
- F3 (operator, later): the real `~/.omp/plugins/node_modules/pi-claude-bridge` symlink targets a `/tmp` path without `node_modules`; `omp plugin uninstall pi-claude-bridge` or U2's install replaces it.
- F4 (records): pilot-facts corrections, §3 items 1, 2 and 4 above.
- F5 (U2 instrument): a scripted check that fails when stderr or the omp log contains `Failed to load extension`, so a silent load regression cannot pass.
