---
format: 2
task_id: dotfiles-T129-normalised-comparison-lint-followup-a04
kind: code
security: false
design_review:
  receipt: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round22.md
  design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md
allowed_files:
  - scripts/lint-comparisons.py
  - scripts/lint-comparisons-baseline.tsv
  - tests/unit/test_lint_comparisons.py
  - .orchestration/dotfiles-T129-normalised-comparison-lint-followup-a04/**
after: []
reset_of: [dotfiles-T129-normalised-comparison-lint-followup-a02]
threat_table:
  - control: scripts/lint-comparisons.py
    disposition: "residual: statement-local static analysis cannot determine runtime-generated shell words or jq programs; AST-derived syntax, the stated jq grammar and the named fixtures bound this implementation."
  - control: scripts/lint-comparisons-baseline.tsv
    disposition: "closed: tests/unit/test_lint_comparisons.py::LintComparisonsTest::test_a_baseline_row_matching_no_hit_fails_as_stale"
  - control: tests/unit/test_lint_comparisons.py
    disposition: "residual: finite regression fixtures establish the named cases, not complete Bash or jq semantics; red evidence, mutation output and the final-head audit check their reach."
  - control: .orchestration/dotfiles-T129-normalised-comparison-lint-followup-a04/**
    disposition: "residual: task.md and evidence are process records, not reviewer authentication; compare this task copy byte-for-byte with dispatch and record its SHA256; .orchestration/dotfiles-T129-normalised-comparison-lint-followup-a02/task.md is inherited read-only history."
  - control: "shfmt's JSON AST is the only shell reader; a parse failure refuses the file with its shfmt message"
    disposition: "closed: tests/unit/test_lint_comparisons.py::LintComparisonsTest::test_shfmt_parse_failure_refuses_with_original_message"
  - control: task metadata
    disposition: "residual: metadata declares scope but cannot authenticate its author; the orchestrator checks the dispatched task digest and task consistency."
  - control: metadata separators
    disposition: "residual: front-matter parsing alone does not bind the body; the task-copy comparison covers the complete dispatched bytes."
  - control: in-process effects
    disposition: "residual: Python and shfmt execute inside the sandbox; repository shell and jq inputs are parsed as data and never executed."
  - control: workflow and interpreter or environment inputs
    disposition: "residual: the observed shfmt is v3.14.1, but unit-job PATH provisioning is not guaranteed by the workflow; missing shfmt must refuse rather than select another reader."
  - control: new or renamed scripts
    disposition: "residual: no new or renamed production script is permitted; the RESULT inventory and final diff expose additions beyond the three named implementation files."
  - control: orchestrator effect merge
    disposition: "residual: none in this worker assignment; the worker never merges, approves or pushes main; eventual integration belongs to Orchestrator Playbook step 10."
  - control: orchestrator effect update-branch
    disposition: "residual: none assigned to the worker; an orchestrator head update invalidates head-bound evidence and requires the applicable checks again."
  - control: orchestrator effect forced worker removal
    disposition: "residual: none planned or authorized by this task; worker teardown remains an orchestrator operation."
  - control: the task-file copy on the branch (.orchestration/dotfiles-T129-normalised-comparison-lint-followup-a04/task.md)
    disposition: "residual: byte-identical to the dispatched file (its sha256 is in the TASK line); the orchestrator compares at acceptance and the regime job compares it with the text on main"
premises:
  - claim: The read-only authoring probe observes shfmt 3.14.1.
    command: |-
      shfmt --version
    output: |-
      v3.14.1
  - claim: CI pins its mise execution to shfmt 3.14.1; the host mise declaration actually says latest, so it is not a literal host version pin.
    command: |-
      rg -n 'shfmt' home/dot_mise/config.toml .github/workflows/test.yaml
    output: |-
      home/dot_mise/config.toml:22:shfmt = "latest"
      .github/workflows/test.yaml:308:      - name: Run `shfmt`
      .github/workflows/test.yaml:311:          # shfmt is version-pinned via mise: brew/apt ship divergent versions
      .github/workflows/test.yaml:313:          git ls-files -- ':(glob)install/**/*.sh' ':(glob)scripts/**/*.sh' | xargs mise x shfmt@3.14.1 -- shfmt -i 4 -sr -d
  - claim: The matrix job installs mise without automatic tools and runs shfmt through a scoped mise execution; its later unit-test step has no explicit shfmt PATH installation.
    command: |-
      rg -n 'Setup mise|install: false|mise .*install |mise x shfmt|Run Python unit tests|make unit-test' .github/workflows/test.yaml
    output: |-
      223:      - name: Setup mise for statusline smoke
      229:          install: false
      236:          mise -C "${RUNNER_TEMP}/statusline-mise" install node
      238:          mise -C "${RUNNER_TEMP}/statusline-mise" install npm:ccstatusline npm:ccusage
      239:          mise -C "${RUNNER_TEMP}/statusline-mise" install ruff npm:prettier
      313:          git ls-files -- ':(glob)install/**/*.sh' ':(glob)scripts/**/*.sh' | xargs mise x shfmt@3.14.1 -- shfmt -i 4 -sr -d
      339:      - name: Run Python unit tests
      349:          make unit-test
  - claim: "At e520a7fe, Bot 4313892754 concerns lines 47-49 and 125-129; Bot 4313892766 concerns 178-184; Bot 4313892783 concerns 88-100. Audit findings 1-7 respectively concern 73-75, 125-129, 125-129, 98-100, 178-180, 88-94 and 98-100."
    command: |-
      git show e520a7fe:scripts/lint-comparisons.py | sed -n '47,49p;73,75p;88,100p;125,129p;178,184p'
    output: |2-
          r"""(?:\\[\s\S]|"\$(?:[^"\\]|\\[\s\S])*"|"(?!(?:[^"\\\n]|\\[\s\S])*")(?=[^\n]*\S)|[^'"\\\n;&|])*+"""
          r"""('[^']*'|"(?:[^"\\]|\\[\s\S])*")"""
      )  # the first quoted word after the jq word, before a separator, that is no "$expansion" and no stray closing quote
      def expands(word):  # the shell expands a variable in this word: a $name outside '…' and after no backslash
          pieces = re.findall(r"""'[^']*'|"(?:[^"\\]|\\.)*"|\\.|[^'"\\]+""", word)
          return any(re.search(r"\$\{?[A-Za-z_]", re.sub(r"\\.", "", p)) for p in pieces if p[0] not in "'\\")
                  if c == "\\" and q != "'":
                      i += 2
                      continue
                  if q:
                      q = "" if c == q else q
                  elif c in "'\"":
                      q = c
                  elif c == "#" and (i == 0 or line[i - 1] in " \t;|&("):
                      out[n] = line[i:]
                      break
                  elif (doc := re.match(r"<<(-?)[ \t]*(['\"]?)([A-Za-z_]\w*)\2", line[i:])) and line[i - 1 : i] != "<":
                      docs.append((doc[3], bool(doc[1])))
                      i += len(doc[0])
              if q:  # the program's text, a double-quoted one as the shell hands it to jq
                  begin, close = m.end() + q.start(1) + 1, m.end() + q.end(1)
                  inner = code[begin : close - 1]  # the original text: the folding above only located it
                  # unescaped as the shell does; a backslash-newline becomes a newline, so the line numbers hold
                  yield begin, re.sub(r'\\([\\"$`\n])', r"\1", inner) if q[1][0] == '"' else inner, close
          lines, buf, at, note = text.split("\n"), "", 0, comments(text)
          for n, raw in enumerate(lines, 1):
              code, at = raw[: len(raw) - len(note.get(n, ""))], at if buf else n
              # a continuation (an odd run of trailing backslashes): the statement goes on, reported at its first line
              if (len(code) - len(code.rstrip("\\"))) % 2:
                  buf += code[:-1]  # the shell deletes a backslash-newline: the lines join with no separator
                  continue
  - claim: The current authoring checkout baseline contains 87 nonblank rows.
    command: |-
      rg -c '\S' scripts/lint-comparisons-baseline.tsv
    output: |-
      87
  - claim: The continuation anchor baseline contains 88 nonblank rows; this differs from the authoring checkout and must not be silently substituted.
    command: |-
      git show e520a7fe:scripts/lint-comparisons-baseline.tsv | rg -c '\S'
    output: |-
      88
