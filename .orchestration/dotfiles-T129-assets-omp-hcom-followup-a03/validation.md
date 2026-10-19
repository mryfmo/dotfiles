---
task_id: dotfiles-T129-assets-omp-hcom-followup-a03
seat: claude-standard-dot-a009
code_head: 9a8e24697b032f1051062aaf53d0af2343257e98
base: 205fe85c19c03750fe3551bb96e084e9f0a676b6
---

# Validation: dotfiles-T129-assets-omp-hcom-followup-a03

- Every block ran from this worktree on `tools/assets-omp-hcom-followup-a03` at the code head `9a8e2469`; the only later commit adds this directory's records. Each block prints its commands, their verbatim output (the home directory shown as `~`) and the block's last exit status.
- `MAIN` is the main checkout, `T` the task id, `$S` the session scratchpad and `<user-temp>` the per-user macOS temporary directory. §4r, §6a, §6b and §7 ran outside the sandbox, because the inherited `update_omp` tests need macOS `mktemp -d`, which the sandbox refuses (sandbox record). The tests use fakes only.
- **Red, then green:** §4r is red at `205fe85c`: each of the five selectors ran one test and failed by assertion. §6b is green at the code head, and §6a is the Check.
- **§8 exits 1 on an inherited finding:** its last command is ruff on `test_remove_agent_asset.py`. That reports EXE001 and I001 on the module's header, and the same two on `origin/main`. ShellCheck, shfmt, bash 3.2 and `ruff format` are clean.

## 1. Task file (sha256 cfa229f1…) and the branch copy
```console
$ shasum -a 256 "~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T129-assets-omp-hcom-followup-a03.md" ".orchestration/dotfiles-T129-assets-omp-hcom-followup-a03/task.md"; cmp "~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T129-assets-omp-hcom-followup-a03.md" ".orchestration/dotfiles-T129-assets-omp-hcom-followup-a03/task.md" && echo byte-identical
cfa229f155b349f3ba02854f1440339e8bd481756ee657ee476e32afc90c844d  ~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T129-assets-omp-hcom-followup-a03.md
cfa229f155b349f3ba02854f1440339e8bd481756ee657ee476e32afc90c844d  .orchestration/dotfiles-T129-assets-omp-hcom-followup-a03/task.md
byte-identical
[exit 0]
```

## 1a. The task-consistency check on the dispatched file
```console
$ uv run --offline --no-project --with pyyaml python -I scripts/orchestrator/task-consistency-check.py --root "$PWD" "~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T129-assets-omp-hcom-followup-a03.md"
dotfiles-T129-assets-omp-hcom-followup-a03.md: OK
[exit 0]
```

## 2. Branch, base and commits
```console
$ git rev-parse --abbrev-ref HEAD; git rev-parse origin/main; git merge-base origin/main HEAD; git log --format='%H %s' origin/main..HEAD
tools/assets-omp-hcom-followup-a03
205fe85c19c03750fe3551bb96e084e9f0a676b6
205fe85c19c03750fe3551bb96e084e9f0a676b6
9a8e24697b032f1051062aaf53d0af2343257e98 fix(assets): the #416 scripts compare paths through their normalisers; their seven lint baseline rows go (T129 assets-omp-hcom follow-up a03)
d3aab756b5026d3ca888fec82af735a73d4f2d53 chore(orchestration): the dotfiles-T129-assets-omp-hcom-followup-a03 task copy
[exit 0]
```

