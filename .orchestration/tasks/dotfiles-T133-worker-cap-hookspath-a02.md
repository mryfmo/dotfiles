---
format: 2
task_id: dotfiles-T133-worker-cap-hookspath-a02
kind: code
security: true
allowed_files:
  - home/dot_agents/agent-config.yaml
  - home/dot_local/bin/common/executable_herdr-agents
  - home/dot_agents/skills/agmsg-orchestration/SKILL.md
  - tests/unit/test_herdr_agents.py
  - .orchestration/dotfiles-T133-worker-cap-hookspath-a02/**
after: []
reset_of: [dotfiles-T133-worker-cap-hookspath-a01]
threat_table:
  - control: "home/dot_agents/agent-config.yaml (the worker_cap: 4 key beside worker_worktree and its explanatory comment)"
    disposition: "closed: tests/unit/test_herdr_agents.py::test_the_skill_names_the_manifest_worker_cap"
  - control: "home/dot_local/bin/common/executable_herdr-agents (the cap, exclusive lock through registration, absolute common-directory lock path and absence of Git configuration writes)"
    disposition: "residual: the tests in items 5 and 6 exercise refusal, re-seating, concurrent registration, separate-git-dir locking and absence of configuration writes; the final-head audit and security review assess their combined coverage."
  - control: "home/dot_agents/skills/agmsg-orchestration/SKILL.md (only the two cap sentences)"
    disposition: "closed: tests/unit/test_herdr_agents.py::test_the_skill_names_the_manifest_worker_cap"
  - control: "tests/unit/test_herdr_agents.py (the retained cap tests and the separate-git-dir regression test)"
    disposition: "residual: temporary repositories, a temporary HOME, fake agmsg scripts and fake Herdr exercise the launcher without changing live topology; the audit reads the fixtures and their assertions."
  - control: ".orchestration/dotfiles-T133-worker-cap-hookspath-a02/** (the reset task's branch artifacts)"
    disposition: "residual: artifacts remain within this task's directory, carry command and head provenance, and are checked against the final diff and CI before acceptance."
  - control: "the task-file copy on the branch (.orchestration/dotfiles-T133-worker-cap-hookspath-a02/task.md) replaces the reset_of task's copy (.orchestration/dotfiles-T133-worker-cap-hookspath-a01/task.md)"
    disposition: "residual: the a02 copy is byte-identical to the dispatched text and its own SHA256 appears in the TASK and RESULT; the orchestrator verifies the replacement and byte identity before acceptance."
  - control: "the branch evidence records under .orchestration/dotfiles-T133-worker-cap-hookspath-a02/ (report.md, validation.md, sandbox.md, learning.md and measure.md)"
    disposition: "residual: the records distinguish historical evidence from final-head results, disclose the stale PR description and refused commands, and are read during the final-head audit."
  - control: task metadata
    disposition: "residual: the orchestrator checks the dispatched front matter with task-consistency-check C1 to C10 and C7b before dispatch and at acceptance; byte identity covers subsequent metadata changes."
  - control: metadata separators
    disposition: "residual: the YAML front matter is bounded by the first document separators and the dispatched-file byte comparison covers the complete task copy."
  - control: in-process effects
    disposition: "residual: add-worker runs on the host and serializes counting through identity registration; the no-configuration test checks that this change introduces no Git configuration writes, and live deployment remains subject to the operator's make update restriction."
  - control: workflow and interpreter or environment inputs
    disposition: "residual: no workflow or interpreter file changes; the deployed manifest uses the existing positive-digits parser, missing or malformed values print the explicit no-cap warning, and this task adds no hooks-path environment transport."
  - control: new or renamed scripts
    disposition: "residual: this task adds or renames no executable script; the audit compares the complete file inventory against allowed_files."
  - control: orchestrator effect merge
    disposition: "residual: the orchestrator merges only with gh pr merge --squash --match-head-commit <audited head> after the integration gate; no local merge or push to main is authorized."
  - control: orchestrator effect update-branch
    disposition: "residual: gh pr update-branch changes the head, so the required CI, feedback sweep, task-level audit and security review bind the resulting final head before the gate."
  - control: orchestrator effect forced worker removal
    disposition: "residual: no forced removal is planned; any forced removal follows the existing dirty-worktree rule and records the discarded uncommitted state in the acceptance record."
premises:
  - claim: the SKILL states the cap as three in two sentences while four seats are registered, the mismatch P1-7 removes
    command: /usr/bin/grep -c -E 'Keep at most three workers in total|Keep about three concurrent workers at most' home/dot_agents/skills/agmsg-orchestration/SKILL.md
    output: |-
      2
  - claim: the manifest has no worker_cap today
    command: /usr/bin/grep -c '^worker_cap:' home/dot_agents/agent-config.yaml
    output: |-
      0
  - claim: the #393 branch (stopped under D4) holds the cap check and its tests, the material this task reuses
    command: git grep -c worker_cap 9c07098147d3b16d68a9be2772fbcba2460b8851 -- home/dot_local/bin/common/executable_herdr-agents tests/unit/test_herdr_agents.py home/dot_agents/agent-config.yaml
    output: |-
      9c07098147d3b16d68a9be2772fbcba2460b8851:home/dot_agents/agent-config.yaml:1
      9c07098147d3b16d68a9be2772fbcba2460b8851:home/dot_local/bin/common/executable_herdr-agents:4
      9c07098147d3b16d68a9be2772fbcba2460b8851:tests/unit/test_herdr_agents.py:11
  - claim: herdr-agents mentions core.hooksPath only in comments today and sets none
    command: /usr/bin/grep -c 'hooksPath' home/dot_local/bin/common/executable_herdr-agents
    output: |-
      2
---

# AGMSG-TASK dotfiles-T133-worker-cap-hookspath-a02 — INV-6 reset of dotfiles-T133-worker-cap-hookspath-a01 (plan 006 S2; plan 024 P1-7)

This text is the independent redesign by a review-profile context other than the author of a01. Plan 006 INV-6 stopped a01 at S2 after three changes to its task text. The task-level audit of `c96697ae309afbe67527f53f5006fe24f055982a` returned `incorrect`. The earlier local review and worker report remain historical evidence.

PR #408 continues under this task on the same branch, `tools/worker-cap-hookspath-a01`. The implementation at `c96697ae309afbe67527f53f5006fe24f055982a` is the starting point. The next push replaces `.orchestration/dotfiles-T133-worker-cap-hookspath-a01/task.md` with this dispatched text's byte-identical copy at `.orchestration/dotfiles-T133-worker-cap-hookspath-a02/task.md`. The orchestrator handles removal of the predecessor task copy as reset bookkeeping; worker edits remain within `allowed_files`. The a01 acceptance history retains its stopped status and original counters.

The four premises preserve a01's write-time observations verbatim. Validation below records the redesigned final head separately. The reusable cap material originated at `9c07098147d3b16d68a9be2772fbcba2460b8851` on the stopped #393 branch.

## Goal

`herdr-agents --add-worker` enforces the deployed manifest's `worker_cap: 4`, with counting and registration under one exclusive lock, and the SKILL names that manifest cap. Ordinary main checkouts and main checkouts created with `git init --separate-git-dir` use the repository's actual common Git directory for the lock. This task introduces no hooks-path configuration and no Git configuration write.

## Files

1. `home/dot_agents/agent-config.yaml` contains `worker_cap: 4` immediately after `worker_worktree`, with the existing-style comment explaining the maximum number of seated worker worktrees and the deployed `~/.agents/agent-config.yaml` source. Other manifest values remain unchanged. `make render-check` and `make validate-agent-assets` accept the key without renderer or validator changes. A validator refusal produces a `status=blocked` PONG with the command and output.

2. `home/dot_local/bin/common/executable_herdr-agents` enforces the cap in add-worker mode after the main-checkout check and before `write_spawn_options`. A seat is a registered Git worktree under `.claude/worktrees/` holding a `claude-code` or `codex` agmsg identity; a worktree holding both counts once. Re-seating an existing seat adds none. The deployed manifest's cap uses the existing positive-digits-only `sed` parser. A missing or malformed key prints `no worker_cap in <path>; no cap enforced.` on stderr and continues. An unseated target with `seats >= cap` prints `worker_cap is <cap> and <n> worker seats are registered; remove one with --remove-worker first.` and exits 2 before any Herdr or agmsg write. One exclusive `flock` covers the count, `ensure_worker_identity`, `ensure_worker_worktree` and the registration completed by `spawn.sh`. A concurrent invocation waits and recounts after the first registration. The lock remains held through the spawn wait and is released afterwards. Item 6 defines its path.

3. `home/dot_agents/skills/agmsg-orchestration/SKILL.md` changes only the two cap sentences. The first becomes ``Keep at most `worker_cap` workers (4 in the manifest today); raw herdr topology commands stay forbidden (T21 G7).`` The second becomes ``Keep at most `worker_cap` workers in total (4 in the manifest today; `herdr-agents --add-worker` refuses the next seat).`` Its following sentence, ``Seat workers with `herdr-agents --add-worker` only up to that cap.``, stays in place. The remaining text of both bullets stays unchanged. The rule file `home/dot_config/claude/rules/agmsg-orchestration.md` remains unchanged.

4. The launcher retains the cap sentence in its add-worker header documentation. This task contains no added `extensions.worktreeConfig`, `config --worktree`, `core.hooksPath` setting, hooks-path spawn environment, or seat-specific hooks configuration. The launcher writes no Git configuration. The hooks-path feature belongs to the separate task `dotfiles-T133-worker-hooks-path-a01`. The failed caller-environment transport design is not reused.

5. `tests/unit/test_herdr_agents.py` retains the four tests from the reduced a01 implementation in the existing fixture style, using a temporary HOME, temporary repositories, fake agmsg scripts and fake Herdr. `test_add_worker_refuses_a_seat_beyond_the_manifest_worker_cap` covers the missing and malformed-key warning, refusal of a fifth seat at cap four without mutating fake calls, and successful re-seating. `test_add_worker_cap_count_and_registration_are_serialized_under_one_lock` starts two additions with one free seat, slows fake identity registration, and asserts exactly one success, one refusal and one new registration; holding the lock prevents counting until release. `test_add_worker_writes_no_git_configuration` records Git invocations and verifies that neither the common repository nor the worker worktree gains `extensions.worktreeConfig` or `core.hooksPath`. Its red reference is `982eeee02b22b0eae3cf5fc21fe48fd74791993e`. `test_the_skill_names_the_manifest_worker_cap` checks the manifest value and both exact cap sentences. Historical red evidence for retained tests carries the tested commit and command; their green results are rerun on this task's final head. `tests/unit/test_agmsg_orchestration_docs.py` passes unchanged.

6. The implementation P2 at launcher line 1832 is fixed by deriving the lock directory with `git -C "${workdir}" rev-parse --path-format=absolute --git-common-dir` and opening `herdr-agents-seat.lock` beneath that absolute directory. The launcher never constructs this path from a literal `${workdir}/.git`. The existing main-checkout predicate stays unchanged. The new `test_add_worker_uses_git_common_dir_for_the_seat_lock` creates a real temporary checkout with `git init --separate-git-dir`, asserts that its `.git` is a file and its resolved common directory is absolute, and uses the real common-directory lock. With that lock held, add-worker waits before counting or registration; after release, it seats the worker successfully and enforces the cap on the next unseated target. The concurrency fixture also derives its lock path through Git. The new regression test is written first, is red against `c96697ae309afbe67527f53f5006fe24f055982a` at the failing lock redirection, and is green after the path fix. Both results and their commands appear in `validation.md`.

7. The ownership P2 on the a01 acceptance record is corrected explicitly. Advisory row `4305808095` is the separate-git-dir lock-path defect and belongs to `dotfiles-T133-worker-cap-hookspath-a02`, through item 6. The a01 owner task, `dotfiles-T133-worker-cap-hookspath-followup-a01`, withdraws its item for that row in favour of item 6; no fix to `is_main_checkout` is prescribed for it. The orchestrator records the withdrawal and corrected ownership in the acceptance records, outside the worker's edit boundary. The red evidence is the old acceptance disposition assigning the defect to `is_main_checkout`; item 6's red-then-green regression demonstrates the actual cause. A read-only record check is green when the corrected acceptance record assigns `4305808095` to this task, names item 6's test and final fix commit, and records the predecessor owner's withdrawal. The worker's report names this correction and the orchestrator supplies the record evidence before acceptance.

8. The PR-description P2 is handled through accurate scope evidence under the live no-prompt rule. The worker writes `.orchestration/dotfiles-T133-worker-cap-hookspath-a02/report.md` with the final scope: manifest cap four, serialized registration, the common-directory lock-path fix, the two SKILL cap sentences, the tests, and no hooks-path configuration or Git configuration writes. The report names the final head and this task's hash and identifies the old PR description as stale. `gh pr edit` matches a live ask rule and prompts the operator, so no command edits the PR body. No API, browser or alternate command performs that edit. The orchestrator's acceptance record states that PR #408's description is stale and is corrected when the ask rule is gone. A read-only evidence assertion checks that the report states the final scope and the acceptance record explicitly acknowledges the stale description and its correction condition. That assertion is recorded red before those records are corrected and green after they contain the required statements. The live description is never reported as fixed by this push.

## Out of scope

The hooks-path feature belongs to `dotfiles-T133-worker-hooks-path-a01`. `.githooks/*`, upstream agmsg and Herdr transport, the integration seat, the pre-RESULT gate, the receipt verifier, renderer and validator changes, the rule file, `--remove-worker`, model or profile arguments, permission or hook defaults, and cap six remain outside this task. The worker does not edit the predecessor task's canonical text, acceptance records or owner task. The orchestrator performs the reset and ownership bookkeeping described above.

## Check

The validation file contains the commands, verbatim output, exit statuses and tested heads for `make render-check`, `make validate-agent-assets`, `make format`, `shellcheck home/dot_local/bin/common/executable_herdr-agents`, `shfmt -d home/dot_local/bin/common/executable_herdr-agents`, and `uv run python -m unittest tests.unit.test_herdr_agents tests.unit.test_agmsg_orchestration_docs -v`. The launcher checks are clean and the unit modules are green. Any inherited failure is reproduced against the unchanged base and recorded as a failure with that evidence; it is never labelled a passing check or repaired outside `allowed_files`.

The validation includes item 6's real separate-git-dir proof, the retained no-configuration proof, and the red-then-green evidence and record checks for items 6 to 8. No local `bats` test runs. GitHub Actions supplies any required Bats result.

`git diff --numstat origin/main...HEAD` shows at most 200 changed lines outside `tests/` and `.orchestration/`, and at most 360 changed lines under `tests/`. Changed lines are additions plus deletions. `measure.md` records those totals and the final changed-file inventory. The orchestrator runs the format-2 task-consistency checker, including C1 to C10 and C7b, before dispatch and at acceptance.

## Completion

One branch, `tools/worker-cap-hookspath-a01`, carries this task and continues PR #408. The next push contains the replacement a02 task copy. No second implementation PR or fresh branch is created for this reset.

The Completion clause of `.orchestration/tasks/dotfiles-T129-normalised-comparison-lint-a01.md` applies as written, with `dotfiles-T133-worker-cap-hookspath-followup-a01` as the owner of any advisory P2 and `task_copy=<sha256 of .orchestration/dotfiles-T133-worker-cap-hookspath-a02/task.md>` in the RESULT. Row `4305808095` is owned and fixed by this task as item 6 states. Every worker-side fix round, before or after the first RESULT, counts toward INV-6 under C-61. The a01 history remains stopped and is not rewritten to exclude its earlier rounds.

A Codex seat writes its evidence at the same relative paths in its own worktree and says so in the RESULT. Worker-side review evidence uses the required `-worker-` infix. The report and RESULT identify the head, base, branch, changed files, tests, caps, task-copy hash, feedback dispositions and evidence paths. The orchestrator copies worktree evidence by absolute path before review.

This task is `security: true`. The orchestrator runs the task-level audit and a separate security-profile review on the final head before the gate. Final-head CI, the feedback sweep, audit dispositions, acceptance record and gate follow Orchestrator Playbook step 10 in its prescribed order. A changed head receives the required fresh evidence.

The no-prompt rule governs the inherited review workflow. No `@codex review` comment, `gh pr edit` or `gh pr comment` is issued. Automatic reviews are observed for the bounded window; absence after 15 minutes is recorded as `bot: none`. No write-form API command bypasses a live ask rule. Commands for `gh` and Git writes run individually, without shell chaining or a wrapper combining them.

The live launcher changes only at the operator's `make update`, which plan 024 forbids until the merge-gate replacement lands. The report and RESULT state that restriction. The acceptance record carries the ownership correction and the acknowledgement that PR #408's description remains stale until the ask rule is gone.

## Checks (pasted by the orchestrator before each send)

```
dotfiles-T133-worker-cap-hookspath-a02.md: OK
premises: the a01's four, outputs pasted at write time (2026-10-18 13:3x JST)
redesigned by the codex review profile (headless, read-only) at 2026-10-18T07:03Z as the INV-6 reset of a01 with the audit of c96697ae folded in; checked and dispatched by the orchestrator
```

Live Herdr and local Bats are not exercised by this task. A missing or malformed deployed `worker_cap` leaves additions uncapped with an explicit warning.