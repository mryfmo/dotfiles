# dot-herdr-sheldon-T1-a02
status: ready_for_review
cost: n/a

## Result
- Saved original eight-file binary diff in `/Users/mryfmo/Workspace/dotfiles/.claude/worktrees/herdr-sheldon/.agents/worklog/codex/herdr-sheldon-pre-rebase.patch`; reverse apply check succeeded before the explicitly requested resets. Branch remains fix/herdr-reload-and-sheldon-client, now based on origin/main d377ad09d87a7f2154ead48c77043d11850b2e48.
- Reapplied only six source files: Makefile, README.md, Dockerfile, scripts/update-agent-assets.sh (header only), home/dot_agents/README.md, tests/install/common/lifecycle.bats.
- Dropped superseded Sheldon ubuntu.toml and setup.bats changes; no mise changes.
- Preserved upstream unmerged-index-first check and manifest-driven worker_kind wording. Lifecycle fixture adds reload_output at argument 13, preserving upstream git_unmerged at 12.
- Moved both tasks' twelve a01 historical task/report/validation/sandbox/learning/autoskill files into canonical .orchestration unchanged; SHA256 before/after evidence included. Unrelated update-convergence/upgrade-pins histories remain untouched in the worktree.
- No commit, push, PR, VM/Docker, local Bats or operator-home apply.

## Validation
395 unit tests passed. Asset validator, direct reload fixture (protocol mismatch succeeds, ordinary failure fails), unmerged feature fixture, stale-text check (no matches), shfmt, shellcheck -x, diff check and Crit gate passed.
Initial bare shellcheck reported only SC1091 missing sourced inputs; -x passed without source edits.
No Docker rebuild: unchanged a01 Docker diff retains its historical VM proof, as task requires.
Crit evidence and receipt: `/Users/mryfmo/Workspace/dotfiles/.claude/worktrees/herdr-sheldon/.agents/worklog/codex/review/a02.json` and `a02-receipt.md`.
Saved patch recovers the removed old diffs. Temporary fixture directories were cleaned.

## Durable decision
[memory:decision] Retain main's deletion of the Ubuntu local plugin; protocol_mismatch-only reload tolerance and documentation changes must preserve newer worker_kind and unmerged-index handling.
Executed in canonical repository:
`python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content 'dot-herdr-sheldon-T1-a02 supersedes the a01 Sheldon decision: retain main deletion of the Ubuntu local plugin, keep protocol_mismatch-only reload tolerance, and preserve manifest-driven worker_kind plus unmerged-index-first update checks when reapplying the prior docs/Docker changes.'`
Decision ID: e6194b5f-d34d-407c-8d3e-bb801a8169ab.
Exact command outputs are in the matching validation artifact.
