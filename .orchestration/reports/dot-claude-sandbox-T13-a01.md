# Report: dot-claude-sandbox-T13-a01 — blocked (operator stop at step 8)

- Worker: claude-standard-dot-a003
- Worktree: `.claude/worktrees/env-converge-T10`, branch `feat/claude-sandbox-manifest`
- **PR: https://github.com/mryfmo/dotfiles/pull/179** (OPEN, left as is per the STOP)
- Pushed head: `b729f54875ab9a24b6a961d4ee68b075d938a146` (4 commits on origin/main f2288d6)
- **status: blocked, reason=operator-stop.**
  - Nothing was pushed or committed after the STOP.
  - Per the STOP ACCEPTANCE, only this report and the validation file were written. No sandbox, learning or autoskill artefact was written for T13.
- Evidence: `.orchestration/validation/dot-claude-sandbox-T13-a01.md`

## State at the STOP

- **CI on b729f54:**
  - Failed: `test (ubuntu-latest, client)`, `test (ubuntu-latest, server)` and `test (macos-14, client)`. The cause is bats `bwrap_apparmor.bats` cases 2 and 4 (`[[ "${output}" == *"sudo tee"* ]]`).
  - Passed: `public-bootstrap` ubuntu-server and macOS, plus validate, build, private-bootstrap and changes.
  - `public-bootstrap (ubuntu-latest, client)` was still pending.
  - Because `public-bootstrap (ubuntu-latest, server)` passed, the new `run_once_before_51` installer and the extended `dependencies.sh` ran on a real ubuntu-latest runner without failing.
- **Root cause (test fixture bug, not installer bug):** the script runs `printf … | sudo tee "$PROFILE_PATH" > /dev/null`. That redirect also swallows the fake `sudo()`'s own log line on stdout, so the assertion never sees `sudo tee`. Case 3 (idempotent) passes because the profile really is written.
- **Uncommitted local fix, not pushed:** `tests/install/ubuntu/common/bwrap_apparmor.bats` L20 now reads `printf "sudo %s\n" "$*" >&2` (the fake logs to stderr, which bats `run` captures). It is left unstaged in the worktree (`git status`: ` M tests/install/ubuntu/common/bwrap_apparmor.bats`) and not verified by CI. Discard it with `git -C .claude/worktrees/env-converge-T10 checkout -- tests/install/ubuntu/common/bwrap_apparmor.bats`, or commit and push it once work resumes.

## Design delivered (commits on PR #179)

| Commit                  | Content                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| ----------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `21d5def` feat(agents)  | `claude.sandbox` in `agent-config.yaml`: enabled, failIfUnavailable, autoAllowBashIfSandboxed and allowUnsandboxedCommands all true; `excludedCommands: []`; `allowedDomains` = github.com, api.github.com, uploads.github.com, objects.githubusercontent.com, codeload.github.com. `render_claude_sandbox()` in the generator takes `filesystem.allowWrite` from `codex.sandbox_workspace_write.writable_roots`, a single list. The template was regenerated (`--check` up to date). `validate_claude_sandbox()` enforces the three `true` flags, the existing agmsg-roots helper, allowWrite ⊇ every Codex root, and a non-empty list of bare hostnames. There are 3 unit tests: 1 positive, one negative per rule as subtests, and the extra-Codex-root case. The `home/dot_agents/README.md` parity policy gains item 9 |
| `f6b2445` feat(install) | `dependencies.sh` adds `bubblewrap` and `socat` (17 packages; bats updated). New `install/ubuntu/common/bwrap_apparmor.sh` installs the documented profile at `/etc/apparmor.d/bwrap` only when the sysctl is 1 and the profile differs, reloads AppArmor if it is active, and otherwise prints a deferral notice. New wrapper `home/.chezmoiscripts/ubuntu/run_once_before_51-setup-bwrap-apparmor.sh.tmpl`, and new `tests/install/ubuntu/common/bwrap_apparmor.bats` (5 cases)                                                                                                                                                                                                                                                                                                                                           |
| `04eedfa` feat(doctor)  | `check_claude_sandbox()` in `scripts/check-tools.sh` (section "Claude Code sandbox") reports bwrap, socat, the sysctl and the profile. The existing doctor fixture got healthy fakes; the new unit test covers the 4 Linux states and the Darwin case                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| `b729f54` docs(readme)  | README "Claude Code sandbox": what is confined, why nested worktrees stay writable, the plan-mode caveat, the pre-installer `--settings '{"sandbox":{"failIfUnavailable":false}}'` recovery, and how to inspect denials                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |

Design notes:

- **Not added to allowWrite:**
  - `~/.claude/projects`: `~/.claude` is a sandbox-protected path, and `allowWrite` cannot lift that. Memory writes use the Write tool, not Bash.
  - `herdr-agents.log`: it is written by a SessionStart hook, which runs outside the sandbox.
