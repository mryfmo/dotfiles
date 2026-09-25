# dot-builtin-git-auto-T1-a01 sandbox record

- OpenSandbox was not used because the task explicitly required `limactl shell adh-test`.
- The first full E2E call was blocked before VM access by the host filesystem sandbox; it was retried with approval scoped to `limactl shell adh-test`.
- Validation used only public GitHub artifacts and the public dotfiles repository. No credentials were copied into the VM.
- Two diagnostic retries failed after creating scratch users; their EXIT traps removed both users and task-specific temporary directories.
- The successful run used credential-free users `dotgita01` and `dotgitb01`; `userdel --remove` removed both homes, and a follow-up assertion confirmed no users or `/tmp/dot-builtin-git-auto.*` directories remained.
- Repository writes stayed within the task's `allowed_files`.
