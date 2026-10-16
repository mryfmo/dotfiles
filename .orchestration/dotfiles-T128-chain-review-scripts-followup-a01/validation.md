---
task_id: dotfiles-T128-chain-review-scripts-followup-a01
seat: claude-standard-dot-a003
commit: 5880df9b
---

# Validation: dotfiles-T128-chain-review-scripts-followup-a01

## 1. Task copy, premises and base

```text
$ shasum -a 256 .orchestration/dotfiles-T128-chain-review-scripts-followup-a01/task.md
1d11eb079db07273df9862870ab819a1e112c7b844cb553165394b8c786f6ebb  .orchestration/dotfiles-T128-chain-review-scripts-followup-a01/task.md
(rc=0)
$ git show origin/main:.orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a01.md | shasum -a 256
0b10249e58b59d53c26da4468a264970cce7c41934c59bd9727899157147a3a7  -
(rc=0)
$ cmp "$(git rev-parse --path-format=absolute --git-common-dir)/../.orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a01.md" .orchestration/dotfiles-T128-chain-review-scripts-followup-a01/task.md && echo identical-to-the-dispatched-file
identical-to-the-dispatched-file
(rc=0)
$ git cat-file -e origin/main:.orchestration/tasks/dotfiles-T128-chain-review-scripts-a01.md && echo present || echo absent
present
(rc=0)
$ git show origin/main:.orchestration/acceptance/dotfiles-T128-chain-review-scripts-a01.md 2>/dev/null | /usr/bin/grep -q '^## Owned by dotfiles-T128-chain-review-scripts-followup-a01' && echo present || echo absent
present
(rc=0)
$ git merge-base HEAD origin/main | cut -c1-8; git rev-parse --short origin/main
f0faa33a
59599783
(rc=0)
```

- **The task copy** is byte-identical to the dispatched file, whose sha256 `1d11eb07…` is the TASK's `task_sha256`.
- **`origin/main`'s copy hashes to `0b10249e…`,** the pair-confirmed text the TASK note names. The dispatched file is that text plus amendment 1: decision A's P1 as the first row, and the shared resolver in the environment row. The orchestrator's record for this task names it, with the `1d11eb07…` hash, and sent it for a second review round before dispatch.
- **Both premises replay** as `present`.
- **The base** is `f0faa33a`.

## 2. The owned rows

The section `## Owned by dotfiles-T128-chain-review-scripts-followup-a01` runs from line 138 to the next heading at line 152:

```text
$ git show origin/main:.orchestration/acceptance/dotfiles-T128-chain-review-scripts-a01.md | shasum -a 256
f727e05848a1dd1bc86d6a04d70749dab89465795c84fd439610125c2453cf23  -
(rc=0)
$ git show origin/main:.orchestration/acceptance/dotfiles-T128-chain-review-scripts-a01.md | /usr/bin/grep -n '^## '
138:## Owned by dotfiles-T128-chain-review-scripts-followup-a01 (advisory findings of the final head; plan 020 step 1.2; rows id<TAB>class)
152:## Dispatch (bus lines)
(rc=0)
$ git show origin/main:.orchestration/acceptance/dotfiles-T128-chain-review-scripts-a01.md | sed -n '138,151p' | awk -F'\t' 'NF == 2 && $1 !~ / / {n++; print n": "$0} END {print "rows=" n}'
1: 4270918132	stale-review-file-on-error
2: 4270918140	reuse-keyed-by-sha7
3: local:b6ce4ff:1	stale-review-file-on-error
4: local:b6ce4ff:2	reuse-keyed-by-sha7
5: audit:b6ce4ff:1	review-binary-shim
6: audit:b6ce4ff:2	task-arg-traversal
7: audit:b6ce4ff:3	sed-path-interpolation
8: audit:b6ce4ff:4	test-order-unproven
rows=8
(rc=0)
```

## 3. What each row names

The local review and the audit of `b6ce4ff`. A row id `<source>:b6ce4ff:<n>` names the n-th finding of that file; the audit's findings 5 to 7 are not owned rows:

