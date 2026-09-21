#!/usr/bin/env bats
# shellcheck disable=SC2016 # SCRIPT_PATH is intentionally expanded outside bash -c strings.

readonly SCRIPT_PATH="./install/ubuntu/client/default_shell.sh"
readonly TMPL_PATH="./home/.chezmoiscripts/ubuntu/run_once_51-client-default-shell.sh.tmpl"

@test "[ubuntu-client] default shell changes to zsh only once" {
    local calls_path="${BATS_TEST_TMPDIR}/default-shell-calls.txt"

    run env CALLS_PATH="${calls_path}" USER="alice" bash -c '
        source "'"${SCRIPT_PATH}"'"
        command() {
            if [ "$1" = "-v" ] && [ "$2" = "zsh" ]; then
                printf "/usr/bin/zsh\n"
                return
            fi
            builtin command "$@"
        }
        getent() {
            if /usr/bin/grep -q "^chsh " "${CALLS_PATH}" 2> /dev/null; then
                printf "alice:x:1000:1000::/home/alice:/usr/bin/zsh\n"
            else
                printf "alice:x:1000:1000::/home/alice:/bin/bash\n"
            fi
        }
        grep() {
            return 1
        }
        sudo() {
            printf "%s\n" "$*" >> "${CALLS_PATH}"
            if [ "$1" = "tee" ]; then
                cat > /dev/null
            fi
        }

        main
        main
    '

    [ "${status}" -eq 0 ]
    [ "$(grep -c '^chsh -s /usr/bin/zsh alice$' "${calls_path}")" -eq 1 ]
    [ "$(grep -c '^tee -a /etc/shells$' "${calls_path}")" -eq 1 ]
    [[ "${output}" == *"Login shell is already /usr/bin/zsh."* ]]
}

@test "[ubuntu-client] default shell is a no-op when zsh is current" {
    run env USER="alice" bash -c '
        source "'"${SCRIPT_PATH}"'"
        command() {
            if [ "$1" = "-v" ] && [ "$2" = "zsh" ]; then
                printf "/usr/bin/zsh\n"
                return
            fi
            builtin command "$@"
        }
        getent() {
            printf "alice:x:1000:1000::/home/alice:/usr/bin/zsh\n"
        }
        sudo() {
            printf "unexpected sudo: %s\n" "$*"
            return 1
        }

        main
    '

    [ "${status}" -eq 0 ]
    [ "${output}" = "Login shell is already /usr/bin/zsh." ]
}

@test "[ubuntu-client] default shell runs only for Ubuntu clients" {
    grep -Fq 'include "../install/ubuntu/client/default_shell.sh"' "${TMPL_PATH}"
    grep -Fq 'if eq .system "client"' "${TMPL_PATH}"
}
