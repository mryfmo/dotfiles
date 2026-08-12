# T43 CompactionDB integration

Completed the CompactionDB integration and revision on `feat/compactiondb-integration`:

- `b76522c chore(vendor): import CompactionDB 2.0.0 pristine`
- `53467d5 fix(vendor): harden compactiondb redaction, retention, marker parsing`
- `dea935d feat(agents): manage CompactionDB sync and per-project install`
- `cd64143 fix(vendor): support both memory marker forms and add regression tests`
- `f560c89 chore(validate): exempt compactiondb dummy secret fixtures`

The revision restores `[memory:kind] trailing content`, supports free-text bracket markers and leading known-kind prefixes, adds redaction and SessionEnd retention regression coverage, and regenerates the vendor manifest. All 43 vendor tests, all 10 `validate.py` checks, and the repository agent-asset validator pass. The secret scanner exemption is limited to four exact CompactionDB dummy-fixture paths.
