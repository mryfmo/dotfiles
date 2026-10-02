# Learning triage: dot-ua-graph-refresh-T55-a01

Candidate lessons only. None is promoted; that decision belongs to the orchestrator.

1. **The worktree redirect conflicts with the worker-worktree rule.**
   - Lesson: Understand-Anything 2.9.7's `/understand` Phase 0 moves `PROJECT_ROOT` from any git worktree to the main checkout. A worker in a `.claude/worktrees/*` worktree would therefore write `.ua/` into the main checkout, which is outside its allowed area.
   - Mitigation used: pin `PROJECT_ROOT`, equivalent to `UNDERSTAND_NO_WORKTREE_REDIRECT=1`.
   - Candidate: future UA graph tasks should state that worker `UNDERSTAND_NO_WORKTREE_REDIRECT=1` is required.
2. **Sandbox mask devices enter the scan.**
   - Lesson: `scan-project.mjs` enumerates with `git ls-files -co --exclude-standard`, which includes untracked files. Inside the Claude sandbox, the `/dev/null` deny masks at the worktree root (`.bashrc`, `.mcp.json`, `.claude/skills`, …) look like untracked files.
   - Mitigation used: pass them as `--exclude`, then check every graph `filePath` against `git ls-files`.
   - Candidate: a repo-side check in the UA acceptance (filePaths ⊆ `git ls-files`).
3. **Stale intermediate shards from an aborted run.**
   - Lesson: `.ua/intermediate/batch-*.json` left by an aborted run (T51) would be merged silently into the next full build, because the merge globs every `batch-*.json`.
   - Mitigation used: clear `.ua/intermediate/` before Phase 1.
   - Candidate: the task template says to start from an empty `.ua/intermediate/`.
4. **`.ua/.trash-*` is not gitignored.**
   - Lesson: the Phase 7 cleanup in 2.9.7 moves scratch into `.ua/.trash-<ts>/`, which is not gitignored. That leaves an untracked tail in the worktree.
   - Mitigation used: send trash to `$TMPDIR`.
   - Candidate: a `.gitignore` entry `.ua/.trash-*/`, via a separate task, since this task forbids `.gitignore` changes.
5. **The `tested_by` linker ignores `.bats`.**
   - Lesson: the merge drops production → `.bats` `tested_by` edges, so graph test coverage under-represents bats suites. This is plugin behavior.
   - Candidate: record it as a known limitation next to the T51/T52 UA notes.
6. **`gitCommitHash` vs branch HEAD wording.**
   - Lesson: "meta `gitCommitHash` must equal your branch HEAD" cannot hold literally once the `.ua` commit exists. The working convention (T41 #212, T55) is that meta holds the analyzed source commit, and the branch HEAD is that commit plus a `.ua`-only commit.
   - Candidate: reword future UA task files to "equals the source HEAD the build ran on; `git diff --name-only <hash>..HEAD` lists only `.ua/`".

## Revise round 1 additions (candidates only)

7. **The skill's validator is weaker than the plugin's.**
   - Lesson: the `/understand` Phase 6 inline validator (`ua-inline-validate.cjs`) checks only presence and references. The plugin's `validateGraph` (`packages/core/dist/schema.js`, used by the dashboard) also validates field types, and it dropped 2 nodes and 20 edges that the inline check passed.
   - Candidate: UA graph acceptance runs `validateGraph` on the committed graph and pastes `validNodes == inputNodes` and `validEdges == inputEdges`.
8. **Symbol coverage is blind to edges.**
   - Lesson: `ua-symbol-coverage` counts symbols only. An analyzer that leaves out intra-file `calls` edges, here because it read "cross-file only" as the rule, passes it with 0 regressions.
   - Candidate: extend `ua-symbol-coverage` (a separate task) or add an acceptance step with per-file outgoing edge counts by type, old vs new.
9. **The fused-batch prompt needs to say "intra-file calls".**
   - Lesson: the file-analyzer for batches 1–3 emitted only cross-file `calls`, and the one for batch 23 emitted none.
   - Candidate: future UA task prompts say explicitly "emit `calls` edges for every call between emitted nodes, intra-file and cross-file", and the self-check compares per-file `calls` counts against the previous graph.
10. **`agmsg-dispatch` sandbox exclusion.**
    - Lesson: `excludedCommands` did not take effect for either seat in this environment (the orchestrator confirmed it). `agmsg-dispatch` has to run with the sandbox disabled.
    - Candidate: a check or doc fix for the excludedCommands rendering, via a separate task.
