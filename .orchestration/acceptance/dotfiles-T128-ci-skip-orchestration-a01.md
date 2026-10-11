# Acceptance: dotfiles-T128-ci-skip-orchestration-a01 (plan 006 Phase A5: records-only PRs skip the heavy steps, fail-closed)

- **Decision:** pending the audit of the final head (this section precedes the audit).
- pr=320
- **Worker:** `claude-standard-dot-a003` (Claude Code, `standard`), `.claude/worktrees/worker-f`, branch `feat/ci-skip-orchestration`, PR #320. TASK 445 at 05:42:10Z (task file `6dd3d682…`), draft PR 05:42:55Z (45 s; INV-10 holds), PONG 446 at 05:44:48Z with GitHub doc evidence that the `changes`-job pattern is fail-open, amendment 1 (TASK 447 at 05:46:20Z, task file `8e9c23da…`: in-job fail-closed decision, two threat-table rows added once, `test.yaml` fixed the same way), RESULT 456 at 06:32:16Z on head `d6343494`: commits `be935742` (task.md), `f7393ee1` (task.md at amendment 1), `9fcd2b04` (content), `b3f88beb` (evidence), `e872f69f` (Bot fix round 1), `d6343494` (evidence). CI 13 of 13 (the `changes` context no longer exists; the seven required contexts are unchanged), watcher joined. `bot_rounds=3`, one fix round: round 1 on `b3f88beb` found one P2 (shallow base fetch after a full checkout left no merge-base; reproduced rc 128; fixed in all three fetches with a test that moves `origin/main` after the head), later heads drew no review (👍 06:22:39Z). No P0/P1 on any head.
- **Orchestrator review (`…-ci-skip-orchestration-a01-crit.json`, receipt `…-review-receipt.md`):** approved; details in the records. The worker's finding that the specified `changes`-job pattern was fail-open (GitHub docs: a job that `needs` a failed or skipped job is skipped, and a skipped required job reports Success) corrected the task's own premise; the amendment adopted the worker's default.
- **Sweep (`…-ci-skip-orchestration-a01-pr-feedback.json`, head `d6343494`, 8 items, every item dispositioned):** 4240499289 `fixed:e872f69f` (replied and resolved by the orchestrator at 06:34Z; 0 unresolved); the review container, two issue comments, three runner notices and the CodeRabbit status `not-applicable:` with reasons.
- **Counters by hand before this acceptance action (A1 item 5; A3 not yet on `main`):**

  ```
  $ H=~/.agents/skills/agmsg/scripts/history.sh; $H dotfiles-conformance --limit 1000 >"$TMPDIR/h.txt"; wc -l <"$TMPDIR/h.txt"; date -u +%FT%TZ
  457
  2026-10-11T06:34:01Z
  $ T=dotfiles-T128-ci-skip-orchestration-a01; grep -c "AGMSG-TASK v1 task_id=$T " "$TMPDIR/h.txt"; grep "AGMSG-TASK v1 task_id=$T " "$TMPDIR/h.txt" | grep -c 'amendment='; grep "AGMSG-PONG v1 task_id=$T " "$TMPDIR/h.txt" | grep -c 'status=question'; grep -c "AGMSG-RESULT v1 task_id=$T " "$TMPDIR/h.txt"; grep "AGMSG-ACCEPTANCE v1 task_id=$T " "$TMPDIR/h.txt" | grep -c 'status=revise'
  2
  1
  0
  1
  0
  $ gh api --paginate repos/mryfmo/dotfiles/pulls/320/comments --jq '[.[]|select(.in_reply_to_id==null and (.body|test("P0 Badge|P1 Badge")))]|length'
  0
  ```

  tasks=2 amendments=1 questions=0 results=1 revises=0 first_result_head=d6343494 bot_p1_heads_after_result=0 audits=1 (below) wall=05:42:10Z..06:32:16Z (0:50). No S2 threshold; S1: one P2 class, once.
