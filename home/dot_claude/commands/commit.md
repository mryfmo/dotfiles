# Commit changes to Git

- Step 1: Review all the uncommited changes in the current session.
- Step 2: Notify the user if there are:
  - Files with security concerns
  - Files with temporary changes
- Step 3: If there are files detected in Step 2, stop and let the user decise what to do next. Else, process to step 4.
- Step 4: Add all changed files to staging. Respect .gitignore and similar files.
- Step 5: Write a commit message following the Conventional Commit policy in `~/.agents/skills/gh-first-workflow/references/gh-git-rules.md`.
- Step 6: Ask if user approves the message. Give 3 options:
  - Approve
  - Regenerate
  - I will write the commit message myself
- Step 7:
  - If user chose Approve on step 6, commit the changes with the generated message.
  - If user chose Regenerate, re-run from step 5.
  - If user chose to write commit message themselves, run `git commit`. It should open a text editor so that the user can write their commit message.
