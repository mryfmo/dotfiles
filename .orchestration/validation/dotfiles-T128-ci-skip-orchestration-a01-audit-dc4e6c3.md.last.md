📝 まとめ: Audited [PR #320](https://github.com/mryfmo/dotfiles/pull/320) at `dc4e6c374bf396160fac969ece26b62fb70eee0b`, read-only. Two findings remain.

[P2] high implementation tests/unit/test_workflow_orchestration_skip.py:72 The reader still misses valid block-style YAML keys such as `if : false` and `"\x69f": false`; the step matcher at line 84 likewise misses `continue-on-error : true`. In-memory mutations parsed correctly with Ruby YAML while the corresponding structural tests passed. The original quoted-key cases are fixed, but the parser’s false negatives remain: required jobs can regain skip/error-suppression settings without these tests detecting them. Use a YAML parser or fail closed on unsupported syntax.

[P2] high orchestration .orchestration/acceptance/dotfiles-T128-ci-skip-orchestration-a01.md:35 The design-on-main finding remains applicable: main at `b896d9bc` lacks this task’s `implementing_tasks` entry, and its INV-2 sentence differs from the committed task’s sentence. Publishing the design after the implementation merges does not satisfy the task’s explicit pre-dispatch prerequisite; recording that deferral as `not-applicable` does not resolve the mismatch.

Verified:

- `--no-renames` closes the rename finding; both named revision tests pass in final-head CI.
- Current required jobs have no job-level `if` or `needs`. Decision steps retain fail-closed Git error handling, and heavy steps carry their decision gates.
- Final-head required checks succeeded; the inspected [CI log](https://github.com/mryfmo/dotfiles/actions/runs/38119985302/job/114412529399) records 938 passing Python tests, including classification and workflow-security tests.
- The refreshed sweep targets the correct head, dispositions all 10 items, and includes the resolved thread and reply. The freshness finding is closed.
- Both task premises hold against live GitHub data and [documented skipped-job semantics](https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/control-jobs-with-conditions).

INV-2: violated .orchestration/tasks/dotfiles-T128-ci-skip-orchestration-a01.md:14 — main-design registration and sentence equality fail; size caps hold: 3 files, 130 production additions, 339 test additions.

Orchestration findings: 1

Not rerun locally: full suite or Bats. The post-merge ≤10-minute boundary-PR measurement remains pending; structural-test false negatives remain a risk.
Verdict: incorrect