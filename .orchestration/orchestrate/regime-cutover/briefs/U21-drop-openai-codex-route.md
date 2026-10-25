# U21 Drop the `openai-codex` route (plan 025 E1, decision 29) — brief

GOAL
The repository recognises two model routes for omp seats, `claude-bridge` and `openai-siwc`; the retired `openai-codex` fallback leaves the generator's and the validator's route regexes and the tests that pin it, so a manifest or profile naming it is refused instead of accepted. Decision 29's default E1 (gates.md G5) applied; G2 passed (the three audit-side profiles log in through openai-siwc).

SCOPE
One branch `chore/drop-openai-codex-route` from `origin/main` (170eb71d or later). May write: `scripts/generate-agent-configs.py` (the route regex and any `openai-codex` branch), `scripts/validate-agent-assets.py` (the route check), `tests/unit/test_generate_agent_configs.py`, `tests/unit/test_validate_agent_assets.py`, `tests/unit/test_omp_config_merge.py` (the cases that name the route), `home/dot_agents/agent-config.yaml` only if a comment or a key still names the route, the generated files `make render-check` regenerates. Nothing else. U28 (PR #504, in flight) edits `scripts/validate-agent-assets.py` in its omp-policy section: keep your hunks in the route check only and merge `origin/main` before the RESULT if U28 lands first.

CONTEXT (measured on 170eb71d)
`git grep -c -i openai-codex -- . ':!.orchestration'`: `scripts/generate-agent-configs.py` 3, `scripts/validate-agent-assets.py` 2, `tests/unit/test_generate_agent_configs.py` 7, `tests/unit/test_omp_config_merge.py` 1, `tests/unit/test_validate_agent_assets.py` 1. No profile, policy or manifest entry names the route (`~/.agents/omp/profiles/*.yml` on this host: audit and security on openai-siwc, the rest on claude-bridge).

CHANGE
1. The route regex and the validator's accepted-route set name exactly `claude-bridge` and `openai-siwc`; a manifest or profile that names `openai-codex` fails validation with a message naming the retired route and the two accepted ones.
2. Tests: the cases that pinned `openai-codex` as accepted become refusal cases (the message asserted); a positive case per accepted route stays.
3. `make render-check` and `make validate-agent-assets` on the branch: pasted.

ACCEPTANCE
1. `git grep -c -i openai-codex -- . ':!.orchestration'` on the head lists only the refusal message and its tests (paste); `make validate-agent-assets` and `make render-check` pass (paste).
2. CI green on the head; the unit tests named above pass in CI.
3. PR body `Program-Unit: regime-cutover/U21`, a threat table (one row: the validator now refuses a route it accepted; no installed state changes), the footer; pre-RESULT five-point self-check; orchestrator verdict.

TIMEBOX
45 minutes.

FORBIDDEN
No change to the live `~/.agents/omp/profiles` or policies by hand (chezmoi deploys them); no omp subagent; no merge, rebase, force-push, PR close.

REPORT
Per STANDING 12 plus the RESULT line (standing order 23).

STANDING
`~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` (lines 20 to 24).

ADDENDUM (orchestrator-sari, 2026-10-24T15:3xZ, worker RESULT row 8680): CHANGE 1's "exactly `claude-bridge` and `openai-siwc`" was a slip; `anthropic/` stays an accepted route as the API-key fallback (gates G1, `docs/pi-claude-bridge.md:139`). The unit retires `openai-codex` only, as its title, GOAL and ACCEPTANCE 1 say; the worker's reading is the brief's.
