# AGMSG-TASK dotfiles-T77-harness-dead-code-a01

Drafted 2026-10-04 by the orchestrator seat from the approved correction plan (Phase 4, dotfiles-T77). Depends on T70 (merged), T68 (merged f32f33a0), T91 (merged 312fef3f) and T71 (PR #249, generator); dispatch after #249 merges. Shares no file with T72 except `scripts/validate-agent-assets.py` and `scripts/upgrade-tools.sh`, so run it before or after T72, never concurrently.

## Objective

Principle 9: harness code that nothing runs.

1. **`herdr()` wrapper and `herdr-session`**: delete the `herdr()` function in `home/dot_zshrc` (~21-32) and `home/dot_local/bin/common/executable_herdr-session`; `tests/unit/test_herdr_agents.py` pins (`herdr-session` at ~30, 464-466, 589, 1339) and `README.md:528`, `:898` follow.
2. **`agent-fanout`**: delete `home/dot_local/bin/common/executable_agent-fanout`; `scripts/validate-agent-assets.py:1049-1062` (the fanout checks), `scripts/require-crit-review.py:68` and `tests/unit/test_require_crit_review.py:141` (the path list), `tests/unit/test_runtime_health.py` (~132-160 and the fanout suite), the `generate-agent-configs.py:771` comment and `home/dot_agents/model-profiles.env` header ("sourced by agent launchers (herdr-agents, agent-fanout)") and the README mention follow.
3. **`report_ccr_adoption_gates`** in `scripts/upgrade-tools.sh` (~644-666 and its `run_optional_phase` call at ~741) and `tests/unit/test_runtime_health.py` (~1830-1860): delete; the CCR gates were a one-time adoption notice.
4. **`HERDR_AGENTS_CODEX_PROFILE` alias** in `executable_herdr-agents` (~61-64, 162-171), `scripts/validate-agent-assets.py:1059`, `tests/unit/test_herdr_agents.py` (~557, 616, 1468, 2092) and `README.md:817`: delete; `HERDR_AGENTS_WORKER_PROFILE` from the manifest is the only source.
5. **`home/dot_claude/hooks/executable_enforce-uv.sh`**: it emits `"decision": "block"` JSON (lines 22-99). VERIFY the current Claude Code PreToolUse contract (`hookSpecificOutput.permissionDecision: deny` with `permissionDecisionReason`, versus the legacy top-level `decision`) against the official hooks reference and paste the source; convert if the legacy form is deprecated, otherwise record why it stays. Approve paths stay silent exit 0.
6. **`archive/CompactionDB-2.0.0.zip`**: delete and reword the `agent-config.yaml:585` note (the vendored copy under `vendor/compactiondb` is the source).

Forbidden: `.github/workflows/docs.yml` permissions; `vendor/compactiondb/**` (T81); any pin.

[memory:decision] dotfiles-T77 (operator 2026-10-03): the `herdr()` zsh wrapper and `herdr-session`, `agent-fanout`, the CCR adoption-gate notice, the `HERDR_AGENTS_CODEX_PROFILE` alias and `archive/CompactionDB-2.0.0.zip` are deleted; `enforce-uv.sh` speaks the current PreToolUse contract.

## Repo / branch

- Work ONLY in your own worktree. `git fetch origin`; `git switch -c chore/harness-dead-code origin/main` (the commit that merged #249 or later). Verify the dispatched task_rev; else stop and PONG blocked.
- Strict status checks: if `main` moves, `gh pr update-branch <pr>` and wait for CI again before RESULT.

## Allowed files

- `home/dot_zshrc`, `home/dot_local/bin/common/executable_herdr-session` (delete), `home/dot_local/bin/common/executable_agent-fanout` (delete), `home/dot_local/bin/common/executable_herdr-agents` (alias only), `home/dot_claude/hooks/executable_enforce-uv.sh`, `home/dot_agents/model-profiles.env`, `home/dot_agents/agent-config.yaml` (the one note), `archive/CompactionDB-2.0.0.zip` (delete), `scripts/validate-agent-assets.py`, `scripts/require-crit-review.py` (the path list), `scripts/upgrade-tools.sh`, `scripts/generate-agent-configs.py` (the comment), `README.md` (the named lines), `tests/unit/test_herdr_agents.py`, `tests/unit/test_require_crit_review.py`, `tests/unit/test_runtime_health.py`, `tests/unit/test_enforce_uv.py` (if present)
- `.orchestration/{reports,validation,sandboxes,learning,autoskill/runs}/dotfiles-T77-harness-dead-code-a01.md` (main checkout)

## Validation commands (paste verbatim output)

```
git diff origin/main --stat
git ls-files | grep -E 'herdr-session|agent-fanout|archive/' ; echo "rc=$?"
grep -rn "agent-fanout\|herdr-session\|HERDR_AGENTS_CODEX_PROFILE\|CCR gate\|\"decision\": *\"approve\"" home scripts tests README.md ; echo "rc=$?"
make render-check
make unit-test
make validate-agent-assets
gh pr checks <pr-number>
gh api repos/mryfmo/dotfiles/pulls/<pr-number> --jq '.mergeable_state'
```

## Completion

1. PR to `main`, English title/description ending with `🤖 Generated with [Claude Code](https://claude.com/claude-code)`. CI green on the final head, branch up to date.
2. After the final push: `gh pr checks <pr> --watch`; wait (≤15 min) for the Codex Bot on that head by listing `gh api repos/mryfmo/dotfiles/pulls/<pr>/reviews --paginate --jq '.[]|select(.user.type=="Bot")|[.commit_id,.submitted_at]|@tsv'`; fix P0/P1 inline findings and repeat; do not resolve threads. The RESULT names every unresolved thread with `fixed:<sha>` or a proposed `not-applicable:<reason>`, and `plan-mode-used=<worktree>` if Plan Mode was used.
3. Artifacts at the exact expected paths; validation with verbatim outputs, PR number, head SHA.
4. CompactionDB `memory add --kind decision --scope project` with the `[memory:decision]` text from the main checkout; paste the exact command and output.
5. `AGMSG-RESULT v1 task_id=dotfiles-T77` via `agmsg-dispatch dotfiles <your identity> claude-remediation-dot wT:p1 "<single line>"` (outside the sandbox). `cost:` line. max_turns=30.
