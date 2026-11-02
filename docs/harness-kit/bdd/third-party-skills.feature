Feature: Third-party skill provenance
  A third-party skill is adopted only with a verified publisher, a commit pin
  with a sha256 or a vendored copy that records its upstream commit, a curated
  subset, validator-clean frontmatter and a review cadence. The engineering
  and operations skills of anthropics/knowledge-work-plugins are adopted as a
  skills-first port. The mukul975 cybersecurity skills pack is held. ADR-004
  records the decision.

  @R-15 @holds-today
  Scenario: Every third-party asset declares its pin and verification
    Given the assets block of the manifest
    When the validator runs
    Then it requires one complete declaration per asset with its upstream, release or pin, and verification

  @R-15 @holds-today
  Scenario: A vendored skill tree is pinned by commit and archive digest
    Given the pstack asset in the manifest
    When its declaration is read
    Then it names a cursor/plugins commit and the sha256 of that commit's archive

  @R-16 @holds-today
  Scenario: The validator admits only the Agent Skills frontmatter fields
    Given a SKILL.md with a field outside name, description, license, compatibility, metadata and allowed-tools
    When the validator runs
    Then it exits 1 naming the unknown field

  @R-17 @holds-today
  Scenario: The cybersecurity skills pack is not installed or referenced
    Given the manifest, the scripts and the installers
    When they are searched for the Anthropic-Cybersecurity-Skills repository
    Then no reference exists

  @R-17 @holds-today
  Scenario: The committed-secret scan covers every tracked file
    Given the validator's committed-secret scan
    When it runs
    Then every tracked, non-ignored file is scanned against the secret rules

  @R-18 @target
  Scenario: A ported knowledge-work skill records its upstream
    Given a skill copied from the engineering or operations plugin into home/dot_agents/skills
    When its SKILL.md frontmatter is read
    Then metadata names the upstream path and the commit 2574e29 it was copied from
    And the Apache-2.0 notice is kept
    And its frontmatter holds only the admitted fields

  @R-18 @target
  Scenario: A ported skill works without Claude Code command substitutions
    Given a ported skill
    When its body is read
    Then it holds no `$ARGUMENTS`, no `@$1` and no `~~connector` placeholder

  @R-19 @target
  Scenario: Drift from the recorded upstream commit is visible
    Given a ported skill with a recorded upstream commit
    When the unit tests run
    Then a test diffs the copy against the recorded upstream text and fails on an unreviewed change
