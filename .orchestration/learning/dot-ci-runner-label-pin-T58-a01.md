# Learning triage: dot-ci-runner-label-pin-T58-a01

Candidates only; nothing is promoted.

1. **A canary needs label-agnostic branches.**
   - Lesson: a canary matrix cell is useless if the scripts compare `${OS}` to exact labels and treat everything else as "not supported". Before adding a canary, grep the OS comparisons and match the family (`ubuntu-*`) where the behaviour is shared.
2. **Grounding greps miss tests that assert workflow text.**
   - Lesson: the task's grounding grep did not include `tests/unit/test_supply_chain_policy.py`, which asserts a label token in `test.yaml`.
   - Candidate: the orchestrator's grounding for workflow-text changes also greps `tests/` for `assertIn(` on workflow strings, or simply greps every path.
3. **First Ubuntu 26.04 data point.** `ccstatusline --version` hangs (over 5 s) without network on Ubuntu 26.04. It is a candidate follow-up task before the explicit label moves to 26.04.
