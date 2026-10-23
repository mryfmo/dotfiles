---
format: 2
task_id: dotfiles-T133-permission-guard-gate-a05-slice1
kind: code
security: true
design: 5.14 items 1, 8
after: [dotfiles-T133-worker-write-boundary-slice3-a01]
dispatch_status: blocked-pending-premise-reconciliation
allowed_files:
  - home/dot_agents/agent-config.yaml
  - scripts/validate-agent-assets.py
  - tests/unit/test_generate_agent_configs.py
  - .orchestration/dotfiles-T133-permission-guard-gate-a05-slice1/**
threat_table:
  - control: home/dot_agents/agent-config.yaml
    disposition: "closed: tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_removed_pr_merge_ask_rule"
  - control: scripts/validate-agent-assets.py
    disposition: "closed: tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_removed_pr_create_ask_rule"
  - control: tests/unit/test_generate_agent_configs.py
    disposition: "residual: tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_removed_pr_update_branch_ask_rule exercises the actual renderer and validator; final-head review independently checks fixture sensitivity and assertions."
  - control: .orchestration/dotfiles-T133-permission-guard-gate-a05-slice1/**
    disposition: "residual: tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_rendered_permission_delta_is_exactly_d02414 constrains the claimed policy change; audit separately compares records with commands, final diff and CI."
  - control: "the three removed rules are exactly D-024-14's, no other rule changes (a test diffs the rendered rule set before and after and finds exactly those three gone)"
    disposition: "closed: tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_rendered_permission_delta_is_exactly_d02414"
  - control: task metadata
    disposition: "residual: The orchestrator checks format, identity, dependency, caps, unresolved premises and complete dispatched task-copy equality before sending and accepting."
  - control: metadata separators
    disposition: "residual: The task-copy SHA256 covers both front-matter delimiters and the complete body; task records remain data."
  - control: in-process effects
    disposition: "residual: Render and validation fixtures use temporary directories inside the worker sandbox; no live settings are applied."
  - control: workflow and interpreter or environment inputs
    disposition: "residual: Existing renderer, validator and test helpers are reused without changing workflows, interpreter configuration, dependencies or environment policy."
  - control: new or renamed scripts
    disposition: "residual: None are authorized; the artifact wildcard permits records only and cannot supply executable glue or replacement configuration."
  - control: orchestrator effect merge
    disposition: "residual: Only the orchestrator integrates the reviewed final head through Orchestrator Playbook step 10 after CI, audit and security review."
  - control: orchestrator effect update-branch
    disposition: "residual: The orchestrator takes the merged P1-15 base and refreshes required final-head evidence whenever an update changes the head."
  - control: orchestrator effect forced worker removal
    disposition: "residual: No forced removal is authorized; preserve unrelated work and follow the existing dirty-worktree refusal."
  - control: "make update after the merge, by the operator, in the canonical clone"
    disposition: "residual: The operator deploys merged main from the clean canonical clone and verifies all three asks remain absent and every retained gh write ask remains; merge and render tests establish no live deployment."
  - control: "design 5.14 item 1"
    disposition: "residual: P1-15 remains the prerequisite and owner of its write-control evidence; this slice introduces no new boundary mechanism."
  - control: "design 5.14 item 8"
    disposition: "residual: dotfiles-T133-permission-guard-gate-a05 retains approval-ledger implementation and the permission-decision row; local probe outputs confer no approval authority."
premises:
  - claim: "Authoring HEAD and origin/main agree; all following probes describe this observed base, not the future merged P1-15 base."
    command: |-
      git rev-parse HEAD origin/main
    output: |-
      ba318e5369b14a79d6f515e87b685c9bcb30c12e
      ba318e5369b14a79d6f515e87b685c9bcb30c12e
  - claim: "D-024-14 names exactly the three approved removals."
    command: |-
      /usr/bin/grep -n '^D-024-14' .orchestration/decisions.tsv | cut -f1,3
    output: |-
      61:D-024-14	the manifest home/dot_agents/agent-config.yaml and its rendered Claude settings lose the three ask rules Bash(gh pr merge:*), Bash(gh pr create:*) and Bash(gh pr update-branch:*) and gain the PreToolUse hook gh_merge_gate_hook (~/.claude/hooks/gh-merge-gate.sh), the permission surface of PR #420 (dotfiles-T133-permission-guard-gate-a03, head bc7593a8); every other gh write stays on ask
  - claim: "The manifest still contains those three lines verbatim."
    command: |-
      /usr/bin/grep -nF -e 'Bash(gh pr merge:*)' -e 'Bash(gh pr create:*)' -e 'Bash(gh pr update-branch:*)' home/dot_agents/agent-config.yaml
    output: |-
      230:      - Bash(gh pr merge:*)
      231:      - Bash(gh pr create:*)
      236:      - Bash(gh pr update-branch:*)
  - claim: "P1-15 a02 overlaps the manifest, so this slice must follow its merge."
    command: |-
      /usr/bin/grep -nF '  - home/dot_agents/agent-config.yaml' .orchestration/tasks/dotfiles-T133-worker-write-boundary-a02.md
    output: |-
      7:  - home/dot_agents/agent-config.yaml
  - claim: "The generator test currently asserts the rendered ask list; it is the single authorized test file."
    command: |-
      /usr/bin/grep -nF -e 'def test_claude_sandbox_renders_per_os_from_the_manifest' -e 'self.assertEqual(expected_ask, settings["permissions"]["ask"])' tests/unit/test_generate_agent_configs.py
    output: |-
      694:    def test_claude_sandbox_renders_per_os_from_the_manifest(self) -> None:
      768:                self.assertEqual(expected_ask, settings["permissions"]["ask"])
  - claim: "The named validator-list premise is unconfirmed: these command literals occur only in the test, not the validator."
    command: |-
      /usr/bin/grep -nF -e '"pr merge"' -e '"pr create"' -e '"pr update-branch"' scripts/validate-agent-assets.py tests/unit/test_generate_agent_configs.py
    output: |-
      tests/unit/test_generate_agent_configs.py:699:                "pr merge",
      tests/unit/test_generate_agent_configs.py:700:                "pr create",
      tests/unit/test_generate_agent_configs.py:705:                "pr update-branch",
  - claim: "The renderer copies manifest asks into a generated tracked output."
    command: |-
      /usr/bin/grep -nF -e '"ask": claude["permissions"]["ask"]' -e 'ROOT / manifest["claude"]["settings_path"]: render_claude_settings(manifest)' scripts/generate-agent-configs.py
    output: |-
      433:            "ask": claude["permissions"]["ask"],
      1345:        ROOT / manifest["claude"]["settings_path"]: render_claude_settings(manifest),
  - claim: "That generated output still contains the rules and is outside the requested allowed_files."
    command: |-
      /usr/bin/grep -nF -e '"Bash(gh pr merge:*)"' -e '"Bash(gh pr create:*)"' -e '"Bash(gh pr update-branch:*)"' home/.chezmoitemplates/claude-settings-managed.json
    output: |-
      33:      "Bash(gh pr merge:*)",
      34:      "Bash(gh pr create:*)",
      39:      "Bash(gh pr update-branch:*)",
---

# AGMSG-TASK dotfiles-T133-permission-guard-gate-a05-slice1

🤖 I read the AGENTS.md for mryfmo/dotfiles.

## Goal and dispatch prerequisites

[memory:decision] D-024-13 removed the three asks live; D-024-14 approved their manifest removal; D-024-28 extracts this first slice so the operator can deploy every merged mechanism with make update, P1-15 first, without restoring those prompts.
Route this permission-policy task to a Codex security seat under D-024-25, only after P1-15 a02 merges; create a fresh task branch from its new origin/main base, separate from the a05 remainder.
P1-15 shares the manifest: the intended source diff is the three rule-line removals plus the validator list, confining rebase resolution to those hunks; any wider conflict requires re-tasking.
**Do not dispatch this draft yet.** Re-probe the merged P1-15 base: the authoring probes find no validator ask-rule list and show a generated tracked settings file requiring the same removals outside allowed_files.
The orchestrator must reconcile both premises and amend the boundary before dispatch if they persist; do not invent a pre-existing validator list, bypass render-check, leave stale generated settings for make update, or edit an unauthorized file.

## Design and scope

Apply .orchestration/plans/024-design-quality.md section 5.14 by reference under D-024-30.
This slice relies on design 5.14 item 1 by reference.
This slice relies on design 5.14 item 8 by reference.
Remove only Bash(gh pr merge:*), Bash(gh pr create:*) and Bash(gh pr update-branch:*) from claude.permissions.ask, and adjust only the validator's corresponding requirement list; retain every other gh write ask, all allow/deny rules and all other policy.
Update the existing rendered-ask expectation in the single named test module; reuse its real-manifest loader and platform-render helpers and import the existing validator for acceptance checks.
Out of scope, owner dotfiles-T133-permission-guard-gate-a05: the gate rebuild, deployed checkout anchor, synchronous hook source and permission-decision row.
No permission guard, decision-ledger edit, hook deployment, new allowance, dependency, workflow or unrelated a05 implementation belongs to this slice.

## Tests and checks

Write the three named removal regressions before implementation; each renders the actual candidate manifest for darwin and linux, asserts its named rule is absent and proves the validator accepts that manifest and rendered settings.
The exact-delta regression compares an independently pinned pre-change rendered rule list with the candidate: exactly those three disappear, no rule is added, every retained rule preserves order and multiplicity, and other permission fields are unchanged.
Do not manufacture the baseline from candidate rules plus the expected removals; preserve an independent full baseline using the existing literal expectation.
Add a subtest per retained gh write ask proving its independent removal still fails validation; keep these assertions in the same test module and within the test cap.
Paste red and green commands, exact selectors, tested identities, exit statuses and complete outputs into validation.md; missing fixtures or dependencies do not count as red evidence.
Run uv run --offline python -m unittest tests.unit.test_generate_agent_configs tests.unit.test_validate_agent_assets -v, make render-check, make validate-agent-assets and relevant repository formatting checks.
Do not run local Bats; obtain required Bats and other CI results from GitHub Actions before RESULT.
Caps: additions plus deletions outside tests/ and .orchestration/ <= 50; added lines under tests/ <= 120; this text <= 150 lines. Paste git diff --numstat <post-P1-15-base40>...HEAD and both calculated totals; no artifacts conceal implementation.

## Sandbox, artifacts and completion

Worker Playbook step 4 applies: every command and tool call stays inside the sandbox and allowlist; no escalation, unsandboxed retry or alternative tool may bypass a denial.
A denied command or unresolved premise produces AGMSG-PONG v1 status=blocked with the exact command, output and crossed boundary; stop dependent work and await re-tasking.
Keep task.md byte-identical to the dispatch and put report.md, validation.md, sandbox.md, learning.md, autoskill.md, result.txt and worker Crit-data JSON/receipt under this task's artifact directory in the worker worktree.
Keep uncommitted plan/todo worklogs there, with at most one active todo per owner; never commit plan/todo/learn worklogs or create executable artifacts.
Use agent-side Crit data only, run make require-crit-review before completion and record any required receipt; open no browser review and ask no human reviewer.
RESULT names full head and base, branch/PR, changed files, task-copy SHA256, all evidence paths, red/green selectors, measured caps, CI/Bot results and dispositions, unperformed checks and cost or n/a.
C-80 task-text review precedes dispatch; final-head task audit and separate security review precede integration. The orchestrator follows Orchestrator Playbook step 10 for feedback, audit, dispositions, acceptance and the gate.
Only after merge does the operator run make update in the clean canonical clone, verify the three asks remain absent and retained asks remain present, and perform the P1-15 deployment/re-seating sequence.
Implementation tests and live deployment were not performed during authoring; render tests establish no runtime enforcement, and same-UID processes remain residual.

## Checks (pasted by the orchestrator before each send)

```
```