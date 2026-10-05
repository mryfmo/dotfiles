# T29 validation — dot-version-currency-T29-a01

All blocks are verbatim command output (ANSI codes may remain from test runners).

## task_rev verification
```
$ git rev-parse --short origin/main
00c77f5
$ git show 5b15d1e:.orchestration/tasks/dot-version-currency-T29-a01.md | sha256sum
7e1a66e44eabdd6734fe2c2e80ab45b6024da400a653211bc3f14a19d839429b  -
$ git merge-base --is-ancestor 5b15d1e HEAD && echo base-contains-task-commit
base-contains-task-commit
```

## 1. Renovate

First attempt: the npx cache reused a stale Renovate 37.440.7, which rejects `managerFilePatterns`:
```
$ npx --yes --package renovate -- renovate --version
37.440.7
$ npx --yes --package renovate@44.115.10 -- renovate-config-validator --strict renovate.json
npm error code ETARGET
npm error notarget No matching version found for renovate@44.115.10 with a date before 2026/9/20 13:19:33.
```
Validation with the newest guard-eligible Renovate 44:
```
$ npx --yes --package renovate@44 -- renovate --version
44.103.6
$ npx --yes --package renovate@44 -- renovate-config-validator --strict renovate.json
npm warn EBADENGINE Unsupported engine {
npm warn EBADENGINE   package: 'renovate@44.103.6',
npm warn EBADENGINE   required: { node: '^24.11.0', pnpm: '^11.0.0' },
npm warn EBADENGINE   current: { node: 'v26.9.0', npm: '11.19.1' }
npm warn EBADENGINE }
[32m INFO[39m: Validating renovate.json as global config
[32m INFO[39m: Config validated successfully against 1 file(s)
exit=0
$ npx --yes --package renovate@44 -- renovate-config-validator --strict   # repo-config mode, no file argument
[32m INFO[39m: Validating renovate.json
[32m INFO[39m: Config validated successfully against 1 file(s)
exit=
(The repo-mode `exit=` is empty because this shell is zsh, which has no PIPESTATUS. The `Config validated successfully` line is the result.)
```
Regex manager extraction against the real manifest (node, same JS RegExp as Renovate):
```
github-releases jdx/mise v2026.9.12
github-releases starship/starship v1.25.1
github-releases tomasz-tomczyk/crit v0.20.3
github-releases zed-industries/zed v1.21.0
crate sheldon 0.8.5
```

## 2. ccusage org move: grep before (origin/main) and after (HEAD)
```
$ git -C worker-c grep -n -iE 'ryoppippi|github\.com/[^ ]*ccusage' origin/main -- ':!.ua' ':!.orchestration'   # (origin/main)
exit=1
$ git -C worker-c grep -n -iE 'ryoppippi|github\.com/[^ ]*ccusage' HEAD -- ':!.ua' ':!.orchestration'   # (HEAD)
exit=1
```
There are zero references to the old org, so no files changed. The ccusage version is untouched (no mise/workflow/test/script files are in the diff stat below).

