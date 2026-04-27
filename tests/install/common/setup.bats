#!/usr/bin/env bats

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
