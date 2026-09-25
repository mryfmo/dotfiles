# dot-shell-sp-T1-a01 sandbox record

- OpenSandbox was not used because the task explicitly required the existing `adh-test` Lima VM.
- VM access used only the approved `limactl shell adh-test` prefix.
- The scratch user `dotspcheck` was credential-free; no host Codex authentication or other credential was copied.
- An initial mise install discovered the host-mounted working directory config. The user was recreated, `HOME` was explicitly isolated, and the process changed to `/home/dotspcheck` before the locked install.
- F1 live validation used a temporary `/etc/sudoers.d/dotspcheck` entry limited to `chsh` and `tee`. Both the entry and scratch user/home were removed, and absence was verified.
- Repository writes stayed within `allowed_files`.
- No persistent external side effects remain.
