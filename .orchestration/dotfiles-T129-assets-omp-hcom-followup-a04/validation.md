---
task_id: dotfiles-T129-assets-omp-hcom-followup-a04
seat: claude-standard-dot-a009
code_head: 42414b6df9983dcb99aeb411843e3a65bd7dbd44
base: 51ba580149fcace54a912358e7e87c5b07cd8760
---

# Validation: dotfiles-T129-assets-omp-hcom-followup-a04

- **Where:** every block ran inside the sandbox, from this worktree on `tools/assets-omp-hcom-followup-a04`. §1 to §8 ran at the code head `42414b6d`, and §10 to §12 after the PR opened. The later commits add only this directory's records.
- **Placeholders:** each block prints its commands, their verbatim output and the block's last exit status. `MAIN` is the main checkout, `T` the task id, `$S` the session scratchpad, `$TMPDIR` the sandbox's temporary directory, `<user-temp>` the per-user macOS temporary directory, and `~` the home directory.
- **Red, then green:** §4r is red at `725b25bf`, inside the sandbox: the selector runs one test and fails by assertion. The old `update_omp`'s untemplated `mktemp -d` ignored `TMPDIR`, and the sandbox refused the per-user default it picked. §6b is green at the code head, and §6 is the Check.

## 1. Task file (sha256 fc324db7…) and the branch copy
```console
$ shasum -a 256 "~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T129-assets-omp-hcom-followup-a04.md" ".orchestration/dotfiles-T129-assets-omp-hcom-followup-a04/task.md"; cmp "~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T129-assets-omp-hcom-followup-a04.md" ".orchestration/dotfiles-T129-assets-omp-hcom-followup-a04/task.md" && echo byte-identical
fc324db78e16cdc8f0601d88a0c7755453b76ee63af916eafd99f5a0434a6efe  ~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T129-assets-omp-hcom-followup-a04.md
fc324db78e16cdc8f0601d88a0c7755453b76ee63af916eafd99f5a0434a6efe  .orchestration/dotfiles-T129-assets-omp-hcom-followup-a04/task.md
byte-identical
[exit 0]
```

## 1a. The task-consistency check on the dispatched file
```console
$ uv run --offline --no-project --with pyyaml python -I scripts/orchestrator/task-consistency-check.py --root "$PWD" "~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T129-assets-omp-hcom-followup-a04.md"
dotfiles-T129-assets-omp-hcom-followup-a04.md: OK
[exit 0]
```

## 2. Branch, base and commits
```console
$ git rev-parse --abbrev-ref HEAD; git rev-parse origin/main; git merge-base origin/main HEAD; git log --format='%H %s' origin/main..HEAD | cut -c1-140
tools/assets-omp-hcom-followup-a04
51ba580149fcace54a912358e7e87c5b07cd8760
51ba580149fcace54a912358e7e87c5b07cd8760
42414b6df9983dcb99aeb411843e3a65bd7dbd44 test(assets): update_omp makes its download directory under TMPDIR; the a03 revise round's revise.y
ecea1a45a2b1be54285d69150ffe6333e1e2bb3c chore(orchestration): the dotfiles-T129-assets-omp-hcom-followup-a04 task copy
[exit 0]
```

