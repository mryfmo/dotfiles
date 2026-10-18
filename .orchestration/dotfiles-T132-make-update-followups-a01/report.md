---
task_id: dotfiles-T132-make-update-followups-a01
seat: claude-standard-dot-a011
branch: tools/make-update-followups-a01
base: 99a4a80f (origin/main at dispatch and at this report)
code_commit: 09414805 (the test commit eedf0db9, the fix cc01fdb4; the worker review P1 round: the test commit 7eb9438f and the fix 09414805)
pr: 405
task_sha256: 6f4511ffb314dfd9ab498472402163188af10985f340476544d69e23e0480fed
---

# Report: dotfiles-T132-make-update-followups-a01

- Seat: `claude-standard-dot-a011` in `.claude/worktrees/worker-d`, on a fresh branch `tools/make-update-followups-a01` from `origin/main` `99a4a80f` (`--no-track`). The branch `portability/followup-a01` was pushed and clean before the switch, and it stays untouched.
- Task file: dispatched 2026-10-17T23:45:11Z at `6f4511ff…`, copied byte-identical to `task.md`. The task-consistency check passes, and both premises re-run unchanged against `origin/main` (validation §1, §1a and §2).
- Timeline: the code, the tests, the push and draft PR #405 came before the STOP of 08:51 JST (PING at 23:57:01Z). The STOP arrived at the turn end. Nothing ran after it until T133 item 0 (04:22:16Z) told this seat to commit these records, push and mark #405 ready.

## What changed

1. **`scripts/update-agent-assets.sh`, `update_omp()` only (6 added lines)**: after the tarball's sha256 is verified and before `npm install -g --prefix "${HOME}/.local"`, a symlink at `${HOME}/.local/bin/omp` whose target is missing (`[ -L ] && [ ! -e ]`) is removed with a plain `rm` of that one path. One line names the link and its former target (`readlink`). A live link, a regular file or a directory is left alone, and npm handles it as before. The removal comes after verification, so a failed download or checksum never touches the link.
2. **`scripts/upgrade-tools.sh`, the uv phase only (30 added and 2 removed lines, with the P1 round)**: a new `manifest_wheel_pin <tool>` prints the manifest `pin` of an asset that has a `.whl` URL among its keys (today `assets.hcom.files`), and nothing otherwise. `upgrade_uv_tools` reads `uv tool list` (tool lines are `<name> v<version>`; entry points `- <command>` are skipped) and upgrades each tool with `uv tool upgrade <name>`, except the ones the manifest pins from a wheel. For each skipped tool it prints `skip: <tool> (manifest pins <version> from a wheel)`. One failed upgrade no longer stops the others and still fails the phase, which stays `run_optional_phase`. An unreadable manifest fails the phase instead of upgrading hcom from the index.
3. **Tests (158 lines, with the P1 round)**: `tests/unit/test_update_agent_assets.py::test_update_omp_removes_only_a_dangling_symlink_at_the_install_path` covers (a) a dangling link, which is removed, the install succeeds and stdout names the old target; (b) a live link, which is not removed, npm fails with `EEXIST`, and the link still points where it did; (c) no link, where the install succeeds and nothing is reported. The shared fixture npm now fails with `EEXIST` over a symlink, as npm does over a bin link it does not own. The new module `tests/unit/test_upgrade_tools.py` has a fake uv that records argv and a fixture manifest:
   - `test_a_tool_the_manifest_pins_from_a_wheel_is_skipped_and_the_others_upgraded` (a)
   - `test_without_a_wheel_pin_every_tool_is_upgraded_and_one_failure_fails_the_phase` (b, plus failure aggregation)
   - `test_an_empty_tool_list_upgrades_nothing` (c)
   - `test_the_repository_manifest_pins_hcom_from_a_wheel_at_the_rendered_pin` (the reader against the real manifest equals the rendered `HCOM_PIN_VERSION`, and omp gives nothing)
4. **The worker review's P1 round (`7eb9438f` red, `09414805` fix)**: uv colours each `uv tool list` tool line when `FORCE_COLOR` or `CLICOLOR_FORCE` is set, and herdr-agents exports both in every pane it creates, so the phase read `\e[1mhcom` as a tool name. The phase now runs `uv tool list --color never`. The fake uv colours its tool lines under those variables unless it is given `--color never`, and every uv-phase test sets them, as herdr panes do. The `shortcut:` comment of the manifest reader now names its real limit: unquoted block style.

## VERIFY

