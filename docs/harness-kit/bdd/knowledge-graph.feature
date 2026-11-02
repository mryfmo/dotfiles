Feature: Knowledge and code navigation, graphify as an optional per-project tool
  graphify builds a code graph with tree-sitter and answers questions from a
  flat JSON file. The kit treats it as an optional per-project tool: a pinned
  `uv tool install`, a project-scoped install, code-only extraction, no
  manifest MCP entry and no hosted service. ADR-005 records the decision.

  @R-20 @holds-today
  Scenario: No graphify entry exists in the managed trees
    Given the manifest, the scripts and the installers
    When they are searched for graphify
    Then no reference exists

  @R-20 @holds-today
  Scenario: A manifest MCP server must be exposed to Codex only
    Given a manifest MCP server exposed to an agent other than Codex
    When the validator runs
    Then it exits 1 saying the server must be exposed to Codex, the one agent whose MCP config the repository renders

  @R-21 @target
  Scenario: A graphify trial installs a pinned release
    Given an operator trialling graphify in one project
    When the tool is installed
    Then it is installed with `uv tool install` at a release named in an assets entry with a checksum

  @R-22 @target
  Scenario: A project-scoped install leaves the generated trees untouched
    Given a graphify trial with `graphify install --project`
    When the runtime doctor runs afterwards
    Then ~/.claude/skills, ~/.agents/skills, ~/.claude/settings.json and ~/.codex/config.toml are unchanged

  @R-23 @target
  Scenario: Extraction is code-only and reads no provider key
    Given a graphify trial
    When the graph is built
    Then it is built with `--code-only` or GRAPHIFY_BACKEND=none
    And no provider key is read from the environment

  @R-23 @target
  Scenario: A generated graph is not committed without the secret scan
    Given a graphify-out directory in a project
    When a graph file is proposed for commit
    Then the validator's secret scan has run over it or the directory stays untracked

  @R-20 @target
  Scenario: The hosted graphify route is refused without a review
    Given the hosted graphify MCP endpoint with OAuth
    When an agent or operator proposes it
    Then it is refused until a credentials, scope and network review is written
