---
task_id: dotfiles-T128-playbook-rules-followup-a01
seat: claude-standard-dot-a002
permission_gated_commands: see the table
---

# Sandbox record: dotfiles-T128-playbook-rules-followup-a01

- Period: from the AGMSG-TASK (2026-10-14T06:47:41Z) to the RESULT.
- These ran inside the sandbox:
  - the HTTPS `git fetch` and `git push`;
  - the branch, the edits, the task copy and the commits;
  - every test and format run, with `UV_OFFLINE=1`, since uv cannot reach pypi from the sandbox.
- No local mutation was chained onto a call that ran outside the sandbox.

Calls outside the sandbox: `gh` through the permission gate (`dangerouslyDisableSandbox`; `gh` fails TLS inside the sandbox) and `agmsg-dispatch` through `excludedCommands`.

| # | Command | Step 4 case |
|--:|---|---|
| 1 | `agmsg-dispatch … AGMSG-PONG v1 task_id=dotfiles-T128-playbook-rules-followup-a01 status=question …` (06:50Z, the scope of the procedure-migration row) | `agmsg-dispatch` |
| 2 | `agmsg-dispatch … AGMSG-PONG v1 … status=alive note=working…` (06:53Z) | `agmsg-dispatch` |
| 3 | `gh pr create --draft …` | `gh` |
| 4 | `gh pr ready <n>` | `gh` |
| 5 | Bot wait from the ready (background; `gh api` reads every 30 seconds) | `gh` |
| 6 | `gh pr checks <n> --watch` (exit status joined) | `gh` |
| 7 | `agmsg-dispatch … AGMSG-RESULT v1 task_id=dotfiles-T128-playbook-rules-followup-a01 …` | `agmsg-dispatch` |
