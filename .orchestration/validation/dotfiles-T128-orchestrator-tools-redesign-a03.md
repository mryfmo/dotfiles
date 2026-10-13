---
reviewed_at: 2026-10-13T16:48:06Z
reviewer: claude-review-dot-a001
profile: review
session: 2089b04f-f9c7-498b-86c5-76f2140048d5
design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md@fa2c5157e6b962d10076a505788cb9d074e366acc73a8fa5e83877b77c5a863a
task: dotfiles-T128-orchestrator-tools-redesign-a03
round: 1
task_file: dotfiles-T128-orchestrator-tools-redesign-a03@16226536ad0999563559a9fa3a899b8521e432d808ea75af08e1a5fd462665ea
reset_of: dotfiles-T128-orchestrator-tools-a02
source: .orchestration/tasks/dotfiles-T128-orchestrator-tools-a02.md@a4c929b14f28ba5f67d007548f7e3b8e5bdcf48cf37c17eae76c4375cb363ce5
successor: .orchestration/tasks/dotfiles-T128-orchestrator-tools-a05.md@eaac8e4bd03cda154273097736944b3762581f872d5f5fbcdca67650b43236ea
consistency_check: "dotfiles-T128-orchestrator-tools-a05.md: OK (C1 to C10, C7b)"
verdict: accept
---

# Redesign round 1: dotfiles-T128-orchestrator-tools-a05, the INV-6 reset of a02 (plan 020 step 4.2, after the audit of PR #346's final head 7b574d32)

Both hashes of the 16:34:11Z TASK line recomputed and equal (brief 16226536, a02 on disk and on origin/main a4c929b1). The successor was produced from `git show origin/main:.orchestration/tasks/dotfiles-T128-orchestrator-tools-a02.md` by thirteen asserted single-occurrence replacements (an edit script, each `old` counted once before the replace), never retyped, so the diff against a02 on main is exactly the brief's items 1 to 7. a05 is 159 lines, 29 threat rows (a02: 146 lines, 26 rows), 16 allowed files, the same three premises; its sha256 is in the header.

## Diff summary against a02 on main (`diff` hunks, a02 line numbers first)

