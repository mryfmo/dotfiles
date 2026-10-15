---
format: 2
task_id: dotfiles-T128-playbook-rules-followup-a01
kind: docs
security: false
design_review:
  receipt: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round22.md
  design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md
allowed_files:
  - home/dot_agents/skills/agmsg-orchestration/SKILL.md
  - AGENTS.md
  - tests/unit/test_agmsg_orchestration_docs.py
  - tests/fixtures/regime/*.md
  - .orchestration/dotfiles-T128-playbook-rules-followup-a01/**
after: [dotfiles-T128-playbook-rules-a04]
threat_table:
  - control: the PR edits home/dot_agents/skills/agmsg-orchestration/SKILL.md, the rules Claude seats follow once it is applied
    disposition: "residual: the applied copy changes only after the merge and the operator's make update; before the merge the orchestrator's diff review and the audit from main judge every sentence, and tests/unit/test_agmsg_orchestration_docs.py pins each new sentence with a token and each changed section whole"
  - control: the PR edits AGENTS.md "Code Review Rules", which the Codex Bot reads from the PR tree, so a PR can rewrite the Bot's rules for its own review
    disposition: "residual: the Bot's review of a PR that edits its own rules is swept feedback with no gate authority (INV-7); the task-level audit runs with main's AGENTS.md as its instruction root (INV-5) and the orchestrator's review reads the diff; a change to Code Review Rules is review tier with one schema audit (INV-1)"
  - control: the PR edits tests/unit/test_agmsg_orchestration_docs.py, the module that pins its own rule sentences, so it controls the oracle as well as the text
    disposition: "residual: the orchestrator's diff review and the task-level audit from main read the test diff beside the prose diff"
  - control: the PR edits tests/fixtures/regime/*.md, the expected values of test_regime_rule_sections_are_pinned_whole, so a rule and its fixture can change together
    disposition: "residual: a fixture diff is the declared change itself (the test's message requires listing it in the RESULT, INV-12); the orchestrator's diff review and the task-level audit from main read each fixture diff beside the prose diff, and main keeps the previous fixture to compare against"
  - control: the task-file copy on the branch (.orchestration/dotfiles-T128-playbook-rules-followup-a01/task.md)
    disposition: "residual: the copy is byte-identical to the dispatched task file (sha256 in the worker's validation file, compared by the orchestrator at acceptance); the pair's receipts name this file's hash"
  - control: "task metadata (the front matter of the task copy: kind, allowed_files, threat_table, premises)"
    disposition: "residual: read with PyYAML by task-consistency-check C1 to C6 before dispatch and by the orchestrator at acceptance, never by a hand-written parser; a changed field fails the byte comparison above"
  - control: metadata separators (the --- lines that bound the front matter of the task copy and of every evidence record)
    disposition: "residual: PyYAML splits on the first document only and the byte comparison covers the whole file, so a second front matter or a moved separator fails acceptance"
  - control: the branch evidence records under .orchestration/dotfiles-T128-playbook-rules-followup-a01/ (report.md, validation.md, sandbox.md, learning.md, autoskill.md)
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
  - claim: "the a04 task names this task as the owner of the residual findings of PR #328's final head"
    command: "grep -c 'owned by dotfiles-T128-playbook-rules-followup-a01' .orchestration/tasks/dotfiles-T128-playbook-rules-a04.md"
    output: "1"
  - claim: "the a04 acceptance record is on origin/main (the owned section is appended to it by the boundary after a04's merge, before this task dispatches)"
    command: "git cat-file -e origin/main:.orchestration/acceptance/dotfiles-T128-playbook-rules-a04.md && echo present"
    output: "present"

---

# AGMSG-TASK dotfiles-T128-playbook-rules-followup-a01 — the residual findings of PR #328's final head (the owner task of T703 a04's Completion clause, plan 017; C-32's owner-first pattern)

Written 2026-10-13 10:19Z by the orchestrator seat, pair-reviewed before dispatch. T703's a04 (PR #328) gets one revise round for the findings of its amendment-1 head (the Bot's and the C-32 local review's); a P2 finding on the final head that round did not fix is dispositioned on PR #328 as `not-applicable:advisory P2 owned by dotfiles-T128-playbook-rules-followup-a01; evidence=git show origin/main:.orchestration/tasks/dotfiles-T128-playbook-rules-followup-a01.md | grep -n 'item 1'` (the gate's full form once PR #329 lands) and recorded as a row of `.orchestration/acceptance/dotfiles-T128-playbook-rules-a04.md`'s ledger. This task fixes exactly those rows in the rule text after a04 merges; it exists on `main` before the findings do, so no boundary commit is needed between a04's final head and its merge. Review tier by INV-1 (`kind: docs`; the same files as a04). The threat table names every `allowed_files` entry plus the non-path controls; `task-consistency-check.py` C1 to C10 and C7b pass on this file.

## What to do

1. The owned rows: the `<id>\t<class>` rows under the heading `## Owned by dotfiles-T128-playbook-rules-followup-a01` in `.orchestration/acceptance/dotfiles-T128-playbook-rules-a04.md` as read from `origin/main` (Codex Bot P2 threads and local-review findings on a04's final head after its one revise round, each dispositioned on PR #328 as `not-applicable:advisory P2 owned by dotfiles-T128-playbook-rules-followup-a01; evidence=git show origin/main:.orchestration/tasks/dotfiles-T128-playbook-rules-followup-a01.md | grep -n 'item 1'` (the gate's full form once PR #329 lands)). That section is this item's whole definition, closed at a04's acceptance and landed by the boundary after a04's merge; this task dispatches only after that boundary (the dispatch line names the record's hash); a finding outside the section is not owned here, and a missing or empty section at dispatch makes this task a no-op that report.md states (the section is created at the lineage's acceptance, so it does not exist before that). For each row: the rule sentence it names is corrected against the design on `main` (`.orchestration/tasks/dotfiles-T128-regime-v3-a01.md`, read from main) and the thread's text, with one token test per changed sentence in `tests/unit/test_agmsg_orchestration_docs.py` (and the fixture under `tests/fixtures/regime/` when the pinned section changes), in the style of a04's item 7; the RESULT lists each row with `fixed:<sha>`. The `procedure-migration` row (`audit:71eb920:1`) covers every sentence in this task's allowed files that still states the retired gate input (`AUDIT_DISPOSITIONS`, or the `audit-finding:` prose as what the gate reads), since the gate on main reads the acceptance record's JSON `audit_findings` (`{n, reason, evidence}`, PR #329): the step 10 lines the audit named, the task-level audit bullet of the SKILL, the AGENTS.md gate sentence, and the pinned fixture `tests/fixtures/regime/invariants.md` where `tests/unit/test_agmsg_orchestration_docs.py` holds them (the lines on `origin/main` at 26909ee4 and after are pasted in the Change section below); each changed sentence gets its token test as above (amendment 1, the worker's question of 06:50Z).
2. Nothing else changes: not the Worker Playbook, not the message contract, not any sentence outside the owned rows.

## Validation

- `uv run --no-project python -m unittest tests/unit/test_agmsg_orchestration_docs.py -v` output in the validation file, with the changed tests named and the fixture list.
- `git diff --numstat origin/main...HEAD` in the validation file (INV-2 caps: at most 15 changed files outside `.orchestration/`, 500 added lines outside `tests/`, 1000 under `tests/`).

## Completion

The PR is ready for the orchestrator's integration when CI is green, the Bot wait of Worker Playbook step 15 is done, the validation file carries the outputs above, and the RESULT names every unresolved Bot thread with `fixed:<sha>` or a proposed `not-applicable:<reason>; evidence=<command>`. A fresh branch `regime/playbook-rules-followup` from `origin/main` after a04 merges, a new PR, `kind: docs`; the orchestrator runs the local review (C-32) on the pushed head and returns its findings with the Bot's in one revise round at most.

## Change (amendment 1, 2026-10-14)

Why: the worker's question (bus 1108, 06:50:50Z): two sentences outside SKILL lines 171 to 178 state the retired gate mechanism (`AUDIT_DISPOSITIONS`, the `audit-finding:` prose as the gate's input), the task-level audit bullet and AGENTS.md's gate sentence, and item 2 forbids sentences outside the owned rows. What changed: item 1 gained one sentence defining the `procedure-migration` row's scope as every such sentence in the allowed files, with the fixture, each with its token test; nothing else. The lines on `origin/main` (c15ba668) that the row now covers, pasted:

```text
$ git show origin/main:home/dot_agents/skills/agmsg-orchestration/SKILL.md | grep -n 'AUDIT_DISPOSITIONS\|audit-finding'
90:  - The orchestrator dispositions every `[P0-P3]` finding in the acceptance record, whatever the verdict: exactly one `audit-finding: <n> …` line per finding
171:    3. Write the acceptance record, summarising the dispositions, with an `audit-finding:` line for every audit finding whatever the verdict (the gate needs
172:    4. Run the gate: `AUDIT_EVIDENCE=<audit> [AUDIT_DISPOSITIONS=<acceptance record>] AGENT_REVIEWED=1 REVIEW_EVIDENCE=<receipt> ACCEPTANCE_EVIDENCE=<accept
178:       - `AUDIT_EVIDENCE` must be the task-level file `.orchestration/validation/<task>-audit-<sha7>.md` (the same `<task>` as the feedback JSON); a per-com
$ git show origin/main:AGENTS.md | grep -n 'AUDIT_DISPOSITIONS'
44:- Before merging a pull request, follow the integration order in the agmsg-orchestration SKILL's Orchestrator Playbook step 10 and `home/dot_config/claude/ru
$ git show origin/main:tests/fixtures/regime/invariants.md | grep -n 'AUDIT_DISPOSITIONS\|audit-finding'
27:  - The orchestrator dispositions every `[P0-P3]` finding in the acceptance record, whatever the verdict: exactly one `audit-finding: <n> …` line per finding
```