## 3. Understand-Anything pin resolution
```
$ gh api repos/Egonex-AI/Understand-Anything/commits/main --jq '.sha + " " + .commit.committer.date'
6df3065f1d8ddc2ce3615314d1d493f36d6b1c80 2026-09-12T05:31:43Z
$ gh api repos/Egonex-AI/Understand-Anything/compare/797ce7969312411be2e125c39628854166f055d7...6df3065f1d8ddc2ce3615314d1d493f36d6b1c80 --jq '.status + " ahead_by=" + (.ahead_by|tostring) + " behind_by=" + (.behind_by|tostring)'
ahead ahead_by=81 behind_by=0
$ for c in 797ce79… 6df3065…; do curl -fsSL https://raw.githubusercontent.com/Egonex-AI/Understand-Anything/$c/install.sh | shasum -a 256; done
797ce7969312411be2e125c39628854166f055d7  54f0350d09f43fcc8245f3f1fb2057bd322c36c6f158483dd47dcaf5f4a44eba
6df3065f1d8ddc2ce3615314d1d493f36d6b1c80  cb84ca53ced03f41662c5c86edf11fa598a0403c347f1e815f987ccaae5bc464
$ diff -u install-797ce79.sh install-6df3065.sh
--- /tmp/claude-1000/-home-moriya-Workspace-dotfiles/3e54f9a0-f011-4421-9a8a-a9eb113df7ad/scratchpad/t29/install-797ce79.sh	2026-09-27 13:17:48.829037047 +0900
+++ /tmp/claude-1000/-home-moriya-Workspace-dotfiles/3e54f9a0-f011-4421-9a8a-a9eb113df7ad/scratchpad/t29/install-6df3065.sh	2026-09-27 13:17:48.878422030 +0900
@@ -38,7 +38,7 @@
 vscode|$HOME/.copilot/skills|per-skill
 hermes|$HOME/.hermes/skills|folder
 cline|$HOME/.cline/skills|folder
-kimi|$HOME/.kimi/skills|folder
+kimi|$HOME/.kimi-code/skills|folder
 trae|$HOME/.trae/skills|per-skill
 nanobot|$HOME/.nanobot/workspace/skills|per-skill
 kiro|$HOME/.kiro/skills|per-skill
$ uv run --with pyyaml scripts/generate-agent-configs.py --set-asset understand-anything-installer.pin=6df3065f1d8ddc2ce3615314d1d493f36d6b1c80 --set-asset understand-anything-installer.sha256=cb84ca53ced03f41662c5c86edf11fa598a0403c347f1e815f987ccaae5bc464
asset pins updated: understand-anything-installer.pin, understand-anything-installer.sha256
$ git diff origin/main -- home/dot_agents/agent-config.yaml scripts/update-agent-assets.sh
diff --git a/home/dot_agents/agent-config.yaml b/home/dot_agents/agent-config.yaml
index 97ea1b1..03d8441 100644
--- a/home/dot_agents/agent-config.yaml
+++ b/home/dot_agents/agent-config.yaml
@@ -504,9 +504,9 @@ assets:
   understand-anything-installer:
     source: git-commit
     upstream: Egonex-AI/Understand-Anything
-    pin: 797ce7969312411be2e125c39628854166f055d7
+    pin: 6df3065f1d8ddc2ce3615314d1d493f36d6b1c80
     verify: sha256
-    sha256: 54f0350d09f43fcc8245f3f1fb2057bd322c36c6f158483dd47dcaf5f4a44eba
+    sha256: cb84ca53ced03f41662c5c86edf11fa598a0403c347f1e815f987ccaae5bc464
     install_path: ~/.understand-anything/repo
     installer: scripts/update-agent-assets.sh#update_codex_understand_anything
     render:
diff --git a/scripts/update-agent-assets.sh b/scripts/update-agent-assets.sh
index da49725..6f3da58 100755
--- a/scripts/update-agent-assets.sh
+++ b/scripts/update-agent-assets.sh
@@ -64,8 +64,8 @@ readonly CLAUDE_UNDERSTAND_ANYTHING_MARKETPLACE_NAME="understand-anything"
 # Rendered from assets.understand-anything-installer in
 # home/dot_agents/agent-config.yaml; change the commit and sha256 there together
 # after reviewing the upstream installer diff.
-readonly CODEX_UNDERSTAND_ANYTHING_INSTALLER_COMMIT="797ce7969312411be2e125c39628854166f055d7"
-readonly CODEX_UNDERSTAND_ANYTHING_INSTALLER_SHA256="54f0350d09f43fcc8245f3f1fb2057bd322c36c6f158483dd47dcaf5f4a44eba"
+readonly CODEX_UNDERSTAND_ANYTHING_INSTALLER_COMMIT="6df3065f1d8ddc2ce3615314d1d493f36d6b1c80"
+readonly CODEX_UNDERSTAND_ANYTHING_INSTALLER_SHA256="cb84ca53ced03f41662c5c86edf11fa598a0403c347f1e815f987ccaae5bc464"
 readonly CODEX_UNDERSTAND_ANYTHING_INSTALLER_URL="https://raw.githubusercontent.com/Egonex-AI/Understand-Anything/${CODEX_UNDERSTAND_ANYTHING_INSTALLER_COMMIT}/install.sh"
 # Versions and installer checksums for both URLs are pinned in
 # scripts/lib/installer-pins.sh and bumped by scripts/upgrade-tools.sh.
```

