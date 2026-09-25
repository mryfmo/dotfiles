# dot-ubuntu-parity-T9-a01 — validation (verbatim)

## Pre-branch: confirm origin/main already has T8

$ git fetch origin
From https://github.com/mryfmo/dotfiles
b1d1641..95bd97c main -> origin/main

$ git log --oneline origin/main -3
95bd97c chore(orchestration): accept T8
d93552c chore(orchestration): record dot-ubuntu-parity-T8-a01 worker artifacts
96e59cf fix(ubuntu): create zed parent dir before staging move

$ git checkout -b fix/usage-timer-visibility origin/main
Switched to a new branch 'fix/usage-timer-visibility'
branch 'fix/usage-timer-visibility' set up to track 'origin/main'.

## Confirm setup.sh's CI temp-destDir guard (the task's technical premise)

$ grep -n "destDir\|RUNNER_TEMP\|CI" setup.sh
...
344: if is_ci && { [ -z "${RUNNER_TEMP:-}" ] || [["${HOME}/" != "${RUNNER_TEMP%/}/"*]]; }; then
345: echo "Refusing to apply in CI outside RUNNER_TEMP: ${HOME}" >&2

Confirms: in CI, setup.sh requires the apply's $HOME to be under
RUNNER_TEMP, i.e. a temp destDir — never the real $HOME.

## The fix

$ git diff home/.chezmoiscripts/ubuntu/run_onchange_after_60-enable-usage-snapshot-timer.sh.tmpl
--- a/home/.chezmoiscripts/ubuntu/run_onchange_after_60-enable-usage-snapshot-timer.sh.tmpl
+++ b/home/.chezmoiscripts/ubuntu/run_onchange_after_60-enable-usage-snapshot-timer.sh.tmpl
@@ -14,6 +14,14 @@
exit 0
fi

+# systemctl --user always reads the real user's XDG config dir, regardless of
+# any $HOME override chezmoi applied under (e.g. CI's RUNNER_TEMP destDir).
+# Guard on the unit actually being visible there, not just on chezmoi having
+# rendered it: this covers both a temp-destDir apply (unit written but never
+# in this path) and any future run-order regression, with a single check.
+if [ ! -f "${XDG_CONFIG_HOME:-${HOME}/.config}/systemd/user/usage-snapshot.timer" ]; then

- echo "unit not visible to the user manager (temp destDir apply?); skipping" >&2
- exit 0
  +fi
- systemctl --user daemon-reload
  systemctl --user enable --now usage-snapshot.timer

## Confirm this machine's real chezmoi data matches an ubuntu client (no faking needed)

$ chezmoi data --format json | python3 -c "..."
system: client
os: linux
osRelease.idLike: debian
homeDir: /home/moriya
workingTree: /home/moriya/.local/share/chezmoi

## Render the modified template against THIS worktree's source

$ chezmoi execute-template -S "$(pwd)/home" '{{ .chezmoi.sourceDir }}'
/home/moriya/Workspace/worktrees/chezmoi-ubuntu-parity/home

$ chezmoi execute-template -S "$(pwd)/home" --file home/.chezmoiscripts/ubuntu/run_onchange_after_60-enable-usage-snapshot-timer.sh.tmpl
#!/usr/bin/env bash

set -Eeuo pipefail

# This script only runs (chezmoi run_onchange) when its rendered content

# changes. Embed the units' content hashes so an edit to either unit file

# also changes this script's content and re-triggers the enable/reload below.

# usage-snapshot.service sha256sum: df2d0f24d488aeb9c89ddea755e8424d39ac20e2e49022f4a726ce0e48353e13

# usage-snapshot.timer sha256sum: 2fb92d0aeded5ca6d6da0cd3264345ac676fb9ec08e0a8294cea2281dc781f3d

if ! command -v systemctl > /dev/null 2>&1 || [ -z "${XDG_RUNTIME_DIR:-}" ] || ! systemctl --user status > /dev/null 2>&1; then
echo "No user systemd instance available; skipping usage-snapshot timer setup." >&2
exit 0
fi

# systemctl --user always reads the real user's XDG config dir, regardless of

# any $HOME override chezmoi applied under (e.g. CI's RUNNER_TEMP destDir).

# Guard on the unit actually being visible there, not just on chezmoi having

# rendered it: this covers both a temp-destDir apply (unit written but never

# in this path) and any future run-order regression, with a single check.

