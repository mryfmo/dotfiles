# dot-ubuntu-parity-T6-a01 — validation (verbatim)

## Pre-branch: confirm origin/main already has T5

$ git fetch origin
(no output)

$ git log --oneline origin/main -3
2bf351f chore(orchestration): accept T5
fe2b64e chore(orchestration): record dot-ubuntu-parity-T5-a01 worker artifacts
ba6f6a8 fix(usage): run timer enablement after files are applied

$ git checkout -b fix/drop-ineffective-chezmoiremove origin/main
Switched to a new branch 'fix/drop-ineffective-chezmoiremove'
branch 'fix/drop-ineffective-chezmoiremove' set up to track 'origin/main'.

## Confirm the ignore/remove conflict is real in this repo

$ cat home/.chezmoitemplates/chezmoiignore.d/ubuntu/client
.local/bin/server

.bash/server/bashrc

$ cat home/.chezmoiremove
.codex/ccgate.jsonnet
.claude/ccgate.jsonnet
.local/bin/common/start-cognee-mcp
{{ if and (eq .chezmoi.os "linux") (eq .system "client") }}
.local/bin/server
{{ end }}

Confirms .local/bin/server is unconditionally ignored for ubuntu/client,
and the same path is guarded into .chezmoiremove for exactly linux+client —
the ignore always applies wherever the remove entry would, so the remove
entry is provably a no-op on every host it targets.

## Reference-search before editing

$ grep -rn "chezmoiremove\|\.local/bin/server" tests/unit/
tests/unit/test_runtime_health.py:51: server = home / ".local/bin/server"

(Context checked: this is an unrelated bashrc-guard test fixture from B7,
not an assertion on .chezmoiremove content — see report.)

## The edit

$ git diff home/.chezmoiremove
diff --git a/home/.chezmoiremove b/home/.chezmoiremove
index 4d7b851..adf91fd 100644
--- a/home/.chezmoiremove
+++ b/home/.chezmoiremove
@@ -1,6 +1,3 @@
.codex/ccgate.jsonnet
.claude/ccgate.jsonnet
.local/bin/common/start-cognee-mcp -{{ if and (eq .chezmoi.os "linux") (eq .system "client") }}
-.local/bin/server -{{ end }}

## make unit-test (uv run python -m unittest discover -s tests/unit -v)

... (tail) ...
test_checkout_does_not_persist_credentials_without_explicit_exemption (test_workflow_security.WorkflowSecurityTest.test_checkout_does_not_persist_credentials_without_explicit_exemption) ... ok
test_checkout_rejects_duplicate_or_non_false_credential_settings (test_workflow_security.WorkflowSecurityTest.test_checkout_rejects_duplicate_or_non_false_credential_settings) ... ok
test_checkout_setting_does_not_leak_from_the_next_step (test_workflow_security.WorkflowSecurityTest.test_checkout_setting_does_not_leak_from_the_next_step) ... ok
test_external_actions_use_full_commit_shas (test_workflow_security.WorkflowSecurityTest.test_external_actions_use_full_commit_shas) ... ok
test_quoted_unnamed_checkout_is_detected (test_workflow_security.WorkflowSecurityTest.test_quoted_unnamed_checkout_is_detected) ... ok
test_unnamed_checkout_setting_does_not_leak_from_the_next_step (test_workflow_security.WorkflowSecurityTest.test_unnamed_checkout_setting_does_not_leak_from_the_next_step) ... ok
test_workflows_have_exact_top_level_permissions (test_workflow_security.WorkflowSecurityTest.test_workflows_have_exact_top_level_permissions) ... ok
test_workflows_have_no_job_level_permission_overrides (test_workflow_security.WorkflowSecurityTest.test_workflows_have_no_job_level_permission_overrides) ... ok

---

Ran 376 tests in 23.854s

OK (skipped=1)

## Commit

$ git add home/.chezmoiremove
$ git -c commit.gpgsign=false commit -m "fix(chezmoi): drop ineffective .chezmoiremove entry for ignored path ..."
[fix/drop-ineffective-chezmoiremove 7813ebc] fix(chezmoi): drop ineffective .chezmoiremove entry for ignored path
1 file changed, 3 deletions(-)

$ git log --oneline -3
7813ebc fix(chezmoi): drop ineffective .chezmoiremove entry for ignored path
2bf351f chore(orchestration): accept T5
fe2b64e chore(orchestration): record dot-ubuntu-parity-T5-a01 worker artifacts

## CompactionDB memory add

$ python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content "chezmoi の .chezmoiignore は .chezmoiremove に優先する: ignore されたターゲットパスは target state の計算から除外されるため、.chezmoiremove に同じパスを列挙しても宣言的には削除されない(chezmoi の仕様)。ignore 済みパスの残骸を掃除するには、手動削除するか ignore 自体を解除する必要がある。"
e9d5e7c0-93f7-47c2-8899-25df46df03b9
