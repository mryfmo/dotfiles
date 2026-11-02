# anthropics/knowledge-work-plugins

"Plugins that turn Claude into a specialist for your role, team, and company. Built for Claude Cowork, also compatible with Claude Code" (doc, README). Each plugin "bundles the skills, connectors, slash commands, and sub-agents for a specific job function", and "every component is file-based: markdown and JSON, no code, no infrastructure, no build steps" (doc, README). URL: https://github.com/anthropics/knowledge-work-plugins. License: Apache-2.0 (doc, LICENSE and the GitHub page). Default branch: `main` (measured, the clone's checked-out branch). Last commit: `2574e29377c7173d0cecffef29a6ecbd7f8ccb5d`, 2026-10-27, "Update marketplace.json (#1402)" (measured, `git log`). Latest release or tag: none; `git tag` prints nothing and the releases feed is empty (measured, 2026-11-02). Stars 34,391, forks 3,804, 160 open issues and pull requests, of which 67 are open pull requests (measured through the GitHub page and the search API, 2026-11-02). Maintainers: Anthropic; `marketplace.json` names the owner as "Anthropic" (doc), and the human commits of the last 90 days come mostly from one Anthropic account, `jordanecker-ant` (measured, `git shortlog`).

## What it provides

### The marketplace

- One Claude Code plugin marketplace: `.claude-plugin/marketplace.json` with the three required top-level keys `name`, `owner`, `plugins` (measured).
- The marketplace name is `knowledge-work-plugins`, one of the names Claude Code reserves for marketplaces fetched from `github.com/anthropics/` (doc, marketplace reference). A fork under another owner must be renamed before it can be added (inferred from that rule).
- 123 plugin entries: 22 with a relative-path `source` (plugins vendored in this repository, five of them under `partner-built/`) and 101 external entries (measured).
- External entries: 59 of source type `url` and 42 of type `git-subdir`; every one is pinned to a 40-character `sha`, and 42 also carry a `ref` (measured).
- Entry keys in use: `name`, `description`, `source`, `displayName`, `homepage`, `category`, `author`, and once each `strict` and `skills` (measured).
- Categories on the external entries: productivity 31, development 15, finance 11, monitoring 8, security 5, database 4, design 4, deployment 4, automation 3 (measured).

### The plugin format

- Per-plugin layout (doc, README; measured on the clone): `.claude-plugin/plugin.json`, `.mcp.json`, `skills/<name>/SKILL.md`, optional `commands/*.md`, optional `agents/*.md`, a `README.md` and a `CONNECTORS.md`.
- `plugin.json` carries `name`, `version`, `description`, `author`, and sometimes `keywords`, `homepage`, `license`, `repository` (measured over the 22 vendored manifests). Every entry name equals its manifest name (measured).
- `CONNECTORS.md` maps `~~category` placeholders such as `~~source control` to the MCP servers the plugin ships and to alternatives (doc, `engineering/CONNECTORS.md`). The skills use those placeholders in their "If Connectors Available" sections (measured).
- Commands: `commands/*.md` exists only in `pdf-viewer` (4 files) and `product-management` (1); the vendor docs call commands "the older format" that skills supersede (doc, components page).
- Agents: `agents/*.md` only in `partner-built/brand-voice` (5 files) (measured).
- Hooks: no `hooks.json` in any vendored plugin (measured, `find`). The format allows `hooks/hooks.json`, and the upstream policy scan reviews it when present (doc, `.github/policy/prompt.md`).
- MCP: 186 server declarations across the vendored `.mcp.json` files; 185 are `http` to vendor-hosted endpoints (Slack, Notion, Atlassian, Linear, Asana, GitHub Copilot MCP, PagerDuty, Datadog, and others), and one is a `command`, in `pdf-viewer`, running `npx -y @modelcontextprotocol/server-pdf --stdio` (measured).
- Placeholder servers with `"url": ""` for Google Calendar and Gmail appear in every vendored plugin except `pdf-viewer`, `small-business` and the partner plugins, one to four per file (measured, `grep`).
- Skills: 181 `SKILL.md` files in the vendored plugins (measured). Frontmatter beyond `name` and `description`: `argument-hint` (67 files), `allowed-tools` (44), `tiers` (36, sales), `user-invocable` (12), and a few `query`, `compatibility`, `version`, `text` (measured).
- The engineering and operations skills are 32 to 158 lines of prompt text each, with no scripts and no references directories (measured, `wc -l`). Python scripts exist only in `bio-research` and in `data/skills/data-context-extractor` (measured).
- Commands and skills both surface as `/<plugin>:<name>` in Claude Code (doc). The engineering README still advertises `/review` and `/incident`, while the shipped skills are `code-review` and `incident-response` (measured mismatch).

