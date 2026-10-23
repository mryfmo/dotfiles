- [P2] High confidence .orchestration/tasks/dotfiles-T133-ci-efficiency-followup-a04.md:163 — The symlinked-installation and forbidden-interpreter tests cannot construct their candidates while confined to temporary roots and prohibited from modifying or redirecting the real passwd-home installation; earlier refusals can satisfy their assertions without exercising the named checks.
- [P2] High confidence .orchestration/tasks/dotfiles-T133-ci-efficiency-followup-a04.md:155 — Temporary-root destination fixtures already violate destination containment, so exit-2/no-effect assertions can pass without working symlink, case-alias or ledger/reservation validation; exercise each mutation against an otherwise accepted CI-provisioned baseline.

All allowed-file entries and required non-path controls have threat rows. The sandbox deployment prerequisite addresses the Linux `gh` exception conditionally; unrestricted same-UID replacement remains explicitly residual.

📝 まとめ: Completed the read-only design and cited-record review; two findings are submitted for orchestrator disposition.
Not checked: implementation, runtime tests, CI or deployed protection; the specified negative tests can provide misleading assurance.
Verdict: incorrect