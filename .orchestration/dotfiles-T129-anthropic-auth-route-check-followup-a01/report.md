---
task_id: dotfiles-T129-anthropic-auth-route-check-followup-a01
seat: claude-standard-dot-a007
branch: tools/anthropic-auth-route-structured
base: 862ab31c11edc0ba0c8830a19946d8b04dd01955 (PR #389's head; the branch rebases onto origin/main after #389 merges)
task_sha256: 52db410226c5361d3a8400ffe429acf7def38bb9973006a20126ee97324eee1d
---

# Report: dotfiles-T129-anthropic-auth-route-check-followup-a01

- Seat: `claude-standard-dot-a007` in `.claude/worktrees/worker-c`. origin/main has no `validate_anthropic_auth_route` until PR #389 merges, so the branch `tools/anthropic-auth-route-structured` starts from #389's head 862ab31c (amendment 1's base statement). The draft PR is stacked on #389's branch (amendment 2). After #389 merges, the branch rebases onto origin/main and the PR is retargeted to main before CI, the Bot wait and the RESULT.
- Task file: the amended text, sha256 `52db4102…` (amendment 2; amendment 1 `4f00b00c…`, first dispatch `14424640…`), copied byte-identical; the task-consistency check passes on it (validation §1). One question (Q1, PONG 13:53:53Z, answered by amendment 1).
- The owned rows, read from the lineage's acceptance record at dispatch: the re-plan item 0 (4302758230, class escaped-name), 4302758234 (single-quoted-reference) and 4302758239 (json-delimiter-after-value).

## What changed in `scripts/validate-agent-assets.py`

Validation §3 holds the diff against 862ab31c (125 added, 15 deleted).

- **The format decides the reading** (amendment 1). `applied_file_format()` strips chezmoi's attribute prefixes from the basename.
  - A `modify_`, `run_`, `symlink_` or `encrypted_` source holds a script, a link target or ciphertext, so it is text, as is every `.tmpl` source and every other suffix.
  - A remaining `.json`, `.toml`, `.yaml` or `.yml` source is parsed. Of this repository's 35 such sources, 27 parse and the 8 `modify_` scripts are text (validation §2).
- **Parsed formats.**
  - Parsers: `json.loads` with a pairs hook (`JsonPairs`), so a duplicate key cannot hide behind the last one; `tomllib`, which already refuses duplicates; and the YAML node graph from `yaml.compose_all`, which keeps duplicate pairs and decodes quoted escapes.
  - A parse failure is a refusal that names the file and the error type only, since a parser's message can quote the file.
  - The walk is iterative, and each container is visited once, so YAML aliases cannot multiply the work.
- **R2 on parsed data.** A decoded key that ends in `ANTHROPIC_API_KEY` (the names the line grammar covers) passes only with null or a string that is one `$NAME`/`${NAME}` reference, one `{{ }}` template, or empty. A number, a boolean, a mapping or a list is refused.
- **R1 and the line form of R2 on decoded text.** Every decoded key and string is read for R1 and for the line form of R2, line by line. That catches an env entry such as `"ANTHROPIC_API_KEY=literal"` and embedded shell.
- **Line checks per format.** The raw-line R1 still runs on every file, so a comment that names the token is refused. The raw-line R2 runs only on text: in a parsed file, quotes, escapes and delimiters are syntax.
- **Messages.** A parsed refusal names the file, the rule and the dotted key path, escaped with `unicode_escape`. A key is PR text, and a newline in it could forge a CI log line or a workflow command. A value is never printed.
- **Row 4302758234.** In text, a `$NAME`/`${NAME}` reference passes bare or double-quoted only. Bash expands nothing inside single quotes, so `'$NAME'` assigns the text `$NAME`, a broken credential. Templates keep their optional quotes; the row names references only.
- **Row 4302758239.** A JSON reference before a comma or a brace now passes, because the parser reads the value alone.
- `SECRET_PATTERN`, the placeholders and `validate_no_obvious_secrets` are unchanged. PyYAML is required when a YAML source is scanned, as `load_yaml` requires it.

## Tests (one per row; red on 862ab31c, validation §4)

- **The re-plan (4302758230):**
  - `test_anthropic_auth_route_reads_json_and_toml_through_their_parsers`. Refused by the parse and missed by the line grammar (the test asserts the grammar misses each one): a TOML basic-quoted key with `\u` escapes, a JSON key with `\u` escapes, a key nested in a JSON object over a line break, an env-list string with an escaped assignment, and a TOML key that decodes to the OAuth name (R1). Also refused: a JSON duplicate key whose first value is a literal, a numeric value, and a key holding a newline, which is printed escaped. Passed: a reference in TOML, a template in a nested TOML table, an empty JSON value beside `apiKeyEnv`, and a `modify_` script read as text. That script with a literal is refused at its line, and a JSON file that does not parse is refused.
  - `test_anthropic_auth_route_reads_yaml_through_its_parser` (skipped without PyYAML). Refused: a YAML double-quoted key with `\u` escapes, a nested mapping whose value continues on the next line, a top-level plain scalar on the next line, and a duplicate key whose first value is a literal. Passed: a reference, null, a quoted template, and aliases. A YAML file that does not parse is refused.
- **4302758234:** `test_anthropic_auth_route_refuses_a_single_quoted_reference_in_text`. `'$DEPLOYED_KEY'`, `'${DEPLOYED_KEY}'` and the quoted-key form `'ANTHROPIC_API_KEY' = '${ANTHROPIC_API_KEY}'` in a shell fixture are refused. A double-quoted reference, a bare reference and a single-quoted template pass, and the TOML literal-string form passes through the parser. The two lineage pass cases that held a single-quoted reference in a shell fixture, `'${DEPLOYED_KEY}'` in the round-2 test and the quoted-key form in the round-3 test, move to this test's refused side; that is the row's own change.
- **4302758239:** `test_anthropic_auth_route_reads_a_json_reference_before_a_delimiter`. `{"ANTHROPIC_API_KEY": "${ANTHROPIC_API_KEY}", "x": 1}` passes, and the test asserts the line grammar would have refused it.
- **Shared helper.** `anthropic_route_fixture()` takes extra tracked files and can write a fixture verbatim; between checks a JSON fixture holds `{}`, so it stays parseable.

## Results

- On 862ab31c's validator the four new tests fail 19 subtests (validation §4).
- Nine mutants each fail a test (validation §4): the pairs hook removed, raw R2 run on parsed files, a parse failure skipped, a single-quoted reference accepted, `modify_` sources parsed, decoded strings not read, decoded keys not compared, and key paths printed unescaped.
- The module runs 105 tests OK both without PyYAML (one skipped: the YAML test) and with it (none skipped) (validation §5).
- Ruff reports the same eight findings as on the base copies, all in untouched lines (validation §6).
- `make validate-agent-assets` exits 0 (validation §7).

## Limits

- **YAML and TOML comments.** A comment line that assigns a literal is not read by R2, because the parser drops comments and the raw-line R2 runs on text only. R1 still reads every raw line, and `SECRET_PATTERN` still catches an `sk-`-shaped key anywhere.
- **The YAML test in CI.** CI's unit-test job (`make unit-test`, `uv run python -m unittest discover`) has no PyYAML, so the YAML test is skipped there. The validator itself runs with PyYAML in the agent-assets workflow. The Makefile and the workflow are outside `allowed_files`; validation §5 pastes the run with PyYAML.

## Caps and what follows

- Against 862ab31c: 140 changed lines outside `tests/` and `.orchestration/` (<= 250, this task's cap); 122 added under `tests/` (<= 1000). The caps against origin/main are pasted after the rebase.
- `task_copy=52db410226c5361d3a8400ffe429acf7def38bb9973006a20126ee97324eee1d`.
- After #389 merges: rebase onto origin/main, re-run the Check there, retarget the PR to main, `gh pr ready`, CI and the Bot wait, then the RESULT. The worker replies to and resolves no thread, and does not merge.
- No new durable decision was made, so no CompactionDB memory was added; the learning candidates are in learning.md, not promoted. AutoSkill was not used. The Understand-Anything graph was not touched.

cost: n/a
