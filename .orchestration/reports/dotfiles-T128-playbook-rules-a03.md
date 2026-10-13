# Report: dotfiles-T128-playbook-rules-a03

- Seat: `claude-standard-dot-a003` in `.claude/worktrees/worker-c`, branch `regime/playbook-rules`, PR #328, continued from a02's head `c4e0bb72`. a03 is a02's reset under plan 009 option A (`reset_of: [a01, a02]`).
- Task file sha256 `ee638518…` matches the TASK's `task_sha256`. It is copied byte-identical in `196d73ca` to `.orchestration/dotfiles-T128-playbook-rules-a03/task.md` (validation §1).
- History copies are not edited under a03. The a01 copy is unchanged since `1083a8c1`, and the a02 copy since `4486dbdd`. The a02 copy holds `07b78f64…`, a02 as last dispatched (amendment 1), which a02's acceptance record names at lines 24 and 25; its line 3 names the first dispatch `7929fe7a…` (§1).

## Commit `f40e530a`: items 2, 3 and 4 in the landing-condition form

| Item | Sentence now (verbatim from a03) | Test |
|---|---|---|
| 2 | "… (hashed, checked by the task-consistency check C1 to C6 once plan 007 T704 lands it and by hand until then, confirmed by the review seat), never as a PONG answer." | `test_rule_changes_travel_as_task_amendments` |
| 3 | "Once `dotfiles-T128-gate-evidence-a02` lands, the gate refuses the action without the paste; until then the orchestrator refuses it by rule. Every `not-applicable` disposition carries `; evidence=<command>` with the output pasted in the record." | `test_three_repeats_start_with_a_pasted_correction_search`: one token per sentence, plus `assertNotIn("gate-evidence-a01")` on the bullet |
| 4 | "…; C4 of the task-consistency check (plan 007 T704) verifies the path half once it lands, and the task-file review checks it by hand until then." | `test_threat_table_rows_have_a_fixed_unit`, plus `assertNotIn("C4 verifies the path half before dispatch")`; the AGENTS.md clause is unchanged |

Each landing condition holds on `main` `e0e2fe62` (§2). Nothing in `scripts/` or the Makefile reads `ACCEPTANCE_EVIDENCE`; no task-consistency checker is in the tree; `regime/gate-evidence` is open on the remote.

Item 6: the SKILL text is unchanged, and step 10.4's gate command carries `ACCEPTANCE_EVIDENCE=<acceptance record>` as before (§3). a03 renames `gate-evidence-a01` to `-a02` inside item 6's parenthetical. As in a01, the parenthetical is the task's rationale, not quoted rule text: items 2, 3 and 4 quote their sentences, and item 6 never has. Neither the task nor the operator's option A ("the three sentences") quotes a sentence for step 10.4. The Bot reviewed that command on three heads without a finding, and a SKILL sentence the task does not quote would be an undeclared change (INV-12). If the orchestrator wants the landing condition stated in step 10.4, that is a quoted sentence in an amendment. The test comment on `test_the_gate_reads_the_acceptance_record` now names `gate-evidence-a02`.

## Declared fixture changes (INV-12)

- `tests/fixtures/regime/invariants.md`: items 2, 3 and 4 (`f40e530a`).
- `tests/fixtures/regime/orchestrator-step-6.md` and `code-review-orchestration.md` were regenerated and are unchanged (`f40e530a` touches three files, §7).

## Results

- Every quoted span of items 1 to 6 is in the prose verbatim, and item 5's replaced clause is absent (§3).
- Docs module 47 OK (§4). `test_pr_feedback.py` OK, ruff clean (§5).
- 17 mutants, 17 failures (§6), including each a02 sentence put back (2b, 3e, 4c).
- Size (§7): 6 files outside `.orchestration/`; 7 added lines outside `tests/`; 100 under `tests/` (caps 500 and 1000). Every SKILL hunk lands where it did in a02.

## Bot threads

| Thread | Head | Disposition |
|---|---|---|
| 4248711363 | `c4e0bb72` | `fixed:f40e530a` (the gate sentence names its landing condition) |
| 4248711371 | `c4e0bb72` | `fixed:f40e530a` (the C4 clause names its landing condition) |
| 4248319936 | `375bae0f` | `fixed:4b62feda` (a02 amendment 1) |
| 4248319926 | `375bae0f` | the orchestrator's `gh pr update-branch` brings `main`'s `classes:` fields into the PR tree |
| 4247933544, 4247933561, 4247933574 | `9b2c02a1` | `fixed:95ba4e4c`, `fixed:8b1dbefc`, `fixed:8b1dbefc` (a02 report) |

The worker resolves no thread.

## CI and the Codex Bot on the a03 head `fe34f7db` (main-checkout copy)

- CI: all 12 check runs on `fe34f7db` are `completed success`, and the watcher exited 0 (validation §10).
- Bot: review 5492353166 of `fe34f7db` at 14:45:52Z, 350 s after the push. Two P1s and two P2s, all on sentences the task quotes verbatim (items 1 and 3), so none is fixed here; each fix is a rule-sentence change, which travels as an amendment (item 2). Counts: Bot reviews on PR #328 = 4 (`9b2c02a1`, `375bae0f`, `c4e0bb72`, `fe34f7db`); worker P0/P1 fix rounds = 0.

| Thread | Finding | Verified premise (§10) | Proposed handling |
|---|---|---|---|
| 4249303413 | P1, SKILL.md:164 (item 1): "the bus line `history.sh <team>` prints" and "the open TASK list is re-derived from the bus" read a view that `history.sh` truncates to the latest 20 rows by default | `history.sh:9` `LIMIT="${3:-20}"`; the regime-counters-a02 task file records the same limit as a threat row | `open:4249303413`: an amendment that names a complete read (an explicit limit or the storage facade `scripts/regime-counters.sh` uses) |
| 4249303433 | P1, SKILL.md:74 (item 3): the class from `scripts/regime-counters.sh` is the first three words of a review title, unfiltered, and the procedure substitutes it into an unquoted `memory search <class slug>` and into a single-quoted grep pattern | `regime-counters.sh:146-147` lowercases and splits the title, with no character filter | `open:4249303433`: an amendment that defines the slug (for example `[a-z0-9-]` only) or passes it as one quoted argument. This is a trust-boundary point: review-derived text reaching the orchestrator's shell |
| 4249303398 | P2, SKILL.md:74 (item 3): a correction can carry a partial status, which is neither `landed` nor `pending` | `C-2.md:13` `status: "landed for fixtures and the bullet; pending for C4 and T703 …"` | `open:4249303398`: define partial handling, or normalize the records |
| 4249303426 | P2, SKILL.md:164 (item 1): "with no bus event from its seat since" is false forever after one early PONG, so a later stall never triggers the PING | the sentence's own wording | `open:4249303426`: count from the seat's latest event for that task |

## Not done, or outside scope

- `gh pr update-branch`: the orchestrator's, after the a03 head (task Completion).
- `tests/unit/test_regime_counters.py` and `test_require_crit_review.py` were not run locally (PyPI is unreachable from the sandbox); neither reads the changed files.
- Understand-Anything hook: did not fire. plan-mode-used: no.

## CompactionDB

`memory add` printed `651f5fce-7002-4db5-9d48-b9af40a34601` (§8). The earlier ids stand: `aa6c26f7…`, `8bbacd66…`, `e187a179…`.

cost: n/a
