#!/bin/bash -p
# @file pre-send.sh
# @brief Check a task text's final bytes before each send, with every machine check CI or the regime applies to it.
# @description
#   The entrypoint of scripts/orchestrator/pre_send.py (T133 pre-send-check a03; D-024-51, D-024-56). `bash -p` ignores
#   an inherited BASH_ENV and exported functions. It resolves uv through the pinned mise, or the probed absolute
#   install, never a PATH search, then re-executes unconditionally under `env -i` with only PATH (uv's directory and
#   /usr/bin:/bin), HOME, TMPDIR and LANG, and runs the pinned 3.15 interpreter isolated, through uv with no config, no
#   project and offline PyYAML. It forwards only the exit status: the Python prints every label and the digest, and a
#   failure to start it prints a fixed label. No text of the task, the checker or a tool reaches either stream.
# @arg $1 string The task text to check.
# @exitcode 0 Every check passes.
# @exitcode 1 A check refuses, the argument is missing or unreadable, or the interpreter cannot start.
set -u
uv="$(/usr/bin/env -i PATH=/usr/bin:/bin HOME="${HOME}" "${HOME}/.local/bin/mise" which uv 2> /dev/null)"
[[ -x ${uv} && -z ${uv%%/*} ]] || uv="${HOME}/.local/share/mise/installs/uv/0.13.1/uv-aarch64-apple-darwin/uv"
if [[ ! -x ${uv} ]]; then
    echo "startup: refused"
    exit 1
fi
root="$(cd -- "$(dirname -- "$0")/../.." && pwd)"
py="${HOME}/.local/share/mise/installs/python/3.15.0/bin/python3"
# shellcheck disable=SC2016 # the single-quoted program expands its own positional arguments
exec /usr/bin/env -i PATH="$(dirname -- "${uv}"):/usr/bin:/bin" HOME="${HOME}" TMPDIR="${TMPDIR:-/tmp}" LANG=C.UTF-8 \
    /bin/bash -p -c '"$1" run --no-config --no-project --offline --python "$2" --with pyyaml python -I "$3" "${@:4}" 2> /dev/null
rc=$?
if ((rc > 1)); then
    echo "interpreter: refused"
    rc=1
fi
exit "${rc}"' pre-send "${uv}" "${py}" "${root}/scripts/orchestrator/pre_send.py" "${root}" "$@"
