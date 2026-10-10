---
reviewed_at: 2026-10-10T09:02:00Z
reviewer: claude-review-dot-a002
profile: review
session: 76641dce-e0d5-4654-b475-8f2ebdbf8cc9
design: .orchestration/tasks/dotfiles-T124-design-gate-and-reset-rule-a01.md@d31c1bb73c9568e6d65b8a55d9160d1f32d3b0167405297b85466928d38ffe0f
task: dotfiles-T124-design-review-a01
round: 3
previous: .orchestration/validation/dotfiles-T124-design-gate-and-reset-rule-a01-design-review-round2.md
---

# Design review round 3: T124 design v3

Scope as requested: each round-2 correction checked as applied, and v3 read for anything that reopens a finding. Same sources as rounds 1 and 2; no new script facts were needed beyond `require-crit-review.py:127-134` (`git_root` resolves the process cwd, so `main`'s script with the review worktree as cwd judges the review tree) and `check-regime-boundary.sh:21-23` (it already reads the seat lock through `check-agent-runtime.py`).

## Invariants

INV-1: accepted. Unchanged from v2, applied.

INV-2: accepted. Two tiers applied as written; the design tier is explicit and narrow. Note for wave 1's task, not a reopen: four design-tier entries are prose, not patterns ("the `assets:` section of `agent-config.yaml`", "sandbox and permission settings", "credential and auth helpers", "`home/dot_codex/**` policy"); a derivation rule matches paths, so wave 1 names the patterns (`home/dot_agents/agent-config.yaml` whole, `home/.chezmoitemplates/claude-settings-managed.json`, `home/.chezmoitemplates/codex-config-managed.toml`, `home/dot_claude/modify_private_settings.json`, `home/dot_agents/permgate-policy.yaml`, and the auth-helper files by path).

INV-3: accepted. One hash over the design task's keys, `design_review: {receipt, design}`, the subset rule, no `design_sha256=`, bootstrap through `main`'s gate: all applied as written. One rollout step is implied but not scheduled: waves 0, 2b and 3a merge under a gate that has INV-3, so each needs a receipt whose `design:` is the canonical key hash of the design task file, and none of the three receipts so far carries it (they hash this markdown file whole, as their task said). Required before wave 0 is dispatched: restate this design once as the `format: 2` design task file (name it; v3 leaves open whether that is this file with front matter or wave 1's task file), then one short review RESULT from a non-orchestrator identity whose receipt carries the canonical hash and `INV-1..9: accepted`. Wave 1 is the right place to produce the file; the receipt follows it.

INV-4: accepted. Unchanged, applied.

INV-5: accepted. `audit=<sha7>` on revise ACCEPTANCEs with the file required per named sha, and the Codex-orchestrator statement: applied as written; the threshold table matches (a').

INV-6: accepted. Unchanged, applied.

INV-7: accepted. `format: 2` scope, 3b before 2a, the `SKILL.md:77` rewrite: applied as written.

INV-8: accepted. The two tests are added.

INV-9: accepted. `session_id` and `cwd` in the record, the seat-lock or `cwd` mapping, the TASK-to-RESULT window, `tool == Bash` against permission-gated commands, Claude-only coverage, wave 0 and the `<task>-permgate.jsonl` extract: applied as written. Two notes for wave 2b's task: the sandbox record needs one machine-readable line the gate reads (for example `permission_gated_commands: <n>` in its front matter), which v3 does not name; and the seat lock holds the current session only, so a worker re-seated mid-task spans two sessions and the `cwd` mapping is the one that covers the whole window.

## Trust anchors

The "gate from `main`" rule is applied as written and closes the round-2 reopen. One consequence for the prose row: `make require-crit-review` is named as the gate command in `home/dot_config/claude/rules/crit-review.md`, `pr-integration.md`, `AGENTS.md` "Agent Review Evidence" and SKILL step 10.4, and the Makefile recipe runs `./scripts/require-crit-review.py` relative to its own directory (`Makefile:210-216`), so it cannot run `main`'s script against another cwd. Either those four texts name the direct invocation, or the Makefile gains a `REVIEW_TREE=<path>` variable that the target passes as the cwd. Add the three rule and AGENTS files to wave 1's allowed files or to the prose row.

## Waves

Order 1, 3b, 2a, 0, 2b, 3a is right. One routing inconsistency: wave 1 moves `HIGH_RISK_*` out of `require-crit-review.py` into the shared module, which edits the gate source that waves 2a and 2b route to the operator. Default to adopt: wave 1 creates `scripts/lib/high_risk_paths.py` and the validator imports it, the gate keeps its constants until 2a switches it to the import, and `test_validate_task.py` asserts the module's review tier equals the gate's constants in the interim, so no second list drifts. Otherwise route wave 1 to the operator.

## Nothing reopens a finding

Standing fact, history and GitHub as the only sources, the main-checkout file reads, the visible waiver, the grandfather, the grammar, the lock, the split waves, the stated residual: all stand. The residual section states the Claude-only, post-wave-0 coverage of T5 for worker conduct, as asked.

Design verdict: accept
