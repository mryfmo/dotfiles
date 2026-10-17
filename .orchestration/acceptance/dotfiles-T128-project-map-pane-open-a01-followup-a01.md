---
{
  "audit_findings": [
    {
      "evidence": "shasum -a 256 .orchestration/tasks/dotfiles-T128-project-map-pane-open-a01-followup-a02.md (2bc357240403629a94e91f44a4e6cf6a2f95359ed621fa7f3f6dd8521ff83240)",
      "n": "1",
      "reason": "advisory P2 owned by dotfiles-T128-project-map-pane-open-a01-followup-a02 (the path-form class after the re-plan line, the same finding as 3288959:1: the suffix is checked after realpath, so a symlinked map is rejected; hook line 40)"
    },
    {
      "evidence": "shasum -a 256 .orchestration/tasks/dotfiles-T128-project-map-pane-open-a01-followup-a02.md (2bc357240403629a94e91f44a4e6cf6a2f95359ed621fa7f3f6dd8521ff83240)",
      "n": "2",
      "reason": "advisory P2 owned by dotfiles-T128-project-map-pane-open-a01-followup-a02 (the path-form class after the re-plan line, the same finding as 3288959:2: realpath keeps case on macOS; hook line 56)"
    },
    {
      "evidence": "sqlite3 ~/.agents/skills/agmsg/db/messages.db \"select created_at, substr(body,1,160) from messages where to_agent='claude-deep-dot' and body like 'AGMSG-RESULT v1 task_id=dotfiles-T128-project-map-pane-open-a01-followup-a01%' order by id\" (three rows, pasted in the chain-6 section of the orchestrator's report)",
      "n": "3",
      "reason": "a record finding, never a merge stop (C-61), and the auditor is right about the record: the 3288959:3 line above called the third RESULT an update-branch head, but the bus holds three RESULTs with the code heads c0c3ff05 (round 1), 02fdf061 (round 2) and e234a05b (round 3, 07:44:35Z, the canonicaliser, guard and separator changes), so revises=2 are two real fix rounds and INV-6's cap of two is reached, not exceeded; the continuation after it was no further round (the heads 32889597 and 00048df are update-branch merges with no code change) and the re-plan line D-S1-379 of 10:08Z; the corrected S2 reading stands here and the 3288959:3 sentence is superseded by this line"
    }
  ],
  "dispatch": [
    "AGMSG-ACCEPTANCE v1 task_id=dotfiles-T128-project-map-pane-open-a01-followup-a01 status=accepted reason=merged:head-00048df7(the-update-branch-merge-of-32889597-onto-59db77bb)through-gate-and-gh-pr-merge-squash-match-head-commit-at-14:07:11Z,main-e9bc99d2;audit-of-00048df-incorrect-with-three-P2-dispositioned(two-advisory-under-dotfiles-T128-project-map-pane-open-a01-followup-a02,one-record-finding-corrected);the-live-check-of-the-hook-follows-the-operator-s-make-update next_action=none-for-this-task;the-branch-may-be-deleted;your-T130-work-continues read_at=unread"
  ],
  "format": 1,
  "head": "00048df75bbeb1f85cbce0b9c6fa5fac017b2fee",
  "ledger": [
    {
      "class": "path-form-normalisation",
      "id": "4300474045"
    },
    {
      "class": "path-form-normalisation",
      "id": "4300561777"
    },
    {
      "class": "path-form-normalisation",
      "id": "4301859324"
    },
    {
      "class": "path-form-normalisation",
      "id": "4301888204"
    },
    {
      "class": "path-form-normalisation",
      "id": "audit:990b607:1"
    },
    {
      "class": "record-counting",
      "id": "audit:990b607:2"
    },
    {
      "class": "evidence-checkpoint",
      "id": "audit:990b607:3"
    },
    {
      "class": "path-form-normalisation",
      "id": "audit:8607a87:1"
    },
    {
      "class": "live-verification",
      "id": "audit:8607a87:2"
    },
    {
      "class": "record-counting",
      "id": "audit:8607a87:3"
    },
    {
      "class": "path-form-normalisation",
      "id": "audit:3288959:1"
    },
    {
      "class": "path-form-normalisation",
      "id": "audit:3288959:2"
    },
    {
      "class": "record-counting",
      "id": "audit:3288959:3"
    },
    {
      "class": "path-form-normalisation",
      "id": "audit:00048df:1"
    },
    {
      "class": "path-form-normalisation",
      "id": "audit:00048df:2"
    },
    {
      "class": "record-counting",
      "id": "audit:00048df:3"
    }
  ],
  "pr": 379,
  "searches": [
    {
      "class": "path-form-normalisation",
      "records": []
    },
    {
      "class": "record-counting",
      "records": []
    }
  ],
  "task": "dotfiles-T128-project-map-pane-open-a01-followup-a01"
}
---

