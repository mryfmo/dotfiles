# U359: the CI unit-test step's bound follows the measured step

GOAL
Every pull request's macOS leg went red on 2026-11-07 without a failing test: the `Run Python unit tests` step of `.github/workflows/test.yaml` timed out at its 24-minute bound on main 238f898e (run 42356218234) and on PRs 721 and 722 (runs 42357321733, 42357655680) while every test that ran passed. The bound dates from a step of at most 664 s; on main the macos-15 client step now takes 19.0 min (49f3c33c, run 42347799380) and 18.1 min (6ad1be23, run 42356259565), because one module, `tests/unit/test_hcom_seat_dsh.py`, runs about 270 lever launches and the shards split by module. The bound follows the measurement as BoundOrderTest's formula requires: the step's rest is the measured step doubled, 2280 s, and `timeout-minutes` is the formula's 39. Shortening the module is a later unit.

SCOPE
Branch `fix/ci-macos-unit-test-step-timeout` from main 6ad1be23; the coordinator's own commit 0605b7a5. Files: `.github/workflows/test.yaml` (the step's comment and `timeout-minutes`), `tests/unit/test_apt_mirror.py` (`REST_ONLY_BUDGET["Run Python unit tests"]` and the docstring's measurement sentence). Not: the job's 45 minutes; the shard layout; any test module.

CONTEXT
`tests/unit/test_apt_mirror.py` `step_minutes` (the ceiling of the apt bounds plus the measured rest, plus one minute) and `BoundOrderTest`; the job's `timeout-minutes: 45` (the macOS job took 21 to 27 min with the step at 18 to 24).

DATA SHAPE
One constant and one bound, equal through the formula.

CHANGE
1. The constant and the bound. 2. `uv run --with pyyaml python -m unittest tests.unit.test_apt_mirror tests.unit.test_ci_workflows` OK. 3. ruff format and lint-comparisons 0.

ACCEPTANCE
1. 91 tests OK (measured). 2. ruff format 0; lint-comparisons 0 (measured). 3. The pull request's own macOS leg passes under the new bound (CI).

VERIFY
The body's Verification section; the pull request's CI.

CLOSURE
remove

TRUST
TRUST: the unit trusts BoundOrderTest's formula as the rule for a step bound and the two main runs as the measurement.

TIMEBOX
15 minutes.

FORBIDDEN
No change to any test module's content; no change to the job bound.

WORKER RULES
The coordinator's own commit; no worker.

REPORT
The pull request body.

STANDING
`preferences.md` (standing orders 21, 49); `tests/unit/test_apt_mirror.py` BoundOrderTest.
