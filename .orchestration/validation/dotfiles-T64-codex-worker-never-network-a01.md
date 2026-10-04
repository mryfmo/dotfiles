# Validation: dotfiles-T64-codex-worker-never-network-a01

- **task_rev:** `sha256:41d4fdf3237f5398c068524cff0a607aebead952c8e77327e393474d6ff8f830`. `sha256sum` of the task file in the main checkout matches it.
- **Branch:** `chore/codex-worker-never-network` from `origin/main` c6de5156.
- **PR:** #236, https://github.com/mryfmo/dotfiles/pull/236.
- **Commits:**
  - `b9c1aefa`: the change.
  - `d950ac69`: docs scope fix for the network trade-off.
- **Final head:** `d950ac69ac77b7478dc506272889800695390eff`.

## Validation commands (verbatim, on the final head)

```
$ git log -1 --format=%H
d950ac69ac77b7478dc506272889800695390eff
$ git diff origin/main --stat
 README.md                                          | 27 +++++++++----
 .../dot_agents/skills/agmsg-orchestration/SKILL.md |  2 +-
 home/dot_local/bin/common/executable_herdr-agents  | 32 ++++++++++-----
 tests/unit/test_herdr_agents.py                    | 47 +++++++++++++++-------
 4 files changed, 75 insertions(+), 33 deletions(-)
$ grep -c 'ask-for-approval never' home/dot_local/bin/common/executable_herdr-agents
6
$ grep -n 'ask-for-approval never' home/dot_local/bin/common/executable_herdr-agents
31:#   `--ask-for-approval never` and `sandbox_workspace_write.network_access=true`,
97:--ask-for-approval never and sandbox_workspace_write.network_access=true: it
319:#   runs with --ask-for-approval never, so nothing escalates). Granted:
376:#   --sandbox workspace-write --ask-for-approval never --config
401:    [[ ${kind} == claude ]] || args="--profile ${HERDR_AGENTS_WORKER_PROFILE} --sandbox workspace-write --ask-for-approval never --config sandbox_workspace_write.network_access=true"
1163:        worker_args=(--sandbox workspace-write --profile "${HERDR_AGENTS_WORKER_PROFILE:-standard}" --ask-for-approval never -c sandbox_workspace_write.network_access=true)
$ grep -n 'network_access=true' home/dot_local/bin/common/executable_herdr-agents
31:#   `--ask-for-approval never` and `sandbox_workspace_write.network_access=true`,
97:--ask-for-approval never and sandbox_workspace_write.network_access=true: it
377:#   sandbox_workspace_write.network_access=true` for codex, as start_worker_agent
401:    [[ ${kind} == claude ]] || args="--profile ${HERDR_AGENTS_WORKER_PROFILE} --sandbox workspace-write --ask-for-approval never --config sandbox_workspace_write.network_access=true"
1163:        worker_args=(--sandbox workspace-write --profile "${HERDR_AGENTS_WORKER_PROFILE:-standard}" --ask-for-approval never -c sandbox_workspace_write.network_access=true)
$ uv run python -m unittest tests.unit.test_herdr_agents 2>&1 | tail -3
Ran 218 tests in 129.886s

FAILED (failures=2)
$ make unit-test (tail -3)

