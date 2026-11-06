# Needs validation: dotfiles at 2256b56c83975cef17d8058ede5660c25f6cf35f

No unresolved record exists in this run, and run-4 carried none.

The brief's questions were each settled from source. These are the child's command and environment rows, the JSON-line parser, the abort and exit paths including round 3's forget-before-kill, what the proof runner writes and where, and whether user content can forge or escape the `<dsh-system>` block. The two new round-3 notes are same-process diagnostics and lifecycle hardening in `REPORT.md` section 6, not leads: the old child's stderr reaching the new child's tail, and `close()` not waiting for a killed child.

The error-text note becomes a lead once a profile that uploads session logs loads the plugin. Its checks are unchanged:
- **Owner-observed:** whether `omp auth-gateway stdio` writes credential text to stderr on its failure paths.
- **Local, bounded:** a stub fixture that writes a dummy marker to stderr before exiting, to confirm the marker appears in the `LlmError` message.