---

# AGMSG-TASK dotfiles-T129-normalised-comparison-lint-followup-a04 — replace the shell hand-parser

## Goal

[memory:decision] Reset a02 with a design change: shell syntax comes exclusively from shfmt's mvdan/sh JSON AST, and R3 examines the shell-concatenated jq program through the bounded jq scanner below.

Assign to one Claude standard worker, a008 or a009, in its existing worktree. Repository root: `$HOME/Workspace/dotfiles`. Continue PR #432's branch `tools/lint-comparisons-followup-a02` from the implementation anchor `e520a7fe4dd5f84acb46927927999998c188eb51`; open no second PR or implementation branch. Preserve existing descendants, including base-update commits, and record the actual starting head before editing; unexpected implementation drift requires a blocked PONG rather than a rewind.

## Why this reset exists

Read `.orchestration/tasks/dotfiles-T129-normalised-comparison-lint-followup-a02.md`, `.orchestration/acceptance/dotfiles-T129-normalised-comparison-lint-followup-a02.md` and `.orchestration/validation/dotfiles-T129-normalised-comparison-lint-followup-a02-audit-b24d313.md.last.md` before editing. The acceptance record's final `re-plan: hand-parser` line is the design decision this task implements.

[memory:failure] a02 already replaced physical-line matching with a hand-planned tokenizer, then fixed Bot threads 4313892754, 4313892766 and 4313892783 in f6fd955e; the next audit still found seven defects in the same parser family. Another quote-state or heredoc regex patch is not this reset.

