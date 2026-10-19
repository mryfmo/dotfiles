---
task_id: dotfiles-T129-assets-omp-hcom-followup-a03
seat: claude-standard-dot-a009
branch: tools/assets-omp-hcom-followup-a03
pr: 428
round: 2
branch_point: 205fe85c19c03750fe3551bb96e084e9f0a676b6
base: 69dccca98aa772b790f366d63194228372a3c3b0
previous_head: 725b25bf731d4612d350c1da6642ecbdc385ede6
copy_commit: d3aab756
fix_commit: 9a8e2469
template_commit: 92d39f00
code_head: 92d39f00a18a3ceff72a48c9cded96f54e5cf0fe
task_sha256: cfa229f155b349f3ba02854f1440339e8bd481756ee657ee476e32afc90c844d
cost: n/a (the seat's token and time usage is not visible to the worker)
---

# Report: dotfiles-T129-assets-omp-hcom-followup-a03 (the assets lineage's owner of the seven lint baseline rows)

- **Seat and task file:** `claude-standard-dot-a009` in `.claude/worktrees/worker-c`, from the AGMSG-TASK of message 2442. The dispatched file and the branch copy are byte-identical (validation §1). The task-consistency check passes (§1a).
- **Branch:** a fresh `tools/assets-omp-hcom-followup-a03` from `origin/main` `205fe85c`, which carries the changed-scope lint of PR #415 (§2). `d3aab756` adds the task copy, and the first push carries it.
- **Scope:** the seven rows under `## Owned by dotfiles-T129-assets-omp-hcom-followup-a03` in `.orchestration/acceptance/dotfiles-T129-assets-omp-hcom-followup-a02.md`. §3 maps each row's hash to its line at `205fe85c`. Nothing outside those rows changes, except round 2's `mktemp` templates, which the revise ordered.

## Round 2 (the revise of message 2490, after the task-level audit of `725b25bf`)

| Check | Done |
|---|---|
| (1) The updater's temporary directory uses a `$TMPDIR` template, so its tests run inside the sandbox | `92d39f00` templates the six `mktemp` calls the in-sandbox tests reach: `update_omp` and `update_hcom` (`mktemp -d`), and `agmsg_state_snapshot` and the agmsg installer (`mktemp`, `mktemp -d`). Each becomes `mktemp [-d] "${TMPDIR:-/tmp}/update-agent-assets.XXXXXX"`. Other `mktemp` calls no test reaches stay as they were. Inside the sandbox, the Check passes 35 of 35 (§6), and `test_runtime_health` with the lint tests passes 69 of 69 (§7). The selectors are red there (§4r) and green there (§6b). |
| (2) The whole Check re-run inside the sandbox, with the PR creation, CI and Bot outputs | Validation §1 to §12 all ran inside the sandbox at `92d39f00`. §10 is the PR record and timeline, with round 1's creation output quoted. §11 is CI and §12 the Bot, for the latest pushed head, `725b25bf`. With one push, the new head's CI and Bot state are in the RESULT. |
| (3) The sandbox record rewritten | No row outside the sandbox in this round. Every refusal of both rounds is listed. Round 1's out-of-sandbox runs are stated as replaced history. |
| (4) The Bot-wait facts and `cost:` | See Completion. `cost: n/a` is in the front matter. |
| (5) No other code change; one push | `git diff 725b25bf 92d39f00` is the six template lines alone (§4a). |

- **The audit's P2 on the acceptance record's dispatch array** is the orchestrator's own record, outside this seat's edit boundary.
- **Red in round 2:** without a template, the base's `mktemp -d` fails inside the sandbox before a row's assertion is reached. So §4r applies only this round's template hunk to `205fe85c` (four hunks, 6+/6−, the patch's sha256 printed). There, all five selectors fail by assertion: `Moving` is printed, the strict check accepts the root, and the lint flags both `uname` case lines.

