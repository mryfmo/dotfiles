# T69: CompactionDB Pi extension — tool-granular capture (π3)

task_id: T69
repo: /Users/mryfmo/Workspace/dotfiles
team: dotfiles-conformance
worker: codex-deep-dot
plan: .orchestration/tasks/PLAN-pi-worker-integration.md (Phase 5)
depends: T66 (accepted)

[memory: decision — Pi sessions in CompactionDB-opted-in projects get tool-granular automatic capture via the contextdb.ts extension: tool_execution_end, turn_end, and session_compact flow into `ingest --ingested-from pi` with the same never-block, silent-failure contract as the codex notify receiver.]

## Goal

Give Pi workers capture parity BEYOND codex (tool granularity, not just
turn granularity), using the extension events confirmed in the pinned
v0.84.1 sources.

## Allowed files (edit boundary)

- home/dot_pi/agent/extensions/contextdb.ts (NEW)
- scripts/validate-agent-assets.py (add the extension to the pi-assets
  SHA-256 integrity set — same mechanism as permgate.ts)
- tests/unit/ (matching modules; handler-direct node tests like T66)
- Your artifact paths (T69 five artifacts)
- FORBIDDEN: vendor/compactiondb/\*\* (`--ingested-from pi` passes the
  existing token validation; if anything vendor-side blocks, STOP and ask)

## Forbidden actions

git commit; git push; chezmoi apply; bats; dependency changes; vendor
changes; real pi execution; network access from the extension; blocking
any Pi operation on capture failure.

## Extension spec (fixed)

- Default-export factory per the pinned loader contract (reuse T66's
  cited anchors).
- Events: `tool_execution_end` (normalize {tool, success, primary arg —
  command for bash, path for read/write/edit, pattern for grep/find}),
  `turn_end` (last assistant text, 240-char cap), `session_compact`
  (summary text).
- Delivery: only when `<cwd>/.claude/hooks/contextdb_cli.py` exists, run
  `python3 <cwd>/.claude/hooks/contextdb_cli.py ingest --ingested-from pi`
  with a hook-shaped JSON payload on stdin (mirror the codex receiver's
  payload shape so normalize maps it; the T48-established contract).
  5s timeout per invocation; every failure silent (one stderr line
  allowed); NEVER throws into Pi's event loop (wrap all handlers).
- Non-opted cwd: completely silent no-op (existence check cached per
  session start, re-checked on session_start event).
- No state files, no network, node builtins + pi virtual modules only.

## Tests (handler-direct via node, child_process stubbed)

(a) each of the three events produces one ingest invocation with the
normalized payload (assert argv + stdin);
(b) non-opted cwd -> zero invocations;
(c) ingest failure/timeout -> handler returns normally, one stderr line;
(d) thrown-exception guard: a handler internal error never propagates
(assert the wrapper);
(e) validate integrity: matching hash passes, tampered fails.

## Validation (record in validation artifact)

1. make format / unit-test / validate-agent-assets green (+ node --check
   / tsc --noEmit per the T66 choice).
2. Fixture transcripts for (a)-(d).
3. `git status --porcelain` / `git diff --stat` -> only Allowed files.

## Completion / RESULT contract

Five artifacts (T69 set); memory add with the decision fact;
effects=none. Live capture proof is T72 E2E-π3.
Reply `AGMSG-RESULT v1 task_id=T69`. max_turns=20.