### Agent surfaces

- Cowork first, Claude Code second (doc, README). Cowork and Claude Code both load skills, commands, agents, hooks and remote MCP servers; claude.ai chat ignores agents and hooks (doc, platform-support table).
- Codex: no `.codex-plugin/plugin.json`, no root `plugin.json` with the Agent Plugins schema, no `agents/openai.yaml` anywhere in the tree (measured, `find`). Codex therefore cannot load these as plugins as shipped (inferred from the Codex packaging docs, which require one of the two manifests).

### Plugins relevant to engineering and operations

- `engineering` 1.2.0, ten skills: architecture, code-review, debug, deploy-checklist, documentation, incident-response, standup, system-design, tech-debt, testing-strategy (measured).
- `operations` 1.3.0, nine skills: capacity-plan, change-request, compliance-tracking, process-doc, process-optimization, risk-assessment, runbook, status-report, vendor-review (measured).
- Adjacent: `data` (ten skills: SQL, analysis, validation, dashboards), `cowork-plugin-management` 0.2.2 (two skills for authoring and customizing plugins), `pdf-viewer` 0.2.0 (measured).
- External development, monitoring, security and database entries: Datadog, Grafana, Honeycomb, SigNoz, incident.io, Langfuse, PlanetScale, ClickHouse, Qdrant, Auth0, StackHawk, Vanta, GitKraken, Qodo, Mintlify, and Anthropic's own `security-guidance` from `claude-plugins-official` (measured, `marketplace.json`).
- Other knowledge work, not engineering: sales, marketing, legal, finance, human-resources, customer-support, product-management, design, enterprise-search, productivity, small-business, bio-research (doc, README table).

## How it runs

- Install (doc, README): `claude plugin marketplace add anthropics/knowledge-work-plugins`, then `claude plugin install engineering@knowledge-work-plugins`.
- Claude Code clones the marketplace under `~/.claude/plugins/marketplaces/<name>/`, records it in `known_marketplaces.json` and in `extraKnownMarketplaces` of the user settings, copies the plugin to `cache/<marketplace>/<plugin>/<version>/`, and writes `"engineering@knowledge-work-plugins": true` under `enabledPlugins` (doc, plugin loading reference).
- The version directory is the `version` from `plugin.json`, `1.2.0` for engineering and `1.3.0` for operations (measured).
- Runtime dependencies: none for the engineering and operations plugins; they are Markdown and JSON only (measured).
- `pdf-viewer` needs Node and downloads `@modelcontextprotocol/server-pdf` through `npx -y` at first use (measured, `.mcp.json`). `bio-research` skills carry `requirements.txt` and Python scripts (measured).
- Configuration: `.mcp.json` per plugin is the only configuration; the README tells users to edit it to swap connectors (doc). Nothing in the engineering or operations plugin reads a config file or an environment variable (measured).
- Network and credentials: every connector is a remote MCP server. Claude Code connects from its own process and runs the vendor's OAuth flow when the user connects (doc, components page). The Slack entry carries a public OAuth `clientId` and a `callbackPort` (measured).
- No token literal is in the tree (measured by reading the `.mcp.json` files). The upstream `check-mcp-urls` workflow probes only liveness of the vendored URLs (doc).
- What executes and as whom: skills and commands are prompt text inside the Claude Code session, so anything they ask for runs under the session's permission rules and sandbox (inferred).
- The one local MCP command, `npx`, runs as the user outside the Bash sandbox, because Claude Code starts MCP servers itself (inferred from README point 9, which scopes the sandbox to Bash).
- Validation: `claude plugin validate` on the marketplace passes with one warning (no marketplace `description`). On `engineering` and `operations` it passes with two directory-listing warnings each (no icon, no `privacyPolicyUrl`) and reports no MCP error for the empty-URL entries (measured, Claude Code 2.1.312, 2026-11-02).

## Security and trust boundary