## Item 1: the owned rows

| Row id (line at `205fe85c`) | Fix in `9a8e2469` | Red-then-green test |
|---|---|---|
| `baseline:executable_remove-agent-asset:R1:ff2e0ca` (82, `path_has_prefix`: `[ "$1" = "$2" ] \|\| [[ "$1" == "$2/"* ]]`) | `path_has_prefix` folds both operands with `os.path.normpath` in `python3 -I -c` (a normaliser R1 names) and compares the folded strings. An optional `strict` refuses the prefix itself. For inputs already normalised, as every caller passes, the result is the old one, the root `/` included (`q + os.sep` keeps `//`). | `test_path_has_prefix_folds_both_paths_before_comparing`: a `..` that leaves the prefix (`/r/a/../b` under `/r/a`) is refused, and `/r/a/./b` under `/r/a/` is accepted. At `205fe85c` the first passes as a descendant. |
| `baseline:executable_remove-agent-asset:R1:5903a3c`, row 1 (101, `path_is_in_safe_root`: `[ "${candidate}" != "${root}" ] && path_has_prefix …`) | `if path_has_prefix "${candidate}" "${root}" strict; then`: the strict-descendant check runs on the folded paths, inside the normaliser. | `test_a_safe_root_is_not_inside_itself_in_any_spelling`, the `path_is_in_safe_root` subcases: a safe root spelled `<root>/` or `<root>/.` is not inside itself. At `205fe85c` both pass the string inequality and are accepted. |
| `baseline:executable_remove-agent-asset:R1:5903a3c`, row 2 (211, `is_plugin_data_path`, the same statement) | The same call. | The same test, the `path_has_prefix … strict` subcase on the plugin cache root, the call line 211 now makes. `is_plugin_data_path` folds its argument before the call, so no spelling reaches the call from outside. The inherited plugin tests (`test_crit_plugin_falls_back_to_data_path_but_not_config` and the others) stay green. |
| `baseline:update-agent-assets.sh:R1:1c780a5` (950, `[[ -z "${link}" \|\| "${link}" == /* ]] && part=…`, then a fold loop) | `normalize_node_path`, a new function that holds the old fold loop, resolves segments as Node's `path.resolve` does, the fold npm applies before its ownership check (bin-links check-bin). An absolute segment restarts the path. `resolved="$(normalize_node_path "${entry%/*}" "${link}")"` replaces the absolute-or-relative choice and the loop. | `test_npm_s_own_absolute_link_stays_under_a_home_with_a_trailing_slash`: npm's own link, written absolute, stays when `HOME=<home>/`. At `205fe85c` it moves aside to `omp.previous`. |
| `baseline:update-agent-assets.sh:R1:1d5afaf` (959, `[[ "${resolved}" != "${HOME}/.local/lib/node_modules/@oh-my-pi/pi-coding-agent/"* ]]`) | The package prefix is folded on the same line: `"$(normalize_node_path "${HOME}/…/pi-coding-agent")/"*`. **The defect:** the link was folded, but the prefix was compared as `HOME` spells it. With `HOME=<home>/`, npm's own link did not match `<home>//.local/…`, so `update_omp` moved it aside. | `test_npm_s_own_relative_link_stays_under_a_home_with_a_trailing_slash`: the same with npm's relative link. At `205fe85c` it prints `Moving …` and moves the link aside. |
| `baseline:update-agent-assets.sh:R2:851db69`, row 1 (274, `ensure_crit_cli`: `case "$(uname -s)/$(uname -m)" in`) | `case "$(uname -s)-$(uname -m)" in`, with `Linux-x86_64 \| Linux-amd64)` and the other patterns. **Deviation:** the operand is a platform pair, not a path, so no path normaliser applies. `realpath Darwin/arm64` would resolve against the working directory. The rewrite drops the path-shaped spelling instead. | `test_the_platform_cases_read_no_path_operand`: the lint, with no baseline, flags no `uname` line of the updater. At `205fe85c` it flags both case lines. Behaviour does not change, so the test is the lint. `test_runtime_health.py` (55 tests, §7) and the hcom platform tests still pass. |
| `baseline:update-agent-assets.sh:R2:851db69`, row 2 (982, `update_hcom`, the same statement) | The same rewrite. | The same test. `test_update_hcom_downloads_verifies_the_wheel_hash_and_installs_at_the_pin` drives all four platforms and an unsupported one through a `uname` fake. |

