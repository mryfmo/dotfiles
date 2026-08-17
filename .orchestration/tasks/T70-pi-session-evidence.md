# T70: pi-session-evidence — acceptance-record extraction from session JSONL (π5)

task_id: T70
repo: /Users/mryfmo/Workspace/dotfiles
team: dotfiles-conformance
worker: codex-deep-dot
plan: .orchestration/tasks/PLAN-pi-worker-integration.md (Phase 6)
depends: T68 (accepted)

[memory: decision — Pi worker acceptance reviews consume a deterministic extract of the session JSONL: pi-session-evidence prints compaction details (readFiles/modifiedFiles), model changes, usage/cost totals, and branch structure from the tree-ordered active path, read-only.]

## Goal

Machine-extract the acceptance-relevant facts from a Pi session file so
orchestrator reviews of Pi workers get the same evidence quality as
CompactionDB gives for Claude/Codex.

## Allowed files (edit boundary)

- home/dot_local/bin/common/executable_pi-session-evidence (NEW; bash or
  python per repo conventions — python via uv shebang is acceptable;
  state the choice)
- tests/unit/ (matching module with fixture JSONL files)
- Your artifact paths (T70 five artifacts)

## Forbidden actions

git commit; git push; chezmoi apply; bats; dependency changes; real pi
execution; writing to the session file (read-only, open without
modification).

## Spec (fixed)

`pi-session-evidence <session.jsonl> [--json]`:

1. Parse the entry tree (id/parentId per the pinned v0.84.1 session
   format — cite the reference doc/source lines). Determine the ACTIVE
   path (root -> current leaf; investigate how the leaf is identified in
   the format and document it — if the format does not persist the leaf
   pointer, use the last appended entry's branch and say so).
2. Extract, from the active path: CompactionEntry list (summary first
   120 chars, tokensBefore, details.readFiles/modifiedFiles),
   ModelChangeEntry list (model ids in order), usage/cost aggregation
   from assistant message entries (input/output/cacheRead/cacheWrite
   token totals and cost totals when present), entry counts by type, and
   branch statistics (total entries vs active-path entries, number of
   leaves).
3. Output: human-readable summary by default; `--json` for the full
   structured form. Malformed lines are counted and reported, never
   fatal (best-effort with a warning line).
4. Bounded: cap file read at 50 MB with a clear error beyond.

## Tests

Fixture JSONLs: linear session; branched session (fork + two leaves);
session with compaction + model change; malformed-line tolerance;
oversize refusal.

## Validation

make format / (bash -n or uv checks) / unit-test / validate-agent-assets
green; fixture transcripts; scope check.

## Completion / RESULT contract

Five artifacts (T70 set); memory add with the decision fact;
effects=none. Live use is T72 E2E-π5.
Reply `AGMSG-RESULT v1 task_id=T70`. max_turns=15.
