title: feat(orchestrator): the regime CI job checks a PR's task copy with the base's verifier (T133 regime-ci a02, plan 024 P1-11)

## Summary

This PR adds the regime CI job (plan 024 P1-11, programs item (6); the a02 redesign of task `dotfiles-T133-regime-ci-a01`). It checks on GitHub what the verdict otherwise checks at acceptance. It starts as an optional check. Adding `regime` to the ruleset's required contexts is the operator's step.

The trust boundary is that the pull request supplies data only. The workflow, the verifier, the task-consistency checker and the policy all come from the base.

- `.github/workflows/regime.yml` runs one job, `regime`, on `pull_request_target` (opened, synchronize, reopened, ready_for_review). Superseded runs of a PR are cancelled.
  - `pull_request_target` runs the workflow as it is on the base.
  - `actions/checkout` checks out the base sha (`github.event.pull_request.base.sha`) with full history and no persisted credentials.
  - The PR's head is fetched as `refs/pull/<n>/head` into `refs/regime/pr-head`, and its sha must equal the event's head sha. It is never checked out or executed.
  - `contents: read`, no uv cache, and every expression reaches the shell through `env`.
  - `actions/checkout` and `astral-sh/setup-uv` are pinned to the shas the other workflows use.
- `scripts/orchestrator/regime-ci.py --base <sha> --head <sha>` runs from the base checkout as `uv run --no-config --no-project --with pyyaml python -I`. It reads the head only through `git show` and never imports or executes head content.
  - It takes each task whose `.orchestration/<t>/` the diff touches and that has a `task.md` copy at the head. Of a `reset_of` lineage it takes only the latest copy, and only when both copies authenticate against the base's dispatched text.
  - For each such task it prints one `regime-ci: <t>: <rule>: <detail>` line per violation and `regime-ci: warning: …` lines.
  - `checker`: the base's task-consistency checker runs on the base's dispatched text (`.orchestration/tasks/<t>.md` at the base), never on a pull request's own text.
  - `task-copy`: the copy must equal the base's dispatched text, which is the policy (allowed_files, caps, reset_of). Without dispatched text at the base, the copy is unverifiable. That is a warning until `REGIME_REQUIRE_DISPATCHED=1` makes it a violation.
  - `precheck`: precheck.json's head must be the head, or an ancestor whose code the head leaves unchanged outside `.orchestration/<t>/`. Its sha256 must equal result.txt's `precheck=`. Without precheck.json it is a warning.
  - `allowed-files`: every changed path must match an allowed_files entry.
  - `caps`: the changed lines are checked against the copy's `## Check` sentence.
  - A diff without a task copy passes as `no target (records-only)` only when every changed path is under `.orchestration/`. No branch name grants anything.
  - A diff that changes the verifier, the checker or the workflow gets a warning, because this run executed the base's version and the audit reads the change.
  - Exit codes: 1 on any violation, 2 when git cannot list the diff, else 0 after `regime-ci: ok <n> task(s)`.
- `tests/unit/test_regime_ci.py` uses temporary repositories whose head content is never executed. Its tests cover:
  - the base verifier reading the head as data;
  - a pull request's text never reaching the checker;
  - lineage authentication and supersession;
  - content-based records-only exemption;
  - the unverifiable-copy warning and its flag;
  - the workflow's base-only shape;
  - one violation line per rule in a consistent-PR table;
  - the checker run without the checkout's uv config;
  - refusal of a checkout not at the base;
  - the task-id mismatch;
  - the records-only pass;
  - the two warnings.
- `tests/unit/test_workflow_security.py` gains one `EXPECTED_PERMISSIONS` entry: `"regime.yml": {"contents": "read"}`.

## Evidence

The task copy, report, validation output and sandbox record are under:

- `.orchestration/dotfiles-T133-regime-ci-a02/` (the a02 redesign that merged);
- `.orchestration/dotfiles-T133-regime-ci-a01/` (the stopped a01 design, kept as history).

🤖 Generated with [Claude Code](https://claude.com/claude-code)
