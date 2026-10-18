---
task_id: dotfiles-T133-result-precheck-a03
round: revise-1
reset_of: dotfiles-T133-result-precheck-a02
status: precheck-recorded
---

# Report

Worker `claude-standard-dot-a009` (Claude Code, worker-c).

- Branch `tools/result-precheck-a01`, PR #411, continued from 4ed1b27a666ba939db76051243143a7d7ed2aaa5.
- Merge base with `origin/main`: de3b73cc. `origin/main` itself is now 3e41e36a.
- Tested code head: 1ac3a1a674df895b541aff3a2fac8709b934abc9. The RESULT names the final evidence-only head.
- Task copy `.orchestration/dotfiles-T133-result-precheck-a03/task.md` is byte-identical to the dispatched file: sha256 `f416aee0dd314b3dbb33db7ef71da78f261f06bb822ed684adc685ad77034e39`.
- INV-6 for a03: amendments=1, questions=0, revises=1 after revise 1 below (no further round).
- Revise 1: code head 024ba0eb on bccb2dea; the task copy is amendment 1's text, sha256 `d8048ef508676f65c5eaee82cc69a9f83f04b4418ed3e61bb9e4803d5c0a32ba`.
- Parked PR of a01's item 0: #406.

Inherited, not re-derived here: the a01 and a02 records, their stopped history and counters, and the historical red baseline a5cb73b4 of the a02 regressions. Fresh: everything in this directory.

## Reset bookkeeping (first push)

Code commit 1ac3a1a6 holds the bookkeeping the task directs:
- the a03 task copy;
- `git rm` of `.orchestration/dotfiles-T133-result-precheck-a02/task.md` and `.orchestration/dotfiles-T133-result-precheck-a01/task.md` (both were present);
- the redesign and its tests.

No other path outside `allowed_files` changed.

## The redesign

### One blob, one detector run (items 1 and 5)

`result-precheck.sh` replaces a02's `secrets_in` with `scan_one`, which scans one input alone:
- A blob (`<commit> <path>`) is read with `git show --no-textconv`, so no binary attribute or NUL byte turns it into a summary. A file (`--secrets <file>`) is copied unchanged.
- The input is placed at its own repository-relative path under a fresh directory below the script's `$TMPDIR` work directory, which the EXIT trap removes.
- An embedded `python -I` program, run through `uv`, loads `scripts/validate-agent-assets.py` and applies its detector exactly as `validate_no_obvious_secrets` reads a tracked file:
  - `read_scannable_text`: UTF-8, or UTF-16 with a BOM. Anything else, a NUL, or UTF-16 under `.orchestration/` is refused.
  - `json_strings` for a JSON document's keys and string values.
  - `strip_allowed_secret_placeholders`, then `SECRET_PATTERN`.
- `read_scannable_text` judges a path relative to the validator's `ROOT`, so `ROOT` points at the temporary root for that one call. The `.orchestration/` refusals therefore apply by the blob's original path.

The concatenated stream, the revise-1 newline separator and the NUL-to-newline and NUL-stripped views are deleted. So are the masker-based comparison and the `mask()` helper; the masker now only normalises the evidence logs, inline.

Who calls `scan_one`:
- The `secrets` check calls it for every blob that `git diff --name-only -z --no-renames --diff-filter=d origin/main...HEAD` changes.
- `--secrets <file>` scans exactly that file.
- `--blob <commit>:<path>` is the pre-push hook's entry point.

`.githooks/pre-push` keeps its range rules (every commit of the pushed range, merges included) but calls `--blob` once per changed blob and never builds a shared input. It sums the secret counts into `pre-push: <n> match(es) in <range> (<ref>)` and prints each other finding on its own `pre-push: …` line. A scan that fails without any recognised line prints `pre-push: scan: <commit>:<path> failed`.

### Distinct, value-free diagnostics (item 1)

The detector prints only:
- `secrets: <n> match(es)`;
- `decoding: <path> cannot be decoded`;
- `home-path: <path> names a home directory`.

`scan_one` adds `unreadable: <commit>:<path> cannot be read`. Secret counts come only from `SECRET_PATTERN` matches. A failing `git diff`, `git cat-file` or blob read fails the check explicitly; errexit is not relied on.

### Home paths (item 7)