- Read, write, execute: by itself the repository executes nothing in the engineering and operations plugins (measured).
- Reach: whatever the connected MCP servers expose under the user's OAuth identity, which for `engineering` means Slack messages, Jira and Linear issues, Notion pages, GitHub through `api.githubcopilot.com/mcp/`, PagerDuty incidents and Datadog metrics (measured, `engineering/.mcp.json`).
- Skills instruct Claude to pull PR diffs, post status updates and link findings to tickets when those connectors exist (doc, `code-review` and `incident-response` SKILL.md).
- Sandboxing: none provided; the plugin relies on the host. A user-scope marketplace install loads the plugin's MCP servers with the plugin; the per-server approval applies only to project-scope plugins (doc, plugin loading reference).
- Secrets: no secret material in the tree; OAuth at connect time (measured, doc). The upstream policy prompt hunts for cross-service credential exfiltration and undisclosed telemetry in submitted plugins (doc, `.github/policy/prompt.md` and `schema.json`).
- Supply chain, upstream side: external entries are pinned by commit `sha`. A nightly workflow bumps them one PR per plugin after `claude plugin validate`; a Claude-run policy scan with a cached verdict per (plugin, sha) is a required check; a liveness check probes vendored MCP URLs daily; non-member PRs may only add marketplace entries whose source repository already backs a live entry (doc, the four workflow files).
- The vendored plugins themselves move with `main`. There is no tag, no signed release and no lockfile (measured).
- Supply chain, consumer side: Claude Code installs the marketplace's current copy and keeps users on a `version` until `plugin.json` changes it (doc, manifest reference). Marketplace and plugin auto-update stop under `DISABLE_AUTOUPDATER`, which this repository sets (doc, manifest comment at `claude.env`).
- A skill is prompt text, so a content change at the same `version` is possible and only a content digest would catch it (inferred; this repository already pins `frontend-design` that way).
- Known issues: README drift (eleven plugins listed, 22 vendored); README slash names differ from shipped skill names; `.mcp.json` placeholder entries with empty URLs (all measured). A third-party guide of 2026-10-30 notes the same drift and the empty URLs (doc, developersvoice.com).

## Maturity and risk

- Activity: first commit 2026-01-29; 1,128 commits on `main`; 594 commits in the last 90 days, 395 of them by `github-actions[bot]` (the SHA bump workflow) and 155 by `jordanecker-ant`; 61 commits in the last 30 days (measured, `git`).
- 67 open pull requests, the newest being automated bump PRs (measured, search API). About 93 open issues (inferred: 160 open items minus 67 PRs).
- Release cadence: no releases or tags. Per-plugin `version` strings move independently: engineering 1.2.0, operations 1.3.0, productivity 1.3.1, cowork-plugin-management 0.2.2, pdf-viewer 0.2.0 (measured).
- Breaking changes: slash names moved from `/review`-style commands to `/engineering:code-review`-style skills, with the README not yet updated (measured; the 2026-10-30 guide says the same, doc). Commands are "the older format" that skills supersede (doc), so further moves are plausible (inferred).
- Bus factor: one dominant human committer in the last 90 days; thirteen other humans with one to eight commits each (measured).
- Status: production. Anthropic lists `engineering` in the claude.com plugin directory as "Anthropic verified", with its source link pointing at commit `2574e29` (doc, claude.com/marketplace/plugins/engineering).

## Fit with this repository

### Where it would plug in

- A Claude plugin pin under `assets.claude-plugins.plugins` in `home/dot_agents/agent-config.yaml`, shaped `engineering@knowledge-work-plugins: {marketplace: anthropics/knowledge-work-plugins, pin: 1.2.0}`. `scripts/update-agent-assets.sh` then registers the marketplace through `ensure_claude_plugin_marketplace`, installs at user scope, and disables the plugin when the installed version leaves the pin (doc, the asset note and the script). The `version` field exists upstream, so a version pin works here, unlike the content pin `frontend-design` needs (measured).
- Copies of selected `SKILL.md` files under `home/dot_agents/skills/` with a `skills.audience` line, which reach Claude Code, Codex and the omp seats at once (doc, `home/dot_agents/README.md`).
- Nothing on the Codex side; see the next point.

### The `plugins` key and `create_marketplace.json`

