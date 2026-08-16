# T65b: Repin Pi to 0.84.1 (7-day supply-chain cooldown) — anchors re-verified

task_id: T65b
repo: /Users/mryfmo/Workspace/dotfiles
team: dotfiles-conformance
worker: codex-deep-dot
plan: PLAN-pi-worker-integration.md (decision log: cooldown ruling)

[memory: decision — The Pi pin is 0.84.1, the newest version satisfying the 7-day npm supply-chain cooldown; 0.84.2 promotion follows the normal staleness-managed upgrade once it ages past the cooldown. All pinned-source anchors are re-cited against the v0.84.1 tag.]

## Background (orchestrator-verified live)

`mise install` enforces a 7-day version cooldown (upgrade-tools.sh
`--before 7d`; npm ETARGET "with a date before 8/9"). 0.84.2 (released
2026-08-14) is 2 days old and correctly blocked. Bypassing the policy is
declined; the root-cause fix is pinning 0.84.1 (2026-08-07).

## Fix (exact)

1. scripts/validate-agent-assets.py: the pi assets category's exact-pin
   constant 0.84.2 -> 0.84.1 (keep the range/latest rejection).
2. Re-verify EVERY pinned-source anchor cited in T65/T66/T67 against the
   v0.84.1 tag (raw.githubusercontent.com at refs/tags/v0.84.1):
   settings-manager.ts defaultProjectTrust values; security.md trust
   semantics; extensions loader default-export factory; extensions
   types.ts tool_call input/block-reason and mode/hasUI lines. For each:
   confirm identical semantics and update the line references in a short
   anchor table written to .orchestration/validation/T65b-anchors.md.
   If ANY anchor differs semantically, STOP and report via agmsg.
3. Update the T67 checker's enforced version constant
   (executable_pi-model-access-check) 0.84.2 -> 0.84.1.
4. Update tests that pin the version constant; full suite green.
5. Do NOT touch home/dot_mise (the pin lands in the orchestrator chore).

## Allowed files

- scripts/validate-agent-assets.py
- home/dot_local/bin/common/executable_pi-model-access-check
- .orchestration/validation/T65b-anchors.md (NEW)
- tests/unit/ (matching modules)
- Your artifact paths (T65b five artifacts)

## Forbidden actions

git commit; git push; chezmoi apply; bats; dependency changes; mise
config edits; cooldown-policy changes; real pi execution.

## Validation

make format / bash -n / unit-test / validate-agent-assets green; anchor
table complete; scope check.

## Completion / RESULT contract

Five artifacts (T65b set); memory add with the decision fact;
effects=none. Reply `AGMSG-RESULT v1 task_id=T65b`. max_turns=15.
