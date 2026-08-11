# T39: Align the herdr bats pin with the committed toolchain bump

## Objective

PR #113 CI fails because `tests/install/common/mise.bats:131` greps for
`"github:ogulcancelik/herdr" = "0.7.5"` while the mise pair commit on
`chore/orchestration-evidence-t35-t37` bumps herdr to `0.8.0`.

## Steps (exact)

1. `git checkout chore/orchestration-evidence-t35-t37` (leave the dirty
   tracked T37/PR-112 files alone; they carry over harmlessly).
2. In `tests/install/common/mise.bats`, change the herdr pin from `0.7.5` to
   `0.8.0` (single line). Confirm no other file pins `0.7.5` for herdr.
3. Commit exactly that one file: `test(mise): align herdr pin with 0.8.0 toolchain bump`.
4. `git checkout main`. Do not push.

## Forbidden actions

- No push, no PR ops, no other file edits, no bats execution.

## Expected artifacts

Append a short `## T39` section to the existing T38 artifact files
(report/validation/sandbox/learning/autoskill) instead of creating new ones —
this is a CI-fix rider on the same sync batch. Validation: `git show --stat`
of the new commit and the grep proving the new pin.

## Done signal

`AGMSG-RESULT v1 task_id=T39-herdr-pin-fix status=ready_for_review|blocked`
(reuse the T38 artifact paths). Max turns: 8.
