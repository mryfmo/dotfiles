# Report: dotfiles-T104-pins-2026-10-06-a01

- **PR:** #290, branch `pins/upgrade-2026-10-06` on base `origin/main` `ca5d28ec`.
- **Diff head:** `8c4a34e619988cb1ef6293b11e3b0ea96449288c`, one commit.
- **Final head:** `bd0327a01789148f65c4f0a8c93ccce216d387b3`. This is the `gh pr update-branch` merge of `main` `b3f0bc61`: #289, the boundary commit, `.orchestration` files only, which merged cleanly.
- **task_rev:** `sha256:8598b22b…b1b739d5522d`, verified.
- **Kind:** pins only.

## What changed

1. **The diff, applied verbatim.** `git apply --index <main checkout>/.orchestration/validation/pins-2026-10-06.diff` returned rc=0 and staged exactly the seven allowed files, 57 lines added and 57 removed: `home/dot_agents/agent-config.yaml`, `home/dot_mise/config.toml`, `home/dot_mise/mise.lock`, `install/common/mise.sh`, `install/ubuntu/common/aws_cli.sh`, `scripts/lib/installer-pins.sh` and `setup.sh`.
2. **The pins:**
   - mise v2026.9.14 → v2026.9.16
   - aws-cli 2.37.4 → 2.37.5
   - chezmoi: the bootstrap pin 2.70.4 (in `setup.sh` and `installer-pins.sh`) and the mise pin 2.72.2 → 2.73.0
   - dotenvx 2.30.0 → 2.31.1
   - hugo-extended 0.166.0 → 0.167.0
   - claude-code 2.1.288 → 2.1.289
   - codex 0.160.0 → 0.160.1
   - ccusage 20.0.24 → 20.0.26
   - pnpm 12.7.0 → 12.8.1
   - `mise.lock` entries to match.
3. **Renderer:** `make render-check` is clean. The rendered installer pin lines in the diff (`mise.sh`, `aws_cli.sh`, `installer-pins.sh`, `setup.sh`) agree with the manifest, so the diff and the renderer don't disagree.
4. **Tests:** no file under `tests/**` changed, because no test asserts these live values. The old values that remain are self-contained fixtures:
   - **`tests/unit/test_generate_agent_configs.py`:**
     - lines 260–279: a synthetic `chezmoi-bootstrap` asset with pin `2.70.4`, checked against its own rendered output;
     - line 781: a comment recording the hashes Codex 0.160.0 reported (a historical fact; hook trust is not touched).
   - **`tests/unit/test_release_asset_pins.py`:**
     - lines 72, 131, 140–157 and 191–194: a fake release listing and fake HTTP dates for mise v2026.9.14 and aws-cli 2.37.4;
     - line 104: a fixture manifest whose comment says "Fixed pins keep the fixture independent of the live manifest".
   - **`tests/unit/test_validate_agent_assets.py`:** line 696, a fake `setup.sh` checked for hard-coded versions.

   `make unit-test` passes with no test change. The bats suites (`tests/install/**`) contain none of the old values; they run in CI.
5. **No other change.** In particular there's no hook-trust edit; the Codex 0.160.1 hash check is the orchestrator's post-deploy step.

## Validation

- `make render-check`: clean.
- `make unit-test`: 917 tests, OK (skipped=1).
- The validator: rc=0.
- **CI:** green on the diff head, and green on the final head (16 checks pass; `mergeable_state` is `clean`).
- **Bot wait:** it ended on the Codex quota notice at 00:44:41Z, as the task instructs.
- **Codex security review of `8c4a34e`:** completed with no review or inline comment.
- **Independent review:** a subagent found no findings (`-worker-crit.json` and the receipt, `review_outcome: approved`).
  - **Its one note:** comments still cite Codex rust-v0.160.0. That is left to the orchestrator's post-deploy hook-hash check, as the task says.

[memory:decision] dotfiles-T104 (orchestrator 2026-10-06): the pending `make upgrade` pin diff of the canonical clone travels as one pin PR with synced test assertions; the orchestrator verifies the Codex hook hashes after deploy.

CompactionDB: recorded as `924aedfd-d0da-4af7-916b-f136112529df`; the command and readback are in the validation file.

- **Not run:** `make update`, `make upgrade`, `make apply`.

cost: n/a
