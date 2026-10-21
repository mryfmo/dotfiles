---
format: 2
reset_of: dotfiles-T128-chain-glue-finish-a01
redesign_task: dotfiles-T128-chain-glue-finish-a02
design_sha256: ddb8c53f4bb98a9cd3dc1dfd75d4b65c09b4e548dc1ae9908f0d59bc661bd369
redesign_source: dotfiles-T128-chain-glue-finish-a02-redesign-review-a01
redesign_seat: claude-standard-dot-a011 (standard profile, a context other than the a01 workers a002/a006 and other than the implementer)
reason: "PR #378 (five worker rounds up to 2026-10-17) fails main's comparison lint after its update-branch to b09c88c6 (R1 at scripts/orchestrator/chain-finish.sh:67 and :111, a lint merged after round 5); the mechanism-PR two-round limit forbids a sixth worker round (D-024-63), so a bounded reset text by another context carries the two-line lint conformance and one fixture."
---

# Design reset: dotfiles-T128-chain-glue-finish-a01, anchored 2026-10-21

- **What stopped:** no sixth worker round; the a01 design (`dotfiles-T128-regime-v3-a01` by reference) is unchanged, only the comparison form of two lines.
- **Why this record now:** the regime's reset form wants the redesign accepted by another context before dispatch.
- **Redesign:** `.orchestration/tasks/dotfiles-T128-chain-glue-finish-a02.md` at sha256 `ddb8c53f4bb98a9cd3dc1dfd75d4b65c09b4e548dc1ae9908f0d59bc661bd369` (64 lines, 3 allowed_files, caps 40/120 for the reset's own commits, Checks pasted: canonical main 4eafd890, PR head b09c88c6, merge-base 4eafd890, inherited 178/275, the CI failure line). Authored by the orchestrator (security: false, no C-80).
- **Anchor:** RESULT 2994 of `dotfiles-T128-chain-glue-finish-a02-redesign-review-a01` by claude-standard-dot-a011: `verdict=accept design_sha256=ddb8c53f…`; one P3 noted in its review file (worker-d, until the next records boundary).
- **Dispatch:** to claude-standard-dot-a008 (worker-f) at these bytes, continuing PR #378's branch `tools/chain-glue-finish` from b09c88c6.
- **Waiver:** none.
