---
id: M-20261020-04
date: 2026-10-20
classes: [environment-contract, evidence-integrity]
severity: P2
---

# A text mandated a checker-side environment input with no caller edit, and the RESULT's own counts showed the breakage

**What happened.** The a06-checker text (b9e04cb9, PR #440) says at line 117 "retain … the absolute-cache requirement" and at line 47 "No caller or workflow edit is authorized". a012 implemented the requirement as an import-time refusal in `scripts/orchestrator/task-consistency-check.py:37-39` (`refused: UV_CACHE_DIR must be set to an absolute path`). Every caller on main that sets no `UV_CACHE_DIR` (regime-ci.py's checker launch, the regime workflow, the pre-send glue) gets no verdict: six `tests/unit/test_regime_ci.py` failures on all three Linux CI jobs of head b8bf8066 (run 39402138504, `FAILED (failures=7)`). a012's own `validation.md:36` reported base 150 vs candidate 156 failures and called every failure inherited; the RESULT was sent at 09:42:16Z, before the run ended at 09:45Z.

**What the rules say.** C-80: the text review judges the text against the trusted-execution contract and the callers it binds; the a06 Check clause: compare inherited failures against the unchanged base and preserve their exact multiplicities; the transport PING: RESULT after CI as read by the orchestrator (D-024-36).

**Why the rules did not fire.** The C-80 round 2 verdict `correct` read line 117 as a contract restatement, not as an obligation on callers the text forbids editing; no mechanism compared the RESULT's own base/candidate counts, and the orchestrator read the RESULT before reading the head's CI. The Codex seat cannot read CI (no network), so its "inherited" claim rested on its sandbox base with 150 failures.

**Mechanism.** (1) `pre-send.sh` fails a text that holds both a mandatory-environment sentence (`UV_CACHE_DIR`, `TRUSTED_*` with `must be set`, `requirement`, `mandatory`) and a no-caller-edit sentence, naming both lines; the author rewrites to a checker-side default or names the on-main caller tests (C-112). (2) `.agents/worklog/orchestrator-glue/result-evidence-check.sh <task> <head40> [<pr>]` runs on every RESULT before judgement and refuses extra candidate failures without names and a head whose CI is not concluded green (C-113). Run on b8bf8066 it refuses (`extra=6`, `0 test names`).

**Disposition of the round.** ACCEPTANCE `status=revise round=1` (2827) with R1 (import-time refusal → private temporary cache default), R2 (`test_canonical_path_pipeline_rejects_normalised_collisions` fails on Linux: C12 key computed after an APFS-only normalisation-insensitive `exists()` probe) and R3 (named candidate-minus-base set); round 2 is the last worker round.
