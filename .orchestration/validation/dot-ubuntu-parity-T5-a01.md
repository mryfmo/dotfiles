# dot-ubuntu-parity-T5-a01 — validation (verbatim)

## Pre-branch verification: origin/main already contains T2-T4 content

$ git fetch origin
(no output)

$ git log --oneline origin/main -15
8810fef chore(orchestration): record dot-ubuntu-parity-T4-a01 worker artifacts
93fcb45 fix(mise): extend upgrade-tools test fixture for the B13a zed pin fetch
fc551f2 chore: drop dead ignore entries and de-hardcode agmsg template home
b2293ba feat(ubuntu): port macos defaults to gnome gsettings on client
9e8f2ac feat(ubuntu): install chromium and tailscale on client
1735147 feat(ubuntu): install zed on client from pinned release
1162141 chore(orchestration): record dot-ubuntu-parity-T3-a01 worker artifacts
e79bcf6 fix(mise): finish yq backend migration in lock and tests
55e7335 fix(mise): update supply-chain checksum-block count for the B10 font externals
42ce5f2 style(bin): satisfy shfmt on contextdb-codex-notify and herdr-agents
7bc96cd fix(git): correct hardcoded user.name
49dc373 fix(gpg): configure pinentry on linux
20e97a5 fix(ubuntu): wire orphaned server timezone setup script
1c77521 fix(fonts): ship JetBrainsMono on both OS and LINE Seed JP on linux
7c9a18b feat(usage): schedule usage snapshot via systemd user timer on linux

$ git show origin/main:home/dot_mise/config.toml | grep -n yq
19:"aqua:mikefarah/yq" = "4.53.6"

Confirms origin/main carries all of T2-T4's changes (same commit subjects,
different hashes than this worktree's feat/ubuntu-parity — consistent with a
rebase/re-apply rather than fast-forward merge), matching the task file's
stated rationale for branching from main instead of feat/ubuntu-parity.

$ git checkout -b fix/usage-timer-ordering origin/main
Switched to a new branch 'fix/usage-timer-ordering'
branch 'fix/usage-timer-ordering' set up to track 'origin/main'.

## Other run_once scripts checked for the same ordering dependency

$ cat home/.chezmoiscripts/ubuntu/run_once_52-client-install-zed.sh.tmpl
#!/usr/bin/env bash

set -Eeuo pipefail

{{ if eq .chezmoi.os "linux" -}}
{{   if eq .chezmoi.osRelease.idLike "debian" -}}
{{     if eq .system "client" -}}
(
{{       include "../scripts/lib/installer-pins.sh" }}
{{       include "../install/ubuntu/client/zed.sh" }}
)
{{     end -}}
{{   end -}}
{{ end -}}

$ cat home/.chezmoiscripts/ubuntu/run_once_53-client-install-tailscale.sh.tmpl
{{ if eq .chezmoi.os "linux" -}}
{{   if eq .chezmoi.osRelease.idLike "debian" -}}
{{     if eq .system "client" -}}
{{       include "../install/ubuntu/client/tailscale.sh" }}
{{     end -}}
{{   end -}}
{{ end -}}

$ cat home/.chezmoiscripts/ubuntu/run_once_99-client-gnome-defaults.sh.tmpl
{{ if eq .chezmoi.os "linux" -}}
{{   if eq .chezmoi.osRelease.idLike "debian" -}}
{{     if eq .system "client" -}}
{{       include "../install/ubuntu/client/gnome_settings.sh" }}
{{     end -}}
{{   end -}}
{{ end -}}

$ cat home/.chezmoiscripts/ubuntu/run_once_50-server-setup-timezone.sh.tmpl
{{ if eq .chezmoi.os "linux" -}}
{{   if eq .chezmoi.osRelease.idLike "debian" -}}
{{     if eq .system "server" -}}
{{       include "../install/ubuntu/server/setup_timezone.sh" }}
{{     end -}}
{{   end -}}
{{ end -}}

None reference any home/dot_config/\*\* or other chezmoi target path — all
four only include repo-tracked installer scripts. No ordering dependency,
no change needed for any of them.

## Filename-reference search (rename safety)

