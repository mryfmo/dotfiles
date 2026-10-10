---
format: 2
task_id: dotfiles-T128-v1b-pr-caps-a01
kind: code
security: true
design_review:
  receipt: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round13.md
  design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md
allowed_files:
  - scripts/regime-check.sh
  - scripts/pr-caps.sh
  - tests/unit/test_pr_caps.py
  - home/dot_agents/skills/agmsg-orchestration/SKILL.md
invariants:
  INV-2: "a PR is mergeable only within the caps the CI regime job enforces from main's workflow (at most 15 changed files outside .orchestration/, 500 added lines outside tests/, .orchestration/ and the data list scripts/legacy-task-ids.txt, and 1000 added lines under tests/), and its task.md invariants equal the design's as a set of ids and byte-for-byte as sentences (the design read from main, never from the PR; a task id ending in -contract-a01 is compared with its implementing task's entry); the design file must be on main (through a boundary PR) before the implementing TASK is dispatched and the regime job fails closed when the design named by task.md is absent from main; exceeding a cap is a split, never a finding to disposition (the cap changes the unit of work: T116 +529 and T118 +881 would have been split)"
premises:
  - claim: the cap is computable from git alone on the base-branch checkout with the PR head fetched as data
    command: "git diff --numstat origin/main...origin/feat/task-validator | awk '$3 !~ /^(tests\\/|\\.orchestration\\/)/ {a+=$1} END {print a}'"
    output: "1827 (PR 313 would have been refused)"
  - claim: the task file names exactly one invariant for a code task, so the one-invariant rule is a count over the front matter the V1 validator already parses
    command: "awk '/^invariants:/{f=1;next} /^[a-z_]+:/{f=0} f && /^  INV-/' .orchestration/tasks/dotfiles-T128-v1-task-schema-a01.md | wc -l"
    output: "1"
---

# AGMSG-TASK dotfiles-T128-v1b-pr-caps-a01 — regime v3 wave V1b: PR caps in the main-pinned CI check

DRAFT; dispatched after V1c merges (it extends regime-check.sh). Implements T128 INV-2 only. Design tier (workflow). Claude seat, `.claude/worktrees/worker-c`, branch `feat/pr-caps` from `origin/main`.

## What to build

1. `scripts/pr-caps.sh <base> <head>`: prints `files=<n> added=<n>` from `git diff --numstat <base>...<head>`: the file count excludes `.orchestration/` (the worker's evidence directory of INV-8) and counts everything else including `tests/`; the added-line count excludes `tests/`, `.orchestration/` and the data list `scripts/legacy-task-ids.txt`; a third figure `tests_added=<n>` counts additions under `tests/` with its own cap of 1000; exits 1 with one line per breached cap (`files 20 > 15`, `added 1827 > 500`, `tests_added 1200 > 1000`); caps are three constants at the top, overridable by `PR_CAP_FILES`, `PR_CAP_ADDED` and `PR_CAP_TESTS_ADDED` for tests only. shdoc header. Under 60 lines.
2. `scripts/regime-check.sh` (V1's) gains two steps: `scripts/pr-caps.sh $(git merge-base origin/main pr/head) pr/head`, and a comparison of the PR's `.orchestration/<task id>/task.md` invariant ids with the design's `implementing_tasks` entry for that task id (read both with `uv run --no-project --with pyyaml python -c`, ten lines, no new script): the ids must equal, as a set, the invariant list the design's map assigns to that task id, and each sentence must equal the design's byte for byte (the design read from `main`'s checkout); when the design file named by the task.md's `design_review.design` is absent from `main`'s checkout the step fails closed with that message (design INV-2), never with a Python traceback. The design's "steps in regime.yml" live inside `regime-check.sh`; the workflow stays a thin caller. A boundary PR (`.orchestration/`-only diff) passes trivially because its added count is zero and it has no task.md.
3. `tests/unit/test_pr_caps.py`: a scratch repository with commits over and under each cap; the exclusion of `tests/` and `.orchestration/`; the invariant comparison against fixtures whose task.md names two invariants, one whose id is not in the design, and one whose sentence differs from the design's by one character. Each test fails when its rule is removed.
4. SKILL Orchestrator Playbook step 3: one sentence, the caps and that an over-cap PR is split, never dispositioned.

## Validation

`bash tests` via `make unit-test` or the module alone; `shellcheck scripts/pr-caps.sh`; `scripts/pr-caps.sh origin/main HEAD` on your own branch pasted (must pass); `invariant: INV-2 → …` lines.

## First commit

Copy this task file to `.orchestration/dotfiles-T128-v1b-pr-caps-a01/task.md` as the first commit; evidence files go under the same directory on the branch.

## Completion

Draft PR within 30 minutes (`feat(regime): refuse pull requests above the file and added-line caps`), CI, Bot wait, artifacts, `memory add`, RESULT via `agmsg-dispatch … claude-deep-dot w5:p1`. max_turns=8. Forbidden: anything else; `make update`; thread resolution.
