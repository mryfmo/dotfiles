---
task_id: dotfiles-T129-assets-omp-hcom-followup-a01
seat: claude-standard-dot-a007
permission_gated_commands: see the table
---

# Sandbox record: dotfiles-T129-assets-omp-hcom-followup-a01

- Period: from the AGMSG-TASK (2026-10-17T14:53:56Z) to the RESULT.
- Inside the sandbox (Claude Code, macOS Seatbelt) ran: the HTTPS `git fetch`; the branch from PR #388's head b49da6dd, the commits (`git -c commit.gpgsign=false`) and, after #388 merges, the rebase; the task copy, the edits, every test, lint and mutation run (uv offline). The updater tests ran with an evidence-run `mktemp` shim first on PATH, because macOS `mktemp` without a template ignores TMPDIR and the sandbox denies its default directory; the shim is in the validation file and nowhere in the repository. Also inside: the masker, and the HTTPS `git push` with a one-command `-c url.https://github.com/mryfmo/.pushInsteadOf=https://github.com/mryfmo/` rule (no configuration is written).
- Read only, outside this worktree: the main checkout's task file, the lineage's acceptance record and PR #388's local review file. Nothing was written outside worker-c except files under `$TMPDIR` and the scratchpad; the tests' fixture homes live in temporary directories they remove.
- No local mutation was chained onto a call that ran outside the sandbox.

Calls outside the sandbox: `gh` through the permission gate (`dangerouslyDisableSandbox`, Worker Playbook step 4) and `agmsg-dispatch` through `excludedCommands`, planned in advance:

| # | Command | Step 4 case |
|--:|---|---|
| 1 | `gh pr view 388` reads of #388's head and state | `gh` |
| 2 | after the rebase: `gh pr create --draft --repo mryfmo/dotfiles --base main --head tools/assets-hcom-receipt …` and `gh pr ready <pr>` | `gh` |
| 3 | `gh pr checks <pr> --watch` (background, exit status joined; restarted on a transport error) | `gh` |
| 4 | the Bot wait: `gh api --paginate` reads of the Bot's reviews, top-level review comments and summary state on the head, every 30 seconds for at most 15 minutes, and `gh pr comment <pr> --body '@codex review'` only at 10 minutes when no review of the head was reported | `gh` |
| 5 | after a P0/P1 fix round only: the push (inside), then `gh pr comment <pr> --body '@codex review'` and the same Bot wait (`bot_rounds=2`) | `gh` |
| 6 | `agmsg-dispatch … AGMSG-PONG v1 …` and `agmsg-dispatch … AGMSG-RESULT v1 task_id=dotfiles-T129-assets-omp-hcom-followup-a01 …` | `agmsg-dispatch` |
