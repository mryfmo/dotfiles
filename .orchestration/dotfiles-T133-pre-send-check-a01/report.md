---
task_id: dotfiles-T133-pre-send-check-a01
seat: claude-standard-dot-a008
branch: tools/pre-send-check-a01
base: 60a6fb2b324d0381c4a6e539b37c650105154a7e
test_commit: ff212a70
code_commit: 5e0ea536
bot_fix_commit: 0bfa4eda
fixture_fix_commit: c7581cc5
task_sha256: 907cb3d4735fa9803827aa5b358e3db98a5ee57aa622b97fe138431b4fe43f5b
---

# Report: dotfiles-T133-pre-send-check-a01, the final-byte task preflight

- **Seat and task:** `claude-standard-dot-a008` in `.claude/worktrees/worker-f`. The TASK arrived at 2026-10-20T06:27:05Z.
- **Branch:** fresh from `origin/main` `60a6fb2b`. The task copy is byte-identical to the dispatched file (`907cb3d4…`; validation §3 shows the preflight printing that digest).
- **Untouched:** PR #432's branch is left for its pending integration. The glue, `dispatch.sh`, the checker, the validator and the workflows are unchanged.

## Item 1: `scripts/orchestrator/pre-send.sh` (89 lines)

The glue moved two parents up to `scripts/orchestrator/` and changed as the premises require:

- the root is `$(dirname "$0")/../..`;
- the interpreter is pinned to `$HOME/.local/share/mise/installs/python/3.15.0/bin/python3`;
- uv runs with `--no-config --no-project --offline … --root "$root"`.

It takes exactly one readable file, reads it as data and prints `sha256:` last. Each failed check prints one line `<name>: refused (<detail>)`:

- **consistency:** the checker's nonzero exit, a tool or dependency failure included, with its output folded onto the one line.
- **secret-pattern:** `SECRET_PATTERN` is taken from the validator's syntax tree (`ast`: the assignment's literal arguments, compiled). The validator is neither imported nor executed, and the regex is not copied. The check scans every line and reports the count and line numbers only. A missing or non-literal assignment refuses by name.
- **literal-home:** uses the validator's own `compiled_home_path_pattern`, read from its syntax tree and run alone with no host home.
  - It covers user homes on both platforms (a bare name too), `/var/home` and `/export/home`, runner homes, and the root homes of Linux and macOS (root's dot-directories, and the var-root home, also under private).
  - `$HOME` and `<home>` pass.
- **self-cap:** the first `at or under N lines` or `at or under **N lines**`, against `wc -l`. A text at the cap passes, and a text without a cap passes.
- **bash-syntax:** `/bin/bash -n` over every fenced `bash`/`sh` block, every block checked after a failure. No block is ever run.
  - Fences follow CommonMark: three or more backticks, indented up to three spaces, closed by a fence at least as long.
- **owner-section:** applies when the text reads `## Owned by <task_id>`, with task_id taken from the front matter.
  - The record is the first `.orchestration/acceptance/*.md` path in the text, resolved from the root.
  - The section is that heading, alone or followed by a space, and it ends at the next `## `.
  - Rows are `<id>\t<class>` lines or `- ` bullets.
  - A missing record or section always refuses. An empty section refuses only when the text has at most one `## Item`.
- **input:** a missing or extra argument, or an unreadable path, exits 1 by name, with no digest.

## Item 2: `tests/unit/test_pre_send.py` (169 lines), red then green

The script, checker and validator are symlinked into a temporary root, so records resolve there and no live record changes.

- **The pinned interpreter:** the pinned path, under a temporary HOME, links to the running interpreter. This makes the test independent of the host's mise and lets CI run it. `UV_CACHE_DIR` keeps the real cache, so uv stays offline.
- **Fixtures:** the secret and home fixtures are joined from fragments, and the expected secret lines come from the test's own reading of the validator's assignment.

Every test failed before the script existed (validation §1, 20 failures over 9 tests, exit 1) and passes with it (validation §3, 9 of 9):

| Test | Red (no script) | Green |
| --- | --- | --- |
| `test_consistency_refusal` | FAIL | ok |
| `test_secret_pattern_matches_validator` | FAIL | ok |
| `test_literal_home_refusal` | FAIL | ok |
| `test_self_cap` | FAIL (3 subtests) | ok |
| `test_fenced_bash_syntax` | FAIL | ok |
| `test_owner_section_and_rows` | FAIL (7 cases) | ok |
| `test_all_refusals_are_reported` | FAIL | ok |
| `test_passes_and_prints_final_sha256` | FAIL | ok |
| `test_input_refusal` | FAIL (4 cases) | ok |

## The Codex Bot's review of 6a9edf5b (two P2s, fixed in 0bfa4eda)

| Thread | Finding | Fix | Red on 6a9edf5b (validation §2), green at 0bfa4eda (§3) |
| --- | --- | --- | --- |
| 4322154981 | the root homes of Linux and macOS passed | the validator's own `compiled_home_path_pattern` replaces the narrow regex | `test_literal_home_refusal`: `line(s) 14,16,17,18` (old: 14,16) |
| 4322154977 | a ```` ````bash ```` or indented fence was skipped | CommonMark fence opener and matching closer | `test_fenced_bash_syntax`: `block(s) 2,3,4` (old: 2) |

- **Bot round:** P2 only, so no `@codex review` was requested, and the worker does not resolve threads. Proposed dispositions: `fixed:0bfa4eda` for both.

## Check (validation §4, §5)

- **The script:** `bash -n`, `shellcheck -x` and `shfmt -i 4 -sr -d` exit 0.
- **The test:** `ruff check` and `ruff format --check` with `ruff.toml` exit 0.
- **The comparison lint:** exits 0 on the new script.
- **The preflight on the dispatched task text:** exit 0 and its sha256.
- **`make require-crit-review`:** "Review not required".
- **Caps, over `60a6fb2b…HEAD`:** 89 of 90 changed lines outside `tests/` and `.orchestration/`, and 169 of 220 under `tests/`.
- **CI and the Bot:** both are in the RESULT, because the records commit precedes them.

## CI on 1364630f

- **`validate` failed on the secret fixture's own source** (validation §6). Fixed in `c7581cc5`; the validator now passes locally on the whole tree.
- **`regime` fails, outside this task's files.** regime-ci reads the cap sentence "at most 90 changed lines outside tests/ and .orchestration/, and at most 220 under tests/, measured by … `git diff --numstat <base40>...<head40>`".
  - It takes its excluded paths from the backticked spans of that sentence, which are the command, not `tests/` and `.orchestration/`.
  - So it counts all 851 changed lines against 90.
  - The dispatched text is also not on the base ("task copy unverifiable").
  - Both need the orchestrator: the task text's wording or regime-ci's parser, and the records boundary.

## Residuals

- **Trust:** a mistake detector, not a boundary. A same-user process can change the uv cache, the validator or the checker.
- **The owner record:** the first `.orchestration/acceptance/*.md` path the text names. A text naming another acceptance record first would be checked against that one.
- **The home pattern:** it is the validator's own, and the helper runs that one function from the validator's source. A broken validator therefore refuses every text by name or by traceback.
- **The test's interpreter:** CI runs the test on CI's interpreter through the pinned-path symlink, so the test does not prove that the host's 3.15 pin exists.

cost: n/a