`home_path_pattern` applies only when the original path starts with `.orchestration/`, to the text and its decoded JSON strings, as the validator scopes it. A public file with home-path examples passes; the same text under `.orchestration/` fails with the home-path line and no secret count. Evidence log masking is unchanged.

### Revise ordering (item 6)

`dispatch.sh`'s precheck block finds the task's latest `status=revise` ACCEPTANCE anywhere in the pre-send window. If it follows the newest RESULT, that RESULT is refused with `precheck: result the newest RESULT for task_id=<t> precedes its latest status=revise ACCEPTANCE`, or warned about without `PRECHECK_REQUIRED=1`. Otherwise its `check=` selectors are the requested proofs. Another task's revise is ignored.

### Retained

- The revise-1 guarantees and their tests: blob boundary, UTF-16 decoding or refusal, and the executed-assertion red proof.
- The selector proof: this head's module in a detached worktree of `--previous-head`; exit 1, `Ran n>0`, failures and no errors.
- The six-check and selector validation in `dispatch.sh`, the staged pre-commit checks, the deferred local review and both `shortcut:` header lines.

## Tests (`tests/unit/test_result_precheck.py`)

New (items 5 to 7), written first and red against 4ed1b27a with this head's test source:
- `test_pre_push_scans_each_blob_on_its_own_and_keeps_json_decoding`: `{"key": "ghp_…"}` followed by a clean JSON document. `--secrets` finds the credential in the first document alone (exit 1) and none in the two concatenated (exit 0). The real push is refused with the match count, no remote ref, and no value in the output. The precheck's `secrets` is `false`, and a clean pair pushes.
- `test_pre_push_fails_closed_on_an_undecodable_blob`: invalid UTF-8 stops the push with `pre-push: decoding: …` and no match line. The precheck's `secrets` is `false`, and a decodable counterpart pushes.
- `test_dispatch_acceptance_check_requires_a_result_newer_than_the_latest_revise`:
  - With a revise after the ready RESULT, the send exits 1 under `PRECHECK_REQUIRED=1`, and under `0` it warns and sends.
  - The same RESULT after the revise passes, as does one followed only by another task's revise.
- `test_pre_push_reports_home_path_rewrites_only_under_orchestration`: `docs/guide.md` with a macOS home-directory example (`/Users/<name>/...` form) pushes and the precheck's `secrets` is `true`. `.orchestration/x/report.md` with the same text is refused with `pre-push: home-path: …` and no match line, and the precheck's `secrets` is `false`.

Changed to the redesigned behaviour:
- **UTF-16 refusal (item 4):** a BOM-less UTF-16 file is now a decoding refusal rather than a match, and a NUL-bearing blob (`nul`, `nul-clean`) is refused as undecodable, clean or not. This is in `test_result_precheck_decodes_or_refuses_utf16_before_the_secret_scan` and `test_pre_push_scans_binary_marked_blobs_in_every_pushed_commit`.
- **Real secret trigger:** the `secrets` failure of `test_precheck_exits_1_and_records_ok_false_for_each_failing_check` is a committed token found by the real detector, instead of the masker stub's `masker-changes`.
- **`uv` stub:** the stub skips `--no-project` and `--with <pkg>` before `python`.

Consolidated to fit the 520-line cap, without dropping a case:
- the four push tests share `push()` and `secrets_ok()`;
- the pre-commit tests share `hooked_commit()`;
- the `--secrets` calls share `scan()`;
- the two dispatch-record tests share `evidence()`.

## Red and green (validation.md)

Each red run copies this head's test module (sha256 `edd94951d8abb4639c6463b0b8b04a83ea010e3e3b92736dad0ab9540ff7fef5`) into a scratch worktree of the reviewed production commit:
- **Against 4ed1b27a, the four new tests:** 4 failures, no error.
  - JSON push accepted: `0 != 1`.
  - Undecodable push accepted: `0 != 1`.
  - Stale RESULT accepted: `(0, True, False) != (1, False, True)`.
  - Public home-path push refused: `1 != 0`.
- **Against 9cd5514a, the three retained revise-1 tests:** 6 failures, no error.
  - Joined push accepted.
  - `test_always` and `test_helper` accepted as red proofs.
  - Each UTF-16 encoding scanned as `secrets: 0 match(es)`.

Their passing state at 4ed1b27a is retained, not presented as a new red. A first replay attempt with `/usr/bin` prepended to PATH ran the system Python 3.9 and failed for that reason. It was discarded and rerun (sandbox.md).

