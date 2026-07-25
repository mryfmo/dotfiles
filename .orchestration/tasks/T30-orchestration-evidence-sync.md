# Orchestration task: T30 sync T29 orchestration evidence

## Assignment

- Task ID: `T30-orchestration-evidence-sync`
- Repo: `/Users/mryfmo/Workspace/dotfiles`
- The main worktree is dirty with UNRELATED changes (`home/dot_mise/*`).
  Create a separate git worktree from `origin/main` (e.g. `git worktree add
../dotfiles-t30 -b chore/t29-evidence-sync origin/main`) and do ALL work
  there.

## Objective

Commit the T29 orchestration evidence (operator approved, 2026-07-25). Copy
these six untracked files from the MAIN worktree into the same paths in the
T30 worktree, byte-identical, then commit:

- `.orchestration/tasks/T29-agmsg-regime-default-on.md`
- `.orchestration/tasks/T30-orchestration-evidence-sync.md` (this file)
- `.orchestration/reports/T29-agmsg-regime-default-on.md`
- `.orchestration/validation/T29-agmsg-regime-default-on.md`
- `.orchestration/sandboxes/T29-agmsg-regime-default-on.md`
- `.orchestration/learning/T29-agmsg-regime-default-on.md`
- `.orchestration/autoskill/runs/T29-agmsg-regime-default-on.md`

Commit message (Conventional Commit, English), suggested:
`chore(orchestration): sync T29 regime default-on evidence`

## Constraints

- allowed_files: exactly the seven paths above (in the T30 worktree), plus
  the expected artifact paths below (MAIN worktree).
- forbidden_actions: `edits-outside-allowed-files; content-modification-of-
copied-evidence; git-push (until orchestrator authorizes); chezmoi-apply;
live-herdr-mutation; deps-or-ci-changes; local-bats; llm-calls`

## Validation commands (full output into the validation artifact)

- `git -C <t30-worktree> status --short` (clean after commit)
- `git -C <t30-worktree> show --stat HEAD`
- `diff -r` (or per-file `diff`) between each copied file and its main
  worktree original, proving byte-identity

## Expected artifacts (exact paths, MAIN worktree)

- report: `.orchestration/reports/T30-orchestration-evidence-sync.md`
- validation: `.orchestration/validation/T30-orchestration-evidence-sync.md`
- sandbox: `.orchestration/sandboxes/T30-orchestration-evidence-sync.md`
- learning: `.orchestration/learning/T30-orchestration-evidence-sync.md`
- autoskill: `.orchestration/autoskill/runs/T30-orchestration-evidence-sync.md`

When done send:
`AGMSG-RESULT v1 task_id=T30-orchestration-evidence-sync status=ready_for_review report=... validation=... sandbox=... learning=... autoskill=... worktree=... branch=... commit=...`
Max turns: 10.
