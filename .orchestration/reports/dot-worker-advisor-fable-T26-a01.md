# Report: dot-worker-advisor-fable-T26-a01

- Worker: claude-standard-dot-a005 (claude-opus-5-5, high)
- Status: **ready_for_review**. CI is fully green on head `a63666b`: 12 pass and 1 skipping (nix). On all three runners, shfmt, ShellCheck, the Python unit tests, and the bats unit tests ran and passed; the only skipped steps were the unrelated-changes shortcut and Codecov on macOS.
- task_rev verified: the sha256 of the task file at origin/main `030273d` is `f886451c7d1c0eb0fdb9408c3922ad97f8d686a6aaae20a52a964980fd072153`, which matches. The worktree was clean. The base contains T25 (`herdr-agents --restart-worker` is in README).
- Branch `feat/worker-advisor-fable` from origin/main `030273d`. **Head `a63666b` (`a63666bb3cbc21f8d5c1cb80e26fe0b450daba56`)**.
- PR: https://github.com/mryfmo/dotfiles/pull/188 (not merged)
- Evidence: `.orchestration/validation/dot-worker-advisor-fable-T26-a01.md`

[memory:decision] T26: worker claude launches carry --advisor fable from manifest claude.advisor. The validator pins the worker profile's advisor to fable, and the interactive advisorModel is rendered from the manifest (operator 2026-09-27). CompactionDB id `a7c20de3-85d6-460c-91e4-3264ddefda5e`.

## Changes (all within allowed_files)

1. `home/dot_agents/agent-config.yaml`: `standard.claude` and `deep.claude` gain `advisor: fable`. No other profile changed, and neither did worker_kind, worker_profile, interactive_profile, or any codex value.
2. `scripts/generate-agent-configs.py`
   - New `PROFILE_OPTIONAL_KEYS = {"claude": ("advisor",)}`. When the key is present, it goes through the same `PROFILE_VALUE_RE` launcher-safe check and message as the required keys. The required keys are still model/effort.
   - `render_model_profiles_env()` appends ` --advisor <value>` to `MODEL_PROFILE_<P>_CLAUDE_ARGS` when the key is set.
   - `render_claude_settings()` emits `"advisorModel"` immediately after `effortLevel` only when the interactive profile's claude side sets advisor; otherwise the key is absent.
   - Regenerated diff: exactly `home/dot_agents/model-profiles.env` (STANDARD and DEEP CLAUDE_ARGS gain `--advisor fable`) and `home/.chezmoitemplates/claude-settings-managed.json` (`"advisorModel": "fable"`). Codex outputs and `express-explorer.md` are unchanged.
   - Delivery check: `home/dot_claude/modify_private_settings.json` `merge_settings` copies every managed key. `advisorModel` therefore reaches `~/.claude/settings.json` at apply time, with the same value as the operator's manual setting.
3. `scripts/validate-agent-assets.py`: right after the worker_profile membership check, the validator requires `model_profiles[worker_profile].claude.advisor == "fable"`. The failure message is `<manifest> worker profile '<name>' must set claude.advisor: fable (operator pin)`. The schema loop checks only required keys, so the optional key was already accepted elsewhere and needed no change there.
   - **Note for the orchestrator:** I check the pin against `worker_profile` literally, with no fallback to interactive_profile. A missing `worker_profile` therefore now fails validation (it fails the pin as `None`). In effect, `worker_profile` is now required while the pin exists.
4. Part B: `home/dot_local/bin/common/executable_herdr-agents`
   - **Exit dialog:** in `restart_worker_in_pane`, after `herdr agent prompt <pane> "/exit"`, the existing bounded `wait_for_shell_prompt` (50 polls of `pane process-info`) serves as the "agent gone" check. If it fails, the function sends `herdr agent send-keys <pane> Enter` once, then calls `start_worker_agent … true` unchanged. That call waits for the shell again and keeps the fail-safe refusal. The only other caller of `restart_worker_in_pane` (full-mode heal) passes agentless panes, so it never reaches the new wait.
   - **Legacy label:** the restart-mode block relabels the resolved worker pane with `herdr pane rename <pane> <kind>-worker` when its label is not `<kind>-worker`. This happens after the ambiguity check passes and before `/exit`, and uses the same jq-guard pattern as the orchestrator relabel. `attach_panes_are_unambiguous` is unchanged.
   - **Baseline finding (honest scope):** before this change, a legacy-labeled worker pane was already *tolerated*. The restart-mode orchestrator lookup excludes the worker pane, and `start_worker_agent` renamed the pane on success. The gap was the ordering: the rename happened only after a successful start, so a refused restart (for example, the T25 exit-dialog case) left the label broken. The new code repairs the label before the restart can refuse. The baseline outputs are in the validation file.
   - shdoc `@description` for the file and for `restart_worker_in_pane` each gain one clause.
5. Docs
   - `README.md`: the `--restart-worker` sentence mentions Enter-once dialog confirmation and legacy-label relabeling. The worker-profile paragraph says the worker profile carries `advisor: fable`, rendered as `--advisor fable`, and that a running worker picks it up with `herdr-agents --restart-worker`.
   - `home/dot_config/claude/rules/model-selection.md`: the first bullet says the advisor model lives only in `model_profiles` (`claude.advisor`) and must never be set with ad-hoc `/advisor` or `--advisor` flags outside the rendered args.
6. Tests
   - `tests/unit/test_generate_agent_configs.py`: 3 new tests. (a+b) `--advisor fable` is rendered only for the profile that sets it (count == 1; express has none). (c) An unsafe advisor raises SystemExit. (d) `advisorModel` is absent without an advisor and equals `fable` with one.
   - `tests/unit/test_validate_agent_assets.py`: the fixture gains `worker_profile: standard` and `standard.claude.advisor: fable`. One new test with 2 subtests: a missing advisor and `opus` both fail with the pin message.
   - `tests/unit/test_herdr_agents.py`
     - The fake herdr gains a `process-info` state file (`shell` / `exit-dialog`, which stays claude until an `agent send-keys … Enter` / `stuck`).
     - 4 new tests: (a) env-file `--advisor fable` reaches the `agent start` args. (b1) The exit dialog is confirmed exactly once, in the order `/exit` < `agent send-keys w-old:p2 Enter` < `agent start`. (b2) A stuck pane exits nonzero with "refusing agent start", no `agent start`, one Enter, and 100 `process-info` polls, which proves both bounded waits ran. (c) A `claude-orchestrator`-labeled worker pane is renamed `claude-worker` before `/exit`, and the restart succeeds.
     - The existing relaunch test now also asserts that no `agent send-keys` is sent on the normal path.
     - A no-op `sleep` shim applies to the two dialog tests only.
   - The 3 new herdr Part B tests fail against the unmodified script (baseline pasted). (a) passes on the baseline by design: it is a regression guard, because the script already passes the env-file args through.
   - Local bats: not run (repo policy).

## Not done / out of scope

- Understand-Anything graph refresh: the post-commit hook requested it, but `.ua/` is outside allowed_files. Task it separately if wanted.
- `make require-crit-review`: orchestrator-side.
- No validator check that the settings' `advisorModel` equals the manifest value: `generate-agent-configs.py --check` already enforces render fidelity.

## CompactionDB

The command and output are pasted verbatim in the validation file. The id is `a7c20de3-85d6-460c-91e4-3264ddefda5e`.

cost: n/a