The audit also found the cap sentence omitted `.orchestration/`, counted 1,976 changed lines against 350, and established that pre-push correction 5b6c5a8a plus f6fd955e spent a02's two fix rounds under C-61. Preserve that history; do not describe a04 as a02's third correction round or reuse the completed predecessor a03 as the owner of new findings.

## Design

`.orchestration/plans/024-design-quality.md` section 5.14 applies by reference under D-024-30; these sentences identify the items relied on without restating their contracts.

- Item 0 supplies the threat model and its residuals.
- Item 1 governs the Claude seat's write boundary.
- Item 2 governs executable launches and read-only probes.
- Item 4 governs the identity of consumed task text and evidence.
- Item 6 governs residual claims.
- Item 9 governs the trusted interpreter and private execution cache.
- Item 10 governs every worker command, including commands for which older playbook text described exceptions.

Read every caller of the replaced shell helpers before editing. Replace the shared shell-reading path once; remove its shlex fallback, quote-state scanner, continuation joiner, heredoc regex and regex-based jq-program locator. Python remains on its existing `ast` and `tokenize` paths.

Invoke the selected shfmt executable as a subprocess with `-ln bash --tojson`, passing the file contents as data. Walk its AST for command words and word parts, quoting, parameter expansions, arithmetic, redirections, comments, `case`, `[[ ... ]]`, and the argument structures of `[` and `test`. Heredoc bodies are excluded from shell-rule and marker scanning; all parser-valid delimiter forms, including numeric, punctuation, escaped and mixed-quoted delimiters, follow the AST.

R1 reads comparison operands structurally and retains the existing path-name and literal criteria. R2, shell R5 and shell R6 use the same AST reader. R5 expansion detection includes positional and special parameters, including `$1`, `${10}`, `$@`, `$?`, `$$` and `$!`; quoted literal or escaped dollar signs do not become expansions. Arithmetic shifts never become heredocs.

A shell allow marker counts only in an AST comment node associated with the relevant statement; retain continued-statement and trailing-program comment coverage. Python markers require Python comment tokens, and jq markers require jq comment tokens. Text inside ordinary strings or heredoc data cannot supply a marker or a reasonless-marker R0. Use AST source positions for physical line numbers; retain a source-position mapping when decoding and concatenating jq word parts.

