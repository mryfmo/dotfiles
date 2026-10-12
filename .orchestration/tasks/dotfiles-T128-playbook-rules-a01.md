---
format: 2
task_id: dotfiles-T128-playbook-rules-a01
kind: docs
security: false
reset_of: []
design_review:
  receipt: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round22.md
  design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md
allowed_files:
  - home/dot_agents/skills/agmsg-orchestration/SKILL.md
  - AGENTS.md
  - tests/unit/test_agmsg_orchestration_docs.py
  - tests/fixtures/regime/*.md
  - .orchestration/dotfiles-T128-playbook-rules-a01/**
after: []
threat_table:
  - control: the PR edits home/dot_agents/skills/agmsg-orchestration/SKILL.md, the rules Claude seats follow once it is applied
    disposition: "residual: the applied copy changes only after the merge and the operator's make update; before the merge the orchestrator's diff review and the audit from main judge every sentence, and tests/unit/test_agmsg_orchestration_docs.py pins each new sentence with a token and each changed section whole"
  - control: the PR edits AGENTS.md "Code Review Rules", which the Codex Bot reads from the PR tree, so a PR can rewrite the Bot's rules for its own review
    disposition: "residual: the Bot's review of a PR that edits its own rules is swept feedback with no gate authority (INV-7); the task-level audit runs with main's AGENTS.md as its instruction root (INV-5) and the orchestrator's review reads the diff; a change to Code Review Rules is review tier with one schema audit (INV-1)"
  - control: the PR edits tests/unit/test_agmsg_orchestration_docs.py, the module that pins its own rule sentences, so it controls the oracle as well as the text
    disposition: "residual: the orchestrator's diff review and the task-level audit from main read the test diff beside the prose diff"
  - control: the PR edits tests/fixtures/regime/*.md, the expected values of test_regime_rule_sections_are_pinned_whole, so a rule and its fixture can change together
    disposition: "residual: a fixture diff is the declared change itself (the test's message requires listing it in the RESULT, INV-12); the orchestrator's diff review and the task-level audit from main read each fixture diff beside the prose diff, and main keeps the previous fixture to compare against"
  - control: the task-file copy on the branch (.orchestration/dotfiles-T128-playbook-rules-a01/task.md)
    disposition: "residual: the copy is byte-identical to the dispatched task file (sha256 in the worker's validation file, compared by the orchestrator at acceptance)"
  - control: "task metadata (the front matter of the task copy: kind, allowed_files, threat_table, premises)"
    disposition: "residual: read with PyYAML by task-consistency-check C1 to C6 before dispatch and by the orchestrator at acceptance, never by a hand-written parser; a changed field fails the byte comparison above"
  - control: metadata separators (the --- lines that bound the front matter of the task copy and of every evidence record)
    disposition: "residual: PyYAML splits on the first document only and the byte comparison covers the whole file, so a second front matter or a moved separator fails acceptance"
  - control: the branch evidence records under .orchestration/dotfiles-T128-playbook-rules-a01/ (report.md, validation.md, sandbox.md, learning.md, autoskill.md)
    disposition: "residual: they are the worker's untrusted claims; acceptance re-checks each claim against the diff, CI and the test output, and the audit reads those sources itself"
  - control: in-process effects
    disposition: "residual: none; the declared test module reads prose and fixtures and imports no changed script"
  - control: workflow and interpreter or environment inputs
    disposition: "residual: none in allowed_files; an undeclared change to such a file is outside the task and fails at the audit (INV-12)"
  - control: new or renamed scripts
    disposition: "residual: none; allowed_files names no script path, so a new or renamed script is an undeclared change the audit fails"
  - control: orchestrator effect merge
    disposition: "residual: merge only through gh pr merge --squash --match-head-commit <audited head> after the gate (Orchestrator Playbook step 10.5); never a local merge or a push to main"
  - control: orchestrator effect update-branch
    disposition: "residual: gh pr update-branch moves the head, so CI, the sweep and the audit run again on the new head before any gate (Orchestrator Playbook step 10)"
  - control: orchestrator effect forced worker removal
    disposition: "residual: none planned; herdr-agents --remove-worker refuses a dirty worktree without --force, and a forced removal is recorded in the acceptance record with the uncommitted state it discarded"
premises:
  - claim: "the four SKILL places this task edits exist on main at these lines: the task-file-review bullet (69), the threat-table bullet (71), the counters bullet (72), Orchestrator Playbook step 6 (162)"
    command: "grep -n -E '^- A task-file review is one round|^- A task that touches a trust boundary|^- Before every acceptance action|^6\\. Send `AGMSG-TASK v1`' home/dot_agents/skills/agmsg-orchestration/SKILL.md | cut -c1-90"
    output: |-
      69:- A task-file review is one round with a fixed stop condition: no contradiction with th
      71:- A task that touches a trust boundary (anything the design tier lists, CI that decides
      72:- Before every acceptance action (revise, accept, merge) the orchestrator runs `scripts
      162:6. Send `AGMSG-TASK v1` with the exact artifact paths and `done_signal=AGMSG-RESULT`. 
  - claim: "the AGENTS.md trust-boundary review bullet this task extends begins at line 78"
    command: "grep -n 'Judge from the diff' AGENTS.md | cut -c1-60"
    output: "78:- Judge from the diff, whatever the task's metadata says,"
  - claim: "whole-section pinning compares each named section with tests/fixtures/regime/<name>.md and names the fixture to update in its failure message"
    command: "sed -n '240,252p' tests/unit/test_agmsg_orchestration_docs.py | grep -n -E 'PINNED_SECTIONS|fixtures/regime|declare the change'"
    output: |-
      2:        for name, path, outer, (start, end) in self.PINNED_SECTIONS:
      7:                fixture = ROOT / "tests/fixtures/regime" / f"{name}.md"
      11:                    f"regime rule section {name} changed: declare the change by updating "
      12:                    f"tests/fixtures/regime/{name}.md in the same commit and listing it in the RESULT",
---

# AGMSG-TASK dotfiles-T128-playbook-rules-a01 (amendment 1, 2026-10-12: Bot threads 4247933544, 4247933561, 4247933574 on PR #328 head 9b2c02a1) — the orchestrator's rules as rule text: dispatch evidence, amendments not replies, the three-repeat procedure, the threat-row unit (plan 007 T703; C-5, C-12; plan 006 B0's dead clause)

Written 2026-10-12 by the orchestrator seat under plan 007 (Phase 1, T703). Amendment 1 (worker PONG `question`, 12:27Z): the orchestrator-effects row split into three rows (F1), item 5's invariant check qualified to tasks that carry an `invariants` key (F2), item 3's search keyed on the mistake records' `classes:` field after the Bot replayed the old commands against the records (F3: `grep -rl bookkeeping corrections/` 0 files, `grep -rl sources corrections/` 15 files); the worker's head `9b2c02a1` stays and its three threads are answered by this amendment, not by replies. Review tier by INV-1 (`kind: docs`): the regime's own rule prose. Each sentence below is owned by the SKILL or AGENTS.md; plan 007 cites them, it does not restate them. The threat table names every `allowed_files` entry plus the non-path controls; `task-consistency-check.py` C1 to C6 pass on this file.

## What to do (each item is one sentence or one replacement; keep the surrounding text)

1. Orchestrator Playbook step 6 (SKILL line 162): append the dispatch-evidence sentences (C-12): "Every dispatch (TASK, ACCEPTANCE, PING) is recorded in the current acceptance record under a `dispatch:` key as the bus line `history.sh <team>` prints, with its read marker; a seat is reported as working only from such a line, and after a context compaction the open TASK list is re-derived from the bus before any status is reported. A RESULT wait past the task's expected duration ends in a bus read, then a PING, never in a longer silent wait."
2. "Review and integration invariants", after the counters bullet (line 72): a new bullet for the amendment rule (plan 007 Phase 0): "A change to a rule sentence requested of a worker travels as a task amendment (hashed, checked by task-consistency-check C1 to C6, confirmed by the review seat), never as a PONG answer."
3. Same section, after that bullet: the three-repeat procedure (plan 007 S6): "When a finding class reaches three on one artifact (the record's ledger) or `scripts/regime-counters.sh` prints an S1 candidate, the next acceptance action is a search pasted into the record under a `search:` line naming the class: `grep -l 'classes:.*<class slug>' .orchestration/learning/mistakes/` (each mistake record names its ledger classes; its `corrections:` ids lead through `.orchestration/learning/index.yaml` to the corrections) and `uv run --no-project .claude/hooks/contextdb_cli.py memory search <class slug>`. A matching correction with `status: landed` is applied as written; a `pending` one lands first; no match means a new mistake record carrying the class and a new correction are researched from official sources and recorded before any dispatch. The gate refuses the action without the paste (`dotfiles-T128-gate-evidence-a01`), and every `not-applicable` disposition carries `; evidence=<command>` with the output pasted in the record."
4. The threat-table bullet (line 71): after the list of things the PR or the orchestrator controls, add the row unit: "The row unit is one row per `allowed_files` entry, one row per listed control that is not a path (task metadata, workflow and interpreter or environment inputs, in-process effects, new or renamed scripts, metadata separators), carried by the declared test module's row where that is where the control acts, and one row per orchestrator effect from the fixed list (forced removal, merge, update-branch); task-consistency-check C4 verifies the path half before dispatch." In AGENTS.md line 78's bullet, after "report a missing table or a missing row;", insert: "a row's unit is the SKILL threat-table bullet's (one per `allowed_files` entry, one per non-path control, one per orchestrator effect), so review a missing row at that unit;".
5. The task-file-review bullet (line 69): replace "one invariant check (a `-contract-a01` id maps to its implementing entry)" with "one invariant check (for a task that carries an `invariants` key: the task id maps to its `implementing_tasks` entry and the invariant ids match; a task without the key needs no entry)", following design v20 (plan 006 B0), which removed contract PRs; the token test at `tests/unit/test_agmsg_orchestration_docs.py` line 278 that asserts the old clause becomes the new clause's token in the same commit.
6. Orchestrator Playbook step 10.4 (line 170): the gate command gains `ACCEPTANCE_EVIDENCE=<acceptance record>` beside `PR_FEEDBACK_EVIDENCE` (required in PR mode once `dotfiles-T128-gate-evidence-a01` lands; the record whose ledger and `search:` line the gate reads); any existing token test that asserts that sentence is updated to the new text in the same commit.
7. Tests: one token test per new sentence (items 1 to 6) in the style of `test_counters_run_before_every_acceptance_action`; register Orchestrator Playbook step 6 in `PINNED_SECTIONS` with a new fixture `tests/fixtures/regime/orchestrator-step-6.md`; update `tests/fixtures/regime/invariants.md` and `code-review-orchestration.md` for the changed sections, and list every fixture change in the RESULT (INV-12's declared change).
8. Nothing else changes: not the Worker Playbook, not the counters bullet's text, not the message contract.

## Validation

- `uv run --no-project python -m unittest tests/unit/test_agmsg_orchestration_docs.py -v` output in the validation file, with the new tests named and the fixture list.
- `git diff --numstat origin/main...HEAD` in the validation file (INV-2 caps: at most 15 changed files outside `.orchestration/`, 500 added lines outside `tests/`, 1000 under `tests/`).

## Completion

The PR is ready for the orchestrator's integration when CI is green, the Bot wait of Worker Playbook step 15 is done, the validation file carries the outputs above, and the RESULT names every unresolved Bot thread with `fixed:<sha>` or a proposed `not-applicable:<reason>; evidence=<command>`. Branch `regime/playbook-rules`, draft PR from `origin/main`, `kind: docs`.
