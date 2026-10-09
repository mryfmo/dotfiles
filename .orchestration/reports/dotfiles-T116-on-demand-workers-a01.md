# Report: dotfiles-T116-on-demand-workers-a01

Worker `claude-standard-dot-a001` (Claude Code), worktree `.claude/worktrees/worker-c`, branch `feat/on-demand-workers` from `origin/main` 02d65ca7. PR #306, final head `bb2edb384f8f791e46ac37a01d8884d1604b916a`; all 13 checks pass (validation §6).

## Status: ready_for_review

## Commits

- `93ec0b0e` feat(herdr-agents): seat only the orchestrator at startup and workers on demand
- `04c37440` feat(regime): report a worker left seated at a boundary
- `60d49593` docs(regime): describe on-demand workers instead of the resident pair
- `dfdbb8c5` fix(herdr-agents): never take a seated claude worker for the orchestrator (Bot P1 4225776331)
- `bb2edb38` test(runtime-health): pin the add-worker profile literal (Amendment 1)

## What changed

**`home/dot_local/bin/common/executable_herdr-agents`**
- `--restart-worker` exits 2 immediately after `--help` handling with the task's line verbatim, before the orchestrator-kind check and any `require_command`; it touches nothing.
- Full mode creates the workspace with the orchestrator pane only (no `prepare_worker_seat`, no split, no worker start) and no longer requires the worker CLI. Healing an existing workspace restarts a missing orchestrator only: in an agentless pane, or in a new pane split from one that is not the `audit` pane, not a `files` pane and not in a linked worktree (a worker's own tab); with only those left it exits 1 with a hint to open a tab. A Claude worker never counts as the orchestrator: `worker_pane_filter` (any pane in a linked worktree, or labeled `codex-worker`/`claude-worker` after seat-label normalization) replaces the label-plus-cwd `added_worker_pane_filter`, which missed the manifest worker whose self-named label is normalized to `claude-worker` (Bot P1 4225776331).
- Attach (unmanaged pane) renames the pane `claude-orchestrator` unless self-named, claims the seat, prints the directive, bootstraps agmsg; it never splits, starts, restarts or repairs a worker. It exits quietly in any linked worktree under `.claude/worktrees/` (generalising the manifest-seat exit, so an `--add-worker` seat's own SessionStart does nothing) and for a pane labeled `<kind>-worker` (a legacy pair worker still on this machine).
- `--add-worker [<worktree>]`: an omitted worktree is the manifest `worker_worktree`. Parsing rule: two positionals are `<worktree> DIR`; a lone positional is the worktree when it starts with `.claude/worktrees/`, otherwise DIR; an option directly after `--add-worker` means no worktree. `--add-worker /tmp/x DIR` is still rejected as before.
- Directive line: `(default worker worktree <path>)` and `seat one first (herdr-agents --add-worker [<worktree>], default <path>) and remove it with herdr-agents --remove-worker <worktree> when its task is done`. Pane-less summary: "the orchestrator pane is not started".
- `bootstrap_agmsg` configures only the orchestrator's claude-code delivery and identity check in the main checkout (the main-checkout Codex delivery, `/hooks` hint and claude-worker identity hint served only a worker seated in the main checkout, which no mode creates now; `codex-orchestrate` sets a Codex orchestrator's own delivery).
- Deleted as dead: `prepare_worker_seat`, `worker_seat_applies`, `seat_pane_shell`, `start_worker_agent`, `restart_worker_in_pane`, `repair_attach_pane_order`, `repair_attach_pane_ratio`, `attach_panes_are_unambiguous`, `panes_on_pane_tab`, `live_worker_pane_id`, `labeled_worker_pane_id`, `pane_has_agent`, `require_distinct_worker_identity`; `HERDR_AGENTS_CLAUDE_WORKER_ARGS` (pair-worker only) is gone. `distinct_agmsg_identity_count`, `start_agent_in_pane`, `agent_name_for_workspace`, the trust-dialog helper and the seat-label normalization stay (orchestrator start, add-worker, bootstrap).
- Kept deliberately: `AGMSG_CC_MONITOR_KEEP_ALIVE=1` on the add-worker own-workspace path (not the pair worker's); the audit tab logic; the internal `pair_workspace_id` variable name.
- shdoc header, options, examples and usage text rewritten.

**`scripts/check-regime-boundary.sh`**: the main checkout is the only active seat (empty → reported, >1 → stray, not on main → reported as before). For every other checkout: any identity at a path under `<main>/.claude/worktrees/` → `worker still seated at .claude/worktrees/<name> (herdr-agents --remove-worker .claude/worktrees/<name>)` (relative path, so the command is copy-pasteable); >1 per type → `stray <type> identities at …` as before. The tab check no longer exempts the manifest worktree, so every worker tab is reported. Header `@description` updated. The T114 canonical-clone section is unchanged.

**Prose**: SKILL — activation (seat with `--add-worker [<worktree>]`, remove when accepted), pane-less bullet, start checklist, the launch bullet (`--add-worker`/`--remove-worker`, `--restart-worker` retired, profile change = remove then add, "Never run full mode from inside an existing managed workspace"), parallel workers (`seated workers`, cap three without the pair worker), teardown seat rule (one name at main, none at a worker worktree), delivery (`unattended worker pane`; KEEP_ALIVE only for an own-workspace seat), the "Worker panes run in their worktree" bullet for add-worker seats, Stop checklist (`remove every worker`, `orchestrator workspace stays resident`). Rule Activation bullet: `Without a seated worker, seat one (`herdr-agents --add-worker [<worktree>]`) before any repository mutation`. README: the pair description, worker-seat preparation, the retirement note, attach/full-mode paragraph, managed-workspace paragraph, the orchestrator-kind sentence, the add-worker paragraph and bullets, delivery/agmsg mentions, the verification paragraph. Docs test pins the new phrases.

## Decisions and deviations the orchestrator should see

1. **Rule wording**: the rule file never contained `--restart-worker in the pair, --add-worker otherwise`; its Activation bullet only said "seat one before any repository mutation". I added `(`herdr-agents --add-worker [<worktree>]`)` there. The word budget test (≤ 450) then failed at 453, so the bullet reads "Without a seated worker, seat one (…)" and "the agmsg bus and a seated worker exist here" (was "for this repository"); the rule is 449 words.
2. **Boundary tab check**: the manifest worktree's tab is now reported like any added worker's (only the main checkout is a seat). On this machine the live report therefore lists this very seat (`worker still seated at .claude/worktrees/worker-c` and its tab) while I am seated; that is the intended signal at a boundary.
3. **Heal split anchor**: excludes audit, `files` and linked-worktree panes, but still allows a legacy pair worker pane in the main checkout (same tab as the orchestrator), which keeps `test_existing_legacy_files_pane_is_not_reused_for_claude_or_split_again` green.
4. **Bootstrap**: no Codex delivery in the main checkout any more, for any repository (see above).
5. **Test inventory** (validation §4): 55 tests of retired behaviour deleted (worker split, restart-worker, pane order/width repairs, the main-checkout worker identity guard, full-mode worker kind/profile/args, main-path worker seating); 11 rewritten or converted (the two worker-seat refusals became add-worker tests that also cover the default worktree); 4 new (worktree attach exit, empty manifest worktree at a boundary, and two Bot-P1 regressions). Two fixtures orphaned by the deletions (`write_legacy_seated_pair`, `install_noop_sleep`) were removed. `resolve_worker_kind`/`resolve_worker_profile` are unchanged; their full-mode tests were deleted, and add-worker tests exercise them.
6. **Out of allowed_files, not edited** (stale wording only, both still pass): `scripts/validate-agent-assets.py:773-774` requires the README to contain `herdr-agents --restart-worker` "for worker relaunches" — satisfied by the retirement note, but the message is stale; `home/dot_codex/rules/default.rules:16` comment still says `herdr-agents --restart-worker`. Known residual in a named site, left unchanged: SKILL "Identity, delivery, and storage" still says `herdr-agents --bootstrap-agmsg` sets Codex to `turn` and Claude Code to `both`; after this change that holds for the manifest worker worktree (bootstrap mode calls `ensure_worker_delivery` there), and the main checkout gets only the orchestrator's `both`. The SKILL's audit "pair form" wording and its architecture line 12 / self-naming line 32, and README lines on the audit "pair" form, were left as named-site discipline.

## Bot threads (none resolved by the worker)

- 4225776331 (P1, executable_herdr-agents:2098, a normalized claude worker taken for the orchestrator): `fixed:dfdbb8c5`; regression tests fail on 60d49593 and pass now (validation §3).
- 4225776337 (P1, executable_herdr-agents:2095, two `--config` overrides through spawn options): proposed `not-applicable: the installed upstream agmsg 1.5.0 lib/spawn-options.sh parser is line-based and emits a --config token pair for every "  --config:" line, verified in validation §5 with our exact two-line shape, so both the network and writable-roots overrides reach codex; the add-worker spawn options are unchanged by this PR`.
- Bot on the final head bb2edb38: `bot: none` (no review within the 15-minute wait ending 02:11:22Z, none at the 02:11:47Z recheck).

## Validation summary

shellcheck rc=0; `--restart-worker /tmp/nonexistent` → the retirement line, rc=2; `test_herdr_agents` + docs: 206 tests, failures=28 errors=3, exactly the sandbox baseline (add-worker tests that cannot run in this sandbox; all pass in CI); `make unit-test` at bb2edb38: failures=73 errors=10, identical id list to origin/main 02d65ca7 in the same sandbox (`comm -3` empty); validate-agent-assets rc=0; boundary `--report` rc=0 with the expected live lines; prettier clean; CI 13/13 pass.

## Other

- CompactionDB: decision `0a4b804a-1356-4b94-8188-93c1aeb684a9` (validation §7). [memory:decision] dotfiles-T116 (orchestrator 2026-10-09): Claude Code startup seats only the orchestrator; workers are seated on demand with `herdr-agents --add-worker [<worktree>]` (default: the manifest worker_worktree) and removed with `--remove-worker`; `--restart-worker` is retired; a worker identity left at a worktree at a boundary is a violation; the cap stays at three concurrent workers.
- Forbidden actions: none of the task's ran (no make update/upgrade, no canonical-clone access beyond the boundary check's read-only probes, no live herdr-agents mode — every launcher run was a unit test with fakes, except `--restart-worker /tmp/nonexistent`, which exits before touching anything; no agent-config.yaml edit; no thread resolution; no `git worktree prune`).
- Out-of-sandbox actions, all Worker Playbook step 4 exceptions: `git push` / `gh` (HTTPS push with the T114 command), the CompactionDB `memory add`, writing and masking these artifacts in the main checkout, `agmsg-dispatch`.
- Live verification (fresh run and persisted-session restore) is the orchestrator's, per the task.
- Stale-graph hook: did not fire. plan-mode-used: no. cost: n/a

## Revise round 1 (2026-10-09): status ready_for_review

- **Final head** `ff4ffa0f55a09c36db2467f2568914608aaec4d4` on PR #306 (one commit on bb2edb38); all 13 checks pass. `main` is still 02d65ca7.
- `scripts/validate-agent-assets.py`: the README pin now requires both `herdr-agents --add-worker` and `herdr-agents --remove-worker`, message `README.md must document herdr-agents --add-worker and --remove-worker for seating workers on demand`. `tests/unit/test_validate_agent_assets.py`: both README fixtures carry the two commands, and the pin test is renamed `test_agent_manifest_requires_readme_to_document_on_demand_seating` with the new message; against the old validator it fails, and the fixture-based manifest test errors on the old `--restart-worker` demand (validation, round 1).
- `home/dot_codex/rules/default.rules`: the comment now reads `(herdr-agents --remove-worker and then --add-worker for a worker seat)`.
- SKILL "Identity, delivery, and storage": the bootstrap sentence now says `--bootstrap-agmsg` (and full or attach mode) sets the main checkout's orchestrator hooks, Claude Code on `both`, and that a worker seat gets its own hooks from `--add-worker` (Codex `turn`, Claude Code `both`) in the worktree's `.codex/hooks.json` or `.claude/settings.local.json`; the rest of the bullet is unchanged. This closes the residual named in the first report.
- The only `--restart-worker` text left in the tree is the launcher's own retirement (its `@option` line, usage note and exit message) and the tests and README retirement note that pin it.
- `make render-check` rc=0; `validate-agent-assets` rc=0; `test_validate_agent_assets` + `test_agmsg_orchestration_docs`: 112 tests OK; prettier on SKILL.md clean.
- **Bot:** `bot: none` on ff4ffa0f (15-minute wait ended 02:44:30Z; none at the 02:44:45Z recheck). Threads unchanged: 4225776331 `fixed:dfdbb8c5`; 4225776337 dispositioned not-applicable by the orchestrator.
- plan-mode-used: no. cost: n/a
