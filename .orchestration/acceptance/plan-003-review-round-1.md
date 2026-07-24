# Plan 003 adversarial review — round 1

**Verdict: REVISE**

Reviewed the complete `c3e69ade4d3700b4d624416ce2e5d59b31dce191..d0b4abca5a5f16080559d07b2cdb6e1ceada9665` diff, Plan 003, and its five required orchestration artifacts. No Bats test was run.

## Findings

### P1

1. **`setup.sh:158-159,199` — failed downloads can execute partial installer output.** Both installers are executed as an argument containing command substitution. Bash gives the simple command the status of `/bin/bash` or `sh`, not the nested fetch; a local reproduction with a fetcher that printed `printf partial` and returned 23 executed `partial` and returned 0. Bash also removes trailing newlines from command substitution. Thus a truncated curl/wget response can be executed despite a transfer failure. curl's `--fail` and wget's documented nonzero network/protocol statuses do not repair this shell-level masking. Minimal fix: capture each installer in an assignment whose status is checked (`installer="$(fetch_url URL)" || return`), then execute it; add a fixture that prints a side-effecting partial body, returns nonzero, and proves the body was not run. Sources: [Bash command substitution](https://www.gnu.org/s/bash/manual/html_node/Command-Substitution.html), [Bash simple-command status](https://www.gnu.org/s/bash/manual/html_node/Simple-Command-Expansion.html), [curl `--fail`](https://curl.se/docs/manpage.html#-f), [GNU Wget exit statuses](https://www.gnu.org/software/wget/manual/wget.html#Exit-Status).

2. **`setup.sh:210-245` — the drift gate occurs after mutations, contradicting the no-mutation guarantee.** `chezmoi init` can create/regenerate config, `chezmoi update --init` pulls the source and regenerates config, and line 227 deletes encrypted source files before `status` runs. A drift or status/diff failure therefore does not justify “no files were changed,” and existing config/source state can already differ. Minimal fix: on an existing initialized installation, run and enforce the old-state `status`/`diff` gate before `init`, `update --init`, or source deletion; retain a post-update preview before apply, and add config/source sentinels to the failure oracle. Official chezmoi documents init config creation and `update --init` config regeneration: [init sequence](https://www.chezmoi.io/reference/commands/init/), [update and `--init`](https://www.chezmoi.io/reference/commands/update/).

3. **`tests/install/common/setup.bats:240-251` — the wget-only fixture is not runnable and is not portable.** The subprocess PATH is only `${tmpdir}/bin`, but fake `wget` calls external `cat`, which is never linked; static reproduction yields `cat: command not found`. The fixture also hardcodes `/bin/find`, while macOS common Bats runs this file and `find` is not portably at that path. Consequently the authored clean/drift/failure oracle cannot provide the claimed Ubuntu/macOS evidence. Minimal fix: include `cat` and link every fixture command from `command -v` (or use known absolute commands per runner), then let GitHub Bats validate both OSes.

4. **`tests/install/common/setup.bats:280-282,312-315` — the apply-failure preservation oracle is vacuous.** Fake apply exits before writing anything, so unchanged hashes do not test the Plan 003 invariant that a failing apply leaves targets unchanged. Real `chezmoi apply` ensures multiple targets and scripts in application order; this change adds no transaction/rollback. Minimal fix: make the fake apply mutate one target and then fail; either implement recovery/rollback that makes the test pass or narrow the plan/report/README claim to drift/status/diff failures rather than failed apply. Source: [chezmoi apply](https://www.chezmoi.io/reference/commands/apply/).

### P2

5. **`install/ubuntu/common/dependencies.sh:57` — fatal dpkg-query errors are misclassified as missing packages.** Debian documents exit 1 for a missing query and exit 2 for fatal/unrecoverable errors. The current `! query || status != installed` path treats both as “missing” and proceeds to apt operations, masking a broken package database or invalid invocation. Minimal fix: capture the query status, accept 0 plus exact `install ok installed`, treat 1/non-installed status as missing, and propagate status 2; add one fatal-query fixture. Source: [Debian dpkg-query(1)](https://manpages.debian.org/bookworm/dpkg/dpkg-query.1.en.html).

6. **`.github/workflows/remote.yaml:12-108` — checkout credentials have broader default permissions than this read-only bootstrap needs.** `actions/checkout@v7` is current and the PR merge-SHA/local-branch logic is otherwise consistent, but checkout recommends explicit `contents: read`; without a workflow/job `permissions` block, trusted-event defaults may be broader and credentials are persisted for subsequent installer-controlled git commands. Minimal fix: add top-level `permissions: contents: read` and set `persist-credentials: false` on both checkouts. Source: [official actions/checkout v7 README](https://github.com/actions/checkout).

### P3

None.

## Confirmed areas

- The chezmoi first-column parser matches the official two-column contract; first column is last-written versus actual, second is actual versus target. A missing second-column-only fixture is a coverage gap, not a parser defect by itself. [chezmoi status](https://www.chezmoi.io/reference/commands/status/)
- `dpkg-query -W -f='${Status}'` and exact `install ok installed` comparison are valid for successful queries.
- Fork and Dependabot secret handling is fail-closed here: unavailable secrets evaluate empty, secret-derived job env is the documented way to gate steps, and the public job does not reference secrets. [GitHub secrets](https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/use-secrets), [Dependabot restrictions](https://docs.github.com/en/code-security/reference/supply-chain-security/dependabot-on-actions)
- `actions/checkout@v7`, default `pull_request` merge-commit checkout, `GITHUB_SHA`, and `${{ runner.temp }}` are current and valid. The eight changed files are all within the allowed implementation list.

REVIEW-RESULT v1 task_id=plan-003 verdict=REVISE report=/Users/mryfmo/Workspace/dotfiles/.orchestration/acceptance/plan-003-review-round-1.md
