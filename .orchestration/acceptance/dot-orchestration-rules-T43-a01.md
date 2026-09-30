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

Codex audit of 99c1174: queued at 21:08Z (operator paused Codex, rate
limit); run 2026-09-30 04:10Z after the operator confirmed the pause lifted.

## Round 2 audits (2026-09-30, `herdr-agents --audit`, gpt-6-astra, read-only, high)

- 99c1174 (`…-audit-99c1174.md`): **Verdict: correct**, no findings; 12
  read-only probes passed; CI not re-verified by the auditor (GitHub
  unreachable from its sandbox) — CI all pass confirmed by the orchestrator
  on 1843dd1 via `gh pr view`.
- 1843dd1 (`…-audit-1843dd1.md`, the `.orchestration`-only merge):
  **Verdict: incorrect**, two P2s:
  1. T44 task file `allowed_files` says "sandbox.network block only" and
     forbids other sandbox keys while addendum 8 requires
     `filesystem.extra_allow_write`. Confirmed; not a T43 defect (the file
     arrived through the merge from main). Disposition: T44 task file
     amended by the orchestrator (see its acceptance record); the worker
     already resolved the conflict in favour of the explicit addendum.
  2. Validation :137 recorded `exit=0` after `| grep`, so the claimed gate
     exit 1 was not evidenced (my round-2 sentence "8 regressions exit 1"
     repeated the worker's claim). Confirmed. Disposition: re-derived by the
     orchestrator from git objects (script at 1843dd1, graphs 72b8901 →
     c3afc7a, `--repo-ref 72b8901`): `gate_exit=1`, `regressions: 8`;
     self-compare exit 0; unresolvable ref exit 2. Evidence gap closed; the
     r3 validation must capture exit codes without a pipe.

## PR #214 feedback sweep (head 1843dd1, `…-pr-feedback.json`, 22 items)

Codex GitHub review on 1843dd1, six inline comments, none resolved:

- P1 fail-closed on unreadable ref (script:66, outdated) → `fixed:99c1174`.
- P1 the global rule mandates `python3 scripts/ua-symbol-coverage.py`, which
  exists only in dotfiles while the rule is installed for every repository.
  Confirmed (rule bullet 6 at 1843dd1; helper lives in `scripts/`). → r3.
- P2 ×2 `--repo-ref <base>` is the wrong revision: `def_lines(REF)` explains a
  decrease only when `new >= min(old, defs)`, so reading the pre-change
  source makes every legitimate deletion a REGRESSION. The ref must be the
  revision the new graph was built from (`.ua/meta.json gitCommitHash`,
  normally HEAD); the T41 incident is still caught because unchanged source
  keeps `defs == old`. Confirmed. → r3.
- P2 `def_pattern` recognises Python only by `.py` or `python` in line 1, so
  `#!/usr/bin/env -S uv run --script` executables (permgate, 16 nodes) always
  report REGRESSION. Confirmed (script:48-51). → r3.
- P2 add the policies to the repo `AGENTS.md` → not-applicable: the policy is
  a global user rule with its Codex mirror in `home/dot_config/codex/AGENTS.md`;
  the repo `AGENTS.md` is dotfiles-scoped.
- 10 runner notices, 1 Homebrew tap-trust warning (macOS runner, no install
  path in this diff), CodeRabbit skip comment/status, 2 Codex container
  comments → not-applicable (reasons in the JSON).

**Decision (round 2): REVISE r3** — queued in worker-c behind T47 (one task
per worktree). Amendment appended to the task file; the ACCEPTANCE message
goes out when the T47 RESULT arrives. The sweep re-runs on the r3 head.
