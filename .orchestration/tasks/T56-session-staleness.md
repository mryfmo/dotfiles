# T56: Session staleness detection (H4)

task_id: T56
repo: /Users/mryfmo/Workspace/dotfiles
team: dotfiles-conformance
worker: codex-deep-dot
plan: .orchestration/tasks/PLAN-harness-composability-integration.md (Phase 3)
analysis: .orchestration/analysis/harness-composability-research.md (H4)

[memory: decision — Sessions detect their own staleness: an async SessionStart hook and a doctor mode compare managed-asset update times against session start and print a restart recommendation; detection is an approximation from mtimes/plugin-cache versions, never from harness internals.]

## Goal

The harness has no HMR; the best external approximation is detecting "this
session is running code older than what is installed" and saying so.

## Allowed files (edit boundary)

- home/dot_local/bin/common/executable_agent-session-staleness (NEW;
  language per step 1 — record the choice and reason)
- scripts/check-agent-runtime.py (doctor integration)
- home/dot_agents/agent-config.yaml (ONE async SessionStart hook entry)
- scripts/generate-agent-configs.py ONLY if the hook entry flows through
  generation (verify; state the finding)
- Regenerated outputs of the generator if and only if the yaml change
  requires them (home/.chezmoitemplates/claude-settings-managed.json)
- tests/unit/ (matching module)
- Your artifact paths (T56 five artifacts)

## Forbidden actions

git commit; git push; chezmoi apply; bats; dependency changes; parsing
harness-internal/undocumented state files; synchronous hook registration;
changing existing hook order (append only — T55's category must stay
green).

## Work order (exact; ambiguity -> ask via agmsg)

1. Discovery: determine the observable "installed version" signals, in
   this preference order, and record evidence:
   (a) Claude plugin cache directories (~/.claude/plugins/cache/<mkt>/<plugin>/<version>/)
   vs the highest installed version present;
   (b) mtimes under ~/.agents/ managed asset roots (compactiondb, skills,
   plugins) and the rendered ~/.claude/settings.json / ~/.codex/\*.toml.
   Do NOT read harness session state; the detection contract is
   "approximation from public filesystem artifacts" (document in shdoc).
2. Implement `agent-session-staleness check --since <epoch>`:
   - Lists managed assets updated after <epoch>: newer plugin-cache
     version dirs than the newest one older than <epoch>, and files under
     the mtime-scanned roots with mtime > epoch (bounded scan; exclude
     state/spool/health and _.sqlite_ patterns).
   - Output: nothing + exit 0 when clean; otherwise 1-5 lines starting
     with `restart recommended:` listing the assets (dedup by root).
   - Hard limits: 5s wall (self-enforced), any internal failure -> exit 0
     silent (stderr one line allowed). Never nonzero exit.
   - No arguments mode: prints the 10 most recent managed-asset updates
     with timestamps (doctor/debug use).
3. Wire ONE async SessionStart hook entry (append, after existing
   entries) passing the session start time; if the hook payload does not
   carry an epoch, use hook-invocation time (== session start for
   SessionStart) — state the mechanism.
4. Doctor: add `--session-staleness [epoch]` to check-agent-runtime.py
   that shells the same script (single source of truth; no logic
   duplication).
5. Tests: fake HOME fixture with controlled mtimes/cache dirs — detect /
   no-detect / failure-exit-0 / bounded-scan (a huge tree does not blow
   the time budget — use a generated fixture with many files and assert
   wall time < 5s).
6. Style gates for the chosen language (shdoc+shfmt or uv/ruff via repo
   conventions).

## Validation (record in validation artifact)

1. `make validate-agent-assets` green (T55 category must accept the new
   hook entry — if it fails on ordering, DO NOT touch T55's constants
   without asking via agmsg).
2. `make unit-test` all green (totals + new count).
3. `make format` exit 0; `bash -n` if bash.
4. Fake-HOME three-case transcripts.
5. `git status --porcelain` / `git diff --stat` -> only Allowed files.

## Completion / RESULT contract

- Five artifacts (T56 set); T45-contract memory add executed and quoted.
- Live verification (real session warning) is T61 E2E-2'.
- Reply `AGMSG-RESULT v1 task_id=T56 status=ready_for_review ...`.
  max_turns=25.
