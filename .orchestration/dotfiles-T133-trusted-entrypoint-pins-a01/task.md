---
format: 2
task_id: dotfiles-T133-trusted-entrypoint-pins-a01
kind: code
security: true
allowed_files: ["home/dot_mise/config.toml","tests/unit/test_generate_agent_configs.py","tests/unit/test_supply_chain_policy.py",".orchestration/dotfiles-T133-trusted-entrypoint-pins-a01/**"]
after: []
threat_table:
  - {"control":"home/dot_mise/config.toml","disposition":"closed: tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_trusted_entrypoint_mise_versions_are_exact"}
  - {"control":"tests/unit/test_generate_agent_configs.py","disposition":"residual: The installed-command regression retains full equality and synthetic migration coverage; owner dotfiles-T133-trusted-entrypoint-pins-a01, selector tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_managed_hooks_use_installed_permgate_paths."}
  - {"control":"tests/unit/test_supply_chain_policy.py","disposition":"closed: tests/unit/test_supply_chain_policy.py::SupplyChainPolicyTest::test_mise_tools_track_latest_behind_the_cooldown"}
  - {"control":".orchestration/dotfiles-T133-trusted-entrypoint-pins-a01/**","disposition":"residual: Only task copies, reports and review/validation data are allowed; no executable helper or runtime configuration; owner dotfiles-T133-trusted-entrypoint-pins-a01."}
  - {"control":"predecessor/current task copies","disposition":"residual: Preserve predecessor copies and compare .orchestration/dotfiles-T133-trusted-entrypoint-pins-a01/task.md with the complete dispatched bytes and SHA-256; owner dotfiles-T133-trusted-entrypoint-pins-a01."}
  - {"control":"task metadata","disposition":"residual: Check this id, security true, after [] and exactly four allowed entries before dispatch and acceptance; owner dotfiles-T133-trusted-entrypoint-pins-a01."}
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
  - producer: "worker (Codex seat, review-profile authoring context)"
    command: "rg -n '^(uv|python|node) = ' home/dot_mise/config.toml"
    output: |
      3:node = "latest"
      6:python = "3.15.0"
      18:uv = "latest"
---

# AGMSG-TASK dotfiles-T133-trusted-entrypoint-pins-a01 — exact trusted-entrypoint pins

Worker: a Codex seat (worktree named at dispatch)
Worker profile: standard; max_turns=8.

History: amendment 1; previous_sha256: 0908b8f4dbd60000f2d6045bdd74c7d570eacf1c31c83753ddce99f33437b273. PONG 2953 and independent pre-push review P1 exposed the previous text’s omitted supply-chain policy test and adjacent reason-comment requirements; add that fourth allowed entry and raise caps to 16/48. Matching prepared config/test edits remain valid; preserve prior evidence and counters.

## Objective and binding source

This is the second, separate task file specified in `.orchestration/tasks/dotfiles-T133-trusted-entrypoint-binding-a01.md`, lines 398–417. Amendment 1 retains its three original allowed_files entries and adds only `tests/unit/test_supply_chain_policy.py`, for four entries total. Accept it before dispatching `dotfiles-T133-ci-efficiency-followup-a04` (the resolver) or `dotfiles-T133-trusted-entrypoint-binding-a01`; both consume the pinned declaration read-only. No primary binding implementation is authorized.

Pin uv=0.13.1, python=3.15.0 and node=26.12.0 in home/dot_mise/config.toml, replacing only those latest values. Preserve every other tool and setting. Do not install or apply anything.

[memory:decision] Current authoring probes above show Python already at 3.15.0; retain it and replace only remaining latest values. Keep Python’s existing reason comment. Add a one-line English `# ` reason immediately above node and another immediately above uv; use one of these to explain all three trusted-entrypoint pins. The user-visible effect is that these tools stop following latest in every mise consumer.

In GenerateAgentConfigsTest add test_trusted_entrypoint_mise_versions_are_exact, red before the config change and green afterward. Refactor test_managed_hooks_use_installed_permgate_paths to compare the complete rendered PermissionRequest command with the real manifest declaration rendered through the existing template helper; retain exactly one managed entry, permgate executable-leaf/claude-argument checks and the Codex assertion. Keep synthetic legacy-command fixtures. The primary task adds strict bound-sequence and parent-selected-manifest validation.

Use the existing tomllib import, load_manifest_fixture and render_claude_template helpers. Remove only the installed-template legacy literal pin; synthetic legacy/custom/idempotence cases remain unchanged. Do not edit generator code, agent manifests, templates, launchers, workflows, resolver code or tests outside the two allowed modules.

In `SupplyChainPolicyTest.test_mise_tools_track_latest_behind_the_cooldown`, add `held["node"] = "node = "` and `held["uv"] = "uv = "` in the same change as the pins. Keep the held/pinned-set equality assertion, all non-held tools’ latest requirement and the immediately preceding reason-comment check unchanged; do not broaden or bypass this policy.

## Host premises and design references

The version choices and historical host probes bind by reference to the shared `premises` and `Applicable design — C-88 verbatim quotations` in `.orchestration/tasks/dotfiles-T133-trusted-entrypoint-binding-a01.md`. Design source: `.orchestration/plans/024-design-quality.md`, §5.14 items 0–10, especially 1, 2 and 9. Apply those references without restating their execution contract.