- **VERIFY 1** (validation §3): the key is `assets.<name>.files`, the per-platform URLs, which end in `.whl` only for hcom. `upstream` is the PyPI project page (`https://pypi.org/project/hcom/0.7.30/#files`) and does not end in `.whl`, so the task's wording "a `.whl` upstream" is read as "a `.whl` file URL". `pin` gives the version. Shell scripts in this repository consume constants rendered from the manifest and never parse it. Rendering a new constant would change the manifest or the renderer, which is out of scope. So `manifest_wheel_pin` reads the manifest's block style with `awk` (no new dependency), declared as a `shortcut:` comment, and the fourth test pins it to the rendered constant. No fallback list was needed.
- **VERIFY 3** (validation §12): `uv tool upgrade hcom` exits 1 with `Distribution not found at: file://<darwin-user-temp>/hcom-0.7.30-py3-none-macosx_11_0_arm64.whl`. uv's receipt names the deleted temporary wheel, which is the defect PR #398 addresses. hcom is the only uv tool on this machine. `uv tool list` prints "No tools installed" on stderr with an empty stdout (§12a).

## The Check

- `uv run python -m unittest tests/unit/test_update_agent_assets.py tests/unit/test_upgrade_tools.py -v`: green, all 9 tests, with a validation-only `mktemp` shim (§7). Without the shim, inside the Claude sandbox, the command fails 15 subtests, every one with `mkdtemp … Operation not permitted`. That is because macOS `mktemp -d` without a template ignores `TMPDIR`, and the Darwin user temp directory is denied (§5). The same module on untouched `origin/main` fails 12 subtests the same way (§6). The four `test_upgrade_tools` tests pass without the shim. The shim lives only in the seat's scratchpad. CI runs unsandboxed on ubuntu-24.04 and macos-14 and is the authority.
- Red: on the test commit `eedf0db9` the new tests fail for the expected reasons: npm `EEXIST` over the dangling link, `['tool upgrade --all']` instead of the per-tool calls, and `manifest_wheel_pin: command not found`. On `7eb9438f` the phase calls `tool upgrade \x1b[1mhcom` (§7). The 15 `upgrade` tests of `test_runtime_health.py` stay green at the head (§7).
- `shellcheck -x` and `shfmt --indent 4 --space-redirects --diff` are clean on both scripts, and `ruff format --check` and `ruff check` are clean on both test modules (§8). `make render-check` reports nothing generated changes (§9).
- Caps (§10): `scripts/update-agent-assets.sh` 6 changed lines and `scripts/upgrade-tools.sh` 32 (cap 40 each); `tests/` 158 (cap 160). Scope (§11): one hunk in `update_omp`, and three in `upgrade-tools.sh` around `upgrade_uv_tools`. git labels the first of those with the preceding function `upgrade_mise_tools`, because `manifest_wheel_pin` is inserted just before `upgrade_uv_tools`.

## Completion clause, declared

- Rebase: the a02 follow-up PR (`tools/assets-hcom-followup-a02`) is not open yet, because PR #398 is still open, and `origin/main` has not moved since dispatch (`99a4a80f`). The rebase the task asks for is therefore still pending on that merge. It happens before acceptance, and a textual conflict is a `PONG status=blocked`.
- Out of the task's files: `README.md:194` still says "Homebrew, `uv tool upgrade --all` and GitHub CLI extensions take their newest release". That sentence is now one notch inexact: uv tools are upgraded one by one, and wheel-pinned ones are skipped. README is not in `allowed_files`, so it is left for the orchestrator.

## Review, hook, cost

- Worker-side independent review: the first run was stopped by the STOP before it reported. The second run, one round on `cc01fdb4` by a fresh read-only subagent, returned `Verdict: incorrect` with one P1 (forced colour), fixed in `7eb9438f`/`09414805` and re-derived by the worker before the fix. It also raised two P3, both declared: the manifest reader's limits (quoted values; any `.whl` line in the asset's block), named in the `shortcut:` comment; and `manifest_wheel_pin` is a helper beside `upgrade_uv_tools`, called only from it, which the threat_table row's wording ("only in upgrade_uv_tools") does not name. Files: `dotfiles-T132-make-update-followups-a01-worker-crit.json` and receipt `dotfiles-T132-make-update-followups-a01-worker-review-receipt.md`. This fix round is the one worker-side round.
- No Understand-Anything hook prompt fired, and no Plan Mode was used.
- cost: n/a (the runtime exposes no token or cost figure to the seat).
- CompactionDB: one decision added in this worktree's store before completion, id `2a3bde5d-7630-493b-9ef7-03b3d8b351d0` (validation §14).