FAILED (failures=2, skipped=1)
make: *** [Makefile:163: unit-test] エラー 1
$ make validate-agent-assets; echo exit=$?
exit=0
WARN: regime-boundary: crit review server still running (pgrep -f 'crit _serve')
WARN: regime-boundary: additional worker workspace still open: dotfiles worker worker-d (herdr-agents --remove-worker)
WARN: regime-boundary: additional worker workspace still open: dotfiles worker worker-e (herdr-agents --remove-worker)
agent asset validation ok
$ mise x node npm:prettier -- prettier --check README.md home/dot_agents/skills/agmsg-orchestration/SKILL.md
Checking formatting...
All matched files use Prettier code style!
$ mise x shfmt -- shfmt -i 4 -sr -d home/dot_local/bin/common/executable_herdr-agents; shellcheck home/dot_local/bin/common/executable_herdr-agents
shfmt exit=0
shellcheck exit=0
```

Note on the two failures above. That run was unsandboxed, and so were its `make unit-test` and `make validate-agent-assets`. Two regime-boundary tests (`test_regime_boundary_check_flags_empty_seats_only` and `test_regime_boundary_check_counts_names_across_runtime_types_at_an_active_seat`) failed with `'review' unexpectedly found in "...regime-boundary: crit review server still running (pgrep -f 'crit _serve')"`. `scripts/check-regime-boundary.sh` runs `pgrep -f 'crit _serve'` against the host process table, and the host had two live crit servers from other worker seats:

```
$ pgrep -af 'crit _[s]erve'   (unsandboxed)
4129281 /home/moriya/.local/bin/crit _serve --plan-dir /home/moriya/.crit/plans/plan-agmsg-actas-claude-standard-dot-a006-2026-10-04 --name plan-agmsg-actas-cla
4150161 /home/moriya/.local/bin/crit _serve --plan-dir /home/moriya/.crit/plans/plan-agmsg-actas-claude-standard-dot-a007-2026-10-04 --name plan-agmsg-actas-cla
$ pgrep -fc 'crit _[s]erve'   (sandboxed, own pid namespace)
0
```

The same tree, re-run in the Claude sandbox, which hides host processes:

```
$ uv run python -m unittest tests.unit.test_herdr_agents 2>&1 | tail -3
Ran 218 tests in 127.202s

OK (skipped=1)
$ make unit-test (tail -3)
Ran 713 tests in 158.821s

OK (skipped=2)
```

This is a test-isolation gap that already exists: the boundary tests read the host `pgrep`. This change does not cause it, and CI is green. A follow-up is proposed in the report.

`grep -c 'ask-for-approval never'` returns 6, not the expected 2. The two code lines are 401 (`write_spawn_options`) and 1163 (`start_worker_agent`). The other four are documentation that names the flag: the header at 31, the usage text at 97, the writable-roots comment at 319, and the `write_spawn_options` comment at 376. I did not reword the docs to fit the count.

## CI, mergeable_state and branch (final head)

```
CodeRabbit	pass
changes	pass
private-bootstrap (macos-14, client)	pass
private-bootstrap (ubuntu-24.04, client)	pass
private-bootstrap (ubuntu-24.04, server)	pass
public-bootstrap (macos-14, client)	pass
public-bootstrap (ubuntu-24.04, client)	pass
public-bootstrap (ubuntu-24.04, server)	pass
test (macos-14, client)	pass
test (ubuntu-24.04, client)	pass
test (ubuntu-24.04, server)	pass
validate	pass
nix	skipping
test (ubuntu-26.04, client)	pass
{
"baseRefOid": "c6de5156f4583ac22d5a901364515cb0525e2dde",
"headRefOid": "d950ac69ac77b7478dc506272889800695390eff",
"mergeStateStatus": "CLEAN"
}
clean
behind_by=0 ahead_by=2

