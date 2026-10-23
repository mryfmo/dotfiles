# Clean-up table (after the cutover): open old-regime pull requests and leftover worktrees

Inventory taken 2026-10-23T21:58:15Z from `gh pr list --state open` and `git worktree list --porcelain` (read-only). Defaults follow D-024-131 (the agmsg regime is off): an old-regime PR closes as superseded unless its branch carries work the cutover did not replace; a worktree of a landed unit or a merged sync goes. Executing a row is a later, explicit step; nothing here was closed or removed.

## Open pull requests

| PR | branch | opened | files | title | default |
| --- | --- | --- | --- | --- | --- |
| #378 | `tools/chain-glue-finish` | 2026-10-16 | 16 | feat(orchestrator): chain-finish.sh finishes a PR after the audit's dispositions, merging only the audited head (plan 022 T8, T128 chain-glue finish a01, reset a02) | close: superseded by the cutover (agmsg-regime tooling) |
| #395 | `portability/sandbox-a01` | 2026-10-17 | 11 | test(portability): guard the tracked scripts against diff with process substitution and hard-coded /tmp (T130 sandbox-portability a01) | close: superseded by the cutover (agmsg-regime tooling) |
| #396 | `tools/anthropic-auth-route-structured` | 2026-10-17 | 186 | fix(validator): the Anthropic auth route check reads JSON, TOML and YAML through their parsers (T129 anthropic-auth-route-check followup a01) | close: superseded by the cutover (agmsg-regime tooling) |
| #404 | `tools/anthropic-auth-runtime-check` | 2026-10-17 | 8 | feat(doctor): refuse the Anthropic OAuth route at run time (T129 anthropic-auth-runtime-check a01) | close: superseded by the cutover (agmsg-regime tooling) |
| #407 | `tools/hcom-dispatch-bus-a01` | 2026-10-18 | 2 | docs(orchestration): hcom-dispatch bus stage 1 item 0 findings (T129 hcom-dispatch-bus a01) | close: superseded by the cutover (agmsg-regime tooling) |
| #410 | `tools/verdict-audit-pool-a01` | 2026-10-18 | 12 | feat(orchestrator): verdict.sh, audit-pool.sh, orch-audit.sh json mode and the class vocabulary (T133 verdict-audit-pool a01) | close: superseded by the cutover (agmsg-regime tooling) |
| #411 | `tools/result-precheck-a01` | 2026-10-18 | 87 | feat(orchestrator): the pre-RESULT precheck, the accepted-ACCEPTANCE gate and the commit and push hooks (T133 result-precheck a01) | close: superseded by the cutover (agmsg-regime tooling) |
| #412 | `tools/anthropic-auth-route-structured` | 2026-10-18 | 34 | feat(agents): validate structured Anthropic auth routes | carry: judge the branch's diff against main (not regime tooling by name) |
| #419 | `tools/dispositions-a01` | 2026-10-18 | 10 | feat(orchestrator): dispositions.py proposes thread dispositions and verifies refutation forms; orch-gate.sh re-validates them (T133 dispositions a01) | close: superseded by the cutover (agmsg-regime tooling) |
| #420 | `tools/permission-guard-gate-a01` | 2026-10-18 | 17 | feat(agents): gate GitHub writes with bound task evidence | carry: judge the branch's diff against main (not regime tooling by name) |
| #424 | `tools/ci-efficiency-followup-a02` | 2026-10-19 | 9 | fix(orchestrator): ci-rerun.sh pins its tools and starts its interpreter by its own path (T133 ci-efficiency follow-up a02, security:4fe2438:1) | close: superseded by the cutover (agmsg-regime tooling) |
| #426 | `tools/hold-playbook-a01` | 2026-10-19 | 9 | feat(orchestrator): hold-playbook.sh expands a class's remedy into a replan skeleton and records a pending decision for out-of-scope globs (T133 hold-playbook a01, plan 024 P1-13) | close: superseded by the cutover (agmsg-regime tooling) |
| #431 | `tools/worker-write-boundary-a01` | 2026-10-19 | 22 | fix(agents): screen Claude worker startup inputs | close: superseded by the cutover (agmsg-regime tooling) |
| #432 | `tools/lint-comparisons-followup-a02` | 2026-10-19 | 22 | fix(lint): the comparison lint reads tokens: the F2 lineage's nine detection gaps (T129 normalised-comparison-lint followup a02) | close: superseded by the cutover (agmsg-regime tooling) |
| #439 | `tools/chain-review-scripts-followup-a07` | 2026-10-20 | 11 | fix(orchestrator): local-review.sh reviews against canonical main from gh api, never a local ref (T128 chain-review-scripts follow-up a07) | close: superseded by the cutover (agmsg-regime tooling) |
| #440 | `tools/task-generator-plan-check-a05-checker` | 2026-10-20 | 449 | fix(orchestrator): enforce checker contracts and preserve dispatch compatibility | close: superseded by the cutover (agmsg-regime tooling) |
| #456 | `tools/gh-binding-a02` | 2026-10-22 | 16 | fix(orchestration): bind gh and isolate feedback descendants | close: superseded by the cutover (agmsg-regime tooling) |
| #457 | `tools/install-ppa-resilience-a02` | 2026-10-22 | 7 | fix(install): an unreachable Ghostty PPA never fails the apply, attributed by command scope (T133 install-ppa-resilience a02) | close: superseded by the cutover (agmsg-regime tooling) |