- **The baseline:** `scripts/lint-comparisons-baseline.tsv` loses exactly these seven rows (§4). The changed-scope gate exits 0. The two scripts have no hit even with no baseline. `--all` reports no stale row (§5).
- **Red at `205fe85c`:** each selector was run by exact id inside the sandbox, in a scratch worktree of `205fe85c` with round 2's template hunk only, using this branch's test modules (§4r). Each ran one test and failed by assertion, never by error. **Green at the code head:** §6b, also inside the sandbox.

## Check (§6 to §9)

- **The Check's tests:** `uv run python -m unittest tests/unit/test_remove_agent_asset.py tests/unit/test_update_agent_assets.py -v` exits 0 inside the sandbox, 35 tests (§6).
- **ShellCheck:** `shellcheck -x`, the CI form, is clean on both scripts (§8). shfmt is clean, and `/bin/bash` 3.2 parses both scripts.
- **ruff:** both test modules pass `ruff format --check`. `ruff check` reports EXE001 and I001 on `test_remove_agent_asset.py`'s header, the same two on `origin/main`.
- **Caps, `origin/main...HEAD` (§9):**
  - outside `tests/` and `.orchestration/`: 96 of 120;
  - under `tests/`: 73 of 400.

## Review

- **The one pre-push round** covered `205fe85c..9a8e2469`. It was a fresh, read-only general-purpose subagent of this seat, and returned `Verdict: correct` with no P0, P1 or P2 (the worker-crit JSON and its receipt).
- **Its three P3**, none of which needed a code change, so the code head stays `9a8e2469`:
  - **The behaviour-neutral rows:** the rewrites at lines 950 and 211 change no behaviour, so their tests are red through the neighbouring fix (row 959's HOME fold, and the `strict` call). No behavioural test can tell such a rewrite from its original. The lint gate is the guard instead: the rows are gone, so reverting either call site is an unbaselined hit in a changed file.
  - **One `python3` per guard check:** this costs speed only. The remover already starts `python3` for every `normalize_*` call, and the guard refuses when `python3` is missing.
  - **The absolute-segment check inside the normaliser:** informational. The reviewer judged it not to be lint evasion.

## Completion

- **PR:** #428, opened as a draft at 2026-10-19T06:30:25Z on `9a8e2469`. No `@codex review` comment is posted.
- **The Bot wait, as it happened (§10, §12):**
  - The PR stayed a draft until the orchestrator marked it ready at 2026-10-19T07:17:48Z.
  - The Bot does not review drafts. Round 1's RESULT (06:47:16Z) said `bot=none-in-15min`, but that window lay wholly inside the draft period, so it was no Bot wait. The audit's P2 holds.
  - After the PR was marked ready, Codex reviewed `1b3e0ee8`: the code review completed at 07:21:13Z and the security review at 07:21:49Z, both with `has_any_findings: false`. There are no review threads.
- **Open items:** no Bot thread, no advisory row and no open question. Any advisory P2 belongs to `dotfiles-T129-assets-omp-hcom-followup-a04`.
- **Observations:**
  - The untemplated `mktemp` calls no test reaches (`install_crit_release`, `update_codex_understand_anything` and `run_pinned_installer`) stay as they were. That keeps to the revise's "no other code change".
  - `normalize_node_path` matches a `path.resolve` reference under `/bin/bash` 3.2 for six inputs (§8a).
