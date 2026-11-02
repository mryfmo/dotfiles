Feature: Composition model, skills first on the single-source manifest
  The kit composes Claude Code, Codex and the omp seats from one hand-edited
  manifest, home/dot_agents/agent-config.yaml. Shared workflows are skills
  under home/dot_agents/skills, each named in skills.audience, because a skill
  reaches all three agents while a plugin reaches one. A plugin is used only
  where it brings a namespace or hook semantics a skill cannot. MCP servers in
  the manifest are Codex-only and disabled; Claude connectors are the
  operator's own `claude mcp add`. ADR-001 records the decision.

  @R-01 @holds-today
  Scenario: Every shared skill directory has an audience entry
    Given the skill tree home/dot_agents/skills
    When each directory name is looked up in skills.audience of the manifest
    Then every directory has an entry naming the agents that list it

  @R-01 @target
  Scenario: A ported third-party skill reaches all three agents
    Given a skill copied from an upstream plugin into home/dot_agents/skills
    When the generator renders the agent configs
    Then Claude Code, Codex and the omp seats named in its audience list it
    And no agent outside its audience lists it

  @R-02 @holds-today
  Scenario: The manifest declares no MCP server today
    Given the manifest key mcp_servers
    When it is read
    Then it is the empty mapping

  @R-02 @holds-today
  Scenario: The validator refuses an enabled MCP server
    Given a manifest MCP server whose enabled flag is not false
    When the validator runs
    Then it exits 1 saying the server must be disabled by default in the shared manifest

  @R-03 @holds-today
  Scenario: A Claude plugin without a version is pinned by content digest
    Given the claude-plugins asset in the manifest
    When its plugin pins are read
    Then a plugin whose upstream has no version carries a sha256 content pin

  @R-04 @holds-today
  Scenario: The validator refuses a Claude-targeted MCP server
    Given a manifest MCP server with agents.claude set
    When the validator runs
    Then it exits 1 naming the `claude mcp add --scope user` route instead

  @R-05 @holds-today
  Scenario: The knowledge-work-plugins engineering plugin is not pinned
    Given the manifest, the scripts and the installers
    When they are searched for the knowledge-work-plugins marketplace
    Then no reference exists

  @R-05 @target
  Scenario: A plugin adoption names the semantics a skill cannot provide
    Given a proposal to pin a Claude or Codex plugin
    When the unit brief is written
    Then it names the namespace or hook semantics that the plugin brings and a skill cannot
    Or the proposal is replaced by a skills-first port