- That key renders a Codex marketplace in the Codex format: `interface.displayName`, `policy.installation`, `policy.authentication`, `source.source: local` with a `./`-prefixed path, deployed as `~/.agents/plugins/marketplace.json` (doc, the manifest comment and the Codex packaging page).
- Upstream ships neither `.codex-plugin/plugin.json` nor a root Agent Plugins `plugin.json` (measured), and a Codex marketplace entry needs a plugin that carries one (doc).
- A local entry would also need the plugin tree on disk under the home directory, which nothing here deploys (inferred).
- The Codex route is therefore closed until upstream adds a portable manifest, or this repository vendors a skills-only copy with its own manifest (inferred).

### The skills-first policy

- README point 6: "Claude plugins are not enabled by settings.json unless this repository also installs the marketplace/plugin. Shared workflows should live in skills first" (doc).
- The engineering and operations plugins are the case that policy is written for: their only payload is skills, no hooks, no scripts, no agents (measured). Copying a skill is what makes it reach Codex and omp; the plugin route is Claude-only (inferred from the architecture).
- Constraint: `scripts/validate-agent-assets.py` admits only the Agent Skills fields `name`, `description`, `license`, `compatibility`, `metadata`, `allowed-tools`, so `argument-hint`, present in every engineering skill, must go (measured).
- Constraint: the `~~source control` placeholders and the `../../CONNECTORS.md` link must be rewritten, since no `CONNECTORS.md` exists beside a copied skill (measured, inferred).
- Constraint: `@$1` and `$ARGUMENTS` are Claude Code command substitutions that Codex and omp do not expand (inferred from the vendor docs).
- Constraint: generic names such as `code-review` and `documentation` collide with crit and pstack skill names, which omp namespaces with a warning (doc, `docs/omp-skills.md`). Codex lists every `~/.agents/skills` skill, so each copy costs listing budget (doc, manifest comment).

### Overlap and conflicts

- Overlap: `code-review` with the pinned `crit` plugin, `scripts/orchestrator/pr-audit.sh` and the `AGENTS.md` review rules; `documentation` with `shdoc-shell-docs`; `architecture`, `system-design`, `tech-debt`, `testing-strategy` with `superpowers` 7.0.0 (inferred from the skill descriptions and the pins).
- No counterpart here: `incident-response`, `deploy-checklist`, `standup`, `runbook`, `change-request`, `status-report`, `risk-assessment`, `capacity-plan` (inferred from the skill tree).
- Conflict with MCP parity (README points 1 to 3): the plugin's `.mcp.json` would add eight Claude-only remote MCP servers (`plugin:engineering:slack` and so on), enabled with the plugin and connected on OAuth, outside the `~/.claude.json` route the README reserves for Claude servers (doc, README).
- Conflict with the command policy: the GitHub connector gives Claude a GitHub write path that the `Bash(gh *)` ask rule and the `command_policy` renders never see, because an MCP call is not a shell command (inferred from README point 9 and the `command_policy` comment).
- Conflict with the pinned-asset posture: `pdf-viewer` downloads code with `npx -y` at run time (inferred).
- No conflict with the Bash sandbox itself, which governs only shell commands (doc, README point 9).

## Integration options

1. Skills-first port (recommended, adopt now). Copy a curated subset, for example `incident-response`, `deploy-checklist`, `architecture`, `tech-debt`, `testing-strategy`, `runbook`, `change-request`, `risk-assessment`, `status-report`, into `home/dot_agents/skills/kwp-<name>/SKILL.md`. Trim the frontmatter to the admitted fields, record the upstream path and commit `2574e29` in `metadata`, rewrite the placeholders to "the tools available in this session", keep the Apache-2.0 notice, and add a `skills.audience` line per skill.
   - Cost: one to two days of reading and editing, plus a test that diffs each copy against the recorded upstream commit so drift is visible.
   - Risk: low. Prompt text only, no network, no execution.
   - Reversible: delete the directories and the audience lines; `.chezmoiremove` retires the deployed links.
   - Why: it is the only shape that reaches Codex and omp, it obeys README point 6 verbatim, and it brings none of the MCP servers.
2. Claude plugin pin (hold). Add `engineering@knowledge-work-plugins` with pin `1.2.0` to `assets.claude-plugins.plugins` and let `make update` install it.
   - Cost: one manifest line, one fixture, one `make update`.
   - Risk: medium. The install enables eight Claude-only remote MCP servers that the parity policy forbids and that `validate-agent-assets.py` does not see; it also adds a `/engineering:code-review` beside crit.
   - Reversible: remove the pin, `claude plugin uninstall`, `claude plugin marketplace remove`.
