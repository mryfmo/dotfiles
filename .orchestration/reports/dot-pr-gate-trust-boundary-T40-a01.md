# T40 implementation complete; Git integration pending

Status: in progress under revision 3. The task file SHA256 matches `dc06f4776657a2f229be66992fd2fb21ebe1e29061f7e5dfc61e21c138ca3424`. Branch: `fix/pr-gate-trust-boundary`, currently based on `f45cf73551c449c689a69fa931adb858d4dd08fd`. The five allowed implementation files are staged; there are no implementation commits or PR yet.

The collector records GitHub base_ref/base_sha and passes only integers through gh -F; strings use -f. The guard queries GitHub head/base metadata before executing a collector, rejects mismatched evidence, checks exact/older/advanced base relationships, and executes the collector from the GitHub-authenticated base SHA. The advanced local base cannot substitute its own code or delete the collector to trigger fallback. An older base must be outside HEAD's first-parent chain. Evidence exclusions validate both lexical and resolved paths under .orchestration/validation/ with the required suffix; symlink aliases remain in the diff.

The initial regressions failed before implementation. Additional independent-review findings were reproduced and fixed, with tests for sibling-base collector replacement/deletion, evidence aliases, and first-parent ancestry. Final targeted guard suite: 53 passed. Full suite: 625 tests, one skip, successful. Agent-asset validation passed. Independent agent follow-up found no remaining scoped findings. Local review gate passed using the saved review JSON and receipt. No local Bats execution.

The collector deliberately uses the authenticated GitHub base SHA rather than an arbitrary accepted advanced local base: ancestry and merge-base equality ensure diff coverage but cannot authenticate that local commit's code. Bootstrap remains available only when the authenticated base lacks the collector and the requested base passes binding.

Git integration is pending: origin/main advanced to a5f33eede3feb15c59031c5af904bf1c3838649b while this task was paused, so the current ancestor check failed. Revision 3 asks for a rebase preserving WIP and forbids escalation after a denied Git write. The exact index.lock denial and staged-WIP state were reported via AGMSG-PONG; orchestrator action is pending. No reset, forced checkout, force push, or merge occurred.

[memory:decision] T40: the PR integration gate binds --base to the PR recorded GitHub base, excludes from diff sizing only a .orchestration/validation/*-pr-feedback.json evidence file, and passes GraphQL string variables raw (-f), closing the three findings deferred from T38 (operator 2026-09-29).

CompactionDB decision: fdccdfbf-e3b3-4452-850d-c66b0a6df852. Exact command/output is in validation. Main-checkout DB access was explicitly excepted by the orchestrator; sandbox retry required escalation for its writer lock.

Remaining: orchestrator-assisted Git update/rebase, commit/push, PR creation with the required Doc follow-up, CI checks, final-head feedback collection/dispositions, positive/negative integration gate checks, final artifact sync and RESULT. The PR body is prepared in /tmp/t40-pr-body.md. README and Codex AGENTS.md remain unchanged.

cost: n/a