## 3. The owned rows at the base: each hash and the line it names in 205fe85c
```console
$ git show origin/main:scripts/lint-comparisons-baseline.tsv | /usr/bin/grep -n -e executable_remove-agent-asset -e update-agent-assets.sh; for f in home/dot_local/bin/common/executable_remove-agent-asset scripts/update-agent-assets.sh; do git show origin/main:$f | uv run --no-project python -I -c 'import hashlib, sys; [print(sys.argv[1], n, hashlib.sha256(l.strip().encode()).hexdigest()[:12], l.strip()[:90]) for n, l in enumerate(sys.stdin.read().split("\n"), 1) if hashlib.sha256(l.strip().encode()).hexdigest()[:7] in ("5903a3c", "ff2e0ca", "1c780a5", "1d5afaf", "851db69")]' $f; done
21:home/dot_local/bin/common/executable_remove-agent-asset	R1	5903a3cfc9310928d0438ee9dee4e09fc314e0c70d3d17cbd36297288b208d4f
22:home/dot_local/bin/common/executable_remove-agent-asset	R1	5903a3cfc9310928d0438ee9dee4e09fc314e0c70d3d17cbd36297288b208d4f
23:home/dot_local/bin/common/executable_remove-agent-asset	R1	ff2e0ca268ac61d911860ae79ea5165571fb624f3335912a0fd16bfc3b40912e
73:scripts/update-agent-assets.sh	R1	1c780a546a27e0a65e2d6b2a6431df9c1fa1a84006a5cdf62579d97724ee8966
74:scripts/update-agent-assets.sh	R1	1d5afafa1445dd075af19378727e3660a631287a1f251e19b0c9c450ca381e45
75:scripts/update-agent-assets.sh	R2	851db696b62d42ddfefa5fbc21df66a2bf37a6906e735a2a802cf1b1b54e878a
76:scripts/update-agent-assets.sh	R2	851db696b62d42ddfefa5fbc21df66a2bf37a6906e735a2a802cf1b1b54e878a
home/dot_local/bin/common/executable_remove-agent-asset 82 ff2e0ca268ac [ "$1" = "$2" ] || [[ "$1" == "$2/"* ]]
home/dot_local/bin/common/executable_remove-agent-asset 101 5903a3cfc931 if [ "${candidate}" != "${root}" ] && path_has_prefix "${candidate}" "${root}"; then
home/dot_local/bin/common/executable_remove-agent-asset 211 5903a3cfc931 if [ "${candidate}" != "${root}" ] && path_has_prefix "${candidate}" "${root}"; then
scripts/update-agent-assets.sh 274 851db696b62d case "$(uname -s)/$(uname -m)" in
scripts/update-agent-assets.sh 950 1c780a546a27 [[ -z "${link}" || "${link}" == /* ]] && part="${link}" || part="${entry%/*}/${link}"
scripts/update-agent-assets.sh 959 1d5afafa1445 if { [ -f "${entry}" ] || [ -L "${entry}" ]; } && [[ "${resolved}" != "${HOME}/.local/lib/
scripts/update-agent-assets.sh 982 851db696b62d case "$(uname -s)/$(uname -m)" in
[exit 0]
```

