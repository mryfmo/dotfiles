# Acceptance: dotfiles-T88-parallel-execution-rule-a01

- **Decision:** ACCEPTED after six revise rounds and four PONG decisions. PR #243 (`docs/parallel-execution-rule`, worker-d) squash-merged to `main` as `febd0cb7`; final head `62845ab9be1ae25469e06067410db636ee8ba80d`; substantive commits e50150df, e68eb6a7, c544c79f, 8978517d, c5706e2e, d609c768, 0aed931c, 0407fb07, d0f03418, 99f84926, 0189cfb3, fb4c9a9a, 62845ab9; base `57885db1`, update-branch merges through main `f2b5c115`. Merged without `--delete-branch`; worker-d holds the branch.
- **Worker:** `claude-standard-dot-a006` (worker-d). task_rev chain from `41cf14c6…` through round 6 matched. Paused for the T66 revise round and resumed; T68 ran on the same seat between rounds. Parallel wave with T75/T91/T74/T71/T94/T93/T95 (a005) and T65/T92 (a007).
- **Exemption declared:** acceptance and final integration; the orchestrator mutated no repository code.
- **Plan reference:** 並列実行の規定 and the Claude seat Self-Modification constraint (operator 2026-10-04: 「今回のみではなく dotfiles の作業のやりかたとして規定化する」).

## What was accepted (3 files, +35/−4)

- `rules/agmsg-orchestration.md`: parallel-execution invariant (pairwise-disjoint code files, prose files in disjoint sections with `gh pr update-branch` merging the base in, three workers in total counting the resident pair worker, freed workers re-tasked at once, acceptance in RESULT order, audits queued on the single tab); seat-capability routing (Claude permission-policy sources go to a Codex worker or the operator; a refused Claude worker sends a blocked PONG naming Self-Modification, never evades); nested-worktree bullet aligned with T64 (`--ask-for-approval never`, in-sandbox network, no worker escalation). Word count 1269 → 1454; T83 absorbs it.
- `SKILL.md`: "Parallel execution procedure" (wave table, seat cap, dispatch to free seats, re-task, record in acceptance records, gate and merges one at a time); Playbook step 3 routing by allowed files plus the `auto` facts (built-in since 2.1.283; a project-level `auto` disables the user-level value); worker step 4 classifier denial = boundary; new step 14 `crit stop` (never `--all`) with unsandboxed `pgrep` confirmation.
- `tests/unit/test_agmsg_orchestration_docs.py`: shared-token test for the two invariants; test that "network access stays off" is gone from the rule.

## Orchestrator re-derivation

- Read every hunk of the three files at c8d31501. The rule and SKILL say the same thing about the cap, the dispatch bound, the merge semantics of `gh pr update-branch` and the blocked-PONG path. No sentence in `AGENTS.md` contradicts them (worker grep pasted in validation, re-run here: zero hits for "network access", "escalation", "pairwise", "Self-Modification").
- The worker also corrected two literal `%H %s` lines and one `exit status: %s` line in its own T66 validation file (a `%%` escaping slip), replacing them with real `git show` output and a re-derived `gh pr checks` exit status. Recorded here; the T66 acceptance stands.

## Audit / Bot / sweep / gate

| commit | verdict |
|---|---|
| task-level, final head 62845ab9 | incorrect (1, evidence only) → disposition below |
| task-level fb4c9a9a, 0189cfb3, 5bef5588, 19becfc5, 04fd9425 | incorrect → each fixed by the next round (62845ab9, fb4c9a9a, 0189cfb3, 99f84926, c544c79f/c5706e2e) |
| per-commit e50150df | incorrect: 4 findings → e68eb6a7, c544c79f, c5706e2e |
| per-commit e68eb6a7 | correct |

audit-finding: 1 the report's final-head Prettier and validate-agent-assets evidence is a summary (`rc=0`) rather than pasted output → not-applicable:evidence-only finding with no code defect; CI's prettier and validate jobs pass on 62845ab9 per the sweep JSON and the orchestrator ran the docs test locally; the worker pastes the final-head commands and output as an artifact correction that does not move the head

- audit-finding: e50150df SKILL.md:37 seat cap ignores the pair worker and dispatches whole waves → fixed:e68eb6a7 (audited correct)
- audit-finding: e50150df SKILL.md:40 `gh pr update-branch` merges, not rebases → fixed:e68eb6a7 (audited correct)
- audit-finding: e50150df SKILL.md:163 bare `crit stop` misses a daemon started on another branch → revise round 1 (leftover path: pgrep → `/proc/<pid>/cwd` is own worktree → `kill <pid>`)
- audit-finding: e50150df SKILL.md:163 unsandboxed `pgrep` said to contradict step 4 / never-approval → revise round 1 scopes step 14 to Claude workers (Plan Mode is Claude-only) and names the gate-allowed unsandboxed reads; for a Claude seat the permission gate, not `never`, governs unsandboxed commands (observed on a006 in T66/T88)

- Codex Bot: fourteen threads over the PR, twelve fixed in-PR and two not-applicable (the worker kind is the manifest's; rule prose is not the execution boundary), all replied and resolved by the orchestrator; thumbs-up on the final heads. Sweep (head 62845ab9): 54 items, 0 failure/warning, all dispositioned. Gate at 62845ab9 with `AUDIT_EVIDENCE` and `AUDIT_DISPOSITIONS=<this record>`: exit 0, evidence copies removed.

## Rounds 2-6 (task-level audits and PONG decisions 2-4)

- Step 14 covers any worker whose session started a Crit plan review (a Codex seat does so through the Crit plugin's Stop hook); the worker only reports `plan-mode-used=<worktree>`; the orchestrator inspects the host outside its sandbox through the permission gate, confirms the live pid's command and cwd (`readlink /proc/<pid>/cwd`, `lsof` on macOS) before `kill`, and removes stale records.
- Routing follows the boundary a change touches: Claude-only sources (the `claude.*` blocks, the rendered Claude settings, the merge script, the Claude-rendering parts of the renderer) go to a Codex seat; Codex-only sources to a Claude seat; both or unsplittable, and permgate (both seats' PermissionRequest hook), to the operator; the kind is recorded in the task file. The Codex `security`-profile worker reviews permgate changes before acceptance (the model-selection rule assigns it audits, not edits).
- Every in-flight PR whose base moved runs `gh pr update-branch` before CI, Bot wait and gate; the worker commits and pushes before each RESULT and takes a clean checkpoint before every branch switch, so a revise re-checks out the earlier branch safely.
- Recorded not-applicable: the worker kind stays the manifest's `worker_kind` (T83 drops the legacy Codex wording); rule and skill prose are not the execution boundary.

## Follow-ups

- Worker note: on seat a006 the first sandboxed `agmsg-dispatch` fails with a herdr socket `PermissionDenied` and needs an unsandboxed retry, contrary to Worker Playbook step 11 (`excludedCommands`). Observed on a spawn-seated worker whose environment never received the pane env (T89 finding 1). Carry into the T89 spawn-env follow-up task.
- Whether a bare `crit stop` reaches a Plan Mode plan server is unverified (step 14 pairs it with `pgrep`).

## CompactionDB

- Worker decision `33356f9a-a70b-4d61-b725-dde6d67594d0`; cited, no amendment.
