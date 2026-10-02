# Report: dot-ci-runner-label-pin-T58-a01

- **Worker and branch:** `claude-standard-dot-a005` in worker-c. Branch `chore/ci-runner-label-pin` from `origin/main` 3c4c2cec, with one commit, `88f797360b3d7b590e5e5d1e56f9c0b1b842d88e`.
- **PR:** #229, https://github.com/mryfmo/dotfiles/pull/229.
- **task_rev:** the first dispatch was `d03d9941…`, with PONG blocked before any edit. It was resolved by the orchestrator's decision section, now `e2776a15…`. Both matched.
- **Status:** ready_for_review.
  - **Required checks:** every required context is green, including the renamed `test (ubuntu-24.04, client|server)` and `public-bootstrap (ubuntu-24.04, client|server)`.
  - **Canary:** `test (ubuntu-26.04, client)` is red and `continue-on-error`. The `Unit test` workflow run concludes `success`.
  - **Merge state:** `mergeStateStatus` is `UNSTABLE`, meaning a non-required check failed; the PR is still mergeable.

## Change (9 files, +30/−23)

1. **Explicit labels.** Every `ubuntu-latest` became `ubuntu-24.04`:
   - `runs-on:` in `test.yaml` (`changes`), `agent-assets.yml`, `docs.yml` and `ubuntu.yaml`;
   - matrix `os:` in `test.yaml` (`test`, `nix`) and `remote.yaml` (`public-bootstrap`, `private-bootstrap`, two entries each).

   `macos-14` is unchanged.
2. **Canary.** The `test` matrix gets `include: - os: ubuntu-26.04, system: client` and a job-level `continue-on-error: ${{ matrix.os == 'ubuntu-26.04' }}`. I keyed this on `matrix.os` rather than an extra matrix key, so the default check names stay `test (<os>, <system>)`.
3. **Shell OS checks (decision 2).** These now use `[[ "${OS}" == ubuntu-* ]]`, so the canary takes the Ubuntu branch instead of "not supported": `test.yaml` Install tools, the statusline smoke and the Python unit tests, plus `scripts/run_unit_test.sh` (`run_os_specific_test`, `run_files_test`). The Codecov setup and upload steps keep `matrix.os == 'ubuntu-24.04'`, so the canary never uploads coverage.
4. **Renamed contexts.**
   - The README ruleset payload now lists `test (ubuntu-24.04, server|client)` and `public-bootstrap (ubuntu-24.04, server|client)`.
   - The `test_pr_feedback.py` fixture name is `test (ubuntu-24.04, server)`.
   - `test_supply_chain_policy.py` now asserts `ubuntu-24.04` (decision 1; only that assertion changed).
   - `test_pr_feedback.py:130` keeps GitHub's annotation text "The ubuntu-latest label will migrate…" (decision 3). It is the only line the post-edit grep returns.

## Canary finding (for adopting Ubuntu 26.04 later; not fixed here)

- **Where it ran:** image `ubuntu-26.04`, release `ubuntu26/20260927.149`.
- **What passed:** checkout, the Ubuntu branch of `Install tools` (apt `bats curl iproute2 parallel ruby shellcheck`, pinned chezmoi), statusline config and mise setup.
- **What failed:** `Smoke-test statusline tools without network`. `scripts/check-statusline-tools.py` timed out (5 s) on `ccstatusline --version` under `sudo unshare --net` on the 26.04 image, which ships Python 3.14. Steps after it did not run.
- **Next step:** to adopt Ubuntu 26.04, a follow-up task investigates why `ccstatusline` (npm 2.2.30 via mise) hangs without network on 26.04, then changes the explicit label.

## Operator / orchestrator actions after merge

- **Re-apply the README ruleset payload.** If a live ruleset or branch protection keys on the old `(ubuntu-latest, …)` contexts, the operator must re-apply the README payload. Otherwise required checks would wait on contexts that no longer report.
- **Sweep disposition.** The PR-feedback sweep will list the canary's `failure` check run. It needs a `not-applicable` disposition with a concrete reason, for example: "non-required continue-on-error Ubuntu 26.04 canary; tracked finding: ccstatusline --version timeout without network".

## Notes

- **`make unit-test`:** 718 tests, OK (2 skipped).
- **Other checks:** `make validate-agent-assets` exits 0; shellcheck and the pinned shfmt are clean on `run_unit_test.sh`.
- **actionlint:** not installed locally. CI's `validate` job passed.
- **Round 1 (PONG blocked):** I raised three questions before editing (the uncovered `test_supply_chain_policy.py` assertion, exact-label checks blocking the canary, and the annotation fixture). The orchestrator answered all three as proposed.

## CompactionDB

```
cd /home/moriya/Workspace/dotfiles && python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content 'T58 (operator 2026-10-02): CI runner labels are explicit (`ubuntu-24.04`, `macos-14`), never `*-latest`; a new OS image is adopted through a non-required canary cell first, then by changing the explicit label.'
e6bdb8d4-9297-4616-998d-b7a108578112
```

[memory:decision] T58 (operator 2026-10-02): CI runner labels are explicit (`ubuntu-24.04`, `macos-14`), never `*-latest`; a new OS image is adopted through a non-required canary cell first, then by changing the explicit label.

## Artifacts

- validation: `.orchestration/validation/dot-ci-runner-label-pin-T58-a01.md`
- sandbox: `.orchestration/sandboxes/dot-ci-runner-label-pin-T58-a01.md`
- learning: `.orchestration/learning/dot-ci-runner-label-pin-T58-a01.md`
- autoskill: `.orchestration/autoskill/runs/dot-ci-runner-label-pin-T58-a01.md`

cost: n/a (no subagents; the runtime does not expose session totals)