## 4. The baseline diff: exactly the seven owned rows go
```console
$ git diff origin/main...HEAD -- scripts/lint-comparisons-baseline.tsv
diff --git a/scripts/lint-comparisons-baseline.tsv b/scripts/lint-comparisons-baseline.tsv
index cca63d44..bf950ca5 100644
--- a/scripts/lint-comparisons-baseline.tsv
+++ b/scripts/lint-comparisons-baseline.tsv
@@ -18,9 +18,6 @@ home/dot_local/bin/common/executable_herdr-agents	R3	06ee79c6acaf8c7295987ce0df5
 home/dot_local/bin/common/executable_herdr-agents	R3	b9fdf4394d550c9ab79dadac55f11ff21c58d33f97d3cfe346de62ba483df16b
 home/dot_local/bin/common/executable_herdr-agents	R3	de8d2d7c93d68b7d8ddeef07ba996751b9ea5d73923798f0e38f12e2bc6f335f
 home/dot_local/bin/common/executable_herdr-agents	R6	13c54d0bd6403f303661f90a3de5104417c000e49bec361a7f4d00f9b4b24e6a
-home/dot_local/bin/common/executable_remove-agent-asset	R1	5903a3cfc9310928d0438ee9dee4e09fc314e0c70d3d17cbd36297288b208d4f
-home/dot_local/bin/common/executable_remove-agent-asset	R1	5903a3cfc9310928d0438ee9dee4e09fc314e0c70d3d17cbd36297288b208d4f
-home/dot_local/bin/common/executable_remove-agent-asset	R1	ff2e0ca268ac61d911860ae79ea5165571fb624f3335912a0fd16bfc3b40912e
 home/dot_local/bin/common/executable_ua-symbol-coverage	R4	21421c95ee060bc6bb5566ae3f9d99179c27894bada70ecebc8942626d9297ac
 home/dot_local/bin/common/executable_ua-symbol-coverage	R4	33dc904ec7d1b06003787977929e7fcc6112aa697412572541cbe1e55fe2172e
 home/dot_local/bin/common/executable_ua-symbol-coverage	R4	340e40b4e14f074669d9a68610907f91c4239069ef404c1dee2db4c62bd0190f
@@ -70,10 +67,6 @@ scripts/require-crit-review.py	R4	4485ef36304b22adf0a481d0ab45031f304d197c997ad6
 scripts/require-crit-review.py	R4	5fe2a097290c874909ecd58a2bad704aa11e36fca5510619096f26e067042299
 scripts/require-crit-review.py	R4	6bad1276f1c726c98b39ca8bc14525951b26918b3b071d69d8d94cdf8a51e1e0
 scripts/require-crit-review.py	R4	a7b373231c29c04d17bfaa0565c4735cbcfdc362f1e8d39222458806f93b0b5b
-scripts/update-agent-assets.sh	R1	1c780a546a27e0a65e2d6b2a6431df9c1fa1a84006a5cdf62579d97724ee8966
-scripts/update-agent-assets.sh	R1	1d5afafa1445dd075af19378727e3660a631287a1f251e19b0c9c450ca381e45
-scripts/update-agent-assets.sh	R2	851db696b62d42ddfefa5fbc21df66a2bf37a6906e735a2a802cf1b1b54e878a
-scripts/update-agent-assets.sh	R2	851db696b62d42ddfefa5fbc21df66a2bf37a6906e735a2a802cf1b1b54e878a
 scripts/upgrade-tools.sh	R1	89aa4b2e31a61a753be955b4b05bae4a5b58289c3c5b2b08a14ae9c6783c81ac
 scripts/validate-agent-assets.py	R4	11097b8bd9cfd9b6fa06a1dac729c1b48bd7fe63dab2e05dcbee3d69933cec35
 scripts/validate-agent-assets.py	R4	31eed231c1d39f8fc59edda83230fd0218d8e092e10435ff5601f6955bb341b5
[exit 0]
```

