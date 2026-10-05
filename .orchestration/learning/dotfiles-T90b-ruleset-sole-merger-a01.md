# T90b learning

[memory:failure] PR-only bypass limits the merge path, not which protections inside the ruleset can be skipped. Preserve non-bypassable CI, thread resolution and history protection in a separate integrity ruleset. Required approvals alone do not enforce who merges.

[memory:failure] gh pr merge preflight can reject BLOCKED even for a bypass user; --auto does not engage that bypass at completion. Use the authorized synchronous REST merge with exact head SHA after integrity checks, and verify actual operator behavior. Sources and installed version are in report/validation.

A boundary exemption must use the complete committed diff, not filtered review-sizing paths; disable rename detection so moving an outside file under .orchestration cannot hide its deletion.

No rule promotion; decisions recorded by orchestrator at acceptance.
