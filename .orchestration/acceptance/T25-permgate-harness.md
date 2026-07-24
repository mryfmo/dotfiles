# T25 acceptance: permgate harness

- Task: `.orchestration/tasks/T25-permgate-harness.md`
- Result under review: PR [#92](https://github.com/mryfmo/dotfiles/pull/92),
  head `06c5a17a815e839d025322fd75272f7d57c97c82` (post adversarial-repair head;
  the bus RESULT at 2026-07-24T01:54Z referenced pre-repair head `bdfd6b2` —
  this acceptance reviewed the repaired head directly).
- Verdict: **accepted** (next_action=merge).

## Adversarial verification performed

- Full read of the 610-line `executable_permgate` and the complete
  `permgate-policy.yaml`; every fail-closed path re-derived independently:
  log-write failure suppresses allow; timeout/malformed/non-zero/missing CLI,
  invalid policy, unsafe options, sensitive structured input all end in ask;
  `PERMGATE_INNER` sentinel is a complete no-op.
- Refutation attempts, all defeated:
  - shell composition/expansion/quoting bypass — blocked by
    `SHELL_CONTROL`/`SHELL_EXPANSION` before allow patterns are consulted;
  - `git -c diff.external=…` / env-var-prefix injection — defeated by
    adjacent-token anchoring in every allow regex;
  - write-capable read options (`--output`, `--ext-diff`, `--textconv`,
    `--web`, `--watch`, `-O`, `-w`) — double-blocked by
    `UNSAFE_READ_OPTIONS` and the git-diff lookahead;
  - `git branch --list -D <branch>` — live-tested in a throwaway repo: git
    rejects the combination (exit 129, branch preserved);
  - `sysctl` write — impossible: the argument charset excludes `=`;
  - LLM overreach — the classifier can only confirm actions the deterministic
    policy already maps to the returned category, never denies, and both
    providers ship `llm_enabled: false`; enablement is additionally gated in
    the validator and lifecycle tests.
- All eight review findings (native + CodeRabbit) re-located in the diff with
  their regression tests; 28 permgate unit tests plus Claude-settings and
  Codex-config merge regression tests cover the hard requirements
  (both hook schemas fixture-validated, shadow-mode invariants, secret
  boundary, recursion, timeout, stale-ccgate replacement, idempotent merge).
- Wiring: manifest-driven generator renders the PermissionRequest hook for
  both agents; `REMOVED_MANAGED_PREFIXES` deleted with a regression test
  proving a stale private `ccgate codex` table cannot survive; Claude merge
  treats `PermissionRequest` as managed while preserving unrelated user hooks.
- Docs updated in README, `model-selection.md`, and Codex `AGENTS.md`;
  ccgate mise package intentionally retained (separate cleanup task).
- CI at head `06c5a17`: all GitHub Actions checks and CodeRabbit SUCCESS;
  all four PR review threads resolved; PR mergeable.
- Bench (validation artifact): Claude 2/5 successes p50 6071 ms, Codex 3/5
  successes p50 4911 ms — neither meets the enablement gate
  (5 successes, p50 ≤ 3000 ms, p95 ≤ 7000 ms), so both providers correctly
  remain shadow-only. This is the enforced operational gate working as
  designed, not a defect.

## Review guard

`make require-crit-review` satisfied with
`AGENT_REVIEWED=1 REVIEW_EVIDENCE=.agents/worklog/claude/T25-crit-review-receipt.md`
(evidence: `.agents/worklog/claude/T25-crit-review.json`, 9 resolved records,
preserved from the T25 worktree before its removal).

## Next action (delegated to worker)

Squash-merge PR #92 with branch deletion, verify a clean tracked tree, ff-only
sync of local `main`, remove the `/private/tmp/dotfiles-t25.LQ2j7E` worktree
and the local `feat/permgate` branch, then report completion via AGMSG-RESULT.
