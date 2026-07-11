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
    cat > "${MISE_BIN}" <<'EOF'
#!/bin/sh
[ "$1" = exec ] && [ "$2" = --locked ] && [ "$3" = -- ] && [ "$4" = cargo ] || exit 98
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
