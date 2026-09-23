# refkit-P2-A learning triage

[memory:decision] Validated reusable fact: this session's Edit/Write tools run an automatic
post-write formatter on every touched Markdown/Python file, reformatting the _whole_ file
(table realignment, quote-style normalization, and inserting spaces between Latin/digit and
CJK characters in Japanese prose) — not just the edited region, and it re-applies on every
subsequent Edit too (confirmed by reverting and re-editing). For files where exact-text
fidelity across files matters (e.g. this kit's template-vs-sample table-header matching,
or any file with a paired counterpart the task doesn't allow touching), write the change via
`Bash`/`python` file I/O instead of the Edit/Write tools — that path does not trigger the
formatter. Kept the diff to `git diff --stat`-sized minimal changes this way for all six
`references/` files touched in this task.

Disposition: recorded in CompactionDB (see `.orchestration/reports/refkit-P2-A.md`). Worth
promoting to a standing rule if future tasks in this repo keep hitting the same formatter —
not done here since this is the first time it mattered enough to document.
