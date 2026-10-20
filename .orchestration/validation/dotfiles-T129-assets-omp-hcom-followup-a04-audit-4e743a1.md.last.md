[P2] high orchestration `.orchestration/acceptance/dotfiles-T129-assets-omp-hcom-followup-a04.md:4` — `dispatch` is empty despite TASK message 2509 and pending-integration ACCEPTANCE message 2529 having confirmed `read_at` timestamps. The required bus lines and delivery markers are missing, repeating the predecessor’s dispatch-record defect.

[P3] high evidence `.orchestration/dotfiles-T129-assets-omp-hcom-followup-a04/report.md:26` — The claimed GNU-shim red run has no command, shim source, or output in `validation.md`. The recorded red run demonstrates the macOS sandbox refusal only. Preserve the GNU-run evidence or describe that platform conclusion as an inference.

The task declares no explicit invariants mapping; applicable inherited controls are:

INV-2: holds `.orchestration/dotfiles-T129-assets-omp-hcom-followup-a04/validation.md:233` — Changes satisfy both caps: 0/120 and 25/400.
INV-3: holds `.orchestration/dotfiles-T129-assets-omp-hcom-followup-a04/revise.yaml:11` — The owned historical repair supplies the selector, revision record, and recorded red/green runs.
INV-6: holds `.orchestration/acceptance/dotfiles-T129-assets-omp-hcom-followup-a04.md:65` — Read-only bus inspection confirms one TASK, one RESULT, zero amendments, questions, or revisions.
INV-8: holds `.orchestration/dotfiles-T129-assets-omp-hcom-followup-a04/report.md:16` — Worker artifacts are committed at the audited head; the task copy matches its dispatched hash.

Orchestration findings: 1

No implementation or security regression found. After `gh` failed, the GitHub connector confirmed [PR #430](https://github.com/mryfmo/dotfiles/pull/430) and successful workflows; [final-head CI logs](https://github.com/mryfmo/dotfiles/actions/runs/39249929501/job/118050947696) explicitly show the new test passing. The macOS job skipped test execution.

📝 まとめ: Read-only audit completed; nothing modified. Tests and Bats were not rerun locally; the dispatch-record and validation-evidence gaps remain.
Verdict: incorrect