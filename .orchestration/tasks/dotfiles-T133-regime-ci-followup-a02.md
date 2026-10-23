---
format: 2
task_id: dotfiles-T133-regime-ci-followup-a02
kind: code
security: true
design: 5.14 items 0-10
design_review:
  design: .orchestration/plans/024-design-quality.md
allowed_files:
  - scripts/orchestrator/regime-ci.py
  - .github/workflows/regime.yml
  - tests/unit/test_regime_ci.py
  - tests/unit/test_workflow_security.py
  - .orchestration/dotfiles-T133-regime-ci-followup-a02/**
after: []
threat_table:
  - {control: "scripts/orchestrator/regime-ci.py", disposition: "residual: dotfiles-T133-regime-ci-followup-a03; behavioral fixtures and an independent final-head audit constrain the verifier changes; host provenance is not closed."}
  - {control: ".github/workflows/regime.yml", disposition: "closed: tests/unit/test_workflow_security.py::WorkflowSecurityTest::test_regime_verifier_sets_private_uv_cache"}
  - {control: "tests/unit/test_regime_ci.py", disposition: "residual: dotfiles-T133-regime-ci-followup-a03; preserve existing assertions, isolate all Git operations and independently audit each regression against its claim."}
  - {control: "tests/unit/test_workflow_security.py", disposition: "residual: dotfiles-T133-regime-ci-followup-a03; exact-step assertions and final-head CI constrain workflow regressions without authenticating the local runtime."}
  - {control: ".orchestration/dotfiles-T133-regime-ci-followup-a02/** including task.md and all evidence", disposition: "residual: dotfiles-T133-regime-ci-followup-a03; compare the whole dispatched copy and digest and reconcile every reported command, commit and CI result at acceptance."}
  - {control: "task metadata", disposition: "residual: dotfiles-T133-regime-ci-followup-a03; run consistency checks before dispatch and acceptance and compare the complete anchored bytes."}
  - {control: "metadata separators", disposition: "residual: dotfiles-T133-regime-ci-followup-a03; parse the first YAML document and compare all dispatched bytes, including separators and populated Checks."}
  - {control: "in-process effects", disposition: "closed: tests/unit/test_regime_ci.py::RegimeCiTest::test_git_environment_cannot_redirect_fixture_writes"}
  - {control: "workflow and interpreter or environment inputs", disposition: "residual: dotfiles-T133-regime-ci-followup-a03; measured bindings and descendant probes are dispatch conditions; same-UID tool provenance remains unproved."}
  - {control: "new or renamed scripts", disposition: "residual: dotfiles-T133-regime-ci-followup-a03; none authorized; inventory and audit reject new runtime code hidden in evidence."}
  - {control: "retained-directory acceptance rule", disposition: "closed: tests/unit/test_regime_ci.py::RegimeCiTest::test_retained_predecessor_entries"}
  - {control: "patch-id equality rule", disposition: "closed: tests/unit/test_regime_ci.py::RegimeCiTest::test_precheck_survives_main_merge_only"}
  - {control: "workflow env UV_CACHE_DIR", disposition: "closed: tests/unit/test_workflow_security.py::WorkflowSecurityTest::test_regime_verifier_sets_private_uv_cache"}
  - {control: "cap measurement and refusal diagnostics", disposition: "closed: tests/unit/test_regime_ci.py::RegimeCiTest::test_caps_refusal_names_merge_base_and_counts"}
  - {control: "task-copy target selection", disposition: "closed: tests/unit/test_regime_ci.py::RegimeCiTest::test_targets_only_changed_task_copies"}
  - {control: "records-only boundary and evidence-sync recognition", disposition: "closed: tests/unit/test_regime_ci.py::RegimeCiTest::test_records_sync_is_not_a_task_pr"}
  - {control: "merge-record authentication", disposition: "residual: dotfiles-T133-regime-ci-followup-a03; independently authenticated gate results are mandatory inputs; missing or unverifiable provenance fails closed and blocks dispatch."}
  - {control: "bootstrap checker and evidence consumption", disposition: "residual: dotfiles-T133-regime-ci-followup-a03; replacement probes must bind actual consumed bytes to the validated snapshot; they do not exclude arbitrary same-UID host compromise."}
  - {control: "orchestrator effect merge", disposition: "residual: dotfiles-T133-regime-ci-followup-a03; only the orchestrator integrates the audited exact head through Orchestrator Playbook step 10.5."}
  - {control: "orchestrator effect update-branch", disposition: "residual: dotfiles-T133-regime-ci-followup-a03; recompute measurements and renew CI, feedback, audit and gate after every moved head."}
  - {control: "orchestrator effect forced worker removal", disposition: "residual: dotfiles-T133-regime-ci-followup-a03; none planned; preserve dirty state and record any forced discard in acceptance."}
  - {control: "orchestrator effect successor owner stub", disposition: "residual: dotfiles-T133-regime-ci-followup-a03; create its owner stub before anchoring this text or recording advisory ownership; the worker cannot edit it."}
  - {control: "orchestrator effect pre-dispatch measurements", disposition: "residual: dotfiles-T133-regime-ci-followup-a03; populate Checks from authenticated measurements before review; unresolved bindings or gate sources prohibit dispatch."}
  - {control: "5.14 item 0", disposition: "residual: dotfiles-T133-regime-ci-followup-a03; item 0 applies by reference; Item 5 detects at the next records PR and makes no prevention claim."}
  - {control: "5.14 item 1", disposition: "residual: dotfiles-T133-regime-ci-followup-a03; item 1 applies by reference; record measured Codex boundaries without claiming other seat deployments."}
  - {control: "5.14 item 2", disposition: "residual: dotfiles-T133-regime-ci-followup-a03; item 2 applies by reference; require binding and hostile-environment probes before execution; wider host provenance remains residual."}
  - {control: "5.14 item 3", disposition: "residual: dotfiles-T133-regime-ci-followup-a03; item 3 applies by reference; require symlink, case-alias and worker-root negatives without claiming a host trust boundary."}
  - {control: "5.14 item 4", disposition: "residual: dotfiles-T133-regime-ci-followup-a03; item 4 applies by reference; actual checker and evidence replacement probes are mandatory; fixture equality alone is insufficient."}
  - {control: "5.14 item 5", disposition: "residual: dotfiles-T133-regime-ci-followup-a03; item 5 applies by reference; create no new integration reservation and bind all reported heads in full."}
  - {control: "5.14 item 6", disposition: "residual: dotfiles-T133-regime-ci-followup-a03; item 6 applies by reference; report unavailable probes and unproved boundaries without upgrading them to closed."}
  - {control: "5.14 item 7", disposition: "residual: dotfiles-T133-regime-ci-followup-a03; item 7 applies by reference; reuse the existing shared probes and distinguish modeled, native and live observations."}
  - {control: "5.14 item 8", disposition: "residual: dotfiles-T133-regime-ci-followup-a03; item 8 applies by reference; PR-supplied references and acceptance prose cannot authenticate predecessor or gate authority."}
  - {control: "5.14 item 9", disposition: "residual: dotfiles-T133-regime-ci-followup-a03; item 9 applies by reference; Item 4 lands the workflow caller half only; checker refusal remains held in a07-checker."}
  - {control: "5.14 item 10", disposition: "residual: dotfiles-T133-regime-ci-followup-a03; item 10 applies by reference; any sandbox denial stops the worker with a blocked PONG."}
premises: []
---

# AGMSG-TASK dotfiles-T133-regime-ci-followup-a02 — verifier rules and caller cache

[memory:decision] Supersede the owner stub written 2026-10-19. PR #425 merged; slice 2 shares no file, so after is empty. TASK names a Codex seat; a012 is free.
[memory:failure] The 2026-10-21 reset lineages #442 a03, #411 a04 and #378 a02 were refused despite declared rules; per-PR not-applicable sweep rows are a stopgap. Fix the verifier itself.
Read .agents/worklog/orchestrator-glue/BRIEF-TEMPLATE-NOTES.md and the a01 acceptance record. Design 5.14 items 0-10 in .orchestration/plans/024-design-quality.md apply by reference. The orchestrator creates the a03 owner stub if absent before anchor review.

## Items

1. Read retained_predecessor_directories from the authoritative task front matter. Accept an otherwise forbidden retained path only when its bytes, Git object type and entry mode match a regular-file entry at that same path in the established predecessor PR head or main/base; otherwise refuse. Preserve dispatched-policy precedence and authenticate reference provenance under item 8.
   Add RegimeCiTest.test_retained_predecessor_entries: predecessor-only/main-only matches pass; neither match, absent references, changed bytes, regular-to-symlink/executable/gitlink swaps, escaping/malformed directories, prefix lookalikes, untrusted SHAs and unrelated forbidden paths refuse. A retained directory never grants a blanket exemption.
   Gap: regime-ci.py --base 3594070f --head b3ca1b80 on #442 refused six retained pre-send-check-a01 files (D-024-64).

2. Preserve precheck ancestry, digest and evidence-only rules. Accept update-branch only when main merges explain the intervening history, git patch-id --verbatim over each head's merge-base..head is unchanged, and every merge's resulting tree outside existing evidence exemptions equals the independently recomputed conflict-free merge of its actual parents. Authenticate the main parents; refuse conflicts, extra source commits, comparison errors or tree drift.
   Add RegimeCiTest.test_precheck_survives_main_merge_only: clean main merges pass; patch drift, unrelated ancestry, reverted code drift and merge-resolution edits refuse. Include repeated identical blocks where a hunk moves with equal patch IDs, both directly and through a merge resolution; assert equal IDs and rejection by the tree/history check. Line numbers are excluded from [patch IDs](https://git-scm.com/docs/git-patch-id).
   Gap: #411 at 94fa6465 refused precheck head d3eb4249 as differing outside result-precheck-a04 evidence.

3. Keep cap counting PR-wide from git merge-base <base> <head>, additions plus deletions. Refusal messages name the full resolved merge-base and both measured counts and limits; change no counting or acceptance behavior.
   Add RegimeCiTest.test_caps_refusal_names_merge_base_and_counts with an advanced base, both exceeded caps, exact-limit controls and unchanged verdicts.

4. Set the base-verifier step's env UV_CACHE_DIR to ${{ runner.temp }}/uv-cache, the workflow equivalent of "${RUNNER_TEMP}/uv-cache"; checker descendants inherit it. Add WorkflowSecurityTest.test_regime_verifier_sets_private_uv_cache against that exact step's env.
   This lands design 5.14 item 9's caller half. The missing-variable refusal belongs to held dotfiles-T133-task-generator-plan-check-a07-checker; do not edit that checker, restore its refusal here or expand to unrelated callers.

5. At dispatch read every Owned by dotfiles-T133-regime-ci-followup-a02 section and continuation in .orchestration/acceptance/dotfiles-T133-regime-ci-followup-a01.md. Snapshot all row IDs/classes in report.md and fix every owned row in this PR; each row has its own independently red behavioral subcase and named green selector.
   ci:39194965216:1: test_targets_only_changed_task_copies targets added/changed task.md copies, not all historical directories; missing dispatch warns until REGIME_REQUIRE_DISPATCHED.
   ci:39239649184:1 and local:8f7b976:1: test_records_sync_is_not_a_task_pr recognizes records boundaries/evidence sync by content and established provenance; code changes or forged branch names cannot exempt a PR. Preserve secrets/home-path scans and acceptance detection.
   ci:detection:1: test_records_pr_detects_unrecorded_merge checks every main integration since the authenticated preceding boundary when acceptance records change. Match the accepted PR head through its GitHub merge mapping, including squash merges; require acceptance JSON head plus independently authenticated gate success bound to mryfmo/dotfiles, that exact PR head and that boundary. The boundary itself needs authenticated boundary provenance, not a task acceptance record.
   Select gate producer/workflow identity from trusted preceding-boundary policy, never the candidate records. PR-controlled prose, a matching JSON head, a bare success status, or records that authenticate each other are insufficient. Fixtures cover genuine success, missing/unrecorded integration, forged matching prose/JSON, wrong repository/head/boundary/producer, replay and unavailable authentication; all invalid/unavailable cases refuse. Missing trusted gate production is a dispatch blocker, not another sweep exception.
   security:80e4040:1, security:380e7f4:1 and 4310261909: RegimeCiTest.test_workflow_contract_matches_protected_base verifies this task's workflow contract against the exact protected-base selection and GitHub-owned base_ref; task-copy contract subcases are independently red on the old text.
   security:380e7f4:2: test_git_environment_cannot_redirect_fixture_writes fixes the inherited-environment harness before any fixture commit/reset. Reuse trusted_exec_contract probes: hostile GIT_DIR, GIT_WORK_TREE, GIT_CONFIG_* and local config cannot redirect reads/writes or launch helpers; a second disposable repository's refs, index and bytes stay unchanged. Real Git runs in temporary repositories under the measured sanitized bindings; do not claim fake-PATH isolation.
   audit:380e7f4:1: test_bootstrap_uses_validated_snapshot bootstraps the candidate verifier at the code head with the base checker through design 5.14 items 3-4. Exercise the actual launch and consumed task/design/evidence inputs, injecting symlink, case-alias and same-user replacement after validation; only the validated bytes may execute/be consumed, or the operation refuses. Reject worker-root aliases; compare executed checker and consumed evidence digests, not fixture-copy equality. A later evidence commit changes only this task's directory; report.md names the bootstrapped code head.
   test_bound_descendants_ignore_path_shims binds the harness and actual verifier/checker descendants to the measured uv/Python/Git selection under items 2 and 9; reuse the bound parent Python for checker children instead of another bare uv discovery. The four item-7 probes must exercise real consumers; list any native case-alias limitation separately from deterministic coverage.
   Any further owned row present at dispatch gets its own fixture and report mapping. Correct this task's rows/wording; never rewrite historical task copies or substitute not-applicable sweep rows for fixes.

## Check

Write fixtures before production edits. For each Item and each owned row record red against origin/main production bytes, its full baseline SHA and red-fixture commit, then green at the fix commit. Red must fail the behavioral assertion, never imports, tooling, setup or a missing new API; retain every existing assertion.
The required suite is uv run python -m unittest tests.unit.test_regime_ci tests.unit.test_workflow_security -v; execute it with the measured uv absolute path and explicit measured Python selection under design 5.14 items 2 and 9. Record the fully expanded invocation; checker children remain isolated. Tests supply temporary absolute UV_CACHE_DIR values.
Run ruff check and ruff format --check on scripts/orchestrator/regime-ci.py, tests/unit/test_regime_ci.py and tests/unit/test_workflow_security.py using ruff.toml. Run actionlint .github/workflows/regime.yml if installed and record absence otherwise. Never run Bats locally.
at most 650 changed lines outside `tests/` and `.orchestration/`, and at most 1600 under `tests/`.
Measure with git diff --numstat <merge-base40> <head40>.
Resolve the RESULT-time merge-base with git merge-base <authenticated-main40> <head40>; paste full SHAs, changed-file inventory, per-file additions/deletions and both totals. Caps cover the whole PR and leave headroom for all five fixes, their fixtures and one Bot fix round; recount after update-branch.

Host resolution: /usr/bin/env -i PATH=/usr/bin:/bin HOME="$HOME" UV_CACHE_DIR="$UV_CACHE_DIR" "$HOME/.local/bin/mise" which uv. Paste actual output, never guess an install path or add bin. Resolve Python from the measured mise installation too; the supplied host measurement is version 3.15.0.
A resolver transcript alone is not a binding. Before any validation, the orchestrator measures the item-2/item-9 launch bindings, hashes/versions and descendant probes, including baseline descendant resolution; every execution uses those bindings. The candidate's replacement regression must be green before its bootstrap. after: [] waives no binding prerequisite. Missing launch-binding support or authenticated gate source blocks dispatch; no shim/default-cache fallback and no new wrapper under evidence.
Before anchor review the orchestrator replaces all HOLD fields in the seven-line Checks fence with measured commands, output, source identities and exits. HOLD bytes cannot be approved or dispatched; reviews and task digests stay outside the text. Dispatch the anchored bytes unchanged; any later edit invalidates review.
Bootstrap uses the candidate code head, the base checker and the same verified-consumption path tested above. Paste verifier/checker/input sources and digests, both heads, expanded command and output. Final-head GitHub Actions must pass too; the base workflow cannot exercise its own candidate verifier changes.
Every evidence item names its producer: worker (Codex seat) or orchestrator (Claude seat, sandboxed Bash). validation.md contains every executed validation command, exit and verbatim redacted stdout/stderr; every claimed PR/commit identifier appears there. No Codex herdr-socket probe.

## Completion

Worker Playbook steps 2-15 apply, especially step 4: every command stays sandboxed, including HTTPS push. Any denial goes in sandbox.md and sends AGMSG-PONG v1 status=blocked with exact command, exit, output and boundary; wait for re-tasking without an outside retry.
Fetch origin/main inside the sandbox; create fresh tools/regime-ci-followup-a02 with git switch -c tools/regime-ci-followup-a02 --no-track origin/main. Push with git push https://github.com/mryfmo/dotfiles.git HEAD:refs/heads/tools/regime-ci-followup-a02 without -u; never change shared Git config.
Open one draft PR with an English title/body, then follow step 15's ready transition, exact-head CI and bounded Bot wait. One worker Bot fix-round at most; surviving P0/P1 stops for the operator, and the worker resolves no thread. Name mryfmo/dotfiles explicitly in GitHub commands.
Commit under .orchestration/dotfiles-T133-regime-ci-followup-a02/: byte-identical task.md, report.md, validation.md, sandbox.md, learning.md, autoskill.md and result.txt. Keep plan/todo/learn worklogs current and uncommitted. No executable evidence or unrelated edits.
report.md maps five Items and every owned row to selector, baseline/red-fixture SHA and green-fix SHA; include bootstrap code head, provenance observations, residuals and cost: observed or n/a. autoskill.md records used/not-used.
Follow AGENTS.md's agent-side Crit JSON/receipt and make require-crit-review procedure when required, with -worker- evidence names inside the allowed evidence directory; no browser review/publication. Include plan-mode-used when applicable.
result.txt carries task_copy=<SHA256 of task.md> and a literal head=<full 40-hex code head>; commit it through the current evidence-only procedure. The outgoing RESULT names the actual final evidence head and the bound code head separately; include precheck= when emitted.
Send AGMSG-RESULT v1 task_id=dotfiles-T133-regime-ci-followup-a02 status=ready_for_review naming PR, branch, full head, code_head, merge_base, caps=650/1600, changed_non_tests, changed_tests, five Item red/green SHA pairs, per-owned-row pairs, task_copy, artifact paths and proposed feedback dispositions.
The orchestrator owns advisory disposition and integration under Playbook step 10: final-head feedback sweep, task audit/security review, acceptance, gate with required evidence, then exact-head merge. New heads renew the evidence; no worker merge.

## Checks
