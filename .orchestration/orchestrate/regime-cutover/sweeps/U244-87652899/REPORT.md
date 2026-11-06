# Security audit report: dotfiles at 87652899ec44388fae2c59b7c368e51c173cd7ee

## 1. Run, scope and limits

**This is a partial pass.** It is a scoped run, and it ran without independent agents.

**Profile and scope.** The profile is `standard`, scoped to the U244 change against the merged main, cf68daf67..87652899ec44388fae2c59b7c368e51c173cd7ee (branch `feat/pr-merge-sweep-every-unit`), eleven files:
- the merge lever `scripts/orchestrator/pr-merge.sh` and its deployed copy;
- the manifest pin and the generated-outputs record;
- the README;
- the AGENTS.md sweep sentence and its regime template;
- the hcom-orchestration skill sentence;
- three test modules.

The brief names `d1ecd495` as the base and `c4195463..HEAD` (29 paths) as the change, and calls run-9 the U244 head; run-9 swept U227e, and no earlier run of this seat swept U244. Every other top-level directory and the root files are carried as `out_of_scope` units, and no coverage claim is made for them.

**Source ref.** The checkout was clean at the head both before and after the run.

**Budget.** None was set. Planned: four reconnaissance agents, one hunter wave, two critics, and one verifier per candidate. Spent: zero delegated agents.

**Execution.** Sandboxed source-and-local-only policy, and in practice source only. No target code ran. The lever's blob was hashed by its object ID.

**Independence gap.** The platform's delegation tool and eval kernel are denied by policy on this seat. Reconnaissance, the hunter wave and both critics ran in the parent, and no fresh independent agent reviewed this coverage. `run-metadata.json` therefore records `run_status: "incomplete"` with reason `independent_agents_unavailable`. No candidate survived the hunt, so there was nothing for a Phase 3 or Phase 5 verifier to verify.

**Prior runs.** I carried run-9 (`~/.local/state/omp-seats/dotfiles/.state/sweep-2/security-audit/run-9`, source 88d53ce1), the newest ledger. Its seven U227b units are absent at this head and carry as changed-source, out-of-scope units, and its 37 other units carry. No prior run holds a finding.

**Deferred.** Nothing.

## 2. Security posture

No candidate survives. The change narrows the gate:
- **Under U147,** the unit's brief could only exempt the unit from the sweep: a brief without `TRUST` merged with no sweep row.
- **U244 deletes that reading.** The trust probe, the brief path and the brief-checker dependency are gone.
- **The sweep gate now runs for every unit** (`pr-merge.sh:613-677`), after the verdict and disposition gates and before CI and the one write (`:752-782`).

No refusal path it removed could have stood between an attacker and a merge.

**The lever's remaining inputs:**
- **The body's `Program-Unit` line** (`:206`, `:689-718`). Exactly one line, a strict regex, and the store walked with ownership and no-symlink checks. `--records` (the coordinator's argument) must equal that store. The ledger row for this PR and head must carry the body's unit or a fix unit of it (`:354-367`), so a body the PR author edits cannot borrow another unit's verdict or sweep.
- **The ledger reader's sweep answer.** `ledger.py` is run with its status read: 2 is a refusal, anything but 0 or 2 a failure. The answer must be `none` (a refusal naming the rule) or one four-field row with a ts (`:615-631`).
- **The manifest pin probe.** The verifier must be `security-audit-skill <pin>`, with the pin word a prefix of the manifest's `assets.security-audit-skill.pin` as read by `sweep_pin_probe`, which exits 2 rather than pass on any doubt (`:243-290`, `:639-657`).
- **The findings-file checks.** The path is `sweeps/<path>.json` with no `..`, `.` or empty component, under a `sweeps/` directory, regular, this user's and no symlink (`:661-676`).

**Is any refusal path left open to a store or body under an attacker's control?**
- **The store is the coordinator's:** files of this user inside the main checkout, with symlinks refused. A principal that can write it already holds the coordinator's authority.
- **The body selects nothing on its own.** Its line must agree with a ledger row for this PR and head, and with the coordinator's `--records`.

**The deployed copy and pin.** Both paths are one blob, whose sha256 `5e235e90d6ee5b00a1014750744b07da48d7962e64abffc5b2f0a0fb56fd9772` is the pin (`agent-config.yaml:891`) and the generated-outputs record (`scripts/generated-agent-outputs.json:473`). The self-check refuses any other bytes (`:129-178`).

## 3. Confirmed findings

None.

| Severity | Title | Affected boundary | Observed result |
|---|---|---|---|
| — | none | — | — |

## 4. Confirmed finding details

None.

## 5. Needs validation

None.

## 6. Hardening notes and positive patterns

These are not findings.

### Hardening

1. **The gate does not read what a sweep found.** Since U244 every merge passes through the sweep row. But the gate checks only that the row exists, at the pinned skill, with a findings file present, and never what the sweep found (`pr-merge.sh:613-677`).

   So a sweep whose RESULT reports an open, unvalidated candidate still admits the merge. The other seat's U263, U265 and U267 sweeps are an example: they carry a `decisions.tsv:509` candidate about published account identifiers.

   That is the stated design (`AGENTS.md:71`: sweep rows are advisory, and the Codex verdict stays the one merge gate). The coordinator's reading of the sweep summary is therefore the only control there. A row field for open candidates, which the gate refuses, would make it machine-checked.

### Positive patterns

- A strictly narrower gate, with its dependency on the brief checker removed.
- Every reader's status is read, and every unreadable answer is a refusal or a failure.
- The body's unit is bound to the ledger row's unit.
- A byte-identical deployed copy under its sha256 self-check.
- Tests pin both sides: a plain-brief unit without a sweep row is refused, and one with a well-formed row merges with or without `briefs/` (`tests/unit/test_pr_merge.py:132-162`).

## 7. Coverage summary

From `coverage-ledger.json` (49 units):

| Status | Units |
|---|---|
| covered | 5 |
| candidate | 0 |
| blocked | 0 |
| deferred | 0 |
| out_of_scope | 44 |

The five covered units are all new, each owned by `parent-hunter` with source checks:
1. the every-unit sweep gate (business logic);
2. the `Program-Unit` body line (access control);
3. sweep-row acceptance (release authorization);
4. the deployed copy and pin (generated-source provenance);
5. the documentation and tests (obvious things).

The 44 out-of-scope units are carried from run-9.

**Critic results.** Neither the post-wave critic nor the final-clean critic found work. The sweep reader `scripts/orchestrator/ledger.py` is not in the diff and is read only as the producer the gate calls. Neither critic was an independent agent (see section 1), so this is a single-reviewer coverage statement, not a clean independent pass.
