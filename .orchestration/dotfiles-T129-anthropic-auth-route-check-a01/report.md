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
- One question, no other amendment. Question 1 (PONG 11:08Z): the R2 regex as first written refused four lines that item 2 passes. Amendment 1 answered it by stating R2 as its intent and making item 2's test lines the specification. Question 2 (the JSON key form) was not taken into the amendment; the Bot raised it as P1 4302702584 and revise round 3 (D-389-round3) brought it in (below).

## What changed in `scripts/validate-agent-assets.py`

Validation §4 holds the diff of the first head 53d9b608, §9.2 the fix round's, §10.2 revise round 2's and §11.2 revise round 3's; together 36 added lines, nothing deleted.

- **`validate_anthropic_auth_route()`**, called from `main` right after `validate_no_obvious_secrets()`. It reads the files `git ls-files -z -- home install` lists, as UTF-8 with undecodable bytes replaced, line by line. Each refusal is `fail(...)` with `<file>:<line>: R1:` or `<file>:<line>: R2:`.
  - **R1:** the line contains `ANTHROPIC_OAUTH_TOKEN`, anywhere on it.
  - **R2** (since revise round 2, the operator's re-plan D-389-replan): `ANTHROPIC_API_KEY_LITERAL` refuses an assignment of `ANTHROPIC_API_KEY` (a `=`, a `:` or, since revise round 3, Bash's `+=` after the name, which is bare or, since round 3, in matching quotes as a JSON, YAML or TOML key) unless its whole value, up to the end of the line or a `#` comment after whitespace, is one of these, each optionally quoted with a matching quote: one `$NAME`/`${NAME}` reference, one `{{ … }}` template whose body holds no `}}`, or empty (`=`, `=""`, `=''`). Anything else is a literal Bash could assign: `$'…'`, `$"…"`, `$(…)`, `${NAME:-…}`, a reference with more after it, or a `#` glued to the value. The grammar sits inside one negative lookahead after the `=`/`:`, so no optional piece can match empty in front of a value and let it through. Validation §11.3's table has the branch regex right on all 25 lines in scope; the first regex of the task is wrong on 14 of them.
- **Security properties** (each with a mutant that fails a test, validation §5, §10.3 and §11.3):
  - The message names the file, the line number and the rule, never the line, so a real key never reaches a CI log.
  - A failed `git ls-files` fails the run instead of passing on an empty list.
  - A tracked symlink is not followed, because on a PR checkout it could point at a device and hang the run. None is tracked under `home/` or `install/` today (validation §2).
- `SECRET_PATTERN`, the placeholders and `validate_no_obvious_secrets` are byte-identical (the diff only adds lines).

## Test

`test_anthropic_auth_route_refuses_an_oauth_token_in_applied_files_and_a_literal_api_key_assignment`, beside the secret-scan tests, and since revise round 2 its two checks, `test_anthropic_auth_route_r2_accepts_only_a_whole_value_reference_template_or_empty` and `test_anthropic_auth_route_reads_a_comment_after_an_empty_value_as_empty`. Revise round 3 adds `test_anthropic_auth_route_r2_reaches_a_quoted_key_and_a_compound_assignment`. The four share `anthropic_route_fixture()`: the module's temporary `ROOT`, made a git repository with three tracked files, and the function called directly, as the secret-scan tests do. The names are split (`"ANTHROPIC_API_" + "KEY"`) so the module passes the committed-secret scan.

- **Refused**, with `ERROR: <file>:2: <rule>:` on stderr and the line absent from it:
  - R1: `export ANTHROPIC_OAUTH_TOKEN=x` under `home/`, and the same line under `install/`.
  - R2: the quoted literal `ANTHROPIC_<redacted:secret-pattern>` (the case item 2 shows redacted), `ANTHROPIC_API_KEY: literal`, and `ANTHROPIC_API_KEY=literal` under `install/`; since the fix round also `ANTHROPIC_API_KEY=$'literal-value'`, `ANTHROPIC_API_KEY=$"literal-value"` and `ANTHROPIC_API_KEY=$(cat key-file)`.
