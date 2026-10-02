# Acceptance: dot-ua-graph-refresh-T51-a01

Dispatched 2026-10-01T22:53:13Z (msg 668) to `claude-standard-dot-a005`
(worker-c): incremental refresh of `.ua/` from `meta.gitCommitHash` 72b8901
to `origin/main` ef9e5be. PONG **blocked** 23:02:59Z (msg 669) with report
and validation synced to the main checkout.

## Findings (orchestrator review of the worker's evidence)

- The plugin procedure ran as specified: `prepare-incremental.mjs` →
  `ARCHITECTURE_UPDATE` (analyze 28, cosmetic 3, ignored 208, generated 3),
  12 batches analyzed with `previousSymbols`, `merge-batch-graphs.py` →
  **exit 1 "Symbol validation blocked publication; baseline not advanced"**.
  Candidate 909 nodes / 1333 edges; baseline untouched; nothing committed;
  no PR. Cost ≈ 956k subagent tokens.
- Cause (verified against the plugin source: `validate-incremental-symbols.mjs`
  `hasPreservedIdentity`, SKILL.md Phase 2 "Parser limitation", the
  auto-update prompt's "manual investigation or parser support"): three
  changed files scan as `language: unknown` — the extension-less shell
  scripts `executable_herdr-agents` (34 symbols) and `executable_agmsg-dispatch`
  (1) and the Python chezmoi `modify_private_settings.json` (7). All 42 old
  IDs are present in the candidate with the same id/name/type, yet each is
  `unknown` ("source parsing is unavailable") and blocks publication. No
  per-path language override exists (`config.json` holds only
  `outputLanguage`/`autoUpdate`; no shebang detection). The one symbol
  retry cannot change language detection, so the worker asked before
  spending it (no-improvisation rule) — correct.
- Structural consequence: under UA 2.9.7 any incremental update that
  touches those files blocks; `herdr-agents` changes in nearly every task.
  Every `.ua` commit since b277a51 was a full rebuild, consistent with this.
- Task-file correction accepted: `git show 72b8901:.ua/knowledge-graph.json`
  is the 7b69b1e graph (853 nodes); the real 72b8901 baseline is the graph
  committed in 8f1061f (#212, 885 nodes / 1325 edges).
- Side note recorded for a possible task: batch-8 analyzer flagged
  `merge_config` in `home/dot_codex/modify_private_{audit,security}.config.toml`
  calling `emitted_current.add(current_name)` on a set of chunk indexes
  (latent, harmless; out of scope here).

## Operator decision (AskUserQuestion, 2026-10-02)

**Defer and codify.** No full rebuild now (hundreds of thousands to millions
of tokens per refresh, repeated whenever `herdr-agents` changes); the graph
stays stale and the search-first rule already falls back to grep when the
diff since `meta.gitCommitHash` lists non-`.ua` paths. T52 codifies: this
repository's UA refresh is a **full rebuild only**, run on operator request
at a regime boundary; the per-commit auto-update hook prompting is turned
off (`.ua/config.json` `autoUpdate: false`, reversing the T40-UA setting);
the rule text "Re-runs are incremental and cheap" is corrected.

**Decision: ACCEPTED as a blocked investigation** — no graph change, no
merge, branch `chore/ua-graph-refresh` abandoned (no commits), the
gitignored `.ua/intermediate/` candidates may be deleted by the worker. The
worker's RESULT obligations are satisfied by the blocked report and
validation; T52 follows as a new AGMSG-TASK.

cost: ≈956k subagent tokens (worker-reported) + session tokens n/a
