---
id: M-20261020-06
date: 2026-10-20
classes: [id-collision, records-overwrite]
severity: P2
---

# A new mechanism task reused an existing lineage's id and overwrote its dispatched text

**What happened.** The orchestrator named the RESULT-evidence precheck glue `result-precheck.sh` and its promotion task `dotfiles-T133-result-precheck-a01` (10:00Z) without listing `.orchestration/tasks/` and `.orchestration/acceptance/` first. That id is plan 024 P1-5's lineage (result-precheck.sh with dispatch.sh's PRECHECK_REQUIRED refusal and the git hooks; a01 withdrawn on 10-18, a04 on PR #411). `cp` of the authored text onto `.orchestration/tasks/dotfiles-T133-result-precheck-a01.md` overwrote the dispatched a01 text (11:04Z), the C-80 review was filed under the wrong lineage, and the record sync ran against the a01 record (its three thread rows stayed intact).

**What the rules say.** Orchestrator Playbook step 6: a record is created before the first dispatch and a lineage's id is unique; D-024-40 and the regime check depend on the dispatched bytes of every task text on main.

**Why the rules did not fire.** The brief, the authoring, the install and the review are four steps with no id check; pre-send.sh checks bytes and rows of the text it is given, not whether the id is free; the acceptance-record write had an existence assertion and that is what surfaced the collision.

**Mechanism.** pre-send.sh refuses a text whose task id already has a record or a task file unless the text is an amendment (`previous_sha256:`) or a reset (`reset_of:`) (C-116). Repair: the a01 text restored from HEAD and verified by sha; the review files moved to `dotfiles-T133-result-evidence-check-a01-text-security-99c37ca.md(.last.md)`; the glue renamed `result-evidence-check.sh`; the new lineage `dotfiles-T133-result-evidence-check-a01` carries the four C-80 rows as `text-security:99c37ca:1-4`.