## 4r. Red at 205fe85c: this branch's test modules in a scratch worktree of the base, each selector by exact id (outside the sandbox)
```console
$ S=<the session scratchpad>; git worktree add --detach -q "$S/red-a03" 205fe85c; cp tests/unit/test_remove_agent_asset.py tests/unit/test_update_agent_assets.py "$S/red-a03/tests/unit/"; shasum -a 256 tests/unit/test_remove_agent_asset.py tests/unit/test_update_agent_assets.py "$S/red-a03/tests/unit/test_remove_agent_asset.py" "$S/red-a03/tests/unit/test_update_agent_assets.py"
5ed45a4407cdbaca02744410a22698f1584ee0bc41c6b2d33c895c1e122f2ea4  tests/unit/test_remove_agent_asset.py
613b7d54bd5433004eff13cc32ec31e150c205d9ef6b6a0ea6c964ec39ac3e33  tests/unit/test_update_agent_assets.py
5ed45a4407cdbaca02744410a22698f1584ee0bc41c6b2d33c895c1e122f2ea4  $S/red-a03/tests/unit/test_remove_agent_asset.py
613b7d54bd5433004eff13cc32ec31e150c205d9ef6b6a0ea6c964ec39ac3e33  $S/red-a03/tests/unit/test_update_agent_assets.py
$ bash "$S/red-ids.sh" "$S/red-a03" <the five ids of §6b>
tree=205fe85c19c03750fe3551bb96e084e9f0a676b6 dirty=2
$ uv run python -m unittest tests.unit.test_remove_agent_asset.RemoveAgentAssetTest.test_path_has_prefix_folds_both_paths_before_comparing
exit=1
FAIL: test_path_has_prefix_folds_both_paths_before_comparing
AssertionError: 1 != 0
Ran 1 test in 0.034s
FAILED (failures=1)
$ uv run python -m unittest tests.unit.test_remove_agent_asset.RemoveAgentAssetTest.test_a_safe_root_is_not_inside_itself_in_any_spelling
exit=1
FAIL: test_a_safe_root_is_not_inside_itself_in_any_spelling (argv=('path_is_in_safe_root', '<user-temp>/remove-agent-asset-test-bakk3xaq/home/.agents/'))
AssertionError: 1 != 0
FAIL: test_a_safe_root_is_not_inside_itself_in_any_spelling (argv=('path_is_in_safe_root', '<user-temp>/remove-agent-asset-test-bakk3xaq/home/.agents/.'))
AssertionError: 1 != 0
FAIL: test_a_safe_root_is_not_inside_itself_in_any_spelling (argv=('path_has_prefix', '<user-temp>/remove-agent-asset-test-bakk3xaq/home/.claude/plugins/ca
AssertionError: 1 != 0
Ran 1 test in 0.435s
FAILED (failures=3)
$ uv run python -m unittest tests.unit.test_update_agent_assets.UpdateAgentAssetsTest.test_npm_s_own_absolute_link_stays_under_a_home_with_a_trailing_slash
exit=1
FAIL: test_npm_s_own_absolute_link_stays_under_a_home_with_a_trailing_slash
AssertionError: 'Moving' unexpectedly found in '\n==> omp\nMoving <user-temp>/tmp8gw_7cfi//.local/bin/omp to <user-temp>/tmp8g
Ran 1 test in 1.035s
FAILED (failures=1)
$ uv run python -m unittest tests.unit.test_update_agent_assets.UpdateAgentAssetsTest.test_npm_s_own_relative_link_stays_under_a_home_with_a_trailing_slash
exit=1
FAIL: test_npm_s_own_relative_link_stays_under_a_home_with_a_trailing_slash
AssertionError: 'Moving' unexpectedly found in '\n==> omp\nMoving <user-temp>/tmpr0zg5dpb//.local/bin/omp to <user-temp>/tmpr0
Ran 1 test in 0.371s
FAILED (failures=1)
$ uv run python -m unittest tests.unit.test_update_agent_assets.UpdateAgentAssetsTest.test_the_platform_cases_read_no_path_operand
exit=1
FAIL: test_the_platform_cases_read_no_path_operand
AssertionError: Lists differ: [] != ['case "$(uname -s)/$(uname -m)" in', 'case "$(uname -s)/$(uname -m)" in']
Ran 1 test in 0.059s
FAILED (failures=1)
$ git worktree remove --force "$S/red-a03"; echo "removed=$?"
removed=0
```

## 5. The lint: the changed-scope gate, the two scripts with no baseline, and --all
```console
$ uv run --no-project python -I scripts/lint-comparisons.py; echo "gate exit=$?"; uv run --no-project python -I scripts/lint-comparisons.py --all --baseline /dev/null home/dot_local/bin/common/executable_remove-agent-asset scripts/update-agent-assets.sh; echo "baseline-free exit=$?"; uv run --no-project python -I scripts/lint-comparisons.py --all | /usr/bin/grep -c -e '(baseline)' ; uv run --no-project python -I scripts/lint-comparisons.py --all | /usr/bin/grep -e 'stale baseline row' -e 'executable_remove-agent-asset:' -e 'update-agent-assets.sh:'; echo "no stale row and no hit in the two scripts: grep exit=$?"
warning: scripts/orchestrator/regime-ci.py:65: R6 an identifier is interpolated into a regex (grep -E on $name; re.* on an f-string)
warning: scripts/orchestrator/regime-ci.py:71: R4 Python compares a path or URL by its string form
warning: scripts/orchestrator/regime-ci.py:72: R4 Python compares a path or URL by its string form
warning: scripts/orchestrator/regime-ci.py:90: R4 Python compares a path or URL by its string form
warning: scripts/orchestrator/regime-ci.py:246: R4 Python compares a path or URL by its string form
warning: 5 unbaselined hit(s) and 0 stale row(s) in unchanged files
gate exit=0
baseline-free exit=0
86
no stale row and no hit in the two scripts: grep exit=1
[exit 0]
```

