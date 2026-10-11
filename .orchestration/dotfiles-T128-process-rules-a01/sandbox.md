---
task_id: dotfiles-T128-process-rules-a01
seat: claude-standard-dot-a003
permission_gated_commands: 21
---

# Sandbox record: dotfiles-T128-process-rules-a01

- Seat: `claude-standard-dot-a003` (Claude Code, profile `standard`) in `.claude/worktrees/worker-f`; branch `docs/regime-pattern` from `origin/main` `b896d9bc`.
- Period: from the AGMSG-TASK (2026-10-11T04:16:13Z) to the RESULT.

## Isolation

Every edit, the docs tests, prettier, ruff, the sentence-removal proofs and the local premise commands (`date`, `history.sh`, `grep`, `wc`) ran inside the Claude Code Seatbelt sandbox. The fetch of `origin` ran inside the sandbox (public remote). No `allowed_domains` were used, and no command was refused.

In-sandbox shims, stated as such: `prettier` and `ruff` ran from their mise installs on PATH, because `mise x …` fails inside the sandbox. Commits use `git -c commit.gpgsign=false`, because the signing key is unreadable in the sandbox.

## Out-of-sandbox commands (permission gate, `dangerouslyDisableSandbox`)

`permission_gated_commands` counts every Bash call that ran with `dangerouslyDisableSandbox`, one per call, prompt or not (`agmsg-dispatch` included; each Bot loop is one call). This copy was written before #16, so #16 to #21 are counted in advance; the RESULT names them.

|   # | Command                                                                                                                                                                               | Step 4 case                              |
| --: | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------- |
|   1 | `gh pr view 317 --repo mryfmo/dotfiles --json title,state,headRefName,files --jq …`                                                                                                   | `gh`                                     |
|   2 | `gh pr diff 317 --repo mryfmo/dotfiles \| awk … \| cut … \| head` (PR 317's SKILL hunks)                                                                                              | `gh` (local text filters only)           |
|   3 | `GIT_CONFIG_GLOBAL=/dev/null git -c credential.helper= -c 'credential.helper=!gh auth git-credential' push https://github.com/mryfmo/dotfiles docs/regime-pattern` (first commit)     | `git push`, the authorized form          |
|   4 | `gh pr create … --body-file /tmp/claude-501/pr318-body.md` (failed: wrong path)                                                                                                       | `gh`                                     |
|   5 | `gh pr create --draft … --body-file <scratchpad>/pr318-body.md` (PR #318)                                                                                                             | `gh`                                     |
|   6 | `agmsg-dispatch … AGMSG-PONG … status=alive note=draft PR 318 …`                                                                                                                      | `agmsg-dispatch`                         |
|   7 | the authorized push (`f7c229ff`)                                                                                                                                                      | `git push`                               |
|   8 | `gh pr ready 318 …; date -u +%FT%TZ`                                                                                                                                                  | `gh` (`date` bundled)                    |
|   9 | `gh pr checks 318 --repo mryfmo/dotfiles --watch --interval 30` (background)                                                                                                          | `gh`                                     |
|  10 | Bot wait loop 1: `gh api` reviews, comments, issue comments, at most 30 polls 30 s apart, `@codex review` after 10 minutes (background)                                               | `gh` only; SKILL step 15's bounded wait  |
|  11 | `gh api …/pulls/317/reviews` twice (the premises), with `echo` headers                                                                                                                | `gh`                                     |
|  12 | `cd ~/Workspace/dotfiles && uv run --no-project .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content '…'`                                              | main-checkout `memory add`               |
|  13 | `gh api repos/mryfmo/dotfiles/issues/comments/6105387884 --jq .body \| grep …; gh api …/issues/318/reactions`                                                                         | `gh`                                     |
|  14 | Bot wait loop 2 (the Code Review row, a review object or 👍; same bounds) (background)                                                                                                | `gh` only                                |
|  15 | `gh api …/pulls/318/comments …; gh api …/pulls/318/reviews/5481888792 --jq .body \| grep`                                                                                             | `gh`                                     |
|  16 | the authorized push (`e9ae8b65` and the evidence commit)                                                                                                                              | `git push`                               |
|  17 | `gh pr checks 318 … --watch` on the final head (background)                                                                                                                           | `gh`                                     |
|  18 | Bot wait on the final head (background)                                                                                                                                               | `gh` only                                |
|  19 | the masked copy of the five evidence files to the TASK's `expected_*` paths in the main checkout, `uv run --no-project --with pyyaml scripts/validate-agent-assets.py --mask-secrets` | artifact copy with the repository masker |
|  20 | final recheck of reviews and review comments right before the RESULT (`gh api` only)                                                                                                  | `gh`                                     |
|  21 | `agmsg-dispatch … AGMSG-RESULT v1 task_id=dotfiles-T128-process-rules-a01 …`                                                                                                          | `agmsg-dispatch`                         |

Deviations: #8 bundled a `date` with `gh pr ready`, and #13 and #15 piped `gh` output through `grep`. No other local action ran outside the sandbox, and no refusal was reworked.