# Acceptance record: dotfiles-T128-project-map-pane-open-a01-followup-a01 (the residual findings of PR #359: the map tab matched to the event before the pane is declared present; plan 020 step 1; the owner task of the pane-open lineage; Codex seat)

- 2026-10-15T00:3xZ record created before the first dispatch (Orchestrator Playbook step 6). The task text was written when the Bot's first advisory P2 on PR #359 (thread comment 4277695198, head 73f51ab2) appeared, as the lineage task's Completion requires; its paired one-round review (brief `dotfiles-T128-project-map-pane-open-a01-followup-review-a01`) goes to the review seat and the Codex half; its two premises read `origin/main` and replay `absent` until the boundary that lands the lineage task file and the record's owner section; the dispatch follows that boundary, the hook follow-up's merge (the same four files, INV-10) and a one-round refresh of the premise outputs, to `codex-standard-dot-a004` (Claude-boundary files).
- 2026-10-15T00:34Z pair-confirmed on `ace9aebd46d6c440d90a41dd501cbe3fa6108c44ea1a39e5340196b39560b738` (one round): the Codex half's receipt `validation/dotfiles-T128-project-map-pane-open-a01-followup-review-a01-codex-r1.md` (`confirm`, no finding) and the review seat's `AGMSG-RESULT … round=1 verdict=confirm owner_task_sha256=ace9aebd…` at 00:34:23Z; ACCEPTANCE accepted to the seat. Premise 1 reads `present` (the lineage task file landed with boundary (15)); premise 2 reads `absent` until the boundary that lands the lineage record's owner section (one row today, `4277695198`, plus the audit row `audit:73f51ab:1`); the pre-boundary copy is kept under the orchestrator's glue directory for the refresh round. Dispatch order: after PR #359 merges, after the hook follow-up (the same four files) merges, after that boundary and the one-round premise refresh; to `codex-standard-dot-a004`.

re-plan: path-form-normalisation -> specification: the hook compares every tab URL and map path in one canonical form, the file URL that pathToFileURL(realpath) yields (home expanded, physical cwd, no trailing slash, percent-encoding as Node encodes it); design: one normaliser function on both sides of every comparison, no string form compared directly (plan 023 PR F2 lints the forms); implementation: the four fixes of rounds 2 and 3 (c0c3ff05, 02fdf061, 40d18027, e234a05b) route each input through that normaliser; verification: one test per form (encoded tilde, logical cwd, bare tilde, trailing slash, encoded separator) asserting identity of the normalised values, not absence of a mismatch. Written 2026-10-17T10:08Z by the orchestrator (D-S1-379, default A); the six path-form rows above are this one class.

## Ledger rows (id<TAB>class; read by the block writer)

Written 2026-10-17T10:25Z by the orchestrator (the chain 3 and 4 refusals of 2026-10-17 10:0xZ: the block writer reads tab rows, not the block): the four Bot threads of PR #379 and the six findings of the audits of 990b607 and 8607a87, six of them one class, which the re-plan line above covers.

4300474045	path-form-normalisation
4300561777	path-form-normalisation
4301859324	path-form-normalisation
4301888204	path-form-normalisation
audit:990b607:1	path-form-normalisation
audit:990b607:2	record-counting
audit:990b607:3	evidence-checkpoint
audit:8607a87:1	path-form-normalisation
audit:8607a87:2	live-verification
audit:8607a87:3	record-counting
audit:3288959:1	path-form-normalisation
audit:3288959:2	path-form-normalisation
audit:3288959:3	record-counting

## Owned by dotfiles-T128-project-map-pane-open-a01-followup-a02 (advisory P2 of the final head; plan 020 step 1.2; rows id<TAB>class)

local:3288959:1	advisory-p2
local-finding: 3288959:1 not-applicable:advisory P2 owned by dotfiles-T128-project-map-pane-open-a01-followup-a02 (- [P2] Check the map suffix before resolving its symlinks — home/dot_claude/hooks/executable_project-map-reload.sh:39-40); evidence=shasum -a 256 .orchestration/tasks/dotfiles-T128-project-map-pane-open-a01-followup-a02.md (2bc357240403629a94e91f44a4e6cf6a2f95359ed621fa7f3f6dd8521ff83240)
local:3288959:2	advisory-p2
local-finding: 3288959:2 not-applicable:advisory P2 owned by dotfiles-T128-project-map-pane-open-a01-followup-a02 (- [P2] Compare map identity on case-insensitive filesystems — home/dot_claude/hooks/executable_project-map-reload.sh:55-); evidence=shasum -a 256 .orchestration/tasks/dotfiles-T128-project-map-pane-open-a01-followup-a02.md (2bc357240403629a94e91f44a4e6cf6a2f95359ed621fa7f3f6dd8521ff83240)

