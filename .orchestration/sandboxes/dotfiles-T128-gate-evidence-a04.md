---
task_id: dotfiles-T128-gate-evidence-a04
seat: claude-standard-dot-a002
permission_gated_commands: 29
---

# Sandbox record: dotfiles-T128-gate-evidence-a04

- Period: from a01's AGMSG-TASK (2026-10-12T11:58:43Z), through a01's withdrawal (13:02:30Z), a02's AGMSG-TASK (13:17:02Z), its first RESULT (14:16:46Z), amendment 1 (14:28:26Z), the withdrawal (15:25:13Z) a03's AGMSG-TASK (15:41:03Z), the hold (01:12:46Z), amendment 1 (01:45:59Z), a03's RESULT (02:30:16Z) and withdrawal (02:37:48Z), a04's AGMSG-TASK (03:13:46Z), its RESULT (04:48:43Z) and the revise (04:57:32Z), to the revise RESULT. Edits, the unit tests, ruff, prettier, the mutation checks, the records-only `make require-crit-review` and the commits ran inside the sandbox. No `allowed_domains`.
- Worktree `.claude/worktrees/worker-f`, branch `regime/gate-evidence` (created for a01 with `git switch -c regime/gate-evidence --no-track origin/main`, so `.git/config` gained no upstream). Commits use `git -c commit.gpgsign=false`.
- Two sandbox effects on test runs, both environment-only:
  - The global `commit.gpgsign` reads `~/.ssh/id_ed25519.pub`, which the sandbox denies, so every `git commit` inside the test fixtures fails and the module showed 73 failures on unmodified `origin/main`. Test runs set `GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=commit.gpgsign GIT_CONFIG_VALUE_0=false` for their own process (validation §2).
  - PyPI is unreachable; `--with pyyaml` runs use `UV_OFFLINE=1`.
  - Under the YAML form (`b2b3db45` to `7581d590`), the gate spawned `uv run --offline … --with pyyaml` for the acceptance record. Overnight the uv cache was pruned to 38M, without PyYAML: every offline load then failed, the online retry was blocked (pypi.org is not in the sandbox allowlist), and a module run timed out at 600 s. One command with `allowed_domains` pypi.org and files.pythonhosted.org fetched PyYAML 6.0.3 back. Amendment 1 (plan 013 A′) removed the subprocess: the gate now reads a JSON block with the standard library, so the gate makes no network call.
- The full unit suite fails the same 78 tests on this branch as on `origin/main`, in six modules no file of this task feeds (validation §7).
- Scratch worktrees of `origin/main` and of the code heads (`$TMPDIR/basewt`, `recwt` to `recwt10`, all detached) served the base comparisons and the records-only runs, and were removed with `git worktree remove` (`--force` only for an untracked probe file).
- The first push, `git push origin regime/gate-evidence`, failed ("Could not read from remote repository"), because the global `url.git@github.com:.pushinsteadof` turns the HTTPS remote into SSH, and there is no SSH key. Every push since uses `GIT_CONFIG_GLOBAL=/dev/null git -c credential.helper= -c 'credential.helper=!gh auth git-credential' push https://github.com/mryfmo/dotfiles regime/gate-evidence`.
- Out-of-sandbox actions are only the Worker Playbook step 4 cases: `git push`, `gh`, the main-checkout CompactionDB `memory add`, writing and masking the main-checkout evidence copies, and `agmsg-dispatch` (`excludedCommands`). The main-checkout copy of this file counts them.
- Revise 1 (audit finding 2): call 7 of the main-checkout copy ran a local branch creation, a checkout and the commit `27e8a0ea` outside the sandbox, chained after a fetch. From the revise on, every repository mutation runs inside the sandbox. That covers the fetch of `20d776d4`, `git switch`, the `--ff-only` merge, both commits (`2231a4f7`, `09caaa91`), the scratch worktree `$TMPDIR/revwt` and both HTTPS pushes. Only the `gh` reads (Bot wait, CI, reviews) run outside it, because `gh` fails TLS verification in the sandbox (`x509: OSStatus -26276`).

