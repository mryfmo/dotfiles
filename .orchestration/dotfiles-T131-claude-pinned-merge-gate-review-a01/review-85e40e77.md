# PR #400 — interrupted adversarial review of the assigned snapshot

- PR: https://github.com/mryfmo/dotfiles/pull/400
- Assigned and fetched head: `85e40e77672ccd5b5d5d5a060a698d9e25fdf7ec`
- Merge base: `a8a747af06b32ff1d0d1720467892f34d9465ae4`
- Date UTC: 2026-10-17; exact completion timestamp is appended below.
- Status: **blocked: PR moved**. The final read-only `gh pr view 400 --repo mryfmo/dotfiles --json headRefOid,state,url` returned `eb6af9e50c1448fc17f6efecab63107e56064e9b`, OPEN. Review stopped immediately. Findings and tests below apply only to the assigned old snapshot; no conclusion is made about the new head. This is input to acceptance, never approval.

What this change does: It replaces the merge, update-branch and create permission prompts with a Claude PreToolUse hook, adds settings/runtime validation, and removes the HTTPS-to-SSH push rewrite. The expected load is a few concurrent agent seats using shared orchestration records. A clean clone under this task directory was used because the original tracked-clean worktree has an existing cherry-pick state and refused checkout; that state and PR #399's branch were preserved.

## Findings at the assigned head

All examples below are dry inputs against the test suite's stub gh. No merge/create command was sent to GitHub. Finding identifiers are local review identifiers, not GitHub thread IDs.

1. [P1] High — `home/dot_claude/hooks/executable_gh-merge-gate.sh:55` — Quoted executable/subcommand spellings bypass the only detector and return no decision after the corresponding ask rules were removed.
   - `"gh" pr merge 7 --admin`, `gh pr "merge" 7 --admin`, and `g''h pr merge 7 --admin` all returned exit 0 with empty stdout (`quoted-binary`, `quoted-subcommand`, `concatenated-binary`). Their shell command is still gh. An alias-shaped `gh land 7 --admin` also receives no decision; its expansion was not executed or configured.
   - Fix the actual-command recognition and conservatively ask on unresolved executable/alias forms. Silence leaves ordinary auto-mode permission handling in charge instead of this gate.

2. [P1] High — `home/dot_claude/hooks/executable_gh-merge-gate.sh:36` — The decision reason is interpolated into JSON after preserving whitespace, so a rejected tab-separated command emits invalid JSON instead of ask.
   - `gh<TAB>pr<TAB>merge 7; true` returned exit 0 and a JSON parse failure (`tab-json`); line 33 retains tabs in the captured command reason. Use a JSON encoder rather than printf interpolation.

