---
reviewed_at: 2026-10-12T15:23:58Z
reviewer: claude-review-dot-a001
profile: review
session: 2089b04f-f9c7-498b-86c5-76f2140048d5
design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md@9c9d42cb00c52457e8e7df37bf5276d42978d3466768286cd30b326fb8fdc0e2
task: dotfiles-T128-playbook-rules-redesign-a03
reset_of: dotfiles-T128-playbook-rules-a03
source: .orchestration/tasks/dotfiles-T128-playbook-rules-a03.md@ee6385184e3db246df45970bf71862525d5fd990aa41f92b2b9d03654d45adb2
successor: .orchestration/tasks/dotfiles-T128-playbook-rules-a04.md@e64ee6912c33d98305e70b4206f4d0f55bd4236730131a080f0fd81e7227f254
consistency_check: "dotfiles-T128-playbook-rules-a04.md: OK (C1 to C9)"
verdict: accept
---

# Redesign: the successor task file dotfiles-T128-playbook-rules-a04 (plan 010 option D: obligation plus script plus landing condition)

Written by this seat into the main checkout, as the TASK's allowed_files permit, from a03 at ee638518 (the copy on main at e0e2fe62, byte-equal) by a script that applied each edit exactly once and asserted it, then parsed the front matter with PyYAML. The successor is 94 lines; its sha256 is in the header.

## Diff summary, a03 to a04 (ten hunks)

1. Front matter (item 1): task_id a04; reset_of [a01, a02, a03]; allowed_files names .orchestration/dotfiles-T128-playbook-rules-a04/** in place of a03's; the a01 and a02 copy rows stay, the a03 copy row becomes a history row (no hash binding, so C5 is silent) and a fourth row names the a04 copy with the residual that binds the a04 file's hash; the evidence-records row names the a04 directory; design_review.receipt stays round 22.
2. Item 1 (item 2): the quoted step-6 text is the brief's sentence, byte for byte: the dispatch: line with its read marker; a complete bus read after compaction, never a default-limited one; thirty minutes of silence since the seat's latest bus event for the task (INV-10's figure) gets a bus read then a PING; once plan 007 T718 lands, scripts/orchestrator/dispatch.sh writes the line and scripts/orchestrator/bus-read.sh performs the read and the silence check; until then history.sh <team> --limit 1000 and a paste.
3. Item 3 (item 3): the quoted bullet is the brief's sentence, byte for byte: the records search pasted as the search: template line; the matching correction applied when its mechanism is landed, or landed first when pending, mechanism by mechanism; a class is a slug of [a-z0-9-] assigned at disposition time, never review-title text; once T718 lands, scripts/orchestrator/three-repeat.sh <class> validates the slug and runs both searches without a shell; until then by hand with a validated slug; once dotfiles-T128-gate-evidence-a02 lands the gate refuses without the line, until then the orchestrator refuses by rule; every not-applicable carries ; evidence=<command>. The unquoted task sentence after the bullet (the classes: fields are on main) stays.
4. Items 2, 4, 5, 6, 7 and 8 unchanged (item 4).
5. Heading, introduction and Completion (item 5): the heading names the reset under plan 010 option D after the third S1 cycle; the introduction names the three cycles, the four threads, M-20261012-21 and C-23, the operator's choice at 15:19Z, the reset record, the a03 head fe34f7db with the three commits kept, T718's three scripts, and that items 2, 4, 5, 6, 7 and 8 are unchanged; Completion continues from the worker's head fe34f7db and says the PR stays open with the orchestrator's update-branch already at e12872cd.

The premises, Validation and the other rows are byte for byte a03's (item 6); premise 1 replayed with /usr/bin/grep against origin/main at e0e2fe62 is byte-equal to its pasted output (lines 69, 71, 72, 162), so the premise blocks are unchanged.

## Checks

- Checker: OK (C1 to C9). Re-derived by hand: C3, rows name the a01, a02, a03 and a04 task copies; C7, the eight names (task metadata, metadata separators, in-process effects, workflow and interpreter or environment inputs, new or renamed scripts, orchestrator effect merge, orchestrator effect update-branch, orchestrator effect forced worker removal); C9, every mechanism a quoted sentence names, against origin/main (git ls-tree and git grep): scripts/regime-counters.sh is on main; scripts/orchestrator/dispatch.sh, bus-read.sh and three-repeat.sh are not and each carries "Once plan 007 T718 lands"; the gate's refusal carries "Once dotfiles-T128-gate-evidence-a02 lands" (ACCEPTANCE_EVIDENCE is not on main); item 2's C1 to C6 and item 4's C4 carry their landing conditions as in a03; history.sh is the agmsg script, outside the repository. T718's task file (dotfiles-T128-orchestrator-tools-a01) names the same three scripts under scripts/orchestrator/, so the paths agree.
- Items 1 and 3 contain no command text beyond the two named interim commands (history.sh <team> --limit 1000; the two searches by hand), no grammar other than the slug's [a-z0-9-], and the only limit figure is inside the interim command, as the brief's sentence has it.
- No SKILL or AGENTS.md sentence is restated beyond a03's; items 2, 4, 5, 6, 7 and 8 are untouched.
- Bookkeeping for the orchestrator, outside this file: T718's task file carries after: [dotfiles-T128-playbook-rules-a03] and should name a04.

Verdict: accept, this RESULT being the reset anchor under the record's redesign_source.
