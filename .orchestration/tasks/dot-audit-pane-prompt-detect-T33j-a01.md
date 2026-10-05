# AGMSG-TASK dot-audit-pane-prompt-detect-T33j-a01

## Objective

`herdr-agents --audit` refused two consecutive runs on 2026-09-29 with
"audit pane wJ:p5 is busy (not at a shell prompt)" although the pane was at
its zsh prompt. Evidence (orchestrator, read-only): `herdr pane process-info
--pane wJ:p5` reported the foreground process `/usr/bin/zsh` (the shell
itself, no child); `herdr pane read wJ:p5 --source recent-unwrapped` ended
with the prompt `❯❯❯`; but `herdr pane read wJ:p5 --source visible --lines 5`
returned stale wrapped lines from the previous audit's transcript, so
`wait_for_shell_prompt`'s `herdr pane wait-output … --regex '[$#%❯➜>]+[[:space:]]*$'
--source visible --lines 5 --timeout 10000` timed out. The audit tab had been
recreated (wJ:t3/p4 → wJ:t4/p5) after the operator closed tabs; the `visible`
snapshot of a background tab is not a reliable view of the terminal state.

Deliver, in `home/dot_local/bin/common/executable_herdr-agents`:

1. `wait_for_shell_prompt`: treat `process-info` as authoritative — when the
   foreground process of the pane is the pane's own shell (`shell_pid` equals
   the single foreground process's pid, or the foreground process name is a
   known shell and there is no child), return 0 without the visible-snapshot
   regex. Keep the existing exit-dialog / "stuck" classifications for the
   worker-pane use case (`--restart-worker`) unchanged.
2. When a prompt regex is still needed (process-info unavailable), read
   `--source recent-unwrapped` and ignore trailing blank lines instead of
   `--source visible --lines 5`.
3. Tests in `tests/unit/test_herdr_agents.py` (mutation baseline against the
   unmodified origin/main script): (a) fake process-info reports the shell as
   the only foreground process while the fake `visible` snapshot has stale
   non-prompt text → `--audit` proceeds; (b) fake process-info reports a
   non-shell foreground process → still refused as busy; (c) fallback path
   without process-info uses `recent-unwrapped`.
4. README `--audit` paragraph: one sentence that the busy check is based on
   the pane's foreground process.

[memory:decision] T33j: herdr-agents decides "audit pane busy" from the pane's
foreground process (shell = free), not from a visible-snapshot prompt regex,
because background-tab visible snapshots can be stale (operator 2026-09-29).

## Repo / branch

- Work ONLY in `~/Workspace/dotfiles/.claude/worktrees/worker-c`.
- `git fetch origin`; `git switch -c fix/audit-pane-prompt-detect origin/main`
  (after T33i #204 merges; if it has not, PONG and wait — the audit-mode code
  you edit must include T33i's mask step).
  Verify the dispatched task_rev sha256 against this file on your base, else
  stop and PONG. If the worktree has uncommitted files, stop and PONG.

## Allowed files

- `home/dot_local/bin/common/executable_herdr-agents`
- `tests/unit/test_herdr_agents.py`
- `README.md`
- `.orchestration/{reports,validation,sandboxes,learning,autoskill/runs}/dot-audit-pane-prompt-detect-T33j-a01.md` (main checkout)

## Forbidden actions

- Reading or probing real herdr panes (use `--help` and the fake harness);
  running a real audit or codex; touching rules/SKILL, AGENTS.md,
  model_profiles, permgate, hooks configs, `reviews/ADH_Integrated_Plan/`;
  merging; force push; local bats; `make apply`/`chezmoi apply`; writes
  outside the worktree except the listed `.orchestration` paths.

## Validation commands (paste verbatim output)

```
make validate-agent-assets
make unit-test
shellcheck -x home/dot_local/bin/common/executable_herdr-agents
shfmt --indent 4 --space-redirects --diff home/dot_local/bin/common/executable_herdr-agents
git -C ~/Workspace/dotfiles/.claude/worktrees/worker-c diff origin/main --stat
gh pr checks <pr-number>
```

## Completion

1. PR to `main`, English title/description ending with
   `🤖 Generated with [Claude Code](https://claude.com/claude-code)`. CI green.
2. Artifacts at the exact expected paths; validation with verbatim outputs
   (including the mutation baseline) and the PR number/head SHA.
3. CompactionDB from the main checkout: `memory add --kind decision --scope project` with the `[memory:decision]` text above — paste command and output.
4. `inbox.sh dotfiles claude-standard-dot-a005` at each milestone.
5. `AGMSG-RESULT v1` with all artifact paths; `cost:` line in the report.
   Live E2E (a real `--audit` run on the reused pane) is orchestrator-side.
