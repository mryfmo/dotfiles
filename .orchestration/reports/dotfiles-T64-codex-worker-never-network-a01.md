# Report: dotfiles-T64-codex-worker-never-network-a01

- **Worker:** `claude-standard-dot-a005` in worker-c.
- **Branch:** `chore/codex-worker-never-network` from `origin/main` c6de5156.
- **task_rev:** `41d4fdf3…`, matched.
- **PR:** #236, https://github.com/mryfmo/dotfiles/pull/236.
- **Commits:**
  - `b9c1aefa`: the change.
  - `d950ac69`: narrows the network-trade-off wording (see section 3).
- **Final head:** `d950ac69`.
  - **CI:** green; 13 pass, including CodeRabbit, and `nix` is skipped.
  - **`mergeable_state`:** `clean`.
  - **Branch:** up to date with `main` c6de5156 (behind_by=0).
  - **Codex bot:** 👍 on the final head at 23:02:55Z, with no inline finding.
- **Status:** ready_for_review.

## 1. Change

- **`herdr-agents`, both codex worker launch paths:**
  - **`start_worker_agent` (pair pane):** `worker_args` gains `--ask-for-approval never -c sandbox_workspace_write.network_access=true`, after `--sandbox workspace-write --profile <p>` and before the existing writable-roots `-c`.
  - **`write_spawn_options` (`--add-worker`):** gains the `--ask-for-approval: never` and `--config: sandbox_workspace_write.network_access=true` lines. They pass the existing `^--[a-z][a-z0-9-]*$` / value-charset validation. Upstream `spawn-options.sh` emits repeated `--config` keys as separate token pairs, so the writable-roots `--config` line still follows.
  - **Docs inside the script:** the usage text, the header `@description`, the `write_spawn_options` and `codex_worktree_writable_roots` comments, and the shallow-clone stderr message now describe failure instead of an "operator-approved escalation".
- **Tests:**
  - 11 argv pins and 2 spawn-options pins are updated.
  - One explicit assertion checks that the spawn options carry `--ask-for-approval: never` and the `network_access=true` `--config` line.
  - The shallow-clone stderr assertion now expects "in the codex worker fails.".
- **README** (Codex worker paragraph) **and SKILL.md:46:**
  - There is no escalation prompt for a worker.
  - Out-of-sandbox writes and execpolicy-forbidden commands fail and are reported as `AGMSG-PONG v1 status=blocked`.
  - The network switch is a boolean, and no domain allowlist is configured.
  - The permgate PermissionRequest hook never fires for the worker seat and stays live for interactive sessions.
  - Interactive Codex sessions keep the base config.
- **Untouched:** `agent-config.yaml`, templates, profiles, the audit lane, permgate and the rules file. `~/.codex` was not edited.

## 2. VERIFY summary (details and sources in the validation file)

| Item | Result | Evidence |
|---|---|---|
| (a) git fetch / gh pr view without a prompt | shown | run2: `git fetch origin main` exit 0 in a linked worktree with the herdr roots, FETCH_HEAD written. run1: `gh pr view 235` exit 0. `codex sandbox`: `git ls-remote` works with network true and fails to resolve with false. |
| (b) an outside write fails back to the model | shown | runs 1–3: `touch $HOME/…` exit 1, Read-only file system, file absent. run5: an escalation request is rejected with "approval policy is Never; reject command". |
| (c) a forbidden command is refused with its justification | shown | run1: `rm -rf` and `sudo` were rejected with the T63 justification texts, and the directory remained. |
| (d) PermissionRequest does not fire | shown, with a caveat | No approval event in any rollout, and permgate's Codex entries stayed at 34 before and after. The caveat follows. |

Caveats I want the orchestrator to weigh:

1. **`codex exec` forces `approval_policy = never`.** It did so even with `-a on-request`; the run4 and run5 rollouts record `never`, while `config.toml` says `on-request`.
   - So the exec runs show how `never` behaves, but not the effect of the flag.
   - The flag's effect on the interactive config path the seat uses is shown with `codex debug prompt-input`. With the seat flags the rendered permissions text reads "Approval policy is currently never … commands will be rejected" and "Network access is enabled". With the base config it carries the escalation-request instructions and "Network access is restricted".
   - A headless TUI run under `script` hung on terminal capability queries, so there is no TUI rollout.
