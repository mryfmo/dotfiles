#!/usr/bin/env bats

readonly SCRIPT_PATH="./install/common/tpm.sh"

@test "[common] uninstall_tpm calls rm for TPM_DIR" {
    local args_path="${BATS_TEST_TMPDIR}/uninstall_tpm_args.txt"

    run env ARGS_PATH="${args_path}" DOTFILES_DEBUG= bash -c '
        source "'"${SCRIPT_PATH}"'"

        rm() {
            echo "$*" > "${ARGS_PATH}"
        }

        uninstall_tpm
    '
    [ "${status}" -eq 0 ]

    run cat "${args_path}"
    [ "${status}" -eq 0 ]
    [ "${output}" = "-rfv ${HOME%/}/.tmux/plugins/tpm" ]
}

@test "[common] is_tmux_mem_cpu_load_installed checks command -v" {
    run env DOTFILES_DEBUG= bash -c '
        source "'"${SCRIPT_PATH}"'"

        command() {
            if [ "$1" = "-v" ] && [ "$2" = "tmux-mem-cpu-load" ]; then
                return 0
            fi
            builtin command "$@"
        }

        is_tmux_mem_cpu_load_installed
    '

    [ "${status}" -eq 0 ]
}

@test "[common] install_tmux_mem_cpu_load returns early when binary is already installed" {
    run env DOTFILES_DEBUG= bash -c '
        source "'"${SCRIPT_PATH}"'"

        is_tmux_mem_cpu_load_installed() {
            return 0
        }

        git() {
            echo "unexpected git call" >&2
            return 1
        }

        cmake() {
            echo "unexpected cmake call" >&2
            return 1
        }

        make() {
            echo "unexpected make call" >&2
            return 1
        }

        install_tmux_mem_cpu_load
    '

    [ "${status}" -eq 0 ]
    [ -z "${output}" ]
}

@test "[common] install_tpm configures tmux global plugin path before installing plugins" {
    local calls_path="${BATS_TEST_TMPDIR}/install_tpm_calls.txt"
    local home_path="${BATS_TEST_TMPDIR}/home"

    run env CALLS_PATH="${calls_path}" HOME="${home_path}" DOTFILES_DEBUG=1 bash -c '
        source "'"${SCRIPT_PATH}"'"

        tmux() {
            printf "tmux %s\n" "$*" >> "${CALLS_PATH}"
        }

        clone_tpm() {
            printf "clone_tpm %s\n" "$*" >> "${CALLS_PATH}"
        }

        install_tpm_plugins() {
            printf "install_tpm_plugins %s\n" "$*" >> "${CALLS_PATH}"
        }

        install_tpm
    '

    [ "${status}" -eq 0 ]
    run cat "${calls_path}"
    [ "${status}" -eq 0 ]
    [ "${lines[0]}" = "tmux start-server ; set-environment -g TMUX_PLUGIN_MANAGER_PATH ${home_path%/}/.tmux/plugins" ]
    [ "${lines[1]}" = "clone_tpm ${home_path%/}/.tmux/plugins/tpm" ]
    [ "${lines[2]}" = "install_tpm_plugins ${home_path%/}/.tmux/plugins/tpm" ]
}

@test "[common] client tmux config sets TPM path before using it" {
    run bash -c '
        python3 - <<'"'"'PY'"'"'
from pathlib import Path

content = Path("home/dot_tmux.conf.d/system/client.conf").read_text()
set_index = content.index("set-environment -g TMUX_PLUGIN_MANAGER_PATH")
status_index = content.index("$TMUX_PLUGIN_MANAGER_PATH/tmux-powerline")
run_index = content.index(".tmux/plugins/tpm/tpm")
assert set_index < status_index < run_index
PY
    '

    [ "${status}" -eq 0 ]
}

@test "[common] uninstall_tmux_mem_cpu_load calls rm for binary path" {
    local args_path="${BATS_TEST_TMPDIR}/uninstall_tmux_mem_cpu_load_args.txt"

    run env ARGS_PATH="${args_path}" DOTFILES_DEBUG= bash -c '
        source "'"${SCRIPT_PATH}"'"

        rm() {
            echo "$*" > "${ARGS_PATH}"
        }

        uninstall_tmux_mem_cpu_load
    '
    [ "${status}" -eq 0 ]

    run cat "${args_path}"
    [ "${status}" -eq 0 ]
    [ "${output}" = "-fv ${HOME%/}/.local/bin/tmux-mem-cpu-load" ]
}
