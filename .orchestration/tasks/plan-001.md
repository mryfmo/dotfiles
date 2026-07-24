# AGMSG task: Plan 001

## Objective

Implement `plans/001-contain-starship-cleanup.md` in the isolated worktree.

## Allowed implementation files

- `install/ubuntu/server/starship.sh`
- `tests/install/ubuntu/server/starship.bats`

## Forbidden actions

- Do not edit files outside the allowed implementation files.
- Do not run Bats locally.
- Do not push, merge, open a PR, install dependencies, or modify the main worktree.
- Do not weaken or delete existing tests.

## Required validations

- `bash -n install/ubuntu/server/starship.sh tests/install/ubuntu/server/starship.bats`
- `shfmt -i 4 -sr -d install/ubuntu/server/starship.sh tests/install/ubuntu/server/starship.bats`
- `make unit-test`
- `rg -n 'rm -rf .*BIN_DIR|rm -rf .*\.local/bin' install tests` returns no matches

## Expected artifacts

- Report: `/Users/mryfmo/Workspace/dotfiles/.orchestration/reports/plan-001.md`
- Validation: `/Users/mryfmo/Workspace/dotfiles/.orchestration/validation/plan-001.md`
- Sandbox: `/Users/mryfmo/Workspace/dotfiles/.orchestration/sandboxes/plan-001.md`
- Learning: `/Users/mryfmo/Workspace/dotfiles/.orchestration/learning/plan-001.md`
- AutoSkill: `/Users/mryfmo/Workspace/dotfiles/.orchestration/autoskill/runs/plan-001.md`

## Completion

- Commit the two-file implementation in the isolated worktree using a Conventional Commit.
- Report COMPLETE or STOPPED with steps, files changed, validation results, and deviations.
