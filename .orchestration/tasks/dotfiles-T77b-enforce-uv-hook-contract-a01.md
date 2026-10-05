# AGMSG-TASK dotfiles-T77b-enforce-uv-hook-contract-a01

Drafted 2026-10-05 by the orchestrator seat: item 5 of dotfiles-T77, routed out of that Claude-seat task because `home/dot_claude/hooks/executable_enforce-uv.sh` is a Claude PreToolUse hook (a Claude seat's own execution boundary; seat-capability rule), so a Codex seat edits it. Depends on T77 (merged 67451fc6). Disjoint from T80 (PR #264, generator/validator) and from T79/T81 (queued).

## Objective

Principle 9: a hook that speaks a deprecated contract is dead configuration in waiting.

1. **VERIFY the current Claude Code PreToolUse hook output contract** against the official hooks reference (paste the URL and the relevant excerpt in the validation file): whether the legacy top-level `{"decision": "block", "reason": …}` form is still honoured for PreToolUse, and whether the current form is `{"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny", "permissionDecisionReason": …}}` (with `allow`/`ask` as the other values).
2. If the legacy form is deprecated or ignored, convert every `"decision": "block"`/`"approve"` emission in `executable_enforce-uv.sh` to the current form: a block becomes `permissionDecision: "deny"` with the existing reason text as `permissionDecisionReason`; an approve becomes a silent `exit 0` with no JSON (the hook must not claim an allow it does not need). Keep the detection logic, exit codes and messages otherwise unchanged; stay shdoc-compatible in comments.
3. If the legacy form is still honoured and documented, change nothing in the hook and record the source; the task then delivers only the VERIFY evidence and a one-line note in the hook header naming the contract and the reference date.
4. Tests: the unit tests that exercise the hook (grep `enforce-uv` under `tests/unit/`) follow the chosen contract: a blocked command yields the deny JSON (or the legacy block if kept), an allowed command yields no stdout and exit 0.
5. `make validate-agent-assets` (it inventories Claude hooks), `make unit-test`, shellcheck and shfmt on the hook.

Forbidden: any other hook; `.claude/settings.json`; `home/dot_agents/agent-config.yaml`; permgate; new dependencies.

[memory:decision] dotfiles-T77b (orchestrator 2026-10-05, from T77 item 5): `enforce-uv.sh` speaks the current Claude Code PreToolUse contract (hookSpecificOutput.permissionDecision deny with a reason; silence on allow) as verified against the official hooks reference, or the legacy form is kept with the reference recorded if it is still honoured.

## Repo / branch

- Work ONLY in your own worktree. `git fetch origin`; `git switch -c fix/enforce-uv-hook-contract --no-track origin/main`. Verify the dispatched task_rev; else stop and PONG blocked.

## Allowed files

- `home/dot_claude/hooks/executable_enforce-uv.sh`, the unit tests that name it under `tests/unit/`
- `.orchestration/{reports,validation,sandboxes,learning,autoskill/runs}/dotfiles-T77b-enforce-uv-hook-contract-a01.md` plus `-worker-crit.json` / `-worker-review-receipt.md` (in your worktree; the orchestrator transfers them)

## Validation commands (paste verbatim output)

```
git diff origin/main --stat
shellcheck home/dot_claude/hooks/executable_enforce-uv.sh; mise x shfmt -- shfmt -i 4 -sr -d home/dot_claude/hooks/executable_enforce-uv.sh
uv run python -m unittest discover -s tests/unit -p 'test_enforce*' -v 2>&1 | tail -5
make unit-test 2>&1 | tail -3
make validate-agent-assets
printf '%s' '{"tool_name":"Bash","tool_input":{"command":"pip install requests"}}' | bash home/dot_claude/hooks/executable_enforce-uv.sh; echo "rc=$?"
printf '%s' '{"tool_name":"Bash","tool_input":{"command":"uv run python -V"}}' | bash home/dot_claude/hooks/executable_enforce-uv.sh; echo "rc=$?"
gh pr checks <pr-number>
gh api repos/mryfmo/dotfiles/pulls/<pr-number> --jq '.mergeable_state'
```

## Completion

1. PR to `main`, English title/description ending with `🤖 Generated with [Claude Code](https://claude.com/claude-code)`. CI green on the final head, branch up to date.
2. After the final push: Bot wait per the agmsg-orchestration SKILL Worker Playbook (diff head only); fix P0/P1 inline findings; do not resolve threads.
3. Artifacts at the exact expected paths; validation with verbatim outputs, PR number, head SHA, the VERIFY source.
4. The main-checkout CompactionDB is outside your writable roots: the orchestrator records the `[memory:decision]` at acceptance; say so in the report.
5. `AGMSG-RESULT v1 task_id=dotfiles-T77b` via `agmsg-dispatch dotfiles codex-security-dot-a007 claude-remediation-dot wT:p1 "<single line>"`. `cost:` line. max_turns=25.

## Dispatch

- 2026-10-05 04:15Z to `codex-security-dot-a007` (worker-e, wT:p8) after its T90b acceptance (PR #265 merged as b13132d0). Branch from `origin/main` b13132d0 or later with `--no-track`.

### PONG decision (orchestrator, 2026-10-05 04:25Z)

1. Conversion branch confirmed (the official reference deprecates top-level `decision`/`reason`): deny JSON with the reason encoded through the existing `jq -Rs`, silent `exit 0` on allow. New `tests/unit/test_enforce_uv.py` is in scope (no direct tests exist).
2. Shellcheck cleanup authorized, behaviour-preserving and limited to the five baseline diagnostics you named: split `local` declaration and assignment (SC2155), drop the unused `file_path`/`current_dir` reads (SC2034), remove the redundant `python3*` case arm already covered by `python*` (SC2221/SC2222), replace the two simple `sed` substitutions with equivalent first-match shell expansions (SC2001). No detector or parser expansion; list each change in the report.