Green on 1ac3a1a6:
- both modules give 75 tests OK;
- the final proof's four selectors each fail by assertion on 4ed1b27a (`Ran 1 test`, `FAILED (failures=1)`) and pass here.

## The Check (validation.md)

- `make render-check`: exit 0.
- `shellcheck -x` and `shfmt -d -i 4 -sr` on the four scripts: clean.
- CI's three formatting commands in CI's scopes: all exit 0.
- The two modules: 75 tests OK.
- `make format`: exits 2 at `shfmt --diff .`, with the same twelve pre-existing files as a pristine `origin/main` 3e41e36a worktree.
- The default precheck run (`result-precheck.sh dotfiles-T133-result-precheck-a03`) exits 1:
  - `unit-test` (`make unit-test`) fails 305 tests inside the sandbox, the identical sorted set a pristine `origin/main` worktree fails in the same sandbox (`cmp`), none in this task's modules;
  - render-check, format, shellcheck and secrets pass. The secrets check scanned the branch's real changed blobs, the a01 and a02 evidence included.
- **Final proof:** `result-precheck.sh dotfiles-T133-result-precheck-a03 --tests tests.unit.test_result_precheck tests.unit.test_orchestrator_tools --previous-head 4ed1b27a… --check` × 4 exits 0.
  - `precheck=6701ae4f035dc4aec568cc37bec44028b217018c9f0825be496e2ff439c71589`;
  - record `head` 1ac3a1a6;
  - the five executed checks `true`, `local-review` the exact deferred record, the four selectors `ok: true`.
- **Caps (`git diff --numstat origin/main...HEAD`):** 419 changed lines outside `tests/` and `.orchestration/` (cap 420), 520 under `tests/` (cap 520). The changed files outside `.orchestration/`:
  - `.githooks/pre-commit` (unchanged since a02);
  - `.githooks/pre-push`;
  - `scripts/orchestrator/dispatch.sh`;
  - `scripts/orchestrator/result-precheck.sh`;
  - `tests/unit/test_result_precheck.py`.

## Feedback dispositions

- **Local review of 4ed1b27** (`.orchestration/validation/dotfiles-T133-result-precheck-a02-local-review-4ed1b27.md`), all three fixed:1ac3a1a6:
  - [P1] scan blobs separately to preserve JSON secret detection (`.githooks/pre-push:27-31`);
  - [P2] reject RESULTs that precede the latest revise (`dispatch.sh:174-176`);
  - [P2] separate home-path normalisation from secret detection (`result-precheck.sh:98-103`).

  The two P2 were recorded as advisory before; this task owns them now. The orchestrator records that superseding ownership.
- **Local review of 9cd5514**, the three retained guarantees: still fixed. Their tests are green on 1ac3a1a6 and red against 9cd5514a with this head's test source.
- **The Bot:** no `@codex review` (the no-prompt rule). The window after the push is recorded in the RESULT.

## Observations for the orchestrator (no change made)

- **Undecodable blobs now stop pushes.** Under item 1's fail-closed rule, every blob the detector cannot decode stops a push once `core.hooksPath` is live (P1-7): images, archives, any NUL-bearing or non-UTF-8 file. That is the specified behaviour; the hooks-path task should know it before enabling the hook.
- **Vendored fixtures are not exempt.** `validate_no_obvious_secrets` exempts four vendored CompactionDB test files, but that list is local to the function and `scan_one` does not inherit it. A push touching those files is refused for their dummy credentials. Reusing the list needs a validator change, which is outside `allowed_files`.
- **One `uv` start per blob.** One `--blob` scan took 0.19 to 0.21 s here (validation.md), so a push touching 100 blobs adds about 20 s.

[memory:decision] T133 P1-5 a03: result-precheck.sh scan_one feeds each blob unchanged to validate-agent-assets.py's own read_scannable_text, json_strings, strip_allowed_secret_placeholders and SECRET_PATTERN (home_path_pattern only under .orchestration/); an undecodable blob fails closed; pre-push calls --blob <commit>:<path> per blob; dispatch.sh requires the newest RESULT to follow the task's latest status=revise. Recorded with `uv run --no-project .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content '…'` as memory `67366379-780e-431d-8764-2b1f46cf95dc` (validation.md).

## Revise 1 (the task-level audit of bccb2de and amendment 1)

