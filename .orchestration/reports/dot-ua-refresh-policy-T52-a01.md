# Report: dot-ua-refresh-policy-T52-a01

- worker: claude-standard-dot-a005 (claude-code, standard profile), worktree worker-c
- task_rev: 4ffe983717f2171fa760ed4e781da2363b884d343ea72a28442a7695af1233da (verified with sha256sum)
- branch: `chore/ua-refresh-policy` from origin/main 0790fb74; one commit, **f700b14**, pushed without `-u`
- PR: https://github.com/mryfmo/dotfiles/pull/223, head `f700b1461cdfda90e06db0634ecf83621c806a29`. CI results are in the validation file.
- cost: n/a. Docs and config only; no subagents and no graph analysis.

## Changes

1. **`.ua/config.json`:** `"autoUpdate": false`, previously `true`. I checked which flag the hooks read in the plugin 2.9.7 source; the output is pasted in the validation file.
   - **SessionStart** (`hooks/hooks.json`): `grep -q '"autoUpdate".*true' $UA_DIR/config.json` gates the staleness line. The origin/main config passes the gate (exit 0, prompt fires); this branch fails it (exit 1, prompt silenced). So `autoUpdate: false` **does** silence the SessionStart staleness line, too.
   - **PostToolUse** (`hooks/post-tool-use-auto-update.mjs`): `autoUpdateEnabled()` returns `config.autoUpdate === true`, which is `false` on this branch, and `main()` returns before printing.
2. **`home/dot_config/claude/rules/understand-anything.md`:**
   - "Re-runs are incremental and cheap" is removed.
   - A new bullet scoped to the dotfiles repository says:
     - refresh only with `/understand --full`, run by a worker task when the operator asks at a regime boundary;
     - incremental updates cannot publish, because the 2.9.7 `validate-incremental-symbols.mjs` marks unowned functions `unknown` in parser-less files. The bullet names `executable_herdr-agents`, `executable_agmsg-dispatch` and `modify_private_settings.json`, notes that there is no per-path language override and that `herdr-agents` changes in nearly every task, and cites T51;
     - `autoUpdate: false` silences both hook prompts;
     - between refreshes the graph is stale by design and the freshness check routes to grep.
   - The acceptance-gate bullet is kept, with one added clause: for a full rebuild, `--old-ref` is the previous `meta.gitCommitHash`.
3. **`home/dot_config/codex/AGENTS.md`** (Understand-Anything section, in Japanese): "増分解析(2 回目以降)は軽量です" is removed, and the same facts are added in Japanese, using `$understand --full` for Codex. The coverage-gate bullet gets the same `--old-ref` clause.
4. **`README.md`:**
   - The core-build sentence now ends "so the plugin's graph helpers run" instead of "so `.ua/` incremental updates work".
   - A new paragraph gives the full-rebuild-only policy, the parser-less-file block, `autoUpdate: false`, and stale-by-design with the grep fallback.
   - The `.ua/` commit and ignore guidance and the `ua-symbol-coverage` acceptance paragraph are unchanged.
5. **Left unchanged:**

   - `home/dot_agents/skills/agmsg-orchestration/SKILL.md`: item 13 already treats the hook instruction as out of scope, and nothing in it says re-runs are incremental.
   - `home/dot_agents/agent-config.yaml`: it has no UA, graph or incremental wording; its only `understand` mentions are the installer pin and the plugin pin.

   So the generator was not run, and none of its rendered files changed. `make render-check` passes.

## Tests and checks

- `make render-check`: exit 0.
- `make unit-test`: 705 tests OK, 1 skipped; exit 0.
- `make validate-agent-assets`: exit 0.
- `git diff --stat origin/main`: 4 files.

These are docs and config changes, so there is no new test. The hook check is the behavioural evidence.

## CompactionDB

`python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content 'T52: …'` was run in the main checkout. Memory id: **99f9a168-9014-4524-bc17-5fee9962d5ad**.

[memory:decision] T52: this repository refreshes `.ua/` only by operator-requested full rebuild at a regime boundary; incremental UA updates block on parser-less shell/chezmoi scripts; `autoUpdate` is off (operator 2026-10-02).

## Notes

- **T51 leftovers:** the gitignored candidates in worker-c's `.ua/intermediate/` and `.ua/tmp/` are still there, because the permission gate denied the optional delete. They are not tracked and not part of this branch. The T51 branch was not touched.
- **Understand-Anything hook:** it fired and was not acted on (`.ua/**` is in allowed_files only for `config.json`).
