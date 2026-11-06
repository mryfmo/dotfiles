# DeepSeek harness (dsh) under srt

`dsh-srt` (`scripts/orchestrator/dsh-srt`, installed as
`~/.local/bin/common/dsh-srt`) is the one way this kit starts the DeepSeek
harness: it renders `<DSH_HOME>/.sandbox/srt-settings.json` from the worker
seat's lists in `scripts/orchestrator/hcom-seat` (the read denies of
credentials, the operator's Claude Code state, the chezmoi sources,
`~/Workspace`, the omp and hcom state; the domain list; no unix socket and no
local binding), with `DSH_HOME`, a scratch working directory
`$TMPDIR/dsh-srt-<uid>` and the bridge child's Claude state
`<DSH_HOME>/.state/claude` as the only write roots and the settings directory
itself read- and write-denied; runs the seat shim's canary under those settings
(a write into the sandbox directory, a read of the settings and a listing of
`~/.ssh` must all fail inside); and only then execs `srt --settings <file> --
<DSH_HOME>/bin/dsh --profile <name> <args>` from the scratch directory with the
environment reduced to the names the launcher lists (`HOME`, `PATH`, `USER`,
`DSH_HOME`, `TMPDIR`, `LANG`, `TERM`, `CLAUDE_CONFIG_DIR` and the two AWS file
names set to `/dev/null`). srt not on PATH or of another line, no executable
`<DSH_HOME>/bin/dsh`, a `DSH_HOME` or `TMPDIR` inside a read-denied path, a
settings file that does not parse, or a canary that answers anything but
`write-denied read-denied ssh-denied` is a refusal (exit 2) before anything
starts; there is no uncontained fallback (regime-cutover U251, after the M-21
measurement of 2026-11-06). Every list is one table at the top of the script,
each row naming the hcom-seat line it copies, and
`tests/unit/test_dsh_srt.py` reads those lines from hcom-seat's source so a
drift between the two fails the test.
