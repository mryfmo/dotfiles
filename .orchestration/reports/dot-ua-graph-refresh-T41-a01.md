# T41 report: .ua knowledge-graph refresh (dot-ua-graph-refresh-T41-a01)

- worker: claude-standard-dot-a005 (worktree `.claude/worktrees/worker-c`)
- task_rev: 05dc8ca7250cd5aa2696f5d6ed2c9d60bdfd4b57be8420489c022b80db4aceb2 (sha256 verified against the main-checkout file and the `origin/main:` blob at 72b8901)
- branch: `chore/ua-graph-refresh-T41` from origin/main 72b8901. worker-c was clean and detached at 9184fe4 before the switch.
- commit: c3afc7a `chore(ua): full knowledge-graph rebuild at 72b8901 (T41)`
- PR: https://github.com/mryfmo/dotfiles/pull/212 (revision 2 head 7ee3658; CI 12/12 pass, nix skipped; MERGEABLE)

## 1. Incremental attempt (recorded verbatim, per ruling)

- `prepare-incremental.mjs "$PWD" 7b69b1e…` →
  `scan-project: filesScanned=361 filteredByIgnore=1671 complexity=large` /
  `Incremental plan: ARCHITECTURE_UPDATE; analyze=30; delete=0; cosmetic=2; ignored=51; generated=3`
  (`"reason":"30 files have structural changes — architecture re-analysis needed"`, rerunArchitecture/rerunTour true).
- `compute-batches --changed-files` → 15 batches. I dispatched 15 file-analyzers with `previousSymbols` from `incremental-symbol-baseline.json`. Every agent confirmed it re-emitted each previous symbol with its original ID.
- `merge-batch-graphs.py` → **exit 1**, "Symbol validation blocked publication; baseline not advanced". The **candidate was 874 nodes / 1318 edges**.
- `unresolvedFiles` = `install/ubuntu/common/aws_cli.sh`, `install/ubuntu/common/dependencies.sh`, `scripts/check-tools.sh`. 13 old symbols (3/3/7) were flagged `status: unknown`, "Old symbol cannot be mapped uniquely, or source parsing is unavailable/failed". A per-ID check showed **all 13 IDs present** in the candidate. The gate has no deterministic parser for `.sh`, and auto-update-prompt.md says such cases "remain unknown and require manual investigation or parser support" and must not be waived.
- I stopped before the one mandated retry and PONGed (11:00Z; the evidence correction at 11:01Z). The retry re-analyzes the same `.sh` files and cannot fix a parser limit. Ruling (b) at 11:03:20Z: full rebuild, skip the retry.
- The incremental evidence (plan, symbol report, merge stderr, candidate counts) is kept in the session scratchpad. Nothing from it was published.

## 2. Full rebuild (`/understand --full` path)

- The stale intermediates were moved to the scratchpad, because the merge script switches to incremental mode when `incremental-plan.json` exists. The worktree redirect was disabled. `.understandignore` is unchanged since b277a51.
- Scan: 365 files (the helper's 361 plus `.ua/`'s own 4 data files, which the full-path scanner includes, as in T36), with 1671 filtered. 31 batches.
- Merge: 841 nodes / 1192 edges. 44 `tested_by` edges were dropped by the linker, and 3 `calls` edges in `apparmor_userns.sh` were dropped as dangling.
- The assemble-reviewer made three kinds of fix:
  - It recovered the 3 missing `apparmor_userns.sh` function nodes (`profile_source`, `skip_reason`, `install_profile`) and restored the 3 dropped edges, giving 844 / 1198.
  - It **removed 4 prose `lineRange` values**: `file:home/dot_bash/client/bashrc`, `file:home/dot_claude/hooks/executable_enforce-uv.sh`, `config:home/dot_claude/modify_private_settings.json` and `file:home/dot_claude/private_mcp.json.tmpl`. This is the T33c P2 pattern recurring despite the tuple rule in every analyzer prompt.
