# dot-ubuntu-parity-T9-a01 — sandbox / OpenSandbox status

Not used. Verification was: `chezmoi execute-template` rendering (against
this worktree's own source), `bash -n` on the rendered output, and
directly running that rendered script twice — once against the real
`$HOME` (read-only `systemctl --user is-enabled`/`enable` calls, both
idempotent no-ops since the timer was already enabled) and once against
an isolated `mktemp -d` standing in for `$HOME` (no real system state
touched). No sandboxing beyond that was needed.
