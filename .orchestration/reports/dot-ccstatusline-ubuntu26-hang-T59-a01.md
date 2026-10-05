# Report: dot-ccstatusline-ubuntu26-hang-T59-a01

- **Worker and branch:** `claude-standard-dot-a005` in worker-c. Branch `fix/ccstatusline-ubuntu26-hang` from `origin/main` 750cc4a9.
- **PR:** #230, https://github.com/mryfmo/dotfiles/pull/230, now marked ready.
- **Final head:** `cc19dd4c84e500ec617b95752032e3b3c86c424a`.
- **task_rev:** `7e090867…`, then `be02c71f…` after PONG decision 1. Both matched.
- **Status:** ready_for_review. All checks pass on the final head, including the canary `test (ubuntu-26.04, client)`, and the Unit test run concludes `success`. `make unit-test` passes (718 tests, 2 skipped).

## Root cause: what the cold start waits on

The cold start waits on **reading the image's system node binary from disk**. There is no network wait. The evidence comes from the canary cell; the verbatim job-log excerpts are in the validation file.

1. **The command resolves to the wrong node.** ccstatusline's `#!/usr/bin/env node` resolves through `~/.local/share/mise/shims/node`. The smoke runs outside the statusline-mise config and with an overridden `HOME`, so the shim falls back to the image's **system** node. mise trace shows `shim[node] SYSTEM /usr/local/bin/node`, and strace shows the `execve("/usr/local/bin/node", …)` chain. The pinned `mise.lock` node 26.10.0, which the install step had just placed, was not used.
2. **That binary is cold on the 26.04 runner.** `fincore` reported `0 / 126595440` bytes of `/usr/local/bin/node` resident before the first run. The first run then faulted in 54 MB of it. Measured cold durations were 0.62 s (diagnostics 3), 2.80 s under strace (diagnostics 2), and more than 5 s in the original failure (run 37064146970). Every later run took about 0.22 s.
3. **The network is not involved.** The cold strace has no `connect`/`sendto`/DNS syscall and no syscall gap over 0.3 s; the time is spent in page faults. Proxy variables, loopback up or down, a fresh `HOME`, `MISE_OFFLINE=1` and the mise shim itself (0.03 s) made no difference. Diagnostics 1 also showed that the real smoke step **passes** once any earlier call has warmed the binary.
4. **Control case.** With the pinned node first on `PATH`, the same cold, no-network `--version` took **0.22 s**. That node was fully resident after the install step.

ccstatusline itself is not at fault. In 2.2.30, `--version` prints `getPackageVersion()` and exits before any config or network code runs, so no upstream fix or pin bump is involved.

## Fix (final head, 2 files, +15/−3)

- **`.github/workflows/test.yaml`, statusline smoke step:**
  - `node_bin_dir="$(mise -C "${statusline_mise_dir}" where node)/bin"` is put first on the smoke's `PATH`.
  - A `case` check asserts that `node` resolves from mise's pinned install, in the same style as the existing ccstatusline and ccusage resolution checks.
  - The smoke now exercises the exact pinned toolchain. The 5-second budget, the no-network sandbox (`unshare --net` and the macOS `sandbox-exec`) and `check-statusline-tools.py` are unchanged.
- **`tests/unit/test_runtime_health.py`** (PONG decision 1, the second 26.04 failure): the no-tar `PATH` guard is now `not (link.exists() or link.is_symlink())`.
  - The 26.04 image has a dangling `/usr/bin/grub-ntldr-img`. `Path.exists()` follows symlinks, so the `/bin` pass re-linked that name and raised `FileExistsError`.
  - Nothing is caught, skipped or deduplicated, and the purpose of the test (a `PATH` without `tar`) is unchanged.
  - The first Edit-tool attempt was reformatted by the PostToolUse formatter hook. I restored the file from `origin/main` and applied the change with a script; the diff is +3/−2.

## Diagnostics commits

`6e0faeba`, `1e280118` and `50588cfc` are `ci(diag): TEMPORARY` commits on the canary cell only. `cc19dd4c` removes them, so `git grep "T59 diag\|TEMPORARY T59" -- .github` returns nothing on the final head. Squash-merging collapses all four commits.

## Sweep note for the orchestrator

The diagnostics runs left `failure` check runs on older heads only. On the final head every check passes, including the canary.

## CompactionDB

```
cd ~/Workspace/dotfiles && python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content 'T59 (operator 2026-10-03): the Ubuntu 26.04 canary stays non-required but must be green; a canary failure is fixed at its root (here `ccstatusline --version` hanging without network on the 26.04 image), never dispositioned repeatedly.'
e547c5a4-c593-47a6-bb13-3eff3f99ea7d
```

[memory:decision] T59 (operator 2026-10-03): the Ubuntu 26.04 canary stays non-required but must be green; a canary failure is fixed at its root (here `ccstatusline --version` hanging without network on the 26.04 image), never dispositioned repeatedly.

## Artifacts

- validation: `.orchestration/validation/dot-ccstatusline-ubuntu26-hang-T59-a01.md`
- sandbox: `.orchestration/sandboxes/dot-ccstatusline-ubuntu26-hang-T59-a01.md`
- learning: `.orchestration/learning/dot-ccstatusline-ubuntu26-hang-T59-a01.md`
- autoskill: `.orchestration/autoskill/runs/dot-ccstatusline-ubuntu26-hang-T59-a01.md`

cost: n/a (no subagents; the runtime does not expose session totals)
