# dotfiles-T77-harness-dead-code-a01 — report (status: ready_for_review)

- PR: #260 (https://github.com/mryfmo/dotfiles/pull/260), branch `chore/harness-dead-code`.
- Final head: `977bdf1f`, two commits on `origin/main` f6320f37:
  - `6f8b5683`: the deletions;
  - `977bdf1f`: `.chezmoiremove`, per the PONG decision.
- CI: all 13 checks pass. The branch is up to date with main (which is unchanged). `mergeable_state` is `blocked`: an unresolved Bot thread and the required review.

## Changes

1. **`herdr()` wrapper and `herdr-session`** (deleted):
   - removed the "Herdr in Ghostty" block from `home/dot_zshrc`, and `executable_herdr-session`;
   - `test_herdr_agents.py` loses the wrapper and session tests and their dead helpers (`install_zshrc_fakes`, `run_session_helper`, `run_zshrc_herdr`, `run_interactive_ghostty_herdr`, `materialize_agmsg_scripts`), the `HERDR_SESSION_SCRIPT` constant, and the now-unused `errno`, `pty`, `hashlib` and `tarfile` imports;
   - kept: `test_ghostty_config_does_not_auto_start_herdr_session` (it checks the Ghostty config) and the zprofile test.
2. **`agent-fanout`** (deleted):
   - `validate-agent-assets.py`: the fanout read and its two checks are gone;
   - `require-crit-review.py` and `test_require_crit_review.py`: the high-risk path is removed;
   - `test_runtime_health.py`: `test_agent_runs_are_private_and_ignored`, the four `test_agent_fanout_*` tests and the fanout half of `test_agent_launchers_do_not_hardcode_model_ids` are gone;
   - `generate-agent-configs.py`: the header now reads "(herdr-agents)", and `model-profiles.env` is regenerated (`make render-check` is clean);
   - `README.md`: there was no fanout mention, so nothing changed.
3. **CCR adoption-gate notice** (deleted):
   - `report_ccr_adoption_gates` and its `run_optional_phase` line in `scripts/upgrade-tools.sh`;
   - both CCR tests, and the two CCR cases in the upgrade fixture's `gh` stub.
4. **`HERDR_AGENTS_CODEX_PROFILE` alias** (deleted):
   - its shdoc `@arg` and alias sentences, and the branch in `resolve_worker_profile`;
   - the validator now checks `HERDR_AGENTS_WORKER_PROFILE` instead of the alias;
   - tests: the two `env.pop` lines, `test_codex_profile_env_override_wins_over_generated_profile` and `test_worker_profile_env_takes_priority_over_deprecated_codex_alias`.
5. **`enforce-uv.sh`**: excluded (Claude-boundary routing, T77b). Its two `"decision": "approve"` lines are the only remaining hits of the task grep's last pattern.
6. **`archive/CompactionDB-2.0.0.zip`** (deleted): the `agent-config.yaml` note now reads `local-fork-vendored-under-vendor/compactiondb`. Nothing reads the field.
7. **PONG decision**: `home/.chezmoiremove` lists `.local/bin/common/herdr-session` and `.local/bin/common/agent-fanout`, and `test_chezmoiremove_agmsg.py` pins them in `RETIRED`.

README: the Ghostty paragraph no longer describes the wrapper or the `exec zsh` advice. The worker-profile sentence drops the alias. In the verification paragraph, I removed the session-entrypoint and agmsg-delivery clauses, because the tests behind them were deleted.

## Codex Bot thread

- **4178373800** (P2, on 6f8b5683): "Remove retired executables from existing homes" → `fixed:977bdf1f`. Both paths are now in `home/.chezmoiremove`. The Bot posted no review of 977bdf1f within 15 minutes. The thread is not resolved.

## Reporting notes

- Out of scope, left as the PONG decision says:
  - `.gitignore:10 .agents/runs/` (agent-fanout's output directory);
  - the `plans/005-*.md` fanout references;
  - the `.orchestration/*T33-herdr-session*` and `T5-herdr-session*` historical records that the `git ls-files` grep matches.
- Lost coverage: the deleted `test_upgrade_skips_ccr_notice_when_gh_is_unavailable` was the only test that ran `upgrade-tools.sh` with `gh` absent. The remaining `gh` callers either check `has_command gh` (the crit and zed pin fetches, gh extensions) or run inside the optional `bump_release_asset_pins` phase, which treats a failed `gh api` as an optional-phase failure. No test covers the gh-absent path any more.
- Process slip, fixed before push: my first attempt to delete methods by regex mis-cut the test files. I restored them with `git checkout` and deleted by AST line ranges instead. Separately, the first `git add` failed on the removed `archive` pathspec, so I amended the first commit to include all edits. Neither reached GitHub in a broken state.
- `make require-crit-review` will treat this as needing review: `home/dot_zshrc` and `executable_herdr-agents` are high-risk files.

cost: n/a (the Claude Code runtime does not expose per-session token or cost figures to the worker)
