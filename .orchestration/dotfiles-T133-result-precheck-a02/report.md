---
task_id: dotfiles-T133-result-precheck-a02
round: 1
reset_of: dotfiles-T133-result-precheck-a01
status: precheck-recorded
---

# Report

Worker `claude-standard-dot-a009` (Claude Code, worker-c). Branch `tools/result-precheck-a01`, PR #411 (continued from a01), base `origin/main` 99a4a80f, tested code head 38b9178b7a25df16ac26e01110294edfdd30d61c (the RESULT names the final evidence-only head). Task copy `.orchestration/dotfiles-T133-result-precheck-a02/task.md` is byte-identical to the dispatched file: sha256 `fda18e21e738bb222a50ebd29be302fa009fd1a2822b660311abe81aa1397e61`. The predecessor's copy and records under `.orchestration/dotfiles-T133-result-precheck-a01/` are untouched (outside `allowed_files`; the orchestrator does the reset bookkeeping). Parked PR of a01's item 0: #406.

Inherited, not re-derived here: a01's records, its Bot threads (4305945403, 4305945406, 4305945407, all fixed in a01 by a7b0da2f and bdd8ab81) and its counters. Fresh: everything in this directory.

## What changed (from a5cb73b4 to 38b9178b)

- `.githooks/pre-push` (item 5, the local review's P1): every commit of the pushed range, merges included (`git diff-tree -r -m --root --diff-filter=d`), appends the whole content of each blob it adds or changes, read with `git cat-file blob <commit>:<path>` (the raw form of `git show <commit>:<path>`, without textconv), so a `-diff` or `binary` attribute or a NUL byte never turns content into a `Binary files differ` summary; a range git cannot read still stops the push.
- `scripts/orchestrator/result-precheck.sh` (items 5 and 6): the `secrets` input is `git diff --text origin/main...HEAD`; the detector `secrets_in` (shared with `--secrets`, the pre-push entry) turns bytes outside printable ASCII into newlines before masking, so a NUL-bearing or binary blob hides nothing and cannot make the masker fail on decoding. Every command a check needs fails its check explicitly (`|| return` or a named failure), since errexit is off in a function run through `||`: the formatter file listings (a new `on_files` helper that tells a failed listing from an empty one), the shellcheck file list, the secrets diff, the seat review's `git rev-parse` and PR number, and the `--staged` index export.
- `scripts/orchestrator/dispatch.sh` (item 7): the checker takes the requested selectors from the newest `status=revise` ACCEPTANCE before the newest RESULT (every `check=` token), requires each of the six names `unit-test`, `render-check`, `format`, `shellcheck`, `secrets` and `local-review` exactly once with `ok` the JSON boolean `true` (the exact `{name: local-review, ok: null, deferred: orchestrator}` record is the only null), and requires `selectors` to be a list of passing proofs holding exactly one entry for each requested selector. Failures name `precheck.json:checks` or `precheck.json:selectors`.
- `tests/unit/test_result_precheck.py`: the three regressions `test_pre_push_scans_binary_marked_blobs_in_every_pushed_commit`, `test_precheck_records_failed_commands_as_not_ok` and `test_dispatch_rejects_malformed_checks_and_missing_requested_selectors`, written first; item 4's updates (ruff and prettier failures in the formatter cases, all six checks plus the exact deferred record in the dispatch success fixture, commits that hold only the record). The `uv` stub hands masking to the real uv while a `real-masker` marker exists; `gh` fails while `gh-fails` exists.

Caps (validation.md): 398 changed lines outside `tests/` and `.orchestration/` (cap 420), 446 under `tests/` (cap 520). Changed files against `origin/main`: `.githooks/pre-commit`, `.githooks/pre-push`, `scripts/orchestrator/dispatch.sh`, `scripts/orchestrator/result-precheck.sh`, `tests/unit/test_result_precheck.py`, and the two evidence directories.

## Red and green (validation.md)

The current test source in a detached worktree at a5cb73b4 fails all three regressions by assertion: 17 failures, no error (the push cases `diff-attr`, `binary-attr`, `nul`, `added-then-removed` and the precheck's forced-text secrets case; the failed-prerequisite cases; all eleven malformed records). On 38b9178b the three pass, and both modules give 67 tests OK. The first version of the malformed-record test passed on a5cb73b4 for the wrong reason (learning.md) and was corrected before this red run.

## The precheck

The default run on 38b9178b exits 1: `unit-test` (`make unit-test`) fails 296 tests inside the sandbox, the identical set fails on a pristine `origin/main` worktree in the same sandbox (`cmp` of the sorted names), none in this task's modules; render-check, format, shellcheck and secrets pass. The final proof, `scripts/orchestrator/result-precheck.sh dotfiles-T133-result-precheck-a02 --tests tests.unit.test_result_precheck tests.unit.test_orchestrator_tools`, exits 0: `precheck=67de44ecedc495308e539fae5a48518ff081b2208bac6ca02288d7d20dd6eed8`, record `head` 38b9178b. CI's `make unit-test` decides the full suite.

## Feedback dispositions

- Local review of a5cb73b4 (`.orchestration/validation/dotfiles-T133-result-precheck-a01-local-review-a5cb73b.md`): [P1] binary-marked content in pre-push and the precheck's secrets input: fixed:38b9178b (item 5); [P2] diff errors recorded as passing checks: fixed:38b9178b (item 6); [P2] missing and non-boolean check results: fixed:38b9178b (item 7).
- The Bot: no `@codex review` (the no-prompt rule); the window after this push is recorded in the RESULT.

## Observation for the orchestrator (no code change)

Item 5 scans whole blobs, so content already in a touched file counts too. 13 of 5485 tracked files hold text the masker flags today (validation.md: 45 matches in `tests/unit/test_validate_agent_assets.py`, 38 in `tests/install/common/setup.bats`, 16 in `scripts/validate-agent-assets.py`, and the vendored CompactionDB tests among them); once P1-7 sets `core.hooksPath`, a push touching one of them is refused. A rule that counts only matches a commit adds (or scans added lines) would avoid that; it is outside this task's text.

[memory:decision] T133 a02: pre-push scans the whole content of every blob each pushed commit adds or changes with git cat-file blob, and dispatch.sh's precheck gate requires the six checks once with ok true (only the exact deferred local-review record is null) plus one passing proof per selector the newest revise ACCEPTANCE requested.

## Not done yet

The evidence commit, the one push, CI on the final head, the Bot window and the RESULT (`parked_pr=406`).

cost: n/a
