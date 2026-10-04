# Learning: dotfiles-T76-ineffective-settings-a01

- **Deleting a managed table is not removal when the merge preserves current-only tables.** The Codex `modify_private_config.toml` keeps any table the new baseline no longer names, so retiring managed config needs an explicit retired list in the merge script. The Claude MCP file is a full template and has no such issue.
- **Check how the merge treats the key before deleting it.** `enabledPlugins` is a `RUNTIME_KEYS` entry, and the merge keeps current-only keys, so dropping the managed key leaves users' enabled plugins intact.
- **A name regex needs digits.** `[a-z_]+` silently skipped `context7`; the simulation's first count was five, not six.

## Revise round 1

- **Retiring managed config needs a convergence step in the merge, not just a baseline deletion.** Gate the purge on the last managed state (`enabled = false`), so an operator's own re-enabled copy survives.
- **Match the full table path.** A bare-name check would also hit an unrelated top-level table of the same name.

## Revise round 2

- **A TOML table is never alone.** Purging a parent must take its dotted child tables, or the result is an invalid partial entry.
- **Decide on a config value by parsing, not by regex.** Text inside a string value looks like an assignment. When parsing is unavailable or fails, keep the input.
- **A regression test must reach the code path it targets.** My first P2 case put the string in the child table, which the old regex never examined; only a direct check showed the case did not discriminate.
