---
task_id: dotfiles-T128-chain-github-scripts-followup-a01
seat: claude-standard-dot-a002
branch: tools/chain-github-scripts-followup
base: 727180dbc33f50b8934c2f2ed229d1c6a744ce0d
code_commit: 1650bfb9
pr: 360
task_sha256: c89f6dc8cb5eeefcb7b8538b83dde533077d3b8e63ad919225066ffdd068597b
---

# Report: dotfiles-T128-chain-github-scripts-followup-a01

- Seat: `claude-standard-dot-a002` in `.claude/worktrees/worker-f`, on a fresh branch `tools/chain-github-scripts-followup` from `origin/main` `727180db` (boundary 15, after PR #356 merged as `ec94dc56`), PR #360.
- Task file: sha256 `c89f6dc8…`, copied byte-identical to `.orchestration/dotfiles-T128-chain-github-scripts-followup-a01/task.md`; the task-consistency check passes on the dispatched file (validation §1).
- Dispatched 00:21:35Z. Both premises replay `present` (validation §2). No question and no amendment. An alive PONG at the push named the readings and the candidates below before the Bot saw the PR.

## The owned rows and what each changed

Item 1's rows, read from `origin/main` (validation §3): five rows. The record pairs two of them as the same defect (the audit's reasons say so), so they come down to three changes, all in `scripts/orchestrator/resolve-threads.sh`.

| Row | Class | Change | Test |
|---|---|---|---|
| `4270684630` (Bot thread on PR #356, `resolve-threads.sh:65`) | resolve-response-unchecked | The mutation's `isResolved` answer is kept in `state`. A thread counts as resolved only when it is `true`. Any other answer prints `thread <id> not resolved (isResolved: <answer or none>); left open`, sets the existing left-open flag, so the exit is 3, and moves on. | `test_resolve_threads_counts_a_thread_resolved_only_when_the_mutation_answers_true` (`false`, `null` and an empty answer) |
| `audit:d15fa87:1` | resolve-response-unchecked | The same change: the audit's finding 1 is the same defect as the Bot thread (record, `audit_findings` 1). | the same test |
| `audit:d15fa87:2` | graphql-id-interpolation | The mutation text is the constant `resolve`, `mutation ($threadId: ID!) { resolveReviewThread(input: {threadId: $threadId}) { thread { isResolved } } }`. The id travels as `-f threadId=<id>`, which `gh api` sends as a GraphQL variable (`gh api --help`: "all fields other than query and operationName are interpreted as GraphQL variables"); `-f` is the string form. | `test_resolve_threads_passes_the_thread_id_as_a_graphql_variable` (an id with quotes, braces and an `addComment` text: the mutation text equals the constant and the variable equals the id) |
| `local:d15fa87:1` (the local review of `d15fa87`) | advisory-p2 | Both reply sentences carry the disposition in backticks, the form `fill_sweep.py`'s `REPLY` reads back. | `test_resolve_threads_replies_round_trip_through_fill_sweep` (the replies the stub recorded go through this checkout's `fill_sweep.py`, which recovers `fixed:abc1234` from the table row and a `not-applicable:` that lived only in the sweep JSON) |
| `audit:d15fa87:3` | reply-template-unparseable | The same change: the audit's finding 3 names the local review's finding (record, `audit_findings` 3). | the same test |

Every hunk of the diff (validation §4) serves those rows:

- `resolve-threads.sh`:
  - the `@description` sentence and `@exitcode 3`, which describe the three changes;
  - the two backticked reply sentences;
  - the `resolve` constant, with its comment and its `shellcheck disable=SC2016` directive, since `$threadId` is GraphQL's variable and not the shell's;
  - the `state` call and its check.
- `test_chain_github_scripts.py`:
  - the module docstring's one added sentence (the round-trip test runs `fill_sweep.py`);
  - the `thread_ids()` helper, which reads the `threadId` variable, so the dropped `re` import, used only for reading the id from the query text, goes too;
  - the existing test's two expected bodies, now backticked, and its two thread-id assertions, now on the variable;
  - the three new tests.

`pr-cost.sh` is unchanged: no owned row names it.

Readings, declared:

- **Exit code of a not-true answer:** it sets the existing `missing` flag, so the exit is 3, the script's code for a thread it leaves open. The summary line keeps its format (`resolved <n> thread(s); missing rows: <flag>`), since no row names a new counter.
- **Tests per row:** one test per row, but two pairs of rows are one defect each, so each pair shares its test (the table).

## Tests

The Check: 5 tests OK (validation §5); `test_orchestrator_tools.py`, which holds `fill_sweep.py`'s own tests, 40 OK (§8). Mutation pass on the script: 8 mutations, 8 caught (§9): the response check removed, the id back in the query text, each sentence without its backticks, the exit 3 and the `continue` of the new branch, the `none` default, and a named operation.

## Caps

Validation §7:

- outside `tests/` and `.orchestration/`: 1 file, 17 added + 8 deleted = 25 changed lines (cap 200);
- under `tests/`: 89 added lines (cap 1000);
- 2 files outside `.orchestration/`.

## CI and the Bot

- **The Bot:** PR #360 was opened as a draft and marked ready (00:32:22Z) after the evidence commit `9b90ab6b`. No Bot review came within 10 minutes, so `@codex review` was posted at 610 seconds (issue comment 6181708706). The Bot answered with issue comment 6181729129 at 00:44:14Z: `Codex Review: Didn't find any major issues`, `**Reviewed commit:** 9b90ab6b9d`, the head. There is no review object and no inline thread, so there is nothing to disposition (validation §10).
- **CI on `9b90ab6b`:** 13 of 13 checks pass (validation §10).
- **CI on the final head (this commit, the evidence update):** in the RESULT.

## Not done, or outside scope

Beyond the rows, not changed (item 2), and named in the alive PONG of 00:30:41Z for a next owner if the orchestrator wants one:

1. The thread query reads `reviewThreads(first:100)`. With more than 100 threads, the later ones are never read and the script can still exit 0.
2. The reply is posted before the resolve. A not-true answer therefore leaves a reply up with the thread open, and a rerun posts a second reply.
3. A disposition outside the gate's grammar is posted in a form `REPLY` cannot read back: a `fixed:<sha>` with trailing text (the existing test's table row `fixed:abc1234 evidence=git show abc1234` is one), or any backtick. The next sweep then shows a gap, so it fails closed.

- `--jq` of the resolve call is unchanged from the input and keys no stub answer (the stub keys GraphQL calls on the operation alone), so a change to it would not be caught.
- Understand-Anything hook: did not fire. plan-mode-used: no.
- cost: n/a (the runtime exposes no session figures to the seat).
