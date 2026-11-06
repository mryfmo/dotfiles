# Architecture: dotfiles at 87652899 (scoped to unit U244)

## Product, principals and resources

A personal dotfiles repository whose `scripts/orchestrator/` holds the regime-cutover program's levers.

`pr-merge.sh` is the orchestrator seat's only merge path; the policy allows the lever and denies `gh pr merge` text. It runs in the main checkout and reads only the program store there (`.orchestration/orchestrate/<program>/`). It squash-merges a pull request only when the conditions below hold; the one write is `gh pr merge --squash --match-head-commit <head>`.

1. The ledger holds a `correct` row, or a `carried` row from a `correct` head, for that PR at that head.
2. The verdict file's findings have their dispositions.
3. The unit's sweep row exists at the audited head.
4. CI is green.

The generator copies the lever byte for byte to `home/dot_local/bin/common/executable_pr-merge.sh`, which is pinned under `claude.levers.sha256`.

**Principals.** The coordinator, who writes the store and runs the lever; the pull-request author, who controls the PR body including its `Program-Unit` line; GitHub, through `gh`; and the sweep seats, which produce findings files that the coordinator copies into the store.

**Resource.** The integrity of the merge decision on `main`.

## The change under hunt (main cf68daf6..87652899)

U244 deletes the trust probe and the brief reading. Under U147, the unit's brief decided whether a sweep was required: a brief without `TRUST` merged with no sweep row. Now `require_sweep_row` (`pr-merge.sh:613-677`) runs for every unit (call order `:752-756`).

It also updates:
- the manifest pin (`agent-config.yaml:891`) and the generated-outputs record (`scripts/generated-agent-outputs.json:473`);
- the AGENTS.md sweep sentence (`AGENTS.md:71`) and its regime template (`home/dot_agents/regime/AGENTS-audit-section.md:27`);
- the hcom-orchestration skill's Verify step and its pinned test;
- the README, including a prettier reflow;
- `tests/unit/test_pr_merge.py` and `tests/unit/test_pr_levers.py`.

## The lever's remaining inputs

1. **The PR body's `Program-Unit` line.** `resolve_store` (`:689-718`; regex at `:206`) requires exactly one line. The store path is walked with ownership and no-symlink checks, and `--records` must equal it.
2. **The ledger reader's verdict and sweep answers.** The checkout's `ledger.py`, run as `python3 -I -S`, with status read. `require_verdict_row` (`:354-393`) binds the row's unit to the body's unit; `require_sweep_row` checks the answer's shape (`:615-631`).
3. **The manifest pin probe.** `sweep_pin_probe` (`:243-290`) runs over `LEVER_MANIFEST`. The sweep row's pin word must be a prefix (8 or more hex) of the manifest's pin (`:639-657`).
4. **The findings-file checks.** `sweeps/<path>.json` with no `..`, `.` or empty component, under a `sweeps/` directory, regular, this user's, no symlink, and never opened (`:661-676`).
5. **`gh` reads** of state, base, head, draft and checks, bounded per call (`:320-322`, `:745-779`).

## Comparable baseline

A branch-protection gate that requires a set of status artifacts before a merge. The artifact here is a store row whose content the gate does not judge, as with an advisory status check.

## Trust boundaries and strongest controls

- **PR body to store and unit selection.** A strict regex. The ledger row for this PR and head must carry the body's unit, and `--records` is the coordinator's argument.
- **Store to gate.** The coordinator's own files: this user's, no symlinks, inside the main checkout. All readers' statuses are checked, so any unreadable answer is a refusal or failure, never a pass.
- **Source to deployed copy.** A byte-identical generated copy, a sha256 pin, and the lever's self-check.

## Prior coverage

run-9 (`~/.local/state/omp-seats/dotfiles/.state/sweep-2/security-audit/run-9`, source 88d53ce1, U227e) is the newest ledger and is carried. U227b is absent at this head, so its seven covered units carry as changed-source, out-of-scope units. No earlier run of this seat swept U244. No prior run holds a finding.

## Companion selection

`SUPPLY-CHAIN-AND-RELEASE.md` is selected: release authorization (the sweep row as a merge artifact) and generated-source provenance (the copy and the pin). Every other companion is excluded with its reason in the ledger.

## Execution and independence limits of this run

No target code ran, by task rule. The delegation tool (Task) and eval kernel are denied by policy on this seat, so every phase ran in the parent. `run-metadata.json` records the run as incomplete for that reason.
