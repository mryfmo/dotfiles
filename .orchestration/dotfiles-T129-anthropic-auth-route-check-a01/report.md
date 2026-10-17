---
task_id: dotfiles-T129-anthropic-auth-route-check-a01
seat: claude-standard-dot-a007
branch: tools/anthropic-auth-route-check
base: 35ab0e95a7fe27c501db3478d4f37e69a514d532
task_sha256: 6722f83d7327378040bd35b0a7c8d72dbfd7e1d5c93c99a437a1473fab0aa07f
---

# Report: dotfiles-T129-anthropic-auth-route-check-a01

- Seat: `claude-standard-dot-a007` in `.claude/worktrees/worker-c`, on a fresh branch `tools/anthropic-auth-route-check` from `origin/main` `35ab0e95` (boundary (18), PR #385). The PR #375 and #386 branches stay in the worktree, committed and pushed, until their acceptance.
- Task file: the amended text, sha256 `6722f83d…` (amendment 1, 2026-10-17T11:11:16Z; first dispatch `5c00408f…`), copied byte-identical; the task-consistency check passes on it and the four premises replay `0`, `1 0`, `1` and `10` (validation §1, §2).
- One question, no other amendment. Question 1 (PONG 11:08Z): the R2 regex as first written refused four lines that item 2 passes. Amendment 1 answered it by stating R2 as its intent and making item 2's test lines the specification. Question 2 (the JSON key form) was not taken into the amendment, so it stays out of scope (below).

## What changed in `scripts/validate-agent-assets.py`

Validation §4 holds the diff of the first head 53d9b608 and §9.2 the fix round's; together 33 added lines, nothing deleted.

- **`validate_anthropic_auth_route()`**, called from `main` right after `validate_no_obvious_secrets()`. It reads the files `git ls-files -z -- home install` lists, as UTF-8 with undecodable bytes replaced, line by line. Each refusal is `fail(...)` with `<file>:<line>: R1:` or `<file>:<line>: R2:`.
  - **R1:** the line contains `ANTHROPIC_OAUTH_TOKEN`, anywhere on it.
  - **R2:** `ANTHROPIC_API_KEY_LITERAL`, the line assigns `ANTHROPIC_API_KEY` (a `=` or `:` after the name) a value that is not empty (`=`, `=""`, `=''`), not a `$NAME` or `${NAME}` reference (quoted or not; `$'…'`, `$"…"` and `$(…)` are refused since the fix round, the Bot's P1) and not a template expression (`{{ … }}`). The whitespace after the `=`/`:` and the optional quote sit inside the negative lookahead, so neither can match empty in front of a reference. That backtracking was the fault of the first regex (validation §3: on 12 lines in scope the first regex was wrong on four, the branch regex on none).
- **Security properties** (each with a mutant that fails the test, validation §5):
  - The message names the file, the line number and the rule, never the line, so a real key never reaches a CI log.
  - A failed `git ls-files` fails the run instead of passing on an empty list.
  - A tracked symlink is not followed, because on a PR checkout it could point at a device and hang the run. None is tracked under `home/` or `install/` today (validation §2).
- `SECRET_PATTERN`, the placeholders and `validate_no_obvious_secrets` are byte-identical (the diff only adds lines).

## Test

`test_anthropic_auth_route_refuses_an_oauth_token_in_applied_files_and_a_literal_api_key_assignment`, beside the secret-scan tests. The fixture tree is the module's temporary `ROOT`, made a git repository with three tracked files, and the function is called directly, as those tests do. The names are split (`"ANTHROPIC_API_" + "KEY"`) so the module passes the committed-secret scan.

- **Refused**, with `ERROR: <file>:2: <rule>:` on stderr and the line absent from it:
  - R1: `export ANTHROPIC_OAUTH_TOKEN=x` under `home/`, and the same line under `install/`.
  - R2: the quoted literal `ANTHROPIC_<redacted:secret-pattern>` (the case item 2 shows redacted), `ANTHROPIC_API_KEY: literal`, and `ANTHROPIC_API_KEY=literal` under `install/`; since the fix round also `ANTHROPIC_API_KEY=$'literal-value'`, `ANTHROPIC_API_KEY=$"literal-value"` and `ANTHROPIC_API_KEY=$(cat key-file)`.
- **Passed:** `ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY`, `apiKey: ANTHROPIC_API_KEY`, `env: ANTHROPIC_API_KEY`, `ANTHROPIC_API_KEY=`, `ANTHROPIC_API_KEY=""`, the quoted reference `ANTHROPIC_<redacted:secret-pattern>` (the pass case item 2 shows redacted), `ANTHROPIC_API_KEY= $ANTHROPIC_API_KEY`, `ANTHROPIC_API_KEY: {{ .anthropic }}`, and the OAuth line under `scripts/`.
- **Also covered:** a tracked symlink under `home/` that points at an OAuth line passes, and a mocked failed `git ls-files` refuses.
- Item 2's two redacted lines are inferred from `SECRET_PATTERN`, which masks any quoted `api_key` assignment: a quoted literal (refused) and a quoted reference (passed).

Results (validation §5, §6):

- On origin/main's validator every subtest errors, because the function does not exist.
- With the first regex the four lines of §3 fail.
- Five mutants (R1 removed, R2 removed, symlinks followed, a failed listing passes, the message quotes the line) each fail at least one subtest (§5). After the fix round the same five and `any $ exempts`, the regex before the round, each fail too (§9.3).
- The module runs 98 tests, OK. `ruff format --check` passes. `ruff check` reports the same eight findings as on origin/main's copies of the two files, all in untouched lines; the new code adds none.
- `uv run --offline --with pyyaml scripts/validate-agent-assets.py` exits 0 on the branch with the rule live (validation §7, and again after the fix round, §9.4). Premise 1 holds: no applied file names either variable.

## Out of scope, as left by amendment 1

- The JSON key form `"ANTHROPIC_API_KEY": "<literal>"`, the name in double quotes before the colon (a Claude `env` block), is not reached by R2 (validation §3, the two `n/a` lines). It was question 2, and amendment 1 changed nothing else. A follow-up could widen R2 to an optional closing quote after the name, with one more pass case for the quoted reference.
- check-tools.sh, omp's configuration and any workflow are untouched, as the task says.

## The Bot's review of 53d9b608 and the fix round

Review 5557555178 (2026-10-17T11:24:20Z) left two inline threads on `scripts/validate-agent-assets.py:1577`:

- **4302488371, P1** (the dollar-reference exemption): `fixed:6e4669b03d455e5325d580f98a025640b766dc99`. The exemption is now `\$\{?[A-Za-z_]`, the `$NAME` and `${NAME}` forms amendment 1 names, so `$'…'` and `$"…"` (literal data in Bash) and `$(…)` are refused. The three refusal cases failed on 53d9b608 (validation §9.1) and pass after the fix (§9.3). This is the one worker-side fix round; `@codex review` follows the push.
- **4302488376, P2** (a comment after an empty value): the worker proposes a C-50 revise round, since it is small and within `allowed_files`. The empty-value branch would read a `#` comment after whitespace as empty (`(?:\s+#.*)?` before the end), while `ANTHROPIC_API_KEY=#x` stays refused, because in a shell word a `#` without whitespace before it is data. Proposed check: `tests/unit/test_validate_agent_assets.py::test_anthropic_auth_route_reads_a_comment_after_an_empty_value_as_empty`. Otherwise it is advisory, owned by `dotfiles-T129-anthropic-auth-route-check-followup-a01`.

## Caps and evidence

- Caps (`git diff --numstat origin/main...HEAD`; validation §8 for the first head, the round adds 3 and 4): 33 changed lines outside `tests/` and `.orchestration/` (<= 200); 63 added under `tests/` (<= 1000).
- `task_copy=6722f83d7327378040bd35b0a7c8d72dbfd7e1d5c93c99a437a1473fab0aa07f`.
- This report and the validation are in the PR's first commit (53d9b608), and, updated for the fix round, in the evidence commit after 6e4669b0. CI and the Bot's re-review of the final head come after the commit, so the RESULT names them.
- The worker replies to and resolves no thread, and does not merge. No new durable decision was made, so no CompactionDB memory was added; the learning candidates are in learning.md, not promoted. AutoSkill was not used. The Understand-Anything graph was not touched.

cost: n/a