`permission_gated_commands` counts a04's Bash calls with `dangerouslyDisableSandbox`, one per call, read from the session transcript from a04's AGMSG-TASK (03:13:46Z) on. a01's, a02's and a03's calls are in their main-checkout copies. Call 7 also ran a local branch creation and a commit outside the sandbox, because they were chained after the fetch; neither needed it. The `agmsg-dispatch` calls run through `excludedCommands` and are not counted: the PONGs of 03:45:49Z (pushed, with the INV-2 flag), 03:56:22Z (Bot round 1), 04:11:06Z (the split, part 1) and 04:23:20Z (the split done), the first RESULT (04:48:43Z), the PONG of 05:18:13Z (revise 1 pushed), and this RESULT (validation §17). A sandboxed `gh api` call failed with a TLS error (`x509: OSStatus -26276`) and was re-run as call 12. From revise 1 on (calls 23 to 29), only `gh` and the main-checkout copy left the sandbox. The `gh` calls are reads, plus the Worker Playbook step 15 `@codex review` comments that `bot-wait.sh` posts. The fetch, the switch, the commits, the scratch worktree and both pushes ran inside it (the sandbox record above).

| # | Command | Step 4 case |
|--:|---|---|
| 1 | `memory add` (decision `39e1994d…`, a04) | main-checkout `memory add` |
| 2 | HTTPS push of `9db7ed3c` and `863ae465` (with an inbox read) | `git push` |
| 3 | HTTPS push of `ca7dcd73` (with an inbox read) | `git push` |
| 4 | `gh pr checks 329 --watch` on `ca7dcd73` (background) | `gh` |
| 5 | `bot-wait.sh` on `ca7dcd73` (background) | `gh` |
| 6 | `gh api` review 5498584052 and its comments | `gh` |
| 7 | HTTPS fetch of `main`, chained in the same call with the local `git switch -c regime/gate-evidence-fixtures --no-track origin/main`, the checkout of the fixtures and the commit `27e8a0ea`; only the fetch needed the network | `git push` (the fetch) |
| 8 | HTTPS push of `regime/gate-evidence-fixtures` and `gh pr create` (#340) | `git push`, `gh` |
| 9 | HTTPS push of `8d54fd76`, `8c0c015b` and `ffe7d872`, and `gh pr view 340` | `git push`, `gh` |
| 10 | `bot-wait.sh` on #340, then #329 (background) | `gh` |
| 11 | `gh pr checks --watch` on #340, then #329 (background) | `gh` |
| 12 | `gh api` review 5498822030, its comments and #340's reviews | `gh` |
| 13 | `gh api` the Bot's summary comments on both PRs | `gh` |
| 14 | `gh run list`/`gh run view --log-failed` on #329's failed run | `gh` |
| 15 | `gh run view --log-failed`, grouped by job and module | `gh` |
| 16 | `gh run view --json jobs` (the cancelled jobs) | `gh` |
| 17 | `collect-a04.sh`: check runs, the failed job and the Bot listings on a04's heads (validation §12, §13) | `gh` |
| 18 | `gh api` #340's update-branch commit, its reviews and comments, with an inbox read | `gh` |
| 19 | CI watch on `20d776d4` (background, validation §12) | `gh` |
| 20 | `gh api` the patched Bot wait's issue-comment query against #340 (it finds 6138208548) | `gh` |
| 21 | `gh api` every Codex review on #329 and #340, unfiltered by commit (validation §13) | `gh` |
| 22 | copy these five files into the main checkout with `cp -n`, mask them with its `scripts/validate-agent-assets.py --mask-secrets`, and read the inbox (first RESULT) | main-checkout artifacts |
| 23 | revise 1: `bot-wait.sh` on #340's `2231a4f7`, then its CI (background) | `gh` |
| 24 | revise 1: `gh api` #340's no-findings comment, CI and both PRs' states | `gh` |
| 25 | revise 1: `bot-wait.sh` on #329's `2239c2eb`, then its CI (background) | `gh` |
| 26 | revise 1: the CI and Bot listings on the revise heads (validation §18, §19) | `gh` |
| 27 | revise 1: GitHub's update-branch merges `bbe62911` and `60d152a1`, their CI and #340's comments | `gh` |
| 28 | revise 1: CI on `60d152a1` until it finished | `gh` |
| 29 | revise 1: overwrite these five files in the main checkout (they were committed in #342), mask them, and read the inbox | main-checkout artifacts |

