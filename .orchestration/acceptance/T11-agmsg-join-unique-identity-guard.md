# T11 agmsg join unique-identity guard — WITHDRAWN

**Verdict: WITHDRAWN by operator decision (2026-07-16, Asia/Tokyo)**

## Decision

The operator ruled that identity-name uniqueness and multi-project session
separation are handled by a naming/registration convention, not by code:

1. One physical agent = one unique identity name:
   `<runtime>-<model+effort>-<project-suffix>` (e.g. `codex-gpt56sol-dot`,
   `codex-gpt56sol-flue`; task-scoped workers add `-aNNN`).
2. Registration `project` is always the real repo path — `$HOME`
   registrations are forbidden. With zero `$HOME` registrations, the codex
   global hook resolution key `(codex, $HOME)` matches nothing, so the
   check-inbox "use first identity on multi-match" path is structurally
   unreachable.
3. Worker delivery is explicit nudge (team + identity named); automatic turn
   delivery is not relied upon.
4. Concurrent resident workers use separated stores (`AGMSG_STORAGE_PATH`).

The T11 code guard (join.sh cross-team deny) and the T12 env-pinning proposal
were both withdrawn under this ruling.

## Review findings before withdrawal (for the record)

- Implementation quality was good: exact-match via `json_each`, deny before
  any write, `--same-agent` positional-contract preserved.
- One blocking defect found: the test was pytest-style, invisible to this
  repo's runner (`make unit-test` = `python -m unittest discover`) — it would
  never execute (vacuous evidence). Root cause: the orchestrator's task spec
  wrongly mandated pytest against repo convention. Revision 1 was drafted but
  superseded by the withdrawal.

## Cleanup evidence

- Worker discarded `executable_join.sh` changes (`git restore`) and deleted
  `tests/unit/test_agmsg_join_unique_guard.py`; confirmed by orchestrator:
  `git status` shows only pre-existing `home/dot_mise/*` modifications.
- Retired `codex-gpt55-high` (with its `$HOME` registration) removed from
  team `dotfiles-conformance` via `leave.sh`; message history retains its
  name (leave edits team config only).
- Remaining `$HOME` registrations exist only in team `ai-ops-platform`
  (`orchestrator-fable5`, `codex-gpt56sol-high`) — operator decision pending.
