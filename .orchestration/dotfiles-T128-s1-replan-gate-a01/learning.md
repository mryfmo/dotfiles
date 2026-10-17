---
task_id: dotfiles-T128-s1-replan-gate-a01
status: pre_push_checkpoint
---

No promotion requested. Two validated reusable observations:
- Python re and jq/Oniguruma native word boundaries differ for combining marks. A shared grammar must use an explicit word-character definition; here Unicode letters/numbers/underscore tokens and exact membership agree across 12 actual-tool cases. The tests cover the discovered U+0301 case without adding more than the requested six methods.
- Temporary Git fixture commits inherit global signing. If the signing key is unavailable inside the sandbox, a process-only commit.gpgsign=false override enables the fixture rather than changing persistent Git config or editing unrelated test setup. Both requested full modules then pass.

The existing acceptance reader is imported by acceptance-front-matter.py; its signature and return shape were preserved. No durable new policy or model setting is promoted.
