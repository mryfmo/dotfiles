# Report: dotfiles-T94-upgrade-pins-a01

- **Worker and branch:** `claude-standard-dot-a005` in worker-c, branch `chore/upgrade-pins-2026-10-04` from `origin/main` f32f33a0.
- **task_rev:** `bb76e641…`, matched.
- **PR:** #250, https://github.com/mryfmo/dotfiles/pull/250.
- **Commit:** `6f5c776c`.
- **Final head:** `6f5c776c`.
  - **CI:** green; 16 pass, including CodeRabbit and the `build` jobs.
  - **`mergeable_state`:** `clean`.
  - **Branch:** up to date with main f32f33a0.
  - **Codex:** 👍, with no threads.

## Change

- **Patch:** `git apply --3way .orchestration/tasks/dotfiles-T94-pending-pins.patch` applied cleanly to all six files, so no hunk was reproduced by hand.
- **The diff matches the stated value changes and nothing else:**
  - mise v2026.9.13 → v2026.9.14;
  - aws-cli 2.37.3 → 2.37.4;
  - crit v0.21.0 → v0.21.1, with its four platform sha256 values;
  - claude-code 2.1.287 → 2.1.288 and pnpm 12.6.0 → 12.7.0, in `config.toml` and `mise.lock`.
- **Rendered files:** `make render-check` exits 0. The rendered `mise.sh`, `aws_cli.sh` and `installer-pins.sh` equal the generator output from the manifest.
- **Test pins:** none needed syncing. The old values appear nowhere under `home`, `install`, `scripts`, `tests` or `.github` (grep rc=1); T73 moved the statusline/version assertions to read the config.
- **crit sha256:** the four new values were cross-checked against the upstream `checksums.txt` of the `v0.21.1` release; all match.
- **Totals:** 751 tests OK, and `make validate-agent-assets` exits 0.
- **Not run:** `make upgrade` and `make update`.

## CompactionDB

```
cd /home/moriya/Workspace/dotfiles && python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content 'dotfiles-T94 (operator 2026-10-04): pins advance to mise v2026.9.14, aws-cli 2.37.4, crit v0.21.1, claude-code 2.1.288 and pnpm 12.7.0 through one class-pure PR carrying the whole `make upgrade` diff; the canonical clone no longer holds an uncommitted pin diff.'
ae1d260b-0507-4e32-ab4a-260d5a92ded1
```

[memory:decision] dotfiles-T94 (operator 2026-10-04): pins advance to mise v2026.9.14, aws-cli 2.37.4, crit v0.21.1, claude-code 2.1.288 and pnpm 12.7.0 through one class-pure PR carrying the whole `make upgrade` diff; the canonical clone no longer holds an uncommitted pin diff.

## Artifacts

- validation: `.orchestration/validation/dotfiles-T94-upgrade-pins-a01.md`
- sandbox: `.orchestration/sandboxes/dotfiles-T94-upgrade-pins-a01.md`
- learning: `.orchestration/learning/dotfiles-T94-upgrade-pins-a01.md`
- autoskill: `.orchestration/autoskill/runs/dotfiles-T94-upgrade-pins-a01.md`

cost: n/a (no subagents, no model-driven runs; the runtime does not expose session totals).