Locate a jq command's program argument through AST arguments, respecting option operands, redirections and command boundaries. Preserve the inherited fixtures for jq command spellings and option values. Concatenate every literal quoted or unquoted fragment of that one shell word in order, with shell quote removal and escape semantics; backslash-newline disappears where Bash removes it and remains literal where Bash preserves it. Do not execute substitutions or invent runtime expansion values; retain statically readable fragments and report runtime-generated program text as a limit.

The jq scanner's grammar is whitespace, line comments beginning with `#` outside strings, double-quoted string literals with backslash escapes, `.identifier` field paths including `.path` and `.url`, `$identifier` variables, identifiers, `==` and `!=`, and balanced punctuation for grouping, calls and pipelines; jq string interpolation re-enters code with balanced parentheses. Strings and comments cannot supply operators or normaliser applications. Boolean and conditional separators bound individual comparisons, while grouping keeps an `if ... end` expression together. Preserve the existing R3 string-comparison functions and require an actual defined normaliser application on each relevant operand side. Apply R3 to the complete concatenated program, rather than separately to its fragments.

Keep the CLI, rule IDs, Python behavior, baseline TSV format, content hashes, duplicate-row accounting and changed-versus-unchanged severity. Remove obsolete baseline rows and account for newly exposed genuine hits individually; do not baseline parser failures or broaden exemptions.

Missing shfmt causes a nonzero refusal containing `shfmt missing`. A shfmt parse failure refuses the file with its original shfmt diagnostic; invalid JSON also refuses. Neither case falls back to regex scanning or becomes a successful `--all` run.

## Regression fixtures

Each row below names an executable C11 selector. Add the seven audit regressions and strengthen the three existing Bot tests with the indicated still-failing variants. Expected results include rule IDs, physical line numbers and accepted controls.

| Finding | Required behavior | Selector |
| --- | --- | --- |
| audit:b24d313:1 | `pgrep -f "$1"` and special-parameter variants produce R5; literal dollar patterns do not. | `tests/unit/test_lint_comparisons.py::LintComparisonsTest::test_process_patterns_include_positional_and_special_parameters` |
| audit:b24d313:2 | Splitting either `==` or `.path` across a double-quoted backslash-newline still produces R3. | `tests/unit/test_lint_comparisons.py::LintComparisonsTest::test_double_quoted_jq_joins_split_operator_and_path` |
| audit:b24d313:3 | `jq -r 'select(''.url == $p)'` produces R3 after word-part concatenation. | `tests/unit/test_lint_comparisons.py::LintComparisonsTest::test_jq_program_concatenates_all_word_parts` |
| audit:b24d313:4 | `$((1 << shift))` preserves subsequent real comments, including R0 and valid allow comments. | `tests/unit/test_lint_comparisons.py::LintComparisonsTest::test_arithmetic_shift_keeps_following_marker_comments` |
| audit:b24d313:5 | Heredoc data containing `[[ $path == /x ]]` produces no shell-rule finding. | `tests/unit/test_lint_comparisons.py::LintComparisonsTest::test_heredoc_data_is_excluded_from_shell_rules` |
| audit:b24d313:6 | `$'it\'s fine'` does not hide a following valid allow comment. | `tests/unit/test_lint_comparisons.py::LintComparisonsTest::test_ansi_c_quotes_preserve_following_marker_comments` |
| audit:b24d313:7 | `'123'`, `'END-DATA'`, mixed or escaped delimiters and tab-stripped bodies do not expose body markers. | `tests/unit/test_lint_comparisons.py::LintComparisonsTest::test_all_valid_heredoc_delimiters_exclude_body_markers` |
| 4313892754 | Retain the original continued-program cases; add a command-substitution case whose double-quoted program splits `.path` across a continuation. | `tests/unit/test_lint_comparisons.py::LintComparisonsTest::test_a_jq_program_continued_by_backslash_newline_is_located_and_r3_applies` |
| 4313892766 | Retain the original joined-word cases; add `pgrep -f` with `$1` split between `$` and `1` by backslash-newline, requiring R5. | `tests/unit/test_lint_comparisons.py::LintComparisonsTest::test_a_backslash_newline_joins_the_physical_lines_without_a_separator` |
| 4313892783 | Retain multiline strings and heredocs; add a reasonless marker inside an `'END-DATA'` body, requiring no R0. | `tests/unit/test_lint_comparisons.py::LintComparisonsTest::test_a_marker_inside_a_multiline_string_or_heredoc_body_is_not_a_comment` |

