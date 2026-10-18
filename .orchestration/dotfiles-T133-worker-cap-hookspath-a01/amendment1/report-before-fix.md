# T133 worker cap and hooksPath

Status: blocked on task amendment after the final-head Codex Bot review; CI watcher joined successfully with exit 0; all 13 listed checks succeeded. Worker codex-standard-dot-a010, round 1. Expected artifacts are at these relative paths in worker-e, not the main checkout; the orchestrator must copy them before acceptance.

PR: https://github.com/mryfmo/dotfiles/pull/408 (ready). Material inspected: https://github.com/mryfmo/dotfiles/pull/393 at 9c07098147d3b16d68a9be2772fbcba2460b8851; reused only its requested cap block, not integration-seat, receipt-verifier or pre-RESULT-gate code.

head: ffd8454dd3a42924e47290aa68a016d211c21c17
base: 99a4a80f5a5b32a70cf7eb4f4d0db5a02d113841
branch: tools/worker-cap-hookspath-a01
task_copy: 9d6aaf8cb439616e3a022f862925d75ab9e2dd0bc2f21eebe49d322dd798acc0
cost: n/a

Changed files: home/dot_agents/agent-config.yaml; home/dot_local/bin/common/executable_herdr-agents; home/dot_agents/skills/agmsg-orchestration/SKILL.md; tests/unit/test_herdr_agents.py; the unchanged dispatched task copy under this directory. Source changed lines 31 <= 120; tests 103 <= 250. The task copy adds 97 evidence lines and is excluded from both caps. No new production script, rename, validator/renderer/rule/model change or remove-worker edit. Exactly two SKILL sentences changed.

Behavior: the deployed worker_cap: 4 limits registered worker worktrees holding either runtime identity. A fifth seat is rejected with exit 2 before writes; reseating proceeds. Missing/malformed cap warns and proceeds, per task. Add-worker enables common extensions.worktreeConfig once and sets worktree-local core.hooksPath=.githooks every run; main hooks are unchanged. This enables hooks that exist in that worker checkout; adding hooks is owned by P1-5.

Validation: temporary Git proof, render-check, launcher shellcheck/shfmt, changed Python formatting, clean changed-snapshot asset validation and independent final-diff review passed. Three new tests passed: test_add_worker_refuses_a_seat_beyond_the_manifest_worker_cap; test_add_worker_sets_the_worktree_hooks_path_and_enables_worktree_config_once; test_the_skill_names_the_manifest_worker_cap. Unchanged docs module: all 53 passed. Combined requested modules: 249 tests, 248 passed, one existing live-Claude-process seat-lock test failed identically on unchanged base because this sandbox cannot inspect process names; no suppression or unrelated code fix. make format failures are byte-identical on clean base and changed snapshots; the root run additionally sees preserved untracked artifacts. Root asset validation stops at an old unrelated untracked home-path log, while the clean changed copy passes. Ruff has the same 22 inherited findings and no additions. Complete outputs are in validation.md.

Local review: Crit had no review data/session. Independent read-only subagent reviewed the final four-file diff SHA256 1c87a1b2723ad1e6219ce74b83f0e5dda3f1a9609bf242fbf1613205cbfa8922 and found no actionable issues. Resolved JSON evidence and worker receipt were read; AGENT_REVIEWED=1 REVIEW_EVIDENCE=... make require-crit-review passed. This does not replace the orchestrator's task-level audit and separate security-profile final-head review required by security:true.

Isolation: no live apply/restart/add/remove, Bats, graph refresh, merge or review-thread resolution. All 1422 prior inventory paths are still present (path-preservation check only). Old blocked artifacts are retained under raw/pre-resume-*.md. Host repair PING 2094 cleared the legacy cherry-pick state before branch creation resumed. Optional packed-refs cleanup warnings, initial stale-pane dispatch failure, SSH push failure, command-scoped HTTPS success and unavailable process inspection are recorded in sandbox.md.

Live herdr-agents changes only at the operator's make update. Plan 024 forbids that update until the merge-gate replacement lands; no deployment was performed.

Bot review: 5561476764 of final head ffd8454d arrived 280 seconds after ready. Review body has no finding; two top-level inline P1 findings are open:

- 4305767690, launcher:1845, serialize cap count with creation/identity registration; concurrent additions can both see 3/4 and create five seats. https://github.com/mryfmo/dotfiles/pull/408#discussion_r4305767690
- 4305767694, task.md:17, the launcher threat row closes cap and hooks behavior with only the cap test selector; add hooks test selector or split the controls. https://github.com/mryfmo/dotfiles/pull/408#discussion_r4305767694

Both identify real gaps. They cannot be fixed under the exact current task: item 2 requires the original cap block as written and the task copy must remain byte-identical to the dispatched SHA. Requested an amended task authorizing serialization/concurrency tests and a corrected threat row with a new task-copy SHA. This is a task-specification change, not sandbox permission approval. No worker-side fix round used, no thread replied to/resolved, no code change after the reviewed head. At blocked dispatch CI was still running; it has since exited 0. No RESULT issued because the task amendment is required.

## Blocker dispatch receipt

AGMSG blocked PONG was sent as message 2101. agmsg-dispatch exited 1 after its bounded receipt wait: delivery failed or unread; verify receipt before resending. No duplicate was sent. The final-head Bot watcher completed and CI watcher has now exited 0. No RESULT has been issued while the task amendment is required.

## Final CI and delivery state

CI watcher exited 0 and final GitHub metadata still names ffd8454dd3a42924e47290aa68a016d211c21c17; all 13 listed checks succeeded. Final-head Bot review has the two open P1 findings above. The official history helper shows the blocked PONG as read (○), after agmsg-dispatch itself timed out; no duplicate was sent. Await the amended task before changing the literal cap block or task copy.
