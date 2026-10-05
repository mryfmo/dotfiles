# dotfiles-T66-permgate-dead-lanes-a01 — report (status: ready_for_review)

Worker: `claude-standard-dot-a006` (Claude Code, `standard`), worktree `.claude/worktrees/worker-d`.
PR: https://github.com/mryfmo/dotfiles/pull/240 — branch `chore/permgate-dead-lanes`.
- Task commit: `8ae3fdc9eb88030a3238d25def30ac8a00ab36a6`.
- Final head: `4ab48bce085dc834220b891858a4693587db8ac2`, the `gh pr update-branch` merge of main `3a0816e6` (#239). The merge was clean.
- CI: all pass (nix skipped). `mergeable_state` = `clean`. `main` was unchanged at 3a0816e6 when this was written.

Task file revisions verified: `ee8185bc…` (dispatch) and `0b77e4e6…` (PONG decision 1).

## Changes

1. **`home/dot_local/bin/common/executable_permgate`** (788 → 252 lines).
   - Deleted:
     - the LLM shadow lane: `classifier_schema`, `classification_subject`, `parse_classification`, `classify`, the classifier branch in `decide`, and the shadow fields in the decision record;
     - `contains_sensitive_input`, `SECRET_MARKER`, `SENSITIVE_KEY`, `ACTION_NAME`, `CLASSIFIABLE_ACTIONS`, which only gated the classifier;
     - the cli lane: `strict_candidate_path`, `workspace_path_allowed`, `cli_read_decision`, `cli_workspace_decision`, `cli_payload`, `run_cli`, and the `cli` dispatch;
     - `run_bench` and the `bench` dispatch;
     - the `providers`/`cli`/`categories`/`classifier_*`/`enablement` validation in `load_policy`;
     - the unused imports (`math`, `statistics`, `subprocess`, `tempfile`, `stat`).
   - Kept:
     - `deny_patterns`, then `allow_patterns` only for non-Bash tools or a bounded single command (`is_bounded_shell_command`, `has_unsafe_read_option`, unchanged);
     - `hook_output`, giving byte-identical output for both hook schemas;
     - `append_log` (append-only, 0600) and `decision_record` (hash plus summary, same 8 keys);
     - the `PERMGATE_INNER` guard;
     - fail-closed handling: invalid JSON, policy load errors and decide exceptions all produce empty stdout and a native prompt.
   - `load_policy` now requires `schema_version == 3`.
2. **`home/dot_agents/permgate-policy.yaml`:** `schema_version` 2 → 3; `allow_patterns` (9) and `deny_patterns` (1) unchanged. Dropped `providers`, `cli`, `enablement`, `categories`, `classifier_prompt`, `classifier_actions`, and `metrics`. Per PONG decision 1(3), `metrics` was dropped because no code read it: neither the old permgate (no `metrics` reference on `origin/main`) nor the validator nor any test.
3. **`tests/unit/test_permgate.py`** (1052 → 17 tests):
   - Deleted all cli, classifier, shadow, bench and provider-enablement tests and the fake `claude`/`codex` CLIs.
   - Kept the layer-one allow/deny contract tests, `test_layer_one_deny_uses_both_hook_output_schemas`, `test_claude_and_codex_hook_outputs_match_golden_bytes` (incl. undecided → `""`), the recursion sentinel, invalid policy, shell chaining, the `--output` option, structured/bash secret redaction, `apply_patch`, unconstrained native reads, and the mutating/executable read options.
   - Adapted the classifier-specific assertions to `layer == "fallthrough"`.
   - New tests:
     - `test_undecided_request_falls_through_to_the_native_prompt`;
     - `test_repository_policy_allows_and_falls_through` (loads the real policy: `gh pr view 1` → allow, `ls` → fallthrough);
     - `test_invalid_policy_fields_fail_closed` (schema 2 and a bad regex → config-error).
   - The log-shape test now asserts the exact key set and mode 0600.
4. **`scripts/validate-agent-assets.py`:** lines 989-1017 used to require the classifier providers, Haiku/luna model IDs, provider timeouts, classifier categories, and CLI tokens (`PERMGATE_CODEX_COMMAND`, `--safe-mode`, `--tools`, `--disable-slash-commands`, `--ignore-user-config`, `--ignore-rules`, `classification_subject`). They now require the policy key set to be exactly `{schema_version, allow_patterns, deny_patterns}` and keep the `--no-cache`, `PERMGATE_INNER` and `decisions.jsonl` tokens. No test pinned the removed messages (grep).
5. **`tests/unit/test_supply_chain_policy.py`:** no permgate, classifier or policy-key references, so it is unchanged.
6. **`tests/install/common/lifecycle.bats`:** deleted the 4 approved pins (`"llm_enabled": false`, the two classifier model IDs, `PERMGATE_CODEX_COMMAND`); kept the `PERMGATE_INNER` line.
7. **Docs:**
   - `README.md`: the two permgate paragraphs became one deterministic-only paragraph. It also drops the "historical metrics remain in the permgate policy provenance" sentence, since `metrics` is gone.
   - `home/dot_config/claude/rules/model-selection.md`: removed line 3's "Permgate classifier IDs are separately pinned in its security policy."; rewrote line 11 as deterministic-only.
   - `home/dot_config/codex/AGENTS.md:55` (approved): reworded in Japanese to deterministic-only.
   - prettier passes on all three.

The PermissionRequest wiring in the Claude and Codex templates is unchanged. No lanes or policy keys were added.

## User-visible impact

- **No auto-allow is lost.** The shadow lane never allowed anything (`llm_enabled: false`), and the deterministic allow/deny patterns are byte-identical.
- **Deploy ordering.** The executable and policy both reach `$HOME` through one `chezmoi apply`. Until then, the new executable reads the old schema-2 live policy, logs `config-error` and falls through to the native prompt. It fails closed, never open. The task's literal smoke command omits `PERMGATE_POLICY_PATH`, so it shows exactly that against the live policy (pasted in validation). With `PERMGATE_POLICY_PATH=home/dot_agents/permgate-policy.yaml`, it prints the allow JSON for `gh pr view 1` and empty stdout for `ls`.
- **Stale live state after apply (not touched by this task).**
  - `~/.local/state/permgate/decisions.jsonl` keeps its old shadow records.
  - Old `~/.local/state` logs from `permgate cli` callers: there are none, since it had no callers.

## Codex Bot

- No review and no inline comments on either head.
- It reacted `+1` at 2026-10-04T00:39:38Z (after the 8ae3fdc9 push) and again at 00:48:33Z (after update-branch to 4ab48bce). Per its PR note, it comments when it has suggestions and otherwise reacts 👍.
- No threads exist, so there is nothing to disposition.

## Crit

- The dispatch note said to close my Crit server before RESULT. The Plan Mode hook had started pid 4129281 (`plan-agmsg-actas-claude-standard-dot-a006-2026-10-04`) at session start, and I stopped it with `kill`.
- The a007 seat's server (pid 4150161) belongs to another session and was left running.

[memory:decision] dotfiles-T66 (operator 2026-10-03): permgate keeps only its deterministic deny/allow lanes and the native-prompt fallthrough; the shadow LLM classifier lane, the cli workspace lane and the benchmark are deleted as dead code (0 denies in 425 decisions, 0 callers).

CompactionDB, run in the main checkout outside the sandbox:

```
cd ~/Workspace/dotfiles && python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content "<the [memory:decision] text above, verbatim>"
151d0f98-0bd5-4d65-a43d-ebebcd3004ed
```

cost: n/a (the Claude Code runtime does not expose per-session token or cost figures to the worker)

## Revise round 1 (task_rev b7fa55fe…): Codex P2s fixed in the PR

The final head is `a31dcf868d06103564d9ff643dc928e20f8c62b2`. CI is all pass (nix skipped). `origin/main` = 57885db1, and the branch is up to date with it. `mergeable_state` = `blocked` while the three Codex threads are unresolved; threads were not resolved, per the task.

1. **`a93fcb94`** `fix(permgate): reject non-object policies and drop the stale classifier-model sentence` fixes findings 4175645727 and 4175645733 from the f26975ab review.
   - `home/dot_config/codex/AGENTS.md`: removed "permgate の分類器モデルだけは security policy で別途固定します。" from the `model_profiles` bullet. Only the deterministic-only line mentions 分類器 now.
   - `scripts/validate-agent-assets.py`: the check moved into `validate_permgate_policy(policy_path)`. It requires a JSON object, exactly `{schema_version, allow_patterns, deny_patterns}`, and `schema_version == 3`, and every failure message names the file. Named test: `tests/unit/test_validate_agent_assets.py::ValidateAgentAssetsTest::test_permgate_policy_requires_a_schema_3_object`. It covers a valid object and the array, old-schema and extra-key cases.
   - Root cause in the executable, the same class as finding 4175645733: `load_policy` now rejects a non-object policy, so an array policy logs `config-error` and falls through instead of exiting 1. `test_invalid_policy_returns_ask_and_logs_config_error` gained the array case.
2. The Codex Bot gave no response to a93fcb94 between 01:30Z and 01:50Z, so I recorded `bot: none` for that head. Then main moved to 57885db1 (#242, `herdr-agents` only), and `gh pr update-branch` produced `55933ff8`. Its Codex review raised P2 4175753764: a `null` pattern entry made `decide()` raise an uncaught `AttributeError`, so the hook exited 1 with no decision log.
3. **`a31dcf86`** `fix(permgate): fail closed on malformed pattern entries` fixes 4175753764.
   - `main()` now catches `AttributeError` with the other `decide()` errors, giving `config-error`, empty stdout and the native prompt.
   - `validate_permgate_policy` requires both pattern arrays to be lists of objects with string `tool` and `regex`.
   - Tests: the permgate test covers null allow and null deny entries. The validator test covers a null allow entry and a non-list `deny_patterns`. Smoke result with `allow_patterns: [null]`: exit 0, empty stdout, `layer: config-error`.
   - Local `make unit-test` (700 OK), `make validate-agent-assets` and ruff format all pass.
4. Codex Bot on the final head a31dcf86: no review and no inline comment. It reacted `+1` at 2026-10-04T02:07:23Z, after the push.

Proposed dispositions:
- 4175645727 → `fixed:a93fcb94`
- 4175645733 → `fixed:a93fcb94`
- 4175753764 → `fixed:a31dcf86`

T88 was paused for this round. Its branch `docs/parallel-execution-rule` (PR #243, head e68eb6a7) is untouched, and I resume it next.
