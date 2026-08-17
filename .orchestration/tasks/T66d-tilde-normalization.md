# T66d: send.sh lane — leading-tilde normalization (E2E-π1 round-3 finding)

task_id: T66d
repo: /Users/mryfmo/Workspace/dotfiles
team: dotfiles-conformance
worker: codex-deep-dot
plan: PLAN-pi-worker-integration.md (Phase 2; live finding round 3)
depends: T66c (accepted)

[memory: failure — E2E-π1 round 3: the worker created the artifact but its send.sh RESULT call was denied because the command used the `~/` form while the bash allow lane compares against the expanded absolute prefix only; bash expands a leading tilde at execution, so the two forms are semantically identical and the gate must normalize a LEADING `~/` before prefix comparison.]

## Live evidence

Session tool call:
bash `~/.agents/skills/agmsg/scripts/send.sh dotfiles-conformance
pi-standard-dot claude-deep-dot "AGMSG-RESULT v1 task_id=P1 ..."` ->
blocked; assistant reported "The required agmsg send command was blocked
by execution policy." hello.txt was created correctly (write lane OK).

## Fix (exact)

1. permgate pi bash lane: before the exact-prefix comparison, if the
   trimmed command begins with `~/`, replace ONLY that leading `~` with
   the home directory. No other tilde processing (no `~user`, no
   mid-string tildes). Metacharacter rejection unchanged and evaluated
   on the ORIGINAL string.
2. Tests: tilde-form send.sh with clean args ALLOW; absolute form still
   ALLOW (regression); `~user/` form NOT normalized (falls through);
   tilde form with `;` injection still not allowed; claude/codex goldens
   byte-identical.

## Allowed files

- home/dot_local/bin/common/executable_permgate
- tests/unit/ (matching module)
- Your artifact paths (T66d five artifacts)

## Forbidden actions

git commit; git push; chezmoi apply; bats; dependency changes; real pi
execution; any other lane change.

## Validation

make format / unit-test / validate-agent-assets green; diff pasted;
scope check.

## Completion / RESULT contract

Five artifacts; memory add (kind=failure); effects=none.
Reply `AGMSG-RESULT v1 task_id=T66d`. max_turns=10.