2. **Hooks warning, and why (d) has no positive control.** Every run printed `loading hooks from both ~/.codex/hooks.json and ~/.codex/config.toml; prefer a single representation for this layer`. `hooks.json` holds only SessionStart and was modified 2026-10-04 07:45. I could not show the PermissionRequest hook firing in an on-request contrast run (see caveat 1). The last Codex permgate entry is from 2026-10-01T21:54Z.
3. **Scratch rules and an unsandboxed fetch failure.**
   - The live `~/.codex/rules/default.rules` is still the pre-T63 file, so the forbidden rules were loaded from the scratch project layer under a per-invocation trust override.
   - run1's `git fetch` in a plain main clone failed with `.git/FETCH_HEAD: Read-only file system`. That is Codex's `.git` protection under a writable root, not a network failure. The worker worktree avoids it through the granted git metadata roots.
4. **`--json` misses tool calls.** `codex exec --json` does not show the model's code-mode `exec` tool calls. Evidence comes from the rollout files under `~/.codex/sessions/2026/10/0{3,4}/`, which are cited per run.

## 3. Deviations and findings

- **`grep -c 'ask-for-approval never'` = 6, not 2.**
  - The two code lines are 401 and 1163.
  - The other four are documentation that names the flag (header 31, usage 97, comments 319 and 376).
  - I left the docs as they are, because rewording them only to meet the count would be gaming the check.
- **"No domain allowlist" was wrong as worded.**
  - The task text said Codex has no domain allowlist. `strings` of the 0.160.0 binary shows a network-proxy domain policy (`codex_network_proxy`, `allowed_domains`, `denied_domains`, `managed_allowed_domains_only`).
  - `d950ac69` rewords the README and SKILL: the `sandbox_workspace_write.network_access` switch is a boolean, and this repository configures no domain allowlist.
  - Possible follow-up: evaluate the Codex network proxy for a GitHub-only allowlist on the worker seat.
- **The rule file now contradicts the SKILL (outside allowed_files).**
  - `home/dot_config/claude/rules/agmsg-orchestration.md:17` still says "network access stays off, so a GitHub fetch or push remains a boundary action whose escalation prompt only the human operator answers".
  - That contradicts SKILL.md:46. The rule's "Worker commands complete inside the sandbox … the worker fails it, sends `AGMSG-PONG v1 status=blocked`" bullet already agrees with the new behaviour.
  - Proposed follow-up: align rule line 17 in a separate task.
- **Host-dependent regime-boundary tests.**
  - Unsandboxed, two regime-boundary tests fail on this machine because `scripts/check-regime-boundary.sh` runs `pgrep -f 'crit _serve'` against the host. Two real crit servers from the a006 and a007 seats are running.
  - In the sandbox (its own pid namespace) the same tree passes: 218 herdr-agents tests and 713 overall. CI is green.
  - Proposed follow-up: stub `pgrep` in those tests.
- **Activation:** the live pair keeps its current argv until the operator runs `make update`, then `herdr-agents --restart-worker`. I restarted nothing.

## 4. Codex bot

| Head | Result |
|---|---|
| `d950ac69` (final) | 👍 2026-10-03T23:02:55Z, no review comments |

The PR was opened only after `d950ac69` was pushed, so `b9c1aefa` never had a bot review of its own.

## CompactionDB

```
cd ~/Workspace/dotfiles && python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content 'dotfiles-T64 (operator 2026-10-03): herdr-agents launches Codex worker seats with `--ask-for-approval never` and `sandbox_workspace_write.network_access=true`; a worker never prompts, out-of-sandbox and execpolicy-forbidden actions fail and are reported as blocked PONGs; interactive Codex sessions keep on-request and network off.'
cd40adce-50c0-49f2-8016-6ca52883df0a
```

[memory:decision] dotfiles-T64 (operator 2026-10-03): herdr-agents launches Codex worker seats with `--ask-for-approval never` and `sandbox_workspace_write.network_access=true`; a worker never prompts, out-of-sandbox and execpolicy-forbidden actions fail and are reported as blocked PONGs; interactive Codex sessions keep on-request and network off.

## Artifacts

- validation: `.orchestration/validation/dotfiles-T64-codex-worker-never-network-a01.md`
- sandbox: `.orchestration/sandboxes/dotfiles-T64-codex-worker-never-network-a01.md`
- learning: `.orchestration/learning/dotfiles-T64-codex-worker-never-network-a01.md`
- autoskill: `.orchestration/autoskill/runs/dotfiles-T64-codex-worker-never-network-a01.md`

cost: n/a (no subagents). Five `codex exec` runs (run1–run5) used the express profile; run4 used no tools. A sixth invocation stopped while waiting on stdin before the session started. Two `codex debug prompt-input` renders and a headless TUI attempt, which hung on terminal queries, rendered no model output. The runtime does not expose session totals.
