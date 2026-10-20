---
task: dotfiles-T129-integration-seat-result-gate-cap-a01
head: 9c07098147d3b16d68a9be2772fbcba2460b8851
pr: 393
base: 99a4a80f5a5b32a70cf7eb4f4d0db5a02d113841
started: 2026-10-17T23:19:44Z
finished: 2026-10-17T23:25:44Z
findings: 10
engine: codex review --base main (profile review, read-only)
---

- [P1] Accept finding-free RESULTs as an empty thread list — scripts/orchestrator/integrate-seat.sh:94-95
- [P1] Anchor the artifact exemption to the repository root — scripts/orchestrator/result-precheck.sh:33-33
- [P1] Check the task copy stored in the reviewed commit — scripts/orchestrator/result-precheck.sh:50-51
- [P1] Invoke receipt verification before consuming a RESULT — scripts/orchestrator/integrate-seat.sh:33-34
- [P1] Validate the receipt head before comparing commits — scripts/orchestrator/result-precheck.sh:29-33
- [P1] Verify integration scripts match the trusted commit — scripts/orchestrator/integrate-seat.sh:23-24
- [P2] Include findings received during the integration wait — scripts/orchestrator/integrate-seat.sh:92-94
- [P2] Record Bot dispositions in the acceptance ledger — scripts/orchestrator/integrate-seat.sh:98-102
- [P2] Require the two-round exception for open high-priority findings — scripts/orchestrator/result-precheck.sh:90-92
- [P2] Validate execution evidence rather than command-name presence — scripts/orchestrator/result-precheck.sh:75-76

