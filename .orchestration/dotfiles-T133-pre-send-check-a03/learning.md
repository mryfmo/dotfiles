# Learning triage: dotfiles-T133-pre-send-check-a03

These are candidates only; nothing is promoted.

1. [memory:failure] A "no PATH search before the clean re-exec" rule covers every external command in the entrypoint's prelude, not only the interpreter. `dirname` stayed PATH-resolved, and the decoy test missed it because its decoy list named only the obvious tools. Enumerate the prelude's external commands and decoy each, or call them by absolute path.
2. [memory:decision] Replacing a regex parser of another tool's output with a structured parser of the input removes a whole finding class: the checker becomes exit-status-only, and locations come from PyYAML marks. Two rounds of patches to the echoed-output parser had kept reopening it.
3. [memory:failure] An "unwritable TMPDIR" fixture can pass vacuously on a legacy head, because Python's `tempfile` silently falls back to another writable directory. Create temporary files with `dir=os.environ["TMPDIR"]` when the test means that directory.
4. [memory:decision] When a branch is checked out in another seat's worktree, continue on a local branch at the same commit and push `HEAD:<branch>`. Do not touch the other worktree.
