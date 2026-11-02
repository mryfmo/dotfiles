# ADR-001: Composition model, skills first on the single-source manifest

Status: accepted
Date: 2026-11-02

## Context

The kit composes three agents from one file. `home/dot_agents/agent-config.yaml` is the only hand-edited source for shared agent settings, and `scripts/generate-agent-configs.py` renders the agent-native files from it (`home/dot_agents/README.md:7-14`). Shared skills live in `home/dot_agents/skills` and are exposed as `~/.agents/skills`; `skills.audience` names, per skill, the agents that list it, and the generator renders one audience map per agent: symlinks under `~/.claude/skills` for Claude Code, `[[skills.config]] enabled = false` entries in the Codex config for skills Codex is not given, and `skills.ignoredSkills` in each omp seat overlay (`home/dot_agents/README.md:8-13`, `home/dot_agents/agent-config.yaml:81-120`).

The parity policy already decides the plugin and MCP questions in outline. Every MCP server in the manifest targets Codex only, and the validator rejects `agents.claude: true`; Claude Code user-scope servers live in `~/.claude.json`, which the repository does not manage, and are added with `claude mcp add --scope user` (`home/dot_agents/README.md:25`). MCP servers stay disabled by default (`README.md:27`). Claude plugins are not enabled by `settings.json` unless the repository installs the marketplace and plugin, and shared workflows live in skills first (`README.md:30`). Today the manifest holds `mcp_servers: {}` (`agent-config.yaml:1072`), seven pinned Claude plugins under `assets.claude-plugins.plugins` (`agent-config.yaml:1382-1389`) and a Codex marketplace with one plugin, crit (`agent-config.yaml:1055-1069`).

The research on anthropics/knowledge-work-plugins is the test case for this model. The engineering and operations plugins are Markdown and JSON only, with no hooks, scripts or agents (research/anthropics-knowledge-work-plugins.md, "What it provides", "Plugins relevant to engineering and operations"). Codex cannot load them as plugins because upstream ships no Codex manifest ("Agent surfaces", "The `plugins` key and `create_marketplace.json`"). A Claude plugin pin would enable eight Claude-only remote MCP servers through the plugin's `.mcp.json`, outside the route the parity policy reserves for Claude servers, and would give Claude a GitHub write path the command policy never sees ("Overlap and conflicts"). Copying the skills is the only shape that reaches Codex and the omp seats, and the validator admits only the six Agent Skills fields, so `argument-hint` and the connector placeholders must go ("The skills-first policy").

## Decision

Skills first on the single-source manifest. Plugins only where a plugin brings namespace or hook semantics a skill cannot. MCP stays Codex-only and disabled by default. Claude connectors stay the operator's `claude mcp add`.

Concrete rules:

1. A shared workflow is a directory `home/dot_agents/skills/<name>/SKILL.md` with one `skills.audience` entry naming every agent that lists it. The generator refuses a directory without an entry (`docs/omp-skills.md`, "Per-consumer audience").
2. A skill's frontmatter holds only `name`, `description`, `license`, `compatibility`, `metadata` and `allowed-tools` (`scripts/validate-agent-assets.py:469`). Claude Code command substitutions such as `$ARGUMENTS` and `@$1` and connector placeholders are rewritten before a copy lands, because Codex and omp do not expand them.
3. A plugin is pinned under `assets.claude-plugins.plugins` or `assets.codex-plugins.plugins` only when its unit brief names the namespace or hook semantics it brings that a skill cannot. A plugin whose upstream has no version is pinned by content digest, as `frontend-design` is (`agent-config.yaml:1364-1385`).
4. A plugin that ships `.mcp.json` servers for Claude is not pinned. The knowledge-work-plugins engineering plugin is therefore not pinned; its skills are ported under ADR-004.
5. `mcp_servers` in the manifest holds only servers that are Codex-only, `enabled: false`, `sampling: false`, with a `stdio` command or an `http` url (`validate-agent-assets.py:1512-1536`). The rendered Codex config holds exactly those names (`:1540-1544`).
6. A Claude Code MCP server is the operator's `claude mcp add --scope user`, recorded nowhere in the repository.

Forbidden: a hand edit of a generated file that is not moved back into the manifest (`README.md:31`); a plugin enabled from `settings.json` without a pin; a skill copied to `~/.codex/skills` or another root the generator does not render.

## Alternatives considered

- Pin `engineering@knowledge-work-plugins` as a Claude plugin at version 1.2.0. Rejected: it enables eight Claude-only remote MCP servers that the parity policy forbids and the validator does not see, adds `/engineering:code-review` beside the pinned crit plugin, and reaches neither Codex nor omp (research/anthropics-knowledge-work-plugins.md, "Integration options", option 2).
- A repository-owned Claude marketplace with a vendored, MCP-stripped copy of the plugin. Held as a trial only if the `/engineering:<skill>` namespace is wanted; it costs a new external, a digest, a marketplace file and doctor checks, and stays Claude-only ("Integration options", option 3).
- A Codex marketplace entry for the plugin. Closed: upstream ships no `.codex-plugin/plugin.json` and no root Agent Plugins manifest, so Codex cannot load it ("The `plugins` key and `create_marketplace.json`").
- Loosening the parity policy to admit Claude-targeted MCP servers in the manifest. Rejected: the research lists this as an open operator question, and nothing in the eight candidates needs it ("Open questions").

## Consequences

Positive:

- One manifest, one audience map and one validator keep the three agents in step.
- A ported skill reaches Claude Code, Codex and the omp seats at once.
- No new network reach or OAuth connector enters the kit through a plugin.
- The parity policy stays as written; no validator rule is loosened.

Negative:

- Every ported skill is edited by hand to the admitted fields and loses its slash-command namespace.
- Codex lists every `~/.agents/skills` skill, so each port costs listing budget (research/anthropics-knowledge-work-plugins.md, "The skills-first policy").
- Namespace collisions with crit, superpowers and shdoc skills must be avoided by name.
- A plugin-only feature, such as a hook or an agent definition, needs its own brief before it can enter.

Units created:

- The knowledge-work skills port, under ADR-004 (rollout phase 2).
- No unit for plugin pins.

## Verification

`bdd/composition.feature`, run by `check.py --holds-today` for the scenarios that hold today:

- `@R-01`: every shared skill directory has an audience entry (holds today); a ported skill reaches all three agents (target).
- `@R-02`: the manifest declares no MCP server today; the validator refuses an enabled server (both hold today).
- `@R-03`: a Claude plugin without a version is pinned by content digest (holds today).
- `@R-04`: the validator refuses a Claude-targeted MCP server (holds today).
- `@R-05`: the knowledge-work-plugins engineering plugin is not pinned (holds today); a plugin adoption names the semantics a skill cannot provide (target).
