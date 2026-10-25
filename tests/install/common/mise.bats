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

#
# @description Put fake curl, gh, gpg and gpgv first on PATH, so install_mise runs offline against a fixture
#   release of jdx/mise: a releases list whose newest stable release is FIXTURE_MISE_TAG, the artifact for this
#   platform, its SHASUMS256.asc and the release key. curl refuses any other URL as a 404 would, so a case never
#   reaches the network (unauthenticated api.github.com answers 403 once the runner's rate limit is spent). gh is
#   not authenticated, so the GPG signature is the check. Every call is logged under MISE_FAKE_DIR.
# @noargs
# @set MISE_FAKE_DIR path The fakes' directory: bin/ (on PATH), serve/ (the served files), curl.log and calls.log.
# @set MISE_FAKE_FINGERPRINT string The fingerprint fake gpg reports, MISE_GPG_FINGERPRINT.
# @set FIXTURE_MISE_TAG string The release tag the fixture serves as newest stable.
# @set FIXTURE_MISE_ARTIFACT string The served artifact's name for this platform.
# @set PATH string The fakes' bin/ first.
#
function serve_fixture_release() {
    export MISE_FAKE_DIR="${BATS_TEST_TMPDIR}/fake"
    export MISE_FAKE_FINGERPRINT="${MISE_GPG_FINGERPRINT}"
    FIXTURE_MISE_TAG="v2026.1.0"
    FIXTURE_MISE_ARTIFACT="$(mise_artifact "${FIXTURE_MISE_TAG}")"
    local artifact="${FIXTURE_MISE_ARTIFACT}" bin="${MISE_FAKE_DIR}/bin" serve="${MISE_FAKE_DIR}/serve" stage="${MISE_FAKE_DIR}/stage" sum
    mkdir -p "${bin}" "${serve}" "${stage}/mise/bin"

    cat > "${stage}/mise/bin/mise" << 'EOF'
#!/bin/sh
case "$1" in
--version) printf '2026.1.0 fixture\n' ;;
activate) printf 'export MISE_FIXTURE_ACTIVE=1\n' ;;
*) exit 1 ;;
esac
EOF
    chmod +x "${stage}/mise/bin/mise"
    tar -czf "${serve}/${artifact}" -C "${stage}" mise
    sum="$(shasum -a 256 "${serve}/${artifact}")"
    printf '%s  ./%s\n' "${sum%% *}" "${artifact}" > "${serve}/SHASUMS256.asc"
    printf 'fixture release key\n' > "${serve}/release-key.asc"
    # The API's layout, which github_release_tag parses: a newer prerelease that must be passed over.
    cat > "${serve}/releases.json" << 'EOF'
[
  {
    "tag_name": "v2026.2.0-rc.1",
    "draft": false,
    "prerelease": true,
    "published_at": "2026-01-02T00:00:00Z"
  },
  {
    "tag_name": "v2026.1.0",
    "draft": false,
    "prerelease": false,
    "published_at": "2026-01-01T00:00:00Z"
  }
]
EOF

    cat > "${bin}/curl" << 'EOF'
#!/usr/bin/env bash
out="" url=""
while [ "$#" -gt 0 ]; do
    case "$1" in
    -o) out="$2" && shift ;;
    -K) [ "$2" != - ] || cat > /dev/null && shift ;;
    -H) shift ;;
    https://*) url="$1" ;;
    esac
    shift
done
printf '%s\n' "${url}" >> "${MISE_FAKE_DIR}/curl.log"
case "${url}" in
"https://api.github.com/repos/jdx/mise/releases?per_page=30") file=releases.json ;;
"https://keys.openpgp.org/vks/v1/by-fingerprint/${MISE_FAKE_FINGERPRINT}") file=release-key.asc ;;
https://github.com/jdx/mise/releases/download/v2026.1.0/*) file="${url##*/}" ;;
*) file="" ;;
esac
if [ -z "${file}" ] || [ ! -f "${MISE_FAKE_DIR}/serve/${file}" ]; then
    printf 'curl: (22) The requested URL returned error: 404 (fake network: %s)\n' "${url}" >&2
    exit 22
fi
if [ -n "${out}" ]; then cp "${MISE_FAKE_DIR}/serve/${file}" "${out}"; else cat "${MISE_FAKE_DIR}/serve/${file}"; fi
EOF
    cat > "${bin}/gh" << 'EOF'
#!/bin/sh
printf 'gh %s\n' "$*" >> "${MISE_FAKE_DIR}/calls.log"
exit 1
EOF
    cat > "${bin}/gpg" << 'EOF'
#!/usr/bin/env bash
printf 'gpg %s\n' "$*" >> "${MISE_FAKE_DIR}/calls.log"
case " $* " in
*" --import-options show-only "*)
    printf 'pub:-:255:22:8B81C9D17413A06D:1700000000::::::\n'
    printf 'fpr:::::::::%s:\n' "${MISE_FAKE_FINGERPRINT}"
    ;;
*" --dearmor "*)
    while [ "$1" != --output ]; do shift; done
    : > "$2"
    ;;
*) exit 2 ;;
esac
EOF
    # The fixture SHASUMS256.asc holds the checksum lines themselves: gpgv prints them as the signed text.
    cat > "${bin}/gpgv" << 'EOF'
