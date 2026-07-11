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

create_chezmoi_release_fixture() {
    local fixture_dir="$1" os="$2" arch="$3" artifact checksum
    fixture_dir="${fixture_dir}/release"
    mkdir -p "${fixture_dir}/payload"
    artifact="chezmoi_${CHEZMOI_VERSION}_${os}_${arch}.tar.gz"
    cp "${fixture_dir}/chezmoi" "${fixture_dir}/payload/chezmoi"
    tar -czf "${fixture_dir}/${artifact}" -C "${fixture_dir}/payload" chezmoi
    checksum="$(sha256_file "${fixture_dir}/${artifact}")"
    printf '%s  %s\n' "${checksum}" "${artifact}" > "${fixture_dir}/chezmoi_${CHEZMOI_VERSION}_checksums.txt"
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
    grep -q 'NONINTERACTIVE=1 /bin/bash' setup.sh
    grep -q 'https://raw.githubusercontent.com/Homebrew/install/${HOMEBREW_INSTALL_COMMIT}/install.sh' setup.sh
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

@test "[common] setup.sh does not execute partial installer output from a failed fetch" {
    local marker="${BATS_TEST_TMPDIR}/partial-installer-ran"

    run env MARKER="${marker}" HOME="${BATS_TEST_TMPDIR}" bash -c '
        source ./setup.sh
        get_os_type() { printf Linux; }
        uname() { printf x86_64; }
        fetch_file() {
            printf '\''#!/bin/sh\nprintf ran > "%s"\n'\'' "${MARKER}" > "$2"
            return 23
        }
        run_chezmoi
    '

    [ "${status}" -eq 23 ]
    [ ! -e "${marker}" ]
}

@test "[common] checksum verification fails closed for corrupt or missing digests" {
    local payload="${BATS_TEST_TMPDIR}/payload"
    local marker="${BATS_TEST_TMPDIR}/executed"
    printf '#!/bin/sh\ntouch %q\n' "${marker}" > "${payload}"

    run bash -c 'source ./setup.sh; verify_sha256 "$1" "$2" && sh "$1"' _ "${payload}" "$(printf corrupt | shasum -a 256 | awk '{print $1}')"
    [ "${status}" -ne 0 ]
    [ ! -e "${marker}" ]

    run bash -c 'source ./setup.sh; verify_sha256 "$1" "" && sh "$1"' _ "${payload}"
    [ "${status}" -ne 0 ]
    [ ! -e "${marker}" ]
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
    mkdir -p "${tmpdir}/bin" "${tmpdir}/home/fakebrew/bin" "${tmpdir}/release"
    source ./setup.sh

    cat > "${tmpdir}/release/chezmoi" <<'EOF'
#!/usr/bin/env bash
echo "chezmoi $*" >> "${HOME}/log"
case "${1:-}" in
    source-path)
        mkdir -p "${HOME}/source"
        printf '%s\n' "${HOME}/source"
        ;;
esac
EOF
    chmod +x "${tmpdir}/release/chezmoi"
    create_chezmoi_release_fixture "${tmpdir}" darwin arm64

    cat > "${tmpdir}/home/fakebrew/bin/brew" <<'EOF'
#!/usr/bin/env bash
case "${1:-}" in
    --prefix) printf '%s\n' "${HOME}/fakebrew" ;;
    shellenv) printf 'export PATH="%s/bin:${PATH}"\n' "${HOME}/fakebrew" ;;
esac
EOF
    chmod +x "${tmpdir}/home/fakebrew/bin/brew"

    cat > "${tmpdir}/bin/uname" <<'EOF'
#!/usr/bin/env bash
if [ "${1:-}" = -m ]; then printf 'arm64\n'; else printf 'Darwin\n'; fi
EOF
    chmod +x "${tmpdir}/bin/uname"

    cat > "${tmpdir}/bin/curl" <<'EOF'
#!/usr/bin/env bash
while [ "$#" -gt 0 ]; do
    if [ "$1" = -o ]; then output="$2"; shift 2; else url="$1"; shift; fi
done
cp "${CHEZMOI_FIXTURE_DIR}/${url##*/}" "${output}"
EOF
    chmod +x "${tmpdir}/bin/curl"

    run env HOME="${tmpdir}/home" PATH="${tmpdir}/home/fakebrew/bin:${tmpdir}/bin:/usr/bin:/bin" CI=true \
        RUNNER_TEMP="${tmpdir}" \
        CHEZMOI_FIXTURE_DIR="${tmpdir}/release" \
        HOMEBREW_PREFIX_CANDIDATES="${tmpdir}/home/fakebrew" \
        bash -c "$(cat setup.sh)"

    [ "$status" -eq 0 ]
    grep -q 'chezmoi apply' "${tmpdir}/home/log"
}