Historical host facts; producer: orchestrator (Claude seat, sandboxed Bash): mise at `$HOME/.local/bin/mise`; `env -i PATH=/usr/bin:/bin HOME="$HOME" "$HOME/.local/bin/mise" which uv` -> `$HOME/.local/share/mise/installs/uv/<version>/uv-<target>/uv` (no `bin` subdirectory, no pin file); python 3.15.0 at `$HOME/.local/share/mise/installs/python/3.15.0/bin/python3`.

The worker (Codex seat) runs that read-only uv resolve command and pastes its actual output; never substitute a guessed installed path. Re-probe the declaration in the dispatched worktree. Do not probe the herdr socket from a Codex sandbox. A mismatch or denial is reported, never repaired by installing or applying tools.

## Check — validation and change budget

Worker (Codex seat): retain matching prepared edits and genuine recorded red/green evidence; record tested revisions. Run `uv run python -m unittest tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_trusted_entrypoint_mise_versions_are_exact -v` red before changing config and green afterward; preserve both outputs and tested revisions. Also show the policy selector failing with pins but without its two held entries, then passing with them; temporary test data may reproduce this without discarding prepared edits. Then run each command separately:

- `make render-check`
- `make validate-agent-assets`
- `uv run python -m unittest tests.unit.test_generate_agent_configs -v`
- `uv run python -m unittest tests.unit.test_supply_chain_policy -v`
- `ruff check --config ruff.toml tests/unit/test_generate_agent_configs.py tests/unit/test_supply_chain_policy.py`
- `ruff format --config ruff.toml --check tests/unit/test_generate_agent_configs.py tests/unit/test_supply_chain_policy.py`
- `uv run python -I scripts/lint-comparisons.py --changed <changed paths>`; expand the complete measured diff path list as separate arguments.

Do not run Bats locally. Preserve synthetic legacy migration checks; report baseline failures and unrun commands honestly. No lint-baseline edits, suppressions or extra helper files are authorized.

Budget includes both new adjacent reason comments, exact-pin assertions, the installed-command refactor and the two held-map additions; no extra refactor is authorized.

The final diff has at most 16 changed lines outside `tests/` and `.orchestration/`, and at most 48 under `tests/`.

Measure `git diff --numstat <base40>...<head40>`.

The orchestrator pastes base40 at dispatch; head40 is the final RESULT head, both full 40-hex SHAs. For a records-only round after update-branch, base40 is the branch head at that dispatch. Count additions plus deletions, paste per-file numstat and both totals, and exclude only records from the source cap. An overrun blocks; the worker does not raise caps.

## Dispatch, evidence and completion

The orchestrator (Claude seat, sandboxed Bash) obtains and reads the accepted task-consistency checker/test revision before dispatch; check C1–C10, C7b and C11 and this task's regime-copy checks before dispatch and acceptance. Re-probe premises manually rather than executing unchecked premise strings. C-80 independent security-profile text review of the complete amended bytes precedes re-send and has at most 2 rounds total, including 0908b8f4’s round 1; amendment 1 resets no counter. Dispatch requires no surviving P0/P1; any need for a third round holds dispatch for re-plan.

Completion: continue tools/trusted-entrypoint-pins-a01 and its one PR (create only if absent); write task.md, report.md, validation.md, sandbox.md, learning.md, autoskill.md and worker review evidence under .orchestration/dotfiles-T133-trusted-entrypoint-pins-a01/. Only the primary task’s quoted Completion round, sandbox, CI/Bot and integration rules apply with this task’s own identifiers; no predecessor deletion is authorized. Advisory owner is dotfiles-T133-trusted-entrypoint-binding-followup-a01, created before disposition. Only the orchestrator integrates; no deployment is claimed.

Every evidence item names its producer and seat kind: `orchestrator (Claude seat, sandboxed Bash)` or `worker (Codex seat)`; review evidence also names its profile. validation.md contains verbatim stdout/stderr and real exit statuses for every executed command, including both modules’ red/green selectors, probes, lint and numstat. Record full base/head, branch, PR, changed paths, task-copy SHA-256, row-to-selector mapping, limits and `cost: n/a` unless observed.

Keep the complete current task copy byte-identical to the amended dispatch; the orchestrator compares bytes and SHA-256 rather than trusting a reported hash. Preserve predecessor evidence. Keep plan/todo/learn worklogs uncommitted, with at most one active todo per owner. Use [memory:decision] / [memory:failure] for durable facts under the existing memory procedure.

Complete agent-side review with resolved repo-local JSON and receipt under the allowed artifact directory and run the required review gate. Do not open or publish a browser review. Commit/push only task changes; wait for final-head green CI and the bounded automatic Bot window, recording `bot: none` on expiry. Do not post `@codex review`. The orchestrator dispositions findings and follows Playbook step 10 for integration.

Every command stays in the sandbox. On denial, send `AGMSG-PONG v1 task_id=dotfiles-T133-trusted-entrypoint-pins-a01 status=blocked` with the exact command, failure status/output and boundary; do not retry through another execution surface. Before RESULT write result.txt under the task artifact directory; send AGMSG-RESULT with status, final head, task_copy and all artifact paths, including precheck evidence required by the accepted regime.

## Checks (pasted by the orchestrator before each send)

