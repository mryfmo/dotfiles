---
id: M-20261021-03
date: 2026-10-21
classes: [hand-typed-chain, parallel-overlap]
severity: P2
---

# pins-a01 was dispatched while open PR #448 changes one of its allowed files

**What happened.** At 11:04 JST the orchestrator dispatched `dotfiles-T133-trusted-entrypoint-pins-a01` (allowed_files: home/dot_mise/config.toml, tests/unit/test_generate_agent_configs.py, its evidence dir) to a012 through send-task.sh. PR #448 (worker-sandbox-exclusions-a02, a013, held for integration) already changes `tests/unit/test_generate_agent_configs.py`. The project-map agent found the overlap at 11:05; a hold PING went to a012 at 2026-10-21T02:09Z.

**What the rules say.** Parallel workers: concurrent tasks need pairwise-disjoint `allowed_files` for code files (agmsg-orchestration rule "Parallelism"; SKILL "Parallel workers"). The orchestrator verifies disjointness before dispatch.

**Why the rules did not fire.** send-task.sh checks the text and the line (C-118, C-119, C-121) but not the overlap of allowed_files with in-flight PRs or dispatched tasks; the orchestrator checked the WIP count and skipped the file check by hand.

**Mechanism.** C-124: send-task.sh refuses a dispatch whose allowed_files intersect the files of any open PR in the ledger's active set (`gh pr view --json files`) or the allowed_files of any dispatched, unmerged task text, unless the line carries `after=<that task>`; probed with #448's test file before first use. Until it lands in the repository (R1-9), the glue version runs on every send.
