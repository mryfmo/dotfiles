#!/usr/bin/env bats

readonly SCRIPT_PATH="./install/common/sheldon.sh"

function setup() {
    ORIGINAL_HOME="${HOME}"
    HOME="$(mktemp -d)"
    export HOME
    source "${SCRIPT_PATH}"
}

function teardown() {
    run uninstall_sheldon
    rm -rf -- "${HOME}"
    HOME="${ORIGINAL_HOME}"
    export HOME

    # reset PATH
    PATH=$(getconf PATH)
    export PATH
}

@test "[ubuntu-server] sheldon" {
    mkdir -p "$(dirname "${MISE_BIN}")"
    cat > "${MISE_BIN}" << 'EOF'
#!/bin/sh
[ "$1" = exec ] && [ "$2" = -- ] && [ "$3" = cargo ] || exit 98
mkdir -p "${CARGO_INSTALL_ROOT}/bin"
printf '#!/bin/sh\n' > "${CARGO_INSTALL_ROOT}/bin/sheldon"
chmod +x "${CARGO_INSTALL_ROOT}/bin/sheldon"
EOF
    chmod +x "${MISE_BIN}"

    DOTFILES_DEBUG=1 bash "${SCRIPT_PATH}"

    export PATH="${PATH}:${HOME%/}/.local/bin"
    [ -x "$(command -v sheldon)" ]
}

@test "[ubuntu-server] failed locked cargo install leaves no Sheldon binary" {
    mkdir -p "$(dirname "${MISE_BIN}")"
    printf '#!/bin/sh\nprintf "registry checksum mismatch\\n" >&2\nexit 1\n' > "${MISE_BIN}"
    chmod +x "${MISE_BIN}"

    run install_sheldon

    [ "${status}" -ne 0 ]
    [ ! -e "${BIN_DIR}/sheldon" ]
}

# A mise whose `exec -- cargo install` writes a sheldon under CARGO_INSTALL_ROOT, as the first case's does.
function stub_mise_cargo_install() {
    mkdir -p "$(dirname "${MISE_BIN}")"
    printf '#!/bin/sh\nmkdir -p "${CARGO_INSTALL_ROOT}/bin"\nprintf "#!/bin/sh\\n" > "${CARGO_INSTALL_ROOT}/bin/sheldon"\nchmod +x "${CARGO_INSTALL_ROOT}/bin/sheldon"\n' > "${MISE_BIN}"
    chmod +x "${MISE_BIN}"
}

@test "[ubuntu-server] uninstall_sheldon removes the binary install_sheldon writes and nothing beside it" {
    stub_mise_cargo_install
    run install_sheldon
    [ "${status}" -eq 0 ]
    [ -x "${BIN_DIR}/sheldon" ]

    run uninstall_sheldon

    [ "${status}" -eq 0 ]
    [ ! -e "${BIN_DIR}/sheldon" ]
    [ -x "${MISE_BIN}" ]
}

@test "[ubuntu-server] the uninstall_sheldon check catches an uninstaller that removes another path" {
    local mutant="${BATS_TEST_TMPDIR}/sheldon.sh"
    sed 's|^    rm "${BIN_DIR}/sheldon"$|    rm -f "${BIN_DIR}/sheldon.old"|' "${SCRIPT_PATH}" > "${mutant}"
    if cmp -s "${SCRIPT_PATH}" "${mutant}"; then
        false
    fi
    stub_mise_cargo_install
    run install_sheldon
    [ "${status}" -eq 0 ]

    run bash -c 'source "$1"; uninstall_sheldon' _ "${mutant}"

    # The mutant left the binary, which the check above refuses.
    [ "${status}" -eq 0 ]
    [ -e "${BIN_DIR}/sheldon" ]
}
