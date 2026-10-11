---
reviewed_at: 2026-10-11T05:19:31Z
reviewer: claude-review-dot-a001
profile: review
session: 2089b04f-f9c7-498b-86c5-76f2140048d5
design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md@15957fbc6b47ff8f2424072ca5b5849911b7be90582e1d850f5d315563494cd4
task: dotfiles-T128-task-review-a02-a01
round: 2
previous: .orchestration/validation/dotfiles-T128-task-review-a02-a01.md
files:
  - dotfiles-T128-process-rules-a02@287cee8e440ac8cef10c1c23c02369ddb8ccce671c5d476946aec64ab76b0a7f
verdicts:
  dotfiles-T128-process-rules-a02: "revise: 2 item 5 invents an INV-6 trigger"
---

# Task-file review round 2: a02's two new sentences for the third-round P1 threads

New content only (section "Also", items 4 and 5), judged against design v16 and the PR head aeb6c5ad.

- Item 4: the phrase it replaces exists verbatim on the PR head (counters bullet, line 72), the replacement names the explicit limit and the storage facade as the other complete read, and the token test pins it. It closes thread 4240348412 (the 20-row default undercounts). Note, not an item: a fixed --limit 1000 ages (the history is past 400 rows and grows by the day); the sentence already names the facade, and A3's script retires the by-hand rule, so leave it.
- Item 5 (R2): the appended step-10.1 sentence is right until its last clause. "An open:<thread id> item from a worker's third Bot round is a sweep item like any other: it becomes fixed:<sha> through a revise round that carries its check=, or not-applicable:<reason> with a pasted refutation" matches the PR integration rule (no stopgap or deferral), INV-3 (a revise carries check=) and A2. "when neither applies, the task is reset under INV-6" does not match INV-6: its resets fire on counts (revises, amendments, questions, Bot heads, audit heads), not on an open thread, and a prose-only trigger the gate cannot evaluate is the class the design removed. Right: "when neither applies the PR is not merged; the revise round that fixes it counts toward INV-6 like any other". The token "never merged with the thread open" can stay; the token test should not assert "reset under INV-6". It closes thread 4240348414 once reworded.
- Neither sentence contradicts the relayed redesign text or anything else on the PR head; both carry one token test as A1 asks; the RESULT line names both threads as fixed:<sha>, which is the sweep form.

Verdict ready once the item(s) above are applied; the fenced redesign blocks are untouched.