- **Passed:** `ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY`, `apiKey: ANTHROPIC_API_KEY`, `env: ANTHROPIC_API_KEY`, `ANTHROPIC_API_KEY=`, `ANTHROPIC_API_KEY=""`, the quoted reference `ANTHROPIC_<redacted:secret-pattern>` (the pass case item 2 shows redacted), `ANTHROPIC_API_KEY= $ANTHROPIC_API_KEY`, `ANTHROPIC_API_KEY: {{ .anthropic }}`, and the OAuth line under `scripts/`.
- **Also covered:** a tracked symlink under `home/` that points at an OAuth line passes, and a mocked failed `git ls-files` refuses.
- **Round 2, the whole value:** refused are `${DEPLOYED_KEY:-literal-value}`, `${DEPLOYED_KEY}literal-value` and `$DEPLOYED_KEY$'literal-value'` (the three of P1 4302531070), `$DEPLOYED_KEY#literal-value`, `{{ .anthropic }}literal-value{{ .x }}` and a mismatched `"$DEPLOYED_KEY'`. Passed are `$DEPLOYED_KEY`, `${DEPLOYED_KEY}`, `"$DEPLOYED_KEY"`, `'${DEPLOYED_KEY}'`, `: "{{ .anthropic }}"` and `$DEPLOYED_KEY  # from the environment`.
- **Round 2, a comment after an empty value:** `= # supplied externally`, `: # populated at runtime` and `"" # empty on purpose` pass (P2 4302488376); `=#literal-value` is refused.
- **Round 3, the key side:** refused are `"ANTHROPIC_API_KEY": "literal-value"`, `"ANTHROPIC_API_KEY": literal-value`, `'ANTHROPIC_API_KEY' = 'literal-value'` (P1 4302702584) and `ANTHROPIC_API_KEY+=literal-value` (P2 4302702588). Passed are the quoted key with `"${ANTHROPIC_API_KEY}"` and with `"{{ .anthropic }}"`, `'ANTHROPIC_API_KEY' = '${ANTHROPIC_API_KEY}'`, and `ANTHROPIC_API_KEY+=$ANTHROPIC_API_KEY`.
- Item 2's two redacted lines are inferred from `SECRET_PATTERN`, which masks any quoted `api_key` assignment: a quoted literal (refused) and a quoted reference (passed).

Results (validation §5, §6):

- On origin/main's validator every subtest errors, because the function does not exist.
- With the first regex the four lines of §3 fail.
- Five mutants (R1 removed, R2 removed, symlinks followed, a failed listing passes, the message quotes the line) each fail at least one subtest (§5). After the fix round the same five and `any $ exempts`, the regex before the round, each fail too (§9.3).
- After revise round 3, ten variants each fail a test (§11.3): a13645d8's regex, the key unquoted, no `+=`, a template body holding `}}`, a `#` without whitespace, an unpaired value quote, R1 removed, R2 removed, symlinks followed, and a failed listing that passes.
- The module runs 101 tests, OK (after revise round 3, §11.4; 100 after round 2, 98 before it). `ruff format --check` passes. `ruff check` reports the same eight findings as on origin/main's copies of the two files, all in untouched lines; the new code adds none.
- `uv run --offline --with pyyaml scripts/validate-agent-assets.py` exits 0 on the branch with the rule live (validation §7, again after the fix round, §9.4, after revise round 2, §10.4, and after revise round 3, §11.4). Premise 1 holds: no applied file names either variable.

## Out of scope

- The JSON key form `"ANTHROPIC_API_KEY": "<literal>"`, the name in double quotes before the colon (a Claude `env` block), is not reached by R2 (validation §3, the two `n/a` lines). It was question 2, and amendment 1 changed nothing else. A follow-up could widen R2 to an optional closing quote after the name, with one more pass case for the quoted reference.
- check-tools.sh, omp's configuration and any workflow are untouched, as the task says.
- A reference followed by a JSON `,` or `}` is not a whole value, so `"ANTHROPIC_API_KEY": "${ANTHROPIC_API_KEY}",` is refused (validation §11.3, the `n/a` row). This is a false positive on a legitimate JSON reference, left outside round 3's key-side change, and there is no fourth round. A follow-up could let an optional `,` or `}` close the value.

