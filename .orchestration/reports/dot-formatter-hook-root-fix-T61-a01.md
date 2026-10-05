# Report: dot-formatter-hook-root-fix-T61-a01

- **Worker and branch:** `claude-standard-dot-a005` in worker-c. Branch `chore/formatter-root-fix` from `origin/main` f8e22ba3, which is unchanged since.
- **PR:** #233, https://github.com/mryfmo/dotfiles/pull/233.
- **task_rev:** `f93ae279…`, matched.
- **Status:** ready_for_review. The final head is `7dff3a5c` (round 3); CI, `mergeable_state` and the thread state on that head are in the validation file.

## Commits

| # | SHA | Kind | Content |
|---|---|---|---|
| 1 | `45d44292` | tooling | Pins, `ruff.toml`, `.prettierignore`, hook, `agent-config.yaml` hooks block, generator plus its test, CI step, `make format` |
| 2 | `bd9a7995` | tooling | The ruff check passes `--config ruff.toml` (see "Findings during the format") |
| 3 | `e5648fa6` | **format only** | The output of `ruff format --config ruff.toml` and `prettier --write` on 46 tracked files (+1288/−2166). No other edits; no excluded path touched. |
| 4 | `ff37f41d` | review fix | `should_test` covers every formatted path; the hook reports a missing formatter (Codex P2, and P1 in part) |
| 5 | `b5084de5` | review fix | `plans/004` and `plans/005` are restored and listed in `.prettierignore` (Codex P2) |
| 6 | `772ff3c6` | review fix | The hook runs its formatters from each edited file's repository root; new hook tests (Codex P1) |
| 7 | `57021632` | review fix | All of `plans/` is excluded from prettier and restored to its `origin/main` text (Codex P2 on plans/001; supersedes the per-file exclusion from commit 5) |
| 8 | `ae806f37` | review fix | `.agents` is added to ruff's `extend-exclude`, as `.prettierignore` already had it (Codex P2 on ruff.toml) |

Commits 4–8 come after the format-only commit, because the Codex findings arrived on it and force-pushing is forbidden. Commit 3 stays pure formatter output. Commits 5 and 7 revert the formatter output for `plans/`, where it changed the meaning of command tables (see below). The net change to `plans/` against `origin/main` is zero.

## Chosen versions and the target-version derivation

- **ruff:** 0.16.10, the latest stable in `mise ls-remote ruff` (backend `aqua:astral-sh/ruff`).
- **prettier:** 3.9.9, the latest 3.x in `mise ls-remote npm:prettier`.
- **Lock entries:** generated with `mise lock ruff npm:prettier` in a scratch copy of the config. A TOML comparison shows only these two tools were added and no existing entry changed.
- **`target-version = "py312"`:** the lowest Python in the CI matrix. `uv run python` uses the image's `python3` (no `pyproject.toml`), and the runner-images readmes for the tags the jobs ran on give:
  - ubuntu-24.04 (ubuntu24/20260927.320): Python 3.12.3;
  - ubuntu-26.04 (ubuntu26/20260927.149): 3.14.4;
  - macos-14 (macos-14-arm64/20260831.0302): 3.14.7.

## Findings during the format (not in the task file)

1. **ruff's per-file config bypasses the root exclusions.** ruff discovers configuration per file, and `vendor/compactiondb` has its own `pyproject.toml` with `[tool.ruff]`. So the root `extend-exclude`, even with `force-exclude = true`, did not apply there, and the first format run rewrote 24 vendor files. I reverted them. CI and `make format` now pass `--config ruff.toml`, which makes the root configuration govern every file. In this repository, the global hook would format a vendor file under vendor's own config only if an agent edited one, which is forbidden anyway.
2. **The task's verbatim ruff check is not the right check.** `git ls-files '*.py' | xargs mise x ruff -- ruff format --check` without `--config` reports the 24 vendor files ("24 files would be reformatted"). The form CI runs, with `--config ruff.toml`, reports "37 files already formatted". Both outputs are pasted.
3. **prettier is not idempotent on `plans/005`.** A wrapped inline code span in a list item lost two columns of indentation per pass. That file is now excluded (Codex P2), and the rest of the tree is a fixpoint: a further pass of both tools changes nothing.
4. **`make format` already fails on `origin/main`.** Its pre-existing first line, `shfmt --indent 4 --space-redirects --diff .` (Makefile:157), runs the local shfmt over the whole tree and fails there too (exit 1, pasted). This PR changes no `.sh` file. The two new lines pass when run on their own (pasted).

