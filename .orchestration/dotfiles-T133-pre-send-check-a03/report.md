---
task_id: dotfiles-T133-pre-send-check-a03
seat: claude-standard-dot-a009
reset_of: dotfiles-T133-pre-send-check-a02
pr: 442
branch: tools/pre-send-check-a01 (worked on the local branch a03/pre-send-check; see sandbox.md)
production_head: 1d72f16978018c3d016bbc239d79d3d7d0675105
red_fixture_commit: 96d0afefe904c5ec8b3bf13ff82a7151bb8518f1
fix_commit: 9dc5c565d6d21d4f52d5f317ca7f40d577425010
correction_commit: b8a5c394be64a666a6531435b562c5a3a9e0b878
merge_base: e00de4e0e4158de19e2c8921e572461e7e9e4ca0
task_sha256: 53f78f967929b80987eb515affaabde637d12c1f52edb8bce5262c95f8282f77
cost: n/a (the seat's token and time usage is not visible to the worker)
---

# Report: dotfiles-T133-pre-send-check-a03 (the reset of a02: Python replaces echoed-output parsing)

- **Task:** the AGMSG-TASK of 07:25:42Z (sha `53f78f96…`). The task copy is byte-identical (validation §1). PR #442 continues from `1d72f169`, keeping all a01/a02 history and the 28 tests.
- **The design (Item 1):**
  - **`pre-send.sh` is only the entrypoint (32 lines).** `bash -p` ignores BASH_ENV and exported functions. It resolves uv as the absolute path that `$HOME/.local/bin/mise which uv` prints under `env -i`, falling back to the probed absolute install, with no PATH search; `dirname` is called by absolute path too.
    - Missing both, it prints the fixed `startup: refused`.
    - Otherwise it re-executes unconditionally under `env -i` with only `PATH=<uv dir>:/usr/bin:/bin`, `HOME`, `TMPDIR` and `LANG=C.UTF-8`, and runs `pre_send.py` through `uv run --no-config --no-project --offline --python <pinned 3.15> --with pyyaml python -I`, with stderr discarded.
    - It forwards only the exit status. A uv or interpreter failure (rc > 1) becomes the fixed `interpreter: refused`.
    - The shdoc carries `@file`, `@brief`, `@description`, `@arg` and `@exitcode`.
  - **`pre_send.py` (194 lines)** reads the task once as bytes. Every check and the sha256 use that buffer, and the path is never reopened.
    - CRLF and lone CR are normalized in the derived text, while the raw buffer gives the digest and the wc-style newline count.
    - PyYAML parses the front matter. Its error marks are the only YAML locations, as task lines (mark + 2).
    - The checker runs as `sys.executable -I task-consistency-check.py --root <root> -- <snapshot>`, on a byte-identical snapshot with the original file name under `TMPDIR`. Both streams are discarded and only its exit status counts.
    - One CommonMark fence state machine serves the task and the owner record: backticks or tildes, length at least three, up to three leading spaces, a same-character closer at least as long, EOF closure, and bash or sh by the first info word.
    - Headings, Items and owner sections are counted outside fences only. `bash -n` runs on a temporary file under `TMPDIR`.
    - Every a02 rule is kept: the validator's SECRET_PATTERN through `ast` without importing the validator, over the complete text and each line; its home pattern; both self-cap spellings with wc semantics; and the named record's exact `## Owned by <task_id>` section, ended by every CommonMark level-two heading, with the row and Item rule.
    - All checks run despite refusals. A temp failure prints `tempfile: refused`, any other failure the fixed `preflight: helper failed (exit 1)`. The digest comes last for every read buffer.

## The six reset regressions (Item 2)

| Class | Attack | Selector | Red (96d0afef, production 1d72f169) | Green |
|---|---|---|---|---|
| argument-injection-bypass | a multiline YAML `task_id` carrying a fake `line 1234567890` location | `test_multiline_task_id_has_parser_locations` | prints `consistency: refused line(s) 1234567891` | `9dc5c565` |
| fence-forms | CRLF and lone CR close a non-shell tilde fence before an invalid shell fence; CRLF front matter still names the owner | `test_crlf_tilde_closer` | 3 subtests: no bash-syntax or owner-section refusal (exit 0) | `9dc5c565` |
| heading-form-gap | a fenced `## Item` beside one real Item, with an empty owner section | `test_fenced_item_does_not_supply_owner_work` | passes (exit 0) | `9dc5c565` |
| digest-toctou | the checker replaces the path, then a later helper failure | `test_digest_survives_replacement_and_helper_failure` | the digest is the replacement's | `9dc5c565` |
| inherited-environment | `env -i PATH=/usr/bin:/bin` and a decoy PATH | `test_entrypoint_fixed_environment` | both exit 1 (uv not found, or the decoy used) | `9dc5c565`; its `dirname` decoy is red at `9dc5c565` and green at `b8a5c394` |
| diagnostic-redaction | an unwritable `TMPDIR` | `test_temp_failure_is_redacted` | exits 0 | `9dc5c565` |

- **On the temp row:** on this host the legacy helper did not print raw diagnostics. Python's `tempfile` fell back to another writable directory, so nothing refused. a03 creates its temporary files explicitly under `TMPDIR`, so an unusable `TMPDIR` is the fixed `tempfile: refused`, now pinned by the test.
- **The 28 preserved tests:** they pass at `96d0afef`, where the 9 failures are exactly the six regressions' subtests, and at `b8a5c394` (34 of 34; validation §3, §4).
- **The extended output test:** `test_output_is_labels_and_numbers_only` checks both streams. No 8-character window of the task's lines, the secret fixture, or the real checker's output may appear once the fixed label text is stripped. The label set is pinned in `LABELS`, shared with `GRAMMAR`.
- **Fixture setup:** it links `pre_send.py` only when it exists, so legacy heads run, and gives the temporary HOME a pinned `mise` that answers with the real uv.

## Checks and caps (validation §5)

- **Static checks:** `bash -n`, `shellcheck -x`, `shfmt -i 4 -sr -d`, `ruff check`, `ruff format --check` and the comparison lint on the three files all exit 0.
- **Cumulative caps from merge-base `e00de4e0`:**
  - `changed_non_tests` 226 of 360 (`pre-send.sh` 32, `pre_send.py` 194);
  - `changed_tests` 359 of 480.
- **Final-line attribution at `b8a5c394`:**
  - implementation: inherited a01/a02 12, a03 214;
  - tests: inherited 258, a03 101.

  This is blame attribution, not change churn. The authoring measurement at `1d72f169` was 104 implementation and 260 test lines.

## Review (one round)

- **The verdict:** a fresh read-only subagent reviewed `1d72f169..9dc5c565` and returned `Verdict: incorrect`.
- **Fixed in the correction round `b8a5c394`:**
  - **P2:** `dirname` went through the inherited PATH before the re-exec. The reviewer reproduced a decoy `dirname` running.
  - **P2:** the decoy list did not include `dirname`.
  - **P3:** the temp label was not pinned.
  - **P3:** the label set was not pinned.
- **Kept, one P3:** a YAML error rides on the `consistency` label rather than its own, because the preserved a02 test requires `consistency: refused line(s) 6,7`. Only `task_id` is read from the mapping; the checker validates the other fields. This is advisory for `dotfiles-T133-pre-send-check-followup-a01`.
- **The gate:** `make require-crit-review` is satisfied with the worker evidence (§6).

## Residuals

- **Not shown in the sandbox:** a same-UID process can still replace an executable or the cache. The live hosted-runner behaviour is CI's.
- **The fallback path:** the absolute fallback uv path is the author's probe for this host's architecture.
- **Not run:** Bats was not run locally.
