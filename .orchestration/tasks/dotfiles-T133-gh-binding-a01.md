---
format: 2
task_id: dotfiles-T133-gh-binding-a01
kind: code
security: true
dispatch_status: draft-owner-stub
allowed_files:
  - home/dot_mise/config.toml
  - home/dot_agents/agent-config.yaml
  - scripts/generate-agent-configs.py
  - scripts/validate-agent-assets.py
  - tests/unit/test_generate_agent_configs.py
  - tests/unit/test_supply_chain_policy.py
  - .orchestration/dotfiles-T133-gh-binding-a01/**
after: [dotfiles-T133-trusted-entrypoint-binding-a01]
---

# AGMSG-TASK dotfiles-T133-gh-binding-a01 — bind gh by absolute pinned path (owner stub)

Owner stub written 2026-10-21T09:27Z by the orchestrator seat (C-51). Three C-80 rounds of the a07-checker text (`…-text-security-922292d/0edbd8c/fd8c003.md`) found the same P1: every canonical read of the regime, the checker's and the orchestrator's own acceptance-time `gh api` reads, trusts a PATH- or mise-selected `gh` whose executable nothing binds; design 5.14 items 2-4 and `dotfiles-T133-trusted-entrypoint-binding-a01` bind uv, Python, Node and permgate only. On this host gh is mise-managed at `~/.local/share/mise/installs/github-cli-cli/latest/bin/gh` (version tracking `latest`). This stub is never dispatched; its text is authored after the binding task merges.

## Scope

Pin `github-cli` to an exact version in `home/dot_mise/config.toml` (the pins pattern of PR #449), declare the absolute gh path in `agent-config.yaml` beside the uv/Python/Node declarations, validate it with the same supply-chain policy tests, and make every orchestrator-side canonical read (`scripts/orchestrator/*.sh`, the checker's `executable("gh")`) resolve gh through that declaration with `--hostname github.com` fixed; one refusal test per route. Until it lands, every text names the gh reads as non-authoritative-residual owned here.

## Owned rows

- a07-checker text row "gh executable provenance" and its siblings (gh child environment, canonical-main design read, C6 canonical receipt binding), text-security:922292d:1, text-security:0edbd8c:1, text-security:fd8c003:1-2.

## Checks (pasted by the orchestrator before each send)

```text
(empty until the dispatch text is authored)
```