| Hunk | Brief item | Change |
| --- | --- | --- |
| 3c3 | 1 | `task_id` a05 |
| 6c6 | 1 | `reset_of: [dotfiles-T128-orchestrator-tools-a02]` |
| 26c26 | 1 | `allowed_files`: the a05 evidence directory replaces a02's |
| 34a35,36 | 6 | new closed row: orch-audit.sh receipt freshness (item 9), `test_orch_audit_refuses_a_run_that_leaves_no_fresh_receipt` |
| 38a41,44 | 6 | two new closed rows: fill_sweep.py reply trust (item 7) and badged bodies (item 8), each with its test |
| 59,60c65,68 | 1 | the a02 copy row becomes the history row (a02 copy and its evidence records, not edited under a05); the a05 copy row added, binding the a05 file's hash to the reset record |
| 65c73 | 1 | the branch evidence records row names the a05 directory |
| 105c113 | 2 | heading: a05, the INV-6 reset of a02 after the audit of 7b574d32; a03 and a04 named as the first slice |
| 107c115 | 2 | new intro: trigger (the three P1 as the brief quotes them, with the audit receipt path and the 16:12:55Z RESULT and 16:30Z audit times from a02's acceptance record), plan 020 step 4.2, the counters line, the root cause, the worker and PR #346 continuity, PR-B |
| 108a117,118 | 2 | a02's intro kept verbatim as "History (a02)." |
| 119c129 | 6 | item 2 gains the three test names |
| 124a135,137 | 3, 4, 5 | items 7, 8, 9 |
| 134c147 | 7 | Completion: PR #346 continues from 7b574d32, one fix round for items 7 to 9, local review once plus the audit, a surviving P0/P1 goes to the operator, P2 owned by the followup task |

Nothing else differs: a02's items 1 to 6 (except the appended sentence of item 2), its Validation section, its three "Change of" sections and its premises are byte-identical.

## Checks

- Checker, pasted (run from the main checkout on the copy named by the task id, so C6 and C8 resolve against the design and origin/main):

```text
dotfiles-T128-orchestrator-tools-a05.md: OK
```

  Re-derived: C3 finds `-a02/task.md` in the history row and `-a05/task.md` in the copy row; C4 for the new rows: the a05 evidence directory is named by the copy row and the evidence-records row, and the three new closed rows name no allowed_files prefix (they name the script by basename, so C7b counts them as zero-entry rows, as a04's dispatch.sh rows are); C7: the eight non-path controls are a02's, unchanged; C5: the only "names the … file's hash" phrase says a05.
- Sweep, pasted (`amend-sweep.sh` on a05 for the brief's term; its one hit is the a02 history copy row, which the brief excludes):

```text
65:  - control: the task-file copy of a02 on the branch (.orchestration/dotfiles-T128-orchestrator-tools-a02/task.md) and the a02 evidence records beside it, kept as history
leftovers above: fix before hashing
```

  The same sweep on a copy of a05 without that line, with the superseded terms added:

```text
no leftover of: orchestrator-tools-a02/ names the a02 file Bot wait after a01 merges
```

- The history row's claim replayed: `git show 7b574d32:.orchestration/dotfiles-T128-orchestrator-tools-a02/task.md | shasum -a 256` = a4c929b1…, the a02 file as dispatched, which a02's acceptance record carries once.
- Each of the three test names appears exactly once as a `closed:` disposition, once in item 2 and once in its own item (three occurrences each).
- The audit's three P1 map one to one: `fill_sweep.py:49` (reply trust) is item 7, `fill_sweep.py:60` (badged bodies) is item 8, `orch-audit.sh:72` with the copy loop at 62 (receipt freshness) is item 9; the intro numbers them (1), (2), (3) as the brief does.
- No GitHub login as a literal: `grep -c -E 'mryfmo|chatgpt-codex|\[bot\]|coderabbit'` on a05 = 0 (the Bot is named by role). No home path in a05 or in this receipt (grep count 0 on both).
- Count words in the new text: "three P1" (twice), "three tests", "three refusals"; "nine scripts" in the a02 tests row stays correct; the checker-range phrase reads "C1 to C10 and C7b" at both places, as a02 already did.
- Event times are copied from a02's acceptance record (10:00:24Z question, 10:02Z answer, 16:12:55Z revise RESULT, 16:30Z audit) and the bus (16:34:11Z TASK); none from the clock.

## Derivations beyond the brief's letter (for the orchestrator and the Codex half to confirm or object)

1. Item 8's badge grammar (C-31): the brief says "carries a P0 to P3 badge" without a form. The sweep JSON of 7b574d32 shows the Bot's findings as the Markdown image `![P1 Badge](https://img.shields.io/badge/P1-orange?style=flat)` and the Codex review-summary issue comment carrying `"blockingSeverityThreshold":"P0"` inside an HTML comment (pasted below). A bare `P[0-3]` match would turn every PR's summary comment into a permanent gap, so a05 defines the badge as the image form `![P<n> Badge](` and adds a third case to the named test (the bare-P0 summary shape keeps the issue_comment rule).

```text
$ python -I -c '<print source, level, url tail, body[:90], P-badge matches per item>' .orchestration/validation/dotfiles-T128-orchestrator-tools-a02-pr-feedback.json
head_sha 7b574d323c4ec30d5982755bc6f9fe627264de5f pr 346 items 10
issue_comment comment True | ll/346#issuecomment-6148837696 | '<!-- codex-pull-request-review-summary -->\n<!-- codex-security-review:v1 {"blockingSeverit' | badges: ['P0","headSha":"1287af3435e4847ef819e43972b']
review_comment comment True | ull/346#discussion_r4260535901 | '**<sub><sub>![P1 Badge](https://img.shields.io/badge/P1-orange?style=flat)</sub></sub>  En' | badges: ['P1 Badge](https://img.shields.io/badge/P1-']
```

2. The counters line: the brief's `first_result_head` is 35 hex characters (`…4bfe1`); a05 carries the 40-character value from the pasted counters output in a02's acceptance record (`scripts/regime-counters.sh dotfiles-T128-orchestrator-tools-a02 --pr 346`: `first_result_head=1287af3435e4847ef819e43972b0da4bfe156e60`), and names that command as the source.
3. Item 7's test also exercises the option's three refusals (absent, malformed, repeated: exit 2), the C-31 standing item's "the tests enumerate the table"; the brief's own case (another login ignored, the given login fills) is the first case.
4. Completion drops a02's "the Bot wait of Worker Playbook step 15 is done" (the Bot's trigger is PR-open only since plan 020 step 2, 13:33Z, and PR #346 is open) and "draft PR from origin/main after a01 merges" (PR #346 exists); the brief's item 7 lists the Completion's content and names neither.
5. PR-B: a02 never names PR-A or PR-B; the split is its Validation clause, proposed in the worker's 10:00:24Z question and answered at 10:02Z (a02's acceptance record). The intro says so instead of "as a02 defined it" alone.

Verdict: accept on eaac8e4bd03cda154273097736944b3762581f872d5f5fbcdca67650b43236ea, this RESULT being the reset anchor under the a02 reset record's redesign_source.
