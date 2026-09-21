# dot-ubuntu-fix-T1-a01 sandbox record

- OpenSandbox was not used; the task explicitly required the existing `adh-test` Lima VM.
- Initial VM access was blocked by the local filesystem sandbox, then approved for the scoped `limactl shell adh-test` prefix.
- F2 diagnostics and validation used only the VM and public release artifacts. No host credentials were copied.
- A `HOME`-override attempt still discovered the login user's global mise config and exhausted `/tmp`; all three task-created `/tmp/dot-ubuntu-fix-*` directories were removed.
- Final validation used credential-free scratch user `dotf2test`; `userdel --remove dotf2test` removed it and its home after success.
- Repository writes stayed within the task's allowed files.
- The Docker keyring revision needed no additional VM mutation; its rerun path was isolated with command mocks and left no external effects.
- The bats login-shell revision changed one test flag and used only local temporary directories, which were removed after validation.
