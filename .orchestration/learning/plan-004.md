# Plan 004 Learning Triage

## Validated reusable observations

- Sheldon 0.8.5 accepts `rev`, not `commit`, for a full Git revision. Its unused-key warnings are a required semantic oracle; text scans alone falsely accepted mutable plugin sources.
- The global mise config at `~/.config/mise/config.toml` pairs with `~/.config/mise/mise.lock`, not `config.lock`.
- `mise lock` can exit zero while reporting skipped platforms after API rate exhaustion. Acceptance must require no warnings/skips, config-to-lock completeness, strict install dry-run, and an identical second generation.
- Aqua's yq registry metadata selected amd64 on ARM64 macOS at 4.53.3; the explicit GitHub backend generated the correct native artifact/checksum. fd 10.4.2 had no Intel macOS artifact, so the newest four-platform release is 10.3.0.
- Exact mise pins need maintenance commands to set `MISE_LOCKED=0` while regenerating config/lock; ordinary installs remain strict.

## Promotion decision

Keep as Plan 004 evidence for the orchestrator to promote after CI validates Linux and macOS bootstrap behavior.
