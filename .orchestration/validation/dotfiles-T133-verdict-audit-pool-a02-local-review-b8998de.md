---
task: dotfiles-T133-verdict-audit-pool-a02
head: b8998de162afc72d53d07679b8f0a194fcc480ff
pr: 410
base: 3e41e36abc949acd7e6b4859c1a22df9e665c8d4
started: 2026-10-18T22:58:35Z
finished: 2026-10-18T23:06:22Z
findings: 5
engine: codex review --base main (profile review, read-only)
---

- [P1] Run the integration gate before dispatching or merging — scripts/orchestrator/verdict.sh:254-258
- [P1] Verify previous findings in differential audit results — scripts/orchestrator/orch-audit.sh:169-171
- [P2] Honor amended test caps instead of the first historical cap — scripts/orchestrator/verdict.sh:175-175
- [P2] Mask decoded values before printing schema errors — scripts/orchestrator/orch-audit.sh:56-57
- [P2] Prevent concurrent reservations of the same audit key — scripts/orchestrator/audit-pool.sh:52-55

```text
The apply path bypasses required integration checks, and differential audits can lose unresolved findings. Duplicate scheduling, diagnostic redaction, and amended-cap handling also contain reproducible defects. Full unit tests were not run in the read-only sandbox.

Full review comments:

- [P1] Run the integration gate before dispatching or merging — scripts/orchestrator/verdict.sh:254-258
  Once four shadow comparisons agree, `--apply` can dispatch acceptance and merge without running the required integration gate. All nine conditions can pass without a native-review receipt or dispositions for an incorrect audit's findings, which the existing gate would reject. Require the trusted gate to succeed for this head before either side effect, as required by [AGENTS.md:44](AGENTS.md#L44).

- [P1] Verify previous findings in differential audit results — scripts/orchestrator/orch-audit.sh:169-171
  When differential mode is enabled, an auditor response that omits an existing P1 and returns `findings: []` passes these checks: the extractor never receives or compares the previous findings. `verdict.sh` consequently counts zero open P0/P1 findings, even though the earlier defect may lie outside the newly audited hunks. Before retaining a differential result, require every previous finding to appear with an explicit `fixed` or `still-open` status.

- [P2] Mask decoded values before printing schema errors — scripts/orchestrator/orch-audit.sh:56-57
  If an invalid enum value contains a Unicode-escaped token, the initial Markdown masker leaves it encoded, but `json.loads` decodes it and this diagnostic prints the raw secret. The pool then persists that stderr in its `.log` and `.request.rejected` files; removing the invalid JSON does not remove the leak. This is reproducible with an escaped fake GitHub token in `class`. Mask decoded diagnostics before emitting them.

- [P2] Prevent concurrent reservations of the same audit key — scripts/orchestrator/audit-pool.sh:52-55
  If the same task/head is enqueued again while its original request is `.running-1`, this picker reserves slot 2 for the duplicate. Both audits then remove and write the same task/head Markdown and JSON outputs despite using separate worktrees; a failing duplicate can delete the successful audit's JSON. Exclude already-running task/head keys while holding the queue lock.

- [P2] Honor amended test caps instead of the first historical cap — scripts/orchestrator/verdict.sh:175-175
  For tasks containing a later cap amendment, `head -n 1` selects the obsolete limit. This PR's a02 task contains the original 500-line test cap followed by Amendment 1 raising it to 550; the parser returns 500, so the actual 531 changed test lines incorrectly fail condition 5. Resolve the effective amended limit rather than taking the first historical occurrence.
The apply path bypasses required integration checks, and differential audits can lose unresolved findings. Duplicate scheduling, diagnostic redaction, and amended-cap handling also contain reproducible defects. Full unit tests were not run in the read-only sandbox.

Full review comments:

- [P1] Run the integration gate before dispatching or merging — scripts/orchestrator/verdict.sh:254-258
  Once four shadow comparisons agree, `--apply` can dispatch acceptance and merge without running the required integration gate. All nine conditions can pass without a native-review receipt or dispositions for an incorrect audit's findings, which the existing gate would reject. Require the trusted gate to succeed for this head before either side effect, as required by [AGENTS.md:44](AGENTS.md#L44).

- [P1] Verify previous findings in differential audit results — scripts/orchestrator/orch-audit.sh:169-171
  When differential mode is enabled, an auditor response that omits an existing P1 and returns `findings: []` passes these checks: the extractor never receives or compares the previous findings. `verdict.sh` consequently counts zero open P0/P1 findings, even though the earlier defect may lie outside the newly audited hunks. Before retaining a differential result, require every previous finding to appear with an explicit `fixed` or `still-open` status.

- [P2] Mask decoded values before printing schema errors — scripts/orchestrator/orch-audit.sh:56-57
  If an invalid enum value contains a Unicode-escaped token, the initial Markdown masker leaves it encoded, but `json.loads` decodes it and this diagnostic prints the raw secret. The pool then persists that stderr in its `.log` and `.request.rejected` files; removing the invalid JSON does not remove the leak. This is reproducible with an escaped fake GitHub token in `class`. Mask decoded diagnostics before emitting them.

- [P2] Prevent concurrent reservations of the same audit key — scripts/orchestrator/audit-pool.sh:52-55
  If the same task/head is enqueued again while its original request is `.running-1`, this picker reserves slot 2 for the duplicate. Both audits then remove and write the same task/head Markdown and JSON outputs despite using separate worktrees; a failing duplicate can delete the successful audit's JSON. Exclude already-running task/head keys while holding the queue lock.

- [P2] Honor amended test caps instead of the first historical cap — scripts/orchestrator/verdict.sh:175-175
  For tasks containing a later cap amendment, `head -n 1` selects the obsolete limit. This PR's a02 task contains the original 500-line test cap followed by Amendment 1 raising it to 550; the parser returns 500, so the actual 531 changed test lines incorrectly fail condition 5. Resolve the effective amended limit rather than taking the first historical occurrence.
```
