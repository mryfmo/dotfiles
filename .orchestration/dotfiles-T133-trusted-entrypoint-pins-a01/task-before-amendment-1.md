---
format: 2
task_id: dotfiles-T133-trusted-entrypoint-pins-a01
kind: code
security: true
allowed_files: ["home/dot_mise/config.toml","tests/unit/test_generate_agent_configs.py",".orchestration/dotfiles-T133-trusted-entrypoint-pins-a01/**"]
after: []
threat_table:
  - {"control":"home/dot_mise/config.toml","disposition":"closed: tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_trusted_entrypoint_mise_versions_are_exact"}
  - {"control":"tests/unit/test_generate_agent_configs.py","disposition":"residual: The installed-command regression retains full equality and synthetic migration coverage; owner dotfiles-T133-trusted-entrypoint-pins-a01, selector tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_managed_hooks_use_installed_permgate_paths."}
  - {"control":".orchestration/dotfiles-T133-trusted-entrypoint-pins-a01/**","disposition":"residual: Only task copies, reports and review/validation data are allowed; no executable helper or runtime configuration; owner dotfiles-T133-trusted-entrypoint-pins-a01."}
  - {"control":"predecessor/current task copies","disposition":"residual: Preserve predecessor copies and compare .orchestration/dotfiles-T133-trusted-entrypoint-pins-a01/task.md with the complete dispatched bytes and SHA-256; owner dotfiles-T133-trusted-entrypoint-pins-a01."}
  - {"control":"task metadata","disposition":"residual: Check this id, security true, after [] and exactly three allowed entries before dispatch and acceptance; owner dotfiles-T133-trusted-entrypoint-pins-a01."}
  - {"control":"metadata separators","disposition":"residual: Parse front matter as data, reject duplicate keys and compare separators with the complete dispatched text; owner dotfiles-T133-trusted-entrypoint-pins-a01."}
  - {"control":"evidence","disposition":"residual: Record producer, seat kind, full base/head, outputs and statuses; historical probes never approve a new head; owner dotfiles-T133-trusted-entrypoint-pins-a01."}
  - {"control":"in-process effects","disposition":"residual: Tests use temporary data; no mise install/update, chezmoi apply or live hook execution is authorized; owner dotfiles-T133-trusted-entrypoint-pins-a01."}
  - {"control":"workflow and interpreter or environment inputs — every mise consumer","disposition":"residual: Pins intentionally stop latest tracking for herdr-agents, make targets and CI's mise setup; render checks and final-head CI bound the change, with remaining runtime compatibility owned by dotfiles-T133-trusted-entrypoint-binding-followup-a01."}
  - {"control":"new or renamed scripts","disposition":"residual: None is authorized; reuse existing generator/template helpers and keep artifact files data-only; owner dotfiles-T133-trusted-entrypoint-pins-a01."}
  - {"control":"orchestrator effect merge","disposition":"residual: Only the orchestrator integrates the reviewed final head through Playbook step 10; shared-credential risk remains; owner dotfiles-T133-trusted-entrypoint-pins-a01."}
  - {"control":"orchestrator effect update-branch","disposition":"residual: Only the orchestrator updates the branch and refreshes evidence after a head change; owner dotfiles-T133-trusted-entrypoint-pins-a01."}
  - {"control":"orchestrator effect forced worker removal","disposition":"residual: None is planned; only the orchestrator may remove a worker and record discarded state; owner dotfiles-T133-trusted-entrypoint-pins-a01."}
  - {"control":"design 5.14 item 0","disposition":"residual: Declaration tests do not close item 0; its same-UID and credential residuals remain with owner dotfiles-T133-trusted-entrypoint-binding-followup-a01."}
  - {"control":"design 5.14 item 1","disposition":"residual: Pinning supplies declaration data only; item 1 protection remains with owner dotfiles-T133-trusted-entrypoint-binding-followup-a01."}
  - {"control":"design 5.14 item 2","disposition":"residual: No execution boundary is implemented here; item 2 remains with owner dotfiles-T133-ci-efficiency-followup-a04."}
  - {"control":"design 5.14 item 3","disposition":"residual: A resolution probe is observation only; item 3 validation remains with owner dotfiles-T133-ci-efficiency-followup-a04."}
  - {"control":"design 5.14 item 4","disposition":"residual: Exact declaration assertions do not verify installed executable identity; owner dotfiles-T133-trusted-entrypoint-binding-a01."}
  - {"control":"design 5.14 item 5","disposition":"residual: Full base/head and task-copy SHA-256 identify this proposal; no new reservation is introduced; owner dotfiles-T133-trusted-entrypoint-pins-a01."}
  - {"control":"design 5.14 item 6","disposition":"residual: Report declaration, test and CI evidence separately from unperformed deployment; owner dotfiles-T133-trusted-entrypoint-pins-a01."}
  - {"control":"design 5.14 item 7","disposition":"residual: Red/green pin and installed-command regressions cover this split only; broader verification remains with owner dotfiles-T133-trusted-entrypoint-binding-a01."}
  - {"control":"design 5.14 item 8","disposition":"residual: This task and local evidence grant no integration authority; Playbook step 10 remains required; owner dotfiles-T133-trusted-entrypoint-pins-a01."}
  - {"control":"design 5.14 item 9","disposition":"residual: This task changes version input only; item 9 execution controls remain with owner dotfiles-T133-ci-efficiency-followup-a04."}
  - {"control":"design 5.14 item 10","disposition":"residual: All commands remain sandboxed; denial produces blocked evidence without escalation or another execution surface; owner dotfiles-T133-trusted-entrypoint-pins-a01."}
