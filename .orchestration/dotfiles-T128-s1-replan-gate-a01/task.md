---
format: 2
task_id: dotfiles-T128-s1-replan-gate-a01
kind: code
security: false
design_review:
  receipt: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round22.md
  design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md
allowed_files:
  - scripts/regime-counters.sh
  - scripts/require-crit-review.py
  - tests/unit/test_regime_counters.py
  - tests/unit/test_require_crit_review.py
  - tests/fixtures/gate-evidence/acceptance-s6-present.md
  - .orchestration/dotfiles-T128-s1-replan-gate-a01/**
after: []
threat_table:
  - control: "the PR edits scripts/regime-counters.sh in one place (the S1 line gains re-plan=present|missing read from the record, and the class advisory-p2 is filtered out of the S1 lines, both new)"
    disposition: "residual: the script reads the acceptance record as data (the JSON block's ledger rows as today, and, new, the body's re-plan: lines by exact prefix); the orchestrator's diff review and the task-level audit compare the diff against this row"
  - control: the PR edits scripts/require-crit-review.py in one place (the S1 refusal beside the S6 check)
    disposition: "residual: the gate already reads the record's ledger and searches (S6) and discards the prose; the new check keeps the body text and reads re-plan: lines by exact prefix, refusing the merge, never approving; an edit outside the check is an undeclared change the audit fails"
  - control: the PR edits tests/unit/test_regime_counters.py for the S1 cases (three new tests; the two existing S1 assertions at lines 485 and 525 gain the re-plan=missing token, nothing else of them changes)
    disposition: "residual: the tests write records and bus fixtures to a temporary directory and run the script as a subprocess; the other existing tests stay"
  - control: "the PR edits tests/unit/test_require_crit_review.py for the S1 cases (three new tests) and in the helper write_record (line 420), which gains a re-plan line in the record body for every class it writes at three or more rows, so test_s6_searches_entry_must_equal_the_recomputed_records_search (line 1349) keeps its S6 assertions; the other existing tests stay"
    disposition: "residual: the tests write a record and run the gate as a subprocess in a temporary repository (two existing gate tests load the module with importlib, unchanged)"
  - control: "the PR edits tests/fixtures/gate-evidence/acceptance-s6-present.md in one place (its body gains a re-plan line for its class at three rows, class-count-scope)"
    disposition: "residual: the shared fixture of the gate tests (guard_base writes it as the record of every test that names none); with the new refusal it must carry the line or every gate test fails; one line added, the rows unchanged"
  - control: "the re-plan: line the gate and the counters read (a line of the acceptance record the orchestrator writes)"
    disposition: "residual: matched by the exact prefix re-plan: <class> -> and the four words specification, design, implementation and verification; the class is the ledger's slug ([a-z0-9-], as S6 validates it), so no review text reaches a command; a line without the four words is missing, never a partial pass"
  - control: the task-file copy on the branch (.orchestration/dotfiles-T128-s1-replan-gate-a01/task.md)
    disposition: "residual: byte-identical to the dispatched file (its sha256 is in the TASK line); the orchestrator compares at acceptance"
  - control: the branch evidence records under .orchestration/dotfiles-T128-s1-replan-gate-a01/ (report.md, validation.md, sandbox.md, learning.md)
    disposition: "residual: prose and pasted command output; the sandbox record lists every permission-gated command; the audit reads them"
  - control: "task metadata (the front matter of the task copy: kind, allowed_files, threat_table, premises)"
    disposition: "residual: read with PyYAML by the task-consistency check C1 to C10 and C7b before dispatch and at acceptance; a changed field fails the byte comparison above"
  - control: metadata separators (the --- lines that bound the front matter of the task copy and of every evidence record)
    disposition: "residual: PyYAML splits on the first document only and the byte comparison covers the whole file"
  - control: in-process effects
    disposition: "residual: the two test modules run the scripts as subprocesses with fixtures in a temporary directory; two existing gate tests load require-crit-review.py into the test process with importlib and keep doing so; the modules import the standard library only"
  - control: workflow and interpreter or environment inputs
    disposition: "residual: no workflow or interpreter file is in allowed_files; regime-counters.sh runs jq and gh as today; the gate is run as ./scripts/require-crit-review.py under its shebang #!/usr/bin/env python3 (the Makefile's recipe, and sys.executable in the tests) and runs git through run_git and the GitHub reads the tests stub on PATH, as today; a PR checkout as cwd chooses nothing new"
  - control: new or renamed scripts
    disposition: "residual: no new or renamed script; any new or renamed script is an undeclared change the audit fails"
  - control: orchestrator effect merge
    disposition: "residual: merge only through gh pr merge --squash --match-head-commit <audited head> after the gate (Orchestrator Playbook step 10.5); never a local merge or a push to main"
  - control: orchestrator effect update-branch
    disposition: "residual: gh pr update-branch moves the head, so CI, the sweep and the audit run again on the new head before any gate (Orchestrator Playbook step 10)"
  - control: orchestrator effect forced worker removal
    disposition: "residual: none planned; herdr-agents --remove-worker refuses a dirty worktree without --force, and a forced removal is recorded in the acceptance record with the uncommitted state it discarded"
premises:
  - claim: 'regime-counters.sh on origin/main prints an S1 line per ledger class with three or more rows and nothing about a re-plan (the phrase appears 2 times: the header comment and the jq line)'
    command: 'git show origin/main:scripts/regime-counters.sh | /usr/bin/grep -c "S1: class="'
    output: |-
      2
  - claim: 'the gate on origin/main checks S6 (searches) at the class limit three and knows no re-plan line'
    command: 'git show origin/main:scripts/require-crit-review.py | /usr/bin/grep -c "S6_CLASS_LIMIT\|re-plan"'
    output: |-
      2
  - claim: 'the SKILL on origin/main names the records search as the next acceptance action at three repeats and no re-plan line yet (the rule text follows this task through the rules lineage)'
    command: 'git show origin/main:home/dot_agents/skills/agmsg-orchestration/SKILL.md | /usr/bin/grep -c "re-plan:"'
    output: |-
      0
---

# AGMSG-TASK dotfiles-T128-s1-replan-gate-a01 — the S1 stop becomes mechanical: no merge and no further round while a finding class at three rows has no re-plan line (C-59; the operator's correction of 2026-10-17)

Written 2026-10-17 by the orchestrator seat after the operator stopped PR #374's sixth single-source round of one finding class (M-20261017-04): the counters already print an `S1: class=<slug> count=<n>` line for a ledger class at three rows, and nothing acted on it. This task makes the stop mechanical in the two tools the regime runs at every acceptance action: the counters say whether the re-plan exists, and the gate refuses the merge until it does. The dispatcher's half (no revise line and no amendment line while an S1 class has no re-plan) is the row `C-59:1` of `dotfiles-T128-orchestrator-tools-followup-a04`, since `scripts/orchestrator/dispatch.sh` is in flight in PR #374.

## What to do

1. `scripts/regime-counters.sh`: the S1 line becomes `S1: class=<slug> count=<n> re-plan=present|missing source=record` (the new token before the trailing `source=`); `present` when the acceptance record's body holds a re-plan line for that class, `missing` otherwise. The re-plan line's grammar, stated once for both tools: a line of the record body (the text after the JSON block's closing `---`) beginning with the exact prefix `re-plan: <slug> -> ` whose text contains the four words `specification`, `design`, `implementation` and `verification`; `<slug>` is the ledger's class slug (`[a-z0-9-]`, as S6 validates it). New work in the script: today it reads nothing but the JSON block and groups every ledger class into S1 lines; it now scans the body for the lines and filters the class `advisory-p2` out of the S1 lines (the SKILL's counters bullet reads S1 over non-advisory rows). The two existing S1 assertions in `tests/unit/test_regime_counters.py` (lines 485 and 525) gain `re-plan=missing`, nothing else of them changes.
2. `scripts/require-crit-review.py`: beside the S6 check, for each ledger class other than `advisory-p2` with `S6_CLASS_LIMIT` or more rows the record body must hold a re-plan line of the grammar in item 1; otherwise the gate refuses with one line `S1: <slug> at <n> rows without a re-plan line (C-59)` and its usual non-zero exit. New work in the gate: it keeps the record's body text (today it parses the JSON block and discards the prose) and scans it for the lines. The shared fixture `tests/fixtures/gate-evidence/acceptance-s6-present.md` (class `class-count-scope` at three rows) gains one re-plan line in its body, and the helper `write_record` (test module line 420) writes a re-plan line for every class it puts at three or more rows (the `scope` and `absent` ledgers of `test_s6_searches_entry_must_equal_the_recomputed_records_search`, line 1349, keep their S6 assertions and pass the new check), so the existing gate tests keep passing.
3. Tests: in `tests/unit/test_regime_counters.py`, one test for `re-plan=present`, one for `re-plan=missing`, one that `advisory-p2` at three rows prints no S1 line; in `tests/unit/test_require_crit_review.py`, one test that a class at three rows without the line refuses with the S1 line, one that the line with the four words passes, one that a line missing a word refuses. Nothing else changes beyond the two assertion updates, the fixture line and the write_record helper's re-plan lines named above.

## Validation

- `uv run python -m unittest tests/unit/test_regime_counters.py tests/unit/test_require_crit_review.py -v` green in the validation file, with the six new tests named; `shellcheck scripts/regime-counters.sh`.
- `git diff --numstat origin/main...HEAD` in the validation file: at most 200 changed lines outside `tests/` and outside `.orchestration/` (plan 021 step 7.2) and 1000 added lines under `tests/` (INV-2).

## Completion

One PR from a fresh branch off `origin/main` (after PR #376 merged as f7847616; no other merge is a precondition). The PR is ready for the orchestrator's integration when the ruleset's required checks are green, the Bot's review of the final head is in (at PR open, and once more on `@codex review` after a P0/P1 fix round: plan 020 step 2), every Bot thread is replied to and resolved by the orchestrator with its disposition, the validation file carries the outputs above, and the RESULT names every P0/P1 thread with `fixed:<sha>` and every P2 thread with the disposition the worker proposes; the orchestrator's audit of the final head is dispositioned finding by finding before the gate, and a P0/P1 it leaves is the operator's decision. The Bot's P0 and P1 get at most one fix round, worker-side before the RESULT, each named `fixed:<sha>` in the RESULT; a P0 or P1 that survives the round is listed as `open:<thread id>` with `bot_rounds=2` (the Bot's review at PR open and its re-review after the fix round), stops the PR and goes to the operator as a decision; a P2 on this PR's own change whose fix stays within `allowed_files` and is small (one flag or a few lines plus one test) is fixed in a revise round the orchestrator sends with a `check=` while INV-6's counts allow it (C-50); any other P2 is advisory, owned by `dotfiles-T128-s1-replan-gate-followup-a01`, which the orchestrator writes when the first advisory P2 appears, before the PR's dispositions (C-51), and recorded under `## Owned by dotfiles-T128-s1-replan-gate-followup-a01` in this task's acceptance record. The third finding of one class on this PR stops the rounds until the orchestrator's `re-plan:` line (C-59). The orchestrator integrates (local review once per head, sweep, audit, gate) and merges with `gh pr merge --squash --match-head-commit <audited head>`. The RESULT names head, base, branch, files, every Bot thread with its disposition, the test names, the caps, `task_copy=<sha256 of .orchestration/dotfiles-T128-s1-replan-gate-a01/task.md>` and the evidence paths.

## Change (round 1, 2026-10-17T02:07:28Z)

The Codex half's round 2 (P2; its round 1 was a prompt residue, dispositioned in the acceptance record): items 1 and 2 and two threat rows said the record body was read as today; on `origin/main` the counters read only the JSON block and the gate discards the prose, so the body scan for `re-plan:` lines is new work in both and is now stated so. Nothing else changes from `580ed45a`.

## Change (round 2, 2026-10-17T02:27:45Z)

The review seat's round 1 (P1, P2, P2, P3 ×4): the two existing S1 assertions of the counters tests and the gate tests' shared fixture `acceptance-s6-present.md` (class-count-scope at three rows, no re-plan line) would fail under the new token and the new refusal, so the fixture joins `allowed_files`, the assertion updates and the fixture line are named, and "nothing else changes" is scoped; the advisory-p2 filter is stated as new work and named in the first row; the workflow row states the gate's interpreter resolution as it is (`./scripts/require-crit-review.py`, shebang `#!/usr/bin/env python3`; git through run_git; the GitHub reads); the in-process row names the two importlib tests; the grammar is stated once in item 1 with the token's position before `source=`; the Change note names the Codex round correctly; the Completion clause carries the template's S1 sentence of 2026-10-17. Nothing else changes from `813b2ec7`.

## Change (round 3, 2026-10-17T02:32:28Z)

The Codex half's round 4 (P1): `test_s6_searches_entry_must_equal_the_recomputed_records_search` builds three-row ledgers through the helper `write_record` without re-plan lines, so the new refusal would fail it; the helper now writes a re-plan line per class at the limit and the test keeps its S6 assertions; named in item 2 and the module's row. Nothing else changes from `59c898ae`.