## Audit of 32889597 (chain 5, Verdict: incorrect, three P2) dispositioned 2026-10-17T12:25Z

audit-finding: 3288959:1 not-applicable:advisory P2 owned by dotfiles-T128-project-map-pane-open-a01-followup-a02 (the path-form class after the re-plan line: the suffix is checked after realpath, so a symlinked map is rejected; hook line 40); evidence=shasum -a 256 .orchestration/tasks/dotfiles-T128-project-map-pane-open-a01-followup-a02.md (2bc357240403629a94e91f44a4e6cf6a2f95359ed621fa7f3f6dd8521ff83240)
audit-finding: 3288959:2 not-applicable:advisory P2 owned by dotfiles-T128-project-map-pane-open-a01-followup-a02 (the path-form class after the re-plan line: realpath keeps case on macOS, so case aliases compare unequal; hook line 56); evidence=shasum -a 256 .orchestration/tasks/dotfiles-T128-project-map-pane-open-a01-followup-a02.md (2bc357240403629a94e91f44a4e6cf6a2f95359ed621fa7f3f6dd8521ff83240)
audit-finding: 3288959:3 not-applicable:a record finding, never a merge stop (C-61): the INV-6 revises=2 threshold has its counter snapshot pasted below (S2 decided from it: two revises are the two rounds of the re-planned path-form class, both before the re-plan line; the third RESULT was the update-branch head); evidence=scripts/regime-counters.sh dotfiles-T128-project-map-pane-open-a01-followup-a01 --pr 379
- counters (`scripts/regime-counters.sh dotfiles-T128-project-map-pane-open-a01-followup-a01 --pr 379`, 2026-10-17T12:25Z):
  jq: parse error: Invalid numeric literal at line 1, column 2
  task=dotfiles-T128-project-map-pane-open-a01-followup-a01 tasks=2 amendments=1 questions=1 results=3 withdrawn=0 revises=2 first_result_head=c0c3ff05f50846d8f880b7ccfb54d0c74630adf4 bot_p1_heads_after_result=unknown audits=unknown wall=2026-10-17T00:15:37Z..2026-10-17T07:44:35Z (7:28) source=live
  S2: revises 2 >= 2 source=live
  S1: class=path-form-normalisation count=6 re-plan=present source=record
  detail: pr=379 authors=claude-deep-dot tasks=01a14736-d028-799d-817e-f8bb7293562b,01a148b2-b228-7b9d-8d50-db4d432549ad results=01a14758-eaa0-7303-8208-526e6ab63edf,01a14846-f038-73ff-8635-4f68ce96dcea,01a148d1-dab8-71ab-8924-466976547c9c questions=01a1489e-62f0-79f7-82f6-98ea9f8f3926 withdrawn=- bot_heads=- source=live
  bot_p1_heads_after_result=unknown: no Bot P1 on any head of this PR (the sweep JSON lists P2 threads only): 0. audits=unknown: the audit receipts of this task in .orchestration/validation/ are 990b607, 8607a87 and 3288959 (three).
