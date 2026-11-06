# DeepSeek harness (dsh) under srt

`dsh-srt` (`scripts/orchestrator/dsh-srt`, installed as
`~/.local/bin/common/dsh-srt`) is the one way this kit starts the DeepSeek
harness: it renders `<DSH_HOME>/.sandbox/srt-settings.json` from the worker
seat's lists in `scripts/orchestrator/hcom-seat` (the read denies of
credentials, the operator's Claude Code state, the chezmoi sources,
`~/Workspace`, the omp and hcom state; the domain list; no unix socket and no
local binding), with `DSH_HOME`, a scratch working directory
`$TMPDIR/dsh-srt-<uid>` and the bridge child's Claude state
`<DSH_HOME>/.state/claude` as the only write roots, the settings directory
itself read- and write-denied, and the paths srt 0.0.81 would make writable
on its own (`/tmp/claude`, `/private/tmp/claude`, `~/.npm/_logs`) denied as
well, where `hcom-seat` accepts them as seat roots; the scratch directory is
dsh's `TMPDIR` inside too (srt reads it from the `CLAUDE_CODE_TMPDIR` the
launcher passes). It runs the seat shim's canary under those settings (a write
into the sandbox directory, a read of the settings and a listing of `~/.ssh`
must all fail inside); and only then execs `srt --settings <file> --
<DSH_HOME>/bin/dsh --profile <name> <args>` from the scratch directory with the
environment reduced to the names the launcher lists (`HOME`, `PATH`, `USER`,
`DSH_HOME`, `TMPDIR`, `CLAUDE_CODE_TMPDIR`, `LANG`, `TERM`, `CLAUDE_CONFIG_DIR`
and the two AWS file names set to `/dev/null`); srt adds its own runtime and
proxy variables inside (`SANDBOX_RUNTIME`, `HTTP_PROXY`, `HTTPS_PROXY`,
`NO_PROXY`, `GIT_SSH_COMMAND` and the rest its `generateProxyEnvVars` emits).
Nothing a contained dsh could have written runs outside srt: the dsh runtime is
only stat-checked by the launcher (a regular file of this user, not writable by
group or other) and runs under srt alone, and `srt`, `python3` and the Linux
tools are refused when PATH finds them under `DSH_HOME` or the scratch
directory. Every directory the launcher relies on is created 0700 and refused
when it exists with another owner or with group or other bits, and the settings
file is written through a `mktemp` name inside that directory and renamed onto
the final name, which is refused when it is a link or open to its group. srt
not on PATH or of another line, no executable `<DSH_HOME>/bin/dsh` or one that
is a link or group-writable, a `DSH_HOME` or `TMPDIR` inside a read-denied path
or inside a path srt would make writable, a settings file that does not parse,
or a canary that answers anything but `write-denied read-denied ssh-denied` is
a refusal (exit 2) before anything starts; there is no uncontained fallback
(regime-cutover U251 and its round 2 U251b, after the M-21 measurement of
2026-11-06). Every list is one table at the top of the script, each row naming
the hcom-seat line it copies or the srt source line it answers, and
`tests/unit/test_dsh_srt.py` reads the hcom-seat lines from its source so a
drift between the two fails the test.