$ grep -rn "run_onchange_60-enable-usage-snapshot-timer\|60-enable-usage-snapshot" --include="_.bats" --include="_.py" --include="\*.tmpl" .
(no output — no matches)

## The rename

$ git mv home/.chezmoiscripts/ubuntu/run_onchange_60-enable-usage-snapshot-timer.sh.tmpl home/.chezmoiscripts/ubuntu/run_onchange_after_60-enable-usage-snapshot-timer.sh.tmpl
$ git status --short
R home/.chezmoiscripts/ubuntu/run_onchange_60-enable-usage-snapshot-timer.sh.tmpl -> home/.chezmoiscripts/ubuntu/run_onchange_after_60-enable-usage-snapshot-timer.sh.tmpl

## make format

$ make format
shfmt --indent 4 --space-redirects --diff .
(no diff output — clean)

## make unit-test (uv run python -m unittest discover -s tests/unit -v)

... (374 lines of individual test names omitted for brevity; tail below) ...
test_checkout_does_not_persist_credentials_without_explicit_exemption (test_workflow_security.WorkflowSecurityTest.test_checkout_does_not_persist_credentials_without_explicit_exemption) ... ok
test_checkout_rejects_duplicate_or_non_false_credential_settings (test_workflow_security.WorkflowSecurityTest.test_checkout_rejects_duplicate_or_non_false_credential_settings) ... ok
test_checkout_setting_does_not_leak_from_the_next_step (test_workflow_security.WorkflowSecurityTest.test_checkout_setting_does_not_leak_from_the_next_step) ... ok
test_external_actions_use_full_commit_shas (test_workflow_security.WorkflowSecurityTest.test_external_actions_use_full_commit_shas) ... ok
test_quoted_unnamed_checkout_is_detected (test_workflow_security.WorkflowSecurityTest.test_quoted_unnamed_checkout_is_detected) ... ok
test_unnamed_checkout_setting_does_not_leak_from_the_next_step (test_workflow_security.WorkflowSecurityTest.test_unnamed_checkout_setting_does_not_leak_from_the_next_step) ... ok
test_workflows_have_exact_top_level_permissions (test_workflow_security.WorkflowSecurityTest.test_workflows_have_exact_top_level_permissions) ... ok
test_workflows_have_no_job_level_permission_overrides (test_workflow_security.WorkflowSecurityTest.test_workflows_have_no_job_level_permission_overrides) ... ok

---

Ran 376 tests in 23.230s

OK (skipped=1)
RC=0

## make validate-agent-assets (uv run --with pyyaml scripts/validate-agent-assets.py)

$ uv run --with pyyaml scripts/validate-agent-assets.py
agent asset validation ok
RC=0

## Commit

$ git -c commit.gpgsign=false commit -m "fix(usage): run timer enablement after files are applied ..."
[fix/usage-timer-ordering 026ce2e] fix(usage): run timer enablement after files are applied
1 file changed, 0 insertions(+), 0 deletions(-)
rename home/.chezmoiscripts/ubuntu/{run_onchange_60-enable-usage-snapshot-timer.sh.tmpl => run_onchange_after_60-enable-usage-snapshot-timer.sh.tmpl} (100%)

$ git log --oneline -3
026ce2e fix(usage): run timer enablement after files are applied
8810fef chore(orchestration): record dot-ubuntu-parity-T4-a01 worker artifacts
93fcb45 fix(mise): extend upgrade-tools test fixture for the B13a zed pin fetch

## CompactionDB memory add

$ python3 .claude/hooks/contextdb*cli.py memory add --kind decision --scope project --content "chezmoi executes .chezmoiscripts entries in target-name lexical order interleaved with file application (.chezmoiscripts/... sorts before .config/... on a fresh bootstrap). A script that depends on files chezmoi applies (e.g. enabling a systemd unit shipped via home/dot_config/\*\*) must use the run_onchange_after* / run*once_after* prefix so chezmoi defers it until all target state is applied, matching the existing run_once_after_04-install-aws-cli.sh.tmpl convention."
ebab46ec-b613-400d-91ac-2b2a0de8ee88

## git status -sb after commit (clean except this task's own artifacts, not yet written at time of this command)

$ git status -sb

## fix/usage-timer-ordering
