---
reviewed_at: 2026-10-10T22:41:28Z
reviewer: claude-review-dot-a001
profile: review
session: 2089b04f-f9c7-498b-86c5-76f2140048d5
design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md@84cec99c360383912134e6d2f5ae0963078c40c3ee0033b2e1017f030d8448d3
task: dotfiles-T128-task-review-v1-v2-a01
round: 8
previous: .orchestration/validation/dotfiles-T128-task-review-v1-v2-a01-round7.md
files:
  - dotfiles-T128-v1-task-schema-a01@20ee9c47d5b53c55bd94414f9a0a05068a5eec9488ee9650c0ed5c0ed75d86c1
  - dotfiles-T128-v1b-pr-caps-a01@fe452320f26adcf62061a5d424a1bdf708a08e2975a52cd2fc75cd4a4233dfe0
  - dotfiles-T128-v1c-regime-ci-check-a01@52580173338fdc8a3e1607497553cd6f1d774d0986e260c9108d3f1adfad6176
  - dotfiles-T128-v2-audit-schema-and-runner-a01@6cc99f9ed41a9281b332599efa8761e8878ec4c34b2531c2db21fe263dc49cf7
verdicts:
  dotfiles-T128-v1-task-schema-a01: ready
  dotfiles-T128-v1b-pr-caps-a01: ready
  dotfiles-T128-v1c-regime-ci-check-a01: ready
  dotfiles-T128-v2-audit-schema-and-runner-a01: "revise: R8-1 the runner computes the inputs manifest"
---

# Task-file review round 8: the four files after design v8

PyYAML check: each file's invariant equals design v8 byte for byte; all four pointers name the round-8 receipt; the hashes match the TASK. The design is at revise this round (INV-1 owner, INV-5 wording, INV-10 timestamp); INV-1 and INV-5 are sentences V1, V1c and V2 carry, so those three files will move again with the pointers.

- V1, V1c: ready. INV-1 v8's waiver clause names a mechanism neither task builds, which is correct for them; its owner is the design's gap, not theirs.
- V1b: ready; pointer only.
- V2: revise. Item 1 (line 52) adds the inputs object to the schema, with the acceptance record's pre-audit part, and puts it first in the property order. Item 2 does not say who fills it. A model cannot be trusted to hash files, so the runner computes the manifest (sha256 of every input as read, the acceptance record's text above the audit-input-boundary marker), passes it in the prompt, and after the run overwrites the JSON's inputs with its own computation before the sha256 and the AGMSG-AUDIT record; the test in item 6 covers a mismatch. One sentence in item 2 and one case in item 6.
