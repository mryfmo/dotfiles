#!/usr/bin/env bats

render_role_config() {
    local data="$1"
    shift

    {
        printf '{{- define "config" -}}\n'
        cat home/.chezmoi.yaml.tmpl
        printf '{{- end -}}{{ template "config" %s }}\n' "${data}"
    } | CI=true chezmoi execute-template "$@"
}

@test "[common] chezmoi config accepts Linux roles and defaults macOS to client" {
    local context='"chezmoi" (dict "homeDir" "/tmp/home" "workingTree" "/tmp/source"'

    run render_role_config "(dict \"email\" \"ci@example.invalid\" \"system\" \"client\" ${context} \"os\" \"linux\"))" --init
    [ "${status}" -eq 0 ]
    grep -qx '    system: "client"' <<< "${output}"

    run render_role_config "(dict \"email\" \"ci@example.invalid\" \"system\" \"server\" ${context} \"os\" \"linux\"))" --init
    [ "${status}" -eq 0 ]
    grep -qx '    system: "server"' <<< "${output}"

    run render_role_config "(dict \"email\" \"ci@example.invalid\" ${context} \"os\" \"darwin\"))" --init
    [ "${status}" -eq 0 ]
    grep -qx '    system: "client"' <<< "${output}"
}

@test "[common] chezmoi config rejects invalid roles before rendering YAML" {
    local context='"chezmoi" (dict "homeDir" "/tmp/home" "workingTree" "/tmp/source" "os" "linux")'
    local role

    run render_role_config "(dict \"email\" \"ci@example.invalid\" \"system\" \"persisted-invalid\" ${context})" --init
    [ "${status}" -ne 0 ]
    [[ "${output}" == *"client or server"* ]]
    [[ "${output}" != *"sourceDir:"* ]]

    for role in typo '' ' '; do
        run render_role_config "(dict \"email\" \"ci@example.invalid\" ${context})" \
            --init --promptString "System (client or server)=${role}"
        [ "${status}" -ne 0 ]
        [[ "${output}" == *"client or server"* ]]
        [[ "${output}" != *"sourceDir:"* ]]
    done
}

@test "[common] setup.sh keeps macOS sudo alive without Keychain password storage" {
    run grep -Eq "add-generic-password|find-generic-password|delete-generic-password|SUDO_ASKPASS|security -i" setup.sh
    [ "$status" -eq 1 ]

    grep -q "/usr/bin/sudo -v" setup.sh
    grep -q "/usr/bin/sudo -n true" setup.sh
}

@test "[common] setup.sh updates an existing chezmoi source before applying" {
    local update_count
    local update_line
    local apply_count
    local apply_line
    local update_block

    update_count="$(grep -c '"${chezmoi_cmd}" update' setup.sh)"
    apply_count="$(grep -c '"${chezmoi_cmd}" apply' setup.sh)"
    [ "${update_count}" -eq 1 ]
    [ "${apply_count}" -eq 1 ]

    update_line="$(grep -n '"${chezmoi_cmd}" update' setup.sh | head -n 1 | cut -d: -f1)"
    apply_line="$(grep -n '"${chezmoi_cmd}" apply' setup.sh | head -n 1 | cut -d: -f1)"

    [ -n "${update_line}" ]
    [ -n "${apply_line}" ]
    [ "${update_line}" -lt "${apply_line}" ]

    update_block="$(sed -n "${update_line},${apply_line}p" setup.sh)"
    grep -q -- '--apply=false' <<< "${update_block}"
    grep -q -- '--init' <<< "${update_block}"
}

@test "[common] setup.sh installs Homebrew non-interactively and continues from its prefix" {
    grep -q 'NONINTERACTIVE=1 /bin/bash -c' setup.sh
    grep -q 'https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh' setup.sh
    grep -q 'hash -r' setup.sh
    grep -q 'get_homebrew_prefix' setup.sh
    grep -q 'HOMEBREW_PREFIX_CANDIDATES:-/opt/homebrew /usr/local' setup.sh
    grep -q 'keepalive_sudo' setup.sh
    grep -q '"${brew_prefix}/bin/brew" shellenv' setup.sh

    run grep -Eq 'arch\).*brew shellenv|Invalid CPU arch' setup.sh
    [ "$status" -eq 1 ]
}

