---
format: 2
task_id: dotfiles-T128-task-checkers-a01
kind: code
security: false
design_review:
  receipt: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round22.md
  design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md
allowed_files:
  - scripts/orchestrator/task-consistency-check.py
  - scripts/orchestrator/ledger-check.py
  - scripts/orchestrator/orch-audit.sh
  - tests/unit/test_task_checkers.py
  - tests/unit/test_orchestrator_tools.py
  - tests/unit/test_agmsg_orchestration_docs.py
  - tests/fixtures/lessons/**
  - home/dot_agents/skills/agmsg-orchestration/SKILL.md
  - tests/fixtures/regime/invariants.md
  - .orchestration/dotfiles-T128-task-checkers-a01/**
after: [dotfiles-T128-orchestrator-tools-a05]
threat_table:
  - control: the PR adds scripts/orchestrator/task-consistency-check.py, the pre-dispatch and acceptance check of a format-2 task file (reads task files and the design file under --root, probes origin/main with git for C8 to C10, writes nothing); this row covers the checks the ten historical files reach (C2, C3, C4, C6, C7)
    disposition: "closed: tests/unit/test_task_checkers.py::test_task_consistency_check_detects_the_ten_historical_files"
  - control: scripts/orchestrator/task-consistency-check.py, the checks the ten historical files do not reach (C1, C5, C7b, C8, C9, C10) (amendment 2, Bot thread 4266930643, where one test did not close the whole checker)
    disposition: "closed: tests/unit/test_task_checkers.py::test_task_consistency_check_reaches_every_other_check"
  - control: scripts/orchestrator/task-consistency-check.py, the pass path (a complete task file prints OK and exits 0) (amendment 2, the same thread)
    disposition: "closed: tests/unit/test_task_checkers.py::test_task_consistency_check_passes_a_complete_task_file"
  - control: scripts/orchestrator/task-consistency-check.py, C4's path-boundary rule (amendment 2, Bot thread 4266930635)
    disposition: "closed: tests/unit/test_task_checkers.py::test_task_consistency_check_c4_names_an_entry_only_at_a_path_boundary"
  - control: the PR adds scripts/orchestrator/ledger-check.py, the pre-audit ledger check (reads the acceptance record, the sweep JSON with the standard library's json and the audit .last.md files; writes nothing)
    disposition: "closed: tests/unit/test_task_checkers.py::test_ledger_check_reports_the_gaps_of_the_pre_fix_record"
  - control: scripts/orchestrator/ledger-check.py, the two alignments with the gate (badged Codex Bot review bodies; bulleted audit lines) (amendment 2, Bot threads 4266930617 and 4266930623)
    disposition: "closed: tests/unit/test_task_checkers.py::test_ledger_check_counts_what_the_gate_counts"
  - control: the PR edits scripts/orchestrator/orch-audit.sh (the ledger check beside it runs on every audit; --ledger-check keeps naming a tracked script as an override)
    disposition: "closed: tests/unit/test_orchestrator_tools.py::test_orch_audit_runs_the_ledger_check_by_default_and_refuses_a_gap"
  - control: the PR adds tests/unit/test_task_checkers.py, the oracle of the two checkers
    disposition: "residual: it runs the checkers as subprocesses under uv run --no-project --with pyyaml python -I with a stub git on PATH whose answers each case sets (the module pattern of the orchestrator tools tests); the audit reads each case against the table in item 4"
  - control: the PR edits tests/unit/test_orchestrator_tools.py (one added case for the orch-audit.sh default)
    disposition: "residual: one added case in the existing harness and no change to an existing case; the audit reads the diff"
  - control: the PR edits tests/unit/test_agmsg_orchestration_docs.py (the two assertions that pin the two SKILL sentences)
    disposition: "residual: the two assertions move from the landing-condition sentences to the landed ones and the superseded sentences join the stale lists; no other assertion changes"
  - control: the PR adds tests/fixtures/lessons/** (a data wildcard, one row), the front matter of the ten historical task files in one file, and the pre-fix record triple
    disposition: "residual: data read by the tests only, copied from origin/main without body text, the sweep JSON on one line, none of it executed; no home path (premise 4); the .txt names keep prettier (which checks every tracked *.md) off the copies"
  - control: the PR edits home/dot_agents/skills/agmsg-orchestration/SKILL.md, sentence one of item 6 (line 73 of origin/main 7d58d6cd, the amendment rule's landing-condition form that names plan 007 T704)
    disposition: "closed: tests/unit/test_agmsg_orchestration_docs.py::test_rule_changes_travel_as_task_amendments"
  - control: the PR edits home/dot_agents/skills/agmsg-orchestration/SKILL.md, sentence two of item 6 (line 71 of origin/main 7d58d6cd, the row-unit bullet's last clause that names plan 007 T704); no third sentence changes
    disposition: "closed: tests/unit/test_agmsg_orchestration_docs.py::test_threat_table_rows_have_a_fixed_unit"
  - control: the PR edits tests/fixtures/regime/invariants.md, the whole-section fixture of the SKILL invariants that test_regime_rule_sections_are_pinned_whole compares byte for byte, in the same two sentences as item 6 and nothing else (amendment 1, the worker's question of 04:18Z)
    disposition: "residual: a data fixture read by the tests only; its diff is the two sentences of item 6 verbatim (the audit compares the fixture diff with the SKILL diff); no other line changes"
  - control: the task-file copy on the branch (.orchestration/dotfiles-T128-task-checkers-a01/task.md)
    disposition: "residual: byte-identical to the dispatched file (its sha256 is in the TASK line); the orchestrator compares at acceptance"
  - control: the branch evidence records under .orchestration/dotfiles-T128-task-checkers-a01/ (report.md, validation.md, sandbox.md, learning.md)
    disposition: "residual: prose and pasted command output; the sandbox record lists every permission-gated command; the audit reads them"
  - control: "task metadata (the front matter of the task copy: kind, allowed_files, threat_table, premises)"
    disposition: "residual: read with PyYAML by the task-consistency check C1 to C10 and C7b before dispatch and at acceptance; a changed field fails the byte comparison above"
  - control: metadata separators (the --- lines that bound the front matter of the task copy and of every evidence record)
    disposition: "residual: PyYAML splits on the first document only and the byte comparison covers the whole file"
  - control: in-process effects
    disposition: "residual: nothing is imported into another process; the tests run both checkers as subprocesses and import only the standard library"
  - control: workflow and interpreter or environment inputs
    disposition: "residual: no workflow or interpreter file is in allowed_files; the checkers resolve git and the interpreter `python` under `uv run --no-project --with pyyaml`, a closed list the tests stub (git) or pin (uv); the audit replays the list from the diff"
  - control: new or renamed scripts
    disposition: "residual: the two new scripts are under scripts/orchestrator/, named in allowed_files and listed in the RESULT; any other new or renamed script is an undeclared change the audit fails"
  - control: orchestrator effect merge
    disposition: "residual: merge only through gh pr merge --squash --match-head-commit <audited head> after the gate (Orchestrator Playbook step 10.5); never a local merge or a push to main"
  - control: orchestrator effect update-branch
    disposition: "residual: gh pr update-branch moves the head, so CI, the sweep and the audit run again on the new head before any gate (Orchestrator Playbook step 10)"
  - control: orchestrator effect forced worker removal
    disposition: "residual: none planned; herdr-agents --remove-worker refuses a dirty worktree without --force, and a forced removal is recorded in the acceptance record with the uncommitted state it discarded"
premises:
  - claim: "the input task-consistency check fails each of the ten historical task files plan 007 line 28 names (format-2 files dispatched before the row unit, the evidence-directory rule and the round-22 receipt), on the checks the output lists; these ten are the fixtures of item 5a"
    command: "for t in process-rules-a01 process-rules-a02 process-rules-a03 process-rules-a04 process-rules-a05 process-rules-a06 regime-counters-a01 regime-counters-a02 ci-skip-orchestration-a01 ci-skip-orchestration-a02; do uv run --no-project --with pyyaml python -I .orchestration/tasks/dotfiles-T128-task-checkers-a01-input/task-consistency-check.py .orchestration/tasks/dotfiles-T128-$t.md 2>&1 | awk 'NR==1{printf \"%s\", $0; next} {match($0, /C[0-9]+b?/); printf \" %s\", substr($0, RSTART, RLENGTH)} END{print \"\"}'; done"
    output: |-
      dotfiles-T128-process-rules-a01.md: FAIL C2 C6
      dotfiles-T128-process-rules-a02.md: FAIL C2 C4 C6 C7 C7 C7 C7 C7 C7 C7 C7
      dotfiles-T128-process-rules-a03.md: FAIL C2 C4 C6 C7 C7 C7 C7 C7 C7 C7 C7
      dotfiles-T128-process-rules-a04.md: FAIL C2 C4 C6 C7 C7 C7 C7 C7 C7 C7 C7
      dotfiles-T128-process-rules-a05.md: FAIL C4 C4 C4 C6 C7 C7 C7 C7 C7 C7 C7 C7
      dotfiles-T128-process-rules-a06.md: FAIL C4 C4 C6 C7 C7 C7 C7 C7 C7 C7 C7
      dotfiles-T128-regime-counters-a01.md: FAIL C2 C4 C4 C4 C6 C7 C7 C7 C7 C7 C7 C7 C7
      dotfiles-T128-regime-counters-a02.md: FAIL C2 C3 C3 C4 C4 C6 C7 C7 C7 C7 C7 C7 C7 C7
      dotfiles-T128-ci-skip-orchestration-a01.md: FAIL C2 C4 C4 C4 C6 C7 C7 C7 C7 C7 C7 C7 C7
      dotfiles-T128-ci-skip-orchestration-a02.md: FAIL C2 C3 C3 C4 C4 C4 C6 C7 C7 C7 C7 C7 C7 C7 C7
  - claim: "the input ledger check fails the pre-fix acceptance record of dotfiles-T128-process-rules-a05 (plan 007 T704: 'the 31-line pre-fix a05 record') against its sweep and its audit: no ledger row for any of the 36 findings; this triple is the fixture of item 5b"
    command: "out=$(uv run --no-project --with pyyaml python -I .orchestration/tasks/dotfiles-T128-task-checkers-a01-input/ledger-check.py .orchestration/acceptance/dotfiles-T128-process-rules-a05.md .orchestration/validation/dotfiles-T128-process-rules-a05-pr-feedback.json .orchestration/validation/dotfiles-T128-process-rules-a05-audit-4af8939.md.last.md); rc=$?; printf '%s\\n' \"$out\" | awk 'NR==1 || /^GAP audit/'; echo \"exit $rc\""
    output: |-
      ledger rows 0; findings 36; gaps 36
      GAP audit:4af8939:1
      GAP audit:4af8939:2
      GAP audit:4af8939:3
      exit 1
  - claim: "the record on origin/main is still the 31-line pre-fix version (b67ea752), so the fixture is a copy of the current file"
    command: "git show b67ea752:.orchestration/acceptance/dotfiles-T128-process-rules-a05.md | wc -l | tr -d ' '; git diff --quiet b67ea752 origin/main -- .orchestration/acceptance/dotfiles-T128-process-rules-a05.md && echo same"
    output: |-
      31
      same
  - claim: "fifteen format-2 task files pass the input check today (the fourteen code tasks dispatched under the current regime and one docs task); one of them is the pass oracle of item 4, and the replay count in the Check section starts from this number"
    command: "for t in aws-cli-macos-a01 gate-evidence-a01 gate-evidence-a02 gate-evidence-a03 gate-evidence-a04 gate-evidence-followup-a01 homebrew-attestation-token-a01 orchestrator-tools-a01 orchestrator-tools-a02 orchestrator-tools-a03 orchestrator-tools-a04 orchestrator-tools-a05 orchestrator-tools-followup-a01 playbook-rules-followup-a01 update-bootstrap-canonical-a01; do uv run --no-project --with pyyaml python -I .orchestration/tasks/dotfiles-T128-task-checkers-a01-input/task-consistency-check.py .orchestration/tasks/dotfiles-T128-$t.md 2>&1 | head -1; done | grep -c ': OK$'"
    output: |-
      15
  - claim: "the fixture sources carry no home path"
    command: "cat .orchestration/tasks/dotfiles-T128-{process-rules-a01,process-rules-a02,process-rules-a03,process-rules-a04,process-rules-a05,process-rules-a06,regime-counters-a01,regime-counters-a02,ci-skip-orchestration-a01,ci-skip-orchestration-a02}.md .orchestration/acceptance/dotfiles-T128-process-rules-a05.md .orchestration/validation/dotfiles-T128-process-rules-a05-pr-feedback.json .orchestration/validation/dotfiles-T128-process-rules-a05-audit-4af8939.md.last.md | grep -c '/Users/'"
    output: |-
      0
---

# AGMSG-TASK dotfiles-T128-task-checkers-a01 — plan 007 T704: the two checkers land in scripts/orchestrator/ (plan 021 step 6.2, the first task in the step-7 short form)

Drafted 2026-10-14 by the orchestrator seat (the bus time of its TASK line is the dispatch time). The inputs are the two scratchpad scripts as they ran on 2026-10-14, attached under `.orchestration/tasks/dotfiles-T128-task-checkers-a01-input/` (sha256 `fdab23e0f690f280a7e889a8c38e9ae526a29d88ff590981e50e285452b94df8` task-consistency-check.py, `7f2395011075fe471929c50f86cc25eec9dadb2e8ea5174360deab540954de61` ledger-check.py); they define what each check means, and nothing here changes a meaning or adds one. Dispatch follows the merge of PR #350 (`after:`); the branch starts fresh from `origin/main`. Keep the attached inputs untouched.

## Goal

Land the two checkers with their tests so that the task-consistency check runs before every dispatch and at acceptance and the ledger check runs in every audit, and point the two SKILL sentences that name plan 007 T704 as their landing condition at the landed script.

## Files

1. `scripts/orchestrator/task-consistency-check.py [--root <repo>] <task.md>...`: the input's C1 to C10 and C7b, unchanged in meaning except one alignment (amendment 2, Bot thread 4266930635): C4 counts an `allowed_files` entry as named by a row only when the entry's prefix is followed in the control text by the end, a space, a slash, a quote, a parenthesis, a comma or a glob character, so `scripts/foo.py.bak` no longer covers `scripts/foo.py`. `--root` (default: `git -C <directory of the first file> rev-parse --show-toplevel`) is where design paths resolve (C6) and where `git` probes `origin/main` (C8 to C10). Output as the input: `<file name>: OK` or `<file name>: FAIL` followed by one `  C<n> …` line per finding; exit 1 when any file fails, 0 otherwise. Runs as `uv run --no-project --with pyyaml python -I scripts/orchestrator/task-consistency-check.py …` (PyYAML, as `scripts/orchestrator/design-keydiff.py`). English shdoc-style module docstring naming each check in one line.
2. `scripts/orchestrator/ledger-check.py <record.md> <sweep.json> <audit .last.md>...`: the input unchanged in meaning except two alignments with the gate (amendment 2, Bot threads 4266930617 and 4266930623): the Codex Bot's `review` item whose body holds a `![P<n> Badge]` token counts as a finding, keyed by its `pullrequestreview-<id>` as the gate's `swept_finding_ids()` keys it (`scripts/require-crit-review.py:858-865`; the gate counts no other item source there), and an audit line counts when it matches the gate's `AUDIT_FINDING` regex (an optional Markdown bullet and whitespace before `[P0]` to `[P3]`); ledger rows are the record's `id<TAB>class` lines, as today's records carry them beside the JSON block. Output and exit as the input. English shdoc-style module docstring.
3. `scripts/orchestrator/orch-audit.sh`: the ledger check runs on every audit from `$(dirname "$0")/ledger-check.py`; `--ledger-check <script>` keeps its meaning as an override that must name a tracked script; the refusal text and exit 3 stay.
4. `tests/unit/test_task_checkers.py` (new): each checker runs as a subprocess under `uv run --no-project --with pyyaml python -I` with a stub `git` on PATH whose answers (`cat-file -e` present or absent, `grep -q` found or not) each case sets through an environment variable, the subprocess pattern of `tests/unit/test_orchestrator_tools.py`. Cases, by name:
   - `test_task_consistency_check_detects_the_ten_historical_files`: the ten of item 5a, each written to `<tmp>/<task_id>.md`, run with `--root` the repository: the set of failing check ids per file equals the replay of the amended checker over the ten (amendment 2: C4's boundary rule may add C4 to a file; the worker pastes that replay in the validation file and, beside it, for each file whose set differs from premise 1, the row text and the `allowed_files` entry that cause the new C4, so the table is checked rather than copied; premise 1 is the pre-amendment replay).
   - `test_task_consistency_check_passes_a_complete_task_file`: a file the test writes under a temporary `--root` that holds a design file whose receipt the task points at, with the eight non-path rows, one row per allowed_files entry and its own evidence directory, the stub answering found: `OK` (hermetic; the live task files are the replay in the Check section).
   - `test_task_consistency_check_reaches_every_other_check`: six files the test writes from strings, one per check the ten do not reach, each at most 20 lines, and the named check appears among that file's failures: C1 (task_id differs from the file name), C5 (a residual that binds a predecessor's hash), C7b (one row naming two allowed_files entries), C8 (a code task whose body names a new `*_EVIDENCE` input without a row), C9 (a docs task quoting a sentence that names an absent scripts/ path with no landing clause), C10 (a docs task quoting a sentence that names a present script beside a backticked literal the stub reports missing).
   - `test_ledger_check_reports_the_gaps_of_the_pre_fix_record`: the triple of item 5b: first line `ledger rows 0; findings 36; gaps 36`, 36 `GAP` lines, exit 1 (the a05 fixtures hold no badged review body and no bulleted audit line, so the two alignments leave this count).
   - `test_ledger_check_counts_what_the_gate_counts`: a sweep the test writes with one badged Codex Bot `review` body (keyed `pullrequestreview-<id>`) and an audit text with one bulleted `- [P1]` line: `findings 2`, both as `GAP` when the record lacks them (amendment 2).
   - `test_task_consistency_check_c4_names_an_entry_only_at_a_path_boundary`: a row naming only `scripts/foo.py.bak` leaves the entry `scripts/foo.py` uncovered (C4 fails), and the same entry covers it when followed by the end of the control text, a slash, a parenthesis, a space, a quote, a comma or a glob character, one case each (amendment 2).
   - `test_ledger_check_passes_a_complete_record`: a record the test writes with one tab row per id of a small sweep and audit: first line `ledger rows <n>; findings <n>; gaps 0`, exit 0; the same record with one row removed: one `GAP` line, exit 1.
   - in `tests/unit/test_orchestrator_tools.py`: `test_orch_audit_runs_the_ledger_check_by_default_and_refuses_a_gap`: with no `--ledger-check`, a record missing one id makes orch-audit.sh exit 3 before codex runs.
   - in `tests/unit/test_agmsg_orchestration_docs.py`, two existing tests whose assertions move to the new sentences of item 6: `test_rule_changes_travel_as_task_amendments` (the line-73 sentence) and `test_threat_table_rows_have_a_fixed_unit` (the line-71 clause); each superseded sentence joins that test's stale list.
5. `tests/fixtures/lessons/`, four files (prettier checks every tracked `*.md`, so the copies carry `.txt` names and stay byte-identical):
   a. `historical-front-matter.txt`: the ten front matters (first `---` to second `---`, inclusive, nothing else) of `dotfiles-T128-process-rules-a01` to `-a06`, `dotfiles-T128-regime-counters-a01`, `-a02`, `dotfiles-T128-ci-skip-orchestration-a01`, `-a02` from `origin/main`, each preceded by a line `# <task_id>`; the test splits on those lines.
   b. the pre-fix record triple: `dotfiles-T128-process-rules-a05.record.txt` (the acceptance record, premise 3), `dotfiles-T128-process-rules-a05-pr-feedback.json` written on one line (`json.dumps(obj, separators=(",", ":"))`: the same object), `dotfiles-T128-process-rules-a05-audit-4af8939.md.last.txt` (the audit's last message; the name keeps `-audit-4af8939.md`, which the check reads the sha from).
6. `home/dot_agents/skills/agmsg-orchestration/SKILL.md`, two sentences and nothing else (line numbers of `origin/main` 7d58d6cd):
   - line 73: "checked by the task-consistency check C1 to C6 once plan 007 T704 lands it and by hand until then, confirmed by the review seat" becomes "checked by `scripts/orchestrator/task-consistency-check.py` (C1 to C10 and C7b) before dispatch and at acceptance, confirmed by the review seat";
   - line 71, the last clause: "C4 of the task-consistency check (plan 007 T704) verifies the path half once it lands, and the task-file review checks it by hand until then." becomes "C4 and C7b of `scripts/orchestrator/task-consistency-check.py` verify the path half before dispatch, and the task-file review checks the rest.";
   - the two tests that pin these sentences are the last bullet of item 4; `tests/fixtures/regime/invariants.md` (the whole-section fixture `test_regime_rule_sections_are_pinned_whole` compares) changes in the same two sentences, verbatim, in the same commit (amendment 1).

## Out of scope

T705 (`scripts/validate-task.py` absorbing C1 to C6 and the key hash), T706 (`scripts/new-successor.py`), a change to what any check means beyond the three alignments of amendment 2, fixing the historical task files, the other scratchpad scripts (plan 021 step 6.3), any fixture line beyond the two sentences, reading ledger ids from the record's JSON block (the block becomes the only ledger form with T705), any rule sentence beyond the two in item 6, and `scripts/orchestrator/dispatch.sh` calling the check itself (a later task).

## Check

One command, pasted in the validation file: `uv run python -m unittest tests/unit/test_task_checkers.py tests/unit/test_orchestrator_tools.py tests/unit/test_agmsg_orchestration_docs.py -v`. Also pasted: `shellcheck scripts/orchestrator/orch-audit.sh`; the replay `for f in $(grep -l '^format: 2' .orchestration/tasks/*.md); do uv run --no-project --with pyyaml python -I scripts/orchestrator/task-consistency-check.py "$f"; done | grep -c ': OK$'` (15 on 2026-10-14 before this task's own file, which passes, joined `.orchestration/tasks/` (premise 4); the worker reports the count it gets, never fixes it); `git diff --numstat origin/main...HEAD` with at most 200 changed lines (added plus deleted) outside `tests/` (plan 021 step 7.2; amendment 2: the three Bot alignments may take it past 200, within INV-2's 500, and the RESULT states the count) and 1000 added lines under `tests/` (INV-2); when `tests/` overflows, shorten the six strings of item 4, never item 5, and say so in the RESULT.

## Completion

One PR from a fresh branch off `origin/main` after PR #350 merges. The Bot reviews once, at PR open; its P0 and P1 get at most one fix round, worker-side before the RESULT, each named `fixed:<sha>` in the RESULT; a P0 or P1 that survives the round stops the PR and goes to the operator as a decision; P2 are advisory and owned by `dotfiles-T128-task-checkers-followup-a01`, which the orchestrator writes when the first P2 appears and lands by the next boundary before the merge. The orchestrator integrates (local review once per head, sweep, audit, gate) and merges with `gh pr merge --squash --match-head-commit <audited head>`. The RESULT names head, base, branch, files, every Bot thread with its disposition, the test names, the replay count, the caps, `task_copy=<sha256 of .orchestration/dotfiles-T128-task-checkers-a01/task.md>` and the evidence paths.

## Change of 2026-10-14 (amendment 1, after the worker's question of 04:18Z, before any push)

1. `allowed_files` gains `tests/fixtures/regime/invariants.md`: `tests/unit/test_agmsg_orchestration_docs.py::test_regime_rule_sections_are_pinned_whole` compares the SKILL's invariants section with that fixture byte for byte (its lines 8 and 10 are SKILL lines 71 and 73), so item 6's two sentences fail that test unless the fixture carries the same two sentences in the same commit.
2. One residual threat row for the fixture (C4), the sentence in item 6, and the out-of-scope list names any other fixture line. Nothing else changes; items 1 to 5 stand.

## Change of 2026-10-14 (amendment 2, after the Bot's review of PR #352 and the worker's question of 05:08Z, before the RESULT)

1. The Bot's four P1 on head 63433cf1 are fixed in the task's one round (plan 020 step 4): 4266930617 and 4266930623 (ledger-check counts the Codex Bot's badged `review` bodies, keyed `pullrequestreview-<id>`, and bulleted `[P` audit lines as the gate does), 4266930635 (C4 names an entry only at a path boundary), 4266930643 (the checker's closed row is four rows: the ten-file test for the checks the ten reach, the every-other-check test, the pass-path test and the C4-boundary test; the ledger-check alignments have their own closed row and test). The first three change what a check means by exactly that much; item 1, item 2 and the out-of-scope list say so.
2. Item 4's ten-file table is the replay of the amended checker (pasted by the worker); `test_ledger_check_counts_what_the_gate_counts` is added; the Check's 200-line practice cap yields to these fixes within INV-2's 500.
3. Nothing else changes; amendment 1 stands.
