---
permission_gated_commands: 54
---

# Sandbox record: dotfiles-T124-wave1-task-validator-a01

- Seat: `claude-standard-dot-a001` (Claude Code, worker kind `claude`, profile `standard`) in `.claude/worktrees/worker-c`.
- Period: from the AGMSG-TASK (2026-10-10T09:00:29Z) to RESULT round 2 (revise round 1 included).
- `permission_gated_commands` counts every Bash call of this task that ran with `dangerouslyDisableSandbox: true`, prompted or not. It includes the `agmsg-dispatch` calls (which `excludedCommands` runs outside the sandbox anyway), and the two that come after the list in validation §9 was drawn for RESULT round 2: the masked artifact copy and that RESULT's `agmsg-dispatch`. Validation §9 lists the other 52 verbatim, from the session transcript; among them are the first RESULT's two masked copies and its dispatch. 54 in all.

## Isolation, stated exactly

- Every edit, commit but one, test, mutation run, download and validation ran inside the Claude Code Seatbelt sandbox in the worker worktree, or in scratch worktrees under the session scratchpad.
- Outside the sandbox, through the permission gate, ran only Worker Playbook step 4's cases, plus the one deviation below:
  - `git push` with `gh auth git-credential`;
  - `gh` printing to stdout through text filters (`gh pr create`, `gh pr checks`, background `--watch` and Bot-wait loops of `gh` calls with `sleep`, `gh api` reads of the Bot's comments and reviews and of one CI job log, and `gh pr edit` of the PR body);
  - the main-checkout CompactionDB `memory add`;
  - the masked artifact copy with the repository masker;
  - `agmsg-dispatch` (the questions q1–q6, the status PONGs, the first RESULT and RESULT round 2).
- The branch's first fetch, `git fetch -q origin`, ran inside the sandbox, against the public remote with no credential.
- **One deviation.** At the commit of 5a17d633 (validation §9, item 10, 09:43:26Z), `git add -u` and `git -c commit.gpgsign=false commit` ran in the same unsandboxed command as the `git push`. They wrote only the worktree's index and the commit object, the same commit a sandboxed run makes, and nothing else. Step 4 names `git push`, not the commit, so this is outside step 4. Every later commit ran inside the sandbox, and its push ran alone.
- **No command was refused.** The sandbox denied only:
  - `mise x node npm:prettier` (mise has no TLS in the sandbox). The prettier on `PATH` was used instead, and stated as such (validation §1–2).
  - the process substitution `/dev/fd` in one `diff`, which was redone with temp files.

## Stated in-sandbox shims

- A `mktemp` that honours `TMPDIR`, first on `PATH` for the full-suite runs. macOS `mktemp -d` ignores `TMPDIR`, and the sandbox refuses `/var/folders`.
- `commit.gpgsign=false` through `GIT_CONFIG_COUNT/KEY/VALUE`, for test runs whose git fixtures commit. The host signs commits, and its key is unreadable in the sandbox. Without the shim, the sixteen existing boundary-check tests fail at their fixture's commit, at the base as well.
- `allowed_domains` `pypi.org` and `files.pythonhosted.org`, for `uv run --with pyyaml` in the parser-against-PyYAML checks (validation §6). `github.com` and the release-asset hosts were needed for no download in this task.

## Other boundaries (unchanged)

- Commit signing: the key is unreadable in the sandbox, so commits use `git -c commit.gpgsign=false`.
- Scratch worktrees (`base-d29ce4c1`, `mut`) are removed with `git worktree remove --force` before the RESULT; `git worktree prune` is never run.