- **Three metrics (PR #320):** revision rounds 0 (one amendment, one Bot fix round); wall TASK to RESULT 50 min (merge time added below); cost `n/a` from the worker (27 permission-gated commands, two gate denials not reworked: an `rm -rf` on a variable path and a GraphQL thread-state query, both avoided); seats: one standard worker, one audit.
- **Completion condition still open (A5):** the next `.orchestration`-only PR merges within 10 minutes with every required check reported; measured on the boundary PR after this merge and pasted here.
- **Exemption declared:** acceptance and evidence-sync bookkeeping; agmsg control plane.

<!-- audit-input-boundary -->

## Audit of `d6343494` (headless, `…-ci-skip-orchestration-a01-audit-d634349.md`, verdict `incorrect`, four findings) and revise round 1

- Finding 1 (P2, `test.yaml` decide step allows rename detection, so a move from `home/a` to `.orchestration/a` skips the tests): real; `--no-renames` as in `remote.yaml`, with a rename case in the decision test. Revise round 1, check `test_the_unit_test_decision_ignores_renames`.
- Finding 2 (P2, the hand-written YAML reader ignores quoted keys, so `'if': false` on a required job or `'continue-on-error': true` on `decide` passes the structural tests): real; the reader treats quoted keys like bare ones (or a real parser when the test environment has one), with a quoted-key mutation test. Revise round 1, check `test_structural_tests_see_quoted_keys`.
- Finding 3 (P2, INV-2: the task's invariant sentence matches the working-copy design v16, not committed `main` at `b896d9bc`, whose map also lacks this task): true as stated. The dispatch followed plan 006 Phase 0's operator-approved rule (A1 item 3: a boundary PR is never a dispatch prerequisite) while V1c's regime job, the mechanical check, does not exist yet; the design v16 lands with the boundary PR that follows the Phase A merges. Recorded as a process deviation, not refuted: `not-applicable:` in the gate's terms, with this reason.
- Finding 4 (P2, the sweep JSON predated the orchestrator's reply and thread resolution): the sweep is re-run after thread resolution and immediately before the gate, on the final head; the order (resolve, then sweep, then audit) is now the orchestrator's procedure. `not-applicable:` evidence freshness, refreshed before the gate.
- Revise ACCEPTANCE sent 06:47Z (`previous_head=d6343494`, two `check=` selectors); the final head gets a fresh audit.

## Revise round 1 RESULT (485, 07:12:59Z) on `dc4e6c37`

- One commit `dc4e6c37` (fixes, tests, evidence, `revise.yaml` with `previous_head=d6343494` and the two checks). Checks: `tests/unit/test_workflow_orchestration_skip.py::DecisionTest::test_the_unit_test_decision_ignores_renames` and `…::RequiredContextsTest::test_structural_tests_see_quoted_keys` (the module has no single class; each check lives in the class that owns its rule). Fixes: `test.yaml`'s unit-test decision diff runs with `--no-renames`; the hand-written reader reads quoted keys and job names like bare ones (no PyYAML in the test environment; block-style mappings only, stated). Removal proofs 4 of 4 including the audit's quoted-key mutations. CI 13 of 13, watcher joined. `bot_rounds=4`, one fix round in total; no thread open (the Bot left no review on `dc4e6c37`, 👍 07:04:32Z).
- Orchestrator review of the delta: approved (`…-crit.json` record a5-review-4; receipt moved to head `dc4e6c37`).
- Sweep refreshed at `dc4e6c37` after thread resolution (the order the first audit asked for): every item dispositioned, including the review object GitHub created for the orchestrator's own reply.
- Counters by hand before this acceptance action (07:14Z, `history.sh --limit 1000` to a file, 485 rows): tasks=2 amendments=1 questions=0 results=2 revises=1 (INV-6 counts the revise RESULT) bot_p1_heads_after_result=0. No S2 threshold; S1: no class twice. Audit 2 of `dc4e6c37` below.
