# dot-ubuntu-parity-T2-a01 learning

- `[memory:decision]` chezmoi `run_once_*.sh.tmpl` scripts retrigger purely
  from a content-hash change of their rendered output; no `chezmoi state
delete-bucket`/rename dance is needed when the underlying script changes
  (e.g. B1's `configure_docker_group()` addition). Registered in
  CompactionDB, id `6c8f2285-58bb-444e-a028-dd0c09a9141f`.

- With this repo's `home/dot_mise/config.toml` setting `locked = true`,
  `mise install <new-tool>` for a tool that has never appeared in
  `mise.lock` fails outright ("No lockfile URL found ... (--locked mode)"),
  even with `mise lock` run first (`mise lock` itself refuses to add an
  unresolved entry while locked). The unlock-once pattern that works:
  `MISE_LOCKED=0 mise install <new-tool>@<version>` to populate the lockfile
  entry, then normal `mise lock`/`mise install --locked` work from then on.

- `mise lock` never prunes a lockfile entry for a tool no longer referenced
  by `config.toml` (e.g. switching a tool's backend from `github:` to
  `aqua:` leaves the old `github:`-keyed entry behind, additive only). Don't
  assume a config.toml backend swap implies the old lock entry disappears —
  check for tests or tooling that key off the exact lock-table name before
  deciding whether to hand-delete it.

- `scripts/check-agent-runtime.py` delegates `modify_private_config.toml`
  rendering to a real subprocess call (`same_modified()`, `CHEZMOI_SOURCE_DIR`
  only) rather than re-implementing template substitution locally. When
  adding a new `{{ .chezmoi.* }}` placeholder to a `modify_` script, check
  whether the checker actually needs a mirrored local substitution or
  already gets it for free via subprocess delegation — don't add one
  speculatively.

- Grep the whole repo (not just `allowed_files`) for an identifier before
  changing its exact text. Two out-of-scope tests
  (`tests/unit/test_supply_chain_policy.py`,
  `tests/unit/test_herdr_agents.py`) hardcoded literal strings
  (`"github:mikefarah/yq"`, `"herdr-agents --attach"`) that this task's
  edits would otherwise have broken; both were out of `allowed_files`, so
  the implementation had to be shaped (kept the stale lock entry; left the
  new command unquoted) to keep them passing rather than editing them.
