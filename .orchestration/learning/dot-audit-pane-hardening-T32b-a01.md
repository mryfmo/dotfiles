# T32b learning triage

## Candidates

1. When a command string is sent to another shell, build the complete command
   first and quote it **once** with `printf %q`, as in
   `bash -c "$(printf %q "$inner")"`. `%q` output is valid only as a
   standalone shell word. Under `LC_ALL=C`, bash `%q` emits `$'\NNN'` for
   non-ASCII bytes, and `$'…'` placed inside an outer `'…'` breaks the outer
   quoting.
2. A test that decodes shell-quoted output with `eval "set -- …"` must run
   under an empty PATH. If the string under test is mis-quoted, as on a
   mutation baseline, eval would otherwise execute real binaries.
3. herdr `pane wait-output` / `pane read` take `--source recent-unwrapped`.
   Use it whenever a marker line may be longer than the pane width.

## Promotion

None. These are candidates only; the task does not allow promotion.
