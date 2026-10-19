---
task_id: dotfiles-T133-result-precheck-a04
round: 1
---

# Learning

Task-local triage; nothing promoted.

- Masking before publication only protects what it masks. a03 wrote raw captures straight into the evidence directory and masked them afterwards, so any exit in between, or the masker's own stderr, published raw text. Capture privately, publish only masked copies, and make the failure path delete before it writes its diagnostic. Applies to any tool that records command output as evidence.
- A writer that opens a path by name follows whatever the path is. Check every existing component for a symlink before writing, and write through a temporary file in the checked directory, then rename it into place. Applies to every writer in a directory a PR controls.
- A fake must fail the way the real thing fails. The first fake masker printed one file and exited, so the old code's leak of a later file stayed hidden and the red run errored instead of failing. Build the stub so the old code's real failure mode shows.
- A bus line is only as trustworthy as its sender. Selecting the newest RESULT or revise by text alone let any team member replace it. Filter by the expected sender and recipient pair before ordering.
- A changed argv is an interface change: every test that pins the old argv, inside or outside allowed_files, moves with it. Search for the exact old string before the first commit, so a scope question goes out before the code is written. Here it went out after.
- Bash reads a script as it runs, so editing a script while a long run executes it corrupts that run. It happened twice here: the first time the run had to be stopped, and its private directory is left behind. The second time the committed bytes were restored at once. Edit only between runs, or run a copy.
- A constant spelled like a credential assignment (`<redacted:secret-pattern> + …`) trips the repository's own secret scan even when its value is built at run time. The precheck's `secrets` check caught it, after one push. Name such fixtures neutrally.
- CI's ShellCheck (0.9) and the seat's (0.11) name the indirect-call warning differently, SC2317 and SC2329. A disable directive for indirectly called functions needs both names.
- Line caps make every new test pay rent. Fold an unnamed test into the named one that covers the same cases, share a helper, and turn a docstring into a trailing comment before deleting any assertion.
