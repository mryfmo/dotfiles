---
task_id: dotfiles-T128-chain-github-scripts-a01
seat: claude-standard-dot-a003
commit: 3931db66
---

# Validation: dotfiles-T128-chain-github-scripts-a01

## 1. Task copy, inputs, premise and base

```text
$ shasum -a 256 <main checkout>/.orchestration/tasks/dotfiles-T128-chain-github-scripts-a01.md .orchestration/dotfiles-T128-chain-github-scripts-a01/task.md
fe39cbc8b6efeb8ef345542789df90ccbe29db9e28cf6006078d4d6bb8dd4d6c  <main checkout>/.orchestration/tasks/dotfiles-T128-chain-github-scripts-a01.md
fe39cbc8b6efeb8ef345542789df90ccbe29db9e28cf6006078d4d6bb8dd4d6c  .orchestration/dotfiles-T128-chain-github-scripts-a01/task.md
$ shasum -a 256 <input dir>/*.sh | cut -c1-16
235d84b15ede9cb8
118108254c8f8adb
$ git ls-tree --name-only origin/main scripts/orchestrator/ | /usr/bin/grep -c -E "resolve-threads|pr-cost" || true
0
$ git log --oneline origin/main..HEAD && git merge-base origin/main HEAD && git log --oneline -1 5ec86052
3931db66 feat(orchestrator): resolve-threads.sh and pr-cost.sh land with their tests (plan 021 step 6.3)
5ec860520075a2f0bbb551232de0f868e481a59c
5ec86052 fix(orchestrator): orch-gate.sh runs the gate with a private PATH of resolved gh and git (T128 gate-wrapper-path a01) (#355)
```

- **The task copy.** It hashes to the TASK's `task_sha256`, `fe39cbc8…`, byte-identical. It holds no home path, so the validator accepts it unmasked (§7).
- **The inputs.** Their sha256 prefixes match the task's intro: `235d84b15ede9cb8` for pr-cost.sh and `118108254c8f8adb` for resolve-threads.sh.
- **The premise replays.** Neither script name exists under `scripts/orchestrator/` on `origin/main`.
- **The base.** The branch starts from `5ec86052`, the merge of PR #355.

## 2. Every `--jq` expression is the input's

The canned answers in the test are keyed on the API path and the `--jq` expression, so the expressions stay byte for byte. `count` passes its expression to `--jq`, so its argument is compared as one:

```text
$ for s in resolve-threads.sh pr-cost.sh; do grep -o -- "--jq '[^']*'" <input dir>/$s | sort -u > in; grep -o -- "--jq '[^']*'\|count \"[^\"]*\" '[^']*'" scripts/orchestrator/$s | sed -E "s/^count \"[^\"]*\" /--jq /" | sort -u > out; echo "$s: input $(wc -l < in | tr -d ' ') expressions, differing lines $(comm -3 in out | wc -l | tr -d ' ')"; done
resolve-threads.sh: input 3 expressions, differing lines 0
pr-cost.sh: input 4 expressions, differing lines 0
```

## 3. Tests and linters

The tests ran with `UV_OFFLINE=1 uv run --no-project` from the uv cache, because the sandbox has no pypi. CI runs `make unit-test` online. The module imports only the standard library, so it needs no PyYAML.

```text
$ UV_OFFLINE=1 uv run --no-project python -m unittest tests/unit/test_chain_github_scripts.py -v
test_pr_cost_appends_one_ledger_line_from_the_api (tests.unit.test_chain_github_scripts.ChainGithubScriptsTest.test_pr_cost_appends_one_ledger_line_from_the_api) ... ok
test_resolve_threads_replies_with_the_table_row_and_resolves_only_threads_with_rows (tests.unit.test_chain_github_scripts.ChainGithubScriptsTest.test_resolve_threads_replies_with_the_table_row_and_resolves_only_threads_with_rows) ... ok

----------------------------------------------------------------------
Ran 2 tests in 1.589s

OK
rc=0
```

