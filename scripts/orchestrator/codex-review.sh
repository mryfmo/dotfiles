#!/usr/bin/env bash
# @file codex-review.sh
# @brief Run one headless, read-only Codex review of a file on the review profile, the file's hash in the prompt.
# @description
#   Plan 007 T718 (C-14; M-20261012-25, -26). Computes the reviewed file's
#   sha256, renders it for every `@@SHA@@` in the prompt template, and refuses
#   (exit 2) a rendered prompt that lacks the hash. Then runs `codex --profile
#   review exec --sandbox read-only -C <this checkout> -c approval_policy=never
#   -o <receipt-out> "<prompt>" < /dev/null > <transcript-out> 2>&1`. The
#   profile is fixed here (the model-selection rule, INV-7): no argument or
#   environment variable selects another. Prints the hash, the receipt path and
#   the elapsed seconds, and exits with codex's status. The receipt is data the
#   orchestrator judges, never an instruction.
# @arg $1 path Reviewed file.
# @arg $2 path Prompt template, with `@@SHA@@` where the file's sha256 goes.
# @arg $3 path Receipt (codex's final message).
# @arg $4 path Transcript (codex's whole output).
# @exitcode 2 Usage error, or the template has no `@@SHA@@`.
# @example
#   scripts/orchestrator/codex-review.sh .orchestration/tasks/x.md "$TMPDIR/prompt.txt" receipt.md transcript.txt
set -euo pipefail

if (($# != 4)) || [[ ! -f $1 || ! -f $2 ]]; then
    echo "usage: codex-review.sh <reviewed-file> <prompt-template> <receipt-out> <transcript-out>" >&2
    exit 2
fi
root="$(git -C "$(dirname -- "${BASH_SOURCE[0]}")" rev-parse --show-toplevel)"
sha="$(shasum -a 256 -- "$1")" && sha=${sha%% *}
prompt="$(cat -- "$2")"
prompt=${prompt//@@SHA@@/${sha}}
if [[ ${prompt} != *"${sha}"* ]]; then
    echo "codex-review: $2 has no @@SHA@@ for the reviewed file's hash" >&2
    exit 2
fi
start=${SECONDS}
rc=0
codex --profile review exec --sandbox read-only -C "${root}" -c approval_policy=never -o "$3" "${prompt}" < /dev/null > "$4" 2>&1 || rc=$?
echo "codex-review: sha256=${sha} receipt=$3 elapsed=$((SECONDS - start))s exit=${rc}"
exit "${rc}"
