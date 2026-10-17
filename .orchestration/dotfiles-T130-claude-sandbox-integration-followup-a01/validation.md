---
task_id: dotfiles-T130-claude-sandbox-integration-followup-a01
seat: claude-review-dot-a005
code_commit: bfcb0525
---

# Validation: dotfiles-T130-claude-sandbox-integration-followup-a01

Every command ran from the worktree `.claude/worktrees/worker-d` on the branch `docs/claude-sandbox-readme-a01` at `bfcb0525` (the README commit `0b226806` and the review-round commit `bfcb0525`; §3 to §5 were re-run on `bfcb0525`), inside the sandbox; `MAIN` names the main checkout and `T` the task id. uv ran offline. The output is verbatim, with the main checkout's and the home directory's paths replaced by `$MAIN` and `$HOME`, and each block ends with the exit status of the command shown.

## 1. Task file (sha256 ea5f5328…) and task copy
```console
$ shasum -a 256 "$MAIN/.orchestration/tasks/$T.md" ".orchestration/$T/task.md"; cmp "$MAIN/.orchestration/tasks/$T.md" ".orchestration/$T/task.md" && echo byte-identical
ea5f53285ac406a1dd45f705f95fbde49714327d2c7b1ed227fdf7dcad516bbf  $MAIN/.orchestration/tasks/dotfiles-T130-claude-sandbox-integration-followup-a01.md
ea5f53285ac406a1dd45f705f95fbde49714327d2c7b1ed227fdf7dcad516bbf  .orchestration/dotfiles-T130-claude-sandbox-integration-followup-a01/task.md
byte-identical
[exit 0]
```
## 1a. The task-consistency check on the dispatched file
```console
$ uv run --offline --no-project --with pyyaml python -I scripts/orchestrator/task-consistency-check.py --root "$PWD" "$MAIN/.orchestration/tasks/$T.md"
dotfiles-T130-claude-sandbox-integration-followup-a01.md: OK
[exit 0]
```
## 2. Base (origin/main after PR #392's merge) and branch
```console
$ git rev-parse --short=8 origin/main; git log --oneline -1 origin/main; git branch --show-current
a8a747af
a8a747af fix(claude): render scoped sandbox access per platform (#392)
docs/claude-sandbox-readme-a01
[exit 0]
```
## 3. The Check: prettier on README.md (the repository's `make` target runs the same `prettier --check` over every tracked .md; CI's prettier comes from mise `npm:prettier`)
```console
$ prettier --version; prettier --check README.md
3.9.10
Checking formatting...
All matched files use Prettier code style!
[exit 0]
```
## 3a. The Check: make validate-agent-assets (exit 0; the WARN lines are the regime-boundary counters' advisory output about the main checkout's untracked records and amendment counts, unrelated to the README; 1478 lines in all, condensed to the shapes with their counts)
```console
$ UV_OFFLINE=1 make validate-agent-assets
uv run --offline --with pyyaml scripts/validate-agent-assets.py
WARN: regime-boundary: untracked .orchestration file in $MAIN: … (1361 such lines, the orchestrator's pending acceptance and review records in the main checkout; elided here)
WARN: regime-boundary: <task> S<n>: … (106 counter lines over 61 tasks; elided here, the last two kept)
WARN: regime-boundary: dotfiles-T130-codex-local-review-exclusion-a01 S2: amendments 5 >= 2 source=live
WARN: regime-boundary: dotfiles-T130-sandbox-portability-a01 S2: amendments 2 >= 2 source=live
agent asset validation ok
[exit 0]
```
## 4. The Check: git diff --numstat origin/main...HEAD (README.md only outside .orchestration/) and the branch
```console
$ git diff --numstat origin/main...HEAD; git log --oneline origin/main..HEAD
73	31	README.md
[exit 0]
bfcb0525 docs(readme): the Linux socket block is the seccomp filter's, the Mach entry is an additional service, and the ask rules are counted rather than called complete (T130 claude-sandbox-integration followup a01, worker review P3s)
0b226806 docs(readme): describe the Claude Code sandbox from the rendered settings of each OS (T130 claude-sandbox-integration followup a01)
[exit 0]
```
## 5. Sentence-to-settings check: every value the rewritten section names is read back from the rendered template and compared (both OS blocks parsed as JSON; the section's domains, excluded entries, allowWrite extras, Mach service, socket, four flags, env map, allow rule, defaultMode, the 32 ask rules and their forms)
```console
$ UV_OFFLINE=1 uv run --no-project python - <<PY … PY   # the script is described in report.md "Readings"
ok  domains named = darwin list = linux list
ok  macOS excludedCommands
ok  linux excludedCommands
ok  allowWrite extras
ok  mach
ok  unix sockets
ok  flags
ok  env
ok  allow
ok  defaultMode auto
ok  ask subcommands named
ok  ask api forms
ok  ask has no git push rule
ok  ask count
[exit 0]
```
## 6. Upstream sentences the text relies on

