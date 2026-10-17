#!/usr/bin/env bash
# @file seat-args.sh
# @brief Compare a seated worker's live arguments with its rendered profile.
# @description
#   Reads profile text and process probes without sourcing, writing or signalling.
#   SEAT_ARGS_PS and SEAT_ARGS_LSOF replace the absolute probes in tests.
# @arg $1 string Comma-separated teams of the seated identity.
# @arg $2 string Identity in kind-profile-suffix form.
# @arg $3 string Agent type, claude-code or codex.
# @arg $4 path Project cwd used to select a Codex process.
# @exitcode 0 Profile pairs match.
# @exitcode 2 Arguments differ, or identity/profile is unknown.
# @exitcode 3 No launched process matches.
# @exitcode 4 A required probe binary is unavailable.
set -euo pipefail

teams=$1 identity=$2 agent_type=$3 project=$4
if [[ ! ${identity} =~ ^(claude|codex)-([a-z][a-z0-9_]*)-[a-z0-9]+(-[a-z0-9]+)*$ ]]; then
    printf 'seat %s args=unknown-identity\n' "${identity}"
    exit 2
fi
kind=${BASH_REMATCH[1]} profile=${BASH_REMATCH[2]}
if [[ ${kind}:${agent_type} != claude:claude-code && ${kind}:${agent_type} != codex:codex ]]; then
    printf 'seat %s args=unknown-identity\n' "${identity}"
    exit 2
fi
label="seat ${identity} profile=${profile} kind=${kind}"
key="MODEL_PROFILE_$(tr '[:lower:]' '[:upper:]' <<< "${profile}_${kind}")_ARGS"
expected="$(awk -v key="${key}" 'index($0, key "=\"") == 1 && substr($0, length($0), 1) == "\"" {
    print substr($0, length(key) + 3, length($0) - length(key) - 3); exit
}' "${HOME}/.agents/model-profiles.env" 2> /dev/null)" || expected=""
if [[ -z ${expected} ]]; then
    printf '%s args=unknown-profile\n' "${label}"
    exit 2
fi
[[ ${kind} != codex ]] || expected="--profile ${profile}"
read -r -a expected_args <<< "${expected}"
IFS=, read -r -a team_names <<< "${teams}"
ps_probe=${SEAT_ARGS_PS:-/bin/ps}
lsof_probe=${SEAT_ARGS_LSOF:-/usr/sbin/lsof}
[[ -n ${SEAT_ARGS_LSOF+x} || -x ${lsof_probe} ]] || lsof_probe=/usr/bin/lsof
if [[ ! -x ${ps_probe} ]] || { [[ ${kind} == codex ]] && [[ ! -x ${lsof_probe} ]]; }; then
    printf '%s args=unknown-probe\n' "${label}"
    exit 4
fi

# @description Skip a probe whose result cannot establish process visibility.
# @arg $1 string Diagnostic without probe output.
unknown_probe() {
    printf '%s args=unknown-probe\n' "${label}"
    printf 'seat-args: %s\n' "$1" >&2
    exit 4
}

probe_status=0
processes="$("${ps_probe}" -axo pid=,command= 2> /dev/null)" || probe_status=$?
if ((probe_status != 0)); then unknown_probe "ps failed (exit ${probe_status})"; fi
if ! grep -Eq '^[[:blank:]]*[0-9]+[[:blank:]]+[^[:blank:]]' <<< "${processes}"; then
    unknown_probe 'ps listed no process'
fi

# @description Find one literal adjacent pair in the current process tokens.
# @arg $1 string Flag.
# @arg $2 string Value.
has_pair() {
    local index
    for ((index = 1; index + 1 < ${#words[@]}; index++)); do
        [[ ${words[index]} != "$1" || ${words[index + 1]} != "$2" ]] || return 0
    done
    return 1
}

selected_pid="" cwd_diagnostic=""
while read -r pid process_args; do
    [[ ${pid} =~ ^[0-9]+$ ]] || continue
    if [[ -n ${selected_pid} ]] && ((10#${pid} >= 10#${selected_pid})); then continue; fi
    read -r -a words <<< "${process_args}"
    program=${words[0]:-}
    if [[ ${kind} == claude ]]; then
        [[ ${program##*/} == claude ]] || continue
        matched=false
        for team in "${team_names[@]}"; do
            if has_pair -n "${team}-${identity}"; then
                matched=true
                break
            fi
        done
        [[ ${matched} == true ]] || continue
    else
        if [[ ${program##*/} != codex ]] &&
            { [[ ${program##*/} != node ]] || [[ ${words[1]:-} != */codex ]]; }; then continue; fi
        probe_status=0
        cwd="$("${lsof_probe}" -a -p "${pid}" -d cwd -Fn 2> /dev/null | sed -n 's/^n//p')" || probe_status=$?
        if ((probe_status != 0)) || [[ -z ${cwd} ]]; then
            [[ -n ${cwd_diagnostic} ]] || cwd_diagnostic="lsof failed (exit ${probe_status})"
            continue
        fi
        [[ ${cwd} == "${project}" ]] || continue
    fi
    selected_pid=${pid}
    selected=("${words[@]}")
done <<< "${processes}"

if [[ -z ${selected_pid} ]]; then
    [[ -z ${cwd_diagnostic} ]] || unknown_probe "${cwd_diagnostic}"
    printf '%s process=none args=unlaunched\n' "${label}"
    exit 3
fi
words=("${selected[@]}")
ok=true
states=()
order=()
found=()
((${#expected_args[@]} % 2 == 0)) || ok=false
for ((arg_index = 1; arg_index < ${#words[@]}; arg_index++)); do
    for ((index = 0; index + 1 < ${#expected_args[@]}; index += 2)); do
        [[ ${words[arg_index]} == "${expected_args[index]}" ]] || continue
        [[ -n ${states[index]:-} ]] || order+=("${index}")
        if [[ ${states[index]:-} != differs && ${words[arg_index + 1]:-} == "${expected_args[index + 1]}" ]]; then
            states[index]=ok
        else
            states[index]=differs
        fi
    done
done
for ((index = 0; index + 1 < ${#expected_args[@]}; index += 2)); do
    if [[ -z ${states[index]:-} ]]; then
        states[index]=missing
        order+=("${index}")
    fi
    [[ ${states[index]} == ok ]] || ok=false
done
for ((arg_index = 0; arg_index < ${#order[@]}; arg_index++)); do
    index=${order[arg_index]}
    found+=("${expected_args[index]}:${states[index]}")
done
if [[ ${ok} == true ]]; then
    printf '%s process=%s args=ok\n' "${label}" "${selected_pid}"
    exit 0
fi
printf '%s process=%s args=differs expected=%s found=%s\n' \
    "${label}" "${selected_pid}" "${expected_args[*]}" "${found[*]-}"
exit 2