- Architecture: 9 layers, previous IDs kept, 366 file-level nodes each assigned once. Tour: 15 steps, all 65 node references valid.
- Inline validator: 0 issues (52 orphan warnings). Core `validateGraph`: 844/844 nodes, 1198/1198 edges, 0 issues. Non-tuple `lineRange`: 0.
- Save order: graph, then fingerprints (365 files), then meta. Commit scope is exactly the three `.ua/` files; `.gitignore` is unchanged, since it already has both lines.

## Counts before → after

| | before (graph at 72b8901, meta 7b69b1e) | after (commit c3afc7a, meta 72b8901) |
|---|---|---|
| nodes | 853 | 844 |
| edges | 1219 | 1198 |
| analyzed files | 360 | 365 |
| layers / tour | 9 / 15 | 9 / 15 |
| incremental candidate (not published) | — | 874 / 1318 |

After, by type: file 267, function 442, class 36, config 49, document 41, pipeline 7, service 2.

New in the graph (T37–T39): `scripts/pr-feedback.py`, `tests/unit/test_pr_feedback.py`, `rules/pr-integration.md` and its symlink, `.coderabbit.yaml`, `check_claude_sandbox`, `render_claude_sandbox`, `validate_claude_sandbox`, `base_ref_error`-era guard functions, and more.

The full rebuild has fewer edges than the incremental candidate (1198 vs 1318). Its analyzers see an empty neighborMap and add fewer cross-batch edges, and the linker dropped 44 `tested_by` edges.

## Secret / sensitive-value scan

- Common token/key patterns: 0.
- `model-profiles.env` values of 12+ characters: **1 hit**, `MODEL_PROFILE_AUDIT_CODEX_ARGS` = `--profile audit`. It appears in the summary of `config:home/dot_codex/modify_private_audit.config.toml`. It is a non-secret CLI argument, and `home/dot_agents/model-profiles.env` is tracked in this public repo. I left it as is, since hand-editing generated summaries for a coincidental phrase is not warranted. Recorded so the acceptance check is not surprised.

## Notes

- The auto-update hook fired after the commit. I did not act on it: `git diff --name-only 72b8901..HEAD` lists only `.ua/` paths.
- Dispatch prompts were generated verbatim from the skill templates into files, with the added lineRange-tuple, worktree and secret constraints.

[memory:decision] T41 (re-affirms T36): the `.ua/` knowledge graph is refreshed incrementally
by a worker task whenever the SessionStart hook reports it stale; the
orchestrator never runs the graph update in its own session (operator
2026-09-29).

[memory:failure] T41: any Understand-Anything incremental update that touches a `.sh` file with function nodes blocks at `merge-batch-graphs.py` (the symbol gate marks them `unknown`: no deterministic shell parser) until the plugin gains a shell parser or `.sh` symbols are excluded; the fallback is a full `/understand` rebuild.

## CompactionDB (main checkout)

```
$ cd ~/Workspace/dotfiles && python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content "T41 (re-affirms T36): the .ua/ knowledge graph is refreshed incrementally by a worker task whenever the SessionStart hook reports it stale; the orchestrator never runs the graph update in its own session (operator 2026-09-29)."
6704a725-799b-4c4b-ad51-d8adec806abc
$ python3 .claude/hooks/contextdb_cli.py memory add --kind failure --scope project --content "T41: any Understand-Anything incremental update that touches a .sh file with function nodes blocks at merge-batch-graphs (symbol gate marks them unknown: no deterministic shell parser) until the plugin gains a shell parser or .sh symbols are excluded; the fallback is a full /understand rebuild."
16001714-ab6e-4386-ab29-1915fe73fdf7
```

## Effects

None outside the repository working tree.

cost: 50 LLM dispatches, 0 retries. Incremental: 15 file-analyzers, 1,040,482 tokens. Full: 1 scan + 31 file-analyzers + assemble + architecture + tour = 35 dispatches, 2,686,230 tokens (analyzers 2,394,557; scan 56,936; assemble 58,803; architecture 81,090; tour 94,844). Total 3,726,712 subagent tokens as reported by the harness. Orchestrating session n/a.

