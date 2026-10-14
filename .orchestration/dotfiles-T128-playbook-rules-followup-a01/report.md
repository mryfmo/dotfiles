---
task_id: dotfiles-T128-playbook-rules-followup-a01
seat: claude-standard-dot-a002
branch: regime/playbook-rules-followup
base: c15ba668da20dc2956220077cb0f20054ab352c7
rule_commit: 7a282f3b
task_sha256: ec415eaf526937fd43907a59fccfc455de117850003ba3d48cd20b065fc5564b
---

# Report: dotfiles-T128-playbook-rules-followup-a01

- Seat: `claude-standard-dot-a002` in `.claude/worktrees/worker-f`, on a fresh branch `regime/playbook-rules-followup` from `origin/main` `c15ba668`. The task-checkers branch stays as it is.
- Task file: amendment 1, sha256 `ec415eaf…`, copied byte-identical to `.orchestration/dotfiles-T128-playbook-rules-followup-a01/task.md` (validation §1).
- Round 1 was dispatched at 06:47:41Z. At 06:50Z I asked whether two more sentences belonged to the `procedure-migration` row: the task-level audit bullet and AGENTS.md:44, which both state the retired gate input outside SKILL lines 171 to 178. Amendment 1 (07:03:44Z) put them in the row. Nothing was pushed before it.

## The owned rows

The `## Owned by dotfiles-T128-playbook-rules-followup-a01` section of `.orchestration/acceptance/dotfiles-T128-playbook-rules-a04.md` on `origin/main` (sha256 `3bfd13d7…`) holds four rows (validation §2):

| Row | Class | What changed (`7a282f3b`) |
|---|---|---|
| `local:65a3d71:1` | rule-gap | Orchestrator Playbook step 6: "so the orchestrator creates that record, `.orchestration/acceptance/<task>.md`, before the task's first dispatch (`scripts/orchestrator/dispatch.sh` refuses a record that does not exist or that names another task)". `dispatch.sh` refuses a record that is not an existing regular file or whose `task` is another task (its header, validation §3). The pinned fixture `orchestrator-step-6.md` changes with it. |
| `audit:65a3d71:2` | rule-gap | The same finding as `local:65a3d71:1`, as the audit of `65a3d71b` raised it, so it is fixed by the same sentence. |
| `audit:71eb920:1` | procedure-migration | Every sentence in the allowed files that still stated the retired gate input (amendment 1); the gate on `main` reads the record's JSON `audit_findings` and only reports `AUDIT_DISPOSITIONS` as retired (validation §3). The changed sentences are listed below the table. |
| `audit:65a3d71:1` | disposition-range | No rule sentence: the finding was a sweep-table disposition (`fixed:a03c1daa` outside base..head), corrected in a04's sweep at 14:41Z. Nothing changes for it. |

The `procedure-migration` row changed these sentences:

- **The task-level audit bullet (invariants section):**
  - An `incorrect` verdict is dispositioned in `audit_findings`, the only form the gate reads: one `{n, reason, evidence}` entry per finding, `n` a string, `reason` at least 20 characters. The entries are written with `acceptance-front-matter.py --audit-dispositions`, and an entry never cites a fix.
  - A `Verdict: correct` finding keeps its `audit-finding: <n> …` prose line.
  - The pinned fixture `invariants.md` changes with it.
- **Step 10.3:** it now points to that bullet.
- **Step 10.4:** the gate command drops `[AUDIT_DISPOSITIONS=<acceptance record>]`, and the `AUDIT_EVIDENCE` bullet now asks for an `audit_findings` entry per finding.
- **AGENTS.md:44:** the gate takes `PR_FEEDBACK_EVIDENCE`, `AUDIT_EVIDENCE` and `ACCEPTANCE_EVIDENCE`.

Each changed sentence has a token test, and the superseded forms are asserted absent:

- `test_dispatches_are_recorded_from_the_bus`;
- `test_the_gate_reads_the_acceptance_record`;
- `test_an_incorrect_audit_is_dispositioned_in_audit_findings` (new).

The documentation module runs 48 tests OK (validation §4).

## Caps and checks

- **INV-2** (validation §7): 5 files outside `.orchestration/`, 6 added lines outside `tests/` and 50 added lines under `tests/`.
- **Formatting:** prettier and `ruff format --check` are clean.
- **`ruff check`:** reports the module's implicit-concatenation style (ISC004) on the new tuples as on its existing ones, 12 against 7 on `origin/main`. CI runs only the format check.

## CI and the Bot

In the RESULT. The Bot reviews once, at PR open.

## Not done, or outside scope

- Understand-Anything hook: did not fire. plan-mode-used: no.
- cost: n/a (the runtime exposes no session figures to the seat).
