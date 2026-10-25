# U22 `omp skill list` without the 56 foreign-provider warnings; the hcom pin evaluated against measured facts — brief

GOAL
Two measured clean-ups of the seat environment. (1) `omp skill list` on a seat profile prints 56 "Agent Plugins" warnings for skills found under `~/.claude`, `~/.codex` and `~/.cursor` (docs/omp-skills.md:39: `enabledProviders` governs which skill roots omp reads); the seat overlays enable only the providers the seats use, so the list is quiet and the warnings cannot hide a real one. (2) The hcom pin: hcom 0.7.31 (2026-10-21) has been available for the whole day ("hcom v0.7.31 available" on every call); the pin is bumped only if every hcom fact the levers rely on still holds under 0.7.31, measured, else the facts that changed are recorded and the pin stays.

SCOPE
One branch `chore/omp-skill-providers-hcom-pin` from `origin/main` (b51d44eb or later). May write: `home/dot_agents/agent-config.yaml` (the omp profile `skills`/`enabledProviders` keys the generator renders into `~/.agents/omp/profiles/<role>.yml`), `scripts/generate-agent-configs.py` only if the key is not yet rendered, the generated profile files, `tests/unit/test_generate_agent_configs.py` and `tests/unit/test_omp_config_merge.py` for the pin; for the hcom part: the hcom pin's single source (find it: `git grep -n '0.7.30' -- . ':!.orchestration'`), its lockfile or receipt if any, and `docs/` lines that name the version. Nothing else.

CHANGE
1. Measure first, under a scratch HOME with the rendered profile copied in (`HOME=$TMPDIR/u22-home`): `omp --profile audit skill list --json` count of warnings and of listed skills before; the same after the overlay change; paste both. The seats' own skills (`~/.agents/skills`, the `customDirectories` entry) must still be listed in full, same count.
2. hcom: list the facts the levers and tests assume (from `scripts/orchestrator/hcom-seat`, `hcom-dispatch`, `bus-history.sh`, `regime-start`, `tests/unit/test_hcom_seat.py`, `test_hcom_dispatch.py`: the `hcom omp` launch flags and `--go`, `extract_launch_flags` consuming only before `--`, `hcom list <name> directory`, `hcom send --thread --from --json`, the `listening`/`active` statuses, the stop-record fields `regime-start` parses). For each, the 0.7.31 measurement in a scratch store (`HCOM_DIR=$TMPDIR/u22-hcom`): the command and its output. If all hold, bump the pin, regenerate, and paste the installed version check; if one differs, no bump, the fact table in the PR body, and the orchestrator decides.

ACCEPTANCE
1. Before/after warning counts pasted (after: 0 from foreign providers), the seats' skill count unchanged; `make render-check` and `make validate-agent-assets` pass.
2. The hcom fact table with one measured row per fact and the disposition (bump or hold); on a bump, `hcom --version` from the installed path pasted after `make update` is the orchestrator's step 7, not yours.
3. CI green; PR body `Program-Unit: regime-cutover/U22`, a threat table (the overlay change narrows what omp reads; the pin bump changes a tool every seat runs: name the facts measured), the footer; pre-RESULT five-point self-check; orchestrator verdict for part 1; part 2 with a bump gets the audit seat when it is back, else the orchestrator holds the bump as a separate commit on the same branch (one commit per part).

TIMEBOX
90 minutes.

FORBIDDEN
No edit to the live `~/.agents/omp/profiles` or `~/.omp` by hand (scratch HOME only; chezmoi deploys); no `hcom update` on this host; no omp subagent; no merge, rebase, force-push, PR close.

REPORT
Per STANDING 12 plus the RESULT line (standing order 23).

STANDING
`~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` (lines 20 to 24).
