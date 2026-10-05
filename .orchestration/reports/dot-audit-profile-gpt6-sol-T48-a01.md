# Report: dot-audit-profile-gpt6-sol-T48-a01

- status: ready_for_review
- worker: claude-standard-dot-a005 (worktree `.claude/worktrees/worker-c`)
- task_rev: 7e72b32255a4e12508ae92180fdedba5704074c1913f0b874ca028b52dbcea11 at dispatch. Superseded by the operator-override amendment, task_rev 38a86dd0d72acbfbb3b19eef0e7484c77d04a882088e86b5c844bb674b535672 (PING 00:35:42Z). Both sha256 values were verified against the main-checkout task file.
- branch: `fix/audit-profile-gpt6-sol` from origin/main c8fc05c (`git switch --no-track -c`). The worktree left `feat/orchestration-rules-T43` (c878b0d) clean and untouched. `fix/sandbox-unix-sockets` was untouched too.
- commit / head sha: `8956c3df44df936ba7b77db9fb069a323bdbb3de` (commits 81d720f + 8956c3d; all CI checks pass, nix skipped; mergeStateStatus CLEAN)
- PR: https://github.com/mryfmo/dotfiles/pull/218
- cost: 0 subagent dispatches; about 25k context tokens consumed (session budget counter; no per-task figure exposed)

## Operator override (applied)

The amendment replaces `gpt-6-sol` with **`gpt-6.1-sol`** everywhere and adds the API-key requirement. 81d720f was already pushed with `gpt-6-sol`, and force-push is forbidden, so **8956c3d** adds a commit on top that applies the override. The net diff against main contains only `gpt-6.1-sol`. The final values and texts are:

- manifest: `model: gpt-6.1-sol`, `model_reasoning_effort: xhigh`, `sandbox_mode: read-only`;
- validator pin comment: "Operator pin (2026-10-01): the auditor is codex gpt-6.1-sol xhigh, read-only; this model needs API-key auth (rejected under ChatGPT login: 400 'not supported when using Codex with a ChatGPT account', probe 2026-10-01)";
- README: "Codex `gpt-6.1-sol`, xhigh reasoning effort, read-only sandbox; the audit lane requires Codex API-key authentication, because the ChatGPT-login account rejects the model";
- model-selection rule: "auditor=`audit` (Codex gpt-6.1-sol xhigh, read-only sandbox; the audit lane requires Codex API-key auth because the ChatGPT-login account rejects the model)";
- pin test: also rejects `gpt-6-sol`.

No fallback model was added anywhere. Known consequence, which the orchestrator recorded and which is the operator's lane: until Codex has API-key auth on this machine (`auth_mode: chatgpt` today), `herdr-agents --audit` fails at the model call.


## Changes (net of 81d720f + 8956c3d)

1. `home/dot_agents/agent-config.yaml` `model_profiles.audit.codex`: `model: gpt-6.1-sol` and `model_reasoning_effort: xhigh`. `sandbox_mode: read-only` and `notify` are kept. The comment above ("Auditor tier (監査役): cross-vendor read-only audit of worker changesets.") names no model, so it is unchanged. `security` and `adh` are untouched.
2. Regenerated with `uv run --with pyyaml scripts/generate-agent-configs.py` ("generated agent configs updated"). The only file it rewrote is `home/dot_codex/modify_private_audit.config.toml`, where the MANAGED block now has `model = "gpt-6.1-sol"` and `model_reasoning_effort = "xhigh"`. `git status --untracked-files=no` after the run is pasted in the validation file.
3. `scripts/validate-agent-assets.py`: the audit pin is now `gpt-6.1-sol` / `xhigh` / `read-only`, with the amendment's comment quoted above. The security pin is unchanged.
4. Docs:
   - `README.md:265`: the auditor sentence quoted above (model, effort, sandbox, and the API-key clause).
   - `home/dot_config/claude/rules/model-selection.md:3`: the auditor clause quoted above.
5. Tests:
   - `tests/unit/test_validate_agent_assets.py`: the valid-manifest fixture's audit codex block now uses `gpt-6.1-sol` / `xhigh` / `read-only`. `test_agent_manifest_pins_the_audit_codex_profile` gains three rejected values, `("model", "gpt-6-astra")`, `("model", "gpt-6-sol")` and `("model_reasoning_effort", "high")`, so the test proves the earlier values fail. No new test method was added.
   - `tests/unit/test_generate_agent_configs.py`: the `test_audit_profile_renders_read_only_sandbox_override` sample uses `gpt-6.1-sol` / `xhigh`. The values are not asserted, but this removes an auditor-specific `gpt-6-astra` mention.

## Remaining `gpt-6-astra` mentions (git grep, all non-auditor)

- `agent-config.yaml:54` (security) and `:70` (adh).
- `modify_private_security.config.toml` and `modify_private_adh.config.toml` (rendered).
- `scripts/check-agent-runtime.py:82,370`, `scripts/generate-agent-configs.py:25,148` and `scripts/validate-agent-assets.py:64,843`: adh defaults and messages.
- `validate-agent-assets.py:743,746`: the security pin.
- `test_generate_agent_configs.py:452,477`: the security render test.
- `test_validate_agent_assets.py:193`: the security fixture.
- `test_validate_agent_assets.py:555`: the old audit value, as a value that must be **rejected**.

## Deviation: `make render-check` does not exist on main

`make render-check` arrives with T43 (PR #214, not yet merged), so on `origin/main` it exits 2 ("no rule to make target"). The Makefile is outside T48's allowed files, so I ran the command that target wraps instead: `uv run --with pyyaml scripts/generate-agent-configs.py --check` reports "generated agent configs are up to date", exit 0. All three outputs are pasted, including the failing `make`.

## Checks

At head 8956c3d, all output is verbatim in the validation file, with every exit captured directly:
- `make unit-test`: 612 OK (1 skipped);
- `make validate-agent-assets`: ok;
- the render check as above;
- the `git grep`;
- `gh pr view` / `gh pr checks`;
- CompactionDB.

## Notes

- The Understand-Anything auto-update hook fired after the commit. I did not act on it.
- Out of scope, not done: running the auditor or `chezmoi apply`, and touching `model-profiles.env` (`MODEL_PROFILE_AUDIT_CODEX_ARGS` stays `--profile audit`) or the security profile.
- **User-visible impact:** after `chezmoi apply`, `codex --profile audit` / `herdr-agents --audit <sha>` requests `gpt-6.1-sol` at xhigh, and fails until Codex uses API-key auth.

[memory:decision] T48: the auditor (`audit` profile) runs Codex `gpt-6.1-sol` at `xhigh`, read-only; it requires API-key auth; ChatGPT login rejects it (operator decision 2026-10-01, probe recorded in the T48 task file).

## CompactionDB (main checkout)

The current decision is **90843027-5c79-4107-9bcb-8d2174d6b36b** (`gpt-6.1-sol`). It supersedes **ae7ca177-4bce-4581-88ae-03f9c01299aa**, which was written before the override and says `gpt-6-sol`; its text says so. Please drop or ignore ae7ca177 at consolidation. Both commands and outputs are in the validation file:

```
cd ~/Workspace/dotfiles && python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content "<the [memory:decision] text above>"
```

## Effects

None outside the repository working tree. The config takes effect only at the operator's `chezmoi apply`.
