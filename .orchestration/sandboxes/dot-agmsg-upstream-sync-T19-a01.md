# Sandbox

OpenSandbox not used.

- Writes: this worktree (`.claude/worktrees/worker-b`), branch `feat/agmsg-upstream-sync` (6 commits); pushed the branch; created PR #184. Scratch-`$HOME` E2E writes under the session scratchpad directory only (real network fetches of upstream's public tarball/registry, real `install.sh` runs, real `join.sh`/`identities.sh`/`doctor.sh`/`team.sh` calls) — never the real `$HOME`.
- Read-only `herdr pane list` against the live, shared herdr server to confirm it existed before deciding not to attempt deliverables 6(b)/6(c) against it; no pane created, closed, or mutated.
- Not run: `make update`, `make upgrade`, `chezmoi apply` (real HOME), `install.sh` against the real HOME, local bats, force-push. No merge, no vendoring of upstream scripts.

## Revision 2

- Rebased `feat/agmsg-upstream-sync` onto `origin/main` (`3375fb0`); no other branch touched.
- New scratch-`$HOME` writes (session scratchpad only, never real `$HOME`): a fresh v1.5.0 install for Fix 5's `join.sh`/`whoami.sh`/`session-start.sh` reproduction, including one background `exec -a claude sleep 300` process (a fake agent process for the marker-liveness test) killed afterward.
- A second, separate scratch `$HOME` + scratch chezmoi config/cache for Fix 3's `.chezmoiremove` verification: `chezmoi apply` (both `--dry-run` and real, `--exclude=scripts` to skip an unrelated sudo-gated ubuntu bootstrap script) ran only against that scratch destination, never the real `$HOME`.
- One CompactionDB `memory add --kind decision --scope project` write (repo-local, gitignored ledger).
- Not run this round either: `make update`/`make upgrade`/`chezmoi apply` against the real `$HOME`, local bats, force-push, merge.
