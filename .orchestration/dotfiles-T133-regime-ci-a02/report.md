---
task_id: dotfiles-T133-regime-ci-a02
reset_of: dotfiles-T133-regime-ci-a01
seat: claude-standard-dot-a008
branch: tools/regime-ci-a01
continues_from: 4a921414
pr: 418
copy_commit: 64be693c
redesign_test_commit: d16bfc6e
retained_test_commit: 6a423f4c
redesign_commit: bcbd6949
review_test_commits: [56ccbee1, 357ff237]
review_fix_commit: 1ee15af1
amendment_copy_commit: 3636fc05
previous_head: f7d2c48dad9fcf37b7111003b609e80d320f666a
revise_test_commit: 9ee208d5
revise_fix_commit: 3d695ed1
previous_task_sha256: 015a5e0f48f07cc12a2e7b65241de3f1e8547d89e091591fe1a7bbd7daf0aa90
task_sha256: 807c6b7446b7bbf795aa2b6aa6db1c46b9543b8ac953e40b4309dfd735322219
precheck: pending-411
---

# Report: dotfiles-T133-regime-ci-a02 (S1 redesign of dotfiles-T133-regime-ci-a01)

- Seat: `claude-standard-dot-a008` in `.claude/worktrees/worker-f`.
  - AGMSG-TASK at 2026-10-18T21:00:17Z with `task_sha256=015a5e0f…`. The dispatched file and the branch copy `.orchestration/dotfiles-T133-regime-ci-a02/task.md` match byte for byte (validation §1).
  - PR #418 continues on `tools/regime-ci-a01` from `4a921414`.
  - The first commit, 64be693c, deletes the a01 copy and adds the a02 copy. a01's other evidence is unchanged historical evidence.
  - An unpushed local a01 evidence commit (452e8306: the Bot round and the job's own run, written into a01's directory) was dropped before the first a02 commit, because a02 keeps a01's records unchanged. Its content is in this report's Bot section.
- Kept from a01: the worker-review fixes (the fail-closed re-plan, the checker verdict rule, the precheck evidence-only ancestor rule, the caps wording, `--no-config`, the checked git listings), amendment 1's allowlist line, and amendment 1's lineage rule. The head-execution, head-authentication and branch-name rules are replaced as below.

## What changed (Files items 1, 2, 5 to 7)

1. `.github/workflows/regime.yml` now runs on `pull_request_target` (opened, synchronize, reopened, ready_for_review), with top-level `permissions: contents: read` only and no job-level override.
   - `actions/checkout@3d3c42e5…` checks out `ref: <base sha>` with `fetch-depth: 0` and `persist-credentials: false`. `astral-sh/setup-uv@c18668ad…` runs with `enable-cache: false`.
   - A fetch step runs `git fetch --no-tags origin "refs/pull/${PR_NUMBER}/head:refs/regime/pr-head"` and fails unless that ref equals the event's head sha.
   - The verifier step runs the base's `scripts/orchestrator/regime-ci.py --base "${BASE_SHA}" --head "${HEAD_SHA}"` under `uv run --no-config --no-project --with pyyaml python -I`.
   - No step checks out, switches to, sources or runs anything from the head, and every event expression reaches the shell through `env`.
   - Concurrency, the job name `regime`, `ubuntu-24.04` and `timeout-minutes: 10` are kept.
