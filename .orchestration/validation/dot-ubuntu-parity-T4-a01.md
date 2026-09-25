## Zed checksum fetch (B13a)
$ curl -fsSL https://api.github.com/repos/zed-industries/zed/releases/latest | jq -r .tag_name
v1.20.2

$ curl -fsSL -o /tmp/zed-linux-x86_64.tar.gz https://github.com/zed-industries/zed/releases/download/v1.20.2/zed-linux-x86_64.tar.gz && sha256sum /tmp/zed-linux-x86_64.tar.gz
647dc85e09fcd99cd175365a89b7b70ccf96469c4844eb8ae6eb83dfa82f7600  /tmp/zed-linux-x86_64.tar.gz

$ curl -fsSL -o /tmp/zed-linux-aarch64.tar.gz https://github.com/zed-industries/zed/releases/download/v1.20.2/zed-linux-aarch64.tar.gz && sha256sum /tmp/zed-linux-aarch64.tar.gz
715a5252234522bc9e8e4a8c1f9b462cf7bb2881eed23b7c8ae650b41c24aa6f  /tmp/zed-linux-aarch64.tar.gz

No published checksums manifest exists for this release; both values were obtained by downloading the exact upstream release asset URL directly, not fabricated.

## B15 dead-entry verification (corrected methodology: current-tree existence, not git-log-ever-added)

$ for p in home/dot_zsh/server home/dot_config/sheldon/plugin_sources/client.toml home/dot_local/bin/client home/dot_zsh/zshrc_client home/dot_zsh/zprofile_client home/private_dot_zlogin home/dot_zlogin home/dot_zpreztorc home/dot_zlogout home/dot_p10k.zsh; do [ -e "$p" ] && echo "EXISTS: $p" || echo "absent: $p"; done
absent: home/dot_zsh/server
absent: home/dot_config/sheldon/plugin_sources/client.toml
absent: home/dot_local/bin/client
absent: home/dot_zsh/zshrc_client
absent: home/dot_zsh/zprofile_client
absent: home/private_dot_zlogin
absent: home/dot_zlogin
absent: home/dot_zpreztorc
absent: home/dot_zlogout
absent: home/dot_p10k.zsh

$ git log --all --oneline -- "home/dot_config/sheldon/plugin_sources/client.toml"  (exact path, never added in history)
(empty output above confirms: never existed at this exact path)

$ git log --all --diff-filter=D --name-only --format=%H -- "home/dot_local/bin/client/*"
fd535883142b7bd4e4af9bd09533aae9726daaba

home/dot_local/bin/client/executable_login-ghcr
603a007d026f956018cf6a892ada7cfbec0445c9

home/dot_local/bin/client/executable_connect-hosei-vpn
home/dot_local/bin/client/executable_disconnect-vpn
(shows the directory was deleted in earlier commits fd53588 / 603a007, before this task)

$ git log --all --oneline -- "*zsh/server*" "*zshrc_client*" "*zprofile_client*"
(empty output above confirms: no zsh/server or *_client zsh path was ever added)

## bash -n syntax check on all new/changed shell scripts
$ bash -n install/ubuntu/client/zed.sh
OK
$ bash -n install/ubuntu/client/tailscale.sh
OK
$ bash -n install/ubuntu/client/misc.sh
OK
$ bash -n install/ubuntu/client/gnome_settings.sh
OK
$ bash -n scripts/lib/installer-pins.sh
OK
$ bash -n scripts/upgrade-tools.sh
OK

## make format
$ make format
shfmt --indent 4 --space-redirects --diff .

## make validate-agent-assets
$ make validate-agent-assets
uv run --with pyyaml scripts/validate-agent-assets.py
agent asset validation ok

