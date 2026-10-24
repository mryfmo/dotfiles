# U39 audit at fed47ef6 (PR #493): incorrect, findings=2 (P2, P3), fix round U39b

Audit seat audit-kimi, worktree positioned at fed47ef6, TASK receipt id=4898 (2026-10-24T10:44:11Z), VERDICT row 4986 (`incorrect`, findings=2), findings PONG row 5002. The audit verified: all 14 checks pass, the seven required context names are unchanged, the CI logs show 1418 tests with one combined OK summary and 11 plus 22 bun tests passing, the Codex measurement-step removal is present, and the disclosed six-minute target miss is not a finding. Copied by the orchestrator (orchestrator-sari) before the fix TASK per hcom-orchestration step 4.

## F1 (P2, confidence high): the render-only skip is wider than its guard

`.github/workflows/remote.yaml:103` (and the identical `private-bootstrap.yaml` rule): the skip accepts every `home/dot_local/bin` path, but the reader guard at `tests/unit/test_ci_workflows.py:25` checks only the destinations `.local/bin/common` and `.local/bin/server`. A PR adding `home/dot_local/bin/executable_mise` or `executable_omp` is classified render-only although the bootstrap installers execute those root binaries (`install/common/gh_extensions.sh:15-26`, `scripts/update-agent-assets.sh:958`). The fast job excludes the installer scripts and cannot replace that check. Required fix: narrow both rules to the audited `common/` and `server/` subtrees, or classify the root-bin consumers explicitly; align the guard with the rule; add root-bin negative cases.

## F2 (P3, confidence high): the omp install's temp directory is not under RUNNER_TEMP

`.github/workflows/test.yaml:272-273`: setting only `HOME` and `PATH` does not enforce the claimed RUNNER_TEMP-only writes of the omp install for the bun step: `update_omp` (`scripts/update-agent-assets.sh:964`) creates its download directory under `TMPDIR` or `/tmp`, and the step sets neither. Required fix: create and pass a `TMPDIR` under `RUNNER_TEMP` to the installer and verify the containment, or correct the claimed boundary in the threat table.

## Disposition

Both accepted. Fix round U39b on the same branch `ci/critical-path`, SCOPE unchanged (the two workflows, `test_ci_workflows.py`, the threat table in the PR comment); new RESULT with the five-point self-check at push time, then a re-audit at the new head.
