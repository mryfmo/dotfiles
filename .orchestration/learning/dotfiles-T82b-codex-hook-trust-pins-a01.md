# Learning: dotfiles-T82b-codex-hook-trust-pins-a01

- **Verify against the tool itself, not against recorded state.** Codex's app-server `hooks/list` reports `currentHash` and `trustStatus` read-only. It showed the recorded Ponytail pins were stale, where a check against recorded values alone would have given a false positive.
- **Before pinning managed state into a runtime-merged file, check the merge's precedence.** Here existing entries won, so a managed pin could never repair a stale one; the fix is declared keys overriding existing ones.
- **A modify script's view of the template is not chezmoi's.** `modify_private_config.toml` only string-replaces three placeholders, so template functions such as `sha256sum` never run there.
- **Match the chunk convention when adding chunks to a merge.** `split_chunks` gives a chunk its trailing blank line; a chunk with a leading blank line grows a blank line on every apply (caught by the idempotency test).
