[P1] high implementation scripts/orchestrator/orch-gate.sh:69 — **Python isolation is lost in the feedback collector.** The wrapper preserves `PYTHONPATH`; its trusted gate subsequently launches `[sys.executable, collector, …]` without `-I`, with the PR checkout as cwd (`scripts/require-crit-review.py:610`). With an inherited `PYTHONPATH=.`, a PR-supplied `sitecustomize.py` executes with the orchestrator’s credentials before collection. A read-only probe confirmed that the isolated parent preserves the variable and the child restores cwd to its import path. Python documents this startup import behavior. The stubbed gate test misses this subprocess. [Python startup documentation](https://docs.python.org/3.15/library/site.html#sitecustomize)

[P2] high orchestration .orchestration/acceptance/dotfiles-T128-orchestrator-tools-a05.md:139 — The block now binds PR 350 and `a06c874e`, but its four `audit_findings` still disposition PR-A’s `046901b` audit. These head-independent finding numbers can misattribute old reasons to a subsequent audit. Clear them before this audit and populate dispositions from its actual findings afterward; preserve historical dispositions in the prose.

[P2] high orchestration .orchestration/acceptance/dotfiles-T128-orchestrator-tools-a05.md:301 — Current counter evidence is missing after amendment 1 and RESULT 993. The last complete paste concerns PR 346 with two RESULTs; the later excerpt predates this round. The operator’s release is documented, but the required current counts and explanations for `unknown` components remain unrecorded.

The requested delta over `f48593d6` otherwise checks out:

- Line 56 resolves Python after entering the trusted root; line 71 executes that resolved path directly. The original review-cwd `uv` discovery path is removed.
- Line 58 installs the EXIT trap before checkout. Ordinary `mkdir`, `cp`, and gate failures reach restoration; the named setup-failure test covers partial copying. Signals are explicitly excluded by the amendment.
- The committed task copy matches the supplied amendment exactly: `6b238e5a958ed5124d997e129391a4e10cc2b61b7b9f57052e8b463b4f549f23`.
- The sweep matches the head/base. GitHub independently confirms successful Actions workflows and all four test jobs on the final head. [PR 350](https://github.com/mryfmo/dotfiles/pull/350), [test run](https://github.com/mryfmo/dotfiles/actions/runs/38497634877)

The task has no explicit front-matter invariant map; its referenced invariants assess as follows:

INV-1: holds .orchestration/tasks/dotfiles-T128-orchestrator-tools-a05.md:10 — changed paths are allowed; amended task copy matches.
INV-2: holds .orchestration/tasks/dotfiles-T128-orchestrator-tools-a05.md:145 — 3 non-record files, 198 added non-test lines, 205 added test lines.
INV-4: holds .orchestration/tasks/dotfiles-T128-orchestrator-tools-a05.md:89 — all three premises verified; the documented skill line shift is accurate.
INV-6: violated .orchestration/acceptance/dotfiles-T128-orchestrator-tools-a05.md:301 — current counting evidence is incomplete; decision A’s release itself is documented.
INV-7: holds .orchestration/acceptance/dotfiles-T128-orchestrator-tools-a05.md:300 — amendment confirmation names the matching hash; this diff changes no design keys.

Orchestration findings: 2

📝 まとめ: Read-only audit completed; nothing was modified. The surviving P1 triggers decision A’s reset path.

Not rerun: fixture-writing tests or a full malicious-file exploit. The confirmed import-path exposure requires an inherited relative `PYTHONPATH`; none was present in this audit process.
Verdict: incorrect