2. `scripts/orchestrator/regime-ci.py`:
   - It runs from the base checkout (`HEAD` must equal the resolved base, a `checkout` refusal otherwise) and reads the head only through `git show <head sha>:<path>`.
   - The base's checker runs only on the base's dispatched bytes (amendment 1, below), written to a temporary `task.md`, so the C1 filter still matches `task`.
   - **Policy.** The dispatched text is read only at the base, as `<base>:.orchestration/tasks/<t>.md`, and it is the policy for `allowed_files`, the caps and `reset_of`. A head copy that differs from it is a `task-copy` violation.
   - **Without base text.** The copy's own policy is provisional, and `regime-ci: warning: <t>: task copy unverifiable (no dispatched text at base)` is printed. With `REGIME_REQUIRE_DISPATCHED=1` that becomes a `task-copy` violation (exit 1).
   - **result.txt.** It stays a consistency check (`task_copy=` against the copy's sha256) only when it is the sole binding claim. A matching token is self-attested and never removes the warning.
   - **Lineage.** A task's `reset_of` predecessors, read from the base text when it exists, keep their directories exempt from allowed-files and the evidence-only precheck rule, even after the predecessor copy is deleted. A retained predecessor copy still prints amendment 1's warning.
   - **Records-only.** It is decided by the changed paths alone; no branch name grants anything.
   - **Self-touch.** The warning now says the run executed the base's version.
3. Each Bot P1 maps to a fix:
   - 4308651010 → items 1 and 2: the base-selected workflow, the base-sha checkout, the pull ref fetched as data, and the base-only verifier and checker.
   - 4308651011 → item 2's base-dispatched policy. Head-dispatched files and result.txt tokens stay claims, and missing base text is the warning or, with the flag, the failure.
   - 4308651013 → item 2's content-only records-only exemption.

## Amendment 1 (AGMSG-TASK 2026-10-18T21:43:26Z, `task_sha256=807c6b74…`): the checker never reads a pull request's text

- **The P0.** My worker review of `4a921414..bcbd6949` (the review below) found a P0 of class `trust-boundary-pr-input`, the fourth.
  - Item 2's sentence that checks against the claimed copy still run fed the head's copy to the base checker.
  - The checker's C10 passes a backticked literal of the text to `git grep -qF` unquoted, so a literal `--open-files-in-pager=CMD` ran CMD inside the `pull_request_target` job. The reviewer reproduced it with a marker.
  - Its C6 opens the design path the text names, which was a read outside the checkout (P2).
- **The amendment** withdraws that sentence and adopts the re-plan (1ee15af1):
  - `checker(root, data)` runs the base checker only on the base's dispatched bytes.
  - An unverifiable copy skips it, with `regime-ci: warning: <t>: checker skipped: the copy is unverifiable, and the base's checker reads only the base's text`. Only the pure-Python reads of the copy still run (`allowed_files` and the Check sentence through `yaml.safe_load` and regular expressions), with no subprocess given a string from it.
  - A `reset_of` chain counts only when both copies verify against the base, so neither a head-only successor nor a verified successor drops the other copy.
  - The precheck diff takes `--no-renames`, so a prechecked code file moved into the evidence directory is drift.
- **The checker's own hardening** (`git grep -e` for literals, C6 path containment) belongs to P1-12 (`dotfiles-T133-task-generator-plan-check-a02`) and lands before `regime` is promoted.
- **Regressions:**
  - 56ccbee1 is red at bcbd6949, where the marker was written (validation §4a).
  - 357ff237 asserts that the hostile copy is reported unverifiable and that the chain needs both copies verified.
  - A verified copy reaches the checker from base bytes, as the "checker" subtest's C4 shows.
- INV-6: amendments 1. This was the one pre-push fix round, and it stands.

## The tests (Files item 3)

- The four redesign tests were written first (d16bfc6e) and are red against `4a921414` (validation §4):
  - `test_the_regime_workflow_runs_base_code_only`;
  - `test_regime_ci_reads_the_head_as_data_and_runs_the_base_verifier` (a head that rewrites the verifier and the checker into passing marker programs, and forges a dispatched text with a matching token, is judged by the base);
  - `test_regime_ci_exempts_records_only_heads_by_content_not_branch_name`;
  - `test_regime_ci_unverifiable_copy_is_a_warning_until_the_flag`.
- The retained a01 tests run on the base-checkout model (6a423f4c):
  - every rule branch's subtest;
  - the task-id test;
  - the uv-config isolation;
  - the result.txt binding (now with the unverifiable warning);
  - the checkout refusal (now at the base) and the no-merge-base exit 2;
  - amendment 1's lineage, plus a case where the predecessor copy is deleted, which is this PR's own shape;
  - records-only;
  - the warnings.
- The head-execution workflow test is replaced by `test_the_regime_workflow_runs_base_code_only`.
- The review regressions (56ccbee1, 357ff237) are listed under Amendment 1 above.
- Single-rule mutants of the redesigned logic each fail a test, including the checker fed the head copy, the chain counted with the successor alone, and the precheck diff with renames (validation §5a).

## Design notes and readings

- The precheck ancestor correction from a01 is kept. A committed precheck.json cannot name the commit that adds it, so it names an ancestor whose difference to the head lies under `.orchestration/<t>/`, or under the policy's `reset_of` predecessor directories. A `gh pr update-branch` turns the job red until a new precheck names a head the merge descends from.
- **The two transition warnings:**
  - **`task copy unverifiable (no dispatched text at base)`.** Dispatched texts currently land on `main` at boundaries, after the PR. Promotion therefore needs dispatch-before-PR order, and then the operator's `REGIME_REQUIRE_DISPATCHED=1` makes the warning a failure.
  - **`precheck absent`.** It stays a warning until the later `PRECHECK_REQUIRED` task.
- `result.txt` and `precheck.json` tokens establish consistency among the PR's own records, not authorization.
- **The operator's separate decision rows:**
  - making `regime` a required check, through `ruleset-request.sh` after P1-14;
  - setting `REGIME_REQUIRE_DISPATCHED=1`, which this task implements and leaves unset.

## The first PR's own job (Files item 8)

- The base (`origin/main`) has no `regime.yml` (premise 6, validation §0), so `pull_request_target` cannot run this PR's job.
- Validation §6 instead records a local run of the job's command line in an isolated checkout at the base sha, with:
  - the reviewed candidate `regime-ci.py` installed for that run, since the base has none;
  - the base's checker;
  - the head as data.
- The workflow gains no head-execution fallback.
- The a01 `regime` runs on this PR (pull_request, from the head) are historical evidence only.

## Residuals

- Under `pull_request_target` the job holds a read-only `GITHUB_TOKEN`, and it never executes head content. The fetched head's objects are present in the runner's repository only as data.
- Until dispatched texts land at the base before a PR, a target's policy is the PR's own claim (the unverifiable warning). The job is advisory for such PRs until the operator enables the flag.
- A PR that touches the directory of an old dispatched task, one that still has its `task.md` at the head, makes that task a target, whose authenticated policy then applies, even with the flag. The check authenticates the policy text, not which task a PR belongs to. This must be recorded before promotion; the reviewer read it from the code (worker review P3).
- The window between merge and promotion (worker review round 2, P3). The base checker reads base dispatched texts from the day `regime.yml` merges, not from promotion, and a pull request picks which one by adding `.orchestration/<that task>/task.md`.
  - Every dispatched text on `main` is therefore checker input from the merge on. A future docs text whose rule sentence names a script beside an option-shaped literal (`--open-files-in-pager=…`, or an abbreviation such as `--op…`) would run that literal under `pull_request_target`.
  - Current exposure is none: the reviewer scanned the 514 dispatched texts on `origin/main`. The only option-shaped literals are `--env HERDR_AGENTS_ROLE=...` and `- [P1]`, and git rejects both.
  - The P1-12 hardening (`git grep -e`, C6 containment) should land before regime.yml merges, not only before promotion. That is the orchestrator's ordering decision.
- The caps count additions plus deletions, and a binary file counts 0 lines. `allowed_files` globs: `/**` takes its prefix, `*` and `?` stay within one segment, and `[...]` is literal.

## Caps (validation §9)

- Outside `tests/` and `.orchestration/`: 325 of 330 (regime.yml 42, regime-ci.py 283).
- `tests/`: 417 of 480 (test_regime_ci.py 416, test_workflow_security.py 1, which differs from `origin/main` by the one `regime.yml` entry).

## Worker review (the record and the receipt name every finding)

An independent read-only reviewer did the review: a fresh general-purpose subagent of this seat, not a01's reviewer, given the task file, the threat table and the commit range.

1. Round 1 on `4a921414..bcbd6949` returned `Verdict: incorrect`, with one P0, one P2 and four P3.
   - The P0, the P2 and two P3s (lineage, renames) are fixed under amendment 1.
   - One P3 (borrowing an old task's policy) is a residual above.
   - One P3 (the evidence records missing at bcbd6949) is closed by this commit.
2. Round 2 on `bcbd6949..1ee15af1`, the same reviewer with its context kept: `Verdict: correct`.
   - The P0, the C6 read and the lineage and rename P3s are closed. Its PoCs ran again against 1ee15af1: no marker, no out-of-checkout value, exit 1 for the lineage and rename cases.
   - 20 of its 21 mutants die. The survivor (caps read from the head copy) makes no difference while byte identity fails any differing copy.
   - Its one new P3 is the residual below on the window between merge and promotion.

## Revise round (AGMSG-ACCEPTANCE status=revise, 2026-10-18T22:59:08Z, previous_head f7d2c48d; `revise.yaml`)

The task-level audit of f7d2c48 returned `Verdict: incorrect`, with two P2 and one P3 and no P1.

1. **P2 (`regime-ci.py:260`), supersession.** It checked only that both base texts existed, so an altered predecessor copy was skipped.
   - Fixed in 3d695ed1: a predecessor is superseded only when both head copies equal their base dispatched texts byte for byte (`exact[t] and exact[p]`). An altered predecessor copy is now checked as its own task, a `task-copy` violation.
   - Test: `test_regime_ci_supersedes_a_predecessor_only_when_both_copies_are_byte_equal_to_base` (9ee208d5), red at f7d2c48's verifier (validation §4b).
   - Two more mutants, supersession without byte equality and on the successor alone, are killed (§5a).
2. **P2 (validation), the bootstrap on the final head.** It now runs against the round's last head before this paste (§6). This file's commit is the only change after that head, and regime-ci reads no evidence content. The RESULT reports the same run on the final head and its identical output.
3. **P3 (the stale PR description).** It is an owner row, not this round: editing it needs `gh pr edit`, which matches a live ask rule.

The a02 receipt's `reviewer:` field now holds the one allowlisted word `claude` (the F1 lineage's lesson audit:274a536:4), with the explanation moved into the receipt's body.

## Bot

- **On a01's head 4a921414** (review 5564850518, 20:41:57Z), the three P1s:
  - 4308651010, the verifier from the PR head;
  - 4308651011, the policy bound to PR-controlled files;
  - 4308651013, the branch-name exemption.
- Under C-59 they stopped a01, and the redesign above is their fix, as `fixed:bcbd6949` each, verified by the redesign tests red at 4a921414 and green at bcbd6949.
- No `@codex review` was posted. The Bot's automatic review at ready is the only one.

cost: n/a