## 6. The remover module (inside the sandbox)
```console
$ uv run python -m unittest tests/unit/test_remove_agent_asset.py tests/unit/test_lint_comparisons.py 2>&1 | tail -4
----------------------------------------------------------------------
Ran 37 tests in 48.697s

OK
[exit 0]
```

## 6a. The Check: both test modules, -v (outside the sandbox: update_omp's mktemp -d is refused inside it)
```console
$ uv run python -m unittest tests/unit/test_remove_agent_asset.py tests/unit/test_update_agent_assets.py -v
test_a_safe_root_is_not_inside_itself_in_any_spelling (tests.unit.test_remove_agent_asset.RemoveAgentAssetTest.test_a_safe_root_is_not_inside_itself_in_any_spelling) ... ok
test_all_paths_are_preflighted_before_any_deletion (tests.unit.test_remove_agent_asset.RemoveAgentAssetTest.test_all_paths_are_preflighted_before_any_deletion) ... ok
test_brew_refuses_ambiguous_formula (tests.unit.test_remove_agent_asset.RemoveAgentAssetTest.test_brew_refuses_ambiguous_formula) ... ok
test_brew_uses_uninstall_for_unambiguous_formula (tests.unit.test_remove_agent_asset.RemoveAgentAssetTest.test_brew_uses_uninstall_for_unambiguous_formula) ... ok
test_crit_plugin_falls_back_to_data_path_but_not_config (tests.unit.test_remove_agent_asset.RemoveAgentAssetTest.test_crit_plugin_falls_back_to_data_path_but_not_config) ... ok
test_default_and_explicit_dry_run_print_without_mutating (tests.unit.test_remove_agent_asset.RemoveAgentAssetTest.test_default_and_explicit_dry_run_print_without_mutating) ... ok
test_hcom_dry_run_without_uv_prints_the_plan (tests.unit.test_remove_agent_asset.RemoveAgentAssetTest.test_hcom_dry_run_without_uv_prints_the_plan) ... ok
test_hcom_removal_deletes_the_recorded_binary (tests.unit.test_remove_agent_asset.RemoveAgentAssetTest.test_hcom_removal_deletes_the_recorded_binary) ... ok
test_hcom_removal_deletes_the_retained_wheel (tests.unit.test_remove_agent_asset.RemoveAgentAssetTest.test_hcom_removal_deletes_the_retained_wheel) ... ok
test_hcom_removal_skips_the_uninstall_when_uv_has_no_hcom_and_removes_the_rest (tests.unit.test_remove_agent_asset.RemoveAgentAssetTest.test_hcom_removal_skips_the_uninstall_when_uv_has_no_hcom_and_removes_the_rest) ... ok
test_hcom_removal_uninstalls_the_uv_receipt (tests.unit.test_remove_agent_asset.RemoveAgentAssetTest.test_hcom_removal_uninstalls_the_uv_receipt) ... ok
test_hcom_removal_uninstalls_the_uv_tool_environment (tests.unit.test_remove_agent_asset.RemoveAgentAssetTest.test_hcom_removal_uninstalls_the_uv_tool_environment) ... ok
test_hcom_removal_without_uv_reports_and_removes_nothing (tests.unit.test_remove_agent_asset.RemoveAgentAssetTest.test_hcom_removal_without_uv_reports_and_removes_nothing) ... ok
test_integration_uses_verified_herdr_uninstall (tests.unit.test_remove_agent_asset.RemoveAgentAssetTest.test_integration_uses_verified_herdr_uninstall) ... ok
test_invalid_manifest_is_rejected (tests.unit.test_remove_agent_asset.RemoveAgentAssetTest.test_invalid_manifest_is_rejected) ... ok
test_parameterized_step_removal_preserves_sibling_identity (tests.unit.test_remove_agent_asset.RemoveAgentAssetTest.test_parameterized_step_removal_preserves_sibling_identity) ... ok
test_path_has_prefix_folds_both_paths_before_comparing (tests.unit.test_remove_agent_asset.RemoveAgentAssetTest.test_path_has_prefix_folds_both_paths_before_comparing) ... ok
test_plugin_uses_verified_claude_uninstall (tests.unit.test_remove_agent_asset.RemoveAgentAssetTest.test_plugin_uses_verified_claude_uninstall) ... ok
test_plugin_uses_verified_codex_remove (tests.unit.test_remove_agent_asset.RemoveAgentAssetTest.test_plugin_uses_verified_codex_remove) ... ok
test_recorded_symlink_is_removed_without_following_target (tests.unit.test_remove_agent_asset.RemoveAgentAssetTest.test_recorded_symlink_is_removed_without_following_target) ... ok
test_tampered_manifest_outside_safe_roots_is_refused (tests.unit.test_remove_agent_asset.RemoveAgentAssetTest.test_tampered_manifest_outside_safe_roots_is_refused) ... ok
test_unknown_step_lists_known_steps_without_guessing (tests.unit.test_remove_agent_asset.RemoveAgentAssetTest.test_unknown_step_lists_known_steps_without_guessing) ... ok
test_yes_removes_only_recorded_path_and_preserves_other_steps (tests.unit.test_remove_agent_asset.RemoveAgentAssetTest.test_yes_removes_only_recorded_path_and_preserves_other_steps) ... ok
test_a_link_target_escaping_the_npm_prefix_is_refused (tests.unit.test_update_agent_assets.UpdateAgentAssetsTest.test_a_link_target_escaping_the_npm_prefix_is_refused) ... ok
test_npm_s_own_absolute_link_stays_under_a_home_with_a_trailing_slash (tests.unit.test_update_agent_assets.UpdateAgentAssetsTest.test_npm_s_own_absolute_link_stays_under_a_home_with_a_trailing_slash) ... ok
test_npm_s_own_relative_link_stays_under_a_home_with_a_trailing_slash (tests.unit.test_update_agent_assets.UpdateAgentAssetsTest.test_npm_s_own_relative_link_stays_under_a_home_with_a_trailing_slash) ... ok
test_omp_version_check_accepts_the_branded_omp_slash_version_form (tests.unit.test_update_agent_assets.UpdateAgentAssetsTest.test_omp_version_check_accepts_the_branded_omp_slash_version_form) ... ok
test_the_platform_cases_read_no_path_operand (tests.unit.test_update_agent_assets.UpdateAgentAssetsTest.test_the_platform_cases_read_no_path_operand) ... ok
test_update_hcom_downloads_verifies_the_wheel_hash_and_installs_at_the_pin (tests.unit.test_update_agent_assets.UpdateAgentAssetsTest.test_update_hcom_downloads_verifies_the_wheel_hash_and_installs_at_the_pin) ... ok
test_update_hcom_drops_the_retained_wheel_when_uv_fails_so_the_next_run_retries (tests.unit.test_update_agent_assets.UpdateAgentAssetsTest.test_update_hcom_drops_the_retained_wheel_when_uv_fails_so_the_next_run_retries) ... ok
test_update_hcom_keeps_the_wheel_uv_records_as_its_source (tests.unit.test_update_agent_assets.UpdateAgentAssetsTest.test_update_hcom_keeps_the_wheel_uv_records_as_its_source) ... ok
test_update_hcom_reinstalls_a_pinned_install_without_its_retained_wheel (tests.unit.test_update_agent_assets.UpdateAgentAssetsTest.test_update_hcom_reinstalls_a_pinned_install_without_its_retained_wheel) ... ok
test_update_omp_downloads_verifies_the_tarball_hash_and_installs_at_the_pin (tests.unit.test_update_agent_assets.UpdateAgentAssetsTest.test_update_omp_downloads_verifies_the_tarball_hash_and_installs_at_the_pin) ... ok
test_update_omp_moves_an_entry_npm_does_not_own_aside_and_puts_it_back_when_the_install_fails (tests.unit.test_update_agent_assets.UpdateAgentAssetsTest.test_update_omp_moves_an_entry_npm_does_not_own_aside_and_puts_it_back_when_the_install_fails) ... ok
test_updates_use_managed_binaries_when_path_is_shadowed (tests.unit.test_update_agent_assets.UpdateAgentAssetsTest.test_updates_use_managed_binaries_when_path_is_shadowed) ... ok

----------------------------------------------------------------------
Ran 35 tests in 59.123s

OK
[exit 0]
```

