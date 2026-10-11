# Report: dotfiles-T128-process-rules-a03

- Seat: `claude-standard-dot-a003` in `.claude/worktrees/worker-f`, branch `docs/regime-pattern`, PR #318. Second reset continuation of PR #318 (`reset_of: [dotfiles-T128-process-rules-a01, dotfiles-T128-process-rules-a02]`); a02 was reset under INV-6 after two Bot P1 heads past its RESULT `27ea99b2` (`108b43bd`, `97288f6f`) and the amendment threshold.
- Task file sha256 `867ea4ca…` checked against TASK 472 and copied byte-identical in `f4d45983` to `.orchestration/dotfiles-T128-process-rules-a03/task.md` (the `…-a01/` and `…-a02/` directories stay as history). It is the a02 text plus the fourth threat-table row (the PR controls its own test oracle) and the corrected citation of row 1 (INV-7).

## Carried over (on the branch before this task)

Items 1 to 5 (`c31b8327`, `3ff0cade`), the a02 revise round's five checks (`108b43bd`, `052eea4c`) and the three Bot P2 fixes of `21c160c8` stand unchanged, as the task says; their evidence is in `.orchestration/dotfiles-T128-process-rules-a02/`.

## This task's commits

- `798fa098` (made under a02, pushed as a03's first push on the orchestrator's answer of 06:59:22Z): Bot thread 4240598179 (P2, SKILL.md:183): "only the push leaves the sandbox" contradicted a Codex seat, which pushes from inside its sandbox and never leaves it. Worker Playbook step 2 now says "for a Claude seat only the push leaves the sandbox, and a Codex seat pushes from inside it (step 4)" → `test_workers_commit_inside_the_sandbox` asserts it; both proofs fail their test (validation §3).
- `f4d45983`: the task copy; then this evidence.

## Bot threads opened after the a02 RESULT

| Thread | Head | Finding | Disposition |
|---|---|---|---|
| 4240566259 | `108b43bd` | P1: the task records carry no `threat_table` | `fixed:e8d20aae` (a02 Amendment 1, three rows), now the a03 table of four rows in `f4d45983` |
| 4240566263 | `108b43bd` | P2: pin "revises once per pair of results" | `fixed:21c160c8` |
| 4240566266 | `108b43bd` | P2: step 2 must open the PR as a draft | `fixed:21c160c8` |
| 4240566268 | `108b43bd` | P2: pin "pastes its output into the acceptance record" | `fixed:21c160c8` |
| 4240598178 | `97288f6f` | P1: the boundary-merge sentence names the in-job decision, untrue on this tree until PR 320 merges | the orchestrator's ordering disposition (PING 06:59:22Z): PR 320 merges first and PR 318 takes the new base with `gh pr update-branch` before its audit; the sentence stays as it is |
| 4240598179 | `97288f6f` | P2: the push-only exit conflicts with Codex seats | `fixed:798fa098` |

The worker resolves no thread. The final head's CI and Bot wait are in the RESULT and the main-checkout copy of this report.

## Notes

- Nothing here touches the threat-table rule's payload wording.
- The repository masker reads a unittest `subTest` label (the `token` keyword with a quoted value) as a secret pattern; an output line cut before its closing quote let one match run across lines and swallow evidence in an a02 draft. The pasted logs here keep every label on one line (at most 400 characters), and the masker's line count is checked before and after.
- Understand-Anything hook: did not fire. plan-mode-used: no.

## CompactionDB

`memory add` printed `ae486f65-e10d-44bd-8680-8261d6fa4492` (validation §4).

cost: n/a
