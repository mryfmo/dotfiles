Feature: Sandbox layering, srt for the omp seats and the Claude Bash sandbox, Codex on its own
  Anthropic's sandbox-runtime (srt) is the OS boundary for the omp seats and
  the engine behind the Claude Code Bash sandbox. Codex keeps its own Seatbelt
  and bubblewrap sandbox, because srt cannot wrap it. The kit adds no sandbox
  of its own and pins the srt version instead of following `latest`. ADR-002
  records the decision.

  @R-06 @holds-today
  Scenario: The Claude Bash sandbox is strict and fails closed
    Given the claude.sandbox block of the manifest
    When it is read
    Then the sandbox is enabled, failIfUnavailable is true and allowUnsandboxedCommands is false
    And the excluded commands are exactly `git push *` and `gh *`

  @R-06 @holds-today
  Scenario: No Unix socket switch is set in the Claude sandbox
    Given the claude.sandbox block of the manifest
    When it is searched for allowUnixSockets and allowAllUnixSockets
    Then neither key is set

  @R-07 @holds-today
  Scenario: A seat starts only after its sandbox canary holds
    Given hcom-seat launching an orchestrator or worker seat
    When the seat shim runs
    Then it runs a canary under the seat's srt settings before omp starts
    And it refuses to start omp when the canary does not hold

  @R-07 @holds-today
  Scenario: Seat approval is not containment
    Given the orchestrator and worker seat policies
    When their header comments are read
    Then each says approval is not containment and names the srt sandbox as the OS boundary

  @R-08 @target
  Scenario: The srt version is pinned in mise
    Given home/dot_mise/config.toml
    When the sandbox-runtime entry is read
    Then it names one version and not `latest`
    And a bump is a reviewed change that re-reads the behaviours hcom-seat relies on

  @R-09 @holds-today
  Scenario: The Codex audit runs under Codex's own permission profile, never under srt
    Given pr-audit.sh, the Codex audit route
    When its text is read
    Then it runs codex under the `audit` permission profile with a scratch HOME
    And it never invokes srt

  @R-10 @holds-today
  Scenario: Sandboxed commands cannot read the SSH keys
    Given the claude.sandbox credentials block of the manifest
    When its file entries are read
    Then ~/.ssh is denied

  @R-10 @target
  Scenario: The first Linux seat run is measured before it is relied on
    Given an Ubuntu host with bubblewrap, socat and ripgrep installed
    When the first seat is launched there
    Then the canary result and the open srt Linux issues are recorded in the program's records
    And a canary exit 2 stops the seat rather than running it uncontained
