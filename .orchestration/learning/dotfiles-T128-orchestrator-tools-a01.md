# Learning triage: dotfiles-T128-orchestrator-tools-a01

These are candidates only; nothing is promoted.

1. [memory:decision] A tool that reproduces a gate's computation must use the gate's own match, not a stricter one. `three-repeat.sh` greps `^classes:.*<class>` (anchored, substring) because the gate rebuilds the `searches` set that way. An exact-element match would print a `search:` line the gate refuses.
2. [memory:failure] A task-state rule written from the message contract alone misses live statuses. The contract names accepted, revise and withdrawn, but the history also carries `reset`, `parked`, `superseded` and `under_review`; the first live `bus-read.sh` run showed three long-closed tasks as open. Count the statuses in the real history before fixing a closer list, and keep unknown statuses non-closing.
3. [memory:decision] `wc -l` counts newlines, so a two-line file without a final newline reads as one line. To require a single line, read the content with `$(< file)` (which drops trailing newlines) and refuse any remaining newline.
4. [memory:failure] A command run outside the sandbox sees another `$TMPDIR`, so files a sandboxed step wrote there are missing. Evidence a mixed run assembles should live in the session scratchpad, whose path both sides share.
5. [memory:failure] Never run a script under test with the host's real side-effecting binaries on PATH, even for a quick check. Use the stubs, or a missing binary, instead.
6. [memory:decision] A script that runs code from a checkout (a CLI, a hook) takes that checkout from its own location (`git -C <script dir> rev-parse --show-toplevel`), never from the caller's directory, which can be a PR worktree.
