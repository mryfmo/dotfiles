# Report: dot-ua-graph-refresh-T55-a01

- Worker: `claude-standard-dot-a005` in `/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c`
- Task file sha256 `c4f1df2e32d7a7ae634d25fd4a93573f5b3c8abab0e97fd74c99e27b7a95ffae`. It matches the dispatched task_rev. It was verified against the main-checkout copy because the task file is not committed on `origin/main`: `git show origin/main:<task>` is empty, sha `e3b0c442…`.
- Branch `chore/ua-graph-refresh-T55` from `origin/main` 940a3a2b; one commit `98bdf43ff966f4b73dd25832d1f77c1196dc0bdb`; PR #226 (https://github.com/mryfmo/dotfiles/pull/226).
- Status: ready_for_review. CI is green on `98bdf43f`: 12 pass and `nix` skipped by change detection. CodeRabbit shows pass because automatic reviews are disabled. The verbatim `gh pr checks 226` output is in the validation file.

## What was done

A full rebuild with Understand-Anything 2.9.7, `/understand --full`, run through every phase from 0 to 7:

| Phase           | What happened                                                                                                   |
| --------------- | --------------------------------------------------------------------------------------------------------------- |
| Scan            | `project-scanner` agent: 368 files, 13 languages, frameworks Docker and GitHub Actions.                         |
| Batching        | 31 batches.                                                                                                     |
| Analysis        | 19 `file-analyzer` dispatches, with small batches fused. Every batch was written per `batchIndex`, as 38 files. |
| Merge           | `merge-batch-graphs.py`.                                                                                        |
| Assemble review | `assemble-reviewer` agent: no fixes needed.                                                                     |
| Architecture    | `architecture-analyzer` agent: 9 layers, with the same IDs and names as before.                                 |
| Tour            | `tour-builder` agent: 15 steps.                                                                                 |
| Validation      | Inline validator: 0 issues and 45 orphan warnings.                                                              |
| Save            | `build-fingerprints.mjs` (368 files), then `meta.json`.                                                         |

Results:

- **Graph size:** 885 → 984 nodes and 1325 → 1774 edges.
- **`ua-symbol-coverage`:** 368 files, 0 regressions. Every per-file symbol change is an increase, for example `herdr-agents` 34 → 44, `update-agent-assets.sh` 30 → 41 and `upgrade-tools.sh` 22 → 35. The new files are `executable_ua-symbol-coverage` (0 → 6) and its test (0 → 3).
- **Config:** `.ua/config.json` is unchanged (`git diff --exit-code` exits 0).
- **Ignored paths:** `.ua/intermediate/`, `.ua/tmp/` and `.ua/diff-overlay.json` are not committed.

## Deviations and judgment calls

