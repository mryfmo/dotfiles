#!/usr/bin/env bash
# @file masked-dirname-check.sh
# @brief Refuse a `$(dirname …)` or `$(basename …)` nested inside another command substitution.
# @description
#   ShellCheck's SC2312 (check-extra-masked-returns) exempts dirname and basename, so the U31 shape
#   `dir=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)` passes it although the inner status is
#   lost. This check parses each file with shfmt (`shfmt -ln bash --to-json`) and walks the syntax
#   tree: every simple command whose command word is literally `dirname` or `basename`, run inside a
#   command substitution that is itself inside another one, is reported as `file:line: …` at the line
#   where the command word starts; capture the path first or split it in the shell (`${path%/*}`,
#   `${path##*/}`). The parser resolves what a lexical scan got wrong: heredoc delimiters, comments
#   and line continuations inside a substitution, `case` patterns. The command word is read after
#   quote removal (`\dirname`, `"dirname"`, `'dirname'`, `$'dir\x6eame'`, `dir\`+newline+`name`); a word with any
#   expansion in it is not a literal name and is not reported. A heredoc body whose delimiter has
#   any quoted or escaped part is literal and skipped, as bash reads it (shfmt expands the body of
#   a partly quoted delimiter such as `<<'E'OF`).
#   The files are parsed as bash: `make shellcheck` passes only bash scripts, and bash also parses
#   the repository's POSIX scripts. A file shfmt cannot parse is refused, never read as clean; that
#   includes a heredoc delimiter with ANSI-C escapes (`<<$'\x45OF'`), which shfmt 3.14.1 and
#   ShellCheck 0.11.0 both fail to terminate.
# @arg $@ path The files to check (the ShellCheck groups of `make shellcheck`).
# @env SHFMT The shfmt to run (default `shfmt` on PATH; CI puts the mise-pinned 3.14.1 there).
# @exitcode 0 No nested dirname or basename substitution.
# @exitcode 1 At least one finding, each printed as `file:line: …`.
# @exitcode 2 No file given, a listed file cannot be read or parsed, or shfmt or python3 is missing:
#   the list is refused, never read as clean.
# @example
#   scripts/ci/masked-dirname-check.sh scripts/orchestrator/hcom-seat
set -euo pipefail

shfmt=${SHFMT:-shfmt}

if (($# == 0)); then
    echo "masked-dirname-check: no file to check; an empty list is refused" >&2
    exit 2
fi

for tool in "${shfmt}" python3; do
    if ! command -v "${tool}" > /dev/null; then
        echo "masked-dirname-check: ${tool} not found; the list is refused" >&2
        exit 2
    fi
done

for file in "$@"; do
    if [[ ! -f ${file} || ! -r ${file} ]]; then
        echo "masked-dirname-check: cannot read ${file}; the list is refused" >&2
        exit 2
    fi
done

# Reads shfmt's typed JSON on stdin; argv[1] names the file. Exits 1 when it prints a finding.
walk=$(
    cat << 'PY'
import json
import re
import sys

MESSAGE = (
    "a $(dirname) or $(basename) inside another command substitution loses its status;"
    " capture it first or split the path in the shell"
)


# bash's $'…' escapes (bash(1) QUOTING); shfmt keeps the raw text in SglQuoted.Value.
ANSI_C = re.compile(r"\\(?:([abeEfnrtv\\'\"?])|([0-7]{1,3})|x([0-9A-Fa-f]{1,2})|u([0-9A-Fa-f]{1,4})|U([0-9A-Fa-f]{1,8})|c(.))", re.DOTALL)
ANSI_C_SIMPLE = {"a": "\a", "b": "\b", "e": "\x1b", "E": "\x1b", "f": "\f", "n": "\n", "r": "\r", "t": "\t", "v": "\v"}


def ansi_c(value):
    def decode(match):
        simple, octal, hex2, hex4, hex8, control = match.groups()
        if simple:
            return ANSI_C_SIMPLE.get(simple, simple)
        if control:
            return chr(ord(control) & 0x1F)
        if octal or hex2:
            # bash stores one byte, so `\544` wraps to `\144` (d); bash 3.2 and 5.2 both print dirname for $'\544irname'.
            return chr(int(octal or hex2, 8 if octal else 16) & 0xFF)
        return chr(int(hex4 or hex8, 16))

    return ANSI_C.sub(decode, value)


def literal(word):
    """The word after quote removal, or None when any part of it expands."""
    text = []
    for part in word.get("Parts") or []:
        kind = part.get("Type")
        if kind == "Lit":
            text.append(re.sub(r"\\(.)", r"\1", part["Value"], flags=re.DOTALL))
        elif kind == "SglQuoted":
            text.append(ansi_c(part["Value"]) if part.get("Dollar") else part["Value"])
        elif kind == "DblQuoted":
            # $"…" is "…" unless a message catalog translates it, which no lint run has.
            for inner in part.get("Parts") or []:
                if inner.get("Type") != "Lit":
                    return None
                text.append(re.sub(r'\\([$`"\\])', r"\1", inner["Value"]))
        else:
            return None
    return "".join(text)


def quoted(word):
    """Whether any part of the word is quoted or escaped."""
    return any(
        part.get("Type") in ("SglQuoted", "DblQuoted") or (part.get("Type") == "Lit" and "\\" in part["Value"])
        for part in word.get("Parts") or []
    )


findings = []


def walk(node, depth):
    if isinstance(node, list):
        for item in node:
            walk(item, depth)
        return
    if not isinstance(node, dict):
        return
    kind = node.get("Type")
    if kind == "CmdSubst":
        depth += 1
    elif kind == "CallExpr" and depth >= 2 and node.get("Args"):
        words = node["Args"]
        # `command` and `exec` run the next word as the command and ShellCheck's SC2312 exempts dirname behind
        # them too (`env` and `time` it flags itself); their options come first (`command -p dirname`).
        while len(words) > 1 and literal(words[0]) in ("command", "exec"):
            words = words[1:]
            while len(words) > 1 and (literal(words[0]) or "").startswith("-"):
                words = words[1:]
        word = words[0]
        if literal(word) in ("dirname", "basename"):
            findings.append((word["Pos"]["Line"], word["Pos"]["Col"]))
    elif node.get("Hdoc") and quoted(node["Word"]):
        # shfmt 3.14.1 parses the body of a partly quoted delimiter (`<<'E'OF`, `<<E"O"F`) as expanded text;
        # bash makes the body literal once any part of the delimiter is quoted.
        node = {key: value for key, value in node.items() if key != "Hdoc"}
    for value in node.values():
        walk(value, depth)


walk(json.load(sys.stdin), 0)
for line, _ in sorted(findings):
    print(f"{sys.argv[1]}:{line}: {MESSAGE}")
sys.exit(1 if findings else 0)
PY
)

status=0
for file in "$@"; do
    if ! tree=$("${shfmt}" -ln bash --to-json < "${file}"); then
        echo "masked-dirname-check: shfmt cannot parse ${file}; the list is refused" >&2
        exit 2
    fi
    python3 -c "${walk}" "${file}" <<< "${tree}" || {
        code=$?
        if ((code != 1)); then
            echo "masked-dirname-check: cannot walk the syntax tree of ${file} (python3 exit ${code}); the list is refused" >&2
            exit 2
        fi
        status=1
    }
done
exit "${status}"
