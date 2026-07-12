#!/usr/bin/env bats

# bats file_tags=common

setup() {
    REPO_ROOT="$(cd "${BATS_TEST_DIRNAME}/../.." && pwd)"
}

assert_file_matches() {
    [ -f "$1" ] && cmp -s "$1" "$2"
}

assert_link_target() {
    [ -L "$1" ] && [ "$(readlink "$1")" = "$2" ]
}

assert_mode() {
    [ "$(stat -c '%a' "$1" 2> /dev/null || stat -f '%Lp' "$1")" = "$2" ]
}

assert_absent() {
    [ ! -e "$1" ] && [ ! -L "$1" ]
}

# bats test_tags=ubuntu:client
@test "[ubuntu-client] representative manifest" {
    assert_link_target "${HOME}/.bashrc" ".bash/client/bashrc"
    assert_file_matches "${HOME}/.bashrc" "${REPO_ROOT}/home/dot_bash/client/bashrc"
    assert_file_matches "${HOME}/.config/ghostty/config" "${REPO_ROOT}/home/dot_config/ghostty/config"
    assert_file_matches "${HOME}/.config/yazi/yazi.toml" "${REPO_ROOT}/home/dot_config/yazi/yazi.toml"
    assert_file_matches "${HOME}/.local/bin/common/dev" "${REPO_ROOT}/home/dot_local/bin/common/executable_dev"
    assert_mode "${HOME}/.local/bin/common/dev" 755
    assert_absent "${HOME}/.local/bin/server/cache.sh"
}

# bats test_tags=ubuntu:client
@test "[ubuntu-client] second apply is idempotent and preserves an unmanaged sentinel" {
    managed_targets=(
        "${HOME}/.bashrc"
        "${HOME}/.bash/client/bashrc"
        "${HOME}/.config/ghostty/config"
        "${HOME}/.config/yazi/yazi.toml"
        "${HOME}/.local/bin/common/dev"
    )
    assert_idempotent_apply ubuntu-client "${managed_targets[@]}"
}

# bats test_tags=ubuntu:client
@test "[ubuntu-client] manifest assertion rejects a removed required target" {
    target="${HOME}/.local/bin/common/dev"
    backup="${BATS_TEST_TMPDIR}/dev"
    mv "${target}" "${backup}"

    run assert_file_matches "${target}" "${REPO_ROOT}/home/dot_local/bin/common/executable_dev"
    [ "$status" -ne 0 ]

    mv "${backup}" "${target}"
    assert_file_matches "${target}" "${REPO_ROOT}/home/dot_local/bin/common/executable_dev"
}

# bats test_tags=ubuntu:server
@test "[ubuntu-server] representative manifest" {
    assert_link_target "${HOME}/.bashrc" ".bash/server/bashrc"
    assert_file_matches "${HOME}/.bashrc" "${REPO_ROOT}/home/dot_bash/server/bashrc"
    assert_file_matches "${HOME}/.local/bin/server/cache.sh" "${REPO_ROOT}/home/dot_local/bin/server/cache.sh"
    assert_absent "${HOME}/.bash/client/bashrc"
    assert_absent "${HOME}/.config/powerlevel10k/p10k.zsh"
}

# bats test_tags=ubuntu:server
@test "[ubuntu-server] second apply is idempotent and preserves an unmanaged sentinel" {
    managed_targets=(
        "${HOME}/.bashrc"
        "${HOME}/.bash/server/bashrc"
        "${HOME}/.local/bin/server/cache.sh"
    )
    assert_idempotent_apply ubuntu-server "${managed_targets[@]}"
}

# bats test_tags=ubuntu:server
@test "[ubuntu-server] manifest assertion rejects a removed required target" {
    target="${HOME}/.local/bin/server/cache.sh"
    backup="${BATS_TEST_TMPDIR}/cache.sh"
    mv "${target}" "${backup}"

    run assert_file_matches "${target}" "${REPO_ROOT}/home/dot_local/bin/server/cache.sh"
    [ "$status" -ne 0 ]

    mv "${backup}" "${target}"
    assert_file_matches "${target}" "${REPO_ROOT}/home/dot_local/bin/server/cache.sh"
}

assert_idempotent_apply() {
    sentinel="${HOME}/.phase5-$1-sentinel"
    shift
    printf 'keep\n' > "${sentinel}"

    run chezmoi diff "$@"
    [ "$status" -eq 0 ]
    [ -z "$output" ]
    run chezmoi apply --exclude=scripts "$@"
    [ "$status" -eq 0 ]
    run chezmoi diff "$@"
    [ "$status" -eq 0 ]
    [ -z "$output" ]
    [ "$(cat "${sentinel}")" = keep ]

    rm "${sentinel}"
}
