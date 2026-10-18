---
task_id: dotfiles-T133-task-generator-plan-check-a02
round: 1
---

# Learning

Task-local triage; nothing promoted.

- A generator that needs prose from a task record depends on that record existing. Bundling the template beside the script removes the dependency, and makes the template reviewable with the code that reads it. Applies to any tool that copies wording from another record.
- Text that will be executed is only as trustworthy as the revision it comes from. Refuse a dirty source group before anything runs, and read the command text with `git show <rev>:<path>`, so the executed text is the committed text. The same idea is C14's dispatched sha.
- A glob is a set of files, not a string. Disjointness, threat coverage and scope all have to be decided on the concrete tree matches; comparing two spellings proves nothing. F2, C12 and the generator's concrete rows all took this fix.
- A literal handed to `git grep` must follow `-e`, or a value such as `--open-files-in-pager=<cmd>` becomes an option and runs a program. Applies to every tool that passes data as a command-line argument.
- A check added to a checker can collide with a frozen test module. The first escape, reporting a missing design only for a task with invariants, reopened the bypass the check exists to close: the pre-push review's P2, a mistyped path. The narrower rule keeps the finding for any path that names no design anywhere and exempts only a design in flight in the checkout. Look for the exemption that the fixtures actually need, not the broadest one that makes them pass.
- A regression for a review finding must be run against the head the review read. The first item 16 case passed on eb20d063, because its shared line was untimed and the old code ranked untimed events lowest, so it proved nothing until the shared line carried a timestamp.
- A long-running suite in a worktree blocks a branch switch. Commit first, and give any reviewer its own scratch worktree from the start, so an interruption costs nothing.
- In zsh, `"$VAR:t…"` and `"$VAR:s…"` are history modifiers; write `"${VAR}:…"`. This cost two replay runs here, both caught by their outputs.