## Codex Bot threads (I did not resolve any)

| Thread | Where | Disposition |
|---|---|---|
| P1 Install the formatter binaries before invoking this hook | hook | **Partly fixed in `ff37f41d` and `772ff3c6`.** A missing ruff, prettier or git is now reported (`ruff is not installed; run \`mise install --locked\``) with a non-blocking exit and no traceback. **The root fix is outside my allowed files.** `make update` (Makefile:71-72) installs only `node npm:ccstatusline npm:ccusage npm:pnpm`, so existing machines get ruff and prettier only through a full `mise install --locked` (`install/common/mise.sh` does that at first setup). **Proposed follow-up:** add `ruff npm:prettier` to the `make update` install line. |
| P2 Preserve literal command text in Markdown tables | plans/004 | fixed in `b5084de5` (plans/004 and 005 restored and excluded), then superseded by `57021632` (all of `plans/`). |
| P2 Run the formatting check for every formatted path | test.yaml | fixed in `ff37f41d` (`should_test` now also matches root-level `*.md`, `plans/`, `docs/`, `.github/*.md`, `ruff.toml` and `.prettierignore`). `.orchestration/` still skips, as T60 requires. |
| P1 Resolve formatter configuration from the edited repository | hook | fixed in `772ff3c6` (the hook runs from each file's git root; tests cover it). This bug reformatted this task's own `.orchestration` reports in the main checkout during the session. |
| P2 Exclude `.agents` from direct Ruff formatting | ruff.toml | fixed in `ae806f37`. The task's ruff exclusion list omitted `.agents` while the `.prettierignore` list included it. A probe file under `.agents/worklog` is now excluded, both with `--config ruff.toml` and with automatic config discovery. |
| P2 Preserve the removal-scan command in this table | plans/001 | fixed in `57021632`. **My first content check missed this case:** it discarded `|` characters, so prettier padding a regex alternation's `|` inside a table code span was invisible to it. A targeted scan for table rows whose code spans contain `|` (pasted) found exactly plans/001, 003, 004 and 005. All of `plans/` is now excluded and restored, and no such row remains in a prettier-managed file. |

## Tests touched

- `tests/unit/test_generate_agent_configs.py`: new `test_claude_settings_render_the_format_hook_from_its_path`.
- `tests/unit/test_format_edited_files_hook.py` (new):
  - `test_formatters_run_from_the_edited_files_repository_root`
  - `test_a_missing_formatter_is_reported_without_a_traceback`
- No supply-chain or workflow test needed changes; the full suite passes (712 tests, OK).

## Operator notes after merge

- **Install the formatters:** run `mise install --locked` (or `make update` once the follow-up lands) on each machine, so the hook finds `ruff` and `prettier`. Until then the hook prints the instruction on each Python or Markdown edit.
- **The installed hook is still the old one** until `make update` applies the new hook. Until then, agent edits to `.md`/`.py` are still reformatted by `npx prettier@2`. To avoid that, this task wrote its artifacts with shell heredocs.

## CompactionDB

```
cd ~/Workspace/dotfiles && python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content 'T61 (operator 2026-10-03): the repository is formatted once with ruff (line length 120) and prettier 3, both pinned in the mise config; the Claude formatter hook runs only `ruff format` and `prettier --write` from the pinned tools, and CI checks formatting, so an agent'"'"'s edit never produces unrelated diff lines. Vendored and record paths are excluded.'
d7c79b1d-bad6-491b-b0f1-e77c4b54e164
```

[memory:decision] T61 (operator 2026-10-03): the repository is formatted once with ruff (line length 120) and prettier 3, both pinned in the mise config; the Claude formatter hook runs only `ruff format` and `prettier --write` from the pinned tools, and CI checks formatting, so an agent's edit never produces unrelated diff lines. Vendored and record paths are excluded.

## Artifacts

- validation: `.orchestration/validation/dot-formatter-hook-root-fix-T61-a01.md`
- sandbox: `.orchestration/sandboxes/dot-formatter-hook-root-fix-T61-a01.md`
- learning: `.orchestration/learning/dot-formatter-hook-root-fix-T61-a01.md`
- autoskill: `.orchestration/autoskill/runs/dot-formatter-hook-root-fix-T61-a01.md`

cost: n/a (no subagents; the runtime does not expose session totals)

## Revise round 1 (task_rev `c4c2fb43…`)

All three fixes are in one commit, `0827371f`:

1. **Formatter installs.** `make update` (Makefile:72) and first setup (`install/common/mise.sh:108`) now install `ruff npm:prettier`, which addresses Codex P1 "Install the formatter binaries" and audit P1 on 45d44292. Tests that pin those exact install lines were updated and are named here: `tests/unit/test_update_agent_assets_ua_core.py`, `tests/install/common/lifecycle.bats` (the expected call list, the failure-injection argument and the grep), and `tests/install/common/mise.bats`. Any other mention of the old install line now returns 0 hits (grep pasted).
2. **`CLAUDE.md`.** It is restored to its `origin/main` bytes (`git diff --quiet` pasted) and listed in `.prettierignore` with the reason: the CompactionDB-managed block would otherwise ping-pong with `vendor/compactiondb/install.py`.
3. **Hook.** `repository_root` now uses `rstrip("\n")` (audit P3 on 772ff3c6).

The format-only commit `e5648fa6` is untouched. After the push, `main` moved to 3915e327 (#232, `.orchestration` only), so `gh pr update-branch 233` produced `3da4cfad`.

### Codex threads, complete list (I did not resolve any)

| Thread | Fix commit |
|---|---|
| P1 Install the formatter binaries before invoking this hook | `ff37f41d` (missing-tool message) and `0827371f` (installed by `make update` and setup) |
| P2 Preserve literal command text in Markdown tables (plans/004) | `b5084de5`, then `57021632` |
| P2 Run the formatting check for every formatted path | `ff37f41d` |
| P1 Resolve formatter configuration from the edited repository | `772ff3c6` |
| P2 Preserve the removal-scan command in this table (plans/001) | `57021632` |
| P2 Exclude `.agents` from direct Ruff formatting | `ae806f37` |
| P2 Check formatting for unlisted source paths (new on 0827371f) | **not fixed in this round** (round scope fixed at three fixes). It is valid: nested `.md` files such as `.github/ISSUE_TEMPLATE/*.md` and `.py` files in new directories do not set `should_test`. **Proposed fix:** match `(^\|/)[^/]+\.(py\|md)$` outside `.orchestration/` in the filter, or make the formatting step unconditional. |
| P2 Resolve the formatter tools without the untrusted project config (new on 0827371f) | **not fixed in this round.** It is valid: the repo root has a `mise.toml`, and `mise x` refuses while it is untrusted. **Proposed fix:** call the `ruff` and `prettier` shims from `PATH` in `make format` instead of `mise x`. |
| P2 Force the hook to honor root Ruff exclusions (new on 3da4cfad) | **not fixed in this round.** It is valid, and it is the limitation named in "Findings during the format" item 1: an edit to a `vendor/compactiondb` file is formatted under vendor's own `pyproject.toml`. **Proposed fix:** the hook already resolves each file's repository root, so it can pass `--config <root>/ruff.toml` to `ruff format` when that file exists. |

- **Final head:** `3da4cfad`.
  - **CI:** all checks pass (13 pass, `nix` skipped).
  - **Branch:** up to date with `main` (3915e327).
  - **`mergeable_state`:** `blocked`, solely by the nine unresolved Codex threads above: six fixed, and three new P2s on the last two heads, proposed as follow-ups.

## Revise round 2 (task_rev `47e7df20…`)

The three Codex P2 findings from round 1 are fixed in one commit, `74ade52f`:

| Thread | Fix in `74ade52f` |
|---|---|
| P2 Check formatting for unlisted source paths | `should_test` is set by any changed `*.py`/`*.md` outside `.orchestration/` (`(^\|/)[^/]+\.(py\|md)$` after filtering out `^\.orchestration/`), plus the existing directory and config entries. `.orchestration`-only diffs still skip. **Additional finding:** the step runs `set -euo pipefail`, so the old `git diff \| grep -Eq` pattern could SIGPIPE the writer when `grep -q` exits early, and report a false negative on a long file list. The filter now uses no pipe: a captured list, a `grep -v` into a variable, and a here-string test. I checked it under `pipefail` with a 20,000-line `.orchestration` list plus `README.md` (true), nested `.github/ISSUE_TEMPLATE/bug.md` (true), `newdir/tool.py` (true), `.orchestration`-only (false) and `LICENSE` (false). |
| P2 Resolve the formatter tools without the untrusted project config | `make format` calls `ruff format --config ruff.toml --check` and `prettier --check` from `PATH` (the mise shims that `make update` installs since `0827371f`), not `mise x`. |
| P2 Force the hook to honor root Ruff exclusions | When `<repository root>/ruff.toml` exists, the hook passes `--config <root>/ruff.toml` to `ruff format`. `tests/unit/test_format_edited_files_hook.py` now creates a root `ruff.toml` and asserts the flag in the fake ruff's recorded arguments. |

**Codex review of the new head.** Codex reacted 👍 to PR #233 (`chatgpt-codex-connector[bot] +1 2026-10-03T05:02:35Z`, after the push of `74ade52f`). No review and no inline comment exist for `74ade52f`, so this head has no open finding.

**All Codex threads with their fix commits:**
- P1 Install the formatter binaries: `ff37f41d`, `0827371f`
- P2 Markdown tables, plans/004: `b5084de5`, then `57021632`
- P2 Formatting check for every formatted path: `ff37f41d`
- P1 Formatter configuration from the edited repository: `772ff3c6`
- P2 Removal-scan command, plans/001: `57021632`
- P2 Exclude `.agents`: `ae806f37`
- P2 Unlisted source paths: `74ade52f`
- P2 Untrusted project config: `74ade52f`
- P2 Hook honors root Ruff exclusions: `74ade52f`

None is open without a fix, and none was resolved by me.

## Revise round 3 (task_rev `d0836233…`)

- **Finding (audit P2 on `74ade52f`):** `git diff --name-only` quotes non-ASCII paths by default (`core.quotePath`). A changed `.github/ISSUE_TEMPLATE/日本語.md` therefore reached the filter as `".github/ISSUE_TEMPLATE/\346\227\245\346\234\254\350\252\236.md"`, which matched neither alternative.
- **Fix:** commit `7dff3a5c`. The filter reads the paths with `git -c core.quotePath=false diff --name-only "${diff_range}"`. The here-string logic from `74ade52f` is unchanged, with no pipe.
- **Reproduction** (`$TMPDIR/t61-quote.sh`, pasted in the validation file):
  - It needs git's default config (`GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1`), because this host's global config already sets `core.quotePath=false`. That setting hid the bug on the first local attempt; the attempt is also pasted.
  - With the defaults, the plain command gives the quoted path and **`should_test=false`**. `git -c core.quotePath=false` gives the raw path and **`should_test=true`**.
- **`should_nix` check left unchanged:** it also runs `git diff --name-only`, but it only matches the ASCII paths `flake.nix`, `flake.lock` and `nix/`.
- **CI on `7dff3a5c`:** all checks pass (`nix` skipped), and the branch is up to date with `main` (3915e327).
- **Codex review of `7dff3a5c`: not observed.** I polled 25 times at 60-second intervals after the push (05:27:02Z–05:51:34Z). In that window there was no review on `7dff3a5c`, no inline comment and no new reaction. The PR's only 👍 is `chatgpt-codex-connector[bot] +1 2026-10-03T05:02:35Z`, which predates this push (it belongs to `74ade52f`). GitHub keeps one reaction per user and content, so a "no findings" verdict on this head may leave no new trace. I therefore **cannot confirm** that Codex completed a review of `7dff3a5c`. I did not post an `@codex review` request on the PR; that is the orchestrator's call.
- **Threads:** nine, all with fix commits (see round 2). The orchestrator has resolved all nine (GraphQL `resolved=true`, pasted). No new thread on `7dff3a5c`.
