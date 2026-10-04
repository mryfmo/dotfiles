# AGMSG-TASK dotfiles-T66-permgate-dead-lanes-a01

Drafted 2026-10-04 by the orchestrator seat from the approved correction plan (Phase 1, dotfiles-T66). Worker: the identity named in the dispatch, in its own worktree.

## Objective

Principle 9 and 1: permgate (`home/dot_local/bin/common/executable_permgate`, 788 lines, policy `home/dot_agents/permgate-policy.yaml`) has produced 0 denies in 425 decisions; its LLM classifier lane is shadow-only (`llm_enabled: false`, prompt says "Never deny") and its `cli` workspace lane has no caller outside its tests. Delete both lanes and keep the deterministic hook: `deny_patterns` + `allow_patterns` + `hook_output`.

1. `executable_permgate`: remove the LLM shadow lane (classifier schema/prompt/`classify`, ~265-452, the branch in `decide` ~611-635, the shadow fields in `append_log`/`decision_record` ~453-485), the cli lane (~126-159, 486-575, 643-682 and the `cli` dispatch in `main`), `run_bench` (~683-726) and its dispatch, and the policy validation of `providers`/`cli` (~95-190). Keep: `deny_patterns`, `allow_patterns`, `is_bounded_shell_command`, `hook_output` (both hook schemas), the decisions log (append-only, 0600, hash + summary), the recursion guard, and the fail-closed-to-native-prompt behaviour (undecided → empty stdout).
2. `home/dot_agents/permgate-policy.yaml`: keep `schema_version`, `deny_patterns`, `allow_patterns`; drop `providers`, `cli`, `enablement`, `categories`, `classifier_prompt`, `classifier_actions`. Bump `schema_version` if the loader checks it.
3. `tests/unit/test_permgate.py`: delete the cli tests (~275-568) and classifier/bench tests (~601-974); keep deny/allow/protocol/golden-bytes tests (incl. `test_layer_one_deny_uses_both_hook_output_schemas`, `test_claude_and_codex_hook_outputs_match_golden_bytes`, the undecided → empty stdout tests).
4. Docs: `README.md` permgate paragraphs (grep `classifier`, `shadow`, `permgate cli`, `bench`), `home/dot_config/claude/rules/model-selection.md:3` sentence "Permgate classifier IDs are separately pinned in its security policy" and line ~12 "both providers remain shadow-only until …" → state that permgate is deterministic-only. Also `scripts/validate-agent-assets.py` if it pins classifier model IDs or policy keys (grep `permgate`), and `tests/unit/test_supply_chain_policy.py` likewise.

Forbidden: new lanes; any change to the PermissionRequest wiring in the Claude/Codex templates; policy additions beyond deleting keys.

[memory:decision] dotfiles-T66 (operator 2026-10-03): permgate keeps only its deterministic deny/allow lanes and the native-prompt fallthrough; the shadow LLM classifier lane, the cli workspace lane and the benchmark are deleted as dead code (0 denies in 425 decisions, 0 callers).

## Repo / branch

- Work ONLY in your own worktree (worker-d for a006). `git fetch origin`; `git switch -c chore/permgate-dead-lanes origin/main` (523fda06 or later). README: T89 (a005) edits the add-worker paragraphs concurrently; keep your edits to the permgate paragraphs and rebase with `gh pr update-branch` if main moves. Verify the dispatched task_rev; else stop and PONG blocked.
- Strict status checks: if `main` moves, `gh pr update-branch <pr>` and wait for CI again before RESULT.

## Allowed files

- `home/dot_local/bin/common/executable_permgate`, `home/dot_agents/permgate-policy.yaml`, `tests/unit/test_permgate.py`
- `README.md` (permgate paragraphs), `home/dot_config/claude/rules/model-selection.md` (the two permgate sentences)
- `scripts/validate-agent-assets.py`, `tests/unit/test_supply_chain_policy.py` (only lines that reference permgate classifier IDs or removed policy keys; name them)
- `.orchestration/{reports,validation,sandboxes,learning,autoskill/runs}/dotfiles-T66-permgate-dead-lanes-a01.md` (main checkout)

## Validation commands (paste verbatim output)

```
git diff origin/main --stat
wc -l home/dot_local/bin/common/executable_permgate            # expect well under 400
grep -n '"cli"\|classif\|bench\|shadow' home/dot_local/bin/common/executable_permgate; echo "exit=$?"   # expect no matches
uv run python -m unittest tests.unit.test_permgate 2>&1 | tail -3
printf '%s' '{"tool_name":"Bash","tool_input":{"command":"gh pr view 1"}}' | PERMGATE_STATE_PATH=$TMPDIR/pg.jsonl python3 home/dot_local/bin/common/executable_permgate claude   # allow JSON
printf '%s' '{"tool_name":"Bash","tool_input":{"command":"ls"}}' | PERMGATE_STATE_PATH=$TMPDIR/pg.jsonl python3 home/dot_local/bin/common/executable_permgate claude; echo "[exit=$? stdout must be empty]"
make unit-test
make validate-agent-assets
mise x node npm:prettier -- prettier --check README.md home/dot_config/claude/rules/model-selection.md
gh pr checks <pr-number>
gh api repos/mryfmo/dotfiles/pulls/<pr-number> --jq '.mergeable_state'
```

## Completion

1. PR to `main`, English title/description ending with `🤖 Generated with [Claude Code](https://claude.com/claude-code)`. CI green on the final head, branch up to date.
2. After the final push: `gh pr checks <pr> --watch`; wait (≤15 min) for the Codex Bot review; fix P0/P1 inline findings and repeat; do not resolve threads.
3. Artifacts at the exact expected paths; validation with verbatim outputs, PR number, head SHA.
4. CompactionDB `memory add --kind decision --scope project` with the `[memory:decision]` text from the main checkout; paste command and output.
5. `AGMSG-RESULT v1` via `agmsg-dispatch dotfiles <your identity> claude-remediation-dot wT:p1 "<single line>"` (outside the sandbox). `cost:` line. max_turns=30.

## PONG decision 1 (2026-10-04T00:09Z, scope questions)

1. `tests/install/common/lifecycle.bats:441-444`: added to the allowed files; delete the four pins (`llm_enabled false`, the two classifier model IDs, `PERMGATE_CODEX_COMMAND`), keep the `PERMGATE_INNER` line.
2. `home/dot_config/codex/AGENTS.md:55`: added; reword that one line to "permgate is deterministic-only (deny/allow patterns, native prompt fallthrough)", mirroring `model-selection.md`.
3. Policy key `metrics`: keep it only if the retained code reads it; if it fed the deleted lanes (bench/shadow), drop it and its validation. State which in the report.

## Revise round 1 (2026-10-04, Codex review of the update-branch head f26975ab)

Two valid P2s arrived after the update-branch merge; fix both at the root in one commit on `chore/permgate-dead-lanes` (pause T88 in worker-d, switch branches, fix, push, then resume T88):

1. `home/dot_config/codex/AGENTS.md`: a sentence near line 55 still tells Codex users to configure a separately pinned permgate classifier model; delete it (the file must not contradict the deterministic-only line).
2. `scripts/validate-agent-assets.py` (~991): the permgate policy check accepts any JSON whose key set matches; require a mapping (`isinstance(policy, dict)`) and `schema_version == 3`, with a failure message naming the file; add the negative test cases (array policy, wrong schema_version) to the validator tests (`tests/unit/test_validate_agent_assets.py`, name the test).

Push, wait for the Codex review of the new head, new RESULT; do not resolve threads. The orchestrator re-sweeps and gates at the new head.
