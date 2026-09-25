# AGMSG-TASK dot-task-contract-v2-T23-a01: immutable, versioned task specs (Message Contract v2)

## Root cause being fixed (2026-09-25 23:1xZ)
Task specs are distributed as a bare `task_file=<path>` with no revision or hash. The orchestrator appended a "G7/G8 addendum" to a task file in the main checkout without committing; worker-c read its own worktree's committed copy (a6df24c) and correctly reported "no addendum exists". Two contents existed under one path and the protocol could not say which was authoritative. This is a defect of Message Contract v1 in `home/dot_agents/skills/agmsg-orchestration/SKILL.md`, not a one-off.

## Deliverables
1. **Task file header** (front matter): `task_id`, `revision` (integer), `supersedes` (previous revision or none), `created_at`. Content of a revision is immutable; changes create a new revision section or file (`<task>.rN.md`) — never an in-place edit of a dispatched revision.
2. **Message fields**: `AGMSG-TASK v2` and `AGMSG-ACCEPTANCE v2 status=revise` carry `task_rev=<sha256 of the task file>` and `task_commit=<commit that contains it>`. Worker Playbook step 2: `sha256sum` the file at `task_commit` (or the absolute path) and compare; mismatch → `AGMSG-RESULT status=blocked reason=task-rev-mismatch` without doing work.
3. **Dispatch precondition**: the orchestrator's send wrapper (`agmsg-dispatch` now; the upstream-based wrapper after T19) refuses to send a TASK/revise when `git -C <repo> status --porcelain -- <task_file>` is non-empty or the file is not in `origin/main`; it computes `task_rev` itself so the orchestrator cannot forget it.
4. **Validation**: `scripts/validate-agent-assets.py` checks every `.orchestration/tasks/*.md` for the header; unit tests for the wrapper precondition and for the worker-side check (fixture task files); SKILL Orchestrator/Worker Playbooks and the rules file updated; migration note for existing v1 task files (grandfathered, listed).
5. pr-feedback sweep + CodeRabbit full review on the final head per pr-integration.

## allowed_files
`home/dot_agents/skills/agmsg-orchestration/SKILL.md`, `home/dot_config/claude/rules/agmsg-orchestration.md` (+ Codex mirror), `home/dot_local/bin/common/executable_agmsg-dispatch` (or its successor), `scripts/validate-agent-assets.py`, tests, README, artefacts.

## forbidden_actions
editing existing dispatched task files' content (add revisions instead); `make update`; merging; local bats; force-push.

## Artefacts / Done signal
Standard five + pr-feedback JSON. `[memory:decision]`: "task specs are immutable per revision; TASK messages carry task_rev/task_commit; workers verify before starting; the dispatcher refuses uncommitted task files". RESULT via send.sh. max_turns=40.
