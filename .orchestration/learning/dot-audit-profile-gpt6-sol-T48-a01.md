# Learning: dot-audit-profile-gpt6-sol-T48-a01

1. **Tasks must only name make targets that exist on their base.** T48 named `make render-check`
   (added by the unmerged T43 PR #214), and on `origin/main` it exits 2. Until #214 merges, task
   files based on main should name `uv run --with pyyaml scripts/generate-agent-configs.py --check`,
   or the orchestrator should check the target exists on the base before dispatch, as the SKILL's
   "verify every CLI constraint by running the real command" step says. Status: observation for
   the orchestrator.
2. A pin test that lists rejected values should include the previous pinned value whenever a pin
   moves, so the test proves the old value now fails. Status: observation.

No rule or skill was promoted.
