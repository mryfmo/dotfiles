# dot-ubuntu-parity-T8-a01 — validation (verbatim)

## Pre-branch: confirm origin/main already has T7

$ git fetch origin
From https://github.com/mryfmo/dotfiles
4fa45bc..b1d1641 main -> origin/main

$ git log --oneline origin/main -3
b1d1641 chore(orchestration): accept T7 and file T8 (zed fresh-home bug)
b1d7a90 chore(orchestration): record dot-ubuntu-parity-T7-a01 worker artifacts
ec15006 fix(tests): resolve interpreters and core tools under stripped PATH in T4 bats

$ git checkout -b fix/zed-fresh-home origin/main
Switched to a new branch 'fix/zed-fresh-home'
branch 'fix/zed-fresh-home' set up to track 'origin/main'.

## The fix in install/ubuntu/client/zed.sh

$ git diff install/ubuntu/client/zed.sh
--- a/install/ubuntu/client/zed.sh
+++ b/install/ubuntu/client/zed.sh
@@ -68,9 +68,9 @@ function install_pinned_zed() (
}

     tar -xzf "${download}" -C "${tmpdir}" || return

- rm -rf "${staging}"
- mv "${tmpdir}/zed.app" "${staging}" || return
  mkdir -p "$(dirname "${ZED_APP_DIR}")" || return

* rm -rf "${staging}"
* mv "${tmpdir}/zed.app" "${staging}" || return
  rm -rf "${ZED_APP_DIR}"
     mv "${staging}" "${ZED_APP_DIR}"
  )

## Removing T7's now-unneeded test workaround

$ git diff tests/install/ubuntu/client/zed.bats
--- a/tests/install/ubuntu/client/zed.bats
+++ b/tests/install/ubuntu/client/zed.bats
@@ -31,8 +31,6 @@
@test "[ubuntu-client] main downloads, verifies, and links zed when not already installed" {

- mkdir -p "${BATS_TEST_TMPDIR}/.local/share"
-     run env HOME="${BATS_TEST_TMPDIR}" bash -c '

## Target test, verified green without the workaround

$ bats -f "main downloads, verifies, and links zed when not already installed" tests/install/ubuntu/client/zed.bats
1..1
ok 1 [ubuntu-client] main downloads, verifies, and links zed when not already installed

## Syntax check on the modified script

$ bash -n install/ubuntu/client/zed.sh && echo "bash -n OK"
bash -n OK

## make format

$ shfmt --indent 4 --space-redirects --diff install/ubuntu/client/zed.sh tests/install/ubuntu/client/zed.bats
(no output — clean)

## uv run python -m unittest discover -s tests/unit -v

... (tail) ...
test_external_actions_use_full_commit_shas (test_workflow_security.WorkflowSecurityTest.test_external_actions_use_full_commit_shas) ... ok
test_quoted_unnamed_checkout_is_detected (test_workflow_security.WorkflowSecurityTest.test_quoted_unnamed_checkout_is_detected) ... ok
test_unnamed_checkout_setting_does_not_leak_from_the_next_step (test_workflow_security.WorkflowSecurityTest.test_unnamed_checkout_setting_does_not_leak_from_the_next_step) ... ok
test_workflows_have_exact_top_level_permissions (test_workflow_security.WorkflowSecurityTest.test_workflows_have_exact_top_level_permissions) ... ok
test_workflows_have_no_job_level_permission_overrides (test_workflow_security.WorkflowSecurityTest.test_workflows_have_no_job_level_permission_overrides) ... ok

---

Ran 376 tests in 23.366s

OK (skipped=1)

## uv run --with pyyaml scripts/validate-agent-assets.py

$ uv run --with pyyaml scripts/validate-agent-assets.py
agent asset validation ok

## Commit

$ git add install/ubuntu/client/zed.sh tests/install/ubuntu/client/zed.bats
$ git -c commit.gpgsign=false commit -m "fix(ubuntu): create zed parent dir before staging move ..."
[fix/zed-fresh-home 96e59cf] fix(ubuntu): create zed parent dir before staging move
2 files changed, 1 insertion(+), 3 deletions(-)

$ git log --oneline -3
96e59cf fix(ubuntu): create zed parent dir before staging move
b1d1641 chore(orchestration): accept T7 and file T8 (zed fresh-home bug)
b1d7a90 chore(orchestration): record dot-ubuntu-parity-T7-a01 worker artifacts

## CompactionDB memory add (decision, resolves T7's failure record)

$ python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content "..."
c614ffea-f9be-4564-8a48-ec2b9f7c76cb
