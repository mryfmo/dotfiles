---
reviewed_at: 2026-10-10T22:54:26Z
reviewer: claude-review-dot-a001
profile: review
session: 2089b04f-f9c7-498b-86c5-76f2140048d5
design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md@07b621d1fe2f0a5616b39b87807df0d08b06243cd6060cdc680f894d2b353eeb
task: dotfiles-T128-task-review-v1-v2-a01
round: 11
previous: .orchestration/validation/dotfiles-T128-task-review-v1-v2-a01-round9.md
supersedes_round: 10 (folded in)
files:
  - dotfiles-T128-v0-main-tests-a01@55e052c248cf6ee1b48477f770178863f9bb79eed8edeb522571a19ae340f7f0
  - dotfiles-T128-v1-task-schema-a01@134bd790aa7b3fc00921031db6d12db555d87b586fb6789705938c252069d94c
  - dotfiles-T128-v1b-pr-caps-a01@474a0b1e122f548f4259b8eac86237cbfbccbd747801784cf17cd18cf0b29194
  - dotfiles-T128-v1c-regime-ci-check-a01@65599bca743b6c9c8d286e19a215078887779d37ab8e3eceea55d416ab33289a
  - dotfiles-T128-v2-audit-schema-and-runner-a01@9e25391f7e4faa2d5844ef8bcb4079c88114ef41c4de4641a738b41abb809884
verdicts:
  dotfiles-T128-v0-main-tests-a01: "revise: R11-1 root resolution, R11-2 module selection, R11-3 contract lifecycle and task.md parsing"
  dotfiles-T128-v1-task-schema-a01: ready
  dotfiles-T128-v1b-pr-caps-a01: ready
  dotfiles-T128-v1c-regime-ci-check-a01: ready
  dotfiles-T128-v2-audit-schema-and-runner-a01: ready
---

# Task-file review round 11: V0 in full, the four others as a diff

PyYAML check: each file's invariant equals design v11 byte for byte; all five pointers name the round-11 receipt; the hashes match the TASK.

## V0 (dotfiles-T128-v0-main-tests-a01): revise

1. Scope and sentence: INV-12 only, verbatim, map [INV-12]; the first wave by the Order line. V0 ships script and test together, which the design states.
2. allowed_files: test.yaml, scripts/main-tests.sh, tests/unit/regime_contract.py, tests/unit/test_main_tests.py, the SKILL; complete for the job, the script, the decorator and the prose. Caps: five files, well under the lines. Touch points: the changes job's outputs are unchanged; the rule-file word budget is not touched; test.yaml is PR-editable until V1c lands, a bootstrap window to note in the acceptance record.
3. Premises: premise 2 holds (git archive origin/main tests/unit | tar -t lists tests/unit/test_agent_session_staleness.py first); premise 1 is unverifiable from this seat (its gh api call needs GitHub; the sed half holds). Missing premise, and it is the bug: every test module resolves the repository root from its own path (34 of 34 modules in tests/unit carry ROOT = Path(__file__).resolve().parents[2]; none takes it from the cwd), so main's modules extracted into <tmp> look for scripts under <tmp>, not in the PR tree, and item 1's "with the PR's working tree as the project root" does not happen.
   R11-1: copy the PR tree to <tmp> (or git worktree add --detach <tmp> HEAD), remove <tmp>/tests/unit, extract main's tests/unit into <tmp>, and run unittest discover -s <tmp>/tests/unit -t <tmp>; add the premise with the grep count.
4. Routing: Claude seat; test.yaml, a script, tests and SKILL are no Claude-boundary source.
5. Ponytail and questions: R11-2: item 1 maps a script to tests/unit/test_<stem>.py; home/dot_local/bin/common/executable_herdr-agents and executable_permgate map to test_executable_*.py, which do not exist (the modules are test_herdr_agents.py and test_permgate.py), and a script with no module under the rule runs nothing in mode (a), so an undeclared change to it passes. Drop the stem rule: mode (b) runs main's copy of the test modules the task.md's allowed_files list under tests/unit/ with REGIME_CONTRACT=1; mode (a) runs every other main module as it is. No mapping, nothing slips. R11-3: item 1 reads allowed_files from the task.md in the range; say the YAML is read with uv run --no-project --with pyyaml python -c (INV-1 forbids a hand-written parser and V1's validator is not on main yet); item 4 should say the implementation PR removes the @contract decorator from the tests it satisfies, so they become ordinary tests on merge (the design-side clause of the round-11 receipt).
6. Contradictions: none with INV-12 v11 beyond the two clauses the design receipt names; the job shape (needs: changes, always reports, fetch-depth 0) matches the design.

## V1, V1b, V1c, V2: ready

- V1 and V1c: INV-1 v11 verbatim; V1c line 53 names the Actions event policy action.
- V1b: INV-2 v11 verbatim with the -contract-a01 mapping (line 15).
- V2: INV-5 v11 verbatim; item 1 (line 52) says the runner computes the inputs object after the run and overwrites whatever the model wrote; the premises map is in the schema; the .claude/ refusal is in item 2 (line 53). The round-9 note on the test fixture (.claude/ outside skills) stands.

All five will move with v12's INV-12 edit and pointers.
