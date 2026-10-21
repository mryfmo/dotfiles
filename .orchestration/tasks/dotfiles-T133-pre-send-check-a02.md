---
format: 2
task_id: dotfiles-T133-pre-send-check-a02
reset_of: [dotfiles-T133-pre-send-check-a01]
retained_predecessor_directories: [.orchestration/dotfiles-T133-pre-send-check-a01/]
previous_sha256: 438089b8b9eb46db347e724913c1d4070d575df5091e3ea4a7e1d4b46412bf95
kind: code
security: false
allowed_files:
  - scripts/orchestrator/pre-send.sh
  - tests/unit/test_pre_send.py
  - .orchestration/dotfiles-T133-pre-send-check-a02/**
after: []
threat_table:
  - control: the PR edits scripts/orchestrator/pre-send.sh
    disposition: "closed: tests/unit/test_pre_send.py::PreSendTest::test_all_refusals_are_reported"
  - control: the PR edits tests/unit/test_pre_send.py
    disposition: "residual: temporary fixtures exercise the real preflight and checker; final-head CI and the task-level audit verify the assertions; owner: dotfiles-T133-pre-send-check-a02"
  - control: the task-file copy (.orchestration/dotfiles-T133-pre-send-check-a02/task.md); predecessor .orchestration/dotfiles-T133-pre-send-check-a01/task.md is inherited read-only
    disposition: "residual: byte-identical to the dispatched text; the orchestrator compares its SHA256 with the TASK line at acceptance; owner: dotfiles-T133-pre-send-check-a02"
  - control: the evidence records under .orchestration/dotfiles-T133-pre-send-check-a02/** (report.md, validation.md, sandbox.md, learning.md, autoskill.md)
    disposition: "residual: records contain command output and learning triage; sandbox.md lists refused commands, and the audit checks claims against the final head; owner: dotfiles-T133-pre-send-check-a02"
  - control: task metadata (kind, security, allowed_files, after, reset_of, retained_predecessor_directories, previous_sha256, threat_table, premises)
    disposition: "residual: the consistency checker reads the front matter before dispatch and at acceptance; byte comparison detects a changed task copy; owner: dotfiles-T133-pre-send-check-a02"
  - control: metadata separators (the --- boundaries in the task copy and evidence records)
    disposition: "residual: front matter remains YAML; the checker parses the task and byte comparison covers the entire dispatched file; owner: dotfiles-T133-pre-send-check-a02"
  - control: in-process effects
    disposition: "closed: tests/unit/test_pre_send.py::PreSendTest::test_fenced_bash_syntax"
  - control: workflow and interpreter or environment inputs
    disposition: "residual: no workflow or interpreter file changes; isolated Python and no-config offline uv use the pinned interpreter, while same-UID cache mutation remains possible; owner: dotfiles-T133-pre-send-check-a02"
  - control: new or renamed scripts
    disposition: "residual: the sole new script is scripts/orchestrator/pre-send.sh; shdoc, shellcheck and shfmt cover it, and no other script is added or renamed; owner: dotfiles-T133-pre-send-check-a02"
  - control: orchestrator effect merge
    disposition: "residual: gh pr merge --squash --match-head-commit <audited head> follows the gate under Orchestrator Playbook step 10; no local merge or push to main; owner: dotfiles-T133-pre-send-check-a02"
  - control: orchestrator effect update-branch
    disposition: "residual: gh pr update-branch changes the head, requiring fresh final-head CI, feedback sweep and audit before the gate under Orchestrator Playbook step 10; owner: dotfiles-T133-pre-send-check-a02"
  - control: orchestrator effect forced worker removal
    disposition: "residual: none planned; herdr-agents --remove-worker refuses a dirty tree without --force, and any forced removal records discarded state in acceptance; owner: dotfiles-T133-pre-send-check-a02"
  - control: fixed refusal labels and line numbers without task-derived or checker-derived text
    disposition: "closed: tests/unit/test_pre_send.py::PreSendTest::test_output_is_labels_and_numbers_only"
  - control: malformed front matter whose checker excerpts contain secret fragments
    disposition: "closed: tests/unit/test_pre_send.py::PreSendTest::test_checker_diagnostics_never_echo_secret_fragments"
  - control: checker exit status and structured-location numeric line extraction without echoing either captured stream
    disposition: "closed: tests/unit/test_pre_send.py::PreSendTest::test_checker_exit_and_line_numbers_only"
  - control: SECRET_PATTERN matches across the complete task text
    disposition: "closed: tests/unit/test_pre_send.py::PreSendTest::test_secret_spanning_two_lines"
  - control: complete Markdown fence parsing before bash or sh selection
    disposition: "closed: tests/unit/test_pre_send.py::PreSendTest::test_complete_fences_before_shell_selection"
  - control: task_id obtained from parsed YAML front matter
    disposition: "closed: tests/unit/test_pre_send.py::PreSendTest::test_task_id_yaml_comment"
  - control: checker task operand follows the option terminator
    disposition: "closed: tests/unit/test_pre_send.py::PreSendTest::test_checker_option_terminator"
  - control: free-text digits cannot become checker location numbers
    disposition: "closed: tests/unit/test_pre_send.py::PreSendTest::test_checker_structured_locations_only"
  - control: every CommonMark level-two heading ends an owner section
    disposition: "closed: tests/unit/test_pre_send.py::PreSendTest::test_owner_commonmark_boundaries"
  - control: helper exit 1 with empty stdout cannot yield only a digest
    disposition: "closed: tests/unit/test_pre_send.py::PreSendTest::test_helper_exit_one_empty_stdout"
  - control: validation and digest consume the same once-read bytes
    disposition: "closed: tests/unit/test_pre_send.py::PreSendTest::test_digest_uses_validated_buffer"
  - control: cleared entrypoint environment suppresses inherited BASH_ENV
    disposition: "closed: tests/unit/test_pre_send.py::PreSendTest::test_entrypoint_clears_bash_env"
  - control: deferred advisory rows in the a02 acceptance record
    disposition: "out-of-scope: dotfiles-T133-pre-send-check-followup-a01"
premises:
  - claim: "Historical a01 pre-promotion observation, re-pasted: the local glue has 39 lines, both target files are absent, and the checker and validator already exist; promotion needs no dependency or caller change."
    producer: "orchestrator (Claude seat, sandboxed Bash); historical a01 evidence re-pasted"
    command: |-
      python3 -I -c 'from pathlib import Path; p=Path(".agents/worklog/orchestrator-glue/pre-send.sh"); print("glue lines:", len(p.read_bytes().splitlines())); print("new paths absent:", all(not Path(x).exists() for x in ("scripts/orchestrator/pre-send.sh", "tests/unit/test_pre_send.py"))); print("dependencies present:", all(Path(x).is_file() for x in ("scripts/orchestrator/task-consistency-check.py", "scripts/validate-agent-assets.py")))'
    output: |-
      glue lines: 39
      new paths absent: True
      dependencies present: True
  - claim: "Historical a01 pre-promotion observation, re-pasted: the glue's root depth, floating interpreter and missing --no-config must change when promoted."
    producer: "orchestrator (Claude seat, sandboxed Bash); historical a01 evidence re-pasted"
    command: |-
      sed -n '7,9p' .agents/worklog/orchestrator-glue/pre-send.sh
    output: |-
      root=$(cd "$(dirname "$0")/../../.." && pwd)
      PY=$HOME/.local/share/mise/installs/python/latest/bin/python3
      uv run --no-project --offline --python "$PY" --with pyyaml python -I "$root/scripts/orchestrator/task-consistency-check.py" "$f" || { echo "checker: refused"; rc=1; }
---

# AGMSG-TASK dotfiles-T133-pre-send-check-a02 — reset the final-byte task preflight

Written 2026-10-20 after M-20261020-01 (a refused string survived in an amendment note), M-20261020-03 (dispatch followed a failed edit), and C-102 (owner sections must exist and carry work). Read those records in .orchestration/learning/ and the untracked glue at `$HOME/Workspace/dotfiles/.agents/worklog/orchestrator-glue/pre-send.sh` (read-only reference, absent from origin/main); the premises re-paste a01's historical pre-promotion observations. This reusable preflight precedes the loop-limits lineage's dispatch.sh --next integration, which owns amendment-hash/failed-edit dispatch control.

Design 5.14 (.orchestration/plans/024-design-quality.md), frozen by D-024-29, applies by reference under D-024-30: rely on items 0 (threat model), 2 (clean environment and isolated Python), 4 (checked contents and digest), 6 (honest residuals), 9 (no-config/offline pinned interpreter), and 10 (sandbox-only commands); this security:false preflight detects mistakes and does not establish a hostile same-UID trust boundary.

## History

a01 spent round 1 and its one revise round: .orchestration/validation/dotfiles-T133-pre-send-check-a01-local-review-d067910.md found P1 raw checker output, P2 tilde/EOF fences, and P2 task_id parsed with sed. The round-2 local review of head 11584e19, saved in .orchestration/validation/dotfiles-T133-pre-send-check-a01-local-review-09e2e95.md, found the same P1 diagnostic-redaction class (checker excerpts expose secret fragments), P2 per-line secret scanning, and P2 shell selection before complete fence parsing. INV-6 returns the lineage to design by this different review-profile context; a02 changes the design to suppression, complete-text scanning and complete-fence parsing, continuing PR #442 with claude-standard-dot-a008.

Amendment 1 (2026-10-21) replaces dispatched a02 SHA256 prefix 438089b8: the audit and security review of head 78882410718dff320194339e02d37fb54c2e856a found six implementation P2. Add the six regressions below, C-123 merge-base caps (130/300 instead of 90/220), and the a02 acceptance-record advisory handoff; update-branch had imported 597 upstream test lines into the obsolete fixed-base count. Keep the reset lineage, allowed_files and existing requirements.

## Item 1

Revise executable scripts/orchestrator/pre-send.sh, retaining the a02 implementation reviewed at 78882410718dff320194339e02d37fb54c2e856a (original a02 starting head 11584e19757286ebdfb8b427c4bcef9555c55545); retain the two-parent repository-root lookup, exactly one task-text argument, and English shdoc @file, @brief, @description, @arg and @exitcode comments. Never edit the input or execute its prose; check the complete final bytes, including front matter, notes and Checks.

- Consistency: run `uv run --no-config --no-project --offline --python "$HOME/.local/share/mise/installs/python/3.15.0/bin/python3" --with pyyaml python -I "$root/scripts/orchestrator/task-consistency-check.py" --root "$root" -- "$task"` against the buffered contents; nonzero, including tool/dependency failure, refuses. Capture stdout/stderr and consume the status. Take task line numbers only from the checker's structured location record, never digits matched in free text, YAML excerpts or quoted tokens; convert to numbers and print only those numbers, never either captured stream.
- Output: neither stdout nor stderr may contain any task-derived or checker-derived text or fragment. Apart from the required digest and the fixed helper-failure message below, emit only fixed `<check>: refused` labels, optionally followed by ` line(s) 12,40`; no excerpts, paths, block indices, match counts, other exit codes, tool errors or tracebacks. Produce one line per failed check; checker-derived line numbers are converted to numbers before printing.
- Secret pattern: extract and compile only the validator's SECRET_PATTERN assignment, never import its unrelated initialization or copy its regex. Use its pattern and flags with re.MULTILINE over the complete text to decide refusal, then once per line for line numbers; also derive lines from complete-match offsets so a match spanning a line break refuses even when neither line alone matches. Use the same pinned Python with -I.
- Literal homes: refuse macOS and Linux home-directory literals, including a home name without a trailing slash; allow $HOME and <home>. Report task line numbers only.
- Self cap: recognize both `at or under **N lines**` and `at or under N lines` with numeric N; compare with `wc -l` newline-counting semantics on the buffer, refuse above the cap, accept equality, allow absence, and report only the declaration's line number on refusal.
- Shell syntax: one CommonMark-style pass parses all fences before selecting bash/sh by the first info-string word, including info-string attributes. Handle backtick and tilde fences of three or more, up to three spaces of indentation, same-character closers at least as long (including longer or indented closers), and open fences closing at EOF; enclosed fence examples stay data. Run `/bin/bash -n` on every selected block, including later blocks after failure, capture diagnostics without echoing them, and report task line numbers only; never execute blocks.
- Owner work: self is task_id from parsed YAML front matter, including `task_id: x # comment`; never extract it with sed. For a reference to `## Owned by <self>` in a named record, resolve relative paths from the repository root and require that exact section bounded by the next CommonMark level-two heading, including `##\tNext` (a literal tab), up to three spaces of indentation, and bare `##`; rows beyond any such boundary cannot satisfy it. With at most one `## Item` heading require a nonempty `<id>\t<class>` row or `- ` bullet inside; with additional Items allow an empty existing section. Missing record or section always refuses; report only the task reference's line number.
- Completion: run all applicable checks despite refusals; exit 0 only when all pass, otherwise 1. Read the input file once into memory; all checks validate that buffer and the final SHA256 hashes that same buffer, never a later reopening of the original path. A path-only checker may consume a byte-identical temporary snapshot preserving filename semantics. For every readable input, including refusals, print `sha256: <64 lowercase hex>` last on stdout. Argument/read failures exit 1 as `input: refused`; suppress all input-derived, subprocess and helper diagnostics on both streams.
- Helper failure: exit 1 with empty helper stdout must produce exactly `preflight: helper failed (exit 1)` and nonzero status, followed by the required digest; never emit only the digest.
- Entrypoint: apply design 5.14 item 2 using `env -i` with only the fixed PATH, HOME, TMPDIR and LANG named in Check before BASH_ENV can emit anything. Cover the actual entrypoint, without caller edits or a new dependency.

## Item 2

Keep tests/unit/test_pre_send.py using unittest, TemporaryDirectory, fixture texts/records and `unittest.main()`; exercise the real preflight/checker offline without live-record edits. Write and run each new regression before production edits, red then green, recording named outcomes in report.md; retained already-green rules keep their a01 red/green provenance rather than a fabricated a02 red. The four round-2 tests and helper may be kept or rewritten. Refusal assertions require exit 1 and the fixed named diagnostic, so missing/broken tooling cannot count as a behavior's red; construct refused secret/home fixtures from fragments and redact evidence.

Retain PreSendTest coverage: test_consistency_refusal; test_secret_pattern_matches_validator (independent assignment extraction, matching lines, a non-match and a final Checks hit); test_literal_home_refusal (both platforms); test_self_cap (both spellings, equality, over, absent and wc newline counting); test_fenced_bash_syntax (multiple blocks, later failure and a never-executed side-effect sentinel); test_owner_section_and_rows (missing record/section even with another Item, empty sole Item, both row forms, rows outside, empty section with another Item); test_all_refusals_are_reported (all named reasons and final digest); test_passes_and_prints_final_sha256 (exact hashlib digest); test_input_refusal (arguments/read).
Add one named test per new rule, using the six original a02 threat-table selectors (each new regression red before the fix and green after): enforce the output grammar on both streams; feed malformed front matter holding a long secret-shaped token that provokes clipped checker excerpts and assert the token and every contiguous 8-character substring are absent from stdout and stderr; verify checker nonzero status and numeric-only named lines; refuse a secret spanning two lines; exclude a bash-looking example inside a larger non-shell fence while accepting attributes on real shell openers; verify `task_id: x # comment` still triggers the owner check. Add a separate test per fence form: backtick, tilde, longer opener, longer closer, indented opener, indented closer and EOF; cover bash and sh. Preserve all unchanged semantics while updating assertions to line-only refusals and the sole fixed helper-failure exception above.

## Check

Worker Playbook step 4: every command runs inside the sandbox; record boundary refusals in sandbox.md and send `AGMSG-PONG v1 status=blocked`, never retry outside. Every evidence item names its producer and seat kind: `worker (Claude seat)`, or `orchestrator (Claude seat, sandboxed Bash)` for orchestrator-produced evidence. Before production edits and after, paste commands, exit statuses and verbatim redacted output into validation.md.

Resolve uv with `/usr/bin/env -i PATH=/usr/bin:/bin HOME="$HOME" "$HOME/.local/bin/mise" which uv`; paste the actual absolute output and use it as `uv_path`, never a guessed version path or an added bin subdirectory/pin file. The fixed entrypoint PATH is that resolved executable's directory plus `/usr/bin:/bin`; HOME and TMPDIR are the worker values and LANG is `C.UTF-8`. Run:

`/usr/bin/env -i PATH="$(dirname "$uv_path"):/usr/bin:/bin" HOME="$HOME" TMPDIR="$TMPDIR" LANG=C.UTF-8 "$HOME/.local/share/mise/installs/python/3.15.0/bin/python3" -I tests/unit/test_pre_send.py`

Amendment 1 adds these six named fixtures in tests/unit/test_pre_send.py; each must be red before its production fix and green after, with the behavior-specific assertion failing rather than tooling:

- `test_checker_option_terminator`: a readable file named `--help` lacks front matter and must exit 1 with `consistency: refused`, never be accepted as checker help.
- `test_checker_structured_locations_only`: malformed YAML a malformed-YAML line whose quoted token contains a ten-digit run followed by `, column 7` (the test file defines the literal; no digit run of eight or more appears in this text) must emit no digits from that token as location numbers on either stream; assert only the actual structured location is reported, with the required digest still last.
- `test_owner_commonmark_boundaries`: an empty sole-Item owner section followed by each CommonMark level-two heading form and another section's rows must exit 1 with `owner-section: refused`; include tab, indentation and bare-heading fixtures.
- `test_helper_exit_one_empty_stdout`: a helper exits 1 with empty stdout; require `preflight: helper failed (exit 1)`, nonzero status and the final digest.
- `test_digest_uses_validated_buffer`: replace the task file between validation and hashing; the digest must equal hashlib's hash of the validated original bytes, not the replacement.
- `test_entrypoint_clears_bash_env`: inherit BASH_ENV pointing to a fixture that echoes a marker; exercise the entrypoint's clearing (do not remove BASH_ENV in the test harness before invoking it) and require the marker absent on both streams.

Run `bash -n scripts/orchestrator/pre-send.sh`, `shellcheck -x scripts/orchestrator/pre-send.sh`, `shfmt -i 4 -sr -d scripts/orchestrator/pre-send.sh`, `ruff check --config ruff.toml tests/unit/test_pre_send.py` and `ruff format --config ruff.toml --check tests/unit/test_pre_send.py`.
Caps: at most 130 changed lines outside `tests/` and `.orchestration/`, and at most 300 under `tests/`.
Measure summed additions plus deletions with `git diff --numstat <merge-base> <head>`, where `<head>` is RESULT's final 40-hex head and `<merge-base>` is `git merge-base origin/main <head>` at RESULT time (C-123); replace the fixed dispatch base entirely. State both 40-hex commits and both cap totals in RESULT and validation.md.
Author at most 193 lines before the approximately seven-line Checks block; this whole task text stays at or under **200 lines**, including Checks.

Do not run Bats locally. After the final push verify GitHub Actions for the exact final head with `gh pr checks 442 --repo mryfmo/dotfiles --watch`, fix in-scope failures and repeat before RESULT; follow Worker Playbook step 15 for the bounded Bot wait and findings. Before completion run `make require-crit-review` and, if required, follow AGENTS.md's crit-data receipt procedure; keep evidence with -worker- filenames under this task's allowed directory and never open a browser review.

## Completion

Continue the existing tools/pre-send-check-a01 branch and PR #442 with claude-standard-dot-a008 (Claude seat, worktree worker-f), retaining the implementation reviewed at 78882410718dff320194339e02d37fb54c2e856a; do not reset to the original 11584e19757286ebdfb8b427c4bcef9555c55545 starting point or start a fresh branch from main. Save .orchestration/dotfiles-T133-pre-send-check-a02/task.md byte-identical to the dispatched text; leave inherited a01 evidence read-only. In the a02 directory write report.md (implementation, named red/green outcomes, residuals, cost), validation.md (commands/output and cumulative cap totals), sandbox.md, learning.md and autoskill.md (used or not-used); do not commit plan/todo/learn worklogs. No changes to dispatch.sh, checker, validator, workflows or untracked glue, and no new dependency or caller changes.

Completion additionally requires all six amendment fixtures' named red/green evidence and preserved original coverage. Deferred advisory rows live in .orchestration/acceptance/dotfiles-T133-pre-send-check-a02.md; owner task dotfiles-T133-pre-send-check-followup-a01 reads them there. The orchestrator corrects that owner's line 41; the worker edits neither the owner task nor the acceptance record.

Push inside the sandbox with `GIT_CONFIG_GLOBAL=/dev/null git -c credential.helper= -c 'credential.helper=!gh auth git-credential' push -u https://github.com/mryfmo/dotfiles.git tools/pre-send-check-a01`; update PR #442 with an English title/body for the final a02 implementation. Once final-head checks pass send `AGMSG-RESULT v1 task_id=dotfiles-T133-pre-send-check-a02 status=ready_for_review pr=<url> head=<40-hex> task_copy=<sha256>` with `merge_base=<40-hex> changed_non_tests=<n> changed_tests=<n>` and artifact paths; no merge by the worker.

## Checks (pasted by the orchestrator before each send)

