# Needs validation: dotfiles at 6531a212d627314f8aa843e4d9f18cf63c76da35

No unresolved record exists in this run, and run-2 carried none.

The `<dsh-system>` question was settled from source and needs no outside fact:
- the block is built only from system sources, as a separate text block;
- no code reads the tag;
- with no `system` field sent, a forged block carries the same user-turn provenance as the real one.

So it is recorded as a covered unit and hardening note 1 in `REPORT.md`, not as a lead.

The error-text note (hardening note 2) stays a note while no profile loads the plugin. It becomes a lead once a profile that uploads session logs loads the plugin. Its checks are unchanged from run-2:
- **Owner-observed:** whether `omp auth-gateway stdio` writes any token or credential text to stderr on its failure paths.
- **Local, bounded:** a stub fixture that writes a dummy marker to stderr before exiting, to confirm the marker appears in the `LlmError` message.
