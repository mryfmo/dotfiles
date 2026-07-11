#!/usr/bin/env bats

readonly SCRIPT_PATH="./install/common/mise.sh"
readonly TMPL_SCRIPT_GLOB="./home/.chezmoiscripts/common/run_once_after_*-install-mise.sh.tmpl"

function setup() {
    export HOME="${BATS_TEST_TMPDIR}/home"
    mkdir -p "${HOME}/.local/bin"

    source "${SCRIPT_PATH}"
}

function teardown() {
    if [ -e "${MISE_INSTALL_PATH}" ]; then
        uninstall_mise
    fi

    # reset PATH
    PATH=$(getconf PATH)
    export PATH
}

@test "[common] mise" {
    compgen -G "${TMPL_SCRIPT_GLOB}" > /dev/null

    DOTFILES_DEBUG=1 bash "${SCRIPT_PATH}"

    export PATH="${PATH}:${HOME}/.local/bin"
    [ -x "$(command -v mise)" ]
}

@test "[common] run_mise_install uses hardcoded min-release-age days" {
    printf "min-release-age=99\n" > "${HOME}/.npmrc"

    function mise() {
        echo "$*" > "${BATS_TEST_TMPDIR}/mise_install_args.txt"
    }

    run_mise_install

    run cat "${BATS_TEST_TMPDIR}/mise_install_args.txt"
    [ "${status}" -eq 0 ]
    [ "${output}" = "install --locked --before ${DEFAULT_NPM_MIN_RELEASE_AGE_DAYS}d" ]
}

@test "[common] blocc is only installed on Linux x64" {
    run grep -F '"github:shuntaka9576/blocc" = { version = "0.6.0", os = ["linux/x64"] }' home/dot_mise/config.toml
    [ "${status}" -eq 0 ]
}

@test "[common] herdr is installed by mise on Linux and macOS" {
    run grep -F '"github:ogulcancelik/herdr" = "0.7.1"' home/dot_mise/config.toml
    [ "${status}" -eq 0 ]
}

@test "[common] mise rejects another artifact checksum" {
    local archive="${BATS_TEST_TMPDIR}/mise.tar.gz"
    local manifest="${BATS_TEST_TMPDIR}/SHASUMS256.txt"
    printf 'artifact' > "${archive}"
    printf '%s  ./other.tar.gz\n' "$(printf other | shasum -a 256 | awk '{print $1}')" > "${manifest}"

    run verify_mise_archive "${archive}" "${manifest}" "other.tar.gz"
    [ "${status}" -ne 0 ]
}
