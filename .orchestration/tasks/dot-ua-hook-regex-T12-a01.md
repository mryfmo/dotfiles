# AGMSG-TASK dot-ua-hook-regex-T12-a01: upstream fix for the understand-anything commit-detection regex (plan part C)

Plan: `/home/moriya/Workspace/dotfiles/.agents/worklog/claude/melodic-conjuring-sifakis.md` §C. This task mutates no dotfiles checkout; it prepares an upstream pull request.

## Problem (verified)

`understand-anything-plugin/hooks/post-tool-use-auto-update.mjs` L3: `const COMMIT_COMMAND = /git\s+(commit|merge|cherry-pick|rebase)/;` matches `git merge-base`, `git merge-tree`, `git commit-tree`, `git rebase--interactive` helpers, and any Bash whose text merely contains those words (e.g. a heredoc mentioning "git commit"). Each false positive injects a "Commit detected … update the graph" instruction into the session.

## Steps

1. Clone upstream `https://github.com/Egonex-AI/Understand-Anything.git` into `/home/moriya/Workspace/Understand-Anything` (new directory; do NOT modify `~/.understand-anything/repo`, which the installer manages). If a fork under the authenticated GitHub account does not exist, create one with `gh repo fork --remote=false` and add it as remote `fork` (declare this as an effect).
2. Branch `fix/hook-commit-regex-word-boundary`. Change the regex so that only real commit-creating subcommands match: subcommand must be followed by end-of-string, whitespace, or a non-`-` character, e.g. `/(^|[;&|]\s*|\s)git\s+(?:-C\s+\S+\s+|--\S+\s+)*(commit|merge|cherry-pick|rebase)(?![\w-])/`. Keep the change minimal and readable; explain it in a one-line comment.
3. Extend `tests/hooks/post-tool-use-auto-update.test.mjs`: positive cases `git commit -m x`, `git -C /p commit`, `git merge main`, `cd x && git rebase main`; negative cases `git merge-base A B`, `git merge-tree --write-tree A B`, `git commit-tree`, `echo "git commit"` is acceptable to leave as-is if the existing tests treat plain text as a command (state what the current tests expect). Run `pnpm test -- tests/hooks` (or the root `pnpm test` if filtering is unsupported) and paste the output.
4. Commit (conventional style), push to the fork, open the PR against upstream `main` in English with the reproduction and the test list. Paste `gh pr view --json url,number`.
5. Note in the report that the dotfiles side needs no change: the fix reaches this machine via the managed plugin update on a later `make update`.

## allowed_files

Only files under `/home/moriya/Workspace/Understand-Anything` (new clone) plus the five artefact files below.

## forbidden_actions

editing `~/.understand-anything/repo`, `~/.claude/plugins/cache/**`, or any dotfiles checkout; `chezmoi apply`; `make update`; force-push.

## effects

`gh-fork-understand-anything` (reverse: `gh repo delete <account>/Understand-Anything` after the PR is merged or closed), `local-clone-workspace-understand-anything` (reverse: `rm -rf /home/moriya/Workspace/Understand-Anything`).

## Artefacts (in `/home/moriya/Workspace/dotfiles`)

report `.orchestration/reports/dot-ua-hook-regex-T12-a01.md` (PR URL, regex before→after, effects with reverse mapping, `[memory:decision]`: "understand-anything commit hook false positives are fixed upstream, not by patching the plugin cache"), validation, sandbox, learning, autoskill (same basename). `contextdb_cli.py memory add` from the main checkout; paste command and output.

## Done signal

`AGMSG-RESULT v1 task_id=dot-ua-hook-regex-T12-a01 status=ready_for_review|blocked pr=<url> effects=gh-fork-understand-anything;local-clone-workspace-understand-anything report=... validation=... sandbox=... learning=... autoskill=...` via `send.sh dotfiles <your identity> claude-remediation-dot "<message>"`. max_turns=25.