## 5. Policy-test baseline (new test vs origin/main export, then branch)
```
$ (origin/main export + new test) python3 -m unittest -v tests.unit.test_supply_chain_policy.SupplyChainPolicyTest.test_renovate_owns_dependency_update_notifications
test_renovate_owns_dependency_update_notifications (tests.unit.test_supply_chain_policy.SupplyChainPolicyTest.test_renovate_owns_dependency_update_notifications) ... [31mFAIL[0m

======================================================================
[31mFAIL[0m[1;31m: test_renovate_owns_dependency_update_notifications (tests.unit.test_supply_chain_policy.SupplyChainPolicyTest.test_renovate_owns_dependency_update_notifications)[0m
----------------------------------------------------------------------
Traceback (most recent call last):
  File [35m"/tmp/claude-1000/-home-moriya-Workspace-dotfiles/3e54f9a0-f011-4421-9a8a-a9eb113df7ad/scratchpad/t29/base.9aVO/tests/unit/test_supply_chain_policy.py"[0m, line [35m468[0m, in [35mtest_renovate_owns_dependency_update_notifications[0m
    [31mself.assertFalse[0m[1;31m((ROOT / ".github" / name).exists())[0m
    [31m~~~~~~~~~~~~~~~~[0m[1;31m^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^[0m
[1;35mAssertionError[0m: [35mTrue is not false[0m

----------------------------------------------------------------------
Ran 1 test in 0.000s

[1;31mFAILED[0m ([1;31mfailures=1[0m)
$ (branch) python3 -m unittest -v tests.unit.test_supply_chain_policy.SupplyChainPolicyTest.test_renovate_owns_dependency_update_notifications
test_renovate_owns_dependency_update_notifications (tests.unit.test_supply_chain_policy.SupplyChainPolicyTest.test_renovate_owns_dependency_update_notifications) ... [32mok[0m

----------------------------------------------------------------------
Ran 1 test in 0.000s

[32mOK[0m
```

