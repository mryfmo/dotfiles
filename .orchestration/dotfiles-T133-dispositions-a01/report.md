---
task_id: dotfiles-T133-dispositions-a01
round: 1
status: result
---

# Report

Worker `claude-standard-dot-a009` (Claude Code, worker-c). Branch `tools/dispositions-a01`, fresh from `origin/main` de3b73cc; PR #419; code head 5c28ccf65d195ad574ae339de33b8ef789818234, then dd567d772d94c90b720b4e0c1dbc0c118ed9a6c3 after CI round 1 and Bot round 1 (below; the RESULT names the final evidence-only head). The task copy `.orchestration/dotfiles-T133-dispositions-a01/task.md` is byte-identical to the dispatched file: sha256 `5ed78fc9a916decddb3fd668e3fb5494b7a01f219e02a68e4c93b7794feeae48`. INV-6: amendments=0 questions=0 revises=0. `origin/main` moved to 3e41e36a (#409) during the task; it touches none of this task's files.

## What changed

- `scripts/orchestrator/dispositions.py <pr> <head> --feedback <sweep.json> [--out <json>] [--require-refutation] [--commits <json>]` (new, standard library only, `python -I`).
- `scripts/orchestrator/orch-gate.sh` (one step).
- `tests/unit/test_dispositions.py` (new, three tests).
- `tests/unit/test_orch_gate_path.py`: one new case, plus three supporting lines:
  - the setUp copies `dispositions.py` next to `orch-gate.sh`;
  - the default sweep fixture gains `"items": []`, so the step reads it without a hold line;
  - the fake interpreter hands a `dispositions.py` run to the real one, so only gate runs write `gate-env`.

## The proposal rule

A thread is a `review_comment` item of the sweep, or a `review` item whose body carries a P0–P3 badge. Its path and line are the item's own; a review-body finding has neither in the sweep, so they come from its body's first `/blob/<sha>/<path>#L<n>` link (Bot round 1). A thread with no location still gets the not-applicable demand, and its not-applicable is still verified. Every path reaches git as `:(literal)<path>`, so a PR's file name is never pathspec magic (Bot round 1). The commit is resolved in this order:

1. the item's `original_commit_id` (or `commit`, which review items carry);
2. the `--commits` map (url → commit);
3. `gh api repos/<repo>/pulls/comments/<id> --jq .original_commit_id`, the id taken from the `#discussion_r<id>` URL.

A gh failure, or a commit that is not a commit in this checkout, is a `hold` line. Holding sets `proposal: null` and exit 2; it never guesses.

`git diff <commit>..<head> -- <path>` (`--no-ext-diff --no-textconv -U3`) is parsed for a hunk whose old or new range covers the line. When one does, `git log --no-merges <commit>..<head> ^<base_sha> -- <path>` is walked newest first. The proposal is `fixed:<c>` for the first commit whose own hunks overlap that hunk. The `--no-merges ^<base_sha>` restriction keeps the proposal inside `base..HEAD`, which the gate requires of a `fixed:` commit. With no covering hunk, the proposal is `not-applicable:` with the reason to fill. A thread without a line (a file-level comment) gets that demand directly, and no commit is needed. The existing `disposition` is never changed.

## The three refutation forms and their verification

A disposition keeps the gate's grammar, `not-applicable:<reason>; evidence=<form>` (`scripts/require-crit-review.py` is not edited). The refutation form is the evidence:

- `test:<selector>`, either `tests/<path>.py::<name>` (run as `-m unittest tests.<path> -k <name>`, as the precheck does) or a dotted unittest name. It runs as `uv run --no-project python -m unittest …` in this checkout. It is accepted only on exit 0, which excludes `Ran 0 tests` (exit 5). The record is `exit <n>: <last line>`.
- `source:{"url": …, "fetched_at": …, "quote": …}`, a JSON object with an https or file URL. The page is fetched (at most 10 MiB, 30 s). The quote must occur in the page text: tags removed, entities unescaped, whitespace collapsed. The record is the page's `sha256=`.
- `diff:<range>`, a `<rev>..<rev>` range (`[\w./^~]`, two or three dots). It is accepted only when `git diff <range> -- <path>` has no hunk covering the thread's line.
- Any other evidence is `legacy-evidence`, and a not-applicable without `; evidence=` is `none`. Both are reported as `unverified`, and count as `FAIL` (exit 1) only under `--require-refutation`.

