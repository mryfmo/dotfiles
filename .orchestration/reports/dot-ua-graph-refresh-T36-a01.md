# T36 report: .ua knowledge-graph refresh (dot-ua-graph-refresh-T36-a01)

- worker: claude-standard-dot-a005 (worktree `.claude/worktrees/worker-c`)
- task_rev: c7bde73e21f49c294c4d0ae73258550ff9f3b4513ac8125ac66b69c9e0bde847 (sha256 verified against origin/main 7b69b1e; the first dispatch, 741320f2…9da, was verified against 2126564)
- branch: `chore/ua-graph-refresh-T36` from origin/main 7b69b1e
- commit: 476c6e1 `chore(ua): full knowledge-graph rebuild at 7b69b1e (T36)`
- PR: https://github.com/mryfmo/dotfiles/pull/208 (head 476c6e1, MERGEABLE; CI 12/12 pass, nix skipped; CodeRabbit skipped)

## What happened

1. **Incremental path tried first.** With plugin 2.9.7 and the core built in
   `~/.understand-anything-plugin`, `prepare-incremental.mjs` against base
   935e198 returned `FULL_UPDATE`: analyze=29, delete=67, cosmetic=1,
   ignored=150, generated=3. Its reason was "96 files have structural changes
   (>30 files)". Per the task I stopped and sent `AGMSG-PONG status=blocked`
   (05:54:45Z) with the size estimate, sent it again after the task-text
   correction (7b69b1e), and received ruling (a), a full run in this session,
   at 05:56:53Z.
2. **Full `/understand --full`** in worker-c, with the worktree redirect
   disabled so every write stayed in worker-c `.ua/`. The stale
   `.ua/intermediate` and `.ua/tmp` from T33c were first moved into the
   session scratchpad, because the merge script switches to incremental mode
   whenever `intermediate/incremental-plan.json` exists. The skill has two interactive confirmation gates: the Phase 0.5 `.ua/.understandignore` review and the Phase 1 >100-file warning. No operator was in the loop, and ruling (a) did not mention either gate, so I passed both on my own judgment. `.understandignore` is unchanged since b277a51, the baseline T33c used, and ruling (a) was given knowing the ~356-file size. The Phase 1 scanner counted 360 files, 4 more than the helper's 356; the extra files are `.ua/`'s own data files (see Notes).
3. **Phases:** scan (360 files, 1621 filtered) → 31 semantic batches → 31
   file-analyzer dispatches → merge (853 nodes / 1219 edges; 53 `tested_by`
   edges dropped as orphan or same-side pairs) → assemble-reviewer (no
   changes) → architecture (9 layers, previous layer IDs kept) → tour (15
   steps) → inline validation (0 issues, 92 orphan warnings) → save,
   fingerprints (360 files), then meta.
4. **Validation before commit.** Core `validateGraph` gave 853/853 nodes,
   1219/1219 edges, 0 issues. The non-tuple `lineRange` count is 0.
   `meta.gitCommitHash` is 7b69b1e, which equals the branch base.
5. **Commit scope** is exactly `.ua/knowledge-graph.json`,
   `.ua/fingerprints.json` and `.ua/meta.json`. `.gitignore` already
   contained `.ua/intermediate/` and `.ua/diff-overlay.json` (and
   `.ua/tmp/`), so no change was needed. `.ua/config.json` is unchanged.

## Counts before → after

|                | before (graph at 7b69b1e, meta 935e198) | after (commit 476c6e1, meta 7b69b1e) |
| -------------- | --------------------------------------- | ------------------------------------ |
| nodes          | 870                                     | 853                                  |
| edges          | 1333                                    | 1219                                 |
| analyzed files | 424                                     | 360                                  |
| layers         | 9                                       | 9                                    |
| tour steps | 15 | 15 |

After, by node type: file 264, function 457, class 35, config 48,
document 40, pipeline 7, service 2.

After, by edge type: contains 493, calls 267, exports 121, depends_on 94,
documents 67, related 59, imports 43, tested_by 40, configures 24,
triggers 11.

The drop is fully reconciled. 67 file-level paths left the scan, all of them
vendored agmsg files: 34 under `home/dot_agents/skills/agmsg`, 31 under
`home/dot_claude/skills/agmsg`, plus `tests/unit/test_agmsg_send.py` and
`home/dot_claude/commands/symlink_agmsg.md.tmpl`. Three new test files were
added, so 424 − 67 + 3 = 360.

## Notes and deviations

- **Dispatch prompts** were generated verbatim from the skill's templates
  into scratchpad files. Each agent was told to read its file, which kept
  the 31 payloads out of the orchestration context. Each prompt added one
  constraint: `lineRange` must be a two-integer tuple or omitted (the T33c
  P2) and nothing may be written outside worker-c `.ua/`.
- **The full-path scanner includes `.ua/`'s own 4 data files**
  (config.json, fingerprints.json, knowledge-graph.json, meta.json) as
  nodes. The incremental helper excludes them. The T33c graph had the same 4
  nodes, so the documented full-path behavior was kept.
- **Phase 7 cleanup** moved scratch output into the session scratchpad, not
  `.ua/.trash-*`, which `.gitignore` does not cover. The dashboard
  auto-launch (Phase 7 step 6) was skipped because it is outside the task.
- **The PostToolUse auto-update hook** fired twice: after the commit, and again after the validation-file write. I did not act on it either time: `git diff --name-only 7b69b1e..HEAD` lists only `.ua/` paths, which
  the task accepts as current.
- **Plugin gaps seen again** (as in T33c):
  - the extractor misses shell functions with a subshell body; analyzers added 7 by hand;
  - it has no parser for `.tmpl`/`.bats`/extensionless files, so analyzers read those directly;
  - 53 `tested_by` edges were dropped by the merge linker.

[memory:decision] T36: the `.ua/` knowledge graph is refreshed incrementally
by a worker task whenever the SessionStart hook reports it stale; the
orchestrator never runs the graph update in its own session (operator
2026-09-28).

[memory:failure] T36: a graph left stale across the T33a–T35 batch (96
structural files including the vendored agmsg removal) exceeded
prepare-incremental's 30-file threshold and forced a second full rebuild of
35 dispatches; refresh right after each accepted batch to stay incremental.

- **`fingerprints.json` entries for `.ua/`'s own files are stale.** The
  entries for `.ua/fingerprints.json` and `.ua/meta.json` were hashed before
  those two files were rewritten; the graph was saved first, so its entry is
  current. This is harmless because `prepare-incremental` excludes `.ua/`
  with `--exclude-analysis-data`. T33c had the same entries.

## CompactionDB (main checkout)

```
$ cd ~/Workspace/dotfiles && python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content "T36: the .ua/ knowledge graph is refreshed incrementally by a worker task whenever the SessionStart hook reports it stale; the orchestrator never runs the graph update in its own session (operator 2026-09-28)."
c99ba88c-c4da-4e34-a776-f53f538d8be8
```

## Effects

None outside the repository working tree. Scratch files live only in this
session's scratchpad.

cost: 35 LLM dispatches (1 project-scanner + 31 file-analyzer + 1 assemble-reviewer + 1 architecture-analyzer + 1 tour-builder), 0 retries; subagent tokens 2,733,626 total as reported by the harness (scan 58,715; 31 analyzers 2,427,464, range 61,219–125,816; assemble 50,954; architecture 101,097; tour 95,396); orchestrating-session token/cost figures n/a.
