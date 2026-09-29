# T36 learning triage

## Candidates

1. **Keep the graph fresh per batch.** T33c's candidate 1 recurred: after
   the T33a–T35 batch (including the 67-file vendored agmsg removal),
   `prepare-incremental.mjs` again chose FULL_UPDATE (96 structural files,
   threshold 30). Deletions count toward that threshold even though they
   cost no analysis. Refresh right after each accepted batch, or dispatch
   the refresh together with any task that deletes many files.
2. **Clear stale intermediates before a full run.** `merge-batch-graphs.py`
   reads `intermediate/incremental-plan.json` and switches to incremental
   mode, merging `batch-existing.json`. A full rebuild after a
   prepare-incremental probe must therefore clear `.ua/intermediate/` first,
   or the old graph leaks into the new one.
3. **Two scan paths disagree about `.ua/`.** The full-path project scanner
   includes `.ua/`'s own data files, while the incremental helper excludes
   them with `--exclude-analysis-data`. The graph therefore carries 4
   self-referential nodes, which is an upstream issue candidate.
4. **Pass dispatch prompts by file.** Generating the file-analyzer,
   architecture and tour prompts from the skill templates into files, and
   telling each agent to read its file, kept a 31-batch run's payloads out
   of the orchestrating context without changing prompt content.

## Promotion

None. These are candidates only.
