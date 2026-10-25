---
description: Commit this session's changes with a Conventional Commit message
argument-hint: "[optional commit message hint]"
---

# Commit changes to Git

- Step 1: Review the uncommitted changes with `git status` and `git diff`, and identify the files this session changed.
- Step 2: Notify the user if there are:
  - Files with security concerns
  - Files with temporary changes
  - Staged, unstaged or untracked changes this session did not make
- Step 3: If Step 2 found anything, stop and let the user decide what to do next. Otherwise, continue to Step 4.
- Step 4: Stage only the files this session changed, by explicit path (`git add -- <path>...`); never `git add -A` or `git add .`. Leave unrelated changes unstaged so they do not enter the commit.
- Step 5: Write a commit message following the Conventional Commit policy in `~/.agents/skills/gh-first-workflow/references/gh-git-rules.md`. Use `$ARGUMENTS` as a hint when given.
- Step 6: Ask if the user approves the message. Give 3 options:
  - Approve
  - Regenerate
  - I will write the commit message myself
- Step 7:
  - If the user chose Approve in Step 6, commit the staged changes with the generated message.
  - If the user chose Regenerate, re-run from Step 5.
  - If the user chose to write the commit message themselves, run `git commit`. It should open a text editor so that the user can write their commit message.
