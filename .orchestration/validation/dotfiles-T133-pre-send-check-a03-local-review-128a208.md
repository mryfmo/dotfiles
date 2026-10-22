---
task: dotfiles-T133-pre-send-check-a03
head: 128a2088767927c4351bf593d328891fde084ec1
pr: 442
base: 7da0cdfab9de9fbea673b82379acd4e317115065
started: 2026-10-22T00:56:01Z
finished: 2026-10-22T01:01:13Z
findings: 3
engine: codex review --base main (profile review, read-only)
---

- [P2] Preserve ordinary paragraphs starting with hashes or hyphens — scripts/orchestrator/pre_send.py:169-169
- [P2] Reset fence state at the front-matter boundary — scripts/orchestrator/pre_send.py:64-65
- [P2] Resolve the record associated with the owner reference — scripts/orchestrator/pre_send.py:152-154

```text
Read-only reproductions confirmed that invalid shell blocks and missing owner work can pass the new preflight. The full temporary-file test suite was not run because the sandbox is read-only.

Full review comments:

- [P2] Reset fence state at the front-matter boundary — scripts/orchestrator/pre_send.py:64-65
  A valid YAML scalar such as `notes: |\n  ```text` opens a non-shell fence that remains active across the closing front-matter delimiter. A subsequent real bash block containing `if then` is swallowed into that fence, so the consistency checker passes and no bash-syntax refusal occurs. Separate YAML metadata from Markdown structure, preserving original line numbers.

- [P2] Resolve the record associated with the owner reference — scripts/orchestrator/pre_send.py:152-154
  When a task mentions another acceptance record before its owner-work instruction, this search opens the earlier record regardless of which record the instruction names. If that earlier record contains matching owner rows, the check passes even when the intended record or section is missing. Associate the record path with the owner reference instead of selecting the first path anywhere in the task.

- [P2] Preserve ordinary paragraphs starting with hashes or hyphens — scripts/orchestrator/pre_send.py:169-169
  For valid setext headings such as `#Next\n---` or `-Next\n---`, this prefix check clears `para` even though the title is neither an ATX heading nor a list item. The underline therefore fails to end the owner section, and a following bullet incorrectly satisfies its work requirement. Reset paragraph state only for actual Markdown block starts.
Read-only reproductions confirmed that invalid shell blocks and missing owner work can pass the new preflight. The full temporary-file test suite was not run because the sandbox is read-only.

Full review comments:

- [P2] Reset fence state at the front-matter boundary — scripts/orchestrator/pre_send.py:64-65
  A valid YAML scalar such as `notes: |\n  ```text` opens a non-shell fence that remains active across the closing front-matter delimiter. A subsequent real bash block containing `if then` is swallowed into that fence, so the consistency checker passes and no bash-syntax refusal occurs. Separate YAML metadata from Markdown structure, preserving original line numbers.

- [P2] Resolve the record associated with the owner reference — scripts/orchestrator/pre_send.py:152-154
  When a task mentions another acceptance record before its owner-work instruction, this search opens the earlier record regardless of which record the instruction names. If that earlier record contains matching owner rows, the check passes even when the intended record or section is missing. Associate the record path with the owner reference instead of selecting the first path anywhere in the task.

- [P2] Preserve ordinary paragraphs starting with hashes or hyphens — scripts/orchestrator/pre_send.py:169-169
  For valid setext headings such as `#Next\n---` or `-Next\n---`, this prefix check clears `para` even though the title is neither an ATX heading nor a list item. The underline therefore fails to end the owner section, and a following bullet incorrectly satisfies its work requirement. Reset paragraph state only for actual Markdown block starts.
```
