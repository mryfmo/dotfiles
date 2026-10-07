# Learning: dotfiles-T113-codify-T111-lessons-a01

- **`var="$(cmd | head -n N)"` under `set -o pipefail` fails with 141** once `cmd` writes more than the pipe buffer after `head` exits. Under `set -e` the script then dies before its next line. Append `|| true` to the assignment: the captured lines are kept. [memory:failure] A refusal guard lost its message (rc 141) because `head` closed the pipe under pipefail.
- **`git rev-parse --abbrev-ref --symbolic-full-name '@{upstream}'` prints the literal `@{upstream}` and exits 128** when the configured upstream's ref is gone. A function that lets that stdout through and then echoes a fallback returns two lines. Capture into a variable and echo only on success.
- **To exercise a long `git status` in a test, put the files directly in a tracked directory.** git collapses an untracked directory into one `?? dir/` line. Clean up thousands of files with `find … -delete`, because a glob passed to `rm` hits the argument-length limit.
- **Read every verbatim block of a task against the implementation,** not only against each other (lesson C): the README sentence "uncommitted changes" would have under-described a guard that also refuses unmerged and stale trees.
- No rule candidate is promoted. A unit test for the new boundary line in `tests/unit/test_herdr_agents.py` is a follow-up candidate.

## Revise round 1

- **A unit test is complete only when it fails without the change.** A temporary `git show <base>:<file> > <file>`, the test run and `git checkout -- <file>` prove that in one command without stashing. Then paste `git diff --stat HEAD -- <file>` to show the restore.
- **The stop gate counts a revise ACCEPTANCE as a new open task.** Read the inbox when the gate fires after a RESULT, instead of assuming the gate is stale.

## Revise round 2

- **State a guard's guarantee as narrowly as its predicate.** A "changes reach the host only through a merged pull request" sentence promised more than a check that skips git-ignored files. Name what the guard does not check next to the guarantee, instead of widening the predicate past its purpose.
