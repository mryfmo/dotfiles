# U40 Dead manifest keys of the herdr-agents worker era, and the lever table rows U36 left out — brief

GOAL
The manifest `home/dot_agents/agent-config.yaml` carries no key that nothing reads, and `scripts/orchestrator/README.md`'s lever table names every lever the kit ships. Two small clean-ups with a grep inventory as their evidence.

SCOPE
One branch `chore/dead-manifest-keys-lever-table` from `origin/main` (after U36 lands, so `regime-start` and `regime-stop` are on main; if U36 is still open when you start, do part 1 first and merge `origin/main` before part 2). May write: `home/dot_agents/agent-config.yaml` (the five keys), `scripts/generate-agent-configs.py` and `scripts/validate-agent-assets.py` (the lines that emit or check those keys), their tests under `tests/unit/` (`test_generate_agent_configs.py`, `test_validate_agent_assets.py`), the generated files those lines produce if any (run `make render-check`; paste its result), `scripts/orchestrator/README.md` (lever table rows), `README.md` one line only if it lists the manifest keys. Nothing else.

CONTEXT
- U26 removed `herdr-agents`' layout, attach, audit and directive modes and their callers; U27's ADDENDUM item 1 recorded that since then nothing reads the keys `worker_kind`, `orchestrator_kind`, `worker_profile`, `worker_worktree`, `worker_cap` in the manifest. Start from the inventory: `git grep -n -E 'worker_kind|orchestrator_kind|worker_profile|worker_worktree|worker_cap' -- . ':!.orchestration'` on your branch head (paste it in the PR body); a hit outside the manifest, generator, validator and their tests is a reader and changes the plan: stop and ask.
- U36's PR body "Not done": `scripts/orchestrator/README.md`'s lever table does not list `regime-start` and `regime-stop` (outside U36's SCOPE). The table's existing rows give the form (one row per lever: name, what it does, who runs it).

CHANGE
1. Remove the five keys from the manifest, their emitting lines from the generator and their checks from the validator; keep every other key; update the tests that pinned them (a test that asserts the keys are gone is enough; no new fixture).
2. Add the two lever rows to the README table in the existing form, after `regime-env`/`regime-init` if those rows exist, with the one-line descriptions from the levers' `@brief`.

ACCEPTANCE
1. The inventory grep on the head returns no hit outside `.orchestration/` (paste); `make validate-agent-assets` and `make render-check` pass and are pasted; `uv run python -m unittest tests.unit.test_generate_agent_configs tests.unit.test_validate_agent_assets` OK pasted.
2. The lever table lists `regime-start` and `regime-stop`; `grep -c` of each name in the README pasted.
3. CI green on the head; PR body `Program-Unit: regime-cutover/U40`, a threat table of one line per edited file (a records-and-manifest clean-up: say so), the footer; pre-RESULT five-point self-check; orchestrator verdict.

TIMEBOX
45 minutes.

FORBIDDEN
No change to `herdr-agents`, the levers, or any installed state; no `# noqa`; no merge, rebase, force-push, PR close; no omp subagent (the Task tool kills a seat on the claude-bridge route).

REPORT
Per STANDING 12 plus the RESULT line (standing order 23).

STANDING
`~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` (lines 20 to 23).

ADDENDUM (orchestrator-sari, 2026-10-24T12:2xZ, worker inventory bus row 6530, answer row 6575)
Inventory on e7bb65b5: no runtime reader (herdr-agents has no hit for the keys, the `HERDR_AGENTS_*` variables or `model-profiles.env`; nothing under `home/dot_local`, `scripts/orchestrator`, `.chezmoiscripts`, `install` or `setup.sh` sources the fragment; `check-agent-runtime.py:721` compares whole-file source to deployed; `validate-agent-assets.py:1197` requires `HERDR_AGENTS_ORCHESTRATOR_KIND` in the fragment and is in SCOPE). Four hits outside SCOPE, granted: (1) `home/dot_config/codex/AGENTS.md:46` deleted (the rule that names `worker_kind` as the source of truth; `:45` stays for the `model-profiles.env` token `validate-agent-assets.py:1209` requires); (2) `tests/unit/test_herdr_agents.py:350`, the `env.pop` of `HERDR_AGENTS_WORKER_KIND`, deleted; (3) `.gitignore:28` comment reworded to the omp seat worktrees, the `/.claude/worktrees/` rule unchanged (the stop gate relies on it); (4) `.ua/fingerprints.json` and `knowledge-graph.json` left (the Understand-Anything index, refreshed only by a full rebuild; recorded as the index residual in the PR body). The inventory is pasted in the PR body as evidence.
