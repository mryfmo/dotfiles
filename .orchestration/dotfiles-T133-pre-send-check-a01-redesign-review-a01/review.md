---
task_id: dotfiles-T133-pre-send-check-a01-redesign-review-a01
seat: claude-standard-dot-a011
task_sha256: 9ce5c998c1c13373592ab07e7b8591a1e99162a07bf2f953bb94acc862c62b3a
design: .orchestration/tasks/dotfiles-T133-pre-send-check-a02.md
design_sha256: 438089b8b9eb46db347e724913c1d4070d575df5091e3ea4a7e1d4b46412bf95
verdict: accept
---

# Review: the a02 redesign as the INV-6 reset of dotfiles-T133-pre-send-check-a01

Read only, in the main checkout on 2026-10-20. B is `.orchestration/tasks/dotfiles-T133-pre-send-check-a02.md`; A is the a01 text.

## Hash

`shasum -a 256 .orchestration/tasks/dotfiles-T133-pre-send-check-a02.md` gives `438089b8b9eb46db347e724913c1d4070d575df5091e3ea4a7e1d4b46412bf95`, which equals the task's value.

## Item 1: the hash

ok.

## Item 2: the six findings closed by design, and no widening

ok. B:4 reads `reset_of: [dotfiles-T133-pre-send-check-a01]`. The findings come from `grep '^- \[P[0-3]\]'` over the two local reviews:

| Finding | Closed by | Selector |
| --- | --- | --- |
| d067910 P1, redact the consistency-check diagnostics (pre-send.sh:35-36) | B:80-81: the streams are captured and never printed; output is fixed labels and line numbers only | B:38 `test_output_is_labels_and_numbers_only`; B:42 `test_checker_exit_and_line_numbers_only` |
| d067910 P2, tilde and EOF-terminated fences (pre-send.sh:59-61) | B:85: one CommonMark-style pass over backtick and tilde fences, longer openers and closers, indentation, and a fence open at EOF | B:46; B:94 adds one test per fence form, for bash and sh |
| d067910 P2, the owner task id from YAML (pre-send.sh:72-73) | B:86: `task_id` comes from parsed YAML, including `# comment`, never sed | B:48 `test_task_id_yaml_comment` |
| 09e2e95 P1, checker excerpts exposing secret fragments (pre-send.sh:43-46) | B:80-81: no task-derived or checker-derived text or fragment on either stream | B:40 `test_checker_diagnostics_never_echo_secret_fragments` |
| 09e2e95 P2, matching secrets over the complete text (pre-send.sh:47-49) | B:82: `re.MULTILINE` over the complete text, with lines taken from match offsets, so a match spanning a line break refuses | B:44 `test_secret_spanning_two_lines` |
| 09e2e95 P2, parsing complete fences before selection (pre-send.sh:56-58) | B:85: all fences are parsed before bash or sh is selected; enclosed examples stay data | B:46 `test_complete_fences_before_shell_selection` |

This is a change of design, not a patch: suppression replaces redaction, complete-text scanning replaces per-line scanning, and a complete fence parse replaces per-block matching (B:74).

- **Selectors.** Each new rule has a `closed:` selector: the six new rows B:37 to B:48, plus the closed rows B:14 and B:26.
- **The output-suppression test.** B:94 feeds a long secret-shaped token through malformed front matter and asserts that "the token and every contiguous 8-character substring are absent from stdout and stderr".
- **No widening.** Against A:
  - `allowed_files` differs only by the evidence directory (B:10 and A:9);
  - `security: false` is unchanged;
  - the push command is the same (B:110 and A:91);
  - B:108 adds no changes to dispatch.sh, the checker, the validator, workflows or the glue, and no new dependency or caller;
  - the residual at B:28 states the same-UID cache mutation honestly.
- **Caps.** 90 and 220 are intact (B:102 and A:83).
- **The C-107 grammar.** It holds: the cap sentence backticks only `tests/` and `.orchestration/`, and the numstat command is its own sentence. base40 stays the a01 base `60a6fb2b…`, never `11584e19`.
- **The self cap.** It rises from 110 to 130 lines, and B is 114 lines.

Advisory note, P3: B:115 has an empty Checks block. The orchestrator pastes it before the send.

## Item 3: read only

ok. No file other than this record in the seat's worktree was changed. No commit, push, PR or dispatch.

## Verdict

accept