## Worktrees

| path | head | branch | default |
| --- | --- | --- | --- | 
| `/private/tmp/claude-501/records-program-1` | 3b6fa294 | `records/program-store-1` | prune: scratchpad worktree of a past session (`git worktree prune` once the directory is gone) |
| `/private/tmp/claude-501/records-program-2` | b8742836 | `records/program-store-2` | prune: scratchpad worktree of a past session (`git worktree prune` once the directory is gone) |
| `~/.local/state/omp-seats/audit` | 994c3616 | `detached` | judge |
| `~/.local/state/omp-seats/worker` | c67d4d0b | `detached` | judge |
| `~/Workspace/dotfiles/.claude/worktrees/agent-a11ce75e4e80ccab9` | 940d05b7 | `feat/hcom-dispatch-bus` | remove: poteto-agent isolation worktree of a landed unit (check `git status` first) |
| `~/Workspace/dotfiles/.claude/worktrees/agent-a148a20a9c044d2f5` | d4dd2b16 | `feat/omp-run` | remove: poteto-agent isolation worktree of a landed unit (check `git status` first) |
| `~/Workspace/dotfiles/.claude/worktrees/agent-a1b53ce19ab67c0fd` | ccc40eae | `feat/hcom-seat` | remove: poteto-agent isolation worktree of a landed unit (check `git status` first) |
| `~/Workspace/dotfiles/.claude/worktrees/agent-a2945f89a3aaa8c52` | ac7a4e0f | `fix/omp-overlays-no-wizard` | remove: poteto-agent isolation worktree of a landed unit (check `git status` first) |
| `~/Workspace/dotfiles/.claude/worktrees/agent-a30fc59e8289c4220` | f201d2fe | `feat/omp-seat-policy` | remove: poteto-agent isolation worktree of a landed unit (check `git status` first) |
| `~/Workspace/dotfiles/.claude/worktrees/agent-a337fcea648851ced` | 62f0f15d | `feat/regime-ci-program-marker` | remove: poteto-agent isolation worktree of a landed unit (check `git status` first) |
| `~/Workspace/dotfiles/.claude/worktrees/agent-a346a24db554b4f14` | 9a795960 | `feat/pi-claude-bridge-asset` | remove: poteto-agent isolation worktree of a landed unit (check `git status` first) |
| `~/Workspace/dotfiles/.claude/worktrees/agent-a55e506e15f6730f0` | 63b81a04 | `tools/omp-config-render` | remove: poteto-agent isolation worktree of a landed unit (check `git status` first) |
| `~/Workspace/dotfiles/.claude/worktrees/agent-a6244fa3bc5832b63` | 12b27b3d | `u9c-fix` | remove: poteto-agent isolation worktree of a landed unit (check `git status` first) |
| `~/Workspace/dotfiles/.claude/worktrees/agent-a65a17b406ca7e1c3` | ac2288b6 | `fix/stop-gate-audit-verdict` | remove: poteto-agent isolation worktree of a landed unit (check `git status` first) |
| `~/Workspace/dotfiles/.claude/worktrees/agent-a77f166537f192118` | 0f9cfdf5 | `u3b-openai-siwc` | remove: poteto-agent isolation worktree of a landed unit (check `git status` first) |
| `~/Workspace/dotfiles/.claude/worktrees/agent-a78202bf9ff6af81a` | f95738b4 | `fix/audit-seat-reply-route` | remove: poteto-agent isolation worktree of a landed unit (check `git status` first) |
| `~/Workspace/dotfiles/.claude/worktrees/agent-a8b0cb0a2dba7320c` | d7ea7262 | `fix/hcom-seat-go` | remove: poteto-agent isolation worktree of a landed unit (check `git status` first) |
| `~/Workspace/dotfiles/.claude/worktrees/agent-a9170ab705b6a2d0d` | 9a795960 | `detached` | remove: poteto-agent isolation worktree of a landed unit (check `git status` first) |
| `~/Workspace/dotfiles/.claude/worktrees/agent-a96c96c26d6a270eb` | af35fd50 | `worktree-agent-a96c96c26d6a270eb` | remove: poteto-agent isolation worktree of a landed unit (check `git status` first) |
| `~/Workspace/dotfiles/.claude/worktrees/agent-ab1e1d6945873419c` | ccc40eae | `feat/hcom-seat` | remove: poteto-agent isolation worktree of a landed unit (check `git status` first) |
| `~/Workspace/dotfiles/.claude/worktrees/agent-ab74be3bf07405ef0` | c4d18653 | `u2b/pi-claude-bridge-asset` | remove: poteto-agent isolation worktree of a landed unit (check `git status` first) |
| `~/Workspace/dotfiles/.claude/worktrees/agent-aba52b897ca0bae08` | a4d1045f | `fix/audit-worktree-positioning` | remove: poteto-agent isolation worktree of a landed unit (check `git status` first) |
| `~/Workspace/dotfiles/.claude/worktrees/agent-abb36dac62fb5460d` | a86ed4c6 | `fix/audit-policy-name` | remove: poteto-agent isolation worktree of a landed unit (check `git status` first) |
| `~/Workspace/dotfiles/.claude/worktrees/agent-acd493023dd912cc3` | 50a11a7c | `worktree-agent-acd493023dd912cc3` | remove: poteto-agent isolation worktree of a landed unit (check `git status` first) |
| `~/Workspace/dotfiles/.claude/worktrees/agent-ad750c64ea7ec6197` | 81a48c2a | `feat/pstack-skills-asset` | remove: poteto-agent isolation worktree of a landed unit (check `git status` first) |
| `~/Workspace/dotfiles/.claude/worktrees/agent-ae2bb242b04adcb5c` | 0f9cfdf5 | `detached` | remove: poteto-agent isolation worktree of a landed unit (check `git status` first) |
| `~/Workspace/dotfiles/.claude/worktrees/agent-ae5d88e2dbc68c33d` | 5b17ae6a | `detached` | remove: poteto-agent isolation worktree of a landed unit (check `git status` first) |
| `~/Workspace/dotfiles/.claude/worktrees/agent-aebb8ae730c03ede4` | 99ddf5cc | `u14b-fix` | remove: poteto-agent isolation worktree of a landed unit (check `git status` first) |
| `~/Workspace/dotfiles/.claude/worktrees/agent-af6e0e866f1c5f5ad` | d661a9f4 | `detached` | remove: poteto-agent isolation worktree of a landed unit (check `git status` first) |
| `~/Workspace/dotfiles/.claude/worktrees/agent-af7be47ea3025ebe6` | 5b17ae6a | `feat/openai-siwc-extension` | remove: poteto-agent isolation worktree of a landed unit (check `git status` first) |
| `~/Workspace/dotfiles/.claude/worktrees/agent-afb46e4612b6d057f` | 4520243f | `feat/omp-role-overlays` | remove: poteto-agent isolation worktree of a landed unit (check `git status` first) |
| `~/Workspace/dotfiles/.claude/worktrees/agent-afbdc2535b58d894b` | 3809e407 | `u6d/fix-audit-policy-name` | remove: poteto-agent isolation worktree of a landed unit (check `git status` first) |
| `~/Workspace/dotfiles/.claude/worktrees/boundary-2026-10-22` | 3037430c | `orchestration/boundary-2026-10-22` | judge |
| `~/Workspace/dotfiles/.claude/worktrees/boundary-24b` | 6f71c21d | `orchestration/boundary-2026-10-19-24` | judge |
| `~/Workspace/dotfiles/.claude/worktrees/orchestrator-review` | 51f4b2f8 | `detached` | judge |
| `~/Workspace/dotfiles/.claude/worktrees/orchestrator-review-2` | b8013697 | `detached` | judge |
| `~/Workspace/dotfiles/.claude/worktrees/orchestrator-review-3` | 99a4a80f | `detached` | judge |
| `~/Workspace/dotfiles/.claude/worktrees/orchestrator-review-4` | e9bc99d2 | `detached` | judge |
| `~/Workspace/dotfiles/.claude/worktrees/orchestrator-review-5` | e9bc99d2 | `detached` | judge |
| `~/Workspace/dotfiles/.claude/worktrees/orchestrator-review-6` | e9bc99d2 | `detached` | judge |
| `~/Workspace/dotfiles/.claude/worktrees/orchestrator-review-7` | e9bc99d2 | `detached` | judge |
| `~/Workspace/dotfiles/.claude/worktrees/orchestrator-review-8` | 99b5f862 | `detached` | judge |
| `~/Workspace/dotfiles/.claude/worktrees/orchestrator-security-0e5d880` | 0e5d8807 | `detached` | judge |
| `~/Workspace/dotfiles/.claude/worktrees/orchestrator-security-c0f50fa` | c0f50fa1 | `detached` | judge |
| `~/Workspace/dotfiles/.claude/worktrees/orchestrator-security-fefa1dc` | fefa1dcc | `detached` | judge |
| `~/Workspace/dotfiles/.claude/worktrees/pr375` | c87546e9 | `detached` | judge |
| `~/Workspace/dotfiles/.claude/worktrees/records-sync-26` | 041a906b | `records/sync-dispatched-texts-26` | remove: old-regime records sync, clean, its PR merged |
| `~/Workspace/dotfiles/.claude/worktrees/records-sync-27` | 40b61c66 | `records/sync-dispatched-texts-27` | remove: old-regime records sync, clean, its PR merged |
| `~/Workspace/dotfiles/.claude/worktrees/records-sync-28` | 0b7e66ea | `records/sync-dispatched-texts-28` | remove: old-regime records sync, clean, its PR merged |
| `~/Workspace/dotfiles/.claude/worktrees/worker-c` | 5c6727af | `a03/pre-send-check` | remove after its PR row above is executed (old agmsg seat worktree, identity retired at X9) |
| `~/Workspace/dotfiles/.claude/worktrees/worker-d` | 9cb70cc5 | `tools/trusted-exec-contract-tests-a01` | remove after its PR row above is executed (old agmsg seat worktree, identity retired at X9) |
| `~/Workspace/dotfiles/.claude/worktrees/worker-e` | 5e1f1e7b | `tools/worker-write-boundary-a01` | remove after its PR row above is executed (old agmsg seat worktree, identity retired at X9) |
| `~/Workspace/dotfiles/.claude/worktrees/worker-f` | d961efa3 | `tools/hcom-dispatch-bus-a02` | remove after its PR row above is executed (old agmsg seat worktree, identity retired at X9) |
| `~/Workspace/dotfiles/.claude/worktrees/worker-g` | db968b84 | `tools/gh-binding-a02` | remove after its PR row above is executed (old agmsg seat worktree, identity retired at X9) |
| `~/Workspace/dotfiles/.claude/worktrees/worker-h` | c8c712f1 | `security/worker-sandbox-exclusions-a02` | remove after its PR row above is executed (old agmsg seat worktree, identity retired at X9) |

Counts: 18 open PRs; worktrees by group: agent 28, old-worker 6, records-sync 3, scratch 2, other 16.
