The scripts preserve the attached inputs’ behavior with the specified changes. All three input hashes and the task-copy hash match; every changed file is within `allowed_files`. GitHub confirms successful final-head Actions runs, including all three new tests within the 1,084-test unit suite. [PR #357](https://github.com/mryfmo/dotfiles/pull/357), [unit-test run](https://github.com/mryfmo/dotfiles/actions/runs/38569353137).

- [P1] high specification .orchestration/dotfiles-T128-chain-review-scripts-a01/task.md:38 `command -v` does not guarantee that the actual reviewer is selected before checkout: this host resolves `codex` to a mise shim, which selects its executable and environment when invoked from the PR worktree. With trusted project configuration or inherited mise trust overrides, PR configuration can execute code before the reviewer’s read-only sandbox starts. Pinning a concrete executable is necessary; the existing `orch-gate.sh` addresses this same boundary. [Mise shim behavior](https://mise.jdx.dev/dev-tools/shims.html), [configuration trust](https://mise.jdx.dev/security.html).

- [P2] high implementation scripts/orchestrator/local-review.sh:27 The unchecked task argument escapes the promised output directory: `task=../escape` writes `.orchestration/escape-local-review-<sha7>.md`; additional `../` components escape the repository. `local-advisory.sh:24` similarly permits appending outside `acceptance/`. Neither the scripts nor their tests establish the claimed write confinement.

- [P2] high implementation scripts/orchestrator/local-review.sh:62 `W` is interpolated directly into a sed program. A valid worktree path containing `[1]` fails literal prefix removal; `#` and newline characters can inject additional sed commands, including `w` with another output path. Read-only probes confirmed incorrect stripping and interpretation of an injected `p` command.

- [P2] high evidence tests/unit/test_chain_review_scripts.py:114 The decoy case proves resolution happens in the repository root, but does not prove it precedes checkout. Moving the resolution block below checkout while retaining the root cwd leaves every asserted result unchanged. The implementation’s ordering is correct; the test does not close that specific requirement.

- [P2] high orchestration .orchestration/validation/dotfiles-T128-chain-review-scripts-a01-pr-feedback.json:116 This disposition and the one at line 129 acknowledge valid defects and defer them to a follow-up task, without fixing or refuting them. Naming an owner does not satisfy AGENTS.md’s prohibition on deferral as a disposition. The same treatment appears in the acceptance record at lines 45–46.

- [P2] high evidence .orchestration/dotfiles-T128-chain-review-scripts-a01/sandbox.md:21 The record claims to list every unsandboxed call, but acceptance line 54 explicitly acknowledges omitted final-head `gh` reads and says they were left unrecorded to preserve the head. The supplied evidence therefore does not support its completeness claim.

- [P3] high evidence .orchestration/dotfiles-T128-chain-review-scripts-a01/report.md:5 The reported full base SHA is invalid: `git show` returns `bad object`. Validation line 28 and Git history identify the actual original base as `5ec860520075a2f0bbb551232de0f868e481a59c`.

The non-worktree-root test checks exit 2, no reviewer invocation, and unchanged main HEAD. The advisory and sandbox-scan tests cover their specified behavior. The sole task premise replays as `0`. Finding and sandbox text are processed as data without shell evaluation; task paths and environment inputs nevertheless defeat the broader command/write-confinement claim.

INV-2: holds .orchestration/dotfiles-T128-chain-review-scripts-a01/task.md:78 — the named cap obligation is met: 148 script lines, 230 test additions, four files outside `.orchestration/`.

Orchestration findings: 1

📝 まとめ: Completed the read-only audit; seven findings remain. No files were modified.
Not rerun: mutating tests, the mutation harness, or the real reviewer; the execution and write-boundary risks above remain.
Verdict: incorrect