## 6b. The five new selectors by exact id, green at the code head (outside the sandbox)
```console
$ bash $S/red-ids.sh "$PWD" tests.unit.test_remove_agent_asset.RemoveAgentAssetTest.test_path_has_prefix_folds_both_paths_before_comparing tests.unit.test_remove_agent_asset.RemoveAgentAssetTest.test_a_safe_root_is_not_inside_itself_in_any_spelling tests.unit.test_update_agent_assets.UpdateAgentAssetsTest.test_npm_s_own_absolute_link_stays_under_a_home_with_a_trailing_slash tests.unit.test_update_agent_assets.UpdateAgentAssetsTest.test_npm_s_own_relative_link_stays_under_a_home_with_a_trailing_slash tests.unit.test_update_agent_assets.UpdateAgentAssetsTest.test_the_platform_cases_read_no_path_operand
tree=9a8e24697b032f1051062aaf53d0af2343257e98 dirty=5
$ uv run python -m unittest tests.unit.test_remove_agent_asset.RemoveAgentAssetTest.test_path_has_prefix_folds_both_paths_before_comparing
exit=0
Ran 1 test in 0.147s
OK
$ uv run python -m unittest tests.unit.test_remove_agent_asset.RemoveAgentAssetTest.test_a_safe_root_is_not_inside_itself_in_any_spelling
exit=0
Ran 1 test in 1.966s
OK
$ uv run python -m unittest tests.unit.test_update_agent_assets.UpdateAgentAssetsTest.test_npm_s_own_absolute_link_stays_under_a_home_with_a_trailing_slash
exit=0
Ran 1 test in 0.223s
OK
$ uv run python -m unittest tests.unit.test_update_agent_assets.UpdateAgentAssetsTest.test_npm_s_own_relative_link_stays_under_a_home_with_a_trailing_slash
exit=0
Ran 1 test in 0.246s
OK
$ uv run python -m unittest tests.unit.test_update_agent_assets.UpdateAgentAssetsTest.test_the_platform_cases_read_no_path_operand
exit=0
Ran 1 test in 0.053s
OK
[exit 0]
```

