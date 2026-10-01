# T43 sandbox record

- No container or VM isolation was used. All git work happened in
  `.claude/worktrees/worker-c` on `feat/orchestration-rules-T43` from
  origin/main 258339f, which was clean before the switch.
- Graph comparisons read committed graphs via `git show` into the session
  scratchpad. No `.ua/**` change.
- The unit test creates and removes a temporary git repository under the
  system temp dir.
- Network: `git push` of the task branch, `gh pr create` and `gh pr checks`.
  No `make update`, no local Bats, no force push, no merge.
- Writes outside the worktree were limited to the listed `.orchestration`
  artifacts and the CompactionDB `memory add`.

## Revision 3

- worker-c switched from `fix/orchestrator-pane-profile-args` (#217 merged as 262b492) to
  `feat/orchestration-rules-T43` after the orchestrator's go (PING 22:47:32Z). Before deleting
  the five T47 artifact copies, I confirmed with `cmp` that each was byte-identical to the
  committed copies in c8fc05c. The T45 sandbox record was left untouched.
- 12d3f80 (fix) + 681957f (`git merge origin/main`, no force push), pushed without `-u`.
- Unsandboxed: `make render-check`/`unit-test`/`validate-agent-assets` (uv cache; AF_UNIX
  test), `git push`, `gh`, CompactionDB `memory add` in the main checkout, and appending these
  main-checkout artifacts (the main working tree is outside the Bash sandbox write allowlist).
- The temporary pre-fix revert for the negative check happened only in the worktree and was
  restored byte-identical (`git diff --exit-code` exit 0) before any commit.

## Revision 4

- Same worktree and branch. 6b53337 sits directly on 681957f (base-ok held, so no merge).
  Pushed without `-u`.
- Unsandboxed: `uv run --with pyyaml scripts/generate-agent-configs.py` (regeneration, uv
  cache), the three make targets, `git push`, `gh`, the main-checkout CompactionDB entry, and
  these artifact appends.
- For the negative check, the r3 script was temporarily restored in the worktree with
  `git show 12d3f80:<path> > <path>`, then restored with `git checkout -- <path>`
  (`git diff --exit-code` exit 0) before any further step.

## Revision 5

- Same worktree and branch. c878b0d sits directly on 6b53337 (base-ok held, so no merge).
  Pushed without `-u`.
- Unsandboxed: the three make targets, `git push`, `gh`, the main-checkout CompactionDB
  entry, and these artifact appends.
- For the negative check, the r4 script was swapped in temporarily with
  `git show 6b53337:<path> > <path>` and then restored from a copy (`cmp` exit 0) before
  the commit.
