Feature: Testing, end-to-end coverage without tester-army/e2e
  tester-army/e2e drives browsers and devices. The kit has neither, so it is
  not adopted as a test tool. The bootstrap and the seats stay covered by
  Bats, Python unittest and throwaway containers. Its CI patterns are compared,
  and its skill is listed for a future web or mobile project. ADR-007 records
  the decision.

  @R-28 @holds-today
  Scenario: tester-army/e2e is not a dependency of the kit
    Given the manifest, the scripts, the installers, the Makefile, mise.toml and the workflows
    When they are searched for tester-army or the e2e packages
    Then no reference exists

  @R-29 @holds-today
  Scenario: The bootstrap is run end to end in CI
    Given the Ubuntu workflow
    When it runs on a pull request touching setup.sh or the installers
    Then it runs setup.sh from the checkout and then the Bats file suites

  @R-29 @holds-today
  Scenario: The apply check runs offline in a container
    Given the Makefile's apply-check target
    When it runs
    Then the working tree is applied in a container with no network

  @R-29 @holds-today
  Scenario: Bats runs in CI, not on the operator's host
    Given the Test Policy section of AGENTS.md
    When it is read
    Then it says not to run bats locally and to read the results from GitHub Actions

  @R-30 @holds-today
  Scenario: The unit-test workflow is never path-filtered at the workflow level
    Given the Unit test workflow
    When its trigger block is read
    Then it says a required check must always report a final status and carries no workflow-level paths filter

  @R-30 @target
  Scenario: The gate-job pattern is compared for the platform workflows
    Given the Ubuntu and macOS workflows, which filter by paths at the workflow level
    When the comparison unit runs
    Then it records whether each stays an optional check or gains a changes job and a gate job

  @R-31 @target
  Scenario: The e2e skill is installed only for a web or mobile project
    Given a future project with a browser or device surface
    When its agent session needs end-to-end tests
    Then the e2e skill is installed for that project with a skills.audience entry
    And nothing in this repository changes for it