## make unit-test (tail summary; full output is long, this is the closing summary line plus totals)
$ make unit-test
test_manifest_home_paths_reject_hard_coded_linux_home (test_validate_agent_assets.ValidateAgentAssetsTest.test_manifest_home_paths_reject_hard_coded_linux_home) ... [32mok[0m
test_manifest_home_paths_reject_non_codex_projects_mapping (test_validate_agent_assets.ValidateAgentAssetsTest.test_manifest_home_paths_reject_non_codex_projects_mapping) ... [32mok[0m
test_secret_scan_allows_exact_placeholder_tokens (test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_allows_exact_placeholder_tokens) ... [32mok[0m
test_secret_scan_checks_docs_paths (test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_checks_docs_paths) ... [32mok[0m
test_secret_scan_checks_extensionless_executables (test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_checks_extensionless_executables) ... [32mok[0m
test_secret_scan_checks_utf16_bom_text (test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_checks_utf16_bom_text) ... [32mok[0m
test_secret_scan_rejects_placeholder_with_suffix (test_validate_agent_assets.ValidateAgentAssetsTest.test_secret_scan_rejects_placeholder_with_suffix) ... [32mok[0m
test_checkout_does_not_persist_credentials_without_explicit_exemption (test_workflow_security.WorkflowSecurityTest.test_checkout_does_not_persist_credentials_without_explicit_exemption) ... [32mok[0m
test_checkout_rejects_duplicate_or_non_false_credential_settings (test_workflow_security.WorkflowSecurityTest.test_checkout_rejects_duplicate_or_non_false_credential_settings) ... [32mok[0m
test_checkout_setting_does_not_leak_from_the_next_step (test_workflow_security.WorkflowSecurityTest.test_checkout_setting_does_not_leak_from_the_next_step) ... [32mok[0m
test_external_actions_use_full_commit_shas (test_workflow_security.WorkflowSecurityTest.test_external_actions_use_full_commit_shas) ... [32mok[0m
test_quoted_unnamed_checkout_is_detected (test_workflow_security.WorkflowSecurityTest.test_quoted_unnamed_checkout_is_detected) ... [32mok[0m
test_unnamed_checkout_setting_does_not_leak_from_the_next_step (test_workflow_security.WorkflowSecurityTest.test_unnamed_checkout_setting_does_not_leak_from_the_next_step) ... [32mok[0m
test_workflows_have_exact_top_level_permissions (test_workflow_security.WorkflowSecurityTest.test_workflows_have_exact_top_level_permissions) ... [32mok[0m
test_workflows_have_no_job_level_permission_overrides (test_workflow_security.WorkflowSecurityTest.test_workflows_have_no_job_level_permission_overrides) ... [32mok[0m

----------------------------------------------------------------------
Ran 376 tests in 22.726s

[32mOK[0m ([33mskipped=1[0m)

## git log --oneline main..HEAD (T2+T3+T4 full history)
$ git log --oneline main..HEAD
481fb0f fix(mise): extend upgrade-tools test fixture for the B13a zed pin fetch
a8a1a8b chore: drop dead ignore entries and de-hardcode agmsg template home
c09a062 feat(ubuntu): port macos defaults to gnome gsettings on client
4d6f348 feat(ubuntu): install chromium and tailscale on client
0d53cc5 feat(ubuntu): install zed on client from pinned release
14a23b7 chore(orchestration): record dot-ubuntu-parity-T3-a01 worker artifacts
e7f1e9e fix(mise): finish yq backend migration in lock and tests
6df6aa1 fix(mise): update supply-chain checksum-block count for the B10 font externals
9871106 style(bin): satisfy shfmt on contextdb-codex-notify and herdr-agents
480b008 fix(git): correct hardcoded user.name
3add060 fix(gpg): configure pinentry on linux
63ca8f3 fix(ubuntu): wire orphaned server timezone setup script
04a73fe fix(fonts): ship JetBrainsMono on both OS and LINE Seed JP on linux
990c0bd feat(usage): schedule usage snapshot via systemd user timer on linux
07b8e3f fix(zsh): only add existing homebrew dirs to PATH
bb6e0f3 fix(ubuntu): guard server sourcing in client bashrc and remove stale server bin
dac183f chore(orchestration): record dot-ubuntu-parity-T2-a01 worker artifacts
70c5967 fix(claude): invoke herdr-agents attach hook by absolute path
352833b fix(doctor): tolerate cowork-synced skills and own crit codex skills
aaef350 fix(sheldon): drop dead ubuntu-command local plugin
fce3fc3 fix(agents): key codex project trust to the chezmoi working tree
f9223d9 fix(mise): normalize yq shim via aqua and adopt watchexec
720a3fd fix(ubuntu): add user to docker group on client install

## git status -sb (clean except .orchestration)
$ git status -sb
## feat/ubuntu-parity
?? .orchestration/reports/dot-ubuntu-parity-T4-a01.md
?? .orchestration/validation/dot-ubuntu-parity-T4-a01.md

## CompactionDB memory add
$ python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content "..."
returned id: befac170-eb33-46f8-859f-1a7d2e2a6581