```

Codex review of the final head (`d950ac69`, pushed 2026-10-03T22:58:04Z):

```
reviews with commit_id=d950ac69: 0; review comments on PR 236: 0
chatgpt-codex-connector[bot] +1 2026-10-03T23:02:55Z
```

bot: 👍 on the final head, with no inline findings.

## VERIFY (scratch repositories under /tmp/claude-1000/t64-verify-azrv; the live seat and ~/.codex were not touched)

### Setup and caveats

- **Scratch repos:**
  - `repo/` is a shallow clone of mryfmo/dotfiles. It is a main checkout, so the worktree roots do not apply.
  - `wt/` is a linked worktree of `full/`, a non-shallow `--filter=blob:none` clone. Its git metadata roots come from the branch's own `codex_worktree_writable_roots`, sourced from the script.
  - Each scratch repo carries the T63 rules at `.codex/rules/default.rules` and is trusted for that invocation only with `-c projects."<path>".trust_level="trusted"`.
- **Live rules:** the live `~/.codex/rules/default.rules` is still the pre-T63 file (23 allow rules, 0 forbidden), because `make update` has not run. The forbidden rules were therefore loaded from the scratch project layer.
- **`codex exec` forces `never`:** it runs with `approval_policy = never` whatever the flag says. The control runs record `never` in their rollout `turn_context` both without `-a` (run4) and with `-a on-request` (run5), while `~/.codex/config.toml` says `approval_policy = "on-request"`.
  - The exec runs therefore show how `never` behaves, not the effect of the flag.
  - The flag's effect on the interactive path the seat uses is shown with `codex debug prompt-input` (below).
  - A headless TUI run under `script` hung on terminal capability queries and produced no rollout.
- **Where the tool calls are recorded:** `codex exec --json` does not emit `command_execution` items for the model's code-mode `exec` tool calls. The authoritative record of every tool call and its output is each run's rollout file, extracted below.

### Seat argv takes effect on the interactive config path

```
$ cd wt; codex --sandbox workspace-write --profile express --ask-for-approval never -c sandbox_workspace_write.network_access=true debug prompt-input 'x'   (grep of the rendered permissions text)
   Network access is enabled.
   Approval policy is currently never. Do not provide the `sandbox_permissions` for any reason, commands will be rejected.
$ codex --sandbox workspace-write --profile express debug prompt-input 'x'   (base config: on-request, network off)
   Network access is restricted.
   Escalation Requests / ... escalation outside the sandbox: / ... ALWAYS proceed to use the `sandbox_permissions` and `justification` parameters ...
```

### Deterministic sandbox probes (`codex sandbox`, no model)

```
$ codex sandbox -c sandbox_mode="workspace-write" -c sandbox_workspace_write.network_access=true -c <roots> -- touch $HOME/t64-outside-probe
touch: '/home/moriya/t64-outside-probe' に touch できません: 読み込み専用ファイルシステムです
rc=1
$ codex sandbox … -- touch ./t64-inside-probe
rc=0
$ codex sandbox … -- git ls-remote origin refs/heads/main
c6de5156f4583ac22d5a901364515cb0525e2dde	refs/heads/main
rc=0
$ codex sandbox (network_access=false) -- git ls-remote origin refs/heads/main
fatal: unable to access 'https://github.com/mryfmo/dotfiles/': Could not resolve host: github.com
```

(The `rc=0` printed after the last command was `tail`'s exit status, so it is omitted. The failure line itself is the evidence.)

### End-to-end `codex exec` runs (tool calls and outputs from the rollouts)

Command for run1, run2 and run3. run1 omitted the writable roots and ran in `repo/`.

```
codex --sandbox workspace-write --profile express --ask-for-approval never -c sandbox_workspace_write.network_access=true -c "$ROOTS" -c 'projects."<wt>".trust_level="trusted"' exec --json -C <wt> "<prompt>" < /dev/null
```

```
### run1: ~/.codex/sessions/2026/10/03/rollout-2026-10-03T22-00-23-01a101d9-f07f-7ca2-979c-be27e6d26fb9.jsonl
turn_context: approval_policy=never sandbox=workspace-write network_access=True writable_roots=4 cwd=/tmp/claude-1000/t64-verify-azrv/repo
CALL "sed -n '1,240p' .agents/worklog/codex/learn/learn_index.md && printf '\\\\n--- AGMSG SKILL ---\\\\n' && sed -n '1,260p' /home/moriya/.agents/skills/agmsg-orchestration/SKILL.md"
  -> Script completed Wall time 0.1 seconds Output:  sed: can't read .agents/worklog/codex/learn/learn_index.md: No such file or directory
CALL "sed -n '1,320p' /home/moriya/.agents/skills/agmsg-orchestration/SKILL.md"
  -> Script completed Wall time 0.1 seconds Output:  --- name: agmsg-orchestration description: Coordinate structured agmsg task orchestration between a Claude Code orchestrator and Codex workers. Use when Codex or Claude Code needs to run or supervise AGMSG-TASK / AGMSG-RESULT / AGMSG-ACCEPTANCE workflows, bootstrap workers in herdr panes, manage .orchestration 
