# dot-ubuntu-parity-T2-a01 validation

Worktree: `/home/moriya/Workspace/worktrees/chezmoi-ubuntu-parity`

## B1 — docker group

```text
$ grep -n "configure_docker_group\|main()" install/ubuntu/client/docker.sh
85:function configure_docker_group() {
92:function main() {
96:    configure_docker_group
```

## B2 — mise yq/watchexec

```text
$ MISE_CONFIG_DIR="$PWD/home/dot_mise" MISE_LOCKED=0 mise install aqua:mikefarah/yq@4.53.6 aqua:watchexec/watchexec@2.7.3
mise by @jdx – installing 2 tools
mise ✓ aqua:watchexec/watchexec@2.7.3  883ms  watchexec-2.7.3-aarch64-unknown-linux-gnu.tar.xz
mise ✓ aqua:mikefarah/yq@4.53.6        2.5s  yq_linux_arm64
mise ████████████████ 2/2 · installed 2 tools in 2.5s

$ MISE_CONFIG_DIR="$PWD/home/dot_mise" mise lock
! No tools configured to lock in this project, but global config declares tools. Run mise lock --global to lock those.
(mise install above already wrote lockfile entries for both new pins; this
warning is unrelated noise from MISE_CONFIG_DIR pointing at a subdirectory)

$ grep -c '"aqua:mikefarah/yq"\."platforms\.' home/dot_mise/mise.lock
4
$ grep -c '"aqua:watchexec/watchexec"\."platforms\.' home/dot_mise/mise.lock
4

$ MISE_CONFIG_DIR="$PWD/home/dot_mise" mise which yq
/home/moriya/.local/share/mise/installs/aqua-mikefarah-yq/4.53.6/yq
$ MISE_CONFIG_DIR="$PWD/home/dot_mise" mise exec -- yq --version
yq (https://github.com/mikefarah/yq/) version v4.53.6

$ uv run python -m unittest tests.unit.test_supply_chain_policy -v
test_executable_downloads_are_verified_and_not_piped_to_shell ... ok
test_external_checksum_failure_preserves_destination ... ok
test_externals_render_without_network_discovery ... ok
test_externals_use_fixed_urls_and_checksums ... ok
test_installer_cleanup_preserves_failure_status ... ok
test_installer_cleanup_survives_mock_function_returns ... ok
test_mise_lock_matches_config_and_supported_platforms ... ok
test_mise_lock_url_entries_have_checksums ... ok
test_mise_main_preserves_install_failure ... ok
test_mise_npm_backend_uses_npm_and_limits_lifecycle_scripts ... ok
test_mise_versions_are_exact_and_locking_is_enforced ... ok
test_nix_inputs_lock_and_ci_use_2605 ... ok
test_setup_ci_rejects_and_preserves_local_drift ... ok
test_sheldon_git_sources_have_revisions ... ok
test_sheldon_uses_locked_crates_io_source ... ok

----------------------------------------------------------------------
Ran 17 tests in 0.114s

OK
```

## B3 — codex project trust

```text
$ uv run --with pyyaml python3 scripts/generate-agent-configs.py
generated agent configs updated
$ git diff home/.chezmoitemplates/codex-config-managed.toml | grep -A2 -B2 projects
 trusted_hash = "sha256:28c43eada804ad00a4e651d6af6320c01e763b1df060af0ab74865a55bc1c9a9"

-[projects."/Users/mryfmo/Workspace/dotfiles"]
+[projects."{{ .chezmoi.workingTree }}"]
 trust_level = "trusted"

$ printf '' | CHEZMOI_SOURCE_DIR="$PWD/home" python3 home/dot_codex/modify_private_config.toml | grep -A2 '\[projects\.'
[projects."/home/moriya/Workspace/worktrees/chezmoi-ubuntu-parity"]
trust_level = "trusted"

$ make validate-agent-assets
uv run --with pyyaml scripts/validate-agent-assets.py
agent asset validation ok
```

## B4 — sheldon dead reference

```text
$ python3 -c "import tomllib; tomllib.loads(open('home/dot_config/sheldon/plugin_sources/client/ubuntu.toml').read()); print('OK: valid empty TOML')"
OK: valid empty TOML
$ git log --all --diff-filter=A --name-only -- '*client/ubuntu.sh'
(no output — the file has never existed in this repository's history)
```

## B5 — doctor cowork/crit

Covered by the full unit-test run below
(`test_compare_claude_skills_ignores_cowork_synced_subtree`,
`test_crit_codex_skills_are_not_orphans`).

## B6 — herdr hook absolute path

Covered by the full unit-test run below, plus the out-of-scope
`tests/unit/test_herdr_agents.py` (not in `allowed_files`, run to confirm no
regression):

