---
task: dotfiles-T128-orchestrator-tools-a03
head: 0d1994758a96a21b48d1af58037ccada59ca9d07
pr: 336
base: a5475d9e
started: 2026-10-13T06:56:02Z
finished: 2026-10-13T06:57:17Z
findings: 1
engine: codex review --base main (profile review, read-only; the C-32 probe, run by hand before local-review.sh existed)
---

- [P2] Validate the record destination before sending — scripts/orchestrator/dispatch.sh:187-187

```text
The dispatch helper can successfully send a message and only afterward discover that its requested evidence record cannot be written, leaving bus state and review evidence inconsistent.

Review comment:

- [P2] Validate the record destination before sending — scripts/orchestrator/dispatch.sh:187-187
  When the optional record does not exist and its parent directory is missing or unwritable, `agmsg-dispatch` sends the irreversible bus message first, then `mkstemp` fails and leaves the dispatch unrecorded. This contradicts the documented missing-record behavior and can break review evidence; validate or prepare the destination before calling `agmsg-dispatch`.
The dispatch helper can successfully send a message and only afterward discover that its requested evidence record cannot be written, leaving bus state and review evidence inconsistent.

Review comment:

- [P2] Validate the record destination before sending — scripts/orchestrator/dispatch.sh:187-187
  When the optional record does not exist and its parent directory is missing or unwritable, `agmsg-dispatch` sends the irreversible bus message first, then `mkstemp` fails and leaves the dispatch unrecorded. This contradicts the documented missing-record behavior and can break review evidence; validate or prepare the destination before calling `agmsg-dispatch`.
probe exit 0 at 06:57:17
```
