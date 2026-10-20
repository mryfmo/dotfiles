---
format: 2
task_id: dotfiles-T129-anthropic-auth-route-check-followup-a02
kind: code
security: true
allowed_files:
  - scripts/validate-agent-assets.py
  - tests/unit/test_validate_agent_assets.py
  - .orchestration/dotfiles-T129-anthropic-auth-route-check-followup-a02/**
after: []
reset_of: [dotfiles-T129-anthropic-auth-route-check-followup-a01]
threat_table:
  - control: "scripts/validate-agent-assets.py (the Anthropic credential check and its registration in main)"
    disposition: "closed: tests/unit/test_validate_agent_assets.py::test_anthropic_auth_route_refuses_an_oauth_token_in_applied_files_and_a_literal_api_key_assignment"
  - control: "tests/unit/test_validate_agent_assets.py (parser, decoding, shell-name, template-rendering and real-entry fixtures)"
    disposition: "residual: temporary fixture repositories exercise real file discovery and credential validation; registration mutation proves that the entry test fails when main omits the check"
  - control: "the branch evidence records under .orchestration/dotfiles-T129-anthropic-auth-route-check-followup-a02/** (report.md, validation.md, sandbox.md, learning.md and worker review evidence)"
    disposition: "residual: records separate inherited evidence from new results, omit credentials and machine-specific home paths, and bind red and green outputs to their source revisions for the final audit"
  - control: "the task-file copy on the branch .orchestration/dotfiles-T129-anthropic-auth-route-check-followup-a02/task.md replaces .orchestration/dotfiles-T129-anthropic-auth-route-check-followup-a01/task.md in the next push"
    disposition: "residual: the orchestrator owns predecessor-copy removal; the new copy is byte-identical to the dispatched a02 text, and its own sha256 is compared with the TASK and RESULT at acceptance"
  - control: "applied-file inputs under home/ and install/ (structured documents, chezmoi template sources and shell text controlled by the PR)"
    disposition: "residual: tracked regular files are read without executing their contents or following symlinks; structured decoding, rendering and parsing failures refuse validation, and diagnostics omit values and escape key paths"
  - control: task metadata
    disposition: "residual: the dispatched file passes task-consistency checks C1 to C10 and C7b before dispatch and acceptance; whole-file byte comparison binds the branch copy to that file"
  - control: metadata separators
    disposition: "residual: the first YAML document supplies front matter, and whole-file byte comparison covers its separators and the task body"
  - control: in-process effects
    disposition: "residual: parsers and the existing template renderer inspect data without executing applied scripts; fixture tests use temporary roots and leave the live home directory untouched"
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

# AGMSG-TASK dotfiles-T129-anthropic-auth-route-check-followup-a02 — INV-6 (S2) reset of dotfiles-T129-anthropic-auth-route-check-followup-a01

This redesign is written by a review-profile context other than a01's author under plan 006 INV-6 (S2). Three amendments and the surviving shell-name P1 stopped a01. The orchestrator records a01 as reset by this task before dispatch and retains its acceptance history and round counts.

PR #412 continues against `main` on the same branch, `tools/anthropic-auth-route-structured`, under this task. The next push replaces `.orchestration/dotfiles-T129-anthropic-auth-route-check-followup-a01/task.md` with this text's byte-identical copy at `.orchestration/dotfiles-T129-anthropic-auth-route-check-followup-a02/task.md`. The orchestrator owns predecessor-copy removal as reset bookkeeping. The worker's edit boundary remains `allowed_files`.

PR #396 stays open as the stacked record until #412 merges. PR #389 is superseded and supplies no merge precondition. Existing lineage evidence remains historical evidence.

The a010 handoff records an uncommitted amendment-3 WIP with one failure among 108 tests and no approved current receipt. Its surviving case is a dynamic export hidden after a `case` pattern's closing parenthesis. The saved CI failure identifies `home/.chezmoitemplates/claude-settings-managed.json` as template text incorrectly parsed as raw JSON. The WIP supplies implementation material and red evidence; it does not establish completion.

## Goal

The Anthropic credential check reads JSON, TOML and YAML sources through their parsers, renders chezmoi template sources before parsing, and keeps a fail-closed line grammar for shell text. Decoded keys and values cannot hide the OAuth token name or a literal API-key assignment through quoting, escaping, delimiters or line breaks. Every open finding has a named regression test with red and green evidence.

## Files

1. `scripts/validate-agent-assets.py` retains `validate_anthropic_auth_route()` in the validator's real `main()` entry beside `validate_no_obvious_secrets()`. The check discovers tracked files through `git ls-files -z -- home install`, refuses a failed listing, and does not follow tracked symlinks. R1 refuses occurrences of `ANTHROPIC_OAUTH_TOKEN` in applied text and decoded structured content. R2 permits an API-key value only when its whole value is one environment reference, one template expression or empty. Shell references pass bare or double-quoted; single-quoted references are literal text and are refused. Suffixes, fallback expansions, command substitutions and concatenated values remain refused. `tests/unit/test_validate_agent_assets.py::test_anthropic_auth_route_r2_accepts_only_a_whole_value_reference_template_or_empty`, `tests/unit/test_validate_agent_assets.py::test_anthropic_auth_route_reads_a_comment_after_an_empty_value_as_empty`, `tests/unit/test_validate_agent_assets.py::test_anthropic_auth_route_r2_reaches_a_quoted_key_and_a_compound_assignment` and `tests/unit/test_validate_agent_assets.py::test_anthropic_auth_route_refuses_a_single_quoted_reference_in_text` retain these cases.

2. `applied_file_format` decides the format after stripping chezmoi attribute prefixes from the basename. `modify_`, `run_`, `symlink_`, `encrypted_` and `.tmpl` sources remain script text under the line grammar. Every other `.json`, `.toml`, `.yaml` or `.yml` source uses `json.loads`, `tomllib` or the validator's existing YAML reader. Every decoded key path and string value is inspected. Duplicate mapping entries remain visible, and YAML aliases cannot multiply traversal. A structured parse failure is a refusal naming the source. `tests/unit/test_validate_agent_assets.py::test_anthropic_auth_route_reads_json_and_toml_through_their_parsers` and `tests/unit/test_validate_agent_assets.py::test_anthropic_auth_route_reads_yaml_through_its_parser` cover escaped JSON and TOML keys, quoted YAML keys, nested mappings, multiline values, duplicate keys, invalid documents and allowed references. Their fixtures also cover attribute-prefixed structured sources and the script-text classifications. `tests/unit/test_validate_agent_assets.py::test_anthropic_auth_route_reads_a_json_reference_before_a_delimiter` preserves the pass case for a JSON reference followed by a comma or closing brace. These cases retain the fixes for 4302758230, 4302758234 and 4302758239.

3. Structured sources are decoded as strict UTF-8 before parsing or template rendering. Malformed bytes cause a refusal with the source name and a fixed error type; diagnostics contain neither malformed content nor credential values. Script-text decoding retains its existing behavior. `tests/unit/test_validate_agent_assets.py::test_anthropic_auth_route_check_refuses_malformed_utf8_in_a_structured_source` covers malformed bytes in JSON, TOML and YAML and the unchanged text cases. The a01 red evidence for 4305863865 remains identified by its source revision, and the test is green on the final head.

4. The `escaped-name-bypass` finding 4305965376 and the surviving a010 case are fixed in the shell-text line grammar. The grammar normalises the name token by removing quotes and backslashes before matching, so `"ANTHROPIC_API_KEY"=`, `'ANTHROPIC_API_KEY'=` and `ANTHROPIC_API_\KEY=` name the same variable. Value quoting remains intact. An assignment whose name token carries `$`, a backtick or a parameter expansion is refused as an unreadable name. A case-pattern or another construct that prevents the grammar from reading an assignment also causes refusal. A case-pattern closing parenthesis never hides the following export. `tests/unit/test_validate_agent_assets.py::test_anthropic_auth_route_normalizes_shell_names_and_refuses_unreadable_names` covers each quoted and escaped form, dynamic names, parameter expansions, backticks, command substitutions and line continuations. Its red cases include `  ANTHROPIC_*) export "$name"=literal-value ;;`, whitespace and quoting variants, a complete multiline `case`, and the saved failing form `out="$(case x in x) export "$NAME"=literal-value ;; esac)"`. The same test preserves pass cases for readable names with allowed values, ordinary parameter expansions in values, and single-line and multiline quoted awk programs. The original name bypasses are red against the committed head, the surviving case is red against the a010 WIP, and every case is green after the fix.

5. The `test-calls-helper-only` finding 4305965379 is fixed by replacing the parent row's helper-only registration test. `tests/unit/test_validate_agent_assets.py::test_anthropic_auth_route_refuses_an_oauth_token_in_applied_files_and_a_literal_api_key_assignment` calls the real `main()` entry used by `make validate-agent-assets` on a temporary fixture tree. The Anthropic check and Git file discovery remain real while unrelated validators are isolated. The test asserts OAuth and literal-key refusals under `home/` and `install/`, allowed-reference passes, and the exclusion of the same OAuth text under `scripts/`. Refusals identify the fixture and auth rule, and pass cases complete successfully. A temporary source copy with only the Anthropic registration removed from `main()` supplies the red proof; the registered entry supplies the green proof. The helper-only version is replaced rather than retained beside the entry test.

6. The `template-classified-as-data` CI failure is fixed by reusing `render_template_text(path, os_name)`. A structured-format source under `home/.chezmoitemplates/` whose text contains `{{` is rendered for `darwin` and `linux` before parsing. Each rendering is parsed and checked as the format selected from its source name. A rendering that fails to parse is a refusal. The renderer's existing default and callers retain their behavior. `tests/unit/test_validate_agent_assets.py::test_anthropic_auth_route_parses_both_platform_renderings_of_chezmoi_templates` uses a fixture containing an `if eq .chezmoi.os` block. It passes when both branches contain allowed references, refuses a literal credential in either branch, and refuses malformed structured output from either rendering. The fixture is red against the uncorrected committed head and green after the fix. `make validate-agent-assets` also passes on the continuing branch with main's current managed template.

Diagnostics preserve the existing protection against credential disclosure and forged log lines. Literal values and parser exception messages are omitted, and decoded key paths are escaped. Existing parser, duplicate-key, alias, placeholder and secret-scan coverage remains green.

## Out of scope

The omp auth store probe, PR #404, any manifest change and any rendered settings change are outside this task. Changes to `SECRET_PATTERN`, its placeholder allowlist, workflow files and dependencies are outside this task. Live credential inspection and applying files to the user's home directory are outside this task.

## Check

`uv run python -m unittest tests/unit/test_validate_agent_assets.py -v` is green, and its output is pasted in `.orchestration/dotfiles-T129-anthropic-auth-route-check-followup-a02/validation.md`. The YAML parser cases run with the repository's existing PyYAML environment, and any dependency-related skip is identified.

`make validate-agent-assets` exits 0 on the continuing branch with main's current template, and its output and exit status are pasted in the same validation file. The red and green outputs for items 4, 5 and 6 identify their exact source revisions or isolated registration mutation.

`ruff check scripts/validate-agent-assets.py tests/unit/test_validate_agent_assets.py` and `git diff --numstat origin/main...HEAD` are recorded. The diff contains at most 300 changed lines, added plus deleted, outside `tests/` and `.orchestration/`, and at most 1000 changed lines under `tests/`. Fixture lines count toward the test cap. Bats tests are not run locally.

## Completion

One branch and one continuing implementation PR complete this task. PR #412 remains the main-target PR on `tools/anthropic-auth-route-structured`. PR #396 remains open as the stacked record until #412 merges.

The Completion clause of `.orchestration/tasks/dotfiles-T129-normalised-comparison-lint-a01.md` applies as written with `dotfiles-T129-anthropic-auth-route-check-followup-a03` as the owner of any advisory P2 and `task_copy=<sha256 of .orchestration/dotfiles-T129-anthropic-auth-route-check-followup-a02/task.md>` in the RESULT. This task's continuing branch, existing PR and command restrictions govern the corresponding steps of that clause. The orchestrator writes the advisory owner's task before recording its first owned row.

The RESULT names `pr=412`, the final head, base, branch, files, test names, cap totals, evidence paths and the a02 task-copy hash. It records 4305965376 and 4305965379 with their fixing commits, identifies the template CI fix and surviving case regression, and retains the disposition of 4305863865.

Evidence is written under `.orchestration/dotfiles-T129-anthropic-auth-route-check-followup-a02/` in the worker's worktree. A Codex seat uses those same relative paths and explicitly says so in its report and RESULT. The records distinguish inherited outputs from checks run on the final head.

`security: true` requires the task-level audit and security review on the final head before integration. The orchestrator follows Orchestrator Playbook step 10 for feedback collection, audit dispositions, acceptance, the integration gate and merge. A changed head requires refreshed final-head evidence.

Git and gh writes run as single commands. The worker posts no `@codex review` request and runs no `gh pr edit` or `gh pr comment`. CI and automatic reviews are awaited within the existing bounded window; an absent automatic Bot review is recorded as `bot: none` after that window. Thread replies and resolutions remain the orchestrator's responsibility.

The redesign uses read-only repository evidence and claims no new implementation or green validation. The surviving shell case remains blocking until the worker supplies green final-head evidence.

## Checks (pasted by the orchestrator before each send)

```
dotfiles-T129-anthropic-auth-route-check-followup-a02.md: OK
premises 1 to 4: re-run by the orchestrator at dispatch (2026-10-18 16:1x JST), outputs equal
redesigned by the codex review profile (headless, read-only) at 2026-10-18T07:12Z as the INV-6 reset of a01; checked and dispatched by the orchestrator
```