## 3. The owned row and the a03 record's facts it is written from (the main checkout's record)
```console
$ f="~/Workspace/dotfiles/.orchestration/acceptance/dotfiles-T129-assets-omp-hcom-followup-a03.md"; { awk '/^## Owned by dotfiles-T129-assets-omp-hcom-followup-a04/,0' "$f" | head -3; /usr/bin/grep -n -e '09:38:46Z' -e '10:06:33Z' -e '10:17:03Z' "$f" | cut -c1-400; } | sed 's/^/> /'
> ## Owned by dotfiles-T129-assets-omp-hcom-followup-a04
> 
> - `audit:9e30542:1` revise-check-grammar: one red-then-green test runs the updater's mktemp path with TMPDIR set to a sandbox-like directory and asserts the temporary directory is created under it (`tests/unit/test_update_agent_assets.py`); the revision record `revise.yaml` for the a03 revise round is written into the a04 evidence directory from the a03 record's facts.
> 73:- 2026-10-19T09:38:46Z: the chain on 725b25bf (sweep 0 gaps, local review clean): task-level audit `…-audit-725b25b.md`: `Verdict: incorrect`: P1 (conformance) three test runs outside the sandbox after `mktemp -d` was refused (tests are no escalation exception); P2 the Bot-wait claim while the PR was a draft; P2 validation.md without PR, CI and Bot outputs; P2 the record's dispatch array withou
> 79:- 2026-10-19T10:06:33Z: a009 RESULT revise 2 (round 2 of 2): head 9e305424 (code head 92d39f00) on main 69dccca9, one push; the six mktemp calls the in-sandbox tests reach take `"${TMPDIR:-/tmp}/update-agent-assets.XXXXXX"` (three unreached calls unchanged); the Check 35/35, test_runtime_health + test_lint_comparisons 69/69 and the five selectors red-then-green, all inside the sandbox; validati
> 80:- 2026-10-19T10:17:03Z: the chain on 9e305424 (CI 7/7 required green; local review and sweep clean): task-level audit `…-audit-9e30542.md`: `Verdict: incorrect` on one P2 (orchestration): my revise line's check= was prose, not `tests/<file>::<name>` selectors; no revise.yaml; no test changed for the mktemp fixes. Root cause: the revise message contract (selectors in check=) was not followed by 
[exit 0]
```

## 4. The change: the test, its helper parameter, and revise.yaml
```console
$ git diff origin/main...HEAD -- tests .orchestration/dotfiles-T129-assets-omp-hcom-followup-a04/revise.yaml
diff --git a/.orchestration/dotfiles-T129-assets-omp-hcom-followup-a04/revise.yaml b/.orchestration/dotfiles-T129-assets-omp-hcom-followup-a04/revise.yaml
new file mode 100644
index 00000000..b0e6954c
--- /dev/null
+++ b/.orchestration/dotfiles-T129-assets-omp-hcom-followup-a04/revise.yaml
@@ -0,0 +1,12 @@
+# The revise round of 2026-10-19T09:40:27Z for dotfiles-T129-assets-omp-hcom-followup-a03 (AGMSG-ACCEPTANCE status=revise,
+# message 2490), as the message contract asks. Written by its owner task dotfiles-T129-assets-omp-hcom-followup-a04 for
+# audit:9e30542:1, from the a03 acceptance record's facts: that revise line's check= carried prose, not selectors, so the
+# selector below is the test this task adds for the revise's check (1), the updater's mktemp under a sandbox-like TMPDIR.
+task_id: dotfiles-T129-assets-omp-hcom-followup-a03
+round: 2
+revise: 1
+previous_head: 725b25bf731d4612d350c1da6642ecbdc385ede6
+result_head: 9e30542438e0d88404bd1587aa529bf758837aec
+reason: "the task-level audit of 725b25b: P1 three test runs outside the sandbox after mktemp -d was refused; P2 the Bot-wait claim while the PR was a draft; P2 validation.md without PR, CI and Bot outputs; P2 the record's dispatch array without read markers (the orchestrator's); P3 no cost: field"
+checks:
+  - tests/unit/test_update_agent_assets.py::test_update_omp_makes_its_download_directory_under_tmpdir
diff --git a/tests/unit/test_update_agent_assets.py b/tests/unit/test_update_agent_assets.py
index d442baaf..45c77a13 100644
--- a/tests/unit/test_update_agent_assets.py
+++ b/tests/unit/test_update_agent_assets.py
@@ -192,9 +192,9 @@ class UpdateAgentAssetsTest(unittest.TestCase):
     def test_update_omp_downloads_verifies_the_tarball_hash_and_installs_at_the_pin(self):
         self.exercise_update("omp")
 
-    def update_omp_in(self, home, version, spelling=""):
-        # update_omp with the fixture curl and npm on PATH and HOME=<home><spelling>; the caller has placed any entry at
-        # ~/.local/bin/omp.
+    def update_omp_in(self, home, version, spelling="", tmpdir=None):
+        # update_omp with the fixture curl and npm on PATH, HOME=<home><spelling> and any TMPDIR; the caller has placed
+        # any entry at ~/.local/bin/omp.
         binary = home / ".local/bin"
         binary.mkdir(parents=True, exist_ok=True)
         for name in ("curl", "npm"):
@@ -212,7 +212,8 @@ class UpdateAgentAssetsTest(unittest.TestCase):
                 "CALLS": str(home / "calls.jsonl"),
                 "PAYLOAD": str(payload),
                 "FIXTURE_VERSION": version,
-            },
+            }
+            | ({"TMPDIR": str(tmpdir)} if tmpdir else {}),
             stdin=subprocess.DEVNULL,
             capture_output=True,
             text=True,
@@ -220,6 +221,22 @@ class UpdateAgentAssetsTest(unittest.TestCase):
             check=False,
         )
 
+    def test_update_omp_makes_its_download_directory_under_tmpdir(self):
+        # audit:9e30542:1: the download directory takes its mktemp template from TMPDIR, as a sandbox sets it, never the
+        # per-user default macOS mktemp picks without a template (which the agent sandbox refuses).
+        with tempfile.TemporaryDirectory() as directory:
+            home = Path(directory)
+            sandbox_tmp = home / "sandbox-tmp"
+            sandbox_tmp.mkdir()
+            result = self.update_omp_in(home, "18.11.3", tmpdir=sandbox_tmp)
+            log = home / "calls.jsonl"
+            calls = [json.loads(line) for line in log.read_text().splitlines()] if log.exists() else []
+            outputs = [Path(row["argv"][row["argv"].index("-o") + 1]) for row in calls if row["tool"] == "curl"]
+            output = result.stdout + result.stderr
+            self.assertEqual([sandbox_tmp], [path.parent.parent for path in outputs], output)
+            self.assertTrue(outputs[0].parent.name.startswith("update-agent-assets."), output)
+            self.assertEqual(0, result.returncode, output)
+
     def test_a_link_target_escaping_the_npm_prefix_is_refused(self):
         # The Bot's P2 4307029052: npm resolves the link before its ownership check (bin-links check-bin), so a target
         # that starts with this prefix's package but leaves it through `..` is not npm's own and moves to the kept path.
[exit 0]
```

