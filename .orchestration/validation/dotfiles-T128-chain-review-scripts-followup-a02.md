---
task_id: dotfiles-T128-chain-review-scripts-followup-a02
seat: claude-standard-dot-a003
commit: fbc1d4ac
---

# Validation: dotfiles-T128-chain-review-scripts-followup-a02

## 1. Task copy, premises, owned rows, tests, linters and size

The task copy hashes to the TASK line's `task_sha256`, the main checkout's file. The copy on `origin/main` (`1d418126`) hashes to `d76a00f9…`, the pair-confirmed text before the task's two pre-dispatch Change sections. Both premises replay with the task's outputs (2 and 1). The owned rows `audit:2e3ff49:1` and `local:2e3ff49:1`, class `env-s-quoting`, stand under `## Owned by dotfiles-T128-chain-review-scripts-followup-a02` in the a01 record, and the audit row also under its audit heading (line 103).

```text
$ shasum -a 256 .orchestration/dotfiles-T128-chain-review-scripts-followup-a02/task.md
2cc46db329450914878fa51b471bb7a2f6db3dde486593b8d79d8ce7302bcf15  .orchestration/dotfiles-T128-chain-review-scripts-followup-a02/task.md
$ git log --oneline -1; git merge-base HEAD origin/main
fbc1d4ac fix(orchestrator): local-review.sh refuses an env -S shebang it cannot split as e
1d418126
$ the two premises (origin/main)
2
1
$ the owned rows (origin/main, the a01 record)
103:audit:2e3ff49:1	env-s-quoting
145:## Owned by dotfiles-T128-chain-review-scripts-followup-a02 (advisory P2 of the final head; plan 020 step 1.2; rows id<TAB>class)
155:local:2e3ff49:1	env-s-quoting
156:audit:2e3ff49:1	env-s-quoting

$ GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=commit.gpgsign GIT_CONFIG_VALUE_0=false UV_OFFLINE=1 uv run --no-project python -m unittest tests/unit/test_chain_review_scripts.py -v
(rc=0)
test_local_advisory_matches_the_owner_heading_literally ... ok
test_local_advisory_records_p2_rows_and_stops_on_p0_p1 ... ok
test_local_advisory_refuses_a_malformed_owner_id ... ok
test_local_review_and_local_advisory_refuse_a_task_or_head_that_leaves_their_directory ... ok
test_local_review_keeps_env_S_shebang_arguments ... ok
test_local_review_pins_the_review_binary_interpreter ... ok
test_local_review_refuses_a_quoted_env_S_shebang ... ok
test_local_review_resolves_codex_through_mise_and_refuses_a_shim ... ok
test_local_review_resolves_the_review_binary_before_the_checkout ... ok
test_local_review_reuses_only_a_file_that_records_this_head ... ok
test_local_review_runs_the_review_binary_read_only_at_the_head_and_writes_one_file ... ok
test_local_review_strips_a_worktree_path_holding_sed_syntax_literally ... ok
test_local_review_writes_no_file_when_the_review_binary_fails ... ok
test_sandbox_scan_prints_the_unsandboxed_mutation_calls ... ok
Ran 14 tests in 9.485s
OK

$ shellcheck scripts/orchestrator/local-review.sh; shfmt --indent 4 --space-redirects -d scripts/orchestrator/local-review.sh
(rc=0)
$ ruff check tests/unit/test_chain_review_scripts.py; ruff format --check tests/unit/test_chain_review_scripts.py
All checks passed!
1 file already formatted
(rc=0)

$ git diff --numstat origin/main...HEAD -- . ':!.orchestration'
13	5	scripts/orchestrator/local-review.sh
28	0	tests/unit/test_chain_review_scripts.py
files: 2; changed lines outside tests/ and .orchestration/: 18; added under tests/: 28
```

## 2. Mutation proofs

Each mutant of `scripts/orchestrator/local-review.sh` runs against `test_local_review_refuses_a_quoted_env_S_shebang`, and the file is restored after each (`a02-mutate.py`, a scratch script outside the repository). M2 to M5 drop one character from the refused class and M6 the comment-word check; each fails exactly the case it drops, because every case starts with no interpreter marker, no codex log, no review file and the review worktree at `main`.

```text
M1 the local-review.sh of origin/main -> killed; failing cases: "'x'", '${HOMEX}/lib', '--require "/opt/a b/x.js"', 'a\\ b', 'one # two'
M2 no double quote -> killed; failing cases: '--require "/opt/a b/x.js"'
M3 no single quote -> killed; failing cases: "'x'"
M4 no backslash -> killed; failing cases: 'a\\ b'
M5 no dollar sign -> killed; failing cases: '${HOMEX}/lib'
M6 no comment word -> killed; failing cases: 'one # two'
file restored (equal to the working copy before the run): True
```

## 3. PR #376: CI and the Bot on `b20a0141`, the final head (main-checkout copy only)

```text
$ gh pr checks 376; gh pr view 376 --json headRefOid,mergeStateStatus
CodeRabbit: pass
GitGuardian Security Checks: pass
private-bootstrap (macos-14, client): pass
private-bootstrap (ubuntu-24.04, client): pass
private-bootstrap (ubuntu-24.04, server): pass
public-bootstrap (macos-14, client): pass
public-bootstrap (ubuntu-24.04, client): pass
public-bootstrap (ubuntu-24.04, server): pass
test (macos-14, client): pass
test (ubuntu-24.04, client): pass
test (ubuntu-24.04, server): pass
test (ubuntu-26.04, client): pass
validate: pass
{"headRefOid":"b20a0141d29c9080b1d40cf14ca7c580f08699d9","mergeStateStatus":"CLEAN"}
```

```text
$ the code_review and security_review states of the Bot's summary; gh api …/pulls/376/reviews; …/pulls/376/comments; …/issues/376/reactions
"code_review":{"commit_sha":"b20a0141d29c9080b1d40cf14ca7c580f08699d9","has_any_findings":false,"has_unresolved_findings":false,"status":"completed"}
"security_review":{"commit_sha":"b20a0141d29c9080b1d40cf14ca7c580f08699d9","has_any_findings":false,"has_unresolved_findings":false,"status":"completed"}
chatgpt-codex-connector[bot] +1
```

Both of the Bot's reviews completed on `b20a0141` with no finding: no review comment, no thread, a 👍 reaction, so no fix round.
