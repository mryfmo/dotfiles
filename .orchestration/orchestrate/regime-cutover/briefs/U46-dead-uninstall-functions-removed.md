# U46 The six dead `uninstall_*` installer functions leave the installers — brief (U45 follow-up)

GOAL
U45 (PR #507) measured six `uninstall_*` functions with no caller anywhere in the repository: `uninstall_chezmoi_private` (`install/common/chezmoi_private.sh:38`), macOS `uninstall_docker` (`install/macos/common/docker.sh:28`), `uninstall_docker_engine` (`install/ubuntu/client/docker.sh:78`), Ubuntu `uninstall_ghostty` (`install/ubuntu/client/ghostty.sh:51`), `uninstall_misc` (`install/ubuntu/client/misc.sh:40`), `uninstall_tailscale` (`install/ubuntu/client/tailscale.sh:47`). Dead code in an installer is a liability without a test; this unit removes the six functions and the comments that still name them, and proves nothing else changed.

SCOPE
One branch `chore/dead-uninstall-functions` from `origin/main` (the U45 merge or later). May write: the six installer files (the function bodies and any line that only exists for them: a `case` arm, a usage line, a comment), the Bats files whose comments name them (`docker.bats:12`, `ghostty.bats:12`, `misc.bats:12`, `tailscale.bats:12` per the U45 table), `README.md` or `docs/` only where a removed function is named. Nothing else; no change to any `install_*` function.

CHANGE
1. Re-run U45's inventory on the branch head (`git grep -n -w <name> -- . ':!.orchestration'` per function) and paste it: every function must still have zero callers before deletion; a new caller stops the unit.
2. Delete the six functions and their orphaned lines; keep each file's `main` and every `install_*` path byte-identical apart from the removed text (`git diff` of each installer shows removals only, plus at most a blank line; paste `git diff --stat` and a `grep -c '^+' <<< "$(git diff -- install/)"` of 0 or the explained additions).
3. If a removed function was the only consumer of a helper (a variable, a `PACKAGES` array read only by it), say so and leave the helper in place; its removal is not this unit's.

ACCEPTANCE
1. The inventory table with zero callers per function; the removal diff is deletions only (paste).
2. CI green on the head: the four test cells, the three public-bootstrap and three chezmoi-apply jobs (installers changed, the bootstrap runs in full); `make shellcheck` green (the installer group is under the rc since U38b).
3. PR body `Program-Unit: regime-cutover/U46`, a threat table (one row per installer: what the file still installs, unchanged; what left), the footer; pre-RESULT five-point self-check; audit seat (installers).

TIMEBOX
45 minutes.

FORBIDDEN
No change to any `install_*` function or its arguments; no new `# shellcheck disable`; no local Bats as evidence; no omp subagent; no merge, rebase, force-push, PR close.

REPORT
Per STANDING 12 plus the RESULT line (standing order 23).

STANDING
`~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` (lines 20 to 24).
