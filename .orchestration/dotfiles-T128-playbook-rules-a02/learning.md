# Learning triage: dotfiles-T128-playbook-rules-a02

These are candidates only; nothing is promoted. a01's three candidates stand (`.orchestration/dotfiles-T128-playbook-rules-a01/learning.md`).

1. [memory:failure] In this host's Claude Code Bash, `grep` is a shell function that runs ugrep with `--ignore-files`. It searches a directory argument recursively and skips gitignored files. `ls` is aliased to eza. A command that a rule or task prescribes for every seat therefore has to be checked with `/usr/bin/grep`; a01 amendment 1's `grep -l … mistakes/` passed in a Claude seat and exits 2 everywhere else. Do not capture a path from `ls -d` in evidence scripts: here it printed eza's header, and a `cd` into it failed silently inside a subshell. Use a shell glob.
2. [memory:failure] A mutation script that restores files with `git checkout --` destroys uncommitted edits, so commit before running it. A hook's refusal of a bare `python3` call is what caught this one here.
3. [memory:decision] On an INV-6 reset that continues the same branch, the predecessor's task copy stays at the hash its acceptance record names. Discard any held edit to it, and write the successor's copy at the new path.