- the class record-counting reaches three rows (audit:990b607:2, audit:8607a87:3, audit:3288959:3): S1 on the record, not on the code. The records search:
search: record-counting -> none
- (`scripts/orchestrator/three-repeat.sh record-counting` at 2026-10-17T12:25Z; search-body none, compactiondb 0 matches: no mistake record names the class yet; the mechanism that ends hand-written counter snapshots is plan 023 PR F3's record-from-result.py, and PR F1 (#390) makes the gate read the re-plan from the block; until they land each record pastes the counters as above.)
- main moved to ce032e14 (boundary 19, #391) after this audit, so the merge needs an update-branch head and its own local review and audit; the chain is rerun on that head and these dispositions stay as the record of 32889597.
local:00048df:1	advisory-p2
local-finding: 00048df:1 not-applicable:advisory P2 owned by dotfiles-T128-project-map-pane-open-a01-followup-a02 (- [P2] Compare existing map files by filesystem identity — home/dot_claude/hooks/executable_project-map-reload.sh:55-56); evidence=shasum -a 256 .orchestration/tasks/dotfiles-T128-project-map-pane-open-a01-followup-a02.md (2bc357240403629a94e91f44a4e6cf6a2f95359ed621fa7f3f6dd8521ff83240)

## Audit of 00048df (chain 6, the update-branch merge of 32889597 onto main 59db77bb; Verdict: incorrect, three P2) dispositioned 2026-10-17T13:50Z

audit-finding: 00048df:1 not-applicable:advisory P2 owned by dotfiles-T128-project-map-pane-open-a01-followup-a02 (the path-form class after the re-plan line, the same finding as 3288959:1: the suffix is checked after realpath, so a symlinked map is rejected; hook line 40); evidence=shasum -a 256 .orchestration/tasks/dotfiles-T128-project-map-pane-open-a01-followup-a02.md (2bc357240403629a94e91f44a4e6cf6a2f95359ed621fa7f3f6dd8521ff83240)
audit-finding: 00048df:2 not-applicable:advisory P2 owned by dotfiles-T128-project-map-pane-open-a01-followup-a02 (the path-form class after the re-plan line, the same finding as 3288959:2: realpath keeps case on macOS; hook line 56); evidence=shasum -a 256 .orchestration/tasks/dotfiles-T128-project-map-pane-open-a01-followup-a02.md (2bc357240403629a94e91f44a4e6cf6a2f95359ed621fa7f3f6dd8521ff83240)
audit-finding: 00048df:3 not-applicable:a record finding, never a merge stop (C-61), and the auditor is right about the record: the 3288959:3 line above called the third RESULT an update-branch head, but the bus holds three RESULTs with the code heads c0c3ff05 (round 1), 02fdf061 (round 2) and e234a05b (round 3, 07:44:35Z, the canonicaliser, guard and separator changes), so revises=2 are two real fix rounds and INV-6's cap of two is reached, not exceeded; the continuation after it was no further round (the heads 32889597 and 00048df are update-branch merges with no code change) and the re-plan line D-S1-379 of 10:08Z; the corrected S2 reading stands here and the 3288959:3 sentence is superseded by this line; evidence=sqlite3 ~/.agents/skills/agmsg/db/messages.db "select created_at, substr(body,1,160) from messages where to_agent='claude-deep-dot' and body like 'AGMSG-RESULT v1 task_id=dotfiles-T128-project-map-pane-open-a01-followup-a01%' order by id" (three rows, pasted in the chain-6 section of the orchestrator's report)
- the local review of 00048df found one P2, filed by local-advisory.sh under the a02 owner (its `local:00048df:1` row); the sweep had 0 gaps; the block holds 13 ledger rows with searches for path-form-normalisation and record-counting (both at three or more rows; `search: … -> none` lines above).
- 2026-10-17T13:50Z acceptance action: integrate (finish-pr with head 00048df75bbeb1f85cbce0b9c6fa5fac017b2fee: the block, the sweep re-run, the gate, `gh pr merge --squash --match-head-commit`, the fast-forward); the ACCEPTANCE status=accepted follows the merge. After the merge the operator runs `make update` for the hook (the live check is recorded then).

audit:00048df:1	path-form-normalisation
audit:00048df:2	path-form-normalisation
audit:00048df:3	record-counting

- the gate (finish-pr, 2026-10-17T13:57Z) refused: `S1: record-counting at 4 rows without a re-plan line (C-59)`; the class's rows are audit:990b607:2, audit:8607a87:3, audit:3288959:3 and audit:00048df:3, all record findings about the INV-6 counter snapshot missing or misread in this record; the records search above found no mistake record for the class.
re-plan: record-counting -> specification: every acceptance action of a record pastes the regime counters of that moment (the command and its full output), and each `unknown` component is read from its INV-6 source and pasted beside it, so an auditor reads the S2 decision from the record, never infers it; design: the snapshot is generated, not typed: plan 023 PR F3's `record-from-result.py` attaches `regime-counters.sh` output verbatim to every generated entry, and PR F1 (#390) makes the gate read the re-plan from the record block; implementation: F3 (dotfiles-T129-orchestrator-load-mechanisms-a01, queued on a004) and F1 (#390, accepted pending integration); until they land every record pastes the counters by hand as the entries above do (the 13:0xZ and later entries of this record); verification: the gate's S2 reading from the pasted counters and F3's test that the generated entry carries the counters output. Written 2026-10-17T13:57Z by the orchestrator (D-S1-379-records, default: the mechanism is the two in-flight PRs; the operator may override).

- 2026-10-17T14:07Z merged: finish-pr (third run; the first two were refused by the gate for the record-counting re-plan line, absent and then bulleted) wrote the block (16 ledger rows, 3 audit findings), accepted the audit of 00048df and the receipt, passed the gate and merged with `gh pr merge --squash --match-head-commit 00048df75bbeb1f85cbce0b9c6fa5fac017b2fee` at 14:07:11Z; main e9bc99d2 = origin/main; ACCEPTANCE status=accepted sent to a004 (the line in the dispatch list above). The hook lives under home/, so the operator's `make update` applies it; the live check of the pane reload is recorded after that.
