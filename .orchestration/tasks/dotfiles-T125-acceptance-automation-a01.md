> **Superseded 2026-10-10 by T126** (`dotfiles-T126-regime-v2-a01`, accepted in design review round 3); not dispatched.

---
format: legacy-superseded
task_id: dotfiles-T125-acceptance-automation-a01
kind: design
security: true
design_review:
  receipt: (pending; review by a -review- identity after T124 wave 1 merges)
  design: .orchestration/tasks/dotfiles-T125-acceptance-automation-a01.md
threat_model:
  E1: the orchestrator's acceptance steps (sweep, dispositions, records, gate, merge, ACCEPTANCE, consolidation) are typed by hand each time, so they cost 10-20 minutes per task and admit transcription errors (T119: two count corrections)
  E2: the task-level audit starts only when the orchestrator notices the RESULT, so each round's wall time is the sum of worker, audit and orchestrator latencies instead of their maximum
  E3: seats sit idle while dispatchable tasks exist, because nothing measures it (this session: one busy seat for most of 22 hours with T120 and T124 wave 3b dispatchable)
  E4: workers hold a round for one to two hours before the first push, so Bot and CI findings arrive after the design has hardened
trust_anchors:
  - the same two sources as T124 (agmsg history, GitHub) plus main-checkout files; automation reads them, never the gate's cwd
  - automation never decides acceptance; it prepares the evidence and runs the gate, and the orchestrator's ACCEPTANCE in history stays the decision
  - an audit started automatically is the same read-only headless audit as today, keyed to the head sha, re-run when the head changes
invariants:
  INV-A1: scripts/accept-task.py <task> --head <sha> performs sweep, disposition scaffolding (thread map from history replies and verified fixed shas supplied by the orchestrator), receipt and acceptance-record updates, the gate from main, and prints the merge command; it never merges, never sends ACCEPTANCE, and refuses when any item lacks a disposition
  INV-A2: an audit of a pushed head starts without the orchestrator (a watcher on the PR's head, or the worker's RESULT hook) and its verdict file is keyed by the head sha; a RESULT whose head has no audit file yet makes the orchestrator wait, not re-run
  INV-A3: check-regime-boundary and the orchestrator's stop gate warn when a seated worker has had no AGMSG-TASK in flight for more than N minutes while a task file with no RESULT and no in-flight TASK exists (dispatchable backlog), computed from history and the task directory
  INV-A4: the worker playbook requires a first push within 30 minutes of the TASK (a draft PR is enough) so Bot and CI run on the design early; the stop gate warns a worker past that window
  INV-A5: every acceptance record carries measured cost fields (rounds, amendments, worker wall time from TASK to final RESULT in history, audit count, CI runs, and token counts where the runtime logs expose them) written by accept-task.py, never n/a; check-regime-boundary warns when a task exceeds its tier's baseline
  INV-A6: the process a task follows is a function of its tier, stated in one table the validator reads (design tier: design review, invariant tests, audit, reset rule; review tier: Bot, CI, one audit, two revises; docs tier: Bot and CI on the express profile), and the orchestrator cannot add or skip a stage outside the table without an operator waiver
---

# AGMSG-TASK dotfiles-T125-acceptance-automation-a01 — DESIGN DRAFT: acceptance automation, early audits, idle detection

Drafted 2026-10-10 by the orchestrator seat after the operator asked how to raise efficiency and quality further and answered 「あるべき姿」 to the proposal. Companion to T124 (which bounds and verifies tasks); T125 removes the orchestrator's hand-run steps and the dead time between rounds. `security: true` because it touches the gate invocation, `herdr-agents` and the stop gate. Design review by a `-review-` identity after T124 wave 1 merges (the validator then checks this file); waves are cut after the review.

## Pieces

