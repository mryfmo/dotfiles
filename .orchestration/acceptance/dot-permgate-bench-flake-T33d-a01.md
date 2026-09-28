# AGMSG-ACCEPTANCE dot-permgate-bench-flake-T33d-a01

RESULT 2026-09-28T10:33:36Z from claude-standard-dot-a005 (worker-c): status=ready_for_review, PR #200 head e161082e393c8fb8622133140da3fda1c9e6b309, branch test/permgate-bench-flake from origin/main 7d47e46. CI green after one rerun (macOS public-bootstrap hit a Homebrew 503 — external).

## Adversarial review (orchestrator, from origin refs and the orchestrator-review worktree)

- Scope: `tests/unit/test_permgate.py` only (+14/−7); product code untouched, as the task required absent a proven product defect.
- Diagnosis quality: the task's hypothesis (interpreter startup under CPU load) was REFUTED with evidence — claude's fake classified in ~17 ms under full load while codex's fake timed out at ~202 ms (= the 0.2 s fixture timeout) in 5/5 calls. Proven mechanism: `executable_permgate` `classify()` passes the codex prompt as the last argv element and leaves stdin inherited; the fake codex did `sys.stdin.read()`, which blocks while the test runner's stdin is an open pipe or socket. Deterministic reproduction without load: `sleep 20 | python3 -m unittest tests.unit.test_permgate -k bench` → `0 != 5`; `< /dev/null` → 5/5 even under load.
- Fix: fake codex reads the prompt from `args[-1]` (the real contract); bench policy timeout raised to the validator's maximum (8 s) since the test asserts every classification succeeds; assertion messages now carry the per-agent benchmark JSON.
- Orchestrator re-derivation: (see the verification block appended below).
- Product hardening candidate raised by the worker and ACCEPTED as a follow-up (not proven a defect; `codex` invocation was forbidden in-task): add `stdin=subprocess.DEVNULL` to the codex `subprocess.run` in `classify()` (and bench) so the classifier never depends on the caller's stdin. → queue after T33f as a product-scoped task with fake-CLI tests.
- CompactionDB: ee4256a6-39e0-4788-af4c-2b5a31055d02 present; its wording states the proven mechanism, not the task's refuted hypothesis, as instructed.

### Orchestrator verification (orchestrator-review worktree, detached)

- `sleep 20 | python3 -m unittest tests.unit.test_permgate -k bench` at origin/main 7d47e46 → `FAILED (failures=1)` (deterministic, no load).
- Same command at e161082 → `OK`; full `tests.unit.test_permgate` module at e161082 → `OK (skipped=1)`.
- The failure is therefore reproducible and fixed; the four earlier "flaky" observations were runner-stdin dependent, not load dependent.

## Pre-merge Codex audit (head e161082, VISIBLE LANE via codex exec) — first pre-merge audit with a machine-checked verdict

`Audit verdict: correct`, exit 0; last message: "No findings … an independent in-memory check reproduced the parent's unwanted read and verified the fix … production code is unchanged … Verdict: correct." Evidence `.orchestration/validation/dot-permgate-bench-flake-T33d-a01-audit.md` (+ `.last.md`). No findings to disposition.

## Review guard

`make require-crit-review` satisfied via AGENT_REVIEWED=1 with REVIEW_EVIDENCE=.orchestration/validation/dot-permgate-bench-flake-T33d-a01-receipt.md (resolved review-scope approval record r_f20b0b, crit session 16eb550d49a7, exported JSON at .orchestration/validation/dot-permgate-bench-flake-T33d-a01-crit.json).

**Decision: ACCEPTED.** Merge #200 --squash (no --delete-branch while worker-c holds the branch); no host deploy (test-only change); then dispatch T33f.

[memory:decision] T33d accepted 2026-09-28: the permgate bench test flake was a fixture defect — the fake codex read inherited stdin while permgate passes the codex prompt in argv — fixed in the fixture (argv prompt, validator-max timeout, JSON in assertion messages); product untouched; hardening follow-up: `stdin=subprocess.DEVNULL` for the codex classify/bench subprocess. PR #200 squash-merged.

cost: n/a (worker report gives no token figures)
