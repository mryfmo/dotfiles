---
format: 2
task_id: dotfiles-T129-anthropic-auth-route-check-followup-a03
kind: code
security: true
allowed_files:
  - scripts/validate-agent-assets.py
  - tests/unit/test_validate_agent_assets.py
  - .orchestration/dotfiles-T129-anthropic-auth-route-check-followup-a03/**
after: []
reset_of: [dotfiles-T129-anthropic-auth-route-check-followup-a02]
threat_table:
  - control: "scripts/validate-agent-assets.py (the shared shell scanner and decoder, Anthropic credential validation and registration in main)"
    disposition: "closed: tests/unit/test_validate_agent_assets.py::test_anthropic_check_bypass_corpus"
  - control: "tests/unit/test_validate_agent_assets.py (retained parser and real-entry fixtures, the six new tests and the bypass corpus)"
    disposition: "residual: temporary tracked fixture repositories exercise real discovery and validation; regression assertions check verdicts and diagnostics, and the final audit checks the corpus against both local reviews"
  - control: ".orchestration/dotfiles-T129-anthropic-auth-route-check-followup-a03/** (the reset task's branch artifacts)"
    disposition: "residual: artifacts remain within this task's directory, identify their tested revisions and commands, and are checked against the final diff and CI before acceptance"
  - control: "the task-file copy on the branch .orchestration/dotfiles-T129-anthropic-auth-route-check-followup-a03/task.md replaces .orchestration/dotfiles-T129-anthropic-auth-route-check-followup-a02/task.md in the first push"
    disposition: "residual: the worker deletes only the predecessor task copy as the explicit reset-bookkeeping exception; the a03 copy is byte-identical to the dispatched text, and its own sha256 is compared with the TASK and RESULT at acceptance"
  - control: "the branch evidence records under .orchestration/dotfiles-T129-anthropic-auth-route-check-followup-a03/ (report.md, validation.md, sandbox.md, learning.md and worker review evidence)"
    disposition: "residual: records separate inherited evidence from new results, omit credentials and machine-specific home paths, and bind red and green outputs to their source revisions for the final audit"
  - control: "applied-file inputs under home/ and install/ (structured documents, chezmoi template sources and shell text controlled by the PR)"
    disposition: "residual: tracked regular files are read without executing their contents or following symlinks; structured decoding, rendering and parsing failures refuse validation, shell names are decoded or refused as unsupported, and assignment payloads are redacted before diagnostic key paths are escaped"
  - control: task metadata
    disposition: "residual: the dispatched file passes task-consistency checks C1 to C10 and C7b before dispatch and acceptance; whole-file byte comparison binds the branch copy to that file"
  - control: metadata separators
    disposition: "residual: the first YAML document supplies front matter, and whole-file byte comparison covers its separators and the task body"
  - control: in-process effects
    disposition: "residual: parsers, the scanner, the decoder and the existing template renderer inspect data without executing applied scripts or evaluating shell expansions; fixture tests use temporary roots and leave the live home directory untouched"
  - control: workflow and interpreter or environment inputs
    disposition: "residual: workflow, dependency and interpreter configuration changes are outside allowed_files; the existing Python and PyYAML environment runs the check, and failed Git discovery or unavailable required parsing refuses validation"
  - control: new or renamed scripts
    disposition: "residual: this task changes the existing validator and test module only; the final diff and audit reject any new or renamed executable"
  - control: orchestrator effect merge
    disposition: "residual: the orchestrator merges PR 412 through gh pr merge --squash --match-head-commit only after final-head feedback, task-level audit, security review, acceptance and the integration gate"
  - control: orchestrator effect update-branch
    disposition: "residual: an update changes the head, so CI, feedback collection, local review, task-level audit and security review are refreshed before the integration gate"
  - control: orchestrator effect forced worker removal
    disposition: "residual: ordinary removal refuses a dirty worktree; any forced removal requires an acceptance record identifying the uncommitted state it discards"
premises:
  - claim: the current validator already defines the template-rendering helper that this task reuses
    command: /usr/bin/grep -c '^def render_template_text' scripts/validate-agent-assets.py
    output: |-
      1
  - claim: the continuing branch remains at the committed head reviewed by PR 412
    command: git rev-parse tools/anthropic-auth-route-structured
    output: |-
      65841e68f3ee119adcb8ab130e698256f9268ed0
  - claim: the current managed Claude settings source contains an OS-conditional chezmoi template block
    command: /usr/bin/grep -c '{{ if eq .chezmoi.os' home/.chezmoitemplates/claude-settings-managed.json
    output: |-
      1
  - claim: the continuing branch already contains the applied-file format classifier
    command: git show 65841e68f3ee119adcb8ab130e698256f9268ed0:scripts/validate-agent-assets.py | /usr/bin/grep -c '^def applied_file_format'
    output: |-
      1
---

# AGMSG-TASK dotfiles-T129-anthropic-auth-route-check-followup-a03 — S1 redesign of dotfiles-T129-anthropic-auth-route-check-followup-a02 (plan 006 INV-6; PR #412)

This redesign is written by a review-profile context other than a02's author. The local review of a02's revise-1 head, update-branched to `a64daf175c24a7f3e00d6f558cd255ea9ba5b356`, found one P1 and three P2. The ANSI-C name bypass is the third finding of class `shell-quoting-bypass`, triggering S1. The artifact has used its one revise round, another would reach plan 006 INV-6's second revise, and the operator's directive forbids a third round. The orchestrator records a02 as withdrawn and reset by this task before dispatch and preserves its acceptance history and counts.

PR #412 continues against `main` on the same branch, `tools/anthropic-auth-route-structured`, from revise-1 implementation head `a9056299ba965457b569de2d52aa0cbb7abb6e50`. Its incorporated main updates remain preserved. The worker deletes `.orchestration/dotfiles-T129-anthropic-auth-route-check-followup-a02/task.md` in the first push and adds this dispatched text's byte-identical copy at `.orchestration/dotfiles-T129-anthropic-auth-route-check-followup-a03/task.md`. That predecessor-copy deletion is the sole reset-bookkeeping exception to `allowed_files`. The worker changes no other predecessor artifact or canonical task text.

Seat a010 executes this task first. The same seat holds `dotfiles-T133-permission-guard-gate-a03`, stacked on this branch, and resumes that task by rebasing it onto the new #412 head afterwards. Its deadline remains `2026-10-19T03:00Z`. This redesign stays within the existing caps and closes the named findings before that stacked work resumes.

PR #396 stays open as the stacked record until #412 merges. PR #389 is superseded and supplies no merge precondition. Existing lineage evidence remains historical evidence.

The premises preserve a02's write-time observations verbatim. Current branch identities and rerun observations are recorded separately before dispatch and acceptance. The requested a02 report paths are absent from the `a9056299` tree; the corresponding `revise1-report.md`, `report.md` and `validation.md` under worker-e's same relative a02 directory supply inherited evidence. Their recorded checks do not establish this task's final-head results.

## Goal

The Anthropic credential check uses parsed structured data and one shared shell word scanner with one decoder. Shell quoting, escaped names, Markdown prose and non-LF characters cannot hide a prohibited authentication assignment. Unsupported authentication name forms cause refusal, and diagnostics never disclose an assignment's payload. The two fixes at `a9056299` remain intact, and the four open findings of `a64daf1` receive named red-then-green regression tests.

## Files

1. `scripts/validate-agent-assets.py` retains `validate_anthropic_auth_route()` in the real `main()` entry beside `validate_no_obvious_secrets()`. Discovery uses `git ls-files -z -- home install`, refuses a failed listing and does not follow tracked symlinks. R1 refuses occurrences of `ANTHROPIC_OAUTH_TOKEN` in applied text and decoded structured content. R2 permits an API-key value only when its whole value is one environment reference, one template expression or empty. Shell references pass bare or double-quoted; single-quoted references are literal text and are refused. Suffixes, fallback expansions, command substitutions and concatenated values remain refused.

   One scanner function with one decoder supplies the export and assignment check, Markdown example inspection and the whole-value allowlist. Shell-text decisions use scanner output rather than regexes over raw lines. The scanner handles single quotes, double quotes, backslash quoting, ANSI-C `$'…'` and locale `$"…"` quoting. The decoder applies the quoting form's rules before comparing a name with the two credential variable names. Backslashes remain literal inside single quotes. Runtime-dependent names are refused as unsupported rather than evaluated.

   An assignment word extends to its unquoted blank or shell operator. Space and tab are shell blanks, and LF is the only line ending. U+2028, U+2029 and vertical tab remain word characters. Quoted or escaped blanks remain part of the word. The whole-value decision uses that complete word and preserves the distinction between a reference and literal text.

   Existing R2 tests retain whole-value references, empty values, comments after empty values, quoted keys, compound assignments and refusal of single-quoted references. `test_anthropic_auth_route_normalizes_shell_names_and_refuses_unreadable_names` retains quoted and escaped names, line continuations, dynamic exports, case-pattern boundaries, nested substitutions, ordinary parameter expansions in values and quoted awk programs. The saved case-pattern bypass remains refused. Existing tests that inspect the old raw-line regex are converted to behavioral assertions over the same fixtures as that implementation is replaced.

2. `applied_file_format` continues to select the format after stripping chezmoi attribute prefixes from the basename. `modify_`, `run_`, `symlink_`, `encrypted_` and `.tmpl` sources remain script text inspected through the shared scanner. Every other `.json`, `.toml`, `.yaml` or `.yml` source uses `json.loads`, `tomllib` or the validator's existing YAML reader. Every decoded key path and string value is inspected. Duplicate mapping entries remain visible, and YAML aliases cannot multiply traversal. Structured values retain data semantics after their format parser has decoded quoting and escapes.

   Structured sources are decoded as strict UTF-8 before parsing or template rendering. Malformed bytes, structured parse failures and unavailable required parsing cause refusal naming the source and a fixed error type. Parser exception messages and malformed content are omitted. Script-text decoding retains its existing behavior.

   `test_anthropic_auth_route_reads_json_and_toml_through_their_parsers`, `test_anthropic_auth_route_reads_yaml_through_its_parser`, `test_anthropic_auth_route_reads_a_json_reference_before_a_delimiter` and `test_anthropic_auth_route_check_refuses_malformed_utf8_in_a_structured_source` remain green. Their fixtures retain escaped keys, nested mappings, multiline values, duplicate keys, invalid documents, attribute-prefixed sources, script classifications, aliases and allowed references. These cases retain the dispositions of 4302758230, 4302758234, 4302758239 and 4305863865.

3. The real-entry and template fixes remain in place. `test_anthropic_auth_route_refuses_an_oauth_token_in_applied_files_and_a_literal_api_key_assignment` calls the real `main()` on a temporary tracked fixture tree, with the Anthropic check and Git discovery real and unrelated validators isolated. It retains OAuth and literal-key refusals under `home/` and `install/`, allowed-reference passes and exclusion of the same OAuth text under `scripts/`. Its registration-only mutation evidence remains identified by the tested source revision.

   A structured-format source under `home/.chezmoitemplates/` containing `{{` is rendered for both `darwin` and `linux` through `render_template_text(path, os_name)` before each output is parsed and checked. A malformed rendering causes refusal. The renderer's existing default and other callers retain their behavior. `test_anthropic_auth_route_parses_both_platform_renderings_of_chezmoi_templates` retains its conditional-platform fixture, allowed-reference pass, literal-credential refusals in either branch and malformed-output refusal. These cases retain the fixes for 4305965376, 4305965379, the template-classification CI failure and the surviving a010 case.

4. The P1 `local:a64daf1:1` is fixed by decoding ANSI-C-escaped authentication names before comparison. `test_anthropic_check_decodes_ansi_c_escaped_names` in `tests/unit/test_validate_agent_assets.py` is written first and is red against the unchanged `a9056299` validator. It reports `export $'ANTHROPIC_API_\x4bEY'=literal-value` as R2 and the OAuth equivalent `export $'ANTHROPIC_OAUTH_\x54OKEN'=literal-value` as R1. Fixture bytes preserve the shell escapes so Python does not decode the bypass before validation. The test also preserves an allowed whole-value reference for the decoded API-key name. The shared decoder supplies the fix, and the test is green on the final head.

5. The P2 `local:a64daf1:2` is fixed by parsing each Markdown fenced example as independent shell text with a fresh quote state. Fence extraction precedes shell scanning and never joins separate examples into one shell input. Prose and preceding examples cannot carry quote state into a later example. `test_anthropic_check_parses_each_fenced_example_with_a_fresh_quote_state` is written first and is red against the unchanged `a9056299` validator. A tracked Markdown fixture begins with `Don't store credentials.` and later contains a fenced example with `NAME=ANTHROPIC_API_KEY; export "$NAME"=literal-value`. The test asserts refusal with the unsupported-name diagnostic and no payload disclosure. The same example after prose without an apostrophe has the same verdict. The test is green on the final head.

6. The P2 `local:a64daf1:3` is fixed by applying the LF-only rule throughout shell scanning, including `anthropic_text_findings`, applied script inspection and whole-value validation. `splitlines()` and Unicode whitespace predicates do not determine shell word boundaries. `test_anthropic_check_splits_shell_text_on_lf_only` is written first and is red against the unchanged `a9056299` validator. Its fixtures place actual U+2028, U+2029 and vertical-tab characters between `$DEPLOYED_KEY` and `literal-value` in an API-key assignment. Each suffix remains in the assignment word and causes R2 refusal, including when the shell text is a decoded structured string. Ordinary LF-separated commands and unquoted space or tab after an allowed reference retain their expected verdicts. The test is green on the final head.

7. The P2 `local:a64daf1:4` is fixed by redacting assignment payloads before constructing or printing diagnostic key paths. The text after an assignment's `=` is replaced with `<redacted>`, including in mapping keys and ancestor key-path components. The sanitized path is then escaped to prevent forged log lines. `test_anthropic_check_redacts_assignment_payloads_in_diagnostics` is written first and is red against the unchanged `a9056299` validator. The JSON fixture `{"ANTHROPIC_API_KEY=literal-value": "unused"}` is refused, its diagnostic contains `<redacted>` and does not contain `literal-value`. A decoded TOML-escaped assignment-bearing key and a nested key-path fixture retain the same protection. Parser messages, assignment payloads and structured values never enter diagnostics. The test is green on the final head.

8. Unsupported authentication name forms are refused whenever the scanner cannot decode a name statically. Parameter indirection, command substitution and variable-assembled names do not become harmless because their partially decoded spelling is not an identifier. `test_anthropic_check_rejects_undecodable_name_forms` is written first and is red against the unchanged `a9056299` validator. It checks `${x}EY` and `$(echo ANTHROPIC_API_KEY)` as export assignment names and asserts refusal with the diagnostic category `unsupported authentication name form`. It also covers parameter indirection and a quoted variable-assembled name. The diagnostic contains no assignment payload. Existing unreadable-name refusals retain their verdicts, and their diagnostic assertions follow the explicit unsupported category. The test is green on the final head.

9. `test_anthropic_check_bypass_corpus` is written first and is red against the unchanged `a9056299` validator. One table records each fixture's source kind, shell text or structured input, expected verdict and required diagnostic assertions. It includes the bypass strings and legitimate forms of both local reviews: the single-quoted backslash followed by a dynamic export, environment-only assignments followed by a command or operator, both ANSI-C-escaped credential names, the Markdown prose-and-fence case, the non-LF suffix cases and the assignment-bearing mapping key. It also includes the unsupported-name forms, the other required quoting forms, an environment-only reference followed by a command, a quoted literal that is not a credential name and a statically decoded ordinary variable name. Each row asserts its expected verdict. Refusal rows assert the rule or unsupported category and absence of the payload, and the mapping-key row asserts `<redacted>`. The corpus reuses the existing temporary tracked fixture pattern and is green on the final head.

The two findings of `b139995` remain fixed at `a9056299`: single-quote backslash semantics retain `test_anthropic_check_keeps_single_quote_semantics_for_backslashes`, and assignment-word boundaries retain `test_anthropic_check_accepts_an_environment_reference_followed_by_a_command`. Their historical red evidence identifies the pre-fix revision, and both tests run green on this task's final head.

All six new tests are written before the implementation changes and produce recorded red results against `a9056299ba965457b569de2d52aa0cbb7abb6e50`. The unsupported-name test's red assertion includes the explicit unsupported diagnostic category. Retained tests are not claimed to be red against that already-fixed head. Existing parser, duplicate-key, alias, placeholder and secret-scan coverage remains green.

## Out of scope

The omp auth store probe, PR #404, any manifest change and any rendered settings change are outside this task. Changes to `SECRET_PATTERN`, its placeholder allowlist, workflow files and dependencies are outside this task. Live credential inspection and applying files to the user's home directory are outside this task.

## Check

`uv run python -m unittest tests/unit/test_validate_agent_assets.py -v` is green, and its output is pasted in `.orchestration/dotfiles-T129-anthropic-auth-route-check-followup-a03/validation.md`. The YAML parser cases run with the repository's existing PyYAML environment, and any dependency-related skip is identified.

`make validate-agent-assets` exits 0 on the continuing branch with main's current template, and its output and exit status are pasted in the same validation file. The red and green outputs identify their exact source revisions or isolated registration mutation. Each of the six new tests has red output against `a9056299ba965457b569de2d52aa0cbb7abb6e50` and green output on the final head. The two retained `b139995` regression tests carry their historical red provenance and fresh final-head green results.

`ruff check scripts/validate-agent-assets.py tests/unit/test_validate_agent_assets.py` and `git diff --numstat origin/main...HEAD` are recorded. The diff contains at most 300 changed lines, added plus deleted, outside `tests/` and `.orchestration/`, and at most 1000 changed lines under `tests/`. Fixture lines count toward the test cap. Bats tests are not run locally.

Inherited Ruff findings are recorded with their exit status and compared against the unchanged baseline at the original filenames. A failing command is not labelled passing, and this task adds no suppression or unrelated repair.

The orchestrator runs the format-2 task-consistency checker, including C1 to C10 and C7b, before dispatch and at acceptance. The first-push file inventory proves removal of the a02 task copy and addition of the byte-identical a03 copy.

## Completion

One branch and one continuing implementation PR complete this task. PR #412 remains the main-target PR on `tools/anthropic-auth-route-structured`. PR #396 remains open as the stacked record until #412 merges. The first push contains the predecessor-copy deletion and the new a03 task copy. No second implementation PR or fresh branch is created for this reset.

The Completion clause of `.orchestration/tasks/dotfiles-T129-normalised-comparison-lint-a01.md` applies as written with `dotfiles-T129-anthropic-auth-route-check-followup-a04` as the owner of any advisory P2 and `task_copy=<sha256 of .orchestration/dotfiles-T129-anthropic-auth-route-check-followup-a03/task.md>` in the RESULT. This task's continuing branch, existing PR and command restrictions govern the corresponding steps of that clause. The orchestrator writes the advisory owner's task before recording its first owned row.

The four open findings of `a64daf1` are owned and fixed by this task. They are not deferred as advisory P2. The earlier advisory-owner text using this task's identifier is superseded by this S1 reset. The a02 acceptance history and its revise count remain preserved. Every worker-side fix round counts toward INV-6, including a round before the first RESULT.

The RESULT names `pr=412`, the final head, base, branch, files, test names, cap totals, evidence paths and the a03 task-copy hash. It records each of `local:a64daf1:1` through `local:a64daf1:4` with its fixing commit, identifies the unsupported-name and corpus checks, and retains both `b139995` findings as fixed at `a9056299` with fresh green regression evidence. It retains 4305965376 and 4305965379 with their fixing commits, identifies the template CI fix and surviving case regression, and retains the disposition of 4305863865.

Evidence is written under `.orchestration/dotfiles-T129-anthropic-auth-route-check-followup-a03/` in the worker's worktree. A Codex seat uses those same relative paths and explicitly says so in its report and RESULT. The records distinguish inherited outputs from checks run on the final head. Worker-side review evidence uses the required `-worker-` infix and follows the repository's review-evidence and receipt gate rules.

`security: true` requires the task-level audit and a separate security-profile review on the final head before integration. The orchestrator follows Orchestrator Playbook step 10 for feedback collection, audit dispositions, acceptance, the integration gate and merge. A changed head requires refreshed final-head evidence.

Git and gh writes run as single commands, without shell chaining or a wrapper combining writes. The worker posts no `@codex review` request and runs no `gh pr edit` or `gh pr comment`. CI and automatic reviews are awaited within the existing bounded window; an absent automatic Bot review is recorded as `bot: none` after that window. Thread replies and resolutions remain the orchestrator's responsibility.

Until P1-14 lands, any string containing the words `gh pr merge` or `gh pr create` is written with the file-edit tool, never in a Bash heredoc or `echo`. This restriction applies to task copies, reports and evidence text.

After this task's new head is pushed and its handoff is complete, seat a010 resumes `dotfiles-T133-permission-guard-gate-a03` and rebases that stacked task onto the new #412 head. Its `2026-10-19T03:00Z` deadline remains unchanged.

The redesign uses read-only repository evidence and claims no new implementation or green validation. The four open findings remain blocking until the worker supplies the required final-head evidence.

## Checks (pasted by the orchestrator before each send)

```
dotfiles-T129-anthropic-auth-route-check-followup-a03.md: OK
premises: copied from a02 verbatim (write-time outputs of 2026-10-18)
masked 0 match(es) in .orchestration/tasks/dotfiles-T129-anthropic-auth-route-check-followup-a03.md
```