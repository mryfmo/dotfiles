# WP-E: Remove hermes-agent-orchestration skills

task_id: WP-E
repo: /Users/mryfmo/Workspace/dotfiles
team: dotfiles-tmux-hermes-removal
worker: codex-wpe

## Objective

Delete the hermes-agent-orchestration skill sources (both the shared dot_agents copy and the dot_claude symlink templates). The agmsg-orchestration skill is the deliberate non-Hermes replacement and MUST be kept untouched.

## Changes (exhaustive — do all, nothing else)

DELETE:

- home/dot_agents/skills/hermes-agent-orchestration/ (entire directory: SKILL.md, agents/openai.yaml, anything else inside)
- home/dot_claude/skills/hermes-agent-orchestration/ (entire directory: symlink_SKILL.md.tmpl, agents/symlink_openai.yaml.tmpl, anything else inside)

KEEP (verify untouched):

- home/dot_agents/skills/agmsg-orchestration/ (its prose mentions Hermes descriptively — that is fine, do not edit)
- home/dot_agents/skills/agmsg/

Check: `grep -rln "hermes-agent-orchestration" home/ scripts/ docs/ mkdocs.yml 2>/dev/null || true` — if any file still references the deleted skill by name (e.g. a skill index, docs nav, validator fixture), report it; only fix it if the file is not owned by another task (WP-D owns scripts/validate-agent-assets.py, generate-agent-configs.py, check-agent-runtime.py, agent-config.yaml; WP-F owns README/Makefile/.github). Report cross-owned findings instead of editing.

## Allowed files (edit boundary)

Only the two skill directories above, plus your artifact paths, plus any skill-index file discovered by the Check that no other task owns (list it in the report).

## Forbidden actions

git commit; git push; chezmoi apply; running bats; adding dependencies; editing agmsg-orchestration skill; editing files owned by WP-D/WP-F.

## Validation (run and capture output)

1. both directories gone
2. Check-grep output captured
3. `git status --porcelain` → only expected deletions

## Expected artifacts (write to these exact paths)

- report: .orchestration/reports/WP-E.md
- validation: .orchestration/validation/WP-E.txt
- sandbox: .orchestration/sandboxes/WP-E.md (record: codex exec --sandbox workspace-write fallback)
- learning: .orchestration/learning/WP-E.md ("none" if nothing)
- autoskill: .orchestration/autoskill/runs/WP-E.md (record "not-used")

## Done signal

```
bash ~/.agents/skills/agmsg/scripts/send.sh dotfiles-tmux-hermes-removal codex-wpe orchestrator-fable5 "AGMSG-RESULT v1 task_id=WP-E status=ready_for_review report=.orchestration/reports/WP-E.md validation=.orchestration/validation/WP-E.txt sandbox=.orchestration/sandboxes/WP-E.md learning=.orchestration/learning/WP-E.md autoskill=.orchestration/autoskill/runs/WP-E.md"
```

If blocked: same message with status=blocked, artifacts explaining why.

max_turns: 20
