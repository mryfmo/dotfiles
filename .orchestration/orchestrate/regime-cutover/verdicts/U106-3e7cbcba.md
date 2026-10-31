- P3, high confidence — `scripts/orchestrator/pr-audit.sh:1146`: JSON Schema accepts integral numbers such as `1.0` as integers, but this validator rejects them, causing a schema-conforming verdict to fail.

Reproduced:

- 36 direct reader cases and three injected I/O failures passed.
- Separately confirmed rejection of `line: 1.0`.
- `AuditConfigSourceTest`, Bash syntax, ShellCheck, shfmt, byte comparison, and checksum verification passed.
- Tree remained clean.

Four focused integration tests stopped before reaching the changed code because the sandbox blocks `libperl.dylib`. CI and live Codex behavior were not verified.

Verdict: correct