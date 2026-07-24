# T11 agmsg join unique-identity guard report

## Status

Ready for review.

## Result

- `join.sh` now removes `--same-agent` from any argv position before applying the existing four-positional-argument contract.
- Before creating a team directory or config, it scans sibling `teams/*/config.json` files and rejects an identity found in another team unless `--same-agent` is present.
- Rejection exits 1, lists every conflicting team, explains the project-suffixed-name and `--same-agent` choices, and writes nothing for the requested team.
- Same-team registration extension and explicit same-physical-agent cross-team joins retain the previous behavior.
- The header usage is documented with shdoc annotations.

## Files

- `home/dot_agents/skills/agmsg/scripts/executable_join.sh`
- `tests/unit/test_agmsg_join_unique_guard.py`

## Test-first evidence

Before the guard was implemented, the new cross-team scenario returned `second_status=0` and created `teams/beta/config.json`. After implementation, all four test functions pass through the direct local harness, including all five possible positions for `--same-agent`.

## Validation limitation

Both required `uv run pytest` commands stop before collection because this checkout does not provide a `pytest` executable. Dependency or network changes were forbidden, so pytest was not installed. The full command output and passing fallback evidence are in the validation artifact.

## Review notes

- Existing `join.sh` callers under `home/` and `.claude/` use exactly the existing four positional arguments; no STOP condition was found.
- No locking or registry abstraction was added. The single existing write path remains authoritative.
- `make require-crit-review` correctly requests native review. It was not bypassed; the orchestrator must complete Crit-data review because the required `.agents/worklog/...` evidence paths are outside this worker's allowed files.

## Withdrawn

The operator withdrew T11 in favor of the unique-per-project naming convention. Per acceptance `next_action`, `home/dot_agents/skills/agmsg/scripts/executable_join.sh` was restored and `tests/unit/test_agmsg_join_unique_guard.py` was deleted; no other file was discarded.

`git status --short` after the discard:

```text
 M home/dot_mise/config.toml
 M home/dot_mise/mise.lock
?? .orchestration/acceptance/plan-001.md
?? .orchestration/acceptance/plan-002.md
?? .orchestration/acceptance/plan-003-final-pr.md
?? .orchestration/acceptance/plan-003-review-round-1.md
?? .orchestration/acceptance/plan-003-review-round-2.md
?? .orchestration/acceptance/plan-003.md
?? .orchestration/autoskill/runs/T11-agmsg-join-unique-identity-guard.md
?? .orchestration/autoskill/runs/plan-001.md
?? .orchestration/autoskill/runs/plan-002.md
?? .orchestration/autoskill/runs/plan-003.md
?? .orchestration/learning/T11-agmsg-join-unique-identity-guard.md
?? .orchestration/learning/plan-001.md
?? .orchestration/learning/plan-002.md
?? .orchestration/learning/plan-003.md
?? .orchestration/learning/plan-004.md
?? .orchestration/reports/T11-agmsg-join-unique-identity-guard.md
?? .orchestration/reports/plan-001.md
?? .orchestration/reports/plan-002.md
?? .orchestration/reports/plan-003.md
?? .orchestration/reports/plan-004-inventory.md
?? .orchestration/reports/plan-004-stop.md
?? .orchestration/reports/plan-004.md
?? .orchestration/sandboxes/T11-agmsg-join-unique-identity-guard.md
?? .orchestration/sandboxes/plan-001.md
?? .orchestration/sandboxes/plan-002.md
?? .orchestration/sandboxes/plan-003.md
?? .orchestration/sandboxes/plan-004.md
?? .orchestration/tasks/T11-agmsg-join-unique-identity-guard.md
?? .orchestration/tasks/plan-001.md
?? .orchestration/tasks/plan-002.md
?? .orchestration/tasks/plan-003.md
?? .orchestration/validation/T11-agmsg-join-unique-identity-guard.md
?? .orchestration/validation/plan-001.md
?? .orchestration/validation/plan-002-crit-comments.json
?? .orchestration/validation/plan-002-crit-structure.json
?? .orchestration/validation/plan-002.md
?? .orchestration/validation/plan-003-pr-final.md
?? .orchestration/validation/plan-003.md
?? .orchestration/validation/plan-004.md
?? docs/verification/
?? plans/
```
