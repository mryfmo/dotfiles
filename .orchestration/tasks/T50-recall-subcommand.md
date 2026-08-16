# T50: `contextdb recall` — dual-view fusion retrieval (P3)

task_id: T50
repo: /Users/mryfmo/Workspace/dotfiles
team: dotfiles-conformance
worker: codex-deep-dot
plan: .orchestration/tasks/PLAN-compactiondb-research-integration.md (Phase 5)
analysis: .orchestration/analysis/compactiondb-compaction-research.md (P3)
depends: T46 (accepted)

[memory: decision — CompactionDB gains a zero-token `recall` subcommand fusing FTS5 lexical rank with optional external-embedding similarity (min–max normalized, rho=0.6) plus a three-path closure (same tool_use_id, adjacent event id in session, shared file), read-only and deterministic when embeddings are unset.]

## Goal

Query-conditioned retrieval over events and memories (Zero-Mem's dual-view
idea reduced to this ledger's scale): lexical FTS5 + optional semantic
view, min–max normalization, weighted fusion, co-occurrence closure.
No NER, no PageRank, no new embedding generation.

## Allowed files (edit boundary)

- vendor/compactiondb/.claude/contextdb/contextdb/cli.py (subcommand wiring)
- vendor/compactiondb/.claude/contextdb/contextdb/recall.py (NEW module)
- vendor/compactiondb/.claude/contextdb/contextdb/config.py and
  vendor/compactiondb/.claude/contextdb/config.json (ONLY two new keys:
  `recall.rho` default 0.6, `recall.k` default 5; validation in sibling
  style — rho is a number in [0,1], k a non-negative int)
- vendor/compactiondb/tests/test_recall.py (NEW)
- vendor/compactiondb/README.md and the fitting docs/ file
- vendor/compactiondb/CHANGELOG.md (append to 2.0.0+dotfiles.4)
- vendor/compactiondb/MANIFEST.sha256
- Your artifact paths (T50 five artifacts)

## Forbidden actions

git commit; git push; chezmoi apply; bats; dependency changes; LLM or
network calls; embedding GENERATION (only existing stored vectors via the
existing semantic command pathway may be used for the QUERY embedding —
if computing a query embedding requires invoking the external semantic
command, that IS allowed since semantic.py already owns that pathway; no
other external processes); DB writes from recall; changes to
recovery.py/probe.py/storage.py/spool.py/hook.py.

## Work order (exact; ambiguity -> ask via agmsg)

1. `recall "<query>" [--session <id>] [--k N] [--json]`.
2. Lexical view: FTS5 rank (bm25) over events_fts AND memories_fts;
   respect the existing tokenizer selection (trigram/unicode61).
3. Semantic view: ONLY when semantic embeddings are configured AND stored
   vectors exist: embed the query via the existing semantic.py pathway,
   cosine against memory_embeddings. When unavailable, lexical-only
   (silent, deterministic; never an error).
4. Normalization per view (Zero-Mem rule): absent -> 0.0; max==min -> 1.0;
   else (s - min) / (max - min). Fusion: rho _ lexical + (1 - rho) _
   semantic (config `recall.rho`).
5. Closure on top hits that are events: pull (a) events sharing
   tool_use_id, (b) same-session events with adjacent id (±1), (c) events
   touching the same file via event_files. Closure items inherit
   parent_score \* 0.5 and rank directly after their parent; dedup by
   event_uuid keeping the higher score.
6. Output top `recall.k` (CLI --k overrides): text lines
   `<score> <ts> <kind> <summary>`; --json returns full rows plus a
   `via` field (`lexical`, `semantic`, `fused`, `closure:<path>`).
7. Session filter `--session` restricts events to that session; memories
   remain project+that-session scope (same visibility rule as probe).
8. Tests (test_recall.py): (a) lexical-only deterministic ranking on a
   fixed fixture (pin expected order); (b) fusion math with a fake
   embedding command (reuse test_semantic.py's technique); (c) min–max
   degenerate cases (single hit; all-equal scores); (d) three closure
   paths + dedup + score inheritance; (e) --session filtering excludes
   other sessions; (f) read-only (DB hash identical, probe-style);
   (g) rho/k config load + CLI override.
9. Docs: usage + the two intended operational uses (worker recall at task
   start; orchestrator past-failure lookup at acceptance).
10. CHANGELOG bullet (2.0.0+dotfiles.4); MANIFEST regeneration.

## Validation (record in validation artifact)

1. `make -C vendor/compactiondb clean && make -C vendor/compactiondb test`
   -> all green (totals).
2. `make -C vendor/compactiondb clean && make -C vendor/compactiondb validate`
   -> 0 fail.
3. `git status --porcelain` / `git diff --stat` -> only Allowed files.
4. Three example recalls from a populated fixture (exact file path;
   Japanese phrase; English phrase) pasted with their outputs.
5. Performance smoke: a generated fixture of ~10k events; recall wall time
   recorded (target <1s; record the number, do not tune unless it fails).

## Completion / RESULT contract

- Five artifacts at .orchestration/{reports/T50.md, validation/T50.txt,
  sandboxes/T50.md, learning/T50.md, autoskill/runs/T50.md}.
- Report uses `[memory:...]` markers; no `memory add` here.
- Reply `AGMSG-RESULT v1 task_id=T50 status=ready_for_review ...`.
  max_turns=25.
