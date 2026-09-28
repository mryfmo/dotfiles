# T33d sandbox record

- No container or VM isolation was used. All git work happened in the
  dedicated worker worktree `.claude/worktrees/worker-c`, on branch
  `test/permgate-bench-flake` from `origin/main` (7d47e46). The worktree
  was clean before the switch.
- The reproduction drivers (`permgate_bench_repro.py`,
  `permgate_fake_timing.py`) live in this session's scratchpad. They reuse
  the test's own `setUp`/`tearDown`, so all fixtures sit in per-run temp
  directories. They only invoke the fake CLIs; no real claude or codex
  classifier was run.
- The CPU load was 20 background `yes > /dev/null` processes, bounded to
  each measurement and killed afterwards.
- Product code (`executable_permgate`, `permgate-policy.yaml`) was only
  read. There was no `make apply`/`chezmoi apply`, no local bats run, no
  force push and no merge.
