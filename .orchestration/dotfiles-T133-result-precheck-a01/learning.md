---
task_id: dotfiles-T133-result-precheck-a01
round: 1
amendment: 1
---

# Learning

Task-local triage; nothing promoted.

- `make format` (`shfmt --diff .`) fails on `origin/main` itself: it covers twelve tracked files CI's `shfmt` step never formats. Any gate built on `make format` fails every head; a gate that mirrors CI uses CI's commands and scopes (Amendment 1). Applies to any new check or hook that reuses a Makefile target as a pass condition.
- A precheck's checks must run on the head they record, so the script refuses a tree with changes outside its evidence directory; bytecode is ignored by `.gitignore`, so a test fixture repository needs the same ignore line or a second run sees its own `__pycache__`. Applies to tests of tree-clean guards.
- A program that ends by `exec`-ing its last command skips its own EXIT trap, so temporary directories and worktrees survive; the precheck runs its writer as a plain last command under `set -e`. Applies to bash scripts with cleanup traps.
- In a Claude seat's sandbox `make unit-test` fails 296 tests that pass in CI (the identical set on `origin/main` 99a4a80f; 136 in test_require_crit_review, 82 in test_herdr_agents, 28 in test_agent_stop_gate, the rest in six modules), so the precheck's default `unit-test` check cannot be green there; this task recorded a `--tests` run of its own modules (report.md). Applies to every Claude seat running the precheck until those tests stop depending on what the sandbox denies.