if [ ! -f "${XDG_CONFIG_HOME:-${HOME}/.config}/systemd/user/usage-snapshot.timer" ]; then
echo "unit not visible to the user manager (temp destDir apply?); skipping" >&2
exit 0
fi

systemctl --user daemon-reload
systemctl --user enable --now usage-snapshot.timer

## bash -n on the rendered script

$ bash -n rendered_timer_script.sh && echo "bash -n OK"
bash -n OK

## Scenario (a): real $HOME (unit already exists and already enabled)

$ ls -la "${XDG_CONFIG_HOME:-$HOME/.config}/systemd/user/usage-snapshot.timer"
-rw-rw-r-- 1 moriya moriya 147 9 月 23 08:37 /home/moriya/.config/systemd/user/usage-snapshot.timer

$ systemctl --user is-enabled usage-snapshot.timer
enabled

$ bash rendered_timer_script.sh; echo "SCENARIO_A_EXIT=$?"
SCENARIO_A_EXIT=0

## Scenario (b): $HOME pointed at an empty temp directory (unit absent)

$ tmp="$(mktemp -d)"
$ env HOME="${tmp}" XDG_RUNTIME_DIR="${XDG_RUNTIME_DIR}" bash rendered_timer_script.sh
unit not visible to the user manager (temp destDir apply?); skipping
$ echo "SCENARIO_B_EXIT=$?"
SCENARIO_B_EXIT=0
$ rm -rf "${tmp}"

## make format (the actual project gate)

$ shfmt --indent 4 --space-redirects --diff .
(no output — clean)

Note: a direct single-file `shfmt --diff <this file>` invocation reports an
indentation diff on lines this task did not touch (the nested `{{ if }}`
template directive indentation). Confirmed this is pre-existing and NOT
introduced by this change, and NOT something the real gate enforces:

$ git show HEAD:home/.chezmoiscripts/ubuntu/run_onchange_after_60-enable-usage-snapshot-timer.sh.tmpl > /tmp/pre_edit.sh.tmpl
$ shfmt --indent 4 --space-redirects --diff /tmp/pre_edit.sh.tmpl
(same diff appears on the pre-edit HEAD version — confirms pre-existing, not new)

$ shfmt --indent 4 --space-redirects --diff .
(no output — confirms the whole-repo walk that `make format` actually
runs does not pick up .sh.tmpl files at all, so this file was never
covered by the real gate in T2-T8 either)

## uv run python -m unittest discover -s tests/unit -v

... (tail) ...
test_external_actions_use_full_commit_shas (test_workflow_security.WorkflowSecurityTest.test_external_actions_use_full_commit_shas) ... ok
test_quoted_unnamed_checkout_is_detected (test_workflow_security.WorkflowSecurityTest.test_quoted_unnamed_checkout_is_detected) ... ok
test_unnamed_checkout_setting_does_not_leak_from_the_next_step (test_workflow_security.WorkflowSecurityTest.test_unnamed_checkout_setting_does_not_leak_from_the_next_step) ... ok
test_workflows_have_exact_top_level_permissions (test_workflow_security.WorkflowSecurityTest.test_workflows_have_exact_top_level_permissions) ... ok
test_workflows_have_no_job_level_permission_overrides (test_workflow_security.WorkflowSecurityTest.test_workflows_have_no_job_level_permission_overrides) ... ok

---

Ran 376 tests in 23.649s

OK (skipped=1)

## uv run --with pyyaml scripts/validate-agent-assets.py

$ uv run --with pyyaml scripts/validate-agent-assets.py
agent asset validation ok

## Commit

$ git add home/.chezmoiscripts/ubuntu/run_onchange_after_60-enable-usage-snapshot-timer.sh.tmpl
$ git -c commit.gpgsign=false commit -m "fix(usage): only enable the timer when its unit is visible to the user manager ..."
[fix/usage-timer-visibility 7e8ef1d] fix(usage): only enable the timer when its unit is visible to the user manager
1 file changed, 10 insertions(+)

$ git log --oneline -3
7e8ef1d fix(usage): only enable the timer when its unit is visible to the user manager
95bd97c chore(orchestration): accept T8
d93552c chore(orchestration): record dot-ubuntu-parity-T8-a01 worker artifacts

## CompactionDB memory add (decision)

$ python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content "..."
90f10560-425a-4dd8-9cb9-19bee270ef73
