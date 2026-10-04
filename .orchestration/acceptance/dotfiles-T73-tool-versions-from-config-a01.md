# Acceptance: dotfiles-T73-tool-versions-from-config-a01

- **Decision:** ACCEPTED. PR #241 squash-merged to `main` as `40d9eb6c` (final head `b63c6b7d30dbe067c0c04afe6bd89497915c75bb`; substantive commit 60688d49; base `523fda06`, update-branch onto `3a0816e6`). Merged without `--delete-branch`; worker-c holds `chore/tool-versions-from-config`.
- **Worker:** `claude-standard-dot-a005` (worker-c). task_rev `e4368247…` matched. Pulled forward from Phase 3 as the only dispatchable task disjoint from the in-flight set.
- **Exemption declared:** acceptance and final integration; the orchestrator mutated no repository code.
- **Plan reference:** Phase 3, dotfiles-T73 (principle 3: one pin declaration).

## What was accepted (4 files, +35/−23)

- `test.yaml`: `install --locked npm:ccstatusline npm:ccusage` and `where npm:<tool>` against the copied exact config; no `@version` literal.
- `scripts/check-statusline-tools.py`: `expected_versions()` reads `home/dot_mise/config.toml` with `tomllib` relative to the script (the no-network smoke needs no new argument).
- `tests/unit/test_statusline_tools.py`: reads the same config; asserts the workflow carries no `ccstatusline@`/`ccusage@` literal; keeps the node-before-tools ordering check.
- `tests/unit/test_aws_cli_acquisition.py`: `FINGERPRINT` read from the installer's `AWS_CLI_FINGERPRINT`; four fake-gpg fixtures substitute it. The fake key id (last 16 hex digits) stays as unvalidated fixture data.
- No pin value changed. `grep` for the old literals over `.github scripts tests` is empty.

## Audit / Bot / sweep / gate

- Audit 60688d49 `correct` (no findings). Codex Bot thumbs-up on both heads, no thread. Sweep (head b63c6b7d): 5 items, 0 failure/warning, all dispositioned. Gate at b63c6b7d exit 0 with evidence copies, copies removed.

## CompactionDB

- Worker decision `b02665cb-ccee-482d-9ff8-c933438c2de6`; cited.
