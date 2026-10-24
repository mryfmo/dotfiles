#!/usr/bin/env bash
# @file masked-dirname-check.sh
# @brief Refuse a `$(dirname …)` or `$(basename …)` nested inside another command substitution.
# @description
#   ShellCheck's SC2312 (check-extra-masked-returns) exempts dirname and basename, so the U31 shape
#   `dir=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)` passes it although the inner status is
#   lost. This check reports every `$(dirname` or `$(basename` that opens while another `$(` is still
#   open on the same line, as `file:line: …`; capture the path first or split it in the shell
#   (`${path%/*}`, `${path##*/}`). Single-quoted text and comments are skipped.
#   shortcut: a per-line scan, so a substitution split across lines or a heredoc body is read as
#   plain lines; upgrade to an AST walk (shfmt --to-json) if such a shape appears.
# @arg $@ path The files to check (the ShellCheck groups of `make shellcheck`).
# @exitcode 0 No nested dirname or basename substitution.
# @exitcode 1 At least one finding, each printed as `file:line: …`.
# @exitcode 2 No file given, or a listed file cannot be read: the list is refused, never read as clean.
# @example
#   scripts/ci/masked-dirname-check.sh scripts/orchestrator/hcom-seat
set -euo pipefail

if (($# == 0)); then
    echo "masked-dirname-check: no file to check; an empty list is refused" >&2
    exit 2
fi

for file in "$@"; do
    if [[ ! -f ${file} || ! -r ${file} ]]; then
        echo "masked-dirname-check: cannot read ${file}; the list is refused" >&2
        exit 2
    fi
done

status=0
for file in "$@"; do
    # awk exits 1 for a finding; any other failure (a read error) refuses the list.
    awk '
        /^[ \t]*#/ { next }
        {
            line = $0; n = length(line); depth = 0; dq[0] = 0; paren[0] = 0
            for (i = 1; i <= n; i++) {
                c = substr(line, i, 1)
                if (c == "\\") { i++; continue }
                if (!dq[depth] && c == "\047") {
                    j = index(substr(line, i + 1), "\047")
                    if (j == 0) break
                    i += j
                    continue
                }
                if (!dq[depth] && c == "#" && (i == 1 || substr(line, i - 1, 1) ~ /[ \t;]/)) break
                if (c == "\"") { dq[depth] = !dq[depth]; continue }
                if (c == "$" && substr(line, i + 1, 1) == "(") {
                    if (depth > 0 && substr(line, i + 2) ~ /^(dirname|basename)([ \t)]|$)/) {
                        printf "%s:%d: a $(dirname) or $(basename) inside another command substitution loses its status; capture it first or split the path in the shell\n", FILENAME, FNR
                        found = 1
                    }
                    depth++; dq[depth] = 0; paren[depth] = 0; i++
                    continue
                }
                if (dq[depth]) continue
                if (c == "(") { paren[depth]++; continue }
                if (c == ")") {
                    if (paren[depth] > 0) paren[depth]--
                    else if (depth > 0) depth--
                }
            }
        }
        END { exit found ? 1 : 0 }
    ' "${file}" || {
        code=$?
        if ((code != 1)); then
            echo "masked-dirname-check: cannot read ${file} (awk exit ${code}); the list is refused" >&2
            exit 2
        fi
        status=1
    }
done
exit "${status}"
