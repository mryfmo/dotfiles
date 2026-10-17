---
format: 2
task_id: dotfiles-T129-audit-inherit-replan-json-a01
kind: code
security: false
design_review:
  receipt: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round22.md
  design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md
allowed_files:
  - scripts/orchestrator/chain-integrate.sh
  - scripts/require-crit-review.py
  - scripts/regime-counters.sh
  - scripts/orchestrator/acceptance-front-matter.py
  - tests/unit/test_chain_glue.py
  - tests/unit/test_require_crit_review.py
  - tests/unit/test_regime_counters.py
  - tests/unit/test_orchestrator_tools.py
  - tests/fixtures/gate-evidence/acceptance-s6-present.md
  - .orchestration/dotfiles-T129-audit-inherit-replan-json-a01/**
after: []
threat_table:
  - control: the PR edits scripts/orchestrator/chain-integrate.sh in one place (the audit step inherits the previous head's receipt when the head is an update-branch merge whose PR diff has the same patch-id)
    disposition: "closed: tests/unit/test_chain_glue.py::test_integrate_inherits_the_audit_across_an_update_branch_only_head"
  - control: the PR edits scripts/require-crit-review.py in two places (the S1 re-plan is read from the record block's replans object, never from a body line; swept_finding_ids takes an inherited audit's sha7 from the summary's first line)
    disposition: "closed: tests/unit/test_require_crit_review.py::test_s1_replan_is_read_from_the_record_block_json and ::test_s6_reads_an_inherited_audit_s_ids_under_the_parent_sha7"
  - control: the PR edits scripts/regime-counters.sh in one place (the S1 line's re-plan=present|missing is read from the same replans object)
    disposition: "closed: tests/unit/test_regime_counters.py::test_s1_replan_token_comes_from_the_record_block_json"
  - control: the PR edits scripts/orchestrator/acceptance-front-matter.py in one place (it carries a replans object through the block rewrite and validates its shape)
    disposition: "closed: tests/unit/test_orchestrator_tools.py::test_front_matter_keeps_and_validates_the_replans_object"
  - control: the PR edits tests/unit/test_chain_glue.py only for the new case
    disposition: "residual: one new test beside the existing ones, which stay; the module's stub scripts (the stub orch-audit.sh records its calls) and real git in a temporary repository as today"
  - control: the PR edits tests/unit/test_require_crit_review.py only for the two new cases, the write_record helper and the four S1 tests item 3 names (three move to the object, one is removed)
    disposition: "residual: the edits are exactly the list in item 3; every other test stays byte-identical, which the audit's diff review checks"
  - control: the PR edits tests/unit/test_regime_counters.py only for the new case and the four S1 tests item 3 names (two move to the object, one is removed, one fixture line moves)
    disposition: "residual: the edits are exactly the list in item 3; every other test stays byte-identical, which the audit's diff review checks"
  - control: the PR edits tests/unit/test_orchestrator_tools.py only for the new front-matter case
    disposition: "residual: one new test beside the existing ones"
  - control: the PR edits tests/fixtures/gate-evidence/acceptance-s6-present.md only to move its re-plan line into the block's replans object
    disposition: "residual: the fixture follows the schema in the same commit"
  - control: "the record block's replans object as an input (JSON read by jq in the counters and by json in the gate and the front-matter writer)"
    disposition: "residual: one schema for every reader: {<slug>: {specification, design, implementation, verification}} with non-empty strings, validated by the front-matter writer and refused by the gate when malformed; no tool parses a prose line, so the tokenizer and line-ending classes of #382 cannot recur"
  - control: the task-file copy on the branch (.orchestration/dotfiles-T129-audit-inherit-replan-json-a01/task.md)
    disposition: "residual: byte-identical to the dispatched file (its sha256 is in the TASK line); the orchestrator compares at acceptance"
  - control: the branch evidence records under .orchestration/dotfiles-T129-audit-inherit-replan-json-a01/ (report.md, validation.md, sandbox.md, learning.md)
    disposition: "residual: prose and pasted command output; the sandbox record lists every permission-gated command; the audit reads them"
  - control: "task metadata (the front matter of the task copy: kind, allowed_files, threat_table, premises)"
    disposition: "residual: read with PyYAML by the task-consistency check C1 to C10 and C7b before dispatch and at acceptance; a changed field fails the byte comparison above"
  - control: metadata separators (the --- lines that bound the front matter of the task copy and of every evidence record)
    disposition: "residual: PyYAML splits on the first document only and the byte comparison covers the whole file"
  - control: in-process effects
    disposition: "residual: the tests run the four scripts as subprocesses with the modules' fixture storage facade, stub gh, stub scripts and real git in a temporary repository, and import only the standard library; nothing is imported into another process"
  - control: workflow and interpreter or environment inputs
    disposition: "residual: no workflow or interpreter file is in allowed_files; chain-integrate.sh runs git (rev-parse, merge-base, diff-tree, patch-id) and the main checkout's scripts as today, never the PR head's copies; the gate and the front-matter writer run under their interpreter as today; the counters run jq, git and gh as today; a PR checkout as cwd chooses nothing new"
  - control: new or renamed scripts
    disposition: "residual: no new or renamed script; any other new or renamed script is an undeclared change the audit fails"
  - control: orchestrator effect merge
    disposition: "residual: merge only through gh pr merge --squash --match-head-commit <audited head> after the gate (Orchestrator Playbook step 10.5); never a local merge or a push to main"
  - control: orchestrator effect update-branch
    disposition: "residual: gh pr update-branch moves the head, so CI, the sweep and the audit run again on the new head before any gate (Orchestrator Playbook step 10)"
  - control: orchestrator effect forced worker removal
    disposition: "residual: none planned; herdr-agents --remove-worker refuses a dirty worktree without --force, and a forced removal is recorded in the acceptance record with the uncommitted state it discarded"
premises:
  - claim: the chain on origin/main knows no inherited audit
    command: git show origin/main:scripts/orchestrator/chain-integrate.sh | /usr/bin/grep -c "inherited"
    output: |-
      0
  - claim: 'the gate and the counters on origin/main read the re-plan from a body line (the prefix re-plan: appears in both)'
    command: 'for f in scripts/require-crit-review.py scripts/regime-counters.sh; do git show origin/main:$f | /usr/bin/grep -c "re-plan: "; done | tr "\n" " " | sed "s/ $//"'
    output: |-
      1 2
  - claim: the record block on origin/main carries no replans key
    command: git show origin/main:scripts/orchestrator/acceptance-front-matter.py | /usr/bin/grep -c "replans" || true
    output: |-
      0
  - claim: 'the existing tests read the re-plan from a body line: the count of re-plan: lines per test module on origin/main (the lines item 3 migrates or removes)'
    command: 'git grep -c "re-plan: " origin/main -- tests/unit/test_require_crit_review.py tests/unit/test_regime_counters.py | sed "s#^origin/main:##" | tr "\n" " " | sed "s/ $//"'
    output: |-
      tests/unit/test_regime_counters.py:7 tests/unit/test_require_crit_review.py:4
  - claim: 'four acceptance records on origin/main carry a re-plan: body line that the orchestrator migrates after the merge'
    command: 'git grep -lE "^re-plan: " origin/main -- .orchestration/acceptance | wc -l | tr -d " "'
    output: |-
      4
  - claim: the gate on origin/main keys audit finding ids on HEAD alone (one line), the reason an inherited audit needs the first-line marker
    command: git grep -cF 'f"audit:{head[:7]}:{n}"' origin/main -- scripts/require-crit-review.py | sed "s#^origin/main:##"
    output: |-
      scripts/require-crit-review.py:1
---

# AGMSG-TASK dotfiles-T129-audit-inherit-replan-json-a01 — an update-branch-only head inherits its audit, and the S1 re-plan becomes structured JSON read by every tool (plan 023 PR F, C-61 rules 3 and 6; harness-independent)

Written 2026-10-17 by the orchestrator seat as plan 023's PR F1, the harness-independent half of the day's corrections: the chain re-audited heads whose only change was the merge of main (#374 chain 8, #379 chain 2), and the re-plan line was parsed as prose by two tools whose tokenizers and line handling disagreed (#382, class replan-word-boundary, four findings). Mechanisms, not text: the audit is inherited by patch-id; the re-plan is JSON at the record's head and every reader reads the same object.

## Goal

`scripts/orchestrator/chain-integrate.sh` inherits an audit across an update-branch-only head; the S1 re-plan lives in the record block as `replans: {<slug>: {specification, design, implementation, verification}}`, written by the front-matter writer, read by the gate and the counters, with no prose parsing left.

## Files

1. `scripts/orchestrator/chain-integrate.sh`: before the audit step, when the head is a merge commit whose first parent has a receipt `.orchestration/validation/<task>-audit-<parent sha7>.md.last.md`, whose second parent is an ancestor of `origin/main`, and whose PR diff is unchanged (`git diff-tree -p $(git merge-base origin/main <parent>) <parent> | git patch-id --stable` equals the same computation for the head), both receipt files of the parent are copied to the head's names (the file name carries the head's sha7, which `audit_name_error` requires) with a first line `inherited-from: <parent sha7>`; the audit's finding ids stay `audit:<parent sha7>:<n>` (the ledger rows the parent's chain wrote), so the gate's `swept_finding_ids` takes the sha7 from that first line when present, else from HEAD (item 2), and `AUDIT_FINDING` does not match the marker line (asserted by the test); the step logs `audit inherited from <parent sha7>`; otherwise the audit runs as today; the existing refusal of a head that already has its own receipt (line 105) stays.
2. `scripts/require-crit-review.py`: the S1 check reads the record block's `replans` object: a class at the limit passes when `replans[<slug>]` exists with the four keys `specification`, `design`, `implementation`, `verification` as non-empty strings, else the refusal `S1: <slug> at <n> rows without a re-plan (C-59)`; a `replans` value that is not an object of such objects is refused as a malformed block; the body-line parse is removed; `swept_finding_ids` reads the audit sha7 from a first line `inherited-from: <sha7>` of the summary when present, else from HEAD (item 1), the only change to S6. `scripts/orchestrator/acceptance-front-matter.py`: the block rewrite keeps a `replans` object it finds (validated to the same shape, else exit 2 naming the key) and writes `replans: {}` when absent. `scripts/regime-counters.sh`: the S1 line's `re-plan=present|missing` reads `$rec.rec.replans[<slug>]` with the four keys non-empty (jq), the body scan removed.
3. Tests: `test_integrate_inherits_the_audit_across_an_update_branch_only_head` (a temporary repository with real git: P is the audited PR head with stub receipt files, M a commit that moves main; the positive head is `git merge` of M into P's branch with no other change: both receipt files appear under the head's sha7 with the inherited-from first line and the stub orch-audit.sh records no call; the negative head is a merge commit with the same two parents whose tree also changes a PR-side file (`git merge --no-commit`, an edit, `git commit`), so its first parent still carries the receipt and only the patch-id differs: the stub records one call and no inherited file exists; the test asserts the two patch-ids equal in the first case and differ in the second), `test_s6_reads_an_inherited_audit_s_ids_under_the_parent_sha7` (a summary whose first line is the marker and whose body has two findings: ledger rows `audit:<parent sha7>:1` and `:2` pass S6, rows under the head's sha7 alone are refused as missing, and the marker line is not counted as a finding), `test_s1_replan_is_read_from_the_record_block_json` (three rows of one class with the object present passes, absent or missing one key refuses, a non-object replans is a malformed block), `test_s1_replan_token_comes_from_the_record_block_json` (the counters print present with the object, missing without, and a body line alone no longer counts), `test_front_matter_keeps_and_validates_the_replans_object` (kept through a rewrite, written empty when absent, exit 2 on a malformed one); The existing tests that read the body line change exactly as follows (premise 4 counts the lines): in `tests/unit/test_require_crit_review.py` the write_record helper (line 428 on origin/main) writes the object instead of the line; `test_s1_class_at_three_without_a_replan_line_is_refused`, `test_s1_class_at_three_with_all_replan_words_is_accepted` and `test_s1_class_at_three_with_a_missing_replan_word_is_refused` (lines 1326, 1337, 1353) move to the object (absent, complete, one key missing) and are renamed `_replans_object`/`_the_four_keys`/`_a_missing_key`; `test_s1_replan_words_are_ascii_letter_runs` (line 1368) is removed, not migrated: the object has no words to tokenise; in `tests/unit/test_regime_counters.py` `test_s1_reports_replan_present_for_the_class` (line 488) and `test_s1_reports_replan_missing_without_a_complete_matching_line` (line 497, renamed `_without_the_four_keys`) move to the object, `test_s1_replan_words_are_ascii_letter_runs` (line 515) is removed, and the fixture line of `test_s1_excludes_advisory_p2_at_three_rows` (line 522) becomes the object; the fixture `tests/fixtures/gate-evidence/acceptance-s6-present.md` moves its line into its block. No other existing test changes.

## Out of scope

The hcom-based counters of plan 023 PR C (the bus read stays agmsg here); the lints (PR F2); the AGENTS.md Audit section and orch-audit.sh (PR B's omp auditor and PR F2); chain-finish.sh (PR #378); the four acceptance records on origin/main whose body carries a `re-plan:` line (premise 5): the orchestrator moves each line into its block's `replans` object at the boundary after this PR merges (evidence-sync bookkeeping), so until then the counters report `re-plan=missing` for those classes, which the RESULT names as the known gap.

## Check

`uv run python -m unittest tests/unit/test_chain_glue.py tests/unit/test_require_crit_review.py tests/unit/test_regime_counters.py tests/unit/test_orchestrator_tools.py -v` green, pasted in the validation file with `shellcheck scripts/orchestrator/chain-integrate.sh scripts/regime-counters.sh` and `git diff --numstat origin/main...HEAD`: at most 200 changed lines (added plus deleted) outside `tests/` and outside `.orchestration/` (plan 021 step 7.2) and 1000 added lines under `tests/` (INV-2).

## Completion

One PR from a fresh branch off `origin/main` (no other merge is a precondition). The PR is ready for the orchestrator's integration when the ruleset's required checks are green, the Bot's review of the final head is in (at PR open, and once more on `@codex review` after a P0/P1 fix round: plan 020 step 2), every Bot thread is replied to and resolved by the orchestrator with its disposition, the validation file carries the Check's outputs, and the RESULT names every P0/P1 thread with `fixed:<sha>` and every P2 thread with the disposition the worker proposes; the orchestrator's audit of the final head is dispositioned finding by finding before the gate, and a P0/P1 it leaves is the operator's decision. The Bot's P0 and P1 get at most one fix round, worker-side before the RESULT, each named `fixed:<sha>` in the RESULT; a P0 or P1 that survives the round is listed as `open:<thread id>` with `bot_rounds=2` (the Bot's review at PR open and its re-review after the fix round), stops the PR and goes to the operator as a decision; a P2 of the Bot's first review on this PR's own change whose fix stays within `allowed_files` and is small (one flag or a few lines plus one test) is fixed in a revise round the orchestrator sends with a `check=` while INV-6's counts allow it (C-50; every fix round, before or after the first RESULT, counts toward INV-6's cap of two, C-61); the third finding of one class on this PR stops the rounds until the orchestrator's `re-plan:` line (C-59); a later review's P2 and every P3 are advisory (C-61), as is any other P2, owned by `dotfiles-T129-audit-inherit-replan-json-followup-a01`, which the orchestrator writes when the first advisory P2 appears, before the PR's dispositions (C-51), and recorded under `## Owned by dotfiles-T129-audit-inherit-replan-json-followup-a01` in this task's acceptance record. The orchestrator integrates (local review once per head, sweep, audit, gate) and merges with `gh pr merge --squash --match-head-commit <audited head>`. The RESULT names head, base, branch, files, every Bot thread with its disposition, the test names, the caps, `task_copy=<sha256 of .orchestration/dotfiles-T129-audit-inherit-replan-json-a01/task.md>` and the evidence paths.

## Change (round 2, 2026-10-17T10:12:50Z)

The Codex half's round 1 (three P2): an inherited audit's finding ids stay under the parent's sha7 and the gate's `swept_finding_ids` reads the first-line marker (items 1 and 2, the new S6 test, premise 6); the negative case of the inheritance test is a merge commit with the same two parents and a changed tree, so only the patch-id differs, and the mutant sentence is gone (item 3); the existing tests that change are listed one by one with their origin/main line numbers, the ASCII-letter-run tests removed rather than migrated (item 3, premise 4, the two test rows); the four records on main with a body line are the orchestrator's migration after the merge (Out of scope, premise 5).

## Checks (pasted by the orchestrator before each send)

```
dotfiles-T129-audit-inherit-replan-json-a01.md: OK
premise 1: OK
premise 2: OK
premise 3: OK
premise 4: OK
premise 5: OK
premise 6: OK
masked 0 match(es) in .orchestration/tasks/dotfiles-T129-audit-inherit-replan-json-a01.md
```
