# Needs validation: dotfiles at dc336b67ebe6456c976716288b9587555d802922

No unresolved record exists in this run, and run-1 carried none.

The one hypothesis that depended on facts outside the source has no lower-trust reader at this head, so it is recorded as hardening note 1 in `REPORT.md`, not as a lead. The hypothesis: the gateway's stderr tail could reach an `LlmError` and from there an uploaded session log. It depends on two facts outside the source: whether omp ever prints secret material on stderr, and whether the loading profile uploads session logs. No profile loads the plugin, and the proof's scratch profile disables session-log upload (`home/dot_dsh/plugins/omp-gateway/proof/run-proof.mjs:43`).

That note becomes a needs-validation lead once a profile loads the plugin with session-log upload enabled. Two checks would then settle it:
- **Owner-observed:** whether `omp auth-gateway stdio` writes any token or credential text to stderr on its failure paths.
- **Local, bounded:** run the client against the stub with a fixture that writes a dummy marker to stderr before exiting, and confirm the marker appears in the `LlmError` message.
