---
format: 2
task_id: dotfiles-T133-trusted-exec-contract-tests-a01
kind: code
security: false
design: 5.14 items 2, 3, 7, 9
worker: a011
worktree: .claude/worktrees/worker-d
allowed_files:
  - tests/unit/trusted_exec_contract.py
  - tests/unit/test_trusted_exec_contract.py
  - .orchestration/dotfiles-T133-trusted-exec-contract-tests-a01/**
after: []
rendered_forms: []
threat_table:
  - control: tests/unit/trusted_exec_contract.py
    disposition: "residual: A wrong helper could hide a probe that passes vacuously; deliberately failing consumer stubs must trigger its assertions, and final-head review checks the actual subprocess and filesystem observations."
  - control: tests/unit/test_trusted_exec_contract.py
    disposition: "residual: A wrong expectation or inert consumer stub could hide a probe that passes vacuously; each negative case must demonstrate its attack occurred before asserting rejection, alongside a passing consumer."
  - control: .orchestration/dotfiles-T133-trusted-exec-contract-tests-a01/**
    disposition: "residual: Incomplete evidence could hide a probe that passes vacuously; preserve raw test output, per-probe red and green observations, the dispatched task copy and final-head numstat for comparison."
  - control: "the helper's own tests prove each probe detects the condition it probes (a deliberately failing consumer stub per probe)"
    disposition: "closed: tests/unit/test_trusted_exec_contract.py::TrustedExecContractTest::test_each_probe_detects_condition"
    probe_selectors:
      shim_on_path: tests/unit/test_trusted_exec_contract.py::TrustedExecContractTest::test_shim_probe
      hostile_git: tests/unit/test_trusted_exec_contract.py::TrustedExecContractTest::test_hostile_git_probe
      worker_root: tests/unit/test_trusted_exec_contract.py::TrustedExecContractTest::test_worker_root_probe
      swapped_file: tests/unit/test_trusted_exec_contract.py::TrustedExecContractTest::test_swapped_file_probe
      sanitized_environment: tests/unit/test_trusted_exec_contract.py::TrustedExecContractTest::test_sanitized_environment_probe
      trusted_parent: tests/unit/test_trusted_exec_contract.py::TrustedExecContractTest::test_trusted_parent_probe
  - control: task metadata
    disposition: "residual: The orchestrator checks format, identity, three allowed_files entries, security false, empty after and task-copy equality before dispatch and acceptance."
  - control: metadata separators
    disposition: "residual: The complete byte-identical task copy includes its front-matter separators; evidence never becomes an executable instruction source."
  - control: in-process effects
    disposition: "residual: All fixture mutations and subprocesses remain inside the worker sandbox with temporary HOME and explicit cleanup, including when an assertion fails."
  - control: workflow and interpreter or environment inputs
    disposition: "residual: No workflow or interpreter configuration changes; tests exercise clean child environments and simulate directory-service home responses without accessing a real home."
  - control: new or renamed scripts
    disposition: "residual: Only the two named Python test modules are added; fixture executables are temporary data, and no production launcher or artifact-directory runtime helper is introduced."
  - control: orchestrator effect merge
    disposition: "residual: The worker never merges; the orchestrator applies Worker RESULT acceptance and Orchestrator Playbook step 10 to the reviewed final head."
  - control: orchestrator effect update-branch
    disposition: "residual: Only the orchestrator updates an in-flight PR branch; changed heads require refreshed CI, feedback and audit evidence before integration."
  - control: orchestrator effect forced worker removal
    disposition: "residual: No forced removal is planned; worker cleanup removes only its temporary fixtures and never removes another worktree or seat."
premises:
  - claim: "The authoring host's installed Python reports this version; this observation is not a new interpreter pin."
    command: python3 --version
    output: |-
      Python 3.15.0
  - claim: "The authoring host is macOS."
    command: uname -s
    output: |-
      Darwin
  - claim: "The macOS directory-service executable exists; getent is absent on this host."
    command: "python3 -c 'import shutil; print(\"dscl=\" + str(shutil.which(\"dscl\"))); print(\"getent=\" + str(shutil.which(\"getent\")))'"
    output: |-
      dscl=/usr/bin/dscl
      getent=None
  - claim: "The helper path is absent from origin/main at the observed base."
    command: git ls-tree --name-only origin/main -- tests/unit/trusted_exec_contract.py
    output: ""
    exit_code: 0
  - claim: "The origin/main used for the absence observation has this full commit identity."
    command: git rev-parse origin/main
    output: |-
      ba318e5369b14a79d6f515e87b685c9bcb30c12e
---

# AGMSG-TASK dotfiles-T133-trusted-exec-contract-tests-a01

🤖 I read the AGENTS.md for mryfmo/dotfiles.

## Goal and boundary

[​memory:decision] Plan 024 creates the shared verification helper before its production consumers; this is a test-only task for Claude worker seat a011 in worker-d.

Create `tests/unit/trusted_exec_contract.py` and `tests/unit/test_trusted_exec_contract.py`, using only the Python standard library. The helper exposes plain functions and one mixin usable with `unittest.TestCase`. Context-manager functions may own temporary fixtures; no fixture framework, dependency or production resolver is added.

The helper's own tests are its only consumers in this task. P1-6 slice 1, `dotfiles-T133-record-ledger-carry-a01`, and the P1-15 successors import it later. Do not edit those consumers, production scripts, settings, hooks, permissions, workflows, pins or dependency files.

`security: false` applies because this task changes tests only, changes no production trust-boundary code and executes nothing outside the worker sandbox.

## Design references

Apply `.orchestration/plans/024-design-quality.md` section 5.14 by reference under D-024-30.

This task relies on design 5.14 item 2 by reference.
This task relies on design 5.14 item 3 by reference.
This task relies on design 5.14 item 7 by reference.
This task relies on design 5.14 item 9 by reference.

Do not copy, restate or paraphrase those items into this task or its evidence. A threat row naming a design item's wording does so only for the exact wording its named test asserts; the probe requirements below specify this helper's behavior without claiming coverage of entire design items.

## Sandbox and artifacts

Worker Playbook step 4 applies: every command, test, Git operation and tool call completes inside the sandbox and allowlist. This task authorizes no exception for gh, push, directory-service commands, messaging, artifact publication or memory writes.

If a command is denied or requires leaving that boundary, stop the dependent work and send `AGMSG-PONG v1 task_id=dotfiles-T133-trusted-exec-contract-tests-a01 status=blocked` through the available in-sandbox delivery path, naming the exact command, failure and boundary. Never retry unsandboxed, request an escape, change permissions or pursue the same operation through another tool.

Re-run the read-only premises at worker start and paste their actual outputs. A different platform or installed Python is recorded as an observation; select the corresponding supported platform branch without changing production pins.

Write all persistent artifacts under `.orchestration/dotfiles-T133-trusted-exec-contract-tests-a01/` in worker-d:

- `task.md`: byte-identical dispatched task text.
- `report.md`: RESULT details, scope, API names, limitations and cost.
- `validation.md`: exact commands, exit statuses and pasted outputs.
- `sandbox.md`: isolation, temporary HOME, cleanup and refused commands.
- `learning.md` and `autoskill.md`: reusable-learning triage and not-used status where applicable.
- `result.txt`: the RESULT fields before sending.
- Worker Crit-data JSON and receipt, using the `-worker-` infix.

The artifact wildcard permits task records only, never an additional executable helper. The worker does not write artifacts into the main checkout.

## Helper requirements

1. **Shim-on-PATH probe.** Create a temporary bin directory containing executable shims named `uv`, `python3`, `gh`, `git` and `bash`. Each records its executable name and complete argv to a fixture-owned file and exits non-zero. Prepend the directory to the environment offered to a consumer. Provide an assertion that none ran. Use an absolute shim interpreter and unambiguous argument recording; logging must not depend on finding another tool through the poisoned PATH.

2. **Hostile Git probe.** Create fixture repositories, attacker-controlled paths and an environment exporting `GIT_DIR`, `GIT_WORK_TREE`, `GIT_CONFIG_GLOBAL`, `GIT_CONFIG_SYSTEM`, `GIT_CEILING_DIRECTORIES` and `GIT_ALTERNATE_OBJECT_DIRECTORIES`. Plant repository-local `core.worktree` and `include.path` in the fixture repository's real `.git/config`. Supply distinguishable legitimate and attacker file contents so a consumer can assert both its confirmed root and subsequent file accesses remain unaffected. Never modify the worker repository's Git configuration. Exercise environment and local-config attacks separately so one successful redirection cannot conceal an inert second attack.

3. **Worker-root trusted-path probe.** Supply fixture paths under `<root>/.claude/worktrees/<name>/` as existing inputs and as output destinations, including a destination not yet created. The consumer asserts refusal and absence of reads or writes there. Keep these fixture paths separate from the actual worker checkout.

4. **Swapped-file probe.** Provide a deterministic callback or barrier that replaces a checked fixture file with a symlink to attacker content before use. No sleeps or probabilistic race loop. The consumer asserts it never reads the attacker content. Include a case-alias path on a case-insensitive filesystem, with filesystem identity measured rather than inferred from the OS name. On a case-sensitive filesystem, report that alias subcase as unsupported with the measured reason; do not count it as passed.

5. **Sanitized-environment assertion.** Compare the observed child environment's name set for equality with `PATH`, `HOME`, `LANG` and the names explicitly declared by that consumer. Require `PATH=/usr/bin:/bin`. Reject missing allowed names, undeclared names and a different PATH. Do not silently exempt shell bookkeeping variables; a shell consumer declares any such names it actually exports.

6. **Trusted-parent runner.** Export exactly `run_under_trusted_parent(script, *args)`. Start the child with this argv shape:

   ```text
   /usr/bin/env -i PATH=/usr/bin:/bin HOME=<passwd home> LANG=C.UTF-8 /bin/bash --noprofile --norc -p <abs script> [args...]
   ```

   Pass argv directly, without shell interpolation, and give the initial subprocess an empty inherited environment. Preserve each argument as one argument.

   Obtain the real UID's passwd home from its passwd entry (`pwd.getpwuid(os.getuid()).pw_dir`), never from `HOME`, a caller sentinel or a PATH lookup. Cross-check it with `/usr/bin/dscl . -read` on the account record formed from `"/Users/"` and the real UID's username on macOS, or `/usr/bin/getent passwd` with the real UID on Linux, when that lookup can run; both seat sandboxes refuse `dscl` (measured at revise 1, ACCEPTANCE of 2026-10-20), so a lookup that cannot run leaves the passwd entry standing alone, and a lookup that answers differently or malformed is refused. Amendment 1 (2026-10-20T12:2xZ; `previous_sha256: dd7549118bd470af98f52096ee668165a53727981eba4cb8466550641e2dc12c`) records the measured behaviour of revise 1 and changes no code; the task copy on the branch is updated to these bytes in a records-only commit.

   Determine the repository root independently of hostile Git environment variables. Refuse before script execution if the script path is relative, resolves outside that root or is not a regular file. Test traversal, sibling-prefix and symlink escapes. Do not add an alternative production launch path or a caller-selected executable directory.

Every probe owns its cleanup and restores any process state it changes, including on a deliberately failing assertion. Prefer passing environment mappings to subprocesses over changing the test runner's global environment.

Every filesystem write, marker, cache and fixture stays under a temporary directory inside the worker sandbox. Never read or write the real passwd home through a test child.

For runner tests, substitute only the directory-service lookup response with a temporary passwd-home value and bind repository-root discovery to a temporary fixture root. Exercise real `/usr/bin/env` and `/bin/bash` children there. Test the exact lookup argv and parsing for both supported OS branches using standard-library mocks; do not mock away the execution or observations the runner test claims to verify.

## Helper tests and non-vacuity

Write the tests before implementing the helper. Use the six `TrustedExecContractTest` selectors declared in the threat row.

For each probe, run a deliberately noncompliant consumer stub and demonstrate that the helper's contract assertion fails for the intended reason; then run a compliant stub and demonstrate that it passes. A subprocess returning non-zero alone does not prove a probe detected anything.

Required observations include actual shim argv records; attacker root or content exposure; worker-root access attempts; swapped-content consumption; the rejected environment mapping; and rejected or incorrectly constructed parent execution.

For the trusted-parent runner, include an intentionally wrong launch stub so the assertion detects inherited environment or wrong argv, then the real helper launch with temporary passwd-home data. Rejected script paths must leave an execution marker absent.

The aggregate selector `TrustedExecContractTest::test_each_probe_detects_condition` exercises the six named sensitivity cases with subtests and requires the expected assertion failure for each deliberately wrong consumer. It may share case functions with the individual tests. A no-op assertion or an attack that never occurred must make this selector fail.

Also verify cleanup after exceptions, argv preservation, allowed-environment success and failure cases, both passwd lookup branches, and fixture-only Git configuration changes.

## Check

Run the focused suite inside the sandbox with temporary `HOME` and temporary `UV_CACHE_DIR`, using the installed interpreter explicitly through the existing uv workflow:

```text
uv run --no-project --offline --python <observed absolute Python> python -B -m unittest discover -s tests/unit -p test_trusted_exec_contract.py -v
```

Record the expanded command, temporary-environment setup, complete output and exit status. No local Bats execution. Run relevant existing Python checks and required formatting checks without editing unrelated files; a sandbox denial is a blocked PONG.

The helper is at most 250 lines and its own tests at most 350 lines, including comments and blank lines. At RESULT, paste `git diff --numstat origin/main...HEAD` and measure additions plus deletions separately for each named file; these new files must meet their respective caps. Also record final file line counts. Do not move code into the artifact directory to meet a cap.

The task text is at most 250 lines and has exactly the three declared allowed_files entries.

Use agent-side Crit data and a repo-local worker receipt under the authorized artifact directory. Do not open a browser review or ask the operator to review. Run `make require-crit-review` before completion and satisfy any required evidence without leaving the sandbox.

## Completion

Write an `AGMSG-RESULT v1` with `status=ready_for_review` only after the required checks pass; otherwise report `status=blocked` with evidence.

The RESULT report and validation identify:

- Full `head`, base, branch, changed files and dispatched task-copy SHA-256.
- The pasted `git diff --numstat origin/main...HEAD`, per-file cap calculations and final line counts.
- The expanded test command, exit status and full test run output pasted verbatim.
- Every probe red against a deliberately failing stub, then green against a compliant stub, with its exact selector and observed failure reason.
- Separate results for hostile Git environment/local configuration and swapped-file/case-alias subcases; unsupported alias coverage remains explicitly unproved.
- Actual platform and Python observations, directory-service branch coverage, temporary HOME and cleanup evidence.
- Review JSON, receipt, gate output and all artifact paths; CI/PR identifiers only when actually obtained inside the sandbox.
- `cost:` with observed figures or `n/a`, and any denied commands or unperformed checks.

[​memory:decision] This RESULT establishes a shared test helper and its sensitivity tests; production consumer adoption remains with P1-6 slice 1 and the P1-15 successors.

Production behavior and live deployment are not checked here; a defective helper can hide a vacuous pass, so preserve the negative-control evidence and any unsupported filesystem coverage.

## Checks (pasted by the orchestrator before each send)

```
dispatch to a011 (worker-d), 2026-10-19T23:29:36Z; task-consistency-check.py: OK; security: false (test-only helper; no C-80); design 5.14 by reference (D-024-30); files disjoint from every in-flight task (a010 P1-15, a012 P1-12, a008 #432, a011 #434 records); measured text: 198 lines, 3 allowed files; the operator's relayed direction of 2026-10-19T22:59Z suggestion (b)
```