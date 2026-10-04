# Report: dotfiles-T71-generator-multi-target-a01

- **Worker and branch:** `claude-standard-dot-a005` in worker-c, branch `feat/generator-multi-target` from `origin/main` 312fef3f.
- **task_rev:** `561b9425…`, matched.
- **PR:** #249, https://github.com/mryfmo/dotfiles/pull/249.
- **Commits:**
  - `1ea56252`: the change.
  - `383ebbae`: `fixed:` Codex P2, conflicting render mappings.
  - `001affb1`: update-branch merge.
  - `3ecb4876`: `fixed:` Codex P2, canonical render paths.
- **Final head:** `3ecb4876`.
  - **CI:** green; 13 pass including CodeRabbit.
  - **Branch:** up to date with main f32f33a0.
  - **`mergeable_state`:** `blocked`, only by Codex P2 threads (3 fixed, 1 proposed `not-applicable`).

## Change

1. **`render_asset_constants`:**
   - `render:` is one `{file, constants}` mapping or a list of them. Each entry rewrites its own target file through the shared `outputs` map, so two entries or assets that render into one file stay consistent.
   - The regex is `^((?:readonly |declare -r )?NAME=)"[^"$`\\]*"$`.
   - Exactly-once is per (file, constant), and its message names the entry's file.
2. **`validate-agent-assets.py`:**
   - `LITERAL_VERSION_ASSIGNMENT` gains `declare -r ` as a prefix.
   - The `rendered` set is built from every entry.
   - Shape check: every entry must be a mapping with a string `file` and a non-empty `constants` mapping of string to string. Otherwise it fails with `assets.<name>.render entries must each be a mapping …`.
   - The scanned roots are unchanged (`install`, `scripts`); `setup.sh` is not added (T72).
3. **Tests:** 4 new ones, each failing against `origin/main` (validation file). Totals: 745 tests OK, `make render-check` exit 0 (configs up to date), and `make validate-agent-assets` exit 0.
4. **Untouched:** the manifest, every pin value, `setup.sh`, `scripts/lib/**`, `.github/**` and `Dockerfile`. No new CLI flag.

## Codex threads

| Thread | Head | Disposition |
|---|---|---|
| 4176358461 "Reject conflicting render mappings" | 1ea56252 | `fixed:383ebbae`. An assignment claimed by two different (asset, field) pairs fails validation. |
| 4176406485 "Normalize render file paths before detecting conflicts" | 001affb1 | `fixed:3ecb4876`. Render files must be canonical relative paths; `..`, `./` and absolute paths are rejected. |

| 4176458271 "Resolve symlink aliases before checking render conflicts" | 3ecb4876 | `fixed:f03505f3` (revise round 1): the conflict map is keyed on the resolved real path, and a fixture-symlink test covers it. |
| 4176458275 "Support valid unquoted declare -r assignments" | 3ecb4876 | proposed `not-applicable`. The mismatch predates this PR: on `origin/main` the validator already recognises an unquoted `readonly TOOL_VERSION=1.2.3`, while the renderer rewrites only double-quoted values and fails with "must assign … exactly once" (reproduced, validation file). It fails loudly, not silently; render targets use double quotes by convention. Aligning the unquoted forms is a separate change. |

- The first CI run on `1ea56252` failed in `public-bootstrap` on an upstream `cargo:eza` download ("transfer too slow"); the Ubuntu job was cancelled because of that failure. Both passed on `001affb1`.
- Totals: 756 tests OK, render-check exit 0, and asset validation exit 0 on `3ecb4876`.

## Notes

- **Stale base check in the task:** the task's base-check grep (`\bsk-` → 1) predates T91's final pattern, which has no `\b`. The base contains 312fef3f, verified by ancestry.
- **Empty `render:`:** an empty `render:` (falsy) is still skipped, as before.

## CompactionDB

```
cd /home/moriya/Workspace/dotfiles && python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content 'dotfiles-T71 (operator 2026-10-03): `generate-agent-configs.py` renders one asset pin into several target files (`render:` accepts a list) and into `declare -r` assignments; `validate-agent-assets.py` recognises `declare -r` literals; the scanned roots stay `install/` and `scripts/` until T72 adds the bootstrap asset.'
ae8fe450-a4a4-46f5-be5e-5c72fc52220f
```

