## Summary

The regime CI job (plan 024 P1-11, programs item (6); task `dotfiles-T133-regime-ci-a01`). It checks on GitHub what the verdict otherwise checks at acceptance. It starts as an optional check: adding `regime` to the ruleset's required contexts is the operator's step.

- `.github/workflows/regime.yml` runs one job, `regime`, on `pull_request` (opened, synchronize, reopened, ready_for_review), with superseded runs of a PR cancelled.
  - `actions/checkout` and `astral-sh/setup-uv` are pinned by the shas the other workflows use.
  - It checks out the PR's head commit with every branch. `github.sha` is the merge commit on `pull_request` events, which is the design correction to the plan.
  - Read-only `contents`, no persisted credentials, no uv cache, `uv run --no-config`, and the expressions reach the shell through `env`.
- `scripts/orchestrator/regime-ci.py --base <ref> --head <sha>` takes the tasks whose `.orchestration/<t>/` the diff touches and that carry a `task.md` copy. It prints one line per violation (`regime-ci: <t>: <rule>: <detail>`) and its warnings, and passes a rule only on a positive check of parsed, validated input:
  - `checker`: the tracked task-consistency checker on the copy, run as a subprocess.
    - It counts only with its own verdict line and the matching exit code; a crash is a violation.
    - Its C1 file-name line is replaced by `task-id`, because every copy is named `task.md`.
  - `task-copy`: the copy equals the dispatched text, or else result.txt's `task_copy=`. Without either it is a warning.
  - `precheck`: precheck.json's head is a 40-hex id equal to the head, or an ancestor whose difference to the head lies only under `.orchestration/<t>/` (a committed precheck.json cannot name the commit that adds it). Its sha256 equals result.txt's `precheck=`. Without precheck.json it is a warning.
  - `allowed-files`: every changed path matches an entry.
  - `caps`: the changed lines against the copy's `## Check` sentence, with the "(added plus deleted)" wording parsed too. A missing cap is a warning.
  - Every git listing must succeed, or the job exits 2.
  - A records-only diff passes as `no target (records-only)`. A code change without a task copy is a violation.
  - A diff that changes the checker, regime-ci.py or regime.yml prints a warning.
- PR content is read as data only (`git show`, `yaml.safe_load`, `json`).
- `tests/unit/test_regime_ci.py`:
  - A consistent PR passes.
  - One subtest per rule branch gives exactly one violation line with its phrase.
  - The result.txt copy check, the checkout and git refusals, the records-only and `orchestration/` cases, and the warnings.
  - The workflow's pins, PR head, `--no-config`, concurrency and permissions.

## Evidence

`.orchestration/dotfiles-T133-regime-ci-a01/` holds:

- the task copy;
- the report (the design corrections, the re-plan, the two warning forms and when each becomes a failure, the operator's promotion step);
- the validation output (the red runs, the mutants, the Check's run on this branch);
- the sandbox record;
- the learning triage;
- the worker review record and its receipt.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
