#!/usr/bin/env bats

load helpers

setup() {
    REPO_ROOT="$(cd "${BATS_TEST_DIRNAME}/../.." && pwd)"
    managed_targets=(
        "${HOME}/.zshrc"
        "${HOME}/.config/ghostty/config"
        "${HOME}/.config/yazi/yazi.toml"
        "${HOME}/.local/bin/common/dev"
    )
}

@test "[macos-client] representative manifest" {
    assert_file_matches "${HOME}/.zshrc" "${REPO_ROOT}/home/dot_zshrc"
    assert_file_matches "${HOME}/.config/ghostty/config" "${REPO_ROOT}/home/dot_config/ghostty/config"
    assert_file_matches "${HOME}/.config/yazi/yazi.toml" "${REPO_ROOT}/home/dot_config/yazi/yazi.toml"
    assert_file_matches "${HOME}/.local/bin/common/dev" "${REPO_ROOT}/home/dot_local/bin/common/executable_dev"
    assert_mode "${HOME}/.local/bin/common/dev" 755
    assert_absent "${HOME}/.local/bin/server/cache.sh"
}

@test "[macos-client] second apply is idempotent and preserves an unmanaged sentinel" {
    assert_idempotent_apply macos "${managed_targets[@]}"
}

@test "[macos-client] manifest assertion rejects a removed required target" {
    target="${HOME}/.local/bin/common/dev"
    backup="${BATS_TEST_TMPDIR}/dev"
    mv "${target}" "${backup}"

    run assert_file_matches "${target}" "${REPO_ROOT}/home/dot_local/bin/common/executable_dev"
    [ "$status" -ne 0 ]

    mv "${backup}" "${target}"
    assert_file_matches "${target}" "${REPO_ROOT}/home/dot_local/bin/common/executable_dev"
}
