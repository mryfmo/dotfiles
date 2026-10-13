# Learning triage: dotfiles-T128-orchestrator-tools-a01

These are candidates only; nothing is promoted.

1. [memory:decision] A tool that reproduces a gate's computation must use the gate's own match, not a stricter one. `three-repeat.sh` greps `^classes:.*<class>` (anchored, substring) because the gate rebuilds the `searches` set that way. An exact-element match would print a `search:` line the gate refuses.
2. [memory:failure] A task-state rule written from the message contract alone misses live statuses. The contract names accepted, revise and withdrawn, but the history also carries `reset`, `parked`, `superseded` and `under_review`; the first live `bus-read.sh` run showed three long-closed tasks as open. Count the statuses in the real history before fixing a closer list, and keep unknown statuses non-closing.
3. [memory:decision] `wc -l` counts newlines, so a two-line file without a final newline reads as one line, and `$(< file)` drops every trailing newline, so a message followed by a blank line reads as one line too (Bot thread 4254107304). To require exactly one physical line, read with a sentinel (`$(cat -- file && printf x)`), strip the `x` and one final newline, and refuse any newline left.
4. [memory:failure] CI formats shell with `shfmt -i 4 -sr -d`, pinned at v3.14.1 through mise, and runs the apt shellcheck. shfmt wants a continued pipe written with a trailing `|`, never a trailing backslash before a leading `|`, and the apt shellcheck flags SC2015 where 0.11.0 does not. Run the CI's exact commands before the push.