#!/usr/bin/env bash
printf 'gpgv %s\n' "$*" >> "${MISE_FAKE_DIR}/calls.log"
[ "$1" = --keyring ] && [ -f "$2" ] || exit 2
cat "${@: -1}"
EOF
    chmod +x "${bin}/curl" "${bin}/gh" "${bin}/gpg" "${bin}/gpgv"
    export PATH="${bin}:${PATH}"
}

@test "[common] mise installs the newest cooled-down release, verified, and activates it" {
    compgen -G "${TMPL_SCRIPT_GLOB}" > /dev/null
    serve_fixture_release

    run env DOTFILES_DEBUG=1 bash -c 'source "$1"; install_mise && printf "active=%s\n" "${MISE_FIXTURE_ACTIVE:-}"' _ "${SCRIPT_PATH}"

    [ "${status}" -eq 0 ]
    [[ "${output}" == *"active=1"* ]]
    run "${MISE_INSTALL_PATH}" --version
    [ "${output}" = "2026.1.0 fixture" ]
    grep -qx "https://github.com/jdx/mise/releases/download/${FIXTURE_MISE_TAG}/${FIXTURE_MISE_ARTIFACT}" "${MISE_FAKE_DIR}/curl.log"
    grep -q '^gpgv --keyring ' "${MISE_FAKE_DIR}/calls.log"
}

@test "[common] mise installs nothing when the artifact does not match the signed checksums" {
    serve_fixture_release
    printf 'tampered' >> "${MISE_FAKE_DIR}/serve/${FIXTURE_MISE_ARTIFACT}"

    run bash -c 'source "$1"; install_mise' _ "${SCRIPT_PATH}"

    [ "${status}" -ne 0 ]
    [[ "${output}" == *"Checksum mismatch for ${FIXTURE_MISE_ARTIFACT}"* ]]
    [ ! -e "${MISE_INSTALL_PATH}" ]
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

@test "[common] mise archive check names sha256sum when it cannot hash the archive" {
    local archive="${BATS_TEST_TMPDIR}/mise.tar.gz"
    local manifest="${BATS_TEST_TMPDIR}/SHASUMS256.txt"
    printf 'artifact' > "${archive}"
    printf '%s  ./mise.tar.gz\n' "$(printf artifact | shasum -a 256 | awk '{print $1}')" > "${manifest}"
    function sha256sum() { return 1; }

    run verify_mise_archive "${archive}" "${manifest}" "mise.tar.gz"

    [ "${status}" -ne 0 ]
    [ "${output}" = "sha256sum could not hash ${archive}" ]
}

@test "[common] mise release key check refuses when the clock cannot be read" {
    function curl() { : > "${4}"; }
    function gpg() {
        printf 'pub:-:255:22:ABCDEF:1:4102444800::::\n'
        printf 'fpr:::::::::%s:\n' "${MISE_GPG_FINGERPRINT}"
    }
    function date() { return 1; }
    function gpgv() { touch "${BATS_TEST_TMPDIR}/gpgv-ran"; }

    run verify_mise_shasums_signature "${BATS_TEST_TMPDIR}/SHASUMS256.asc" "${BATS_TEST_TMPDIR}"

    [ "${status}" -eq 1 ]
    grep -qF -- "date +%s failed; the mise release key expiry was not checked." <<< "${output}"
    [ ! -e "${BATS_TEST_TMPDIR}/gpgv-ran" ]
}

@test "[common] mise fallback refuses an artifact with no reviewed sha256" {
    function mise_gpg_ready() { return 1; }
    function github_attestation_ready() { return 1; }
    function mise_installed_version() { :; }
    function curl() { : > "${4}"; }
    function verify_mise_archive() { return 0; }
    function mise_fallback_sha256() { return 1; }
    function uname() { [ "$1" = -s ] && printf 'Linux\n' || printf 'x86_64\n'; }

    run _install_mise_binary

    [ "${status}" -eq 1 ]
    grep -qF -- "mise_fallback_sha256 has no reviewed sha256 for mise-${MISE_FALLBACK_VERSION}-linux-x64.tar.gz; nothing was installed." <<< "${output}"
    [ ! -e "${MISE_INSTALL_PATH}" ]
}

# install_mise moves its verified binary to MISE_INSTALL_PATH (install/common/mise.sh), so that path is its
# install set; setup points it into the case's HOME.
@test "[common] uninstall_mise removes the binary install_mise writes and nothing beside it" {
    touch "${MISE_INSTALL_PATH}" "${HOME}/.local/bin/must-survive"

    run uninstall_mise

    [ "${status}" -eq 0 ]
    [ ! -e "${MISE_INSTALL_PATH}" ]
    [ -e "${HOME}/.local/bin/must-survive" ]
}

@test "[common] the uninstall_mise check catches an uninstaller that removes another path" {
    local mutant="${BATS_TEST_TMPDIR}/mise.sh"
    sed 's|^    rm "${MISE_INSTALL_PATH}"$|    rm -f "${MISE_INSTALL_PATH}.old"|' "${SCRIPT_PATH}" > "${mutant}"
    if cmp -s "${SCRIPT_PATH}" "${mutant}"; then
        false
    fi
    touch "${MISE_INSTALL_PATH}"

    # The copy sits outside the checkout, so github-release.sh comes first, as the chezmoi script includes it.
    run bash -c 'source "$1"; source "$2"; uninstall_mise' _ ./scripts/lib/github-release.sh "${mutant}"

    # The mutant left the binary, which the check above refuses.
    [ "${status}" -eq 0 ]
    [ -e "${MISE_INSTALL_PATH}" ]
}
