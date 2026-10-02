# Sandbox: dot-ua-graph-refresh-T55-a01

- **Worktree and branch:** worker-c, branch `chore/ua-graph-refresh-T55` from `origin/main` 940a3a2b. It has one commit, `98bdf43f` (`.ua/` only), which is pushed. `git ls-remote` shows `98bdf43ff966f4b73dd25832d1f77c1196dc0bdb`.
- **Branch switch.** The sandboxed `git switch -c` stopped partway on the read-only `.git/config.lock` stub, the same failure as T53. The branch ref was created at 940a3a2b, and the index and worktree were already there, but HEAD did not move. I finished the switch with `git symbolic-ref HEAD refs/heads/chore/ua-graph-refresh-T55`. After that, `git status --porcelain --untracked-files=no` was empty.
- **Push upstream.** `git push -u` landed the push, but writing the upstream config failed on the same stub, so no tracking config exists.
- **Phantom placeholders.** 19 untracked character devices (1,3) sit at the worktree root: `.bashrc`, `.zshrc`, `.gitconfig`, `.gitmodules`, `.mcp.json`, `.profile`, `.zprofile`, `.bash_profile`, `.ripgreprc`, `.idea`, `.vscode`, and `.claude/{agents,commands,skills,workflows,output-styles,routines,launch.json,loop.md}`. They are the Claude sandbox's `/dev/null` deny masks, not files. They were kept out of the scan with `--exclude` and were never staged.
- **Plugin scratch.** Plugin scratch stayed in the gitignored `.ua/intermediate/` and `.ua/tmp/`. Trash dirs, including the stale T51 shards, went to `$TMPDIR/ua-trash/` rather than the non-ignored `.ua/.trash-*`. After the save, only the gitignored `.ua/intermediate/scan-result.json` remains.
- **Ran sandboxed:**
  - git fetch, switch, commit and push
  - all plugin node and python scripts
  - every subagent's file work
  - `ua-symbol-coverage`
- **Ran unsandboxed** (`dangerouslyDisableSandbox`, permission-gated):
  - `gh pr create`, `gh pr checks` and `gh pr view` (gh auth returns 401 inside the sandbox)
  - CompactionDB `memory add` in the main checkout (its `.writer.lock` is read-only in the sandbox)
  - Edits in the main checkout's `.orchestration/`, which is outside the sandbox write roots:
    - one `sed` on the report's cost line
    - the `cp` of the assembled validation file into `.orchestration/validation/`
    - one python edit of that file (the verbatim validator and PR-identity sections)
  - Copying the CI capture out of `/tmp`, then `rm` of `/tmp/checks.txt` and `/tmp/checks-watch.txt`. Unsandboxed commands get `TMPDIR=/tmp`, sandboxed ones get `/tmp/claude-1000`.
- **`agmsg-dispatch` (RESULT):**
  - **First attempt, plain run from the worktree:** failed with `Error: Os { code: 1, kind: PermissionDenied, message: "Operation not permitted" }` / `agmsg-dispatch: pane not found or unavailable: wT:p1` (rc=1). In this session it ran sandboxed despite the documented `excludedCommands` entry.
  - **No message stored:** messages.db had no T55 RESULT row, so a retry could not double-send.
  - **Retry with `dangerouslyDisableSandbox`:** rc=0. The message is row 687, created 2026-10-02T13:53:14Z and read 2026-10-02T13:53:22Z.
  - This is a candidate check for the orchestrator: the `excludedCommands` coverage of `agmsg-dispatch` did not take effect in this worker session.
- **Writes outside the worktree:** none beyond the five allowed `.orchestration/*/dot-ua-graph-refresh-T55-a01.md` paths in the main checkout, the CompactionDB decision, and `$TMPDIR` scratch.

## Revise round 1

- **Commit and push.** The new commit `8694200f` on top of `98bdf43f` was committed and pushed sandboxed (no force). `git ls-remote` shows `8694200f9fa0a36d3dec8f8a95a0a9f7c7186c52`.
- **Intermediates.** Round-0 intermediates were restored from `$TMPDIR/ua-trash/.trash-1790948053/` into the gitignored `.ua/intermediate/` and `.ua/tmp/`. The revise checklists were written to `.ua/tmp/revise-checklist-*.json`. After the save, the scratch went back to `$TMPDIR/ua-trash/`.
- **Subagents.** Four plugin `file-analyzer` revise subagents edited only `.ua/intermediate/batch-*.json` and `.ua/tmp/`.
- **Ran unsandboxed:**
  - `gh pr checks`, `gh pr edit` and `gh pr view`;
  - the edits that append round-1 sections to the main checkout's `.orchestration/{reports,validation,sandboxes,learning}` files;
  - `agmsg-dispatch`, as the task's round-1 section instructs.
