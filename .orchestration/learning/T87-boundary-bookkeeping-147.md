# T87 Learning

- Incremental UA must explicitly include extensionless shell executables; the stock extension filter skips them. Keep their fingerprint content-hash-only when no parser claims the path.
- Patch the nested `FingerprintStore.files` map and preserve unchanged entries; never treat the envelope as a flat file map.
- When fresh node IDs are unchanged, replacing nodes in place preserves incoming relationships and produces a smaller, auditable graph diff than remove-and-append ordering.
- A generated upgrade batch can cross repository-owned pins. Keep config and lock paired, but retain versions that tests and CI intentionally pin until a separate class updates those contracts.
