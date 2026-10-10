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

    DOTFILES_DEBUG=1 bash -c 'source "$1"; install_mise' _ "${SCRIPT_PATH}"

    export PATH="${PATH}:${HOME}/.local/bin"
    [ -x "$(command -v mise)" ]
}

@test "[common] mise bootstrap resolves the newest cooled-down jdx/mise release" {
    # With a check available before mise runs, the tag comes from github_release_tag.
    function github_attestation_ready() { return 0; }
    function github_release_tag() {
        printf '%s\n' "$1" > "${BATS_TEST_TMPDIR}/repo"
        printf 'v2026.10.3\n'
    }
    function curl() {
        printf '%s\n' "$*" >> "${BATS_TEST_TMPDIR}/curl.log"
        return 7
    }
    function uname() { [ "$1" = -s ] && printf 'Linux\n' || printf 'x86_64\n'; }

    run _install_mise_binary

    [ "${status}" -ne 0 ]
    [ "$(cat "${BATS_TEST_TMPDIR}/repo")" = jdx/mise ]
    grep -q 'https://github.com/jdx/mise/releases/download/v2026.10.3/mise-v2026.10.3-linux-x64.tar.gz' "${BATS_TEST_TMPDIR}/curl.log"
    [ ! -e "${MISE_INSTALL_PATH}" ]
}

@test "[common] mise bootstrap without gpg or an authenticated gh takes the reviewed fallback release" {
    # Nothing runs before an independent check, so no lookup: the reviewed release installs.
    function mise_gpg_ready() { return 1; }
    function github_attestation_ready() { return 1; }
    function github_release_tag() {
        touch "${BATS_TEST_TMPDIR}/looked-up"
        printf 'v9.9.9\n'
    }
    function curl() {
        printf '%s\n' "$*" >> "${BATS_TEST_TMPDIR}/curl.log"
        return 7
    }
    function uname() { [ "$1" = -s ] && printf 'Linux\n' || printf 'x86_64\n'; }

    run _install_mise_binary

    [ "${status}" -ne 0 ]
    [ ! -e "${BATS_TEST_TMPDIR}/looked-up" ]
    [[ "${output}" == *"installing the reviewed mise ${MISE_FALLBACK_VERSION} (assets.mise.fallback)"* ]]
    grep -q "https://github.com/jdx/mise/releases/download/${MISE_FALLBACK_VERSION}/mise-${MISE_FALLBACK_VERSION}-linux-x64.tar.gz" "${BATS_TEST_TMPDIR}/curl.log"
    [ ! -e "${MISE_INSTALL_PATH}" ]
}

@test "[common] run_mise_install trusts the config and runs one bare install" {
    function mise() {
        echo "${npm_config_min_release_age:-unset} $*" >> "${BATS_TEST_TMPDIR}/mise_install_args.txt"
    }

    run_mise_install

    run cat "${BATS_TEST_TMPDIR}/mise_install_args.txt"
    [ "${status}" -eq 0 ]
    [ "${output}" = "unset trust --yes
unset install" ]
}

@test "[common] run_mise_install stops when config trust fails" {
    function mise() {
        if [ "$1" = trust ]; then
            return 41
        fi
        touch "${BATS_TEST_TMPDIR}/unexpected-install"
    }

    run run_mise_install

    [ "${status}" -eq 41 ]
    [ ! -e "${BATS_TEST_TMPDIR}/unexpected-install" ]
}

@test "[common] run_mise_install returns the full install failure" {
    function mise() {
        if [ "$1" = install ] && [ "$#" -eq 1 ]; then
            return 43
        fi
    }

    run run_mise_install

    [ "${status}" -eq 43 ]
}

@test "[common] blocc is only installed on Linux x64" {
    run grep -F '"github:shuntaka9576/blocc" = { version = "latest", os = ["linux/x64"] }' home/dot_mise/config.toml
    [ "${status}" -eq 0 ]
}

@test "[common] herdr is installed by mise on Linux and macOS" {
    run grep -E '^"github:ogulcancelik/herdr" = "[^"]+"$' home/dot_mise/config.toml
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
