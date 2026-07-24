# T28 report: ccgate removal and permgate live deployment

## Result

- Removed the ccgate mise pin, update lifecycle, version check allowlist entry, and positive lifecycle assertions.
- Preserved historical ccgate metrics in the permgate policy and retained every resurrection guard: managed executable cleanup, `.chezmoiremove`, validators, and regression tests.
- Ran the managed agent-assets lifecycle, deployed permgate to both live PermissionRequest hooks, and removed all installed ccgate versions plus its shim.
- Kept both providers in shadow mode (`llm_enabled: false`) and confirmed existing Claude deny/ask rules and Codex approval/sandbox settings were unchanged.
- Opened PR #93 without merging.

## Live verification

- `command -v ccgate`: absent.
- `mise ls` and `mise ls --installed`: no ccgate entry.
- Live mise config remains symlinked to the canonical source; an exact uncommitted shadow of the PR's pin removal keeps the pre-merge live state consistent.
- `~/.local/bin/common/permgate`: executable.
- Claude hook: `~/.local/bin/common/permgate claude`.
- Codex hook: `/Users/mryfmo/.local/bin/common/permgate codex`.
- Six live fixtures appended six redacted decision records:
  - safe reads: deterministic allow for Claude and Codex;
  - dangerous root deletion: deterministic deny for Claude and Codex;
  - ambiguous `gh issue view`: shadow/native ask for Claude and Codex.

## Pull request

- PR: https://github.com/mryfmo/dotfiles/pull/93
- Head: `0dc4ef1098da4c832ad38fe4c71e8a2d03eaf2fe`
- Branch: `chore/remove-ccgate`
- Merge: squash merged after acceptance as `f5c4846f1d5d6e8eba963a380f1899c1141a570f`.
- CI: all required GitHub Actions and CodeRabbit passed; Nix was skipped by workflow conditions.
- Mergeability: `MERGEABLE`; merge state: `CLEAN`.
- Local `main` was fast-forwarded to the merge commit, the dedicated worktree and local/remote task branches were removed, and the tracked tree is clean.
- Final `chezmoi apply` from merged main exited 0; `chezmoi diff` is empty.

## Review

- Adversarial review covered resurrection paths, metrics provenance, fail-closed behavior, lifecycle test inversion, and repository scope.
- Crit data contains a resolved finding-free approval record.
- `make require-crit-review` passed with the repository-local receipt.