- **Rules:** `model-selection.md` and `agmsg-orchestration.md` make no sandbox claims (grep exit 1), so no change is needed.

## Local checks (before the STOP)

- Validator: ok.
- Generator `--check`: up to date.
- Unit tests: full suite 414 OK (1 skipped); `claude_sandbox` 3 OK; doctor 5 OK.
- shellcheck and shfmt: clean.
- ruff: counts are identical to origin/main (all 16 findings pre-existing).
- Bats: not run locally (policy).

## Live E2E (this host, before the installer)

The E2E used the real HOME, but with `--setting-sources project --strict-mcp-config --settings <file with only the rendered sandbox block>` instead of a temporary HOME. That avoids copying the OAuth `.credentials.json` into /tmp, where a token refresh could rotate your real login. The debug log confirms that user settings were not loaded. The session used the express args `--model haiku --effort low`.

| Probe                                                           | Result                                                                                                                                                               |
| --------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Strict settings (`failIfUnavailable: true`)                     | Refused to start, exit 1: `sandbox required but unavailable: … socat not installed … refusing to start without a working sandbox` (expected pre-installer behaviour) |
| Fallback settings (`failIfUnavailable: false`)                  | `⚠ Sandbox disabled … Commands will run WITHOUT sandboxing`. **Every result below is from the unsandboxed fallback**                                                 |
| (a) write to `/tmp/outside-probe-20260925165649` / write in cwd | Both blocked by the **permission layer** (`Output redirection … needs approval`), not the sandbox; neither file exists                                               |
| (b) `gh api user -q .login`                                     | Works (unsandboxed)                                                                                                                                                  |
| (c) `git ls-remote https://github.com/mryfmo/dotfiles.git HEAD` | Works (unsandboxed): `f2288d6…	HEAD`                                                                                                                                  |
| (d) `ssh -T git@github.com`                                     | Authenticates (unsandboxed), exit 1 with the GitHub greeting                                                                                                         |
| (e) `herdr pane list`                                           | Works (unsandboxed)                                                                                                                                                  |
| `bwrap --ro-bind / / --unshare-user --unshare-net true`         | `loopback: Failed RTM_NEWADDR: Operation not permitted`, exit 1: the AppArmor userns restriction the new profile addresses                                           |

## Open questions

1. **ssh push:** under the real sandbox, ssh on port 22 does not use the sandbox's HTTP/SOCKS proxy, so it is expected to be blocked. Decide after `make update` whether agent push remotes should switch to https.
2. **herdr Unix socket:** on Linux only the optional seccomp filter (`@anthropic-ai/sandbox-runtime`) blocks Unix sockets. If `herdr pane list/run` fails under the real sandbox, the minimal addition would be `excludedCommands: ["herdr pane *"]`, with a comment citing that evidence. It is not added now because there is no evidence.
3. **`failIfUnavailable: true`:** once the settings apply, any machine where the installers did not run will refuse to start Claude until `make update` succeeds. The README documents the `--settings` recovery.
4. **Real confinement E2E** (probes a–e) can only run after the operator's `make update` installs socat and the profile.

## Effects

- `scratch-home-e2e`: `…/scratchpad/claude-sandbox-e2e-20260925165649/` (scratch repo, settings, logs, stream-json). Reverse: `rm -rf <scratchpad>/claude-sandbox-e2e-*`.
- **Additional, undeclared in the task:** `claude-projects-e2e-transcript`, meaning Claude Code wrote the E2E session transcript to `~/.claude/projects/-tmp-claude-1000--home-moriya-Workspace-dotfiles-73e6eabe-e514-4cad-81a9-a399b3f7c9c3-scratchpad-claude-sandbox-e2e-20260925165649-repo/`. Reverse: remove that directory. It is left in place (not removed under the `rm -rf` deny rule).

## Incident (reported at start via PONG)

The nested worktree `.claude/worktrees/env-converge-T10` was missing at task start. A chained `cd <missing>; … git switch -c …` therefore ran `git switch -c feat/claude-sandbox-manifest origin/main` in the **main checkout** at 16:46:46 JST.

- There were no tracked changes, and it was reverted immediately with `git switch main`. The main checkout is back on `main` at 3303fbc.
- I then recreated the worktree at the task path with `git worktree add`.
- Since then I've used `&&`-chained absolute paths only.

## Durable facts

[memory:decision] Claude Code sandbox is rendered from claude.sandbox in agent-config.yaml, symmetric with codex.sandbox_workspace_write; agmsg writable roots come from one manifest list

```bash
python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content "Claude Code sandbox is rendered from claude.sandbox in agent-config.yaml, symmetric with codex.sandbox_workspace_write; agmsg writable roots come from one manifest list"
# → 0d3989b0-e129-4e09-8f24-70962d23232c
```

cost: n/a