## Required validation commands
```
$ uv run --with pyyaml scripts/generate-agent-configs.py --check
generated agent configs are up to date
exit=0
$ make validate-agent-assets
uv run --with pyyaml scripts/validate-agent-assets.py
agent asset validation ok
exit=0
```
```
$ make unit-test
uv run python -m unittest discover -s tests/unit -v
test_asset_repair_invokes_only_the_detected_step (test_check_agent_runtime.CheckAgentRuntimeTest.test_asset_repair_invokes_only_the_detected_step) ... <frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfe2533637a60>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfe2533637b50>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfe2533637970>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfe2533637790>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfe2533637d30>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfe2533637c40>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfe2533637f10>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfe2533637e20>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfe25334ec040>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfe25334ec130>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfe25334ec220>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfe25334ec310>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfe25334ec400>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfe25334ec4f0>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfe253391c310>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfe25334ec6d0>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfe25334ec8b0>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfe25334ec9a0>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfe25334ec7c0>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfe25334eca90>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfe25334ecb80>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfe25334ecc70>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfe25334ecd60>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfe25334ece50>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfe25334ecf40>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfe25334ed030>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfe25334ed120>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfe25334ed210>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfe25334ed300>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfe25334ec5e0>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfe25334ed4e0>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfe25334ed5d0>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfe25334ed3f0>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfe25334ed6c0>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfe25334ed8a0>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfe25334ed7b0>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfe25334ed990>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xfe25334edb70>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
ok
test_current_session_start_order_is_preserved (test_claude_settings_merge.ClaudeSettingsMergeTest.test_current_session_start_order_is_preserved)
test_managed_session_start_replacement_keeps_hook_order (test_claude_settings_merge.ClaudeSettingsMergeTest.test_managed_session_start_replacement_keeps_hook_order)
test_managed_session_start_replaces_stale_hard_coded_home_hook (test_claude_settings_merge.ClaudeSettingsMergeTest.test_managed_session_start_replaces_stale_hard_coded_home_hook)
test_model_profiles_reject_incomplete_or_unsafe_entries (test_generate_agent_configs.GenerateAgentConfigsTest.test_model_profiles_reject_incomplete_or_unsafe_entries) ... ERROR: model profile standard is missing codex
ERROR: model profile standard.claude.model must be a launcher-safe string
ERROR: model_profiles must define the express profile
ok
test_model_profiles_reject_unsafe_advisor (test_generate_agent_configs.GenerateAgentConfigsTest.test_model_profiles_reject_unsafe_advisor) ... ERROR: model profile standard.claude.advisor must be a launcher-safe string
ok
test_unknown_interactive_profile_fails (test_generate_agent_configs.GenerateAgentConfigsTest.test_unknown_interactive_profile_fails) ... ERROR: interactive_profile must name a model profile: 'missing'
ok
test_unknown_worker_kind_fails (test_generate_agent_configs.GenerateAgentConfigsTest.test_unknown_worker_kind_fails) ... ERROR: worker_kind must be one of ('codex', 'claude'): 'banana'
ok
test_unknown_worker_profile_fails (test_generate_agent_configs.GenerateAgentConfigsTest.test_unknown_worker_profile_fails) ... ERROR: worker_profile must name a model profile: 'missing'
ok
test_cli_workspace_resolves_macos_var_alias_identically (test_permgate.PermgateTest.test_cli_workspace_resolves_macos_var_alias_identically) ... skipped 'macOS /var alias only'
test_upgrade_uses_current_mise_node_after_runtime_replacement (test_runtime_health.RuntimeHealthTest.test_upgrade_uses_current_mise_node_after_runtime_replacement)
test_repo_claude_settings_reject_machine_specific_interpreter (test_validate_agent_assets.ValidateAgentAssetsTest.test_repo_claude_settings_reject_machine_specific_interpreter) ... ERROR: /tmp/validate-agent-assets-test-1fh07txu/.claude/settings.json hook SessionEnd must not hard-code a machine-specific home path: ~/.local/share/mise/installs/python/3.14.7/bin/python3.14
ok

----------------------------------------------------------------------
Ran 462 tests in 42.124s

OK (skipped=1)
exit=0
```
(Per-test `... ok` lines are elided. The remaining `ERROR:` lines are expected stderr from passing negative tests.)
```
$ git -C ~/Workspace/dotfiles/.claude/worktrees/worker-c diff origin/main --stat
 .github/dependabot.yml                             |   6 -
 .../tasks/dot-codex-apparmor-userns-T30-a01.md     | 123 ---------------------
 AGENTS.md                                          |   6 +
 home/dot_agents/agent-config.yaml                  |   4 +-
 renovate.json                                      |  45 ++++++++
 scripts/update-agent-assets.sh                     |   4 +-
 tests/unit/test_supply_chain_policy.py             |  27 ++++-
 7 files changed, 76 insertions(+), 139 deletions(-)
$ git log --oneline -1
c57c3cf chore(deps): adopt Renovate, pin Understand-Anything installer to 6df3065
$ gh pr view 191 --json number,url,headRefOid
[1;37m{[m
  [1;34m"headRefOid"[m[1;37m:[m [32m"c57c3cf77965cc9edcfb7dc31cc52b320dcb38ab"[m[1;37m,[m
  [1;34m"number"[m[1;37m:[m 191[1;37m,[m
  [1;34m"url"[m[1;37m:[m [32m"https://github.com/mryfmo/dotfiles/pull/191"[m
[1;37m}[m
$ gh pr checks 191
CodeRabbit	pass	0		Review skipped: manual review required for this OSS repository
changes	pass	5s	https://github.com/mryfmo/dotfiles/actions/runs/36294191082/job/108549868016	
private-bootstrap (macos-14, client)	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/36294191123/job/108549868247	
private-bootstrap (ubuntu-latest, client)	pass	5s	https://github.com/mryfmo/dotfiles/actions/runs/36294191123/job/108549868287	
public-bootstrap (macos-14, client)	pass	6m55s	https://github.com/mryfmo/dotfiles/actions/runs/36294191123/job/108549868215	
nix	skipping	0	https://github.com/mryfmo/dotfiles/actions/runs/36294191082/job/108549885303	
private-bootstrap (ubuntu-latest, server)	pass	4s	https://github.com/mryfmo/dotfiles/actions/runs/36294191123/job/108549868104	
public-bootstrap (ubuntu-latest, client)	pass	9m3s	https://github.com/mryfmo/dotfiles/actions/runs/36294191123/job/108549868207	
public-bootstrap (ubuntu-latest, server)	pass	7m3s	https://github.com/mryfmo/dotfiles/actions/runs/36294191123/job/108549868212	
test (macos-14, client)	pass	2m19s	https://github.com/mryfmo/dotfiles/actions/runs/36294191082/job/108549884402	
test (ubuntu-latest, client)	pass	5m20s	https://github.com/mryfmo/dotfiles/actions/runs/36294191082/job/108549884438	
test (ubuntu-latest, server)	pass	2m8s	https://github.com/mryfmo/dotfiles/actions/runs/36294191082/job/108549884448	
validate	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/36294191078/job/108549867893	
exit=0
```

