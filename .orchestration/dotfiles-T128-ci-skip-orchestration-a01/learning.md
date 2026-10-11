# Learning triage: dotfiles-T128-ci-skip-orchestration-a01

These are candidates only; nothing is promoted.

1. [memory:failure] A "decide" job that required jobs `need` is fail-open: a job that needs a failed or skipped job is skipped, and GitHub reports a skipped job as Success even for a required check. A required job decides in its own step and gates its heavy steps; it never carries a job-level `if` or a `needs`. Check a task premise that names a CI mechanism against the actions docs before implementing it (here the PONG before Amendment 1).
2. [memory:decision] Workflow decision logic is testable without PyYAML or a runner: extract the step's `run:` block from the workflow file, run it with bash against a scratch bare origin and clone, and read `GITHUB_OUTPUT` from a temp file. The test then breaks when the workflow's script changes, not a copy of it.
3. [memory:failure] The full `make unit-test` suite fails in the Claude seat's sandbox on `main` as well (188 failing ids, identical at `origin/main` and this head): test commits that inherit the global signing setting, `mktemp` outside the writable paths, no pty devices, no local `main` ref. A worker compares the failing test ids with an `origin/main` run before reading a failure as its own, and leaves the suite's verdict to CI.