The requirement covers threads only (the Goal's "every review-comment item"). Summary comments, annotations and statuses keep their dispositions as the gate checks them.

## The gate step (`orch-gate.sh`)

Right before the gate, after the evidence copy, the wrapper runs `"${python}" -I dispositions.py <pr> <head> --feedback <sweep> --out /dev/null` under the gate's own `env -i PATH=<private> HOME=…`, from this trusted checkout and not from the review worktree. This is the point premise 3 names: the gate's one invocation with `PR_FEEDBACK_EVIDENCE`. `${python}` is the interpreter `uv python find` resolved there.

- With `DISPOSITIONS_REQUIRE_REFUTATION=1` it adds `--require-refutation`, and any nonzero exit (1, or a hold's 2) refuses with exit 2 and the tool's lines. The wrapper's existing trap then restores the review worktree to `origin/main`.
- Otherwise the lines are printed as a report and the gate runs.

Round 1 placed the step before the review worktree moved; CI round 1 below explains why it moved. The private PATH has no `uv`, so a `test:` selector run from the gate uses the wrapper's interpreter (`sys.executable`), which is uv's own. The selector runs in this checkout, the orchestrator's `origin/main`, never in the PR's head.

## Red and green (validation.md)

- The new gate case against `origin/main`'s `orch-gate.sh` (a scratch worktree of the code head with that one file restored) fails: `AssertionError: 2 != 0`. The wrapper ran the gate without re-validating.
- On 5c28ccf6, both modules give 7 tests OK.
- The `dispositions.py` tests cover a new script, so they have no earlier red. The proposal case pins the fix commit rather than the newer line-1 commit; the refutation case pins each form's accept and refuse.
- On dd567d77, both modules and `tests/unit/test_orchestrator_tools.py` (the other module that drives `orch-gate.sh`) give 64 tests OK.

## CI round 1 (74baf481)

The four `test` jobs failed one test, `tests/unit/test_orchestrator_tools.py::test_orch_gate_restores_the_review_worktree_when_setup_fails`, at `self.assertIsNone(self.call("gate-python"))`. That test makes `cp` fail during the evidence copy and proves the gate never ran by "the interpreter was never called". The round-1 step called the same interpreter for `dispositions.py` before the copy, so the proxy broke. That module is outside `allowed_files`, and my miss was not running every test that drives `orch-gate.sh` before pushing.

The root-cause fix follows the task's own premise 3: the re-validation runs right before the gate's one invocation, after the evidence copy, so a setup failure still stops the wrapper before any interpreter runs. A refusal there exits through the existing trap, which restores the review worktree. `test_orch_gate_revalidates_the_dispositions_before_the_gate` now asserts the order: checkout, then the step run from the trusted root, then the trap's restore. It no longer asserts an untouched review directory.

## Bot round 1 (review 5563269439 of 74baf481, 13:55:07Z)

- 4307288053 [P1] `dispositions.py:162`: fixed:dd567d77. A badged review-body finding never reached validation, because the sweep gives `review` items no path or line and the predicate required both. Every badged review item is now a thread. Its location comes from its body's first blob link, and its not-applicable is verified with or without a location. Red-then-green in the two closed-row tests:
  - the proposal case adds a badged review located by its blob link, proposed `fixed:<fix>`, and an unbadged summary review that gets no proposal;
  - the refutation case adds a badged review without a link whose legacy evidence fails under `--require-refutation`.

  On 74baf481's code the first got no proposal and the second no `refutation` at all (`KeyError`).
- 4307288056 [P2] `dispositions.py:51`: fixed:dd567d77. Thread paths reached git as pathspecs, so a legal file name starting with `:` was magic. `git diff`/`git log` now take `:(literal)<path>`. Red-then-green: the fixture gains a file named `:b.py` changed by the fix, and a `diff:` refutation on `:b.py` line 10 must be refused. With the location fix alone it was accepted, because git diffed the untouched `b.py`; on dd567d77 it is refused. This P2 was fixed in the worker round because it is a trust-boundary case on this PR's own code, inside `allowed_files`, three lines long.

No `@codex review` follows the fix round (the no-prompt rule).

## The real run (PR #409's sweep, validation.md)

`dispositions.py 409 4fe24380… --feedback <main checkout>/.orchestration/validation/dotfiles-T133-ci-efficiency-a02-pr-feedback.json` exits 0. gh resolved both thread commits.

- `discussion_r4305896433` (`.github/workflows/remote.yaml:75`): proposal `fixed:99b07d2b…`, equal to the hand disposition.
- `discussion_r4305896435` (`scripts/orchestrator/ci-rerun.sh:90`): proposal `fixed:492e7e28…`, where the hand disposition is `fixed:99b07d2b`. Both commits are in `de3b73cc..4fe24380` and both touch the hunk: 99b07d2b changes lines 86–91 and 492e7e28 inserts at 90. The rule names the newest; the record names the fix of that finding. A proposal is a candidate that a person or item (16)'s second opinion confirms, so this is the case the confirmation exists for.

## The legacy-evidence transition

Run as specified: 37 of the 131 `*-pr-feedback.json` on this branch (`origin/main` de3b73cc) carry `evidence=`, and 47 of 141 in the main checkout (validation.md). Under `DISPOSITIONS_REQUIRE_REFUTATION=1`, a thread whose not-applicable carries that legacy form refuses the gate. The flip is a decision row (Out of scope); until then the step reports.

## Later task

Programs item (16), `audit-pool.sh --second-opinion`, confirms these proposals. It is a later task after PR #410 merges, because `audit-pool.sh` is #410's (premise 5).

## Observations for the orchestrator

- `source:` accepts `file://` URLs, as the task's tests require. In the gate step that means a sweep's disposition can make the wrapper read a local file and report whether a quote occurs in it. The sweep is the orchestrator's own file, so this is a residual on that file's authorship, not a PR input. If dispositions ever come from a PR copy, restrict `file://` to tests.
- The gate step's `env -i` drops proxy variables. Inside a sandbox whose egress goes through a proxy, a `source:` fetch of an https URL may fail and become `FAIL` under the flag. The report mode shows it first.

[memory:decision] T133 P1-10 part 1: dispositions.py proposes fixed:<newest non-merge commit in thread-commit..head ^base touching the covering hunk> or demands not-applicable; the refutation form travels as the gate's evidence= payload (test:, source:{url,fetched_at,quote}, diff:<range>), other evidence is legacy-evidence; orch-gate.sh re-validates before the review worktree moves and refuses only under DISPOSITIONS_REQUIRE_REFUTATION=1. Recorded with `uv run --no-project .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content '…'` as memory `948b228f-b574-462e-99fc-c712602f8b98` (validation.md).

## Not done yet

The evidence commit, the push, CI on the final head, the Bot window from that push and the RESULT (`task_copy=5ed78fc9…`, `precheck=pending-411`, `bot_rounds=2`).

cost: n/a
