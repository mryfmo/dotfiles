# T84c Learning

Chezmoi source-file renames must sweep every test surface, including CI-only Bats suites, because the repository's local unit gate intentionally does not execute Bats. Apply this to future rename plans and validation checklists by grepping both the complete `tests/` tree and active source/docs/scripts for old literal names.

Recorded as project decision memory `2a1b34d8-fd34-4c4c-afdf-bb5e50629dee`.
