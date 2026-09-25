#!/usr/bin/env bats

readonly SCRIPT_TEMPLATE_PATH="./home/.chezmoiscripts/common/run_once_before_01-decrypt-private-key.sh.tmpl"

function render_decrypt_script() {
    local source_dir="$1"
    local output_path="$2"
    local extra_data="${3:-}"

    {
        printf '{{- define "script" -}}\n'
        cat "${SCRIPT_TEMPLATE_PATH}"
        printf '{{- end -}}{{ $c := dict "sourceDir" "%s" }}{{ $d := dict "chezmoi" $c %s }}{{ template "script" $d }}' \
            "${source_dir}" "${extra_data}"
    } | CI=true chezmoi execute-template > "${output_path}"
}

@test "[common] decrypt_age_private_key continues when passphrase decrypt fails" {
    local source_dir="${BATS_TEST_TMPDIR}/source"
    local home_dir="${BATS_TEST_TMPDIR}/home"
    local script_path="${BATS_TEST_TMPDIR}/decrypt-private-key.sh"

    mkdir -p "${source_dir}" "${home_dir}"
    touch "${source_dir}/.key.txt.age"
    render_decrypt_script "${source_dir}" "${script_path}"

    run env CI=false HOME="${home_dir}" bash -lc "
        source '${script_path}'
        function stdin_is_tty() { return 0; }
        function chezmoi() { return 1; }
        decrypt_age_private_key
    "

    [ "${status}" -eq 0 ]
    [[ "${output}" == *"Warning: Failed to decrypt age identity key. Skipping private encrypted dotfiles setup."* ]]
    [ ! -e "${home_dir}/.config/age/key.txt" ]
    [ ! -e "${home_dir}/.config/age/key.txt.tmp" ]
}

@test "[common] decrypt_age_private_key installs age identity through a temporary file" {
    local source_dir="${BATS_TEST_TMPDIR}/source"
    local home_dir="${BATS_TEST_TMPDIR}/home"
    local script_path="${BATS_TEST_TMPDIR}/decrypt-private-key.sh"

    mkdir -p "${source_dir}" "${home_dir}"
    touch "${source_dir}/.key.txt.age"
    render_decrypt_script "${source_dir}" "${script_path}"

    run env CI=false HOME="${home_dir}" bash -lc "
        source '${script_path}'
        function stdin_is_tty() { return 0; }
        function chezmoi() {
            local output_path=''
            while [ \"\$#\" -gt 0 ]; do
                if [ \"\$1\" = '--output' ]; then
                    output_path=\"\$2\"
                    break
                fi
                shift
            done
            printf 'AGE-SECRET-KEY-test\n' > \"\${output_path}\"
            return 0
        }
        decrypt_age_private_key
    "

    [ "${status}" -eq 0 ]
    [ -f "${home_dir}/.config/age/key.txt" ]
    [ ! -e "${home_dir}/.config/age/key.txt.tmp" ]
    [[ "$(< "${home_dir}/.config/age/key.txt")" == "AGE-SECRET-KEY-test" ]]
}

@test "[common] decrypt_age_private_key skips passphrase prompt without a tty" {
    local source_dir="${BATS_TEST_TMPDIR}/source"
    local home_dir="${BATS_TEST_TMPDIR}/home"
    local script_path="${BATS_TEST_TMPDIR}/decrypt-private-key.sh"

    mkdir -p "${source_dir}" "${home_dir}"
    touch "${source_dir}/.key.txt.age"
    render_decrypt_script "${source_dir}" "${script_path}"

    run env CI=false HOME="${home_dir}" bash -c "
        source '${script_path}'
        function chezmoi() { printf 'unexpected chezmoi call\n'; return 99; }
        decrypt_age_private_key
    "

    [ "${status}" -eq 0 ]
    [ -z "${output}" ]
    [ ! -e "${home_dir}/.config/age/key.txt" ]
}

@test "[common] usePrivate=false renders an empty gate with no decrypt function" {
    local source_dir="${BATS_TEST_TMPDIR}/source"
    local script_path="${BATS_TEST_TMPDIR}/decrypt-private-key.sh"

    mkdir -p "${source_dir}"
    render_decrypt_script "${source_dir}" "${script_path}" '"usePrivate" false'

    run bash -c "source '${script_path}'; declare -F decrypt_age_private_key"
    [ "${status}" -ne 0 ]
}

@test "[common] usePrivate=true or missing renders the decrypt function" {
    local source_dir="${BATS_TEST_TMPDIR}/source"

    for extra_data in '' '"usePrivate" true'; do
        local script_path="${BATS_TEST_TMPDIR}/decrypt-private-key-${RANDOM}.sh"

        mkdir -p "${source_dir}"
        render_decrypt_script "${source_dir}" "${script_path}" "${extra_data}"

        run bash -c "source '${script_path}'; declare -F decrypt_age_private_key"
        [ "${status}" -eq 0 ]
    done
}