premises:
  - {"producer":"worker (Codex seat)","command":"rg -n '^(uv|python|node) = ' home/dot_mise/config.toml","output":"3:node = \"latest\"\n6:python = \"3.15.0\"\n18:uv = \"latest\""}
  - {"producer":"worker (Codex seat)","command":"wc -l home/dot_mise/config.toml tests/unit/test_generate_agent_configs.py","output":"      80 home/dot_mise/config.toml\n    2350 tests/unit/test_generate_agent_configs.py\n    2430 total"}
---

# AGMSG-TASK dotfiles-T133-trusted-entrypoint-pins-a01 — exact trusted-entrypoint pins

Worker: a Codex seat (worktree named at dispatch)
Worker profile: standard; max_turns=8.

## Objective and binding source

This is the second, separate task file specified in `.orchestration/tasks/dotfiles-T133-trusted-entrypoint-binding-a01.md`, lines 398–410. It has exactly the three allowed_files entries above. Accept it before dispatching `dotfiles-T133-ci-efficiency-followup-a04` (the resolver) or `dotfiles-T133-trusted-entrypoint-binding-a01`; both consume the pinned declaration read-only. No primary binding implementation is authorized.

Pin uv=0.13.1, python=3.15.0 and node=26.12.0 in home/dot_mise/config.toml, replacing only those latest values. Add one English comment explaining the trusted-entrypoint pins; preserve every other tool and setting. Do not install or apply anything.

[memory:decision] Current authoring probes above show Python already at 3.15.0; retain it and replace only remaining latest values. The comment must explain all three trusted-entrypoint pins. The user-visible effect is that these tools stop following latest in every mise consumer.

In GenerateAgentConfigsTest add test_trusted_entrypoint_mise_versions_are_exact, red before the config change and green afterward. Refactor test_managed_hooks_use_installed_permgate_paths to compare the complete rendered PermissionRequest command with the real manifest declaration rendered through the existing template helper; retain exactly one managed entry, permgate executable-leaf/claude-argument checks and the Codex assertion. Keep synthetic legacy-command fixtures. The primary task adds strict bound-sequence and parent-selected-manifest validation.

Use the existing tomllib import, load_manifest_fixture and render_claude_template helpers. Remove only the installed-template legacy literal pin; synthetic legacy/custom/idempotence cases remain unchanged. Do not edit generators, manifests, templates, launchers, workflows, resolver code or other tests.

## Host premises and design references

The version choices and historical host probes bind by reference to the shared `premises` and `Applicable design — C-88 verbatim quotations` in `.orchestration/tasks/dotfiles-T133-trusted-entrypoint-binding-a01.md`. Design source: `.orchestration/plans/024-design-quality.md`, §5.14 items 0–10, especially 1, 2 and 9. Apply those references without restating their execution contract.

Historical host facts; producer: orchestrator (Claude seat, sandboxed Bash): mise at `$HOME/.local/bin/mise`; `env -i PATH=/usr/bin:/bin HOME="$HOME" "$HOME/.local/bin/mise" which uv` -> `$HOME/.local/share/mise/installs/uv/<version>/uv-<target>/uv` (no `bin` subdirectory, no pin file); python 3.15.0 at `$HOME/.local/share/mise/installs/python/3.15.0/bin/python3`.

