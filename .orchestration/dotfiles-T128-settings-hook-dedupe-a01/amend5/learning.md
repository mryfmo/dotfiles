# T15 amendment5 learning

[memory:failure] Interpreter basename stripping can classify a compound command as an interpreter: ~/bin/audit-edit.sh;/usr/bin/python3 followed by a managed path loses the audit command. A peer found this in uncommitted amendment4; the actual helper reproduction and a red regression confirm it.

[memory:decision] The managed template emits a bare script path. Require exactly one shlex part equal to the tilde or current-home absolute managed path; every multi-token command remains unmanaged. The root cause is fixed by deleting interpreter stripping rather than adding a shell parser. All20 tests pass, including preservation of four interpreter variants and the compound-interpreter case. Current-home equality also closes arbitrary project-local suffix matching.

Scope limit: alternative path spellings, aliases and other-home paths remain unmanaged; no filesystem canonicalization is attempted. Installed apply/restart is operator-owned after integration.
