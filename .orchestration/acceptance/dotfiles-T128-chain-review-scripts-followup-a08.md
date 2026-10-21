# Acceptance record: dotfiles-T128-chain-review-scripts-followup-a08 (pre-dispatch)

Reset of dotfiles-T128-chain-review-scripts-followup-a07 (D-024-41, 2026-10-20 18:22 JST): local-review.sh reads the reviewed head from a private bare clone fetched from GitHub at the 40-hex sha and runs the review there. PR #439 (a07 head a644a7d9) is replaced by the a08 PR. Seat: codex-standard-dot-a013 (worker-h) after the anchor review.

- 2026-10-20: design 1 (102 lines, orchestrator-written) C-80 (`…-text-security-23f5144.md`) incorrect: P1 the preserved review cache lets a matching head/findings:0 artifact bypass Item 3.
- 2026-10-21T04:35Z-04:57Z: design 2 by author-loop (`brief-a08-v2.md`): round 1 (`…-bff1eef.md`) 4 P1 + 1 P2 (advisory consumer reads the legacy filename; a 0700 TMPDIR store is not worker-inaccessible; cache provenance cannot be closed; the caller inherits its environment; inherited regressions conflict with item 9); round 2 (`…-39b60bd.md`) 1 P1 + 1 P2 (chain-integrate.sh decides audit reuse from worker-writable shared objects and passes the shared worktree to orch-audit.sh, outside a08's scope; the committed-ledger `closed` claim is not proven by the named test). S-R5 reached.
- 2026-10-21T05:00Z: the operator chose option A (D-024-52): narrow the two claims to residual, name dotfiles-T128-chain-review-scripts-followup-a09 as the owner of the chain hardening prerequisite (audit-reuse decision and shared worktree inputs), one C-80 round under the re-plan line below, anchor review by claude-standard-dot-a011, implementation by a013.

text-security:23f5144:1	cache-bypass
text-security:bff1eef:1	advisory-consumer-filename
text-security:bff1eef:2	store-not-worker-inaccessible
text-security:bff1eef:3	cache-provenance
text-security:bff1eef:4	inherited-environment
text-security:bff1eef:5	inherited-regressions
text-security:39b60bd:1	integration-trust-chain
text-security:39b60bd:2	unproven-closed-claim

re-plan: integration-trust-chain (rows text-security:23f5144:1, text-security:bff1eef:3, text-security:39b60bd:1; three rounds found that the private local review alone does not authenticate the chain's other inputs) — specification: a08 authenticates only what it produces (the private-clone review artifact and its consumer), states every other chain input (audit reuse from the shared object store, the shared review worktree handed to orch-audit.sh, the committed-ledger reads) as residual, and names dotfiles-T128-chain-review-scripts-followup-a09 as the owner whose completion is the release prerequisite of the chain's trust claims; design: the threat rows for cache provenance and committed-ledger reads are residual with that owner, the private store lives under the orchestrator's private directory with its fetch and canonical lookup on every invocation, and the advisory consumer reads the private full-head filename; implementation: brief v3 and the re-authored a08 text; a09's text carries the two obligations; verification: the C-80 of the re-authored text reports no integration-trust-chain finding and the anchor review of another context accepts the bytes.
