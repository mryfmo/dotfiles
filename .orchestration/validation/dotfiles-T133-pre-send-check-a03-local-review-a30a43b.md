---
task: dotfiles-T133-pre-send-check-a03
head: a30a43bad4b61e7d9087fab3cd235e7729b25375
pr: 442
base: f47e9fc0363c79feddbc6470649960f35941ba4b
started: 2026-10-21T21:52:42Z
finished: 2026-10-21T21:57:35Z
findings: 4
engine: codex review --base main (profile review, read-only)
---

- [P2] End owner sections at setext level-two headings — scripts/orchestrator/pre_send.py:157-158
- [P2] Match complete Item headings rather than their prefix — scripts/orchestrator/pre_send.py:159-162
- [P2] Refuse front matter that the local parser did not recognize — scripts/orchestrator/pre_send.py:49-51
- [P2] Require non-whitespace content in owner bullets — scripts/orchestrator/pre_send.py:22-22

```text
Read-only probes reproduced four cases where owner validation incorrectly accepts missing work. The full integration suite was not run because it requires filesystem writes.

Full review comments:

- [P2] Refuse front matter that the local parser did not recognize — scripts/orchestrator/pre_send.py:49-51
  A UTF-8 BOM before the opening `---` makes this return no mapping and no errors, although `task-consistency-check.py` accepts the same YAML. Consequently, `owner()` sees no task ID and skips validation, allowing a sole-Item task referencing a missing owner section to pass. Parse these inputs consistently or explicitly refuse unrecognized front matter.

- [P2] End owner sections at setext level-two headings — scripts/orchestrator/pre_send.py:157-158
  When an empty owner section is followed by a setext heading (`Other` followed by `-----`), this expression leaves the section open. A bullet belonging to that next section then satisfies the owner's work requirement. Recognize setext headings as boundaries too, as required by the stated CommonMark level-two-heading behavior.

- [P2] Match complete Item headings rather than their prefix — scripts/orchestrator/pre_send.py:159-162
  A task containing one real `## Item 1` and an ordinary `## Items overview` heading is counted as having two Items. This activates the empty-owner-section exception and accepts a task with no owned work. Require a complete `Item` token instead of accepting every heading starting with these characters.

- [P2] Require non-whitespace content in owner bullets — scripts/orchestrator/pre_send.py:22-22
  An owner section containing only `- ` followed by a tab passes because `[^ ]` treats the tab as content. That is an empty Markdown bullet, so a sole-Item task can pass without any owned work. Check for non-whitespace bullet content rather than merely a non-space character.
Read-only probes reproduced four cases where owner validation incorrectly accepts missing work. The full integration suite was not run because it requires filesystem writes.

Full review comments:

- [P2] Refuse front matter that the local parser did not recognize — scripts/orchestrator/pre_send.py:49-51
  A UTF-8 BOM before the opening `---` makes this return no mapping and no errors, although `task-consistency-check.py` accepts the same YAML. Consequently, `owner()` sees no task ID and skips validation, allowing a sole-Item task referencing a missing owner section to pass. Parse these inputs consistently or explicitly refuse unrecognized front matter.

- [P2] End owner sections at setext level-two headings — scripts/orchestrator/pre_send.py:157-158
  When an empty owner section is followed by a setext heading (`Other` followed by `-----`), this expression leaves the section open. A bullet belonging to that next section then satisfies the owner's work requirement. Recognize setext headings as boundaries too, as required by the stated CommonMark level-two-heading behavior.

- [P2] Match complete Item headings rather than their prefix — scripts/orchestrator/pre_send.py:159-162
  A task containing one real `## Item 1` and an ordinary `## Items overview` heading is counted as having two Items. This activates the empty-owner-section exception and accepts a task with no owned work. Require a complete `Item` token instead of accepting every heading starting with these characters.

- [P2] Require non-whitespace content in owner bullets — scripts/orchestrator/pre_send.py:22-22
  An owner section containing only `- ` followed by a tab passes because `[^ ]` treats the tab as content. That is an empty Markdown bullet, so a sole-Item task can pass without any owned work. Check for non-whitespace bullet content rather than merely a non-space character.
```
