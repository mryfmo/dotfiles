[P2] high .orchestration/tasks/dotfiles-T128-audit-s1-report-a01.md:65 The named fixture pins `### Orchestration records and trust-boundary code`, so replacing it with Audit content breaks the existing whole-section assertion; specify a separate Audit fixture and pin, including its allowed_files entry.

[P2] high .orchestration/tasks/dotfiles-T128-audit-s1-report-a01.md:66 The current wrapper delegates record checking to ledger-check.py’s TSV parser rather than extracting JSON, so explicitly specify the new extraction, validation and failure behavior instead of assuming it already exists.

Hash matched; checker OK; mask 0; premises replayed as 0/0. Implementation tests were not run; unresolved task contradictions remain.

Task-file verdict: dotfiles-T128-audit-s1-report-a01: revise