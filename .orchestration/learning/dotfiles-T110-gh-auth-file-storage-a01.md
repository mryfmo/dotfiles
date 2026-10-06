# Learning: dotfiles-T110-gh-auth-file-storage-a01

- **gh's `tokenSource` names the storage.** `gh auth status --json hosts` reports the absolute `hosts.yml` path for a file token, `keyring` for a keyring token, and `default` with `state: "error"` when no token is reachable, which is what a keyring login looks like inside the Claude Linux sandbox. The task text expected `(keyring)`; on this host inside the sandbox it is `(default)`. A storage check must therefore run before any "working" check, or the sandbox case is misreported. [memory:failure] A doctor that counts working gh logins before checking `tokenSource` misreports a sandboxed keyring login as a broken login.
- **`CLICOLOR_FORCE=1` colours gh's `--json` output even through a pipe,** so a parser of gh JSON must strip it from the environment. `--jq` raw string output stays plain.
- **`pkill -f <pattern>` matches the calling shell** when the pattern appears in the command line itself; it killed the command (exit 143). Use `pgrep -fl` first, or a TaskStop on the background task.
- **The built-in removal safety check flags any `bash -c "<script>"`** it cannot inspect; run validation commands directly in a `{ …; } > file` group instead.

## Revise round 1

- **Independent findings beat early returns in a doctor check.** Each early `return [warning]` hid the checks after it, so a second account or an auth error suppressed the keyring and 0600 warnings, which were exactly the states the task cared about. Collect one finding per problem and report `found:` only when none was collected.
- **Bot-wait evidence must show the loop itself:** each command as run, its rc and output, and the elapsed seconds. A label followed by empty results is not evidence of a 15-minute wait.

## Revise round 2

- **A file-permission check stats the file itself, not the file a tool reports reading.** gh's `tokenSource` names only the active account's source, so a token file behind a keyring-sourced active account was invisible. Check the configured path (`${GH_CONFIG_DIR:-${XDG_CONFIG_HOME:-$HOME/.config}/gh}/hosts.yml`) directly, and pass that directory into the function so tests never touch the host's real file.
- **Every claim in a report needs its pasted output.** A claim the report makes about a command run in an earlier round (task_rev, crit status) is pasted from the transcript when the input has since changed.

## Revise round 3

- **An early return on a tool failure skips every independent check after it.** Compute the tool-independent findings first (here the `hosts.yml` `lstat`) and append them to every return path, the failure path included.
