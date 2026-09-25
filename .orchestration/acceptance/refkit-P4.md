# refkit-P4 acceptance record

status: accepted (2026-09-23T11:0xZ)
reviewer: claude-remediation-dot

## Verified
- 56bd3fa: ADR-0001/0002 diffs are exactly the two front-matter keys each. ADR-0003 narrows `addresses` to FR-008, states FR-010/FR-024 as not decided here, option C covers both the decision entry point and the ACT-006 期限処理 entry point, 4.2 gains the second entry-point row. ADR-0004 adds the FR-017 mechanism comparison (a/b/c) and adopts a periodic scan, records the 24h cleanup/競合 consequence, fixes 関連 to RULE-011〜014, carries the 冪等キー definition. Both are full MADR structures with all options having 短所.
- Deviations accepted with reasons: (1) `proposed-on` not added to the template because E024 requires exact key-set parity and accepted ADRs may not gain keys → moved to refkit-P4b together with the linter change; (2) E086 selftest mutations deferred to P4b as the task itself said.
- New E103×2 (new Mermaid diagrams) is expected until P9 regenerates `mermaid_render.json`.

## Follow-ups created
- The `.prettierignore` from P0-05 works only when prettier's cwd is the repository root; from `references/` or `/tmp` the same file is flagged, and `uvx ruff format --check` from `/tmp` reports the kit file as reformattable. The hook runs in the session's current directory, so P0-05 is insufficient. → refkit-P0-06 (fix the hook source in this repo, if managed here) drafted.

cost: n/a
