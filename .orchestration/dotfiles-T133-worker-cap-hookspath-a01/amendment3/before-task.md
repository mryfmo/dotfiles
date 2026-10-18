---
format: 2
task_id: dotfiles-T133-worker-cap-hookspath-a01
kind: code
security: true
allowed_files:
  - home/dot_agents/agent-config.yaml
  - home/dot_local/bin/common/executable_herdr-agents
  - home/dot_agents/skills/agmsg-orchestration/SKILL.md
  - tests/unit/test_herdr_agents.py
  - .orchestration/dotfiles-T133-worker-cap-hookspath-a01/**
after: []
threat_table:
  - control: "the PR edits home/dot_agents/agent-config.yaml in one place (item 1: the key worker_cap: 4 with its comment beside worker_worktree; nothing else)"
    disposition: "closed: tests/unit/test_herdr_agents.py::test_the_skill_names_the_manifest_worker_cap"
  - control: "the PR edits home/dot_local/bin/common/executable_herdr-agents for item 2 (the add-worker cap check read from the deployed manifest, refusing a seat beyond worker_cap)"
    disposition: "closed: tests/unit/test_herdr_agents.py::test_add_worker_refuses_a_seat_beyond_the_manifest_worker_cap"
  - control: "the same launcher edit for item 2's lock (Amendment 1: the seat count and the seat's registration run under one exclusive flock on a file in the repository's common git dir, so two concurrent add-worker runs cannot both count below the cap)"
    disposition: "closed: tests/unit/test_herdr_agents.py::test_add_worker_cap_count_and_registration_are_serialized_under_one_lock"
  - control: "the same launcher edit for item 3 (Amendment 2: core.hooksPath=.githooks reaches the worker only through the worker pane's environment, GIT_CONFIG_COUNT, GIT_CONFIG_KEY_0 and GIT_CONFIG_VALUE_0 in the spawn environment; no git config file is written and extensions.worktreeConfig is never enabled, so the host's git never loads worker-writable configuration)"
    disposition: "closed: tests/unit/test_herdr_agents.py::test_add_worker_passes_the_hooks_path_in_the_worker_environment_and_writes_no_git_config"
  - control: "the PR edits home/dot_agents/skills/agmsg-orchestration/SKILL.md in two sentences (item 4: the two cap sentences name the manifest's worker_cap with its current value; no other text)"
    disposition: "closed: tests/unit/test_herdr_agents.py::test_the_skill_names_the_manifest_worker_cap"
  - control: "tests/unit/test_herdr_agents.py (the three tests of item 5, in the file's existing fixture style: a temporary HOME, fake agmsg scripts and a fake herdr on PATH)"
    disposition: "residual: fakes only, no live Herdr or bus; the audit reads each case"
  - control: the task-file copy on the branch (.orchestration/dotfiles-T133-worker-cap-hookspath-a01/task.md)
    disposition: "residual: byte-identical to the dispatched file (its sha256 is in the TASK line); the orchestrator compares at acceptance"
  - control: "the branch evidence records under .orchestration/dotfiles-T133-worker-cap-hookspath-a01/ (report.md, validation.md, sandbox.md, learning.md)"
    disposition: "residual: prose and pasted command output; the sandbox record lists every command the sandbox refused; the audit reads them"
  - control: "task metadata (the front matter of the task copy: kind, security, allowed_files, threat_table, premises)"
    disposition: "residual: read with PyYAML by the task-consistency check C1 to C10 and C7b before dispatch and at acceptance; a changed field fails the byte comparison above"
  - control: metadata separators (the --- lines that bound the front matter of the task copy and of every evidence record)
    disposition: "residual: PyYAML splits on the first document only and the byte comparison covers the whole file"
  - control: in-process effects
    disposition: "residual: herdr-agents runs on the host at add-worker time; the new writes are one git config in the worker worktree and, once, extensions.worktreeConfig in the common config; the tests run the script against temporary repositories; nothing changes on this Mac until the operator's make update after the merge"
  - control: workflow and interpreter or environment inputs
    disposition: "residual: no workflow or interpreter file is in allowed_files; the cap is read from ~/.agents/agent-config.yaml with a digits-only sed as the #393 branch did, so a malformed value means no cap and a printed warning, never an unbounded seat count by silence"
  - control: new or renamed scripts
    disposition: "residual: none; any new or renamed script is an undeclared change the audit fails"
  - control: orchestrator effect merge
    disposition: "residual: merge only through gh pr merge --squash --match-head-commit <audited head> after the gate (Orchestrator Playbook step 10.5); never a local merge or a push to main"
  - control: orchestrator effect update-branch
    disposition: "residual: gh pr update-branch moves the head, so CI, the sweep and the audit run again on the new head before any gate (Orchestrator Playbook step 10)"
  - control: orchestrator effect forced worker removal
    disposition: "residual: none planned; herdr-agents --remove-worker refuses a dirty worktree without --force, and a forced removal is recorded in the acceptance record with the uncommitted state it discarded"
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

# AGMSG-TASK dotfiles-T133-worker-cap-hookspath-a01 — the numeric worker cap and the worktree hooks path (plan 024 P1-7)

Written 2026-10-18 by the orchestrator seat from plan 024 (wave P-W1 brought forward to P-W0 after D3 branched to (d), `024-todo.md` row P1-7, `024-design-programs.md` item (9), decision D-024-10: cap 4 now, 6 once spark's second seat runs). Seat: codex-standard-dot-a010 (worker-e). The SKILL says three, the regime runs four; the launcher enforces nothing. Routing: `herdr-agents` and the manifest's worker keys are launch surface, not a seat's execution boundary; a Codex seat edits them. The material is PR #393's branch `tools/integration-seat-result-gate-cap` at 9c07098147d3b16d68a9be2772fbcba2460b8851 (stopped under D4): reuse its cap check and tests, leave its integration seat, pre-RESULT gate and receipt verifier (owned by P1-4 and P1-5).

## Goal

`herdr-agents --add-worker` refuses a seat beyond the manifest's `worker_cap`, every worktree it seats runs the repository's `.githooks`, and the SKILL states the cap as the manifest's number.

## Files

1. `home/dot_agents/agent-config.yaml`: after `worker_worktree`, the key `worker_cap: 4` with a comment in the file's style (the number of seated worker worktrees `herdr-agents --add-worker` allows; read from the deployed `~/.agents/agent-config.yaml`; D-024-10). Nothing else; `make render-check` and `make validate-agent-assets` stay green without a renderer or validator change (confirm and paste; a refusal of the key by the validator is a `status=blocked` PONG, not a validator edit).
2. `home/dot_local/bin/common/executable_herdr-agents`, add-worker mode, after the main-checkout check and before `write_spawn_options`: the cap check of 9c07098 lines 1830 to 1848 (Amendment 1: not byte for byte; the count and the registration that follows run under one exclusive `flock` on `${workdir}/.git/herdr-agents-seat.lock`, held from the count through `ensure_worker_identity` and `ensure_worker_worktree`, so a concurrent add-worker waits and recounts) (a seat is a `.claude/worktrees/` worktree holding a claude-code or codex agmsg identity; re-seating a seated worktree adds none; `worker_cap` read with the digits-only `sed`; no key prints `no worker_cap in <path>; no cap enforced.` on stderr and continues; `seats >= cap` for an unseated worktree prints `worker_cap is <cap> and <n> worker seats are registered; remove one with --remove-worker first.` and exits 2 before any Herdr or agmsg write).
3. (Superseded by Amendment 2; the original text is kept for the record.) Same script, after `ensure_worker_worktree` returns the seat directory: `git -C "${workdir}" config --bool extensions.worktreeConfig true` when `git -C "${workdir}" config --get extensions.worktreeConfig` is not `true` (once per repository; the common config is the host's to write), then `git -C "${seat_dir}" config --worktree core.hooksPath .githooks` (per worktree; the main checkout's hooks are untouched; a missing `.githooks` directory runs no hook, and P1-5 adds the hooks). Verify both commands in a temporary repository before relying on them and paste the proof (`git config --worktree` needs the extension; `git -C <wt> config --get core.hooksPath` prints `.githooks` in the worktree and nothing in the main checkout). `--remove-worker` leaves the setting (the worktree is removed with it). The header's add-worker description gains one sentence for the cap and one for the hooks path.
4. `home/dot_agents/skills/agmsg-orchestration/SKILL.md`: the sentence `Keep about three concurrent workers at most; raw herdr topology commands stay forbidden (T21 G7).` becomes `Keep at most `worker_cap` workers (4 in the manifest today); raw herdr topology commands stay forbidden (T21 G7).` and `Keep at most three workers in total. Seat workers with `herdr-agents --add-worker` only up to that cap.` becomes `Keep at most `worker_cap` workers in total (4 in the manifest today; `herdr-agents --add-worker` refuses the next seat). Seat workers with `herdr-agents --add-worker` only up to that cap.`; the parallel-workers bullet gains no other words. The rule file `home/dot_config/claude/rules/agmsg-orchestration.md` names no cap and is not touched.
5. `tests/unit/test_herdr_agents.py`, in the file's fixture style: `test_add_worker_refuses_a_seat_beyond_the_manifest_worker_cap` (from 9c07098 lines 2161 to 2210 adapted to this task: no manifest key → the warning and the seat proceeds; `worker_cap: 4` with four seated worktrees → exit 2 with the message and no Herdr or agmsg call recorded by the fakes; re-seating one of the four → proceeds), `test_add_worker_passes_the_hooks_path_in_the_worker_environment_and_writes_no_git_config` (Amendment 2, replacing the worktree-config test: one add-worker run against a temporary main checkout; the fake spawn.sh records its environment and shows `GIT_CONFIG_COUNT=1`, `GIT_CONFIG_KEY_0=core.hooksPath`, `GIT_CONFIG_VALUE_0=.githooks`; no `git config` write is recorded, and neither the common config nor the worktree's holds `extensions.worktreeConfig` or `core.hooksPath` afterwards; red on 982eeee0, which writes both), `test_the_skill_names_the_manifest_worker_cap` (from 9c07098 line 2212 without the integration-seat half: the manifest's `worker_cap` value appears in the two SKILL sentences as `(4 in the manifest today)` and both sentences say `worker_cap`), `test_add_worker_cap_count_and_registration_are_serialized_under_one_lock` (Amendment 1: two add-worker runs started together against a manifest cap one above the registered seats, the fake identities.sh slowed by a short sleep; exactly one proceeds and the other is refused with the cap message, asserted from the fakes' recorded argv and the two exit codes; a held lock makes a run wait rather than count). `tests/unit/test_agmsg_orchestration_docs.py` keeps passing unchanged (run it and paste).

## Out of scope

`.githooks/*` (P1-5), the integration seat and the receipt verifier (#393, P1-4), the validator and the renderer (in flight in #389 and #396), the rule file, `--remove-worker`, any model or profile argument, the cap value 6 (D-024-10, after spark).

## Check

`make render-check`, `make validate-agent-assets`, `make format`, `shellcheck` and `shfmt -d` on the launcher clean, `uv run python -m unittest tests.unit.test_herdr_agents tests.unit.test_agmsg_orchestration_docs -v` green, the temporary-repository proof of item 3, all pasted in the validation file, with `git diff --numstat origin/main...HEAD`: at most 160 changed lines outside `tests/` and `.orchestration/`, 320 under `tests/` (Amendment 1).

## Completion

One PR from a fresh branch off `origin/main` (`git switch -c tools/worker-cap-hookspath-a01 --no-track origin/main`; your worktree's current branch `feat/codex-local-review-exclusion` is PR #399's, closed under D5, and its 138 untracked evidence files under `.orchestration/` stay where they are). The Completion clause of `.orchestration/tasks/dotfiles-T129-normalised-comparison-lint-a01.md` applies as written, with `dotfiles-T133-worker-cap-hookspath-followup-a01` as the owner of any advisory P2 (written by the orchestrator when the first one appears) and `task_copy=<sha256 of .orchestration/dotfiles-T133-worker-cap-hookspath-a01/task.md>` in the RESULT. A Codex seat writes its evidence at the same relative paths in its own worktree and says so in the RESULT. This task is `security: true`: the orchestrator runs the task-level audit and a second review on the `security` profile on the final head before the gate (plan 024 5.11 Q-A). The live `herdr-agents` changes only at the operator's `make update`, which plan 024 (4) forbids until the merge-gate replacement lands; the RESULT states that.

## Checks (pasted by the orchestrator before each send)

```
dotfiles-T133-worker-cap-hookspath-a01.md: OK
premises 1 to 4: outputs pasted at write time (2026-10-18 13:3x JST)
masked 0 match(es) in .orchestration/tasks/dotfiles-T133-worker-cap-hookspath-a01.md
```

## Amendment 1 (round 1, 2026-10-18T04:54Z)

a010's blocked PONG (04:50:25Z) on PR #408 at ffd8454d, the Codex Bot's two P1: 4305767690 (the cap count and the registration are not serialized, so two concurrent add-worker runs can both count below the cap) and 4305767694 (the hooks-path change has no threat row naming its test). Authorized, the one worker-side fix round of Worker Playbook step 15: item 2 gains the exclusive `flock` on `${workdir}/.git/herdr-agents-seat.lock` held from the count through the registration (the 9c07098 block is reused, not copied byte for byte); item 5 gains `test_add_worker_cap_count_and_registration_are_serialized_under_one_lock`; the launcher's threat row is split into the cap row, the lock row and the hooks-path row, each closed by its own test; the caps rise by 40 and 70 lines. Copy this file as task.md on the branch (the byte identity is to this amended text), push the fix, `@codex review`, then RESULT; no third round.

## Amendment 2 (round 1, 2026-10-18T05:21Z) and the orchestrator's revise round 1

a010's RESULT (05:17:52Z, PR #408 at 982eeee0): the automatic Codex Security Review's P1 4305769826 survives the one worker-side fix round (`bot_rounds=2`, `operator_decision_required=yes`). The finding is correct: enabling `extensions.worktreeConfig` activates `.git/worktrees/<seat>/config.worktree`, a directory the Codex worker's sandbox can write, so a worker can set `core.fsmonitor` to an executable in its worktree and the host's `git status` in `herdr-agents --remove-worker` runs it unsandboxed (class `unbound-evidence`: the host trusts configuration from the worker's writable metadata). Decided by the orchestrator by default under the user's autonomy directive (2026-10-18 13:5x JST), as the orchestrator's revise round 1 of INV-6 (revises 0 to 1; the worker-side Bot round is plan 020 step 2's, counted apart): item 3 is redesigned, not patched. The hooks path reaches the worker only through the worker pane's environment (`GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=core.hooksPath GIT_CONFIG_VALUE_0=.githooks` added by `herdr-agents --add-worker` to the spawn environment beside `AGMSG_RESOLVE_PROJECT=0`), so the worker's own git runs `.githooks` from its worktree while no git config file is written anywhere and the host's git in that worktree loads nothing of the worker's; the `extensions.worktreeConfig` and `git config --worktree` lines leave. The threat row and item 5's test read accordingly; the previous test is removed. INV-6: amendments 2 (this one fixes a security P1 by design change, the second after the Bot's first round's lock), revises 1; a further amendment or revise on this task is a hold and a re-plan, never a third round (plan 024 section 7). `check=tests/unit/test_herdr_agents.py::test_add_worker_passes_the_hooks_path_in_the_worker_environment_and_writes_no_git_config` (red on 982eeee0). Copy this text as task.md, push once, wait for CI and the automatic reviews (no `@codex review` comment), then RESULT with `previous_head=982eeee02b22b0eae3cf5fc21fe48fd74791993e` in `.orchestration/<task>/revise.yaml` as the contract says.
