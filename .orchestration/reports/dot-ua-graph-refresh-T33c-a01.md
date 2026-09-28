# T33c report — dot-ua-graph-refresh-T33c-a01 (revision 2)

- worker: `claude-standard-dot-a005`; orchestrator: `claude-remediation-dot`
- worktree: `/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c` (clean before the switch)
- branch: `chore/ua-graph-refresh` from `origin/main` = `935e198`
- task_rev: sha256 `42d2f7e7083f9797b21d4e354250f72f52da30b37b83cea05000e2e75ecdb392`, checked
- PR: https://github.com/mryfmo/dotfiles/pull/198, head `6f46a1123fe3bcaba12e68277fbe07e34faed10e` (rev2; rev1 head `297f25f`)
- status: ready_for_review (revision 2). CI is green on head 6f46a11: all checks pass except nix, which was skipped. Verbatim `gh pr checks 198` output is in the validation file.

## Revision 2 (AGMSG-ACCEPTANCE status=revise, 2026-09-28T08:02:04Z)

The visible-lane audit of `297f25f` raised one P2, confirmed by the
orchestrator (`.orchestration/validation/dot-ua-graph-refresh-T33c-a01-audit.md`).

- **Cause.** The `file:Makefile` and `file:setup.sh` nodes, both from batch
  7, had their language-notes prose stored as a *string* in `lineRange`.
  The core schema requires `lineRange` to be a numeric `[start, end]`
  tuple, and their `languageNotes` field was empty.
- **Reproduced.** I ran the plugin core's own validator: `validateGraph`
  from `packages/core/dist/index.js`, which `persistence/loadGraph`
  (`dist/persistence/index.js:83`) and the dashboard use. The script is
  `.ua/tmp/ua-core-validate.mjs`. Against `297f25f` it reported 44
  `dropped` issues: 2 `invalid-node` ("expected tuple, received string")
  and 42 edges referencing those nodes. That leaves 870→**868** nodes and
  1333→**1291** edges. Verbatim output is in the validation file.
- **Fixed** in commit `6f46a11` on the same branch and PR #198. The prose
  moved into `languageNotes` (it was empty before) and `lineRange` was
  omitted. No other node had a non-tuple `lineRange`: a `jq` scan found
  exactly these two.
- **Re-validated.** The core validator now reports `success: true` with
  870/870 nodes, 1333/1333 edges and **0 issues** (exit 0). The inline
  Phase 6 validator still gives 0 issues and 24 orphan warnings.
- **Fingerprints and meta are unchanged.** No source file changed, and the
  procedure only regenerates fingerprints from source content.
  `meta.gitCommitHash` stays `935e198`, and
  `git diff --name-only 935e198..HEAD` still lists only `.ua/` paths.
- **Why the inline validator missed it.** The skill's Phase 6
  `ua-inline-validate.cjs` checks only presence (id/type/name/summary/tags),
  duplicate IDs, dangling edge endpoints, and layer/tour references. It
  never checks field *types* against the Zod schema. Neither
  `merge-batch-graphs.py` (which normalizes IDs and complexity only) nor
  the LLM assemble-reviewer schema-validates node fields. So a
  wrong-typed optional field passes every pipeline gate and is dropped only
  at load time. The lesson is recorded in the learning file.

## Timeline (revision 1)

1. **First PONG (07:01:55Z).** Blocked: the plugin core
   (`packages/core/dist`) was missing, and building it would write outside
   the worktree and install dependencies. The orchestrator ran option A: it
   built the core in `~/.understand-anything-plugin` under the machine-state
   hygiene exemption (PING, 07:03:09Z).
2. **Second PONG (07:03:48Z).** `prepare-incremental.mjs` exited 0 with
   **FULL_UPDATE**: "44 files have structural changes (>30 files) — full
   rebuild recommended" (analyze 43/44, delete 1, cosmetic 2, ignored 220,
   generated 4, rerunArchitecture/rerunTour true). The orchestrator approved
   option A, `/understand --full` in this session, with a cap of about 60
   dispatches and "commit only when meta.gitCommitHash == base" (PING,
   07:04:33Z).
3. **Full rebuild**, run by the `/understand` skill procedure:
   - Phase 1: project-scanner found 424 files (code 246, script 74, config 49,
     docs 46, infra 8, markup 1), filtered 1475, complexity large.
   - Phase 1.5: 35 batches.
   - Phase 2: 35 file-analyzers, all outputs present (3 of them written as 2
     parts). The merge gave 870 nodes and 1285 edges; it dropped 73
     `tested_by` edges and recovered 0 imports edges.
   - Phase 3: assemble-reviewer recovered 48 `tested_by` edges (13 flipped
     from test→production) and tagged 34 more nodes "tested", for 1333 edges
     and 0 dangling.
   - Phase 4: architecture kept the same 9 layer IDs and names; all 425
     file-level nodes are assigned exactly once.
   - Phase 5: a 15-step tour (Project Overview, then `setup.sh` in step 2).
   - Phase 6: the inline validator found **0 issues** and 24 orphan-node
     warnings.
   - Phase 7: saved `knowledge-graph.json`. `build-fingerprints.mjs` reported
     "Fingerprints baseline: 424 files"; only after that did I write
     `meta.json` (`gitCommitHash` = `935e198`, analyzedFiles 424).
