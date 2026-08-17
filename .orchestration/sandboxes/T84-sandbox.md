# T84 Sandbox

- Worker: `codex-deep-dot`
- Repository: `/Users/mryfmo/Workspace/dotfiles`
- Durable repository writes are limited to T84 source/test/lifecycle changes, the five T84 artifacts, and mandated Crit evidence/receipt.
- `scripts/validate-agent-assets.py` is included because it was the lifecycle validator hardcoding the old generated profile names.
- Required deployed files under `~/.z*` and `~/.codex/*.config.toml` were read/stat'ed only; none were edited.
- CompactionDB received project decision record `226c1bd7-6f3a-4230-8e67-31d14221ddd4`.
- No Bats, `chezmoi apply`, automatic doctor repair, dependency mutation, commit, push, or browser review occurred.
- `effects=none`

