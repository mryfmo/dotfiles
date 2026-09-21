# dot-update-conv-T1-a01 sandbox record

- OpenSandbox was not used because the task explicitly required the existing adh-test Lima VM.
- VM task work used only limactl shell adh-test and credential-free scratch user dotconvcheck.
- The VM downloaded chezmoi 2.70.4 and verified it against the upstream checksum manifest.
- Old-main source and current source were copied into the VM-local scratch home. No host credentials or Codex login state entered the VM.
- Unrelated pre-bootstrapped mise, agent-asset, Herdr, and agmsg steps were isolated with scratch-only no-op fixtures; actual chezmoi, Makefile update, run_once_51, and Superpowers function behavior were exercised.
- Every failed and successful attempt used cleanup traps. Final evidence verified scratch-user-removed=yes; no scratch user, home, or sudoers entry remains.
- One final rerun required sandbox escalation scoped to limactl shell adh-test after the Lima socket was denied.
- Repository writes stayed within allowed_files. The required CompactionDB decision is the only persistent non-repository effect.