@test "[common] setup.sh fetches with curl first, falls back to wget, and fails without either" {
    local fetchers
    local expected
    local url="https://example.invalid/bootstrap"

    for fetchers in curl wget curl,wget; do
        expected="${fetchers%%,*}"
        run env FETCHERS="${fetchers}" URL_LOG="${BATS_TEST_TMPDIR}/${expected}.log" bash -c '
            source ./setup.sh
            command() {
                if [ "$1" = "-v" ] && { [ "$2" = "curl" ] || [ "$2" = "wget" ]; }; then
                    [[ ",${FETCHERS}," == *",$2,"* ]]
                    return
                fi
                builtin command "$@"
            }
            curl() {
                printf "curl %s\n" "${*: -1}" >> "${URL_LOG}"
                printf "body\n"
            }
            wget() {
                printf "wget %s\n" "${*: -1}" >> "${URL_LOG}"
                printf "body\n"
            }
            fetch_url "'"${url}"'"
        '

        [ "${status}" -eq 0 ]
        [ "${output}" = "body" ]
        grep -qx "${expected} ${url}" "${BATS_TEST_TMPDIR}/${expected}.log"
    done

    run env FETCHERS= bash -c '
        source ./setup.sh
        command() {
            if [ "$1" = "-v" ] && { [ "$2" = "curl" ] || [ "$2" = "wget" ]; }; then
                return 1
            fi
            builtin command "$@"
        }
        fetch_url "'"${url}"'"
    '

    [ "${status}" -ne 0 ]
    [ "${output}" = "Neither curl nor wget is available; cannot download ${url}." ]
}

@test "[common] setup.sh previews and applies without force" {
    grep -q '"${chezmoi_cmd}" status --path-style absolute --exclude=scripts' setup.sh
    grep -q '"${chezmoi_cmd}" diff' setup.sh
    grep -q '"${chezmoi_cmd}" apply ${no_tty_option}' setup.sh
    ! grep -q '"${chezmoi_cmd}" apply --force' setup.sh
}

@test "[common] setup.sh lets chezmoi choose sourceDir instead of cloning into cwd" {
    grep -q '"${chezmoi_cmd}" init "${DOTFILES_REPO_URL}"' setup.sh
    ! grep -q -- '--source' setup.sh
    ! grep -q -- 'cd "${HOME}"' setup.sh
}

@test "[common] setup.sh entrypoint still runs under bash -c snippets" {
    local tmpdir

    tmpdir="$(mktemp -d)"
    mkdir -p "${tmpdir}/bin" "${tmpdir}/home"

    cat > "${tmpdir}/bin/uname" <<'EOF'
#!/usr/bin/env bash
printf 'Darwin\n'
EOF
    chmod +x "${tmpdir}/bin/uname"

    cat > "${tmpdir}/bin/curl" <<'EOF'
#!/usr/bin/env bash
case "${*: -1}" in
    *Homebrew/install*)
        cat <<'BREW'
#!/usr/bin/env bash
mkdir -p "${HOME}/fakebrew/bin"
cat > "${HOME}/fakebrew/bin/brew" <<'BREW_BIN'
#!/usr/bin/env bash
case "${1:-}" in
    --prefix)
        printf '%s\n' "${HOME}/fakebrew"
        ;;
    shellenv)
        printf 'export PATH="%s/bin:${PATH}"\n' "${HOME}/fakebrew"
        ;;
esac
BREW_BIN
chmod +x "${HOME}/fakebrew/bin/brew"
BREW
        ;;
    *get.chezmoi.io*)
        cat <<'CHEZMOI_INSTALL'
#!/usr/bin/env bash
while [ "$#" -gt 0 ]; do
    case "$1" in
        -b)
            shift
            bin_dir="$1"
            ;;
    esac
    shift || true
done
mkdir -p "${bin_dir}"
cat > "${bin_dir}/chezmoi" <<'CHEZMOI_BIN'
#!/usr/bin/env bash
echo "chezmoi $*" >> "${HOME}/log"
case "${1:-}" in
    source-path)
        printf '%s\n' "${HOME}/source"
        mkdir -p "${HOME}/source"
        ;;
esac
CHEZMOI_BIN
chmod +x "${bin_dir}/chezmoi"
CHEZMOI_INSTALL
        ;;
esac
EOF
    chmod +x "${tmpdir}/bin/curl"

    run env HOME="${tmpdir}/home" PATH="${tmpdir}/bin:/usr/bin:/bin" CI=true \
        RUNNER_TEMP="${tmpdir}" \
        HOMEBREW_PREFIX_CANDIDATES="${tmpdir}/home/fakebrew" \
        bash -c "$(cat setup.sh)"

    [ "$status" -eq 0 ]
    grep -q 'chezmoi apply' "${tmpdir}/home/log"
}

