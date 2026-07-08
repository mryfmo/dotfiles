# WP-J Learning

## Reusable Learning

- Ghostty reads `~/.config/ghostty/config`, not `~/.config/ghostty/config.ghostty`; chezmoi source should therefore be `home/dot_config/ghostty/config` when managing the active Ghostty config directly.
- When adopting a live user-authored config, validate that the managed source preserves the live baseline before appending managed extras. A simple prefix comparison is enough here.

## Applied To

- `home/dot_config/ghostty/config`
- `README.md`
- `install/macos/common/defaults.sh`
- `tests/files/macos.bats`
- `tests/unit/test_herdr_agents.py`

## Promotion

No reusable rule candidate was promoted by this worker. The learning is captured here for orchestrator review only.
