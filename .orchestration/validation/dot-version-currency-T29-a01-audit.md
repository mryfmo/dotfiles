# Codex audit — dot-version-currency-T29-a01 (commit 076f9e9)

Invocation: `codex --profile audit review --commit 076f9e9` (orchestrator, 2026-09-27, first audit-lane runs after T30 deploy).

Session header:

```
OpenAI Codex v0.157.1
--------
workdir: /home/moriya/Workspace/dotfiles
model: gpt-6-astra
provider: openai
approval: never
sandbox: read-only
reasoning effort: high
reasoning summaries: concise
session id: 01a0e149-3131-7182-975e-b6f2b5a80de3
--------
user
```

Findings (verbatim, deduplicated tail of the review output):

```
The installer checksum and focused Renovate configuration test pass, but the migration loses bot secret isolation and does not preserve mise's custom-path and platform safeguards.

Full review comments:

- [P1] Preserve secret isolation for Renovate pull requests — /home/moriya/Workspace/dotfiles/renovate.json:3-4
  When repository secrets are configured, Renovate PRs now enter the private bootstrap path: `.github/workflows/remote.yaml:105–115` excludes only `dependabot[bot]`. Unlike Dependabot, same-repository Renovate PRs can access Actions secrets, so an unreviewed dependency update will run bootstrap code with the private dotfiles deploy key available. Extend the exclusion to Renovate or restrict private bootstrap to trusted post-merge events. This preserves the secret-exposure safeguard required by [AGENTS.md:77](AGENTS.md#L77).

- [P2] Make mise artifact generation load the custom config path — /home/moriya/Workspace/dotfiles/renovate.json:8-10
  `managerFilePatterns` enables extraction from this file but does not make mise discover it. Renovate's mise artifact updater runs `mise lock` in the containing directory without setting `MISE_CONFIG_DIR`; `home/dot_mise/config.toml` is not a normally discovered project config. Consequently, version-update PRs cannot reliably regenerate the paired `mise.lock`, breaking `test_mise_lock_matches_config_and_supported_platforms` and locked installs. Use the existing `MISE_CONFIG_DIR`-aware upgrade path or configure artifact generation to load this source file explicitly.

- [P2] Carry forward the fd upgrade exclusion — /home/moriya/Workspace/dotfiles/renovate.json:33-36
  The new mise manager permits `fd` updates, but `scripts/upgrade-tools.sh:236–240` deliberately excludes that tool because newer releases lack macOS x64 artifacts. Renovate bypasses this safeguard and can propose a version that cannot satisfy the repository's four-platform lockfile or install on supported Intel Macs. Add an `fd` exclusion or allowed-version constraint until upstream restores the missing artifacts.




```