## 4r. Red at 725b25bf (the head before the template commit 92d39f00): this branch's test module, by exact id
```console
$ S=<the session scratchpad>; git worktree add --detach -q "$S/red-a04" 725b25bf; cp tests/unit/test_update_agent_assets.py "$S/red-a04/tests/unit/"; shasum -a 256 tests/unit/test_update_agent_assets.py "$S/red-a04/tests/unit/test_update_agent_assets.py"
2636db8f40d7b7681bc9e8768edf0698e9247d786da07ee83b12cc99d2bece9f  tests/unit/test_update_agent_assets.py
2636db8f40d7b7681bc9e8768edf0698e9247d786da07ee83b12cc99d2bece9f  $S/red-a04/tests/unit/test_update_agent_assets.py
$ bash "$S/red-ids.sh" "$S/red-a04" tests.unit.test_update_agent_assets.UpdateAgentAssetsTest.test_update_omp_makes_its_download_directory_under_tmpdir
tree=725b25bf731d4612d350c1da6642ecbdc385ede6 dirty=1
$ uv run python -m unittest tests.unit.test_update_agent_assets.UpdateAgentAssetsTest.test_update_omp_makes_its_download_directory_under_tmpdir
exit=1
FAIL: test_update_omp_makes_its_download_directory_under_tmpdir
AssertionError: Lists differ: [PosixPath('$TMPDIR/tmp_nir8xhq/sandbox-tmp')] != []
Ran 1 test in 0.049s
FAILED (failures=1)
$ grep -o 'mktemp: [^\\]*' "$S/red-ids.log" | head -1    # the run's captured update_omp output
mktemp: mkdtemp failed on <user-temp>/tmp.0Sa1fEBz8H: Operation not permitted
$ git worktree remove --force "$S/red-a04"; echo "removed=$?"
removed=0
```