Read by a read-only fetch of the upstream pages on 2026-10-18 (the fetch tool reports the date, not the clock time); each is quoted, not paraphrased, from the heading named.

| Claim in the README | Source | Quote |
|---|---|---|
| an entry uses the syntax of a `Bash(...)` rule; `agmsg-dispatch *` matches with or without arguments | https://code.claude.com/docs/en/sandboxing, "Run commands outside the sandbox with `excludedCommands`" | "entries use the same syntax as a `Bash(...)` permission rule, where a pattern with no wildcard is an exact match. `docker` matches only `docker` with no arguments. `docker *` matches `docker` with or without arguments" |
| every command in a chained call must match | same | "Every command in the call has to match: `npm ci && docker compose build` stays sandboxed unless another entry covers `npm ci`" |
| the text of the call is matched; a script that runs `gh` internally does not match | same | "Claude Code matches the text of the call: a script or `make` target that calls `docker` internally doesn't match, and neither does `/usr/local/bin/docker`" |
| an excluded command still goes through the normal permission flow; allow rules run without a prompt; the classifier reviews the rest under `auto` | same | "An excluded command goes through the regular permission flow: Read-only commands and commands your allow rules cover run without a prompt; In auto mode, the classifier reviews other excluded commands" |
| `allowUnsandboxedCommands` `true` allows the unsandboxed retry; `false` leaves only the exclusions | https://code.claude.com/docs/en/settings-reference, "`sandbox.allowUnsandboxedCommands`" | "`true`: Claude can retry a command outside the sandbox with the `dangerouslyDisableSandbox` parameter after the sandbox blocks it"; "`false`: Claude Code ignores that parameter, so while the sandbox is running, commands Claude runs are sandboxed unless they match an `excludedCommands` entry" |
| `autoAllowBashIfSandboxed` skips the bare Bash prompt; deny and content-scoped ask rules still apply | same page, "`sandbox.autoAllowBashIfSandboxed`" | "Commands that can't run in the sandbox still go through the regular permission flow, and `deny` rules and content-scoped `ask` rules such as `Bash(git push *)` still apply; a bare `Bash` ask rule is skipped for sandboxed commands" |
| a host outside the list is refused under `auto` unless the command listed it and the classifier approved | https://code.claude.com/docs/en/sandboxing, "Hosts outside your allowed domains" | Auto: "Refused unless the command listed the host and the classifier approved the list" |
| `allowMachLookup` names the Mach services the macOS sandbox may look up | settings-reference, "`sandbox.network.allowMachLookup`" | "List additional XPC and Mach service names the macOS sandbox may look up" |
| `allowUnixSockets` is honoured on macOS only | settings-reference, "`sandbox.network.allowUnixSockets`" | "Claude Code ignores this list on Linux and WSL2, where the seccomp filter can't inspect socket paths; use `allowAllUnixSockets` there instead" |
| `failIfUnavailable` `false` runs unsandboxed when the sandbox cannot start | settings-reference, "`sandbox.failIfUnavailable`" | "`false`: Claude Code runs commands unsandboxed when the sandbox can't start" |

The sentence "`com.apple.trustd.agent`, which macOS certificate validation needs" and the Linux reason "bubblewrap closes Unix sockets and D-Bus (the `gh` keyring read and the herdr socket)" come from the manifest's own comments (`home/dot_agents/agent-config.yaml`, `allowMachLookup` and `linux_excluded_commands`) and the parent task's items 2 and 5.

## 7. CompactionDB memory add (Message Contract: before completion)
```console
$ UV_OFFLINE=1 uv run --no-project .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content "[memory:decision] T130 claude-sandbox-integration followup a01: …"
6ff04934-6296-47a9-ada9-f2d9ee27b2d4
[exit 0]
```
