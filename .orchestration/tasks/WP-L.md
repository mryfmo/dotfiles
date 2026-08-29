# WP-L: Codify the delegation boundary in the agmsg-orchestration rule

task_id: WP-L
repo: /Users/mryfmo/Workspace/dotfiles
team: dotfiles-conformance
worker: codex-deep-dot

## Goal

Add one bullet to `home/dot_config/claude/rules/agmsg-orchestration.md` that codifies the delegation boundary the operator approved on 2026-08-29: the delegation mandate covers repository-mutating work only; control-plane operations, acceptance/final integration, and machine-state hygiene stay orchestrator-side, and direct action requires a one-line exemption declaration.

[memory:decision] The agmsg delegation mandate covers repository-mutating work only; control-plane ops, acceptance/final integration (including merging reviewed CI-green PRs), and non-repository machine hygiene are orchestrator-direct, with a one-line exemption declaration required.

Insert the following bullet verbatim, immediately AFTER the existing bullet that begins "- Delegate all repository-mutating work to resident Codex workers.":

```markdown
- The delegation mandate covers repository-mutating work only. Claude handles the following directly, without delegation: agmsg/herdr control-plane operations and evidence-sync bookkeeping; acceptance and final integration, including merging an already-reviewed, CI-green PR; and machine-state hygiene that touches no repository (tool-manager operations such as `mise install`/`mise prune`, removal of unmanaged `$HOME` files), provided tracked worktrees stay diff-clean throughout. When acting directly under an exemption, declare which exemption applies in one line before mutating anything.
```

Match the file's existing bullet formatting (single-line bullets; do not re-wrap neighboring bullets). Do not change any other bullet.

## Git / PR workflow

Follow repo AGENTS.md: create branch `chore/agmsg-delegation-boundary` from up-to-date `main`, commit the edit, push, and open a PR with an English title and description (suggested title: `chore(rules): codify agmsg delegation boundary and exemption declaration`). Check GitHub Actions CI after pushing; fix and re-push until green. Do not run bats locally.

If `make require-crit-review` exists and requires review for this diff, follow AGENTS.md "Agent Review Evidence": run an agent-side crit self-review, save `crit comments --all --json` evidence repo-locally, write a receipt, and rerun the guard with `AGENT_REVIEWED=1 REVIEW_EVIDENCE=<receipt>`.

## Allowed files (edit boundary)

home/dot_config/claude/rules/agmsg-orchestration.md, plus your artifact paths, worklog files under .agents/worklog/codex/, and crit review evidence files if the guard requires them.

## Forbidden actions

Merging the PR; chezmoi apply; editing any other rules file; dependency changes; running bats locally; touching `~/.config/claude/` or any rendered target outside the repo.

## Validation

1. `git diff main -- home/dot_config/claude/rules/agmsg-orchestration.md` shows exactly one added bullet at the specified position
2. `git status --porcelain` clean after commit (no untracked tail beyond expected artifacts)
3. PR URL and CI check results (all green)
4. CompactionDB: run `python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content "<the [memory:decision] fact above>"` and include the exact command in the report

## Expected artifacts

- report: .orchestration/reports/WP-L.md
- validation: .orchestration/validation/WP-L.txt
- sandbox: .orchestration/sandboxes/WP-L.md
- learning: .orchestration/learning/WP-L.md
- autoskill: .orchestration/autoskill/runs/WP-L.md (record "not-used" if unused)

## Done signal

AGMSG-RESULT v1 with status=ready_for_review (or blocked with report). max_turns=20. Include a `cost:` line in the report.