## 7. The runtime-health module, which drives ensure_crit_cli through a uname fake (outside the sandbox)
```console
$ uv run python -m unittest tests/unit/test_runtime_health.py 2>&1 | tail -3
Ran 55 tests in 46.932s

OK
[exit 0]
```

## 8. shellcheck -x (the CI form), shfmt -d, /bin/bash -n (bash 3.2) on both scripts; ruff on both tests
```console
$ shellcheck -x scripts/update-agent-assets.sh home/dot_local/bin/common/executable_remove-agent-asset && echo 'shellcheck clean'; shfmt --indent 4 --space-redirects -d scripts/update-agent-assets.sh home/dot_local/bin/common/executable_remove-agent-asset && echo 'shfmt clean'; /bin/bash --version | head -1; /bin/bash -n scripts/update-agent-assets.sh && /bin/bash -n home/dot_local/bin/common/executable_remove-agent-asset && echo 'bash 3.2 parses both'; ruff format --config ruff.toml --check tests/unit/test_remove_agent_asset.py tests/unit/test_update_agent_assets.py; ruff check --config ruff.toml --output-format concise tests/unit/test_update_agent_assets.py tests/unit/test_remove_agent_asset.py; echo '--- origin/main:'; git show origin/main:tests/unit/test_remove_agent_asset.py | ruff check --config ruff.toml --output-format concise --stdin-filename tests/unit/test_remove_agent_asset.py -
shellcheck clean
shfmt clean
GNU bash, version 3.2.57(1)-release (arm64-apple-darwin26)
bash 3.2 parses both
2 files already formatted
tests/unit/test_remove_agent_asset.py:1:1: EXE001 Shebang is present but file is not executable
tests/unit/test_remove_agent_asset.py:4:1: I001 [*] Import block is un-sorted or un-formatted
Found 2 errors.
[*] 1 fixable with `--fix`.
--- origin/main:
tests/unit/test_remove_agent_asset.py:1:1: EXE001 Shebang is present but file is not executable
tests/unit/test_remove_agent_asset.py:4:1: I001 [*] Import block is un-sorted or un-formatted
Found 2 errors.
[*] 1 fixable with `--fix`.
[exit 1]
```

