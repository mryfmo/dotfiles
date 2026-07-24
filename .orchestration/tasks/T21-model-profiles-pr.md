# T21: Land pending working-tree changes as PR feat/model-profiles (CI green)

## Objective

Make everything currently pending in the dotfiles working tree land on `main`
so that `make update` / `make upgrade` apply the full state from a clean
checkout. Create a separate worktree branch, transfer ONLY the enumerated
changes, verify, commit in two logical commits, push, open a PR (English), and
drive GitHub Actions CI to green. Do NOT merge until the orchestrator sends
`AGMSG-ACCEPTANCE status=accepted next_action=merge`.

## Background

Two completed-but-uncommitted workstreams sit in /Users/mryfmo/Workspace/dotfiles:

- A) upgrade tooling: mise pin bumps, skip `mise upgrade` for pinned `http:*`
  tools, npm `--allow-scripts` repair, removal of npm-global agent CLI shadows,
  `check_for_update_on_startup=false` rendering.
- B) model profiles: `model_profiles` in `home/dot_agents/agent-config.yaml` as
  the single source of model IDs/efforts; generator renders Claude settings,
  per-profile `~/.codex/<name>.config.toml`, `~/.agents/model-profiles.env`,
  `express-explorer` subagent; launchers de-hardcoded; ccgate PermissionRequest
  hooks removed (incl. jsonnet deletion + `home/.chezmoiremove`); validator,
  runtime doctor, docs, tests updated.

All 180 unit tests, `generate-agent-configs.py --check`, and
`make validate-agent-assets` pass in the main worktree. Bats runs in CI only.

## Steps

1. From /Users/mryfmo/Workspace/dotfiles:
   - `git diff --binary --cached > /tmp/T21-staged.patch` (holds the 2 ccgate.jsonnet deletions)
   - `git diff --binary > /tmp/T21-unstaged.patch`
2. `git worktree add ../dotfiles-model-profiles origin/main -b feat/model-profiles`
3. In the new worktree: `git apply --index /tmp/T21-staged.patch` then
   `git apply /tmp/T21-unstaged.patch`.
4. Copy these untracked new files from the main worktree (same relative paths):
   - `home/.chezmoiremove`
   - `home/dot_agents/model-profiles.env`
   - `home/dot_claude/agents/express-explorer.md`
   - `home/dot_codex/deep.config.toml`, `home/dot_codex/express.config.toml`,
     `home/dot_codex/review.config.toml`, `home/dot_codex/standard.config.toml`
     Do NOT bring over `docs/verification/`, `plans/`, `.orchestration/`,
     `.agents/`, `.crit/`, or anything else untracked.
5. Verify in the worktree (log all output to the validation artifact):
   - `uv run --with pyyaml scripts/generate-agent-configs.py --check`
   - `make unit-test`
   - `make validate-agent-assets`
   - `shellcheck home/dot_local/bin/common/executable_herdr-agents home/dot_local/bin/common/executable_agent-fanout`
   - `git status --short` must show exactly the enumerated files.
6. Commit 1 — `chore(tooling): harden mise/npm upgrade path and bump pinned tools`:
   `home/dot_mise/config.toml`, `home/dot_mise/mise.lock`,
   `scripts/upgrade-tools.sh`, `scripts/update-agent-assets.sh`,
   `install/macos/common/misc.sh`, `tests/install/macos/common/misc.bats`.
7. Commit 2 — `feat(agents): govern model selection via manifest model profiles and disable inactive ccgate hooks`:
   everything else (including shared test files and generated artifacts).
8. `git push -u origin feat/model-profiles`, then `gh pr create` with an
   English title/body: summarize both workstreams, note ccgate hooks are
   disabled (100% fallthrough, no classifier credential) and model IDs now
   live only in `model_profiles`.
9. Watch CI (`gh pr checks <pr> --watch` or `gh run watch`). On failure:
   diagnose, fix within Allowed files, push, repeat until all checks pass.
10. Write artifacts (paths below) and send AGMSG-RESULT. Do not merge yet.

## After acceptance (only when AGMSG-ACCEPTANCE next_action=merge arrives)

1. `gh pr merge <pr> --squash --delete-branch` (or `--merge` if the repo
   setting rejects squash).
2. In /Users/mryfmo/Workspace/dotfiles: `git fetch origin` and confirm
   `git diff origin/main --stat -- <the enumerated tracked files>` is EMPTY
   (identical content landed). Only if empty: `git reset --hard origin/main`
   and `git worktree remove ../dotfiles-model-profiles`. If not empty, STOP
   and report the difference instead of resetting.
3. Send a final AGMSG-RESULT with the merge commit and sync evidence appended
   to the same artifacts.

## Allowed files

- The new worktree `../dotfiles-model-profiles`: only the files enumerated by
  `git status --short` in the main worktree today (27 modified/deleted tracked
  files + the 7 untracked files listed in step 4). CI fixes must stay within
  this same set; if a fix requires another file, report blocked instead.
- Main repo artifacts: the expected report/validation/sandbox/learning/autoskill
  paths below, and `/tmp/T21-*.patch`.
- Main repo git state: only the post-acceptance sync in the section above.

## Forbidden actions

- Merging the PR before AGMSG-ACCEPTANCE with next_action=merge.
- Running bats locally (CI only, per AGENTS.md).
- `chezmoi apply`, `make update`, `make upgrade` (orchestrator runs these at
  final integration).
- Editing `~/.claude`, `~/.codex`, `~/.agents` runtime state.
- Force-push to main; rebase of main; `git reset --hard` outside the guarded
  post-acceptance step; committing `.orchestration/`, `.agents/`, `.crit/`,
  `docs/verification/`, `plans/`.
- Secrets, tokens, or raw auth state in commits or artifacts.
- Dependency additions, product-behavior changes beyond the transferred diff.

## Expected artifacts

- report: .orchestration/reports/T21-model-profiles-pr.md (PR URL, commit SHAs, CI run links, decisions)
- validation: .orchestration/validation/T21-model-profiles-pr.txt (command outputs)
- sandbox: .orchestration/sandboxes/T21-model-profiles-pr.md (sandbox status or fallback rationale)
- learning: .orchestration/learning/T21-model-profiles-pr.md (triage; do not promote rules)
- autoskill: .orchestration/autoskill/runs/T21-model-profiles-pr.md (run status or not-used record)

## Done signal

AGMSG-RESULT v1 with status=ready_for_review (or blocked) and all artifact paths.
max_turns=40
