## Model selection

- Interactive model IDs and efforts live only in `model_profiles` in `home/dot_agents/agent-config.yaml` (dotfiles). Profiles render into Claude settings, `~/.codex/<profile>.config.toml`, and `~/.agents/model-profiles.env`; change interactive models there, never in launchers, rules, or ad-hoc flags. Permgate classifier IDs are separately pinned in its security policy.
- Keep the main session on its startup model. Switching models mid-session invalidates the prompt cache and re-reads the whole history; escalate or downgrade at task boundaries with `/model` and `/effort`, or by launching with another profile.
- Delegate read-heavy exploration (searches, file location, log digests) to the `express-explorer` subagent instead of spending the main model on it.
- Run reviews in a separate context from the implementer on the `review` profile: one capability tier above the worker at reduced effort.
- Escalate to `deep` only for cross-cutting design, unknown failures, or security-sensitive work, and return to `standard` afterward. Model strength never justifies wider permissions, and a cheap model never justifies auto-approving risky actions.
- permgate evaluates PermissionRequest hooks deterministic-first and fails closed to the native prompt. Claude and Codex requests use their own authenticated official CLI with only normalized action metadata; both providers remain shadow-only until reviewed outcomes and successful p50/p95 benchmarks justify enabling one provider.
