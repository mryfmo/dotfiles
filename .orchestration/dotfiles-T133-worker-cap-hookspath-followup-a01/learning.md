---
type: learn
id: '20261018_233812'
owner: codex-standard-dot-a012
created_at: '2026-10-18T23:49:23Z'
updated_at: '2026-10-18T23:49:23Z'
validated: true
apply_to: tests
---

## Date

2026-10-18

## Learnings

Python -c imports can load a repository-local extension-module name from cwd or PYTHONPATH. Both a module file and a package reproduced the fcntl attack. Python -I from / prevents both forms while preserving fd 9 inherited from the parent shell; existing concurrency tests confirmed lock serialization remains intact. Use isolated Python from a trusted cwd for launcher-side inline helpers.

## Plan Updates

The two-call isolation design was retained and validated by the new regression plus existing lock tests. No rule or skill was promoted directly. This learning worklog is not committed.