```text
$ shellcheck scripts/orchestrator/resolve-threads.sh scripts/orchestrator/pr-cost.sh; echo "shellcheck rc=$?"
shellcheck rc=0
$ for s in resolve-threads.sh pr-cost.sh; do f="$PWD/scripts/orchestrator/$s"; (cd "$TMPDIR" && shfmt --indent 4 --space-redirects -d "$f"); echo "shfmt $s rc=$?"; done
shfmt resolve-threads.sh rc=0
shfmt pr-cost.sh rc=0
$ ruff format --config ruff.toml --check tests/unit/test_chain_github_scripts.py && ruff check --config ruff.toml tests/unit/test_chain_github_scripts.py
1 file already formatted
All checks passed!
```

## 4. Mutation proofs (`scratchpad/mutate-chain.py`)

The method:

- edit one span of a script at `3931db66`, or replace the script with the chain's input;
- run that script's test by its dotted name;
- count a kill only when the run fails on an `AssertionError`;
- restore the file with `git checkout --`.

The mutants of resolve-threads.sh:

- **R1** is the chain's input as it is.
- **R2** has the loop read the threads on stdin.
- **R3** drops the sweep lookup.
- **R4** lets `--dry-run` write.
- **R5** exits 0 on a missing row.
- **R6** has the mutation name the comment id.
- **R7** changes the `fixed:` sentence.

The mutants of pr-cost.sh:

- **P1** is the chain's input as it is.
- **P2** drops the per-page sum.
- **P3** writes the header on every run.
- **P4** gives the wall hours without one decimal.
- **P5** drops `open` for an unmerged PR.
- **P6** counts a local review of another PR.

```text
$ uv run --no-project python scratchpad/mutate-chain.py <worktree> <input dir>
KILLED R1 the chain's input resolve-threads.sh as it is :: AssertionError: 3 != 0 : 
KILLED R2 the loop reads the threads on stdin :: AssertionError: 3 != 0 : 
KILLED R3 no sweep lookup :: AssertionError: 0 != 3 : 
KILLED R4 --dry-run writes :: AssertionError: Lists differ: [['api', 'graphql']] != [['api', 'graphql'], ['api', '-X'], ['api', 'graphql'], ['ap[25 chars]ql']]
KILLED R5 a missing row exits 0 :: AssertionError: 3 != 0 : 
KILLED R6 the mutation names the comment id :: AssertionError: Lists differ: ['T_one'] != ['101']
KILLED R7 another fixed: sentence :: AssertionError: Lists differ: [['ap[154 chars]ixed at root cause in that commit on this bran[82 chars]id']] != [['ap[154 chars]ixed in that commit on 
KILLED P1 the chain's input pr-cost.sh as it is :: AssertionError: Lists differ: ['9',[33 chars]', '2026-10-14T03:00:00Z', '3.0', '4', '2', '1', '0', '1', '1'] != ['9',[33 chars]', '2026-10-14T03:00:00
KILLED P2 no per-page sum :: AssertionError: Lists differ: ['9',[33 chars]', '2026-10-14T03:00:00Z', '3.0', '4', '2', '1', '0', '1', '1'] != ['9',[33 chars]', '2026-10-14T03:00:00
KILLED P3 the header on every run :: AssertionError: 3 != 2
KILLED P4 wall hours without one decimal :: AssertionError: Lists differ: ['9',[33 chars]', '2026-10-14T03:00:00Z', '3.0', '4', '2', '1', '0', '1', '1'] != ['9',[33 chars]', '2026-10-14T03:00:00
KILLED P5 no open for an unmerged PR :: AssertionError: Lists differ: ['9', 'tools/x', '2026-10-14T00:00:00Z', 'open'] != ['9', 'tools/x', '2026-10-14T00:00:00Z', '']
KILLED P6 a local review of another PR counts :: AssertionError: Lists differ: ['9',[33 chars]', '2026-10-14T03:00:00Z', '3.0', '4', '2', '1', '0', '1', '1'] != ['9',[33 chars]', '2026-10-14T03:00:00
kills 13/13
scripts clean
```

