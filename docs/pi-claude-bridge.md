# pi-claude-bridge as an omp extension

`pi-claude-bridge` is a Pi extension that registers the `claude-bridge/<model>`
provider and answers each turn through the Claude Agent SDK, which runs the
bundled Claude Code binary on the host's claude.ai login. This repository
installs a pinned, patched copy as an omp extension directory (plan 025
decisions 30, 37, 38 and D-024-129). Pi executes the tools; the child Claude
Code only produces the model turns.

## Route

```text
omp -e ~/.local/lib/omp-extensions/pi-claude-bridge --model claude-bridge/claude-haiku-4-5
  -> src/index.ts registers provider claude-bridge (omp rewrites @earendil-works/* imports to its legacy pi shims)
  -> @anthropic-ai/claude-agent-sdk query() spawns node_modules/@anthropic-ai/claude-agent-sdk-<platform>/cli
  -> the child authenticates with the host's claude.ai login (Keychain), tools: [] and bypassPermissions
```

The model id after `claude-bridge/` is the Anthropic catalog id. The seat
profiles (`model_profiles` in `home/dot_agents/agent-config.yaml`) choose the
model; this document covers only the asset.

## Install

`make update` runs `scripts/update-agent-assets.sh`, whose
`update_pi_claude_bridge` step:

1. downloads `pi-claude-bridge-<pin>.tgz` from `registry.npmjs.org` and checks
   its sha256 against `assets.pi-claude-bridge.sha256` in
   `home/dot_agents/agent-config.yaml`;
2. extracts it into a staging directory beside the target and applies every
   `home/dot_agents/assets/pi-claude-bridge/patches/*.patch` in name order
   with `patch -p1 -F0` (no fuzz: GNU patch would otherwise apply a patch
   whose context drifted and exit 0);
3. copies the committed `bun.lock` in and runs
   `bun install --production --omit=peer --frozen-lockfile`, so the dependency
   set is the reviewed one (peers are omitted because omp's legacy pi compat
   layer provides `@earendil-works/pi-*` and `typebox` itself);
4. runs `gap-check.ts`, which imports omp's three legacy shims and refuses the
   install when the bridge imports a value name they do not export (the guard
   for omp upgrades);
5. writes `RECEIPT` (tarball, patch and lockfile sha256 lines, then the
   installed `@anthropic-ai/claude-agent-sdk*` versions) and renames the
   staging directory to `~/.local/lib/omp-extensions/pi-claude-bridge`.

A run whose `RECEIPT` head already equals the pinned inputs changes nothing.
The step is skipped with a message when `bun` or omp is absent. Run it alone
with `scripts/update-agent-assets.sh update_pi_claude_bridge`.

## Patches

Each patch is a plain `diff -ruN a b` between consecutive stages of the
upstream `package/` tree, so a reviewer can re-derive it.

| Patch                                | Why                                                                                                                                                                                                                                                                                                                                                                             |
| ------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `01-omp-shim-exports.patch`          | omp's legacy `pi-coding-agent` shim does not export `formatSkillsForPrompt`, so `src/skills.ts` carries Pi's implementation (MIT, same output). The shim does export `keyHint` and `buildSessionContext` (`gap-check.ts` lists both as FOUND), so upstream's calls to them stay.                                                                                                |
| `02-content-text.patch`              | The `pi-ai` shim does not export `contentText`; `src/transcript.ts` carries pi-ai 1.4.0's eight-line implementation (MIT). Without it omp logs `Failed to load extension ... Export named 'contentText' not found`.                                                                                                                                                             |
| `03-no-bash-timeout-injection.patch` | Decision 38: the bridge added `timeout: 120` to every bash tool call it handed to Pi (`mapToolArgs` in `src/index.ts`; seen on the wire as `{"command":...,"timeout":120}`). omp's bash tool keeps its own timeout handling.                                                                                                                                                    |
| `04-setting-sources-none.patch`      | The provider `query()` passes `settingSources: []`, so the child Claude Code loads no user, project or local `settings.json`: the host's hooks, plugins and permission rules do not run inside bridge turns. The claude.ai login is not a setting and still applies. Measured 2026-10-23: with the default, the child's thinking cited the host's superpowers system reminders. |

Upstream kept the default `settingSources` so that Bedrock and Vertex users
keep `env` and `apiKeyHelper` from `settings.json` (comment above
`CLAUDE_MD_EXCLUDES` in `src/index.ts`). This route uses the claude.ai login,
so nothing it needs lives in those files. The alternative, a
`PI_CODING_AGENT_DIR` early exit in every hook, would touch every hook script
and still load the host's plugins; one option on the query is smaller.

