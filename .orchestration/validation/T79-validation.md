# T79 validation: clause inventory and zero-loss mapping

## Baseline and method

- Source frozen before editing: 23 bullets in
  `home/dot_config/claude/rules/agmsg-orchestration.md`.
- T77 estimator: English character count / 4, ±20% approximate.
- Before: 8,817 characters / 2,204.25 estimated tokens.
- After: 1,358 characters / 339.50 estimated tokens.
- Reduction: 1,864.75 estimated tokens (84.6%).
- Core target <=350: PASS.

## Clause inventory and mapping

The IDs below preserve the original bullet number and split every compound
duty into independently auditable subclauses.

| ID | Original clause substance | Disposition and destination |
| --- | --- | --- |
| 1a | Activate on operator agmsg/Codex request | kept core; detailed in skill §Regime activation and progress |
| 1b | Activate when bus and resident worker are available | kept core; detailed in skill §Regime activation and progress |
| 1c | agmsg becomes always-on communication path | kept core; detailed in skill §Regime activation and progress |
| 1d | Claude acts only as lightweight-read/judgment/task/acceptance orchestrator | kept core; detailed in skill §Regime activation and progress |
| 1e | Only explicit current-task opt-out permits direct mutation | kept core; detailed in skill §Regime activation and progress |
| 2a | Verify CompactionDB opt-in and install if missing | moved to skill §Regime activation and progress |
| 2b | Regime activation is operator consent to install | moved to skill §Regime activation and progress |
| 2c | Acceptance-time decision consolidation applies | moved to skill §Regime activation and progress |
| 3a | Delegate every repository mutation to resident Codex workers | kept core; detailed in skill §Parallel workers |
| 3b | At most one resident worker per worktree | moved to skill §Parallel workers |
| 3c | Assign sequentially within one worktree | moved to skill §Parallel workers |
| 3d | Parallelize only with worktrees; no parallel codex exec/per-task spawn | moved to skill §Parallel workers |
| 3e | agmsg/herdr control-plane commands are orchestrator exemptions | kept core in tightened form; enumerated in skill §Parallel workers |
| 4a | Every parallel worker owns a registered worktree | moved to skill §Parallel workers |
| 4b | Same-repo workers share default store; no per-worker storage override | moved to skill §Parallel workers |
| 4c | Identity-addressed/worktree whoami isolation needs one watcher; actas cannot support extras | moved to skill §Parallel workers |
| 4d | Every parallel identity, including first, has `-aNNN` | moved to skill §Parallel workers |
| 4e | Expanded allowed-files sets are pairwise disjoint and pre-verified | moved to skill §Parallel workers |
| 4f | Orchestrator performs cross-worktree merge/rebase/conflict integration | moved to skill §Parallel workers |
| 5a | Teardown runs delivery off for exact worker path/all types | moved to skill §Parallel workers |
| 5b | Teardown removes every finished worker membership | moved to skill §Parallel workers |
| 5c | Last task-team member leaves; history remains | moved to skill §Parallel workers |
| 5d | identities output: exactly one line is healthy | moved to skill §Parallel workers |
| 5e | Multiple lines cause attach ambiguity and are cleaned with leave | moved to skill §Parallel workers |
| 5f | Unexpected zero is restored with join, never leave-side edits | moved to skill §Parallel workers |
| 6a | Review every RESULT adversarially across four risk dimensions | kept core; detailed in skill §Review and integration invariants |
| 6b | Try to refute and independently re-derive findings | kept core; detailed in skill §Review and integration invariants |
| 6c | Never treat sampled spot checks as full verification | kept core; detailed in skill §Review and integration invariants |
| 7a | Effects require a report-stated reverse mapping | already present in skill §Message Contract v1 and Orchestrator Playbook step 9 |
| 7b | Irreversible effects and rationale go in acceptance | already present in skill §Message Contract v1 and Orchestrator Playbook step 9 |
| 8 | Acceptance records include reported token/cost or `cost: n/a` | already present in skill §Message Contract v1 |
| 9 | Do not idle-wait; prepare/delegate independent work | moved to skill §Regime activation and progress |
| 10a | Acceptance/adversarial/review-profile work remains Claude-side | kept core; detailed in skill §Review and integration invariants |
| 10b | Never delegate review, acceptance, or Crit gate | kept core; detailed in skill §Review and integration invariants |
| 10c | `make require-crit-review` is final integration step | kept core; detailed in skill §Review and integration invariants |
| 10d | Revisit only if worker capability surpasses orchestrator | kept core; detailed in skill §Review and integration invariants |
| 11a | Check delivery status on activation | moved to skill §Identity, delivery, and storage |
| 11b | If weaker than both, run delivery set both | moved to skill §Identity, delivery, and storage |
| 11c | Start SessionStart watcher persistently | moved to skill §Identity, delivery, and storage |
| 11d | Claim actas exclusivity | moved to skill §Identity, delivery, and storage |
| 12a | Completion is detected only by RESULT through monitor/turn | moved to skill §Regime activation and progress |
| 12b | Liveness/status uses only PING/PONG over bus | moved to skill §Regime activation and progress |
| 12c | Never read worker panes/screens | moved to skill §Regime activation and progress |
| 12d | Pane interaction is prompt injection plus submit only | moved to skill §Regime activation and progress |
| 12e | Never infer completion from pane/agent status | moved to skill §Regime activation and progress |
| 12f | Never use ad-hoc polling sleep loops | moved to skill §Regime activation and progress |
| 13 | Out-of-band Codex completion uses official notify event | moved to skill §Regime activation and progress |
| 14a | One physical agent has one runtime/profile/project identity | moved to skill §Identity, delivery, and storage |
| 14b | Project suffix derives from repo, not checkout | moved to skill §Identity, delivery, and storage |
| 14c | Model IDs appear only in model_profiles manifest | moved to skill §Identity, delivery, and storage |
| 14d | Solo worker needs no instance suffix | moved to skill §Identity, delivery, and storage |
| 14e | All parallel workers use `-aNNN`, including first | moved to skill §Identity, delivery, and storage |
| 14f | Rename incumbent to a001; registration/history follow | moved to skill §Identity, delivery, and storage |
| 14g | Re-claim actas locks after rename | moved to skill §Identity, delivery, and storage |
| 14h | Never mix suffixed and unsuffixed parallel workers | moved to skill §Identity, delivery, and storage |
| 15a | Search every team config before join | moved to skill §Identity, delivery, and storage |
| 15b | Collision requires unique suffix | moved to skill §Identity, delivery, and storage |
| 15c | Never reuse one identity for distinct physical agents | moved to skill §Identity, delivery, and storage |
| 16a | Register real worker worktree path | moved to skill §Identity, delivery, and storage |
| 16b | Path bytes match join/delivery/hook arguments | moved to skill §Identity, delivery, and storage |
| 16c | Trailing slash/unresolved symlink exact mismatch orphans inbox | moved to skill §Identity, delivery, and storage |
| 16d | `$HOME` registration is forbidden due hook ambiguity/theft | moved to skill §Identity, delivery, and storage |
| 17a | Setup runs delivery turn for Codex worktree | moved to skill §Identity, delivery, and storage |
| 17b | Tree-scoped gitignored Codex Stop hook delivers messages | moved to skill §Identity, delivery, and storage |
| 17c | Storage env unset for same repo; dedicated for cross-project | moved to skill §Identity, delivery, and storage |
| 17d | Wrong/stray storage env silently reroutes DB | moved to skill §Identity, delivery, and storage |
| 17e | Pane nudges are generic; message content stays on bus | moved to skill §Identity, delivery, and storage |
| 18a | Separate stores only for concurrent different-project regimes | moved to skill §Identity, delivery, and storage |
| 18b | Worker and orchestrator calls use identical storage env | moved to skill §Identity, delivery, and storage |
| 18c | Mismatch makes tasks/results/pongs unreachable | moved to skill §Identity, delivery, and storage |
| 18d | Same-repo parallel workers always share default store | moved to skill §Identity, delivery, and storage |
| 19a | Live desktop behavior tasks require live E2E | moved to skill §Live verification |
| 19b | E2E covers fresh and persisted restore | moved to skill §Live verification |
| 19c | Unit/static checks alone are insufficient | moved to skill §Live verification |
| 20a | Orchestrator E2E panes use express profile | moved to skill §Live verification |
| 20b | Arguments come from model-profiles env variables | moved to skill §Live verification |
| 20c | Never use ad-hoc model flags | moved to skill §Live verification |
| 21 | Invoke agmsg-orchestration skill for contracts/playbooks | kept core, tightened to immediate full-protocol invocation |
| 22a | Sync evidence at regime/session boundaries | kept core; detailed in skill §Review and integration invariants |
| 22b | Evidence bookkeeping is orchestrator mutation exemption | kept core; detailed in skill §Review and integration invariants |
| 22c | Sync needs no per-task artifact set | moved to skill §Review and integration invariants |
| 22d | Audit is commit with task IDs plus ACCEPTANCE history | moved to skill §Review and integration invariants |
| 22e | Write pending acceptance records first | kept core; detailed in skill §Review and integration invariants |
| 22f | Commit every orchestration file; zero untracked tail | kept core; detailed in skill §Review and integration invariants |
| 22g | Commit mise config/lock upgrade pair as separate chore same session | kept core; detailed in skill §Review and integration invariants |
| 22h | Never leave mise pair dirty across sessions | kept core; detailed in skill §Review and integration invariants |
| 23 | Sync verifies every accepted task has consolidated decision | kept core; detailed in skill §Review and integration invariants |

