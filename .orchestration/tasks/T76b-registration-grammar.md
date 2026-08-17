# T76b: Enforce the identifier grammar at every registration boundary (PR #136 review)

task_id: T76b
repo: /Users/mryfmo/Workspace/dotfiles
team: dotfiles-conformance
worker: codex-deep-dot
plan: PLAN-pi-pivot.md (Phase 3; PR #136 review finding)
depends: T76 (accepted)

[memory: decision — The agmsg identifier grammar (^[a-z0-9][a-z0-9_-]{0,63}$) is enforced consistently at every boundary that creates or renames a team or identity (join, rename, team-rename), not only at send time, so a registration that succeeds can always exchange messages.]

## Finding (chatgpt-codex-connector, orchestrator-triaged REAL)

join.sh and rename.sh accept identifiers the new send.sh grammar rejects,
producing successfully registered teams/identities that cannot send —
a registration/send asymmetry.

## Fix (exact)

1. Inventory every script under home/dot_agents/skills/agmsg/scripts/
   that CREATES or RENAMES a team or identity (expect join.sh, rename.sh,
   rename-team.sh; enumerate what you actually find in the report).
2. Extract the grammar check into ONE shared helper (lib/ or a sourced
   fragment consistent with the existing lib/actas-lock.sh pattern) used
   by send.sh and every registration script — single source of truth,
   no per-script regex copies.
3. Each boundary rejects non-conforming team names and identity names
   with the same usage-style stderr line and exit 1, BEFORE any DB or
   config mutation.
4. Tests: extend the agmsg script tests — join/rename/team-rename reject
   a quote/space/uppercase identifier without mutating state; valid ones
   still work; send.sh behavior regression-kept; the helper is the only
   place the regex literal appears (grep-pinned test).
5. shdoc + shfmt + shellcheck on touched scripts.

## Allowed files

home/dot_agents/skills/agmsg/scripts/\*\* (registration scripts + shared
helper + send.sh only for the helper refactor), tests/unit, artifact
paths (T76b set).

## Forbidden actions

git commit; git push; chezmoi apply; bats; dependency changes; grammar
changes; touching non-registration scripts beyond the helper sourcing.

## Completion / RESULT contract

Five artifacts; memory add; effects=none; cost line in your report if
you can estimate tokens, else n/a.
Reply `AGMSG-RESULT v1 task_id=T76b`. max_turns=15.
