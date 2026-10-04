# Learning triage: dotfiles-T92-stop-gate-sandbox-placeholders-a01

Candidates only. Nothing has been promoted.

1. **The Claude Code sandbox leaks into Stop hooks.** Hooks run inside the bubblewrap mount namespace. Protected paths under the project root appear as `ro` self-bind mounts of 0-byte, mode 0444 files, which `git status` lists as untracked. Any hook that inspects the working tree has to discount them.
2. **mountinfo is the cheap, exact source.** One read of `/proc/self/mountinfo`, fields 5 and 6, in its octal escaping (`\134`, `\040`, `\011`, `\012`), answers "is this exact path a read-only mount point" without a process per path and without following symlinks. Pass values to awk through `ENVIRON`, not `-v`, which interprets escapes.
3. **Do not use `-w` for read-only:** root passes it for mode 0444. Use the mount options instead.
4. **A test override must not be an environment variable** in a security gate: inherited environments are untrusted. Hooks run with fixed argv, so a test-only argument is safe.
5. **Fixture paths on macOS:** `/var` → `/private/var`. Anything compared with `git rev-parse --show-toplevel` or kernel tables must be resolved.
