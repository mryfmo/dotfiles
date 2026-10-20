---
task_id: dotfiles-T128-chain-review-scripts-followup-a07
seat: claude-standard-dot-a011
branch: tools/chain-review-scripts-followup-a07
base: 60a6fb2b (origin/main, records boundary 25)
code_head: f5aaaf7e (f2ab71ff task copy; 6a4190f1 tests, red; fb264487 the script change; 41379201 the amended task copy; 06cc0fe1 the worker review's tests, red; c82e10a8 its fix; dbc8b67d the orchestrator's update-branch merge; 5a983079 revise 1's test, red; f2778f36 its fix; f5aaaf7e acyclic attack fixtures)
previous_head: dbc8b67d26257d76f26dd6871716b7943474fdec (revise 1)
task_sha256: b91cc496e71acaec4d3f8aed6680c59027aa75d2a6eac9d103be442de23e2e36 (amendment 1; previous ae03f0097a5f8b9b58cb6f6a709e4c664569992bd46b38577b2a071166523a75)
---

# Report: dotfiles-T128-chain-review-scripts-followup-a07

- **Seat and branch.** Seat `claude-standard-dot-a011` in `.claude/worktrees/worker-d`. The branch `tools/chain-review-scripts-followup-a07` was created with `--no-track` from `origin/main` `60a6fb2b`, after a single-command `git fetch origin main`. PR #436's branch, the previous task, was clean and pushed before the switch, and it is untouched.
- **Task file.** First `ae03f009…`, then amendment 1, `b91cc496…`, which changes the PR number from #402 to #434 in four places and nothing else. The branch copy was replaced with the amended text in `41379201` and is byte-identical to it. The task-consistency check passes (validation §1). The orchestrator said to disregard message 2710, which carried the unamended sha with the amendment's note.
- **Design.** Section 5.14 item 8 applies by reference. This record names the item and does not restate it.

## Item 1: no owned rows

This seat's first reading, a grep at the start that the validation does not paste, found no `## Owned by dotfiles-T128-chain-review-scripts-followup-a07` section in either the committed a06 acceptance record on `origin/main` or the orchestrator's working copy. The working copy now has the section, last modified at 2026-10-20T04:22:05Z, after the dispatch at 04:13:45Z. It says "No advisory rows": Item 1 is vacuous, and Item 2 carries the task. The working copy's advisory-P2 search lists no records, and the committed record still lacks the section (validation §2). So this PR touches `scripts/orchestrator/local-advisory.sh` not at all, and runs `shellcheck` on it only as the Check asks.


## Revise 1: the overrides codex needs

The orchestrator's local review of `dbc8b67d` found one P1. Codex's checked-in `shell_environment_policy.inherit=core` drops exported variables from the commands the reviewer spawns. So the two exports never reached the reviewer's own git, and a planted replacement still produced a falsely clean review. The Bash review stub had bypassed that boundary.

- **The fix (`f2778f36`).** `local-review.sh` passes both values to codex as `-c 'shell_environment_policy.set.GIT_NO_REPLACE_OBJECTS="1"'` and `-c 'shell_environment_policy.set.GIT_GRAFT_FILE="/dev/null"'`, placed before the `review` subcommand. Codex parses each `-c` value as TOML (validation §3), and the managed `set` table holds strings. So both values are quoted: an unquoted `1` would be a TOML integer.
- **The local-review row's test** is `tests/unit/test_chain_review_scripts.py::ChainReviewScriptsTest::test_local_review_passes_no_replace_and_no_graft_to_the_commands_codex_spawns`. Its stub codex behaves like `inherit=core`: it starts the command it spawns from an empty environment plus its `shell_environment_policy.set` overrides. The stub records the overrides it received, and the spawned command's environment must hold both values. It is red at `5a983079` and green at `f2778f36` (validation §5 and §6).
- **Every local-review argv** now carries the two overrides, so the shared `ARGV` expectation includes them.
- **A flaky fixture, found while revalidating (`f5aaaf7e`).** One generator run showed the "grafts read" mutant passing. The replace and graft fixtures had made canonical main and the head each other's parent, and `git merge-base` resolved that cycle by commit dates that tie within a second. Both attacks now use a parentless fake with the head's tree: the replacement gives canonical main the head's tree, and the graft cuts the head off canonical main. Each export mutant was then red in five runs out of five, and validation §7 shows all thirteen red.
- **Caps hold:** 33 changed lines outside `tests/` and `.orchestration/` (cap 200) and 94 added under `tests/` (cap 1000).
- **Not verified:** that a dotted `-c shell_environment_policy.set.<name>` adds a key alongside the managed `PATH` entry rather than replacing the table. No codex run is possible inside the sandbox.

## Item 2: the review base is canonical main

`scripts/orchestrator/local-review.sh`, as of `c82e10a8`, before revise 1 added its overrides:

- **Before the checkout,** it resolves `gh` with the script's own `resolve` helper, as it resolves `codex`. That means `mise which` under `env -i`, else `command -v`, made absolute, and a path under a `shims` directory is refused.
- **It reads canonical main** with `gh api repos/mryfmo/dotfiles/git/ref/heads/main --hostname github.com --jq .object.sha`, stdin closed.
- **It refuses, exit 2, and runs nothing,** with a named message, in two cases:
  - an answer that is not 40 lowercase hex characters, a failed call included: "canonical main could not be read with gh api; no review base";
  - a sha that is not a local commit: "canonical main <sha> is not a local commit (fetch origin main first)".
- **It passes the sha** to `codex review --base` and records it as the review file's `base:` and in its `engine:` line.
- **What it no longer does.** The `merge-base main HEAD` call and the literal `--base main` are gone. No local `main` or `origin/main` ref is read.
- **No replace ref or graft.** Before any git call it exports `GIT_NO_REPLACE_OBJECTS=1` and `GIT_GRAFT_FILE=/dev/null`, for itself and the review binary, as design 5.14 item 8 asks for replacement. A seat can write `refs/replace/` and `info/grafts` in the shared `.git`, and either can make canonical main look like a descendant of the head, so a review from the merge base would see nothing. The worker review reproduced the replace ref. This seat measured the graft: it moves `git merge-base`, `GIT_NO_REPLACE_OBJECTS` does not stop it, and `GIT_GRAFT_FILE=/dev/null` does.
- **The header** describes the base and the new exit-2 cause.

The test, `tests/unit/test_chain_review_scripts.py::ChainReviewScriptsTest::test_local_review_takes_its_base_from_canonical_main_never_a_local_ref`:

- **Planted refs.** It moves the local `refs/heads/main` and `refs/remotes/origin/main` to the head under review.
- **Refusals.** It runs four refusals: gh failing, gh answering `main`, gh answering a sha that is not local, and gh printing canonical main's sha but exiting 1. Each exits 2 with its message, `codex` never runs, and the review worktree stays where it was.
- **The base.** With the stub answering canonical main, it requires:
  - the exact `gh api` argv, once per run;
  - `--base <canonical sha>` in codex's argv;
  - `base: <canonical sha>` in the review file.
- **Replace ref and graft.** With a stand-in review binary that diffs from `merge-base(base, HEAD)`, as codex takes it, a planted replace ref and a planted graft for canonical main must still yield the head's change as a finding.
- **Red then green.** It was red at `6a4190f1`, in its refusal subtests and on the base. The replace and graft subtests were red at `06cc0fe1`, on `fb264487`'s script. All of it is green at `c82e10a8` (validation §5 and §6).

The existing local-review tests now expect the sha:

- `ARGV` is the `--base ` prefix, and each exact assertion appends the stub's sha.
- `review_head()` and the first test put a `gh` stub on PATH.
- The two interpreter tests' mise stubs answer only for tools that exist, so `gh` falls back to the PATH stub.
- The mise-resolution test expects `gh` among the names mise is asked about.

**Callers.** `scripts/orchestrator/chain-integrate.sh` runs its `fresh` step, `git fetch origin main` in the main checkout, before `local-review.sh`. So canonical main is a local commit there, unless main moves in between, and then the script refuses rather than reviewing against a stale base. Its comment at line 133 still says `local-review.sh` "diffs against" the main checkout's main. That file is outside `allowed_files`, so it is left as an observation.

**User-visible impact.** `local-review.sh` now needs a working `gh` with GitHub API access at the moment it runs. Without it, it refuses with exit 2 instead of reviewing.

## The Check

- `uv run python -m unittest tests/unit/test_chain_review_scripts.py -v`: 20 tests OK at `f5aaaf7e` on the default interpreter, Python 3.10.22 (validation §6). `tests/unit/test_chain_glue.py`: 16 OK.
- `shellcheck scripts/orchestrator/local-advisory.sh scripts/orchestrator/local-review.sh`: clean.
- **Caps:** 33 changed lines outside `tests/` and `.orchestration/` (cap 200) and 94 added lines under `tests/` (cap 1000).
- **Wrong implementations** (validation §7): thirteen replacements, each matching exactly once and each making the module exit 1:
  - the local `main` as the base;
  - `origin/main` as the base;
  - the literal `main` passed to codex;
  - no 40-hex check;
  - no local-commit check;
  - `gh` by `command -v` alone;
  - the recorded base from a local merge-base;
  - replace refs read;
  - grafts read;
  - no override passed to codex;
  - the no-replace override dropped;
  - the no-graft override dropped;
  - the review worktree checked out before canonical main is read.
- **Lint** (validation §8): `ruff format --check` and `ruff check` clean on the test file; `shfmt --indent 4 --space-redirects` shows no diff; `scripts/lint-comparisons.py` with its baseline exits 0 on the script.
- **Live** (validation §3): the real `gh api` call answers `1f97c525…` inside the sandbox, equal to `origin/main`, a local commit.

## Limitations

- The real `codex review --base <sha>` did not run: `local-review.sh` runs outside the Bash sandbox (its header says so), and every test stubs codex.
- Python 3.10 only: the default `uv run python` here. CI runs the module on Linux.
- No local Bats ran.
- **Residuals the task's threat table does not name**, for the orchestrator. A seat that can write the shared `.git` can still:
  - rewrite loose objects in the object store;
  - write a `shallow` file, which makes the merge base fail, so codex exits and no file is written;
  - change the repository configuration codex's git reads.

  Only the first would change a review silently. The `local-review.sh` row's residual covers the refs alone.

## Evidence, review, cost

- **Evidence:** `.orchestration/dotfiles-T128-chain-review-scripts-followup-a07/`: `task.md`, this report, `validation.md`, `sandbox.md`, `learning.md`, `result.txt`, `revise.yaml`, and the worker review JSON and its receipt.
- **Worker review:** one read-only round on `60a6fb2b..fb264487`, `Verdict: correct`, with one P2 and three P3, dispositioned in the review JSON:
  - P2, the replace ref (reproduced): fixed in `06cc0fe1` and `c82e10a8`, together with the graft this seat measured;
  - P3, the exit-2 list in the header: fixed in `c82e10a8`;
  - P3, gh printing a sha while failing: a refusal row in `06cc0fe1`;
  - P3, the stale `chain-integrate.sh:133` comment: declared, the file is outside `allowed_files`.
- **precheck:** pending-411 (`scripts/orchestrator/result-precheck.sh` is not on main).
- **cost:** n/a (the runtime exposes no token or cost figure to the seat).
