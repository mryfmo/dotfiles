---
task_id: dotfiles-T133-pre-send-check-a02
seat: claude-standard-dot-a008
reset_of: dotfiles-T133-pre-send-check-a01
pr: 442
branch: tools/pre-send-check-a01
start_head: 11584e19757286ebdfb8b427c4bcef9555c55545
test_commit: 70fc2f84
code_commit: de7f70ec
task_sha256: 438089b8b9eb46db347e724913c1d4070d575df5091e3ea4a7e1d4b46412bf95
---

# Report: dotfiles-T133-pre-send-check-a02, the preflight reset to suppression

- **Seat and task:** `claude-standard-dot-a008` in `.claude/worktrees/worker-f`. The TASK arrived at 2026-10-20T14:25:55Z.
- **Branch:** PR #442 continues on `tools/pre-send-check-a01` from `11584e19`.
- **Records:** the task copy is byte-identical to the dispatched text (`438089b8…`, and the preflight prints that digest, validation §2). a01's evidence is left as it was.

## Item 1: `scripts/orchestrator/pre-send.sh` (89 lines)

Every check runs as one helper. The helper is read into a variable with `read -d ''`, because a heredoc inside `$( … )` breaks on the apostrophes in its comments. It runs as `python -I -c` under the checker's `uv run --no-config --no-project --offline --python <pinned 3.15> --with pyyaml`.

- **Output:**
  - The helper's stderr and uv's go to `/dev/null`, and its stdout carries only fixed labels: `<check>: refused`, optionally followed by ` line(s) N,M`.
  - The script adds `input: refused` and the final `sha256:`. No excerpt, path, count, exit code or traceback is printed.
  - An unavailable uv, PyYAML or interpreter becomes `consistency: refused`, exit 1.
- **consistency:** the checker runs as a subprocess and both of its streams are captured and never printed. Its YAML marks (`line N, column M`) become task lines N + 1, because the front matter starts after the first `---`.
- **secret-pattern:** `SECRET_PATTERN` comes from the validator's syntax tree, its literal arguments and flags plus `re.MULTILINE`.
  - It runs over the complete text, and every line a match spans is reported, so a match across a line break refuses.
  - It then runs per line as well.
  - A missing or non-literal assignment refuses with no lines.
- **literal-home:** the validator's own `compiled_home_path_pattern`, read from its syntax tree and run alone with no host home. It reports task lines.
- **self-cap:** `at or under N lines` or `at or under **N lines**`, against the file's newline count. The declaration's line is reported.
- **bash-syntax:** one CommonMark-style pass parses every fence before anything is selected.
  - Openers are three or more backticks (whose info string has no backtick) or tildes, with up to three spaces of indent.
  - A closer uses the same character, is at least as long, has up to three spaces of indent and trailing spaces, and an unclosed fence ends at EOF.
  - Shell blocks are those whose info string's first word is `bash` or `sh`; attributes after it are allowed.
  - Content loses up to the opener's indent, then `/bin/bash -n` parses it without running it. The opener lines of failing blocks are reported.
- **owner-section:** applies when the text holds `## Owned by <task_id>`, with task_id taken from `yaml.safe_load` of the front matter, as the checker splits it, so a trailing YAML comment does not leak into the id.
  - The record is the first `.orchestration/acceptance/*.md` path, resolved from the root, and the section ends at the next `## `.
  - The check refuses on a missing record or section, or on no row when the text has at most one `## Item`. It reports the reference's line.

## Item 2: `tests/unit/test_pre_send.py` (215 lines)

- **The grammar on every run:** `run_send` asserts that stderr is empty and every stdout line fits the grammar.
- **The red run:** the final test source against `11584e19`'s script (validation §1) failed 21 of 22 tests (28 failures). `test_passes_and_prints_final_sha256` passed: its output was always just the digest.
- **The green run:** all 22 pass at `de7f70ec` (validation §2).

| New rule (threat-table selector) | Red at 11584e19 | Green at de7f70ec |
| --- | --- | --- |
| `test_output_is_labels_and_numbers_only` | FAIL | ok |
| `test_checker_diagnostics_never_echo_secret_fragments`: no 8-character run of a 30-character token | FAIL | ok |
| `test_checker_exit_and_line_numbers_only`: `consistency: refused line(s) 6,7`, PyYAML's two marks | FAIL | ok |
| `test_secret_spanning_two_lines` | FAIL | ok |
| `test_complete_fences_before_shell_selection`: a ```` ```bash ```` example inside a ```` ````markdown ```` fence is data; `bash {.example}` is selected | FAIL | ok |
| `test_task_id_yaml_comment` | FAIL | ok |
| `test_fence_backtick`, `_tilde`, `_longer_opener`, `_longer_closer`, `_indented_opener`, `_indented_closer`, `_open_at_the_end` (bash and sh), one generated test per form | FAIL (each) | ok (each) |

The retained rules are `test_consistency_refusal`, `test_secret_pattern_matches_validator`, `test_literal_home_refusal`, `test_self_cap`, `test_fenced_bash_syntax`, `test_owner_section_and_rows`, `test_all_refusals_are_reported`, `test_passes_and_prints_final_sha256` and `test_input_refusal`.

- **Provenance:** their behaviour keeps its a01 red/green provenance.
- **Their red here:** the a02 red above comes from the line-only assertions, not from new behaviour.

## Check (validation §2, §3)

- **Script and tests:** `bash -n`, `shellcheck -x`, `shfmt -i 4 -sr -d`, `ruff check` and `ruff format --check` all exit 0.
- **The a02 text:** passes its own preflight.
- **`make require-crit-review`:** "Review not required".
- **Caps:**
  - The PR's own change against `origin/main` is `scripts/orchestrator/pre-send.sh` +89, 89 of 90, and `tests/unit/test_pre_send.py` +215, 215 of 220.
  - The literal `60a6fb2b…HEAD` measure also counts the files that the orchestrator's three main merges (`9ff87ee1`, `9ce253f1`, `d0679105`) brought in, which gives 92 and 245.
  - Those extra lines are main's, not this task's. Both measures are pasted in §3.

## Residuals

- **Trust:** a mistake detector, not a boundary against a same-user process. A changed validator or checker changes what is checked.
- **Line numbers:** a refusal names lines, not causes. The checker's non-YAML findings (C1 to C10) carry no line, so their refusal is the bare label.
- **The owner record:** the first acceptance path the text names.

cost: n/a
