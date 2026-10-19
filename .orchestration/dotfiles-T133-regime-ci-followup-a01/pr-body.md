title: feat(orchestrator): the regime CI job checks a PR's task copy with the base's verifier (T133 regime-ci a02, plan 024 P1-11)

## Summary

This PR adds the regime CI job (plan 024 P1-11, programs item (6); the a02 redesign of task `dotfiles-T133-regime-ci-a01`). It checks on GitHub what the verdict otherwise checks at acceptance. It starts as an optional check. Adding `regime` to the ruleset's required contexts is the operator's step.

The trust boundary is that the pull request's content is data. The workflow, the verifier and the task-consistency checker run from the base, and the PR's head is never checked out or executed. The policy (allowed_files, caps, reset_of) is the base's dispatched `.orchestration/tasks/<t>.md` when the base has one. When the base has none, the copy is unverifiable and the PR's own copy is the provisional policy: the run warns and exits 0, until `REGIME_REQUIRE_DISPATCHED=1` (not set in the workflow) makes it a violation.

- `.github/workflows/regime.yml` runs one job, `regime`, on `pull_request_target` (opened, synchronize, reopened, ready_for_review). Superseded runs of a PR are cancelled.
  - `pull_request_target` runs the workflow as it is on the base.
  - `actions/checkout` checks out the event's base sha (`github.event.pull_request.base.sha`) with full history and no persisted credentials.
  - The PR's head is fetched as `refs/pull/<n>/head` into `refs/regime/pr-head`, and its sha must equal the event's head sha.
  - `contents: read`, no uv cache, and every expression reaches the shell through `env`.
  - `actions/checkout` and `astral-sh/setup-uv` are pinned to the shas the other workflows use.
- `scripts/orchestrator/regime-ci.py --base <sha> --head <sha>` runs from the base checkout as `uv run --no-config --no-project --with pyyaml python -I`. It reads head content only through git (`git show`, `git diff` and `merge-base` against the head), and never checks out, imports or executes it. A checkout that is not at `--base` exits 1 before any check.
  - It takes each task whose `.orchestration/<t>/` the diff `<base>...<head>` touches and that has a `task.md` copy at the head.
  - A `reset_of` lineage counts as one target, the latest copy, only when both copies equal their base dispatched texts. The superseded predecessor then gets a predecessor-copy warning. Otherwise each copy is checked as its own task.
  - For each task it prints one `regime-ci: <t>: <rule>: <detail>` line per violation and `regime-ci: warning: …` lines.
  - `checker`: the base's task-consistency checker runs on the base's dispatched text, never on a pull request's own text. With no dispatched text it is skipped, with a warning.
  - `task-copy`: the copy must equal the base's dispatched text. Without dispatched text, a result.txt `task_copy=` token, if present, must equal the copy's sha256.
  - `precheck`: precheck.json's head must be the head, or an ancestor whose code the head leaves unchanged outside `.orchestration/<t>/`. Its sha256 must equal result.txt's `precheck=`. Without precheck.json it is a warning.
  - `allowed-files`: every changed path must match an allowed_files entry of the policy. A reset_of predecessor's directory is exempt.
  - `caps`: the changed lines are checked against the policy text's `## Check` sentence. A missing cap is a warning.
  - A diff without a task copy passes as `no target (records-only)` only when every changed path is under `.orchestration/`. No branch name grants anything.
  - A diff that changes the verifier, the checker or the workflow gets a warning, because this run executed the base's version and the audit reads the change.
  - Exit codes:
    - 0 after `regime-ci: ok <n> task(s)` or a records-only pass;
    - 1 on any violation, a code change without a task copy, or a checkout not at the base;
    - 2 when git cannot resolve `--base` or `--head` or list the diff, or when PyYAML is missing.
- `tests/unit/test_regime_ci.py` uses temporary repositories whose head content is never executed. Its tests cover:
  - the base verifier reading the head as data;
  - a pull request's text never reaching the checker;
  - lineage authentication and supersession;
  - content-based records-only exemption;
  - the unverifiable-copy warning and its flag;
  - the workflow's base-only shape;
  - one violation line per rule in a consistent-PR table;
  - the checker run without the checkout's uv config;
  - the result.txt `task_copy=` check without dispatched text;
  - refusal of a checkout not at the base, and of a diff git cannot list;
  - the task-id mismatch;
  - only the latest copy of a reset_of lineage being checked;
  - the records-only pass;
  - the warning lines (unverifiable copy, checker skipped, precheck absent, missing caps, a changed checker).
- `tests/unit/test_workflow_security.py` gains one `EXPECTED_PERMISSIONS` entry: `"regime.yml": {"contents": "read"}`.

## Evidence

- `.orchestration/dotfiles-T133-regime-ci-a02/`: the a02 task copy, report, validation output and sandbox record (the redesign that merged).
- `.orchestration/dotfiles-T133-regime-ci-a01/`: the stopped a01 design's report, validation and sandbox records, kept as history. Its task copy was removed by the a02 reset.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
