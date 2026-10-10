---
format: 2
task_id: dotfiles-T128-v1b-pr-caps-a01
kind: code
security: true
design_review:
  receipt: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review.md
  design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md
allowed_files:
  - scripts/regime-check.sh
  - scripts/pr-caps.sh
  - tests/unit/test_pr_caps.py
  - home/dot_agents/skills/agmsg-orchestration/SKILL.md
invariants:
  INV-2: "a PR is mergeable only within the caps the CI regime job enforces from main's workflow (at most 15 changed files and 500 added lines outside tests/, .orchestration/ and the data list scripts/legacy-task-ids.txt), and its task.md invariant ids equal the design's implementing_tasks entry for that task id (a map of task id to invariant ids inside the hashed keys); the design file must be on main (through a boundary PR) before the implementing TASK is dispatched and the regime job fails closed when the design named by task.md is absent from main; exceeding a cap is a split, never a finding to disposition (the cap changes the unit of work: T116 +529 and T118 +881 would have been split)"
premises:
  - claim: the cap is computable from git alone on the base-branch checkout with the PR head fetched as data
    command: "git diff --numstat origin/main...origin/feat/task-validator | awk '$3 !~ /^(tests\\/|\\.orchestration\\/)/ {a+=$1} END {print a}'"
    output: "1827 (PR 313 would have been refused)"
  - claim: the task file names exactly one invariant for a code task, so the one-invariant rule is a count over the front matter the V1 validator already parses
    command: "awk '/^invariants:/,/^[a-z_]+:/' .orchestration/tasks/dotfiles-T128-v1-task-schema-a01.md | grep -c '^  INV-'"
    output: "1"
---

# AGMSG-TASK dotfiles-T128-v1b-pr-caps-a01 — regime v3 wave V1b: PR caps in the main-pinned CI check

DRAFT; dispatched after V1 merges (same workflow file). Implements T128 INV-2 only. Design tier (workflow). Claude seat, `.claude/worktrees/worker-c`, branch `feat/pr-caps` from `origin/main`.

## What to build

1. `scripts/pr-caps.sh <base> <head>`: prints `files=<n> added=<n>` from `git diff --numstat <base>...<head>` excluding `tests/`, `.orchestration/` and the data list `scripts/legacy-task-ids.txt` from the added-line count (every changed path counts toward files), exits 1 with one line per breached cap (`files 20 > 15`, `added 1827 > 500`); caps are two constants at the top, overridable by `PR_CAP_FILES` and `PR_CAP_ADDED` for tests only. shdoc header. Under 60 lines.
2. `scripts/regime-check.sh` (V1's) gains two steps: `scripts/pr-caps.sh $(git merge-base origin/main pr/head) pr/head`, and a comparison of the PR's `.orchestration/<task id>/task.md` invariant ids with the design's `implementing_tasks` entry for that task id (read both with `uv run --no-project --with pyyaml python -c`, ten lines, no new script): the ids must be exactly the invariant set the design assigns to that task, one invariant per implementing task. A boundary PR (`.orchestration/`-only diff) passes trivially because its added count is zero and it has no task.md.
3. `tests/unit/test_pr_caps.py`: a scratch repository with commits over and under each cap; the exclusion of `tests/` and `.orchestration/`; the invariant-set comparison against a fixture whose task.md names two invariants and one whose id is not in the design. Each test fails when its rule is removed.
4. SKILL Orchestrator Playbook step 3: one sentence, the caps and that an over-cap PR is split, never dispositioned.

## Validation

`bash tests` via `make unit-test` or the module alone; `shellcheck scripts/pr-caps.sh`; `scripts/pr-caps.sh origin/main HEAD` on your own branch pasted (must pass); `invariant: INV-2 → …` lines.

## First commit

Copy this task file to `.orchestration/dotfiles-T128-v1b-pr-caps-a01/task.md` as the first commit; evidence files go under the same directory on the branch.

## Completion

Draft PR within 30 minutes (`feat(regime): refuse pull requests above the file and added-line caps`), CI, Bot wait, artifacts, `memory add`, RESULT via `agmsg-dispatch … claude-deep-dot w5:p1`. max_turns=8. Forbidden: anything else; `make update`; thread resolution.
