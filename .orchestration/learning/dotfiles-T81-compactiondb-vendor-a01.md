# Learning: dotfiles-T81-compactiondb-vendor-a01

- **Run an installer, then diff everything it touched.** `install.py` reordered unrelated hooks in a forbidden settings file and wrote a backup beside it.
- **When a generator target does not exist, derive the rule from the artifact and prove it.** The manifest command was accepted only after it reproduced the existing manifest byte for byte.
- **A task's literal validation command can be broken before the change.** Run it on a clean export of the base to tell a pre-existing failure from a regression.
- **Measure a storage claim before acting on it.** After capping every event and running VACUUM, 2.9 MB of FTS5 segments remained against a 0.2 MB fresh database; an FTS `optimize` brought it back.
- **SQLite size accounting:** deleted rows free pages into the freelist, so `(page_count - freelist_count) * page_size` tracks the in-use size inside the transaction. The file shrinks only after `VACUUM`, which must run outside a transaction.

## Revise round 1

- **Measure after the step that changes the measure.** Merging the FTS index changes the in-use page count, so the merge belongs before every size check, not once at the end.
- **Base the VACUUM decision on the file, not on which path deleted rows.** Retention can shrink the data while the cap deletes nothing.
- **When an auditor's reproduction does not reproduce locally, say so with the attempts pasted.** Do not claim a test proves a regression it does not show.
