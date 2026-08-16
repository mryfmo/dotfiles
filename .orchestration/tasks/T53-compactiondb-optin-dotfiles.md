# T53: Opt dotfiles into CompactionDB + codify the regime-activation trigger

task_id: T53
repo: /Users/mryfmo/Workspace/dotfiles
team: dotfiles-conformance
worker: codex-deep-dot

[memory: decision — agmsg orchestration regime activation in a repository is a standing trigger to verify CompactionDB opt-in and install it if missing; the dotfiles repository itself is now opted in.]

## Goal

1. Opt this repository into CompactionDB with the freshly distributed
   2.0.0+dotfiles.4 runtime.
2. Codify the new trigger rule: when the agmsg orchestration regime
   activates in a repo, the orchestrator verifies CompactionDB opt-in and
   installs it if missing (operator-initiated regime start = consent).

## Allowed files

- Files created/modified by `compactiondb-install` at repo root ONLY:
  .claude/settings.json, .claude/hooks/contextdb\_\*.py + query_log.py,
  .claude/contextdb/\*\* (runtime + config; state/spool/health stay
  gitignored), CLAUDE.md (appended snippet), .gitignore (appended lines)
- home/dot_config/claude/rules/agmsg-orchestration.md (one bullet)
- home/dot_config/claude/rules/compactiondb.md (one bullet)
- Your artifact paths (T53 five artifacts)

## Forbidden actions

git commit; git push; chezmoi apply; bats; dependency changes; editing
vendor/; running memory add (the orchestrator backfills decisions);
touching .claude/settings.local.json (agmsg delivery owns it).

## Work order

1. Run `~/.local/bin/common/compactiondb-install /Users/mryfmo/Workspace/dotfiles`
   and paste its full output in the validation artifact.
2. Verify: `.claude/contextdb/config.json` has max_chars 12000 /
   files_budget_chars 2000 (dotfiles.4 defaults);
   `python3 .claude/hooks/contextdb_cli.py health` runs clean;
   `git status --porcelain` shows ONLY committable install artifacts
   (settings.json, hooks, runtime, config, CLAUDE.md, .gitignore) plus
   your artifacts — no state/spool/health files (they must be ignored;
   prove with `git check-ignore .claude/contextdb/state/context.db` style
   checks on the state dir).
3. Confirm the install merged (not clobbered) any existing
   .claude/settings.json content, and that .claude/settings.local.json is
   untouched.
4. Rules (match existing bullet style, English):
   - agmsg-orchestration.md: on regime activation, verify CompactionDB
     opt-in for the repo and install via `compactiondb-install` if
     missing (regime start is operator-initiated consent); acceptance-time
     decision consolidation then applies.
   - compactiondb.md: extend the opt-in bullet: agmsg regime activation is
     a standing install trigger for the active repo.
5. `make validate-agent-assets` green; `make format` still exit 0.

## Validation

Install output, config/health checks, ignore proofs, settings merge
evidence, git status/diff scope, rule diffs, gate outputs — all in the
validation artifact.

## Completion / RESULT contract

Five artifacts (T53). Report uses [memory:...] markers but does NOT run
memory add (DB writes are the orchestrator's backfill step).
Reply AGMSG-RESULT v1 task_id=T53. max_turns=15.
