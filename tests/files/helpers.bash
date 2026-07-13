assert_file_matches() {
    [ -f "$1" ] && cmp -s "$1" "$2"
}

assert_mode() {
    [ "$(stat -c '%a' "$1" 2> /dev/null || stat -f '%Lp' "$1")" = "$2" ]
}

assert_absent() {
    [ ! -e "$1" ] && [ ! -L "$1" ]
}

assert_idempotent_apply() {
    local sentinel="${HOME}/.phase5-$1-sentinel"
    local -a chezmoi_command=(
        "${FILES_TEST_CHEZMOI:?FILES_TEST_CHEZMOI is required}"
        --source "${FILES_TEST_SOURCE:?FILES_TEST_SOURCE is required}"
        --destination "${HOME}"
        --config "${FILES_TEST_CONFIG:?FILES_TEST_CONFIG is required}"
    )
    shift
    printf 'keep\n' > "${sentinel}"

    run "${chezmoi_command[@]}" diff "$@"
    assert_chezmoi_result "initial diff"
    run "${chezmoi_command[@]}" apply --exclude=scripts "$@"
    assert_chezmoi_result "second apply" false
    run "${chezmoi_command[@]}" diff "$@"
    assert_chezmoi_result "final diff"
    [ "$(cat "${sentinel}")" = keep ]

    rm "${sentinel}"
}

assert_chezmoi_result() {
    local operation="$1"
    local require_empty="${2:-true}"

    if [ "$status" -ne 0 ] || { [ "$require_empty" = true ] && [ -n "$output" ]; }; then
        printf 'chezmoi %s failed (status %s):\n%s\n' "$operation" "$status" "$output" >&3
        return 1
    fi
}
