---
format: 2
task_id: dotfiles-T133-codex-worker-network-a01
kind: code
security: true
allowed_files:
  - home/dot_agents/agent-config.yaml
  - scripts/generate-agent-configs.py
  - tests/unit/test_generate_agent_configs.py
  - home/dot_codex/modify_private_standard.config.toml
  - home/dot_codex/modify_private_security.config.toml
  - .orchestration/dotfiles-T133-codex-worker-network-a01/**
after: [dotfiles-T133-worker-write-boundary-slice1-a01]
threat_table:
  - control: home/dot_agents/agent-config.yaml
    disposition: "residual: only the standard and security Codex profiles gain sandbox network access; the shared sandbox defaults, writable roots, approval policy and permission hooks remain unchanged."
  - control: scripts/generate-agent-configs.py
    disposition: "closed: tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_codex_worker_network_is_profile_scoped and tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_codex_worker_network_override_preserves_sandbox_table_settings"
  - control: tests/unit/test_generate_agent_configs.py
    disposition: "residual: render tests execute generated modify scripts in temporary homes and parse their TOML output without accessing credentials or performing network operations."
  - control: home/dot_codex/modify_private_standard.config.toml
    disposition: "closed: tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_codex_worker_network_is_profile_scoped and tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_codex_worker_network_override_preserves_sandbox_table_settings"
  - control: home/dot_codex/modify_private_security.config.toml
    disposition: "closed: tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_codex_worker_network_is_profile_scoped and tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_codex_worker_network_override_preserves_sandbox_table_settings"
  - control: .orchestration/dotfiles-T133-codex-worker-network-a01/**
    disposition: "residual: task artifacts contain the dispatched copy and evidence for this task alone; the final-head audit compares their claims with the diff and CI."
  - control: the task-file copy on the branch (.orchestration/dotfiles-T133-codex-worker-network-a01/task.md)
    disposition: "residual: the copy is byte-identical to the dispatched text; TASK and RESULT bind its own sha256 and the orchestrator compares it at acceptance."
  - control: the branch evidence records under .orchestration/dotfiles-T133-codex-worker-network-a01/ (report.md, validation.md, sandbox.md, learning.md and worker review evidence)
    disposition: "residual: records contain prose and command output; sandbox.md lists every refused command and the audit distinguishes rendered configuration from live enforcement."
  - control: task metadata
    disposition: "residual: the orchestrator checks C1 to C10 and C7b before dispatch and at acceptance; the task-copy byte comparison covers the complete dispatched front matter."
  - control: metadata separators
    disposition: "residual: the checker reads the first YAML front-matter document and the task-copy byte comparison covers every separator."
  - control: in-process effects
    disposition: "residual: rendering changes repository artifacts and temporary test outputs; the worker performs no deployment, authentication change, live policy edit or sandbox-escape probe."
  - control: workflow and interpreter or environment inputs
    disposition: "residual: workflow files, interpreter selection, launch arguments and shell environment policy remain unchanged; tests use the existing unittest and temporary-home conventions."
  - control: new or renamed scripts
    disposition: "residual: no script is added or renamed; the existing renderer and two generated profile modify scripts retain their existing responsibilities."
  - control: design section 5.14 item 1 (Codex worker write boundary)
    disposition: "residual: worker outbound traffic goes through the Codex sandbox with network access enabled; existing writable roots and filesystem restrictions remain unchanged, and this configuration does not establish isolation from same-UID host processes."
  - control: design section 5.14 item 10 (worker commands remain inside the sandbox, D-024-17a)
    disposition: "residual: gh and git push use network access inside the Codex sandbox; the worker never retries outside it, while the permgate Codex no-escape rule remains pending operator action and is not claimed as implemented; the dispatch prerequisite (Out of scope) is P1-15 installed and the seat re-seated, not merely merged, so the first execution already runs under the installed settings."
  - control: orchestrator effect merge
    disposition: "residual: the orchestrator merges only through gh pr merge --squash --match-head-commit <audited head> after the integration gate in Orchestrator Playbook step 10."
  - control: orchestrator effect update-branch
    disposition: "residual: gh pr update-branch moves the head, so CI, the feedback sweep, the task-level audit and the security review bind the new final head before the gate."
  - control: orchestrator effect forced worker removal
    disposition: "residual: no forced removal is planned; herdr-agents --remove-worker refuses a dirty worktree without --force, and any forced removal records discarded uncommitted state in acceptance."
premises: []
---

# AGMSG-TASK dotfiles-T133-codex-worker-network-a01 — plan 024 P1-15's Codex-side item split out for routing (D-024-17a)

## Goal

The Codex worker profiles `standard` and `security` set `sandbox_workspace_write.network_access = true` so `gh` and `git push` run inside the Codex sandbox through its network, as specified by `.orchestration/plans/024-design-quality.md` section 5.14 items 1 and 10 and decision D-024-17a. The shared base configuration and the `audit`, `review`, `express` and `deep` profiles retain their existing behavior. No other sandbox setting changes, and writable roots remain unchanged. This Codex-boundary change is assigned to a Claude seat using the `security` profile under the routing invariant.

## Files

1. `home/dot_agents/agent-config.yaml` declares `sandbox_workspace_write.network_access: true` under `model_profiles.standard.codex` and `model_profiles.security.codex`.

   The shared `codex.sandbox_workspace_write.network_access` remains `false`. The shared block currently supplies one sandbox configuration to all profiles, so the change uses worker-profile overrides. The manifest's writable roots, sandbox modes, approval policy, permission-request hook and Claude settings remain unchanged.

2. `scripts/generate-agent-configs.py` renders the declared worker-profile network overrides through `render_codex_profile`.

   The renderer currently emits the sandbox network setting only in the shared base configuration. A renderer change is therefore required and is included in `allowed_files`. The new profile table overrides only `network_access`. It introduces no writable-root override or launcher-specific setting.

3. `tests/unit/test_generate_agent_configs.py` adds `tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_codex_worker_network_is_profile_scoped`.

   The test uses the existing `unittest`, generated modify-script and temporary-home patterns. It checks the manifest's two worker-profile declarations and parses rendered profile TOML with `tomllib`. The rendered `standard` and `security` profiles carry `network_access = true`. The shared base retains `network_access = false`, and the rendered `audit`, `review`, `express` and `deep` profiles remain unchanged. The audit profile retains its `read-only` sandbox mode, and existing writable-root settings remain unchanged.

   The test is written before the manifest and renderer changes. Its assertions fail against the unchanged implementation and pass after the change. The existing audit-profile and runtime-state preservation tests remain green.

   A second test, `tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_codex_worker_network_override_preserves_sandbox_table_settings`, runs the generated `standard` and `security` modify scripts in a temporary home whose existing profile configuration already holds a `[sandbox_workspace_write]` table with `writable_roots`, `exclude_slash_tmp = true` and `exclude_tmpdir_env_var = true`. After the script runs, those keys keep their values and only `network_access` changes; the current merger replaces managed tables wholesale, so this fixture is what makes the generated-script rows closable. It is red before the implementation and green on the final head.

4. `home/dot_codex/modify_private_standard.config.toml` and `home/dot_codex/modify_private_security.config.toml` are regenerated through the existing generator.

   These two tracked paths are included in `allowed_files` as regeneration-only outputs. They receive no manual edits. Other generated outputs remain unchanged.

5. `.orchestration/dotfiles-T133-codex-worker-network-a01/` contains the byte-identical dispatched `task.md`, `report.md`, `validation.md`, `sandbox.md`, `learning.md` and worker review evidence. Worker review filenames carry the required `-worker-` infix.

   The report maps the requirements to test selectors and states the user-visible effect that Codex sessions selecting `standard` or `security` gain sandbox network access. It states that this boolean setting supplies no outbound domain allowlist.

   The report prepares the operator's exact deterministic rule that stops Codex PermissionRequest handling from approving sandbox escapes or unsandboxed retries. It identifies the insertion point before allow-pattern evaluation in `home/dot_local/bin/common/executable_permgate::decide`, the policy source `home/dot_agents/permgate-policy.yaml` and the existing `permgate codex` hook binding. It accounts for unsupported request shapes without allowing an escape. This is proposed operator text, and neither permgate source is changed by the worker.

## Out of scope

Permgate code, deterministic policy and permission-request hook changes belong to the operator. The worker performs no live policy edit or escape probe.

The Claude-side boundary of P1-15 belongs to `dotfiles-T133-worker-write-boundary-a01`. D-024-20 makes that task's merge and its recorded deployment the dispatch prerequisite, because a merge alone leaves a Claude worker on its old hook bindings and on the platform's automatic `gh` sandbox exclusion until the new settings are installed and the seat restarts. Before this task is dispatched: P1-15 is merged; `make update` has applied it on this host (the canonical clone's `git reflog` shows the pull and `chezmoi status` shows no pending change); the effective-settings check P1-15 specifies is recorded in its acceptance record; and the worker seat that takes this task is re-seated (`herdr-agents --remove-worker` then `--add-worker`) so its first execution runs under the installed settings. The orchestrator pastes that evidence into the Checks block of this text before the send. This task's branch is rebased onto `origin/main` after that merge and before implementation.

Any writable-root change is outside this task. Sandbox modes, approval policy, launch arguments, authentication, credential storage and deployment remain unchanged. The dropped wrapper design is not reintroduced.

## Measurements

The caps in Check are measured from their analogues on `origin/main` (C-79). Source: the existing per-profile `sandbox_mode` override is 2 renderer lines (`scripts/generate-agent-configs.py:598-600`) and 1 manifest line; the network override adds a `[sandbox_workspace_write]` table with one key in `render_codex_profile` (about 6 lines), 2 manifest lines and the matching lines in `render_codex_profile_modify` (line 1036; about 10), so about 20 lines, capped at 40. Tests: the analogous `test_audit_profile_renders_read_only_sandbox_override` is 37 lines (`tests/unit/test_generate_agent_configs.py:795-831`); two tests of that shape (about 74 lines) are capped at 100.

## Check

`make render-check`, `make validate-agent-assets`, `make format` and `uv run --no-project --with pyyaml python -m unittest tests.unit.test_generate_agent_configs -v` have their commands, verbatim output, exit statuses and tested heads pasted in `.orchestration/dotfiles-T133-codex-worker-network-a01/validation.md`. The render check, asset validation and unit module are green.

The new profile-scoping test carries red-before-implementation and green-final-head evidence. Render evidence identifies both changed worker profiles and all four unchanged orchestrator-side profiles. It records the unchanged base sandbox block and writable roots. These tests establish rendered configuration behavior and make no claim of live sandbox enforcement. No local Bats tests run.

An inherited formatting failure is reproduced on the unchanged base and recorded with its output. It remains a reported failure and receives no repair outside `allowed_files`.

`git diff --numstat origin/main...HEAD` shows at most 40 changed lines outside `tests/` and `.orchestration/`, excluding the regenerated `home/dot_codex/modify_private_standard.config.toml` and `home/dot_codex/modify_private_security.config.toml`, and at most 100 changed lines under `tests/`. Changed lines are additions plus deletions. Validation includes per-file numstat, both totals and the complete changed-file inventory.

The orchestrator runs the format-2 task-consistency checker, including C1 to C10 and C7b, before dispatch and at acceptance. The task text and threat table pass the security-profile C-80 review before dispatch, and its findings enter the task's finding-class table. The task copy remains byte-identical to the dispatched file.

## Completion

The Completion clause of `.orchestration/tasks/dotfiles-T133-hold-playbook-a01.md` applies with `dotfiles-T133-codex-worker-network-followup-a01` as the owner of any advisory P2 and `task_copy=<sha256 of .orchestration/dotfiles-T133-codex-worker-network-a01/task.md>` in the RESULT. This task's scope, Check, `security: true`, prerequisite, Claude-seat routing and evidence paths govern that reference.

One PR starts from a fresh branch off `origin/main`. The orchestrator writes the advisory owner task before recording its first ownership disposition. A small in-scope P2 follows the inherited `check=` revise procedure while INV-6 permits it.

The worker's own pre-push review is one round at most. Every worker-side fix round counts toward INV-6. A surviving P0/P1 is sent in the RESULT as `open:<finding-or-thread-id>` and stops integration for the operator's decision. The worker starts no additional private correction-and-review cycle. The third finding of one class stops further rounds until the orchestrator's re-plan.

The RESULT identifies the final head, base, branch, changed files, test selectors, measured caps, evidence paths, task-copy hash, pending operator step and every Bot finding's proposed disposition. It carries the precheck evidence required by the applicable RESULT procedure.

The orchestrator runs the task-level audit and the security review on the final head and dispositions every finding before the gate. Final-head CI, the feedback sweep, audit, security review, acceptance record, gate and merge follow Orchestrator Playbook step 10 and the repository's security-review requirements. A changed head receives fresh evidence.

No `@codex review` comment is issued. Every `gh` write and Git write runs as an individual command without shell chaining or a wrapper combining writes. Every worker command remains inside its sandbox. An operation that cannot complete there produces a blocked PONG naming the exact command and refusal, with no retry outside the sandbox.

## Checks (pasted by the orchestrator before each send)

```
(pasted at dispatch)
```

Implementation and runtime verification remain pending worker execution.
Unrestricted outbound sandbox network access and the pending operator permgate rule remain residuals.