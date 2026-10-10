# Acceptance: dotfiles-T120-npm-provenance-and-claude-channel-a01

- **Decision:** PENDING (round 0 in progress). PR #315 `feat/npm-provenance-and-claude-channel` on main `d29ce4c1`; dispatched 2026-10-10 09:32Z to `claude-standard-dot-a002` (worker-e) concurrently with T124 wave 1 and wave 3b; Amendments 1–8.
- **Worker:** `claude-standard-dot-a002` (worker-e, w4:pC).
- **Exemption declared:** acceptance and final integration; evidence-sync bookkeeping; Bot thread replies and resolution; the orchestrator's live probes (the Claude Code manifest signature, `npm audit signatures`, the mise Codex install with and without `package_manager = "npm"`, Amendments 3 and 5).
- **Process notes to carry (visible exceptions):**
  - Amendment 4's q5 conclusion was wrong because the orchestrator's probe omitted the repository's `package_manager = "npm"`; the worker caught it (q10) and Amendment 5 corrected it with the re-probe pasted.
  - Amendment 8 is the eighth amendment; under T126 INV-6 four amendments reach the reset count. T120 predates T126 and continues under V2 applied by hand. The orchestrator proceeded rather than resetting, because the threat model is unchanged and the implementation is CI-green and Bot-clean on each head, and recorded it here for the operator to overrule.
  - The task's premise that Anthropic's auto-updater moves Claude Code was false on these hosts (`autoUpdates: false` is managed); Amendment 8 makes `make update` move it through the verified path.
- **Origin:** operator decisions of 2026-10-09 (72h cooldown; npm provenance verified after install with day-one Codex; Claude Code on Anthropic's own distribution verified by us; Python CLIs through mise pipx).

## What is under acceptance (PR #315, final head named in the Decision line)

(filled at the RESULT)

## Audit / sweep / gate

| scope | verdict |
|---|---|

- Sweep: (at the final head).
- Bot wait: findings on 41a94b75 (two reviews; the second found late by the worker, its own miss), 8e83a502, cafeae18, f9b5bd85 fixed in the PR.

## Parallelism

- Concurrent with T124 wave 1 (worker-c) and wave 3b (worker-f); shared code files `tests/unit/test_herdr_agents.py` and `executable_herdr-agents` in disjoint hunks (orchestrator exception recorded in all three tasks).

cost: (measured at acceptance)
