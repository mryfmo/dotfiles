# Learning

- Candidate (not promoted): in `herdr-agents`, a resolver that early-returns on an explicit env var and only then sources `~/.agents/model-profiles.env` must `local`-shadow every variable it reads from that file; otherwise an env-file value with the same name as the explicit override is either dead (never read) or leaks. `resolve_worker_kind()` is the reference pattern.
- Candidate (not promoted): when a manifest profile is repointed (e.g. `standard.claude`), check the "one tier above the worker" invariant on `review` in the same change; the comment in agent-config.yaml is the only guard.
