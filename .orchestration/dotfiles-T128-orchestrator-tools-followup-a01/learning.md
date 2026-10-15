# Learning triage: dotfiles-T128-orchestrator-tools-followup-a01

These are candidates only; nothing is promoted. The candidates of `dotfiles-T128-chain-github-scripts-a01` stand (`.orchestration/dotfiles-T128-chain-github-scripts-a01/learning.md`).

1. [memory:failure] `git status --short | awk '{print $NF}'` reduces each entry to one path and drops what the entry is.
   - **The failure.** A deletion then reaches `cp` and aborts under `set -e`, and a rename leaves its old path behind.
   - **The fix.** List with `git status --porcelain -z --no-renames`. Those paths are unquoted, and a rename appears as a deletion plus an addition. Then split present paths from missing ones.
   - **Where it applies.** Any script that mirrors a working tree's changes into another tree.
2. [memory:failure] A script that moves or copies "every modified file" must handle the modified file that is a deletion.
   - **The failure.** `git diff --name-only` lists it, but there is nothing to move.
   - **The fix.** Restore it for the operation that needs a clean tree, then delete it again afterwards on every exit path.
   - **The history.** The two deletion defects, in boundary.sh and ff-main.sh, drew 11 of the 22 owned rows over five heads of one PR.
3. [memory:decision] A rule that dispositions sweep items automatically names the neutral level it accepts per source: annotation `notice`, status `success`, review `commented`. Every other level stays a gap. A denylist of known-bad levels misses the next one, such as `changes_requested` here.
4. [memory:failure] A URL is not an item id in pr-feedback.py's sweep.
   - **The shared URLs.** The annotations of one check run share the run's URL, the run's own `check_run` item shares it too, and every status without a `target_url` shares the empty one.
   - **The rule.** Dispositions keyed by URL must refuse a shared key, and name items by an item-specific id (`item-<n>`).
5. [memory:failure] An EXIT trap that restores state must restore only what the script changed.
   - **The failure.** orch-gate.sh's trap ran `checkout --detach origin/main` unconditionally. A refusal before the script had touched the review worktree therefore still moved it.
   - **The fix.** Set a flag right before the first change, and condition the restore on it.
   - **The test.** It starts the worktree somewhere other than the restore target, so a restore that runs is visible.
6. [memory:failure] A mutation script whose patterns are written before `ruff format` runs can miss its target.
   - **The failure.** Here ruff wrapped a boolean expression across lines, and the replacement failed its count assertion.
   - **The fix.** Write mutation patterns against the formatted file, and keep the assertion that each pattern occurs exactly once, so a miss fails loudly instead of yielding a surviving no-op mutant.
