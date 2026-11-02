Feature: DeepSeek harness seat, an optional fourth seat vendor
  DeepSeek Harness (DSH) becomes an optional fourth seat vendor beside Claude
  Code, Codex and omp, pinned to an upstream tag and never to the one-commit
  Shiguredo fork, with a rendered profile patch that turns session-log upload
  off, routes to Ollama Cloud or on-prem servers, and mounts the kit's Claude
  hooks. The dsh-superagent prototype is design reading, not a service.
  ADR-006 records the decision.

  @R-24 @holds-today
  Scenario: No DeepSeek or Ollama route exists today
    Given the manifest, the scripts and the installers
    When they are searched for DeepSeek or Ollama
    Then no reference exists

  @R-24 @target
  Scenario: The dsh asset is pinned to an upstream release tag
    Given the dsh asset in the manifest
    When its declaration is read
    Then its upstream is deepseek-ai/deepseek-harness at a release tag with a sha256
    And it never names the shiguredo fork

  @R-25 @target
  Scenario: The rendered profile patch turns session-log upload off
    Given the kit's rendered cordis.patch.yml for a dsh profile
    When it is read
    Then session-log-deepseek.enabled is false

  @R-25 @target
  Scenario: Seats default to Ollama Cloud or on-prem routes
    Given the kit's rendered dsh profile
    When its llm-pi-ai providers are read
    Then the default route is an Ollama Cloud or on-prem endpoint
    And the official DeepSeek API route is opt-in per engagement

  @R-25 @target
  Scenario: The kit's Claude hooks gate the dsh seat
    Given the kit's rendered dsh profile
    When its plugins are read
    Then dsh-hooks-claude-code is mounted and points at the rendered Claude hooks

  @R-26 @holds-today
  Scenario: Model ids live in model_profiles only
    Given the manifest
    When the validator runs
    Then it exits 1 when claude.model, claude.effortLevel or codex.model is set outside model_profiles
    And it requires the six base profiles and no others

  @R-27 @holds-today
  Scenario: The superagent prototype is not deployed
    Given the manifest, the scripts and the installers
    When they are searched for the superagent prototype
    Then no reference exists

  @R-27 @target
  Scenario: A proactive seat, if ever added, starts in observe mode
    Given a future seat that reacts to GitHub events
    When its first design is written
    Then it starts with the accept mode observe, recording what it would have accepted
    And it moves to auto only by a decisions.tsv row
