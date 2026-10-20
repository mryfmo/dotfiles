# Independent security-profile worker verification

Manifest profile gpt-6-astra/high; fresh context, read-only scope. Exact command:

````sh
PATH=/private/tmp/a012-t133-a04-parent-bin:/usr/bin:/bin UV_CACHE_DIR=~/Workspace/dotfiles/.claude/worktrees/worker-g/.uv-cache ~/.local/share/mise/installs/python/3.15.0/bin/python3.15 -B -I -c 'import sys,unittest;sys.path.insert(0,"tests/unit");from test_task_consistency_c11_c15 import TaskConsistencyC11C15Test;names=["test_gh_child_preserves_parent_tokens","test_checker_rejects_untrusted_bindings_and_git_configuration","test_isolated_child_and_same_bytes_survive_hostile_startup_inputs","test_c15_uses_canonical_main_only","test_c6_receipt_uses_canonical_design_bytes","test_path_grammar_rejects_escaping_scopes"];suite=unittest.TestSuite(TaskConsistencyC11C15Test(n) for n in names);r=unittest.TextTestRunner(verbosity=2).run(suite);sys.exit(not r.wasSuccessful())'
````

Complete combined stdout/stderr; exit0:

````text
fixture-seed python=~/.local/share/mise/installs/python/3.15.0/bin/python3.15 uv=~/.local/share/mise/installs/uv/0.13.1/uv-aarch64-apple-darwin/uv exit=0

test_gh_child_preserves_parent_tokens (test_task_consistency_c11_c15.TaskConsistencyC11C15Test.test_gh_child_preserves_parent_tokens) ... ok
test_checker_rejects_untrusted_bindings_and_git_configuration (test_task_consistency_c11_c15.TaskConsistencyC11C15Test.test_checker_rejects_untrusted_bindings_and_git_configuration) ... ok
test_isolated_child_and_same_bytes_survive_hostile_startup_inputs (test_task_consistency_c11_c15.TaskConsistencyC11C15Test.test_isolated_child_and_same_bytes_survive_hostile_startup_inputs) ... ok
test_c15_uses_canonical_main_only (test_task_consistency_c11_c15.TaskConsistencyC11C15Test.test_c15_uses_canonical_main_only) ... ok
test_c6_receipt_uses_canonical_design_bytes (test_task_consistency_c11_c15.TaskConsistencyC11C15Test.test_c6_receipt_uses_canonical_design_bytes) ... ok
test_path_grammar_rejects_escaping_scopes (test_task_consistency_c11_c15.TaskConsistencyC11C15Test.test_path_grammar_rejects_escaping_scopes) ... ok

----------------------------------------------------------------------
Ran 6 tests in 8.756s

OK
````

Verdict: correct

Worker review only; no final integration audit, deployment, Bats or live CI. Parent execution/shared cache/shared UID/shared credentials remain owned residuals.