The ACCEPTANCE `status=revise` of 22:16:07Z named three items, each with a `check=` test. Code commit 024ba0eb on bccb2dea:

1. **The proof baseline (audit P2, `dispatch.sh:177`).** Each selector proof in `precheck.json` now records its `previous_head`. The acceptance check reads the latest revise's `previous_head=` and refuses (`PRECHECK_REQUIRED=1`) or warns about a requested proof whose `previous_head` differs: `precheck: precheck.json:selectors … proves […] against another baseline than previous_head=[…]`.
   - The revise's `check=` is read both as repeated tokens and as one comma-separated list, the form the orchestrator's revise lines use, this round's own included. Before, a comma list was one selector that no proof could match, so such a revise could never be accepted under `PRECHECK_REQUIRED=1`.
2. **The clean-tree query (audit P2, `result-precheck.sh:187`).** `git status` writes to a work file, and a failure exits 2 before any check runs; git's own message says why.
3. **Exact test selection (audit P2 on the task text, amendment 1).** A selector runs as `tests.unit.<module>.<Class>.<name>`, never `-k`.
   - An awk scan of this head's module finds the one top-level class defining `def <name>(`. None or two gives exit 2 on both sides and no proof.
   - A red proof needs `Ran 1 test` with failures and no errors; a green one needs `Ran 1 test` and exit 0.
   - `selectors[]` records `id`, `previous_head`, `previous_head_tests` and `head_tests` beside the existing fields.

Tests: `test_dispatch_acceptance_check_compares_the_proof_baseline_with_the_latest_revise`, `test_result_precheck_stops_when_the_clean_tree_query_fails` and `test_previous_head_proof_selects_tests_by_exact_id`. Each is red against bccb2dea with this head's test source, by exact id: `Ran 1 test`, failures only, no error. Each is green on 024ba0eb (validation.md).

Consolidation for the caps. Round 1 left 419 of 420 lines outside `tests/` and 520 of 520 under `tests/`:
- **Production:** 420 of 420.
  - Denser wording for the header's selector paragraph and for two comments.
  - `Path.write_text` for the two record writes.
  - One-line `if …: return` forms in the prechecker.
  - The red predicate as a lambda beside `digest` and `ran`.
- **Tests:** 517 of 520, every case kept.
  - `test_precheck_selector_proof_requires_red_on_previous_head_and_green_on_head` is removed; the task does not name it. Its red-and-green and no-prune cases are in `test_previous_head_proof_requires_an_executed_failing_test`, and its exit-code checks are in the new exact-id test.
  - `test_precheck_records_the_local_review_as_deferred_by_default` becomes the healthy run of `test_precheck_records_failed_commands_as_not_ok`: the deferred record, no local-review run, and the shortcut line.
  - `test_precheck_secrets_mode_counts_and_never_prints_the_match` becomes the UTF-8 case of `test_result_precheck_decodes_or_refuses_utf16_before_the_secret_scan`: an exact count of 1, no matched text, and the input unchanged.
  - One `gated()` helper replaces four copies of the refuse-or-warn pair.
  - `PROOFS`, `SEL_A`, `SEL_B` and `BASE` are shared fixtures, and the one-line `hooks()` helper is inlined.
  - The existing dispatch fixtures' proofs now carry `previous_head`.

The audit's two orchestration findings are not this round's:
- **Finding 1, the stale precheck after the update-branch merge:** it goes to the owner task, as the ACCEPTANCE says. This round's proof is regenerated on 024ba0eb, after that merge.
- **Finding 5, the deferral:** this round answers it.

[memory:decision] T133 P1-5 a03 revise 1: result-precheck.sh proves a --check selector only by its exact unittest id (the one class defining the name; none or two is no proof), with Ran 1 test on both sides, and records id, previous_head and both counts in selectors[]. dispatch.sh reads a revise's check= repeated or comma-separated and refuses or warns about a requested proof whose previous_head differs from the latest revise's previous_head=. A failed git status exits 2 before any check.

## Not done yet

The evidence commit, the one push, CI on the final head, the Bot window and the RESULT `round=revise-1` (`precheck=3b06c13b3a5f582af38198b519387444e1ae07ccc56c46c1f79fcc90f8f97e82`, `task_copy=d8048ef5…`, `previous_head=bccb2deabdf95bc558add6a5e56e4405a6a61b43`).

cost: n/a
