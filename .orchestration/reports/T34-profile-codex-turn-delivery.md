# T34 profile Codex turn delivery

## Result

Profile modify scripts now force `features.hooks = true` and seed missing
`hooks.state` entries from the base Codex config. Existing profile entries win,
so an already trusted hash is preserved verbatim and changed hooks still need
fresh trust.

## Investigation

Codex CLI 0.146 documents `--profile <name>` as layering
`$CODEX_HOME/<name>.config.toml` over the base config. Its hook guidance says
untrusted command hooks are skipped until reviewed and trusted, with a startup
warning directing the user to `/hooks`; it does not use an interactive prompt.
Trust is recorded against each hook definition's current hash.

The observed failure was a profile-local `[hooks.state]` containing only the
permission hook, which shadowed the base trust map. No hash is recomputed or
accepted automatically by this change.

## Validation

`make unit-test` passed 247 tests; `make validate-agent-assets` and a second
generator `--check` pass succeeded. Applying the generated standard modifier
to the installed profile input retained the dotfiles Stop hook's trusted hash.

review_surface: crit-data
reviewer: codex
review_source: .orchestration/validation/T34-profile-codex-turn-delivery.md
review_outcome: approved

Commit: `da9f00f`. PR: https://github.com/mryfmo/dotfiles/pull/108. GitHub
Actions and the orchestrator-owned fresh profile-session E2E are pending.

## Revision blocker

The required stale-hash selection rule cannot be implemented safely yet. Read-only
tests against the installed Codex 0.146 binary's recorded dotfiles Stop-hook
trust pair showed that `trusted_hash` is not the SHA-256 of hooks.json, the raw
or sorted handler JSON, or the raw or sorted matcher group JSON. The binary
exposes no supported hash-calculation command. Choosing base-wins would clobber
a profile-only newer trust, which the orchestrator explicitly forbids.