@test "[common] wget-only Linux bootstrap previews safely and propagates failures" {
    local mode
    local tmpdir
    local before_managed_hash
    local before_mode
    local before_sentinel_hash

    source ./setup.sh
    for mode in clean target-only drift status-fail diff-fail apply-fail; do
        tmpdir="$(mktemp -d)"
        mkdir -p "${tmpdir}/bin" "${tmpdir}/home" "${tmpdir}/release"
        printf 'managed-original\n' > "${tmpdir}/home/managed"
        printf 'sentinel-original\n' > "${tmpdir}/home/sentinel"
        chmod 640 "${tmpdir}/home/managed" "${tmpdir}/home/sentinel"
        before_managed_hash="$(cksum "${tmpdir}/home/managed")"
        before_sentinel_hash="$(cksum "${tmpdir}/home/sentinel")"
        before_mode="$(stat -c '%a' "${tmpdir}/home/managed" "${tmpdir}/home/sentinel" 2> /dev/null || stat -f '%Lp' "${tmpdir}/home/managed" "${tmpdir}/home/sentinel")"

        cat > "${tmpdir}/release/chezmoi" <<'EOF'
#!/bin/bash
printf 'chezmoi %s\n' "$*" >> "${HOME}/log"
case "${1:-}" in
    init)
        mkdir -p "${HOME}/.config/chezmoi"
        printf 'init changed config\n' > "${HOME}/.config/chezmoi/chezmoi.yaml"
        ;;
    update)
        mkdir -p "${HOME}/source"
        printf 'update changed source\n' > "${HOME}/source/update-state"
        ;;
    source-path)
        mkdir -p "${HOME}/source"
        printf '%s\n' "${HOME}/source"
        ;;
    status)
        if [ "${CHEZMOI_TEST_MODE}" = "status-fail" ]; then
            exit 1
        elif [ "${CHEZMOI_TEST_MODE}" = "drift" ]; then
            printf 'M  %s/managed\n' "${HOME}"
        elif [ "${CHEZMOI_TEST_MODE}" = "target-only" ]; then
            printf ' M %s/managed\n' "${HOME}"
        fi
        ;;
    diff)
        printf 'preview\n'
        [ "${CHEZMOI_TEST_MODE}" != "diff-fail" ]
        ;;
    apply)
        printf 'managed-applied\n' > "${HOME}/managed"
        [ "${CHEZMOI_TEST_MODE}" != "apply-fail" ] || exit 1
        ;;
esac
EOF
        chmod +x "${tmpdir}/release/chezmoi"
        create_chezmoi_release_fixture "${tmpdir}" linux amd64

        for command_path in sh find rm mkdir chmod cat cp tar install mv mktemp awk shasum; do
            ln -s "$(command -v "${command_path}")" "${tmpdir}/bin/${command_path}"
        done

        cat > "${tmpdir}/bin/uname" <<'EOF'
#!/bin/bash
if [ "${1:-}" = -m ]; then printf 'x86_64\n'; else printf 'Linux\n'; fi
EOF
        cat > "${tmpdir}/bin/wget" <<'EOF'
#!/bin/bash
while [ "$#" -gt 0 ]; do
    if [ "$1" = -qO ]; then output="$2"; shift 2; else url="$1"; shift; fi
done
printf 'wget %s\n' "${url}" >> "${HOME}/fetch.log"
cp "${CHEZMOI_FIXTURE_DIR}/${url##*/}" "${output}"
EOF
        chmod +x "${tmpdir}/bin/uname" "${tmpdir}/bin/wget"

        run env HOME="${tmpdir}/home" PATH="${tmpdir}/bin" CI=true \
            RUNNER_TEMP="${tmpdir}" CHEZMOI_TEST_MODE="${mode}" \
            CHEZMOI_FIXTURE_DIR="${tmpdir}/release" \
            /bin/bash -c "$(cat setup.sh)"

        grep -qx "wget https://github.com/twpayne/chezmoi/releases/download/v${CHEZMOI_VERSION}/chezmoi_${CHEZMOI_VERSION}_linux_amd64.tar.gz" "${tmpdir}/home/fetch.log"
        grep -qx "wget https://github.com/twpayne/chezmoi/releases/download/v${CHEZMOI_VERSION}/chezmoi_${CHEZMOI_VERSION}_checksums.txt" "${tmpdir}/home/fetch.log"
        grep -q '^chezmoi init ' "${tmpdir}/home/log"
        grep -q '^chezmoi update ' "${tmpdir}/home/log"
        grep -q '^chezmoi status --path-style absolute --exclude=scripts$' "${tmpdir}/home/log"
        grep -qx 'init changed config' "${tmpdir}/home/.config/chezmoi/chezmoi.yaml"
        grep -qx 'update changed source' "${tmpdir}/home/source/update-state"

        if [ "${mode}" = "clean" ] || [ "${mode}" = "target-only" ]; then
            [ "${status}" -eq 0 ]
            grep -q '^chezmoi diff$' "${tmpdir}/home/log"
            grep -q '^chezmoi apply --no-tty$' "${tmpdir}/home/log"
        else
            [ "${status}" -ne 0 ]
        fi

        if [ "${mode}" = "drift" ]; then
            grep -q '^chezmoi diff$' "${tmpdir}/home/log"
        fi

        if [ "${mode}" = "drift" ] || [ "${mode}" = "status-fail" ] || [ "${mode}" = "diff-fail" ]; then
            ! grep -q '^chezmoi apply ' "${tmpdir}/home/log"
            [ "$(cksum "${tmpdir}/home/managed")" = "${before_managed_hash}" ]
            [ "$(stat -c '%a' "${tmpdir}/home/managed" "${tmpdir}/home/sentinel" 2> /dev/null || stat -f '%Lp' "${tmpdir}/home/managed" "${tmpdir}/home/sentinel")" = "${before_mode}" ]
        fi

        [ "$(cksum "${tmpdir}/home/sentinel")" = "${before_sentinel_hash}" ]

        if [ "${mode}" = "apply-fail" ]; then
            grep -qx 'managed-applied' "${tmpdir}/home/managed"
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
