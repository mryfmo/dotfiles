---
format: 2
task_id: dotfiles-T128-ci-skip-redesign-a01
kind: review
security: false
---

# AGMSG-TASK dotfiles-T128-ci-skip-redesign-a01 — the reset redesign of A5 (INV-6: the second round)

Drafted 2026-10-11 07:2xZ by the orchestrator seat. `dotfiles-T128-ci-skip-orchestration-a01` (PR #320, worker `claude-standard-dot-a003`) has two RESULTs (456 at `d6343494`, 485 at `dc4e6c37`: revises=1) and one amendment; the second audit (`.orchestration/validation/dotfiles-T128-ci-skip-orchestration-a01-audit-dc4e6c3.md.last.md`) found the same class a second time (the hand-written workflow reader misses valid block-style YAML forms: `if : false`, `"\x69f": false`, `continue-on-error : true`, after the first audit's quoted keys) and re-raised the design-on-main finding (main at `b896d9bc` holds neither this task's `implementing_tasks` entry nor its INV-2 sentence). Any further round reaches an INV-6 threshold; the rule's path is a reset. You write the successor; this is read-only.

## What to produce

The complete text of `dotfiles-T128-ci-skip-orchestration-a02.md`: the a01 file at sha256 `8e9c23daf670ab73dc26603cfbc4001fd3bbbd560829a46fa3a163c21f6c76a7` (`.orchestration/tasks/dotfiles-T128-ci-skip-orchestration-a01.md`) with exactly these changes:

1. `task_id: dotfiles-T128-ci-skip-orchestration-a02`; `reset_of: [dotfiles-T128-ci-skip-orchestration-a01]`; `after: [orchestration/boundary-2026-10-11-2]` (the boundary PR that puts design v16 on `main`; the worker's first push waits for nothing, but the PR takes the new base with `gh pr update-branch` once that boundary merges and before its audit).
2. Threat table, replacing the "a required job is skipped" and "the decision step itself fails" rows' test wording where it names the reader: a new row "the hand-written workflow reader misses a valid YAML form (quoted, escaped or spaced keys, flow mappings)" → `closed:` the reader fails closed: any key line of a job or step mapping that is not the plain form `name:` (lower-case letters, digits, `_` and `-`, the colon immediately after, no quotes, no escapes, no flow mapping) fails the structural tests outright, so an unsupported form can never read as "no `if`"; tests with `if : false`, `"\x69f": false`, `continue-on-error : true` and a flow mapping `{ if: false }` each fail the structural tests. (A real YAML parser is the alternative only if the test environment gains one; the task does not add a dependency.)
3. A new row "the task's invariant sentence and map entry are not on `main` at dispatch (INV-2)" → `closed:` design v16 lands on `main` through the boundary PR named in `after:`; this PR merges only after `gh pr update-branch` onto that `main`, and its final audit runs on that head; test: none (the acceptance record pastes `git show origin/main:.orchestration/tasks/dotfiles-T128-regime-v3-a01.md | sha256sum`).
4. Item 2 of "What to build" gains the fail-closed reader rule; the Validation list gains the four unsupported-form mutations; a "History" paragraph (a01: amendment 1 turned the `changes`-job pattern into the in-job fail-closed decision; revise round 1 closed rename detection and quoted keys; this reset closes the reader class as a whole and the design-on-main prerequisite); the worker's first commit copies the file byte-identical to `.orchestration/dotfiles-T128-ci-skip-orchestration-a02/task.md` (the a01 directory stays), same branch `feat/ci-skip-orchestration` and PR #320 from `dc4e6c37`.

## Output

`.orchestration/validation/dotfiles-T128-ci-skip-redesign-a01.md` with the usual header and the whole a02 file in one non-empty four-backtick block (plain scalars with a colon-space must be quoted; check with `wc -l` and a YAML parse before sending), then `AGMSG-RESULT v1 task_id=dotfiles-T128-ci-skip-redesign-a01 status=ready_for_review verdict=redesign receipt=<path> receipt_sha256=<sha256> a02_expected_sha256=<sha256 of the block plus a trailing newline>` via `agmsg-dispatch dotfiles-conformance claude-review-dot-a001 claude-deep-dot w5:p1`. The orchestrator writes the file and asks for the one confirmation (`verdict=accept design_sha256=<hash>`). max_turns=3. Forbidden: editing tracked files; branches; PRs.