1. `scripts/accept-task.py` (INV-A1): one command that runs `pr-feedback.py`, applies a disposition map (thread id → `fixed:<full sha>` supplied by the orchestrator after verification in the diff; replies, review headers, bot summaries, runner notices and skipped statuses by the fixed rules used since T118), appends the orchestrator review record skeleton and moves the receipt head, writes the acceptance record's audit row and sweep line from the audit `.last.md` and the JSON, runs `make -C <main> require-crit-review REVIEW_TREE=<review worktree>` with the evidence paths, and prints the exact `gh pr merge --squash --match-head-commit <full sha>` and ACCEPTANCE lines for the orchestrator to run. Idempotent per head. Tests with fakes for gh and the gate.
2. Early audit (INV-A2): `herdr-agents --audit-watch <pr>` (or the worker's RESULT hook) starts the headless audit when CI on a new head is green and the Codex Bot has completed, writes `<task>-audit-<sha7>.md(.last.md)` as today, and the orchestrator's acceptance consumes the file if the head matches. Audits never run on a head the Bot has not finished, so the auditor sees the Bot's threads.
3. Idle detection (INV-A3): `check-regime-boundary.sh` and the orchestrator-side stop gate compute, from history and `.orchestration/tasks/`, the set of seated workers without an in-flight TASK and the set of task files with neither a RESULT nor an in-flight TASK and no `superseded_by`; both non-empty for longer than N minutes (default 20) is a warning naming the task and the seat.
4. Early push (INV-A4): Worker Playbook step and a stop-gate warning for a worker whose TASK is older than 30 minutes with no push on its branch (history has the TASK; GitHub has the branch).

5. Cost measurement (INV-A5): `accept-task.py` computes rounds, amendments, wall time and audit count from history and the task directory, and reads token usage from the Claude Code session JSONL and the Codex session log when the seat's session id is known from the seat lock; the acceptance record's `cost:` line becomes those numbers; `check-regime-boundary` compares each accepted task with its tier's rolling baseline (median of the last ten) and warns above 2×.
6. Tiered process table (INV-A6): one YAML table in `home/dot_agents/agent-config.yaml` (`process_tiers:`) mapping tier → required stages, profiles and round limits; the validator stamps the tier on the task, the gate requires the tier's evidence set and no more, and docs-tier tasks run on the `express` profile by default.

## Open questions for the review

- Whether INV-A2 belongs in `herdr-agents` (pair path) or in a GitHub Actions workflow that runs the audit on the runner with the audit profile (keeps the host's auditor idle; needs the Codex credential on the runner, which may be unacceptable).
- The disposition map's input format and how the orchestrator's verification in the diff is recorded (one line per thread with the file:line checked).
- Thresholds N=20 minutes (idle), 30 minutes (first push).

## Audit staging (operator question 2026-10-10: the auditor as a bottleneck, and at which stage to audit)

Today: one audit tab, one audit at a time, 15–25 minutes each, the wrapper setting aside other tasks' files in the main checkout (so audits exclude each other and the orchestrator's acceptance work), one audit per RESULT head, and T119 ran six. With three concurrent workers the audit queue alone can reach an hour. Design:

| stage | who | what | when | cost |
|---|---|---|---|---|
| 1 | review seat (separate context) | design review of invariants and threat model | before code, design tier only | minutes |
| 2 | worker, in its sandbox | invariant tests written first, mutation checks, shellcheck, unit tests | before each push | none for the regime |
| 3 | Codex Bot + CI | per-push findings | every push, in parallel | none |
| 4 | auditor (headless, read-only) | structured verdict: `INV-n: holds|violated`, orchestration/conformance findings, the fixed grammar | once per RESULT head, only after stage 3 is green on that head; re-run only when the head changes; never for evidence-only revisions | the scarce resource |
| 5 | orchestrator | dispositions, gate, merge (accept-task.py) | per RESULT | minutes |

Mechanisms so stage 4 never becomes the queue:
- INV-A7: audits run concurrently, each in its own detached worktree at the audited head (no main-checkout set-aside); `herdr-agents --audit` takes the worktree path and the audit tab becomes a pool of N (default 2).
- INV-A2 (above): an audit starts when stage 3 is green on a pushed head, so the verdict is ready when the RESULT arrives.
- INV-A6 depth by tier: docs tier skips stage 4; review tier gets one audit; design tier gets one audit with invariant lines plus the reset rule.
- INV-A8: at most one audit per RESULT head; an evidence-only revision (no tree change) is judged by the gate's parser and the orchestrator, never by a new audit; the gate refuses a second audit file for the same head.
- INV-A9: a fallback auditor: when the audit seat is unavailable (credit outage, pane failure), a `review`-profile Claude seat runs the same prompt and the gate accepts its output under the same grammar; the acceptance record names which auditor ran.
