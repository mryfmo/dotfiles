#!/usr/bin/env bash
# @file masked-dirname-check.sh
# @brief Refuse a `$(dirname …)` or `$(basename …)` nested inside another command substitution.
# @description
#   ShellCheck's SC2312 (check-extra-masked-returns) exempts dirname and basename, so the U31 shape
#   `dir=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)` passes it although the inner status is
#   lost. This check reports every `$(dirname` or `$(basename` that opens while another `$(` is still
#   open, as `file:line: …`; capture the path first or split it in the shell (`${path%/*}`,
#   `${path##*/}`). The scan carries its quoting and nesting state across lines, so a substitution
#   split over several lines is seen: the command word of an inner `$(` is tested where it starts,
#   after blanks, line continuations or newlines. It reads a heredoc body the way the shell does: the
#   delimiter is one word after quote removal (unquoted text, `\x`, '…', "…", $'…' with its escapes
#   and $"…" concatenate); an unquoted delimiter's body expands `$(…)` (an apostrophe there is plain
#   text), a delimiter with any quoting (`<<'EOF'`, `<<$'EOF'`, `<<E"O"F`, `<<\EOF`) makes the body
#   literal and skipped. Single-quoted text and comments are skipped.
#   shortcut: a lexical scan, not a parse; a `case` pattern's unbalanced `)` inside a `$(…)` closes
#   the substitution early (a missed finding, never a false one); upgrade to an AST walk
#   (shfmt --to-json) if such a shape appears.
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
    # State per file: depth of open `$(`, per-depth double-quote and paren counts, an open
    # single-quoted string (sq), the heredocs queued on the current line (pending) and the one whose
    # body is being read (hd_word, hd_quoted, hd_strip, its base depth hd_base).
    awk '
        FNR == 1 {
            depth = 0; dq[0] = 0; paren[0] = 0; sq = 0
            hd_active = 0; npending = 0; first_pending = 1
        }
        hd_active {
            body = $0
            if (hd_strip) sub(/^\t+/, "", body)
            if (body == hd_word) {
                hd_active = 0
                start_heredoc()
                next
            }
            if (hd_quoted) next
        }
        {
            line = $0; n = length(line)
            for (i = 1; i <= n; i++) {
                c = substr(line, i, 1)
                if (sq) {
                    j = index(substr(line, i), "\047")
                    if (j == 0) break
                    i += j - 1; sq = 0
                    continue
                }
                # The first word of a substitution opened inside another one may start after blanks, a line
                # continuation or a newline; it is tested where it starts.
                if (await[depth]) {
                    if (c ~ /[ \t]/ || (c == "\\" && i == n)) continue
                    await[depth] = 0
                    if (substr(line, i) ~ /^(dirname|basename)([ \t)]|$)/) {
                        printf "%s:%d: a $(dirname) or $(basename) inside another command substitution loses its status; capture it first or split the path in the shell\n", FILENAME, FNR
                        found = 1
                    }
                }
                # The top level of an unquoted heredoc body reads like double-quoted text, except that a
                # double quote is plain text there too.
                body_text = hd_active && depth == hd_base
                if (c == "\\") { i++; continue }
                if (!body_text && !dq[depth] && c == "\047") {
                    j = index(substr(line, i + 1), "\047")
                    if (j == 0) { sq = 1; break }
                    i += j
                    continue
                }
                if (!body_text && !dq[depth] && c == "#" && (i == 1 || substr(line, i - 1, 1) ~ /[ \t;]/)) break
                if (!body_text && c == "\"") { dq[depth] = !dq[depth]; continue }
                if (c == "$" && substr(line, i + 1, 1) == "(") {
                    depth++; dq[depth] = 0; paren[depth] = 0; await[depth] = depth > 1; i++
                    continue
                }
                if (dq[depth] || body_text) continue
                if (c == "<" && substr(line, i, 3) == "<<<") { i += 2; continue }
                if (c == "<" && paren[depth] == 0 && substr(line, i, 2) == "<<") {
                    i = queue_heredoc(line, i + 2)
                    continue
                }
                if (c == "(") { paren[depth]++; continue }
                if (c == ")") {
                    if (paren[depth] > 0) paren[depth]--
                    else if (depth > 0) depth--
                }
            }
            if (!hd_active) start_heredoc()
        }
        # Reads the delimiter word after a `<<` at position p of s, queues the heredoc and returns the
        # position of the delimiter`s last character. The word is taken as the shell takes it, after quote
        # removal: unquoted text, \x, single, double, $"…" and ANSI-C $`…` quoting concatenate, and any
        # quoting at all makes the body literal.
        function queue_heredoc(s, p,    strip, quoted, word, c, e, k, n) {
            strip = 0; quoted = 0; word = ""; n = length(s)
            if (substr(s, p, 1) == "-") { strip = 1; p++ }
            while (substr(s, p, 1) ~ /[ \t]/) p++
            while (p <= n) {
                c = substr(s, p, 1)
                if (c ~ /[ \t;&|<>()]/) break
                if (c == "\\") { quoted = 1; word = word substr(s, p + 1, 1); p += 2; continue }
                if (c == "$" && substr(s, p + 1, 1) == "\047") {
                    quoted = 1; p += 2
                    while (p <= n && substr(s, p, 1) != "\047") {
                        c = substr(s, p, 1)
                        if (c == "\\") {
                            p++; e = substr(s, p, 1)
                            c = e == "n" ? "\n" : e == "t" ? "\t" : e
                        }
                        word = word c; p++
                    }
                    if (p > n) return n
                    p++
                    continue
                }
                if (c == "$" && substr(s, p + 1, 1) == "\"") { p++; c = "\"" }
                if (c == "\047") {
                    k = index(substr(s, p + 1), "\047")
                    if (k == 0) return n
                    quoted = 1; word = word substr(s, p + 1, k - 1); p += k + 1
                    continue
                }
                if (c == "\"") {
                    quoted = 1; p++
                    while (p <= n && substr(s, p, 1) != "\"") {
                        if (substr(s, p, 1) == "\\" && substr(s, p + 1, 1) ~ /[$`"\\]/) p++
                        word = word substr(s, p, 1); p++
                    }
                    if (p > n) return n
                    p++
                    continue
                }
                word = word c; p++
            }
            if (word == "" && !quoted) return p - 1
            npending++
            pend_word[npending] = word; pend_quoted[npending] = quoted; pend_strip[npending] = strip
            return p - 1
        }
        # Starts the body of the next queued heredoc, at the nesting depth where its operator stood.
        function start_heredoc() {
            if (first_pending > npending) return
            hd_word = pend_word[first_pending]; hd_quoted = pend_quoted[first_pending]
            hd_strip = pend_strip[first_pending]; hd_base = depth; hd_active = 1
            first_pending++
        }
        # A file that ends inside a substitution, a quoted string or a heredoc means the scan lost the
        # shell`s structure, so what it read after that point is not evidence of a clean file.
        END {
            if (depth > 0 || sq || hd_active || first_pending <= npending) exit 3
            exit found ? 1 : 0
        }
    ' "${file}" || {
        code=$?
        if ((code == 3)); then
            echo "masked-dirname-check: ${file} ends inside a substitution, a quoted string or a heredoc; the scan lost its place, the list is refused" >&2
            exit 2
        fi
        if ((code != 1)); then
            echo "masked-dirname-check: cannot read ${file} (awk exit ${code}); the list is refused" >&2
            exit 2
        fi
        status=1
    }
done
exit "${status}"
