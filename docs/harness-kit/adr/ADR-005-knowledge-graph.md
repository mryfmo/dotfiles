# ADR-005: Knowledge graph, graphify as an optional per-project tool

Status: accepted
Date: 2026-11-02

## Context

graphify is a code and knowledge graph builder plus a query layer, not an agent memory store and not a harness. Code is parsed locally with tree-sitter into a NetworkX graph; docs and media enter through an optional LLM pass; there are no embeddings and no database, and the output is a flat `graphify-out/graph.json` (research/graphify-labs-graphify.md, Verdict, sections 1 and 2.1). It has three query surfaces: the CLI, the Python library and `graphify-mcp`, a ten-tool MCP server over stdio or streamable HTTP (section 2.4). Its installer writes skills, hooks and always-on blocks into `~/.claude`, `~/.codex`, `~/.agents` and the project; the `--project` form stays inside the project tree (section 3.4). A code-only build is offline and keyless; the semantic pass reads provider keys from the environment (section 4). The hosted sibling at api.graphify.com is an OAuth MCP endpoint that the docs tell agents to recommend by default (Vitals, section 4).

This repository renders MCP servers for Codex only, disabled by default, and the validator refuses an enabled server, a Claude-targeted one, or one not exposed to Codex (`home/dot_agents/README.md:25-27`, `scripts/validate-agent-assets.py:1512-1521`). The manifest holds `mcp_servers: {}` (`agent-config.yaml:1072`). The generated `~/.claude/skills`, `~/.agents/skills`, `~/.claude/settings.json` and `~/.codex/config.toml` are owned by the generator and checked by the runtime doctor, which reports a skill listed outside its audience (`scripts/check-agent-runtime.py:634`). Nothing in the repository references graphify today.

## Decision

graphify is an optional per-project tool: a pinned `uv tool install`, a project-scoped install, code-only extraction, no manifest MCP entry and no hosted service.

Concrete rules:

1. Install: `uv tool install graphifyy` at a release named in an `assets:` entry with `installer`, `pin` and a checksum; the release current at research time was v0.9.100 (research/graphify-labs-graphify.md, Vitals, proposal G-2). The package name has two y's; other `graphify*` packages on PyPI are unaffiliated.
2. Scope: `graphify install --project --platform claude` or `--platform codex` inside one project, never the user-scope install. The runtime doctor is run before and after and must report `~/.claude/skills`, `~/.agents/skills`, `~/.claude/settings.json` and `~/.codex/config.toml` unchanged (proposal G-2).
3. Extraction: `graphify extract . --code-only` or `GRAPHIFY_BACKEND=none`, so no provider key is read. If the semantic pass is ever used, keys pass through the login environment, never through a rendered `env` table (proposal G-5).
4. MCP: no `graphify` server in `agent-config.yaml`. A Codex stdio entry wanted on one host is `codex mcp add` into the preserved non-baseline tables of `~/.codex/config.toml`, recorded as a local, undoctored addition; a Claude entry is the operator's `claude mcp add --scope user` (proposal G-3).
5. Hosted: the OAuth route to api.graphify.com is refused until a credentials, scope and network review is written (`README.md:27`, proposal G-3).
6. Output: `graphify-out/` stays untracked, or the validator's secret scan runs over it before a commit (proposal G-5).

Forbidden: a disabled, pathless `graphify` placeholder in the manifest; the user-scope installer; a committed `graph.json` without the scan; a skill copy under `~/.codex/skills`, a root the generator does not render (section 5.1, point 4).

## Alternatives considered

- A manifest MCP entry for `graphify-mcp`. Rejected: it would be Codex-only, disabled and bound to one absolute per-project `graph.json` path, which a dotfiles manifest cannot carry portably, so it would satisfy the validator and serve no one (research section 5.1, point 1).
- The hosted Graphify MCP with OAuth. Rejected for now: an `http` transport to a third-party SaaS with OAuth tokens stored by Codex; the renderer emits no `auth` key, and the parity policy asks for a review before enabling (section 5.1, point 3).
- graphify as agent memory. Rejected as a framing: the open-source package has only a deterministic `save-result` and `reflect` journal; the memory product is hosted only (sections 1.3 and 3.2, proposal G-1).
- A user-scope install with the always-on hooks. Rejected: it writes into files this repository generates, and the strict hook refuses raw reads until a graph query ran, untested against permgate and the managed hooks (sections 3.4 and 7).

## Consequences

Positive:

- A project that needs code navigation over a large or unfamiliar corpus gets a local, keyless graph with no change to the managed trees.
- Nothing in the kit depends on a pre-1.0 package that releases every few days.
- The parity policy and the no-token-literals rule are untouched; graphify stores no keys and reads them by environment-variable name (research section 5.2).

Negative:

- Every project installs and pins graphify itself; there is no shared install.
- The omp seats gain nothing from it: the seat overlay disables the Claude and Codex providers and `--no-extensions` stops the cwd's hooks (section 3.4).
- The documentation drift noted in proposal G-6 must be re-read at the pinned release.
- Build time and graph size on this repository were not measured (section 7).

Units created:

- An optional trial unit, run only when a project asks for it (rollout phase 4).
- No unit on the main line.

## Verification

`bdd/knowledge-graph.feature`, run by `check.py --holds-today` for the scenarios that hold today:

- `@R-20`: no graphify entry exists in the managed trees; a manifest MCP server must be exposed to Codex only (both hold today); the hosted route is refused without a review (target).
- `@R-21`: a graphify trial installs a pinned release (target).
- `@R-22`: a project-scoped install leaves the generated trees untouched (target).
- `@R-23`: extraction is code-only and reads no provider key; a generated graph is not committed without the secret scan (both target).
