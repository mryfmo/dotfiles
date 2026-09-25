# dot-mkt-owner-T1-a01 sandbox record

- OpenSandbox was not used; the task explicitly required the live `adh-test` Lima VM.
- VM access was limited to `limactl shell adh-test`.
- Credential-free scratch users `dotmktowner` and `dotmktgate` were used across investigation and acceptance attempts.
- Every attempt used an EXIT trap, and successful cleanup printed `scratch-user-removed=yes`.
- Tool installs, VM-local repository copies, stubbed unrelated installers, and temporary evidence stayed inside scratch-user homes and were removed with those users.
- No Codex or Claude login was performed and no host credentials were copied.
- Local uv validation required approved shared-cache access after sandbox cache initialization failed.