```text
$ git show origin/main:.orchestration/validation/dotfiles-T128-chain-review-scripts-a01-local-review-b6ce4ff.md | sed -n '/^findings:/,/^```/p' | /usr/bin/grep -E '^- \[P'
- [P1] Fail closed when the review process exits nonzero — scripts/orchestrator/local-review.sh:61-61
- [P2] Verify the full commit before reusing a cached review — scripts/orchestrator/local-review.sh:27-28
(rc=0)
$ git show origin/main:.orchestration/validation/dotfiles-T128-chain-review-scripts-a01-audit-b6ce4ff.md.last.md | /usr/bin/grep -nE '^- \[P[0-3]\]' | cut -c1-260
3:- [P1] high specification .orchestration/dotfiles-T128-chain-review-scripts-a01/task.md:38 `command -v` does not guarantee that the actual reviewer is selected before checkout: this host resolves `codex` to a mise shim, which selects its executable and envir
5:- [P2] high implementation scripts/orchestrator/local-review.sh:27 The unchecked task argument escapes the promised output directory: `task=../escape` writes `.orchestration/escape-local-review-<sha7>.md`; additional `../` components escape the repository. `
7:- [P2] high implementation scripts/orchestrator/local-review.sh:62 `W` is interpolated directly into a sed program. A valid worktree path containing `[1]` fails literal prefix removal; `#` and newline characters can inject additional sed commands, including 
9:- [P2] high evidence tests/unit/test_chain_review_scripts.py:114 The decoy case proves resolution happens in the repository root, but does not prove it precedes checkout. Moving the resolution block below checkout while retaining the root cwd leaves every as
11:- [P2] high orchestration .orchestration/validation/dotfiles-T128-chain-review-scripts-a01-pr-feedback.json:116 This disposition and the one at line 129 acknowledge valid defects and defer them to a follow-up task, without fixing or refuting them. Naming an
13:- [P2] high evidence .orchestration/dotfiles-T128-chain-review-scripts-a01/sandbox.md:21 The record claims to list every unsandboxed call, but acceptance line 54 explicitly acknowledges omitted final-head `gh` reads and says they were left unrecorded to pre
15:- [P3] high evidence .orchestration/dotfiles-T128-chain-review-scripts-a01/report.md:5 The reported full base SHA is invalid: `git show` returns `bad object`. Validation line 28 and Git history identify the actual original base as `5ec860520075a2f0bbb551232
(rc=0)
```

The two Bot threads of PR #357 (gated call 1):

```text
$ for id in 4270918132 4270918140; do gh api "repos/mryfmo/dotfiles/pulls/comments/${id}" --jq '"--- \(.id) \(.user.login) \(.path):\(.original_line // .line) commit \(.original_commit_id[0:8])\n\(.body)"'; done
--- 4270918132 chatgpt-codex-connector[bot] scripts/orchestrator/local-review.sh:61 commit 0da6be3e
**<sub><sub>![P2 Badge](https://img.shields.io/badge/P2-yellow?style=flat)</sub></sub>  Reject failed review runs instead of caching them**

When Codex exits nonzero because of authentication, configuration, or runtime failure before producing findings, this handler discards that status and writes a `findings: 0` validation file; subsequent invocations then reuse it as a successful review. The new test explicitly accepts exit 0 for a status-5 reviewer, so the local-review threat-table row does not fail closed. Preserve the reviewer failure status and do not cache the transcript as a completed review.

AGENTS.md reference: [AGENTS.md:L78-L78](https://github.com/mryfmo/dotfiles/blob/0da6be3e10964ff744262e835806fa8081e93ed7/AGENTS.md#L78-L78)

Useful? React with 👍 / 👎.
--- 4270918140 chatgpt-codex-connector[bot] scripts/orchestrator/local-review.sh:28 commit 0da6be3e
**<sub><sub>![P2 Badge](https://img.shields.io/badge/P2-yellow?style=flat)</sub></sub>  Validate the full head before reusing a cached review**

When two heads for the same task share their first seven hexadecimal characters, this branch reuses the earlier file without comparing its recorded full `head:` value to the requested commit; the newer head is therefore never reviewed. The closed test only repeats the identical head and does not establish the promised one-review-per-PR-head behavior. Key the file by the full hash or verify the stored full hash before reuse.

AGENTS.md reference: [AGENTS.md:L78-L78](https://github.com/mryfmo/dotfiles/blob/0da6be3e10964ff744262e835806fa8081e93ed7/AGENTS.md#L78-L78)

Useful? React with 👍 / 👎.
(rc=0)
```

## 4. Tests and linters

```text
$ UV_OFFLINE=1 uv run --no-project python -m unittest -v tests.unit.test_chain_review_scripts 2>&1 | /usr/bin/grep -E ' \.\.\. |^Ran |^OK|FAILED' | sed 's/ (tests.unit[^)]*)//'
test_local_advisory_records_p2_rows_and_stops_on_p0_p1 ... ok
test_local_review_and_local_advisory_refuse_a_task_or_head_that_leaves_their_directory ... ok
test_local_review_resolves_codex_through_mise_and_refuses_a_shim ... ok
test_local_review_resolves_the_review_binary_before_the_checkout ... ok
test_local_review_reuses_only_a_file_that_records_this_head ... ok
test_local_review_runs_the_review_binary_read_only_at_the_head_and_writes_one_file ... ok
test_local_review_strips_a_worktree_path_holding_sed_syntax_literally ... ok
test_local_review_writes_no_file_when_the_review_binary_fails ... ok
test_sandbox_scan_prints_the_unsandboxed_mutation_calls ... ok
Ran 9 tests in 7.041s
OK
(rc=0)
$ UV_OFFLINE=1 uv run --no-project python -m unittest tests.unit.test_chain_github_scripts tests.unit.test_orchestrator_tools tests.unit.test_orch_gate_path 2>&1 | tail -3
Ran 54 tests in 42.139s

OK
(rc=0)
```

```text
$ w="${PWD}"; cd "${TMPDIR}" && shellcheck "${w}"/scripts/orchestrator/{local-review,local-advisory}.sh && "$(command -v shfmt)" --indent 4 --space-redirects -d "${w}"/scripts/orchestrator/{local-review,local-advisory}.sh
(rc=0)
$ uv run --no-project ruff check tests/unit/test_chain_review_scripts.py; uv run --no-project ruff format --check tests/unit/test_chain_review_scripts.py
All checks passed!
1 file already formatted
(rc=0)
```

## 5. Mutation proofs

Each mutant is applied to the working file, the named test runs, and the file is restored byte for byte. C10 and C11 are `origin/main`'s scripts:

```text
C1 scripts/orchestrator/local-review.sh -> test_local_review_writes_no_file_when_the_review_binary_fails: killed (FAILED (failures=1))
C2 scripts/orchestrator/local-review.sh -> test_local_review_reuses_only_a_file_that_records_this_head: killed (FAILED (failures=1))
C3 scripts/orchestrator/local-review.sh -> test_local_review_resolves_codex_through_mise_and_refuses_a_shim: killed (FAILED (failures=1))
C4 scripts/orchestrator/local-review.sh -> test_local_review_resolves_codex_through_mise_and_refuses_a_shim: killed (FAILED (failures=1))
C5 scripts/orchestrator/local-review.sh -> test_local_review_resolves_codex_through_mise_and_refuses_a_shim: killed (FAILED (failures=1))
C6 scripts/orchestrator/local-review.sh -> test_local_review_resolves_the_review_binary_before_the_checkout: killed (FAILED (failures=1))
C7 scripts/orchestrator/local-review.sh -> test_local_review_and_local_advisory_refuse_a_task_or_head_that_leaves_their_directory: killed (FAILED (failures=5))
C8 scripts/orchestrator/local-advisory.sh -> test_local_review_and_local_advisory_refuse_a_task_or_head_that_leaves_their_directory: killed (FAILED (failures=2))
C9 scripts/orchestrator/local-review.sh -> test_local_review_strips_a_worktree_path_holding_sed_syntax_literally: killed (FAILED (failures=1))
C10 scripts/orchestrator/local-review.sh -> test_local_review_writes_no_file_when_the_review_binary_fails: killed (FAILED (failures=1))
C11 scripts/orchestrator/local-advisory.sh -> test_local_review_and_local_advisory_refuse_a_task_or_head_that_leaves_their_directory: killed (FAILED (failures=2))
mutants 11/11 killed; tree restored
```

## 6. Size

```text
$ git diff --numstat origin/main...HEAD -- . ':!.orchestration'
7	2	scripts/orchestrator/local-advisory.sh
50	16	scripts/orchestrator/local-review.sh
113	6	tests/unit/test_chain_review_scripts.py
(rc=0)
$ git diff --numstat origin/main...HEAD -- . ':!.orchestration' | awk '$3 !~ /^tests\// {c += $1 + $2; f++} $3 ~ /^tests\// {t += $1; f++} END {print "files: " f "; changed lines outside tests/ and .orchestration/: " c "; added under tests/: " t}'
files: 3; changed lines outside tests/ and .orchestration/: 75; added under tests/: 113
(rc=0)
```

3 files outside `.orchestration/`, 75 changed lines outside `tests/` and `.orchestration/` (cap 200), 113 added under `tests/` (cap 1000).

## 7. The repository validator

```text
$ UV_OFFLINE=1 uv run --no-project --with pyyaml scripts/validate-agent-assets.py 2>&1 | tail -1  # on 5880df9b, before the commit
agent asset validation ok
(rc=0)
```

## 8. Revise round 2 (`35f76e7d`): the review binary's interpreter

The ACCEPTANCE `status=revise` of 05:32:04Z (previous head `c45f9b53`, the orchestrator's update-branch merge) carries the audit's P1 on `c45f9b5` at local-review.sh:86. The binary `mise which` answers can be a launcher whose first line is an env shebang, so its interpreter was still found on PATH at exec time, with the PR worktree as cwd. `revise.yaml` records the previous head and the check.

```text
$ UV_OFFLINE=1 uv run --no-project python -m unittest -v tests.unit.test_chain_review_scripts
test_local_advisory_records_p2_rows_and_stops_on_p0_p1 ... ok
test_local_review_and_local_advisory_refuse_a_task_or_head_that_leaves_their_directory ... ok
test_local_review_pins_the_review_binary_interpreter ... ok
test_local_review_resolves_codex_through_mise_and_refuses_a_shim ... ok
test_local_review_resolves_the_review_binary_before_the_checkout ... ok
test_local_review_reuses_only_a_file_that_records_this_head ... ok
test_local_review_runs_the_review_binary_read_only_at_the_head_and_writes_one_file ... ok
test_local_review_strips_a_worktree_path_holding_sed_syntax_literally ... ok
test_local_review_writes_no_file_when_the_review_binary_fails ... ok
test_sandbox_scan_prints_the_unsandboxed_mutation_calls ... ok
Ran 10 tests in 7.475s
OK
(rc=0)
$ UV_OFFLINE=1 uv run --no-project python -m unittest tests.unit.test_chain_github_scripts tests.unit.test_orchestrator_tools tests.unit.test_orch_gate_path
Ran 54 tests in 39.890s

OK
(rc=0)
$ shellcheck scripts/orchestrator/local-review.sh; shfmt --indent 4 --space-redirects -d scripts/orchestrator/local-review.sh
(rc=0)
$ ruff check tests/unit/test_chain_review_scripts.py; ruff format --check tests/unit/test_chain_review_scripts.py
All checks passed!
1 file already formatted
(rc=0)
$ git diff --numstat origin/main...HEAD -- . ':!.orchestration'
7	2	scripts/orchestrator/local-advisory.sh
67	19	scripts/orchestrator/local-review.sh
145	6	tests/unit/test_chain_review_scripts.py
files: 3; changed lines outside tests/ and .orchestration/: 95; added under tests/: 145
```

The check `test_local_review_pins_the_review_binary_interpreter` has two cases. In the first, the stub binary's first line is `#!/usr/bin/env -S interp --flag`, and the interpreter the mise stub answers runs with argv `<binary> --profile review -s read-only review --base main`. In the second, mise answers a shims path for the interpreter: the run exits 2, the review worktree stays at `main`, and no file is written. The two earlier tests whose mise stub answered every name now answer only `codex`, so their stub binaries' `#!/usr/bin/env bash` falls back to `command -v bash`; the shim test's mise log gains the `which bash` call.

Mutants of the round, against that test:

```text
R1 no interpreter step: killed (FAILED (failures=1, errors=1))
R2 interpreter resolved after the checkout: killed (FAILED (failures=1))
R3 no env -S: killed (FAILED (failures=1, errors=1))
mutants 3/3 killed; file restored: True
```

## 9. Revise round 3 (`afd36bb8`): the env -S arguments

The ACCEPTANCE `status=revise` of 06:12:13Z (previous head `850fc54e`) carries the local review's P2 at local-review.sh:91-92: the shebang branch kept only the first word after `env -S`. The rest of the line is now split into words, and the run is the interpreter, those words, the binary, then the review arguments. A plain `env NAME` shebang is unchanged.

```text
$ UV_OFFLINE=1 uv run --no-project python -m unittest -v tests.unit.test_chain_review_scripts
test_local_advisory_records_p2_rows_and_stops_on_p0_p1 ... ok
test_local_review_and_local_advisory_refuse_a_task_or_head_that_leaves_their_directory ... ok
test_local_review_keeps_env_S_shebang_arguments ... ok
test_local_review_pins_the_review_binary_interpreter ... ok
test_local_review_resolves_codex_through_mise_and_refuses_a_shim ... ok
test_local_review_resolves_the_review_binary_before_the_checkout ... ok
test_local_review_reuses_only_a_file_that_records_this_head ... ok
test_local_review_runs_the_review_binary_read_only_at_the_head_and_writes_one_file ... ok
test_local_review_strips_a_worktree_path_holding_sed_syntax_literally ... ok
test_local_review_writes_no_file_when_the_review_binary_fails ... ok
test_sandbox_scan_prints_the_unsandboxed_mutation_calls ... ok
Ran 11 tests in 7.691s
OK
(rc=0)
$ UV_OFFLINE=1 uv run --no-project python -m unittest tests.unit.test_chain_github_scripts tests.unit.test_orchestrator_tools tests.unit.test_orch_gate_path
Ran 54 tests in 36.306s

OK
(rc=0)
$ shellcheck scripts/orchestrator/local-review.sh; shfmt --indent 4 --space-redirects -d scripts/orchestrator/local-review.sh
(rc=0)
$ ruff check tests/unit/test_chain_review_scripts.py; ruff format --check tests/unit/test_chain_review_scripts.py
All checks passed!
1 file already formatted
(rc=0)
$ git diff --numstat origin/main...HEAD -- . ':!.orchestration'
7	2	scripts/orchestrator/local-advisory.sh
72	19	scripts/orchestrator/local-review.sh
170	6	tests/unit/test_chain_review_scripts.py
files: 3; changed lines outside tests/ and .orchestration/: 100; added under tests/: 170
```

The check `test_local_review_keeps_env_S_shebang_arguments` uses a stub binary whose first line is `#!/usr/bin/env -S fakeinterp --flag x`. The stub interpreter records `<its path> --flag x <binary> --profile review -s read-only review --base main`. The round-2 test's `-S interp --flag` stub now receives `--flag`, as env -S passes it, and its expectation says so.

```text
T1 the -S words dropped (round 2's behaviour) -> test_local_review_keeps_env_S_shebang_arguments: killed (FAILED (failures=1)); file restored: True
```

## 10. Revise round 5 (`df92b402`): the owner task id

The local review's P1 on `b879aac6`, the update-branch head of `2f4ce7e9`: `local-advisory.sh` left the owner task id (argument 3) unvalidated, used it as a grep regex and wrote it verbatim into the record. The owner now takes the task id's form (exit 2 otherwise), and its heading is matched as a literal string ended by a space or the line's end. The check `test_local_advisory_refuses_a_malformed_owner_id` refuses six malformed owners with nothing written. `test_local_advisory_matches_the_owner_heading_literally` keeps the near-match headings `t-followupXa01` and `t.followup-a01b` from counting as `t.followup-a01`, and adds that heading once over two runs.

```text
$ git log --oneline -1; git merge-base --is-ancestor b879aac6 HEAD
df92b402 fix(orchestrator): local-advisory.sh validates the owner task id and ma
b879aac6 is an ancestor
$ python -m unittest -v tests/unit/test_chain_review_scripts.py
(rc=0)
test_local_advisory_matches_the_owner_heading_literally ... ok
test_local_advisory_refuses_a_malformed_owner_id ... ok
Ran 13 tests in 7.761s
OK
$ shellcheck scripts/orchestrator/local-advisory.sh; shfmt --indent 4 --space-redirects -d scripts/orchestrator/local-advisory.sh
(rc=0)
$ ruff check tests/unit/test_chain_review_scripts.py; ruff format --check tests/unit/test_chain_review_scripts.py
All checks passed!
1 file already formatted
(rc=0)
$ mutation proofs (the script swapped, the two new tests run, the file restored)
M1 the script of b879aac6 ->  1 FAIL: test_local_advisory_matches_the_owner_heading_literally; 6 FAIL: test_local_advisory_refuses_a_malformed_owner_id;
M2 no owner check ->  6 FAIL: test_local_advisory_refuses_a_malformed_owner_id;
M3 a prefix heading match ->  1 FAIL: test_local_advisory_matches_the_owner_heading_literally;
file restored: True
$ git diff --numstat origin/main...HEAD -- . ':!.orchestration'
12	4	scripts/orchestrator/local-advisory.sh
72	19	scripts/orchestrator/local-review.sh
191	6	tests/unit/test_chain_review_scripts.py
files: 3; changed lines outside tests/ and .orchestration/: 107; added under tests/: 191
```
