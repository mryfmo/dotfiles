# T43 report: graph symbol-coverage gate, UA hook scope rule, make render-check (dot-orchestration-rules-T43-a01)

- worker: claude-standard-dot-a005 (worktree `.claude/worktrees/worker-c`)
- task_rev: 2cf825882d080212e2f6fb0b29164861074308864d162289cdbd84c77949fe89 (sha256 verified against the main-checkout file and the `origin/main:` blob at 258339f)
- branch: `feat/orchestration-rules-T43` from origin/main 258339f. worker-c was clean and detached before the switch.
- commit: 557502b
- PR: https://github.com/mryfmo/dotfiles/pull/214 (head 557502b; CI 12/12 pass incl. the CodeRabbit status check, nix skipped; MERGEABLE)

## Changes

1. **`scripts/ua-symbol-coverage.py`** (new, stdlib only, executable).
   - Usage: `<old-graph.json> <new-graph.json> [--repo-ref REF]` (argparse, hyphenated option).
   - Counts `function`+`class` nodes per `filePath` in each graph and prints a markdown table: file, old, new, def-like lines at REF, and a status of `ok`, `explained` or `REGRESSION`. It ends with `files: N, regressions: M`.
   - Exits 1 when any file has `new < old`, unless the source is gone at REF or its def-like line count is below `old`. Without `--repo-ref`, every decrease counts as a regression.
   - Def-like grammar:
     - Python: `def`, `async def`, `class`.
     - Ruby: `def`, `class`, `module`.
     - Shell: `function name` or `name()`, including subshell bodies.
     - Selected by file extension or shebang. `-` means the file type has no grammar.
   - Proof on real data: run against T41 revision 1 (c3afc7a, `--repo-ref 72b8901`), it reports exactly the 8 regressions the audit and orchestrator found, and exits 1. A self-compare of the current graph gives `regressions: 0`, exit 0.
2. **`tests/unit/test_ua_symbol_coverage.py`** (new): one test with two tiny synthetic graphs in a temporary git repo (a.py with 2 defs). Dropping a symbol gives exit 1 and a `REGRESSION` row. Keeping or adding symbols gives exit 0 and an `ok` row.
3. **Rules.**
   - `home/dot_config/claude/rules/understand-anything.md` gets two bullets: the coverage-table acceptance gate, and the rule that task workers treat the auto-update hook as out of scope unless `.ua/**` is in `allowed_files` and record "hook fired; not acted on" (the orchestrator never runs the graph update itself).
   - `home/dot_config/codex/AGENTS.md` `## Understand-Anything` mirrors both bullets in Japanese; that section already mirrors the UA rule.
   - The agmsg-orchestration SKILL gets the coverage sentence in "Review and integration invariants", the hook sentence as Worker Playbook step 13, and "Name the render check as `make render-check` …" in Orchestrator Playbook step 3, the task-file checklist.
4. **`make render-check`:** a new target running `uv run --with pyyaml scripts/generate-agent-configs.py --check`. The generator already prints `ERROR: PyYAML is required: uv run --with pyyaml scripts/generate-agent-configs.py`, and its behaviour is unchanged.
5. **README:** the model-selection/generator paragraph gains a sentence about `make render-check`, and the Understand-Anything paragraph gains one sentence for the coverage rule.

## Checks

- `make render-check`: up to date.
- `make unit-test`: 611 OK (1 skipped).
- `make validate-agent-assets`: ok.
- Self-compare: `regressions: 0`, exit 0.
- CI: see validation.

## Notes

- **Live finding from the T39 sandbox** (it became active in this worker session partway through T43, after the T39 settings were applied). Sandboxed Bash hit two failures:
  - Every `uv`-based make target (`make render-check`, `make unit-test`, `make validate-agent-assets`) fails with `Read-only file system (os error 30) at path "~/.cache/uv/.tmp…"`, because `~/.cache/uv` is not in `sandbox.filesystem.allowWrite`.
  - `gh` fails with `HTTP 401: Requires authentication`. Its token most likely comes from the keyring over a D-Bus Unix socket, and that socket is blocked on Linux, where `allowUnixSockets` is ignored. This is gap (a) from the T39 report.
  - Both commands succeed after the normal unsandboxed retry (`allowUnsandboxedCommands: true`). Section 1 of the validation file was run that way, and section 2 keeps the sandboxed failures verbatim.
  - Suggested follow-up (not done here, outside T43's scope): decide the `uv` cache path (add `~/.cache/uv` to allowWrite, or set `UV_CACHE_DIR`) and the `gh` or keyring socket access (`allowAllUnixSockets` or `excludedCommands: [gh]`) before flipping `failIfUnavailable`.
- The understand-anything auto-update hook fired after the commit. I did not act on it, per the task note and the new rule: hook fired; not acted on.
- No `.ua/**`, plugin, hook, or `generate-agent-configs.py` change.

[memory:decision] T43: `.ua/` graph acceptance requires
`scripts/ua-symbol-coverage.py` (per-file function+class node comparison
against the previous graph, zero unexplained regressions); the
Understand-Anything auto-update hook is out of scope for task workers unless
`.ua/**` is allowed; `make render-check` is the one render-check command
(operator 2026-09-29).

## CompactionDB (main checkout)

```
$ cd /home/moriya/Workspace/dotfiles && python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content "T43: .ua/ graph acceptance requires scripts/ua-symbol-coverage.py (per-file function+class node comparison against the previous graph, zero unexplained regressions); the Understand-Anything auto-update hook is out of scope for task workers unless .ua/** is allowed; make render-check is the one render-check command (operator 2026-09-29)."
992478eb-e330-408e-802c-d8506b7ec378
```

## Effects

None outside the repository working tree.

cost: 0 subagent dispatches; orchestrating-session token/cost figures n/a.
