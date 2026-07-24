# Plan 003 adversarial review — round 2

**Verdict: REVISE**

Reviewed the complete `c3e69ade4d3700b4d624416ce2e5d59b31dce191..b6fa6b2ddb652e30897f9134b83fbe4c2f2a8635` range, the updated Plan 003, round-1 review, and all five updated orchestration artifacts. No Bats test was run. Five round-1 findings are closed; finding 2 is only partially closed because the updated plan still contains the inaccurate pre-apply no-mutation claim that the implementation, README, and artifacts correctly narrowed.

## Round-1 closure

| # | Status | Exact evidence |
|---|---|---|
| 1 | CLOSED | `setup.sh:159-161` and `setup.sh:202-203` capture installer text in a checked assignment before invoking a shell. `tests/install/common/setup.bats:140-153` asserts exact fetch status 23 and no side effect. A non-Bats function-substitution check returned `fetch_status=23` with no installer invocation. GNU Bash documents that an assignment-only command takes the last command-substitution status and `return` without an argument preserves the last command status. |
| 2 | **NOT CLOSED** | Runtime and user-facing wording are corrected: `setup.sh:237-256` limits the guarantee to destination targets; `README.md:291-308` explicitly permits init/update source/config mutations and disclaims apply rollback; `tests/install/common/setup.bats:283-310,327-351` models source/config mutation and partial apply. However, the updated plan still requires printing “no files were changed” at `plans/003-make-bootstrap-safe-and-publicly-testable.md:179-180` and still calls drift a “no-mutation stop” at `:193-195`. That contradicts the same plan's corrected `:169-171,184-185,293-297` boundary and the implementation. |
| 3 | CLOSED | `tests/install/common/setup.bats:258-260` resolves `sh`, `find`, `rm`, `mkdir`, `chmod`, and `cat` with `command -v`; `:266-315` uses only those PATH commands plus Bash builtins inside the constrained fixture, and `:319-321` passes `/bin/bash`, `-c`, and the quoted setup body as separate arguments to Bats `run`. Bats documents that `run` invokes its arguments as the command and arguments. No `/bin/find` assumption remains. |
| 4 | CLOSED | The fake apply writes the managed target before failing at `tests/install/common/setup.bats:308-310`; `:348-351` requires the unrelated sentinel to remain unchanged and the managed target to retain the partial write. `README.md:305-308`, executor report `plan-003.md:27,51`, validation `plan-003.md:29`, and sandbox `plan-003.md:12` all state that apply is non-transactional and has no rollback. |
| 5 | CLOSED | `install/ubuntu/common/dependencies.sh:58-66` treats exit 1 as missing and returns every other query failure. `tests/install/ubuntu/common/dependencies_unit.bats:97-115` covers exit 2 and proves no APT call. A non-Bats check under the sourced script's `set -e` returned `dpkg_status=2` with no APT output. Debian documents 0 success, 1 no package/file, and 2 fatal/unrecoverable error. |
| 6 | CLOSED | `.github/workflows/remote.yaml:12-13` sets top-level `contents: read`; both checkouts set `persist-credentials: false` at `:34-36` and `:91-93`. GitHub documents that unspecified permissions become `none` once one permission is specified, and checkout documents both event-ref defaulting and credential opt-out. |

## Finding

### P2

1. **`plans/003-make-bootstrap-safe-and-publicly-testable.md:179-180,193-195` — the updated plan still promises a broader no-mutation result than the implementation provides.** `chezmoi init` and `chezmoi update --init --apply=false` occur before status at `setup.sh:214-237`; the plan itself now acknowledges at `:169-171` that only destination targets are protected before apply. The stale “no files were changed” / “no-mutation stop” requirements therefore contradict the corrected code, README, validation, report, and safety-regression text. Narrow both plan passages to “no destination targets were changed”; explicitly allow source/config mutation before the drift gate. This is the unresolved remainder of round-1 finding 2, so all six findings are not yet closed. Official chezmoi documents that init initializes the source and creates config before optional apply, while update pulls first and only skips application with `--apply=false`.

No other P0-P2 defect was found in the requested areas.

## Confirmed adversarial areas