4. Committed `297f25f`, whose parent is `935e198`, equal to
   `meta.gitCommitHash`. `git diff --name-only 935e198..HEAD` lists only the
   three `.ua/` files.

## Node/edge counts, before → after

| | before (d906b00) | after (935e198) |
|---|---|---|
| nodes | 1399 | 870 |
| edges | 2398 | 1333 |
| layers / tour | 9 / 12 | 9 / 15 |
| file-level nodes | ~450 (file 317, config 48, document 46, pipeline 37, service 2) | 425 (file 322, config 49, document 46, pipeline 6, service 2) |
| function / class | 916 / 33 | 413 / 32 |

Why the counts fell:
- **Functions.** This run's analyzers skipped functions under 10 lines.
- **Pipelines.** The old graph had 22 Makefile-target and 9 workflow-job
  pipeline nodes; the current extractor reserves "step" nodes, so they were
  not recreated.
- **Coverage.** Every one of the 424 scanned files has a node.
- **Edge types after the rebuild:** contains 446, calls 224, depends_on 218,
  related 109, documents 90, tested_by 87, exports 68, imports 43,
  configures 34, triggers 14.

## Deviations from the skill text (all to stay inside the task boundary)

- **Worktree redirect off.** I set `UNDERSTAND_NO_WORKTREE_REDIRECT=1`.
  Without it the skill writes to the main checkout, outside this worktree;
  the task wants the graph committed on this branch.
- **Plugin root.** I used `~/.understand-anything-plugin`, where the
  orchestrator built the core, instead of the skill's first candidate (the
  Claude plugin cache 2.9.7, whose core is not built). Both are version
  2.9.7.
- **Batch data by reference.** Each file-analyzer prompt passed its
  `batchIndex` and told the agent to read its own entry (`files`,
  `batchImportData`, `neighborMap`) from `batches.json`, instead of
  embedding the JSON inline. Architecture and tour inputs were likewise
  passed as `.ua/intermediate/*.json` file paths. This keeps the
  orchestrating context small; the content is the same.
- **Interactive confirmations** (`.understandignore` review; the ">100
  files" gate) were treated as satisfied by the orchestrator's explicit
  approval of the full run.
- **Phase 7 cleanup skipped.** The skill moves scratch directories into
  `.ua/.trash-<ts>/`, which is **not** gitignored and would leave an
  untracked tail. `.ua/intermediate/` and `.ua/tmp/` are gitignored, so I
  left them in place; that also keeps `scan-result.json`, as the skill
  intends. The dashboard auto-launch was also skipped (non-interactive
  worker run).
- **`.ua/` files as nodes.** The 4 `.ua/*.json` artifacts are part of the
  scanned inventory and became nodes (batch 6). The old graph also had 5
  `.ua/` nodes, so I kept this consistent rather than improvising an
  exclusion.

## Plugin-side findings (not fixed: plugin code is out of scope)

The assemble-reviewer found two gaps in `merge-batch-graphs.py` in plugin
2.9.7:
1. `is_test_path()` does not recognise `.bats`, so every bats `tested_by`
   edge is dropped as production↔production, and the path-convention linker
   produced 0 edges for this repo.
2. `link_tests()` indexes only `file:` production nodes, so `tested_by`
   edges from `config:`/`pipeline:` nodes to `tests/unit/test_*.py` are
   dropped.

The reviewer restored 48 of these edges in this graph only; a future full
merge would drop them again. Worth an upstream issue or a local
`.understandignore`/fixture note.

## Other notes

- Several analyzers found that `extract-structure.mjs` misses shell
  functions with a subshell body (`name() ( … )`). They added
  `_install_mise_binary`, `install_sheldon`, `install_pinned_zed`,
  `install_starship` and `install_aws_cli` by hand from source.
- No secrets entered the graph. Analyzers masked `model-profiles.env`
  values, read only the header of `home/.key.txt.age`, and named env vars
  such as `GITHUB_PERSONAL_ACCESS_TOKEN` without their values.
- The post-commit understand-anything auto-update prompt was a no-op:
  `meta.gitCommitHash..HEAD` touches only `.ua/`, so the graph counts as
  current.

## CompactionDB

[memory:decision] T33c: the `.ua/` knowledge graph is refreshed incrementally by a
worker task whenever the SessionStart hook reports it stale; the orchestrator never runs
the graph update in its own session (operator 2026-09-28).

Command run from the main checkout with the content passed through a shell
variable. Id `bac98060-1b1c-4da2-9752-2cfa0d533ad5`; the output is in the
validation file. This run was a full rebuild because the helper forced
FULL_UPDATE. The recorded decision still describes the default path, and a
correct fingerprint baseline now exists so that the next refreshes can be
incremental.

## Effects

- Repository: only `.ua/{knowledge-graph,fingerprints,meta}.json`.
- Outside the repository, done by me: none. The core build in
  `~/.understand-anything-plugin` was performed by the orchestrator (its
  exemption), not by me.
- Gitignored local scratch: `.ua/intermediate/` and `.ua/tmp/` in worker-c.

cost: 39 agent dispatches (1 project-scanner + 35 file-analyzer + assemble-reviewer + architecture-analyzer + tour-builder), within the ~60 cap. Subagent token usage, summed from the per-dispatch usage reports, is ≈2.8M, about 55k–100k per dispatch. The orchestrating session's own tokens are not exposed.