## Revision 2 (orchestrator status=revise, 11:36:29Z: symbol-coverage regression)

- **Finding reproduced independently.** The per-file function/class/method comparison of the old graph (committed at 72b8901, meta 7b69b1e) against c3afc7a shows exactly 8 files with 35 lost symbols. Their source definitions are unchanged: def-like line counts are identical at 7b69b1e and 72b8901.
  - storage.py 19→1
  - attach_comment_files.py 24→14
  - executable_agent-fanout 2→1
  - history.sh 1→0
  - docker.sh 3→2
  - tailscale.sh 2→1
  - zed.sh 3→2
  - run_bashcov_unit_test.rb 3→1
- **Cause.** The full-rebuild analyzers applied the significance filter. For example, batch 1 skipped `ContextStore` methods because the extractor gave no line ranges, and batch 13 skipped the 9-line `share_history`. Nothing forced them to keep symbols the published graph already had. `validateGraph` checks schema and references, not completeness.
- **Fix.**
  - Restored the full-run intermediates from the scratchpad.
  - Re-ran the file-analyzer for exactly the 8 files as targeted batch 32 (storage.py, attach_comment_files.py, run_bashcov_unit_test.rb) and batch 33 (the 5 shell files), with `previousSymbols` from the old graph and a mandatory coverage assertion. Batch 32 re-emitted 46/46 previous symbols plus 6 qualifying `ContextStore` methods. Batch 33 re-emitted 11/11.
  - Carried the first assemble review's fixes forward as batch 34 (the 3 recovered `apparmor_userns.sh` functions, their 3 edges, and the 4 prose-`lineRange` removals), so a re-merge from batch files cannot undo them.
  - Re-merged, which gave 885/1325 (34 duplicate IDs kept-last, 44 `tested_by` dropped, 0 unfixable).
  - Re-ran the assemble review. It restored `languageNotes` on 2 file nodes and made no other change.
  - Reused rev1's 9 layers and 15-step tour. The file-level node set is identical (366).
- **Gates.**
  - Inline validator: 0 issues.
  - Core `validateGraph`: 885/885 nodes, 1325/1325 edges, 0 issues. Non-tuple `lineRange`: 0.
  - The per-file table for all 360 shared files (validation file) shows **0 files with rev2 < old**, and no file whose source lost definitions.
  - Symbol totals: old 492, rev1 468, rev2 509.
  - `meta.gitCommitHash` stays 72b8901; `meta.json` is unchanged. In `fingerprints.json` only the 3 self-referential `.ua/` entries changed.
- **Commit** 7ee3658 `fix(ua): restore symbol coverage for 8 under-extracted files (T41 rev2)` on the same branch and PR #212.
- **Counts:** before (72b8901) 853 / 1219; rev1 844 / 1198; **rev2 885 / 1325**.
- **Secret scan at rev2:** 0 token/key patterns. The same single non-secret `--profile audit` hit.

[memory:failure] T41 rev2: a full `/understand` rebuild can silently drop previously-published function/class nodes (significance filter, extractor gaps); `validateGraph` does not detect it. Gate every graph commit with a per-file symbol-count comparison against the previous graph (new >= old unless the source lost definitions), and repair with a targeted batch carrying `previousSymbols`.

cost (revision 2): 3 more dispatches (targeted batches 32 and 33, assemble review), 232,722 subagent tokens (102,919 + 74,271 + 55,532). Run total: 53 dispatches, 3,959,434 subagent tokens; orchestrating session n/a.

CompactionDB (revision 2):

```
$ cd ~/Workspace/dotfiles && python3 .claude/hooks/contextdb_cli.py memory add --kind failure --scope project --content "T41 rev2: a full /understand rebuild can silently drop previously-published function/class nodes (significance filter, extractor gaps); validateGraph does not detect it. Gate every graph commit with a per-file symbol-count comparison against the previous graph (new >= old unless the source lost definitions) and repair with a targeted batch carrying previousSymbols."
69a96c4c-6b56-44c1-be92-4e99b6391c0b
```
