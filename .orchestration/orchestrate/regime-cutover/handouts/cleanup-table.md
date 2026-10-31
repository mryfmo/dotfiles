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
| #606 | `records/sync-16` | 2026-10-31 | 20 | chore(records): regime-cutover sync 16 | close: superseded by records sync 17: the regime check refused the store at U126 (three correct audit rows reached the round cap; the mechanism-change row of 2026-10-31T04:51:47Z fixes it) |
| #607 | `records/sync-17` | 2026-10-31 | 21 | chore(records): regime-cutover sync 17 | close: superseded by records sync 18: the records lever's masker (U107) crossed two tabs in ledger row 207 so the copy had 5 columns and the regime check refused it; U107b bounds the masked value to its field |
| #615 | `records/sync-20` | 2026-10-31 | 16 | chore(records): regime-cutover sync 20 | close: superseded by records sync 21: the regime check refused the store at U20 (three correct sync audits since the rule date reached the round cap of standing order 36 with no mechanism-change row; the row of 2026-10-31T10:25:42Z, residual, names the per-sync counting as the follow-up) |

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

## Added 2026-10-24T13:4xZ (U44, worker-2-rosa)

Inventory from `gh pr view`, `gh pr list --state open`, `git worktree list --porcelain`, `git status --porcelain`, `ls` and a scratch copy of the pilot's `hcom.db` (all read-only); the rows above stay as they are. Nothing here was run. Run each row from the operator's shell, outside any seat; the `precondition` is the check to repeat first.

| item | command (operator, as written) | removes | why safe | precondition | source | dry-run |
| --- | --- | --- | --- | --- | --- | --- |
| PR #500 | `gh pr close 500 --delete-branch --comment "Superseded by #501 (U41b), merged as a3dd80dc."` | the open PR #500 and its branch `test/tailscale-case-tracks-nothing` | #501 (branch `test/tailscale-case-tracks-nothing-u41`) merged 2026-10-24T12:34:27Z as `a3dd80dc` from head `ef3f82d7`; #500's branch head is the same `ef3f82d7` (`git ls-remote --heads origin test/tailscale-case-tracks-nothing`), so nothing on it is unmerged | `gh pr view 500 --json state` → `OPEN`; `gh pr view 501 --json state` → `MERGED` | `gh pr close --help` (`-d, --delete-branch`, `-c, --comment`) | operator-only: a GitHub write; seats may not close PRs (standing order 3) |
| U33 pilot scratch: hcom store | `rm -rf ~/.local/state/hcom/kit-pilot` | the pilot's hcom store (352K: `hcom.db`, `config.toml`, `env`, `origin`, `shell_env.json`, `archive/`, `integrations/`, `launches/`, `.tmp/`) | the store has 0 rows in `instances` and 34 `events`, the last at 2026-10-24T09:53:51Z (read from a scratch copy); its `origin` names the pilot checkout in `$TMPDIR`; no dotfiles seat uses it (the live seats are on `~/.local/state/hcom-regime`) | `sqlite3 -readonly ~/.local/state/hcom/kit-pilot/hcom.db 'select count(*) from instances'` → `0` | README.md:974 (the derived store `~/.local/state/hcom/<slug>`) | operator-only: deletes host state (brief U44 FORBIDDEN) |
| U33 pilot scratch: seats root and checkout | `rm -rf ~/.local/state/omp-seats/kit-pilot /private/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/u33-pilot.w8DJ` | the pilot's worker seat worktree (`kit-pilot/worker`, detached `cd386a7`) and the pilot repository it belongs to (`master` `cd386a7` "kit-pilot: one commit", no remote) | the brief said the `$TMPDIR` checkout is gone; it is not (`ls -la` shows `.git` and `.orchestration`), so both go together: removing only the seats root would leave a stale worktree entry in the pilot repo, removing both leaves none; neither is a worktree of the dotfiles repository | `git -C /private/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/u33-pilot.w8DJ/kit-pilot worktree list` → the checkout and `~/.local/state/omp-seats/kit-pilot/worker`, nothing else | README.md:974 (seat worktrees `~/.local/state/omp-seats/<slug>/<seat>`) | operator-only: deletes host state |
| stopped seat worktree `~/.local/state/omp-seats/dotfiles/audit` | `git -C ~/Workspace/dotfiles worktree remove ~/.local/state/omp-seats/dotfiles/audit && rmdir ~/.local/state/omp-seats/dotfiles` | the worktree of the stopped audit seat kimi (detached `67029e60`, the U43 head, squash-merged in `c84070db`) and its empty parent | kimi is stopped (`hcom list --stopped kimi` → `Reason: killed`, 2026-10-24T13:24:55Z); the tree is clean (`git status --porcelain` → 0 entries) and `git worktree remove` refuses a dirty tree; it also occupies `dotfiles/audit`, the target of the one-time store move's `worktree move` (README.md:988) | kimi still stopped; `git -C ~/.local/state/omp-seats/dotfiles/audit status --porcelain` empty | `git worktree remove` (git-worktree(1): refuses unclean trees without `--force`) | operator-only: deletes host state |
| `/private/tmp/claude-501/records-sync-6` | `git -C ~/Workspace/dotfiles worktree remove /private/tmp/claude-501/records-sync-6` | the records sync 6 worktree (`records/program-store-6`, `1e9fca43`) | its PR #489 merged 2026-10-24T06:31:32Z; the tree is clean | `git -C /private/tmp/claude-501/records-sync-6 status --porcelain` empty | git-worktree(1) | operator-only: deletes host state |
| `~/Workspace/dotfiles/.claude/worktrees/agent-aef8f310d7f4c14e2` | `git -C ~/Workspace/dotfiles worktree remove ~/Workspace/dotfiles/.claude/worktrees/agent-aef8f310d7f4c14e2` | the isolation worktree of `ci/public-bootstrap-apt-mirror` (`f225d5d2`) | its PR #480 merged 2026-10-24T00:21:24Z; no open PR has the branch; the tree is clean | `git -C <path> status --porcelain` empty | git-worktree(1) | operator-only: deletes host state |
| `/private/tmp/u38b-base` | after U38b lands: `git -C ~/Workspace/dotfiles worktree remove /private/tmp/u38b-base` | a detached worktree at `039f7e98` (U38's merge, U38b's base) | clean; U38b (PR #505) is in flight, so keep it until its MERGED line | U38b `landed` in units.tsv; `git -C /private/tmp/u38b-base status --porcelain` empty | git-worktree(1) | operator-only: deletes host state |
| U1 pilot profile `~/.omp/profiles/pilot-bridge` (U1 operator steps 1 to 4, now obsolete) | `rm -rf ~/.omp/profiles/pilot-bridge` | the U1 pilot omp profile (9.1M: `agent/agent.db`, `claude-bridge.log`, `cc-cli-logs/`, `models.db`, `cache/`, `logs/`, `run/`), last written 2026-10-23 12:52 local | the bridge route is live through the `worker` and `orchestrator` profiles (`claude-bridge/claude-opus-5-5`, `claude-bridge/claude-fable-5-1`); nova's transcript holds 1203 bridge turns, 1072 of them `toolUse`, which is what U1 rows 1 and 2 were to show; nothing under `home/`, `scripts/`, `install/` or `Makefile` names `pilot-bridge` (`grep -rn`); keep `claude-bridge.log` first if the U1 report should keep its raw log | no omp process runs with `--profile pilot-bridge` (`pgrep -fl 'profile pilot-bridge'` empty) | handouts/U1-operator-steps.md (the obsolete note) | operator-only: seats never modify `~/.omp` (standing order 4) |