## CompactionDB
```
$ python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content "T29: Renovate replaces Dependabot (mise manager at home/dot_mise/config.toml; manifest pins notification-only), ccusage references follow the org move, UA installer pinned to 6df3065, AGENTS.md codified as canonical with CLAUDE.md as Claude-only shim (operator 2026-09-27)"
be406d1a-d948-4866-b447-245036f85e0d
```

## Branch-only diff (origin/main advanced after branching)

`origin/main` moved past the branch base 5b15d1e (orchestrator commit below), so the two-dot `--stat` above lists that commit's T30 task file as a deletion. The branch does not touch it. Merge-base diff:
```
$ git log --oneline 5b15d1e..origin/main
00c77f5 chore(orchestration): T30 task - AppArmor userns profile restoring sandboxed codex (operator decision)
$ git diff origin/main...HEAD --stat
 .github/dependabot.yml                 |  6 -----
 AGENTS.md                              |  6 +++++
 home/dot_agents/agent-config.yaml      |  4 +--
 renovate.json                          | 45 ++++++++++++++++++++++++++++++++++
 scripts/update-agent-assets.sh         |  4 +--
 tests/unit/test_supply_chain_policy.py | 27 +++++++++++++++-----
 6 files changed, 76 insertions(+), 16 deletions(-)
$ git diff 5b15d1e HEAD --stat
 .github/dependabot.yml                 |  6 -----
 AGENTS.md                              |  6 +++++
 home/dot_agents/agent-config.yaml      |  4 +--
 renovate.json                          | 45 ++++++++++++++++++++++++++++++++++
 scripts/update-agent-assets.sh         |  4 +--
 tests/unit/test_supply_chain_policy.py | 27 +++++++++++++++-----
 6 files changed, 76 insertions(+), 16 deletions(-)
```
