# Learning triage: dotfiles-T133-pre-send-check-a01

These are candidates only; nothing is promoted.

1. [memory:decision] A script pinned to a host-only interpreter path can still be tested in CI. The test gives the script a temporary HOME whose pinned path links to the running interpreter, and keeps `UV_CACHE_DIR`, so the offline cache still answers. `test_check_regime_boundary` already keeps the real uv cache under a fake HOME this way.
2. [memory:decision] Read a constant out of another module with `ast` (the assignment's literal arguments) rather than by importing it or `exec`-ing a regex-cut slice. Nothing in the module runs, and ruff's S102 stays quiet.
3. [memory:failure] zsh does not word-split an unquoted `$c` the way bash does. A `for c in "cmd args"; do $c; done` evidence loop runs nothing (exit 127) until it uses `${=c}`. Check every evidence loop's exit codes before pasting them.
