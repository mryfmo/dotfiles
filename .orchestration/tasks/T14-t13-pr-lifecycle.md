# Orchestration task: T14 push + PR for rule/agmsg-orchestration

## Assignment

- Task ID: `T14-t13-pr-lifecycle`
- Executor model: `gpt-5.6-sol`
- Reasoning effort: `high`
- Repo: `/Users/mryfmo/Workspace/dotfiles`, branch `rule/agmsg-orchestration`
  (HEAD `c4f80cf`, one commit ahead of `main`)

## Objective (phase 1 of the PR lifecycle)

1. Push the branch: `git push -u origin rule/agmsg-orchestration`.
2. Create the PR with `gh pr create --base main` — title and body in ENGLISH.
   - Title: `feat(claude-rules): add agmsg orchestration rule and fix ponytail symlink`
   - Body: summarize the FULL PR content (rule file purpose: always-on
     Claude-orchestrator/Codex-worker agmsg regime — delegation boundaries,
     delivery/liveness via both-mode delivery + Monitor, unique
     identity/registration convention; symlink template wiring it into
     `~/.claude/rules/`; ponytail symlink dead-target fix found in review).
     Use repository-relative paths only. End the body with the line:
     `🤖 Generated with [Claude Code](https://claude.com/claude-code)`
3. Record the PR URL and `gh pr view --json url,number,headRefOid` output in
   the validation artifact.
4. Do NOT merge, do NOT respond to CI or bots — the orchestrator reviews CI
   and bot comments and will authorize fixes and the merge in later phases.

## Constraints

- allowed_files: the artifact paths below only (no repo file edits in this phase)
- forbidden_actions: `merge; force-push; new-commits; repo-file-edits;
deps-or-ci-changes; llm-calls; responding-to-bots`

## Expected artifacts

- report: `.orchestration/reports/T14-t13-pr-lifecycle.md`
- validation: `.orchestration/validation/T14-t13-pr-lifecycle.md`
- sandbox: `.orchestration/sandboxes/T14-t13-pr-lifecycle.md`
- learning: `.orchestration/learning/T14-t13-pr-lifecycle.md`
- autoskill: `.orchestration/autoskill/runs/T14-t13-pr-lifecycle.md`

## STOP conditions

- Push rejected or branch diverged → STOP and report.
- `gh` unauthenticated → STOP and report.

When done send: `AGMSG-RESULT v1 task_id=T14-t13-pr-lifecycle status=ready_for_review ...` with all artifact paths and the PR URL in the report.