Mapping count: 87/87 subclauses mapped; dropped/unmapped: 0.

## Contract and core invariants

- `Message Contract v1` pre-edit SHA-256:
  `944fbeef42549f3c77dbc455401ec29e58ec48772dee56899a41e5eb75d79038`
- Post-edit SHA-256: identical.
- Core textual checks: activation, immediate skill invocation, mutation
  delegation, adversarial review, non-delegated acceptance/review, final Crit
  integration, zero-tail sync, accepted-task decision, and mise pair all
  present.
- Other Claude rule changes: none.

## Gates

- `make format`: PASS; shfmt reported no diff.
- `env UV_CACHE_DIR=/private/tmp/t68c-uv-cache make validate-agent-assets`:
  PASS; agent asset validation ok.
- `UV_CACHE_DIR=/private/tmp/t68c-uv-cache uv run python -m unittest discover -s tests/unit -p "test_*.py" -q`:
  PASS; 336 tests in 32.643s, UNIT_EXIT=0. Four expected negative-fixture
  model-profile diagnostics were printed and their assertions passed.
- `git diff --check`: PASS.

## Crit review

- Record: `r_dc8606`, resolved finding-free approval.
- Evidence: `.agents/worklog/codex/review/T79-crit-comments.json`.
- Receipt: `.agents/worklog/codex/review/T79-receipt.md`.
- Gate: PASS with `AGENT_REVIEWED=1` and the receipt above.

## Plan quality

The native validator/Make target, hook, reviewer definition, and matching CI
entrypoint are absent. The plan was manually checked for measured current
state, explicit core invariant and scope boundaries, positive/adversarial
verification, concrete commands, done criteria, and STOP conditions.

## Decision memory

- UUID: `4c8dac80-aa6b-48b6-88ef-4eaa2927ed03`
- Command:
  `python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content 'T79: agmsg orchestration uses two-tier progressive disclosure: a 339.50-token estimated always-on core retains activation, delegation, adversarial and non-delegable review, zero-tail evidence sync, decision completeness, and mise-pair invariants; the full operational protocol lives in the agmsg-orchestration skill with zero mapped clause loss.'`
