[P2] 0.99 implementation scripts/orchestrator/bus-read.sh:56 Literal-space splitting rejects `AGMSG-RESULT  v1 task_id=T1` despite the stop gate accepting it. An in-memory reproduction leaves the completed task open with `skipped=1`; tokenize runs of whitespace.

[P2] 0.99 orchestration .orchestration/acceptance/dotfiles-T128-orchestrator-tools-a04.md:18 The recorded revise lacks the required pasted counter output and repeated-class searches. The handwritten `revises=1` does not establish the other reset counts, and plan 016 G′ does not waive these evidence requirements.

[P2] 0.99 orchestration .orchestration/acceptance/dotfiles-T128-orchestrator-tools-a04.md:20 The ledger contains all 30 Bot findings but only `local:5b99a74:1`; it omits the `0d199475` local dispatch finding fixed by `05e3292f`. This undercounts findings for S1, contrary to the requirement to ledger local findings like Bot findings.

The three premises hold against the local records. Task-copy hashes, fix-commit ancestry, and caps match the evidence. The seven deferred Bot findings have owners in a02 on the base commit.

Shell syntax checks passed. Full tests were not rerun in this read-only audit. GitHub CLI and web access failed; CI verification relies on the supplied head-bound sweep.

The task has no front-matter invariant map; its text explicitly invokes these two design invariants:

INV-2: holds .orchestration/validation/dotfiles-T128-orchestrator-tools-a04.md:327 — independently confirmed 6 files, 393 implementation additions, 485 test additions.
INV-6: violated .orchestration/acceptance/dotfiles-T128-orchestrator-tools-a04.md:18 — required counter/search evidence is absent.

Orchestration findings: 2

📝 まとめ: Audited PR #336 at `3e5cad37` without modifying files; found one implementation defect and two orchestration evidence gaps.

Verdict: incorrect