---
id: M-20261020-07
date: 2026-10-20
classes: [identity-from-name, records-overwrite]
severity: P2
---

# The #432 chain ran under the superseded task id taken from the branch name

**What happened.** After compaction the orchestrator read PR #432's branch `tools/lint-comparisons-followup-a02` as the task id and ran the chain as `dotfiles-T129-normalised-comparison-lint-followup-a02` (10:04Z and 11:07Z). The live lineage is a04: the PR tree carries the a02, a03 and a04 task copies and the a04 record names PR 432 with head 6434c27. The second run stopped at the audit step with 14 gaps (`audit:6434c27:1-14`, the a04 lineage's rows, absent from the a02 record), after its record step had rewritten the a02 record's JSON block, crit.json, review receipt and pr-feedback, and after the orchestrator had added a chronology line and a `re-plan: lint-detection-gap` line to the wrong record.

**What the rules say.** The chain audits "the named changeset" of one task (AGENTS.md Audit); a lineage's live id is the newest task copy on the PR, and records are written only for that id (Orchestrator Playbook step 6).

**Why the rules did not fire.** The chain accepts any task name with a record file; nothing compared the name with the PR tree; the compaction summary named the PR by number and branch, not by task id.

**Mechanism.** `pr-task.sh <pr> [<head40>]` prints the live task id from the PR head tree and the records (C-117), and every chain, audit and security-review invocation reads its task id from it. Repair: the a02 record and its three validation files restored from HEAD (byte-identical to main), the mis-named chain log and local review kept under `.agents/worklog/orchestrator-glue/misrun-432-as-a02/`, the re-plan line and chronology written into the a04 record, and the chain re-run under a04 with owner a05.