3. [P1] High — `home/dot_claude/hooks/executable_gh-merge-gate.sh:55` — Detector errors are treated as unrelated commands, and the installed command hook has no fail-closed failure policy.
   - A local stub grep exiting 23 made a valid pinned merge return exit 0 with no decision (`detector-crash`), because `grep ... || exit 0` conflates non-match with failure. Empty input likewise returned no decision. There is no `set -e` or `pipefail`; the ERR trap does not protect this guarded failure or a process that never starts/crashes.
   - The rendered hook at `home/.chezmoitemplates/claude-settings-managed.json:157` and generator at `scripts/generate-agent-configs.py:447` only set type/command, without failure blocking. Current [Claude hook documentation](https://code.claude.com/docs/en/hooks#block-the-action-when-a-hook-fails) says startup, timeout and invalid-output failures normally continue permission handling; the newer `onFailure` control requires a supporting runtime. This was documentation/static verification, not a live Claude test.
   - Also, an empty successful default-branch result can allow a draft onto an open stack parent (`draft-empty-default-stack`): lines 129–138 never require a nonempty valid default branch. Distinguish all data/error cases and require a valid ask or a blocking failure.

4. [P1] High — `home/dot_claude/hooks/executable_gh-merge-gate.sh:66` — Any newly initialized primary repository qualifies as the main checkout, and its evidence is not bound to the target repository selected by --repo.
   - `arbitrary-primary-checkout` allowed a merge using only the fixture's unrelated `git init` repository. `other-repository-same-head` allowed `--repo other/repo` against the same locally supplied acceptance SHA, with the remote responses switched to that repository. The hook compares git-dir/common-dir but never authenticates the canonical checkout or its GitHub repository.
   - Linked worktrees are rejected, but a worker can create a separate primary repository inside its writable tree and supply records there. Bind both checkout identity and target repository to the actual orchestration authority.

5. [P1] High — `home/dot_claude/hooks/executable_gh-merge-gate.sh:76` — Acceptance is a whole-file text match rather than validated front matter for this PR/task/head.
   - A record whose front-matter head is a different SHA, whose body merely quotes the desired `"head"`, and whose accepted line names an unrelated task still allowed both merge and ready create (`body-only-wrong-task-record`, `ready-body-only-record`). A symlinked acceptance parent was also followed (`symlinked-acceptance-parent`); only the final record path is checked for a symlink.
   - Parse the actual record schema, bind its task/PR/repository/head and latest applicable verdict, and verify the provenance of the evidence used to grant permission.

6. [P1] High — `home/dot_claude/hooks/executable_gh-merge-gate.sh:210` — An audit-shaped pathname is sufficient; the path need not even be a regular audit file.
   - Replacing the matching `.md` file with a directory still returned allow (`audit-is-directory`). A file containing only `Verdict: incorrect` also returned allow (`audit-is-incorrect`), without any finding dispositions. This does not establish the required task audit or integration-gate evidence.
   - Validate the actual regular/readable task audit, its complete head and authoritative verdict/dispositions, rather than the size of a glob array.

7. [P1] High — `home/dot_claude/hooks/executable_gh-merge-gate.sh:113` — The create parser approves unquoted shell glob values before expansion, so the actual CLI can receive flags the gate did not validate.
   - `gh pr create --draft --base main --head task/ok --title *` returned allow (`create-glob-title`). A separate shell that only printed arguments, with fixture filenames `--0-title`, `--draft=false`, `--head=evil`, expanded the final value into those three words (`glob-expanded-arguments`). No gh executable was invoked for that proof. The extra words can change the checked draft/head after the first word becomes the title value.
   - Reject expansion-bearing unquoted words or evaluate a representation whose argument vector is identical to the executed one.

8. [P2] High — `home/dot_claude/hooks/executable_gh-merge-gate.sh:54` — Prose mentioning an exact gh invocation still triggers the hook, despite the false-positive fix claim.
   - `git commit -m 'docs: explain gh pr merge 7'` and a cat heredoc containing those words returned ask (`prose`, `heredoc-prose`). No gh command is invoked. The new tests at `tests/unit/test_gh_merge_gate.py:92` omit the word gh from their prose examples, so they miss this regression.

9. [P2] High — `scripts/validate-agent-assets.py:370` — The validator only protects seven retained ask rules, so it accepts removal of other write prompts it claims to preserve.
   - A settings object with precisely GH_WRITE_ASK and the correct gate, but no DELETE, PATCH, --method or field-based API ask rules, was accepted (`validator-missing-DELETE`). The current manifest still retains those rules at `home/dot_agents/agent-config.yaml:232` onward; the full generator expected-list test limits this regression, but the new validator test derives its rules from the incomplete constant and does not exercise each removal.
   - Check the complete retained write-rule set and each removal independently.

10. [P2] High — `scripts/validate-agent-assets.py:394` — A filename suffix is accepted as proof that a synchronous executable gate is wired.
    - Both `echo /gh-merge-gate.sh` and an async command-hook entry passed (`validator-echo-gate`, `validator-async-gate`), although neither provides a synchronous PreToolUse decision. The check ignores hook type, execution shape and async behavior. Require the exact intended synchronous invocation.

## Evidence for the ten requested stop conditions

The common commands were `git diff "$(git merge-base origin/main HEAD)" HEAD -- <named paths>`, `nl -ba <named path>`, and the recorded dry-probe invocation below. Every line reference is in the clean assigned-head checkout. The review was interrupted by the head change; unverified cases are explicit rather than inferred passing.

1. **Merge allow conditions.** Shape/flag restrictions are at hook lines 54–56, 153–183; primary-worktree test at 59–66; OPEN/non-draft/full head/default-base comparisons at 188–194; branch requirements and check-runs/status union at 196–206; acceptance at 70–80/208; audit pathname at 209–210. Commands: line-numbered hook read, three-suite unittest command, dry probes. Existing/dry negatives include --admin/unpinned/short head; linked worktree; wrong state/isDraft/head/base; empty rules; absent required check; missing record; missing audit, all ask. The record/audit/canonical-repository conditions are not closed (findings 4–6). Contexts are queried on the pinned SHA and check-runs are paginated; required integration IDs are discarded at line 197 and the combined-status endpoint is not paginated. App-provenance/duplicate-context behavior was not dynamically assessed before the head moved.

2. **Failure behavior and colour.** Explicit gh/rules command failures, malformed/coloured PR JSON, missing required rules/checks/files, and a failing create parser produced ask in dry probes. The original colour-forcing unit test passed. The hook sets NO_COLOR=1, CLICOLOR=0, CLICOLOR_FORCE=0 and unsets GH_FORCE_TTY at 47–48; `gh help environment` confirms those controls. The hook has neither errexit nor pipefail; ERR handling is at 40 and the detector's protected failure at 55 escapes it. Invalid JSON and detector failure are proven exceptions (findings 2–3); runtime crashes/timeouts were not executed live. Empty default branch on a stack also allowed. Documentation was needed because gh cannot describe Claude's hook failure semantics.

3. **Create rules.** shlex/punctuation handling at 85–105, whitelist at 106–123, explicit branch/repo grammar at 124–133, default/open-parent test at 134–136, draft exit at 138, main-only ready path at 139, boundary comparison at 140–145, accepted-tip path at 147–148. Existing unit negatives cover missing base/head, other base, unpushed/default head, reviewer/web flags, substitution, operators and unterminated quotes; ready-revise and non-repository cases also ask. Dry `records-outside`, `records-empty`, `records-too-large`, `create-bad-parser-output` ask; `records-ok` allows. `records-count-only` incorrectly allows an output count with no filenames. Draft stacking onto an open unaccepted parent is intentionally allowed; a ready stack with an accepted tip also allows without accepting the parent. Globbing changes the real arguments (finding 7). No live PR creation was attempted.

4. **Actual invocation versus prose/API/wrappers.** Detector at 54, early silent exit at 55, canonical words at 157–160. Dry env prefix, command prefix, absolute gh path, repo-first form and API PUT merge path in both flag orders all ask. Quoted/concatenated gh words and alias form receive no decision; actual prose receives ask (findings 1/8). Aliases were examined as dry text only; no user aliases were read or written. The API path pattern does not depend on method flag position.

5. **Settings/rendering.** The exact diff removes **three** ask rules (merge, update-branch, create), not just the two named in the earlier PR prose. No other current allow/ask/deny rule changes. Generator 438–450 renders the new command in the Bash PreToolUse group; template 149–160 matches; manifest names it at 328. Generate-suite expected-list deletions at 696 onward remove those same three expectations without adding a negative test for bypass forms. Connected `modify_private_settings.json:181` replaces permissions, so obsolete asks do not remain; hook-list merge at 149–151 retains the old enforce-uv group and appends the new group on upgrades, potentially running enforce-uv twice. No policy failure was attributed to that minor duplication. `make render-check` passed.

6. **Validator additions.** Function at 376–395 is called by settings validation at 423. It rejects missing required seven-rule entries, preapproval of strings beginning Bash(gh pr or Bash(gh api, and absent gate suffix when any gated ask is removed. New unit test at 1169–1191 covers a correct gate, all three asks retained, missing hook, one missing rule, one preapproval. It does not remove every retained rule or test a fake/async hook; dry probes confirm findings 9–10. Permission alias/path/global preapproval forms were not fully exercised before interruption.

7. **Git transport.** The named diff removes only the two `[url "git@github.com:"]` / pushInsteadOf lines. Source `home/dot_config/git/config.tmpl:23` retains `helper = !gh auth git-credential`; signing and other config remain. Fetch remotes are not rewritten by this change. HTTPS-configured remotes now push over HTTPS via the existing gh helper from every seat; an already-SSH remote remains SSH. No credentials were read and no push was run. Validator at 1318 onward checks absence of pushInsteadOf and the helper; no live authentication test.

8. **Runtime seven lines.** `scripts/check-agent-runtime.py:820` adds the new source/deployed-hook pair to `check_executable_hook`. The helper at 322–330 checks text equality and owner executable mode. An installation where make update deployed the matching executable passes this check; a missing/stale/non-executable new hook makes doctor fail intentionally, including an unupdated checkout. No healthy/converged-machine false failure was identified. Doctor was not run because it inspects live runtime state outside this read-only review task.

9. **Threat reading.** A normal linked-worker record is rejected by 64–66 (existing linked-worktree test). A separate primary repository, a different --repo with the same SHA, body-only/wrong-task acceptance, symlinked evidence parent and audit directory are allowed (findings 4–6). A sha different from the requested PR's actual head asks at 193 (`wrong-headRefOid`); the server-side --match-head-commit additionally prevents a subsequently moved head from merging. Unaccepted stack parents are allowed at 134–138; this is explicit draft behavior, and ready acceptance checks only the tip at 147. A stack still cannot merge through this hook until its base equals the default branch (194). Existence of an audit pathname is not proof of an acceptable audit. The supplied review task has no threat table, and no threat-table file is among this PR's ten changed paths; a complete owner-task metadata audit was not finished before the head moved.

10. **Tests and omissions.** The new test file has 10 methods and covers the ordinary allow, colour, update-branch, listed invalid command forms, state/head/base/check/file failures, linked worktree, pushed draft and ready/boundary creates. Missing negative cases include quoted executable/subcommand concatenation, aliases, exact gh prose, JSON-control characters, detector/utility crash, empty input/default fields, canonical repo identity, --repo evidence binding, front-matter parsing/task binding, symlinked parents, non-file/invalid audit content, expansion-bearing create values, missing isDraft test in the original suite, each retained ask rule, fake/async gate, remote app provenance, and create tip races. Dry probes cover many of these omissions; remaining cases are unverified. The initial 197-test run failed one non-repository assertion because task-contained TMPDIR had an enclosing worktree. Adding GIT_CEILING_DIRECTORIES at the task boundary isolated discovery; the same required 197 tests then passed in 28.267 seconds. No tracked test was edited. Shellcheck and render-check both exited 0.

## Independent review and limits

Crit status reported no existing review file and no active session; no Crit browser/server was opened. The AGENTS-required independent subagent reviewed the settings/validator/runtime/transport connections at this exact head without mutations, and independently reported the JSON, prose, incomplete-rule and fake-hook findings. Its saved process evidence distinguishes completed review delivery from unresolved code findings. No finding is marked fixed or approved.

No live sandbox, gh write, push, merge, approval, credential read, local Bats, full suite, complete GitHub feedback sweep, or new-head review was performed. All original/source tracked files remained clean at the head-change checkpoint. The required integration gate was not run: this is a read-only review with no tracked diff, and integration belongs to the orchestrator. Cost: n/a.

## Task amendment and delivery

Amendment 1 was subsequently received through inbox: allowed_files is restricted to this evidence directory; the task was reread in full and copied byte-identically as task.md. Current task SHA256 is 4e61ab4beafdf7e80225c0a5ba35c3235bafe7a7ea0ae2255f9108d5e78c32ef. No reviewed-head or review-scope change was authorized. The existing PR-head mismatch therefore remains blocked. PONG message 2051 was sent once; agmsg-dispatch exited 1 with delivery failed or unread. Supported history lookup confirms the matching PONG is unread; no resend or read claim.

## Verbatim validation outputs

The following section is populated from the preserved command logs. Exit statuses are recorded with each invocation. The final verdict concerns only the assigned snapshot and does not certify review completion for the moved PR.

Completion UTC: 2026-10-17T23:36:03.188512+00:00

Environment for required checks: PYTHONDONTWRITEBYTECODE=1, GIT_CONFIG_GLOBAL=/dev/null, GIT_CONFIG_NOSYSTEM=1, GIT_TERMINAL_PROMPT=0; TMPDIR=<task>/tmp; UV_CACHE_DIR=<task>/cache/uv; XDG_CACHE_HOME=<task>/cache; UV_PYTHON_INSTALL_DIR=<task>/cache/uv-python; UV_PYTHON_DOWNLOADS=never. The isolated rerun and dry probes additionally use GIT_CEILING_DIRECTORIES=<task>. Later commands set MISE_STATE_DIR and MISE_CACHE_DIR under <task>/cache/mise. Working directory: <task>/source at the assigned detached head.

### Initial required unit command, environment issue retained

Command: `uv run python -m unittest tests/unit/test_gh_merge_gate.py tests/unit/test_validate_agent_assets.py tests/unit/test_generate_agent_configs.py -v`

Exit: `1`

```text
mise WARN  tracking config: failed to ln -sf ~/Workspace/dotfiles/.claude/worktrees/worker-e/.orchestration/dotfiles-T131-claude-pinned-merge-gate-review-a01/source/mise.toml ~/.local/state/mise/tracked-configs/66fdde7a0d9576a1: Operation not permitted (os error 1)
test_a_colour_forcing_session_still_reads_plain_json (tests.unit.test_gh_merge_gate.GhMergeGateTest.test_a_colour_forcing_session_still_reads_plain_json) ... ok
test_bypass_and_unpinned_forms_ask (tests.unit.test_gh_merge_gate.GhMergeGateTest.test_bypass_and_unpinned_forms_ask) ... ok
test_create_draft_of_a_pushed_task_branch_is_allowed (tests.unit.test_gh_merge_gate.GhMergeGateTest.test_create_draft_of_a_pushed_task_branch_is_allowed) ... ok
test_create_other_forms_ask (tests.unit.test_gh_merge_gate.GhMergeGateTest.test_create_other_forms_ask) ... ok
test_create_ready_needs_acceptance_or_records_only (tests.unit.test_gh_merge_gate.GhMergeGateTest.test_create_ready_needs_acceptance_or_records_only) ... FAIL
test_head_base_checks_and_acceptance_are_enforced (tests.unit.test_gh_merge_gate.GhMergeGateTest.test_head_base_checks_and_acceptance_are_enforced) ... ok
test_linked_worktree_asks (tests.unit.test_gh_merge_gate.GhMergeGateTest.test_linked_worktree_asks) ... ok
test_pinned_accepted_green_head_is_allowed (tests.unit.test_gh_merge_gate.GhMergeGateTest.test_pinned_accepted_green_head_is_allowed) ... ok
test_unrelated_commands_get_no_decision (tests.unit.test_gh_merge_gate.GhMergeGateTest.test_unrelated_commands_get_no_decision) ... ok
test_update_branch_is_allowed (tests.unit.test_gh_merge_gate.GhMergeGateTest.test_update_branch_is_allowed) ... ok
test_a_masked_key_collision_fails_and_leaves_the_file_unchanged (tests.unit.test_validate_agent_assets.MaskSecretsModeTest.test_a_masked_key_collision_fails_and_leaves_the_file_unchanged) ... ok
test_keeps_carriage_returns_and_every_unmasked_byte (tests.unit.test_validate_agent_assets.MaskSecretsModeTest.test_keeps_carriage_returns_and_every_unmasked_byte) ... ok
test_leaves_allowed_placeholders_the_scan_accepts (tests.unit.test_validate_agent_assets.MaskSecretsModeTest.test_leaves_allowed_placeholders_the_scan_accepts) ... ok
test_masks_an_earlier_duplicate_member_so_the_scan_passes (tests.unit.test_validate_agent_assets.MaskSecretsModeTest.test_masks_an_earlier_duplicate_member_so_the_scan_passes) ... ok
test_masks_every_match_in_place_and_reports_counts (tests.unit.test_validate_agent_assets.MaskSecretsModeTest.test_masks_every_match_in_place_and_reports_counts) ... ok
test_masks_json_content_whatever_the_suffix (tests.unit.test_validate_agent_assets.MaskSecretsModeTest.test_masks_json_content_whatever_the_suffix) ... ok
test_masks_json_string_values_and_keeps_the_document_parseable (tests.unit.test_validate_agent_assets.MaskSecretsModeTest.test_masks_json_string_values_and_keeps_the_document_parseable) ... ok
test_missing_file_exits_2_without_touching_others (tests.unit.test_validate_agent_assets.MaskSecretsModeTest.test_missing_file_exits_2_without_touching_others) ... ok
test_normalises_home_paths_in_text_and_json_evidence (tests.unit.test_validate_agent_assets.MaskSecretsModeTest.test_normalises_home_paths_in_text_and_json_evidence) ... ok
test_a_key_after_json_escaped_whitespace_is_flagged (tests.unit.test_validate_agent_assets.SecretPatternBoundaryTest.test_a_key_after_json_escaped_whitespace_is_flagged) ... ok
test_a_key_prefix_inside_a_hyphenated_word_is_clean (tests.unit.test_validate_agent_assets.SecretPatternBoundaryTest.test_a_key_prefix_inside_a_hyphenated_word_is_clean) ... ok
test_a_long_hyphenated_run_scans_in_linear_time (tests.unit.test_validate_agent_assets.SecretPatternBoundaryTest.test_a_long_hyphenated_run_scans_in_linear_time) ... ok
test_a_real_key_prefix_is_still_flagged (tests.unit.test_validate_agent_assets.SecretPatternBoundaryTest.test_a_real_key_prefix_is_still_flagged) ... ok
test_an_sk_key_body_needs_a_hyphen_free_run (tests.unit.test_validate_agent_assets.SecretPatternBoundaryTest.test_an_sk_key_body_needs_a_hyphen_free_run) ... ok
test_masking_keeps_the_escape_before_the_key (tests.unit.test_validate_agent_assets.SecretPatternBoundaryTest.test_masking_keeps_the_escape_before_the_key) ... ok
test_a_one_segment_home_keeps_namespace_roots_intact (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_a_one_segment_home_keeps_namespace_roots_intact) ... ok
test_a_root_home_keeps_sub_agent_identifiers (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_a_root_home_keeps_sub_agent_identifiers) ... ok
test_agent_manifest_accepts_a_worker_worktree_under_claude_worktrees (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_accepts_a_worker_worktree_under_claude_worktrees) ... ok
test_agent_manifest_accepts_exact_security_profile_set (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_accepts_exact_security_profile_set) ... ok
test_agent_manifest_pins_the_audit_codex_profile (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_pins_the_audit_codex_profile) ... ok
test_agent_manifest_rejects_a_worker_worktree_outside_claude_worktrees (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_rejects_a_worker_worktree_outside_claude_worktrees) ... ok
test_agent_manifest_rejects_invalid_or_missing_orchestrator_kind (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_rejects_invalid_or_missing_orchestrator_kind) ... ok
test_agent_manifest_rejects_invalid_or_missing_worker_kind (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_rejects_invalid_or_missing_worker_kind) ... ok
test_agent_manifest_rejects_missing_audit_profile (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_rejects_missing_audit_profile) ... ok
test_agent_manifest_rejects_missing_security_profile (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_rejects_missing_security_profile) ... ok
test_agent_manifest_rejects_the_retired_adh_profile (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_rejects_the_retired_adh_profile) ... ok
test_agent_manifest_rejects_unknown_worker_profile (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_rejects_unknown_worker_profile) ... ok
test_agent_manifest_rejects_wrong_security_codex_model (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_rejects_wrong_security_codex_model) ... ok
test_agent_manifest_requires_fable_advisor_on_the_worker_profile (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_requires_fable_advisor_on_the_worker_profile) ... ok
test_agent_manifest_requires_readme_to_document_on_demand_seating (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_requires_readme_to_document_on_demand_seating) ... ok
test_agent_manifest_requires_readme_to_state_the_orchestrator_kind (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_requires_readme_to_state_the_orchestrator_kind) ... ok
test_agent_manifest_requires_readme_to_state_the_worker_kind (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_requires_readme_to_state_the_worker_kind) ... ok
test_agent_manifest_worker_kind_check_ignores_the_orchestrator_sentence (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_worker_kind_check_ignores_the_orchestrator_sentence) ... ok
test_agmsg_installer_requires_a_release_pin_and_its_tag (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agmsg_installer_requires_a_release_pin_and_its_tag) ... ok
test_agmsg_installer_requires_the_full_tag_commit (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agmsg_installer_requires_the_full_tag_commit) ... ok
test_agmsg_installer_requires_the_npm_bootstrap_integrity (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agmsg_installer_requires_the_npm_bootstrap_integrity) ... ok
test_agmsg_ownership_accepts_the_installer_layout (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agmsg_ownership_accepts_the_installer_layout) ... ok
test_agmsg_ownership_rejects_a_managed_claude_command (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agmsg_ownership_rejects_a_managed_claude_command) ... ok
test_agmsg_ownership_rejects_a_vendored_skill_copy (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agmsg_ownership_rejects_a_vendored_skill_copy) ... ok
test_agmsg_ownership_rejects_removing_installer_owned_paths (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agmsg_ownership_rejects_removing_installer_owned_paths) ... ok
test_agmsg_ownership_requires_retiring_the_symlink_farm (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agmsg_ownership_requires_retiring_the_symlink_farm) ... ok
test_assets_accept_complete_declarations_and_rendered_versions (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_assets_accept_complete_declarations_and_rendered_versions) ... ok
test_assets_accept_rolling_releases_without_pins (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_assets_accept_rolling_releases_without_pins) ... ok
test_assets_reject_a_malformed_render_entry (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_assets_reject_a_malformed_render_entry) ... ok
test_assets_reject_each_incomplete_declaration (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_assets_reject_each_incomplete_declaration) ... ok
test_assets_reject_invalid_rolling_and_pinned_declarations (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_assets_reject_invalid_rolling_and_pinned_declarations) ... ok
test_assets_reject_one_assignment_rendered_from_two_fields (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_assets_reject_one_assignment_rendered_from_two_fields) ... ok
test_assets_reject_one_assignment_rendered_through_a_symlink_alias (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_assets_reject_one_assignment_rendered_through_a_symlink_alias) ... ok
test_assets_reject_unrendered_literal_versions_anywhere_in_install_or_scripts (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_assets_reject_unrendered_literal_versions_anywhere_in_install_or_scripts) ... ok
test_assets_report_an_unrendered_declare_r_version (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_assets_report_an_unrendered_declare_r_version) ... ok
test_assets_scan_setup_sh_for_unrendered_versions (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_assets_scan_setup_sh_for_unrendered_versions) ... ok
test_claude_gh_merge_gate_keeps_writes_on_ask_and_requires_the_hook (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_gh_merge_gate_keeps_writes_on_ask_and_requires_the_hook) ... ok
test_claude_mcp_config_accepts_an_empty_map_and_rejects_a_non_mapping (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_mcp_config_accepts_an_empty_map_and_rejects_a_non_mapping) ... ok
test_claude_permissions_allow_must_list_non_empty_rules (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_permissions_allow_must_list_non_empty_rules) ... ok
test_claude_sandbox_accepts_manifest_symmetric_settings (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_sandbox_accepts_manifest_symmetric_settings) ... ok
test_claude_sandbox_extra_allow_write_must_be_absolute_or_home_paths_without_globs (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_sandbox_extra_allow_write_must_be_absolute_or_home_paths_without_globs) ... ok
test_claude_sandbox_rejects_each_broken_rule (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_sandbox_rejects_each_broken_rule) ... ok
test_claude_sandbox_requires_extra_codex_writable_roots (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_sandbox_requires_extra_codex_writable_roots) ... ok
test_claude_sandbox_unix_sockets_must_be_absolute_or_home_paths_without_globs (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_sandbox_unix_sockets_must_be_absolute_or_home_paths_without_globs) ... ok
test_claude_sandbox_validator_refuses_each_forbidden_form (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_sandbox_validator_refuses_each_forbidden_form) ... ok
test_codex_command_hooks_accept_the_declared_tables (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_codex_command_hooks_accept_the_declared_tables) ... ok
test_codex_command_hooks_reject_bad_entries_and_stray_tables (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_codex_command_hooks_reject_bad_entries_and_stray_tables) ... ok
test_codex_modify_script_requires_executable_source (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_codex_modify_script_requires_executable_source) ... ok
test_codex_projects_accept_working_tree_placeholder (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_codex_projects_accept_working_tree_placeholder) ... ok
test_codex_projects_reject_hard_coded_macos_home (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_codex_projects_reject_hard_coded_macos_home) ... ok
test_codex_projects_reject_missing_working_tree_placeholder (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_codex_projects_reject_missing_working_tree_placeholder) ... ok
test_codex_sandbox_workspace_write_accepts_matching_manifest (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_codex_sandbox_workspace_write_accepts_matching_manifest) ... ok
test_codex_sandbox_workspace_write_must_match_manifest (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_codex_sandbox_workspace_write_must_match_manifest) ... ok
test_codex_sandbox_workspace_write_requires_all_agmsg_roots (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_codex_sandbox_workspace_write_requires_all_agmsg_roots) ... ok
test_compactiondb_project_copy_must_match_the_vendor_tree (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_compactiondb_project_copy_must_match_the_vendor_tree) ... ok
test_home_paths_normalise_to_tilde_and_repository_paths_stay (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_home_paths_normalise_to_tilde_and_repository_paths_stay) ... ok
test_hook_composition_accepts_managed_source_fixture (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_hook_composition_accepts_managed_source_fixture) ... ok
test_hook_composition_pins_sessionstart_order (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_hook_composition_pins_sessionstart_order) ... ok
test_hook_composition_rejects_duplicate_command (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_hook_composition_rejects_duplicate_command) ... ok
test_hook_composition_rejects_sync_timeout_over_budget (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_hook_composition_rejects_sync_timeout_over_budget) ... ok
test_hook_composition_requires_permgate_first (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_hook_composition_requires_permgate_first) ... ok
test_manifest_home_paths_allow_chezmoi_home_dir (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_manifest_home_paths_allow_chezmoi_home_dir) ... ok
test_manifest_home_paths_allow_flow_style_projects (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_manifest_home_paths_allow_flow_style_projects) ... ok
test_manifest_home_paths_exempt_runtime_owned_projects (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_manifest_home_paths_exempt_runtime_owned_projects) ... ok
test_manifest_home_paths_only_exempt_the_projects_subtree (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_manifest_home_paths_only_exempt_the_projects_subtree) ... ok
test_manifest_home_paths_reject_hard_coded_home (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_manifest_home_paths_reject_hard_coded_home) ... ok
test_manifest_home_paths_reject_hard_coded_linux_home (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_manifest_home_paths_reject_hard_coded_linux_home) ... ok
test_manifest_home_paths_reject_non_codex_projects_mapping (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_manifest_home_paths_reject_non_codex_projects_mapping) ... ok
test_permgate_policy_requires_a_schema_3_object (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_permgate_policy_requires_a_schema_3_object) ... ok
test_recursive_scans_skip_gitignored_local_state (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_recursive_scans_skip_gitignored_local_state) ... ok
test_recursive_scans_skip_nested_git_trees_only (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_recursive_scans_skip_nested_git_trees_only) ... ok
test_repo_claude_settings_accept_portable_interpreter (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_repo_claude_settings_accept_portable_interpreter) ... ok
test_repo_claude_settings_reject_machine_specific_interpreter (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_repo_claude_settings_reject_machine_specific_interpreter) ... ERROR: ~/Workspace/dotfiles/.claude/worktrees/worker-e/.orchestration/dotfiles-T131-claude-pinned-merge-gate-review-a01/tmp/validate-agent-assets-test-pc7vwq69/.claude/settings.json hook SessionEnd must not hard-code a machine-specific home path: ~/.local/share/mise/installs/python/3.14.7/bin/python3.14
ok
test_runner_homes_match_anywhere (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_runner_homes_match_anywhere) ... ok
test_secret_scan_allows_exact_placeholder_tokens (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_allows_exact_placeholder_tokens) ... ok
test_secret_scan_checks_docs_paths (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_checks_docs_paths) ... ok
test_secret_scan_checks_extensionless_executables (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_checks_extensionless_executables) ... ok
test_secret_scan_checks_utf16_bom_text (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_checks_utf16_bom_text) ... ok
test_secret_scan_fails_a_nul_in_orchestration_text_and_skips_other_binaries (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_fails_a_nul_in_orchestration_text_and_skips_other_binaries) ... ok
test_secret_scan_flags_the_running_users_home_as_a_backstop (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_flags_the_running_users_home_as_a_backstop) ... ok
test_secret_scan_reads_json_per_key_and_string_value (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_reads_json_per_key_and_string_value) ... ok
test_secret_scan_rejects_home_paths_in_orchestration_evidence_only (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_rejects_home_paths_in_orchestration_evidence_only) ... ok
test_secret_scan_rejects_placeholder_with_suffix (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_rejects_placeholder_with_suffix) ... ok
test_secret_scan_rejects_utf16_orchestration_text_with_the_nul_offset (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_rejects_utf16_orchestration_text_with_the_nul_offset) ... ok
test_a_declare_r_assignment_must_appear_exactly_once (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_a_declare_r_assignment_must_appear_exactly_once) ... ok
test_a_list_render_writes_one_pin_into_several_files_and_declare_r (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_a_list_render_writes_one_pin_into_several_files_and_declare_r) ... ok
test_absent_worker_profile_renders_no_env_line (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_absent_worker_profile_renders_no_env_line) ... ok
test_absent_worker_worktree_renders_no_env_line (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_absent_worker_worktree_renders_no_env_line) ... ok
test_active_plugin_version_matches_codex_on_symlinks_and_invalid_semver (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_active_plugin_version_matches_codex_on_symlinks_and_invalid_semver) ... ok
test_an_empty_mcp_server_map_renders_no_tables_and_an_empty_claude_map (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_an_empty_mcp_server_map_renders_no_tables_and_an_empty_claude_map) ... ok
test_asset_constant_must_be_assigned_exactly_once (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_asset_constant_must_be_assigned_exactly_once) ... ok
test_asset_constants_render_into_their_files (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_asset_constants_render_into_their_files) ... ok
test_asset_pin_must_be_a_plain_value (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_asset_pin_must_be_a_plain_value) ... ok
test_audit_profile_renders_read_only_sandbox_override (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_audit_profile_renders_read_only_sandbox_override) ... ok
test_bootstrap_pins_render_into_setup_and_their_installers (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_bootstrap_pins_render_into_setup_and_their_installers) ... ok
test_check_reports_asset_render_drift (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_check_reports_asset_render_drift) ... ok
test_claude_deny_rules_use_edit_for_file_mutations (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_claude_deny_rules_use_edit_for_file_mutations) ... ok
test_claude_sandbox_renders_optional_socket_and_extra_write_keys (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_claude_sandbox_renders_optional_socket_and_extra_write_keys) ... ok
test_claude_sandbox_renders_per_os_from_the_manifest (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_claude_sandbox_renders_per_os_from_the_manifest) ... ok
test_claude_settings_render_interactive_advisor_only_when_set (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_claude_settings_render_interactive_advisor_only_when_set) ... ok
test_claude_settings_render_the_format_hook_from_its_path (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_claude_settings_render_the_format_hook_from_its_path) ... ok
test_claude_settings_renders_session_start_hooks (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_claude_settings_renders_session_start_hooks) ... ok
test_claude_settings_use_interactive_profile_with_permgate (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_claude_settings_use_interactive_profile_with_permgate) ... ok
test_claude_skill_symlink_outputs_strip_executable_target_prefix (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_claude_skill_symlink_outputs_strip_executable_target_prefix) ... ok
test_codex_command_hooks_render_after_permission_request_in_manifest_order (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_codex_command_hooks_render_after_permission_request_in_manifest_order) ... ok
test_codex_config_renders_permgate_permission_request (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_codex_config_renders_permgate_permission_request) ... ok
test_codex_config_renders_working_tree_project_key (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_codex_config_renders_working_tree_project_key) ... ok
test_empty_or_missing_codex_command_hooks_render_no_table (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_empty_or_missing_codex_command_hooks_render_no_table) ... ok
test_entries_reaching_one_file_through_a_symlink_edit_one_snapshot (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_entries_reaching_one_file_through_a_symlink_edit_one_snapshot) ... ok
test_expected_outputs_uses_codex_baseline_path (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_expected_outputs_uses_codex_baseline_path) ... ok
test_hook_trust_hash_reproduces_codex_current_hashes (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_hook_trust_hash_reproduces_codex_current_hashes) ... ok
test_linux_sandbox_excludes_the_top_level_herdr_agents_invocation (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_linux_sandbox_excludes_the_top_level_herdr_agents_invocation) ... ok
test_managed_claude_sandbox_excludes_agmsg_dispatch (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_managed_claude_sandbox_excludes_agmsg_dispatch) ... ok
test_managed_codex_config_routes_compaction_and_session_end_to_compactiondb (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_managed_codex_config_routes_compaction_and_session_end_to_compactiondb) ... ok
test_managed_codex_path_includes_installed_common_bin (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_managed_codex_path_includes_installed_common_bin) ... ok
test_managed_hooks_use_installed_permgate_paths (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_managed_hooks_use_installed_permgate_paths) ... ok
test_manifest_keeps_model_ids_only_in_profiles (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_manifest_keeps_model_ids_only_in_profiles) ... ok
test_model_profiles_env_renders_claude_advisor_only_when_set (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_model_profiles_env_renders_claude_advisor_only_when_set) ... ok
test_model_profiles_env_renders_orchestrator_kind (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_model_profiles_env_renders_orchestrator_kind) ... ok
test_model_profiles_env_renders_worker_kind (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_model_profiles_env_renders_worker_kind) ... ok
test_model_profiles_env_renders_worker_profile (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_model_profiles_env_renders_worker_profile) ... ok
test_model_profiles_env_renders_worker_worktree (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_model_profiles_env_renders_worker_worktree) ... ok
test_model_profiles_env_selects_no_github_store (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_model_profiles_env_selects_no_github_store) ... ok
test_model_profiles_reject_incomplete_or_unsafe_entries (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_model_profiles_reject_incomplete_or_unsafe_entries) ... ERROR: model profile standard is missing codex
ERROR: model profile standard.claude.model must be a launcher-safe string
ERROR: model_profiles must define the express profile
ok
test_model_profiles_reject_invalid_sandbox_mode (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_model_profiles_reject_invalid_sandbox_mode) ... ok
test_model_profiles_reject_unsafe_advisor (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_model_profiles_reject_unsafe_advisor) ... ERROR: model profile standard.claude.advisor must be a launcher-safe string
ok
test_orchestrator_kind_defaults_to_claude (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_orchestrator_kind_defaults_to_claude) ... ok
test_plugin_versions_order_build_metadata_like_the_semver_crate (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_plugin_versions_order_build_metadata_like_the_semver_crate) ... ok
test_profile_modify_scripts_are_byte_idempotent_with_runtime_state (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_profile_modify_scripts_are_byte_idempotent_with_runtime_state) ... ok
test_profile_modify_scripts_are_quiet_for_matching_hook_trust (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_profile_modify_scripts_are_quiet_for_matching_hook_trust) ... ok
test_profile_modify_scripts_handle_table_headers_with_trailing_comments (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_profile_modify_scripts_handle_table_headers_with_trailing_comments) ... ok
test_profile_modify_scripts_hash_plugin_hooks_or_fall_back_to_the_pin (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_profile_modify_scripts_hash_plugin_hooks_or_fall_back_to_the_pin) ... ok
test_profile_modify_scripts_hash_the_plugin_version_codex_loads (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_profile_modify_scripts_hash_the_plugin_version_codex_loads) ... ok
test_profile_modify_scripts_keep_header_like_lines_inside_multiline_strings (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_profile_modify_scripts_keep_header_like_lines_inside_multiline_strings) ... ok
test_profile_modify_scripts_keep_the_current_content_when_the_merge_is_invalid (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_profile_modify_scripts_keep_the_current_content_when_the_merge_is_invalid) ... ok
test_profile_modify_scripts_preserve_repeated_runtime_tables (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_profile_modify_scripts_preserve_repeated_runtime_tables) ... ok
test_profile_modify_scripts_preserve_runtime_state (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_profile_modify_scripts_preserve_runtime_state) ... ok
test_profile_modify_scripts_replace_a_single_quoted_declared_entry (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_profile_modify_scripts_replace_a_single_quoted_declared_entry) ... ok
test_profile_modify_scripts_replace_declared_dotted_keys_under_hooks_and_at_the_root (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_profile_modify_scripts_replace_declared_dotted_keys_under_hooks_and_at_the_root) ... ok
test_profile_modify_scripts_replace_declared_hook_trust_and_keep_undeclared (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_profile_modify_scripts_replace_declared_hook_trust_and_keep_undeclared) ... ok
test_profile_modify_scripts_replace_inline_table_and_dotted_forms (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_profile_modify_scripts_replace_inline_table_and_dotted_forms) ... ok
test_profile_modify_scripts_seed_base_hook_trust (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_profile_modify_scripts_seed_base_hook_trust) ... ok
test_profile_modify_scripts_treat_equivalent_hook_state_spellings_as_one_table (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_profile_modify_scripts_treat_equivalent_hook_state_spellings_as_one_table) ... ok
test_profile_modify_scripts_warn_on_hook_trust_divergence (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_profile_modify_scripts_warn_on_hook_trust_divergence) ... ok
test_project_map_reload_hook_accepts_only_cdp_target_ids (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_project_map_reload_hook_accepts_only_cdp_target_ids) ... ok
test_project_map_reload_hook_acts_only_on_the_map_and_never_fails (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_project_map_reload_hook_acts_only_on_the_map_and_never_fails) ... ok
test_project_map_reload_hook_compares_canonical_paths_for_every_path_form (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_project_map_reload_hook_compares_canonical_paths_for_every_path_form) ... ok
test_project_map_reload_hook_guards_against_a_tab_navigating_away (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_project_map_reload_hook_guards_against_a_tab_navigating_away) ... ok
test_project_map_reload_hook_matches_percent_encoded_tilde (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_project_map_reload_hook_matches_percent_encoded_tilde) ... ok
test_project_map_reload_hook_opens_event_map_when_only_another_repository_is_open (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_project_map_reload_hook_opens_event_map_when_only_another_repository_is_open) ... ok
test_project_map_reload_hook_opens_the_pane_when_no_browser_shows_the_map (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_project_map_reload_hook_opens_the_pane_when_no_browser_shows_the_map) ... ok
test_project_map_reload_hook_pins_the_bound_tab_when_it_closes (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_project_map_reload_hook_pins_the_bound_tab_when_it_closes) ... ok
test_project_map_reload_hook_rejects_percent_encoded_path_separators (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_project_map_reload_hook_rejects_percent_encoded_path_separators) ... ok
test_project_map_reload_hook_renders_into_post_tool_use (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_project_map_reload_hook_renders_into_post_tool_use) ... ok
test_project_map_reload_hook_resolves_relative_paths_from_physical_cwd (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_project_map_reload_hook_resolves_relative_paths_from_physical_cwd) ... ok
test_project_map_reload_hook_selects_the_event_map_among_two_repositories (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_project_map_reload_hook_selects_the_event_map_among_two_repositories) ... ok
test_repository_marketplace_is_a_runtime_owned_seed (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_repository_marketplace_is_a_runtime_owned_seed) ... ok
test_security_profile_renders_launcher_and_expanded_notify (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_security_profile_renders_launcher_and_expanded_notify) ... ok
test_set_asset_field_reaches_the_fallback_pin_and_its_checksums (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_set_asset_field_reaches_the_fallback_pin_and_its_checksums) ... ok
test_set_asset_field_rejects_unknown_targets_and_unsafe_values (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_set_asset_field_rejects_unknown_targets_and_unsafe_values) ... ok
test_set_asset_field_rewrites_only_the_named_scalar (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_set_asset_field_rewrites_only_the_named_scalar) ... ok
test_set_asset_leaves_files_untouched_when_an_assignment_is_invalid (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_set_asset_leaves_files_untouched_when_an_assignment_is_invalid) ... ok
test_set_asset_refuses_fields_other_than_pins_and_checksums (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_set_asset_refuses_fields_other_than_pins_and_checksums) ... ok
test_set_asset_rejects_a_value_that_does_not_parse_back_as_a_string (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_set_asset_rejects_a_value_that_does_not_parse_back_as_a_string) ... ok
test_set_asset_reports_an_unparsable_manifest_without_a_traceback (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_set_asset_reports_an_unparsable_manifest_without_a_traceback) ... ok
test_set_asset_updates_the_manifest_and_renders_its_pins (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_set_asset_updates_the_manifest_and_renders_its_pins) ... ok
test_unknown_interactive_profile_fails (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_unknown_interactive_profile_fails) ... ERROR: interactive_profile must name a model profile: 'missing'
ok
test_unknown_orchestrator_kind_fails (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_unknown_orchestrator_kind_fails) ... ok
test_unknown_worker_kind_fails (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_unknown_worker_kind_fails) ... ERROR: worker_kind must be one of ('codex', 'claude'): 'banana'
ok
test_unknown_worker_profile_fails (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_unknown_worker_profile_fails) ... ERROR: worker_profile must name a model profile: 'missing'
ok
test_worker_kind_defaults_to_codex (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_worker_kind_defaults_to_codex) ... ok
test_worker_worktree_outside_claude_worktrees_fails (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_worker_worktree_outside_claude_worktrees_fails) ... ERROR: worker_worktree must be a relative path under .claude/worktrees/: 'worker-c'
ERROR: worker_worktree must be a relative path under .claude/worktrees/: '/abs/.claude/worktrees/x'
ERROR: worker_worktree must be a relative path under .claude/worktrees/: '.claude/worktrees/..'
ERROR: worker_worktree must be a relative path under .claude/worktrees/: '.claude/worktrees/a/b'
ERROR: worker_worktree must be a relative path under .claude/worktrees/: '.claude/worktrees/$(x)'
ok

======================================================================
FAIL: test_create_ready_needs_acceptance_or_records_only (tests.unit.test_gh_merge_gate.GhMergeGateTest.test_create_ready_needs_acceptance_or_records_only)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "~/Workspace/dotfiles/.claude/worktrees/worker-e/.orchestration/dotfiles-T131-claude-pinned-merge-gate-review-a01/source/tests/unit/test_gh_merge_gate.py", line 194, in test_create_ready_needs_acceptance_or_records_only
    self.assertIn("not in a git checkout", self.decide(ready, cwd=self.tmp)[1])
    ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 'not in a git checkout' not found in 'gh-merge-gate: a ready PR only from the main checkout_ not a linked worktree'

----------------------------------------------------------------------
Ran 197 tests in 26.443s

FAILED (failures=1)
```

### Required unit command after discovery isolation

Command: `uv run python -m unittest tests/unit/test_gh_merge_gate.py tests/unit/test_validate_agent_assets.py tests/unit/test_generate_agent_configs.py -v`

Exit: `0`

```text
mise WARN  tracking config: failed to ln -sf ~/Workspace/dotfiles/.claude/worktrees/worker-e/.orchestration/dotfiles-T131-claude-pinned-merge-gate-review-a01/source/mise.toml ~/.local/state/mise/tracked-configs/66fdde7a0d9576a1: Operation not permitted (os error 1)
test_a_colour_forcing_session_still_reads_plain_json (tests.unit.test_gh_merge_gate.GhMergeGateTest.test_a_colour_forcing_session_still_reads_plain_json) ... ok
test_bypass_and_unpinned_forms_ask (tests.unit.test_gh_merge_gate.GhMergeGateTest.test_bypass_and_unpinned_forms_ask) ... ok
test_create_draft_of_a_pushed_task_branch_is_allowed (tests.unit.test_gh_merge_gate.GhMergeGateTest.test_create_draft_of_a_pushed_task_branch_is_allowed) ... ok
test_create_other_forms_ask (tests.unit.test_gh_merge_gate.GhMergeGateTest.test_create_other_forms_ask) ... ok
test_create_ready_needs_acceptance_or_records_only (tests.unit.test_gh_merge_gate.GhMergeGateTest.test_create_ready_needs_acceptance_or_records_only) ... ok
test_head_base_checks_and_acceptance_are_enforced (tests.unit.test_gh_merge_gate.GhMergeGateTest.test_head_base_checks_and_acceptance_are_enforced) ... ok
test_linked_worktree_asks (tests.unit.test_gh_merge_gate.GhMergeGateTest.test_linked_worktree_asks) ... ok
test_pinned_accepted_green_head_is_allowed (tests.unit.test_gh_merge_gate.GhMergeGateTest.test_pinned_accepted_green_head_is_allowed) ... ok
test_unrelated_commands_get_no_decision (tests.unit.test_gh_merge_gate.GhMergeGateTest.test_unrelated_commands_get_no_decision) ... ok
test_update_branch_is_allowed (tests.unit.test_gh_merge_gate.GhMergeGateTest.test_update_branch_is_allowed) ... ok
test_a_masked_key_collision_fails_and_leaves_the_file_unchanged (tests.unit.test_validate_agent_assets.MaskSecretsModeTest.test_a_masked_key_collision_fails_and_leaves_the_file_unchanged) ... ok
test_keeps_carriage_returns_and_every_unmasked_byte (tests.unit.test_validate_agent_assets.MaskSecretsModeTest.test_keeps_carriage_returns_and_every_unmasked_byte) ... ok
test_leaves_allowed_placeholders_the_scan_accepts (tests.unit.test_validate_agent_assets.MaskSecretsModeTest.test_leaves_allowed_placeholders_the_scan_accepts) ... ok
test_masks_an_earlier_duplicate_member_so_the_scan_passes (tests.unit.test_validate_agent_assets.MaskSecretsModeTest.test_masks_an_earlier_duplicate_member_so_the_scan_passes) ... ok
test_masks_every_match_in_place_and_reports_counts (tests.unit.test_validate_agent_assets.MaskSecretsModeTest.test_masks_every_match_in_place_and_reports_counts) ... ok
test_masks_json_content_whatever_the_suffix (tests.unit.test_validate_agent_assets.MaskSecretsModeTest.test_masks_json_content_whatever_the_suffix) ... ok
test_masks_json_string_values_and_keeps_the_document_parseable (tests.unit.test_validate_agent_assets.MaskSecretsModeTest.test_masks_json_string_values_and_keeps_the_document_parseable) ... ok
test_missing_file_exits_2_without_touching_others (tests.unit.test_validate_agent_assets.MaskSecretsModeTest.test_missing_file_exits_2_without_touching_others) ... ok
test_normalises_home_paths_in_text_and_json_evidence (tests.unit.test_validate_agent_assets.MaskSecretsModeTest.test_normalises_home_paths_in_text_and_json_evidence) ... ok
test_a_key_after_json_escaped_whitespace_is_flagged (tests.unit.test_validate_agent_assets.SecretPatternBoundaryTest.test_a_key_after_json_escaped_whitespace_is_flagged) ... ok
test_a_key_prefix_inside_a_hyphenated_word_is_clean (tests.unit.test_validate_agent_assets.SecretPatternBoundaryTest.test_a_key_prefix_inside_a_hyphenated_word_is_clean) ... ok
test_a_long_hyphenated_run_scans_in_linear_time (tests.unit.test_validate_agent_assets.SecretPatternBoundaryTest.test_a_long_hyphenated_run_scans_in_linear_time) ... ok
test_a_real_key_prefix_is_still_flagged (tests.unit.test_validate_agent_assets.SecretPatternBoundaryTest.test_a_real_key_prefix_is_still_flagged) ... ok
test_an_sk_key_body_needs_a_hyphen_free_run (tests.unit.test_validate_agent_assets.SecretPatternBoundaryTest.test_an_sk_key_body_needs_a_hyphen_free_run) ... ok
test_masking_keeps_the_escape_before_the_key (tests.unit.test_validate_agent_assets.SecretPatternBoundaryTest.test_masking_keeps_the_escape_before_the_key) ... ok
test_a_one_segment_home_keeps_namespace_roots_intact (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_a_one_segment_home_keeps_namespace_roots_intact) ... ok
test_a_root_home_keeps_sub_agent_identifiers (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_a_root_home_keeps_sub_agent_identifiers) ... ok
test_agent_manifest_accepts_a_worker_worktree_under_claude_worktrees (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_accepts_a_worker_worktree_under_claude_worktrees) ... ok
test_agent_manifest_accepts_exact_security_profile_set (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_accepts_exact_security_profile_set) ... ok
test_agent_manifest_pins_the_audit_codex_profile (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_pins_the_audit_codex_profile) ... ok
test_agent_manifest_rejects_a_worker_worktree_outside_claude_worktrees (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_rejects_a_worker_worktree_outside_claude_worktrees) ... ok
test_agent_manifest_rejects_invalid_or_missing_orchestrator_kind (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_rejects_invalid_or_missing_orchestrator_kind) ... ok
test_agent_manifest_rejects_invalid_or_missing_worker_kind (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_rejects_invalid_or_missing_worker_kind) ... ok
test_agent_manifest_rejects_missing_audit_profile (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_rejects_missing_audit_profile) ... ok
test_agent_manifest_rejects_missing_security_profile (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_rejects_missing_security_profile) ... ok
test_agent_manifest_rejects_the_retired_adh_profile (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_rejects_the_retired_adh_profile) ... ok
test_agent_manifest_rejects_unknown_worker_profile (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_rejects_unknown_worker_profile) ... ok
test_agent_manifest_rejects_wrong_security_codex_model (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_rejects_wrong_security_codex_model) ... ok
test_agent_manifest_requires_fable_advisor_on_the_worker_profile (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_requires_fable_advisor_on_the_worker_profile) ... ok
test_agent_manifest_requires_readme_to_document_on_demand_seating (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_requires_readme_to_document_on_demand_seating) ... ok
test_agent_manifest_requires_readme_to_state_the_orchestrator_kind (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_requires_readme_to_state_the_orchestrator_kind) ... ok
test_agent_manifest_requires_readme_to_state_the_worker_kind (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_requires_readme_to_state_the_worker_kind) ... ok
test_agent_manifest_worker_kind_check_ignores_the_orchestrator_sentence (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agent_manifest_worker_kind_check_ignores_the_orchestrator_sentence) ... ok
test_agmsg_installer_requires_a_release_pin_and_its_tag (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agmsg_installer_requires_a_release_pin_and_its_tag) ... ok
test_agmsg_installer_requires_the_full_tag_commit (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agmsg_installer_requires_the_full_tag_commit) ... ok
test_agmsg_installer_requires_the_npm_bootstrap_integrity (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agmsg_installer_requires_the_npm_bootstrap_integrity) ... ok
test_agmsg_ownership_accepts_the_installer_layout (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agmsg_ownership_accepts_the_installer_layout) ... ok
test_agmsg_ownership_rejects_a_managed_claude_command (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agmsg_ownership_rejects_a_managed_claude_command) ... ok
test_agmsg_ownership_rejects_a_vendored_skill_copy (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agmsg_ownership_rejects_a_vendored_skill_copy) ... ok
test_agmsg_ownership_rejects_removing_installer_owned_paths (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agmsg_ownership_rejects_removing_installer_owned_paths) ... ok
test_agmsg_ownership_requires_retiring_the_symlink_farm (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_agmsg_ownership_requires_retiring_the_symlink_farm) ... ok
test_assets_accept_complete_declarations_and_rendered_versions (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_assets_accept_complete_declarations_and_rendered_versions) ... ok
test_assets_accept_rolling_releases_without_pins (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_assets_accept_rolling_releases_without_pins) ... ok
test_assets_reject_a_malformed_render_entry (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_assets_reject_a_malformed_render_entry) ... ok
test_assets_reject_each_incomplete_declaration (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_assets_reject_each_incomplete_declaration) ... ok
test_assets_reject_invalid_rolling_and_pinned_declarations (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_assets_reject_invalid_rolling_and_pinned_declarations) ... ok
test_assets_reject_one_assignment_rendered_from_two_fields (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_assets_reject_one_assignment_rendered_from_two_fields) ... ok
test_assets_reject_one_assignment_rendered_through_a_symlink_alias (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_assets_reject_one_assignment_rendered_through_a_symlink_alias) ... ok
test_assets_reject_unrendered_literal_versions_anywhere_in_install_or_scripts (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_assets_reject_unrendered_literal_versions_anywhere_in_install_or_scripts) ... ok
test_assets_report_an_unrendered_declare_r_version (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_assets_report_an_unrendered_declare_r_version) ... ok
test_assets_scan_setup_sh_for_unrendered_versions (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_assets_scan_setup_sh_for_unrendered_versions) ... ok
test_claude_gh_merge_gate_keeps_writes_on_ask_and_requires_the_hook (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_gh_merge_gate_keeps_writes_on_ask_and_requires_the_hook) ... ok
test_claude_mcp_config_accepts_an_empty_map_and_rejects_a_non_mapping (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_mcp_config_accepts_an_empty_map_and_rejects_a_non_mapping) ... ok
test_claude_permissions_allow_must_list_non_empty_rules (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_permissions_allow_must_list_non_empty_rules) ... ok
test_claude_sandbox_accepts_manifest_symmetric_settings (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_sandbox_accepts_manifest_symmetric_settings) ... ok
test_claude_sandbox_extra_allow_write_must_be_absolute_or_home_paths_without_globs (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_sandbox_extra_allow_write_must_be_absolute_or_home_paths_without_globs) ... ok
test_claude_sandbox_rejects_each_broken_rule (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_sandbox_rejects_each_broken_rule) ... ok
test_claude_sandbox_requires_extra_codex_writable_roots (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_sandbox_requires_extra_codex_writable_roots) ... ok
test_claude_sandbox_unix_sockets_must_be_absolute_or_home_paths_without_globs (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_sandbox_unix_sockets_must_be_absolute_or_home_paths_without_globs) ... ok
test_claude_sandbox_validator_refuses_each_forbidden_form (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_sandbox_validator_refuses_each_forbidden_form) ... ok
test_codex_command_hooks_accept_the_declared_tables (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_codex_command_hooks_accept_the_declared_tables) ... ok
test_codex_command_hooks_reject_bad_entries_and_stray_tables (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_codex_command_hooks_reject_bad_entries_and_stray_tables) ... ok
test_codex_modify_script_requires_executable_source (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_codex_modify_script_requires_executable_source) ... ok
test_codex_projects_accept_working_tree_placeholder (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_codex_projects_accept_working_tree_placeholder) ... ok
test_codex_projects_reject_hard_coded_macos_home (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_codex_projects_reject_hard_coded_macos_home) ... ok
test_codex_projects_reject_missing_working_tree_placeholder (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_codex_projects_reject_missing_working_tree_placeholder) ... ok
test_codex_sandbox_workspace_write_accepts_matching_manifest (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_codex_sandbox_workspace_write_accepts_matching_manifest) ... ok
test_codex_sandbox_workspace_write_must_match_manifest (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_codex_sandbox_workspace_write_must_match_manifest) ... ok
test_codex_sandbox_workspace_write_requires_all_agmsg_roots (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_codex_sandbox_workspace_write_requires_all_agmsg_roots) ... ok
test_compactiondb_project_copy_must_match_the_vendor_tree (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_compactiondb_project_copy_must_match_the_vendor_tree) ... ok
test_home_paths_normalise_to_tilde_and_repository_paths_stay (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_home_paths_normalise_to_tilde_and_repository_paths_stay) ... ok
test_hook_composition_accepts_managed_source_fixture (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_hook_composition_accepts_managed_source_fixture) ... ok
test_hook_composition_pins_sessionstart_order (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_hook_composition_pins_sessionstart_order) ... ok
test_hook_composition_rejects_duplicate_command (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_hook_composition_rejects_duplicate_command) ... ok
test_hook_composition_rejects_sync_timeout_over_budget (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_hook_composition_rejects_sync_timeout_over_budget) ... ok
test_hook_composition_requires_permgate_first (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_hook_composition_requires_permgate_first) ... ok
test_manifest_home_paths_allow_chezmoi_home_dir (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_manifest_home_paths_allow_chezmoi_home_dir) ... ok
test_manifest_home_paths_allow_flow_style_projects (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_manifest_home_paths_allow_flow_style_projects) ... ok
test_manifest_home_paths_exempt_runtime_owned_projects (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_manifest_home_paths_exempt_runtime_owned_projects) ... ok
test_manifest_home_paths_only_exempt_the_projects_subtree (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_manifest_home_paths_only_exempt_the_projects_subtree) ... ok
test_manifest_home_paths_reject_hard_coded_home (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_manifest_home_paths_reject_hard_coded_home) ... ok
test_manifest_home_paths_reject_hard_coded_linux_home (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_manifest_home_paths_reject_hard_coded_linux_home) ... ok
test_manifest_home_paths_reject_non_codex_projects_mapping (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_manifest_home_paths_reject_non_codex_projects_mapping) ... ok
test_permgate_policy_requires_a_schema_3_object (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_permgate_policy_requires_a_schema_3_object) ... ok
test_recursive_scans_skip_gitignored_local_state (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_recursive_scans_skip_gitignored_local_state) ... ok
test_recursive_scans_skip_nested_git_trees_only (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_recursive_scans_skip_nested_git_trees_only) ... ok
test_repo_claude_settings_accept_portable_interpreter (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_repo_claude_settings_accept_portable_interpreter) ... ok
test_repo_claude_settings_reject_machine_specific_interpreter (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_repo_claude_settings_reject_machine_specific_interpreter) ... ERROR: ~/Workspace/dotfiles/.claude/worktrees/worker-e/.orchestration/dotfiles-T131-claude-pinned-merge-gate-review-a01/tmp/validate-agent-assets-test-ze6xn1kd/.claude/settings.json hook SessionEnd must not hard-code a machine-specific home path: ~/.local/share/mise/installs/python/3.14.7/bin/python3.14
ok
test_runner_homes_match_anywhere (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_runner_homes_match_anywhere) ... ok
test_secret_scan_allows_exact_placeholder_tokens (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_allows_exact_placeholder_tokens) ... ok
test_secret_scan_checks_docs_paths (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_checks_docs_paths) ... ok
test_secret_scan_checks_extensionless_executables (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_checks_extensionless_executables) ... ok
test_secret_scan_checks_utf16_bom_text (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_checks_utf16_bom_text) ... ok
test_secret_scan_fails_a_nul_in_orchestration_text_and_skips_other_binaries (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_fails_a_nul_in_orchestration_text_and_skips_other_binaries) ... ok
test_secret_scan_flags_the_running_users_home_as_a_backstop (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_flags_the_running_users_home_as_a_backstop) ... ok
test_secret_scan_reads_json_per_key_and_string_value (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_reads_json_per_key_and_string_value) ... ok
test_secret_scan_rejects_home_paths_in_orchestration_evidence_only (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_rejects_home_paths_in_orchestration_evidence_only) ... ok
test_secret_scan_rejects_placeholder_with_suffix (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_rejects_placeholder_with_suffix) ... ok
test_secret_scan_rejects_utf16_orchestration_text_with_the_nul_offset (tests.unit.test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_rejects_utf16_orchestration_text_with_the_nul_offset) ... ok
test_a_declare_r_assignment_must_appear_exactly_once (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_a_declare_r_assignment_must_appear_exactly_once) ... ok
test_a_list_render_writes_one_pin_into_several_files_and_declare_r (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_a_list_render_writes_one_pin_into_several_files_and_declare_r) ... ok
test_absent_worker_profile_renders_no_env_line (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_absent_worker_profile_renders_no_env_line) ... ok
test_absent_worker_worktree_renders_no_env_line (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_absent_worker_worktree_renders_no_env_line) ... ok
test_active_plugin_version_matches_codex_on_symlinks_and_invalid_semver (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_active_plugin_version_matches_codex_on_symlinks_and_invalid_semver) ... ok
test_an_empty_mcp_server_map_renders_no_tables_and_an_empty_claude_map (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_an_empty_mcp_server_map_renders_no_tables_and_an_empty_claude_map) ... ok
test_asset_constant_must_be_assigned_exactly_once (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_asset_constant_must_be_assigned_exactly_once) ... ok
test_asset_constants_render_into_their_files (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_asset_constants_render_into_their_files) ... ok
test_asset_pin_must_be_a_plain_value (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_asset_pin_must_be_a_plain_value) ... ok
test_audit_profile_renders_read_only_sandbox_override (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_audit_profile_renders_read_only_sandbox_override) ... ok
test_bootstrap_pins_render_into_setup_and_their_installers (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_bootstrap_pins_render_into_setup_and_their_installers) ... ok
test_check_reports_asset_render_drift (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_check_reports_asset_render_drift) ... ok
test_claude_deny_rules_use_edit_for_file_mutations (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_claude_deny_rules_use_edit_for_file_mutations) ... ok
test_claude_sandbox_renders_optional_socket_and_extra_write_keys (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_claude_sandbox_renders_optional_socket_and_extra_write_keys) ... ok
test_claude_sandbox_renders_per_os_from_the_manifest (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_claude_sandbox_renders_per_os_from_the_manifest) ... ok
test_claude_settings_render_interactive_advisor_only_when_set (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_claude_settings_render_interactive_advisor_only_when_set) ... ok
test_claude_settings_render_the_format_hook_from_its_path (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_claude_settings_render_the_format_hook_from_its_path) ... ok
test_claude_settings_renders_session_start_hooks (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_claude_settings_renders_session_start_hooks) ... ok
test_claude_settings_use_interactive_profile_with_permgate (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_claude_settings_use_interactive_profile_with_permgate) ... ok
test_claude_skill_symlink_outputs_strip_executable_target_prefix (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_claude_skill_symlink_outputs_strip_executable_target_prefix) ... ok
test_codex_command_hooks_render_after_permission_request_in_manifest_order (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_codex_command_hooks_render_after_permission_request_in_manifest_order) ... ok
test_codex_config_renders_permgate_permission_request (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_codex_config_renders_permgate_permission_request) ... ok
test_codex_config_renders_working_tree_project_key (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_codex_config_renders_working_tree_project_key) ... ok
test_empty_or_missing_codex_command_hooks_render_no_table (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_empty_or_missing_codex_command_hooks_render_no_table) ... ok
test_entries_reaching_one_file_through_a_symlink_edit_one_snapshot (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_entries_reaching_one_file_through_a_symlink_edit_one_snapshot) ... ok
test_expected_outputs_uses_codex_baseline_path (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_expected_outputs_uses_codex_baseline_path) ... ok
test_hook_trust_hash_reproduces_codex_current_hashes (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_hook_trust_hash_reproduces_codex_current_hashes) ... ok
test_linux_sandbox_excludes_the_top_level_herdr_agents_invocation (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_linux_sandbox_excludes_the_top_level_herdr_agents_invocation) ... ok
test_managed_claude_sandbox_excludes_agmsg_dispatch (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_managed_claude_sandbox_excludes_agmsg_dispatch) ... ok
test_managed_codex_config_routes_compaction_and_session_end_to_compactiondb (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_managed_codex_config_routes_compaction_and_session_end_to_compactiondb) ... ok
test_managed_codex_path_includes_installed_common_bin (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_managed_codex_path_includes_installed_common_bin) ... ok
test_managed_hooks_use_installed_permgate_paths (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_managed_hooks_use_installed_permgate_paths) ... ok
test_manifest_keeps_model_ids_only_in_profiles (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_manifest_keeps_model_ids_only_in_profiles) ... ok
test_model_profiles_env_renders_claude_advisor_only_when_set (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_model_profiles_env_renders_claude_advisor_only_when_set) ... ok
test_model_profiles_env_renders_orchestrator_kind (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_model_profiles_env_renders_orchestrator_kind) ... ok
test_model_profiles_env_renders_worker_kind (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_model_profiles_env_renders_worker_kind) ... ok
test_model_profiles_env_renders_worker_profile (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_model_profiles_env_renders_worker_profile) ... ok
test_model_profiles_env_renders_worker_worktree (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_model_profiles_env_renders_worker_worktree) ... ok
test_model_profiles_env_selects_no_github_store (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_model_profiles_env_selects_no_github_store) ... ok
test_model_profiles_reject_incomplete_or_unsafe_entries (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_model_profiles_reject_incomplete_or_unsafe_entries) ... ERROR: model profile standard is missing codex
ERROR: model profile standard.claude.model must be a launcher-safe string
ERROR: model_profiles must define the express profile
ok
test_model_profiles_reject_invalid_sandbox_mode (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_model_profiles_reject_invalid_sandbox_mode) ... ok
test_model_profiles_reject_unsafe_advisor (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_model_profiles_reject_unsafe_advisor) ... ERROR: model profile standard.claude.advisor must be a launcher-safe string
ok
test_orchestrator_kind_defaults_to_claude (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_orchestrator_kind_defaults_to_claude) ... ok
test_plugin_versions_order_build_metadata_like_the_semver_crate (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_plugin_versions_order_build_metadata_like_the_semver_crate) ... ok
test_profile_modify_scripts_are_byte_idempotent_with_runtime_state (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_profile_modify_scripts_are_byte_idempotent_with_runtime_state) ... ok
test_profile_modify_scripts_are_quiet_for_matching_hook_trust (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_profile_modify_scripts_are_quiet_for_matching_hook_trust) ... ok
test_profile_modify_scripts_handle_table_headers_with_trailing_comments (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_profile_modify_scripts_handle_table_headers_with_trailing_comments) ... ok
test_profile_modify_scripts_hash_plugin_hooks_or_fall_back_to_the_pin (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_profile_modify_scripts_hash_plugin_hooks_or_fall_back_to_the_pin) ... ok
test_profile_modify_scripts_hash_the_plugin_version_codex_loads (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_profile_modify_scripts_hash_the_plugin_version_codex_loads) ... ok
test_profile_modify_scripts_keep_header_like_lines_inside_multiline_strings (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_profile_modify_scripts_keep_header_like_lines_inside_multiline_strings) ... ok
test_profile_modify_scripts_keep_the_current_content_when_the_merge_is_invalid (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_profile_modify_scripts_keep_the_current_content_when_the_merge_is_invalid) ... ok
test_profile_modify_scripts_preserve_repeated_runtime_tables (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_profile_modify_scripts_preserve_repeated_runtime_tables) ... ok
test_profile_modify_scripts_preserve_runtime_state (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_profile_modify_scripts_preserve_runtime_state) ... ok
test_profile_modify_scripts_replace_a_single_quoted_declared_entry (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_profile_modify_scripts_replace_a_single_quoted_declared_entry) ... ok
test_profile_modify_scripts_replace_declared_dotted_keys_under_hooks_and_at_the_root (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_profile_modify_scripts_replace_declared_dotted_keys_under_hooks_and_at_the_root) ... ok
test_profile_modify_scripts_replace_declared_hook_trust_and_keep_undeclared (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_profile_modify_scripts_replace_declared_hook_trust_and_keep_undeclared) ... ok
test_profile_modify_scripts_replace_inline_table_and_dotted_forms (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_profile_modify_scripts_replace_inline_table_and_dotted_forms) ... ok
test_profile_modify_scripts_seed_base_hook_trust (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_profile_modify_scripts_seed_base_hook_trust) ... ok
test_profile_modify_scripts_treat_equivalent_hook_state_spellings_as_one_table (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_profile_modify_scripts_treat_equivalent_hook_state_spellings_as_one_table) ... ok
test_profile_modify_scripts_warn_on_hook_trust_divergence (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_profile_modify_scripts_warn_on_hook_trust_divergence) ... ok
test_project_map_reload_hook_accepts_only_cdp_target_ids (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_project_map_reload_hook_accepts_only_cdp_target_ids) ... ok
test_project_map_reload_hook_acts_only_on_the_map_and_never_fails (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_project_map_reload_hook_acts_only_on_the_map_and_never_fails) ... ok
test_project_map_reload_hook_compares_canonical_paths_for_every_path_form (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_project_map_reload_hook_compares_canonical_paths_for_every_path_form) ... ok
test_project_map_reload_hook_guards_against_a_tab_navigating_away (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_project_map_reload_hook_guards_against_a_tab_navigating_away) ... ok
test_project_map_reload_hook_matches_percent_encoded_tilde (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_project_map_reload_hook_matches_percent_encoded_tilde) ... ok
test_project_map_reload_hook_opens_event_map_when_only_another_repository_is_open (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_project_map_reload_hook_opens_event_map_when_only_another_repository_is_open) ... ok
test_project_map_reload_hook_opens_the_pane_when_no_browser_shows_the_map (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_project_map_reload_hook_opens_the_pane_when_no_browser_shows_the_map) ... ok
test_project_map_reload_hook_pins_the_bound_tab_when_it_closes (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_project_map_reload_hook_pins_the_bound_tab_when_it_closes) ... ok
test_project_map_reload_hook_rejects_percent_encoded_path_separators (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_project_map_reload_hook_rejects_percent_encoded_path_separators) ... ok
test_project_map_reload_hook_renders_into_post_tool_use (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_project_map_reload_hook_renders_into_post_tool_use) ... ok
test_project_map_reload_hook_resolves_relative_paths_from_physical_cwd (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_project_map_reload_hook_resolves_relative_paths_from_physical_cwd) ... ok
test_project_map_reload_hook_selects_the_event_map_among_two_repositories (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_project_map_reload_hook_selects_the_event_map_among_two_repositories) ... ok
test_repository_marketplace_is_a_runtime_owned_seed (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_repository_marketplace_is_a_runtime_owned_seed) ... ok
test_security_profile_renders_launcher_and_expanded_notify (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_security_profile_renders_launcher_and_expanded_notify) ... ok
test_set_asset_field_reaches_the_fallback_pin_and_its_checksums (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_set_asset_field_reaches_the_fallback_pin_and_its_checksums) ... ok
test_set_asset_field_rejects_unknown_targets_and_unsafe_values (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_set_asset_field_rejects_unknown_targets_and_unsafe_values) ... ok
test_set_asset_field_rewrites_only_the_named_scalar (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_set_asset_field_rewrites_only_the_named_scalar) ... ok
test_set_asset_leaves_files_untouched_when_an_assignment_is_invalid (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_set_asset_leaves_files_untouched_when_an_assignment_is_invalid) ... ok
test_set_asset_refuses_fields_other_than_pins_and_checksums (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_set_asset_refuses_fields_other_than_pins_and_checksums) ... ok
test_set_asset_rejects_a_value_that_does_not_parse_back_as_a_string (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_set_asset_rejects_a_value_that_does_not_parse_back_as_a_string) ... ok
test_set_asset_reports_an_unparsable_manifest_without_a_traceback (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_set_asset_reports_an_unparsable_manifest_without_a_traceback) ... ok
test_set_asset_updates_the_manifest_and_renders_its_pins (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_set_asset_updates_the_manifest_and_renders_its_pins) ... ok
test_unknown_interactive_profile_fails (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_unknown_interactive_profile_fails) ... ERROR: interactive_profile must name a model profile: 'missing'
ok
test_unknown_orchestrator_kind_fails (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_unknown_orchestrator_kind_fails) ... ok
test_unknown_worker_kind_fails (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_unknown_worker_kind_fails) ... ERROR: worker_kind must be one of ('codex', 'claude'): 'banana'
ok
test_unknown_worker_profile_fails (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_unknown_worker_profile_fails) ... ERROR: worker_profile must name a model profile: 'missing'
ok
test_worker_kind_defaults_to_codex (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_worker_kind_defaults_to_codex) ... ok
test_worker_worktree_outside_claude_worktrees_fails (tests.unit.test_generate_agent_configs.GenerateAgentConfigsTest.test_worker_worktree_outside_claude_worktrees_fails) ... ERROR: worker_worktree must be a relative path under .claude/worktrees/: 'worker-c'
ERROR: worker_worktree must be a relative path under .claude/worktrees/: '/abs/.claude/worktrees/x'
ERROR: worker_worktree must be a relative path under .claude/worktrees/: '.claude/worktrees/..'
ERROR: worker_worktree must be a relative path under .claude/worktrees/: '.claude/worktrees/a/b'
ERROR: worker_worktree must be a relative path under .claude/worktrees/: '.claude/worktrees/$(x)'
ok

----------------------------------------------------------------------
Ran 197 tests in 28.267s

OK
```

### Required render check

Command: `make render-check`

Exit: `0`

```text
uv run --with pyyaml scripts/generate-agent-configs.py --check
mise WARN  tracking config: failed to ln -sf ~/Workspace/dotfiles/.claude/worktrees/worker-e/.orchestration/dotfiles-T131-claude-pinned-merge-gate-review-a01/source/mise.toml ~/.local/state/mise/tracked-configs/66fdde7a0d9576a1: Operation not permitted (os error 1)
   Building pyyaml==6.0.3
      Built pyyaml==6.0.3
Installed 1 package in 1ms
generated agent configs are up to date
```

### Required shellcheck

Command: `shellcheck -x home/dot_claude/hooks/executable_gh-merge-gate.sh`

Exit: `0`

```text
mise WARN  tracking config: failed to ln -sf ~/Workspace/dotfiles/.claude/worktrees/worker-e/.orchestration/dotfiles-T131-claude-pinned-merge-gate-review-a01/source/mise.toml ~/.local/state/mise/tracked-configs/66fdde7a0d9576a1: Operation not permitted (os error 1)
```

### Final dry probes (only stub gh and argument printing)

Command: `uv run python ../dry_probes.py`

Exit: `0`

```text
{"name": "baseline", "command": "gh pr merge 7 --squash --match-head-commit 3498973bd057ea4fb405823de718e9da6e40e548", "expected": "allow", "actual": "allow", "exit": 0, "stdout": "{\"hookSpecificOutput\":{\"hookEventName\":\"PreToolUse\",\"permissionDecision\":\"allow\",\"permissionDecisionReason\":\"gh-merge-gate: PR 7 head 3498973bd057 accepted in t.md with green required checks\"}}\n", "stderr": ""}
{"name": "quoted-binary", "command": "\"gh\" pr merge 7 --admin", "expected": "ask", "actual": "no-decision", "exit": 0, "stdout": "", "stderr": ""}
{"name": "quoted-subcommand", "command": "gh pr \"merge\" 7 --admin", "expected": "ask", "actual": "no-decision", "exit": 0, "stdout": "", "stderr": ""}
{"name": "concatenated-binary", "command": "g''h pr merge 7 --admin", "expected": "ask", "actual": "no-decision", "exit": 0, "stdout": "", "stderr": ""}
{"name": "alias", "command": "gh land 7 --admin", "expected": "ask", "actual": "no-decision", "exit": 0, "stdout": "", "stderr": ""}
{"name": "env-prefix", "command": "env gh pr merge 7 --admin", "expected": "ask", "actual": "ask", "exit": 0, "stdout": "{\"hookSpecificOutput\":{\"hookEventName\":\"PreToolUse\",\"permissionDecision\":\"ask\",\"permissionDecisionReason\":\"gh-merge-gate: only the gh pr form can pass\"}}\n", "stderr": ""}
{"name": "command-prefix", "command": "command gh pr merge 7 --admin", "expected": "ask", "actual": "ask", "exit": 0, "stdout": "{\"hookSpecificOutput\":{\"hookEventName\":\"PreToolUse\",\"permissionDecision\":\"ask\",\"permissionDecisionReason\":\"gh-merge-gate: only the gh pr form can pass\"}}\n", "stderr": ""}
{"name": "absolute-binary", "command": "/usr/local/bin/gh pr merge 7 --admin", "expected": "ask", "actual": "ask", "exit": 0, "stdout": "{\"hookSpecificOutput\":{\"hookEventName\":\"PreToolUse\",\"permissionDecision\":\"ask\",\"permissionDecisionReason\":\"gh-merge-gate: only the gh pr form can pass\"}}\n", "stderr": ""}
{"name": "repo-first", "command": "gh --repo o/r pr merge 7 --admin", "expected": "ask", "actual": "ask", "exit": 0, "stdout": "{\"hookSpecificOutput\":{\"hookEventName\":\"PreToolUse\",\"permissionDecision\":\"ask\",\"permissionDecisionReason\":\"gh-merge-gate: only the gh pr form can pass\"}}\n", "stderr": ""}
{"name": "api-method-first", "command": "gh api --method PUT repos/o/r/pulls/7/merge", "expected": "ask", "actual": "ask", "exit": 0, "stdout": "{\"hookSpecificOutput\":{\"hookEventName\":\"PreToolUse\",\"permissionDecision\":\"ask\",\"permissionDecisionReason\":\"gh-merge-gate: only the gh pr form can pass\"}}\n", "stderr": ""}
{"name": "api-method-last", "command": "gh api repos/o/r/pulls/7/merge --method PUT", "expected": "ask", "actual": "ask", "exit": 0, "stdout": "{\"hookSpecificOutput\":{\"hookEventName\":\"PreToolUse\",\"permissionDecision\":\"ask\",\"permissionDecisionReason\":\"gh-merge-gate: only the gh pr form can pass\"}}\n", "stderr": ""}
{"name": "prose", "command": "git commit -m 'docs: explain gh pr merge 7'", "expected": "no-decision", "actual": "ask", "exit": 0, "stdout": "{\"hookSpecificOutput\":{\"hookEventName\":\"PreToolUse\",\"permissionDecision\":\"ask\",\"permissionDecisionReason\":\"gh-merge-gate: not a single simple command around:  gh pr merge \"}}\n", "stderr": ""}
{"name": "heredoc-prose", "command": "cat <<'EOF'\ngh pr merge 7\nEOF", "expected": "no-decision", "actual": "ask", "exit": 0, "stdout": "{\"hookSpecificOutput\":{\"hookEventName\":\"PreToolUse\",\"permissionDecision\":\"ask\",\"permissionDecisionReason\":\"gh-merge-gate: not a single simple command around: gh pr merge \"}}\n", "stderr": ""}
{"name": "tab-json", "command": "gh\tpr\tmerge 7; true", "expected": "ask", "actual": "invalid-json", "exit": 0, "stdout": "{\"hookSpecificOutput\":{\"hookEventName\":\"PreToolUse\",\"permissionDecision\":\"ask\",\"permissionDecisionReason\":\"gh-merge-gate: not a single simple command around: gh\tpr\tmerge \"}}\n", "stderr": ""}
{"name": "unquoted-create", "command": "gh pr create --draft --base main --head task/ok --fill", "expected": "allow", "actual": "allow", "exit": 0, "stdout": "{\"hookSpecificOutput\":{\"hookEventName\":\"PreToolUse\",\"permissionDecision\":\"allow\",\"permissionDecisionReason\":\"gh-merge-gate: draft PR of task/ok onto main\"}}\n", "stderr": ""}
{"name": "wrong-headRefOid", "command": "gh pr merge 7 --squash --match-head-commit 3498973bd057ea4fb405823de718e9da6e40e548", "expected": "ask", "actual": "ask", "exit": 0, "stdout": "{\"hookSpecificOutput\":{\"hookEventName\":\"PreToolUse\",\"permissionDecision\":\"ask\",\"permissionDecisionReason\":\"gh-merge-gate: PR 7 head is not 3498973bd057ea4fb405823de718e9da6e40e548\"}}\n", "stderr": ""}
{"name": "wrong-baseRefName", "command": "gh pr merge 7 --squash --match-head-commit 3498973bd057ea4fb405823de718e9da6e40e548", "expected": "ask", "actual": "ask", "exit": 0, "stdout": "{\"hookSpecificOutput\":{\"hookEventName\":\"PreToolUse\",\"permissionDecision\":\"ask\",\"permissionDecisionReason\":\"gh-merge-gate: PR 7 does not target main\"}}\n", "stderr": ""}
{"name": "wrong-state", "command": "gh pr merge 7 --squash --match-head-commit 3498973bd057ea4fb405823de718e9da6e40e548", "expected": "ask", "actual": "ask", "exit": 0, "stdout": "{\"hookSpecificOutput\":{\"hookEventName\":\"PreToolUse\",\"permissionDecision\":\"ask\",\"permissionDecisionReason\":\"gh-merge-gate: PR 7 is not open\"}}\n", "stderr": ""}
{"name": "wrong-isDraft", "command": "gh pr merge 7 --squash --match-head-commit 3498973bd057ea4fb405823de718e9da6e40e548", "expected": "ask", "actual": "ask", "exit": 0, "stdout": "{\"hookSpecificOutput\":{\"hookEventName\":\"PreToolUse\",\"permissionDecision\":\"ask\",\"permissionDecisionReason\":\"gh-merge-gate: PR 7 is a draft\"}}\n", "stderr": ""}
{"name": "malformed-payload", "command": "gh pr merge 7 --squash --match-head-commit 3498973bd057ea4fb405823de718e9da6e40e548", "expected": "ask", "actual": "ask", "exit": 0, "stdout": "{\"hookSpecificOutput\":{\"hookEventName\":\"PreToolUse\",\"permissionDecision\":\"ask\",\"permissionDecisionReason\":\"gh-merge-gate: unreadable payload\"}}\n", "stderr": ""}
{"name": "empty-payload", "command": "gh pr merge 7 --squash --match-head-commit 3498973bd057ea4fb405823de718e9da6e40e548", "expected": "ask", "actual": "no-decision", "exit": 0, "stdout": "", "stderr": ""}
{"name": "malformed-view", "command": "gh pr merge 7 --squash --match-head-commit 3498973bd057ea4fb405823de718e9da6e40e548", "expected": "ask", "actual": "ask", "exit": 0, "stdout": "{\"hookSpecificOutput\":{\"hookEventName\":\"PreToolUse\",\"permissionDecision\":\"ask\",\"permissionDecisionReason\":\"gh-merge-gate: PR 7 is not open\"}}\n", "stderr": "jq: parse error: Unfinished JSON term at EOF at line 2, column 0\n"}
{"name": "coloured-view", "command": "gh pr merge 7 --squash --match-head-commit 3498973bd057ea4fb405823de718e9da6e40e548", "expected": "ask", "actual": "ask", "exit": 0, "stdout": "{\"hookSpecificOutput\":{\"hookEventName\":\"PreToolUse\",\"permissionDecision\":\"ask\",\"permissionDecisionReason\":\"gh-merge-gate: PR 7 is not open\"}}\n", "stderr": "jq: parse error: Invalid numeric literal at line 1, column 2\n"}
{"name": "gh-failure", "command": "gh pr merge 7 --squash --match-head-commit 3498973bd057ea4fb405823de718e9da6e40e548", "expected": "ask", "actual": "ask", "exit": 0, "stdout": "{\"hookSpecificOutput\":{\"hookEventName\":\"PreToolUse\",\"permissionDecision\":\"ask\",\"permissionDecisionReason\":\"gh-merge-gate: gh repo view failed\"}}\n", "stderr": ""}
{"name": "rules-failure", "command": "gh pr merge 7 --squash --match-head-commit 3498973bd057ea4fb405823de718e9da6e40e548", "expected": "ask", "actual": "ask", "exit": 0, "stdout": "{\"hookSpecificOutput\":{\"hookEventName\":\"PreToolUse\",\"permissionDecision\":\"ask\",\"permissionDecisionReason\":\"gh-merge-gate: cannot read the branch rules\"}}\n", "stderr": ""}
{"name": "empty-rules", "command": "gh pr merge 7 --squash --match-head-commit 3498973bd057ea4fb405823de718e9da6e40e548", "expected": "ask", "actual": "ask", "exit": 0, "stdout": "{\"hookSpecificOutput\":{\"hookEventName\":\"PreToolUse\",\"permissionDecision\":\"ask\",\"permissionDecisionReason\":\"gh-merge-gate: main requires no status checks\"}}\n", "stderr": ""}
{"name": "missing-check", "command": "gh pr merge 7 --squash --match-head-commit 3498973bd057ea4fb405823de718e9da6e40e548", "expected": "ask", "actual": "ask", "exit": 0, "stdout": "{\"hookSpecificOutput\":{\"hookEventName\":\"PreToolUse\",\"permissionDecision\":\"ask\",\"permissionDecisionReason\":\"gh-merge-gate: required check test is not green on 3498973bd057\"}}\n", "stderr": ""}
{"name": "missing-record", "command": "gh pr merge 7 --squash --match-head-commit 3498973bd057ea4fb405823de718e9da6e40e548", "expected": "ask", "actual": "ask", "exit": 0, "stdout": "{\"hookSpecificOutput\":{\"hookEventName\":\"PreToolUse\",\"permissionDecision\":\"ask\",\"permissionDecisionReason\":\"gh-merge-gate: no acceptance record pins head 3498973bd057\"}}\n", "stderr": ""}
{"name": "missing-audit", "command": "gh pr merge 7 --squash --match-head-commit 3498973bd057ea4fb405823de718e9da6e40e548", "expected": "ask", "actual": "ask", "exit": 0, "stdout": "{\"hookSpecificOutput\":{\"hookEventName\":\"PreToolUse\",\"permissionDecision\":\"ask\",\"permissionDecisionReason\":\"gh-merge-gate: no audit of 3498973\"}}\n", "stderr": ""}
{"name": "body-only-wrong-task-record", "command": "gh pr merge 7 --squash --match-head-commit 3498973bd057ea4fb405823de718e9da6e40e548", "expected": "ask", "actual": "allow", "exit": 0, "stdout": "{\"hookSpecificOutput\":{\"hookEventName\":\"PreToolUse\",\"permissionDecision\":\"allow\",\"permissionDecisionReason\":\"gh-merge-gate: PR 7 head 3498973bd057 accepted in t.md with green required checks\"}}\n", "stderr": ""}
{"name": "audit-is-directory", "command": "gh pr merge 7 --squash --match-head-commit 3498973bd057ea4fb405823de718e9da6e40e548", "expected": "ask", "actual": "allow", "exit": 0, "stdout": "{\"hookSpecificOutput\":{\"hookEventName\":\"PreToolUse\",\"permissionDecision\":\"allow\",\"permissionDecisionReason\":\"gh-merge-gate: PR 7 head 3498973bd057 accepted in t.md with green required checks\"}}\n", "stderr": ""}
{"name": "audit-is-incorrect", "command": "gh pr merge 7 --squash --match-head-commit 3498973bd057ea4fb405823de718e9da6e40e548", "expected": "ask", "actual": "allow", "exit": 0, "stdout": "{\"hookSpecificOutput\":{\"hookEventName\":\"PreToolUse\",\"permissionDecision\":\"allow\",\"permissionDecisionReason\":\"gh-merge-gate: PR 7 head 3498973bd057 accepted in t.md with green required checks\"}}\n", "stderr": ""}
{"name": "symlinked-acceptance-parent", "command": "gh pr merge 7 --squash --match-head-commit 3498973bd057ea4fb405823de718e9da6e40e548", "expected": "ask", "actual": "allow", "exit": 0, "stdout": "{\"hookSpecificOutput\":{\"hookEventName\":\"PreToolUse\",\"permissionDecision\":\"allow\",\"permissionDecisionReason\":\"gh-merge-gate: PR 7 head 3498973bd057 accepted in t.md with green required checks\"}}\n", "stderr": ""}
{"name": "arbitrary-primary-checkout", "command": "gh pr merge 7 --squash --match-head-commit 3498973bd057ea4fb405823de718e9da6e40e548", "expected": "ask", "actual": "allow", "exit": 0, "stdout": "{\"hookSpecificOutput\":{\"hookEventName\":\"PreToolUse\",\"permissionDecision\":\"allow\",\"permissionDecisionReason\":\"gh-merge-gate: PR 7 head 3498973bd057 accepted in t.md with green required checks\"}}\n", "stderr": ""}
{"name": "ready-body-only-record", "command": "gh pr create --base main --head task/ok --title t --body b", "expected": "ask", "actual": "allow", "exit": 0, "stdout": "{\"hookSpecificOutput\":{\"hookEventName\":\"PreToolUse\",\"permissionDecision\":\"allow\",\"permissionDecisionReason\":\"gh-merge-gate: PR of task/ok at 3498973bd057 accepted in t.md\"}}\n", "stderr": ""}
{"name": "draft-stack-parent-not-accepted", "command": "gh pr create --draft --base stack/parent --head task/ok --fill", "expected": "allow", "actual": "allow", "exit": 0, "stdout": "{\"hookSpecificOutput\":{\"hookEventName\":\"PreToolUse\",\"permissionDecision\":\"allow\",\"permissionDecisionReason\":\"gh-merge-gate: draft PR of task/ok onto stack/parent\"}}\n", "stderr": ""}
{"name": "ready-stack-parent-not-accepted", "command": "gh pr create --base stack/parent --head task/ok --fill", "expected": "ask", "actual": "allow", "exit": 0, "stdout": "{\"hookSpecificOutput\":{\"hookEventName\":\"PreToolUse\",\"permissionDecision\":\"allow\",\"permissionDecisionReason\":\"gh-merge-gate: PR of task/ok at 3498973bd057 accepted in t.md\"}}\n", "stderr": ""}
{"name": "records-ok", "command": "gh pr create --base main --head orchestration/b --fill", "expected": "allow", "actual": "allow", "exit": 0, "stdout": "{\"hookSpecificOutput\":{\"hookEventName\":\"PreToolUse\",\"permissionDecision\":\"allow\",\"permissionDecisionReason\":\"gh-merge-gate: records PR of orchestration/b onto main\"}}\n", "stderr": ""}
{"name": "records-outside", "command": "gh pr create --base main --head orchestration/b --fill", "expected": "ask", "actual": "ask", "exit": 0, "stdout": "{\"hookSpecificOutput\":{\"hookEventName\":\"PreToolUse\",\"permissionDecision\":\"ask\",\"permissionDecisionReason\":\"gh-merge-gate: create: orchestration/b touches files outside .orchestration\"}}\n", "stderr": ""}
{"name": "records-count-only", "command": "gh pr create --base main --head orchestration/b --fill", "expected": "ask", "actual": "allow", "exit": 0, "stdout": "{\"hookSpecificOutput\":{\"hookEventName\":\"PreToolUse\",\"permissionDecision\":\"allow\",\"permissionDecisionReason\":\"gh-merge-gate: records PR of orchestration/b onto main\"}}\n", "stderr": ""}
{"name": "records-empty", "command": "gh pr create --base main --head orchestration/b --fill", "expected": "ask", "actual": "ask", "exit": 0, "stdout": "{\"hookSpecificOutput\":{\"hookEventName\":\"PreToolUse\",\"permissionDecision\":\"ask\",\"permissionDecisionReason\":\"gh-merge-gate: create: records diff empty or too large\"}}\n", "stderr": ""}
{"name": "records-too-large", "command": "gh pr create --base main --head orchestration/b --fill", "expected": "ask", "actual": "ask", "exit": 0, "stdout": "{\"hookSpecificOutput\":{\"hookEventName\":\"PreToolUse\",\"permissionDecision\":\"ask\",\"permissionDecisionReason\":\"gh-merge-gate: create: records diff empty or too large\"}}\n", "stderr": ""}
{"name": "draft-empty-default", "command": "gh pr create --draft --base main --head task/ok --fill", "expected": "ask", "actual": "ask", "exit": 0, "stdout": "{\"hookSpecificOutput\":{\"hookEventName\":\"PreToolUse\",\"permissionDecision\":\"ask\",\"permissionDecisionReason\":\"gh-merge-gate: create: base main is neither  nor the head of an open PR\"}}\n", "stderr": ""}
{"name": "create-bad-parser-output", "command": "gh pr create --draft --base main --head task/ok --fill", "expected": "ask", "actual": "ask", "exit": 0, "stdout": "{\"hookSpecificOutput\":{\"hookEventName\":\"PreToolUse\",\"permissionDecision\":\"ask\",\"permissionDecisionReason\":\"gh-merge-gate: create: not a single plain gh pr create\"}}\n", "stderr": ""}
{"name": "create-operator", "command": "gh pr create --draft --base main --head task/ok --fill; true", "expected": "ask", "actual": "ask", "exit": 0, "stdout": "{\"hookSpecificOutput\":{\"hookEventName\":\"PreToolUse\",\"permissionDecision\":\"ask\",\"permissionDecisionReason\":\"gh-merge-gate: create: not a single plain gh pr create\"}}\n", "stderr": ""}
{"name": "create-glob-title", "command": "gh pr create --draft --base main --head task/ok --title *", "expected": "ask", "actual": "allow", "exit": 0, "stdout": "{\"hookSpecificOutput\":{\"hookEventName\":\"PreToolUse\",\"permissionDecision\":\"allow\",\"permissionDecisionReason\":\"gh-merge-gate: draft PR of task/ok onto main\"}}\n", "stderr": ""}
{"name": "detector-crash", "command": "gh pr merge 7 --squash --match-head-commit 3498973bd057ea4fb405823de718e9da6e40e548", "expected": "ask", "actual": "no-decision", "exit": 0, "stdout": "", "stderr": ""}
{"name": "other-repository-same-head", "command": "gh pr merge 7 --squash --match-head-commit 3498973bd057ea4fb405823de718e9da6e40e548 --repo other/repo", "expected": "ask", "actual": "allow", "exit": 0, "stdout": "{\"hookSpecificOutput\":{\"hookEventName\":\"PreToolUse\",\"permissionDecision\":\"allow\",\"permissionDecisionReason\":\"gh-merge-gate: PR 7 head 3498973bd057 accepted in t.md with green required checks\"}}\n", "stderr": ""}
{"name": "draft-empty-default-stack", "command": "gh pr create --draft --base stack/parent --head task/ok --fill", "expected": "ask", "actual": "allow", "exit": 0, "stdout": "{\"hookSpecificOutput\":{\"hookEventName\":\"PreToolUse\",\"permissionDecision\":\"allow\",\"permissionDecisionReason\":\"gh-merge-gate: draft PR of task/ok onto stack/parent\"}}\n", "stderr": ""}
{"name": "glob-expanded-arguments", "exit": 0, "stdout": "<pr>\n<create>\n<--draft>\n<--base>\n<main>\n<--head>\n<task/ok>\n<--title>\n<--0-title>\n<--draft=false>\n<--head=evil>\n", "note": "No gh executable was invoked; duplicate draft/head flags appear only after expansion."}
{"name": "validator-missing-DELETE", "expected": "rejected", "actual": "accepted"}
{"name": "validator-echo-gate", "expected": "rejected", "actual": "accepted"}
{"name": "validator-async-gate", "expected": "rejected", "actual": "accepted"}
```

### Final dry-probe stderr

Command: `uv run python ../dry_probes.py (stderr)`

Exit: `0`

```text
```

Review verdict: incorrect