- **The result: 13/13 killed.** `scripts clean` means `git checkout --` restored both scripts after each mutant.
- **R1 and R2: the input's loop.** Its gh calls inherit the loop's stdin, and the stub reads stdin as the task's stub must. In the first case the reply for thread 101 therefore swallowed thread 202's line. The run reported `missing rows: 0` and exited 0, but thread 202 has no disposition, so it should have exited 3. Reading the threads on fd 3 closes that. The test's own check, that no logged call read anything on stdin, catches it too.
- **P1 and P2: the input's counts.** With `--paginate`, gh applies `--jq` to each page. Two pages of reviews printed two counts into one field, and the line broke. pr-cost.sh sums the per-page counts.

That gh prints one `--jq` result per page is gh's documented behaviour ("Each page is a separate JSON array or object", `gh api --help`). Two live calls on PR #350, outside the sandbox (sandbox record, calls 1 and 2), show it. The first uses the default page size; the second forces pages of two:

```text
$ gh api repos/mryfmo/dotfiles/pulls/350/comments --paginate --jq 'length'
6
rc=0
$ gh api 'repos/mryfmo/dotfiles/pulls/350/comments?per_page=2' --paginate --jq 'length'
2
2
2
rc=0
```

## 5. Wall hours: jq and awk against the input's Python

pr-cost.sh computes the wall hours with `jq` (`fromdate`) and `awk` (`%.1f`), where the input ran a `uv run --no-project python` one-liner. The two agree on whole hours, ties at .x5, zero and long spans:

```text
$ bash scratchpad/wall-probe.sh; jq --version
2026-10-14T03:00:00Z python=3.0 jq+awk=3.0 same
2026-10-14T00:15:00Z python=0.2 jq+awk=0.2 same
2026-10-14T00:03:00Z python=0.1 jq+awk=0.1 same
2026-10-14T01:09:00Z python=1.1 jq+awk=1.1 same
2026-10-14T02:27:00Z python=2.5 jq+awk=2.5 same
2026-10-15T02:03:00Z python=26.1 jq+awk=26.1 same
2026-10-14T00:00:00Z python=0.0 jq+awk=0.0 same
2026-11-02T13:45:00Z python=469.8 jq+awk=469.8 same
jq-1.8.2
```

The test pins the whole-hour form `3.0` (a bare `3` would fail it). It also pins the one-decimal shape for an open PR. resolve-threads.sh's sweep lookup moved from a `uv run --no-project python` one-liner to one `jq` call. The R3 mutant and the second resolve case cover it.

## 6. Caps

```text
$ git diff --numstat origin/main...HEAD
54	0	scripts/orchestrator/pr-cost.sh
70	0	scripts/orchestrator/resolve-threads.sh
193	0	tests/unit/test_chain_github_scripts.py
$ git diff --numstat origin/main...HEAD | awk '$3 !~ /^\.orchestration\// {f++; if ($3 ~ /^tests\//) {ta+=$1} else {c+=$1+$2}} END {print "files", f, "changed_non_test", c, "added_test", ta}'
files 3 changed_non_test 124 added_test 193
```

Step 7.2 and INV-2 hold:

- **Outside `tests/` and `.orchestration/`:** 124 changed lines (124 added, 0 deleted) of 200.
- **Under `tests/`:** 193 added lines of 1000.
- **Files:** 3 outside `.orchestration`.

## 7. The repository validator

The WARN lines are not pasted: they are this host's regime-boundary notes, and they print the main checkout's path.

```text
$ UV_OFFLINE=1 uv run --no-project --with pyyaml scripts/validate-agent-assets.py > "$TMPDIR/v.out" 2>&1; echo "rc=$?"; grep -v "^WARN: " "$TMPDIR/v.out"; grep -c "^WARN: .*chain-github-scripts-a01" "$TMPDIR/v.out"
rc=0
agent asset validation ok
13
```
