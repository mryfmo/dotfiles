# dot-mkt-mode-T1-a01 sandbox record

- OpenSandbox was not used because the task explicitly required the existing `adh-test` Lima VM.
- VM access used only `limactl shell adh-test` and a credential-free scratch user named `dotmktcheck`.
- No host credentials or Codex login state entered the VM. `/bin/true` provided only the updater's Codex command-presence fixture; the Crit binary and Crit installer behavior were real.
- The Lima host mount reports group-write mode, so the 1.4 MiB chezmoi source was copied into the scratch user's VM-local filesystem and the managed source file was restored to 0644 before validation.
- Chezmoi ran with umask 022 and Crit ran with explicit umask 002, reproducing the operator's two-writer mode mismatch.
- The cleanup trap removed the scratch user and home after failed and successful runs; final output verified `scratch-user-removed=yes`.
- Repository writes stayed within `allowed_files`. No persistent external side effects remain.
