# T25: Build permgate — a self-hosted permission gate on existing agent auth

## Objective

Replace the retired ccgate with a repo-owned PermissionRequest gate that (a)
uses ONLY existing agent auth legitimately — the LLM layer calls the official
`claude` CLI headless, never raw APIs or extracted tokens — (b) keeps the
classifier model and policy fully under repo control, and (c) is fail-closed:
anything not confidently matched to a pre-defined safe category falls through
to the harness's native prompt.

## Architecture (3 layers, decided)

1. **Deterministic rules** (no LLM): repo-versioned allow/deny patterns
   evaluated first. Generated initially from real ccgate metrics
   (`ccgate codex metrics --details 50`, `ccgate claude metrics --details 50`
   — the binary is still installed; read-only usage is fine).
2. **Bounded LLM classification**: `claude -p --model haiku --max-turns 1`
   with a repo-versioned classification prompt. The classifier may ONLY map a
   request into one of the explicitly whitelisted safe categories (read-only
   inspection / search / status / diff / version checks). Anything else, any
   parse failure, any timeout → layer 3. Tool use disabled for the inner
   session; recursion guarded (see Hard requirements).
3. **Fallthrough**: return the harness's native "ask" so a human decides.

Decisions: allow (layer 1 or confident layer 2 category match), deny (layer 1
deny patterns only — the LLM never denies), ask (everything else). Every
decision appends one JSONL line (ts, agent, tool, input hash/summary, layer,
decision, latency_ms) to `~/.local/state/permgate/decisions.jsonl` — no
secrets, no full command output.

## Hard requirements

- **Both hook contracts verified from official docs first**: Claude Code
  `hooks.PermissionRequest` output schema, and Codex `[[hooks.PermissionRequest]]`
  HookInput/HookOutput. Record the exact schemas + doc URLs in the report.
- **Recursion guard**: the inner `claude -p` call must never trigger permgate
  (set a sentinel env var; permgate exits fallthrough-free/no-op when the
  sentinel is present; ALSO pass flags/settings that disable hooks for the
  inner session if supported). Prove it with a test.
- **Fail-closed everywhere**: CLI missing, non-zero exit, malformed output,
  timeout (hard cap 10s) → ask. The gate must never block the harness longer
  than the cap.
- **The LLM layer ships DISABLED (shadow mode)**: layer 2 runs and logs its
  would-be decision but the returned decision ignores it (layer 1 + ask only)
  until the orchestrator flips `llm_enabled: true` in the policy file after
  reviewing shadow accuracy. Config default in this PR: shadow.
- **Model pinned in policy file** (`model: haiku`), policy prompt versioned in
  repo; no network calls other than the official CLIs.
- Deny/ask safety rules in Claude settings and Codex config are untouched —
  permgate only sees requests that would otherwise prompt.

## Deliverables

1. `home/dot_local/bin/common/executable_permgate` (python via uv shebang or
   bash+python hybrid — pick the simplest testable form; shdoc/docstring per
   repo policy) handling both agents: `permgate claude` / `permgate codex`.
2. Policy file as single source: `home/dot_agents/permgate-policy.yaml`
   (deterministic allow/deny patterns, whitelisted categories, model, llm_enabled,
   timeout). If wiring it through `agent-config.yaml`/generator is cheap, do
   that; otherwise standalone file is acceptable — state the choice.
3. Initial deterministic patterns derived from the real ccgate metrics top
   fallthrough entries (document each pattern's source count in the report).
4. Hook wiring restored through the generator (`scripts/generate-agent-configs.py`):
   Claude settings PermissionRequest → `permgate claude`; Codex managed TOML
   `[[hooks.PermissionRequest]]` → `permgate codex`. Note: T22's
   `REMOVED_MANAGED_PREFIXES` in `home/dot_codex/modify_private_config.toml`
   currently strips `hooks.PermissionRequest` from private merges — adjust it
   so the MANAGED hook renders again while stale ccgate-era private copies
   still cannot resurrect (managed table now exists again, so the removed-
   prefix entry must be deleted or narrowed; add a merge test for this).
5. Tests: `tests/unit/test_permgate.py` — layer-1 allow/deny, unknown → ask,
   recursion sentinel no-op, timeout → ask, malformed inner output → ask,
   shadow mode never allows via layer 2, JSONL line shape, both hook output
   schemas (fixture-validated). Update validator/lifecycle assertions that
   currently require ccgate hooks to be ABSENT (validate_model_profile_assets
   in scripts/validate-agent-assets.py and tests/install/common/lifecycle.bats)
   to instead require the permgate wiring and forbid `ccgate` specifically.
6. Latency measurement: a `permgate bench` subcommand (or documented command)
   that runs N=5 layer-2 classifications against fixtures and prints p50/p95.
   Record results in validation. Acceptance gate for LATER llm enablement
   (not this PR): p50 ≤ 3s, else layer 2 stays shadow/disabled.
7. Docs: short section in README (agent permission assets) + update
   `home/dot_config/claude/rules/model-selection.md` last bullet and
   `home/dot_config/codex/AGENTS.md` model section to describe permgate
   (deterministic-first, LLM shadow, fail-closed) replacing the "ccgate
   disabled" wording.

## Out of scope / forbidden

- No auto mode, no guardian/auto_review adoption, no ccgate re-enable, no raw
  API calls, no token extraction, no new dependencies beyond stdlib + existing
  tools, no enabling llm_enabled by default, no local bats, no make upgrade,
  no merge before acceptance, no secrets in code/logs/artifacts.
- Do not remove the ccgate mise package in this task (separate cleanup once
  permgate is accepted).

## Verification

- `make unit-test`, `make validate-agent-assets`,
  `uv run --with pyyaml scripts/generate-agent-configs.py --check`, shellcheck/
  shfmt for shell parts — all green.
- Live smoke (allowed): run `permgate claude` / `permgate codex` with fixture
  stdin payloads (3 kinds: clearly-safe read, clearly-dangerous, ambiguous)
  and show decisions + JSONL lines + bench numbers in the validation artifact.
  Do NOT flip llm_enabled.
- Branch `feat/permgate` from origin/main in a separate worktree, English
  Conventional commits + PR, CI green; after AGMSG-ACCEPTANCE next_action=merge:
  squash-merge, ff-only main sync, worktree/branch cleanup.

## Expected artifacts

- report: .orchestration/reports/T25-permgate-harness.md
- validation: .orchestration/validation/T25-permgate-harness.txt
- sandbox: .orchestration/sandboxes/T25-permgate-harness.md
- learning: .orchestration/learning/T25-permgate-harness.md
- autoskill: .orchestration/autoskill/runs/T25-permgate-harness.md

## Done signal

AGMSG-RESULT v1 status=ready_for_review. max_turns=60