The original three Bot reproductions already pass at e520a7fe after f6fd955e. Their strengthened selectors must each fail an intended assertion there; identify the failing variant and record overlap with audit coverage. Do not falsely label already-green controls as red.

Retain a02's own fixtures under these selectors, including all `OWNED_ROWS` cases and the `k4.sh` trailing-marker case:

- `tests/unit/test_lint_comparisons.py::LintComparisonsTest::test_a_single_quoted_jq_option_value_is_not_read_as_the_program`
- `tests/unit/test_lint_comparisons.py::LintComparisonsTest::test_a_jq_normaliser_name_inside_a_string_literal_is_no_application`
- `tests/unit/test_lint_comparisons.py::LintComparisonsTest::test_every_f_string_interpolation_in_a_regex_is_escaped`
- `tests/unit/test_lint_comparisons.py::LintComparisonsTest::test_each_owned_row_is_refused_or_accepted_by_its_fixture`

Add `tests/unit/test_lint_comparisons.py::LintComparisonsTest::test_shfmt_missing_refuses_without_fallback` and `tests/unit/test_lint_comparisons.py::LintComparisonsTest::test_shfmt_parse_failure_refuses_with_original_message`; the latter also covers unusable JSON. Retain the stale-row selector named in the threat table.

Amendment 1 (2026-10-20T00:21:41Z, a008's question q1/q2 of 00:19Z): the dialect follows the file (`-ln zsh` for a `.zsh` name or a zsh shebang, else `-ln bash`); a `.tmpl` file is a target only when its name without `.tmpl` or its shebang is shell or Python; chezmoi template actions (`{{ ... }}`) in a shell template are blanked to spaces before shfmt parses it (offsets and newlines kept); shfmt is invoked as `shfmt` on PATH or, when absent, as `mise x shfmt@3.14.1 -- shfmt` (the pinned form `.github/workflows/test.yaml:313` already uses, so the unit jobs need no workflow change); when neither runs, the lint refuses with `shfmt missing`; a real parse failure refuses with shfmt's message, never falls back to a regex scan and never enters the baseline. validation.md records which invocation ran locally and in CI (the job log line).

## Check

The final diff has at most **450 changed lines outside `tests/` and `.orchestration/`, excluding `scripts/lint-comparisons-baseline.tsv`**, measured by `git diff --numstat origin/main...HEAD`; changed lines mean additions plus deletions. The same diff has at most **1200 added lines under `tests/`**. Both totals include inherited branch changes. There is no separate script-length cap. RESULT records the final per-file numstat and both totals without raising either cap.

Before implementation, run the final regression test source against production code from `e520a7fe4dd5f84acb46927927999998c188eb51`. Each of the ten finding selectors must fail for its intended behavior, then pass on the reset head. Record production revision, test-source SHA256, exact invocation, output and exit status. Missing methods, import failures, unavailable shfmt, skipped tests and zero-test runs are not red proofs. Preserve inherited green controls separately.

Run a targeted mutation check of these fixtures, with at least one executed mutant per finding row, and paste each mutation, killing selector, command, output, exit status and killed/total count. Include mutations that bypass AST refusal or restore false comment, continuation, heredoc or word-fragment behavior. A mutant rejected only because its Python source is invalid does not count.

Run the complete lint module suite, the repository Python unit suite, lint and formatting checks through the section 5.14 execution contract. The command payloads are `python -I -m unittest discover -s tests/unit -p test_lint_comparisons.py -v`, `python -I -m unittest discover -s tests/unit -v`, `python -I scripts/lint-comparisons.py`, `ruff check scripts/lint-comparisons.py tests/unit/test_lint_comparisons.py` and `make format`. Paste complete outputs and per-command exit statuses, including formatting failures. Do not run local Bats.

Unit jobs require shfmt on PATH. The premises show the formatting step's scoped 3.14.1 invocation, but no guaranteed PATH provisioning for the subsequent Python step; the host config also says `latest`. Record actual executable/version probes wherever tests run. If a unit job lacks shfmt, preserve the clear refusal and report the dependency blocker; workflow and mise changes are outside `allowed_files`, and tests must not skip or conceal it.

## Scope, artifacts and completion

Worker Playbook step 4 applies with section 5.14 item 10: every command stays inside the sandbox. A denial, unavailable dependency or required operation outside the boundary produces `AGMSG-PONG v1 status=blocked` naming the exact command, output and boundary. Never escape, request an unsandboxed retry or pursue the denied outcome through another tool.

Use `.orchestration/dotfiles-T129-normalised-comparison-lint-followup-a04/` for `task.md`, `report.md`, `validation.md`, `sandbox.md`, `learning.md` and `autoskill.md`. The task copy is byte-identical to dispatch; historical a02 artifacts remain unchanged. Worker Crit JSON and receipt filenames contain `-worker-`. Keep plan/todo/learn uncommitted, with at most one active todo per owner. Record `cost: n/a` when runtime cost data is unavailable.

No workflow, dependency manifest, permission policy, hook, launcher, other comparison implementation or knowledge-graph update is allowed. This is `security: false`: the lint reads repository files locally and in CI, changes no trust boundary, and executes no repository input outside the sandbox.

Use `done_signal=AGMSG-RESULT` and `max_turns=6`. RESULT names PR #432, branch, anchor, actual starting and final heads, base, changed-file inventory, task-copy SHA256, ten finding-to-selector mappings, inherited controls, red/green proofs, mutation evidence, final per-file numstat, both cap totals, dependency observations, proposed feedback dispositions and all artifact paths.

Every corrective round, including pre-push and pre-RESULT review fixes, counts toward a04's INV-6 limit of two; the reset does not erase a02's exhausted history. Stop before a third correction round or another repeated-family patch and request an orchestrator re-plan. Surviving P0/P1 findings remain open for the operator's decision.

Crit review stays agent-side under repository rules. Final-head CI must pass before a ready RESULT; record unavailable checks as blockers. The orchestrator owns feedback collection, thread dispositions, task-level audit, acceptance and the integration gate in Orchestrator Playbook step 10 order, including `make require-crit-review` with the required evidence. The worker never merges and opens no second PR.

Local Bats and deployment are not checked by this task; CI supplies required Bats results. Runtime-generated jq programs and unprovided shfmt remain explicit limits.

## Checks (pasted by the orchestrator before each send)

```
dispatch to a008 (worker-f), 2026-10-20T00:03:38Z; task-consistency-check.py: OK; security: false (no C-80); reset_of dotfiles-T129-normalised-comparison-lint-followup-a02 (its PR #432 continues: ten hand-parser findings after the a02 tokenizer re-plan -> shfmt AST design, re-plan line in the a02 record); predecessor counters (regime-counters.sh): task=dotfiles-T129-normalised-comparison-lint-followup-a02 tasks=2 amendments=1 questions=1 results=2 withdrawn=0 revises=1 first_result_head=26f4897313cef4ad4be3f27c3a3985e63707aab5 bot_p1_heads_after_result=0 audits=unknown wall=2026-10-19T11:36:30Z..2026-10-19T21:37:51Z (10:01) source=live; design 5.14 by reference (D-024-30); measured text: 221 lines, 4 allowed files
amendment 1, 2026-10-20T00:21:41Z: dialect per file, .tmpl targeting, chezmoi actions blanked, pinned mise exec for shfmt when absent (previous_sha256 e58d51b185769577911b5661796529d12f873fb2ffb0f25d1826b47029958b10); checker re-run; S2 counter: amendments 1, questions 1
```