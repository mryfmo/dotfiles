# dot-ubuntu-fix-T1-a01 learning triage

## Candidate

[memory:failure] Under `sudo -i`, overriding `HOME` is insufficient isolation for mise backend testing because mise may still discover the login user's global config. Use a credential-free scratch user with a minimal config, then delete the user.

[memory:decision] mise v2026.9.12 fixes fresh Linux arm64 aqua bin discovery for the repository's locked uv/yazi GNU artifacts by creating resolvable `.mise-bins` entries; no lock edit is required.

## Disposition

- Recorded as a validated Codex learn entry and queued for CompactionDB project memory.
- No skill promotion was performed by the worker.
