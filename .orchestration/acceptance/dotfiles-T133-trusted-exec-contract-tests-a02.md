---
{
  "format": 1,
  "task": "dotfiles-T133-trusted-exec-contract-tests-a02",
  "head": "f66b27f38d18183a5343f014cbb5cf85474b906c",
  "pr": 436,
  "ledger": [
    {
      "id": "audit:9545e59:1",
      "class": "happy-path-closing-test"
    },
    {
      "id": "audit:9545e59:2",
      "class": "evidence"
    },
    {
      "id": "audit:9545e59:3",
      "class": "evidence"
    },
    {
      "id": "audit:9545e59:4",
      "class": "evidence"
    },
    {
      "id": "audit:9545e59:5",
      "class": "acceptance-dispositions"
    },
    {
      "id": "audit:9545e59:6",
      "class": "missing-owner-task"
    },
    {
      "id": "audit:a561e64:1",
      "class": "escape-detection-gap"
    },
    {
      "id": "audit:a561e64:2",
      "class": "escape-detection-gap"
    },
    {
      "id": "audit:a561e64:3",
      "class": "unhashed-text-change"
    },
    {
      "id": "audit:a561e64:4",
      "class": "evidence-placeholders"
    },
    {
      "id": "audit:a561e64:5",
      "class": "disposition-label"
    },
    {
      "id": "audit:f66b27f:1",
      "class": "escape-detection-gap"
    },
    {
      "id": "audit:f66b27f:2",
      "class": "escape-detection-gap"
    },
    {
      "id": "audit:f66b27f:3",
      "class": "unhashed-base-change"
    },
    {
      "id": "audit:f66b27f:4",
      "class": "text-contradiction"
    }
  ],
  "searches": [
    {
      "class": "escape-detection-gap",
      "records": []
    },
    {
      "class": "evidence",
      "records": [
        "M-20261012-3.md",
        "M-20261014-09.md",
        "M-20261014-10.md",
        "M-20261020-04-result-claims-against-own-counts.md"
      ]
    }
  ],
  "audit_findings": [
    {
      "n": "1",
      "reason": "advisory P2 owned by dotfiles-T133-trusted-exec-contract-tests-followup-a01 (assert_untouched checks the input's access time only; the owner adds the output-read probe)",
      "evidence": "`sed -n '120,130p' tests/unit/trusted_exec_contract.py`"
    },
    {
      "n": "2",
      "reason": "advisory P2 owned by dotfiles-T133-trusted-exec-contract-tests-followup-a01 (an adjacent temporary file is not asserted; the owner adds a directory-listing snapshot of new_output.parent)",
      "evidence": "`sed -n '128,134p' tests/unit/trusted_exec_contract.py`"
    },
    {
      "n": "3",
      "reason": "advisory P2 owned by dotfiles-T133-trusted-exec-contract-tests-followup-a01 (orchestration: the completion-check base changed through PING, not a hashed amendment; C-123 fixes the rule for the next texts; the measured comparison at 9cc6c96b is the merge-base the update-branch produced)",
      "evidence": "`git merge-base 9cc6c96b f66b27f38d18183a5343f014cbb5cf85474b906c`"
    },
    {
      "n": "4",
      "reason": "advisory P3 owned by dotfiles-T133-trusted-exec-contract-tests-followup-a01 (the text's completion requirement says four allowlist entries while the front matter declares three; wording defect, the implementation follows the three declared entries)",
      "evidence": "`sed -n '10,13p;205p' .orchestration/tasks/dotfiles-T133-trusted-exec-contract-tests-a02.md`"
    }
  ],
  "replans": {
    "evidence": {
      "specification": "every recorded command in report.md and validation.md is the literal command that ran, with its exit code and output, and every claim about a run names its log; no shell variable, placeholder or summary stands in for a command",
      "design": "the worker writes commands from a command log (the a06 lineage's `*-commands.json` plus `measure.md` pattern) rather than by hand, and the orchestrator's evidence check refuses a validation whose recorded commands contain unexpanded `$VAR` tokens or whose base/candidate counts disagree with their claims (`result-evidence-check.sh`, orchestrator-side)",
      "implementation": "the records-only commit of amendment 1 replaces the placeholders in this lineage; the check is an item of `dotfiles-T133-result-precheck-followup-a01` (D-024-46)",
      "verification": "the task-level audit of the final head reports no evidence-class finding, and the evidence check passes on that head"
    },
    "escape-detection-gap": {
      "specification": "the helper's untouched assertion proves that a refused invocation changed nothing under the fixture root: no entry read (atime) or written (mtime, size, inode) and no entry created or removed, for every path under the root, not only the two named files",
      "design": "assert_untouched() snapshots the whole fixture root before the call (recursive listing with inode, size, mtime and atime per entry) and compares it after, reporting the diff in the failure message, so a read of the output or an adjacent temporary file is a detected change",
      "implementation": "an item of dotfiles-T133-trusted-exec-contract-tests-followup-a01 (the owner of audit:f66b27f:1 and :2), with two regression tests reproducing the audit's in-memory probes (read-only output, adjacent temporary file) red before and green after",
      "verification": "the task-level audit of the owner's final head reports no escape-detection-gap finding and the two probes are fixtures in the helper's test module"
    }
  }
}
---

