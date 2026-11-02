Feature: Audit and merge gate
  A unit's pull request merges only at a head the program's ledger records as
  correct, with CI green, through pr-merge.sh. Each audit is one fresh,
  read-only Codex run per head, with the rules taken from the main branch's
  AGENTS.md and the head treated as data. ADR-003 is a stub until the
  security-audit-skill research lands; the scenarios below describe the gate
  as it stands and the one target that the ADR will settle.

  @R-11 @holds-today
  Scenario: The merge lever refuses without a correct verdict row
    Given pr-merge.sh, the orchestrator's merge lever
    When its contract is read
    Then it squash-merges only a head the ledger records as correct with CI passed
    And it passes the head sha with --match-head-commit

  @R-12 @holds-today
  Scenario: The audit rules come from the main branch, never from the head
    Given pr-audit.sh, the Codex audit route
    When it assembles the auditor's prompt
    Then it reads the Audit section of main's AGENTS.md as the rules
    And Codex runs with a scratch HOME so no user skill or instruction file reaches it

  @R-12 @holds-today
  Scenario: The audit profile is read-only at the pinned model and effort
    Given the audit model profile in the manifest
    When the validator runs
    Then it requires codex gpt-6-astra at xhigh reasoning effort with sandbox_mode read-only

  @R-13 @holds-today
  Scenario: Every audit ends with one verdict line
    Given the Audit section of AGENTS.md
    When it is read
    Then it requires exactly one line `Verdict: correct`, `Verdict: incorrect` or `Verdict: blocked`
    And a finding-free audit still records one justified approval

  @R-13 @holds-today
  Scenario: A trust-boundary change carries a threat table
    Given the Audit section of AGENTS.md
    When a pull request touches hooks, permissions, sandbox, policies, levers or credentials
    Then its body must carry a `## Threat table` with one row per changed path and control

  @R-13 @holds-today
  Scenario: The fourth audit round needs a closing decision
    Given pr-audit.sh with a records store
    When a unit reaches its fourth audit round since its last merge
    Then rounds-check runs before anything else and refuses the round without a decisions.tsv row

  @R-14 @target
  Scenario: An advisory review lens reports findings without a verdict
    Given a third-party security-audit skill adopted under ADR-003
    When it reviews a head
    Then its findings enter the review thread as input to the orchestrator
    And it writes no verdict row and changes no gate decision
