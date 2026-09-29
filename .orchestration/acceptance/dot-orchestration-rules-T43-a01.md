# Acceptance: dot-orchestration-rules-T43-a01

Dispatched 2026-09-29T13:16Z (task_commit 258339f). RESULT r1 13:35Z (head
557502b, PR #214). RESULT r2 21:13Z (head 1843dd1 = fix 99c1174 + merge of
`.orchestration`-only main f45cf73).

## Round 1 review and audit

Orchestrator review of 557502b: `scripts/ua-symbol-coverage.py` (stdlib,
per-file function+class table, exit 1 on unexplained loss) reproduces the
eight T41 regressions; rule bullets in `understand-anything.md`, the Codex
mirror and the SKILL (invariant, Worker Playbook 13, Orchestrator step 3
naming `make render-check`); `make render-check` target; README sentences;
one test. CI all pass. The diff also showed the T39 sandbox becoming active
mid-task in worker-c (uv cache read-only, gh 401, phantom untracked stubs,
herdr rename failure) — recorded under T39 leg 1.

Codex audit of 557502b (`…-audit.md`): `Verdict: incorrect`, two P2s, both
reproduced by the auditor: (1) any failed `git show` counted as a deleted
file, so an invalid `--repo-ref` marked every loss explained and exited 0
(fail-open); (2) `defs < before` excused the whole decrease, including
extraction loss beyond the source deletion. **Decision (round 1): REVISE**
(sent 20:58Z, read).

## Round 2 review

99c1174 (read from origin refs): `verify_ref` rejects empty or `-`-prefixed
refs and unresolvable refs via `rev-parse --verify --quiet --end-of-options
REF^{commit}`, exit 2 before any table; a failed `git show` is "gone" only
when `git ls-tree REF -- path` is empty, otherwise exit 2 (`CoverageError`);
a decrease is explained only when `new >= min(old, defs)`; no-grammar files
never explain a decrease. Tests: unresolvable ref (3 subTests, no `leak`
file), file gone at REF, partial deletion with extra loss → REGRESSION,
partial deletion fully accounted → explained; the worker showed the old
script failing 4 of them. Real data: T41 r1 vs 72b8901 → 8 regressions
exit 1; self-compare → 0, exit 0; bad ref → exit 2. `make unit-test` 614
OK, validate ok, render-check ok (run unsandboxed because of the uv cache).
CI all pass on 1843dd1. CompactionDB 992478eb present.

Codex audit of 99c1174: **queued** — the operator paused Codex at 21:08Z
(rate limit); the audit lane shares that account. Merge waits for the audit
or an explicit operator waiver.

**Decision: PENDING AUDIT** (review complete, no findings from the
orchestrator side).