# Acceptance record: dotfiles-T133-trusted-exec-contract-tests-a02

Lineage: reset of dotfiles-T133-trusted-exec-contract-tests-a01 (INV-6 S2, revises 2) on PR #436; records-only: the code at 612f75f5 is complete and twice audited; the a02 task copy is the only change.

- 2026-10-20T14:26Z: text written whole by the review profile (`trusted-exec-contract-tests-a02-prompt.md`), two checker fixes by the orchestrator (retained_predecessor_directories; the two copy rows), 224 lines, pre-send OK, sha256 0b1923a6299109c1f8db3a56dfbba3cc6ac0c5217d08a577322f99f5617e4380; reset-anchor review accepted by a009 (14:19:49Z); reset record written; dispatched to a011 at the anchored bytes.
- 2026-10-20T14:27:34Z: a011 RESULT `status=blocked round=1`: local head 9cb70cc5 adds only the a02 copy (code unchanged against 612f75f5: `git diff --quiet` exit 0 on tests and the a01 evidence directory; sha256 of the three code files equal to the text's), but `git diff --stat 612f75f5..HEAD` shows two files because the update-branch merge 9cc6c96b brought main's amended a01 text. Orchestrator disposition (2026-10-20T14:28Z, PING, no amendment): the diff-stat check measures from the branch head at dispatch, 9cc6c96b; the code-unchanged proof against 612f75f5 stands; both measurements go into report.md; push and RESULT.
- 2026-10-20T14:47:22Z: a011 RESULT `status=ready_for_review round=1` head 9cb70cc5 (records-only: the a02 copy; code unchanged at 612f75f5; both diff measurements in report.md). ACCEPTANCE `status=pending-integration` (2026-10-20T14:49Z). Integration order: boundary records PR (the a02 text to main) -> update-branch #436 -> chain once -> gate -> merge.
- 2026-10-21T01:48Z: integration start (R0-3): update-branch to main 85a689e7 -> head f66b27f3, CI all pass (CLEAN). `result-evidence-check.sh` refuses by construction (`no validation.md at f66b27f3`): the a02 round is records-only and its item 1 keeps report/validation uncommitted, so the C-113 checker's path assumption does not apply; the evidence taken instead is the head's CI (gh pr checks --watch rc 0), the a02 task copy at the head equal to the dispatched bytes (checked below), and the retained a01 validation. Gap recorded for the glue -> repo task (R1-9): the checker reads the RESULT's `validation=` token and accepts a records-only round that names a retained predecessor path.

## Lineage rows carried from dotfiles-T133-trusted-exec-contract-tests-a01

audit:9545e59:1	happy-path-closing-test
audit:9545e59:2	evidence
audit:9545e59:3	evidence
audit:9545e59:4	evidence
audit:9545e59:5	acceptance-dispositions
audit:9545e59:6	missing-owner-task
audit:a561e64:1	escape-detection-gap
audit:a561e64:2	escape-detection-gap
audit:a561e64:3	unhashed-text-change
audit:a561e64:4	evidence-placeholders
audit:a561e64:5	disposition-label
re-plan: evidence (rows audit:9545e59:2, audit:9545e59:3, audit:9545e59:4; the class reached three rows across the a01 audits: validation records that cannot be replayed or that over-claim) — specification: every recorded command in report.md and validation.md is the literal command that ran, with its exit code and output, and every claim about a run names its log; no shell variable, placeholder or summary stands in for a command; design: the worker writes commands from a command log (the a06 lineage's `*-commands.json` plus `measure.md` pattern) rather than by hand, and the orchestrator's evidence check refuses a validation whose recorded commands contain unexpanded `$VAR` tokens or whose base/candidate counts disagree with their claims (`result-evidence-check.sh`, orchestrator-side); implementation: the records-only commit of amendment 1 replaces the placeholders in this lineage; the check is an item of `dotfiles-T133-result-precheck-followup-a01` (D-024-46); verification: the task-level audit of the final head reports no evidence-class finding, and the evidence check passes on that head.
- 2026-10-21T02:02Z: task-level audit of f66b27f3 (`.orchestration/validation/dotfiles-T133-trusted-exec-contract-tests-a02-audit-f66b27f.md`): Verdict incorrect; 2 P2 implementation (trusted_exec_contract.py:126 assert_untouched checks access time only on the input; :131 an adjacent temporary file passes because only the two named files and new_output.parent are asserted; the audit notes both remain assigned to the existing follow-up task), 1 P2 orchestration (record line 80: the completion-check base moved 612f75f5 -> 9cc6c96b through a PING, not a hashed amendment; the text's line 191 wants the original comparison), 1 P3 orchestration (text line 205 requires four allowlist entries while lines 10-13 declare three). Dispositions: all four advisory, owned by dotfiles-T133-trusted-exec-contract-tests-followup-a01 (rows below); no third worker round on a mechanism PR (standing order) and no text amendment at this point (the text defects are the owner's items); the base change is recorded as C-123 (a completion-check base is the merge-base at RESULT time unless the text pins one, and a pinned base changes only through a hashed amendment).

audit:f66b27f:1	escape-detection-gap
audit:f66b27f:2	escape-detection-gap
audit:f66b27f:3	unhashed-base-change
audit:f66b27f:4	text-contradiction

## Owned by dotfiles-T133-trusted-exec-contract-tests-followup-a01
audit-finding: f66b27f:1 not-applicable:advisory P2 owned by dotfiles-T133-trusted-exec-contract-tests-followup-a01 (assert_untouched checks the input's access time only; the owner adds the output-read probe); evidence=`sed -n '120,130p' tests/unit/trusted_exec_contract.py`
audit-finding: f66b27f:2 not-applicable:advisory P2 owned by dotfiles-T133-trusted-exec-contract-tests-followup-a01 (an adjacent temporary file is not asserted; the owner adds a directory-listing snapshot of new_output.parent); evidence=`sed -n '128,134p' tests/unit/trusted_exec_contract.py`
audit-finding: f66b27f:3 not-applicable:advisory P2 owned by dotfiles-T133-trusted-exec-contract-tests-followup-a01 (orchestration: the completion-check base changed through PING, not a hashed amendment; C-123 fixes the rule for the next texts; the measured comparison at 9cc6c96b is the merge-base the update-branch produced); evidence=`git merge-base 9cc6c96b f66b27f38d18183a5343f014cbb5cf85474b906c`
audit-finding: f66b27f:4 not-applicable:advisory P3 owned by dotfiles-T133-trusted-exec-contract-tests-followup-a01 (the text's completion requirement says four allowlist entries while the front matter declares three; wording defect, the implementation follows the three declared entries); evidence=`sed -n '10,13p;205p' .orchestration/tasks/dotfiles-T133-trusted-exec-contract-tests-a02.md`
- 2026-10-21T02:06Z: S1 (C-59): escape-detection-gap reached four rows; re-plan line below; the operator is told once for this class (re-plan v2 S-R5 / feedback-replan-not-patch).

re-plan: escape-detection-gap (rows audit:a561e64:1, audit:a561e64:2, audit:f66b27f:1, audit:f66b27f:2; the class reached four rows across the a01 and a02 audits: the contract helper's untouched-check misses reads of the output and adjacent temporary files) — specification: the helper's untouched assertion proves that a refused invocation changed nothing under the fixture root: no entry read (atime) or written (mtime, size, inode) and no entry created or removed, for every path under the root, not only the two named files; design: assert_untouched() snapshots the whole fixture root before the call (recursive listing with inode, size, mtime and atime per entry) and compares it after, reporting the diff in the failure message, so a read of the output or an adjacent temporary file is a detected change; implementation: an item of dotfiles-T133-trusted-exec-contract-tests-followup-a01 (the owner of audit:f66b27f:1 and :2), with two regression tests reproducing the audit's in-memory probes (read-only output, adjacent temporary file) red before and green after; verification: the task-level audit of the owner's final head reports no escape-detection-gap finding and the two probes are fixtures in the helper's test module.