## Launcher flag

The seat launcher passes, verbatim:

```text
-e ~/.local/lib/omp-extensions/pi-claude-bridge
```

omp resolves the directory manifest-first (`pi.extensions` in `package.json`
names `./src/index.ts`) and resolves dependencies upward from the entry's real
path, which is why the install directory carries its own `node_modules`.
`--no-extensions` beside `-e` is optional and keeps other extensions out.

## Operator login

The child Claude Code uses the host's claude.ai login: the Keychain on macOS,
`~/.claude/.credentials.json` (mode 0600) on Linux (Claude Code authentication
doc, "Credential management"). Before the first bridge turn, the operator runs
`claude` once and completes `/login` in their own terminal; no script does this.
Without the login a bridge turn ends with `Not logged in · Please run /login`.

A Linux seat host reached over SSH (`herdr --remote`) has no browser of its
own. There, `claude auth login` sends its URL to `$BROWSER`, which
`seat-login-preflight <role>` points at `regime-open-url`, so the laptop
browser opens it. The callback port is random (50903, 50915 and 50920 on three
runs, Claude Code 2.1.309), so no SSH forward can carry it. The URL asks for
the code flow (`code=true`), so the page shows a code to paste at the
terminal's prompt. The fallback is `claude setup-token` on the laptop: the
operator stores the printed one-year token in `~/.config/claude-code/oauth-token`
on the seat host, mode 0600, by hand. `~/.zshenv` and `~/.profile` then export
it as `CLAUDE_CODE_OAUTH_TOKEN` when the file is non-empty. The Agent SDK reads
that variable, except in bare mode, and the bridge never passes `--bare`: its
only extra CLI arguments are `model`, `strict-mcp-config` and
`thinking-display` (`src/index.ts`, `extraArgs`). The steps are in
`docs/remote-host-logins.md`.

## Load check

`omp models` never evaluates extension modules, so the only instrument is a
session:

```sh
HOME=<scratch dir> scripts/update-agent-assets.sh check_pi_claude_bridge
```

It runs
`omp --no-extensions -e <install dir> --no-session --model claude-bridge/claude-haiku-4-5 --max-time 60 -p "Reply with the single word PONG."`,
fails when stderr or the omp log files written by that run contain
`Failed to load extension`, and passes when the output reaches the model
(`PONG` with a login, `Not logged in` without). Point `HOME` at a scratch
directory to keep the session out of the real `~/.omp`; under the real HOME a
logged-in host spends one short model turn. The function is callable from
`make doctor` once the Makefile wires it (follow-up).

## Subagents

An omp Task subagent on the claude-bridge route breaks the seat that spawned it. Measured on
2026-10-24 at about 06:03Z: the orchestrator seat spawned a Task subagent (an inventory scout), the
subagent failed with `No API key for provider: claude-bridge`, and from then on every hcom delivery into
that seat failed with `Extension sendUserMessage failed`, so the seat was dead to the loop; the two worker
seats on the same route and the host login were unaffected. So every seat policy denies the `task` tool
(`tools.approval.task: deny` in `home/dot_agents/omp/policies/{orchestrator,worker,audit}.yml`, U34 in
U36), and the seats do their reading with their own tools. omp refuses the call before the tool runs:
`tests/unit/test_omp_seat_policy.py` `OmpTaskDenyLiveTest` drives the installed omp against a local fake
model that asks for a `task` call and gets back `Tool "task" is blocked by user policy. To allow: remove
"tools.approval.task: deny" from config.` for each role. Revisit the deny when the bridge supports
subagents.

## Fallbacks

- `anthropic/<model>` with `ANTHROPIC_API_KEY` is omp's built-in provider and
  needs no extension; use it when the bridge cannot load or the login is
  unavailable.
- An exported `ANTHROPIC_API_KEY`, `ANTHROPIC_AUTH_TOKEN` or
  `ANTHROPIC_BASE_URL` redirects the child Claude Code to that gateway
  (upstream README), so the bridge seat must not inherit them unless that is
  intended.

## Upgrading

Change `pin` and `sha256` in `assets.pi-claude-bridge`, run
`uv run --no-project --with pyyaml scripts/generate-agent-configs.py` to
render the constants into `scripts/update-agent-assets.sh`, regenerate
`bun.lock` from the new tarball (`bun install --omit=peer --lockfile-only`
inside its `package/`), re-check that every patch still applies, and run the
load check. An omp upgrade needs no change here unless `gap-check.ts` reports
a MISSING row; then the missing name gets a patch like `01` or `02`.
