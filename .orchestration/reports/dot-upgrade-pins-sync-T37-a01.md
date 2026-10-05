# T37 report: make upgrade pins carry + ccusage sync (dot-upgrade-pins-sync-T37-a01)

- worker: claude-standard-dot-a005 (worktree `.claude/worktrees/worker-c`)
- task_rev: fdcc4596e2bc732c46db79b6c6e2b663105d2392a8df9f5107b4a413c4626ae6 (sha256 verified against both the main-checkout file and `33452dc:` blob)
- branch: `chore/upgrade-pins-20260929` from origin/main 33452dc; the merged local `chore/ua-graph-refresh-T36` branch was deleted first. The tree was clean.
- commit: 52d9f6b
- PR: https://github.com/mryfmo/dotfiles/pull/209 (head 52d9f6b, MERGEABLE; CI 14/14 pass, nix skipped; CodeRabbit skipped)

## What was done

1. **Checked the canonical base before applying.** For all five pin files,
   the canonical clone's `origin/main` blob (09a7777) is identical to the
   blob at 33452dc. So `git diff origin/main` from the canonical clone
   applies cleanly and cannot revert anything that landed since 09a7777.
2. **Carried the pins exactly:**
   `git -C ~/.local/share/chezmoi diff origin/main -- <5 files> | git apply --index`
   exited 0. Every file's `git hash-object` equals the canonical clone's.
   None of the five files was edited by hand. The applied diff changes
   exactly the listed versions:
   - node 26.9.0→26.10.0;
   - dotenvx 2.28.2→2.29.0;
   - claude-code 2.1.283→2.1.284;
   - codex 0.157.1→0.158.0;
   - ccusage 20.0.23→20.0.24;
   - pnpm 12.4.1→12.5.1;
   - aws-cli 2.36.49→2.36.50;
   - crit v0.20.3→v0.21.0, plus its four sha256.
3. **ccusage sync.** `grep -rn '20\.0\.23' scripts tests .github` found
   exactly the five expected lines: `check-statusline-tools.py:20`,
   `test_statusline_tools.py:24,104` and `test.yaml:204,215`. All five now
   read 20.0.24, and a re-grep finds none left. ccstatusline stayed at
   2.2.30, so it was left alone.
4. **Supply chain:**
   - `gh api repos/aws/aws-cli/git/refs/tags/2.36.50` exists (tag object 63d7343).
   - The four crit v0.21.0 sha256 values in the manifest match the release
     `checksums.txt`, the GitHub asset digests, and a local `sha256sum` of
     each downloaded binary. All three sources agree, so no PONG was needed.
5. **Tests:**
   - `make unit-test`: 577 tests OK (1 skipped).
   - `make validate-agent-assets`: ok.
   - `uv run --with pyyaml scripts/generate-agent-configs.py --check`:
     "generated agent configs are up to date". A bare `python3` run fails
     with "PyYAML is required", which is the script's documented `uv run`
     form.

## Notes

- **The understand-anything auto-update hook** fired after the commit. I did
  not act on it: `.ua/` is outside T37's allowed files, and under the T36
  decision graph refreshes run as their own worker task. The graph is now
  one code commit behind main.
- **I did not run `make require-crit-review`,** which is the orchestrator's
  final integration step.

[memory:decision] T37: the 2026-09-29 `make upgrade` pins (node 26.10.0,
dotenvx 2.29.0, claude-code 2.1.284, codex 0.158.0, ccusage 20.0.24, pnpm
12.5.1, aws-cli 2.36.50, crit v0.21.0) land together with the ccusage
expected-version sync in check-statusline-tools.py, its test, and test.yaml,
carried from the canonical clone with blob-identity proof (operator 2026-09-29).

## CompactionDB (main checkout)

```
$ cd ~/Workspace/dotfiles && python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content "T37: the 2026-09-29 make upgrade pins (node 26.10.0, dotenvx 2.29.0, claude-code 2.1.284, codex 0.158.0, ccusage 20.0.24, pnpm 12.5.1, aws-cli 2.36.50, crit v0.21.0) land together with the ccusage expected-version sync in check-statusline-tools.py, its test, and test.yaml, carried from the canonical clone with blob-identity proof (operator 2026-09-29)."
3d9f7288-ffae-4a4f-8bbf-9506b1c6f2a5
```

## Effects

None outside the repository working tree. The canonical clone was only read.
The crit binaries were streamed straight into `sha256sum` and never written
to disk.

cost: 0 subagent dispatches; orchestrating-session token/cost figures n/a.
