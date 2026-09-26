# Validation: dot-macos-crit-pinned-install-T17-a01

## Local checks

- `uv run --with pyyaml scripts/generate-agent-configs.py --check` → `generated agent
configs are up to date` (idempotent render of the darwin sha256 pins).
- `uv run --with pyyaml scripts/validate-agent-assets.py` → `agent asset validation ok`.
  (First run failed: `ERROR: scripts/update-agent-assets.sh must manage Crit asset token
'brew install crit'` — a hard-coded token check in `validate_crit_install_assets()` not
  surfaced by prior research; fixed by asserting the new `crit-darwin-amd64`/
  `crit-darwin-arm64` tokens instead, commit `fab3c86`.)
- `shellcheck -x scripts/update-agent-assets.sh scripts/upgrade-tools.sh
scripts/lib/installer-pins.sh` → clean, exit 0.
- `uv run python -m unittest discover -s tests/unit -v` → **434 tests, OK (skipped=1)**,
  including both new Darwin-branch tests
  (`test_darwin_crit_install_is_pinned_atomic_and_recorded`,
  `test_darwin_crit_checksum_failure_preserves_existing_binary`, now in
  `tests/unit/test_runtime_health.py`'s `crit_fixture`, alongside the five existing
  Linux crit tests — all still passing) and the pre-existing
  `test_updater_has_one_recording_call_for_each_install_step` (still exactly one
  `manifest_record "ensure_crit_cli"` call site) and `test_missing_crit_asset_is_repairable`.
- `grep -rn "brew install crit"` repo-wide: only remaining hits are historical task/
  acceptance docs describing the pre-fix defect, and the new negative bats assertion
  `run ! grep -q 'brew install crit' scripts/update-agent-assets.sh`.
- Bats: **not run locally** (forbidden by task spec) — validated via CI below instead.

## Revision round 1 — additional local checks (commit `ed2279d`)

- `check_crit_cli` manually exercised in both states (crit present/absent under a fake
  `$HOME`): confirmed `found:   crit -> <path> (pinned release)` plus real `--version`
  output, and `not applicable: Crit CLI (not installed)` with exit 0, respectively.
- `uv run python -m unittest tests.unit.test_runtime_health -v -k crit` → 9/9 pass,
  including the two new Darwin tests and
  `test_upgrade_bumps_terminal_and_crit_pins_from_fetched_artifacts` (now asserting the
  darwin sha256 fields too).
