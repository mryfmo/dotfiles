# T31 result report

- Task: `T31-codex-profile-modify-pattern`
- Worktree: `/Users/mryfmo/Workspace/dotfiles-t31`
- Branch: `fix/codex-profile-modify`
- Commit: `04a76fc fix(agents): preserve codex runtime state via modify profiles`

Generated executable `modify_<profile>.config.toml` sources now merge managed `model` and `model_reasoning_effort` values with the same Codex runtime table prefixes used by `modify_private_config.toml`. The runtime checker invokes them with `same_modified()`. The agmsg ignore treats `agmsg/db-<project>` stores as runtime-owned while preserving the other existing matches.

The emitted chunk splitter is byte-idempotent for Codex-written profiles: the blank separator before a preserved runtime table remains attached to that table, so a correct deployed profile round-trips unchanged.

Runtime and unknown current chunks are now tracked by occurrence rather than table name. Repeated TOML array-of-tables therefore remain complete and ordered in both generated profile modifiers and `modify_private_config.toml`.

`private_` is not warranted for the profile sources: they hold no secrets, and Codex changing a deployed profile to mode 600 is runtime behavior rather than a source confidentiality requirement.

The approved Bats assertion now points at the generated modifier; Bats was not run locally. No push, chezmoi apply, live Herdr mutation, real-HOME mutation, dependency change, or LLM call was performed.
