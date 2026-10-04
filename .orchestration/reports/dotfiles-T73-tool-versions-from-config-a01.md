# Report: dotfiles-T73-tool-versions-from-config-a01

- **Worker and branch:** `claude-standard-dot-a005` in worker-c, branch `chore/tool-versions-from-config` from `origin/main` 523fda06.
- **task_rev:** `e4368247…`, matched.
- **PR:** #241, https://github.com/mryfmo/dotfiles/pull/241.
- **Commits:**
  - `60688d49`: the change.
  - `b63c6b7d`: `gh pr update-branch` with `main` 3a0816e6 (T89).
- **Final head:** `b63c6b7d`.
  - **CI:** green; 13 pass including CodeRabbit, and `nix` is skipped.
  - **Statusline smoke:** the install and network-denied smoke steps succeeded on all four test jobs, macos-14 included, so the `tomllib` read works on every runner.
  - **`mergeable_state`:** `clean`.
  - **Branch:** up to date with `main` 3a0816e6 (behind_by=0).

## Change (no pin value changes)

1. **`.github/workflows/test.yaml`:**
   - `install --locked npm:ccstatusline@2.2.30 npm:ccusage@20.0.24` becomes `install --locked npm:ccstatusline npm:ccusage`.
   - `where npm:<tool>@<version>` becomes `where npm:<tool>`.
   - Both run with `mise -C "${RUNNER_TEMP}/statusline-mise"` against the copy of `home/dot_mise/config.toml` and `mise.lock` that the job already makes, so mise resolves the configured versions. The neighbouring comment now says every version comes from that config.
2. **`scripts/check-statusline-tools.py`:**
   - `EXPECTED_VERSIONS` is replaced by `expected_versions()`. It reads `tools["npm:ccstatusline"]` and `tools["npm:ccusage"]` from `home/dot_mise/config.toml` with `tomllib`.
   - The path is `Path(__file__).resolve().parents[1]`, so the CI smoke (`python3 scripts/check-statusline-tools.py` from the checkout, under `unshare --net` or `sandbox-exec`) needs no new argument.
3. **`tests/unit/test_statusline_tools.py`:**
   - `EXPECTED_TOOLS` is read from the same config.
   - The workflow-literal tokens are replaced by the name-based install line and the two `where npm:<tool>)"` lines, with the node install still ordered before the tool install.
   - It asserts that the workflow contains neither `ccstatusline@` nor `ccusage@`.
4. **`tests/unit/test_aws_cli_acquisition.py`:**
   - `FINGERPRINT` is read from the installer with `^readonly AWS_CLI_FINGERPRINT="([0-9A-F]{40})"$`. The variable is **`AWS_CLI_FINGERPRINT`** (aws_cli.sh:14), read the same way as `AWS_CLI_VERSION`.
   - The task named only line ~13. The literal also appeared in four fake-`gpg` fixtures (lines 86, 115, 187, 278). They now substitute it: the raw-string fixtures use `@FINGERPRINT@` with `.replace(…)`, following the existing `@AWS_CLI_VERSION@` pattern, and the plain string uses an f-string. Without this, the validation grep could not be clean.

## Notes

- **CI interpreter:** `tomllib` needs Python 3.11 or newer. The CI smoke uses the runner's `python3`: under `sudo unshare` on Ubuntu that is the system Python 3.12 or later. On macos-14 it is the image's PATH `python3`. CI on the final head confirms both: the smoke step succeeded on ubuntu-24.04, ubuntu-26.04 and macos-14 (validation file).
- **Key id:** the fake `gpg` `pub:` lines still carry the key id `A6310ACC4672475C`, the last 16 hex digits of the fingerprint. The installer validates only `fpr`, and the task's grep targets the fingerprint prefix, so I left the key id literal. If the key ever rotates, that fixture value would go stale but nothing would check it.
- **ruff check:** `ruff check` reports findings in the three Python files (EXE001, I001, PLW1510), all on lines that already existed. CI runs only `ruff format --check`, which passes.

## Codex bot

| Head | Result |
|---|---|
| `60688d49` | 👍 00:45:32Z |
| `b63c6b7d` (final) | 👍 00:49:55Z |

There are no threads.

## CompactionDB

```
cd /home/moriya/Workspace/dotfiles && python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content 'dotfiles-T73 (operator 2026-10-03): ccstatusline/ccusage versions are read from home/dot_mise/config.toml by the statusline smoke script, its unit test and the CI workflow (no `@version` literals), and the awscli fingerprint test reads the installer; pins have one declaration.'
b02665cb-ccee-482d-9ff8-c933438c2de6
```

[memory:decision] dotfiles-T73 (operator 2026-10-03): ccstatusline/ccusage versions are read from home/dot_mise/config.toml by the statusline smoke script, its unit test and the CI workflow (no `@version` literals), and the awscli fingerprint test reads the installer; pins have one declaration.

## Artifacts

- validation: `.orchestration/validation/dotfiles-T73-tool-versions-from-config-a01.md`
- sandbox: `.orchestration/sandboxes/dotfiles-T73-tool-versions-from-config-a01.md`
- learning: `.orchestration/learning/dotfiles-T73-tool-versions-from-config-a01.md`
- autoskill: `.orchestration/autoskill/runs/dotfiles-T73-tool-versions-from-config-a01.md`

cost: n/a (no subagents, no model-driven runs; the runtime does not expose session totals).
