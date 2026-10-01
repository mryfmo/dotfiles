# Learning: dot-orchestrator-pane-profile-args-T47-a01

## Triage

1. **Source the model-profiles env file in a subshell when a later step still needs env-overridden globals.**
   `~/.agents/model-profiles.env` defines `HERDR_AGENTS_WORKER_PROFILE`/`_KIND`/`_WORKTREE` as
   well as `MODEL_PROFILE_*`. A global `source` in an early step (orchestrator start precedes the
   worker start in full mode) silently replaces operator overrides resolved at startup.
   Applies to: any new consumer of the env file in `herdr-agents`. Status: candidate rule
   (not promoted); existing precedent `resolve_worker_profile` uses `local` shadowing.
2. **The Claude Code PostToolUse formatter reformats whole Python files.** On
   `tests/unit/test_herdr_agents.py` (not formatter-clean on main) one Edit produced a 783-line
   diff. Check `git diff --stat` before commit and restore unrelated formatting. Status:
   candidate check (a pre-commit diff-size sanity step), not promoted.
3. `make validate-agent-assets` needs the default uv cache or PyPI access
   (`uv run --with pyyaml`); a fresh sandbox `UV_CACHE_DIR` fails offline. Extends the T44 uv
   cache finding. Status: observation.

No rule or skill was promoted by this task.
