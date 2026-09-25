# dot-update-conv-T1-a01 learning triage

- Candidate reusable learning: chezmoi 2.70.4 records run_once execution in scriptState keyed by the SHA-256 of the rendered script, so an existing-machine VM fixture can seed exact historical hashes without executing old installers.
- Applicability: lifecycle migration tests where old run_once installers would be destructive, slow, or credential-dependent.
- Validation: a 23-record old-main state skipped unchanged installers, ran the newly introduced 51 installer once, and remained clean on the second literal make update.
- Promotion: recorded in the Codex worklog learn index; no new skill is warranted for this single command pattern.