- **Worktree redirect overridden.** Phase 0 of the skill redirects `PROJECT_ROOT` from a worktree to the main checkout. That would have written `.ua/` outside the worktree, which the task forbids. `PROJECT_ROOT` was pinned to worker-c, the same as `UNDERSTAND_NO_WORKTREE_REDIRECT=1`.
- **Sandbox placeholders excluded.** The worktree root shows 19 untracked character devices (1,3): `.bashrc`, `.zshrc`, `.gitconfig`, `.mcp.json`, `.idea`, `.vscode`, `.claude/{agents,commands,skills,workflows,...}` and others. These are Claude sandbox `/dev/null` bind-mount deny masks. The scanner enumerates with `git ls-files -co --exclude-standard`, which includes untracked files, so they were passed as `--exclude` patterns. A post-build check confirms every graph `filePath` is in `git ls-files`.
- **Stale scratch moved out.** `.ua/intermediate/` still held batch shards from the T51 attempt. They were moved into a trash directory before the scan so the merge could not pick them up. The skill's `.ua/.trash-*` directory is not gitignored, so trash goes to `$TMPDIR/ua-trash/` instead of `.ua/`.
- **`.understandignore` confirmation (Phase 0.5).** The committed file was used as is, with no interactive wait, because this is a non-interactive worker.
- **Dashboard not launched.** The Phase 7 dashboard auto-launch was skipped. This is a non-interactive worker, and a launch would leave a server running.
- **Large inputs passed by file.** File-analyzer, architecture and tour inputs were handed to the agents through `batches.json` and `.ua/tmp/*.json` files instead of being pasted into prompts. The content is the same.
- **`gitCommitHash` vs branch HEAD.** `meta.json` `gitCommitHash` is `940a3a2b`, the source commit the graph was built from. The branch HEAD is `98bdf43f`, the `.ua` commit on top of it. A commit cannot contain its own hash, and `git diff --name-only 940a3a2b..HEAD` lists only `.ua/` paths, so the freshness rule treats the graph as current. This matches T41 (#212): meta `72b89015`, `.ua` commit `8f1061fd`.

## Known plugin limitation (not patched)

- The merge's `tested_by` linker drops production → `tests/**/*.bats` edges because it does not classify `.bats` as test files. 62 unique pairs were dropped, plus 2 config → `.py` pairs that its pairing rule rejects. The previous graph had only `.py` `tested_by` edges, 39 of them, for the same reason; the new graph has 51.
- The extractor has no parser for `tmpl`, `bats`, `nix` or extension-less executables, and it does not detect shell functions written `name() ( … )`. The analyzers added those symbols by hand from source; the coverage table shows no losses.
- The scan covers `.ua/` itself, as the previous graph also did. So the `config:.ua/knowledge-graph.json`, `config:.ua/fingerprints.json` and `config:.ua/meta.json` node summaries describe the pre-rebuild files: 885 nodes / 1325 edges and 365 files at 72b8901. That lag is inherent to a graph indexing its own directory. The graph was not hand-edited to hide it.

## Understand-Anything hook

- `.ua/**` is in `allowed_files`, so acting on the graph build is in scope. No auto-update hook prompt fired during the task (`autoUpdate: false`).

## CompactionDB

```
cd /home/moriya/Workspace/dotfiles && python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content "T55 (operator 2026-10-02): the .ua/ graph is rebuilt in full as the semantic index before the whole-repository review of tools, libraries and content; the orchestrator never runs the graph build in its own session."
958a79ca-0099-4276-9294-b834ee886185
```

[memory:decision] T55 (operator 2026-10-02): the `.ua/` graph is rebuilt in full as the semantic index before the whole-repository review of tools, libraries and content; the orchestrator never runs the graph build in its own session.

## Artifacts

- validation: `.orchestration/validation/dot-ua-graph-refresh-T55-a01.md`
- sandbox: `.orchestration/sandboxes/dot-ua-graph-refresh-T55-a01.md`
- learning: `.orchestration/learning/dot-ua-graph-refresh-T55-a01.md`
- autoskill: `.orchestration/autoskill/runs/dot-ua-graph-refresh-T55-a01.md`

cost: n/a for this session (the runtime does not expose session totals); the 23 plugin subagents (1 scanner, 19 file-analyzer, 1 assemble-reviewer, 1 architecture, 1 tour) reported 2,279,549 tokens in their task notifications.

## Revise round 1 (task_rev sha256:6540ebdd…)

- **Result:** a new commit `8694200f9fa0a36d3dec8f8a95a0a9f7c7186c52` on top of `98bdf43f`, on the same branch and PR #226, with no force push. The diff from `98bdf43f` touches `.ua/` only.
- **Size:** 984 nodes / 1985 edges, against 984 / 1774 in round 0 and 885 / 1325 in the previous graph.

### Both audit findings were real, and round 0's report was wrong

- **"0 validation issues" was wrong.** Round 0's inline validator does not check field types. The plugin's own `validateGraph`, the dashboard's load path in `packages/core/dist/schema.js`, rejected 2 nodes and 20 edges on the round-0 graph, and I did not run it then. The validation file now pastes it for both graphs.
- **The round-0 coverage check missed lost edges.** `ua-symbol-coverage` counts symbols, so dropped edges went unnoticed. I added a per-file outgoing-edge comparison over all edge types; the script is pasted in full.

### What changed

1. **`lineRange` prose.** `file:home/dot_claude/hooks/executable_enforce-uv.sh` and `config:home/dot_claude/modify_private_settings.json` now have their prose in `languageNotes`. Their `lineRange` is the numeric whole-file range: `[1, 281]` and `[1, 197]`. The count of non-numeric `lineRange` values is 0, and `validateGraph` keeps all 984 nodes and 1985 edges with 0 issues.
2. **Lost edges.** I rebuilt a checklist of every previous-graph edge missing from the round-0 graph, across all edge types: 102 `calls` plus 48 others, in 12 batches. The 102 `calls` are all in contextdb (batches 1–3) and `attach_comment_files.py` (batch 23).
   - **Batches 1–3 and 23 were re-analyzed with the plugin's `file-analyzer`.** The bundled extractor was re-run, and every call between emitted nodes is now an edge, intra-file and cross-file. All 102 `calls` checklist edges are restored.
   - **The other batches were amended edge-only:** 7, 9, 11, 12, 19, 20, 21 and 28. Each checklist edge was re-verified against current source and restored where it still holds. 46 of the 48 non-calls edges are back.
   - **Two edges are deliberately not restored:** the `exports` edges `paths.py → _load_or_create_project_id` and `recover_hook.py → _record_recovery_injected`. Both helpers are underscore-private, the modules have no `__all__`, and they are called only inside their own file; the `git grep` is pasted in the validation file. The previous graph's `exports` edges for them were wrong. Both helpers are still linked by `contains` and by `calls` from `project_paths` and `recovery_output`.
   - **Outcome:** no file has fewer outgoing `calls` edges than in the previous graph (220 → 629 in total). The only per-file decreases of any type are those two `exports` edges.
   - **Duplicate-typed pairs:** 10 restored edges sit next to an existing edge of another type between the same endpoints (`related` + `depends_on`, `configures` + `depends_on`). Both are kept, because the merge dedups by `(source, target, type)`.
3. **Unchanged:** layers and tour are byte-for-byte the round-0 assignments (asserted before saving). `meta.json` `gitCommitHash` stays `940a3a2b`; only `lastAnalyzedAt` moves.
   - `fingerprints.json` changed only in `generatedAt` and in the three `.ua/` self-entries (the graph indexes its own directory).
   - `ua-symbol-coverage`: 368 files, 0 regressions.
   - The assemble-review LLM pass was not re-run. Its checks are deterministic or covered by the plugin's `validateGraph`, which now reports 0 issues.

### Correction to the commit message

The `8694200f` message says "77 other lost edges … are re-verified against source and restored". The correct figure is **48** checklist edges of other types, of which **46** were restored and 2 left out as explained above. Rewriting it would need a force push, which is forbidden, so the correction is recorded here and in the PR description.

### Round-1 cost

cost (round 1): n/a for this session. The 4 revise `file-analyzer` subagents reported 374,399 tokens (79,429 + 84,158 + 88,940 + 121,872).

[memory:failure] T55 round 0: the inline validator in /understand passed 0 issues on a graph that the plugin's own `validateGraph` rejected (prose in `lineRange`). `ua-symbol-coverage` also cannot see lost edges. UA graph acceptance needs the plugin `validateGraph` output and a per-file edge comparison in addition to symbol coverage.