```text
The receipt verifier has reproducible fail-open paths, its workflow enforcement is missing, and ordinary integration scenarios fail. Syntax checks and read-only reproductions were performed; full test suites were not run.

Full review comments:

- [P1] Validate the receipt head before comparing commits — scripts/orchestrator/result-precheck.sh:29-33
  A receipt containing all nine status lines but no valid `head:` passes verification. The resulting `git diff` fails, but `|| true` converts that failure into an empty change list. I reproduced exit 0 with both a missing head and an unknown commit. Require exactly one resolvable receipt head and reject any failed comparison.

- [P1] Anchor the artifact exemption to the repository root — scripts/orchestrator/result-precheck.sh:33-33
  `grep -v -F "${d}/"` removes any changed path containing that substring, not just files inside the task's artifact directory. Consequently, later executable changes such as `scripts/.orchestration/<task>/unsafe.sh` escape `code-after-receipt` detection. Match the allowed directory as a repository-rooted prefix instead.

- [P1] Check the task copy stored in the reviewed commit — scripts/orchestrator/result-precheck.sh:50-51
  Check (a) hashes the working-tree task file rather than the copy committed at `${head}`. A worker can therefore have a matching dispatched copy locally while the reviewed commit contains different task metadata; checks (b)–(d) also use that local copy. Read and verify the task from the supplied commit so the receipt actually covers the submitted branch.

- [P1] Verify integration scripts match the trusted commit — scripts/orchestrator/integrate-seat.sh:23-24
  A worktree with uncommitted changes to `scripts/pr-feedback.py` or another invoked helper still satisfies this HEAD comparison. The chain subsequently executes those modified files with the integration seat's credentials, despite claiming to run trusted `origin/main` scripts. Check the executable inputs against HEAD before running them, as the existing `chain-integrate.sh` does.

- [P1] Invoke receipt verification before consuming a RESULT — scripts/orchestrator/integrate-seat.sh:33-34
  This is the new worker-RESULT consumption path, but it never invokes `result-precheck.sh verify`. Neither the bus reader nor the updated playbook invokes it elsewhere. A RESULT with no receipt or a failing receipt therefore enters integration normally, leaving the advertised mechanical gate unused. Wire verification into the acceptance path before any integration actions.

- [P1] Accept finding-free RESULTs as an empty thread list — scripts/orchestrator/integrate-seat.sh:94-95
  A finding-free RESULT using the existing `threads=none` form reaches this loop and fails `thread-format`; omitting `threads=` instead fails the earlier history lookup. Thus ordinary PRs without findings cannot complete integration. Normalize absent or `none` thread lists to an empty collection before validating actual disposition tokens.

- [P2] Record Bot dispositions in the acceptance ledger — scripts/orchestrator/integrate-seat.sh:98-102
  For a Bot finding not already recorded in the main checkout's acceptance record, this loop writes only the disposition TSV. The later record step imports existing ledger rows, so integration reports readiness but the final gate rejects `S6: ledger lacks <id>`. Advisory findings also receive no required ownership row. Register these findings in the acceptance record before resolving them, following the [ownership procedure](home/dot_agents/skills/agmsg-orchestration/SKILL.md#L170).

- [P2] Include findings received during the integration wait — scripts/orchestrator/integrate-seat.sh:92-94
  If a later Bot review adds a P2 during the wait, the fresh sweep contains it but this loop still enumerates only the earlier worker RESULT's `threads` value. No disposition is generated for the new finding, so thread resolution blocks even when a valid `--owner` was supplied. Reconcile the final feedback with the RESULT instead of using the RESULT as the complete finding list; later-review P2 ownership is covered by the [integration procedure](home/dot_agents/skills/agmsg-orchestration/SKILL.md#L170).

- [P2] Validate execution evidence rather than command-name presence — scripts/orchestrator/result-precheck.sh:75-76
  Check (d) succeeds whenever the validation file mentions each command, even without its output or with an explicitly failed execution. I reproduced success with a transcript containing `make validate-agent-assets` followed by a failure. Validate the recorded execution result and output rather than a substring occurrence, as required by the [RESULT evidence contract](home/dot_agents/skills/agmsg-orchestration/SKILL.md#L123).

- [P2] Require the two-round exception for open high-priority findings — scripts/orchestrator/result-precheck.sh:90-92
  A report containing `<id>:P1:open:<id>` passes this expression even when `bot_rounds` is absent or equals 1. That accepts an unfixed high-priority finding before the permitted exception applies. Require `bot_rounds=2` whenever accepting an `open:` P0/P1 disposition, matching the [RESULT contract](home/dot_agents/skills/agmsg-orchestration/SKILL.md#L133).
The receipt verifier has reproducible fail-open paths, its workflow enforcement is missing, and ordinary integration scenarios fail. Syntax checks and read-only reproductions were performed; full test suites were not run.

Full review comments:

- [P1] Validate the receipt head before comparing commits — scripts/orchestrator/result-precheck.sh:29-33
  A receipt containing all nine status lines but no valid `head:` passes verification. The resulting `git diff` fails, but `|| true` converts that failure into an empty change list. I reproduced exit 0 with both a missing head and an unknown commit. Require exactly one resolvable receipt head and reject any failed comparison.

- [P1] Anchor the artifact exemption to the repository root — scripts/orchestrator/result-precheck.sh:33-33
  `grep -v -F "${d}/"` removes any changed path containing that substring, not just files inside the task's artifact directory. Consequently, later executable changes such as `scripts/.orchestration/<task>/unsafe.sh` escape `code-after-receipt` detection. Match the allowed directory as a repository-rooted prefix instead.

- [P1] Check the task copy stored in the reviewed commit — scripts/orchestrator/result-precheck.sh:50-51
  Check (a) hashes the working-tree task file rather than the copy committed at `${head}`. A worker can therefore have a matching dispatched copy locally while the reviewed commit contains different task metadata; checks (b)–(d) also use that local copy. Read and verify the task from the supplied commit so the receipt actually covers the submitted branch.

- [P1] Verify integration scripts match the trusted commit — scripts/orchestrator/integrate-seat.sh:23-24
  A worktree with uncommitted changes to `scripts/pr-feedback.py` or another invoked helper still satisfies this HEAD comparison. The chain subsequently executes those modified files with the integration seat's credentials, despite claiming to run trusted `origin/main` scripts. Check the executable inputs against HEAD before running them, as the existing `chain-integrate.sh` does.

- [P1] Invoke receipt verification before consuming a RESULT — scripts/orchestrator/integrate-seat.sh:33-34
  This is the new worker-RESULT consumption path, but it never invokes `result-precheck.sh verify`. Neither the bus reader nor the updated playbook invokes it elsewhere. A RESULT with no receipt or a failing receipt therefore enters integration normally, leaving the advertised mechanical gate unused. Wire verification into the acceptance path before any integration actions.

- [P1] Accept finding-free RESULTs as an empty thread list — scripts/orchestrator/integrate-seat.sh:94-95
  A finding-free RESULT using the existing `threads=none` form reaches this loop and fails `thread-format`; omitting `threads=` instead fails the earlier history lookup. Thus ordinary PRs without findings cannot complete integration. Normalize absent or `none` thread lists to an empty collection before validating actual disposition tokens.

- [P2] Record Bot dispositions in the acceptance ledger — scripts/orchestrator/integrate-seat.sh:98-102
  For a Bot finding not already recorded in the main checkout's acceptance record, this loop writes only the disposition TSV. The later record step imports existing ledger rows, so integration reports readiness but the final gate rejects `S6: ledger lacks <id>`. Advisory findings also receive no required ownership row. Register these findings in the acceptance record before resolving them, following the [ownership procedure](home/dot_agents/skills/agmsg-orchestration/SKILL.md#L170).

- [P2] Include findings received during the integration wait — scripts/orchestrator/integrate-seat.sh:92-94
  If a later Bot review adds a P2 during the wait, the fresh sweep contains it but this loop still enumerates only the earlier worker RESULT's `threads` value. No disposition is generated for the new finding, so thread resolution blocks even when a valid `--owner` was supplied. Reconcile the final feedback with the RESULT instead of using the RESULT as the complete finding list; later-review P2 ownership is covered by the [integration procedure](home/dot_agents/skills/agmsg-orchestration/SKILL.md#L170).

- [P2] Validate execution evidence rather than command-name presence — scripts/orchestrator/result-precheck.sh:75-76
  Check (d) succeeds whenever the validation file mentions each command, even without its output or with an explicitly failed execution. I reproduced success with a transcript containing `make validate-agent-assets` followed by a failure. Validate the recorded execution result and output rather than a substring occurrence, as required by the [RESULT evidence contract](home/dot_agents/skills/agmsg-orchestration/SKILL.md#L123).

- [P2] Require the two-round exception for open high-priority findings — scripts/orchestrator/result-precheck.sh:90-92
  A report containing `<id>:P1:open:<id>` passes this expression even when `bot_rounds` is absent or equals 1. That accepts an unfixed high-priority finding before the permitted exception applies. Require `bot_rounds=2` whenever accepting an `open:` P0/P1 disposition, matching the [RESULT contract](home/dot_agents/skills/agmsg-orchestration/SKILL.md#L133).
```
