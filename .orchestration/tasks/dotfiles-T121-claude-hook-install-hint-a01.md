# AGMSG-TASK dotfiles-T121-claude-hook-install-hint-a01

Drafted 2026-10-09 by the orchestrator seat (`claude-deep-dot`, w4:p1). A one-line fix on a Claude hook source, routed to a Codex seat because a Claude seat never edits its own execution boundary (SKILL step 3). It lands on T118's open branch, so PR #310 carries the whole change and Codex Bot thread 4231499859 is fixed in the PR, per the operator's standing instruction. Kind: one message string in a Claude hook and its unit test; Codex seat.

## Objective

1. In `.claude/worktrees/worker-d`: `git fetch origin feat/rolling-tools-single-update` and `git switch -c feat/rolling-tools-single-update --track origin/feat/rolling-tools-single-update` (the branch exists on the remote; do not rebase, merge or rewrite it). Wait for the orchestrator's go (it comes as the TASK itself: the Claude worker has already pushed its last commit when you receive this).
2. `home/dot_claude/hooks/executable_format-edited-files.py` lines ~72–74: the recovery hint `run \`mise install --locked\`` becomes `run \`make update\` (it installs every declared mise tool)`, and the two comment lines above it become `# make update installs every declared mise tool, so a missing formatter means that step was skipped or failed.` Nothing else in the file changes.
3. `tests/unit/test_format_edited_files_hook.py` line ~72: the assertion follows the new message.
4. `uv run python -m unittest tests.unit.test_format_edited_files_hook 2>&1 | tail -3`; `git diff --stat` must show exactly these two files.
5. Commit (English message `fix(hook): point the formatter recovery hint at make update`, attribution footer `Co-Authored-By: Codex <noreply@openai.com>` is not required; the regime footer for Codex seats is none), then push to the same branch: `git push origin feat/rolling-tools-single-update`. If the push fails on SSH (`Permission denied (publickey)`, the host's SSH agent is empty), use `GIT_CONFIG_GLOBAL=/dev/null git -c credential.helper= -c 'credential.helper=!gh auth git-credential' push https://github.com/mryfmo/dotfiles feat/rolling-tools-single-update`; if that fails too, send `AGMSG-PONG v1 status=blocked` with the exact error and leave the commit local.

Forbidden: anything else; any other file; rebasing or force-pushing the branch; opening or editing the PR; thread resolution; `make update`.

## Artifacts

A Codex seat cannot write the main checkout: write `.orchestration/reports/dotfiles-T121-claude-hook-install-hint-a01.md` (what changed, the commit sha, the push result), `.orchestration/validation/dotfiles-T121-claude-hook-install-hint-a01.md` (the verbatim test run, `git diff --stat`, the push output) and `.orchestration/sandboxes/dotfiles-T121-claude-hook-install-hint-a01.md` (one line: worker-d worktree, branch) at those relative paths in your own worktree, untracked (do not commit them); the orchestrator moves them. No learning or autoskill file is needed for a one-line task; say so in the report.

## Completion

`AGMSG-RESULT v1 task_id=dotfiles-T121-claude-hook-install-hint-a01 status=ready_for_review report=… validation=… sandbox=… commit=<sha>` via `agmsg-dispatch dotfiles-conformance <your identity> claude-deep-dot w4:p1 "<single line>"`. max_turns=6.

## Amendment 1 (orchestrator, 2026-10-09) — a local branch and an explicit push refspec

The branch is checked out in worker-c, so a second worktree cannot switch to it. Instead: `git fetch origin feat/rolling-tools-single-update` and `git switch -c t121/hook-hint origin/feat/rolling-tools-single-update --no-track`; make the two-file change; commit; push with an explicit refspec: `git push origin HEAD:feat/rolling-tools-single-update` (SSH), falling back to `GIT_CONFIG_GLOBAL=/dev/null git -c credential.helper= -c 'credential.helper=!gh auth git-credential' push https://github.com/mryfmo/dotfiles HEAD:feat/rolling-tools-single-update`. A non-fast-forward rejection means the Claude worker pushed meanwhile: `git pull --rebase origin feat/rolling-tools-single-update` once and push again. The Codex worklog under `.agents/worklog/` is waived for this one-line task (the sandbox reports the path read-only); the three `.orchestration` artifacts in your worktree are enough.

## Amendment 2 (orchestrator, 2026-10-09) — artifacts authorized; the gate is not yours

`.orchestration/validation/dotfiles-T121-claude-hook-install-hint-a01-worker-crit.json` and `-worker-review-receipt.md` are authorized at those relative paths in your worktree, untracked. `make require-crit-review` is the orchestrator's integration gate and runs on PR #310 as a whole; do not run it. Leave the unused `shlex` import alone (unrelated). Commit f25e9eaf is on the branch; send `AGMSG-RESULT v1 … status=ready_for_review commit=f25e9eaf…` now.