## 5. revise.yaml parses, and its selector is an existing test
```console
$ uv run --no-project --with pyyaml python -I -c 'import sys, yaml; d = yaml.safe_load(open(sys.argv[1])); print(d)' .orchestration/dotfiles-T129-assets-omp-hcom-followup-a04/revise.yaml; uv run python -m unittest tests.unit.test_update_agent_assets.UpdateAgentAssetsTest.test_update_omp_makes_its_download_directory_under_tmpdir 2>&1 | tail -3
{'task_id': 'dotfiles-T129-assets-omp-hcom-followup-a03', 'round': 2, 'revise': 1, 'previous_head': '725b25bf731d4612d350c1da6642ecbdc385ede6', 'result_head': '9e30542438e0d88404bd1587aa529bf758837aec', 'reason': "the task-level audit of 725b25b: P1 three test runs outside the sandbox after mktemp -d was refused; P2 the Bot-wait claim while the PR was a draft; P2 validation.md without PR, CI and Bot outputs; P2 the record's dispatch array without read markers (the orchestrator's); P3 no cost: field", 'checks': ['tests/unit/test_update_agent_assets.py::test_update_omp_makes_its_download_directory_under_tmpdir']}
Ran 1 test in 0.585s

OK
[exit 0]
```

## 6. The Check: both test modules, -v
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
test_update_omp_makes_its_download_directory_under_tmpdir (tests.unit.test_update_agent_assets.UpdateAgentAssetsTest.test_update_omp_makes_its_download_directory_under_tmpdir) ... ok
test_update_omp_moves_an_entry_npm_does_not_own_aside_and_puts_it_back_when_the_install_fails (tests.unit.test_update_agent_assets.UpdateAgentAssetsTest.test_update_omp_moves_an_entry_npm_does_not_own_aside_and_puts_it_back_when_the_install_fails) ... ok
test_updates_use_managed_binaries_when_path_is_shadowed (tests.unit.test_update_agent_assets.UpdateAgentAssetsTest.test_updates_use_managed_binaries_when_path_is_shadowed) ... ok

----------------------------------------------------------------------
Ran 36 tests in 71.990s

OK
[exit 0]
```

## 6b. The new selector by exact id, green here
```console
$ bash $S/red-ids.sh "$PWD" tests.unit.test_update_agent_assets.UpdateAgentAssetsTest.test_update_omp_makes_its_download_directory_under_tmpdir
tree=42414b6df9983dcb99aeb411843e3a65bd7dbd44 dirty=5
$ uv run python -m unittest tests.unit.test_update_agent_assets.UpdateAgentAssetsTest.test_update_omp_makes_its_download_directory_under_tmpdir
exit=0
Ran 1 test in 0.253s
OK
[exit 0]
```

## 7. shellcheck -x (the CI form) on both owned scripts (unchanged); ruff on the test module
```console
$ git diff --quiet origin/main...HEAD -- home/dot_local/bin/common/executable_remove-agent-asset scripts/update-agent-assets.sh && echo 'both scripts unchanged'; shellcheck -x scripts/update-agent-assets.sh home/dot_local/bin/common/executable_remove-agent-asset && echo 'shellcheck clean'; ruff format --config ruff.toml --check tests/unit/test_update_agent_assets.py; ruff check --config ruff.toml --output-format concise tests/unit/test_update_agent_assets.py
both scripts unchanged
shellcheck clean
1 file already formatted
All checks passed!
[exit 0]
```

## 8. Caps against origin/main
```console
$ git merge-base origin/main HEAD; git diff --numstat origin/main...HEAD; git diff --numstat origin/main...HEAD | awk -F '\t' '$3 ~ /^\.orchestration\// {next} $3 ~ /^tests\// {t += $1 + $2; next} {o += $1 + $2} END {printf "outside tests/ and .orchestration/: %d of 120\nunder tests/: %d of 400\n", o, t}'
51ba580149fcace54a912358e7e87c5b07cd8760
12	0	.orchestration/dotfiles-T129-assets-omp-hcom-followup-a04/revise.yaml
63	0	.orchestration/dotfiles-T129-assets-omp-hcom-followup-a04/task.md
21	4	tests/unit/test_update_agent_assets.py
outside tests/ and .orchestration/: 0 of 120
under tests/: 25 of 400
[exit 0]
```
