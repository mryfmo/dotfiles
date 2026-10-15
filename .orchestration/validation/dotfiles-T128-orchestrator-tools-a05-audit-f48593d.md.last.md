📝 まとめ: Read-only audit of [PR #350](https://github.com/mryfmo/dotfiles/pull/350) at `f48593d6` completed. An exploitable P1 remains; nothing was modified.

- [P1] high implementation scripts/orchestrator/orch-gate.sh:67 **Residual (a) is exploitable from a PR.** A PR can supply `.python-version` pointing to a committed executable; `uv` discovers and executes it while probing the interpreter, with the orchestrator’s credentials, before the trusted gate runs. `--no-project` does not disable this discovery, and Python’s `-I` cannot protect against an attacker-selected executable. Resolve and pin a trusted interpreter before entering the PR checkout. The tests stub `uv`, so they miss this path. This conclusion follows from the invocation and [uv’s documented executable-path requests and discovery](https://docs.astral.sh/uv/concepts/python-versions/#python-version-files).

- [P1] high orchestration .orchestration/acceptance/dotfiles-T128-orchestrator-tools-a05.md:230 The record acknowledges three RESULTs and `revises=2`, but defers handling to future per-PR recalibration. INV-6 counts per **task**, with threshold two; an authorized split does not establish a threshold exception. No release covering PR-B is documented in the supplied inputs. Resolve that conflict before integration.

- [P2] high specification .orchestration/tasks/dotfiles-T128-orchestrator-tools-a05.md:38 **The invocation deviation strengthens source trust and preserves the gate’s checks.** The unchanged Makefile target delegates to the same Python gate; calling its verified trusted copy with equivalent inputs avoids PR-controlled Makefile execution. Amend this row and item 1, rather than reverting the code to `make` at the head. The separate interpreter defect above still requires a code fix; the invocation mismatch itself is not P1.

- [P2] high implementation scripts/orchestrator/orch-gate.sh:55 **Residual (b): restoration is not guaranteed.** A `mkdir`/`cp` failure or interruption after checkout exits before lines 69–70, leaving the review worktree at the PR head, potentially with partially copied evidence. After partial writes, the next invocation refuses the dirty tree. This is an availability/recovery defect, not a demonstrated successful-gate bypass. Install cleanup handling before checkout and test a setup failure.

- [P2] high orchestration .orchestration/acceptance/dotfiles-T128-orchestrator-tools-a05.md:5 The machine-readable acceptance block still binds PR **346**, head `046901bc`, and omits all three PR-350 thread IDs from its ledger. Running the trusted field validator against the supplied inputs confirms both identity errors; ledger comparison confirms the omissions. Refresh the block for PR 350 before treating it as current acceptance evidence.

- [P2] high orchestration .orchestration/acceptance/dotfiles-T128-orchestrator-tools-a05.md:241 The restoration defect is marked owned, but `local:f48593d:2` is absent from the a02 acceptance record’s owner section. Follow-up task item 1 explicitly reads that section and excludes findings outside it. The present disposition therefore does not actually assign the work; add the finding to the authoritative owner section.

The Bot fixes in `e30cbed0` assess as follows:

| Thread | Assessment |
|---|---|
| 4265190252 | Original Makefile/gate substitution path fixed; trusted-execution boundary remains open through residual (a). Not fully closed. |
| 4265190259 | Reported tracked-symlink path closed by the pre-checkout tree scan; the test checks that the external destination remains unchanged. |
| 4265190267 | Inherited override path closed: both `CRIT_REVIEW` and `CRIT_REVIEWED` are unset and asserted absent by the test. |

All three remain `resolved:false` in the supplied sweep. That sweep matches the final head/base and records 12 successful check runs plus a successful CodeRabbit status. Code and tests are unchanged from the worker’s `1f3abb55` head. The three task premises hold against the referenced records, current skill text, and attached input files.

The task has no explicit front-matter invariant map; these assessments cover its referenced invariants and premises:

INV-1: holds .orchestration/tasks/dotfiles-T128-orchestrator-tools-a05.md:10 — changes stay within allowed files; committed task copy matches the dispatched hash.
INV-2: holds .orchestration/tasks/dotfiles-T128-orchestrator-tools-a05.md:143 — 3 non-record files, 196 added non-test lines, 174 added test lines.
INV-4: holds .orchestration/tasks/dotfiles-T128-orchestrator-tools-a05.md:87 — all three premises checked.
INV-6: violated .orchestration/acceptance/dotfiles-T128-orchestrator-tools-a05.md:230 — threshold reached without a documented PR-B release.
INV-7: holds .orchestration/tasks/dotfiles-T128-orchestrator-tools-a05.md:126 — this slice changes neither reviewed design keys nor the fixed review profile.

Orchestration findings: 3

Not rerun: fixture-writing tests or an exploit PoC; syntax checks passed. Live CI verification was unavailable through both `gh` and the web fallback; PR-controlled interpreter execution remains the principal risk.
Verdict: incorrect