## 8a. normalize_node_path under /bin/bash 3.2 against a path.resolve reference (os.path.normpath with the leading // folded)
```console
$ for args in '/h/.local/bin|../lib/x/bin/omp' '/h//.local/bin|/abs/./y/../z' '/h/.local/bin|' '/|../../..' '/h/.local/bin|//a//b/' '/h/.local/lib/node_modules/@oh-my-pi/pi-coding-agent'; do IFS='|' read -r a b <<< "$args"; if [ "$args" = "${args%|*}" ]; then set -- "$a"; else set -- "$a" "$b"; fi; out=$(/bin/bash -c 'set -Eeuo pipefail; source scripts/update-agent-assets.sh; normalize_node_path "$@"' bash "$@"); ref=$(uv run --no-project python -I -c 'import os, sys; print(os.path.normpath("/" + os.path.join(*sys.argv[1:]).lstrip("/")))' "$@"); echo "[$*] bash3.2=$out reference=$ref"; [ "$out" = "$ref" ] || exit 1; done
[/h/.local/bin ../lib/x/bin/omp] bash3.2=/h/.local/lib/x/bin/omp reference=/h/.local/lib/x/bin/omp
[/h//.local/bin /abs/./y/../z] bash3.2=/abs/z reference=/abs/z
[/h/.local/bin ] bash3.2=/h/.local/bin reference=/h/.local/bin
[/ ../../..] bash3.2=/ reference=/
[/h/.local/bin //a//b/] bash3.2=/a/b reference=/a/b
[/h/.local/lib/node_modules/@oh-my-pi/pi-coding-agent] bash3.2=/h/.local/lib/node_modules/@oh-my-pi/pi-coding-agent reference=/h/.local/lib/node_modules/@oh-my-pi/pi-coding-agent
[exit 0]
```

## 9. Caps against origin/main (merge-base 205fe85c)
```console
$ git diff --numstat origin/main...HEAD; git diff --numstat origin/main...HEAD | awk -F '\t' '$3 ~ /^\.orchestration\// {next} $3 ~ /^tests\// {t += $1 + $2; next} {o += $1 + $2} END {printf "outside tests/ and .orchestration/: %d of 120\nunder tests/: %d of 400\n", o, t}'
69	0	.orchestration/dotfiles-T129-assets-omp-hcom-followup-a03/task.md
7	6	home/dot_local/bin/common/executable_remove-agent-asset
0	7	scripts/lint-comparisons-baseline.tsv
40	24	scripts/update-agent-assets.sh
30	0	tests/unit/test_remove_agent_asset.py
40	3	tests/unit/test_update_agent_assets.py
outside tests/ and .orchestration/: 84 of 120
under tests/: 73 of 400
[exit 0]
```
