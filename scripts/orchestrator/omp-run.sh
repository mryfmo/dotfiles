#!/usr/bin/env bash
# @file omp-run.sh
# @brief Run one non-interactive omp turn in a seat role and fail closed on any missing input.
# @description
#   Plan 025 W6a (U8). Composes, for `--role <role>`,
#   `omp --profile <role> --config ~/.agents/omp/policies/<role>.yml -e <dir>...
#   --no-session --max-time <s> [--model <provider/id>] --mode <text|json> -p <prompt>`
#   (omp 18.11.3 `omp --help`: `--mode` is "text (default), json, rpc, or rpc-ui",
#   `--config` loads an overlay, `-e` loads an extension, `-p` is print mode and
#   `--max-time` stops the session). The profile name equals the role, so the seat's
#   own `modelRoles.default` applies unless `--model` overrides it. The role's policy
#   overlay owns the approval mode (`home/dot_agents/omp/policies/README.md`), so
#   `--approval-mode` is never passed. Extensions default to the bridge
#   `~/.local/lib/omp-extensions/pi-claude-bridge` and the SIWC
#   `~/.agents/omp/extensions/openai-siwc`; `--ext` replaces that list.
#   Every input is checked before omp starts: an unknown role, an absent or empty
#   prompt file, an absent overlay, extension directory or cwd is exit 2 with the
#   path. omp's stderr is held and replayed after the run; a `Failed to load
#   extension <path>: <error>` line in it (`src/extensibility/extensions/load-errors.ts:5-13`)
#   is exit 2 as well, because a seat whose bridge or policy did not load must never
#   be read as that seat (U1 report F5). Otherwise omp's exit status is returned.
#   `--mode text` passes omp's own print-mode text through and `--mode json` its
#   event stream, one JSON object per line, unchanged. HOME is the caller's: seats
#   run as the operator.
# @option --role <role> orchestrator, worker or audit (required).
# @option --prompt-file <file> The prompt, passed whole after `-p` (required).
# @option --cwd <dir> Directory omp runs in (default: the current directory).
# @option --model <provider/id> Override the profile's default model.
# @option --mode <text|json> omp output mode (default: text).
# @option --max-time <s> omp's `--max-time` (default: 600).
# @option --ext <dir> Extension directory, repeatable; replaces the two defaults.
# @stdout omp's output, unchanged.
# @stderr omp's stderr, replayed after the run, then this script's own refusal.
# @exitcode 2 A refusal: usage, omp absent from PATH, unknown role, missing prompt file, overlay, extension directory or cwd, or an extension failed to load.
# @exitcode * omp's own status otherwise.
# @example
#   omp-run.sh --role audit --prompt-file review.md --cwd /path/to/worktree --mode json --max-time 900
set -euo pipefail

usage='usage: omp-run.sh --role <orchestrator|worker|audit> --prompt-file <file> [--cwd <dir>] [--model <provider/id>] [--mode <text|json>] [--max-time <s>] [--ext <dir>]...'
refuse() {
    echo "omp-run: $*" >&2
    exit 2
}

role='' prompt_file='' cwd=. model='' mode=text max_time=600
exts=()
while (($#)); do
    (($# >= 2)) || refuse "${usage}"
    case $1 in
    --role) role=$2 ;;
    --prompt-file) prompt_file=$2 ;;
    --cwd) cwd=$2 ;;
    --model) model=$2 ;;
    --mode) mode=$2 ;;
    --max-time) max_time=$2 ;;
    --ext) exts+=("$2") ;;
    *) refuse "${usage}" ;;
    esac
    shift 2
done
[[ -n ${role} && -n ${prompt_file} ]] || refuse "${usage}"
case ${role} in
orchestrator | worker | audit) ;;
*) refuse "unknown role '${role}'; roles are orchestrator, worker and audit" ;;
esac
[[ ${mode} == text || ${mode} == json ]] || refuse "mode must be text or json, not '${mode}'"
# omp and the extension paths are made absolute before the cd, so a relative PATH entry cannot pick <cwd>/bin/omp
# from a PR head and omp loads the directories that were checked.
omp_bin=$(command -v omp) || refuse 'omp not found on PATH'
[[ ${omp_bin} == /* ]] || omp_bin=${PWD}/${omp_bin}
[[ -s ${prompt_file} ]] || refuse "prompt file missing or empty: ${prompt_file}"
policy=${HOME}/.agents/omp/policies/${role}.yml
[[ -f ${policy} ]] || refuse "policy overlay not found: ${policy}"
((${#exts[@]})) || exts=("${HOME}/.local/lib/omp-extensions/pi-claude-bridge" "${HOME}/.agents/omp/extensions/openai-siwc")
argv=(--profile "${role}" --config "${policy}")
for ext in "${exts[@]}"; do
    [[ -d ${ext} ]] || refuse "extension directory not found: ${ext}"
    [[ ${ext} == /* ]] || ext=${PWD}/${ext}
    argv+=(-e "${ext}")
done
[[ -d ${cwd} ]] || refuse "cwd not found: ${cwd}"
argv+=(--no-session --max-time "${max_time}")
[[ -z ${model} ]] || argv+=(--model "${model}")
argv+=(--mode "${mode}" -p "$(< "${prompt_file}")")

cd "${cwd}"
# stdout streams to the caller through fd 3 while stderr is held, so a load failure can be judged after the run.
exec 3>&1
status=0
held=$("${omp_bin}" "${argv[@]}" 2>&1 1>&3) || status=$?
exec 3>&-
[[ -z ${held} ]] || printf '%s\n' "${held}" >&2
if [[ ${held} == *'Failed to load extension'* ]]; then
    line=${held##*Failed to load extension }
    refuse "an extension failed to load: ${line%%$'\n'*} (omp exited ${status})"
fi
exit "${status}"
