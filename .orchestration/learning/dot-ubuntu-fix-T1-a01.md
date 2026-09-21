# dot-ubuntu-fix-T1-a01 learning triage

## Candidate

[memory:failure] Under `sudo -i`, overriding `HOME` is insufficient isolation for mise backend testing because mise may still discover the login user's global config. Use a credential-free scratch user with a minimal config, then delete the user.

[memory:decision] mise v2026.9.12 fixes fresh Linux arm64 aqua bin discovery for the repository's locked uv/yazi GNU artifacts by creating resolvable `.mise-bins` entries; no lock edit is required.

[memory:decision] A GPG dearmor pipeline targeting a persistent keyring must use `--batch --yes`; otherwise a rerun attempts `/dev/tty` overwrite confirmation and aborts non-interactive bootstrap.

[memory:failure] Do not use `bash -lc` in a cross-platform bats case that requires empty output; CI runner login profiles can emit unrelated text. Use `bash -c` unless the login shell is itself under test.

## Disposition

- Recorded as a validated Codex learn entry and queued for CompactionDB project memory.
- No skill promotion was performed by the worker.