3. Vendored, MCP-stripped plugin in a repository-owned Claude marketplace (trial behind a flag, only if the `/engineering:<skill>` namespace is wanted). Pin `engineering/` by content the way `assets.pstack` pins a `cursor/plugins` tree (a chezmoi external at a commit with a sha256), drop `.mcp.json`, and list it from a Claude `marketplace.json` of ours with a relative source.
   - Cost: a new external, a digest, a marketplace file and doctor checks, about two days.
   - Risk: low after the strip; still Claude-only.
   - Reversible: remove the external and the marketplace entry.

## Open questions

- Which of the nineteen engineering and operations skills does the operator want, given that review, documentation and design workflows already come from crit, superpowers and shdoc?
- Is a Claude-only remote MCP connector set (Slack, Linear, Atlassian, GitHub, PagerDuty, Datadog) ever acceptable here, or does the parity policy stay absolute? Option 2 depends on the answer.
- Should `argument-hint` be admitted to the validator's field list? Claude Code honours it (doc, components page) while the Agent Skills specification the validator follows does not define it; keeping the spec means editing every copied skill.
- How should copied skills track upstream: a recorded commit with a doctor diff, a periodic manual review, or no tracking? The sources give no versioning for skills below the plugin `version`.
- Will upstream add an Agent Plugins `plugin.json` so Codex can load these plugins directly? Nothing in the tree or the open PRs suggests it (measured, not found).
- Does TechnoPro want the non-engineering plugins (sales, legal, finance, HR) for other roles in the kit? That would change the question from "which skills" to "a Cowork plugin policy".

## Sources

- https://github.com/anthropics/knowledge-work-plugins (README, file tree, star and issue counts), accessed 2026-11-02
- https://api.github.com/search/issues?q=repo:anthropics/knowledge-work-plugins+is:pr+is:open (open PR count), accessed 2026-11-02
- https://github.com/anthropics/knowledge-work-plugins/releases (empty feed), accessed 2026-11-02
- Local clone of the repository at commit 2574e29377c7173d0cecffef29a6ecbd7f8ccb5d: `.claude-plugin/marketplace.json`, `engineering/` and `operations/` trees, `.github/policy/*`, `.github/workflows/*`, read 2026-11-02
- https://code.claude.com/docs/en/plugin-marketplaces (Create a marketplace), accessed 2026-11-02
- https://code.claude.com/docs/en/plugins/marketplace-reference (reserved names, entry fields, plugin sources), accessed 2026-11-02
- https://code.claude.com/docs/en/plugins-reference (plugin.json manifest reference), accessed 2026-11-02
- https://code.claude.com/docs/en/plugins/components (skills, commands, hooks, MCP, agents), accessed 2026-11-02
- https://code.claude.com/docs/en/plugins/loading (install records, cache, versions, enabledPlugins precedence), accessed 2026-11-02
- https://claude.com/docs/plugins/platform-support (component support in chat, Cowork, Claude Code), accessed 2026-11-02
- https://claude.com/marketplace/plugins/engineering (directory listing, "Anthropic verified"), accessed 2026-11-02
- https://developers.openai.com/plugins/build/plugins (Codex plugin manifest and marketplace format), accessed 2026-11-02
- https://learn.chatgpt.com/docs/plugins (Codex plugin overview), accessed 2026-11-02
- https://developersvoice.com/blog/ai_in_daily_life/anthropic-knowledge-work-plugins-complete-guide/ (third-party guide, 2026-10-30), accessed 2026-11-02
- Repository checkout, read-only: `home/dot_agents/README.md`, `home/dot_agents/agent-config.yaml` (`plugins`, `codex.plugins`, `codex.marketplaces`, `assets.claude-plugins`, `assets.codex-plugins`, `skills.audience`), `home/dot_agents/plugins/create_marketplace.json`, `scripts/validate-agent-assets.py` (`SKILL_FIELDS`), `scripts/update-agent-assets.sh` (`ensure_claude_plugin_marketplace`), `home/dot_claude/modify_private_settings.json`, `docs/omp-skills.md`, read 2026-11-02
