---
task_id: dotfiles-T129-assets-omp-hcom-followup-a01
seat: claude-standard-dot-a007
---

# Validation: dotfiles-T129-assets-omp-hcom-followup-a01

Every command ran from the worktree `.claude/worktrees/worker-c` on the branch `tools/assets-hcom-receipt` (from PR #388's head b49da6dd; the code commit ad57e280), inside the sandbox; `MAIN` names the main checkout and `T` the task id. The output is verbatim, with the home directory replaced by `~`; each block ends with the exit status of the command shown. The updater tests run with this evidence-run `mktemp` shim first on PATH (macOS `mktemp` without a template ignores TMPDIR, and the Claude sandbox denies its default directory); the shim is not in the repository:

```sh
#!/bin/sh
# Evidence-run shim, not in the repository: macOS mktemp without a template ignores TMPDIR, and the Claude sandbox
# denies its default directory; give the two template-less forms a TMPDIR template.
if [ "$#" -eq 0 ]; then exec /usr/bin/mktemp "${TMPDIR:-/tmp}/tmp.XXXXXXXX"; fi
if [ "$#" -eq 1 ] && [ "$1" = "-d" ]; then exec /usr/bin/mktemp -d "${TMPDIR:-/tmp}/tmp.XXXXXXXX"; fi
exec /usr/bin/mktemp "$@"
```

## 1. Task file and task copy

```console
$ shasum -a 256 "$MAIN/.orchestration/tasks/$T.md" ".orchestration/$T/task.md"; cmp "$MAIN/.orchestration/tasks/$T.md" ".orchestration/$T/task.md" && echo byte-identical
abd85d3295bfc03b738c765409aaea695ce51c8cb4f9ebbc758eddad5f398777  $MAIN/.orchestration/tasks/dotfiles-T129-assets-omp-hcom-followup-a01.md
abd85d3295bfc03b738c765409aaea695ce51c8cb4f9ebbc758eddad5f398777  .orchestration/dotfiles-T129-assets-omp-hcom-followup-a01/task.md
byte-identical
(exit 0)
$ UV_OFFLINE=1 uv run --no-project --with pyyaml python -I scripts/orchestrator/task-consistency-check.py --root "$PWD" "$MAIN/.orchestration/tasks/$T.md"
dotfiles-T129-assets-omp-hcom-followup-a01.md: OK
(exit 0)
$ git rev-parse HEAD; git log --oneline -1
b49da6dd3c9e9a93301af4c0d3dd62b058852abf
b49da6dd Merge branch 'main' into feat/pinned-omp-hcom
(exit 0)
```

## 2. The diff against b49da6dd

```console
$ git diff b49da6dd3c9e9a93301af4c0d3dd62b058852abf -- scripts tests
diff --git a/scripts/update-agent-assets.sh b/scripts/update-agent-assets.sh
index 1a289a54..4d48a6e5 100755
--- a/scripts/update-agent-assets.sh
+++ b/scripts/update-agent-assets.sh
@@ -952,11 +952,11 @@ function update_omp() (
 )
 
 #
-# @description Verify the pinned platform wheel before uv installs hcom.
+# @description Verify the pinned platform wheel before uv installs hcom, and keep it where uv's receipt points.
 # @exitcode 1 The download checksum or installed version differs from its pin.
 #
 function update_hcom() (
-    local url expected installed download_dir wheel actual
+    local url expected installed download_dir wheel actual wheel_dir
     case "$(uname -s)/$(uname -m)" in
     Darwin/arm64 | Darwin/aarch64) url="${HCOM_DARWIN_ARM64_URL}" expected="${HCOM_DARWIN_ARM64_SHA256}" ;;
     Darwin/x86_64 | Darwin/amd64) url="${HCOM_DARWIN_AMD64_URL}" expected="${HCOM_DARWIN_AMD64_SHA256}" ;;
@@ -986,13 +986,18 @@ function update_hcom() (
         printf 'hcom checksum mismatch: expected %s, got %s.\n' "${expected}" "${actual}" >&2
         return 1
     fi
+    # uv's receipt records this path as hcom's source and `uv tool upgrade` re-reads it, so the verified wheel moves
+    # to a managed path that outlives the run.
+    wheel_dir="${HOME}/.local/share/agent-assets/hcom"
+    mkdir -p "${wheel_dir}" && mv -f "${wheel}" "${wheel_dir}/" || return
+    wheel="${wheel_dir}/${url##*/}"
     uv tool install --force "${wheel}" || return
     installed="$("${HOME}/.local/bin/hcom" --version 2> /dev/null | awk 'NR == 1 { print $NF }')" || installed=none
     if [ "${installed}" != "${HCOM_PIN_VERSION}" ]; then
         printf 'hcom version mismatch: expected %s, got %s.\n' "${HCOM_PIN_VERSION}" "${installed}" >&2
         return 1
     fi
-    manifest_record "update_hcom" installer "${HCOM_PIN_VERSION}" "${HOME}/.local/bin/hcom" -- "uv tool install --force <verified-hcom-wheel>"
+    manifest_record "update_hcom" installer "${HCOM_PIN_VERSION}" "${HOME}/.local/bin/hcom" "${wheel}" -- "uv tool install --force <verified-hcom-wheel>"
 )
 
 #
diff --git a/tests/unit/test_update_agent_assets.py b/tests/unit/test_update_agent_assets.py
index 2687ebb7..f0bc2c42 100644
--- a/tests/unit/test_update_agent_assets.py
+++ b/tests/unit/test_update_agent_assets.py
@@ -132,12 +132,18 @@ class UpdateAgentAssetsTest(unittest.TestCase):
             artifact = Path(records[1]["argv"][-1])
             self.assertEqual(".tgz" if tool == "omp" else ".whl", artifact.suffix)
             self.assertEqual(digest, records[1]["sha256"])
-            self.assertFalse(artifact.exists())
-            self.assertFalse(artifact.parent.exists())
+            wheels = home / ".local/share/agent-assets/hcom"
+            if tool == "omp":
+                self.assertFalse(artifact.exists())
+                self.assertFalse(artifact.parent.exists())
+            else:
+                # uv's receipt names the wheel as hcom's source, so the verified wheel outlives the run (local:b49da6d:1).
+                self.assertEqual(wheels, artifact.parent)
+                self.assertEqual(digest, hashlib.sha256(artifact.read_bytes()).hexdigest())
             receipt_path = home / ".agents/.installed-manifest.json"
             receipt = json.loads(receipt_path.read_text())["steps"][f"update_{tool}"]
             self.assertEqual(pin, receipt["source_version"])
-            self.assertEqual([str(target)], receipt["paths"])
+            self.assertEqual([str(target)] + ([] if tool == "omp" else [str(artifact)]), receipt["paths"])
             repeated = update()
             self.assertEqual(0, repeated.returncode, repeated.stdout + repeated.stderr)
             self.assertIn("already installed", repeated.stdout)
@@ -145,6 +151,8 @@ class UpdateAgentAssetsTest(unittest.TestCase):
 
             reset()
             receipt_path.unlink()
+            for kept in wheels.glob("*"):
+                kept.unlink()
             bad_hash = "0" * 64
             drifted_hash = update(checksum=bad_hash)
             self.assertNotEqual(0, drifted_hash.returncode)
@@ -152,6 +160,7 @@ class UpdateAgentAssetsTest(unittest.TestCase):
             self.assertIn(digest, drifted_hash.stdout + drifted_hash.stderr)
             self.assertEqual(["curl"], [row["tool"] for row in calls()])
             self.assertFalse(Path(calls()[0]["argv"][-1]).parent.exists())
+            self.assertEqual([], list(wheels.glob("*")))  # a wheel that fails its hash never reaches the managed path
             self.assertFalse(receipt_path.exists())
 
             reset()
@@ -160,7 +169,8 @@ class UpdateAgentAssetsTest(unittest.TestCase):
             self.assertIn(pin, drifted_version.stdout + drifted_version.stderr)
             self.assertIn("0.0.1", drifted_version.stdout + drifted_version.stderr)
             self.assertEqual(2, len(calls()))
-            self.assertFalse(Path(calls()[1]["argv"][-1]).parent.exists())
+            # The omp tarball goes with its run; the hcom wheel stays where uv's receipt points.
+            self.assertEqual(tool == "hcom", Path(calls()[1]["argv"][-1]).exists())
             self.assertFalse(receipt_path.exists())
             reset()
             skipped = update(prefix="has_command() { return 1; }; ")
@@ -206,6 +216,11 @@ class UpdateAgentAssetsTest(unittest.TestCase):
                 self.exercise_update("hcom", platform)
         self.exercise_update("hcom", "Plan9/unknown", unsupported=True)
 
+    def test_update_hcom_keeps_the_wheel_uv_records_as_its_source(self):
+        # local:b49da6d:1: `uv tool upgrade` re-reads the wheel uv's receipt names, so the verified wheel stays at the
+        # managed path and the asset manifest lists it; exercise_update asserts the path, its hash and the entry.
+        self.exercise_update("hcom", "Darwin/arm64")
+
     def test_updates_use_managed_binaries_when_path_is_shadowed(self):
         for tool in ("omp", "hcom"):
             for shadow_version in ("pin", "0.0.0"):
(exit 0)
$ git diff --numstat b49da6dd3c9e9a93301af4c0d3dd62b058852abf -- scripts tests
8	3	scripts/update-agent-assets.sh
19	4	tests/unit/test_update_agent_assets.py
(exit 0)
```

## 3. This branch's tests against b49da6dd's script

```console
$ PATH="$TMPDIR/t129h/shim:$PATH" uv run python -m unittest tests.unit.test_update_agent_assets -v   # this branch's tests against b49da6dd's scripts/update-agent-assets.sh; the shim is pasted in the record
test_omp_version_check_accepts_the_branded_omp_slash_version_form ... ok
test_update_hcom_downloads_verifies_the_wheel_hash_and_installs_at_the_pin ... 
  test_update_hcom_downloads_verifies_the_wheel_hash_and_installs_at_the_pin (platform='Darwin/arm64') ... FAIL
  test_update_hcom_downloads_verifies_the_wheel_hash_and_installs_at_the_pin (platform='Darwin/x86_64') ... FAIL
  test_update_hcom_downloads_verifies_the_wheel_hash_and_installs_at_the_pin (platform='Linux/x86_64') ... FAIL
  test_update_hcom_downloads_verifies_the_wheel_hash_and_installs_at_the_pin (platform='Linux/aarch64') ... FAIL
test_update_hcom_keeps_the_wheel_uv_records_as_its_source ... FAIL
test_update_omp_downloads_verifies_the_tarball_hash_and_installs_at_the_pin ... ok
test_updates_use_managed_binaries_when_path_is_shadowed ... 
  test_updates_use_managed_binaries_when_path_is_shadowed (tool='hcom', shadow_version='pin') ... FAIL
  test_updates_use_managed_binaries_when_path_is_shadowed (tool='hcom', shadow_version='0.0.0') ... FAIL
FAIL: test_update_hcom_downloads_verifies_the_wheel_hash_and_installs_at_the_pin (platform='Darwin/arm64')
AssertionError: PosixPath('/tmp/claude-501/tmpd59t92zz/.local/share/agent-assets/hcom') != PosixPath('/tmp/claude-501/tmp.6p59QTkx')
FAIL: test_update_hcom_downloads_verifies_the_wheel_hash_and_installs_at_the_pin (platform='Darwin/x86_64')
AssertionError: PosixPath('/tmp/claude-501/tmpl9imiaha/.local/share/agent-assets/hcom') != PosixPath('/tmp/claude-501/tmp.7HXvruTo')
FAIL: test_update_hcom_downloads_verifies_the_wheel_hash_and_installs_at_the_pin (platform='Linux/x86_64')
AssertionError: PosixPath('/tmp/claude-501/tmprz0ejl85/.local/share/agent-assets/hcom') != PosixPath('/tmp/claude-501/tmp.4SmlhcND')
FAIL: test_update_hcom_downloads_verifies_the_wheel_hash_and_installs_at_the_pin (platform='Linux/aarch64')
AssertionError: PosixPath('/tmp/claude-501/tmpezktvfaq/.local/share/agent-assets/hcom') != PosixPath('/tmp/claude-501/tmp.wYDRE4Ys')
FAIL: test_update_hcom_keeps_the_wheel_uv_records_as_its_source
AssertionError: PosixPath('/tmp/claude-501/tmphilw4pm8/.local/share/agent-assets/hcom') != PosixPath('/tmp/claude-501/tmp.1PA2jzMD')
FAIL: test_updates_use_managed_binaries_when_path_is_shadowed (tool='hcom', shadow_version='pin')
AssertionError: PosixPath('/tmp/claude-501/tmpj7unoykc/.local/share/agent-assets/hcom') != PosixPath('/tmp/claude-501/tmp.gnWJAZb0')
FAIL: test_updates_use_managed_binaries_when_path_is_shadowed (tool='hcom', shadow_version='0.0.0')
AssertionError: PosixPath('/tmp/claude-501/tmplbivlf67/.local/share/agent-assets/hcom') != PosixPath('/tmp/claude-501/tmp.nBSY3Gk6')
Ran 5 tests in 5.242s
FAILED (failures=7)
(exit 1)
```

## 4. One mutant per part of the fix

```python
"""local:b49da6d:1: the updater tests against b49da6dd's script and one mutant per part of the fix."""
import subprocess, sys
from pathlib import Path
script = Path("scripts/update-agent-assets.sh")
fixed = script.read_text()
before = subprocess.run(["git", "show", "b49da6dd3c9e9a93301af4c0d3dd62b058852abf:" + str(script)], capture_output=True, text=True, check=True).stdout
def mutate(old, new):
    assert fixed.count(old) == 1, old
    return fixed.replace(old, new)
MOVE = '    mkdir -p "${wheel_dir}" && mv -f "${wheel}" "${wheel_dir}/" || return\n    wheel="${wheel_dir}/${url##*/}"\n'
variants = [
    ("b49da6dd's script (the wheel stays in the run's temporary directory)", before),
    ("mutant: the wheel is copied, uv installs the temporary file", mutate(MOVE, '    mkdir -p "${wheel_dir}" && cp "${wheel}" "${wheel_dir}/" || return\n')),
    ("mutant: the manifest leaves the wheel out", mutate('"${HOME}/.local/bin/hcom" "${wheel}" --', '"${HOME}/.local/bin/hcom" --')),
    ("mutant: the wheel moves before its hash is checked", mutate(MOVE, "").replace('    actual="$(shasum -a 256 "${wheel}"', MOVE.replace("wheel=", "wheel=") + '    actual="$(shasum -a 256 "${wheel}"', 1)),
]
try:
    for name, body in variants:
        script.write_text(body)
        r = subprocess.run(["uv", "run", "python", "-m", "unittest", "tests.unit.test_update_agent_assets"], capture_output=True, text=True)
        tail = [x for x in r.stderr.splitlines() if x.startswith(("OK", "FAILED"))]
        print(f"{name}: rc={r.returncode} {' | '.join(tail)}")
finally:
    script.write_text(fixed)
print("restored byte-identical:", script.read_text() == fixed)
```

```console
$ PATH="$TMPDIR/t129h/shim:$PATH" uv run --offline --no-project python -I mutants.py   # from the worktree root; the script is pasted in the record
b49da6dd's script (the wheel stays in the run's temporary directory): rc=1 FAILED (failures=7)
mutant: the wheel is copied, uv installs the temporary file: rc=1 FAILED (failures=7)
mutant: the manifest leaves the wheel out: rc=1 FAILED (failures=7)
mutant: the wheel moves before its hash is checked: rc=1 FAILED (failures=7)
restored byte-identical: True
(exit 0)
```

## 5. The Check: the three modules, and test_runtime_health's baseline on b49da6dd

Eight agmsg tests of test_runtime_health fail in this sandbox on this branch and identically on b49da6dd's script: they pin PATH to `{bin}:/usr/bin:/bin`, so the shim cannot reach them, and macOS `mktemp` fails there. CI's Linux runners decide them; the change does not touch agmsg.

```console
$ PATH="$TMPDIR/t129h/shim:$PATH" uv run python -m unittest tests/unit/test_update_agent_assets.py tests/unit/test_asset_manifest.py tests/unit/test_runtime_health.py -v
test_omp_version_check_accepts_the_branded_omp_slash_version_form (tests.unit.test_update_agent_assets.UpdateAgentAssetsTest.test_omp_version_check_accepts_the_branded_omp_slash_version_form) ... ok
test_update_hcom_downloads_verifies_the_wheel_hash_and_installs_at_the_pin (tests.unit.test_update_agent_assets.UpdateAgentAssetsTest.test_update_hcom_downloads_verifies_the_wheel_hash_and_installs_at_the_pin) ... ok
test_update_hcom_keeps_the_wheel_uv_records_as_its_source (tests.unit.test_update_agent_assets.UpdateAgentAssetsTest.test_update_hcom_keeps_the_wheel_uv_records_as_its_source) ... ok
test_update_omp_downloads_verifies_the_tarball_hash_and_installs_at_the_pin (tests.unit.test_update_agent_assets.UpdateAgentAssetsTest.test_update_omp_downloads_verifies_the_tarball_hash_and_installs_at_the_pin) ... ok
test_updates_use_managed_binaries_when_path_is_shadowed (tests.unit.test_update_agent_assets.UpdateAgentAssetsTest.test_updates_use_managed_binaries_when_path_is_shadowed) ... ok
test_chezmoi_rendered_updater_uses_exported_source_root (tests.unit.test_asset_manifest.AssetManifestTest.test_chezmoi_rendered_updater_uses_exported_source_root) ... ok
test_chezmoi_rendered_updater_uses_inlined_manifest_library (tests.unit.test_asset_manifest.AssetManifestTest.test_chezmoi_rendered_updater_uses_inlined_manifest_library) ... ok
test_chezmoi_wrapper_renders_shebang_and_source_root (tests.unit.test_asset_manifest.AssetManifestTest.test_chezmoi_wrapper_renders_shebang_and_source_root) ... ok
test_failed_atomic_commit_leaves_previous_manifest_intact (tests.unit.test_asset_manifest.AssetManifestTest.test_failed_atomic_commit_leaves_previous_manifest_intact) ... ok
test_records_schema_two_steps_and_replaces_one_whole_entry (tests.unit.test_asset_manifest.AssetManifestTest.test_records_schema_two_steps_and_replaces_one_whole_entry) ... ok
test_rendered_updater_fails_when_no_source_root_is_valid (tests.unit.test_asset_manifest.AssetManifestTest.test_rendered_updater_fails_when_no_source_root_is_valid) ... ok
test_same_run_mise_repairs_preserve_both_identity_steps (tests.unit.test_asset_manifest.AssetManifestTest.test_same_run_mise_repairs_preserve_both_identity_steps) ... ok
test_two_real_install_steps_record_under_fake_home (tests.unit.test_asset_manifest.AssetManifestTest.test_two_real_install_steps_record_under_fake_home) ... ok
test_unwritable_destination_warns_once_without_failing (tests.unit.test_asset_manifest.AssetManifestTest.test_unwritable_destination_warns_once_without_failing) ... ok
test_updater_direct_source_resolves_repository_root (tests.unit.test_asset_manifest.AssetManifestTest.test_updater_direct_source_resolves_repository_root) ... ok
test_updater_has_one_recording_call_for_each_install_step (tests.unit.test_asset_manifest.AssetManifestTest.test_updater_has_one_recording_call_for_each_install_step) ... ok
test_agent_asset_update_removes_node_global_shadows_before_agent_commands (tests.unit.test_runtime_health.RuntimeHealthTest.test_agent_asset_update_removes_node_global_shadows_before_agent_commands) ... ok
test_agent_asset_update_repairs_broken_claude_with_npm_backend (tests.unit.test_runtime_health.RuntimeHealthTest.test_agent_asset_update_repairs_broken_claude_with_npm_backend) ... ok
test_agent_asset_update_runs_gh_extension_ensure (tests.unit.test_runtime_health.RuntimeHealthTest.test_agent_asset_update_runs_gh_extension_ensure) ... ok
test_agent_launchers_do_not_hardcode_model_ids (tests.unit.test_runtime_health.RuntimeHealthTest.test_agent_launchers_do_not_hardcode_model_ids) ... ok
test_agmsg_accepts_a_store_the_installer_creates_and_notes_run_changes (tests.unit.test_runtime_health.RuntimeHealthTest.test_agmsg_accepts_a_store_the_installer_creates_and_notes_run_changes) ... FAIL
test_agmsg_already_pinned_skips_download (tests.unit.test_runtime_health.RuntimeHealthTest.test_agmsg_already_pinned_skips_download) ... ok
test_agmsg_checksum_mismatch_fails_closed (tests.unit.test_runtime_health.RuntimeHealthTest.test_agmsg_checksum_mismatch_fails_closed) ... FAIL
test_agmsg_fresh_install_populates_skill_and_records_manifest (tests.unit.test_runtime_health.RuntimeHealthTest.test_agmsg_fresh_install_populates_skill_and_records_manifest) ... FAIL
test_agmsg_migrates_marker_less_legacy_dir_without_losing_live_state (tests.unit.test_runtime_health.RuntimeHealthTest.test_agmsg_migrates_marker_less_legacy_dir_without_losing_live_state) ... ERROR
test_agmsg_migration_reports_an_installer_that_mutates_live_state (tests.unit.test_runtime_health.RuntimeHealthTest.test_agmsg_migration_reports_an_installer_that_mutates_live_state) ... ERROR
test_agmsg_refuses_to_install_when_the_state_snapshot_is_empty (tests.unit.test_runtime_health.RuntimeHealthTest.test_agmsg_refuses_to_install_when_the_state_snapshot_is_empty) ... FAIL
test_agmsg_refuses_to_install_without_tar (tests.unit.test_runtime_health.RuntimeHealthTest.test_agmsg_refuses_to_install_without_tar) ... ok
test_agmsg_reports_an_installer_that_leaves_the_wrong_version (tests.unit.test_runtime_health.RuntimeHealthTest.test_agmsg_reports_an_installer_that_leaves_the_wrong_version) ... FAIL
test_agmsg_update_aborts_when_install_corrupts_live_state (tests.unit.test_runtime_health.RuntimeHealthTest.test_agmsg_update_aborts_when_install_corrupts_live_state) ... FAIL
test_agmsg_update_never_touches_teams_db_run (tests.unit.test_runtime_health.RuntimeHealthTest.test_agmsg_update_never_touches_teams_db_run) ... ok
test_client_bashrc_treats_private_sources_as_optional (tests.unit.test_runtime_health.RuntimeHealthTest.test_client_bashrc_treats_private_sources_as_optional) ... ok
test_codex_crit_normalizes_managed_marketplace_mode (tests.unit.test_runtime_health.RuntimeHealthTest.test_codex_crit_normalizes_managed_marketplace_mode) ... ok
test_codex_superpowers_reports_login_step_when_curated_catalog_is_missing (tests.unit.test_runtime_health.RuntimeHealthTest.test_codex_superpowers_reports_login_step_when_curated_catalog_is_missing) ... ok
test_crit_fails_without_an_install_when_the_download_fails (tests.unit.test_runtime_health.RuntimeHealthTest.test_crit_fails_without_an_install_when_the_download_fails) ... ok
test_crit_never_promotes_a_staged_binary_that_prints_the_banner_but_fails (tests.unit.test_runtime_health.RuntimeHealthTest.test_crit_never_promotes_a_staged_binary_that_prints_the_banner_but_fails) ... ok
test_crit_refuses_a_replaced_release_whose_checksums_txt_matches (tests.unit.test_runtime_health.RuntimeHealthTest.test_crit_refuses_a_replaced_release_whose_checksums_txt_matches) ... ok
test_crit_replaces_an_installed_binary_that_cannot_report_its_version (tests.unit.test_runtime_health.RuntimeHealthTest.test_crit_replaces_an_installed_binary_that_cannot_report_its_version) ... ok
test_crit_replaces_an_installed_binary_that_prints_the_banner_but_fails (tests.unit.test_runtime_health.RuntimeHealthTest.test_crit_replaces_an_installed_binary_that_prints_the_banner_but_fails) ... ok
test_darwin_crit_checksum_failure_preserves_existing_binary (tests.unit.test_runtime_health.RuntimeHealthTest.test_darwin_crit_checksum_failure_preserves_existing_binary) ... ok
test_darwin_crit_install_is_pinned_atomic_and_recorded (tests.unit.test_runtime_health.RuntimeHealthTest.test_darwin_crit_install_is_pinned_atomic_and_recorded) ... ok
test_doctor_has_no_github_role_check (tests.unit.test_runtime_health.RuntimeHealthTest.test_doctor_has_no_github_role_check) ... ok
test_doctor_reports_claude_sandbox_prerequisites (tests.unit.test_runtime_health.RuntimeHealthTest.test_doctor_reports_claude_sandbox_prerequisites) ... ok
test_doctor_required_optional_and_healthy_statuses (tests.unit.test_runtime_health.RuntimeHealthTest.test_doctor_required_optional_and_healthy_statuses) ... ok
test_linux_crit_checksum_failure_preserves_existing_binary (tests.unit.test_runtime_health.RuntimeHealthTest.test_linux_crit_checksum_failure_preserves_existing_binary) ... ok
test_linux_crit_correct_version_is_download_free (tests.unit.test_runtime_health.RuntimeHealthTest.test_linux_crit_correct_version_is_download_free) ... ok
test_linux_crit_failure_does_not_leak_cleanup_trap (tests.unit.test_runtime_health.RuntimeHealthTest.test_linux_crit_failure_does_not_leak_cleanup_trap) ... ok
test_linux_crit_install_is_pinned_atomic_and_recorded (tests.unit.test_runtime_health.RuntimeHealthTest.test_linux_crit_install_is_pinned_atomic_and_recorded) ... ok
test_linux_crit_prefers_pinned_target_over_older_path_binary (tests.unit.test_runtime_health.RuntimeHealthTest.test_linux_crit_prefers_pinned_target_over_older_path_binary) ... ok
test_make_doctor_does_not_skip_runtime_check_when_deployed_root_is_missing (tests.unit.test_runtime_health.RuntimeHealthTest.test_make_doctor_does_not_skip_runtime_check_when_deployed_root_is_missing) ... ok
test_make_doctor_passes_repair_variable_to_runtime_check (tests.unit.test_runtime_health.RuntimeHealthTest.test_make_doctor_passes_repair_variable_to_runtime_check) ... ok
test_make_doctor_propagates_runtime_drift_after_tool_checks (tests.unit.test_runtime_health.RuntimeHealthTest.test_make_doctor_propagates_runtime_drift_after_tool_checks) ... ok
test_make_update_pulls_clean_main_before_apply (tests.unit.test_runtime_health.RuntimeHealthTest.test_make_update_pulls_clean_main_before_apply) ... ok
test_make_update_reports_unmerged_feature_branch_before_branch_notice (tests.unit.test_runtime_health.RuntimeHealthTest.test_make_update_reports_unmerged_feature_branch_before_branch_notice) ... ok
test_make_update_reports_unmerged_index_before_dirty_notice (tests.unit.test_runtime_health.RuntimeHealthTest.test_make_update_reports_unmerged_index_before_dirty_notice) ... ok
test_make_update_skips_dirty_main_with_manual_pull_notice (tests.unit.test_runtime_health.RuntimeHealthTest.test_make_update_skips_dirty_main_with_manual_pull_notice) ... ok
test_upgrade_fails_and_keeps_the_backup_when_a_partial_install_cannot_be_removed (tests.unit.test_runtime_health.RuntimeHealthTest.test_upgrade_fails_and_keeps_the_backup_when_a_partial_install_cannot_be_removed) ... ok
test_upgrade_fails_when_the_final_install_fails_after_a_rebuild (tests.unit.test_runtime_health.RuntimeHealthTest.test_upgrade_fails_when_the_final_install_fails_after_a_rebuild) ... ok
test_upgrade_fails_when_the_node_marker_cannot_be_written (tests.unit.test_runtime_health.RuntimeHealthTest.test_upgrade_fails_when_the_node_marker_cannot_be_written) ... ok
test_upgrade_failure_after_a_successful_install_only_warns (tests.unit.test_runtime_health.RuntimeHealthTest.test_upgrade_failure_after_a_successful_install_only_warns) ... ok
test_upgrade_homebrew_verifies_attestations_when_gh_is_present (tests.unit.test_runtime_health.RuntimeHealthTest.test_upgrade_homebrew_verifies_attestations_when_gh_is_present) ... ok
test_upgrade_network_only_phases_warn_and_the_mise_phase_still_runs (tests.unit.test_runtime_health.RuntimeHealthTest.test_upgrade_network_only_phases_warn_and_the_mise_phase_still_runs) ... ok
test_upgrade_never_restores_an_undeletable_backup_over_a_completed_rebuild (tests.unit.test_runtime_health.RuntimeHealthTest.test_upgrade_never_restores_an_undeletable_backup_over_a_completed_rebuild) ... ok
test_upgrade_rebuilds_npm_tools_when_the_node_marker_differs (tests.unit.test_runtime_health.RuntimeHealthTest.test_upgrade_rebuilds_npm_tools_when_the_node_marker_differs) ... ok
test_upgrade_required_failures_are_nonzero_and_independent (tests.unit.test_runtime_health.RuntimeHealthTest.test_upgrade_required_failures_are_nonzero_and_independent) ... ok
test_upgrade_restores_a_rebuild_backup_left_by_a_killed_run (tests.unit.test_runtime_health.RuntimeHealthTest.test_upgrade_restores_a_rebuild_backup_left_by_a_killed_run) ... ok
test_upgrade_restores_the_npm_tool_when_the_rebuild_is_interrupted (tests.unit.test_runtime_health.RuntimeHealthTest.test_upgrade_restores_the_npm_tool_when_the_rebuild_is_interrupted) ... ok
test_upgrade_runs_mise_against_the_applied_host_config_and_edits_no_file (tests.unit.test_runtime_health.RuntimeHealthTest.test_upgrade_runs_mise_against_the_applied_host_config_and_edits_no_file) ... ok
test_upgrade_self_updates_mise_to_its_latest_release (tests.unit.test_runtime_health.RuntimeHealthTest.test_upgrade_self_updates_mise_to_its_latest_release) ... ok
test_upgrade_skips_every_phase_when_ci_is_true (tests.unit.test_runtime_health.RuntimeHealthTest.test_upgrade_skips_every_phase_when_ci_is_true) ... ok
test_upgrade_skips_unavailable_mise_self_update (tests.unit.test_runtime_health.RuntimeHealthTest.test_upgrade_skips_unavailable_mise_self_update) ... ok

======================================================================
ERROR: test_agmsg_migrates_marker_less_legacy_dir_without_losing_live_state (tests.unit.test_runtime_health.RuntimeHealthTest.test_agmsg_migrates_marker_less_legacy_dir_without_losing_live_state)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "~/Workspace/dotfiles/.claude/worktrees/worker-c/tests/unit/test_runtime_health.py", line 912, in test_agmsg_migrates_marker_less_legacy_dir_without_losing_live_state
    log = (repo / "commands.log").read_text()
  File "~/.local/share/mise/installs/python/latest/lib/python3.15/pathlib/__init__.py", line 986, in read_text
    with self.open(mode='r', encoding=encoding, errors=errors, newline=newline) as f:
         ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "~/.local/share/mise/installs/python/latest/lib/python3.15/pathlib/__init__.py", line 970, in open
    return io.open(self, mode, buffering, encoding, errors, newline)
           ~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
FileNotFoundError: [Errno 2] No such file or directory: '/tmp/claude-501/runtime-health-test-i4ojug9v/agmsg-repo/commands.log'

======================================================================
ERROR: test_agmsg_migration_reports_an_installer_that_mutates_live_state (tests.unit.test_runtime_health.RuntimeHealthTest.test_agmsg_migration_reports_an_installer_that_mutates_live_state)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "~/Workspace/dotfiles/.claude/worktrees/worker-c/tests/unit/test_runtime_health.py", line 978, in test_agmsg_migration_reports_an_installer_that_mutates_live_state
    self.assertNotIn("update=true", (repo / "commands.log").read_text())
                                    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "~/.local/share/mise/installs/python/latest/lib/python3.15/pathlib/__init__.py", line 986, in read_text
    with self.open(mode='r', encoding=encoding, errors=errors, newline=newline) as f:
         ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "~/.local/share/mise/installs/python/latest/lib/python3.15/pathlib/__init__.py", line 970, in open
    return io.open(self, mode, buffering, encoding, errors, newline)
           ~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
FileNotFoundError: [Errno 2] No such file or directory: '/tmp/claude-501/runtime-health-test-171n9fgc/agmsg-repo/commands.log'

======================================================================
FAIL: test_agmsg_accepts_a_store_the_installer_creates_and_notes_run_changes (tests.unit.test_runtime_health.RuntimeHealthTest.test_agmsg_accepts_a_store_the_installer_creates_and_notes_run_changes)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "~/Workspace/dotfiles/.claude/worktrees/worker-c/tests/unit/test_runtime_health.py", line 1014, in test_agmsg_accepts_a_store_the_installer_creates_and_notes_run_changes
    self.assertNotIn("installer failed", output)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 'installer failed' unexpectedly found in '\n==> agmsg\nmktemp: mkstemp failed on /var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/tmp.LD1BqcodUl: Operation not permitted\nagmsg: could not snapshot the live state under /tmp/claude-501/runtime-health-test-u790jsn4/agmsg-home/.agents/skills/agmsg; nothing was installed\nagmsg installer failed (installed: none); see the reason above.\n'

======================================================================
FAIL: test_agmsg_checksum_mismatch_fails_closed (tests.unit.test_runtime_health.RuntimeHealthTest.test_agmsg_checksum_mismatch_fails_closed)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "~/Workspace/dotfiles/.claude/worktrees/worker-c/tests/unit/test_runtime_health.py", line 860, in test_agmsg_checksum_mismatch_fails_closed
    self.assertIn("checksum mismatch", result.stdout + result.stderr)
    ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 'checksum mismatch' not found in '\n==> agmsg\nmktemp: mkstemp failed on /var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/tmp.Aklyfo5HS7: Operation not permitted\nagmsg installer failed (installed: none); see the reason above.\n'

======================================================================
FAIL: test_agmsg_fresh_install_populates_skill_and_records_manifest (tests.unit.test_runtime_health.RuntimeHealthTest.test_agmsg_fresh_install_populates_skill_and_records_manifest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "~/Workspace/dotfiles/.claude/worktrees/worker-c/tests/unit/test_runtime_health.py", line 819, in test_agmsg_fresh_install_populates_skill_and_records_manifest
    self.assertNotIn("installer failed", result.stdout + result.stderr)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 'installer failed' unexpectedly found in '\n==> agmsg\nmktemp: mkstemp failed on /var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/tmp.PaUNtWjrts: Operation not permitted\nagmsg installer failed (installed: none); see the reason above.\n'

======================================================================
FAIL: test_agmsg_refuses_to_install_when_the_state_snapshot_is_empty (tests.unit.test_runtime_health.RuntimeHealthTest.test_agmsg_refuses_to_install_when_the_state_snapshot_is_empty)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "~/Workspace/dotfiles/.claude/worktrees/worker-c/tests/unit/test_runtime_health.py", line 1063, in test_agmsg_refuses_to_install_when_the_state_snapshot_is_empty
    self.assertIn("hashed fewer live-state files than exist", output)
    ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 'hashed fewer live-state files than exist' not found in '\n==> agmsg\nmktemp: mkstemp failed on /var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/tmp.dWCMFe33w6: Operation not permitted\nagmsg: could not snapshot the live state under /tmp/claude-501/runtime-health-test-jbg806qg/agmsg-home/.agents/skills/agmsg; nothing was installed\nagmsg installer failed (installed: 1.0.0); see the reason above.\n'

======================================================================
FAIL: test_agmsg_reports_an_installer_that_leaves_the_wrong_version (tests.unit.test_runtime_health.RuntimeHealthTest.test_agmsg_reports_an_installer_that_leaves_the_wrong_version)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "~/Workspace/dotfiles/.claude/worktrees/worker-c/tests/unit/test_runtime_health.py", line 1033, in test_agmsg_reports_an_installer_that_leaves_the_wrong_version
    self.assertIn(
    ~~~~~~~~~~~~~^
        "agmsg: install.sh --cmd agmsg --agent-type claude-code left VERSION 9.9.9 (want 1.5.0)",
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        output,
        ^^^^^^^
    )
    ^
AssertionError: 'agmsg: install.sh --cmd agmsg --agent-type claude-code left VERSION 9.9.9 (want 1.5.0)' not found in '\n==> agmsg\nmktemp: mkstemp failed on /var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/tmp.kq9j5V5um1: Operation not permitted\nagmsg installer failed (installed: none); see the reason above.\n'

======================================================================
FAIL: test_agmsg_update_aborts_when_install_corrupts_live_state (tests.unit.test_runtime_health.RuntimeHealthTest.test_agmsg_update_aborts_when_install_corrupts_live_state)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "~/Workspace/dotfiles/.claude/worktrees/worker-c/tests/unit/test_runtime_health.py", line 946, in test_agmsg_update_aborts_when_install_corrupts_live_state
    self.assertIn(
    ~~~~~~~~~~~~~^
        "install.sh --update --cmd agmsg --agent-type claude-code changed or removed existing live state", output
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
AssertionError: 'install.sh --update --cmd agmsg --agent-type claude-code changed or removed existing live state' not found in '\n==> agmsg\nmktemp: mkstemp failed on /var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/tmp.DzpZ93xgZd: Operation not permitted\nagmsg: could not snapshot the live state under /tmp/claude-501/runtime-health-test-xnyqdi5r/agmsg-home/.agents/skills/agmsg; nothing was installed\nagmsg installer failed (installed: 1.0.0); see the reason above.\n'

----------------------------------------------------------------------
Ran 71 tests in 52.500s

FAILED (failures=6, errors=2)
(exit 1)
```

```console
$ PATH="$TMPDIR/t129h/shim:$PATH" uv run python -m unittest tests/unit/test_runtime_health.py -v   # against b49da6dd's scripts/update-agent-assets.sh, the baseline in this sandbox
test_agmsg_accepts_a_store_the_installer_creates_and_notes_run_changes ... FAIL
test_agmsg_checksum_mismatch_fails_closed ... FAIL
test_agmsg_fresh_install_populates_skill_and_records_manifest ... FAIL
test_agmsg_migrates_marker_less_legacy_dir_without_losing_live_state ... ERROR
test_agmsg_migration_reports_an_installer_that_mutates_live_state ... ERROR
test_agmsg_refuses_to_install_when_the_state_snapshot_is_empty ... FAIL
test_agmsg_reports_an_installer_that_leaves_the_wrong_version ... FAIL
test_agmsg_update_aborts_when_install_corrupts_live_state ... FAIL
Ran 55 tests in 42.716s
FAILED (failures=6, errors=2)
(exit 1)
```

```console
$ diff fail-base.txt fail-branch.txt && echo "SAME FAILING SET"   # the failing tests of test_runtime_health on b49da6dd's script and on this branch
SAME FAILING SET
(exit 0)
```

## 6. ShellCheck (with -x, as CI runs it), shfmt and Ruff

```console
$ shellcheck -x scripts/update-agent-assets.sh   # -x as CI runs it
(exit 0)
$ shfmt -i 4 -sr -d scripts/update-agent-assets.sh
(exit 0)
$ ruff format --config ruff.toml --check tests/unit/test_update_agent_assets.py; ruff check --config ruff.toml tests/unit/test_update_agent_assets.py
1 file already formatted
All checks passed!
(exit 0)
```

## 7. After PR #388 merged (f32c02b8): the rebase, the caps and the Check on the rebased head

The orchestrator's PING of 15:13:56Z named the merge. The branch is rebased onto origin/main without signing (the signed form failed to write the commit object in the sandbox and was aborted); the code diff is byte-identical to the one of section 2. Caps against origin/main: 8 + 3 = 11 changed lines outside `tests/` and `.orchestration/` (<= 120); 19 added under `tests/` (<= 400). The Check on the rebased head gives the results of section 5, with the same sandbox-only failing set.

```console
$ git rev-parse origin/main HEAD; git log --oneline -3
f32c02b81f788d04916b27840006e1409a7d1bcb
0ef37ff118a0f8a5cf927b51015860a2d2428000
0ef37ff1 chore(orchestration): dotfiles-T129-assets-omp-hcom-followup-a01 task copy and evidence before the rebase (ad57e280)
457984c9 fix(assets): keep the verified hcom wheel where uv's receipt points (T129 assets-omp-hcom followup a01)
f32c02b8 feat(agents): pin verified omp and hcom assets (#388)
(exit 0)
$ git -c commit.gpgsign=false rebase --onto origin/main b49da6dd3c9e9a93301af4c0d3dd62b058852abf tools/assets-hcom-receipt   # run earlier: "Successfully rebased and updated refs/heads/tools/assets-hcom-receipt."
$ git diff b49da6dd3c9e9a93301af4c0d3dd62b058852abf ad57e280104e71069352e128a2758551b7ca6316 -- scripts tests > d1.patch; git diff origin/main 457984c9 -- scripts tests > d2.patch; cmp d1.patch d2.patch && echo "the code diff is identical before and after the rebase"
the code diff is identical before and after the rebase
(exit 0)
$ git diff --numstat origin/main...HEAD
3	0	.orchestration/dotfiles-T129-assets-omp-hcom-followup-a01/autoskill.md
6	0	.orchestration/dotfiles-T129-assets-omp-hcom-followup-a01/learning.md
56	0	.orchestration/dotfiles-T129-assets-omp-hcom-followup-a01/report.md
23	0	.orchestration/dotfiles-T129-assets-omp-hcom-followup-a01/sandbox.md
83	0	.orchestration/dotfiles-T129-assets-omp-hcom-followup-a01/task.md
434	0	.orchestration/dotfiles-T129-assets-omp-hcom-followup-a01/validation.md
8	3	scripts/update-agent-assets.sh
19	4	tests/unit/test_update_agent_assets.py
(exit 0)
```

```console
$ PATH="$TMPDIR/t129h/shim:$PATH" uv run python -m unittest tests/unit/test_update_agent_assets.py tests/unit/test_asset_manifest.py tests/unit/test_runtime_health.py -v   # on the rebased head 0ef37ff1
test_omp_version_check_accepts_the_branded_omp_slash_version_form (tests.unit.test_update_agent_assets.UpdateAgentAssetsTest.test_omp_version_check_accepts_the_branded_omp_slash_version_form) ... ok
test_update_hcom_downloads_verifies_the_wheel_hash_and_installs_at_the_pin (tests.unit.test_update_agent_assets.UpdateAgentAssetsTest.test_update_hcom_downloads_verifies_the_wheel_hash_and_installs_at_the_pin) ... ok
test_update_hcom_keeps_the_wheel_uv_records_as_its_source (tests.unit.test_update_agent_assets.UpdateAgentAssetsTest.test_update_hcom_keeps_the_wheel_uv_records_as_its_source) ... ok
test_update_omp_downloads_verifies_the_tarball_hash_and_installs_at_the_pin (tests.unit.test_update_agent_assets.UpdateAgentAssetsTest.test_update_omp_downloads_verifies_the_tarball_hash_and_installs_at_the_pin) ... ok
test_updates_use_managed_binaries_when_path_is_shadowed (tests.unit.test_update_agent_assets.UpdateAgentAssetsTest.test_updates_use_managed_binaries_when_path_is_shadowed) ... ok
test_chezmoi_rendered_updater_uses_exported_source_root (tests.unit.test_asset_manifest.AssetManifestTest.test_chezmoi_rendered_updater_uses_exported_source_root) ... ok
test_chezmoi_rendered_updater_uses_inlined_manifest_library (tests.unit.test_asset_manifest.AssetManifestTest.test_chezmoi_rendered_updater_uses_inlined_manifest_library) ... ok
test_chezmoi_wrapper_renders_shebang_and_source_root (tests.unit.test_asset_manifest.AssetManifestTest.test_chezmoi_wrapper_renders_shebang_and_source_root) ... ok
test_failed_atomic_commit_leaves_previous_manifest_intact (tests.unit.test_asset_manifest.AssetManifestTest.test_failed_atomic_commit_leaves_previous_manifest_intact) ... ok
test_records_schema_two_steps_and_replaces_one_whole_entry (tests.unit.test_asset_manifest.AssetManifestTest.test_records_schema_two_steps_and_replaces_one_whole_entry) ... ok
test_rendered_updater_fails_when_no_source_root_is_valid (tests.unit.test_asset_manifest.AssetManifestTest.test_rendered_updater_fails_when_no_source_root_is_valid) ... ok
test_same_run_mise_repairs_preserve_both_identity_steps (tests.unit.test_asset_manifest.AssetManifestTest.test_same_run_mise_repairs_preserve_both_identity_steps) ... ok
test_two_real_install_steps_record_under_fake_home (tests.unit.test_asset_manifest.AssetManifestTest.test_two_real_install_steps_record_under_fake_home) ... ok
test_unwritable_destination_warns_once_without_failing (tests.unit.test_asset_manifest.AssetManifestTest.test_unwritable_destination_warns_once_without_failing) ... ok
test_updater_direct_source_resolves_repository_root (tests.unit.test_asset_manifest.AssetManifestTest.test_updater_direct_source_resolves_repository_root) ... ok
test_updater_has_one_recording_call_for_each_install_step (tests.unit.test_asset_manifest.AssetManifestTest.test_updater_has_one_recording_call_for_each_install_step) ... ok
test_agent_asset_update_removes_node_global_shadows_before_agent_commands (tests.unit.test_runtime_health.RuntimeHealthTest.test_agent_asset_update_removes_node_global_shadows_before_agent_commands) ... ok
test_agent_asset_update_repairs_broken_claude_with_npm_backend (tests.unit.test_runtime_health.RuntimeHealthTest.test_agent_asset_update_repairs_broken_claude_with_npm_backend) ... ok
test_agent_asset_update_runs_gh_extension_ensure (tests.unit.test_runtime_health.RuntimeHealthTest.test_agent_asset_update_runs_gh_extension_ensure) ... ok
test_agent_launchers_do_not_hardcode_model_ids (tests.unit.test_runtime_health.RuntimeHealthTest.test_agent_launchers_do_not_hardcode_model_ids) ... ok
test_agmsg_accepts_a_store_the_installer_creates_and_notes_run_changes (tests.unit.test_runtime_health.RuntimeHealthTest.test_agmsg_accepts_a_store_the_installer_creates_and_notes_run_changes) ... FAIL
test_agmsg_already_pinned_skips_download (tests.unit.test_runtime_health.RuntimeHealthTest.test_agmsg_already_pinned_skips_download) ... ok
test_agmsg_checksum_mismatch_fails_closed (tests.unit.test_runtime_health.RuntimeHealthTest.test_agmsg_checksum_mismatch_fails_closed) ... FAIL
test_agmsg_fresh_install_populates_skill_and_records_manifest (tests.unit.test_runtime_health.RuntimeHealthTest.test_agmsg_fresh_install_populates_skill_and_records_manifest) ... FAIL
test_agmsg_migrates_marker_less_legacy_dir_without_losing_live_state (tests.unit.test_runtime_health.RuntimeHealthTest.test_agmsg_migrates_marker_less_legacy_dir_without_losing_live_state) ... ERROR
test_agmsg_migration_reports_an_installer_that_mutates_live_state (tests.unit.test_runtime_health.RuntimeHealthTest.test_agmsg_migration_reports_an_installer_that_mutates_live_state) ... ERROR
test_agmsg_refuses_to_install_when_the_state_snapshot_is_empty (tests.unit.test_runtime_health.RuntimeHealthTest.test_agmsg_refuses_to_install_when_the_state_snapshot_is_empty) ... FAIL
test_agmsg_refuses_to_install_without_tar (tests.unit.test_runtime_health.RuntimeHealthTest.test_agmsg_refuses_to_install_without_tar) ... ok
test_agmsg_reports_an_installer_that_leaves_the_wrong_version (tests.unit.test_runtime_health.RuntimeHealthTest.test_agmsg_reports_an_installer_that_leaves_the_wrong_version) ... FAIL
test_agmsg_update_aborts_when_install_corrupts_live_state (tests.unit.test_runtime_health.RuntimeHealthTest.test_agmsg_update_aborts_when_install_corrupts_live_state) ... FAIL
test_agmsg_update_never_touches_teams_db_run (tests.unit.test_runtime_health.RuntimeHealthTest.test_agmsg_update_never_touches_teams_db_run) ... ok
test_client_bashrc_treats_private_sources_as_optional (tests.unit.test_runtime_health.RuntimeHealthTest.test_client_bashrc_treats_private_sources_as_optional) ... ok
test_codex_crit_normalizes_managed_marketplace_mode (tests.unit.test_runtime_health.RuntimeHealthTest.test_codex_crit_normalizes_managed_marketplace_mode) ... ok
test_codex_superpowers_reports_login_step_when_curated_catalog_is_missing (tests.unit.test_runtime_health.RuntimeHealthTest.test_codex_superpowers_reports_login_step_when_curated_catalog_is_missing) ... ok
test_crit_fails_without_an_install_when_the_download_fails (tests.unit.test_runtime_health.RuntimeHealthTest.test_crit_fails_without_an_install_when_the_download_fails) ... ok
test_crit_never_promotes_a_staged_binary_that_prints_the_banner_but_fails (tests.unit.test_runtime_health.RuntimeHealthTest.test_crit_never_promotes_a_staged_binary_that_prints_the_banner_but_fails) ... ok
test_crit_refuses_a_replaced_release_whose_checksums_txt_matches (tests.unit.test_runtime_health.RuntimeHealthTest.test_crit_refuses_a_replaced_release_whose_checksums_txt_matches) ... ok
test_crit_replaces_an_installed_binary_that_cannot_report_its_version (tests.unit.test_runtime_health.RuntimeHealthTest.test_crit_replaces_an_installed_binary_that_cannot_report_its_version) ... ok
test_crit_replaces_an_installed_binary_that_prints_the_banner_but_fails (tests.unit.test_runtime_health.RuntimeHealthTest.test_crit_replaces_an_installed_binary_that_prints_the_banner_but_fails) ... ok
test_darwin_crit_checksum_failure_preserves_existing_binary (tests.unit.test_runtime_health.RuntimeHealthTest.test_darwin_crit_checksum_failure_preserves_existing_binary) ... ok
test_darwin_crit_install_is_pinned_atomic_and_recorded (tests.unit.test_runtime_health.RuntimeHealthTest.test_darwin_crit_install_is_pinned_atomic_and_recorded) ... ok
test_doctor_has_no_github_role_check (tests.unit.test_runtime_health.RuntimeHealthTest.test_doctor_has_no_github_role_check) ... ok
test_doctor_reports_claude_sandbox_prerequisites (tests.unit.test_runtime_health.RuntimeHealthTest.test_doctor_reports_claude_sandbox_prerequisites) ... ok
test_doctor_required_optional_and_healthy_statuses (tests.unit.test_runtime_health.RuntimeHealthTest.test_doctor_required_optional_and_healthy_statuses) ... ok
test_linux_crit_checksum_failure_preserves_existing_binary (tests.unit.test_runtime_health.RuntimeHealthTest.test_linux_crit_checksum_failure_preserves_existing_binary) ... ok
test_linux_crit_correct_version_is_download_free (tests.unit.test_runtime_health.RuntimeHealthTest.test_linux_crit_correct_version_is_download_free) ... ok
test_linux_crit_failure_does_not_leak_cleanup_trap (tests.unit.test_runtime_health.RuntimeHealthTest.test_linux_crit_failure_does_not_leak_cleanup_trap) ... ok
test_linux_crit_install_is_pinned_atomic_and_recorded (tests.unit.test_runtime_health.RuntimeHealthTest.test_linux_crit_install_is_pinned_atomic_and_recorded) ... ok
test_linux_crit_prefers_pinned_target_over_older_path_binary (tests.unit.test_runtime_health.RuntimeHealthTest.test_linux_crit_prefers_pinned_target_over_older_path_binary) ... ok
test_make_doctor_does_not_skip_runtime_check_when_deployed_root_is_missing (tests.unit.test_runtime_health.RuntimeHealthTest.test_make_doctor_does_not_skip_runtime_check_when_deployed_root_is_missing) ... ok
test_make_doctor_passes_repair_variable_to_runtime_check (tests.unit.test_runtime_health.RuntimeHealthTest.test_make_doctor_passes_repair_variable_to_runtime_check) ... ok
test_make_doctor_propagates_runtime_drift_after_tool_checks (tests.unit.test_runtime_health.RuntimeHealthTest.test_make_doctor_propagates_runtime_drift_after_tool_checks) ... ok
test_make_update_pulls_clean_main_before_apply (tests.unit.test_runtime_health.RuntimeHealthTest.test_make_update_pulls_clean_main_before_apply) ... ok
test_make_update_reports_unmerged_feature_branch_before_branch_notice (tests.unit.test_runtime_health.RuntimeHealthTest.test_make_update_reports_unmerged_feature_branch_before_branch_notice) ... ok
test_make_update_reports_unmerged_index_before_dirty_notice (tests.unit.test_runtime_health.RuntimeHealthTest.test_make_update_reports_unmerged_index_before_dirty_notice) ... ok
test_make_update_skips_dirty_main_with_manual_pull_notice (tests.unit.test_runtime_health.RuntimeHealthTest.test_make_update_skips_dirty_main_with_manual_pull_notice) ... ok
test_upgrade_fails_and_keeps_the_backup_when_a_partial_install_cannot_be_removed (tests.unit.test_runtime_health.RuntimeHealthTest.test_upgrade_fails_and_keeps_the_backup_when_a_partial_install_cannot_be_removed) ... ok
test_upgrade_fails_when_the_final_install_fails_after_a_rebuild (tests.unit.test_runtime_health.RuntimeHealthTest.test_upgrade_fails_when_the_final_install_fails_after_a_rebuild) ... ok
test_upgrade_fails_when_the_node_marker_cannot_be_written (tests.unit.test_runtime_health.RuntimeHealthTest.test_upgrade_fails_when_the_node_marker_cannot_be_written) ... ok
test_upgrade_failure_after_a_successful_install_only_warns (tests.unit.test_runtime_health.RuntimeHealthTest.test_upgrade_failure_after_a_successful_install_only_warns) ... ok
test_upgrade_homebrew_verifies_attestations_when_gh_is_present (tests.unit.test_runtime_health.RuntimeHealthTest.test_upgrade_homebrew_verifies_attestations_when_gh_is_present) ... ok
test_upgrade_network_only_phases_warn_and_the_mise_phase_still_runs (tests.unit.test_runtime_health.RuntimeHealthTest.test_upgrade_network_only_phases_warn_and_the_mise_phase_still_runs) ... ok
test_upgrade_never_restores_an_undeletable_backup_over_a_completed_rebuild (tests.unit.test_runtime_health.RuntimeHealthTest.test_upgrade_never_restores_an_undeletable_backup_over_a_completed_rebuild) ... ok
test_upgrade_rebuilds_npm_tools_when_the_node_marker_differs (tests.unit.test_runtime_health.RuntimeHealthTest.test_upgrade_rebuilds_npm_tools_when_the_node_marker_differs) ... ok
test_upgrade_required_failures_are_nonzero_and_independent (tests.unit.test_runtime_health.RuntimeHealthTest.test_upgrade_required_failures_are_nonzero_and_independent) ... ok
test_upgrade_restores_a_rebuild_backup_left_by_a_killed_run (tests.unit.test_runtime_health.RuntimeHealthTest.test_upgrade_restores_a_rebuild_backup_left_by_a_killed_run) ... ok
test_upgrade_restores_the_npm_tool_when_the_rebuild_is_interrupted (tests.unit.test_runtime_health.RuntimeHealthTest.test_upgrade_restores_the_npm_tool_when_the_rebuild_is_interrupted) ... ok
test_upgrade_runs_mise_against_the_applied_host_config_and_edits_no_file (tests.unit.test_runtime_health.RuntimeHealthTest.test_upgrade_runs_mise_against_the_applied_host_config_and_edits_no_file) ... ok
test_upgrade_self_updates_mise_to_its_latest_release (tests.unit.test_runtime_health.RuntimeHealthTest.test_upgrade_self_updates_mise_to_its_latest_release) ... ok
test_upgrade_skips_every_phase_when_ci_is_true (tests.unit.test_runtime_health.RuntimeHealthTest.test_upgrade_skips_every_phase_when_ci_is_true) ... ok
test_upgrade_skips_unavailable_mise_self_update (tests.unit.test_runtime_health.RuntimeHealthTest.test_upgrade_skips_unavailable_mise_self_update) ... ok

======================================================================
ERROR: test_agmsg_migrates_marker_less_legacy_dir_without_losing_live_state (tests.unit.test_runtime_health.RuntimeHealthTest.test_agmsg_migrates_marker_less_legacy_dir_without_losing_live_state)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "~/Workspace/dotfiles/.claude/worktrees/worker-c/tests/unit/test_runtime_health.py", line 912, in test_agmsg_migrates_marker_less_legacy_dir_without_losing_live_state
    log = (repo / "commands.log").read_text()
  File "~/.local/share/mise/installs/python/latest/lib/python3.15/pathlib/__init__.py", line 986, in read_text
    with self.open(mode='r', encoding=encoding, errors=errors, newline=newline) as f:
         ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "~/.local/share/mise/installs/python/latest/lib/python3.15/pathlib/__init__.py", line 970, in open
    return io.open(self, mode, buffering, encoding, errors, newline)
           ~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
FileNotFoundError: [Errno 2] No such file or directory: '/tmp/claude-501/runtime-health-test-pqdlcg9y/agmsg-repo/commands.log'

======================================================================
ERROR: test_agmsg_migration_reports_an_installer_that_mutates_live_state (tests.unit.test_runtime_health.RuntimeHealthTest.test_agmsg_migration_reports_an_installer_that_mutates_live_state)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "~/Workspace/dotfiles/.claude/worktrees/worker-c/tests/unit/test_runtime_health.py", line 978, in test_agmsg_migration_reports_an_installer_that_mutates_live_state
    self.assertNotIn("update=true", (repo / "commands.log").read_text())
                                    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "~/.local/share/mise/installs/python/latest/lib/python3.15/pathlib/__init__.py", line 986, in read_text
    with self.open(mode='r', encoding=encoding, errors=errors, newline=newline) as f:
         ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "~/.local/share/mise/installs/python/latest/lib/python3.15/pathlib/__init__.py", line 970, in open
    return io.open(self, mode, buffering, encoding, errors, newline)
           ~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
FileNotFoundError: [Errno 2] No such file or directory: '/tmp/claude-501/runtime-health-test-1erl853v/agmsg-repo/commands.log'

======================================================================
FAIL: test_agmsg_accepts_a_store_the_installer_creates_and_notes_run_changes (tests.unit.test_runtime_health.RuntimeHealthTest.test_agmsg_accepts_a_store_the_installer_creates_and_notes_run_changes)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "~/Workspace/dotfiles/.claude/worktrees/worker-c/tests/unit/test_runtime_health.py", line 1014, in test_agmsg_accepts_a_store_the_installer_creates_and_notes_run_changes
    self.assertNotIn("installer failed", output)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 'installer failed' unexpectedly found in '\n==> agmsg\nmktemp: mkstemp failed on /var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/tmp.CM6jH2XTgb: Operation not permitted\nagmsg: could not snapshot the live state under /tmp/claude-501/runtime-health-test-9dhtcxi_/agmsg-home/.agents/skills/agmsg; nothing was installed\nagmsg installer failed (installed: none); see the reason above.\n'

======================================================================
FAIL: test_agmsg_checksum_mismatch_fails_closed (tests.unit.test_runtime_health.RuntimeHealthTest.test_agmsg_checksum_mismatch_fails_closed)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "~/Workspace/dotfiles/.claude/worktrees/worker-c/tests/unit/test_runtime_health.py", line 860, in test_agmsg_checksum_mismatch_fails_closed
    self.assertIn("checksum mismatch", result.stdout + result.stderr)
    ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 'checksum mismatch' not found in '\n==> agmsg\nmktemp: mkstemp failed on /var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/tmp.0eJHmF2VAD: Operation not permitted\nagmsg installer failed (installed: none); see the reason above.\n'

======================================================================
FAIL: test_agmsg_fresh_install_populates_skill_and_records_manifest (tests.unit.test_runtime_health.RuntimeHealthTest.test_agmsg_fresh_install_populates_skill_and_records_manifest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "~/Workspace/dotfiles/.claude/worktrees/worker-c/tests/unit/test_runtime_health.py", line 819, in test_agmsg_fresh_install_populates_skill_and_records_manifest
    self.assertNotIn("installer failed", result.stdout + result.stderr)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 'installer failed' unexpectedly found in '\n==> agmsg\nmktemp: mkstemp failed on /var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/tmp.07r6JucwZg: Operation not permitted\nagmsg installer failed (installed: none); see the reason above.\n'

======================================================================
FAIL: test_agmsg_refuses_to_install_when_the_state_snapshot_is_empty (tests.unit.test_runtime_health.RuntimeHealthTest.test_agmsg_refuses_to_install_when_the_state_snapshot_is_empty)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "~/Workspace/dotfiles/.claude/worktrees/worker-c/tests/unit/test_runtime_health.py", line 1063, in test_agmsg_refuses_to_install_when_the_state_snapshot_is_empty
    self.assertIn("hashed fewer live-state files than exist", output)
    ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 'hashed fewer live-state files than exist' not found in '\n==> agmsg\nmktemp: mkstemp failed on /var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/tmp.ePiJQNLiCi: Operation not permitted\nagmsg: could not snapshot the live state under /tmp/claude-501/runtime-health-test-4lfy6cg1/agmsg-home/.agents/skills/agmsg; nothing was installed\nagmsg installer failed (installed: 1.0.0); see the reason above.\n'

======================================================================
FAIL: test_agmsg_reports_an_installer_that_leaves_the_wrong_version (tests.unit.test_runtime_health.RuntimeHealthTest.test_agmsg_reports_an_installer_that_leaves_the_wrong_version)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "~/Workspace/dotfiles/.claude/worktrees/worker-c/tests/unit/test_runtime_health.py", line 1033, in test_agmsg_reports_an_installer_that_leaves_the_wrong_version
    self.assertIn(
    ~~~~~~~~~~~~~^
        "agmsg: install.sh --cmd agmsg --agent-type claude-code left VERSION 9.9.9 (want 1.5.0)",
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        output,
        ^^^^^^^
    )
    ^
AssertionError: 'agmsg: install.sh --cmd agmsg --agent-type claude-code left VERSION 9.9.9 (want 1.5.0)' not found in '\n==> agmsg\nmktemp: mkstemp failed on /var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/tmp.N6qPJkEWtC: Operation not permitted\nagmsg installer failed (installed: none); see the reason above.\n'

======================================================================
FAIL: test_agmsg_update_aborts_when_install_corrupts_live_state (tests.unit.test_runtime_health.RuntimeHealthTest.test_agmsg_update_aborts_when_install_corrupts_live_state)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "~/Workspace/dotfiles/.claude/worktrees/worker-c/tests/unit/test_runtime_health.py", line 946, in test_agmsg_update_aborts_when_install_corrupts_live_state
    self.assertIn(
    ~~~~~~~~~~~~~^
        "install.sh --update --cmd agmsg --agent-type claude-code changed or removed existing live state", output
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
AssertionError: 'install.sh --update --cmd agmsg --agent-type claude-code changed or removed existing live state' not found in '\n==> agmsg\nmktemp: mkstemp failed on /var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/tmp.GzmKJbcjvG: Operation not permitted\nagmsg: could not snapshot the live state under /tmp/claude-501/runtime-health-test-gy8ingit/agmsg-home/.agents/skills/agmsg; nothing was installed\nagmsg installer failed (installed: 1.0.0); see the reason above.\n'

----------------------------------------------------------------------
Ran 71 tests in 57.256s

FAILED (failures=6, errors=2)
(exit 1)
```

```console
$ diff fail-base.txt fail-rebased.txt && echo "SAME FAILING SET"   # the sandbox baseline of section 5 against the rebased head
SAME FAILING SET
(exit 0)
$ shellcheck -x scripts/update-agent-assets.sh
(exit 0)
$ shfmt -i 4 -sr -d scripts/update-agent-assets.sh
(exit 0)
```

## 8. Revise round 2 (C-50): the Bot's P2 4303212227, the code at 1537863d

Review 5558442187 of ee035dd4 (2026-10-17T15:19:11Z): an hcom installed at the pin before the wheel was kept passed the version guard, so its receipt (a deleted temporary wheel) was never repaired. The ACCEPTANCE `revise` of 15:44:29Z sends one round with its check: the guard also requires the retained wheel. `revise.yaml` records previous_head ee035dd4 and the check. Caps against origin/main: 10 + 4 = 14 changed lines outside `tests/` and `.orchestration/` (<= 120); 61 added under `tests/` (<= 400).

```console
$ PATH="$TMPDIR/t129h/shim:$PATH" uv run python -m unittest tests.unit.test_update_agent_assets.UpdateAgentAssetsTest.test_update_hcom_reinstalls_a_pinned_install_without_its_retained_wheel -v   # against ee035dd4's scripts/update-agent-assets.sh
test_update_hcom_reinstalls_a_pinned_install_without_its_retained_wheel (tests.unit.test_update_agent_assets.UpdateAgentAssetsTest.test_update_hcom_reinstalls_a_pinned_install_without_its_retained_wheel) ... FAIL
AssertionError: 'already installed' unexpectedly found in '\n==> hcom\nhcom 0.7.30 is already installed.\n'
Ran 1 test in 0.311s
FAILED (failures=1)
(exit 1)
```

```console
$ git diff ee035dd4e433041d8bc5bfc0a618388d9863213f -- scripts tests   # revise round 2
diff --git a/scripts/update-agent-assets.sh b/scripts/update-agent-assets.sh
index 4d48a6e5..31cdc4c6 100755
--- a/scripts/update-agent-assets.sh
+++ b/scripts/update-agent-assets.sh
@@ -972,8 +972,12 @@ function update_hcom() (
         return 0
     }
     section "hcom"
+    # uv's receipt records the wheel's path as hcom's source and `uv tool upgrade` re-reads it, so the verified wheel
+    # lives at a managed path that outlives the run.
+    wheel_dir="${HOME}/.local/share/agent-assets/hcom"
     installed="$("${HOME}/.local/bin/hcom" --version 2> /dev/null | awk 'NR == 1 { print $NF }')" || installed=none
-    if [ "${installed}" = "${HCOM_PIN_VERSION}" ]; then
+    # A pinned install without the retained wheel (one from before the wheel was kept) is reinstalled to repair it.
+    if [ "${installed}" = "${HCOM_PIN_VERSION}" ] && [ -f "${wheel_dir}/${url##*/}" ]; then
         printf 'hcom %s is already installed.\n' "${installed}"
         return 0
     fi
@@ -986,9 +990,6 @@ function update_hcom() (
         printf 'hcom checksum mismatch: expected %s, got %s.\n' "${expected}" "${actual}" >&2
         return 1
     fi
-    # uv's receipt records this path as hcom's source and `uv tool upgrade` re-reads it, so the verified wheel moves
-    # to a managed path that outlives the run.
-    wheel_dir="${HOME}/.local/share/agent-assets/hcom"
     mkdir -p "${wheel_dir}" && mv -f "${wheel}" "${wheel_dir}/" || return
     wheel="${wheel_dir}/${url##*/}"
     uv tool install --force "${wheel}" || return
diff --git a/tests/unit/test_update_agent_assets.py b/tests/unit/test_update_agent_assets.py
index f0bc2c42..29fc43d2 100644
--- a/tests/unit/test_update_agent_assets.py
+++ b/tests/unit/test_update_agent_assets.py
@@ -221,6 +221,48 @@ class UpdateAgentAssetsTest(unittest.TestCase):
         # managed path and the asset manifest lists it; exercise_update asserts the path, its hash and the entry.
         self.exercise_update("hcom", "Darwin/arm64")
 
+    def test_update_hcom_reinstalls_a_pinned_install_without_its_retained_wheel(self):
+        # The Bot's P2 4303212227: an hcom installed at the pin before the wheel was kept has a receipt that names a
+        # deleted temporary wheel, so the version alone does not skip it; once the wheel is retained it is skipped.
+        with tempfile.TemporaryDirectory() as directory:
+            home = Path(directory)
+            hcom = home / ".local/bin/hcom"
+            hcom.parent.mkdir(parents=True)
+            hcom.write_text("#!/bin/sh\nprintf 'hcom 0.7.30\\n'\n")
+            hcom.chmod(0o755)
+            payload = "reproduced wheel bytes; no real package\n"
+            digest = hashlib.sha256(payload.encode()).hexdigest()
+            log = home / "calls"
+            wheel = home / ".local/share/agent-assets/hcom/hcom-0.7.30-py3-none-any.whl"
+            stubs = (
+                "HCOM_PIN_VERSION=0.7.30; HCOM_LINUX_AMD64_URL=https://fixture.invalid/hcom-0.7.30-py3-none-any.whl; "
+                f"HCOM_LINUX_AMD64_SHA256={digest}; has_command() {{ return 0; }}; manifest_record() {{ :; }}; "
+                'uname() { if [ "$1" = -s ]; then echo Linux; else echo x86_64; fi; }; '
+                'curl() { printf %s "$PAYLOAD" > "${@: -1}"; echo curl >> "$CALLS"; }; '
+                'uv() { echo "uv $*" >> "$CALLS"; }; '
+            )
+
+            def update():
+                return subprocess.run(
+                    ["bash", "-c", 'source "$1"; ' + stubs + "update_hcom", "bash", str(UPDATER)],
+                    env=os.environ | {"HOME": directory, "PAYLOAD": payload, "CALLS": str(log)},
+                    capture_output=True,
+                    text=True,
+                    timeout=30,
+                    check=False,
+                )
+
+            repaired = update()
+            self.assertEqual(0, repaired.returncode, repaired.stdout + repaired.stderr)
+            self.assertNotIn("already installed", repaired.stdout)
+            self.assertEqual(["curl", f"uv tool install --force {wheel}"], log.read_text().splitlines())
+            self.assertEqual(digest, hashlib.sha256(wheel.read_bytes()).hexdigest())
+            log.write_text("")
+            skipped = update()
+            self.assertEqual(0, skipped.returncode, skipped.stdout + skipped.stderr)
+            self.assertIn("hcom 0.7.30 is already installed", skipped.stdout)
+            self.assertEqual("", log.read_text())
+
     def test_updates_use_managed_binaries_when_path_is_shadowed(self):
         for tool in ("omp", "hcom"):
             for shadow_version in ("pin", "0.0.0"):
(exit 0)
```

```console
$ PATH="$TMPDIR/t129h/shim:$PATH" uv run python -m unittest tests.unit.test_update_agent_assets.UpdateAgentAssetsTest.test_update_hcom_reinstalls_a_pinned_install_without_its_retained_wheel -v   # after the change
test_update_hcom_reinstalls_a_pinned_install_without_its_retained_wheel (tests.unit.test_update_agent_assets.UpdateAgentAssetsTest.test_update_hcom_reinstalls_a_pinned_install_without_its_retained_wheel) ... ok

----------------------------------------------------------------------
Ran 1 test in 0.207s

OK
(exit 0)
```

```console
$ PATH="$TMPDIR/t129h/shim:$PATH" uv run python -m unittest tests/unit/test_update_agent_assets.py tests/unit/test_asset_manifest.py tests/unit/test_runtime_health.py -v   # revise round 2
test_omp_version_check_accepts_the_branded_omp_slash_version_form (tests.unit.test_update_agent_assets.UpdateAgentAssetsTest.test_omp_version_check_accepts_the_branded_omp_slash_version_form) ... ok
test_update_hcom_downloads_verifies_the_wheel_hash_and_installs_at_the_pin (tests.unit.test_update_agent_assets.UpdateAgentAssetsTest.test_update_hcom_downloads_verifies_the_wheel_hash_and_installs_at_the_pin) ... ok
test_update_hcom_keeps_the_wheel_uv_records_as_its_source (tests.unit.test_update_agent_assets.UpdateAgentAssetsTest.test_update_hcom_keeps_the_wheel_uv_records_as_its_source) ... ok
test_update_hcom_reinstalls_a_pinned_install_without_its_retained_wheel (tests.unit.test_update_agent_assets.UpdateAgentAssetsTest.test_update_hcom_reinstalls_a_pinned_install_without_its_retained_wheel) ... ok
test_update_omp_downloads_verifies_the_tarball_hash_and_installs_at_the_pin (tests.unit.test_update_agent_assets.UpdateAgentAssetsTest.test_update_omp_downloads_verifies_the_tarball_hash_and_installs_at_the_pin) ... ok
test_updates_use_managed_binaries_when_path_is_shadowed (tests.unit.test_update_agent_assets.UpdateAgentAssetsTest.test_updates_use_managed_binaries_when_path_is_shadowed) ... ok
test_chezmoi_rendered_updater_uses_exported_source_root (tests.unit.test_asset_manifest.AssetManifestTest.test_chezmoi_rendered_updater_uses_exported_source_root) ... ok
test_chezmoi_rendered_updater_uses_inlined_manifest_library (tests.unit.test_asset_manifest.AssetManifestTest.test_chezmoi_rendered_updater_uses_inlined_manifest_library) ... ok
test_chezmoi_wrapper_renders_shebang_and_source_root (tests.unit.test_asset_manifest.AssetManifestTest.test_chezmoi_wrapper_renders_shebang_and_source_root) ... ok
test_failed_atomic_commit_leaves_previous_manifest_intact (tests.unit.test_asset_manifest.AssetManifestTest.test_failed_atomic_commit_leaves_previous_manifest_intact) ... ok
test_records_schema_two_steps_and_replaces_one_whole_entry (tests.unit.test_asset_manifest.AssetManifestTest.test_records_schema_two_steps_and_replaces_one_whole_entry) ... ok
test_rendered_updater_fails_when_no_source_root_is_valid (tests.unit.test_asset_manifest.AssetManifestTest.test_rendered_updater_fails_when_no_source_root_is_valid) ... ok
test_same_run_mise_repairs_preserve_both_identity_steps (tests.unit.test_asset_manifest.AssetManifestTest.test_same_run_mise_repairs_preserve_both_identity_steps) ... ok
test_two_real_install_steps_record_under_fake_home (tests.unit.test_asset_manifest.AssetManifestTest.test_two_real_install_steps_record_under_fake_home) ... ok
test_unwritable_destination_warns_once_without_failing (tests.unit.test_asset_manifest.AssetManifestTest.test_unwritable_destination_warns_once_without_failing) ... ok
test_updater_direct_source_resolves_repository_root (tests.unit.test_asset_manifest.AssetManifestTest.test_updater_direct_source_resolves_repository_root) ... ok
test_updater_has_one_recording_call_for_each_install_step (tests.unit.test_asset_manifest.AssetManifestTest.test_updater_has_one_recording_call_for_each_install_step) ... ok
test_agent_asset_update_removes_node_global_shadows_before_agent_commands (tests.unit.test_runtime_health.RuntimeHealthTest.test_agent_asset_update_removes_node_global_shadows_before_agent_commands) ... ok
test_agent_asset_update_repairs_broken_claude_with_npm_backend (tests.unit.test_runtime_health.RuntimeHealthTest.test_agent_asset_update_repairs_broken_claude_with_npm_backend) ... ok
test_agent_asset_update_runs_gh_extension_ensure (tests.unit.test_runtime_health.RuntimeHealthTest.test_agent_asset_update_runs_gh_extension_ensure) ... ok
test_agent_launchers_do_not_hardcode_model_ids (tests.unit.test_runtime_health.RuntimeHealthTest.test_agent_launchers_do_not_hardcode_model_ids) ... ok
test_agmsg_accepts_a_store_the_installer_creates_and_notes_run_changes (tests.unit.test_runtime_health.RuntimeHealthTest.test_agmsg_accepts_a_store_the_installer_creates_and_notes_run_changes) ... FAIL
test_agmsg_already_pinned_skips_download (tests.unit.test_runtime_health.RuntimeHealthTest.test_agmsg_already_pinned_skips_download) ... ok
test_agmsg_checksum_mismatch_fails_closed (tests.unit.test_runtime_health.RuntimeHealthTest.test_agmsg_checksum_mismatch_fails_closed) ... FAIL
test_agmsg_fresh_install_populates_skill_and_records_manifest (tests.unit.test_runtime_health.RuntimeHealthTest.test_agmsg_fresh_install_populates_skill_and_records_manifest) ... FAIL
test_agmsg_migrates_marker_less_legacy_dir_without_losing_live_state (tests.unit.test_runtime_health.RuntimeHealthTest.test_agmsg_migrates_marker_less_legacy_dir_without_losing_live_state) ... ERROR
test_agmsg_migration_reports_an_installer_that_mutates_live_state (tests.unit.test_runtime_health.RuntimeHealthTest.test_agmsg_migration_reports_an_installer_that_mutates_live_state) ... ERROR
test_agmsg_refuses_to_install_when_the_state_snapshot_is_empty (tests.unit.test_runtime_health.RuntimeHealthTest.test_agmsg_refuses_to_install_when_the_state_snapshot_is_empty) ... FAIL
test_agmsg_refuses_to_install_without_tar (tests.unit.test_runtime_health.RuntimeHealthTest.test_agmsg_refuses_to_install_without_tar) ... ok
test_agmsg_reports_an_installer_that_leaves_the_wrong_version (tests.unit.test_runtime_health.RuntimeHealthTest.test_agmsg_reports_an_installer_that_leaves_the_wrong_version) ... FAIL
test_agmsg_update_aborts_when_install_corrupts_live_state (tests.unit.test_runtime_health.RuntimeHealthTest.test_agmsg_update_aborts_when_install_corrupts_live_state) ... FAIL
test_agmsg_update_never_touches_teams_db_run (tests.unit.test_runtime_health.RuntimeHealthTest.test_agmsg_update_never_touches_teams_db_run) ... ok
test_client_bashrc_treats_private_sources_as_optional (tests.unit.test_runtime_health.RuntimeHealthTest.test_client_bashrc_treats_private_sources_as_optional) ... ok
test_codex_crit_normalizes_managed_marketplace_mode (tests.unit.test_runtime_health.RuntimeHealthTest.test_codex_crit_normalizes_managed_marketplace_mode) ... ok
test_codex_superpowers_reports_login_step_when_curated_catalog_is_missing (tests.unit.test_runtime_health.RuntimeHealthTest.test_codex_superpowers_reports_login_step_when_curated_catalog_is_missing) ... ok
test_crit_fails_without_an_install_when_the_download_fails (tests.unit.test_runtime_health.RuntimeHealthTest.test_crit_fails_without_an_install_when_the_download_fails) ... ok
test_crit_never_promotes_a_staged_binary_that_prints_the_banner_but_fails (tests.unit.test_runtime_health.RuntimeHealthTest.test_crit_never_promotes_a_staged_binary_that_prints_the_banner_but_fails) ... ok
test_crit_refuses_a_replaced_release_whose_checksums_txt_matches (tests.unit.test_runtime_health.RuntimeHealthTest.test_crit_refuses_a_replaced_release_whose_checksums_txt_matches) ... ok
test_crit_replaces_an_installed_binary_that_cannot_report_its_version (tests.unit.test_runtime_health.RuntimeHealthTest.test_crit_replaces_an_installed_binary_that_cannot_report_its_version) ... ok
test_crit_replaces_an_installed_binary_that_prints_the_banner_but_fails (tests.unit.test_runtime_health.RuntimeHealthTest.test_crit_replaces_an_installed_binary_that_prints_the_banner_but_fails) ... ok
test_darwin_crit_checksum_failure_preserves_existing_binary (tests.unit.test_runtime_health.RuntimeHealthTest.test_darwin_crit_checksum_failure_preserves_existing_binary) ... ok
test_darwin_crit_install_is_pinned_atomic_and_recorded (tests.unit.test_runtime_health.RuntimeHealthTest.test_darwin_crit_install_is_pinned_atomic_and_recorded) ... ok
test_doctor_has_no_github_role_check (tests.unit.test_runtime_health.RuntimeHealthTest.test_doctor_has_no_github_role_check) ... ok
test_doctor_reports_claude_sandbox_prerequisites (tests.unit.test_runtime_health.RuntimeHealthTest.test_doctor_reports_claude_sandbox_prerequisites) ... ok
test_doctor_required_optional_and_healthy_statuses (tests.unit.test_runtime_health.RuntimeHealthTest.test_doctor_required_optional_and_healthy_statuses) ... ok
test_linux_crit_checksum_failure_preserves_existing_binary (tests.unit.test_runtime_health.RuntimeHealthTest.test_linux_crit_checksum_failure_preserves_existing_binary) ... ok
test_linux_crit_correct_version_is_download_free (tests.unit.test_runtime_health.RuntimeHealthTest.test_linux_crit_correct_version_is_download_free) ... ok
test_linux_crit_failure_does_not_leak_cleanup_trap (tests.unit.test_runtime_health.RuntimeHealthTest.test_linux_crit_failure_does_not_leak_cleanup_trap) ... ok
test_linux_crit_install_is_pinned_atomic_and_recorded (tests.unit.test_runtime_health.RuntimeHealthTest.test_linux_crit_install_is_pinned_atomic_and_recorded) ... ok
test_linux_crit_prefers_pinned_target_over_older_path_binary (tests.unit.test_runtime_health.RuntimeHealthTest.test_linux_crit_prefers_pinned_target_over_older_path_binary) ... ok
test_make_doctor_does_not_skip_runtime_check_when_deployed_root_is_missing (tests.unit.test_runtime_health.RuntimeHealthTest.test_make_doctor_does_not_skip_runtime_check_when_deployed_root_is_missing) ... ok
test_make_doctor_passes_repair_variable_to_runtime_check (tests.unit.test_runtime_health.RuntimeHealthTest.test_make_doctor_passes_repair_variable_to_runtime_check) ... ok
test_make_doctor_propagates_runtime_drift_after_tool_checks (tests.unit.test_runtime_health.RuntimeHealthTest.test_make_doctor_propagates_runtime_drift_after_tool_checks) ... ok
test_make_update_pulls_clean_main_before_apply (tests.unit.test_runtime_health.RuntimeHealthTest.test_make_update_pulls_clean_main_before_apply) ... ok
test_make_update_reports_unmerged_feature_branch_before_branch_notice (tests.unit.test_runtime_health.RuntimeHealthTest.test_make_update_reports_unmerged_feature_branch_before_branch_notice) ... ok
test_make_update_reports_unmerged_index_before_dirty_notice (tests.unit.test_runtime_health.RuntimeHealthTest.test_make_update_reports_unmerged_index_before_dirty_notice) ... ok
test_make_update_skips_dirty_main_with_manual_pull_notice (tests.unit.test_runtime_health.RuntimeHealthTest.test_make_update_skips_dirty_main_with_manual_pull_notice) ... ok
test_upgrade_fails_and_keeps_the_backup_when_a_partial_install_cannot_be_removed (tests.unit.test_runtime_health.RuntimeHealthTest.test_upgrade_fails_and_keeps_the_backup_when_a_partial_install_cannot_be_removed) ... ok
test_upgrade_fails_when_the_final_install_fails_after_a_rebuild (tests.unit.test_runtime_health.RuntimeHealthTest.test_upgrade_fails_when_the_final_install_fails_after_a_rebuild) ... ok
test_upgrade_fails_when_the_node_marker_cannot_be_written (tests.unit.test_runtime_health.RuntimeHealthTest.test_upgrade_fails_when_the_node_marker_cannot_be_written) ... ok
test_upgrade_failure_after_a_successful_install_only_warns (tests.unit.test_runtime_health.RuntimeHealthTest.test_upgrade_failure_after_a_successful_install_only_warns) ... ok
test_upgrade_homebrew_verifies_attestations_when_gh_is_present (tests.unit.test_runtime_health.RuntimeHealthTest.test_upgrade_homebrew_verifies_attestations_when_gh_is_present) ... ok
test_upgrade_network_only_phases_warn_and_the_mise_phase_still_runs (tests.unit.test_runtime_health.RuntimeHealthTest.test_upgrade_network_only_phases_warn_and_the_mise_phase_still_runs) ... ok
test_upgrade_never_restores_an_undeletable_backup_over_a_completed_rebuild (tests.unit.test_runtime_health.RuntimeHealthTest.test_upgrade_never_restores_an_undeletable_backup_over_a_completed_rebuild) ... ok
test_upgrade_rebuilds_npm_tools_when_the_node_marker_differs (tests.unit.test_runtime_health.RuntimeHealthTest.test_upgrade_rebuilds_npm_tools_when_the_node_marker_differs) ... ok
test_upgrade_required_failures_are_nonzero_and_independent (tests.unit.test_runtime_health.RuntimeHealthTest.test_upgrade_required_failures_are_nonzero_and_independent) ... ok
test_upgrade_restores_a_rebuild_backup_left_by_a_killed_run (tests.unit.test_runtime_health.RuntimeHealthTest.test_upgrade_restores_a_rebuild_backup_left_by_a_killed_run) ... ok
test_upgrade_restores_the_npm_tool_when_the_rebuild_is_interrupted (tests.unit.test_runtime_health.RuntimeHealthTest.test_upgrade_restores_the_npm_tool_when_the_rebuild_is_interrupted) ... ok
test_upgrade_runs_mise_against_the_applied_host_config_and_edits_no_file (tests.unit.test_runtime_health.RuntimeHealthTest.test_upgrade_runs_mise_against_the_applied_host_config_and_edits_no_file) ... ok
test_upgrade_self_updates_mise_to_its_latest_release (tests.unit.test_runtime_health.RuntimeHealthTest.test_upgrade_self_updates_mise_to_its_latest_release) ... ok
test_upgrade_skips_every_phase_when_ci_is_true (tests.unit.test_runtime_health.RuntimeHealthTest.test_upgrade_skips_every_phase_when_ci_is_true) ... ok
test_upgrade_skips_unavailable_mise_self_update (tests.unit.test_runtime_health.RuntimeHealthTest.test_upgrade_skips_unavailable_mise_self_update) ... ok

======================================================================
ERROR: test_agmsg_migrates_marker_less_legacy_dir_without_losing_live_state (tests.unit.test_runtime_health.RuntimeHealthTest.test_agmsg_migrates_marker_less_legacy_dir_without_losing_live_state)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "~/Workspace/dotfiles/.claude/worktrees/worker-c/tests/unit/test_runtime_health.py", line 912, in test_agmsg_migrates_marker_less_legacy_dir_without_losing_live_state
    log = (repo / "commands.log").read_text()
  File "~/.local/share/mise/installs/python/latest/lib/python3.15/pathlib/__init__.py", line 986, in read_text
    with self.open(mode='r', encoding=encoding, errors=errors, newline=newline) as f:
         ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "~/.local/share/mise/installs/python/latest/lib/python3.15/pathlib/__init__.py", line 970, in open
    return io.open(self, mode, buffering, encoding, errors, newline)
           ~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
FileNotFoundError: [Errno 2] No such file or directory: '/tmp/claude-501/runtime-health-test-pshe3m49/agmsg-repo/commands.log'

======================================================================
ERROR: test_agmsg_migration_reports_an_installer_that_mutates_live_state (tests.unit.test_runtime_health.RuntimeHealthTest.test_agmsg_migration_reports_an_installer_that_mutates_live_state)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "~/Workspace/dotfiles/.claude/worktrees/worker-c/tests/unit/test_runtime_health.py", line 978, in test_agmsg_migration_reports_an_installer_that_mutates_live_state
    self.assertNotIn("update=true", (repo / "commands.log").read_text())
                                    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "~/.local/share/mise/installs/python/latest/lib/python3.15/pathlib/__init__.py", line 986, in read_text
    with self.open(mode='r', encoding=encoding, errors=errors, newline=newline) as f:
         ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "~/.local/share/mise/installs/python/latest/lib/python3.15/pathlib/__init__.py", line 970, in open
    return io.open(self, mode, buffering, encoding, errors, newline)
           ~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
FileNotFoundError: [Errno 2] No such file or directory: '/tmp/claude-501/runtime-health-test-bzqph0r9/agmsg-repo/commands.log'

======================================================================
FAIL: test_agmsg_accepts_a_store_the_installer_creates_and_notes_run_changes (tests.unit.test_runtime_health.RuntimeHealthTest.test_agmsg_accepts_a_store_the_installer_creates_and_notes_run_changes)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "~/Workspace/dotfiles/.claude/worktrees/worker-c/tests/unit/test_runtime_health.py", line 1014, in test_agmsg_accepts_a_store_the_installer_creates_and_notes_run_changes
    self.assertNotIn("installer failed", output)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 'installer failed' unexpectedly found in '\n==> agmsg\nmktemp: mkstemp failed on /var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/tmp.E9yMzqvlLL: Operation not permitted\nagmsg: could not snapshot the live state under /tmp/claude-501/runtime-health-test-483br94j/agmsg-home/.agents/skills/agmsg; nothing was installed\nagmsg installer failed (installed: none); see the reason above.\n'

======================================================================
FAIL: test_agmsg_checksum_mismatch_fails_closed (tests.unit.test_runtime_health.RuntimeHealthTest.test_agmsg_checksum_mismatch_fails_closed)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "~/Workspace/dotfiles/.claude/worktrees/worker-c/tests/unit/test_runtime_health.py", line 860, in test_agmsg_checksum_mismatch_fails_closed
    self.assertIn("checksum mismatch", result.stdout + result.stderr)
    ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 'checksum mismatch' not found in '\n==> agmsg\nmktemp: mkstemp failed on /var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/tmp.OFmDKW4dwD: Operation not permitted\nagmsg installer failed (installed: none); see the reason above.\n'

======================================================================
FAIL: test_agmsg_fresh_install_populates_skill_and_records_manifest (tests.unit.test_runtime_health.RuntimeHealthTest.test_agmsg_fresh_install_populates_skill_and_records_manifest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "~/Workspace/dotfiles/.claude/worktrees/worker-c/tests/unit/test_runtime_health.py", line 819, in test_agmsg_fresh_install_populates_skill_and_records_manifest
    self.assertNotIn("installer failed", result.stdout + result.stderr)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 'installer failed' unexpectedly found in '\n==> agmsg\nmktemp: mkstemp failed on /var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/tmp.cu4KBP5r30: Operation not permitted\nagmsg installer failed (installed: none); see the reason above.\n'

======================================================================
FAIL: test_agmsg_refuses_to_install_when_the_state_snapshot_is_empty (tests.unit.test_runtime_health.RuntimeHealthTest.test_agmsg_refuses_to_install_when_the_state_snapshot_is_empty)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "~/Workspace/dotfiles/.claude/worktrees/worker-c/tests/unit/test_runtime_health.py", line 1063, in test_agmsg_refuses_to_install_when_the_state_snapshot_is_empty
    self.assertIn("hashed fewer live-state files than exist", output)
    ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 'hashed fewer live-state files than exist' not found in '\n==> agmsg\nmktemp: mkstemp failed on /var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/tmp.slZSDF2Ez9: Operation not permitted\nagmsg: could not snapshot the live state under /tmp/claude-501/runtime-health-test-1ore4c15/agmsg-home/.agents/skills/agmsg; nothing was installed\nagmsg installer failed (installed: 1.0.0); see the reason above.\n'

======================================================================
FAIL: test_agmsg_reports_an_installer_that_leaves_the_wrong_version (tests.unit.test_runtime_health.RuntimeHealthTest.test_agmsg_reports_an_installer_that_leaves_the_wrong_version)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "~/Workspace/dotfiles/.claude/worktrees/worker-c/tests/unit/test_runtime_health.py", line 1033, in test_agmsg_reports_an_installer_that_leaves_the_wrong_version
    self.assertIn(
    ~~~~~~~~~~~~~^
        "agmsg: install.sh --cmd agmsg --agent-type claude-code left VERSION 9.9.9 (want 1.5.0)",
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        output,
        ^^^^^^^
    )
    ^
AssertionError: 'agmsg: install.sh --cmd agmsg --agent-type claude-code left VERSION 9.9.9 (want 1.5.0)' not found in '\n==> agmsg\nmktemp: mkstemp failed on /var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/tmp.frCZasKHHr: Operation not permitted\nagmsg installer failed (installed: none); see the reason above.\n'

======================================================================
FAIL: test_agmsg_update_aborts_when_install_corrupts_live_state (tests.unit.test_runtime_health.RuntimeHealthTest.test_agmsg_update_aborts_when_install_corrupts_live_state)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "~/Workspace/dotfiles/.claude/worktrees/worker-c/tests/unit/test_runtime_health.py", line 946, in test_agmsg_update_aborts_when_install_corrupts_live_state
    self.assertIn(
    ~~~~~~~~~~~~~^
        "install.sh --update --cmd agmsg --agent-type claude-code changed or removed existing live state", output
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
AssertionError: 'install.sh --update --cmd agmsg --agent-type claude-code changed or removed existing live state' not found in '\n==> agmsg\nmktemp: mkstemp failed on /var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/tmp.EQvTom1A7i: Operation not permitted\nagmsg: could not snapshot the live state under /tmp/claude-501/runtime-health-test-ysj4wp9l/agmsg-home/.agents/skills/agmsg; nothing was installed\nagmsg installer failed (installed: 1.0.0); see the reason above.\n'

----------------------------------------------------------------------
Ran 72 tests in 56.173s

FAILED (failures=6, errors=2)
(exit 1)
```

```console
$ diff fail-base.txt fail-r2.txt && echo "SAME FAILING SET"   # the sandbox-only agmsg failures of section 5
SAME FAILING SET
(exit 0)
$ shellcheck -x scripts/update-agent-assets.sh
(exit 0)
$ shfmt -i 4 -sr -d scripts/update-agent-assets.sh
(exit 0)
$ ruff format --config ruff.toml --check tests/unit/test_update_agent_assets.py; ruff check --config ruff.toml tests/unit/test_update_agent_assets.py
1 file already formatted
All checks passed!
(exit 0)
$ git diff --numstat origin/main -- scripts tests
10	4	scripts/update-agent-assets.sh
61	4	tests/unit/test_update_agent_assets.py
(exit 0)
```
