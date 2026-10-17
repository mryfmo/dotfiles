# Learning triage: dotfiles-T129-integration-seat-result-gate-cap-a01

These are candidates only; nothing is promoted.

1. [memory:failure] Under `set -euo pipefail`, `x="$(sed … "${missing_file}" 2> /dev/null | head -n 1)"` exits the script: the failed `sed` fails the pipeline and the assignment. A read of an optional file needs `|| x=''`, and its test needs the absent-file case, which the existing add-worker tests supplied here.
2. [memory:failure] A loop that checks items with `cmd && [ ok ]` as its last command reports only the last item's status; an earlier failing item is hidden. Collect a failure flag (`|| bad=1`) and return it.
3. [memory:decision] `git rebase --no-gpg-sign` rebases on this host, where `-c commit.gpgsign=false rebase` still fails its commit step with `failed to write commit object`.
4. [memory:decision] macOS `/bin/bash` 3.2 has no `mapfile`, and test suites that put `/usr/bin:/bin` first run scripts with it; read lines into an array with a `while read` loop and expand it as `${a[@]+"${a[@]}"}`.
