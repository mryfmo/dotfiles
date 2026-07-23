## Model selection

- Model IDs and efforts live only in `model_profiles` in `home/dot_agents/agent-config.yaml` (dotfiles). Profiles render into Claude settings, `~/.codex/<profile>.config.toml`, and `~/.agents/model-profiles.env`; change models there, never in launchers, rules, or ad-hoc flags.
- Keep the main session on its startup model. Switching models mid-session invalidates the prompt cache and re-reads the whole history; escalate or downgrade at task boundaries with `/model` and `/effort`, or by launching with another profile.
- Delegate read-heavy exploration (searches, file location, log digests) to the `express-explorer` subagent instead of spending the main model on it.
- Run reviews in a separate context from the implementer on the `review` profile: one capability tier above the worker at reduced effort.
- Escalate to `deep` only for cross-cutting design, unknown failures, or security-sensitive work, and return to `standard` afterward. Model strength never justifies wider permissions, and a cheap model never justifies auto-approving risky actions.
- ccgate PermissionRequest hooks are disabled (no classifier credential; permission prompts are native). Re-enable only with a dedicated low-cost API key or official support for existing agent auth.
