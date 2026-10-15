[P2] high implementation scripts/orchestrator/orch-gate.sh:63 — Shims refusal does not leave the review worktree untouched: the EXIT trap unconditionally runs `checkout -qf --detach origin/main`. A clean worktree initially on another commit or branch passes line 61 and is moved despite refusal. A read-only stub replay confirmed these commands execute before exit 2. The test at `tests/unit/test_orch_gate_path.py:101` misses this because its git stub never changes worktree state. Guard restoration on whether the head checkout was attempted, and test an initially different clean HEAD.

The remaining requested checks pass:

- Resolution occurs in the trusted root before checkout, using `env -i PATH HOME mise which`, then `command -v`. The gate receives exactly two symlinks as its entire PATH; a06’s remaining allowlist is unchanged.
- The trap precedes `mktemp`; cleanup covers success and refusal. The private-PATH and removal tests support their closed rows; the refusal test does not establish the untouched-worktree requirement.
- `test_orchestrator_tools.py` contains only item 3’s three edits.
- `a8a0ffed` fixes Bot finding `4267889542`; the regression test exports both named mise variables.
- Applying the trusted masker in memory produces the branch task copy byte-for-byte: `f88f60865dfe0c1a8e4abccea4ac2aced9df7283bad8e9a40c141f8879a2ac42`. Only lines 54–56 differ.
- Final-head CI succeeded; the [macOS job log](https://github.com/mryfmo/dotfiles/actions/runs/38532287610/job/115746740107) confirms the new tests ran successfully.

Inputs can still select executable code through retained trust anchors: inherited PATH chooses `mise` and fallback tools, while HOME and trusted-root mise configuration influence resolution. With those inputs trusted, the targeted PR-local mise configuration and inherited `MISE_*` override routes are closed.

INV-2: holds .orchestration/tasks/dotfiles-T128-gate-wrapper-path-a01.md:91 — Three non-record files, 27 changed non-test lines, and 129 added test lines satisfy the caps; this short task declares no front-matter invariant map.

Orchestration findings: 0

📝 まとめ: Completed the read-only audit of PR 355 at a235637; one P2 remains, and no files were modified.

Not rerun locally: filesystem-writing tests and credentialed host probes. Refusal can reset a clean review worktree.
Verdict: incorrect