The worker (Codex seat) runs that read-only uv resolve command and pastes its actual output; never substitute a guessed installed path. Re-probe the declaration in the dispatched worktree. Do not probe the herdr socket from a Codex sandbox. A mismatch or denial is reported, never repaired by installing or applying tools.

## Validation and change budget

Worker (Codex seat): run `uv run python -m unittest tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_trusted_entrypoint_mise_versions_are_exact -v` red before changing config and green afterward; preserve both outputs and tested revisions. Then run each command separately:

- `make render-check`
- `make validate-agent-assets`
- `uv run python -m unittest tests.unit.test_generate_agent_configs -v`
- `ruff check --config ruff.toml tests/unit/test_generate_agent_configs.py`
- `ruff format --config ruff.toml --check tests/unit/test_generate_agent_configs.py`
- `uv run python -I scripts/lint-comparisons.py --changed <changed paths>`; expand the complete measured diff path list as separate arguments.

Do not run Bats locally. Preserve synthetic legacy migration checks; report baseline failures and unrun commands honestly. No lint-baseline edits, suppressions or extra helper files are authorized.

Source budget: three replacements (6 additions/deletions), one reason comment and 5 margin lines = 12. Test budget: about 12 pin-assertion lines, 24 installed-command refactor lines and 4 margin lines = 40.

The final diff has at most 12 changed lines outside `tests/` and `.orchestration/`, and 40 under `tests/`.

Measure `git diff --numstat <base40>...<head40>`.

The orchestrator pastes base40 at dispatch; head40 is the final RESULT head, both full 40-hex SHAs. For a records-only round after update-branch, base40 is the branch head at that dispatch. Count additions plus deletions, paste per-file numstat and both totals, and exclude only records from the source cap. An overrun blocks; the worker does not raise caps.

## Dispatch, evidence and completion

The orchestrator (Claude seat, sandboxed Bash) obtains and reads the accepted task-consistency checker/test revision before dispatch; check C1–C10, C7b and C11 and this task's regime-copy checks before dispatch and acceptance. Re-probe premises manually rather than executing unchecked premise strings. C-80 pre-dispatch security-profile text review has at most 2 rounds; dispatch requires no surviving P0/P1, and a need for a third round stops for re-plan.

Completion: create tools/trusted-entrypoint-pins-a01 and one PR; write task.md, report.md, validation.md, sandbox.md, learning.md, autoskill.md and worker review evidence under .orchestration/dotfiles-T133-trusted-entrypoint-pins-a01/. The primary task's quoted Completion round, sandbox, CI/Bot and integration rules apply with this task's own identifiers; no predecessor deletion is authorized. Advisory owner is dotfiles-T133-trusted-entrypoint-binding-followup-a01, created before disposition. Only the orchestrator integrates; no deployment is claimed.

Every evidence item names its producer and seat kind: `orchestrator (Claude seat, sandboxed Bash)` or `worker (Codex seat)`; review evidence also names its profile. validation.md contains verbatim stdout/stderr and real exit statuses for every executed command, including red/green selectors, probes, lint and numstat. Record full base/head, branch, PR, changed paths, task-copy SHA-256, row-to-selector mapping, limits and `cost: n/a` unless observed.

Keep the complete task copy byte-identical to dispatch; the orchestrator compares bytes and SHA-256 rather than trusting a reported hash. Preserve predecessor evidence. Keep plan/todo/learn worklogs uncommitted, with at most one active todo per owner. Use [memory:decision] / [memory:failure] for durable facts under the existing memory procedure.

Complete agent-side review with resolved repo-local JSON and receipt under the allowed artifact directory and run the required review gate. Do not open or publish a browser review. Commit/push only task changes; wait for final-head green CI and the bounded automatic Bot window, recording `bot: none` on expiry. Do not post `@codex review`. The orchestrator dispositions findings and follows Playbook step 10 for integration.

Every command stays in the sandbox. On denial, send `AGMSG-PONG v1 task_id=dotfiles-T133-trusted-entrypoint-pins-a01 status=blocked` with the exact command and boundary; do not retry through another execution surface. Before RESULT write result.txt under the task artifact directory; send AGMSG-RESULT with status, final head, task_copy and all artifact paths, including precheck evidence required by the accepted regime.

## Checks (pasted by the orchestrator before each send)

