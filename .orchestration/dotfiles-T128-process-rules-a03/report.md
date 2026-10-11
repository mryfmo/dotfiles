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


## Bot round on `c4300f47` (review 5482300822, 07:15:16Z) and fix round 1

| Thread | Finding | Disposition |
|---|---|---|
| 4240646079 | P2, SKILL.md:201: after a fix push step 15 starts over, and `gh pr ready` exits non-zero on a PR that is already ready | `fixed:7524e001`: step 15 marks the PR ready "before the first wait, while it is still a draft"; `test_bot_fix_rounds_are_capped_and_the_pr_is_ready_first` pins it, and the proof fails (validation §5) |
| 4240646082 | P2, SKILL.md:71: a pre-dispatch review cannot check that a `closed:` selector names a test present in the PR tree | reported, not fixed: it is the threat-table rule's shape wording, the class the reset closed, which the task leaves to the orchestrator |

The worker resolves no thread. The final head's CI and Bot wait are in the RESULT and the main-checkout copy of this report.

## Notes

- Nothing here touches the threat-table rule's payload wording.
- The repository masker reads a unittest `subTest` label (the `token` keyword with a quoted value) as a secret pattern; an output line cut before its closing quote let one match run across lines and swallow evidence in an a02 draft. The pasted logs here keep every label on one line (at most 400 characters), and the masker's line count is checked before and after.
- Understand-Anything hook: did not fire. plan-mode-used: no.

## CompactionDB

`memory add` printed `ae486f65-e10d-44bd-8680-8261d6fa4492` (validation §4).

cost: n/a

## Revise round 1 (ACCEPTANCE 2026-10-11T22:20:55Z, final audit of `b7ae2d54`: incorrect; `previous_head=b7ae2d54`)

One commit on `docs/regime-pattern`, recorded in `revise.yaml` beside this report, after a fast-forward to `b7ae2d54` (the branch had taken two `update-branch` merges: PR 320's `0e522059` and PR 319's `52575497`). Each of the three worker-side findings gets a one-sentence rule fix, or pins, and the token test the ACCEPTANCE names:

1. P2 `SKILL.md:71` (thread 4240646082's class): the shape clause now reads "a `closed` selector names a test present in the PR tree at acceptance and in the schema's validation of the PR". After "…checks the three shape rules by hand." it adds: "For a `closed` row it checks the selector's form only, since the test does not exist before implementation." → `test_closed_selector_existence_is_checked_at_acceptance`.
2. P2 `SKILL.md:201` (thread 4243369347): Worker Playbook step 15 lists reviews and top-level comments with `.user.login=="chatgpt-codex-connector[bot]"`, not `.user.type=="Bot"`, and says "A human comment, a CodeRabbit review or an earlier head's review never ends the wait." → `test_the_bot_wait_filters_the_codex_bot`, which also asserts that `.user.type=="Bot"` is gone from step 15. My own Bot-wait script used the same any-Bot filter, so it now filters by the Codex login as well.
3. P2 `tests/…:259`: four existing sentences pinned, with no prose change: "S1 (…) and S2 (…) are decided from that output.", and the three shape rules (closed selector, out-of-scope owner, residual minimum) → `test_shape_rules_and_the_decision_sentence_are_pinned`.

The fourth finding (the sweep JSON) is the orchestrator's, as the ACCEPTANCE says. Every new or pinned sentence fails its test when removed, 9 of 9, the any-Bot filters and the old wait sentence pasted back among them (validation §7). The docs module runs 39 tests, OK. CompactionDB: `fa0f25f1-360c-463e-90f6-df466c8299c4`.

### Bot round on `386f97ff` (review 5485303545, 22:28:07Z) and fix round 1 (`114d5b91`)

| Thread | Finding | Disposition |
|---|---|---|
| 4243516879 | P1, SKILL.md:72: `scripts/regime-counters.sh` (A3, now on `main`) reads inline comments and commits only, so a Bot P0/P1 left in a review body would not reach S1 or S2 once "decided from that output" holds | `fixed:114d5b91`: the counters bullet adds "The script reads inline review comments only, so the orchestrator also counts the P0/P1-badged Bot review bodies of `…/pulls/<n>/reviews`, grouped by `commit_id`, by hand and pastes that command and its output beside the script's, until the script reads review bodies too." The script itself is outside this task's `allowed_files`, so reading `/reviews` there is a follow-up for its owner. `test_counters_add_review_body_findings` |
| 4243516880 | P2, SKILL.md:202: right after a push, `gh pr checks --watch` can exit 1 with `no checks reported` (cli/cli#7401) | `fixed:114d5b91`: step 15 says to start the watcher once a check is listed and to restart it on that message. `test_the_ci_watcher_survives_the_no_checks_race`; this seat's own watcher now waits for a listed check first |

Both proofs fail their tests (validation §8). The docs module runs 41 tests, OK. This is fix round 1 of 2 under the A2 cap; `386f97ff` is the first Bot P1 head after a03's RESULT `b9a9da7d`. The final head's CI and Bot wait are in the RESULT and the main-checkout copy of this report.
