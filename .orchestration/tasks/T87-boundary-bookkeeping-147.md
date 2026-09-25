# T87 — Boundary bookkeeping after #147

## Objective

Close out the T86 regime boundary per the orchestration invariants: bring the
Understand-Anything knowledge graph current for merged PR #147, commit the
`.orchestration` audit tail, and land two pending drift chores — each change
class in its own PR (squash-merge convention: one commit per class).

Branch each PR from up-to-date `origin/main`, stage strictly by pathspec, and
never mix classes. Do not merge any PR — the orchestrator merges at
acceptance. Watch CI (`gh pr checks --watch`) on each PR until green.

## PR A — `chore(ua): incremental knowledge-graph update for #147`

- Run the incremental Understand-Anything update for the current HEAD
  (post-#147). Follow the plugin auto-update instructions at
  `~/.claude/plugins/cache/understand-anything/understand-anything/2.9.4/hooks/auto-update-prompt.md`
  and the same convention as commits #141/#144
  (`chore(ua): incremental knowledge-graph update for #NNN`).
- Commit `.ua/**` except `.ua/intermediate/` and `.ua/diff-overlay.json`
  (already gitignored).
- Include in the same PR every currently untracked `.orchestration/**` file
  (T86 task/report/validation/sandbox/learning/autoskill/acceptance, this T87
  task file, and your T87 artifacts once written) so the audit tail is zero.
  Known UA pitfalls from previous runs are in the repo memory/learning
  records (nested FingerprintStore, TreeSitterPlugin init, merge only
  reanalyzed files); consult `.orchestration/learning/` if the update
  misbehaves.

## PR B — `chore(agmsg): sync upstream template refresh into chezmoi source`

- Commit exactly one file: `home/dot_agents/skills/agmsg/templates/cmd.claude-code.md`
  (drift captured from the agmsg 2026-08-29 upstream update).

## PR C — `chore(mise): commit tool upgrade config/lock pair`

- Commit exactly two files: `home/dot_mise/config.toml`,
  `home/dot_mise/mise.lock` (leftover `make upgrade` bump; must be its own
  commit per the boundary invariant).

## Allowed files

- `.ua/**` (minus gitignored paths), `.orchestration/**`
- `home/dot_agents/skills/agmsg/templates/cmd.claude-code.md`
- `home/dot_mise/config.toml`, `home/dot_mise/mise.lock`
- `.agents/worklog/codex/**`
- T87 artifacts:
  `.orchestration/reports/T87-boundary-bookkeeping-147.md`
  `.orchestration/validation/T87-boundary-bookkeeping-147.md`
  `.orchestration/sandboxes/T87-boundary-bookkeeping-147.md`
  `.orchestration/learning/T87-boundary-bookkeeping-147.md`
  `.orchestration/autoskill/runs/T87-boundary-bookkeeping-147.md`

## Forbidden actions

- Mixing change classes across the three PRs; editing any other path;
  merging PRs; force-push; local bats; dependency changes.

## Validation (record in the validation file)

- `git show --stat` per PR proving class-pure staging.
- `gh pr checks <pr>` final state for all three PRs.
- Post-run `git status --short` showing no untracked `.orchestration` tail
  (except artifacts created after PR A's final push, which you must amend or
  follow up into PR A before requesting review).

## Expected result

`AGMSG-RESULT v1 task_id=T87 status=ready_for_review` with artifact paths and
the three PR numbers + CI states in the report. cost line required.

max_turns=30