@test "[common] wget-only Linux bootstrap previews safely and propagates failures" {
    local mode
    local tmpdir
    local before_hash
    local before_mode

    for mode in clean drift status-fail diff-fail apply-fail; do
        tmpdir="$(mktemp -d)"
        mkdir -p "${tmpdir}/bin" "${tmpdir}/home"
        printf 'managed-original\n' > "${tmpdir}/home/managed"
        printf 'sentinel-original\n' > "${tmpdir}/home/sentinel"
        chmod 640 "${tmpdir}/home/managed" "${tmpdir}/home/sentinel"
        before_hash="$(cksum "${tmpdir}/home/managed" "${tmpdir}/home/sentinel")"
        before_mode="$(stat -c '%a' "${tmpdir}/home/managed" "${tmpdir}/home/sentinel" 2> /dev/null || stat -f '%Lp' "${tmpdir}/home/managed" "${tmpdir}/home/sentinel")"

        for command_path in sh find rm mkdir chmod; do
            ln -s "/bin/${command_path}" "${tmpdir}/bin/${command_path}"
        done

        cat > "${tmpdir}/bin/uname" <<'EOF'
#!/bin/bash
printf 'Linux\n'
EOF
        cat > "${tmpdir}/bin/wget" <<'EOF'
#!/bin/bash
printf 'wget %s\n' "${*: -1}" >> "${HOME}/fetch.log"
cat <<'INSTALLER'
#!/bin/sh
while [ "$#" -gt 0 ]; do
    if [ "$1" = "-b" ]; then
        shift
        bin_dir="$1"
    fi
    shift
done
mkdir -p "${bin_dir}"
cat > "${bin_dir}/chezmoi" <<'CHEZMOI'
#!/bin/bash
printf 'chezmoi %s\n' "$*" >> "${HOME}/log"
case "${1:-}" in
    source-path)
        mkdir -p "${HOME}/source"
        printf '%s\n' "${HOME}/source"
        ;;
    status)
        if [ "${CHEZMOI_TEST_MODE}" = "status-fail" ]; then
            exit 1
        elif [ "${CHEZMOI_TEST_MODE}" = "drift" ]; then
            printf 'M  %s/managed\n' "${HOME}"
        fi
        ;;
    diff)
        printf 'preview\n'
        [ "${CHEZMOI_TEST_MODE}" != "diff-fail" ]
        ;;
    apply)
        [ "${CHEZMOI_TEST_MODE}" != "apply-fail" ] || exit 1
        printf 'managed-applied\n' > "${HOME}/managed"
        ;;
esac
CHEZMOI
chmod +x "${bin_dir}/chezmoi"
INSTALLER
EOF
        chmod +x "${tmpdir}/bin/uname" "${tmpdir}/bin/wget"

        run env HOME="${tmpdir}/home" PATH="${tmpdir}/bin" CI=true \
            RUNNER_TEMP="${tmpdir}" CHEZMOI_TEST_MODE="${mode}" \
            /bin/bash -c "$(cat setup.sh)"

        grep -qx 'wget https://get.chezmoi.io' "${tmpdir}/home/fetch.log"
        grep -q '^chezmoi init ' "${tmpdir}/home/log"
        grep -q '^chezmoi status --path-style absolute --exclude=scripts$' "${tmpdir}/home/log"

        if [ "${mode}" = "clean" ]; then
            [ "${status}" -eq 0 ]
            grep -q '^chezmoi diff$' "${tmpdir}/home/log"
            grep -q '^chezmoi apply --no-tty$' "${tmpdir}/home/log"
        else
            [ "${status}" -ne 0 ]
        fi

        if [ "${mode}" = "drift" ]; then
            grep -q '^chezmoi diff$' "${tmpdir}/home/log"
            ! grep -q '^chezmoi apply ' "${tmpdir}/home/log"
        fi

        if [ "${mode}" != "clean" ]; then
            [ "$(cksum "${tmpdir}/home/managed" "${tmpdir}/home/sentinel")" = "${before_hash}" ]
            [ "$(stat -c '%a' "${tmpdir}/home/managed" "${tmpdir}/home/sentinel" 2> /dev/null || stat -f '%Lp' "${tmpdir}/home/managed" "${tmpdir}/home/sentinel")" = "${before_mode}" ]
        fi
    done
}

@test "[common] setup.sh resolves Homebrew fallback prefixes behaviorally" {
    local tmpdir
    local prefix

    tmpdir="$(mktemp -d)"
    mkdir -p "${tmpdir}/bin" "${tmpdir}/arm/bin" "${tmpdir}/intel/bin"

    cat > "${tmpdir}/bin/curl" <<'EOF'
#!/usr/bin/env bash
printf ':\n'
EOF
    chmod +x "${tmpdir}/bin/curl"

    for prefix in "${tmpdir}/arm" "${tmpdir}/intel"; do
        cat > "${prefix}/bin/brew" <<EOF
#!/usr/bin/env bash
case "\${1:-}" in
    --prefix)
        printf '%s\\n' '${prefix}'
        ;;
    shellenv)
        printf 'export HOMEBREW_TEST_PREFIX=%q\\n' '${prefix}'
        ;;
    *)
        exit 1
        ;;
esac
EOF
        chmod +x "${prefix}/bin/brew"
    done

    # shellcheck source=/dev/null
    source ./setup.sh

    for prefix in "${tmpdir}/arm" "${tmpdir}/intel"; do
        HOMEBREW_TEST_PREFIX=""
        PATH="${tmpdir}/bin:/usr/bin:/bin"
        CI=true
        HOMEBREW_PREFIX_CANDIDATES="${prefix}"
        initialize_os_macos
        [ "${HOMEBREW_TEST_PREFIX}" = "${prefix}" ]
    done
}