- **Exact Bats quoting/PATH:** `tests/install/common/setup.bats:258-321` is statically closed over the six linked external commands, absolute `/bin/bash`, and shell builtins. The quoted `"$(cat setup.sh)"` is one `-c` argument; Bash removes only trailing newlines from command substitution, which does not alter script behavior here. Bats was not run locally.
- **Partial-fetch propagation:** both installer call sites preserve the fetch status and prevent partial output execution (`setup.sh:159-161,202-203`).
- **`dpkg-query` under `set -e`:** the assignment is the `if` condition, so Bash's errexit exemption applies; `$?` is captured immediately in the `else` branch and exit 2 propagates (`install/ubuntu/common/dependencies.sh:58-66`).
- **Workflow matrices and trust split:** public and private matrices are each exactly Ubuntu client, Ubuntu server, and macOS client (`.github/workflows/remote.yaml:16-25,71-80`). Public steps contain no secret reference; secret-derived values and private restoration remain at `:83-115`.
- **Checkout-local SHA:** checkout defaults to the triggering event ref/SHA, the workflow creates `bootstrap-under-test` at that checkout (`.github/workflows/remote.yaml:34-42`), passes the local `GITHUB_WORKSPACE` repo and branch to chezmoi (`:56-58`), and asserts cloned source HEAD equals `GITHUB_SHA` (`:60`). Git documents that cloning a branch points the new HEAD at that branch. Live GitHub matrix proof remains accurately unclaimed in report `plan-003.md:29,31,36,51` and validation `plan-003.md:39-42`.
- **Target-only status:** `setup.sh:242-247` checks only column one; `tests/install/common/setup.bats:300-301,330-333` proves a space in column one with `M` in column two proceeds to diff/apply, matching chezmoi's official two-column status contract.
- **Non-rollback wording outside the plan defect:** `README.md:291-308`, report `plan-003.md:27,51`, validation `plan-003.md:29`, sandbox `plan-003.md:12`, and learning `plan-003.md:11` all accurately distinguish source/config changes, destination-target protection before apply, and partial apply effects.

## Read-only/static checks

- Passed: `bash -n setup.sh install/ubuntu/common/dependencies.sh`
- Passed: `shfmt -i 4 -sr -d setup.sh install/ubuntu/common/dependencies.sh`
- Passed: `shellcheck -x setup.sh install/ubuntu/common/dependencies.sh`
- Passed: Ruby YAML parse and exact public/private matrix extraction
- Passed: `git diff --check c3e69ade4d3700b4d624416ce2e5d59b31dce191..b6fa6b2ddb652e30897f9134b83fbe4c2f2a8635`
- Passed: base ancestry, exact HEAD, and eight-file allowed-scope audit
- Passed: non-Bats shell checks for fetch exit 23/no execution and dpkg-query exit 2/no APT
- Not run: Bats, live installers, live chezmoi apply, GitHub Actions, push, PR, or merge

## Primary official references

- [GNU Bash: command substitution](https://www.gnu.org/s/bash/manual/html_node/Command-Substitution.html), [simple command expansion](https://www.gnu.org/s/bash/manual/html_node/Simple-Command-Expansion.html), and [`return`](https://www.gnu.org/software/bash/manual/html_node/Bourne-Shell-Builtins.html)
- [Bats: `run` command behavior](https://bats-core.readthedocs.io/en/stable/writing-tests.html#run-test-other-commands)
- [Debian `dpkg-query(1)` exit status](https://manpages.debian.org/bookworm/dpkg/dpkg-query.1.en.html#EXIT_STATUS)
- [chezmoi status](https://www.chezmoi.io/reference/commands/status/), [init](https://www.chezmoi.io/reference/commands/init/), [update](https://www.chezmoi.io/reference/commands/update/), and [apply](https://www.chezmoi.io/reference/commands/apply/)
- [GitHub workflow permissions](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax#permissions), [GitHub variables](https://docs.github.com/en/actions/reference/workflows-and-actions/variables), [official `actions/checkout`](https://github.com/actions/checkout), and [Git clone](https://git-scm.com/docs/git-clone)

## Plan-quality gate note

The target repository exposes no plan-quality validator, Make target, hook, subagent definition, or CI entry point. The installed `plan-quality-gate` skill's manual independent-review checklist was therefore applied; no source or plan was edited. The plan has the expected scope, current-state evidence, commands, adversarial checks, STOP conditions, maintenance notes, and safety section, but the contradictory no-mutation wording above prevents acceptance.

REVIEW-RESULT v1 task_id=plan-003 verdict=REVISE report=/Users/mryfmo/Workspace/dotfiles/.orchestration/acceptance/plan-003-review-round-2.md
