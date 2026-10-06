# T108 worker review receipt

review_surface: crit-data
reviewer: claude-code
review_source: .orchestration/validation/dotfiles-T108-one-login-per-machine-a01-worker-crit.json
review_outcome: addressed

- **Why subagent evidence:** `crit status --json` reported no review file for this branch. The independent agent review is saved in the same JSON shape, as AGENTS.md "Agent Review Evidence" allows.
- **Result:** a read-only subagent reviewed `a8ebd8de` against `origin/main` (`e0027811`). It found the code correct and in scope, plus 1 P2 and 7 P3.
  - **Fixed in `b66f4297`:**
    - the P2 docs overclaim: Claude worker seats have no merge denial yet;
    - the execpolicy coverage wording;
    - the gate-authority wording;
    - squash-only described as a ruleset rule;
    - the missing login-failure test.
  - **Not applicable,** with reasons in the records:
    - the design-report citation (it reaches `main` with the boundary commit);
    - Codex keyring access (default storage is the decision; worker_kind is claude);
    - the gate-test fixture (`guard_base` sets HOME to it).
- **No browser review was opened.**
