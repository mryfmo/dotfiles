---
id: M-20261020-02
date: 2026-10-20
classes: [hash-binding, records-form]
severity: P2
---

# Boundary 25 carried task texts older than their dispatched bytes

**What happened.** The regime verifier (`scripts/orchestrator/regime-ci.py`) treats the base's `.orchestration/tasks/<task>.md` as the dispatched policy and refuses a PR whose task copy differs from it. PR #436's update-branched head b3c50768 failed `regime` (run 39364553764, 2026-10-20T03:29Z) because main's text of `dotfiles-T133-trusted-exec-contract-tests-a01` lacks the `dispatch to a011 …` line pasted into its Checks block before the 23:29:38Z dispatch (task_sha256 dd754911…, which the worker's copy and the local text both equal). Boundary 25 (#435) was committed at 00:19:29Z from a file copy made earlier in the boundary's long preparation (masker, validator and push retries), and `dotfiles-T133-loop-limits-a01` was dispatched at 00:55:43Z, after the commit; both texts on main are pre-dispatch snapshots. Fix: records PR #438 (`records/sync-dispatched-texts-26`) replaces both with the dispatched bytes.

**What the rules say.** Design 5.14 item 8: the committed records are the authority, read at the 40-hex sha; regime-ci reads the policy from the base. C-87/C-100: figures and prerequisites are run, not recalled.

**Why the rules did not fire.** Nothing compared the boundary's copies with the bus: the boundary script copied files, masked paths and validated, but never checked that an in-flight task text equalled the `task_sha256` of its latest `AGMSG-TASK` message, and nothing re-copied after the preparation stalled.

**Mechanism.** Before a boundary pushes, it lists every in-flight task (`AGMSG-TASK` messages on the bus without a merged PR) and refuses when the sha256 of the copied `.orchestration/tasks/<task>.md` differs from the latest `task_sha256` dispatched for that task, printing both; the copy step runs immediately before the commit. Glue first (`boundary-26` preparation), tracked home `scripts/orchestrator/boundary.sh` (the boundary lineage's follow-up text). Corollary for planning: every post-dispatch amendment implies a records PR before the worker's PR can pass `regime`, so amendments are batched and their records PR is opened as soon as the amendment is dispatched.
