# Operator patches (prepared by the orchestrator, applied by the operator)

Shared-source changes under the routing rule (the manifest renders both Claude and Codex configs). Each patch was produced in a detached scratch worktree from `origin/main` 683384ea on 2026-10-12 by editing `home/dot_agents/agent-config.yaml`, running `uv run --with pyyaml scripts/generate-agent-configs.py` and `make render-check`; nothing was committed.

| file | decision | files | check |
|---|---|---|---|
| `t717.patch` | Codex `standard`/`review`/`deep` → gpt-6.1-sol xhigh (operator, 2026-10-12 10:54Z) | 5 (manifest, codex-config-managed.toml, three profile files) | render-check OK; no Claude-rendered file changes; `xhigh` is in gpt-6.1-sol's catalog levels |
| `t710.patch` | `permissions.ask` for remove-worker, gh pr merge, git push (plan 007 T710) | 3 (manifest, claude-settings-managed.json, test_generate_agent_configs.py) | render-check OK; `tests.unit.test_generate_agent_configs -k managed_claude_sandbox` OK |
| `t717+t710.patch` | both in one PR | 7 | render-check OK |

Apply from a clean branch off `origin/main`:

```bash
git switch -c operator/model-profiles-and-ask-rules --no-track origin/main
git apply .orchestration/validation/operator-patches/t717+t710.patch
make render-check && uv run --no-project python -m unittest tests.unit.test_generate_agent_configs
git commit -am "chore(agents): Codex profiles to gpt-6.1-sol xhigh; ask rules for irreversible control-plane commands"
git push origin operator/model-profiles-and-ask-rules && gh pr create --fill
```

After the merge: `make -C ~/.local/share/chezmoi update`, then restart Claude Code (one restart covers both patches and the step-1 restart).
