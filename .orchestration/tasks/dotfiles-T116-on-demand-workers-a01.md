# AGMSG-TASK dotfiles-T116-on-demand-workers-a01

Drafted 2026-10-09 by the orchestrator seat (`claude-deep-dot`, w4:p1). Operator directive 2026-10-09 (chat): at Claude Code startup only the orchestrator pane starts; worker panes are seated on demand and removed when done, the way the auditor already runs, instead of the resident pair (orchestrator plus one worker) that `herdr-agents` full mode creates and the SessionStart `--attach` hook heals. Kind: the `herdr-agents` launcher, the boundary check, their unit tests, SKILL, rule and README prose; no permission, sandbox or hook block; Claude seat allowed (precedent T22, T65). Dispatched to `claude-standard-dot-a001` (worker-c) after T114 (#304) merged, because the files overlap T114's.

## Target behaviour, stated once

- **Startup.** `herdr-agents [DIR]` (full mode) creates the managed workspace with the orchestrator pane only and starts Claude there; it never prepares a worker seat, splits a worker pane or starts a worker agent. Healing an existing workspace follows the same rule. The SessionStart `--attach` hook claims the orchestrator seat and prints `seat_claim=` and the `agmsg-orchestration:` directive as today, and never seats, restarts or repairs a worker pane.
- **Workers on demand.** `herdr-agents --add-worker [<worktree>] [--kind codex|claude] [--profile NAME] [--ready-timeout SECONDS] [DIR]` seats a worker in its own tab of the orchestrator's workspace exactly as it does today for additional workers; a missing `<worktree>` defaults to the manifest `worker_worktree` (`HERDR_AGENTS_WORKER_WORKTREE`). `herdr-agents --remove-worker <worktree> [--force]` removes it as today. Every worker identity carries an `-aNNN` suffix (already the add-worker rule). The cap stays at three concurrent workers.
- **Retired.** `--restart-worker` exits 2 with `herdr-agents: --restart-worker is retired; run herdr-agents --remove-worker <worktree> and then herdr-agents --add-worker <worktree> [--kind …] [--profile NAME]` and does nothing else. The resident-pair pane split, `prepare_worker_seat` as a startup step, `restart_worker_in_pane`, the pair-order and equal-width repairs, and `AGMSG_CC_MONITOR_KEEP_ALIVE` for a pair worker go away with it (a spawn-seated worker gets its Monitor through its actas boot, as the SKILL already says). The `audit` tab logic is unchanged.
- **Boundary.** `scripts/check-regime-boundary.sh`: the only active seat is the main checkout. A manifest `worker_worktree` with no identity is normal and never reported. Any agmsg identity (claude-code or codex) at a linked worktree under `.claude/worktrees/` at a boundary is a violation `worker still seated at <worktree> (herdr-agents --remove-worker <worktree>)`; a worktree with more than one name per type stays `stray <type> identities at …` as today. The existing added-worker tab and workspace checks stay. Header `@description` updated.
- **Prose.** The rule `home/dot_config/claude/rules/agmsg-orchestration.md` Activation bullet: `seat one first (herdr-agents --add-worker [<worktree>])` replaces the `--restart-worker in the pair, --add-worker otherwise` wording. The SKILL: "Regime activation and progress" (seat with `--add-worker`; the pane-less bullet and the start checklist lose their pair/`--restart-worker` sentences; `Launch or relaunch a worker pane only through herdr-agents modes` names `--add-worker` and `--remove-worker`; `Activate a worker model or profile change with herdr-agents --restart-worker` becomes remove then add), "Parallel workers" (`resident workers` becomes `seated workers`; `Keep at most three workers in total, counting the resident pair worker` becomes `Keep at most three workers in total`), "Identity, delivery, and storage" (the `AGMSG_CC_MONITOR_KEEP_ALIVE` sentence and the pair-worker bullet that starts `Worker panes run in their worktree` are rewritten for seats created by `--add-worker`: identity registered with `AGMSG_RESOLVE_PROJECT=0` at the worktree, delivery set on that path, Monitor through the actas boot), the Stop checklist (`remove every worker with herdr-agents --remove-worker <worktree>`; `The orchestrator workspace itself stays resident`). README: the pair description (around lines 658–720), the `--restart-worker` section (around 770–792, becomes the retirement note), the resident-pair paragraphs (around 822–829 and 859–875), and the usage block. State each rule once; the README and rule refer to the SKILL for the procedure. `home/dot_local/bin/common/executable_herdr-agents` shdoc header and usage text follow.

## Code anchors (from the orchestrator's read of HEAD 52e56c89; re-locate after #304)

`executable_herdr-agents`: full mode `herdr workspace create` ~2610, orchestrator `start_claude_in_pane` ~2628, `prepare_worker_seat` ~2629, `split_agent_pane` ~2631–2633, `start_worker_agent` ~2635; attach repair ~2470–2493; `--restart-worker` parse ~1981 and block ~2511–2543 with `restart_worker_in_pane` ~1442–1457; directive text ~692 and ~1200; `--add-worker` parse ~1984–2016 (default the worktree here); `ensure_worker_worktree` ~253, `ensure_worker_identity` ~287, `ensure_worker_delivery` ~335, `start_worker_agent` ~1210–1254. `check-regime-boundary.sh`: seats array ~72–73 and the per-seat loop ~84–88. Tests in `tests/unit/test_herdr_agents.py`: full-mode split (~2489, ~2518, ~4118, ~5331, ~5361), attach repairs (~801, ~847, ~864–910), restart-worker (~2409, ~2680, ~3947, ~4032, ~4070, ~4087, ~4104, ~5026, ~5396), directive (~600, ~753), boundary seats (~3541, ~3558). Delete the tests whose behaviour is retired, rewrite the ones whose expectation changes (full mode creates one pane and starts no worker; attach heals no worker; `--restart-worker` exits 2 with the retirement line; `--add-worker` without a worktree uses the manifest one; the boundary check reports a seated worker worktree and accepts an empty one), and keep the rest green. `tests/unit/test_agmsg_orchestration_docs.py` pins SKILL phrases; update what it pins.

Forbidden: anything else; `make update`; `make upgrade`; touching `~/.local/share/chezmoi`; running `herdr-agents` modes against the live workspace (unit tests use fakes; the orchestrator does the live verification); thread resolution; editing `home/dot_agents/agent-config.yaml` (T115 owns the profile values; `worker_worktree` keeps its meaning as the default add-worker seat).

Live verification is the orchestrator's (SKILL "Live verification"): after the merge and `make update`, a fresh `herdr-agents` run and a persisted-session restore must show one orchestrator pane and no worker until `--add-worker`; record it in the acceptance.

[memory:decision] dotfiles-T116 (orchestrator 2026-10-09): Claude Code startup seats only the orchestrator; workers are seated on demand with `herdr-agents --add-worker [<worktree>]` (default: the manifest worker_worktree) and removed with `--remove-worker`; `--restart-worker` is retired; a worker identity left at a worktree at a boundary is a violation; the cap stays at three concurrent workers.

## Repo / branch

worker-c; after #304 merged: `git fetch origin`; `git switch -c feat/on-demand-workers --no-track origin/main`.

## Allowed files

`home/dot_local/bin/common/executable_herdr-agents`, `scripts/check-regime-boundary.sh`, `tests/unit/test_herdr_agents.py`, `tests/unit/test_agmsg_orchestration_docs.py`, `home/dot_agents/skills/agmsg-orchestration/SKILL.md`, `home/dot_config/claude/rules/agmsg-orchestration.md`, `README.md`, `home/dot_agents/README.md` (only if it describes the pair). Artifacts at `.orchestration/{reports,validation,sandboxes,learning}/dotfiles-T116-on-demand-workers-a01.md`, `.orchestration/autoskill/runs/dotfiles-T116-on-demand-workers-a01.md`, worker-side review evidence `-worker-crit.json` / `-worker-review-receipt.md` under `.orchestration/validation/`, all in the main checkout through the permission gate, masked.

## Push

As T114: `GIT_CONFIG_GLOBAL=/dev/null git -c credential.helper= -c 'credential.helper=!gh auth git-credential' push https://github.com/mryfmo/dotfiles feat/on-demand-workers`; `gh pr create --base main --head feat/on-demand-workers …`.

## Validation commands (paste verbatim output, whole)

```
shellcheck home/dot_local/bin/common/executable_herdr-agents scripts/check-regime-boundary.sh; echo "rc=$?"
bash home/dot_local/bin/common/executable_herdr-agents --restart-worker /tmp/nonexistent; echo "rc=$?"
uv run python -m unittest tests.unit.test_herdr_agents tests.unit.test_agmsg_orchestration_docs 2>&1 | tail -3
make unit-test 2>&1 | tail -3
uv run --no-project --with pyyaml scripts/validate-agent-assets.py; echo "rc=$?"
bash scripts/check-regime-boundary.sh --report; echo "rc=$?"
mise x node npm:prettier -- prettier --check README.md home/dot_agents/skills/agmsg-orchestration/SKILL.md home/dot_config/claude/rules/agmsg-orchestration.md 2>&1 | tail -2
gh pr checks <pr>
```

## Completion

PR to `main` (English title `feat(herdr-agents): seat only the orchestrator at startup and workers on demand`, English body stating the user-visible changes: `herdr-agents` no longer starts a worker pane, `--restart-worker` is retired, the SessionStart hook heals no worker, `make check-regime-boundary` reports a worker left seated; attribution footer), CI green, Bot wait per the SKILL, artifacts, the CompactionDB `memory add` of the decision line, then `AGMSG-RESULT v1 task_id=dotfiles-T116-on-demand-workers-a01` via `agmsg-dispatch dotfiles-conformance claude-standard-dot-a001 claude-deep-dot w4:p1 "<single line>"`. max_turns=20.

## Base note (orchestrator, 2026-10-09)

`main` is `02d65ca7` (#304, T114) on `64090870` (#305, T115); branch from that `origin/main`. The SKILL boundary bullet, `check-regime-boundary.sh` and `test_herdr_agents.py` carry T114's changes, so re-locate the anchors above before editing; the canonical-clone section of the boundary check stays as it is.

## Amendment 1 (orchestrator, 2026-10-09) — one runtime-health assertion follows the retired line

`tests/unit/test_runtime_health.py` is added to the allowed files for one change only: `test_agent_launchers_do_not_hardcode_model_ids` pins the retired resident-worker launch line (`--profile "${HERDR_AGENTS_WORKER_PROFILE:-standard}"`). Keep the test's intent (the launcher names no model id, and the worker profile reaches the launch through `HERDR_AGENTS_WORKER_PROFILE` with `standard` as the default) by pinning the surviving `--add-worker` form, the exact literal that `write_spawn_options` (or whichever function builds the spawn args) uses; the three `assertNotIn` lines stay. Nothing else in that file changes. Continue: push, CI, Bot wait, RESULT.

## Revise round 1 (orchestrator, 2026-10-09) — the three stale `--restart-worker` sites your report named, nothing else

Accepted as delivered: dfdbb8c5 (Bot P1 4225776331, `worker_pane_filter`, two regression tests) and the Amendment 1 assertion. Bot P1 4225776337 is dispositioned `not-applicable` by the orchestrator on your validation §5 (the installed agmsg 1.5.0 `agmsg_spawn_options_tokens` emits a `--config` token pair for each line; the spawn options are unchanged by this PR); the upstream flat-map contract is recorded as a known risk in the acceptance.

Retiring `--restart-worker` must not leave live text that still prescribes it. Allowed files gain `scripts/validate-agent-assets.py` (one pin and its message), `tests/unit/test_validate_agent_assets.py` (the assertions of that pin) and `home/dot_codex/rules/default.rules` (one comment):

1. `scripts/validate-agent-assets.py` ~773–774: replace the pin `if "herdr-agents --restart-worker" not in readme: fail("README.md must document herdr-agents --restart-worker for worker relaunches")` with a pin that the README documents on-demand seating: both `herdr-agents --add-worker` and `herdr-agents --remove-worker` must appear, message `README.md must document herdr-agents --add-worker and --remove-worker for seating workers on demand`. Update the fixture and assertion in `tests/unit/test_validate_agent_assets.py` (~457, ~491) accordingly.
2. `home/dot_codex/rules/default.rules` ~16: the comment `(herdr-agents --restart-worker for the pair worker)` becomes `(herdr-agents --remove-worker and then --add-worker for a worker seat)`.
3. `home/dot_agents/skills/agmsg-orchestration/SKILL.md` "Identity, delivery, and storage", the sentence beginning `At worker setup, `herdr-agents --bootstrap-agmsg` sets Codex to `turn` and Claude Code to `both``: rewrite it to state what `--bootstrap-agmsg` now does (the main checkout's orchestrator hooks; a worker seat's hooks come from `--add-worker`/spawn, per your report's residual note), keeping the rest of the bullet.

The `.ua/knowledge-graph.json` mention is out of scope (the graph is stale by design between refreshes). Then `make render-check`, `validate-agent-assets.py`, the two test modules, prettier on SKILL.md, push over HTTPS, CI, Bot wait on the final diff head, `AGMSG-RESULT v1 … round=1`.