- `uv run python -m unittest tests.unit.test_workflow_security` → 8/8 pass (test.yaml
  comment rewrite didn't affect permissions/checkout/SHA-pinning checks).
- `python3 -c "import yaml; yaml.safe_load(...)"` on `.github/workflows/test.yaml` →
  valid.
- Full suite re-run: `uv run python -m unittest discover -s tests/unit -v` → 434 tests,
  OK (skipped=1) — unchanged count (2 tests relocated, not net-added).
- `git diff origin/main..HEAD -- scripts/validate-agent-assets.py
tests/unit/test_runtime_health.py` → confirmed minimal, no formatter-reformatted
  hunks beyond the intended changes.

## CI — https://github.com/mryfmo/dotfiles/pull/183 (head `fab3c86`, then `ed2279d`)

All checks passed:

```
CodeRabbit                              pass (manual review required for OSS repo)
build / build (client) / build (server) pass
changes                                 pass
validate                                pass
private-bootstrap (macos-14, client)    pass
private-bootstrap (ubuntu-latest, *)    pass
public-bootstrap (macos-14, client)     pass  7m38s
public-bootstrap (ubuntu-latest, *)     pass
test (macos-14, client)                 pass  2m12s
test (ubuntu-latest, *)                 pass
nix                                     skipping (as on main)
```

Run: https://github.com/mryfmo/dotfiles/actions/runs/36200567629

### Annotation counts (verbatim requirement: failure-level = 0)

`public-bootstrap (macos-14, client)` (check-run 108286107597):

```
$ gh api repos/mryfmo/dotfiles/check-runs/108286107597/annotations --jq '[.[] | select(.annotation_level=="failure")] | length'
0
$ gh api repos/mryfmo/dotfiles/check-runs/108286107597/annotations --jq '.[] | .annotation_level'
warning
```

The one remaining annotation is a `warning`-level "taps are not trusted: aws/tap
azure/bicep hashicorp/tap" notice. This is **not** the `crit: no bottle available!`
failure the task evidence named — that annotation is gone entirely, confirming the fix.
The warning is a generic Homebrew notice unrelated to crit (this job's workflow,
`remote.yaml`, never calls `brew trust` at all — it only runs `setup.sh` → `chezmoi
apply` → `update-agent-assets.sh`, which no longer calls `brew` for crit either); out of
this task's scope (`remote.yaml`/`setup.sh` are not in `allowed_files`) and not
failure-level, so it does not block this task's validation criterion.

`test (macos-14, client)` (check-run 108286134031) — the job whose `brew trust
aws/tap azure/bicep || true` this task's required change #4 targeted:

```
$ gh api repos/mryfmo/dotfiles/check-runs/108286134031/annotations --jq 'length'
0
```

Zero annotations of any level — the untrusted-tap warning this job previously carried
is gone, and the step now fails hard on any future trust failure (no `|| true`).

### Revision round 1 CI — head `ed2279d`

All checks passed again (run: https://github.com/mryfmo/dotfiles/actions/runs/36203420950
and https://github.com/mryfmo/dotfiles/actions/runs/36203420954), including
`public-bootstrap (macos-14, client)` (6m16s) and `test (macos-14, client)` (1m45s).
Re-confirmed failure-level annotation counts on the new head commit:

```
$ gh api repos/mryfmo/dotfiles/commits/ed2279d/check-runs --jq '.check_runs[] | select(.name=="public-bootstrap (macos-14, client)" or .name=="test (macos-14, client)") | "\(.id)\t\(.name)"'
108294723614	public-bootstrap (macos-14, client)
108294752216	test (macos-14, client)
$ gh api repos/mryfmo/dotfiles/check-runs/108294723614/annotations --jq '[.[] | select(.annotation_level=="failure")] | length'
0
$ gh api repos/mryfmo/dotfiles/check-runs/108294752216/annotations --jq 'length'
0
```

Note: at push time, `origin/main` had advanced one commit ahead (`d97c16d`,
orchestration-only: T23 task spec + G8 addendum) since this branch was created from
`a6df24c`. Confirmed no file overlap with this PR's changes (`git log --oneline
HEAD..origin/main`); no rebase performed, none needed.

### Revision round 3 — head `239b52b`

Local reproduction before the fix (fake `crit` exiting 1):

```
$ HOME=<scratch> bash -c 'source scripts/check-tools.sh; check_crit_cli'
found:   crit -> <scratch>/.local/bin/crit (pinned release)
optional warning: crit --version failed; the managed binary may be corrupt (try REPAIR=1 make doctor)
exit: 0
```

(Before the fix this would have exited nonzero and aborted the rest of `main()`.)

`uv run --with pyyaml scripts/validate-agent-assets.py` → ok. `uv run python -m
unittest discover -s tests/unit -v` → 434 tests, OK (skipped=1), unchanged count (one
bats case added, not counted here). `shellcheck -x scripts/check-tools.sh` → clean.

Replied on CodeRabbit thread `4109698652` (https://github.com/mryfmo/dotfiles/pull/183#discussion_r4109894885)
citing commit `239b52b`.

### Revision round 3 CI — head `239b52b`

All checks passed, including `public-bootstrap (macos-14, client)` (8m41s),
`public-bootstrap (ubuntu-latest, client)` (8m33s), `public-bootstrap (ubuntu-latest,
server)` (7m2s), and both macOS/ubuntu `test` jobs. Re-confirmed zero failure-level
annotations on the new head:

```
$ gh api repos/mryfmo/dotfiles/commits/239b52b/check-runs --jq '.check_runs[] | select(.name=="public-bootstrap (macos-14, client)" or .name=="test (macos-14, client)") | "\(.id)\t\(.name)"'
108320423566	test (macos-14, client)
108320400877	public-bootstrap (macos-14, client)
$ gh api repos/mryfmo/dotfiles/check-runs/108320400877/annotations --jq '[.[] | select(.annotation_level=="failure")] | length'
0
$ gh api repos/mryfmo/dotfiles/check-runs/108320423566/annotations --jq 'length'
0
```

Run: https://github.com/mryfmo/dotfiles/actions/runs/36212031247

## Not validated (blocker, operator-acknowledged)

`pr-feedback.py <n>` disposition output — script only exists on unmerged PR #182
(`feat/pr-feedback-gate`), not on `main` or this worktree. Skipped per operator decision;
see report for detail.