CALL 'git fetch --depth 1 origin main'
  -> Script completed Wall time 0.1 seconds Output:  {"exit_code":255,"output":"error: cannot open '.git/FETCH_HEAD': Read-only file system\n"}
CALL 'gh pr view 235 --repo mryfmo/dotfiles --json number,state'
  -> Script completed Wall time 0.6 seconds Output:  {"exit_code":0,"output":"{\"number\":235,\"state\":\"MERGED\"}\n"}
CALL 'touch /home/moriya/t64-outside-probe'
  -> Script completed Wall time 0.1 seconds Output:  {"exit_code":1,"output":"touch: cannot touch '/home/moriya/t64-outside-probe': Read-only file system\n"}
CALL 'rm -rf t64-junk'
  -> Script failed Wall time 0.0 seconds Output:  Script error: exec_command failed: CreateProcess { message: "Rejected(\"`/usr/bin/zsh -lc 'rm -rf t64-junk'` rejected: Recursive force removal is never delegated; remove specific paths instead.\")" }
CALL 'sudo true'
  -> Script failed Wall time 0.0 seconds Output:  Script error: exec_command failed: CreateProcess { message: "Rejected(\"`/usr/bin/zsh -lc 'sudo true'` rejected: Agents never escalate privileges; ask the operator to run it.\")" }

### run2: ~/.codex/sessions/2026/10/03/rollout-2026-10-03T22-02-33-01a101db-f0a2-7983-bbc4-c0d5a047be87.jsonl
turn_context: approval_policy=never sandbox=workspace-write network_access=True writable_roots=8 cwd=/tmp/claude-1000/t64-verify-azrv/wt
CALL 'git fetch origin main'
  -> Script completed Wall time 0.6 seconds Output:  {"exit_code":0,"output":"From https://github.com/mryfmo/dotfiles\n * branch            main       -> FETCH_HEAD\n"}
CALL 'touch /home/moriya/t64-outside-probe'
  -> Script completed Wall time 0.1 seconds Output:  {"exit_code":1,"output":"touch: cannot touch '/home/moriya/t64-outside-probe': Read-only file system\n"}
CALL 'git log -1 --format=%H FETCH_HEAD'
  -> Script completed Wall time 0.1 seconds Output:  {"exit_code":0,"output":"c6de5156f4583ac22d5a901364515cb0525e2dde\n"}

### run3: ~/.codex/sessions/2026/10/03/rollout-2026-10-03T22-03-49-01a101dd-1993-7d72-a55d-40f0ecb47302.jsonl
turn_context: approval_policy=never sandbox=workspace-write network_access=True writable_roots=8 cwd=/tmp/claude-1000/t64-verify-azrv/wt
CALL 'touch /home/moriya/t64-outside-probe'
  -> Script completed Wall time 0.1 seconds Output:  {"exit_code":1,"output":"touch: cannot touch '/home/moriya/t64-outside-probe': Read-only file system\n"}

### run4: ~/.codex/sessions/2026/10/04/rollout-2026-10-04T07-48-36-01a103f4-7a72-7141-a699-a2c955cb25cc.jsonl
turn_context: approval_policy=never sandbox=workspace-write network_access=False writable_roots=4 cwd=/tmp/claude-1000/t64-verify-azrv/wt

### run5: ~/.codex/sessions/2026/10/04/rollout-2026-10-04T07-55-17-01a103fa-9912-7610-b04a-0b4af5605c7d.jsonl
turn_context: approval_policy=never sandbox=workspace-write network_access=False writable_roots=4 cwd=/tmp/claude-1000/t64-verify-azrv/wt
CALL 'touch /home/moriya/t64-outside-probe'
  -> Script failed Wall time 0.0 seconds Output:  Script error: approval policy is Never; reject command — you cannot ask for escalated permissions if the approval policy is Never
