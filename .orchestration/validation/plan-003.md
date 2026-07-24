# Plan 003 validation

## Final GitHub acceptance

- PR #69 exact head `22f9ec0b914e357923a241ec9f02d82e44da9409` had 15 successful visible checks.
- Thread-aware review inspection found zero review threads and no actionable bot finding.
- Independent full-range review verdict: `ACCEPT` in `.orchestration/acceptance/plan-003-final-pr.md`.
- Squash merge: `69e2338489e22d5279ca3fdf6917f0cbe5950400`.
- Post-merge push workflows all passed: Snippet install `29136528669`, Unit test
  `29136528678`, Ubuntu `29136528670`, macOS `29136528666`, Agent assets
  `29136528714`, and Docs `29136528690`.
- The post-merge public bootstrap completed on Ubuntu client/server and macOS
  client. Private restoration remained unobserved because its secrets were not
  configured; all three jobs used the explicit fail-closed skip path.

## Executed successfully

- `bash -n setup.sh install/ubuntu/common/dependencies.sh`
- `shfmt -i 4 -sr -d setup.sh install/ubuntu/common/dependencies.sh`
- `shellcheck -x setup.sh install/ubuntu/common/dependencies.sh`
- `make unit-test`: 86 tests passed.
- `make validate-agent-assets`: `agent asset validation ok`.
- Exact wrapped config renders: Linux client produced `system: "client"`; Linux server produced `system: "server"`; macOS default produced `system: "client"`.
- Invalid render fixtures: persisted invalid, typo, empty, and whitespace all failed with `client or server`, before `sourceDir:` output.
- Fetch fixture: curl-only, wget-only, both, and neither behaved as specified; both preferred curl and neither returned 1 with the deterministic error.
- Direct non-Bats fetch regression: a fake fetch emitted a side-effecting partial installer and returned 23; `run_chezmoi` returned 23 and the side effect did not occur.
- Package fixture: installed packages were omitted; absent curl and partial git produced ordered `update` then `install -y curl git`.
- Direct non-Bats package regression: fake `dpkg-query` exit 2 propagated as exit 2 and did not reach the fake APT function.
- `ruby -e 'require "yaml"; YAML.load_file(".github/workflows/remote.yaml")'`: valid YAML.
- `git diff --check` passed.
- Allowed-file audit against `c3e69ade4d3700b4d624416ce2e5d59b31dce191` found only the eight authorized files.
- Plan 001 merge `3826729` is an ancestor of the base.
- Chezmoi v2.70.5 help confirms official first-column status semantics.
- `make require-crit-review` first required review, as expected.
- Crit review evidence: `.agents/worklog/codex/review/plan-003-crit.json` contains resolved records `r_879a7f` and revision record `r_2d91af`; receipt is `.agents/worklog/codex/review/plan-003-receipt.md`.
- `AGENT_REVIEWED=1 REVIEW_EVIDENCE=.agents/worklog/codex/review/plan-003-receipt.md make require-crit-review` passed.
- Revision source commit: `b6fa6b2ddb652e30897f9134b83fbe4c2f2a8635`; worktree clean and two commits ahead of `origin/main`.

## Static/fixture inspection

- `tests/install/common/setup.bats` contains wget-only clean bootstrap logging init/status/diff/apply.
- The same fixture covers first-column drift, second-column-only target state, failed status, failed diff, failed apply, no apply before the apply phase, and byte/mode preservation for destination targets on drift/status/diff failures. Init/update source/config mutations are explicit. Failed apply mutates a managed target before returning nonzero; only the unrelated sentinel is preserved.
- Dependency Bats files cover exact installed/absent/partial dpkg states, including `iproute2` and `iputils-ping` installed classification, empty missing set, and update/install ordering.
- Dependency Bats also covers fatal `dpkg-query` exit 2 propagation without APT calls.
- Both installer call sites use checked assignments before execution. Workflow checkout permissions and credential persistence settings match the round-1 requirements.
- Workflow public job has no secret references; all secret references are confined to the separate private job.
- Workflow no longer fetches `main/setup.sh`; it executes checkout `setup.sh`, clones from `GITHUB_WORKSPACE`, and compares source HEAD with `GITHUB_SHA`.
- Workflow public matrix is exactly Ubuntu client, Ubuntu server, and macOS client, with temporary HOME and `.local/bin`, `.ssh`, and unmanaged-home sentinels.

## Not executed

- No Bats tests were run locally.
- No live `chezmoi apply`, remote installer, real-HOME mutation, GitHub Actions, fork/Dependabot run, push, PR, or merge occurred.
- GitHub Ubuntu client/server Bats proof and all three public bootstrap matrix results remain pending authorized CI.
- A014 temporary-marker/log experiment remains pending a PR run.
- `actionlint` and `yamllint` were unavailable; no dependency was installed.

## Non-product command corrections

- System Ruby 2.6 rejected the newer `YAML.load_file(..., aliases: true)` API. Retried with compatible `YAML.load_file`, which passed.
- Crit guard rejected `review_outcome: approved; ...` because it requires exact `approved|addressed`; normalized to `approved` and reran successfully.

## Round 1 revision gates

- Re-ran shell syntax, shfmt diff, ShellCheck, `make unit-test` (86 passed), `make validate-agent-assets`, Ruby YAML parsing, role renders, `git diff --check`, and the allowed-file audit successfully.
- Ran the Crit-data gate on the uncommitted revision diff; the gate required review, resolved record `r_2d91af` was saved to repo-local evidence, and `AGENT_REVIEWED=1 REVIEW_EVIDENCE=.agents/worklog/codex/review/plan-003-receipt.md make require-crit-review` passed.
- No Bats command was run locally.
