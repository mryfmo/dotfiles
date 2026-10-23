---
format: 2
task_id: dotfiles-T129-anthropic-auth-route-check-followup-a05
kind: code
security: true
allowed_files:
  - scripts/validate-agent-assets.py
  - tests/unit/test_validate_agent_assets.py
  - scripts/lint-comparisons-baseline.tsv
  - .orchestration/dotfiles-T129-anthropic-auth-route-check-followup-a05/**
after: []
reset_of: [dotfiles-T129-anthropic-auth-route-check-followup-a04]
threat_table:
  - control: "scripts/validate-agent-assets.py (credential_occurrences, allowed_assignment_line, retained decoders, applied-file discovery and main registration)"
    disposition: "residual: the fixed whole-line allowlist is the whole trust decision; raw and retained decoded views find the recorded corpus, but a credential assembled from pieces that no decoder joins is not found and the final-head audit checks this limit rather than claiming shell-language completeness"
  - control: "tests/unit/test_validate_agent_assets.py (the table-driven lineage corpus, unseen-shape test, retained honest forms, parser and real-entry fixtures)"
    disposition: "residual: temporary tracked repositories exercise discovery and the real entry point; the audit compares every review reproduction and inherited worker corpus row with its fixture bytes, new-policy verdict and redaction assertions"
  - control: ".orchestration/dotfiles-T129-anthropic-auth-route-check-followup-a05/** (this reset task's branch artifacts)"
    disposition: "residual: artifacts stay in this task's directory, name their tested revisions and commands, and distinguish inherited scanner evidence from final-head results"
  - control: the PR edits scripts/lint-comparisons-baseline.tsv only for the rows of its own changed lines (D-024-24 rebase repair)
    disposition: "residual: a row matches a hit of a changed line of this PR and nothing else; tests/unit/test_lint_comparisons.py::LintComparisonsTest::test_the_changed_files_are_clean_against_the_baseline in CI"
  - control: "the task-file copy on the branch .orchestration/dotfiles-T129-anthropic-auth-route-check-followup-a05/task.md and the reset_of task's copy .orchestration/dotfiles-T129-anthropic-auth-route-check-followup-a04/task.md"
    disposition: "residual: the first push deletes the a04 copy as the sole reset-bookkeeping exception; the a05 copy is byte-identical to the dispatched text and its own sha256 is compared with the TASK and RESULT at acceptance"
  - control: "the branch evidence records under .orchestration/dotfiles-T129-anthropic-auth-route-check-followup-a05/ (report.md, validation.md, sandbox.md, learning.md, autoskill.md, measure.md and worker review evidence)"
    disposition: "residual: records omit credentials and machine-specific home paths, preserve historical provenance, and bind new claims to commands, exit statuses and the final head for the audit"
  - control: "applied-file inputs under home/ and install/ (structured documents, chezmoi template sources and shell text controlled by the PR)"
    disposition: "residual: tracked regular files are read without executing their contents or following symlinks; raw text and decoded views are inspected, parsing and rendering failures refuse validation, and payloads are redacted before diagnostic key paths are escaped"
  - control: task metadata
    disposition: "residual: the dispatched file passes task-consistency checks C1 to C10 and C7b before dispatch and acceptance; whole-file byte comparison binds the branch copy to that file"
  - control: metadata separators
    disposition: "residual: the first YAML document supplies front matter, and whole-file byte comparison covers its separators and the task body"
  - control: in-process effects
    disposition: "residual: stateless occurrence detection, fixed regex matching, data parsers and the existing template renderer inspect data without executing applied scripts or evaluating shell expansions; fixture tests leave the live home directory untouched"
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

# AGMSG-TASK dotfiles-T129-anthropic-auth-route-check-followup-a05 — class-stop redesign of a04 (shell-quoting-bypass; plan 006 INV-6; PR #412)

This text is the independent redesign by a review-profile context other than the author of a04. The a02 acceptance record's class table and the a04 acceptance record's withdrawal decision stop the scanner design. The local reviews of `b139995`, `a64daf1` and `325f520` and the worker's reviews repeatedly found another shell form after a scanner correction. The security review of `325f520` adds the unmatched-glob reproduction to the same class. This task implements the a04 record's default-deny re-plan. The earlier scanner specification and a04's 330-line amendment are superseded.

PR #412 continues against `main` on the same branch, `tools/anthropic-auth-route-structured`. Its committed head `325f520bfc8b4dbb25e0744d27878cdf7eab2fd2` is the implementation starting point. The first push deletes `.orchestration/dotfiles-T129-anthropic-auth-route-check-followup-a04/task.md` and adds this dispatched text's byte-identical copy at `.orchestration/dotfiles-T129-anthropic-auth-route-check-followup-a05/task.md`. The a04-copy deletion is the sole reset-bookkeeping exception to `allowed_files`. The worker changes no other predecessor artifact or canonical task text. The incorporated main updates remain preserved, and this reset uses one continuing implementation PR.

Seat a010 takes this task after its P1-14 RESULT for `dotfiles-T133-permission-guard-gate-a03`. The a04 record's fallback puts that P1-14 work on main without the #412 commits first. This task does not restore the superseded order in which P1-14 waited behind #412. The dispatch supplies this round's deadline.

PR #396 stays open as the stacked record until #412 merges. PR #389 is superseded and supplies no merge precondition. The a02, a03 and a04 acceptance histories, their worker-side fix counts and their recorded red and green results remain historical evidence. The premises preserve a04's premises verbatim, including historical branch observations; current branch identities and rerun observations are recorded separately before dispatch and acceptance.

## Goal

The Anthropic credential check defaults to denial without understanding shell. Every credential-name occurrence in raw applied text and each retained decoded view is a finding unless its unchanged containing line matches the fixed allowlist of four environment-reference assignments. A comment beginning with `#` and Markdown prose naming a variable without `=` produce reported `note` findings with exit 0 when no hard finding exists; `docs/` remains outside applied-file discovery. The allowlist is the whole trust decision, diagnostics disclose no assignment payload, and a name assembled from pieces that no retained decoder joins remains an explicit residual.

## Files

1. `scripts/validate-agent-assets.py` retains `validate_anthropic_auth_route()` in the real `main()` beside `validate_no_obvious_secrets()`. Discovery remains `git ls-files -z -- home install`, refuses a failed listing and skips tracked symlinks and non-regular files. `applied_file_format` retains a04's chezmoi-attribute classification for JSON, TOML, YAML, template and script sources. The check inspects raw source before parsing or rendering can discard comments, and then inspects every decoded key and string value and both `darwin` and `linux` template outputs. A later allowed view never erases a finding in an earlier view.

2. `credential_occurrences(text) -> [(line_no, line, decoded_form)]` supplies the shared occurrence search. It finds `ANTHROPIC_API_KEY`, `ANTHROPIC_OAUTH_TOKEN`, decoded spellings of either name and identifiers that become either name after removing quote characters, backslashes, braces and the punctuation of `${…}`. It searches occurrences rather than shell assignment positions. LF alone separates lines; U+2028, U+2029, vertical tab and carriage return remain part of a containing line. The tuple retains the unchanged containing line and its one-based LF line number; `decoded_form` identifies the decoded spelling without becoming printable diagnostic content. Normalization does not trim or rewrite the line passed to the allowlist. Original source locations remain associated with decoded views, and Markdown examples retain their original offsets.

   Existing JSON, TOML and YAML data readers, `parsed_entry` traversal, `json_strings` where applicable and `render_template_text(path, os_name)` are reused. The view pipeline retains the existing decoder's ANSI-C and backslash character transformations and concatenated-piece handling without its shell-token or provenance interface. Percent and Unicode escape views participate in the same stateless occurrence search using existing decoding primitives and the standard library. Raw text and the text after each transformation are inspected. Decoding covers data and spelling transformations, never variable evaluation, arithmetic, commands or shell expansion. Duplicate mapping entries remain visible and YAML aliases cannot multiply traversal. Strict UTF-8, malformed structured-input refusal, missing-PyYAML refusal and malformed-template refusal remain intact. No dependency is added.

3. `allowed_assignment_line(line) -> bool` is the only acceptance predicate for a credential-bearing line. `NAME` is either credential name and `VAR` is an ASCII identifier other than either credential name. The four forms are `NAME=$VAR`, `NAME="$VAR"`, `NAME=${VAR}` and `NAME="${VAR}"`, each optionally preceded by the exact text `export ` and optionally followed by ` <command words>`. A command word is a nonempty run of ASCII letters, digits, `_`, `.`, `/` or `-`; words are separated by one ASCII space. The suffix contains no credential-name occurrence. The complete fixed Python regex is matched without flags against the unchanged line:

   `\A(?:export )?(?:ANTHROPIC_API_KEY|ANTHROPIC_OAUTH_TOKEN)=(?P<q>"?)\$(?:\{(?!ANTHROPIC_(?:API_KEY|OAUTH_TOKEN)\})[A-Za-z_][A-Za-z0-9_]*\}|(?!ANTHROPIC_(?:API_KEY|OAUTH_TOKEN)(?![A-Za-z0-9_]))[A-Za-z_][A-Za-z0-9_]*)(?P=q)(?: (?!.*ANTHROPIC_(?:API_KEY|OAUTH_TOKEN))[A-Za-z0-9_./-]+(?: [A-Za-z0-9_./-]+)*)?\Z`

   No substring match, whitespace stripping, decoded replacement of the original line or additional value allowlist broadens this regex. A quoted or encoded left-hand name, credential self-reference, empty value, template-valued assignment, suffix literal, fallback, compound or subscripted assignment, arithmetic form, wrapper, `env` or `builtin` form has no exception. Heredoc syntax has no dedicated allowance or expansion analysis; its raw credential-bearing lines face this same predicate. The four forms explicitly replace the earlier broader R1/R2 acceptance grammar.

4. The previous `auth_shell_words` scanner, its recursive shell parsing, quote state, word boundaries, command-prefix tables and provenance-based decisions are deleted. The two functions replace the scanner decisions in applied script inspection, Markdown inspection and decoded-content inspection. Markdown prose and code classification does not evaluate shell; prose and fences cannot suppress a code-line occurrence. A `#` at the beginning of a line makes its occurrences `note` findings, and a Markdown prose line naming a credential without `=` makes its occurrences `note` findings. Credential-bearing code and structured data receive no prose exception. Notes are printed and leave exit 0 when there is no hard finding. `docs/` files remain outside `home/` and `install/` discovery and are not added to the scan. Every other non-allowlisted occurrence is a hard finding. Reporting names a source, its location, a rule or note class and a fixed reason; it prints neither the containing line nor `decoded_form`. Assignment-bearing mapping keys and ancestor paths are redacted before log-line escaping.

5. `tests/unit/test_validate_agent_assets.py` consolidates the bypass strings from the three local reviews, the worker's `anthropic_a03_cases()` corpus and its pre-push regressions into one table-driven `test_anthropic_check_bypass_corpus` over raw lines. Each row records provenance, source kind, exact fixture bytes, expected finding class and exit status, and redaction and location assertions. The same rows exercise raw applied text and decoded structured-string views through the existing temporary tracked fixture pattern. The table includes every concrete inherited credential-bearing bypass; no family disappears when the scanner-specific helpers are deleted. A dynamic-name fragment retains its original bytes and the credential-binding context of its reproduction. A fragment containing no detectable credential spelling is a no-occurrence control, not a claim that variable evaluation exists. The following rows identify the lineage reproductions and their new-policy verdicts. In the table, `\"` denotes a double quote and `\n`, `\t`, `\u2028`, `\u2029` and `\v` denote actual fixture characters; shell ANSI-C escapes remain literal fixture bytes. The two presentation-escaped assignment quotes preserve the exact review reproductions without triggering the existing artifact secret scan.

   | Provenance | Raw fixture or retained context | Expected result |
   | --- | --- | --- |
   | `local:b139995:1` | `NAME=ANTHROPIC_API_KEY; printf '%s' '\'; export "$NAME"=literal-value` | Hard finding. |
   | `local:b139995:1` worker regression | `NAME=ANTHROPIC_API_KEY; out=$(printf '%s' '\'; export "$NAME"=literal-value)` | Hard finding. |
   | `local:b139995:1` worker regression | `NAME=ANTHROPIC_API_KEY; out="$(printf '%s' '\'; export "$NAME"=literal-value)"` | Hard finding. |
   | `local:b139995:2` | `ANTHROPIC_API_KEY=$DEPLOYED_KEY client` | Allowed form. |
   | `local:b139995:2` | `export ANTHROPIC_API_KEY=\"$DEPLOYED_KEY\"; exec client` | Hard finding under the new whole-line policy. |
   | `local:a64daf1:1` | `export $'ANTHROPIC_API_\x4bEY'=literal-value` | Hard finding. |
   | `local:a64daf1:1` OAuth equivalent retained by the worker | `export $'ANTHROPIC_OAUTH_\x54OKEN'=literal-value` | Hard finding. |
   | `local:a64daf1:2` | `Don't store credentials.\n\n` followed by a Markdown fence containing `NAME=ANTHROPIC_API_KEY; export "$NAME"=literal-value` | Hard finding at the original example line. |
   | `local:a64daf1:2` control | `Never store credentials.\n\n` followed by the same fenced example | The same hard finding. |
   | `local:a64daf1:3` | `ANTHROPIC_API_KEY=$DEPLOYED_KEY\u2028literal-value` | Hard finding. |
   | `local:a64daf1:3` worker extension | `ANTHROPIC_API_KEY=$DEPLOYED_KEY\u2029literal-value` | Hard finding. |
   | `local:a64daf1:3` | `ANTHROPIC_API_KEY=$DEPLOYED_KEY\vliteral-value` | Hard finding. |
   | `local:a64daf1:4` | `{"ANTHROPIC_API_KEY=literal-value": "unused"}` | Hard finding with payload redacted. |
   | `local:a64daf1:4` worker TOML regression | `"ANTHROPIC_API_\u004bEY=literal-value" = "unused"` | Hard finding with payload redacted. |
   | `local:a64daf1:4` worker ancestor regression | `{"parent=literal-value": {"ANTHROPIC_API_KEY": "literal-value"}}` | Hard finding with every assignment-bearing path component redacted. |
   | a03 worker review, source `577ad0f3` | `NAME=ANTHROPIC_API_KEY; EMPTY=; env $EMPTY "$NAME"=literal-value client` | Hard finding. |
   | a03 worker review, source `577ad0f3` | `NAME=ANTHROPIC_API_KEY; OPTION=-i; env "$OPTION" "$NAME"=literal-value client` | Hard finding. |
   | a03 worker unresolved-prefix class | `env $opts NAME=literal` with its recorded credential-binding context | Hard finding in that context. |
   | a03 worker quoted-leading-blank regression | `ANTHROPIC_API_KEY=\" $DEPLOYED_KEY\"` | Hard finding. |
   | a03 worker escaped-leading-blank regression | `ANTHROPIC_API_KEY=\ $DEPLOYED_KEY` | Hard finding. |
   | a03 worker concatenation regression | `ANTHROPIC_API_KEY=$DEPLOYED_KEY''` and `ANTHROPIC_API_KEY=''$DEPLOYED_KEY` | A hard finding for each row. |
   | a03 worker encoded-key regressions | `{"ANTHROPIC_API_KEY$'\x3d'literal-value": "unused"}` and `{"ANTHROPIC_API_KEY$'\072'literal-value": "unused"}` as correctly JSON-escaped fixture bytes | A hard finding for each row with payload redacted. |
   | a04 worker review, source `c15be6b9` | `ANTHROPIC_API_KEY=/usr/bin/env`, `ANTHROPIC_API_KEY=/usr/bin/export` and the retained wrapper-value rows | A hard finding for each row. |
   | a04 worker review, source `c15be6b9` | `NAME=ANTHROPIC_API_KEY; env >env "$NAME"=literal-value client` and `NAME=ANTHROPIC_API_KEY; env >export "$NAME"=literal-value client` | A hard finding for each row. |
   | a04 worker review, source `c15be6b9` | `NAME=ANTHROPIC_API_KEY; TOOL=env; "$TOOL" "$NAME"=literal-value client` | Hard finding. |
   | a04 worker corpus | `NAME=ANTHROPIC_API_KEY; env "$NAME"=/usr/bin/env client` | Hard finding. |
   | `local:325f520:1` | `export ANTHROPIC_API_KEY=; ANTHROPIC_API_KEY[1]=literal-value` | Hard finding. |
   | a02 class-table subscript variant | `ANTHROPIC_API_KEY[0]=literal-value` | Hard finding. |
   | `local:325f520:2` | `NAME=ANTHROPIC_API_KEY; builtin -- export "$NAME"=literal-value` | Hard finding. |
   | `local:325f520:3` in TOML and YAML | `# export ANTHROPIC_OAUTH_TOKEN=x` | Reported note and exit 0 with no hard finding. |
   | `local:325f520:4` honest reference body | `ANTHROPIC_API_KEY=$DEPLOYED_KEY` | Allowed only by the raw-line regex, with no heredoc exception. |
   | `local:325f520:5` | A Markdown example whose `ANTHROPIC_API_KEY=literal-value` line is line 4 | Hard finding reported at line 4. |
   | security review of `325f520`, unmatched glob | `shopt -s nullglob\nNAME=ANTHROPIC_API_KEY\nenv /__codex_audit_no_such_dir__/* "$NAME"=audit_dummy /usr/bin/printenv ANTHROPIC_API_KEY` | Hard finding. |
   | security review of `325f520`, declaration wrapper | `NAME=ANTHROPIC_API_KEY\nbuiltin -- export "$NAME"=audit_dummy` | Hard finding. |

   The table also retains every concrete expansion of the worker's seven-prefix corpus for `env`, `exec`, `command`, `nohup`, `sudo`, `xargs` and `time`, including unknown and attached options, vanishing and special-parameter expansions, dynamic names, redirection operands, numbered and brace file descriptors, descriptor duplication, append and process redirection, path-qualified env and unresolved executable paths. It retains the quoted, backslash-escaped, ANSI-C, locale, brace-assembled, continued-name, nested-substitution, case-pattern, heredoc, encoded-ancestor and YAML complex-key fixtures already in the a04 tests. Each credential-bearing bypass is a finding under the new policy. Old scanner-only refusal assertions for credential-free shell syntax become no-occurrence controls. Historical allowed rows outside the four forms become explicit rejection rows; no parser-specific acceptance survives implicitly. The table adds percent-escaped, Unicode-escaped and concatenated-piece credential spellings and an allowed-looking prefix followed by a second literal credential assignment. Every hard row asserts refusal and absence of `literal-value` or `audit_dummy` in diagnostics, and note rows assert reporting without refusal.

6. `test_anthropic_check_refuses_an_unseen_shape_without_a_new_rule` adds `typeset -x ANTHROPIC_API_KEY=literal` after the allowlist is fixed. It is a hard finding through the same occurrence search and unchanged regex, without a `typeset` branch, wrapper entry, parser rule or special fixture override. Its red result is recorded before the two-function replacement against `325f520b` where applicable, and its final-head result proves the new design handles the shape without a new rule. A pre-existing rejection is recorded honestly rather than labelled red.

7. Retained honest-form tests cover both credential names, each of the four forms, the exact optional `export ` prefix and a command-word suffix such as ` client` or ` client --flag`, with `DEPLOYED_KEY` or another non-credential identifier. All allowed forms pass. Credential-free ordinary names and shell text remain passing controls. Self-references to either credential name, quoted or decoded left-hand names, empty values, assignment templates, tab separators, shell operators and wrappers have explicit finding expectations under this reset. A command suffix cannot hide a second credential occurrence. Comment and Markdown-prose fixtures assert notes, code fixtures assert hard findings and `docs/` remains excluded. The retained real-entry fixture still proves `main()` registration, `home/` and `install/` coverage, `scripts/` exclusion, failed-listing refusal and symlink skipping. The parser fixtures retain malformed-byte, malformed-document, duplicate-key, alias and redaction coverage with verdicts updated to the fixed policy. Both platform template renderings remain exercised; an honest decoded assignment line passes exactly when it meets the same regex and no other raw or decoded view contains a hard finding.

8. The real applied-tree run calls `validate_anthropic_auth_route()` on the repository's own tracked `home/` and `install/` files and records its command, source head, output and exit 0. `make validate-agent-assets` is also green with main's current templates. Honest forms exercised through the templates pass the same allowlist. The run introduces no baseline, per-path waiver, scanner fallback or edit to an applied file to obtain green.

## Out of scope

The omp auth store probe, PR #404, any manifest change and any rendered settings change are outside this task. Changes to `SECRET_PATTERN`, its placeholder allowlist, workflow files and dependencies are outside this task. Live credential inspection and applying files to the user's home directory are outside this task.

## Check

`uv run python -m unittest tests/unit/test_validate_agent_assets.py -v` is green, and its output is pasted in `.orchestration/dotfiles-T129-anthropic-auth-route-check-followup-a05/validation.md`. The YAML parser cases run with the repository's existing PyYAML environment, and any dependency-related skip is identified.

`make validate-agent-assets` exits 0 on the continuing branch with main's current template, and its output and exit status are pasted in the same validation file. The table-driven corpus runs green on the final head with every bypass string from the three local reviews and the worker's corpus accounted for. The local-review reproductions retain their exact bytes and review provenance. Raw, structured-decoded, rendered-template, spelling-decoded and note-only cases are recorded separately, including both platform outputs, original Markdown line offsets and payload redaction. Item 8's real applied-tree auth run is green.

Tests are written before the scanner replacement. Red and green outputs identify their exact source revisions or isolated registration mutation. The new default-deny rejection rows are tried against unchanged `325f520bfc8b4dbb25e0744d27878cdf7eab2fd2` before implementation. A row already rejected there is recorded as a baseline pass, never as fabricated red evidence. The six a03 redesign tests, item 11's two a04 command-prefix tests and the two `b139995` regressions keep their historical red provenance; their retained behaviors and newly specified verdicts receive fresh final-head green results. The unseen-shape test passes with no shape-specific implementation change.

`ruff check scripts/validate-agent-assets.py tests/unit/test_validate_agent_assets.py` and `git diff --numstat origin/main...HEAD` are recorded. The diff contains at most 300 changed lines, added plus deleted, outside `tests/` and `.orchestration/`, and at most 1000 changed lines under `tests/`. Fixture lines count toward the test cap. `measure.md` records those totals and the changed-file inventory. Scanner deletion and reuse of existing decoders provide the smaller design; no validation or required corpus row is removed to fit. Bats tests are not run locally.

Inherited Ruff findings are recorded with their exit status and compared against the unchanged baseline at the original filenames. A failing command is not labelled passing, and this task adds no suppression or unrelated repair.

The orchestrator runs the format-2 task-consistency checker, including C1 to C10 and C7b, before dispatch and at acceptance. The first-push file inventory proves removal of the a04 task copy and addition of the byte-identical a05 copy. It contains no other predecessor task-copy change.

## Completion

One branch and one continuing implementation PR complete this task. PR #412 remains the main-target PR on `tools/anthropic-auth-route-structured`. PR #396 remains open as the stacked record until #412 merges. The first push contains the a04 task-copy deletion and the new a05 task copy. No second implementation PR or fresh branch is created for this reset.

The Completion clause of `.orchestration/tasks/dotfiles-T129-normalised-comparison-lint-a01.md` applies as written with `dotfiles-T129-anthropic-auth-route-check-followup-a06` as the owner of any advisory P2 and `task_copy=<sha256 of .orchestration/dotfiles-T129-anthropic-auth-route-check-followup-a05/task.md>` in the RESULT. This task's continuing branch, existing PR, round limit, default-deny policy and command restrictions govern the corresponding steps of that clause. The orchestrator writes the advisory owner's task before recording its first owned row.

The findings `local:a64daf1:1` through `local:a64daf1:4`, the a03 command-prefix P1, the a04 worker's `local:c15be6b9:1` through `local:c15be6b9:4` and `local:325f520:1` and `local:325f520:2` remain owned by this reset lineage. They are not deferred as advisory P2. The a04 local review's raw-comment, heredoc and Markdown-location findings receive explicit dispositions against this task's changed policy and final-head evidence. The security review's unmatched-glob and `builtin --` findings join the same corpus and receive their dispositions. Earlier advisory-owner text using this task's identifier is superseded by this class-stop reset. The a02, a03 and a04 acceptance histories and all their worker-side fix counts remain preserved. Every worker-side fix round counts toward INV-6, including a round before the first RESULT.

The worker performs at most one independent pre-push review and one consolidated worker-side fix round. Verification after that round records any surviving P0/P1 as open in the RESULT and stops the task for the orchestrator's decision. A surviving P0/P1 is never fixed a second time. Local findings are identified by their review evidence and finding identifier; Bot findings retain `open:<thread id>` or `open:review-<review id>` as applicable. This limit also governs findings discovered before the first push or RESULT. A third finding of one class stops rounds for a new orchestrator re-plan.

The RESULT names `pr=412`, the final head, base, branch, files, test names, cap totals, evidence paths and `task_copy=<sha256 of .orchestration/dotfiles-T129-anthropic-auth-route-check-followup-a05/task.md>`. It records each inherited and new finding with its fixing commit or proposed evidence-backed disposition and distinguishes policy changes from preserved historical fixes. It retains both `b139995` findings with their `a9056299` provenance and records the new separator verdict explicitly. It retains 4305965376 and 4305965379 with their fixing commits, identifies the template CI fix and surviving case regression, and retains the dispositions of 4302758230, 4302758234, 4302758239 and 4305863865. It names the table-driven corpus, the unseen-shape test, note behavior, retained honest forms and the real applied-tree run. An open P0/P1 remains explicitly open rather than being reported as fixed.

Evidence is written under `.orchestration/dotfiles-T129-anthropic-auth-route-check-followup-a05/` in the worker's worktree. A Codex seat uses those same relative paths and explicitly says so in its report and RESULT. The records distinguish inherited outputs from baseline `325f520b` observations and final-head checks. Worker-side review evidence uses the required `-worker-` infix and follows the repository's review-evidence and receipt gate rules. The report, validation, sandbox, learning, autoskill and measurement records state their actual status.

`security: true` requires the task-level audit and a separate security-profile review on the final head before integration. The orchestrator follows Orchestrator Playbook step 10 for feedback collection, audit dispositions, acceptance, the integration gate and merge. A changed head requires refreshed final-head evidence.

Git and gh writes run as single commands, without shell chaining or a wrapper combining writes. The worker posts no `@codex review` request and runs no `gh pr edit` or `gh pr comment`. CI and automatic reviews are awaited within the existing bounded window; an absent automatic Bot review is recorded as `bot: none` after that window. Thread replies and resolutions remain the orchestrator's responsibility.

Until P1-14 lands, any string containing the words `gh pr merge` or `gh pr create` is written with the file-edit tool, never in a Bash heredoc or `echo`. This restriction applies to task copies, reports and evidence text.

The redesign uses read-only repository evidence and claims no new implementation or green validation. Default denial deliberately rejects credential-bearing forms outside the fixed regex; a credential assembled from pieces that no retained decoder joins remains outside detection.

## Amendment 1 (rebase repair under D-024-24, 2026-10-19T06:0xZ; the withdrawal of 05:59Z is superseded)

The comparison lint of PR #415 (main 205fe85c) guards the files a pull request changes, and this PR changes scripts/validate-agent-assets.py: the required test job fails on `test_the_changed_files_are_clean_against_the_baseline` with R4 at lines 1626 and 1817 (run 39206429721). The repair touches only those two comparisons: one this task wrote is rewritten through the normaliser the rule names; one the task moved gets its baseline row (path, R4, sha256 of the normalized line) in scripts/lint-comparisons-baseline.tsv, which joins allowed_files for exactly that; the worker records which applied to each line with the lint output before and after. Nothing else changes; the revise-1 P1 fix stays. This is a rebase repair, labelled `round=rebase-repair-1`, and does not count against the C-61 cap (D-024-24). The audit and the security review run on the new head.

## Checks (pasted by the orchestrator before each send)

```
dotfiles-T129-anthropic-auth-route-check-followup-a05.md: OK
premises: copied from a04 verbatim (write-time outputs of 2026-10-18)
masked 0 match(es) in .orchestration/tasks/dotfiles-T129-anthropic-auth-route-check-followup-a05.md
```

Implementation tests and live CI are not run in this read-only redesign.
A credential assembled from pieces that no retained decoder joins remains undetectable.