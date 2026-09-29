# T41 learning triage

## Candidates

1. **Incremental updates block on shell files.** Understand-Anything 2.9.7's
   incremental symbol gate cannot publish any update that touches a `.sh`
   file with function nodes. The strict parser has no shell grammar, so
   unchanged symbols are `unknown` and block, even when the candidate
   contains every old ID. This repo is mostly shell, so the incremental
   path only works for changes that avoid shell scripts. Budget a full
   rebuild (about 35 dispatches, 2.7M tokens) whenever a shell script with
   functions changes.
2. **The tuple-only rule is not enough for `lineRange`.** The prose-in-
   `lineRange` defect recurred in 4 nodes even though every analyzer prompt
   required tuples. The assemble-reviewer caught it this time. Keep the core
   `validateGraph` plus the non-tuple jq scan as a hard pre-commit gate.
3. **Coincidental env-value matches.** A `model-profiles.env` value scan will
   match coincidental phrases such as `--profile audit`. Judge each hit by
   whether the value is sensitive, not by the match alone.

## Upstream-issue proposal (filing needs operator OK)

Repository: Egonex-AI/Understand-Anything (plugin 2.9.7, `skills/understand/validate-incremental-symbols.mjs`, `merge-batch-graphs.py`).

Title: "Incremental update always blocks for shell (.sh) files with function nodes: symbol gate marks unchanged symbols `unknown`"

Body:
- What happens: in an incremental update (PARTIAL/ARCHITECTURE_UPDATE), any modified `.sh` file with previously published function nodes fails the symbol-loss gate. Every old symbol is reported `status: unknown` ("Old symbol cannot be mapped uniquely, or source parsing is unavailable/failed"), even when the fresh analysis re-emits each one with its original ID. `merge-batch-graphs.py` exits 1 and the baseline is not advanced. `prepare-symbol-retry.mjs` cannot help, because the cause is the missing parser, not an omission.
- Reproduction: build a full graph for a repo with shell functions, edit one function body in a `.sh` file, and run the incremental update.
- Proposals (either would do):
  - (a) add a declaration-coverage adapter for bash (tree-sitter-bash already covers `function name` / `name()` and subshell bodies);
  - (b) allow a candidate symbol whose `(file, kind, name)` identity and ID are unchanged to count as `present`, without source parsing;
  - (c) let the plan choose FULL_UPDATE up front for unparsable languages with symbols, instead of spending the analysis and then blocking.
- Related gaps seen in the same runs:
  - the extractor misses shell functions with a subshell `( … )` body;
  - `.bats` files are not recognised as tests by the linker (44–53 `tested_by` edges dropped per run);
  - the full-path scanner includes `.ua/` data files while the incremental helper excludes them.

## Promotion

None. These are candidates only.

## Revision 2 addendum

5. **Completeness is not covered by `validateGraph`.** A full rebuild lost 35
   symbols in 8 files: the significance filter and extractor gaps dropped
   `ContextStore` methods and a 9-line shell function the old graph had.
   Candidate rule: before committing any `.ua` graph, compare per-file
   function/class counts with the previous graph and fail on any decrease
   the source does not explain. `.agents`/`.orchestration` tooling could run
   the comparison script this revision used.
6. **Carry reviewer fixes into a batch file.** Assemble-reviewer fixes live
   only in `assembled-graph.json`. Any later re-merge from batch files undoes
   them unless they are captured as a batch file first; batch 34 here
   captured them.
