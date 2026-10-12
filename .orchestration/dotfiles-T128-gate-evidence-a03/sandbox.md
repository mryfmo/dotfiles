---
task_id: dotfiles-T128-gate-evidence-a03
seat: claude-standard-dot-a002
---

# Sandbox record: dotfiles-T128-gate-evidence-a03

- Period: from a01's AGMSG-TASK (2026-10-12T11:58:43Z), through a01's withdrawal (13:02:30Z), a02's AGMSG-TASK (13:17:02Z), its first RESULT (14:16:46Z), amendment 1 (14:28:26Z), the withdrawal (15:25:13Z) and a03's AGMSG-TASK (15:41:03Z), to the RESULT. Edits, the unit tests, ruff, prettier, the mutation checks, the records-only `make require-crit-review` and the commits ran inside the sandbox. No `allowed_domains`.
- Worktree `.claude/worktrees/worker-f`, branch `regime/gate-evidence` (created for a01 with `git switch -c regime/gate-evidence --no-track origin/main`, so `.git/config` gained no upstream). Commits use `git -c commit.gpgsign=false`.
- Two sandbox effects on test runs, both environment-only:
  - The global `commit.gpgsign` reads `~/.ssh/id_ed25519.pub`, which the sandbox denies, so every `git commit` inside the test fixtures fails and the module showed 73 failures on unmodified `origin/main`. Test runs set `GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=commit.gpgsign GIT_CONFIG_VALUE_0=false` for their own process (validation §2).
  - PyPI is unreachable; `--with pyyaml` runs use `UV_OFFLINE=1`.
  - The gate now spawns `uv run --offline … --with pyyaml` for the acceptance record. Inside the sandbox it is served from the uv cache, and the online retry only happens when the offline run cannot start; the test harness keeps `UV_CACHE_DIR` under its fake `HOME`.
- The full unit suite fails the same 78 tests on this branch as on `origin/main`, in six modules no file of this task feeds (validation §7).
- Scratch worktrees of `origin/main` and of the code heads (`$TMPDIR/basewt`, `recwt` to `recwt5`, all detached) served the base comparisons and the records-only runs, and were removed with `git worktree remove` (`--force` only for an untracked probe file).
- The first push, `git push origin regime/gate-evidence`, failed ("Could not read from remote repository"), because the global `url.git@github.com:.pushinsteadof` turns the HTTPS remote into SSH, and there is no SSH key. Every push since uses `GIT_CONFIG_GLOBAL=/dev/null git -c credential.helper= -c 'credential.helper=!gh auth git-credential' push https://github.com/mryfmo/dotfiles regime/gate-evidence`.
- Out-of-sandbox actions are only the Worker Playbook step 4 cases: `git push`, `gh`, the main-checkout CompactionDB `memory add`, writing and masking the main-checkout evidence copies, and `agmsg-dispatch` (`excludedCommands`). The main-checkout copy of this file counts them.
