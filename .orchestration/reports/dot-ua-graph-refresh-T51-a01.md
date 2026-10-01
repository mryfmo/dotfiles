# Report: dot-ua-graph-refresh-T51-a01 — status=blocked

- worker: claude-standard-dot-a005 (claude-code, standard profile), worktree worker-c
- task_rev: 0d9b7bcb14ded5dc42737f87e8db9bc9262e13ba81b748177d850c3d437b537e (verified with sha256sum)
- branch: `chore/ua-graph-refresh` from origin/main ef9e5be. **No commit**; tracked `.ua/` is unchanged (`git status --short .ua` is empty).
- cost: ≈956k subagent tokens across the 12 file-analyzer dispatches (69.9k + 73.7k + 86.8k + 77.1k + 71.5k + 69.8k + 67.9k + 106.3k + 67.8k + 71.0k + 77.0k + 117.1k), plus this session's own tokens (n/a)

## What ran (verbatim in the validation file)

1. `node ~/.understand-anything-plugin/skills/understand/prepare-incremental.mjs <root> 72b890157078c583f45d71a61ee6eba0df86afb5`: **ARCHITECTURE_UPDATE** with analyze=28, delete=0, cosmetic=3, ignored=208, generated=3. It is not FULL_UPDATE, so I continued. The plugin path is the documented fallback because `$CLAUDE_PLUGIN_ROOT` is unset; it is 2.9.7 and its `skills/understand` is identical to the 2.9.7 cache (`diff -rq` is empty).
2. `compute-batches.mjs --changed-files=…`: 12 batches covering exactly the 28 files: 6, 7, 8, 10, 19, 22, 23, 25, 26, 27, 29, 30.
3. One file-analyzer dispatch per batch (up to 5 concurrent), using the `/understand` batch prompt contract plus `previousSymbols` from `incremental-symbol-baseline.json`. Every batch index has its `batch-<i>.json` on disk (batch 27 in two parts). The analyzers re-emitted every previous symbol ID.
4. `python ~/.understand-anything-plugin/skills/understand/merge-batch-graphs.py <root>`: **exit 1, "Symbol validation blocked publication; baseline not advanced"**. The candidate has 909 nodes and 1333 edges, with 43 `imports` edges recovered.

## Blocker

`incremental-symbol-report.json` has `ok: false` and these `unresolvedFiles`:

- `home/dot_claude/modify_private_settings.json`: 7 of 7 symbols reported "missing"
- `home/dot_local/bin/common/executable_agmsg-dispatch`: 1 of 1
- `home/dot_local/bin/common/executable_herdr-agents`: 34 of 34

All 42 of these old IDs **are present in the candidate graph** (7/7, 1/1, 34/34) with the same id, name and type. Every one is classified `unknown` with the reason "Old symbol cannot be mapped uniquely, or source parsing is unavailable/failed".

**Mechanism:**

- In `validate-incremental-symbols.mjs`, `hasPreservedIdentity` returns false for an unowned callable across revisions unless source evidence verifies it.
- These three files scan as `language: unknown`: two extension-less shell scripts, and a Python chezmoi `modify_` script with a `.json` name. The extractor skips them (the batch-26 and batch-23 analyzers reported this), so no parser evidence exists.
- The plugin's SKILL.md (Phase 2, "Parser limitation") describes this case: callables without explicit class containment in files with no deterministic parser block publication "even when their IDs/names stay unchanged".
- The auto-update prompt says these cases "require manual investigation or parser support. Do not use supplemental LLM inspection or regex guesses to waive the gate."

**The one symbol retry was not run.** `prepare-symbol-retry.mjs` is eligible, because `unresolvedFiles` is non-empty. But re-analysis cannot change the language detection or add a parser, so the second merge would block in the same way. Running it would also record attempt 1/1 for 72b8901..ef9e5be and move these files' nodes out into `batch-0.json`. Under the no-improvisation rule I am asking first. The attempt is still unconsumed, so the orchestrator can still order it.

**Structural consequence:** under UA 2.9.7, any incremental update that re-analyzes `executable_herdr-agents`, `executable_agmsg-dispatch` or `modify_private_settings.json` will block. More generally, so will any extension-less or misnamed script with function nodes. Every `.ua` commit since b277a51 has been a full rebuild, which is consistent with this.

There is no per-path language override that could rescue even the Python file: `.ua/config.json` holds only `outputLanguage` and `autoUpdate`, and the scanner has no shebang detection. A full rebuild is the decision this task reserves for the orchestrator.

## Task-file correction

`git show 72b8901:.ua/knowledge-graph.json` is the graph built at **7b69b1e**: 853 nodes, and that commit's `meta.gitCommitHash` is 7b69b1e. The real 72b8901 baseline is HEAD's graph, committed in 8f1061f (#212), with 885 nodes and 1325 edges. Any `ua-symbol-coverage` table must use that graph as `<old-graph>`.

## State left

- The baseline `knowledge-graph.json`, `fingerprints.json` and `meta.json` are unchanged; `finalize-incremental.mjs` was not run.
- The 12 batch outputs, `assembled-graph.json` and `incremental-symbol-report.json` remain in the gitignored `.ua/intermediate/` for diagnosis.
- No PR exists, and no CompactionDB memory was added, because nothing was accepted to record.

## Side note

The batch-8 analyzer flagged a harmless latent bug in `home/dot_codex/modify_private_{audit,security}.config.toml`: `merge_config` calls `emitted_current.add(current_name)` on a set of chunk indexes. It is out of scope and recorded only for a possible task.

Understand-Anything auto-update hook: the hook fired and was not acted on outside this task's procedure.
