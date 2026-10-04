# Sandbox: dotfiles-T64-codex-worker-never-network-a01

- **Worktree and branch:** worker-c, branch `chore/codex-worker-never-network` from `origin/main` c6de5156. The sandboxed `git switch -c` created the ref but stopped on the `.git/config.lock` stub, so I finished the switch with `git symbolic-ref HEAD refs/heads/chore/codex-worker-never-network` and `git reset --hard HEAD` on the clean tree.
- **Commits and push:** two commits, `b9c1aefa` and `d950ac69`, committed and pushed.
- **Scratch VERIFY:** done only under `/tmp/claude-1000/t64-verify-azrv`:
  - a shallow clone, and a non-shallow `--filter=blob:none` clone with a linked worktree;
  - the T63 rules copied into each scratch `.codex/rules/`;
  - trust given only per invocation with `-c projects."<path>".trust_level="trusted"`.
- **Untouched:** no `~/.codex` file was edited, no credential was copied or linked, and the live pair seat was not restarted.
- **Outside-write probe:** `~/t64-outside-probe` was attempted from inside the Codex sandbox only and never created. I confirmed it was absent after every run.
- **Unsandboxed runs** (`dangerouslyDisableSandbox`):
  - `codex` (exec, sandbox, debug prompt-input) and the scratch `git clone`;
  - `gh pr create/checks` and `gh api`;
  - CompactionDB `memory add`;
  - the writes to the main checkout's T64 `.orchestration` files;
  - `agmsg-dispatch`;
  - the read of permgate's `decisions.jsonl` and the Codex rollouts.
- **Test environment:** the sandbox's pid namespace hides host processes. The herdr-agents regime-boundary tests pass sandboxed and fail unsandboxed while host `crit _serve` processes exist (see the report).
