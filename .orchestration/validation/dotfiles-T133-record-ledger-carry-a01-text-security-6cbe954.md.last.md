- [P2] High confidence .orchestration/tasks/dotfiles-T133-record-ledger-carry-a01.md:212 — The five consumption tests omit retained `sandbox-scan.sh`, `local-review.sh` and `local-advisory.sh`, which also lack downstream threat rows; `local-review.sh` independently resolves executables and consumes shared Git objects, so passing these tests cannot establish the complete chain’s execution binding. Include these consumers in the prerequisite inventory and tests.
- [P2] High confidence .orchestration/tasks/dotfiles-T133-record-ledger-carry-a01.md:59 — The named owner, `dotfiles-T133-verdict-audit-pool-a04`, excludes `orch-audit.sh` and explicitly assigns it to the pool sibling at line 124; its merge cannot deliver this prerequisite. Assign an authorized task that actually owns the required hardening; otherwise dispatch must remain blocked.

The strengthened containment and audit-collision tests address the previous findings. Clean-parent execution and deployed sandbox prerequisites conditionally address PATH, inherited environment and Linux `gh`; acknowledged same-UID residuals were not re-reported.

📝 まとめ: Completed the read-only task, threat-table and cited-context review; two findings await orchestrator disposition.
Not checked: implementation, runtime tests, CI or deployed enforcement; no files changed, and complete execution binding remains unverified.
Verdict: incorrect