```text
$ uv run --with pyyaml python3 -m unittest tests.unit.test_herdr_agents
----------------------------------------------------------------------
Ran 65 tests in 9.128s

OK
```

## Finishing

```text
$ make format
shfmt --indent 4 --space-redirects --diff .
diff home/dot_local/bin/common/executable_contextdb-codex-notify.orig home/dot_local/bin/common/executable_contextdb-codex-notify
--- home/dot_local/bin/common/executable_contextdb-codex-notify.orig
+++ home/dot_local/bin/common/executable_contextdb-codex-notify
@@ -8,7 +8,7 @@
     exit 0
 fi

-if ! python3 - "${1-}" 2> /dev/null << 'PY'; then
+if ! python3 - "${1-}" 2> /dev/null << 'PY'
 import json
 import subprocess
 import sys
@@ -48,6 +48,7 @@
 except Exception:
     raise SystemExit(1)
 PY
+then
     printf '%s\n' 'contextdb-codex-notify: ingest failed' >&2
 fi

diff home/dot_local/bin/common/executable_herdr-agents.orig home/dot_local/bin/common/executable_herdr-agents
--- home/dot_local/bin/common/executable_herdr-agents.orig
+++ home/dot_local/bin/common/executable_herdr-agents
@@ -169,14 +169,14 @@
         return
     fi
     case "${agent_output}" in
-        *timeout* | *Timeout* | *timed\ out* | *TIMED_OUT*)
-            if [[ ${newly_created} == true ]] && wait_for_shell_prompt "${pane_id}"; then
-                if agent_output="$(herdr agent start "${agent_name}" --kind "${kind}" --pane "${pane_id}" --timeout 30000 -- "$@" 2>&1)"; then
-                    printf '%s\n' "${pane_id}"
-                    return
-                fi
-            fi
-            ;;
+    *timeout* | *Timeout* | *timed\ out* | *TIMED_OUT*)
+        if [[ ${newly_created} == true ]] && wait_for_shell_prompt "${pane_id}"; then
+            if agent_output="$(herdr agent start "${agent_name}" --kind "${kind}" --pane "${pane_id}" --timeout 30000 -- "$@" 2>&1)"; then
+                printf '%s\n' "${pane_id}"
+                return
+            fi
+        fi
+        ;;
     esac
     printf 'Failed to start %s agent %s: %s\n' "${kind}" "${agent_name}" "${agent_output}" >&2
     return 1
make: *** [Makefile:146: format] エラー 1
```

Both files are outside this task's `allowed_files` and were last modified in
commits `03a01c2` and `d91b835` respectively, well before this task's work;
not fixed here.

```text
$ make validate-agent-assets
uv run --with pyyaml scripts/validate-agent-assets.py
agent asset validation ok

$ make unit-test
[... 376 tests, verbatim tail below ...]
test_workflows_have_exact_top_level_permissions (test_workflow_security.WorkflowSecurityTest.test_workflows_have_exact_top_level_permissions) ... ok
test_workflows_have_no_job_level_permission_overrides (test_workflow_security.WorkflowSecurityTest.test_workflows_have_no_job_level_permission_overrides) ... ok

----------------------------------------------------------------------
Ran 376 tests in 22.857s

OK (skipped=1)
$ echo "exit code: $?"
exit code: 0

$ git log --oneline main..HEAD
70c5967 fix(claude): invoke herdr-agents attach hook by absolute path
352833b fix(doctor): tolerate cowork-synced skills and own crit codex skills
aaef350 fix(sheldon): drop dead ubuntu-command local plugin
fce3fc3 fix(agents): key codex project trust to the chezmoi working tree
f9223d9 fix(mise): normalize yq shim via aqua and adopt watchexec
720a3fd fix(ubuntu): add user to docker group on client install

$ git status --short
(clean)
```

## CompactionDB memory registration

```text
$ python3 .claude/hooks/contextdb_cli.py memory add --kind decision --content "chezmoi run_once scripts retrigger via content-hash change; no state deletion or file rename needed (run_once_10-install-docker.sh.tmpl re-runs automatically when its rendered content changes, e.g. from the B1 configure_docker_group() addition)." --scope project
6c8f2285-58bb-444e-a028-dd0c09a9141f

$ python3 .claude/hooks/contextdb_cli.py memory list | grep run_once
6c8f2285-58bb-444e-a028-dd0c09a9141f [project/decision] confidence=1.00 salience=0.90 chezmoi run_once scripts retrigger via content-hash change; no state deletion or file rename needed (run_once_10-install-docker.sh.tmpl re-runs automatically when its rendered content changes, e.g. from the B1 configure_docker_group() addition).
```