```

Outcomes checked outside the model:

```
FETCH_HEAD-before=absent ... FETCH_HEAD-after=present   (full/.git/worktrees/wt/FETCH_HEAD, run2)
probe-before=absent ... probe-after=absent             (~/t64-outside-probe, every run; still absent before writing this file)
t64-junk after run1: junk-present                      (rm -rf refused)
```

Codex's own router log (run1 stderr):

```
ERROR codex_core::tools::router: error=exec_command failed: CreateProcess { message: "Rejected(\"`/usr/bin/zsh -lc 'rm -rf t64-junk'` rejected: Recursive force removal is never delegated; remove specific paths instead.\")" }
ERROR codex_core::tools::router: error=exec_command failed: CreateProcess { message: "Rejected(\"`/usr/bin/zsh -lc 'sudo true'` rejected: Agents never escalate privileges; ask the operator to run it.\")" }
```

### (a) git fetch and gh pr view without a prompt

**Shown.**
- In the linked worktree with the herdr roots, run2 got `git fetch origin main` exit 0 and FETCH_HEAD was written.
- run1 got `gh pr view 235` exit 0 (`{"number":235,"state":"MERGED"}`).
- The deterministic probe got `git ls-remote` exit 0 with `network_access=true` and "Could not resolve host" with `false`.
- No approval event appears in any rollout.
- run1's `git fetch` in the plain main clone (`repo/`) failed with `.git/FETCH_HEAD: Read-only file system`. That is Codex's read-only protection of `.git` under a writable root, not the network. The worker worktree avoids it through the granted `<common>/worktrees/<name>` root.

### (b) a write outside the writable roots fails back to the model, not a prompt

**Shown.**
- In runs 1–3, `touch $HOME/t64-outside-probe` came back to the model as exit 1 with "Read-only file system", and the file never appeared.
- In run5 an explicit escalation request (`sandbox_permissions: require_escalated`) came back as `approval policy is Never; reject command — you cannot ask for escalated permissions if the approval policy is Never`.

### (c) an execpolicy-forbidden command is refused under never, with the justification text

**Shown.** In run1:
- `rm -rf t64-junk` was rejected with "Recursive force removal is never delegated; remove specific paths instead.", and the directory remained.
- `sudo true` was rejected with "Agents never escalate privileges; ask the operator to run it."

### (d) the PermissionRequest hook does not fire under never

**Shown, with a caveat.**
- No `*approval_request*` event appears in any of the five rollouts.
- permgate's Codex entries in `~/.local/state/permgate/decisions.jsonl` were 34 before run1 and 34 after run5. The file had 470 lines in total; the last Codex entry is from 2026-10-01T21:54:51Z.

**Caveat:** every run also printed `loading hooks from both /home/moriya/.codex/hooks.json and /home/moriya/.codex/config.toml; prefer a single representation for this layer`. `~/.codex/hooks.json` (SessionStart only, modified 2026-10-04 07:45) and the `[[hooks.PermissionRequest]]` entry in `config.toml` coexist. I could not demonstrate the hook firing in an on-request contrast run, because `codex exec` forces `never` and the TUI cannot run headless. The 34 earlier Codex entries show that it fired for interactive sessions up to 2026-10-01.

### Codex 0.160.0 sources for `never`

- **`codex --help` (0.160.0):** "-a, --ask-for-approval … never: Never ask for user approval Execution failures are immediately returned to the model".
- **`codex-rs/core/src/exec_policy.rs`** (local copy at /tmp/claude-1000/codex-exec_policy.rs, fetched for 0.160.0 in T63):
  - **Lines 48–49:** `PROMPT_CONFLICT_REASON = "approval required by policy, but AskForApproval is set to Never"`.
  - **Line 221:** `prompt_is_rejected_by_policy` returns `AskForApproval::Never => Some(PROMPT_CONFLICT_REASON)`.
  - **Lines 801–802:** a dangerous-command match under `Never` is `Decision::Forbidden`.
  - **Lines 810–813:** otherwise `Never` allows the command, "relying on the sandbox for protection".
- **Network allowlist:** `strings` of the 0.160.0 native binary shows a network-proxy domain policy (`codex_network_proxy`, `allowed_domains`, `denied_domains`, `managed_allowed_domains_only`). The README and SKILL therefore say that this repository configures no domain allowlist, not that none exists.
