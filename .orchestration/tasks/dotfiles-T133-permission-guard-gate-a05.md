---
format: 2
task_id: dotfiles-T133-permission-guard-gate-a05
kind: code
security: true
allowed_files:
  - scripts/permission-guard.py
  - scripts/orchestrator/ruleset-request.sh
  - scripts/orchestrator/ruleset-verify.sh
  - home/dot_claude/hooks/executable_gh-merge-gate.sh
  - home/dot_agents/agent-config.yaml
  - home/.chezmoitemplates/claude-settings-managed.json
  - scripts/generate-agent-configs.py
  - scripts/validate-agent-assets.py
  - scripts/check-agent-runtime.py
  - home/dot_config/git/config.tmpl
  - tests/unit/test_gh_merge_gate.py
  - tests/unit/test_permission_guard.py
  - tests/unit/test_ruleset_scripts.py
  - tests/unit/test_generate_agent_configs.py
  - tests/unit/test_validate_agent_assets.py
  - tests/unit/test_check_agent_runtime.py
  - .orchestration/dotfiles-T133-permission-guard-gate-a05/**
  - scripts/orchestrator/integrate-merge.sh
  - scripts/orchestrator/finish-pr.sh
  - scripts/orchestrator/orch-gate.sh
  - tests/unit/test_orch_gate_path.py
  - tests/unit/test_integrate_merge.py
  - tests/unit/test_claude_settings_merge.py
after: [dotfiles-T133-worker-write-boundary-a01]
reset_of: [dotfiles-T133-permission-guard-gate-a04]
threat_table:
  - control: "scripts/permission-guard.py (canonical permission-surface comparison and exact diff SHA256 approval only from git show origin/main:.orchestration/decisions.tsv after fetch in the verified anchored checkout, under D-024-19; working-copy rows and candidate revisions supply no approval authority)"
    disposition: "closed: tests/unit/test_permission_guard.py::PermissionGuardTest::test_guard_reads_the_committed_ledger_never_the_working_copy_or_the_pr_tree"
  - control: "scripts/orchestrator/ruleset-request.sh (expected ruleset 24397953, duplicate-preserving live comparison, unchanged CLI and GET-only access)"
    disposition: "closed: tests/unit/test_ruleset_scripts.py::RulesetScriptsTest::test_ruleset_comparison_preserves_duplicate_rule_types"
  - control: "scripts/orchestrator/ruleset-verify.sh (comparison result and optional updates of an explicitly selected existing progress ledger only on equality)"
    disposition: "closed: tests/unit/test_ruleset_scripts.py::RulesetScriptsTest::test_progress_is_optional_and_missing_file_is_print_only"
  - control: "home/dot_claude/hooks/executable_gh-merge-gate.sh (only the tracked anchored entrypoint can receive allow; direct gh merge, create and update-branch text always asks)"
    disposition: "closed: tests/unit/test_gh_merge_gate.py::GhMergeGateTest::test_gate_asks_for_every_gh_text_form"
  - control: "home/dot_agents/agent-config.yaml (the deployed checkout anchor, synchronous hook source and removal of exactly the three ask rules approved by D-024-14)"
    disposition: "closed: tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_manifest_gates_merge_update_branch_and_create_through_the_hook_and_keeps_every_other_gh_write_on_ask"
  - control: "home/.chezmoitemplates/claude-settings-managed.json (the generated synchronous Bash PreToolUse hook and retained permission rules)"
    disposition: "residual: the existing generator renders this file from the manifest, and make render-check rejects any byte drift."
  - control: "scripts/generate-agent-configs.py (one synchronous Bash PreToolUse command entry rendered from gh_merge_gate_hook)"
    disposition: "closed: tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_manifest_gates_merge_update_branch_and_create_through_the_hook_and_keeps_every_other_gh_write_on_ask"
  - control: "scripts/validate-agent-assets.py (every retained gh write ask rule and the exact synchronous deployed hook entry)"
    disposition: "closed: tests/unit/test_validate_agent_assets.py::ValidateAgentAssetsTest::test_gate_validator_requires_every_retained_ask_rule_and_the_exact_synchronous_hook_entry"
  - control: "scripts/check-agent-runtime.py (the deployed hook's content and executable status)"
    disposition: "closed: tests/unit/test_check_agent_runtime.py::CheckAgentRuntimeTest::test_runtime_check_compares_the_deployed_gh_merge_gate_hook_with_the_source"
  - control: "home/dot_config/git/config.tmpl (removal of the GitHub HTTPS-to-SSH pushinsteadof block)"
    disposition: "residual: the removed block contains no credential, the existing gh credential helper remains, and the operator verifies deployment after make update."
  - control: "tests/unit/test_gh_merge_gate.py (entrypoint identity, exact argv, sanitized checks, trusted tools, gh-text asks, JSON decisions and no-decision cases)"
    disposition: "residual: temporary repositories and synthetic deployed manifests exercise decisions without executing submitted payload text or changing GitHub."
  - control: "tests/unit/test_permission_guard.py (revision fixtures, permission digests, committed origin/main ledgers in temporary anchored checkouts named by deployed manifest fixtures, and forged working-copy and PR-tree rows)"
    disposition: "residual: fixture approvals are committed at origin/main in temporary anchored repositories; uncommitted and PR-tree rows exercise refusal, no external ledger override is used, and the live decision ledger and credentials remain untouched."
  - control: "tests/unit/test_ruleset_scripts.py (GET-only argv capture, duplicate occurrences and optional temporary progress ledgers)"
    disposition: "residual: fake GitHub responses and temporary ledgers preserve the live ruleset and progress records while the audit checks the assertions."
  - control: "tests/unit/test_generate_agent_configs.py (the manifest anchor, rendered synchronous hook and complete retained ask set)"
    disposition: "residual: fixture renders cover supported darwin and linux configurations, and the final-head audit checks the assertions."
  - control: "tests/unit/test_validate_agent_assets.py (independent removal of retained rules and substitution of fake, duplicate or async hook entries)"
    disposition: "residual: fixture settings exercise validation failures without changing deployed settings."
  - control: "tests/unit/test_check_agent_runtime.py (missing, matching, stale and non-executable deployed-hook fixtures)"
    disposition: "residual: a temporary HOME supplies all deployment fixtures, leaving the live runtime untouched."
  - control: ".orchestration/dotfiles-T133-permission-guard-gate-a05/** (this reset's branch artifacts)"
    disposition: "residual: new evidence stays in this directory, separates inherited observations from final-head results and is checked against the diff and CI."
  - control: "scripts/orchestrator/integrate-merge.sh (trusted execution of the gate, final-head security guard, committed-ledger approval, PR checks, pinned squash merge and anchored fast-forward; worker-root trusted paths refuse, and premise 6 retains its Claude-seat residual)"
    disposition: "closed: tests/unit/test_integrate_merge.py::IntegrateMergeTest::test_integrate_merge_binds_gh_and_git_to_the_trusted_root"
  - control: "scripts/orchestrator/finish-pr.sh (tracked finishing glue and publication of validated PR-body bytes through a write-once anchored snapshot rehashed immediately before gh; premise 6 retains its Claude-seat residual)"
    disposition: "closed: tests/unit/test_integrate_merge.py::IntegrateMergeTest::test_finish_pr_passes_a_body_snapshot_never_the_caller_path"
  - control: "tests/unit/test_integrate_merge.py (trusted execution, head mismatch, gate and security refusals, safe fast-forward, publication controls and source- and snapshot-swap fixtures)"
    disposition: "residual: fake binaries capture writes and synthetic files exercise swaps, metadata aliases and evidence failures without merging or publishing anything."
  - control: "scripts/orchestrator/orch-gate.sh (first-action env -i, trusted absolute binaries, explicit Git -C and fixed Git configuration before discovery and across the lines 87-89 environment rebuild; the gate and validator inherit the reconstructed controls)"
    disposition: "closed: tests/unit/test_orch_gate_path.py::OrchGatePathTest::test_orch_gate_sanitizes_the_environment_before_git_discovery"
  - control: "tests/unit/test_orch_gate_path.py (planted environment and Git configuration, discovery ordering, private PATH and validator inheritance through the rebuilt environment)"
    disposition: "residual: temporary repositories and fake binaries capture discovery and descendant environments without changing the live checkout or GitHub."
  - control: "tests/unit/test_claude_settings_merge.py (darwin and linux Bash sandbox renders, seat worktree and scratch/cache allowances, and Bash write denial for trusted paths)"
    disposition: "residual: fixture renders assert only the Bash sandbox policy; Claude file tools, hooks and MCP processes remain outside that sandbox, and the rendered permission policy has no path deny until P1-15 under D-024-17."
  - control: "the task-file copy on the branch (.orchestration/dotfiles-T133-permission-guard-gate-a05/task.md) replaces the reset_of task's copy (.orchestration/dotfiles-T133-permission-guard-gate-a04/task.md)"
    disposition: "residual: the first push deletes the a04 copy and adds the byte-identical dispatched a05 copy; TASK and RESULT carry the a05 copy's SHA256, which the orchestrator verifies at acceptance."
  - control: "the branch evidence records under .orchestration/dotfiles-T133-permission-guard-gate-a05/ (report.md, validation.md, sandbox.md, learning.md and dry-probe transcripts)"
    disposition: "residual: records retain tested identities and verbatim outputs, distinguish historical evidence from new closure and list refused commands for the audit."
  - control: task metadata
    disposition: "residual: the orchestrator checks C1 to C10 and C7b before dispatch and at acceptance, and whole-file byte comparison protects the dispatched metadata."
  - control: metadata separators
    disposition: "residual: the first document separators bound structured metadata, and whole-file byte comparison protects the complete task copy."
  - control: in-process effects
    disposition: "residual: the hook executes no payload text; tests use temporary state; ruleset helpers use GET access and write only an explicitly selected existing temporary progress ledger on equality."
  - control: workflow and interpreter or environment inputs
    disposition: "residual: the retained env bash shebang and Bash startup precede first-action env -i, so initial launch depends on the orchestrator environment. Codex tool writes are sandbox-confined; Claude file tools, hooks and MCP processes lack that boundary until P1-15, and same-UID processes outside every seat sandbox remain residual. Trusted execution then constructs env -i inputs and a private PATH, excludes caller Git and tool-manager overrides, isolates Python and uses only the private offline uv cache."
  - control: new or renamed scripts
    disposition: "residual: the new deployable inventory is the hook, permission guard, two ruleset helpers and two tracked orchestration entrypoints; RESULT lists all six, and no untracked glue becomes an execution dependency."
  - control: "the sanitized environment (section 5.14 item 2)"
    disposition: "closed: tests/unit/test_gh_merge_gate.py::GhMergeGateTest::test_gate_runs_its_identity_checks_under_a_sanitized_environment"
  - control: the interpreter sanitization order
    disposition: "closed: tests/unit/test_gh_merge_gate.py::GhMergeGateTest::test_gate_sanitizes_before_any_other_command"
  - control: "the identity check of the entrypoint (section 5.14 item 4; updatedInput names the verified anchored realpath and preserves the three arguments, subject to premise 6's runtime-specific residuals)"
    disposition: "closed: tests/unit/test_gh_merge_gate.py::GhMergeGateTest::test_gate_allows_only_through_updated_input_naming_the_verified_realpath"
  - control: "the manifest-rendered worker filesystem write boundary (section 5.14 item 1)"
    disposition: "residual: tests/unit/test_claude_settings_merge.py::test_rendered_worker_sandbox_denies_the_trusted_root_for_bash asserts only Bash sandbox denial; Codex confines all tool writes, while Claude file tools, hooks and MCP processes remain outside Seatbelt with no rendered path deny until P1-15 under D-024-17."
  - control: "the trusted-path write-boundary check (section 5.14 item 3; the hook and entrypoint ask when trusted paths lie under .claude/worktrees/ or a manifest-listed worker worktree)"
    disposition: "closed: tests/unit/test_gh_merge_gate.py::GhMergeGateTest::test_gate_refuses_trusted_paths_under_a_worker_writable_root"
  - control: "the approval provenance boundary (section 5.14 item 8)"
    disposition: "closed: tests/unit/test_permission_guard.py::PermissionGuardTest::test_guard_reads_the_committed_ledger_never_the_working_copy_or_the_pr_tree"
  - control: "the executable provenance boundary"
    disposition: "residual: identity checks, verified realpaths and trusted-path refusal bind checked execution; Codex tool writes are confined, while Claude file tools, hooks and MCP processes retain the P1-15 path-deny gap and a same-UID process outside every seat sandbox remains residual."
  - control: "the Git configuration inputs"
    disposition: "closed: tests/unit/test_gh_merge_gate.py::GhMergeGateTest::test_gate_git_ignores_planted_hooks_fsmonitor_and_global_config"
  - control: "the snapshot rule (the entrypoint creates the snapshot directory under the anchored checkout's gitignored .agents/worklog/snapshots/ at mode 0700, writes the snapshot once and compares its SHA256 again immediately before gh)"
    disposition: "closed: tests/unit/test_integrate_merge.py::IntegrateMergeTest::test_finish_pr_reverifies_the_snapshot_before_gh"
  - control: the snapshot write boundary
    disposition: "residual: the last SHA256 comparison refuses a detected change and Codex confines tool writes; mode 0700 does not exclude the same UID, Claude file tools, hooks and MCP processes retain the P1-15 path-deny gap, and a same-UID process outside every seat sandbox can race the final comparison and gh's read."
  - control: "the worker sandbox exclusions (section 5.14 item 10)"
    disposition: "residual: Worker Playbook step 4 sends gh outside the sandbox through the permission gate with no present mitigation for this exclusion; P1-15 owns the pending D-024-17 wrapper using env -i, an absolute trusted gh and a fixed alias-free read-only GH_CONFIG_DIR."
  - control: "the output and reservation identity (section 5.14 item 5)"
    disposition: "residual: new snapshot names carry the full 40-hex head, the content digest and a unique suffix; legacy gate evidence retains its existing filename contract and binds the full head in its contents, and this task introduces no reservation or slot lock."
  - control: "the honest residuals (section 5.14 item 6)"
    disposition: "residual: the report preserves the Claude-seat path-deny gap owned by P1-15, the unmitigated outside-sandbox gh exclusion and the same-UID process risk, and labels none closed."
  - control: "the shared trusted-execution regressions (section 5.14 item 7)"
    disposition: "residual: the required red-then-green fixtures cover caller shims, planted Git inputs, worker-root trusted paths and a source swap after validation; the report records their exact selectors and outputs, and P1-6 owns the future shared helper."
  - control: "the private offline uv cache (section 5.14 item 9)"
    disposition: "closed: tests/unit/test_integrate_merge.py::IntegrateMergeTest::test_integrate_merge_uses_the_private_uv_cache_only"
  - control: orchestrator effect merge
    disposition: "residual: only the trusted entrypoint performs the squash merge, after final-head evidence and API checks, with --match-head-commit binding the merged head; no task branch is merged locally or pushed to main."
  - control: "orchestrator effect PR creation and publication (finish-pr.sh publishes only a snapshot it wrote from validated bytes and reverified, retains the draft flag and applies the records-only check)"
    disposition: "closed: tests/unit/test_integrate_merge.py::IntegrateMergeTest::test_finish_pr_preserves_draft_and_records_only_publication_controls"
  - control: "orchestrator effect fetch, checkout and fast-forward (fetch of origin/main only, fast-forward only, refusal of modified tracked files outside .orchestration and preservation of untracked records)"
    disposition: "closed: tests/unit/test_integrate_merge.py::IntegrateMergeTest::test_integrate_merge_fetches_only_origin_main_and_preserves_local_records"
  - control: orchestrator effect update-branch
    disposition: "residual: direct gh update-branch text asks, and any resulting head receives fresh CI, feedback, audit and security evidence before the integration gate."
  - control: orchestrator effect forced worker removal
    disposition: "residual: no forced removal is planned; the existing dirty-worktree rule applies and the acceptance record identifies any discarded uncommitted state."
premises:
  - claim: none of the five new files exists on origin/main
    command: git ls-files scripts/permission-guard.py scripts/orchestrator/ruleset-request.sh scripts/orchestrator/ruleset-verify.sh home/dot_claude/hooks/executable_gh-merge-gate.sh tests/unit/test_gh_merge_gate.py | wc -l
    output: |-
      0
  - claim: PR #400's branch, the material this task rebuilds from, is at the head the T131 review assessed
    command: git rev-parse origin/fix/claude-pinned-merge-gate
    output: |-
      0b874adb9850ff9647fbc039ec3cf6cc30487488
  - claim: the tracked git config still rewrites GitHub pushes to SSH while the live config (hand-edited) does not, the mismatch D3 (d) resolves
    command: /usr/bin/grep -c 'pushinsteadof = https://github.com/' home/dot_config/git/config.tmpl
    output: |-
      1
  - claim: the manifest still asks for gh pr merge, the rule the hook replaces
    command: /usr/bin/grep -c 'Bash(gh pr merge:\*)' home/dot_agents/agent-config.yaml
    output: |-
      1
  - claim: decisions.tsv carries no permission-scoped decision row yet, so the guard's first run on this PR itself must find the row this task adds
    command: /usr/bin/grep -c 'scope=permission' .orchestration/decisions.tsv
    output: |-
      0
  - claim: >-
      section 5.14 item 1 applies per runtime: a Codex seat's sandbox confines all tool writes to its worktree and enumerated writable paths; a Claude seat's Seatbelt sandbox confines Bash only, while Write/Edit/MultiEdit/NotebookEdit, hooks and MCP processes run outside it and the rendered permission policy has no path deny today. The Claude-seat boundary is residual until P1-15 under D-024-17 adds the permgate path deny. The Bash render test asserts only that sandbox's scope. Approval provenance instead uses the committed origin/main ledger after fetch under D-024-19. Worker Playbook step 4's outside-sandbox gh has no present mitigation and is owned by P1-15, whose pending wrapper uses env -i, an absolute gh and a fixed alias-free read-only GH_CONFIG_DIR. A same-UID process outside every seat sandbox remains residual.
    sources:
      - home/dot_agents/agent-config.yaml
      - home/.chezmoitemplates/claude-settings-managed.json
    verification: tests/unit/test_claude_settings_merge.py::test_rendered_worker_sandbox_denies_the_trusted_root_for_bash
---

# AGMSG-TASK dotfiles-T133-permission-guard-gate-a05 — S1 reset of a04 under D-024-16 (plan 006 S1; plan 024 P1-14 and D3 (d); PR #420)

This text replaces the stopped a04 task under decision D-024-16. The a04 artifact stopped at `2026-10-19T02:20Z` after six findings of the class `decision-not-bound-to-execution` across a03 and a04. The design tier now permits only a trusted tracked entrypoint. The hook never allows a gh text form.

PR #420 continues on `tools/permission-guard-gate-a01` from `911f5202e61a2e46f527fcd9a4eda0041e97410a`. Seat a010, worker-e, keeps its branch, prepared fixes and evidence. One PR carries this task. This reset creates no fresh implementation branch or second implementation PR.

The worker's first push deletes `.orchestration/dotfiles-T133-permission-guard-gate-a04/task.md` and adds the byte-identical dispatched text at `.orchestration/dotfiles-T133-permission-guard-gate-a05/task.md`. That predecessor-copy deletion is the specified reset bookkeeping exception to the edit boundary. The orchestrator owns canonical reset records. Predecessor canonical task texts, evidence and acceptance histories remain unchanged.

The a04 acceptance record preserves the S1 class table, re-plan line and D-024-16. Its six instances are the following.

| Source | Finding | Class |
| --- | --- | --- |
| a03 security review, `31d6c322` | Hook binaries resolve through mise shims. | `decision-not-bound-to-execution` |
| a03 security review, `31d6c322` | `.GIT` case variants bypass Git-metadata exclusion. | `decision-not-bound-to-execution` |
| a03 security review, `31d6c322` | The PR tree supplies its own decision ledger. | `decision-not-bound-to-execution` |
| a04 security review, `911f5202` | The allowed bare gh resolves through the caller's PATH. | `decision-not-bound-to-execution` |
| a04 security review, `911f5202` | The body pathname can be swapped after validation. | `decision-not-bound-to-execution` |
| a04 local review, `911f5202` | Caller GIT_* variables redirect checkout identity checks. | `decision-not-bound-to-execution` |

The `.GIT` finding is the sibling identified in the acceptance record's class accounting. S1 had already been reached by the a04 security review. The attempted instance-by-instance revise after that threshold remains recorded as an orchestration error. This reset does not turn predecessor findings or historical green tests into approvals.

The first five premises preserve a04's write-time observations verbatim. They remain historical observations, including the ledger observation that predates D-024-14. Premise 6 states section 5.14 item 1's runtime-specific boundary and its Claude-seat residual. Its renamed render regression asserts Bash denial only. New reports and evidence use the a05 directory and identify their tested revisions.

The design sources are `.orchestration/plans/024-design-programs.md` item (14), `.orchestration/plans/024-design-quality.md` sections 5.13 and 5.14, D-024-03 (d), D-024-14, D-024-16, D-024-17, D-024-18 and D-024-19. Section 5.14 applies by reference under D-024-18, with a threat row for each item. The a04 acceptance record and the three named a03/a04 review records supply the reset findings. D-024-16 replaces their text-form allowance design. The second C-80 pre-dispatch security review at `.orchestration/validation/dotfiles-T133-permission-guard-gate-a05-text-security.md.last.md` returned `Verdict: incorrect` with four P1 and one P2. The orchestrator amended section 5.14 items 1, 2, 8, 9 and 10 and recorded D-024-18 and D-024-19. This text incorporates those decisions and retains the stated residuals.

The orchestrator sequences `dotfiles-T133-dispositions-a02` after this task because both edit `scripts/orchestrator/orch-gate.sh`.

The deadline `2026-10-19T03:00Z`, which is 12:00 JST, is missed. The new estimate belongs to the orchestrator. The a04 acceptance record reports 14:00–14:30 JST as that estimate, without turning it into a new worker deadline. An open security P1 stops integration regardless of the estimate.

## Goal

The PreToolUse hook decides on the executable identity of one tracked anchored entrypoint and returns its verified realpath through `hookSpecificOutput.updatedInput`, subject to premise 6's runtime-specific residuals. That entrypoint binds the tools, environment, evidence and head used by execution. Every gh merge, create or update-branch text form asks with the reason `the merge runs through integrate-merge.sh`. The permission guard accepts exact-digest approval only from the committed `origin/main` ledger after fetch. The ruleset scripts retain duplicate-preserving display and verification without changing the live ruleset.

## Files

0. The inherited dry-probe baseline remains preserved at `.claude/worktrees/worker-e/.orchestration/dotfiles-T133-permission-guard-gate-a01/validation.md`. Its 54 entries, the a02 independent review and corpus, the a03 Bot fixes and fixture repairs, and the a04 regressions retain their original tested identities and limitations.

   The a03 Ubuntu directory-order repair and macOS resolved-temporary-root repair remain one historical CI-repair round under C-61. The initial omission of the macOS CI failure remains disclosed. Historical formatting, gate, CI and review failures remain failures.

   The a05 validation record references those transcripts and adds a closure table with input, expected a05 result, actual result, exit status and source identity. Former gh-text allow expectations become ask under D-024-16 and are identified explicitly. Retained regressions keep their original red evidence and receive final-head green runs. The new identity contract has red-then-green evidence under `tests/unit/test_gh_merge_gate.py::GhMergeGateTest::test_gate_allows_only_the_tracked_entrypoint_of_the_anchored_checkout`.

1. `scripts/permission-guard.py --base <ref> --head <ref> [--manifest home/dot_agents/agent-config.yaml]` retains its Python CLI apart from removal of `--decisions`, isolated interpreter execution and committed-ledger approval under item 11. PyYAML runs through `UV_CACHE_DIR=<anchored checkout>/.agents/worklog/uv-cache uv run --offline --with pyyaml`; the implementation otherwise uses the standard library. Item 9 fixes the cache for every orchestrator-side uv run.

   It reads both revisions of the manifest and rendered `home/.chezmoitemplates/claude-settings-managed.json` and `home/.chezmoitemplates/codex-config-managed.toml` as data. Its permission surface includes Claude permissions, sandbox settings, permission-deciding PreToolUse hooks, `orchestrator_checkout`, Codex approval and sandbox settings, and the corresponding rendered permission, sandbox and hook surface. Both supported platform renders remain covered.

   Sorted keys and compact JSON produce canonical surfaces. Equal surfaces print `permission surface: unchanged` and exit 0. A changed surface prints the unified canonical diff and its SHA256. A trusted `D-…` row carries `scope=permission`, `approved_by=user` and the exact `diff_sha256=<digest>` in its `basis` or `what` column. A matching row prints its id and exits 0. A missing approval prints one violation per changed key path and exits 1. Revisions and record contents are never executed.

   `tests/unit/test_permission_guard.py::PermissionGuardTest::test_permission_diff_without_an_approved_decision_row_fails_and_with_it_passes` retains its red-then-green evidence, with approval committed to the fixture's origin/main. Unchanged surfaces, non-permission changes, rendered-only changes, sandbox and anchor changes, malformed data and bad revisions remain covered. Item 11 replaces the anchored-working-copy ledger regression with the committed-ledger regression.

2. `scripts/orchestrator/ruleset-request.sh [--expected <json>]` retains its CLI, output, exit behavior and GET-only access. It prints the expected JSON for `main integration gate`, ruleset id `24397953`, with the seven contexts named by `tests/unit/test_workflow_orchestration_skip.py`, `strict_required_status_checks_policy: false`, no `pull_request` rule, and retained `deletion` and `non_fast_forward` rules. It reads the live ruleset with `gh api repos/{owner}/{repo}/rulesets/24397953` and prints the canonical comparison.

   `scripts/orchestrator/ruleset-verify.sh [--expected <json>] [--progress <tsv>]` uses the same comparison. Equality exits 0. An explicitly selected existing progress ledger receives `verified` and the current UTC timestamp in rows `D1` and `D2`, using asserted row anchors and preserving unrelated bytes. An omitted progress flag or absent named file produces print-only behavior and creates no ledger. A difference prints each differing occurrence and key, exits 1 and writes nothing.

   `tests/unit/test_ruleset_scripts.py::RulesetScriptsTest::test_ruleset_request_prints_the_diff_and_never_writes`, `tests/unit/test_ruleset_scripts.py::RulesetScriptsTest::test_ruleset_verify_reports_each_difference_and_writes_progress_only_on_match` and `tests/unit/test_ruleset_scripts.py::RulesetScriptsTest::test_progress_is_optional_and_missing_file_is_print_only` retain red-then-green evidence. Tests use temporary progress records. The live ruleset and `.orchestration/plans/024-progress.tsv` remain untouched.

3. `home/dot_claude/hooks/executable_gh-merge-gate.sh` implements the D-024-16 identity gate with English shdoc comments. Its outcomes are allow, ask and no decision. Every outcome exits 0. Allow and ask emit valid PreToolUse decision JSON. No decision emits empty stdout. Recognition never executes, evaluates or sources submitted command text.

   The orchestrator seat's own Claude Code process launches the interpreter from the orchestrator's environment. The hook keeps `#!/usr/bin/env bash`. Its first executed command enters `env -i` with fixed bootstrap inputs, before any other command, payload parsing, logging, identity check or tool resolution. The shebang's interpreter lookup and Bash startup occur before that first action and remain dependent on the orchestrator's environment. Premise 6 confines Codex tool writes but leaves Claude file tools, hooks and MCP processes residual until P1-15; a same-UID process outside every seat sandbox also remains residual.

   Inside that clean environment, the hook establishes the trusted root from deployed `~/.agents/agent-config.yaml` using shell builtins and fixed bootstrap utilities. It resolves `python3`, `jq`, `gh` and `git` in that root and constructs a private directory of links to the absolute binaries. The hook uses no uv and no PyYAML; its parsing uses jq and Python's standard library. Item 9 governs resolution and environment construction.

   `tests/unit/test_gh_merge_gate.py::GhMergeGateTest::test_gate_sanitizes_before_any_other_command` asserts the retained shebang and that entry into `env -i` precedes every other command. It records red-then-green evidence without claiming that in-script sanitization precedes interpreter startup.

   The manifest's `orchestrator_checkout` is expanded and resolved with realpath. It identifies a primary checkout whose Git common directory resolves to its own `.git` and whose origin identifies `mryfmo/dotfiles`. The deployed manifest supplies the anchor independently of payload cwd and candidate revisions. Its protection follows premise 6's runtime-specific scope, including the Claude-seat residual. Git identity operations use the captured absolute git with explicit `-C <anchored checkout>` under the sanitized environment and item 9's fixed configuration controls. Permission approval comes only from the committed ledger under item 11.

   The hook and the entrypoint refuse with ask when any path they trust lies under `.claude/worktrees/` or under a worker worktree listed by the deployed manifest, including `worker_worktree`. The checks cover the anchored checkout's `scripts/orchestrator`, the Git object store supplying the committed ledger, evidence, the snapshot directory, the private uv cache and every resolved binary. Path resolution and containment use filesystem identity and reject a trusted path reached through a worker-writable component. Checkout identity alone supplies no approval provenance.

   `tests/unit/test_gh_merge_gate.py::GhMergeGateTest::test_gate_refuses_trusted_paths_under_a_worker_writable_root` exercises both the hook and entrypoint with each trusted path placed under `.claude/worktrees/` and under a manifest-listed worker root, including aliases. Each case asks and performs no merge or publication.

   The only allow candidate is one shlex argv containing an executable pathname followed by exactly three arguments: `<task> <head40> <pr>`. The task matches `^[A-Za-z0-9][A-Za-z0-9._-]*$`, the head is a full 40-hex commit id, and the PR is decimal. The executable pathname resolves directly to `<anchored checkout>/scripts/orchestrator/integrate-merge.sh`. The hook performs no PATH search for that submitted pathname. There are no extra flags, assignments, wrappers or trailing commands.

   Raw allow candidates contain none of `;`, `&`, `|`, `<`, `>`, `(`, `)`, backtick, `$`, backslash, newline, `*`, `?`, `[`, `]`, `{`, `}`, `#` or `~`. Space and tab are the permitted separators. Other ASCII control characters are excluded. POSIX shlex performs splitting without expansion or execution.

   The hook fetches `origin/main` using the absolute git and item 9's fixed configuration controls. The anchored checkout's `git rev-parse HEAD` equals the fetched `git rev-parse origin/main`. `git status --porcelain -- scripts/orchestrator/` is empty. The SHA256 of the file selected by `argv[0]` equals the SHA256 of `git show HEAD:scripts/orchestrator/integrate-merge.sh`. Missing tracking, dirty orchestration scripts, a stale HEAD, a different executable identity or a wrong argument shape asks.

   An allow response contains `hookSpecificOutput.updatedInput` with the Bash command rebuilt from the checked argv. `argv[0]` is replaced by the verified realpath inside the anchored checkout, and the three argument values remain unchanged. The returned command is encoded without shell expansion. The hook asks whenever it cannot produce that updated input. It never emits allow for the original unchecked spelling alone. Codex tool writes cannot replace the verified realpath through execution; Claude file tools, hooks and MCP processes retain the P1-15 path-deny gap, and a same-UID process outside every seat sandbox remains residual.

   `tests/unit/test_gh_merge_gate.py::GhMergeGateTest::test_gate_allows_only_through_updated_input_naming_the_verified_realpath` asserts the complete allow JSON, the verified realpath and the unchanged three arguments. It covers a submitted alias, replacement of that alias after validation and failure to construct updated input. The allow response executes through the verified realpath, and missing updated input asks.

   Every visible gh `pr merge`, `pr create` and `pr update-branch` text form asks, including path-prefixed executables, quoted spellings, draft creation, records-only operations and formerly eligible pinned merges. Its reason is `the merge runs through integrate-merge.sh`. Entrypoint-looking commands that fail the identity or argv contract ask. Every other command receives no decision. The remaining gh-text detection supplies ask only and interprets no operation options.

   Missing trusted tools, malformed payloads and failed candidate checks ask. Missing jq uses static valid ask JSON. Decision encoding uses the captured absolute jq and logging uses only constructed trusted paths and tools.

   `tests/unit/test_gh_merge_gate.py::GhMergeGateTest::test_gate_allows_only_the_tracked_entrypoint_of_the_anchored_checkout` is red before the redesign and green afterward. Its positive case is the tracked matching entrypoint at the anchored primary checkout's fetched main. A modified file, an untracked copy with identical bytes, a HEAD behind origin/main, dirty orchestration scripts and each wrong argv shape ask. A failed fetch or hash comparison never allows.

   `tests/unit/test_gh_merge_gate.py::GhMergeGateTest::test_gate_asks_for_every_gh_text_form` is red against the a04 behavior and green afterward. It covers the three operations, bare and path-prefixed executables, quoted spellings, retained wrapper and heredoc examples, and every former positive operation class. Unrelated commands retain empty output.

4. `home/dot_agents/agent-config.yaml` retains `orchestrator_checkout: ~/Workspace/dotfiles` beside `worker_worktree` and `gh_merge_gate_hook: ~/.claude/hooks/gh-merge-gate.sh` under `claude.hooks`. Its English comments describe trusted-entrypoint allowance.

   The permission change remains exactly D-024-14's removal of `Bash(gh pr merge:*)`, `Bash(gh pr create:*)` and `Bash(gh pr update-branch:*)`, together with the synchronous PreToolUse hook. Every other gh write ask rule remains. There is no new general gh allow rule. Direct forms of the three removed rules now ask through the hook.

   `scripts/generate-agent-configs.py` renders exactly one synchronous command hook matching `Bash`. The existing generator regenerates `home/.chezmoitemplates/claude-settings-managed.json`. `scripts/validate-agent-assets.py` checks each retained ask rule independently and requires the exact deployed hook command. Suffix matches, echo commands, duplicate entries and async entries fail. `scripts/check-agent-runtime.py` compares the deployed hook's bytes and executable status with the source.

   The red-then-green selectors remain `tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_manifest_gates_merge_update_branch_and_create_through_the_hook_and_keeps_every_other_gh_write_on_ask`, `tests/unit/test_validate_agent_assets.py::ValidateAgentAssetsTest::test_gate_validator_requires_every_retained_ask_rule_and_the_exact_synchronous_hook_entry` and `tests/unit/test_check_agent_runtime.py::CheckAgentRuntimeTest::test_runtime_check_compares_the_deployed_gh_merge_gate_hook_with_the_source`. Their assertions describe hook routing without preserving any gh-text allowance.

   Premise 6 applies per runtime as section 5.14 item 1 states. A Codex seat's sandbox confines all its tool writes to the seat worktree, scratch and enumerated writable paths. A Claude seat's Seatbelt sandbox confines Bash only. Write/Edit/MultiEdit/NotebookEdit, hooks and MCP processes run outside it, and today's rendered permission policy has no path deny for the anchored checkout, deployed manifest and hooks, trusted binaries, evidence, snapshots or private uv cache. The Claude-seat boundary remains residual until P1-15 under D-024-17 adds the permgate path deny. An unavailable-sandbox fallback supplies no authority to proceed.

   `tests/unit/test_claude_settings_merge.py::test_rendered_worker_sandbox_denies_the_trusted_root_for_bash` replaces the former render selector. It renders the darwin and linux worker policies and asserts only Bash sandbox denial for the anchored checkout, deployed manifest and hooks, trusted binaries, evidence, snapshots and private uv cache. Its containment checks include the working-directory allowance, scratch roots, listed tool caches and resolved aliases. It makes no assertion about Claude file tools, hooks, MCP processes or live sandbox enforcement.

   Worker Playbook step 4's outside-sandbox gh remains a residual with no present mitigation. P1-15 owns the pending D-024-17 wrapper with `env -i`, an absolute trusted gh and a fixed alias-free read-only `GH_CONFIG_DIR` under section 5.14 item 10. D-024-17 is not a present control. A same-UID process outside every seat sandbox also remains residual. Approval provenance uses the committed ledger under item 11 independently of this boundary.

   `home/dot_config/git/config.tmpl` retains removal of the `[url "git@github.com:"] pushinsteadof` block. HTTPS pushes use the existing gh credential helper. The live configuration already lacks this rewrite. The operator's post-merge `make update` reconciles the tracked and deployed states.

5. `tests/unit/test_gh_merge_gate.py` retains applicable three-outcome, valid-JSON, malformed-input, tool-failure and metacharacter coverage. Its table records payload text, fixture conditions and expected decision. The metacharacter property test uses the trusted entrypoint as its positive seed and asserts that no forbidden insertion allows.

   Former merge, create and update-branch allow rows become ask rows. Hook-only fixtures for PR state, body files, acceptance parsing, audit verdicts and records-only exceptions leave with the deleted parser. Execution and publication assertions move into `tests/unit/test_integrate_merge.py`, where those controls act. Their removal from the hook supplies no claim that the underlying safety requirement disappeared.

   `tests/unit/test_integrate_merge.py` defines `IntegrateMergeTest` and exercises both tracked scripts with temporary roots and fake binaries. It captures executable identity, cwd, environment, argv and body bytes. The tests assert that gate or security failures prevent a merge, that the merged head is the checked head, and that fast-forward failure preserves local evidence.

   The red-then-green selectors include `tests/unit/test_integrate_merge.py::IntegrateMergeTest::test_integrate_merge_binds_gh_and_git_to_the_trusted_root`, `tests/unit/test_integrate_merge.py::IntegrateMergeTest::test_integrate_merge_refuses_a_head_the_pr_does_not_carry` and `tests/unit/test_integrate_merge.py::IntegrateMergeTest::test_finish_pr_passes_a_body_snapshot_never_the_caller_path`. The six retained a04 test modules keep assertions relevant to retained behavior.

6. Every new or changed assertion is written before its implementation change and has red-then-green evidence. The validation record contains its exact selector, command, tested revision or source identity, exit status and verbatim output for both results.

   New a05 regressions use `911f5202e61a2e46f527fcd9a4eda0041e97410a` as the historical behavior baseline. New-file contract tests record their initial failing state. Shim, environment and body-swap reproductions exercise functioning historical behavior rather than treating a missing dependency or broken fixture as proof of a security defect.

   The retained trusted-root, metadata-identity and historical anchored-ledger regressions preserve their a03 red evidence against `31d6c322988ebb21eebe1e8bf88d5b3910c11f4d` and their a04 results. Their applicable assertions receive final a05 green runs. The committed-ledger replacement and every changed assertion or added sub-case receive new red evidence. The renamed Bash-only render selector retains applicable evidence and records its final-head run without claiming broader sandbox coverage.

   Uncommitted source identities are recorded with content SHA256 values before red runs and after fixes. Missing intermediate identities in predecessor reports remain evidence limitations. Historical suites and probe counts do not close new regressions by themselves.

7. The text-form allowance parser is deleted. Its merge option grammar, create option grammar, bare update-branch allowance, draft-create allowance, ready-create allowance and records-only boundary allowance are deleted from the hook.

   The hook's PR-body parsing, caller body-file validation, PR comparison pagination and task-copy selection, acceptance-front-matter parsing, latest accepted-dispatch requirement, audit parsing, required-check lookup and operation-specific repository logic are deleted. The former 27-row text-form allowance surface is retired with that parser.

   The hook's `test_legacy_records_do_not_block_bound_acceptance`, body-file operation tests and anchor-versus-worker-draft split cease to specify hook allowance. Applicable evidence and body safety assertions are exercised at the tracked execution boundary. The pre-merge flow never requires a post-merge `AGMSG-ACCEPTANCE status=accepted` notification.

   `tests/unit/test_gh_merge_gate.py::GhMergeGateTest::test_gate_asks_for_every_gh_text_form` supplies red-then-green proof that no former text-form allowance survives. `tests/unit/test_gh_merge_gate.py::GhMergeGateTest::test_gate_allows_only_the_tracked_entrypoint_of_the_anchored_checkout` supplies the replacement positive contract.

   Static recognition still cannot identify commands whose names and gated words are entirely assembled at runtime. Such input receives no new allowance from this hook. Native permission controls, permgate and the auto-mode classifier remain the next layer. This task makes no change to them.

8. The two ruleset scripts preserve every duplicate rule occurrence during canonicalization and comparison. A map keyed only by rule type or a set that removes occurrences does not satisfy this requirement. Two differing rules of one type produce two separately reported differences.

   `tests/unit/test_ruleset_scripts.py::RulesetScriptsTest::test_ruleset_comparison_preserves_duplicate_rule_types` retains its red-then-green evidence for both scripts. Fixtures cover two differing occurrences, an earlier missing or differing occurrence whose last occurrence matches, and exact equality with duplicates. A mismatch leaves the temporary progress ledger byte-identical. Equality permits an update only to an explicitly selected existing ledger.

9. Trusted-root binary resolution remains a requirement before hook processing and becomes an execution requirement of both new tracked orchestration scripts and the existing `scripts/orchestrator/orch-gate.sh`. The resolver runs from the deployed anchored root in a constructed trusted environment. It retains orch-gate.sh's private-directory-of-links pattern while fixing that helper's discovery and environment rebuild. It inherits no caller PATH or tool-manager configuration.

   The hook resolves `python3`, `jq`, `gh` and `git` to absolute non-shim binaries. Empty, relative and `shims` resolutions ask. Every later invocation uses the captured absolute binary or its private link. Returning to another cwd never repeats resolution.

   Environment construction starts with item 3's first-action `env -i`. Caller `GIT_DIR`, `GIT_WORK_TREE`, `GIT_CEILING_DIRECTORIES`, other `GIT_*` overrides, PATH and tool-manager overrides do not reach identity checks. Required HOME, private PATH, color settings and named gate inputs are supplied explicitly. Caller bypass flags and interpreter search-path overrides are not copied.

   Every direct git invocation of the hook and tracked orchestration scripts uses explicit `-C` and `GIT_CONFIG_NOSYSTEM=1`, `GIT_CONFIG_GLOBAL=/dev/null`, `-c core.hooksPath=/dev/null`, `-c core.fsmonitor=false`, `-c protocol.allow=never` and `-c protocol.https.allow=always`. The HTTPS exception permits the required fetch. For Git, fetching `origin/main` is the only network operation. These settings also govern Git subprocesses in the gate and finishing paths. Anchored identity operations use the anchored checkout's `.git/config`, whose protection has premise 6's runtime-specific residual; candidate worktree, global and system configuration supply no approval authority.

   `tests/unit/test_gh_merge_gate.py::GhMergeGateTest::test_gate_git_ignores_planted_hooks_fsmonitor_and_global_config` has red-then-green evidence. It plants hooks, fsmonitor commands and global configuration with execution sentinels and exercises the hook and entrypoints. Captured Git calls carry every required setting, the worker's planted configuration does not redirect checks or execution, and no sentinel executes.

   `tests/unit/test_gh_merge_gate.py::GhMergeGateTest::test_gate_resolves_its_binaries_in_the_trusted_root_and_refuses_shims` remains. Fake caller shims record any execution, trusted-root resolution supplies concrete binaries, and shim-only, empty and relative answers ask with valid JSON. The sentinels remain untouched.

   `tests/unit/test_gh_merge_gate.py::GhMergeGateTest::test_gate_runs_its_identity_checks_under_a_sanitized_environment` is red against a04 and green after the fix. It supplies caller `GIT_DIR`, `GIT_WORK_TREE`, `GIT_CEILING_DIRECTORIES` and PATH values that would redirect the old checks. Neither a forged positive nor a forged negative changes the correct anchored decision.

   The tracked scripts also capture every additional binary their existing gate or finishing path needs before entering a PR worktree. Their private execution environment contains no caller PATH component and uses no caller-selected shell startup file. Their initial interpreter launch shares item 3's orchestrator-environment premise and its runtime-specific residuals.

   Every orchestrator-side `uv run` in this task, including permission-guard.py, the gate and validators, sets `UV_CACHE_DIR=<anchored checkout>/.agents/worklog/uv-cache` and uses `--offline`. The entrypoint creates or verifies this gitignored directory at mode `0700` after resolved containment and worker-root checks. A cache under `.claude/worktrees/` or a manifest-listed worker root is refused before uv runs. No caller `UV_CACHE_DIR`, `UV_PYTHON`, interpreter search override or shared cache is inherited. Trusted execution never reads executable dependencies from `~/.cache/uv`, `~/.local/share/uv` or worker-shared mise state. A private-cache miss refuses without a network fallback. The trusted interpreter is a captured absolute binary outside those shared locations, and Python runs with `-I`. The cache's Claude-seat write protection retains premise 6's P1-15 residual. The hook itself uses no uv, only jq and Python's standard library for parsing.

   `tests/unit/test_integrate_merge.py::IntegrateMergeTest::test_integrate_merge_uses_the_private_uv_cache_only` has red-then-green evidence. It plants executable sentinels in the caller's shared uv cache and supplies a caller cache override. Captured permission-guard, gate and validator uv invocations use only the fixed anchored cache and `--offline`; all sentinels stay untouched. It checks mode `0700`, symlink and worker-root refusal, and refusal without a network fallback when the private cache lacks a dependency.

   `scripts/orchestrator/orch-gate.sh` enters its constructed environment before Git discovery. Its environment rebuild, currently at origin/main lines 87-89, retains the private PATH of links to captured absolute binaries, `GIT_CONFIG_NOSYSTEM=1`, `GIT_CONFIG_GLOBAL=/dev/null` and the private `UV_CACHE_DIR`. Direct Git calls carry explicit `-C` and all four `-c` controls above. The rebuilt environment supplies `GIT_CONFIG_COUNT=4` with fixed `GIT_CONFIG_KEY_0=core.hooksPath`, `GIT_CONFIG_VALUE_0=/dev/null`, `GIT_CONFIG_KEY_1=core.fsmonitor`, `GIT_CONFIG_VALUE_1=false`, `GIT_CONFIG_KEY_2=protocol.allow`, `GIT_CONFIG_VALUE_2=never`, `GIT_CONFIG_KEY_3=protocol.https.allow` and `GIT_CONFIG_VALUE_3=always`. These reconstructed values reach the trusted gate and the validator it starts. The validator's bare git calls inherit the sanitized environment and fixed configuration in the verified gate working directory. Caller `GIT_CONFIG_*` inputs never survive the rebuild.

   `tests/unit/test_orch_gate_path.py::OrchGatePathTest::test_orch_gate_sanitizes_the_environment_before_git_discovery` has red-then-green evidence. It checks sanitization before the first discovery call, captured absolute tools, every direct Git configuration argument and explicit `-C`, and reconstructed configuration in the gate and validator after the environment rebuild. Planted caller Git overrides, global configuration, hooks and fsmonitor sentinels never affect discovery or descendant execution. The HTTPS fetch remains permitted and non-HTTPS Git transports remain refused.

   The four section 5.14 item 7 regressions are the trusted-root binary test, the planted-Git-input test, the worker-root trusted-path test and the source-swap test named in this task. P1-6 owns `tests/unit/trusted_exec_contract.py`, which is not present at this dispatch; its creation remains outside this task.

10. `scripts/orchestrator/finish-pr.sh` moves the required finishing glue into the repository and owns PR-body preparation for its `gh pr create` calls. Its tools and subprocesses follow item 9. It uses existing tracked helpers and the tracked merge entrypoint rather than executing untracked glue.

    The body source is a regular file inside the invoking Git worktree, identified using sanitized absolute git. Validation and copying use the same opened file's bytes. Symlinks, traversal, directories, FIFOs, stdin, external files and cross-worktree sources remain refused.

    Containment and Git-metadata exclusion compare resolved filesystem identities. Both Git directory and common directory are excluded. The filesystem's case-sensitivity probe governs case-folded comparison, so `.GIT/config`, `.Git/…` and equivalent metadata aliases cannot become published content. Evidence paths used by the merge entrypoint receive the same resolved containment, regular-file, symlink and metadata exclusions.

    The entrypoint creates the snapshot directory at `<anchored checkout>/.agents/worklog/snapshots/`, which is gitignored and subject to premise 6's runtime-specific boundary, with mode `0700`. It writes each snapshot once from the validated bytes. Each unique snapshot name includes the invoking worktree's full 40-hex head and the bytes' SHA256, with a unique suffix. The snapshot is outside Git metadata by filesystem identity. Its path and directory are not selected through caller PATH, TMPDIR or a caller-provided destination. The snapshot file is regular with mode `0600`. This task adds no reservation or slot lock.

    Immediately before invoking gh, the script compares the snapshot's SHA256 again with the digest of the validated bytes and refuses a mismatch. The script passes only that snapshot pathname to gh. Gh never opens the caller's `--body-file` pathname. Replacing or deleting the caller's source after validation cannot change the published bytes. Snapshot lifetime includes gh's complete read and cleanup removes only script-owned snapshot state. Codex tool writes cannot rewrite the snapshot; Claude file tools, hooks and MCP processes retain the P1-15 path-deny gap, and mode `0700` alone does not exclude the same UID. That Claude-seat gap and a same-UID process outside every seat sandbox remain residual between the final comparison and gh's read.

    `tests/unit/test_integrate_merge.py::IntegrateMergeTest::test_finish_pr_passes_a_body_snapshot_never_the_caller_path` has red-then-green evidence. It swaps the original source for a synthetic private-target symlink after validation and captures the pathname and bytes received by fake gh. Gh receives the original validated bytes through the script-written snapshot. The same selector covers safe relative and absolute sources, refused source types, metadata case variants, full-head snapshot names, unique names for repeated calls, snapshot permissions and snapshot metadata exclusion. Case-insensitive behavior is exercised deterministically on case-sensitive CI hosts.

    `tests/unit/test_integrate_merge.py::IntegrateMergeTest::test_finish_pr_reverifies_the_snapshot_before_gh` has red-then-green evidence. It alters the snapshot after its initial write and before the final comparison. A digest mismatch refuses without invoking gh. The unchanged snapshot passes and the captured gh invocation receives that snapshot. This test does not claim to close the same-UID process residual after the last comparison.

    The finishing path retains the draft flag and the records-only publication check. Draft creation passes `--draft`. A records-only publication requires a non-empty complete comparison whose every `filename` and present `previous_filename` stays under `.orchestration/`. Existing accepted-tip checks for other non-draft publication remain execution requirements.

    `tests/unit/test_integrate_merge.py::IntegrateMergeTest::test_finish_pr_preserves_draft_and_records_only_publication_controls` has red-then-green evidence. Captured PR creation receives only the script-written validated snapshot and preserves `--draft` for a draft. Records-only publication succeeds for a complete records-only comparison and refuses an empty or incomplete comparison and a renamed source outside `.orchestration/`. A failed publication check produces no gh write.

    The retained filesystem-identity assertions move from hook body-file tests to these execution and evidence fixtures. Synthetic metadata and synthetic private contents provide the fixtures. No real credential file is opened or published.

11. `scripts/permission-guard.py` reads its only approval ledger as `git show origin/main:.orchestration/decisions.tsv` after fetching `origin/main` in the verified anchored checkout. D-024-19 and section 5.14 item 8 make this the committed ledger. It never reads approval rows from the working copy or PR tree. A working-copy row is a proposal until the operator-approved records PR carrying it merges to main. Approval provenance no longer depends on premise 6's worker write boundary.

    The guard obtains the anchor from deployed `~/.agents/agent-config.yaml`, independently of candidate revisions, expands it and resolves it with realpath. The invoking checkout is the anchored primary checkout. Its common Git directory resolves to its own `.git`, and its origin and GitHub repository identity identify `mryfmo/dotfiles`. Fetch and ledger reads use item 9's sanitized environment, captured absolute git, explicit `-C` and fixed Git configuration controls. A failed fetch, missing committed ledger, ambiguous or mismatched anchor or unrelated checkout refuses approval.

    The production `--decisions` exception is removed. There is no external ledger path. Tests create a temporary anchored checkout, name it in the deployed manifest fixture and commit its fixture ledger into origin/main. Uncommitted rows and PR-tree rows are separately forged fixture data. Candidate-manifest changes and aliases cannot choose another ledger.

    `tests/unit/test_permission_guard.py::PermissionGuardTest::test_guard_reads_the_committed_ledger_never_the_working_copy_or_the_pr_tree` replaces the anchored-ledger selector with new red-then-green evidence. A matching row present only in the anchored working copy fails. A matching row present only in the PR tree also fails. Approval succeeds only after the matching row reaches the fixture's fetched origin/main ledger, even when the working-copy ledger is absent, different or contains a forged approval. The test also covers failed fetch, missing committed ledger, missing or mismatched anchors and unrelated checkouts. The executable and anchor retain premise 6's runtime-specific residuals.

    P1-11 owns future CI wiring. That job reads the base commit's ledger rather than the head's ledger. Until it lands, the orchestrator runs the authoritative final-head comparison at acceptance and pastes its output.

12. `scripts/orchestrator/integrate-merge.sh <task> <head40> <pr>` is the new tracked merge entrypoint. It moves the required behavior from `.agents/worklog/orchestrator-glue/integrate-merge.sh` into the repository, with English shdoc comments and no execution dependency on that untracked file.

    The entrypoint validates its three arguments, establishes the same deployed anchored primary checkout and enters its own sanitized execution environment. It applies item 3's worker-writable-root refusal to every trusted path and asks before any effect when the boundary check fails. Its absolute trusted-root gh and git are the binaries used for the eventual writes, with item 9's fixed Git configuration controls. Pinning tools only inside the hook does not satisfy this requirement.

    The entrypoint checks the final-head permission guard from the anchored checkout with item 9's private offline uv cache and accepts approval only from the fetched committed origin/main ledger under item 11. It requires the task's acceptance record and the gate evidence that record names. Evidence remains inside the trusted checkout, outside Git metadata, regular and free of symlink components. Record contents are parsed as data and never sourced or evaluated. The entrypoint records SHA256 values for the evidence it consumes.

    The entrypoint invokes the trusted `scripts/require-crit-review.py` through tracked `scripts/orchestrator/orch-gate.sh`, with the final-head feedback sweep, audit and companion verdict, review receipt, Crit data and acceptance record. It passes a verified PR worktree as orch-gate.sh's second argument, matching that helper's existing `<task> <pr-worktree> <pr>` interface. A SHA string is not substituted for that worktree argument. The worktree's HEAD equals the requested head.

    The gate and validator remain the trusted checkout's copies. A PR-controlled Makefile, gate, interpreter configuration or environment cannot replace them. The allowed orch-gate.sh change implements item 9's environment controls both before discovery and across its environment rebuild, including the validator's inherited Git configuration and private offline uv cache. The task adds no bypass input and does not change the fixed acceptance schema or `scripts/require-crit-review.py`. Existing gate evidence filenames retain their helper-compatible spelling, while the records and comparisons bind the full 40-hex head.

    A `security: true` task requires `.orchestration/validation/<task>-security-<sha7>.md` and its non-empty `.last.md` companion for that head. The final non-blank verdict is `Verdict: correct`. Missing, mismatched or unsuccessful security evidence stops the entrypoint before any merge.

    Trusted gh checks that the PR is open, ready, targets the repository's valid default branch and carries exactly the head argument. Every required check passes on that head. Malformed responses, missing required checks and failed or pending checks stop execution. The entrypoint performs `gh pr merge --squash --match-head-commit <head> <pr>` only after the gate, security guard and PR checks pass.

    The entrypoint refuses modified tracked files outside `.orchestration/` in the anchored checkout before merging or changing the local checkout. After the merge, trusted git fetches only `origin/main`, checks out the default branch and fast-forwards the anchored checkout with `--ff-only`. It fetches no task-branch or PR-head ref. The fast-forward preserves local orchestration evidence and recoverable copies on failure. Untracked records are never removed. It performs no reset that discards local records, no local integration of the task branch and no push to main. Required glue behavior stays within the two allowed tracked scripts and reuses existing tracked helpers.

    `tests/unit/test_integrate_merge.py::IntegrateMergeTest::test_integrate_merge_binds_gh_and_git_to_the_trusted_root` has red-then-green evidence. A shim first on the caller's PATH is never executed. Captured calls prove that identity checks, gate subprocesses, merge and fast-forward use trusted tools and a constructed environment. Its refusal cases prove that a failed gate, missing or incorrect security verdict, unsafe evidence path or failed required check produces no merge.

    `tests/unit/test_integrate_merge.py::IntegrateMergeTest::test_integrate_merge_refuses_a_head_the_pr_does_not_carry` has red-then-green evidence. A PR-head mismatch produces no merge and no fast-forward. The positive case captures the exact `--match-head-commit` argument, binding a later head change to GitHub's merge refusal.

    `tests/unit/test_integrate_merge.py::IntegrateMergeTest::test_integrate_merge_fetches_only_origin_main_and_preserves_local_records` has red-then-green evidence. Captured fetch and checkout calls target only the valid default-branch update and every fast-forward uses `--ff-only`. Modified tracked files outside `.orchestration/` refuse without a merge or local update. Dirty tracked orchestration records and untracked records survive successful and failed fast-forwards, with recoverable copies retained on failure.

## Decision row

D-024-14 describes the approved permission-surface change: the three ask rules leave and the synchronous hook is added, while every other gh write stays on ask. D-024-16 changes the hook's allowance design to the trusted entrypoint. Its design row does not substitute for a permission-scoped digest approval.

At a05 acceptance, the orchestrator runs the guard from the verified anchored checkout with `--base origin/main --head <final head>`, item 9's fixed private `UV_CACHE_DIR` and `--offline`, and records the complete output. It prepares the decision row for that a05 permission-diff digest using the next free `D-024-NN` id and the recorded user-approval basis. The row contains `scope=permission approved_by=user diff_sha256=<exact digest>`.

Under D-024-19, that working-copy row is a proposal. The orchestrator puts it through the records PR for boundary 24, which the operator approves through the live hook before the a05 implementation merge. Only after that records PR merges to main does the row carry approval authority. This records PR is separate from the one implementation PR, #420. The guard fetches origin/main again and reads the row only through `git show origin/main:.orchestration/decisions.tsv`.

The worker does not edit `.orchestration/decisions.tsv`. An inherited digest, an uncommitted anchored row or a matching row in the PR tree supplies no approval. The authoritative comparison is repeated against the explicit final head after the records merge and any base update. A changed final-head permission digest requires a matching operator-approved records PR to reach main before integration.

## Out of scope

Worker-seat allow rules remain a separate task after P1-7 because they edit `herdr-agents`. P1-15 under D-024-17 owns both the Claude-seat permgate path deny and the outside-sandbox gh wrapper using `env -i`, an absolute trusted gh and a fixed alias-free read-only `GH_CONFIG_DIR`. Neither is implemented here. The outside-sandbox gh exclusion has no present mitigation. Claude file tools, hooks and MCP processes retain their path-deny gap until P1-15, and a same-UID process outside every seat sandbox remains residual. The `regime` CI job remains P1-11's work. No Codex boundary file changes.

Permgate, including `home/dot_agents/permgate-policy.yaml`, remains unchanged. The live ruleset itself and its toggles remain unchanged. Ruleset scripts only display and verify. Post-merge `make update` and live deployment remain the operator's actions under DoD2.

No gh text-form allowance of any kind is implemented. The hook's only updated-input rewrite replaces `argv[0]` with its verified anchored realpath and preserves the three arguments. The hook gains no shell parser, PR-body parser, evidence parser, alternate entrypoint or operation-specific exception.

No SKILL file enters `allowed_files`. The worker does not edit predecessor canonical task texts, predecessor evidence, acceptance records, the decision ledger or unrelated orchestration helpers. orch-gate.sh is explicitly inside this task's edit boundary; dispositions-a02 follows this task to avoid concurrent edits to it. The one a04 branch-copy deletion is the stated reset bookkeeping exception. Other reset records belong to the orchestrator.

## Check

`make render-check`, `make validate-agent-assets` and `make format` pass.

`shellcheck home/dot_claude/hooks/executable_gh-merge-gate.sh scripts/orchestrator/ruleset-request.sh scripts/orchestrator/ruleset-verify.sh scripts/orchestrator/integrate-merge.sh scripts/orchestrator/finish-pr.sh scripts/orchestrator/orch-gate.sh` is clean.

`shfmt -d home/dot_claude/hooks/executable_gh-merge-gate.sh scripts/orchestrator/ruleset-request.sh scripts/orchestrator/ruleset-verify.sh scripts/orchestrator/integrate-merge.sh scripts/orchestrator/finish-pr.sh scripts/orchestrator/orch-gate.sh` is clean.

The worker runs `uv run --offline python -m unittest tests.unit.test_gh_merge_gate tests.unit.test_integrate_merge tests.unit.test_orch_gate_path tests.unit.test_permission_guard tests.unit.test_ruleset_scripts tests.unit.test_generate_agent_configs tests.unit.test_validate_agent_assets tests.unit.test_check_agent_runtime tests.unit.test_claude_settings_merge -v` in its own sandbox. The suite is green. The hook, tracked-entrypoint and orch-gate modules run together with the retained a04 modules. Every orchestrator-side replay sets item 9's fixed private `UV_CACHE_DIR` and retains `--offline`.

The worker runs `uv run --offline python -c 'from tests.unit.test_claude_settings_merge import test_rendered_worker_sandbox_denies_the_trusted_root_for_bash; test_rendered_worker_sandbox_denies_the_trusted_root_for_bash()'` in its own sandbox. The Bash-only render assertion is green. An orchestrator replay uses the same fixed private `UV_CACHE_DIR`.

The worker records a worker-worktree refusal as an anchor refusal. From the anchored checkout, the orchestrator runs `UV_CACHE_DIR=<anchored checkout>/.agents/worklog/uv-cache uv run --offline --with pyyaml python -I scripts/permission-guard.py --base origin/main --head <final head>`. It records the complete canonical diff, digest and exit status. Exit 1 before a matching row reaches the fetched committed origin/main ledger remains exit 1. Exit 0 requires that committed approval. No working-copy row makes the command pass.

`git diff --numstat origin/main...HEAD` shows at most 850 changed lines outside `tests/` and `.orchestration/` and at most 1250 changed lines under `tests/`. Changed lines are additions plus deletions. The source total includes orch-gate.sh and the regenerated managed settings. The a04 record at `911f5202` measured 648 source lines and 908 test lines under its historical accounting. The parser deletion reduces the hook. The final per-file inventory and both totals are recorded against the final head. No new dependency is added.

The validation file `.orchestration/dotfiles-T133-permission-guard-gate-a05/validation.md` contains exact commands, verbatim outputs, exit statuses and tested identities. It includes all named a05 red-then-green selectors, retained regression evidence, the updated probe closure table, the gh-text ask table, the entrypoint metacharacter property test, duplicate-ruleset coverage, filesystem-identity cases, the body-swap interleaving and the committed-ledger comparison against working-copy and PR-tree forgeries. It also includes the renamed Bash-only render assertion, first-action sanitization, updated-input binding, trusted-path refusals, Git configuration isolation with the HTTPS exception, the private offline uv-cache regression, orch-gate discovery and validator-inheritance regression, snapshot recheck and both added orchestrator-effect tests. The record states the Claude-seat path-deny gap, same-UID and outside-sandbox gh residuals without calling any closed.

Historical failures remain disclosed. An inherited formatting failure is reproduced against its unchanged base and recorded with its real output. It authorizes no out-of-scope repair.

No local Bats tests run. Required Bats results come from GitHub Actions. The orchestrator runs `UV_CACHE_DIR=<anchored checkout>/.agents/worklog/uv-cache uv run --offline --no-project --with pyyaml python -I scripts/orchestrator/task-consistency-check.py --root <anchored checkout> .orchestration/tasks/dotfiles-T133-permission-guard-gate-a05.md` before dispatch and at acceptance, covering C1 to C10 and C7b. This validator invocation follows item 9's cache and environment contract.

## Completion

The existing branch `tools/permission-guard-gate-a01` continues PR #420 from `911f5202e61a2e46f527fcd9a4eda0041e97410a`. The first push replaces the a04 branch task copy with the byte-identical dispatched a05 copy. Seat a010 keeps its branch, fixes and evidence. The reset creates no second implementation PR. The missed `2026-10-19T03:00Z` deadline remains reported, and the orchestrator owns the new estimate.

The Completion clause of `.orchestration/tasks/dotfiles-T129-normalised-comparison-lint-a01.md` applies with this task's existing branch, the qualifications below, `dotfiles-T133-permission-guard-gate-followup-a01` as the owner of any advisory P2, and `task_copy=<sha256 of .orchestration/dotfiles-T133-permission-guard-gate-a05/task.md>` in RESULT. The orchestrator writes the owner task before assigning its first advisory P2. The six reset defects and retained duplicate-rule defect belong to this task.

Every worker-side fix round, before or after the first RESULT, counts toward INV-6 under C-61. Predecessor counters, the a03 Bot correction, its single CI-repair round, question PONGs, S2 withdrawal and a04 S1 stop remain historical records. They are not recast as approvals.

The worker's own pre-push review is one round at most. A surviving P0/P1 is sent in RESULT as open and stops integration. The worker starts no further private correction-and-review cycle to avoid reporting it. Permitted later rounds remain subject to INV-6 and the inherited completion rule.

No `@codex review` comment is posted. Automatic final-head reviews are observed within the bounded 15-minute window, and absence is recorded as `bot: none`. Required GitHub Actions checks pass before RESULT. Every feedback item carries its proposed disposition. Surviving P0/P1 findings remain open for the operator's decision.

A Codex seat writes evidence at the same relative paths in its worktree and says so in RESULT. Worker review evidence uses the required `-worker-` infix. Agent-side review evidence and its receipt follow the repository's Crit-data rules without opening a browser review or asking the user to review.

RESULT names the final head, base, branch, changed files, Bot findings and dispositions, every open P0/P1, exact test selectors, measured caps, all six new deployable scripts, the orch-gate.sh change, task-copy SHA256 and evidence paths with the SHA256 values consumed by the entrypoint. The report distinguishes predecessor observations from final-head closure and records the indirect-command-recognition residual, interpreter-launch premise, Claude-seat path-deny gap, same-UID process residual and unmitigated outside-sandbox gh exclusion owned by P1-15 under D-024-17. The orchestrator copies worktree evidence by absolute path before acceptance review.

This task is `security: true`. Under C-80, a security-profile context reviews this complete a05 task text before dispatch. That review is a dispatch prerequisite rather than a claim made by this draft. The orchestrator also runs the task-level audit and a separate security-profile review on the final implementation head.

The finding-class table includes `decision-not-bound-to-execution` and preserves the predecessor classes `argv-text-mismatch`, `unbound-evidence` and `fail-open-on-error`. A third non-advisory finding of one class stops the artifact for redesign. It never starts another instance-by-instance correction round. The acceptance record retains the required class search and re-plan evidence.

Final-head feedback collection, task-level audit, finding dispositions, acceptance and the integration gate follow Orchestrator Playbook step 10 in its prescribed order. The gate receives `PR_FEEDBACK_EVIDENCE`, `AUDIT_EVIDENCE`, `ACCEPTANCE_EVIDENCE` and the agent review receipt. A changed head receives fresh required evidence. The security review of that final head precedes the gate.

The deployed hook allows only the anchored tracked `integrate-merge.sh` invocation through updated input naming the verified realpath. The script itself runs each gh and git write as a separate command, without shell chaining. Callers submit the entrypoint as one command with its three arguments. The eventual merge is exactly `gh pr merge --squash --match-head-commit <audited head> <pr>`.

Until PR #420 lands, strings carrying `gh pr merge` or `gh pr create` are written with the file-edit tool rather than Bash heredocs or echo. This includes test fixtures, reports and validation prose. The worker does not deploy the new hook or relax its tracked-main identity conditions to bootstrap this PR.

## Checks (pasted by the orchestrator before each send)

```
(pasted at dispatch)
```

Local Bats, live payload execution and live deployment are not performed by this task; deployment remains unverified until the operator's post-merge checks.
Claude file tools, hooks and MCP processes retain the P1-15 path-deny gap, outside-sandbox gh has no present mitigation, and a same-UID process outside every seat sandbox remains residual.