[memory:decision] dotfiles-T71 (operator 2026-10-03): `generate-agent-configs.py` renders one asset pin into several target files (`render:` accepts a list) and into `declare -r` assignments; `validate-agent-assets.py` recognises `declare -r` literals; the scanned roots stay `install/` and `scripts/` until T72 adds the bootstrap asset.

## Artifacts

- validation: `.orchestration/validation/dotfiles-T71-generator-multi-target-a01.md`
- sandbox: `.orchestration/sandboxes/dotfiles-T71-generator-multi-target-a01.md`
- learning: `.orchestration/learning/dotfiles-T71-generator-multi-target-a01.md`
- autoskill: `.orchestration/autoskill/runs/dotfiles-T71-generator-multi-target-a01.md`

cost: n/a (no subagents, no model-driven runs; the runtime does not expose session totals).

## Revise round 1 (task_rev `166c6282…`): commit `f03505f3`

1. **Symlink aliases (audit P2, Bot 4176458271):** fixed. The render conflict map is keyed on `(ROOT / file).resolve()`, so two canonical names that reach one file through a symlink collide. The error names the earlier path. A test uses a real symlink in the temp tree, and it fails on `3ecb4876`.
2. **Evidence, the symlink check:** the pasted `git ls-files -s | awk … | grep '^(install|…)'` could not match. It is replaced by `git ls-files -s install scripts setup.sh | awk '$1 == "120000"'` with its real output: none of the 50 entries is a symlink.
3. **Evidence, summary labels:** the final-head `make render-check` and `make validate-agent-assets` (and the unit tests) are now pasted as complete verbatim output.

- **Totals:** 757 tests OK on `f03505f3` (validation file has the merge-head run), render-check exit 0, validate-agent-assets exit 0.
- **Round-1 head:** `c7b5fb3d`, the update-branch merge of main 0ea5948b (T94).
  - **CI:** green; 13 pass including CodeRabbit.
  - **`mergeable_state`:** `clean`.
  - **Branch:** up to date.
  - **Codex:** 👍 at 07:18:42Z, with no new threads.

## Revise round 2 (task_rev `e6025943…`): commit `ef4324d0`

1. **Audit P2, outputs keyed by unresolved path: fixed.**
   - Entries are grouped by the resolved real path and share the first-seen `ROOT / file` path as their output key, so a list that renders VERSION and SHA256 through an alias and VERSION through the target edits one snapshot. Writes follow the link.
   - Keying on the resolved path itself would have broken `--check`'s `relative_to(ROOT)` on hosts where the temp root is under a symlinked directory.
   - Test `test_entries_reaching_one_file_through_a_symlink_edit_one_snapshot` uses a fixture symlink. It fails on `c7b5fb3d` (two output keys for one real file) and passes now, with both constants in the one file after `write_outputs`.
   - The validator's `rendered` set stays on the canonical spelling.
2. **Totals:** 758 tests OK, render-check exit 0, validate-agent-assets exit 0.
3. **Final head:** `ef4324d0`.
   - **CI:** green; 13 pass.
   - **Branch:** up to date with main 0ea5948b.
   - **`mergeable_state`:** `blocked`, only by Codex threads.

| Thread | Head | Disposition |
|---|---|---|
| 4176631253 "Resolve rendered aliases when checking literal versions" | ef4324d0 | proposed `not-applicable`. It asks to key the literal-version check on the resolved path, which conflicts with the round-2 directive to keep the validator's `rendered` set on the canonical spelling. The failure mode is loud and safe: an assignment rendered only through an alias is reported as hard-coded, never silently skipped. The remedy is to name the real file in `render:`. |
| 4176458275 "Support valid unquoted declare -r assignments" | 3ecb4876 | proposed `not-applicable` (unchanged; a pre-existing mismatch that fails loudly). |
| 4176358461, 4176406485, 4176458271 | | `fixed:383ebbae`, `fixed:3ecb4876`, `fixed:f03505f3` |