## The Bot's review of 53d9b608 and the fix round

Review 5557555178 (2026-10-17T11:24:20Z) left two inline threads on `scripts/validate-agent-assets.py:1577`:

- **4302488371, P1** (the dollar-reference exemption): `fixed:6e4669b03d455e5325d580f98a025640b766dc99`. The exemption is now `\$\{?[A-Za-z_]`, the `$NAME` and `${NAME}` forms amendment 1 names, so `$'…'` and `$"…"` (literal data in Bash) and `$(…)` are refused. The three refusal cases failed on 53d9b608 (validation §9.1) and pass after the fix (§9.3). This is the one worker-side fix round; `@codex review` follows the push.
- **4302488376, P2** (a comment after an empty value): `fixed:4880c1ea15402f916fd35efe31e306e605296478` by the same grammar in revise round 2 (below). The worker had proposed it as a C-50 round.

## The re-review of 6a00d518 and revise round 2

Re-review 5557603153 (2026-10-17T11:41:18Z) left one inline thread on `scripts/validate-agent-assets.py:1579`:

- **4302531070, P1** (the exemption checked only a reference prefix, so `${NAME:-literal}`, `${NAME}literal` and `$NAME$'literal'` passed). It survived the worker-side fix round (`bot_rounds=2`), so the PR stopped for the operator. The operator's directive (D-389-replan, ACCEPTANCE `revise` of 12:35:23Z) re-plans R2 as the whole-value allowlist above. `fixed:4880c1ea15402f916fd35efe31e306e605296478`. Both checks of the round failed on 6a00d518 (validation §10.1: six and three subtests) and pass at 4880c1ea (§10.3). `revise.yaml` records previous_head 6a00d518 and the two checks.
- The class `dollar-reference-exemption` now has two rows (4302488371 and 4302531070). The re-plan replaced the prefix lookahead with a whole-value grammar instead of a third patch (C-59).

## The review of a13645d8 and revise round 3

Review 5557820069 (2026-10-17T12:46:36Z) left two inline threads on `scripts/validate-agent-assets.py:1579`:

- **4302702584, P1** (a quoted key is not reached by R2): `fixed:f5921767d4239e6e41ad41615cc078d9805eebf0`. The operator's directive (D-389-round3, ACCEPTANCE `revise` of 12:57:29Z) authorized one grammar change on the key side: the name may sit in matching quotes. The check failed on a13645d8 (validation §11.1: four subtests) and passes at f5921767 (§11.3).
- **4302702588, P2** (Bash's `+=`): `fixed:f5921767d4239e6e41ad41615cc078d9805eebf0` in the same change. `+=` joins `=` and `:`.
- `revise.yaml` records round 3 (previous_head a13645d8, the check, D-389-round3) with rounds 2 and 1 under `earlier:`. No fourth round.

## Caps and evidence

- Caps (`git diff --numstat origin/main...HEAD`; validation §8 for the first head, §11.4 at f5921767): 36 changed lines outside `tests/` and `.orchestration/` (<= 200); 132 added under `tests/` (<= 1000).
- `task_copy=6722f83d7327378040bd35b0a7c8d72dbfd7e1d5c93c99a437a1473fab0aa07f`.
- This report and the validation are in the PR's first commit (53d9b608), updated for the fix round in 6a00d518, for revise round 2 in a13645d8, and for revise round 3 in the evidence commit after f5921767. CI and the Bot's review of the final head come after the commit, so the RESULT names them.
- The worker replies to and resolves no thread, and does not merge. No new durable decision was made, so no CompactionDB memory was added; the learning candidates are in learning.md, not promoted. AutoSkill was not used. The Understand-Anything graph was not touched.

cost: n/a
