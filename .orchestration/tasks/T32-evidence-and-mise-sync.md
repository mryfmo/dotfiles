# Orchestration task: T32 sync T30/T31 evidence, mise bump, and codify the policy

## Assignment

- Task ID: `T32-evidence-and-mise-sync`
- Repo: `/Users/mryfmo/Workspace/dotfiles`
- Create a separate git worktree from `origin/main` (e.g. `git worktree add
../dotfiles-t32 -b chore/t30-t31-evidence-mise-sync origin/main`) and do
  ALL work there. The MAIN worktree stays untouched except the expected
  artifact paths.

## Objective (operator approved, 2026-07-25)

One PR containing exactly THREE commits, in this order:

### Commit 1 — `chore(mise): bump managed claude-code to 2.1.219`

Copy these two files from the MAIN worktree into the T32 worktree,
byte-identical (they carry the `make upgrade` write-back):

- `home/dot_mise/config.toml`
- `home/dot_mise/mise.lock`

### Commit 2 — `chore(orchestration): sync T30/T31 evidence`

Copy these THIRTEEN files from the MAIN worktree, byte-identical:

- `.orchestration/autoskill/runs/T30-orchestration-evidence-sync.md`
- `.orchestration/autoskill/runs/T31-codex-profile-modify-pattern.md`
- `.orchestration/learning/T30-orchestration-evidence-sync.md`
- `.orchestration/learning/T31-codex-profile-modify-pattern.md`
- `.orchestration/reports/T30-orchestration-evidence-sync.md`
- `.orchestration/reports/T31-codex-profile-modify-pattern.md`
- `.orchestration/sandboxes/T30-orchestration-evidence-sync.md`
- `.orchestration/sandboxes/T31-codex-profile-modify-pattern.md`
- `.orchestration/tasks/T31-codex-profile-modify-pattern.md`
- `.orchestration/validation/T30-orchestration-evidence-sync.md`
- `.orchestration/validation/T31-codex-profile-modify-pattern.md`
- `.orchestration/tasks/T32-evidence-and-mise-sync.md` (this file)
- (12 listed above plus this task file = 13; if the count on disk differs,
  STOP and report instead of improvising)

### Commit 3 — `docs(rules): codify evidence sync and tool bump timing`

Append ONE bullet to `home/dot_config/claude/rules/agmsg-orchestration.md`
(end of the list, English, single bullet, existing style):

> Sync `.orchestration` evidence in batches at regime or session
> boundaries via one chore task — the sync task's own artifacts remain as
> the converged one-task tail and are picked up by the next round — and
> commit `make upgrade` tool bumps (the mise config/lock pair) as their
> own chore commit in the same working session as the upgrade; never
> leave that pair dirty across sessions.

Wording may be lightly polished for grammar but must keep every element:
batch sync at regime/session boundaries, converged one-task tail,
next-round pickup, upgrade bumps committed same session as their own chore
commit, config/lock pair never left dirty across sessions.

## Constraints

- allowed_files: exactly the files named above (in the T32 worktree), plus
  the expected artifact paths below (MAIN worktree).
- forbidden_actions: `edits-outside-allowed-files;
content-modification-of-copied-files; git-push (until orchestrator
authorizes); chezmoi-apply; live-herdr-mutation; deps-or-ci-changes;
local-bats; llm-calls`

## Validation commands (full output into the validation artifact)

- `git -C <t32-worktree> log --oneline origin/main..HEAD` (exactly 3
  commits, subjects as specified)
- `git -C <t32-worktree> show --stat` for each commit (scope per commit)
- per-file `cmp` proof of byte-identity for every copied file
- `git -C <t32-worktree> status --short` (clean)
- `uv run --with pyyaml scripts/validate-agent-assets.py` (rule file is a
  validated asset — record output)

## Expected artifacts (exact paths, MAIN worktree)

- report: `.orchestration/reports/T32-evidence-and-mise-sync.md`
- validation: `.orchestration/validation/T32-evidence-and-mise-sync.md`
- sandbox: `.orchestration/sandboxes/T32-evidence-and-mise-sync.md`
- learning: `.orchestration/learning/T32-evidence-and-mise-sync.md`
- autoskill: `.orchestration/autoskill/runs/T32-evidence-and-mise-sync.md`

When done send:
`AGMSG-RESULT v1 task_id=T32-evidence-and-mise-sync status=ready_for_review report=... validation=... sandbox=... learning=... autoskill=... worktree=... branch=... commits=<3 hashes>`
Max turns: 12.
