---
format: 2
task_id: dotfiles-T133-pre-send-check-a03
reset_of: [dotfiles-T133-pre-send-check-a02]
retained_predecessor_directories: [.orchestration/dotfiles-T133-pre-send-check-a01/, .orchestration/dotfiles-T133-pre-send-check-a02/]
previous_sha256: fd2a5e96957e0eb628e009673762b1d15c44b06013a16c55bf9e76dae5e8750d
kind: code
security: false
allowed_files:
  - scripts/orchestrator/pre-send.sh
  - scripts/orchestrator/pre_send.py
  - tests/unit/test_pre_send.py
  - .orchestration/dotfiles-T133-pre-send-check-a03/**
after: []
threat_table:
  - control: the PR edits scripts/orchestrator/pre-send.sh
    disposition: "residual: entrypoint fixtures detect startup mistakes; executable replacement by the same UID remains possible; owner: dotfiles-T133-pre-send-check-followup-a01"
  - control: the PR edits scripts/orchestrator/pre_send.py
    disposition: "closed: tests/unit/test_pre_send.py::PreSendTest::test_all_refusals_are_reported"
  - control: the PR edits tests/unit/test_pre_send.py
    disposition: "residual: real-entrypoint fixtures retain the existing assertions; final-head CI and the independent audit check their claims; owner: dotfiles-T133-pre-send-check-followup-a01"
  - control: the PR adds .orchestration/dotfiles-T133-pre-send-check-a03/** as data only
    disposition: "residual: the final-head audit compares these artifacts with the diff, commands and CI; owner: dotfiles-T133-pre-send-check-followup-a01"
  - control: workflow and interpreter or environment inputs; env -i re-exec
    disposition: "residual: test_entrypoint_fixed_environment exercises minimal and decoy PATH through the real entrypoint; same-UID executable/cache mutation remains possible; owner: dotfiles-T133-pre-send-check-followup-a01"
  - control: output contract on both streams
    disposition: "closed: tests/unit/test_pre_send.py::PreSendTest::test_output_is_labels_and_numbers_only"
  - control: single-buffer digest, including failure after validation
    disposition: "closed: tests/unit/test_pre_send.py::PreSendTest::test_digest_survives_replacement_and_helper_failure"
  - control: task metadata
    disposition: "residual: the consistency checker parses the mapping before dispatch and acceptance; task-copy comparison covers changes; owner: dotfiles-T133-pre-send-check-followup-a01"
  - control: metadata separators
    disposition: "residual: YAML marks and normalized line boundaries drive parsing; comparison covers the whole task copy; owner: dotfiles-T133-pre-send-check-followup-a01"
  - control: in-process effects
    disposition: "closed: tests/unit/test_pre_send.py::PreSendTest::test_fenced_bash_syntax"
  - control: new or renamed scripts
    disposition: "residual: only pre_send.py is added; syntax, lint and final-head audit cover the declared implementation; owner: dotfiles-T133-pre-send-check-followup-a01"
  - control: orchestrator effect task copy; .orchestration/dotfiles-T133-pre-send-check-a03/task.md; inherited .orchestration/dotfiles-T133-pre-send-check-a02/task.md and .orchestration/dotfiles-T133-pre-send-check-a01/task.md remain read-only
    disposition: "residual: compare the a03 copy byte-for-byte and by SHA256 with the anchored dispatched text at acceptance; owner: dotfiles-T133-pre-send-check-followup-a01"
  - control: orchestrator effect records
    disposition: "residual: the orchestrator owns acceptance, feedback dispositions and reset records; the worker supplies evidence only; owner: dotfiles-T133-pre-send-check-followup-a01"
  - control: orchestrator effect merge
    disposition: "residual: only the orchestrator integrates the audited head through Orchestrator Playbook step 10; owner: dotfiles-T133-pre-send-check-followup-a01"
  - control: orchestrator effect update-branch
    disposition: "residual: a moved head requires fresh CI, feedback sweep, audit and gate under step 10; owner: dotfiles-T133-pre-send-check-followup-a01"
  - control: orchestrator effect forced worker removal
    disposition: "residual: none planned; any discarded state is recorded by the orchestrator at acceptance; owner: dotfiles-T133-pre-send-check-followup-a01"
premises: []
---

# AGMSG-TASK dotfiles-T133-pre-send-check-a03 — replace echoed-output parsing with Python

[memory:decision] D-024-56 executes the consequence fixed by D-024-51: reset a02 after round-2 audit of PR #442 head 1d72f16978018c3d016bbc239d79d3d7d0675105. The six P2 repeat round-1 classes: argument-injection-bypass, fence-forms, heading-form-gap, digest-toctou, inherited-environment and diagnostic-redaction. Argument-injection-bypass has its third row; the binding S1 re-plan is in .orchestration/acceptance/dotfiles-T133-pre-send-check-a02.md. Two rounds of Bash regex parsing of echoed checker output failed; change the design rather than extending that parser.

Design 5.14 in .orchestration/plans/024-design-quality.md applies by reference: items 0, 2, 4, 6, 9 and 10 (D-024-30). This security:false mistake detector gets no C-80 (D-024-46). The orchestrator names a different Claude context from a008 in TASK, using the standard profile; a008 does not implement a03.

## Item 1

Continue tools/pre-send-check-a01 and PR #442 from the head above, retaining all a01/a02 history and the 28 existing tests. Keep the two-parent root lookup and exactly one task-file argument; never edit the input or execute its prose.

- Make pre-send.sh only the entrypoint: design 5.14 item 2, unconditional clean-environment re-exec, then exec the pinned isolated Python through absolute uv with no-config, no-project and offline PyYAML. It forwards only the exit status and never constructs diagnostics from task, checker or tool text. Retain a startup form that suppresses inherited BASH_ENV before it can run, and English shdoc @file, @brief, @description, @arg and @exitcode comments.
- Add pre_send.py. Read the original file once as bytes; every check and SHA256 use that buffer. Normalize CRLF and lone CR in the derived text before parsing, keeping the raw buffer for the digest and wc-style newline count. Never reopen the original path, including any helper-failure fallback (audit:1d72f16:4).
- Parse front matter with PyYAML; read task_id, kind, security and allowed_files from its mapping. Locations come only from parser-computed YAML marks, fence openings or heading indexes, never task-supplied digit runs or checker output (audit:1d72f16:1). Run task-consistency-check.py as a subprocess with --root and the option terminator; consume only its exit status, suppressing both streams. It may read a byte-identical temporary snapshot with the original filename semantics.
- Use one CommonMark fence state machine for task and owner-record structure: backticks or tildes of length at least three, up to three leading spaces, same-character closers at least as long, EOF closure, and bash/sh chosen by the first info-string word. Count headings, Items and owner sections only outside fences. Check every selected shell block with /bin/bash -n on a temporary file under TMPDIR; report its opening line with the fixed bash-syntax label (audit:1d72f16:2,3).
- Preserve every a02 rule: validator SECRET_PATTERN extracted by ast without importing the validator, complete-text/multiline matching and line locations; literal homes including a bare home name; both self-cap spellings with wc -l semantics, equality and absent-cap acceptance; owner work in the named repository-relative record's exact section. End that section at every CommonMark level-two heading; require a nonempty id-tab-class row or bullet when at most one real Item exists, allow an empty existing section with more Items, and always refuse missing records/sections.
- Run all applicable checks despite refusals; exit 0 only when all pass. Both streams admit only fixed `<check>: refused` labels with optional ` line(s) a,b`, the fixed `preflight: helper failed (exit 1)`, and `sha256: <64 lowercase hex>`. For every successfully read buffer, print its digest last on stdout, including refusals and later failures. Argument/read failures use input: refused; temp creation, interpreter/dependency, YAML and other failure paths use their own fixed labels and exit 1. Never print excerpts, paths, tool errors or tracebacks (audit:1d72f16:6).

## Item 2

Keep unittest, TemporaryDirectory and unittest.main(), fixture repositories and real offline entrypoint/checker execution; do not edit live records. Add pre_send.py and the pinned mise/uv paths to fixture setup; legacy-head red runs must work without the new module. Preserve all 28 tests and their red/green provenance. Extend test_output_is_labels_and_numbers_only to both streams and assert that no contiguous eight-character substring of the constructed task-text lines, secret fixture or checker output appears; build refused values and diagnostic markers from fragments.

Before production edits, add these six behavioral regressions against production head 1d72f16978018c3d016bbc239d79d3d7d0675105; commit the red fixtures, then the fix. Each must fail its named behavioral assertion on that head and pass after the fix; missing tooling, a missing new module or harness failure never qualifies as red.

- test_multiline_task_id_has_parser_locations: multiline YAML task_id injects a fake location with a ten-digit run; only actual parser-computed locations may appear (argument-injection-bypass, audit:1d72f16:1).
- test_crlf_tilde_closer: CRLF text closes a non-shell tilde fence before an invalid shell fence; require bash-syntax refusal. Also cover CRLF owner front matter and lone CR (fence-forms, audit:1d72f16:2).
- test_fenced_item_does_not_supply_owner_work: a fenced `## Item` example beside one real Item cannot satisfy an empty owner section (heading-form-gap, audit:1d72f16:3).
- test_digest_survives_replacement_and_helper_failure: replace the original pathname after validation, then force the later helper failure; assert the final digest equals hashlib's hash of the original buffer, never the replacement (digest-toctou, audit:1d72f16:4).
- test_entrypoint_fixed_environment: spawn the real entrypoint under `env -i PATH=/usr/bin:/bin` and a decoy inherited PATH, with required HOME/TMPDIR supplied; both locate pinned uv/Python and discard inherited PATH. Assert the decoy never runs; retain the inherited BASH_ENV fixture (inherited-environment, audit:1d72f16:5).
- test_temp_failure_is_redacted: non-writable TMPDIR triggers the audited heredoc/temp failure; assert exit 1, a fixed refusal and no raw diagnostics or eight-character fixture fragments on either stream (diagnostic-redaction, audit:1d72f16:6).
- test_missing_front_matter_or_bom_is_refused: a text without the opening `---` and a text with a UTF-8 BOM both end in a fixed `front-matter: refused`, never a silent empty mapping; the owner check does not skip a missing owner record (audit:a30a43b:1).
- test_setext_heading_ends_the_owner_section: a setext level-two heading (`Title` over `---`) closes the owner section, so a bullet under it is not owner work (audit:a30a43b:2).
- test_itemized_heading_is_not_an_item: `## Itemized background` does not count as an Item; only `## Item <n>` headings do (audit:a30a43b:3).
- test_whitespace_bullet_is_not_work: an owner section whose only bullet is `- ` followed by whitespace is empty (audit:a30a43b:4).
- test_startup_exit_one_is_named: a startup subprocess exiting 1 produces the fixed `preflight: helper failed (exit 1)` on stdout and nothing else on either stream (audit:a30a43b:5).
- test_private_cache_required: the entrypoint under `env -i` without UV_CACHE_DIR, or with UV_CACHE_DIR naming a file, prints `refused: UV_CACHE_DIR absent` and exits 1; with a private directory it proceeds (design 5.14 item 9).

## Check

Worker Playbook step 4 applies: every command stays sandboxed, including HTTPS push; record any denial in sandbox.md and send AGMSG-PONG v1 status=blocked with the exact command and boundary, never retry outside. Each evidence item names its producer and seat kind: worker (Claude seat), or orchestrator (Claude seat, sandboxed Bash); the authoring measurements below are worker (Codex seat), read-only.

Host facts (orchestrator measurement, repeated in Checks): mise is `$HOME/.local/bin/mise`; Python is `$HOME/.local/share/mise/installs/python/3.15.0/bin/python3`. Resolve uv once with `/usr/bin/env -i PATH=/usr/bin:/bin HOME="$HOME" "$HOME/.local/bin/mise" which uv`; paste its actual absolute output in validation.md as uv_path, never guess a version, add a bin subdirectory or invent a pin file. Author-probed absolute fallback: `$HOME/.local/share/mise/installs/uv/0.13.1/uv-aarch64-apple-darwin/uv` (expand HOME); if neither resolution nor that executable is available, use a fixed startup refusal. No PATH search fallback.

The fixed entrypoint PATH is uv_path's directory plus /usr/bin:/bin, HOME and TMPDIR are worker values, UV_CACHE_DIR is an explicit private cache directory (design 5.14 item 9: the entrypoint refuses with the fixed label `refused: UV_CACHE_DIR absent` when the variable is unset or names a non-directory, and never falls back to the shared default cache), and LANG=C.UTF-8; clear every inherited variable outside that set. Run `/usr/bin/env -i PATH="$(dirname "$uv_path"):/usr/bin:/bin" HOME="$HOME" TMPDIR="$TMPDIR" UV_CACHE_DIR="$TMPDIR/uv-cache" LANG=C.UTF-8 "$HOME/.local/share/mise/installs/python/3.15.0/bin/python3" -I tests/unit/test_pre_send.py`.

Run `bash -n scripts/orchestrator/pre-send.sh`, `shellcheck -x scripts/orchestrator/pre-send.sh` and `shfmt -i 4 -sr -d scripts/orchestrator/pre-send.sh`. Run `ruff check --config ruff.toml scripts/orchestrator/pre_send.py tests/unit/test_pre_send.py` and `ruff format --config ruff.toml --check scripts/orchestrator/pre_send.py tests/unit/test_pre_send.py`. Python syntax is covered by real execution; shell syntax/lint applies to the shell file. Never run Bats locally.

Caps: at most 360 changed lines outside `tests/` and `.orchestration/`, and at most 480 under `tests/`.
Measure additions plus deletions with `git diff --numstat <merge-base> <head>`, where head is RESULT's final 40-hex commit and merge-base is `git merge-base origin/main <head>` at RESULT time (C-123).
Author measurement: head 1d72f16978018c3d016bbc239d79d3d7d0675105, merge-base e00de4e0e4158de19e2c8921e572461e7e9e4ca0, totals 104 implementation / 260 tests; caps leave 256 / 220 lines for the redesign. Current-line blame attribution a01/a02 is 26/78 implementation and 126/134 tests; distinguish this from change churn. At RESULT remeasure the full cumulative diff, separately attribute inherited a01/a02 and a03 work, and report both commits, caps and totals; never reset accounting to a03 alone.

Paste every executed validation command, exit status and verbatim redacted output into validation.md, with producer (summaries are not evidence; the `gh pr checks --watch` output and the bounded Bot-wait observation are pasted too); every claimed commit/PR identifier must appear there. Record a six-row class/attack/selector/red-sha/green-sha table and preserved 28-test results, before and after implementation. Red evidence names the production baseline and red-fixture commit; green evidence names the fix commit.

After each push inspect final-head Actions with `gh pr checks 442 --repo mryfmo/dotfiles --watch`; fix in-scope failures and repeat. Follow Worker Playbook step 15's bounded Bot wait and at most one worker Bot fix-round. Before RESULT run make require-crit-review; if required, follow AGENTS.md's crit-data JSON/receipt procedure, using -worker- evidence names in the a03 directory, never a browser review.

Keep this whole dispatched text at or under **150 lines**, including the seven-line Checks section below. The orchestrator fills Checks before anchor review; dispatch the anchored bytes unchanged, without a later paste.

## Completion

Write only the four allowed entries. Leave predecessor directories read-only; do not edit dispatch.sh, checker, validator, workflows, untracked glue, owner task or acceptance record, and add no dependency or caller change. Advisory work already owned by dotfiles-T133-pre-send-check-followup-a01 stays there; the six reset regressions above belong to a03.

Under .orchestration/dotfiles-T133-pre-send-check-a03/ save task.md byte-identical to the dispatched text, report.md (implementation, fixtures, residuals, cost), validation.md, sandbox.md, learning.md and autoskill.md (used/not-used). Keep plan/todo/learn worklogs uncommitted. Save result.txt as Worker Playbook requires; include plan-mode-used if applicable.

Push inside the sandbox, without -u: `GIT_CONFIG_GLOBAL=/dev/null git -c credential.helper= -c 'credential.helper=!gh auth git-credential' push https://github.com/mryfmo/dotfiles.git tools/pre-send-check-a01`. Rewrite PR #442's English title/body for the final a03 design, actual test count and cumulative cap totals before RESULT (audit:1d72f16:8).

Once exact-head CI passes and the bounded Bot wait completes, send AGMSG-RESULT v1 task_id=dotfiles-T133-pre-send-check-a03 status=ready_for_review with pr, head, merge_base, both numeric caps, changed_non_tests, changed_tests, inherited attribution, six red/green SHAs, task_copy SHA256 and all artifact paths. No worker merge; orchestration feedback/acceptance changes remain orchestrator-owned.

## Amendment 1 (2026-10-21T22:13Z; D-024-66)

The round-1 audit of a30a43ba found nine P2 and no P1. Round 2 fixes the five implementation rows (the six fixtures added to Item 2 above, red at a30a43ba on their behavioural assertion and green at the fix commit), restores design 5.14 item 9 in the entrypoint contract (an explicit private UV_CACHE_DIR with a fixed refusal when absent; the a03 round-1 contract had dropped the variable, an orchestrator error), and makes validation.md verbatim. The sandbox-exception and record-placement rows are the orchestrator's and are dispositioned in the acceptance record.

## Checks

```text
measurement_base=e00de4e0e4158de19e2c8921e572461e7e9e4ca0 = git merge-base origin/main 1d72f169; origin/main=e00de4e0e4158de19e2c8921e572461e7e9e4ca0; observed 2026-10-21T07:23Z by the orchestrator (Claude seat, sandboxed Bash)
git diff --numstat e00de4e0 1d72f169, additions plus deletions: 104/260 (outside tests/ and .orchestration/ / under tests/) = the inherited a01+a02 lines the caps 360/480 include
env -i PATH=/usr/bin:/bin HOME="$HOME" "$HOME/.local/bin/mise" which uv -> $HOME/.local/share/mise/installs/uv/latest/uv-aarch64-apple-darwin/uv; $HOME/.local/share/mise/installs/python/3.15.0/bin/python3 exists
```
