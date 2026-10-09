#!/usr/bin/env bats

readonly SCRIPT_PATH="./install/ubuntu/client/zed.sh"
readonly HELPER_PATH="./scripts/lib/github-release.sh"
readonly ZED_TEMPLATE="./home/.chezmoiscripts/ubuntu/run_after_05-client-install-zed.sh.tmpl"

# Shared fakes: the resolved release, a curl that builds a Zed tarball, and a gh whose
# behaviour GH_MODE picks (ok, unauthenticated, bad-attestation).
readonly ZED_FAKES='
    source "'"${HELPER_PATH}"'"
    source "'"${SCRIPT_PATH}"'"
    uname() { [ "$1" = -m ] && printf x86_64 || command uname "$1"; }
    github_release_tag() {
        [ -z "${API_FAIL:-}" ] || return 1
        printf "v1.22.0\n"
    }
    curl() {
        local output
        while [ "$#" -gt 0 ]; do
            if [ "$1" = -o ]; then output="$2"; shift 2; else shift; fi
        done
        printf "curl\n" >> "${HOME}/calls.log"
        mkdir -p "${HOME}/tar-src/zed.app/bin"
        printf "#!/bin/sh\necho Zed 1.22.0 deadbeef\n" > "${HOME}/tar-src/zed.app/bin/zed"
        chmod +x "${HOME}/tar-src/zed.app/bin/zed"
        tar -czf "${output}" -C "${HOME}/tar-src" zed.app
    }
    gh() {
        printf "gh %s\n" "$*" >> "${HOME}/calls.log"
        case "${GH_MODE:-ok}:$1 $2" in
            unauthenticated:"auth status") return 1 ;;
            *:"auth status") return 0 ;;
            bad-attestation:"release verify-asset") return 1 ;;
            *:"release verify-asset") return 0 ;;
        esac
        return 3
    }
'

function install_fake_zed() {
    local app_dir="${BATS_TEST_TMPDIR}/.local/share/zed.app"
    mkdir -p "${app_dir}/bin" "${BATS_TEST_TMPDIR}/.local/bin"
    printf '#!/bin/sh\necho "Zed %s deadbeef"\n' "$1" > "${app_dir}/bin/zed"
    chmod +x "${app_dir}/bin/zed"
    ln -sf "${app_dir}/bin/zed" "${BATS_TEST_TMPDIR}/.local/bin/zed"
}

@test "[ubuntu-client] zed_artifact selects the tarball for the current architecture" {
    run bash -c "${ZED_FAKES}"'
        zed_artifact
        uname() { [ "$1" = -m ] && printf aarch64 || command uname "$1"; }
        zed_artifact
    '
    [ "${status}" -eq 0 ]
    [ "${lines[0]}" = "zed-linux-x86_64.tar.gz" ]
    [ "${lines[1]}" = "zed-linux-aarch64.tar.gz" ]
}

@test "[ubuntu-client] zed_artifact rejects an unsupported architecture" {
    run bash -c "${ZED_FAKES}"'
        uname() { [ "$1" = -m ] && printf riscv64 || command uname "$1"; }
        zed_artifact
    '
    [ "${status}" -ne 0 ]
}

@test "[ubuntu-client] main installs the resolved release after its GitHub release attestation verifies" {
    run env HOME="${BATS_TEST_TMPDIR}" bash -c "${ZED_FAKES}"'
        main
        [ -L "${HOME}/.local/bin/zed" ]
        [ -x "${HOME}/.local/bin/zed" ]
        grep -Eq "^gh release verify-asset v1.22.0 .*/zed-linux-x86_64.tar.gz --repo zed-industries/zed$" "${HOME}/calls.log"
    '
    [ "${status}" -eq 0 ]
}

@test "[ubuntu-client] main is a no-op when the resolved release is already installed" {
    install_fake_zed 1.22.0

    run env HOME="${BATS_TEST_TMPDIR}" bash -c "${ZED_FAKES}"'
        main
        [ ! -e "${HOME}/calls.log" ]
    '
    [ "${status}" -eq 0 ]
}

@test "[ubuntu-client] main installs nothing without an authenticated gh and says how to retry" {
    run env HOME="${BATS_TEST_TMPDIR}" GH_MODE=unauthenticated bash -c "${ZED_FAKES}"'
        main
    '
    [ "${status}" -eq 0 ]
    [[ "${output}" == *"zed not installed: run make gh-auth, then make update"* ]]
    [ ! -e "${BATS_TEST_TMPDIR}/.local/bin/zed" ]
    ! grep -q '^curl' "${BATS_TEST_TMPDIR}/calls.log"
}

@test "[ubuntu-client] main keeps an installed zed it cannot update without an authenticated gh" {
    install_fake_zed 1.0.0

    run env HOME="${BATS_TEST_TMPDIR}" GH_MODE=unauthenticated bash -c "${ZED_FAKES}"'
        main
    '
    [ "${status}" -eq 0 ]
    [[ "${output}" == *"zed 1.0.0 stays (not updated to v1.22.0): run make gh-auth, then make update"* ]]
    "${BATS_TEST_TMPDIR}/.local/bin/zed" | grep -q 'Zed 1.0.0'
}

@test "[ubuntu-client] a failed attestation with an authenticated gh fails and installs nothing" {
    run env HOME="${BATS_TEST_TMPDIR}" GH_MODE=bad-attestation bash -c "${ZED_FAKES}"'
        main
    '
    [ "${status}" -ne 0 ]
    [[ "${output}" == *"failed its GitHub release attestation; nothing was installed"* ]]
    [ ! -e "${BATS_TEST_TMPDIR}/.local/bin/zed" ]
    [ ! -e "${BATS_TEST_TMPDIR}/.local/share/zed.app" ]
}

@test "[ubuntu-client] an unreachable release API never fails the apply, with or without an installed zed" {
    install_fake_zed 1.0.0
    run env HOME="${BATS_TEST_TMPDIR}" API_FAIL=1 bash -c "${ZED_FAKES}"'
        main
    '
    [ "${status}" -eq 0 ]
    [[ "${output}" == *"could not resolve a Zed release; Zed 1.0.0 stays"* ]]

    rm -rf "${BATS_TEST_TMPDIR}/.local"
    run env HOME="${BATS_TEST_TMPDIR}" API_FAIL=1 bash -c "${ZED_FAKES}"'
        main
    '
    [ "${status}" -eq 0 ]
    [[ "${output}" == *"zed not installed: could not resolve a zed-industries/zed release; the next make update retries"* ]]
    [ ! -e "${BATS_TEST_TMPDIR}/.local/bin/zed" ]
}

@test "[ubuntu-client] the zed script runs on every apply, after mise installs gh" {
    [ -f "${ZED_TEMPLATE}" ]
    [ ! -e ./home/.chezmoiscripts/ubuntu/run_once_52-client-install-zed.sh.tmpl ]
    [ -f ./home/.chezmoiscripts/common/run_once_after_02-install-mise.sh.tmpl ]
    grep -q '"github:cli/cli"' ./home/dot_mise/config.toml
    # The helper is included before the installer that calls it.
    [ "$(grep -n 'include' "${ZED_TEMPLATE}" | cut -d: -f1 | head -1)" -lt "$(grep -n 'zed.sh' "${ZED_TEMPLATE}" | cut -d: -f1)" ]
    grep -q 'include "../scripts/lib/github-release.sh"' "${ZED_TEMPLATE}"
}
